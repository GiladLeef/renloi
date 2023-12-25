import re

def replace_syntax(input_code):
    output_code = input_code.replace("int main()", "int main(int argc, char *argv[])")
    output_code = output_code.replace("File.write", "File::write")
    output_code = output_code.replace("File.read", "File::read")
    output_code = re.sub(r'string (\w+)', r'char \1[]', output_code)
    output_code = re.sub(r'char (\w+)\[\] = read\(([^)]+)\);', r'char *\1 = read(\2);', output_code)

    return output_code
