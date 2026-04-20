import pytest
from calculator.evaluator import InterPreter
from calculator.parser import parse_input
from calculator.errors import ErrorCode, CalculationError


interpreter = InterPreter()


@pytest.mark.parametrize(
    "expr, error_code",
    [
        ("10 / 0", ErrorCode.DIVISION_BY_ZERO),
        ("11 % 0", ErrorCode.DIVISION_BY_ZERO),
        ("2 + 3 -", ErrorCode.INVALID_FORMAT),
        ("3 + 7 + a", ErrorCode.UNKNOWN_VARIABLE),
        ("2 + 3 & 5", ErrorCode.UNKNOWN_OPERATOR),
    ],
)
def test_errors(expr, error_code):
    with pytest.raises(CalculationError) as e:
        node = parse_input(expr)
        interpreter.run(node)

    assert e.value.code == error_code
