import re

def replace_syntax(input_code):
    output_code = input_code.replace("int main()", "int main(int argc, char *argv[])")
    output_code = output_code.replace("File.write", "File::write")
    output_code = output_code.replace("File.read", "File::read")
    output_code = output_code.replace("Math.", "Math::")
    #output_code = re.sub(r'string (\w+)', r'char \1[]', output_code)
    #output_code = re.sub(r'char (\w+)\[\] = read\(([^)]+)\);', r'char *\1 = read(\2);', output_code)

    return output_code
    
def add_namespace_std(code_content):
    lines = code_content.split('\n')

    new_lines = []
    found_includes = False

    for line in lines:
        new_lines.append(line)
        if re.match(r'^\s*#include', line):
            found_includes = True

    if found_includes:
        # Find the index of the last #include line
        last_include_index = max([i for i, line in enumerate(new_lines) if re.match(r'^\s*#include', line)], default=-1)
        # Insert 'using namespace std;' after the last #include line
        new_lines.insert(last_include_index + 1, 'using namespace std;')
    else:
        new_lines.insert(0, 'using namespace std;')

    return '\n'.join(new_lines)
