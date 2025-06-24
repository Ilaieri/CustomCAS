import re
def tokenize(expression):
    pattern=r'\d+\.?\d*|[a-zA-Z]|\*\*|[+\-*/^()]'
    tokens = re.findall(pattern, expression)
    for i in range(len(tokens)):
        if tokens[i].isdigit() :
            tokens[i] = str(int(tokens[i]))
    return tokens
# Example usage:
# print(tokenize("32x+5*(2y-4)"))  # Output: ['32', 'x', '+', '5', '*', '(', '2', 'y', '-', '4', ')']

    