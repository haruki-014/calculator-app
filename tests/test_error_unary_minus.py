import pytest
from calculator.errors import CalculationError, ErrorCode
from calculator.parser import parse_input
from calculator.evaluator import calculate


@pytest.mark.parametrize(
    "expr",
    [
        "-",
        "2 + -",
        "--",
    ],
)
def test_unary_invalid(expr):
    with pytest.raises(CalculationError) as e:
        tokens = parse_input(expr)
        calculate(tokens)

    assert e.value.code == ErrorCode.INVALID_FORMAT


@pytest.mark.parametrize(
    "expr",
    [
        "-()",
    ],
)
def test_unary_expression_invalid(expr):
    with pytest.raises(CalculationError) as e:
        tokens = parse_input(expr)
        calculate(tokens)

    assert e.value.code == ErrorCode.INVALID_EXPRESSION
