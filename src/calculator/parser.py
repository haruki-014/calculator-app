from .errors import ErrorCode, CalculationError

def parse_input(user_input: str):
    
    parts = user_input.split()
    
    if len(parts) < 3 or len(parts) % 2 == 0:
        
        raise CalculationError(
            code=ErrorCode.INVALID_FORMAT,
            message="invalid expression",
            input=user_input
        )
        
    tokens = []
    
    for i, part in enumerate(parts):
        
        if i % 2 == 0:
            
            try:
                tokens.append(float(part))
            except ValueError as e:
                raise CalculationError(
                    code=ErrorCode.INVALID_NUMBER,
                    message="invalid number",
                    input=user_input
                ) from e
                
        else:
            tokens.append(part)
    
    return tokens