from enum import Enum

class ErrorCode(str, Enum):
    DIVISION_BY_ZERO = "DIVISION_BY_ZERO"
    INVALID_FORMAT = "INVALID_FORMAT"
    INVALID_NUMBER = "INVALID_NUMBER"
    UNKNOWN_OPERATOR = "UNKNOWN_OPERATOR"
    INVALID_EXPRESSION = "INVALID_EXPRESSION"
    EVALUATION_ERROR = "EVALUATION_ERROR"
    
    INVALID_AST = "INVALID_AST"
    UNKNOWN_NODE = "UNKNOWN_NODE"

class CalculationError(Exception):
    
    def __init__(self, code: ErrorCode, message: str, **context):
        
        super().__init__(message)
        self.code = code
        self.context = context