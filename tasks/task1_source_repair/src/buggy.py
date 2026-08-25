# buggy.py
def add_numbers(a: int, b: int) -> int:
    # BUG: Missing return statement
    a + b  # Should be: return a + b

def multiply_numbers(a: int, b: int) -> int:
    # BUG: Wrong operator (using + instead of *)
    return a + b

def divide_numbers(a: int, b: int) -> float:
    # BUG: No handling for division by zero
    return a / b
