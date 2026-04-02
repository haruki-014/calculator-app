from .errors import ErrorCode, CalculationError

def parse_input(user_input: str):
    
    parts = user_input.split()
    
    if len(parts) < 3:
        
        raise CalculationError(
            code=ErrorCode.INVALID_FORMAT,
            message="invalid expression",
            input=user_input
        )
        
    tokens = []
    
    for part in parts:
        
        if part in {"(", ")"}:
            tokens.append(part)
        
        elif part in {"+", "-", "*", "/", "%"}:
            tokens.append(part)
            
        else:
            try:
                tokens.append(float(part))
            except ValueError as e:
                raise CalculationError(
                    code=ErrorCode.INVALID_NUMBER,
                    message="invalid number",
                    input=user_input
                ) from e
    
    return tokens