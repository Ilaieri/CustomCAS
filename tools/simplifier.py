from tools.nodes import NumberNode, VariableNode, OperatorNode,PowerNode, FunctionNode, CommandNode
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
    elif isinstance(tree, PowerNode):
        return PowerNode(normalize(tree.base), normalize(tree.exponent))
    elif isinstance(tree, FunctionNode):
        return FunctionNode(tree.function_name, normalize(tree.argument))
    elif isinstance(tree, CommandNode):
        return CommandNode(tree.command_name, normalize(tree.argument), tree.extra)
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
    """
    Returns (coefficient, variables) where variables is a sorted tuple of (var, exponent).
    Handles NumberNode, VariableNode, PowerNode, and products thereof.
    """
    factors = flattened_product(term)
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

def collect_like_terms(terms):
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
                    var_part = OperatorNode('*', var_part, v)
            # Attach coefficient
            if coeff == 1:
                result.append(var_part)
            else:
                result.append(OperatorNode('*', NumberNode(coeff), var_part))
    return result
def expand(tree):
    if isinstance(tree,OperatorNode):
        if tree.operator=="+":
            return OperatorNode("+", expand(tree.left), expand(tree.right))
        elif tree.operator=="*":
            if isinstance(tree.left,OperatorNode) and tree.left.operator=="+" and isinstance(tree.right,OperatorNode) and tree.right.operator=="+":
                left_terms = flattened_sum(tree.left.simplify())
                right_terms = flattened_sum(tree.right.simplify())
                expanded_terms = []
                for l in left_terms:
                    for r in right_terms:
                        expanded_terms.append(OperatorNode("*", l, r))
                # Build a balanced binary tree with addition operators
                result = None
                for term in expanded_terms:
                    if result is None:
                        result = term
                    else:
                        result = OperatorNode("+", result, term)
                return result

            elif isinstance(tree.left, OperatorNode) and tree.left.operator == "+":
                left_terms = flattened_sum(tree.left.simplify())
                right_factors = expand(tree.right)
                expanded_terms = []
                for l in left_terms:
                    expanded_terms.append(OperatorNode("*", l, right_factors))
                result = None
                for term in expanded_terms:
                    if result is None:
                        result = term
                    else:
                        result = OperatorNode("+", result, term)
                return result
            elif isinstance(tree.right, OperatorNode) and tree.right.operator == "+":
                left_factors = expand(tree.left)
                right_terms = flattened_sum(tree.right.simplify())
                expanded_terms = []
                for r in right_terms:
                    expanded_terms.append(OperatorNode("*", left_factors, r))
                result = None
                for term in expanded_terms:
                    if result is None:
                        result = term
                    else:
                        result = OperatorNode("+", result, term)
                return result
            elif isinstance(tree.right, OperatorNode) and tree.right.operator == "+":
                left_factors = expand(tree.left)
                right_terms = flattened_sum(tree.right.simplify())
                expanded_terms = []
                for r in right_terms:
                    expanded_terms.append(OperatorNode("*", left_factors, r))
                result = None
                for term in expanded_terms:
                    if result is None:
                        result = term
                    else:
                        result = OperatorNode("+", result, term)
                return result
            else:
                left_factors = expand(tree.left)
                right_factors = expand(tree.right)
                return OperatorNode("*", left_factors, right_factors)
    return tree.simplify()
def rebuild_binary_tree(terms):
    # for list of terms being summed
    if not terms:
        return None
    if len(terms) == 1:
        return terms[0]
    
    mid = len(terms) // 2
    left = rebuild_binary_tree(terms[:mid])
    right = rebuild_binary_tree(terms[mid:])
    
    return OperatorNode("+", left, right)
def collect_powers(tree):
    # Handle sums: flatten and process each term, then rebuild as a binary tree
    print("Collecting powers from:", tree)
    if isinstance(tree, OperatorNode) and tree.operator == "+":
        terms = flattened_sum(tree)
        processed_terms = [collect_powers(term) for term in terms]
        # Rebuild as binary tree
        result = processed_terms[0]
        for term in processed_terms[1:]:
            result = OperatorNode("+", result, term)
        return result

    # Handle products: flatten, count variables, sum exponents, rebuild as binary tree
    elif isinstance(tree, OperatorNode) and tree.operator == "*":
        factors = flattened_product(tree)
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
                    others.append(collect_powers(factor))
            else:
                others.append(collect_powers(factor))
        # Build variable part
        var_nodes = []
        for var, exp in sorted(var_counts.items()):
            if exp == 1:
                var_nodes.append(VariableNode(var))
            else:
                var_nodes.append(PowerNode(VariableNode(var), NumberNode(exp)))
        # Add any "other" factors (e.g., functions, complex nodes)
        var_nodes.extend(others)
        # Build product as binary tree
        if not var_nodes:
            return NumberNode(coeff)
        result = NumberNode(coeff)
        for node in var_nodes:
            result = OperatorNode("*", result, node)
        return result

    # For PowerNode, recursively process base and exponent
    elif isinstance(tree, PowerNode):
        return PowerNode(collect_powers(tree.base), collect_powers(tree.exponent))

    # For NumberNode or VariableNode, return as is
    else:
        return tree