import re

def tokenize(user_input: str):
    return re.findall(r"\d+\.?\d*|[a-zA-Z]+|[()+\-*/%^]", user_input)