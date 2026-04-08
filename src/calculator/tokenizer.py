from .errors import ErrorCode, CalculationError


# def tokenize(user_input: str):
#     return re.findall(r"\d+\.?\d*|[a-zA-Z]+|[()+\-*/%^]", user_input)

def tokenize(user_input: str):
    
    tokens = []
    i = 0
    length = len(user_input)
    
    while i < length:
        
        char = user_input[i]
        
        if char.isspace():
            i += 1
            continue
        
        elif char.isdigit() or char == ".":
            start = i
            dot_count = 0
            
            while i < length and (user_input[i].isdigit() or user_input[i] == "."):
                
                if user_input[i] == ".":
                    dot_count += 1
                    
                if dot_count > 1:
                    break
                
                i += 1
                
            tokens.append(user_input[start:i])
            continue
        
        elif char.isalpha():
            start = i
            
            while i < length and char.isalpha():
                
                i += 1
                
            tokens.append(user_input[start:i])
            continue
        
        elif char in "+-*/%^()":
            tokens.append(char)
            i += 1
            continue
        
        else:
            raise CalculationError(
                code=ErrorCode.UNKNOWN_OPERATOR,
                message=f"unknown operator: {char}",
            )
            
    return tokens
    
    