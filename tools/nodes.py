class ExpressionNode:
    def __str__(self):
        return "ExpressionNode"
class NumberNode(ExpressionNode):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)
    
    def evaluate(self,variables=None):
        return self.value
    def simplify(self):
        return self
class VariableNode(ExpressionNode):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name
    
    def evaluate(self, variables={}):
        if self.name in variables:
            return variables[self.name]
        else:
            return VariableNode(self.name)
        raise ValueError(f"Variable '{self.name}' not found in the provided variables.")
    def simplify(self):
        return self
class OperatorNode(ExpressionNode):
    def __init__(self, operator, left, right):
        self.operator = operator
        self.left = left
        self.right = right

    def __str__(self):
        return f"({self.left} {self.operator} {self.right})"
    
    def evaluate(self, variables={}):
        left_val=self.left.evaluate(variables)
        right_val=self.right.evaluate(variables)
        if self.operator == '+':
            return left_val + right_val
        elif self.operator == '-':
            return left_val - right_val
        elif self.operator == '*':
            return left_val * right_val
        elif self.operator == '/':
            if right_val == 0:
                raise ValueError("Division by zero is not allowed.")
            return left_val / right_val
        elif self.operator == '^':
            return left_val ** right_val
        else:
            raise ValueError(f"Unknown operator: {self.operator}")
    def simplify(self):
        left_simplified=self.left.simplify()
        right_simplified=self.right.simplify()
        # Handle cases where both sides are numbers
        if isinstance(left_simplified, NumberNode) and isinstance(right_simplified, NumberNode):
            return NumberNode(self.evaluate())
        # Handle cases where one side is a number and the other is a variable or expression
        if isinstance(left_simplified, NumberNode) and left_simplified.value == 0 and self.operator in ('+', '-'):
            return right_simplified
        if isinstance(right_simplified, NumberNode) and right_simplified.value == 0 and self.operator == '+':
            return left_simplified
        if isinstance(left_simplified, NumberNode) and left_simplified.value == 1 and self.operator == '*':
            return right_simplified
        if isinstance(right_simplified, NumberNode) and right_simplified.value == 1 and self.operator == '*':
            return left_simplified
        if (isinstance(left_simplified, NumberNode) and left_simplified.value == 0 or isinstance(right_simplified, NumberNode) and right_simplified.value == 0) and self.operator == '*':
            return NumberNode(0)
        if isinstance(left_simplified, NumberNode) and left_simplified.value == 1 and self.operator == '^':
            return NumberNode(1)
        if isinstance(right_simplified, NumberNode) and right_simplified.value == 0 and self.operator == '^':
            return NumberNode(1)
        if isinstance(right_simplified, NumberNode) and right_simplified.value == 1 and self.operator == '^':
            return left_simplified
        # Only combine coefficients for multiplication
        if self.operator == '*' and isinstance(left_simplified, NumberNode) and isinstance(right_simplified, NumberNode):
            return NumberNode(left_simplified.value * right_simplified.value)
        if self.operator == '*' and isinstance(left_simplified, NumberNode) and isinstance(right_simplified, VariableNode):
            return OperatorNode('*', left_simplified, right_simplified)
        if self.operator == '*' and isinstance(right_simplified, NumberNode) and isinstance(left_simplified, VariableNode):
            return OperatorNode('*', right_simplified, left_simplified)
 

        return OperatorNode(self.operator, left_simplified, right_simplified)
    
        

# print(OperatorNode("+", NumberNode(1), VariableNode("x")))  #Test