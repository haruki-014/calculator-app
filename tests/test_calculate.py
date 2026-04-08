import pytest
from calculator.main import calculate, parse_input


@pytest.mark.parametrize(
    "expr, expected",
    [
        ("2 + 3 + 8", 13),
        ("5 - 2 - 1", 2),
        ("11 % 3", 2),
        ("2 + 3 * 4", 14),
        ("2 ^ 3 ^ 2", 512),
        ("2 * 3 + 2 ^ 3", 14),
    ],
)
def test_calcs(expr, expected):

    tokens = parse_input(expr)
    result = calculate(tokens)

    assert result == expected
