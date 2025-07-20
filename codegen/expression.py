from llvmlite import ir

class ExpressionCodegen:
    def Return(self, node):
        return self.builder.ret(self.codegen(node.expr))

    def ExpressionStatement(self, node):
        return self.codegen(node.expr)

    def Num(self, node):
        return ir.Constant(ir.IntType(32), node.value)

    def FloatNum(self, node):
        return ir.Constant(ir.FloatType(), float(node.value))

    def String(self, node):
        value = node.value
        if len(value) >= 2 and value[0] == '"' and value[-1] == '"':
            value = value[1:-1]
        return self.createStringConstant(value)

    def Char(self, node):
        return ir.Constant(ir.IntType(8), ord(node.value))

    def BinOp(self, node):
        customRes = self.tryCustomBinop(node)
        if customRes is not None:
            return customRes
        
        if node.op in self.binary:
            intOp, floatOp, resName = self.binary[node.op]
            return self.genArith(node, intOp, floatOp, resName)
        elif node.op in self.comparison:
            intCmp, floatCmp, resName = self.comparison[node.op]
            return self.genCompare(node, intCmp, floatCmp, resName)
        raise ValueError("Unknown binary operator " + node.op)

    def Var(self, node):
        info = self.funcSymtab.get(node.name)
        if info:
            return self.builder.load(info["addr"], name=node.name)
        raise NameError("Undefined variable: " + node.name)

    def handleFunctionArgs(self, func, args):
        llvmArgs = []
        for arg in args:
            llvmArgs.append(self.codegen(arg))
        return self.builder.call(func, llvmArgs)
        
    def FunctionCall(self, node):
        if node.callee.__class__.__name__ == "Var":
            if node.callee.name == "print":
                return self.PrintCall(node)
            func = self.module.get_global(node.callee.name)
            if not func:
                raise NameError("Unknown function: " + node.callee.name)
            return self.handleFunctionArgs(func, node.args)
        elif node.callee.__class__.__name__ == "MemberAccess":
            if node.callee.objectExpr.__class__.__name__ == "Var":
                moduleName = node.callee.objectExpr.name
                functionName = node.callee.memberName

                args = [self.codegen(arg) for arg in node.args]
                res = self.callExternal(moduleName, functionName, args)
                if res is not None:
                    return res

                constRes = self.callExternal(moduleName, functionName, [], constant=True)
                if constRes is not None:
                    return constRes
            obj = self.funcSymtab[node.callee.objectExpr.name]["addr"]
            methodName = node.callee.memberName
            info = self.funcSymtab.get(node.callee.objectExpr.name)
            if not info:
                raise NameError("Undefined variable: " + node.callee.objectExpr.name)
            className = info["datatypeName"]
            qualifiedName = f"{className}_{methodName}"
            llvmArgs = [obj]
            for arg in node.args:
                llvmArgs.append(self.codegen(arg))
            func = self.module.get_global(qualifiedName)
            if not func:
                raise NameError("Method " + qualifiedName + " not defined.")
            return self.builder.call(func, llvmArgs)
        else:
            raise SyntaxError("Invalid function call callee.")

    def formatPrintValue(self, val, i, args, fmtParts, llvmArgs):
        printed, spec, llvmVal = self.preparePrintArg(val)
        if printed:
            if i < len(args) - 1:
                spaceStr = self.createStringConstant(" ")
                self.builder.call(self.printFunc, [spaceStr])
            return True

        fmtParts.append(spec)
        llvmArgs.append(llvmVal)
        return False

    def PrintCall(self, node):
        fmtParts = []
        llvmArgs = []
        
        for i, arg in enumerate(node.args):
            val = self.codegen(arg)
            self.formatPrintValue(val, i, node.args, fmtParts, llvmArgs)
        
        if fmtParts:
            fmtStr = " ".join(fmtParts) + "\n"
            fmtVal = self.createStringConstant(fmtStr)
            return self.builder.call(self.printFunc, [fmtVal] + llvmArgs)
        else:
            nlStr = self.createStringConstant("\n" if node.args else "\n")
            return self.builder.call(self.printFunc, [nlStr], name="print_newline")

    def MemberAccess(self, node):
        objInfo = self.funcSymtab[node.objectExpr.name]
        idx = self.getMemberIndex(objInfo["datatypeName"], node.memberName)
        ptr = self.structFieldPointer(objInfo["addr"], idx, name="memberPointer")
        return self.builder.load(ptr, name=node.memberName)

    def Assign(self, node):
        if node.left.__class__.__name__ == "Var":
            info = self.funcSymtab.get(node.left.name)
            if not info:
                raise NameError("Variable '" + node.left.name + "' not declared.")
            val = self.codegen(node.right)
            val = self.convertValue(val, val.type, info["datatypeName"])
            self.builder.store(val, info["addr"])
            return val
        elif node.left.__class__.__name__ == "MemberAccess":
            return self.MemberAssignment(node.left, self.codegen(node.right))
        elif node.left.__class__.__name__ == "ArrayAccess":
            return self.ArrayElementAssignment(node.left, self.codegen(node.right))
        raise SyntaxError("Invalid left-hand side for assignment")

    def MemberAssignment(self, memberNode, val):
        objInfo = self.funcSymtab[memberNode.objectExpr.name]
        idx = self.getMemberIndex(objInfo["datatypeName"], memberNode.memberName)
        ptr = self.structFieldPointer(objInfo["addr"], idx, name="memberPointer")

        self.builder.store(val, ptr)
        return val

    def ArrayElementAssignment(self, arrayAccessNode, val):
        arrayInfo = self.funcSymtab.get(arrayAccessNode.array.name)
        if not arrayInfo:
            raise NameError(f"Undefined array: {arrayAccessNode.array.name}")

        idx = self.codegen(arrayAccessNode.index)
        self.checkArrayBounds(arrayInfo, idx)
        elemPointer = self.elementPointer(arrayInfo, idx)
        self.builder.store(val, elemPointer)
        return val

    def ArrayAccess(self, node):
        arrayInfo = self.funcSymtab.get(node.array.name)
        if not arrayInfo:
            raise NameError(f"Undefined array: {node.array.name}")

        idx = self.codegen(node.index)
        self.checkArrayBounds(arrayInfo, idx)
        elemPointer = self.elementPointer(arrayInfo, idx)
        return self.builder.load(elemPointer, name="elementValue")

    def NewExpr(self, node):
        if node.className not in self.classStructTypes:
            raise ValueError("Unknown class: " + node.className)
        structType = self.classStructTypes[node.className]
        obj = self.builder.alloca(structType, name="objtmp")
        return obj
        
    def ArrayLiteral(self, node):
        if not node.elements:
            return ir.Constant(ir.ArrayType(ir.IntType(32), 0), [])

        firstElem = self.codegen(node.elements[0])
        elemType = firstElem.type

        arrayType = ir.ArrayType(elemType, len(node.elements))
        array = self.builder.alloca(arrayType, name="array_literal")

        for i, elem in enumerate(node.elements):
            elemValue = self.codegen(elem)
            if elemValue.type != elemType:
                if elemType == ir.FloatType() and elemValue.type == ir.IntType(32):
                    elemValue = self.builder.sitofp(elemValue, ir.FloatType())

            elemPointer = self.elementPointer(array, ir.Constant(ir.IntType(32), i), name=f"element_pointer_{i}")
            self.builder.store(elemValue, elemPointer)

        return array 

    # ------------------------------------------------------------------
    # Helper utilities for custom datatype operator overloading
    # ------------------------------------------------------------------
    def inferDatatypeName(self, astNode):
        cls = astNode.__class__.__name__
        if cls == "Var":
            info = self.funcSymtab.get(astNode.name)
            if info:
                return info.get("datatypeName")
        elif cls == "Num":
            return "int"
        elif cls == "FloatNum":
            return "float"
        elif cls == "String":
            return "string"
        elif cls == "Char":
            return "char"
        return None

    def tryCustomBinop(self, node):
        funcName = getattr(self, "opFuncMap", {}).get(node.op)
        if not funcName:
            return None

        leftVal = self.codegen(node.left)
        rightVal = self.codegen(node.right)

        leftType = self.inferDatatypeName(node.left)
        rightType = self.inferDatatypeName(node.right)

        chosenType = None
        for candidate in (leftType, rightType):
            if candidate in self.externalFunctions and funcName in self.externalFunctions[candidate]:
                chosenType = candidate
                break

        if not chosenType:
            return None

        if leftType != chosenType:
            leftVal = self.convertValue(leftVal, leftVal.type, chosenType)
        if rightType != chosenType:
            rightVal = self.convertValue(rightVal, rightVal.type, chosenType)

        llvmFunc = self.externalFunctions[chosenType][funcName]
        return self.builder.call(llvmFunc, [leftVal, rightVal], name=f"{chosenType}_{funcName}_result") 