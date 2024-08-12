import re


def replaceSyntax(inputCode):
    stringPattern = '(\\".*?\\")'
    commentPattern = "(\\/\\/.*?$|\\/\\*.*?\\*\\/)"
    placeholders = []

    def replaceInCode(match):
        return match.group(0)

    def addPlaceholder(match):
        placeholders.append(match.group(0))
        return f"__PLACEHOLDER_{len(placeholders) - 1}__"

    codeWithPlaceholders = re.sub(
        stringPattern, addPlaceholder, inputCode, flags=re.DOTALL | re.MULTILINE
    )
    codeWithPlaceholders = re.sub(
        commentPattern,
        addPlaceholder,
        codeWithPlaceholders,
        flags=re.DOTALL | re.MULTILINE,
    )
    codeWithScopeReplacement = codeWithPlaceholders.replace("::", ".")

    def restorePlaceholder(match):
        index = int(match.group(1))
        return placeholders[index]

    finalCode = re.sub(
        "__PLACEHOLDER_(\\d+)__", restorePlaceholder, codeWithScopeReplacement
    )
    return finalCode


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
