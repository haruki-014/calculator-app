from .errors import ErrorCode, CalculationError


class ASTNode:
    def pretty(self, prefix="", is_last=True):
        branch = "└── " if is_last else "├── "

        result = f"{prefix}{branch}{self._label()}\n"

        if is_last:
            new_prefix = prefix + "  "
        else:
            new_prefix = prefix + "│   "

        children = self._children()

        for i, child in enumerate(children):
            is_last_child = i == len(children) - 1
            result += child.pretty(new_prefix, is_last_child)

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
        if left is None or right is None:
            raise CalculationError(
                code=ErrorCode.INVALID_AST,
                message="BinaryOpNode requires left and right",
                op=op,
            )

        self.left = left
        self.op = op
        self.right = right

    def __repr__(self):
        return f"({self.left} {self.op} {self.right})"

    def _label(self):
        return f"BinaryOp({self.op})"

    def _children(self):
        if self.left is None or self.right is None:
            raise CalculationError(
                code=ErrorCode.INVALID_AST, message="Invalid BinaryOpNode structure"
            )

        return [self.left, self.right]


# 演算子を含む単一または括弧で覆われた式
class UnaryOpNode(ASTNode):
    def __init__(self, op, operand):
        if operand is None:
            raise CalculationError(
                code=ErrorCode.INVALID_AST,
                message="UnaryOpNode requires operand",
                op=op,
            )

        self.op = op
        self.operand = operand

    def __repr__(self):
        return f"({self.op} {self.operand})"

    def _label(self):
        return f"Unary({self.op})"

    def _children(self):
        return [self.operand]


class VarNode(ASTNode):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name

    def _label(self):
        return f"Var({self.name})"


class AssignNode(ASTNode):
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __repr__(self):
        return f"{self.name} = {self.value}"

    def _label(self):
        return f"Assign({self.name})"

    def _children(self):
        return [self.value]
