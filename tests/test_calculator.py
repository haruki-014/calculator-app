import pytest
from calculator.main import calculate, parse_input, ErrorCode, CalculationError


@pytest.mark.parametrize("expr, error_code", [
    ("10 / 0", ErrorCode.DIVISION_BY_ZERO),
    ("11 % 0", ErrorCode.DIVISION_BY_ZERO),
    ("2 + 3 -", ErrorCode.INVALID_FORMAT),
    ("3 + 7 + a", ErrorCode.INVALID_NUMBER),
    ("2 + 3 & 5", ErrorCode.UNKNOWN_OPERATOR)
])


def test_errors(expr, error_code):
    
    with pytest.raises(CalculationError) as e:
        tokens = parse_input(expr)
        calculate(tokens)
        
    assert e.value.code == error_code