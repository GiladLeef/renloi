import re

def replace_syntax(input_code):
    output_code = input_code.replace("print", "printf")
    output_code = output_code.replace("scan", "scanf")
    output_code = output_code.replace("file.read", "file_read")
    output_code = output_code.replace("file.write", "file_write")
    output_code = re.sub(r'string (\w+)', r'char \1[]', output_code)
    output_code = re.sub(r'char (\w+)\[\] = read\(([^)]+)\);', r'char *\1 = read(\2);', output_code)

    return output_code

def foreach_syntax(input_code):
    pattern = re.compile(r'foreach\s*\(\s*(\w+)\s+(\w+)\s*:\s*(\w+)\s*\)')
    output_code = re.sub(pattern, r'for (\1 \2 = 0; \2 < sizeof(\3) / sizeof(\3[0]); \2++)', input_code)

    return output_code

def print_syntax(input_code):
    # Define a dictionary to map data type specifiers to format specifiers
    type_mapping = {
        'int': '%d',
        'char': '%c',
        'string': '%s',
        'float': '%f',
        'hex': '%x',  # or '%X' for uppercase
        'octal': '%o',
        'unsigned': '%u',
        'pointer': '%p',
        'scientific': '%e',  # or '%E' for uppercase
        'compact_scientific': '%g',  # or '%G' for uppercase
        'hex_float': '%a',  # or '%A' for uppercase
    }

    pattern = r'printf\((\w+): (\w+)\);'

    output_code = re.sub(pattern, lambda match: f'printf("{type_mapping.get(match.group(1), match.group(1))}", {match.group(2)});', input_code)
    return output_code
