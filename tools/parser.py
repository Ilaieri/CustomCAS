from typing import List, Optional

from tools.nodes import *
from tools.symbols import CONSTANTS, FUNCTIONS, COMMANDS

OPERATOR_CLASSES = {
    '+': AddNode,
    '-': SubNode,
    '*': MulNode,
    '/': DivNode,
    '^': PowerNode,
}

class Parser:
    """
    A recursive descent parser that takes a list of tokens and constructs
    an Abstract Syntax Tree (AST) representing the mathematical expression.
    """

    def __init__(self, tokens: List[str]):
        """
        Initializes the parser with a list of tokens.

        Args:
            tokens (List[str]): The tokens to parse.
        """
        self.tokens = tokens
        self.current_token_index = 0

    def current_token(self) -> Optional[str]:
        """Returns the current token, or None if at the end of the input."""
        if self.current_token_index < len(self.tokens):
            return self.tokens[self.current_token_index]
        return None

    def advance(self) -> None:
        """Advances the token index to the next token."""
        if self.current_token_index < len(self.tokens):
            self.current_token_index += 1

    def parse(self) -> Optional[ExpressionNode]:
        """
        Parses the entire token list.

        Returns:
            Optional[ExpressionNode]: The root node of the AST, or None if empty.
        """
        if not self.tokens:
            return None
        return self.parse_expression()

    def parse_expression(self) -> ExpressionNode:
        """
        Parses expressions (handles addition and subtraction).

        Returns:
            ExpressionNode: The parsed expression node.
        """
        node = self.parse_term()
        while self.current_token() in ('+', '-'):
            operator = self.current_token()
            self.advance()
            right = self.parse_term()
            node = OPERATOR_CLASSES[operator](node, right) # type: ignore
        return node

    def parse_term(self) -> ExpressionNode:
        """
        Parses terms (handles multiplication and division).

        Returns:
            ExpressionNode: The parsed term node.
        """
        node = self.parse_factor()
        while self.current_token() in ('*', '/'):
            operator = self.current_token()
            self.advance()
            right = self.parse_factor()
            node = OPERATOR_CLASSES[operator](node, right) # type: ignore
        return node

    def parse_factor(self) -> ExpressionNode:
        """
        Parses factors (handles exponentiation).

        Returns:
            ExpressionNode: The parsed factor node.
        """
        node = self.parse_primary()
        if self.current_token() == '^':
            self.advance()
            right = self.parse_factor()  # recursion for right-associativity
            node = PowerNode(node, right)
        return node

    def parse_primary(self) -> ExpressionNode:
        """
        Parses primary elements: numbers, variables, constants, functions, commands,
        or parenthesized expressions.

        Returns:
            ExpressionNode: The parsed primary node.
        
        Raises:
            ValueError: If the token is unexpected or missing.
        """
        token = self.current_token()
        if token is None:
            raise ValueError("Unexpected end of input")
        
        if token in CONSTANTS:
            return self.parse_constant()
        if token in FUNCTIONS:
            return self.parse_function()
        if token in COMMANDS:              
            return self.parse_command()
        if token.isdigit():
            self.advance()
            return NumberNode(int(token))
        elif self.isfloat(token):
            self.advance()
            return NumberNode(float(token))
        if token.isalpha():
            self.advance()
            return VariableNode(token)
        if token == '(':
            self.advance()
            node = self.parse_expression()
            if self.current_token() != ')':
                raise ValueError("Expected ')'")
            self.advance()
            return node
            
        raise ValueError(f"Unexpected token: {token}")

    def isfloat(self, value: str) -> bool:
        """Checks if a string can be converted to a float."""
        try:
            float(value)
            return True
        except ValueError:
            return False

    def parse_unary(self) -> None:
        """
        Placeholder for parsing unary operators (e.g., '-', '+').
        """
        pass

    def parse_function(self) -> FunctionNode:
        """
        Parses a mathematical function (e.g., sin, cos).

        Returns:
            FunctionNode: The parsed function node.
        
        Raises:
            ValueError: If parentheses are missing or mismatched.
        """
        token = self.current_token()
        self.advance()
        if self.current_token() != "(":
            raise ValueError(f"Expected '(' after function {token}")
        self.advance()
        argument = self.parse_expression()
        if self.current_token() != ")":
            raise ValueError(f"Expected ')' after function argument for {token}")
        self.advance()
        return FunctionNode(token, argument)

    def parse_constant(self) -> ConstantNode:
        """
        Parses a mathematical constant (e.g., pi, e).

        Returns:
            ConstantNode: The parsed constant node.
        
        Raises:
            ValueError: If the constant is unknown.
        """
        token = self.current_token()
        if token in CONSTANTS:
            self.advance()
            return ConstantNode(token)
        raise ValueError(f"Unknown constant: {token}")

    def parse_command(self) -> CommandNode:
        """
        Parses a CAS command (e.g., differentiate, simplify).

        Returns:
            CommandNode: The parsed command node.
        
        Raises:
            ValueError: If command syntax is invalid.
        """
        token = self.current_token()
        if token in COMMANDS:
            self.advance()
            if self.current_token() != "(":
                raise ValueError(f"Expected '(' after command {token}")
            self.advance()
            argument = self.parse_expression()
            extra = None
            if self.current_token() == ",":
                self.advance()
                extra_token = self.current_token()
                if extra_token is None or not extra_token.isalpha():
                    raise ValueError("Expected variable name after ',' in command")
                extra = extra_token
                self.advance()
            if self.current_token() != ")":
                raise ValueError(f"Expected ')' after command argument for {token}")
            self.advance()
            return CommandNode(token, argument, extra)
        raise ValueError(f"Unknown command: {token}")
