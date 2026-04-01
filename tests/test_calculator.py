import pytest
from calculator.main import calculate, parse_input, CalculationError

@pytest.mark.parametrize("expr, error_code", [
    ("10 / 0", "DIVISION_BY_ZERO"),
    ("11 % 0", "DIVISION_BY_ZERO"),
    ("2 + 3 -", "INVALID_FORMAT"),
    ("3 + 7 + a", "INVALID_NUMBER"),
    ("2 + 3 & 5", "UNKNOWN_OPERATOR")
])


def test_errors(expr, error_code):
    
    with pytest.raises(CalculationError) as e:
        tokens = parse_input(expr)
        calculate(tokens)
        
    assert e.value.code == error_code