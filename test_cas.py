import pytest
import math
from tools.parser import Parser
from tools.tokenizer import tokenize
from tools.simplifier import normalize, flattened_sum, collect_like_terms, expand, collect_powers, rebuild_binary_tree
from tools.print_handler import print_flattened
from tools.nodes import AddNode, SubNode, MulNode, DivNode, PowerNode, FunctionNode, CommandNode

def parse_expr(expression):
    return Parser(tokenize(expression)).parse()

def test_parse_expression():
    tree = parse_expr("(x+5)*(x+2)")
    assert str(tree) == "((x + 5) * (x + 2))"

def test_normalize_and_simplify():
    tree = parse_expr("(x+5)*(x+2)")
    simplified = tree.normalize().simplify()
    assert str(simplified) == "((x + 5) * (x + 2))"

def test_flattened_terms():
    tree = parse_expr("(x+5)*(x+2)")
    terms = tree.normalize().flattened_sum()
    flattened_str = print_flattened(terms)
    assert flattened_str == ['((x + 5) * (x + 2))']

def test_expand_and_collect():
    tree = parse_expr("(x+5)*(x+2)")
    
    # Process expression: expand, collect like terms, build binary tree, collect powers
    expanded = tree.normalize().expand().simplify()
    terms = expanded.flattened_sum()
    like_terms = collect_like_terms(terms)
    tree_from_terms = rebuild_binary_tree(like_terms)
    final_expr = tree_from_terms.collect_powers().simplify()
    
    assert str(final_expr) == "(((x ^ 2.0) + (7.0 * x)) + 10.0)"

def test_differentiation_polynomial():
    tree = parse_expr("(x+5)*(x+2)")
    diff_tree = tree.differentiate('x')
    assert str(diff_tree) == "(((x + 5) * (1 + 0)) + ((1 + 0) * (x + 2)))"
    
    simplified_diff_tree = diff_tree.simplify()
    assert str(simplified_diff_tree) == "((x + 5) + (x + 2))"

def test_evaluation():
    # Test variables, constants, and operators
    tree = parse_expr("2*x + pi - y/2")
    variables = {'x': 3, 'y': 4}
    # 2*3 + pi - 4/2 = 6 + 3.1415... - 2 = 4 + pi
    assert abs(tree.evaluate(variables) - (4 + math.pi)) < 1e-6

def test_division_by_zero():
    tree = parse_expr("x / 0")
    with pytest.raises(ValueError, match="Division by zero"):
        tree.evaluate({'x': 5})

def test_functions_evaluation():
    funcs = {
        "sin(x)": math.sin(0.5),
        "cos(x)": math.cos(0.5),
        "tan(x)": math.tan(0.5),
        "log(x)": math.log(0.5),
        "exp(x)": math.exp(0.5),
        "sqrt(x)": math.sqrt(0.5),
        "ln(x)": math.log(0.5)
    }
    for expr, expected in funcs.items():
        tree = parse_expr(expr)
        assert abs(tree.evaluate({'x': 0.5}) - expected) < 1e-6

def test_function_differentiation():
    # Test differentiation structure for a few functions to ensure it builds correct AST
    sin_tree = parse_expr("sin(x)")
    diff_sin = sin_tree.differentiate('x')
    # Should be 1 * cos(x)
    assert isinstance(diff_sin, MulNode)
    assert isinstance(diff_sin.right, FunctionNode)
    assert diff_sin.right.function_name == "cos"

    tan_tree = parse_expr("tan(x)")
    diff_tan = tan_tree.differentiate('x')
    assert isinstance(diff_tan, MulNode)
    assert isinstance(diff_tan.right, DivNode) # sec^2 is 1/cos^2

def test_differentiate_quotient_rule():
    tree = parse_expr("x / y")
    diff_x = tree.differentiate('x')
    assert isinstance(diff_x, DivNode)
    
def test_parser_errors():
    with pytest.raises(ValueError, match="Expected '\\)'"):
        parse_expr("(x + 2")
    
    # Empty string parsing shouldn't crash, but return None
    assert parse_expr("") is None

def test_commands():
    tree = parse_expr("differentiate(x^2, x)")
    assert isinstance(tree, CommandNode)
    # Executing the command evaluates the differentiation mathematically
    result = tree.execute()
    assert str(result) == "(2 * x)" # or something mathematically equivalent

def test_constants():
    assert abs(parse_expr("pi").evaluate() - math.pi) < 1e-6
    assert abs(parse_expr("e").evaluate() - math.e) < 1e-6
    assert abs(parse_expr("phi").evaluate() - ((1 + math.sqrt(5)) / 2)) < 1e-6

def test_implicit_multiplication():
    tree = parse_expr("2x")
    assert str(tree) == "(2 * x)"
    
    tree2 = parse_expr("x(y+1)")
    assert str(tree2) == "(x * (y + 1))"

def test_unwrite_subtraction():
    tree = parse_expr("x - y").normalize()
    unwritten = tree.unwrite_subtraction()
    # It converts addition of negatives back to subtraction
    assert str(unwritten) == "(x - y)"
