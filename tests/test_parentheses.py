import pytest
from calculator.parser import parse_input
from calculator.evaluator import calculate


@pytest.mark.parametrize(
    "expr, expected",
    [
        ("(2+3)", 5),
        ("(2 +3)", 5),
        ("(2+3) *4", 20),
        ("(2 + (3*4))", 14),
        ("((2+3) * 2)", 10),
        ("2 * (2+3) * 4", 40),
        ("2 * (3 + (4 * 5))", 46),
        ("((1+  2) * (3  +4))", 21),
    ],
)
def test_parentheses(expr, expected):

    tokens = parse_input(expr)
    result = calculate(tokens)

    assert result == expected
