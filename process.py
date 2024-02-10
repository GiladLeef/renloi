import re

def replace_syntax(input_code):
    output_code = input_code.replace("int main()", "int main(int argc, char *argv[])")
    output_code = output_code.replace("File.", "File::")
    output_code = output_code.replace("Math.", "Math::")
    output_code = output_code.replace("String.", "String::")
    output_code = output_code.replace("Net.", "Net::")
    output_code = output_code.replace("Net.", "Net::")
    output_code = output_code.replace("ThreadPool.", "ThreadPool::")
    output_code = output_code.replace("thread.id()", "this_thread::get_id()")

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
