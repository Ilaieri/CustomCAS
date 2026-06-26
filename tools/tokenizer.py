import re
from typing import List, Set

from tools.symbols import FUNCTIONS, CONSTANTS, COMMANDS

operators: Set[str] = {"+", "-", "*", "/", "^", "(", ")", ","}

def tokenize(expression: str) -> List[str]:
    """
    Tokenizes a mathematical expression into a list of strings representing
    numbers, variables, operators, and functions.

    It also handles implicit multiplication by inserting '*' between appropriate
    tokens (e.g., '2x' becomes '2 * x', or '(x+1)(x+2)' becomes '(x+1) * (x+2)').

    Args:
        expression (str): The mathematical expression to tokenize.

    Returns:
        List[str]: A list of tokens.
    """
    reserved_words = list(FUNCTIONS.keys()) + list(CONSTANTS.keys()) + list(COMMANDS.keys())
    reserved_words.sort(key=len, reverse=True)
    
    pattern = r"(?:{})|\d+\.?\d*|[a-zA-Z]+|\*\*|[,+\-*/^()]".format(
        "|".join(reserved_words)
    )
    tokens = re.findall(pattern, expression)

    callable_names = set(FUNCTIONS.keys()) | set(COMMANDS.keys())

    i = 0
    while i < len(tokens) - 1:
        a = tokens[i]
        b = tokens[i+1]
        
        # Insert implicit multiplication
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
