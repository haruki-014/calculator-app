from calculator.evaluator import InterPreter
from calculator.parser import parse_input
from calculator.errors import CalculationError


class CalculatorService:
    def __init__(self) -> None:
        self.interpreter = InterPreter()

    def execute(self, text: str) -> str:
        try:
            node = parse_input(text)
            result = self.interpreter.run(node)
            return str(result)
        except CalculationError as e:
            return f"error: {e}"
