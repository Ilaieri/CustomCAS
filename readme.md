# CustomCAS

A simple, homemade **Computer Algebra System** (CAS) in Python.

---

## Features Checklist

### ✅ Current Features
- [x] Custom-built **tokenizer** (handles implicit multiplication, e.g. `2x`, `x(y+1)`)
- [x] Recursive **parser** for mathematical expressions (+, -, *, /, ^, parentheses)
- [x] Expression **evaluation logic** (with variable substitution)
- [x] Parse and evaluate arithmetic expressions
- [x] Support for variables and parentheses
- [x] Handles both explicit and implicit multiplication
- [x] Expression tree **simplification** (basic arithmetic, zero/one rules, constant folding)
- [x] **Normalization** (rewrites subtraction/division for easier manipulation)
- [x] **Flattening** of sums and products (for collecting like terms and powers)
- [x] **Collect like terms** (combines coefficients for matching variable/power combinations)
- [x] **Expansion** (distributes multiplication over addition)
- [x] **Power collection** (combines repeated variables into powers, e.g. `x*x*x` → `x^3`)
- [x] **Pretty-printing** of flattened expressions

### 🛠️ In Progress / Planned
- [ ] Advanced simplification (automatic collection of powers and like terms in `simplify`)
- [ ] Symbolic differentiation (derivatives)
- [ ] Function support (sin, cos, log, etc.)
- [ ] Unary operators (support for unary minus, e.g. `-x`)
- [ ] Multi-letter variables and function names
- [ ] Better error handling and diagnostics
- [ ] More robust pretty-printing and output formatting

---

## Example

```python
from tools.tokenizer import tokenize
from tools.parser import Parser

expression = "32x + 5 * (2y - 4)"
tokens = tokenize(expression)
parser = Parser(tokens)
tree = parser.parse()
print(tree)  # Output: (32 * x + (5 * ((2 * y) - 4)))
```
