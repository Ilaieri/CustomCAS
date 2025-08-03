from tools.parser import Parser
from tools.tokenizer import tokenize
from tools.simplifier import normalize, flattened_sum,collect_like_terms,expand,collect_powers, rebuild_binary_tree
from tools.print_handler import print_flattened
def main():
    expression = "5sin(0)+24cos(0)"
    tokenized_expression = tokenize(expression)
    print("Tokenized Expression:", tokenized_expression)
    parser = Parser(tokenized_expression)
    expression_tree = parser.parse()
    print("Expression Tree:", expression_tree)
    print("Simplified Expression Tree:", expression_tree.simplify())

if __name__ == "__main__":
    main()