"""
PyChronicle - AST Parsing (Week 1)

Reads a target Python file, parses its Abstract Syntax Tree, and
identifies every variable assignment (name, line number, assigned value).
This does NOT run the code -- it's a static, read-only scan.
"""

import ast


def parse_python_file(filepath):
    """Return a list of dicts: {variable, line, value} for every
    simple assignment (e.g. `x = 5`) found in the file."""
    with open(filepath, "r") as file:
        code = file.read()

    tree = ast.parse(code)
    variables = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    variables.append({
                        "variable": target.id,
                        "line": node.lineno,
                        "value": ast.unparse(node.value),
                    })

    return variables


if __name__ == "__main__":
    import json
    import os

    sample_path = os.path.join(os.path.dirname(__file__), "..", "sample", "test.py")
    result = parse_python_file(sample_path)
    print(json.dumps(result, indent=2))
