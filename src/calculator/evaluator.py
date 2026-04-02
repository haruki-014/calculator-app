from .errors import ErrorCode, CalculationError
from .operators import OPERATORS

def find_innermost_parentheses(tokens):
    
    start = None
    
    for i, token in enumerate(tokens):
        
        if token == "(":
            start = i
        elif token == ")":
            if start is None:
                raise CalculationError(
                    code=ErrorCode.INVALID_EXPRESSION,
                    message="unmatched closing parentheses",
                    position=i
                )
            
            return start, i
        
    if start is not None:
        raise CalculationError(
            code=ErrorCode.INVALID_EXPRESSION,
            message="unmatched opening parentheses",
            position=start
        )
        
    return None

      
def process_parentheses(tokens):
    
    result = tokens[:]
    
    while "(" in result:
        found = find_innermost_parentheses(result)
        
        if found is None:
            break
        
        start, end = found
        
        inner = result[start+1:end]
        
        if not inner:
            raise CalculationError(
                code=ErrorCode.INVALID_EXPRESSION,
                message="empty parentheses"
            )
            
        value = calculate(inner)
        
        result[start:end+1] = [value]
    
    return result
    

def process_power(tokens):
    
    result = tokens[:]
    i = len(result) - 2
    
    while i > 0:
        if result[i] == "^":
            try:
                left = result[i-1]
                right = result[i+1]
            except IndexError as e:
                raise CalculationError(
                    code=ErrorCode.INVALID_EXPRESSION,
                    message="invalid_expression",
                    tokens=result,
                    position=i
                )
            
            try:
                value = left ** right
            except Exception as e:
                raise CalculationError(
                    code=ErrorCode.EVALUATION_ERROR,
                    message="evaluation_error",
                    left=left,
                    right=right
                )
            
            result[i-1:i+2] = [value]
            
            i -= 2
        else:
            i -= 1
            
    return result


def process_high_priority(tokens):
    
    result = []
    i = 0
    
    while i < len(tokens):
        
        token = tokens[i]
        
        if token in {"*", "/", "%"}:
            
            try:
                prev = result.pop()
                next_value = tokens[i+1]
            except (KeyError, IndexError):
                raise CalculationError(
                    code=ErrorCode.INVALID_EXPRESSION,
                    message="invalid high priority expression",
                    tokens=tokens,
                    position=i
                )
            
            try:
                value = OPERATORS[token](prev, next_value)
            except CalculationError:
                raise
            except Exception as e:
                raise CalculationError(
                    code=ErrorCode.EVALUATION_ERROR,
                    message="operation failed",
                    operator=token,
                    left=prev,
                    right=next_value
                )
            
            result.append(value)
            i += 2
            
        else:
            result.append(token)
            i += 1
            
    return result


def calculate(tokens):
    
    tokens = process_parentheses(tokens)
    tokens = process_power(tokens)
    tokens = process_high_priority(tokens)
    
    result = tokens[0]
    i = 1
    
    while i < len(tokens):
        
        op = tokens[i]
        
        if op not in OPERATORS:         
            raise CalculationError(
                code=ErrorCode.UNKNOWN_OPERATOR,
                message="unknown_operator",
                op=op
            )
            
        next_value = tokens[i+1]
        
        result = OPERATORS[op](result, next_value)
        i += 2
    
    return result        
