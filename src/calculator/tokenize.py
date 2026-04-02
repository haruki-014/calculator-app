import re

def tokenize(user_input: str):
    return re.findall(r"\d+\.?\d*|[()+\*/%^]", user_input)