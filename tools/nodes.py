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
class VariableNode(ExpressionNode):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name
    
    def evaluate(self, variables={}):
        if self.name in variables:
            return variables[self.name]
        raise ValueError(f"Variable '{self.name}' not found in the provided variables.")
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
# print(OperatorNode("+", NumberNode(1), VariableNode("x")))  #Test 