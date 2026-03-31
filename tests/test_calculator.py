import pytest
from calculator.main import calculate, parse_input, CalculationError


def test_division_by_zero():
    tokens = parse_input("10 / 0")
    
    with pytest.raises(CalculationError) as e:
        calculate(tokens)
        
    assert e.value.code == "DIVISION_BY_ZERO"
    
def test_mod_by_zero():
    tokens = parse_input("10 % 0")
    
    with pytest.raises(CalculationError) as e:
        calculate(tokens)
        
    assert e.value.code == "DIVISION_BY_ZERO"
    
def test_invalid_format():
    
    with pytest.raises(CalculationError) as e:
        parse_input("2 + 3 -")
        
    assert e.value.code == "INVALID_FORMAT"
    
def test_invalid_number():
    
    with pytest.raises(CalculationError) as e:
        parse_input("3 + 7 + a")
        
    assert e.value.code == "INVALID_NUMBER"
    
def test_unknown_operator():
    tokens = parse_input("2 + 3 & 5")
    
    with pytest.raises(CalculationError) as e:
        calculate(tokens)
        
    assert e.value.code == "UNKNOWN_OPERATOR"
    
    
        