import math
from typing import Dict, Union, Any, List, Optional

class ExpressionNode:
    """Base class for all nodes in the Abstract Syntax Tree (AST)."""
    
    def __str__(self) -> str:
        return "ExpressionNode"
        
    def evaluate(self, variables: Dict[str, Union[int, float]] = None) -> Union[int, float]:
        raise NotImplementedError("This method should be implemented by subclasses.")
        
    def simplify(self) -> 'ExpressionNode':
        return self
        
    def differentiate(self, variable: str) -> 'ExpressionNode':
        raise NotImplementedError("This method should be implemented by subclasses.")
        
    def execute(self, variables: Dict[str, Union[int, float]] = None) -> 'ExpressionNode':
        return self

    # --- Polymorphic AST Manipulation Methods ---
    def normalize(self) -> 'ExpressionNode':
        """Normalizes subtraction/division."""
        return self

    def unwrite_subtraction(self) -> 'ExpressionNode':
        """Reverts normalized addition of negatives back to subtraction."""
        return self

    def flattened_sum(self) -> List['ExpressionNode']:
        """Flattens a tree of additions into a flat list of terms."""
        return [self]

    def flattened_product(self) -> List['ExpressionNode']:
        """Flattens a tree of multiplications into a flat list of factors."""
        return [self]

    def expand(self) -> 'ExpressionNode':
        """Expands products of sums."""
        return self.simplify()

    def collect_powers(self) -> 'ExpressionNode':
        """Collects repeated variables into power terms."""
        return self


class NumberNode(ExpressionNode):
    """Represents a numerical constant."""
    
    def __init__(self, value: Union[int, float]):
        self.value = value
        
    def __str__(self) -> str:
        return str(self.value)
    
    def evaluate(self, variables: Dict[str, Union[int, float]] = None) -> Union[int, float]:
        return self.value
        
    def differentiate(self, variable: str) -> ExpressionNode:
        return NumberNode(0)

class VariableNode(ExpressionNode):
    """Represents a mathematical variable (e.g., 'x', 'y')."""
    
    def __init__(self, name: str):
        self.name = name

    def __str__(self) -> str:
        return self.name
    
    def evaluate(self, variables: Dict[str, Union[int, float]] = None) -> Union[int, float, 'VariableNode']:
        if variables is None:
            variables = {}
        if self.name in variables:
            return variables[self.name]
        else:
            return VariableNode(self.name)
            
    def differentiate(self, variable: str) -> ExpressionNode:
        if self.name == variable:
            return NumberNode(1)
        else:
            return NumberNode(0)

class BinaryNode(ExpressionNode):
    """Base class for binary operators."""
    operator = "?"
    
    def __init__(self, left: ExpressionNode, right: ExpressionNode):
        self.left = left
        self.right = right

    def __str__(self) -> str:
        return f"({self.left} {self.operator} {self.right})"
        
    def execute(self, variables: Dict[str, Union[int, float]] = None) -> ExpressionNode:
        if variables is None:
            variables = {}
        return self.__class__(self.left.execute(variables), self.right.execute(variables))

class AddNode(BinaryNode):
    operator = "+"
    
    def evaluate(self, variables: Dict[str, Union[int, float]] = None) -> Union[int, float]:
        if variables is None: variables = {}
        return self.left.evaluate(variables) + self.right.evaluate(variables)
        
    def simplify(self) -> ExpressionNode:
        l = self.left.simplify()
        r = self.right.simplify()
        if isinstance(l, NumberNode) and isinstance(r, NumberNode):
            return NumberNode(l.value + r.value)
        if isinstance(l, NumberNode) and l.value == 0:
            return r
        if isinstance(r, NumberNode) and r.value == 0:
            return l
        return AddNode(l, r)

    def differentiate(self, variable: str) -> ExpressionNode:
        return AddNode(self.left.differentiate(variable), self.right.differentiate(variable))

    def normalize(self) -> ExpressionNode:
        return AddNode(self.left.normalize(), self.right.normalize())

    def unwrite_subtraction(self) -> ExpressionNode:
        # turn x + (-1 * y) into x - (1 * y) 
        if isinstance(self.right, MulNode) and isinstance(self.right.left, NumberNode) and self.right.left.value < 0:
            return SubNode(self.left.unwrite_subtraction(), self.right.right.unwrite_subtraction())
        return AddNode(self.left.unwrite_subtraction(), self.right.unwrite_subtraction())

    def flattened_sum(self) -> List[ExpressionNode]:
        return self.left.flattened_sum() + self.right.flattened_sum()

    def expand(self) -> ExpressionNode:
        return AddNode(self.left.expand(), self.right.expand())

    def collect_powers(self) -> ExpressionNode:
        terms = self.flattened_sum()
        processed_terms = [t.collect_powers() for t in terms]
        result = processed_terms[0]
        for term in processed_terms[1:]:
            result = AddNode(result, term)
        return result

class SubNode(BinaryNode):
    operator = "-"
    
    def evaluate(self, variables: Dict[str, Union[int, float]] = None) -> Union[int, float]:
        if variables is None: variables = {}
        return self.left.evaluate(variables) - self.right.evaluate(variables)

    def simplify(self) -> ExpressionNode:
        l = self.left.simplify()
        r = self.right.simplify()
        if isinstance(l, NumberNode) and isinstance(r, NumberNode):
            return NumberNode(l.value - r.value)
        if isinstance(r, NumberNode) and r.value == 0:
            return l
        if isinstance(l, NumberNode) and l.value == 0:
            return MulNode(NumberNode(-1), r)
        return SubNode(l, r)

    def differentiate(self, variable: str) -> ExpressionNode:
        return SubNode(self.left.differentiate(variable), self.right.differentiate(variable))

    def normalize(self) -> ExpressionNode:
        # Convert A - B into A + (-1 * B)
        return AddNode(self.left.normalize(), MulNode(NumberNode(-1), self.right.normalize()))

    def unwrite_subtraction(self) -> ExpressionNode:
        return SubNode(self.left.unwrite_subtraction(), self.right.unwrite_subtraction())
        
    def expand(self) -> ExpressionNode:
        return SubNode(self.left.expand(), self.right.expand())

    def collect_powers(self) -> ExpressionNode:
        return SubNode(self.left.collect_powers(), self.right.collect_powers())

class MulNode(BinaryNode):
    operator = "*"
    
    def evaluate(self, variables: Dict[str, Union[int, float]] = None) -> Union[int, float]:
        if variables is None: variables = {}
        return self.left.evaluate(variables) * self.right.evaluate(variables)

    def simplify(self) -> ExpressionNode:
        l = self.left.simplify()
        r = self.right.simplify()
        if isinstance(l, NumberNode) and isinstance(r, NumberNode):
            return NumberNode(l.value * r.value)
        if isinstance(l, NumberNode) and l.value == 0: return NumberNode(0)
        if isinstance(r, NumberNode) and r.value == 0: return NumberNode(0)
        if isinstance(l, NumberNode) and l.value == 1: return r
        if isinstance(r, NumberNode) and r.value == 1: return l
        
        if isinstance(l, NumberNode) and isinstance(r, VariableNode):
            return MulNode(l, r)
        if isinstance(r, NumberNode) and isinstance(l, VariableNode):
            return MulNode(r, l)

        if isinstance(l, PowerNode) and isinstance(r, PowerNode):
            if str(l.base) == str(r.base):
                return PowerNode(l.base, AddNode(l.exponent, r.exponent))
                
        return MulNode(l, r)

    def differentiate(self, variable: str) -> ExpressionNode:
        if isinstance(self.left, NumberNode):
            return MulNode(self.left, self.right.differentiate(variable))
        if isinstance(self.right, NumberNode):
            return MulNode(self.left.differentiate(variable), self.right)
        return AddNode(MulNode(self.left, self.right.differentiate(variable)), MulNode(self.left.differentiate(variable), self.right))

    def normalize(self) -> ExpressionNode:
        return MulNode(self.left.normalize(), self.right.normalize())

    def unwrite_subtraction(self) -> ExpressionNode:
        return MulNode(self.left.unwrite_subtraction(), self.right.unwrite_subtraction())

    def flattened_product(self) -> List[ExpressionNode]:
        return self.left.flattened_product() + self.right.flattened_product()

    def expand(self) -> ExpressionNode:
        if isinstance(self.left, AddNode) and isinstance(self.right, AddNode):
            left_terms = self.left.simplify().flattened_sum()
            right_terms = self.right.simplify().flattened_sum()
            expanded_terms = []
            for l in left_terms:
                for r in right_terms:
                    expanded_terms.append(MulNode(l, r))
            result = None
            for term in expanded_terms:
                if result is None: result = term
                else: result = AddNode(result, term)
            return result
        elif isinstance(self.left, AddNode):
            left_terms = self.left.simplify().flattened_sum()
            right_factors = self.right.expand()
            expanded_terms = [MulNode(l, right_factors) for l in left_terms]
            result = None
            for term in expanded_terms:
                if result is None: result = term
                else: result = AddNode(result, term)
            return result
        elif isinstance(self.right, AddNode):
            left_factors = self.left.expand()
            right_terms = self.right.simplify().flattened_sum()
            expanded_terms = [MulNode(left_factors, r) for r in right_terms]
            result = None
            for term in expanded_terms:
                if result is None: result = term
                else: result = AddNode(result, term)
            return result
        else:
            return MulNode(self.left.expand(), self.right.expand())

    def collect_powers(self) -> ExpressionNode:
        from collections import defaultdict
        factors = self.flattened_product()
        coeff = 1.0
        var_counts = defaultdict(float)
        others = []
        for factor in factors:
            if isinstance(factor, NumberNode):
                coeff *= factor.value
            elif isinstance(factor, VariableNode):
                var_counts[factor.name] += 1
            elif isinstance(factor, PowerNode):
                base = factor.base
                exp = factor.exponent
                if isinstance(base, VariableNode) and isinstance(exp, NumberNode):
                    var_counts[base.name] += exp.value
                else:
                    others.append(factor.collect_powers())
            else:
                others.append(factor.collect_powers())
                
        var_nodes = []
        for var, exp in sorted(var_counts.items()):
            if exp == 1:
                var_nodes.append(VariableNode(var))
            else:
                var_nodes.append(PowerNode(VariableNode(var), NumberNode(exp)))
        var_nodes.extend(others)
        
        if not var_nodes:
            return NumberNode(coeff)
        result: ExpressionNode = NumberNode(coeff)
        for node in var_nodes:
            result = MulNode(result, node)
        return result

class DivNode(BinaryNode):
    operator = "/"
    
    def evaluate(self, variables: Dict[str, Union[int, float]] = None) -> Union[int, float]:
        if variables is None: variables = {}
        r_val = self.right.evaluate(variables)
        if r_val == 0: raise ValueError("Division by zero")
        return self.left.evaluate(variables) / r_val

    def simplify(self) -> ExpressionNode:
        l = self.left.simplify()
        r = self.right.simplify()
        if isinstance(l, NumberNode) and isinstance(r, NumberNode):
            return NumberNode(l.value / r.value)
        return DivNode(l, r)

    def differentiate(self, variable: str) -> ExpressionNode:
        u_prime_v = MulNode(self.left.differentiate(variable), self.right)
        u_v_prime = MulNode(self.left, self.right.differentiate(variable))
        numerator = SubNode(u_prime_v, u_v_prime)
        denominator = PowerNode(self.right, NumberNode(2))
        return DivNode(numerator, denominator)

    def normalize(self) -> ExpressionNode:
        return MulNode(self.left.normalize(), PowerNode(self.right.normalize(), NumberNode(-1)))

    def unwrite_subtraction(self) -> ExpressionNode:
        return DivNode(self.left.unwrite_subtraction(), self.right.unwrite_subtraction())
        
    def expand(self) -> ExpressionNode:
        return DivNode(self.left.expand(), self.right.expand())

    def collect_powers(self) -> ExpressionNode:
        return DivNode(self.left.collect_powers(), self.right.collect_powers())

class PowerNode(BinaryNode):
    operator = "^"
    
    def __init__(self, base: ExpressionNode, exponent: ExpressionNode):
        super().__init__(base, exponent)
    
    @property
    def base(self): return self.left
    @property
    def exponent(self): return self.right

    def evaluate(self, variables: Dict[str, Union[int, float]] = None) -> Union[int, float]:
        if variables is None: variables = {}
        return self.base.evaluate(variables) ** self.exponent.evaluate(variables) # type: ignore

    def simplify(self) -> ExpressionNode:
        b = self.base.simplify()
        e = self.exponent.simplify()
        if isinstance(b, NumberNode) and isinstance(e, NumberNode):
            return NumberNode(b.value ** e.value)
        if isinstance(b, NumberNode) and b.value == 0: return NumberNode(0)
        if isinstance(e, NumberNode) and e.value == 0: return NumberNode(1)
        if isinstance(e, NumberNode) and e.value == 1: return b
        return PowerNode(b, e)

    def differentiate(self, variable: str) -> ExpressionNode:
        if isinstance(self.base, VariableNode) and self.base.name == variable:
            if isinstance(self.exponent, VariableNode) and self.exponent.name == variable:
                raise NotImplementedError()
            return MulNode(self.exponent, PowerNode(self.base, SubNode(self.exponent, NumberNode(1))))
        if isinstance(self.exponent, NumberNode) and self.exponent.value == 1:
            return self.base.differentiate(variable)
        if isinstance(self.exponent, NumberNode) and self.exponent.value == 0:
            return NumberNode(0)
        return NumberNode(0)

    def normalize(self) -> ExpressionNode:
        return PowerNode(self.base.normalize(), self.exponent.normalize())

    def unwrite_subtraction(self) -> ExpressionNode:
        return PowerNode(self.base.unwrite_subtraction(), self.exponent.unwrite_subtraction())

    def expand(self) -> ExpressionNode:
        return PowerNode(self.base.expand(), self.exponent.expand())

    def collect_powers(self) -> ExpressionNode:
        return PowerNode(self.base.collect_powers(), self.exponent.collect_powers())


class FunctionNode(ExpressionNode):
    def __init__(self, function_name: str, argument: ExpressionNode):
        self.function_name = function_name
        self.argument = argument

    def __str__(self) -> str:
        return f"{self.function_name}({self.argument})"
        
    def evaluate(self, variables: Dict[str, Union[int, float]] = None) -> Union[int, float]:
        if variables is None:
            variables = {}
        arg_val = self.argument.evaluate(variables)
        if self.function_name == "sin": return math.sin(arg_val) # type: ignore
        elif self.function_name == "cos": return math.cos(arg_val) # type: ignore
        elif self.function_name == "tan": return math.tan(arg_val) # type: ignore
        elif self.function_name == "log": return math.log(arg_val) # type: ignore
        elif self.function_name == "exp": return math.exp(arg_val) # type: ignore
        elif self.function_name == "sqrt": return math.sqrt(arg_val) # type: ignore
        elif self.function_name == "ln": return math.log(arg_val) # type: ignore
        raise ValueError(f"Unknown function: {self.function_name}")
        
    def simplify(self) -> ExpressionNode:
        argument_simplified = self.argument.simplify()
        if isinstance(argument_simplified, NumberNode):
            return NumberNode(self.evaluate())
        return FunctionNode(self.function_name, argument_simplified)
        
    def differentiate(self, variable: str) -> ExpressionNode:
        if self.function_name == "sin":
            return MulNode(self.argument.differentiate(variable), FunctionNode("cos", self.argument))
        elif self.function_name == "cos":
            # d/dx cos(u) = -sin(u) * u'
            return MulNode(MulNode(NumberNode(-1), self.argument.differentiate(variable)), FunctionNode("sin", self.argument))
        elif self.function_name == "tan":
            # d/dx tan(u) = sec^2(u) * u' = (1 / cos^2(u)) * u'
            sec_squared = DivNode(NumberNode(1), PowerNode(FunctionNode("cos", self.argument), NumberNode(2)))
            return MulNode(self.argument.differentiate(variable), sec_squared)
        elif self.function_name in ["log", "ln"]:
            # d/dx ln(u) = (1 / u) * u'
            return MulNode(self.argument.differentiate(variable), DivNode(NumberNode(1), self.argument))
        elif self.function_name == "exp":
            # d/dx exp(u) = exp(u) * u'
            return MulNode(self.argument.differentiate(variable), FunctionNode("exp", self.argument))
        elif self.function_name == "sqrt":
            # d/dx sqrt(u) = (1 / (2 * sqrt(u))) * u'
            two_sqrt_u = MulNode(NumberNode(2), FunctionNode("sqrt", self.argument))
            return MulNode(self.argument.differentiate(variable), DivNode(NumberNode(1), two_sqrt_u))
        raise ValueError(f"Unknown function: {self.function_name}")
        
    def execute(self, variables: Dict[str, Union[int, float]] = None) -> ExpressionNode:
        if variables is None:
            variables = {}
        return FunctionNode(self.function_name, self.argument.execute(variables))

    def normalize(self) -> ExpressionNode:
        return FunctionNode(self.function_name, self.argument.normalize())


class ConstantNode(ExpressionNode):
    def __init__(self, constant_name: str):
        self.constant_name = constant_name
        
    def __str__(self) -> str:
        if self.constant_name in ["pi", "π"]:
            return "π"
        elif self.constant_name == "phi":
            return "φ"
        else:
            return self.constant_name
            
    def evaluate(self, variables: Dict[str, Union[int, float]] = None) -> Union[int, float]:
        if self.constant_name in ["pi", "π"]: return math.pi
        elif self.constant_name == "e": return math.e
        elif self.constant_name == "phi": return (1 + 5 ** 0.5) / 2
        raise ValueError(f"Unknown constant: {self.constant_name}")
        
    def differentiate(self, variable: str) -> ExpressionNode:
        return NumberNode(0)


class CommandNode(ExpressionNode):
    def __init__(self, command_name: str, argument: ExpressionNode, extra: str = None):
        self.command_name = command_name
        self.argument = argument
        self.extra = extra
        
    def __str__(self) -> str:
        if self.extra is not None:
            return f"{self.command_name}({self.argument}, {self.extra})"
        return f"{self.command_name}({self.argument})"
        
    def execute(self, variables: Dict[str, Union[int, float]] = None) -> ExpressionNode:
        from tools.simplifier import (
            normalize,
            flattened_sum,
            collect_like_terms,
            expand,
            collect_powers,
            rebuild_binary_tree,
        )
        cmd = self.command_name
        if cmd == "simplify":
            return self.argument.normalize().simplify()
        if cmd == "expand":
            return self.argument.normalize().expand().simplify()
        if cmd == "collect_like_terms":
            terms = self.argument.normalize().flattened_sum()
            grouped = collect_like_terms(terms)
            tree = rebuild_binary_tree(grouped)
            return tree.simplify()
        if cmd == "collect_powers":
            return self.argument.normalize().collect_powers().simplify()
        if cmd == "differentiate":
            var = self.extra or "x"
            return self.argument.differentiate(var).normalize().simplify()
            
        raise ValueError(f"Unknown command: {cmd}")

    def normalize(self) -> ExpressionNode:
        return CommandNode(self.command_name, self.argument.normalize(), self.extra)

# Alias for backwards compatibility if needed, but not recommended
OperatorNode = BinaryNode
