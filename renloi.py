import argparse
import subprocess
import os
import re
import process

def process_file(input_file, output_file, keep, run, debug):
    with open(input_file, 'r', encoding='utf-8') as f:
        input_code = f.read()

    output_code = process.add_namespace_std(input_code)
    output_code = process.replace_syntax(input_code)

    with open(output_file + ".c", 'w', encoding='utf-8') as f:
        f.write(output_code)
    compile_command = [
        'g++',
        output_file + ".c",
        '-IC:\\renloi\\include',  # Double-backslashes for Windows paths
        '-O3',
        '-o',
        os.path.splitext(output_file)[0]  # Using os.path.splitext to get the base name without extension
    ]
    # Run gcc command
    if debug:
        print(compile_command)
        subprocess.run(compile_command)
    else:
        subprocess.run(compile_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if run:
        subprocess.run([os.path.splitext(output_file)[0]])

    # Remove the source file if not specified to keep
    if not keep:
        os.remove(output_file + ".c")

def main():
    parser = argparse.ArgumentParser(description='Renloi Programming Language Compiler.')
    parser.add_argument('input_file', help='Input file path')
    parser.add_argument('-output_file', help='Output file path', default="output")
    parser.add_argument('-run', action='store_true', help='Run the compiled code')
    parser.add_argument('-keep', action='store_true', help='Keep the source file after compilation')
    parser.add_argument('-debug', action='store_true', help='Keep the source file after compilation')

    args = parser.parse_args()

    process_file(args.input_file, args.output_file, args.keep, args.run, args.debug)

if __name__ == '__main__':
    main()
