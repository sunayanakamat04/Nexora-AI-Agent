import re

def calculator(expression):
    try:
        # Keep only numbers and math operators
        expression = expression.strip()

        # Check that it contains only safe math characters
        if not re.fullmatch(r"[0-9+\-*/().\s]+", expression):
            return "Invalid mathematical expression"

        result = eval(expression, {"__builtins__": {}}, {})

        return str(result)

    except Exception as e:
        return f"Calculation error: {e}"