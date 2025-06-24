# CustomCAS

A simple, homemade **Computer Algebra System** (CAS) in Python, featuring:

- ✨ Custom-built **tokenizer**
- 🧩 Recursive **parser** for mathematical expressions
- ⚡ Expression **evaluation logic**

---

## Features

- Parse and evaluate arithmetic expressions
- Support for variables and parentheses
- Handles both explicit and implicit multiplication

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
