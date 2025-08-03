import math
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
    def differentiate(self, variable):
        return NumberNode(0)
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
    def differentiate(self, variable):
        if self.name == variable:
            return NumberNode(1)
        else:
            return NumberNode(0)
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
        # if isinstance(left_simplified, NumberNode) and left_simplified.value == 1 and self.operator == '^':
        #     return NumberNode(1)
        # if isinstance(right_simplified, NumberNode) and right_simplified.value == 0 and self.operator == '^':
        #     return NumberNode(1)
        # if isinstance(right_simplified, NumberNode) and right_simplified.value == 1 and self.operator == '^':
        #     return left_simplified
        # Only combine coefficients for multiplication
        if self.operator == '*' and isinstance(left_simplified, NumberNode) and isinstance(right_simplified, NumberNode):
            return NumberNode(left_simplified.value * right_simplified.value)
        if self.operator == '*' and isinstance(left_simplified, NumberNode) and isinstance(right_simplified, VariableNode):
            return OperatorNode('*', left_simplified, right_simplified)
        if self.operator == '*' and isinstance(right_simplified, NumberNode) and isinstance(left_simplified, VariableNode):
            return OperatorNode('*', right_simplified, left_simplified)
        if self.operator=="*" and isinstance(left_simplified,PowerNode) and isinstance(right_simplified,PowerNode):
            if left_simplified.base == right_simplified.base:
                return PowerNode(left_simplified.base, OperatorNode('+', left_simplified.exponent, right_simplified.exponent))
 

        return OperatorNode(self.operator, left_simplified, right_simplified)
    def differentiate(self, variable):
        if self.operator=="+":
            return OperatorNode("+", self.left.differentiate(variable), self.right.differentiate(variable))
        elif self.operator=="-":
            return OperatorNode("-", self.left.differentiate(variable), self.right.differentiate(variable))
        elif self.operator=="*":
            if isinstance(self.left, NumberNode):
                return OperatorNode("*", self.left, self.right.differentiate(variable))
            elif isinstance(self.right, NumberNode):
                return OperatorNode("*", self.left.differentiate(variable), self.right)
            else:
                return OperatorNode("+", OperatorNode("*", self.left, self.right.differentiate(variable)), OperatorNode("*", self.left.differentiate(variable), self.right))
        elif self.operator=="/":
            if isinstance(self.left, NumberNode):
                return OperatorNode("/", self.left, self.right.differentiate(variable))
            elif isinstance(self.right, NumberNode):
                return OperatorNode("/", self.left.differentiate(variable), self.right)
            else:
                return OperatorNode("/", self.left.differentiate(variable), self.right.differentiate(variable))
class PowerNode(ExpressionNode):
    def __init__(self, base, exponent):
        self.base = base
        self.exponent = exponent

    def __str__(self):
        return f"({self.base} ^ {self.exponent})"
    
    def evaluate(self, variables={}):
        base_val = self.base.evaluate(variables)
        exponent_val = self.exponent.evaluate(variables)
        return base_val ** exponent_val
    
    def simplify(self):
        base_simplified = self.base.simplify()
        exponent_simplified = self.exponent.simplify()
        if isinstance(base_simplified, NumberNode) and isinstance(exponent_simplified, NumberNode):
            return NumberNode(self.evaluate())
        if isinstance(base_simplified, NumberNode) and base_simplified.value == 0:
            return NumberNode(0)
        if isinstance(exponent_simplified, NumberNode) and exponent_simplified.value == 0:
            return NumberNode(1)
        if exponent_simplified.value == 1:
            return base_simplified
        return PowerNode(base_simplified, exponent_simplified)
    def differentiate(self, variable):
        if isinstance(self.base, VariableNode) and self.base.name == variable:
            if isinstance(self.exponent, VariableNode) and self.exponent.name == variable:
                raise NotImplementedError("Differentiation with respect to a variable exponent is not implemented, will be added when logs are implemented")
        if isinstance(self.base, VariableNode) and self.base.name == variable:
            return OperatorNode("*",self.exponent, PowerNode(self.base, OperatorNode("-", self.exponent, NumberNode(1))))
        if isinstance(self.exponent, NumberNode) and self.exponent.value == 1:
            return self.base.differentiate(variable)
        if isinstance(self.exponent, NumberNode) and self.exponent.value == 0:
            return NumberNode(0)
class FunctionNode(ExpressionNode):
    def __init__(self, function_name, argument):
        self.function_name = function_name
        self.argument = argument

    def __str__(self):
        return f"{self.function_name}({self.argument})"
    def evaluate(self, variables={}):
        if self.function_name == "sin":
            return math.sin(self.argument.evaluate(variables))
        elif self.function_name == "cos":
            return math.cos(self.argument.evaluate(variables))
        elif self.function_name == "tan":
            return math.tan(self.argument.evaluate(variables))
        elif self.function_name == "log":
            return math.log(self.argument.evaluate(variables))
        elif self.function_name == "exp":
            return math.exp(self.argument.evaluate(variables))
        elif self.function_name == "sqrt":
            return math.sqrt(self.argument.evaluate(variables))
        elif self.function_name == "ln":
            return math.log(self.argument.evaluate(variables))
        raise ValueError(f"Unknown function: {self.function_name}")
    def simplify(self):
        argument_simplified = self.argument.simplify()
        if isinstance(argument_simplified, NumberNode):
            return NumberNode(self.evaluate())
        return FunctionNode(self.function_name, argument_simplified)
    def differentiate(self, variable):
        if self.function_name == "sin":
            return OperatorNode("*", self.argument.differentiate(variable), FunctionNode("cos", self.argument))
        elif self.function_name == "cos":
            return OperatorNode("*", self.argument.differentiate(variable), FunctionNode("sin", self.argument))
        elif self.function_name == "tan":
            return OperatorNode("*", self.argument.differentiate(variable), FunctionNode("sec", self.argument))
        elif self.function_name == "log":
            return OperatorNode("*", self.argument.differentiate(variable), FunctionNode("1/x", self.argument))
        elif self.function_name == "exp":
            return OperatorNode("*", self.argument.differentiate(variable), FunctionNode("exp", self.argument))
        elif self.function_name == "sqrt":
            return OperatorNode("*", self.argument.differentiate(variable), FunctionNode("1/(2*sqrt(x))", self.argument))
        elif self.function_name == "ln":
            return OperatorNode("*", self.argument.differentiate(variable), FunctionNode("1/x", self.argument))
        raise ValueError(f"Unknown function: {self.function_name}")