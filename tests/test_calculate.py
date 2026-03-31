from calculator.main import calculate, parse_input

def test_addition():
    tokens = parse_input("2 + 3 + 8")
    assert calculate(tokens) == 13
    
def test_substraction():
    tokens = parse_input("5 - 2 - 1")
    assert calculate(tokens) == 2
    
def test_operator_priority():
    tokens = parse_input("2 + 3 * 4")
    assert calculate(tokens) == 14
    
def test_power_right_associative():
    tokens = parse_input("2 ^ 3 ^ 2")
    assert calculate(tokens) == 512
    
def test_complex_expression():
    tokens = parse_input("2 * 3 + 2 ^ 3")
    assert calculate(tokens) == 14