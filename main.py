from tools.parser import Parser
from tools.tokenizer import tokenize
from tools.simplifier import normalize, flattened_sum,collect_like_terms,expand,collect_powers, rebuild_binary_tree
from tools.print_handler import print_flattened
def main():
    while True:
        expression = input(">>")
        if expression.lower() in ["exit", "quit"]:
            print("Exiting the calculator.")
            break
        elif expression.strip() == "":
            print("Please enter a valid expression.")
            continue
        elif expression.lower() == "help":
            print("Available commands: differentiate(func,var), expand(func), simplify(func), exit, quit, help")
            continue
        tokenized_expression = tokenize(expression)
        parser = Parser(tokenized_expression)
        expression_tree = parser.parse()
        print("Parsed expression tree:", expression_tree)
        if expression_tree is None:
            print("Invalid expression.")
            continue
        executed_expression = normalize(expression_tree).execute()
        if executed_expression is None:
            print("Execution failed.")
            continue
        print(executed_expression)

        
if __name__ == "__main__":
    main()