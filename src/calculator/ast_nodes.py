


class ASTNode:
    
    def pretty(self, depth=0):
        
        # 骨組みを作成
        indent = "  " * depth
        result = f"{indent} {self._label()}\n"
        
        # 子ノードにも再帰
        for child in self._children():
            result += child.pretty(depth+1)
            
        return result
    
    # 呼び出し時に値が返されていなければエラー
    def _label(self):
        raise NotImplementedError
    
    # 子ノード処理の違いを受け取る
    def _children(self):
        return []


# 演算子を含まない単一の値
class NumberNode(ASTNode):
    
    def __init__(self, value):
        self.value = value
        
    def __repr__(self):
        
        return f"{self.value}"
    
    def _label(self):
        return f"Number({self.value})"
    
        
# 単一の値または括弧で覆われた式同士で計算できる式
class BinaryOpNode(ASTNode):
    
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right
        
    def __repr__(self):
        return f"({self.left} {self.op} {self.right})"
    
    def _label(self):
        return f"BinaryOp({self.op})"
    
    def _children(self):
        return [self.left, self.right]
        
        
# 演算子を含む単一または括弧で覆われた式
class UnaryOpNode(ASTNode):
    
    def __init__(self, op, operand):
        self.op = op
        self.operand = operand
        
    def __repr__(self):
        return f"({self.op} {self.operand})"
    
    def _label(self):
        return f"Unary({self.op})"
    
    def _children(self):
        return [self.operand]