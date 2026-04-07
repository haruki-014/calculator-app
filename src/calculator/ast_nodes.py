

# 演算子を含まない単一の値
class NumberNode():
    
    def __init__(self, value):
        self.value = value
        
    def __repr__(self):
        return f"{self.value}"
        
# 単一の値または括弧で覆われた式同士で計算できる式
class BinaryOpNode():
    
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right
        
    def __repr__(self):
        return f"({self.left} {self.op} {self.right})"
        
        
# 演算子を含む単一または括弧で覆われた式
class UnaryOpNode():
    
    def __init__(self, op, operand):
        self.op = op
        self.operand = operand
        
    def __repr__(self):
        return f"({self.op} {self.operand})"