from typing import NoReturn
import sys

from tools.parser import Parser
from tools.tokenizer import tokenize
from tools.simplifier import normalize

def main() -> None:
    """
    Main REPL (Read-Eval-Print Loop) for the CustomCAS system.
    
    Prompts the user for mathematical expressions, tokenizes, parses,
    and executes commands on them. Handles exceptions gracefully to
    prevent the REPL from crashing on invalid input.
    """
    print("Welcome to CustomCAS! Type 'help' for commands or 'exit' to quit.")
    
    while True:
        try:
            expression = input(">> ")
            if not expression:
                continue
                
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
            
        except Exception as e:
            # Catching general Exception here is fine for a REPL to keep it alive.
            print(f"Error: {e}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting the calculator.")
        sys.exit(0)