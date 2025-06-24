from tools.parser import Parser
from tools.tokenizer import tokenize
from tools.simplifier import collect_like_terms, rewrite_subtraction, unwrite_subtraction, flattened_sum
def main():
    # Example input
    expression = "3x-2x+5x+4-2+5y-3y"
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
    print(rewrite_subtraction(expression_tree))
    terms = flattened_sum(rewrite_subtraction(expression_tree))
    print([str(term) for term in terms])
if __name__ == "__main__":
    main()