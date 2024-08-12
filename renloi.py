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
    parser.addArgument("input_file", help="Input file path")
    parser.addArgument(
        "-output_file",
        help="Output file path (default: input file name without extension)",
        default=None,
    )
    parser.addArgument("-run", action="store_true", help="Run the compiled code")
    parser.addArgument(
        "-keep", action="store_true", help="Keep the source file after compilation"
    )
    parser.addArgument(
        "-debug", action="store_true", help="Show g++ compilation warnings/errors"
    )
    args = parser.parseArgs()
    if args.outputFile is None:
        args.outputFile = os.path.splitext(os.path.basename(args.inputFile))[0]
    processFile(args.inputFile, args.outputFile, args.keep, args.run, args.debug)


if Name == "__main__":
    main()
