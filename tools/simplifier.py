from tools.nodes import NumberNode, VariableNode, OperatorNode
def rewrite_subtraction(tree):
    # Rewrite subtraction in the expression tree to addition of negative numbers
    if isinstance(tree, OperatorNode):
        if tree.operator == '-':
            # Recursively rewrite both sides
            left = rewrite_subtraction(tree.left)
            right = rewrite_subtraction(tree.right)
            return OperatorNode('+', left, OperatorNode('*', NumberNode(-1), right))
        else:
            return OperatorNode(tree.operator, rewrite_subtraction(tree.left), rewrite_subtraction(tree.right))
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


def collect_like_terms(tree):
    # Recursively collect like terms from the expression tree including variables with coefficients
    pass