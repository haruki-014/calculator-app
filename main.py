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


def calculate(first, op, second):
    if op not in OPERATORS:
        raise CalculationError(
            code="UNKNOWN_OPERATOR",
            message="unknwon_operator",
            op=op
        )
    
    return OPERATORS[op](first, second)
    
    
def parse_input(user_input: str):
    parts = user_input.split()
    
    if len(parts) != 3:
        raise CalculationError(
            code="INVALID_FORMAT",
            message="format must be: number operator number",
            input=user_input
        )
    
    try:
        first = float(parts[0])
        second = float(parts[2])
    except ValueError as e:
        raise CalculationError(
            code="INVALID_NUMBER",
            message="invalid number",
            input=user_input
        ) from e
    
    op = parts[1]
    
    return first, op, second

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
            first, op, second = parse_input(user_input)
            result = calculate(first, op, second)
        except CalculationError as e:
            print("Error", format_error(e))
        else:
            print(first, op, second, "=", result)
            

if __name__ == "__main__":
    main()