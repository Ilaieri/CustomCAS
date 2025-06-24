class ExpressionNode:
    def __str__(self):
        return "ExpressionNode"
class NumberNode(ExpressionNode):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)
class VariableNode(ExpressionNode):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name
class OperatorNode(ExpressionNode):
    def __init__(self, operator, left, right):
        self.operator = operator
        self.left = left
        self.right = right

    def __str__(self):
        return f"({self.left} {self.operator} {self.right})"
# print(OperatorNode("+", NumberNode(1), VariableNode("x")))  #Test 