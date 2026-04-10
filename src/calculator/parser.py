from .errors import ErrorCode, CalculationError
from .tokenizer import tokenize
from .ast_nodes import NumberNode, BinaryOpNode, UnaryOpNode, VarNode, AssignNode


# AST実装
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    # 現在見ているトークンを返す
    def current(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    # 次のトークンのインデックスを指定
    def eat(self):
        self.pos += 1

    """
    ()  ->  ^ 
    ^   ->  -X
    -X  ->  */%
    */% ->  +-
    の順に再起評価
    """

    def parse_statement(self):
        if (
            isinstance(self.current(), str)
            and self.current().isidentifier()
            and self.pos + 1 < len(self.tokens)
            and self.tokens[self.pos + 1] == "="
        ):
            name = self.current()
            self.eat()
            self.eat()

            value = self.parse_expr()

            return AssignNode(name, value)

        return self.parse_expr()

    def parse_expr(self):
        node = self.parse_term()

        # nodeにプラスまたはマイナスが含まれる限り式を返す
        while self.current() in ("+", "-"):
            op = self.current()
            self.eat()

            if self.current() is None:
                raise CalculationError(
                    ErrorCode.INVALID_FORMAT, message="invalid format"
                )

            right = self.parse_term()

            node = BinaryOpNode(node, op, right)

        return node

    def parse_term(self):
        node = self.parse_unary()

        # nodeに*、/、%が含まれる限り式を返す
        # 右辺は単行演算子の可能性を考慮しparse_unary()を呼び出し
        while self.current() in ("*", "/", "%"):
            op = self.current()
            self.eat()
            right = self.parse_unary()

            node = BinaryOpNode(node, op, right)

        return node

    def parse_unary(self):
        token = self.current()

        # トークンの先頭が単行演算子であった場合
        # 次の数字を単行演算子のクラスにセット
        if token == "-":
            self.eat()

            if self.current() is None:
                raise CalculationError(
                    code=ErrorCode.INVALID_FORMAT, message="invalid format"
                )

            if self.current() == "-":
                raise CalculationError(
                    ErrorCode.INVALID_FORMAT, message="invalid format"
                )

            return UnaryOpNode("-", self.parse_unary())

        return self.parse_power()

    def parse_power(self):
        node = self.parse_factor()

        # 最右辺から順に評価されるよう右辺で
        # parse_power()を再呼び出し
        if self.current() is not None and self.current() == "^":
            op = self.current()
            self.eat()
            right = self.parse_power()

            node = BinaryOpNode(node, op, right)

        return node

    def parse_factor(self):
        token = self.current()

        # トークンが単一の浮動小数点なら数字クラスにセット
        if isinstance(token, float):
            self.eat()
            return NumberNode(token)

        if isinstance(token, str) and token.isidentifier():
            self.eat()
            return VarNode(token)

        if token == "(":
            self.eat()

            # 括弧内が空白な場合文法エラー
            if self.current() == ")":
                raise CalculationError(
                    ErrorCode.INVALID_EXPRESSION, message="invalid expression"
                )

            node = self.parse_expr()

            # 閉じ括弧が式に無ければ文法エラー
            if self.current() != ")":
                raise CalculationError(
                    ErrorCode.INVALID_EXPRESSION, message="invalid expression"
                )

            self.eat()
            return node

        # 式の始まりが数字または適切な単行演算子
        # または開き括弧でなければ文法エラー
        raise CalculationError(
            ErrorCode.INVALID_EXPRESSION, message="invalid expression"
        )


def parse_input(user_input: str):
    parts = tokenize(user_input)
    tokens = []

    if len(parts) < 1:
        raise CalculationError(
            code=ErrorCode.INVALID_FORMAT,
            message="invalid expression",
            input=user_input,
        )

    for part in parts:
        if part in {"+", "-", "*", "/", "%", "^", "(", ")", "="}:
            tokens.append(part)

        else:
            try:
                tokens.append(float(part))
            except ValueError:
                if part.isidentifier():
                    tokens.append(part)
                else:
                    raise CalculationError(
                        code=ErrorCode.INVALID_NUMBER,
                        message="invalid number",
                        input=user_input,
                    )

    parser = Parser(tokens)

    node = parser.parse_statement()

    if parser.current() is not None:
        raise CalculationError(
            ErrorCode.INVALID_EXPRESSION, message="invalid expression"
        )

    return node
