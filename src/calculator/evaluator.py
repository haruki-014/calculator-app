from .errors import ErrorCode, CalculationError
from .operators import OPERATORS

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
            # トークンの最終項がマイナスであればエラー
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
                result.append(-next_token)
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
            
            # 次の項が数字でも(でもなければエラー
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


def validate_parentheses(tokens):
    
    count = 0
    
    for token in tokens:
        
        if token == "(":
            count += 1
        elif token == ")":
            count -= 1
        
        if count < 0:
            raise CalculationError(
                code=ErrorCode.INVALID_EXPRESSION,
                message="unmatched closing parentheses"
            )
            
    if count > 0:
        raise CalculationError(
            code=ErrorCode.INVALID_EXPRESSION,
            message="unmatched opening parentheses"
        )

def find_innermost_parentheses(tokens):
    
    start = None
    
    for i, token in enumerate(tokens):
        
        if token == "(":
            start = i
        elif token == ")":    
            return start, i
        
    return None

      
def process_parentheses(tokens):
    
    result = tokens[:]
    
    while "(" in result:
        found = find_innermost_parentheses(result)
        
        if found is None:
            break
        
        start, end = found
        
        inner = result[start+1:end]
        
        if not inner:
            raise CalculationError(
                code=ErrorCode.INVALID_EXPRESSION,
                message="empty parentheses"
            )
            
        value = calculate(inner)
        
        result[start:end+1] = [value]
    
    return result
    

def process_power(tokens):
    
    result = tokens[:]
    i = len(result) - 2
    
    while i > 0:
        if result[i] == "^":
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
    
    tokens = handle_unary_minus(tokens)
    
    tokens = process_parentheses(tokens)
    tokens = process_power(tokens)
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
