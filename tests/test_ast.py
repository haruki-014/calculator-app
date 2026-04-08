import pytest
from calculator.errors import CalculationError
from calculator.ast_nodes import NumberNode, BinaryOpNode, UnaryOpNode


def test_number_node():
    node = NumberNode(3)
    
    assert node.value == 3
    
    
def test_binary_node():
    
    left = NumberNode(2)
    right = NumberNode(3)
    
    node = BinaryOpNode(left, "+", right)
    
    assert node.left == left
    assert node.right == right
    assert node.op == "+"
    
    
def test_unary_node():
    
    operand = NumberNode(5)
    node = UnaryOpNode("-", operand)
    
    assert isinstance(node.operand, NumberNode)
    assert node.operand.value == 5
    assert node.op == "-"
    
    
def test_pretty_simple():
    
    node = BinaryOpNode(NumberNode(3), "+", NumberNode(4))
    result = node.pretty()
    
    assert "BinaryOp(+)" in result
    assert "Number(3)" in result
    assert "Number(4)" in result
    
    
def test_invalid_binary():
    with pytest.raises(CalculationError):
        BinaryOpNode(None, "+", NumberNode(3))
    