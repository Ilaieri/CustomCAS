import re
from tools.symbols import FUNCTIONS, CONSTANTS, COMMANDS
operators = {"+", "-", "*", "/", "^","(",")",","}

def tokenize(expression):
    functions_pattern = r"|".join(FUNCTIONS.keys())
    constants_pattern = r"|".join(CONSTANTS.keys())
    commands_pattern = r"|".join(COMMANDS.keys())
    pattern = r"(?:{})|\d+\.?\d*|[a-zA-Z]+|\*\*|[,+\-*/^()]".format(
        "|".join([functions_pattern, constants_pattern, commands_pattern])
    )
    tokens = re.findall(pattern, expression)

    callable_names = set(FUNCTIONS.keys()) | set(COMMANDS.keys())

    i = 0
    while i < len(tokens) - 1:
        a = tokens[i]
        b = tokens[i+1]
        if a not in operators and b not in operators:
            tokens.insert(i+1, "*")
            i += 1
        elif a == ")" and b not in operators:
            tokens.insert(i+1, "*")
            i += 1
        elif (a not in operators or a == ")") and b == "(" and a not in callable_names:
            # only insert * if the left token is NOT a function/command
            tokens.insert(i+1, "*")
            i += 1
        i += 1
    return tokens


