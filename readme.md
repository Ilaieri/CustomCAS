# CustomCAS

A simple, homemade **Computer Algebra System** (CAS) in Python, featuring a robust, polymorphic Object-Oriented Architecture.

---

## Installation & Running

The project is packaged and can be installed locally.

```bash
# Install the package locally
pip install .

# Launch the REPL
customcas
```

Alternatively, you can just run `python main.py` directly.

---

## Features Checklist

### ✅ Current Features
- [x] Custom-built **tokenizer** (handles implicit multiplication, e.g. `2x`, `x(y+1)`)
- [x] Recursive **parser** mapping to specific Operator Nodes (AddNode, SubNode, etc.)
- [x] Expression **evaluation logic** (with variable substitution)
- [x] **Symbolic differentiation** (derivatives using sum, product, and quotient rules)
- [x] **Function support** (`sin`, `cos`, `log`, `exp`, etc.)
- [x] Handles both explicit and implicit multiplication
- [x] Expression tree **simplification** (basic arithmetic, zero/one rules, constant folding)
- [x] **Normalization** (rewrites subtraction/division for easier manipulation)
- [x] **Flattening** of sums and products (for collecting like terms and powers)
- [x] **Collect like terms** (combines coefficients for matching variable/power combinations)
- [x] **Expansion** (distributes multiplication over addition)
- [x] **Power collection** (combines repeated variables into powers, e.g. `x*x*x` → `x^3`)
- [x] **Robust REPL** with error handling to gracefully catch invalid math operations

### 🛠️ In Progress / Planned
- [ ] Advanced simplification (automatic collection of powers and like terms in `simplify`)
- [ ] Equation Solving Engine (e.g. solving `2x + 4 = 10` for `x`)
- [ ] Symbolic Integration
- [ ] Unary operators (support for unary minus, e.g. `-x`)
- [ ] Multi-letter variables
- [ ] Graphing and Plotting Expressions
- [ ] Web GUI (React/FastAPI)

---

## Example Usage

```python
from tools.tokenizer import tokenize
from tools.parser import Parser

expression = "32x + 5 * (2y - 4)"
tokens = tokenize(expression)
parser = Parser(tokens)
tree = parser.parse()

# Polymorphic methods are available directly on the AST nodes
print(tree)  # Output: ((32 * x) + (5 * ((2 * y) - 4)))

# Differentiate with respect to x
diff_tree = tree.differentiate('x').simplify()
print(diff_tree) # Output: 32
```

## Testing

The project uses `pytest` for unit testing the CAS functionalities (tokenization, parsing, simplification, differentiation, etc.).

To run the tests:
1. Ensure you have `pytest` installed (`pip install pytest`).
2. Run the following command in the root directory:

```bash
pytest test_cas.py
```
