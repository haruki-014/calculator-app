import pytest
from calculator.errors import CalculationError, ErrorCode
from calculator.evaluator import calculate
from calculator.parser import parse_input


@pytest.mark.parametrize(
    "expr, error_code",
    [
        ("(2 + 3", ErrorCode.INVALID_EXPRESSION),
        ("3 + 4)", ErrorCode.INVALID_EXPRESSION),
        ("()", ErrorCode.INVALID_EXPRESSION),
        ("( )", ErrorCode.INVALID_EXPRESSION),
    ],
)
def test_invalid_parentheses(expr, error_code):

    with pytest.raises(CalculationError) as e:
        tokens = parse_input(expr)
        calculate(tokens)

    assert e.value.code == error_code
