from typing import List, Tuple, Any, Optional

from tools.nodes import NumberNode, VariableNode, PowerNode, ExpressionNode, AddNode, MulNode
from collections import defaultdict

def normalize(tree: ExpressionNode) -> ExpressionNode:
    """Wrapper for polymorphic normalize()."""
    return tree.normalize()

def unwrite_subtraction(tree: ExpressionNode) -> ExpressionNode:
    """Wrapper for polymorphic unwrite_subtraction()."""
    return tree.unwrite_subtraction()

def flattened_sum(tree: ExpressionNode) -> List[ExpressionNode]:
    """Wrapper for polymorphic flattened_sum()."""
    return tree.flattened_sum()

def flattened_product(tree: ExpressionNode) -> List[ExpressionNode]:
    """Wrapper for polymorphic flattened_product()."""
    return tree.flattened_product()

def expand(tree: ExpressionNode) -> ExpressionNode:
    """Wrapper for polymorphic expand()."""
    return tree.expand()

def collect_powers(tree: ExpressionNode) -> ExpressionNode:
    """Wrapper for polymorphic collect_powers()."""
    return tree.collect_powers()

def extract_coefficient_and_vars(term: ExpressionNode) -> Tuple[float, Tuple[Any, ...]]:
    """
    Returns (coefficient, variables) where variables is a sorted tuple of (var, exponent).
    Handles NumberNode, VariableNode, PowerNode, and products thereof.
    """
    factors = term.flattened_product()
    coefficient = 1.0
    variables = []
    for factor in factors:
        if isinstance(factor, NumberNode):
            coefficient *= factor.value
        elif isinstance(factor, VariableNode):
            # x is x^1
            variables.append((factor.name, 1))
        elif isinstance(factor, PowerNode):
            # x^n
            base = factor.base
            exp = factor.exponent
            # Only handle VariableNode^NumberNode for now
            if isinstance(base, VariableNode) and isinstance(exp, NumberNode):
                variables.append((base.name, exp.value))
            else:
                # For more complex powers, use their string representation
                variables.append((str(factor), 1))
        else:
            # For any other node, use its string representation
            variables.append((str(factor), 1))
    # Sort variables for canonical form (so x^2*y == y*x^2)
    return coefficient, tuple(sorted(variables))

def collect_like_terms(terms: List[ExpressionNode]) -> List[ExpressionNode]:
    """
    Groups and sums terms with identical variable parts.
    """
    like_terms = defaultdict(float)
    for term in terms:
        coefficient, variables = extract_coefficient_and_vars(term)
        like_terms[variables] += coefficient

    # Build result as a list of nodes
    result = []
    for variables, coeff in like_terms.items():
        if not variables:  # constant term
            result.append(NumberNode(coeff))
        else:
            # Rebuild the variable part as a product of PowerNodes or VariableNodes
            var_nodes = []
            for var, exp in variables:
                if exp == 1:
                    var_nodes.append(VariableNode(var))
                else:
                    var_nodes.append(PowerNode(VariableNode(var), NumberNode(exp)))
            # Build product node
            if len(var_nodes) == 1:
                var_part = var_nodes[0]
            else:
                var_part = var_nodes[0]
                for v in var_nodes[1:]:
                    var_part = MulNode(var_part, v)
            # Attach coefficient
            if coeff == 1:
                result.append(var_part)
            else:
                result.append(MulNode(NumberNode(coeff), var_part))
    return result

def rebuild_binary_tree(terms: List[ExpressionNode]) -> Optional[ExpressionNode]:
    """
    Rebuilds a balanced binary addition tree from a flat list of summation terms.
    """
    if not terms:
        return None
    if len(terms) == 1:
        return terms[0]
    
    mid = len(terms) // 2
    left = rebuild_binary_tree(terms[:mid])
    right = rebuild_binary_tree(terms[mid:])
    
    return AddNode(left, right) # type: ignore