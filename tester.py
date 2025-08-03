from tools.parser import Parser
from tools.tokenizer import tokenize
from tools.simplifier import normalize, flattened_sum,collect_like_terms,expand,collect_powers, rebuild_binary_tree
from tools.print_handler import print_flattened
def test():
    # Example input
    expression = "(x+5)*(x+2)"
    diff_expression = "x^2+7*x+10"
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
    # print(collect_like_terms(terms))
    print(collect_powers(rebuild_binary_tree(collect_like_terms(flattened_sum(expand(normalize(expression_tree)).simplify())))).simplify())
    print("Differentiating expression:", diff_expression)
    # Tokenize the differentiation expression
    diff_tokens = tokenize(diff_expression)
    # Parse the tokens into an expression tree
    diff_parser = Parser(diff_tokens)
    diff_expression_tree = diff_parser.parse()
    # Differentiate the expression tree with respect to 'x'
    differentiated_tree = expression_tree.differentiate('x')
    print("Differentiated Expression Tree:", differentiated_tree)
    simplified_diff_tree = differentiated_tree.simplify()
    print("Simplified Differentiated Expression Tree:", simplified_diff_tree)
if __name__ == "__main__":
    test()