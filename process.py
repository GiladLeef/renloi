import re

def replace_syntax(input_code):
    output_code = input_code.replace("int main()", "int main(int argc, char *argv[])")
    output_code = output_code.replace("File.write", "File::write")
    output_code = output_code.replace("File.read", "File::read")
    output_code = output_code.replace("#include <stdint.h>", "#include <cstdint.h>")
    output_code = output_code.replace("int64", "int64_t")
    output_code = output_code.replace("uint64", "uint64_t")
    output_code = re.sub(r'string (\w+)', r'char \1[]', output_code)
    output_code = re.sub(r'char (\w+)\[\] = read\(([^)]+)\);', r'char *\1 = read(\2);', output_code)

    return output_code

def foreach_syntax(input_code):
    pattern = re.compile(r'foreach\s*\(\s*(\w+)\s+(\w+)\s*:\s*(\w+)\s*\)')
    output_code = re.sub(pattern, r'for (\1 \2 = 0; \2 < sizeof(\3) / sizeof(\3[0]); \2++)', input_code)

    return output_code

def print_syntax(input_code):
    # Use regular expression to find print statements with variables or string literals
    pattern = re.compile(r'print\s*\(([^()]+(?:\([^()]*\)[^()]*)*)\)')

    # Find matches in the input code
    matches = pattern.finditer(input_code)

    # Process each match in reverse order to avoid index issues
    for match in reversed(list(matches)):
        print_statement = match.group(1)

        # Replace '+' with ' << ' inside the print statement
        replaced_statement = re.sub(r'\s*\+\s*', ' << ', print_statement)

        # Construct the std::cout line
        cout_line = f'std::cout << {replaced_statement} << std::endl'

        # Replace the print statement with the std::cout line in the entire code
        input_code = input_code[:match.start()] + cout_line + input_code[match.end():]

    return input_code

def input_syntax(input_code):
    # Use regular expression to find input statements with or without variables
    pattern = re.compile(r'input\s*\(\s*([^)]*)\s*\)')

    # Find matches in the input code
    match = pattern.search(input_code)

    # If a match is found, replace the input statement
    if match:
        input_statement = match.group(1)

        # Replace ',' with ' >> ' inside the input statement
        replaced_statement = re.sub(r'\s*,\s*', ' >> ', input_statement)

        # Construct the std::cin line with reversed order
        cin_line = f'std::cin >> {replaced_statement}'

        # Replace the input statement with the reversed std::cin line in the entire code
        modified_code = input_code.replace(match.group(0), cin_line)

        return modified_code
    else:
        # If no match is found, return the input code as is
        return input_code
