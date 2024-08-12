import re

def replaceSyntax(cpp_code):
    def replace_match(match):
        before, dot, after = match.groups()
        
        # Don't replace dots in include statements
        if before.lower() == '#include' or after.lower() in ['h', 'hpp', 'cpp']:
            return f"{before}.{after}"
        
        # Check if before and after are valid C++ identifiers
        if re.match(r'^[a-zA-Z_]\w*$', before) and re.match(r'^[a-zA-Z_]\w*', after):
            return f"{before}::{after}"
        else:
            return f"{before}.{after}"

    # Pattern to match dots between potential identifiers, including #include statements
    pattern = r'(\b(?:#include\b)?[a-zA-Z_]\w*)(\.)([a-zA-Z_]\w*\b)'
    
    # Replace . with :: only in appropriate situations
    modified_code = re.sub(pattern, replace_match, cpp_code)
    
    return modified_code

def addNamespaceStd(codeContent):
    lines = codeContent.split("\n")
    newLines = []
    foundIncludes = False
    for line in lines:
        newLines.append(line)
        if re.match("^\\s*#include", line):
            foundIncludes = True
    if foundIncludes:
        lastIncludeIndex = max(
            [i for i, line in enumerate(newLines) if re.match("^\\s*#include", line)],
            default=-1,
        )
        newLines.insert(lastIncludeIndex + 1, "\nusing namespace std;")
    else:
        newLines.insert(0, "using namespace std;")
    return "\n".join(newLines)
