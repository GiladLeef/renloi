import re

def replace_syntax(input_code):
    # Regex to match text within quotes (strings) and comments
    string_pattern = r'(\".*?\")'
    comment_pattern = r'(\/\/.*?$|\/\*.*?\*\/)'
    
    # Temporary placeholders for strings and comments
    placeholders = []
    
    def replace_in_code(match):
        # Add non-matching parts to the result
        return match.group(0)
    
    def add_placeholder(match):
        # Replace matches with placeholders
        placeholders.append(match.group(0))
        return f'__PLACEHOLDER_{len(placeholders) - 1}__'
    
    # Replace strings and comments with placeholders
    code_with_placeholders = re.sub(string_pattern, add_placeholder, input_code, flags=re.DOTALL | re.MULTILINE)
    code_with_placeholders = re.sub(comment_pattern, add_placeholder, code_with_placeholders, flags=re.DOTALL | re.MULTILINE)
    
    # Replace scope resolution operator
    code_with_scope_replacement = code_with_placeholders.replace("::", ".")
    
    # Restore original strings and comments
    def restore_placeholder(match):
        index = int(match.group(1))
        return placeholders[index]
    
    final_code = re.sub(r'__PLACEHOLDER_(\d+)__', restore_placeholder, code_with_scope_replacement)
    
    return final_code
    
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
        new_lines.insert(last_include_index + 1, '\nusing namespace std;')
    else:
        new_lines.insert(0, 'using namespace std;')

    return '\n'.join(new_lines)
