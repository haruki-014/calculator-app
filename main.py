class CalculationError(Exception):
    # 電卓用のカスタム例外は後で作成
    pass

def calculate(first, op, second):
    if op == '+':
        return first + second
    elif op == '-':
        return first - second
    elif op == '*':
        return first * second
    elif op == '/':
        if second == 0:
            raise ZeroDivisionError("division by zero")
        return first / second
    else:
        raise CalculationError(f"unknown operator: {op}")
    
    
def parse_input(user_input: str):
    parts = user_input.split()
    
    if len(parts) != 3:
        raise CalculationError("format must be: number operator number")
    
    try:
        first = float(parts[0])
        second = float(parts[2])
    except ValueError as e:
        raise CalculationError("invalid number") from e
    
    op = parts[1]
    
    return first, op, second


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
            print(f"Input Error: {e}")
        except ZeroDivisionError as e:
            print(f"Math Error: {e}")
        else:
            print(first, op, second, "=", result)
            

if __name__ == "__main__":
    main()