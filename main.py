class CalculationError(Exception):
    
    def __init__(self, code: str, message: str, **context):
        
        super().__init__(message)
        self.code = code
        self.context = context
        

def safe_div(first, second):
    
    if second == 0:
        raise CalculationError(
            code="DIVISION_BY_ZERO",
            message="division by zero",
            first=first,
            second=second
        )
    return first / second

def safe_mod(first, second):
    
    if second == 0:
        raise CalculationError(
            code="DIVISION_BY_ZERO",
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


def calculate(tokens):
    
    result = tokens[0]
    i = 1
    
    while i < len(tokens):
        
        op = tokens[i]
        if op not in OPERATORS:
            
            raise CalculationError(
                code="UNKNOWN_OPERATOR",
                message="unknown_operator",
                op=op
            )
            
        next_value = tokens[i+1]
        
        result = OPERATORS[op](result, next_value)
        i += 2
    
    return result        

    
def parse_input(user_input: str):
    
    parts = user_input.split()
    
    if len(parts) < 3 or len(parts) % 2 == 0:
        
        raise CalculationError(
            code="INVALID_FORMAT",
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
                    code="INVALID_NUMBER",
                    message="invalid number",
                    input=user_input
                ) from e
                
        else:
            tokens.append(part)
    
    return tokens

def format_error(e: CalculationError) -> str:
    
    messages = {
        "INVALID_FORMAT": "入力形式が正しくありません（例: 2 + 3)",
        "INVALID_NUMBER": "数値として認識できません",
        "UNKNOWN_OPERATOR": f"未対応の演算子です: {e.context.get('op')}",
        "DIVISION_BY_ZERO": "ゼロで割ることはできません"
    }
    
    return messages.get(e.code, f"不明なエラー: {e}")


def main():
    
    print("Simple Calculator")
    print("Format: number operator number (e.g. 2 + 3)")
    print("Type 'exit' to quit")

    while True:
        
        user_input = input(">> ")

        if user_input.lower() == 'exit':
            print("selected 'exit'!")
            break

        try:
            tokens = parse_input(user_input)
            result = calculate(tokens)
        except CalculationError as e:
            print("Error", format_error(e))
        else:
            print("result", "=", result)
            

if __name__ == "__main__":
    main()