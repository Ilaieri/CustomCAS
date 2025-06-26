from tools.parser import Parser
from tools.tokenizer import tokenize
from tools.simplifier import normalize, flattened_sum,collect_like_terms
from tools.print_handler import print_flattened
def main():
    # Example input
    expression = "5(x+4)+5(2x+4)"
    # Tokenize the input
    tokens = tokenize(expression)
    # Parse the tokens into an expression tree
    parser = Parser(tokens)
    expression_tree = parser.parse()
    # Print the expression tree
    print("Expression Tree:", expression_tree)
    # Evaluate the expression tree with a variable
    variables = {}
    # try:
    #     result = expression_tree.evaluate(variables)
    #     print("Result:", result)
    # except ValueError as e:
    #     print("Error:", e)
    # # Simplify the expression tree
    # simplified_tree = expression_tree.simplify()
    # print("Simplified Expression Tree:", simplified_tree)
    # # Evaluate the simplified expression tree
    # try:
    #     simplified_result = simplified_tree.evaluate(variables)
    #     print("Simplified Result:", simplified_result)
    # except ValueError as e:
    #     print("Error:", e)
    # Collect like terms from the expression tree
    print(normalize(expression_tree).simplify())
    terms = flattened_sum(normalize(expression_tree))

    # recursively print all terms to account for nested structures
    print(print_flattened(terms))
    print(collect_like_terms(terms))
if __name__ == "__main__":
    main()