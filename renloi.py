import argparse
import subprocess
import os
import re
import process


def processFile(inputFile, outputFile, keep, run, debug):
    with open(inputFile, "r", encoding="utf-8") as f:
        inputCode = f.read()
    outputCode = process.addNamespaceStd(inputCode)
    outputCode = process.replaceSyntax(outputCode)
    with open(outputFile + ".cpp", "w", encoding="utf-8") as f:
        f.write(outputCode)
    compileCommand = [
        "g++",
        "-static-libgcc",
        "-static-libstdc++",
        "-static",
        outputFile + ".cpp",
        "-O3",
        "-o",
        os.path.splitext(outputFile)[0],
    ]
    if "include <net.h>" in inputCode:
        compileCommand.append("-lcurl")
    if "include <bint.h>" in inputCode:
        compileCommand.append("-lgmp")
    if os.name == "nt":
        compileCommand.append("-IC:\\renloi\\include")
    else:
        compileCommand.append("-I/renloi/include")
    if debug:
        print(compileCommand)
        subprocess.run(compileCommand)
    else:
        subprocess.run(compileCommand, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if run:
        subprocess.run([os.path.splitext(outputFile)[0]])
    if not keep:
        os.remove(outputFile + ".cpp")


def main():
    parser = argparse.ArgumentParser(
        description="Renloi Programming Language Compiler."
    )
    parser.add_argument("input", help="Input file path")
    parser.add_argument("--output", help="Output file path (default: input file name without extension)",default=None,)
    parser.add_argument("-run", action="store_true", help="Run the compiled code")
    parser.add_argument("--keep", action="store_true", help="Keep the source file after compilation")
    parser.add_argument("--debug", action="store_true", help="Show g++ compilation warnings/errors")
    args = parser.parse_args()
    if args.output is None:
        args.output = os.path.splitext(os.path.basename(args.input))[0]
    processFile(args.input, args.output, args.keep, args.run, args.debug)


if __name__ == "__main__":
    main()
