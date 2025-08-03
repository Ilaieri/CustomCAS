import re
operators = {"+", "-", "*", "/", "^","(",")"}
functions = {"sin", "cos", "tan", "log", "exp", "sqrt", "ln"}
def tokenize(expression):
    pattern=r"(?:sin|cos|tan|log|exp|sqrt|ln)|\d+\.?\d*|[a-zA-Z]+|\*\*|[+\-*/^()]"
    tokens = re.findall(pattern, expression)
    # Account for implied multiplication 
    i=0
    while i<len(tokens)-1:
        if tokens[i] not in operators and tokens[i+1] not in operators:
            tokens.insert(i+1, "*")
            i += 1
        elif tokens[i] == ")" and tokens[i+1] not in operators:
            tokens.insert(i+1, "*")
            i += 1
        elif tokens[i] not in operators and tokens[i+1] == "(" and tokens[i] not in functions:
            tokens.insert(i+1, "*")
            i += 1
        i += 1
    return tokens
# Example usage:
# print(tokenize("32x+5(2y-4)"))  # Output: ["32", "x", "+", "5", "*", "(", "2", "y", "-", "4", ")"]

    