from tools.nodes import NumberNode, VariableNode, OperatorNode
def rewrite_subtraction(tree):
    # Rewrite subtraction in the expression tree to addition of negative numbers
    if isinstance(tree, OperatorNode):
        if tree.operator == '-':
            return OperatorNode('+', tree.left, OperatorNode('*', NumberNode(-1), tree.right))
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
    if isinstance(tree, NumberNode):
        return tree
    if isinstance(tree, VariableNode):
        return tree 
    if isinstance(tree, OperatorNode):
        if tree.operator == '+':
            left_sum = flattened_sum(tree.left)
            right_sum = flattened_sum(tree.right)
            if isinstance(left_sum, NumberNode) and isinstance(right_sum, NumberNode):
                return NumberNode(left_sum.value + right_sum.value)
            elif isinstance(left_sum, VariableNode) and isinstance(right_sum, VariableNode) and left_sum.name == right_sum.name:
                return OperatorNode('*', NumberNode(2), left_sum)
            else:
                return OperatorNode('+', left_sum, right_sum)
        else:
            return OperatorNode(tree.operator, flattened_sum(tree.left), flattened_sum(tree.right))
def collect_like_terms(tree):
    # Recursively collect like terms from the expression tree including variables with coefficients
    pass