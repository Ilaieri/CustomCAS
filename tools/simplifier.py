from tools.nodes import NumberNode, VariableNode, OperatorNode
from collections import defaultdict
def normalize(tree):
    if isinstance(tree, OperatorNode):
        if tree.operator == '-':
            # Normalize subtraction by rewriting it as addition of the negative
            left = normalize(tree.left)
            right = normalize(tree.right)
            return OperatorNode('+', left, OperatorNode('*', NumberNode(-1), right))
        elif tree.operator == '/':
            # Normalize division by rewriting it as multiplication by the power of -1
            left = normalize(tree.left)
            right = normalize(tree.right)
            return OperatorNode('*', left, OperatorNode('^', right, NumberNode(-1)))
        else:
            return OperatorNode(tree.operator, normalize(tree.left), normalize(tree.right))
    elif isinstance(tree, NumberNode) or isinstance(tree, VariableNode):
        return tree
    else:
        raise ValueError("Unsupported node type in expression tree")
def unwrite_subtraction(tree):
    if isinstance(tree,OperatorNode):
        if tree.operator=="+":
            if isinstance(tree.right, OperatorNode) and tree.right.operator == '*':
                if isinstance(tree.right.left, NumberNode) and tree.right.left.value < 0:
                    return OperatorNode('-', tree.left, tree.right.right)
        return OperatorNode(tree.operator, unwrite_subtraction(tree.left), unwrite_subtraction(tree.right))
    elif isinstance(tree, NumberNode) or isinstance(tree, VariableNode):
        return tree
    else:
        raise ValueError("Unsupported node type in expression tree")

def flattened_sum(tree):
    if isinstance(tree, OperatorNode) and tree.operator == '+':
        left_terms = flattened_sum(tree.left)
        right_terms = flattened_sum(tree.right)
        return left_terms + right_terms
    else:
        return [tree]
def flattened_product(tree):
    if isinstance(tree, OperatorNode) and tree.operator == '*':
        left_factors = flattened_product(tree.left)
        right_factors = flattened_product(tree.right)
        return left_factors + right_factors
    else:
        return [tree]

def extract_coefficient_and_vars(term):
    term=flattened_product(term)
    coefficient = 1
    variables=[]
    for factor in term:
        if isinstance(factor, NumberNode):
            coefficient *= factor.value
        elif isinstance(factor, VariableNode):
            variables.append(factor.name)
        # Add support for x^2 or similar terms in future
    return coefficient, sorted(variables)


def collect_like_terms(terms):
    like_terms = defaultdict(float)
    for term in terms:
        coefficient, variables = extract_coefficient_and_vars(term)
        like_terms[tuple(variables)] += coefficient
    
    return like_terms

