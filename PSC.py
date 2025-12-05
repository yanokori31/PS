#!/usr/bin/env python3
"""
PSC.py - Parser Commander Science Test Runner

This is the main entry point for testing and running the PCS parser system.
Run this file to see demos of all features including:
- Basic arithmetic operations (+, -, *, /)
- Unicode/Alphanumeric conversion for math symbols
- Fraction operations: frac(a, b)
- Mixed number operations: mixf(whole, num, den)
- Decimal operations: dec(value, precision)
- Custom extensible functions
"""

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from src.pcs.parser.tokenizer import Tokenizer
from src.pcs.parser.parser import Parser
from src.pcs.parser.evaluator import Evaluator
from src.pcs.utils.unicode_formatter import UnicodeFormatter
from src.pcs.utils.fraction_utils import frac, mixf, fraction_to_mixed
from src.pcs.functions import load_custom_functions


class PCS:
    """Main PCS interface for parsing and evaluating mathematical expressions."""
    
    def __init__(self):
        self.evaluator = Evaluator()
        self._load_functions()
    
    def _load_functions(self):
        """Load custom functions from the functions directory."""
        custom_funcs = load_custom_functions()
        for name, func in custom_funcs.items():
            self.evaluator.register_function(name, func)
    
    def evaluate(self, expression: str) -> any:
        """
        Parse and evaluate a mathematical expression.
        
        Args:
            expression: A string containing a math expression
            
        Returns:
            The result of the evaluation
        """
        tokenizer = Tokenizer(expression)
        tokens = tokenizer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        result = self.evaluator.evaluate(ast)
        return result
    
    def format_unicode(self, expression: str) -> str:
        """Convert expression to Unicode format with mathematical symbols."""
        return UnicodeFormatter.format_expression(expression)
    
    def format_result(self, result) -> str:
        """Format result for display."""
        return UnicodeFormatter.format_result(result.value, result.display_type)


def print_header(title: str):
    """Print a formatted header."""
    print("\n" + "=" * 60)
    print(f" {title}")
    print("=" * 60)


def print_test(expression: str, pcs: PCS, show_unicode: bool = True):
    """Print test result for an expression."""
    try:
        result = pcs.evaluate(expression)
        formatted = pcs.format_result(result)
        
        if show_unicode:
            unicode_expr = pcs.format_unicode(expression)
            print(f"  {expression:30} -> {formatted}")
            if unicode_expr != expression:
                print(f"  Unicode: {unicode_expr}")
        else:
            print(f"  {expression:30} -> {formatted}")
    except Exception as e:
        print(f"  {expression:30} -> Error: {e}")


def demo_basic_arithmetic():
    """Demo basic arithmetic operations."""
    print_header("1. Basic Arithmetic Operations (+, -, *, /)")
    pcs = PCS()
    
    expressions = [
        "2 + 3",
        "10 - 4",
        "6 * 7",
        "20 / 4",
        "2 + 3 * 4",
        "(2 + 3) * 4",
        "100 / 5 + 10",
        "-5 + 10",
        "3.14 * 2",
        "10.5 / 2.5",
    ]
    
    for expr in expressions:
        print_test(expr, pcs, show_unicode=False)


def demo_unicode_conversion():
    """Demo Unicode conversion for math symbols."""
    print_header("2. Unicode/Alphanumeric Conversion")
    
    examples = [
        ("3 * 4", "Multiplication"),
        ("10 / 2", "Division"),
        ("5 - 3", "Subtraction"),
        ("2 + 2", "Addition"),
    ]
    
    formatter = UnicodeFormatter
    
    for expr, desc in examples:
        unicode_expr = formatter.format_expression(expr)
        alpha_expr = formatter.to_alphanumeric(unicode_expr)
        print(f"  {desc}:")
        print(f"    Original:    {expr}")
        print(f"    Unicode:     {unicode_expr}")
        print(f"    Alphanumeric: {alpha_expr}")
        print()
    
    print("  Superscripts (powers):")
    for i in range(0, 10):
        sup = formatter.format_superscript(str(i))
        print(f"    x^{i} = x{sup}")
    
    print("\n  Subscripts:")
    for i in range(0, 10):
        sub = formatter.format_subscript(str(i))
        print(f"    x_{i} = x{sub}")


def demo_fractions():
    """Demo fraction operations."""
    print_header("3. Fraction Operations - frac(numerator, denominator)")
    pcs = PCS()
    
    expressions = [
        "frac(1, 2)",
        "frac(3, 4)",
        "frac(2, 3)",
        "frac(5, 10)",
        "frac(7, 3)",
        "frac(1, 2) + frac(1, 4)",
        "frac(3, 4) - frac(1, 2)",
        "frac(2, 3) * frac(3, 4)",
        "frac(1, 2) / frac(1, 4)",
    ]
    
    for expr in expressions:
        print_test(expr, pcs)
    
    print("\n  Unicode Fraction Characters:")
    formatter = UnicodeFormatter
    common_fractions = [
        (1, 2), (1, 3), (2, 3), (1, 4), (3, 4),
        (1, 5), (2, 5), (3, 5), (4, 5),
        (1, 8), (3, 8), (5, 8), (7, 8),
    ]
    for num, den in common_fractions:
        print(f"    {num}/{den} = {formatter.format_fraction(num, den)}")


def demo_mixed_fractions():
    """Demo mixed fraction operations."""
    print_header("4. Mixed Fraction Operations - mixf(whole, num, den)")
    pcs = PCS()
    
    expressions = [
        "mixf(1, 1, 2)",
        "mixf(2, 3, 4)",
        "mixf(3, 1, 3)",
        "mixf(0, 5, 6)",
        "mixf(1, 1, 2) + mixf(2, 1, 4)",
        "mixf(3, 1, 2) - mixf(1, 3, 4)",
        "mixf(2, 1, 2) * 2",
    ]
    
    print("  mixf(whole, numerator, denominator) creates a mixed number")
    print("  Example: mixf(1, 1, 2) = 1 1/2 = 3/2")
    print()
    
    for expr in expressions:
        print_test(expr, pcs)


def demo_decimals():
    """Demo decimal operations."""
    print_header("5. Decimal Operations - dec(value, precision)")
    pcs = PCS()
    
    expressions = [
        "dec(3.14159, 2)",
        "dec(2.71828, 3)",
        "dec(1.0 / 3.0, 4)",
        "dec(22 / 7, 6)",
        "3.14159 + 2.71828",
        "10.5 * 2.5",
        "100.0 / 3.0",
    ]
    
    for expr in expressions:
        print_test(expr, pcs)


def demo_custom_functions():
    """Demo custom extensible functions."""
    print_header("6. Custom Functions (from functions/ directory)")
    pcs = PCS()
    
    expressions = [
        "sqrt(16)",
        "sqrt(2)",
        "pow(2, 10)",
        "pow(3, 4)",
        "mod(17, 5)",
        "floor(3.7)",
        "ceil(3.2)",
        "round(3.14159, 2)",
        "gcd(48, 18)",
        "lcm(4, 6)",
        "abs(-5)",
        "max(3, 7)",
        "min(10, 5)",
    ]
    
    print("  Available functions from math_basic.py:")
    print("  sqrt, pow, mod, floor, ceil, round, gcd, lcm, abs, max, min")
    print()
    
    for expr in expressions:
        print_test(expr, pcs)


def demo_complex_expressions():
    """Demo complex expressions combining multiple features."""
    print_header("7. Complex Expressions")
    pcs = PCS()
    
    expressions = [
        "frac(1, 2) + frac(1, 3) + frac(1, 6)",
        "sqrt(pow(3, 2) + pow(4, 2))",
        "mixf(2, 1, 2) * frac(2, 3)",
        "(frac(1, 2) + frac(1, 4)) * 4",
        "pow(2, 8) / pow(2, 4)",
        "gcd(frac(12, 1), frac(18, 1))",
    ]
    
    for expr in expressions:
        print_test(expr, pcs)


def demo_stacked_fractions():
    """Demo stacked fraction display."""
    print_header("8. Stacked Fraction Display")
    
    formatter = UnicodeFormatter
    
    fractions = [
        (1, 2),
        (3, 4),
        (7, 12),
        (15, 8),
        (-5, 6),
    ]
    
    for num, den in fractions:
        print(f"\n  {num}/{den} displayed as stacked:")
        stacked = formatter.format_fraction_stacked(num, den)
        for line in stacked.split('\n'):
            print(f"    {line}")


def run_interactive():
    """Run interactive mode."""
    print_header("Interactive PCS Calculator")
    print("  Type mathematical expressions to evaluate.")
    print("  Available operations: +, -, *, /, frac(), mixf(), dec()")
    print("  Available functions: sqrt, pow, mod, floor, ceil, round, gcd, lcm, abs, max, min")
    print("  Type 'quit' or 'exit' to exit.")
    print()
    
    pcs = PCS()
    
    while True:
        try:
            expr = input("PCS> ").strip()
            if expr.lower() in ('quit', 'exit', 'q'):
                print("Goodbye!")
                break
            if not expr:
                continue
            
            result = pcs.evaluate(expr)
            formatted = pcs.format_result(result)
            unicode_expr = pcs.format_unicode(expr)
            
            print(f"  = {formatted}")
            if unicode_expr != expr:
                print(f"  (Unicode: {unicode_expr})")
            print()
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"  Error: {e}")
            print()


def main():
    """Main function to run all demos."""
    print("\n" + "=" * 60)
    print("   PCS - Parser Commander Science")
    print("   Mathematical Parser System Demo")
    print("=" * 60)
    
    demo_basic_arithmetic()
    demo_unicode_conversion()
    demo_fractions()
    demo_mixed_fractions()
    demo_decimals()
    demo_custom_functions()
    demo_complex_expressions()
    demo_stacked_fractions()
    
    print("\n" + "=" * 60)
    print("  All demos completed successfully!")
    print("=" * 60)
    
    if len(sys.argv) > 1 and sys.argv[1] == '-i':
        run_interactive()


if __name__ == "__main__":
    main()
