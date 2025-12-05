# PCS - Parser Commander Science

## Overview
PCS (Parser Commander Science) is a mathematical parser system built in Python that allows users to evaluate mathematical expressions with support for:
- Basic arithmetic operations (+, -, *, /)
- Fractions and mixed numbers
- Unicode mathematical symbol conversion
- Extensible custom functions
- **Interactive Shell** with IntelliSense-like autocomplete (PowerShell-style)

## Project Structure
```
├── PSC.py                     # Main entry point for testing and running PCS
├── src/
│   └── pcs/
│       ├── __init__.py        # Main PCS module exports
│       ├── parser/            # Parser engine
│       │   ├── tokenizer.py   # Tokenizes input expressions
│       │   ├── parser.py      # Builds AST from tokens
│       │   └── evaluator.py   # Evaluates the AST
│       ├── utils/             # Utility modules
│       │   ├── unicode_formatter.py  # Unicode conversion
│       │   └── fraction_utils.py     # Fraction helpers
│       └── functions/         # Extensible custom functions
│           ├── __init__.py    # Function loader
│           └── math_basic.py  # Basic math functions
```

## How to Run
```bash
python app.py        # Interactive shell with IntelliSense (main)
python PSC.py        # Run all demos/tests
python PSC.py -i     # Simple interactive mode
```

## Key Features

### 1. Basic Arithmetic
```
2 + 3 * 4    -> 14
(2 + 3) * 4  -> 20
10 / 4       -> 2.5
```

### 2. Fractions - frac(numerator, denominator)
```
frac(1, 2)              -> 1/2
frac(1, 2) + frac(1, 4) -> 3/4
```

### 3. Mixed Numbers - mixf(whole, numerator, denominator)
```
mixf(1, 1, 2)  -> 1 1/2 = 3/2
mixf(2, 3, 4)  -> 2 3/4 = 11/4
```

### 4. Decimal Precision - dec(value, precision)
```
dec(3.14159, 2) -> 3.14
dec(22 / 7, 6)  -> 3.142857
```

### 5. Unicode Conversion
- `*` becomes `×`
- `/` becomes `÷`
- `-` becomes `−`
- Superscripts: x² x³ x⁴ ...
- Subscripts: x₀ x₁ x₂ ...
- Common fractions: ½ ⅓ ¼ ⅔ ¾ ...

### 6. Custom Functions (in functions/ directory)
- sqrt, pow, mod, floor, ceil
- round, gcd, lcm, abs, max, min

## Adding Custom Functions
Create a new .py file in `src/pcs/functions/` with:

```python
def my_function(x):
    val = x.value if hasattr(x, 'value') else x
    from src.pcs.parser.evaluator import EvaluationResult
    return EvaluationResult(val * 2)

FUNCTIONS = {
    'my_function': my_function,
}
```

## Interactive Shell Features (app.py)
- **IntelliSense-like autocomplete**: Press Tab to see function suggestions
- **Command history**: Use arrow keys to navigate previous commands
- **Syntax highlighting**: Python-style syntax highlighting
- **Unicode display**: Results automatically converted to beautiful Unicode symbols
- **Built-in help**: Type `help`, `functions`, `examples`, or `unicode` for guidance

## Recent Changes
- 2025-12-03: Added interactive shell with IntelliSense and prompt-toolkit
- 2025-12-03: Initial project setup with parser, Unicode formatter, fraction support

## User Preferences
- Vietnamese language preferred for documentation
- Clean code structure with clear separation of concerns
