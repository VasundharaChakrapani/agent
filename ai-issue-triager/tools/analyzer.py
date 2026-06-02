import ast


def analyze_syntax_complexity(source_code: str):
    """
    Safely analyzes Python code using AST
    without executing it.
    """

    try:
        tree = ast.parse(source_code)

        function_count = 0
        loop_count = 0

        for node in ast.walk(tree):

            if isinstance(node, ast.FunctionDef):
                function_count += 1

            if isinstance(node, (ast.For, ast.While)):
                loop_count += 1

        return {
            "status": "valid",
            "functions": function_count,
            "loops": loop_count
        }

    except SyntaxError as e:
        return {
            "status": "syntax_error",
            "error": str(e)
        }