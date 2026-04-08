import pytest
from calculator.parser import parse_input
from calculator.evaluator import calculate


@pytest.mark.parametrize(
    "expr, expected",
    [("-2", -2), ("-2 + 3", 1), ("-2 + 3 ^ 2", 7), ("2 + -3", -1), ("-2 + -3", -5)],
)
def test_unary_basic(expr, expected):
    tokens = parse_input(expr)
    result = calculate(tokens)
    assert result == expected


@pytest.mark.parametrize(
    "expr, expected",
    [
        ("-(2 + 3)", -5),
        ("(-2 + 3)", 1),
        ("2 + (-3 * 4)", -10),
        ("-(2 + (3 * 4))", -14),
        ("-(2 +-(3 * 4))", 10),
    ],
)
def test_unary_with_parentheses(expr, expected):
    tokens = parse_input(expr)
    result = calculate(tokens)
    assert result == expected


@pytest.mark.parametrize(
    "expr, expected",
    [
        ("-2^2", -4),  # -(2^2)
        ("(-2)^2", 4),  # (-2)^2
        ("-2 * 3", -6),
        ("2 * -3", -6),
    ],
)
def test_unary_precedence(expr, expected):
    tokens = parse_input(expr)
    result = calculate(tokens)
    assert result == expected
