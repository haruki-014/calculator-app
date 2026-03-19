def calculate(first, op, second):
    if op == '+':
        return first + second
    elif op == '-':
        return first - second
    elif op == '*':
        return first * second
    elif op == '/':
        if second == 0:
            return "Error: division by zero"
        return first / second
    else:
        return "Error: unknown operator"


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
            parts = user_input.split()

            if len(parts) != 3:
                print("Invalid format")
                continue

            first = float(parts[0])
            op = parts[1]
            second = float(parts[2])

            result = calculate(first, op, second)
            print(first, op, second, "=", result)

        except ValueError:
            print("Error: invalid number")


if __name__ == "__main__":
    main()