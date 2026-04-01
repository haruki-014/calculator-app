from .errors import ErrorCode, CalculationError

def safe_div(first, second):
    
    if second == 0:
        raise CalculationError(
            code=ErrorCode.DIVISION_BY_ZERO,
            message="division by zero",
            first=first,
            second=second
        )
    return first / second

def safe_mod(first, second):
    
    if second == 0:
        raise CalculationError(
            code=ErrorCode.DIVISION_BY_ZERO,
            message="division by zero",
            first=first,
            second=second
        )
    return first % second

OPERATORS = {
    
    "+": lambda a, b: a + b,
    "-": lambda a, b: a - b,
    "*": lambda a, b: a * b,
    "/": safe_div,
    "^": lambda a, b: a ** b,
    "%": safe_mod
    
}