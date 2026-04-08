from .errors import ErrorCode, CalculationError
from .operators import OPERATORS
from .ast_nodes import NumberNode, BinaryOpNode, UnaryOpNode

DEBUG = True

class DebugMode:
    OFF = 0
    EVAL = 1
    AST = 2
    ALL = 3
    

def calculate(ast, debug=DebugMode.AST):
    
    if debug in (DebugMode.AST, DebugMode.ALL):
        
        print("\n==== AST ====\n")
        print(ast.pretty())
        print("====     ====\n")     
    
    return evaluate(ast, debug=debug)


def evaluate(node, debug=None, depth=0):
    
    if debug is None:
        debug = DEBUG
        
    indent = "  " * depth
    
    if debug:
        print(f"{indent}Evaluating: {node}")
    
    if isinstance(node, NumberNode):
        if debug:
            print(f"{indent} -> {node.value}")
            
        return node.value
    
    elif isinstance(node, UnaryOpNode):
        value = evaluate(node.operand, debug, depth+1)
        
        if node.op == "-":
            value = -value
            
        if debug:
            print(f"{indent} -> {value}")
            
        return value
        
    elif isinstance(node, BinaryOpNode):
        left = evaluate(node.left, debug, depth+1)
        right = evaluate(node.right, debug, depth+1)
        
        result = OPERATORS[node.op](left, right)
        
        if debug:
            print(f"{indent} -> {left} {node.op} {right} = {result}")
        
        return result
    
    else:
        raise Exception("Unkown node")


# 旧計算処理
"""
# 単行演算子と二項演算子を分離
def handle_unary_minus(tokens):
    
    result = []
    i = 0
    
    # 未解析トークンがある限り続行
    while i < len(tokens):
        token = tokens[i]
        
        # トークンがマイナスである
        # かつ
        # 初項であるまたは手前のトークンが演算子または(であれば
        if token == "-" and (
            i == 0 or tokens[i-1] in {"+", "-", "*", "/", "%", "^", "("}
        ):
            # トークンの最終項がマイナスであれば形式エラー
            if i + 1 >= len(tokens):
                raise CalculationError(
                    code=ErrorCode.INVALID_FORMAT,
                    message="invalid unary minus",
                    tokens=tokens
                )
            
            # 次の項を変数に用意
            next_token = tokens[i+1]
            
            # 次の項が整数または浮動小数点であれば
            # 符号を逆にし返すリストに追加
            # 開始位置を次の演算子または(、)に移動
            if isinstance(next_token, (int, float)):
                result.append(-1.0)
                result.append("*")
                result.append(next_token)
                i += 2
                continue
            
            # 次の項が(であれば
            # 括弧内に-1.0が掛ける
            # 開始位置を
            elif next_token == "(":
                result.append(-1.0)
                result.append("*")
                i += 1
                continue
            
            # 次の項が数字または(でなければ形式エラー
            else:
                raise CalculationError(
                    code=ErrorCode.INVALID_FORMAT,
                    message="invalid unary minus operand",
                    value=next_token
                )
        
        # トークンがマイナスでもなく
        # 初項または演算子でもなければ
        # 返すリストにそのまま追加
        # 開始位置を横に移動    
        else:
            result.append(token)
            i += 1
            
    return result           


# 括弧が組として成立しているか
def validate_parentheses(tokens):
    
    count = 0
    
    for token in tokens:
        
        if token == "(":
            count += 1
        elif token == ")":
            count -= 1
        
        # 閉じ括弧が開き括弧より多くなった時点で文法エラー
        if count < 0:
            raise CalculationError(
                code=ErrorCode.INVALID_EXPRESSION,
                message="unmatched closing parentheses"
            )
    
    # 最終的に開き括弧が閉じ括弧より多い場合文法エラー       
    if count > 0:
        raise CalculationError(
            code=ErrorCode.INVALID_EXPRESSION,
            message="unmatched opening parentheses"
        )


def find_innermost_parentheses(tokens):
    
    start = None
    
    for i, token in enumerate(tokens):
        
        # 左から読み込み最も内側の開き括弧を見つける
        # 最も内側の開き括弧に対応した閉じ括弧を見つける
        # 最も内側の括弧の組みのインデックスのタプルを返す
        if token == "(":
            start = i
        elif token == ")":    
            return start, i
        
    return None


# 括弧全体の処理     
def process_parentheses(tokens):
    
    result = tokens[:]
    
    # トークンをコピーした中に開き括弧が見つかる限り
    # 最も内側の括弧の組みを見つける関数を呼び出し
    # 式を計算する関数を括弧内の式に呼び出し
    # 計算結果を( + 元の式　+ ) と入れ替える
    while "(" in result:
        found = find_innermost_parentheses(result)
        
        if found is None:
            break
        
        start, end = found
        
        inner = result[start+1:end]
        
        # 括弧内に式が無ければ文法エラー
        if not inner:
            raise CalculationError(
                code=ErrorCode.INVALID_EXPRESSION,
                message="empty parentheses"
            )
            
        value = calculate(inner)
        
        # 括弧部分に括弧内計算結果を代入
        result[start:end+1] = [value]
    
    return result
    

# 累乗全体の処理
def process_power(tokens):
    
    result = tokens[:]
    
    # 累乗は右から処理するため
    # インデックスを最も右に存在する演算子に設定
    # (単行演算子は処理済みの実装のため)
    i = len(result) - 2
    
    while i > 0:
        
        # 累乗の演算子が見つかる限り実行
        if result[i] == "^":
            
            # 左右に要素が無ければインデックスエラー
            try:
                left = result[i-1]
                right = result[i+1]
            except IndexError as e:
                raise CalculationError(
                    code=ErrorCode.INVALID_EXPRESSION,
                    message="invalid_expression",
                    tokens=result,
                    position=i
                )
            
            # 左右の数字を計算
            # できなければ計算エラー
            try:
                value = left ** right
            except Exception as e:
                raise CalculationError(
                    code=ErrorCode.EVALUATION_ERROR,
                    message="evaluation_error",
                    left=left,
                    right=right
                )
            
            result[i-1:i+2] = [value]
            
            i -= 2
        else:
            i -= 1
            
    return result


# 掛け算、割り算、余り計算を先に計算
def process_high_priority(tokens):
    
    result = []
    i = 0
    
    while i < len(tokens):
        
        token = tokens[i]
        
        if token in {"*", "/", "%"}:
            
            try:
                prev = result.pop()
                next_value = tokens[i+1]
            except (KeyError, IndexError):
                raise CalculationError(
                    code=ErrorCode.INVALID_EXPRESSION,
                    message="invalid high priority expression",
                    tokens=tokens,
                    position=i
                )
            
            try:
                value = OPERATORS[token](prev, next_value)
            except CalculationError:
                raise
            except Exception as e:
                raise CalculationError(
                    code=ErrorCode.EVALUATION_ERROR,
                    message="operation failed",
                    operator=token,
                    left=prev,
                    right=next_value
                )
            
            result.append(value)
            i += 2
            
        else:
            result.append(token)
            i += 1
            
    return result


def calculate(tokens):
    
    validate_parentheses(tokens)
    
    tokens = process_parentheses(tokens)
    tokens = process_power(tokens)
    tokens = handle_unary_minus(tokens)
    tokens = process_high_priority(tokens)
    
    result = tokens[0]
    i = 1
    
    while i < len(tokens):
        
        op = tokens[i]
        
        if op not in OPERATORS:         
            raise CalculationError(
                code=ErrorCode.UNKNOWN_OPERATOR,
                message="unknown_operator",
                op=op
            )
            
        if i + 1 >= len(tokens):
            raise CalculationError(
                code=ErrorCode.INVALID_FORMAT,
                message="missing operand",
                tokens=tokens
            )
            
        next_value = tokens[i+1]
        
        result = OPERATORS[op](result, next_value)
        i += 2
    
    return result    
    
"""    
