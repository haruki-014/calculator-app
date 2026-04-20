import pytest
from calculator.evaluator import InterPreter
from calculator.parser import parse_input


interpreter = InterPreter()


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
    node = parse_input(expr)
    result = interpreter.run(node)

    assert result == expected
