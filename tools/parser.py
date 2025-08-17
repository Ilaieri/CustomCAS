from tools.nodes import *
from tools.symbols import CONSTANTS, FUNCTIONS, COMMANDS
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token_index = 0
    def current_token(self):
        if self.current_token_index<len(self.tokens):
            return self.tokens[self.current_token_index]
        return None
    def advance(self):
        if self.current_token_index < len(self.tokens):
            self.current_token_index += 1
    def parse(self):
        if not self.tokens:
            return None
        return self.parse_expression()
    def parse_expression(self):
        node= self.parse_term()
        while self.current_token() in ('+', '-'):
            operator=self.current_token()
            self.advance()
            right=self.parse_term()
            node = OperatorNode(operator, node, right)
        return node
    def parse_term(self):
        node= self.parse_factor()
        while self.current_token() in ('*', '/'):
            operator=self.current_token()
            self.advance()
            right=self.parse_factor()
            node = OperatorNode(operator, node, right)
        return node
    def parse_factor(self):
        node = self.parse_primary()
        if self.current_token() == '^':
            self.advance()
            right = self.parse_factor()  # recursion for right-associativity
            node = PowerNode(node, right)
        return node
    def parse_primary(self):
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
    def isfloat(self, value):
        try:
            float(value)
            return True
        except ValueError:
            return False
    def parse_unary(self):
        # This method can be implemented if unary operators are needed
        # For now, we assume no unary operators like '-' or '+' at the start
        pass
    def parse_function(self):
        token = self.current_token()
        self.advance()
        if self.current_token()!="(":
            raise ValueError(f"Expected '(' after function {token}")
        self.advance()
        argument = self.parse_expression()
        if self.current_token() != ")":
            raise ValueError(f"Expected ')' after function argument for {token}")
        self.advance()
        return FunctionNode(token, argument)
    def parse_constant(self):
        token = self.current_token()
        if token in CONSTANTS:
            self.advance()
            return ConstantNode(token)
        raise ValueError(f"Unknown constant: {token}")
    def parse_command(self):
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


