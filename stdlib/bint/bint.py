from llvmlite import ir
from stdlib.module import Module

module = Module(
    name="bint",
    datatype="bint",
    typeRepresentation=ir.PointerType(ir.IntType(8)),
    libraries=["-lgmp", "-lgmpxx"]
)

for op in ["add", "sub", "mul", "div", "mod", "and", "or", "xor"]:
    module.functions[op] = ("bint", ["bint", "bint"])

module.functions["not"] = ("bint", ["bint"])

for cmp in ["eq", "ne", "lt", "le", "gt", "ge"]:
    module.functions[cmp] = ("bool", ["bint", "bint"])

module.functions["lshift"] = ("bint", ["bint", "int"])
module.functions["rshift"] = ("bint", ["bint", "int"])
module.functions["print"] = ("void", ["bint"])

module.addConversion("int", "bint", "fromInt")

module.functions["fromInt"] = ("bint", ["int"])
module.mapping["fromInt"] = "bint_from_int"
module.functions["fromString"] = ("bint", ["string"])
module.mapping["fromString"] = "bint_from_string"

def codegen_literal(codegen, node):
    if hasattr(node, '__class__') and node.__class__.__name__ in ("Num", "HEX_NUMBER"):
        value = node.value
        str_val = str(value)
        str_ptr = codegen.createStringConstant(str_val)
        bint_funcs = codegen.externalFunctions.get("bint", {})
        from_string_func = bint_funcs.get("fromString")
        if from_string_func is None:
            raise RuntimeError("bint_from_string function not registered")
        return codegen.builder.call(from_string_func, [str_ptr], name="bintFromString")
    raise NotImplementedError("bint.codegen_literal only supports Num/HEX_NUMBER nodes")

module = module.export()
