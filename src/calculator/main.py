from .errors import ErrorCode, CalculationError
from .operators import OPERATORS
from .parser import parse_input
from .evaluator import calculate


def format_error(e: CalculationError) -> str:
    
    messages = {
        ErrorCode.INVALID_FORMAT: "入力形式が正しくありません（例: 2 + 3)",
        ErrorCode.INVALID_NUMBER: "数値として認識できません",
        ErrorCode.DIVISION_BY_ZERO: "ゼロで割ることはできません",
        ErrorCode.INVALID_EXPRESSION: "式が正しくありません",
        ErrorCode.EVALUATION_ERROR: "計算に失敗しました",
    }
    
    if e.code == ErrorCode.UNKNOWN_OPERATOR:
        return f"未対応の演算子です: {e.context.get('op')}"
    
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
            print(user_input, "=", result)
            

if __name__ == "__main__":
    main()