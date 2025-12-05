#!/usr/bin/env python3
"""
PCS Interactive Shell - PowerShell-style Mathematical Calculator
Features:
- IntelliSense-like autocomplete for functions
- Syntax highlighting
- Command history
- Unicode mathematical display
"""

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import WordCompleter, Completer, Completion
from prompt_toolkit.lexers import PygmentsLexer
from prompt_toolkit.styles import Style
from prompt_toolkit.formatted_text import HTML
from pygments.lexers import PythonLexer

from src.pcs.parser.tokenizer import Tokenizer
from src.pcs.parser.parser import Parser
from src.pcs.parser.evaluator import Evaluator
from src.pcs.utils.unicode_formatter import UnicodeFormatter
from src.pcs.functions import load_custom_functions


BUILTIN_FUNCTIONS = [
    'frac', 'mixf', 'dec', 'abs',
    'sqrt', 'pow', 'mod', 'floor', 'ceil', 'round',
    'gcd', 'lcm', 'max', 'min'
]

COMMANDS = [
    'help', 'exit', 'quit', 'clear', 'cls',
    'history', 'functions', 'unicode', 'examples'
]

FUNCTION_DOCS = {
    'frac': 'frac(a, b) - Tao phan so a/b. Vi du: frac(1, 2) = 1/2',
    'mixf': 'mixf(w, a, b) - Tao hon so w a/b. Vi du: mixf(1, 1, 2) = 1 1/2',
    'dec': 'dec(x, n) - Lam tron x den n chu so thap phan. Vi du: dec(3.14159, 2) = 3.14',
    'sqrt': 'sqrt(x) - Can bac hai cua x. Vi du: sqrt(16) = 4',
    'pow': 'pow(a, b) - Tinh a^b. Vi du: pow(2, 10) = 1024',
    'mod': 'mod(a, b) - Phep chia lay du a % b. Vi du: mod(17, 5) = 2',
    'floor': 'floor(x) - Lam tron xuong. Vi du: floor(3.7) = 3',
    'ceil': 'ceil(x) - Lam tron len. Vi du: ceil(3.2) = 4',
    'round': 'round(x, n) - Lam tron x den n chu so. Vi du: round(3.14159, 2) = 3.14',
    'gcd': 'gcd(a, b) - Uoc chung lon nhat. Vi du: gcd(48, 18) = 6',
    'lcm': 'lcm(a, b) - Boi chung nho nhat. Vi du: lcm(4, 6) = 12',
    'max': 'max(a, b, ...) - Gia tri lon nhat. Vi du: max(3, 7) = 7',
    'min': 'min(a, b, ...) - Gia tri nho nhat. Vi du: min(10, 5) = 5',
    'abs': 'abs(x) - Gia tri tuyet doi. Vi du: abs(-5) = 5',
}


class PCSCompleter(Completer):
    def __init__(self):
        self.functions = BUILTIN_FUNCTIONS
        self.commands = COMMANDS
    
    def get_completions(self, document, complete_event):
        text = document.text_before_cursor
        word = document.get_word_before_cursor()
        
        if not text.strip() or text.strip() == word:
            all_items = self.commands + self.functions
            for item in all_items:
                if item.startswith(word.lower()):
                    if item in self.functions:
                        yield Completion(
                            item + '(',
                            start_position=-len(word),
                            display=item,
                            display_meta=self._get_meta(item)
                        )
                    else:
                        yield Completion(
                            item,
                            start_position=-len(word),
                            display=item,
                            display_meta='command'
                        )
        else:
            for func in self.functions:
                if func.startswith(word.lower()):
                    yield Completion(
                        func + '(',
                        start_position=-len(word),
                        display=func,
                        display_meta=self._get_meta(func)
                    )
    
    def _get_meta(self, func):
        meta_map = {
            'frac': 'phan so',
            'mixf': 'hon so',
            'dec': 'thap phan',
            'sqrt': 'can bac 2',
            'pow': 'luy thua',
            'mod': 'chia lay du',
            'floor': 'lam tron xuong',
            'ceil': 'lam tron len',
            'round': 'lam tron',
            'gcd': 'UCLN',
            'lcm': 'BCNN',
            'max': 'max',
            'min': 'min',
            'abs': 'tri tuyet doi',
        }
        return meta_map.get(func, 'function')


STYLE = Style.from_dict({
    'prompt': '#00aa00 bold',
    'path': '#0088ff',
    'arrow': '#00aa00 bold',
})


class PCSShell:
    def __init__(self):
        self.evaluator = Evaluator()
        self._load_functions()
        
        history_file = os.path.expanduser('~/.pcs_history')
        
        self.session = PromptSession(
            history=FileHistory(history_file),
            auto_suggest=AutoSuggestFromHistory(),
            completer=PCSCompleter(),
            lexer=PygmentsLexer(PythonLexer),
            style=STYLE,
            complete_while_typing=True,
        )
    
    def _load_functions(self):
        custom_funcs = load_custom_functions()
        for name, func in custom_funcs.items():
            self.evaluator.register_function(name, func)
    
    def get_prompt(self):
        return HTML('<prompt>PCS</prompt> <arrow>></arrow> ')
    
    def evaluate(self, expression: str):
        tokenizer = Tokenizer(expression)
        tokens = tokenizer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        result = self.evaluator.evaluate(ast)
        return result
    
    def format_result(self, result) -> str:
        return UnicodeFormatter.format_result(result.value, result.display_type)
    
    def format_unicode(self, expression: str) -> str:
        return UnicodeFormatter.format_expression(expression)
    
    def show_help(self):
        print("""
\033[1;32m============================================================
   PCS - Parser Commander Science
   Mathematical Calculator with IntelliSense
============================================================\033[0m

\033[1;36mLENH CO BAN:\033[0m
  help       - Hien thi tro giup nay
  functions  - Liet ke cac ham co san
  examples   - Xem vi du su dung
  unicode    - Xem bang chuyen doi Unicode
  clear/cls  - Xoa man hinh
  exit/quit  - Thoat chuong trinh

\033[1;36mPHEP TINH:\033[0m
  +  Cong        Vi du: 2 + 3
  -  Tru         Vi du: 10 - 4
  *  Nhan        Vi du: 6 * 7
  /  Chia        Vi du: 20 / 4
  () Dau ngoac  Vi du: (2 + 3) * 4

\033[1;36mGOI Y:\033[0m
  - Nhan Tab de xem goi y ham (IntelliSense)
  - Dung phim mui ten len/xuong de xem lich su lenh
  - Ket qua se tu dong chuyen sang Unicode dep
""")
    
    def show_functions(self):
        print("\n\033[1;36mDANH SACH HAM:\033[0m")
        print("-" * 60)
        for func, doc in FUNCTION_DOCS.items():
            print(f"  \033[1;33m{func:10}\033[0m - {doc.split(' - ')[1]}")
        print()
    
    def show_examples(self):
        print("""
\033[1;36mVI DU SU DUNG:\033[0m
---------------------------------------------------------
\033[1;33mPhep tinh co ban:\033[0m
  2 + 3 * 4          -> 14
  (2 + 3) * 4        -> 20
  10 / 4             -> 2.5

\033[1;33mPhan so:\033[0m
  frac(1, 2)                -> 1/2
  frac(1, 2) + frac(1, 4)   -> 3/4
  frac(2, 3) * frac(3, 4)   -> 1/2

\033[1;33mHon so:\033[0m
  mixf(1, 1, 2)             -> 1 1/2
  mixf(2, 3, 4)             -> 2 3/4

\033[1;33mSo thap phan:\033[0m
  dec(3.14159, 2)           -> 3.14
  dec(22 / 7, 6)            -> 3.142857

\033[1;33mHam toan hoc:\033[0m
  sqrt(16)                  -> 4
  pow(2, 10)                -> 1024
  gcd(48, 18)               -> 6
  sqrt(pow(3, 2) + pow(4, 2)) -> 5
""")
    
    def show_unicode(self):
        formatter = UnicodeFormatter
        print("\n\033[1;36mBANG CHUYEN DOI UNICODE:\033[0m")
        print("-" * 40)
        print("\033[1;33mToan tu:\033[0m")
        print(f"  *  -> {formatter.format_expression('*'):5}  (nhan)")
        print(f"  /  -> {formatter.format_expression('/'):5}  (chia)")
        print(f"  -  -> {formatter.format_expression('-'):5}  (tru)")
        
        print("\n\033[1;33mSo mu (superscript):\033[0m")
        for i in range(10):
            sup = formatter.format_superscript(str(i))
            print(f"  ^{i} -> {sup}", end="  ")
            if (i + 1) % 5 == 0:
                print()
        
        print("\n\033[1;33mChi so duoi (subscript):\033[0m")
        for i in range(10):
            sub = formatter.format_subscript(str(i))
            print(f"  _{i} -> {sub}", end="  ")
            if (i + 1) % 5 == 0:
                print()
        
        print("\n\033[1;33mPhan so Unicode:\033[0m")
        fractions = [(1,2), (1,3), (2,3), (1,4), (3,4), (1,5), (1,8)]
        for num, den in fractions:
            frac_char = formatter.format_fraction(num, den)
            print(f"  {num}/{den} -> {frac_char}", end="  ")
        print("\n")
    
    def clear_screen(self):
        os.system('clear' if os.name != 'nt' else 'cls')
    
    def run(self):
        self.clear_screen()
        print("""
\033[1;32m============================================================
     ____   ____  ____  
    |  _ \\ / ___/ ___|  
    | |_) | |   \\___ \\  Parser Commander Science
    |  __/| |___ ___) | Mathematical Calculator v1.0
    |_|    \\____|____/  
                        
============================================================\033[0m
  Nhap 'help' de xem huong dan. Nhan Tab de xem goi y.
  Nhap 'exit' hoac 'quit' de thoat.
============================================================
""")
        
        while True:
            try:
                text = self.session.prompt(self.get_prompt()).strip()
                
                if not text:
                    continue
                
                cmd = text.lower()
                
                if cmd in ('exit', 'quit', 'q'):
                    print("\n\033[1;32mTam biet! Hen gap lai.\033[0m\n")
                    break
                elif cmd == 'help':
                    self.show_help()
                elif cmd == 'functions':
                    self.show_functions()
                elif cmd == 'examples':
                    self.show_examples()
                elif cmd == 'unicode':
                    self.show_unicode()
                elif cmd in ('clear', 'cls'):
                    self.clear_screen()
                elif cmd == 'history':
                    print("\n\033[1;36mLICH SU LENH:\033[0m")
                    print("  (Dung phim mui ten len/xuong de duyet lich su)")
                    print()
                else:
                    result = self.evaluate(text)
                    formatted = self.format_result(result)
                    unicode_expr = self.format_unicode(text)
                    
                    print(f"\n  \033[1;33m=\033[0m {formatted}")
                    
                    if unicode_expr != text:
                        print(f"  \033[2m(Unicode: {unicode_expr})\033[0m")
                    print()
                    
            except KeyboardInterrupt:
                print("\n\033[2m(Nhan Ctrl+C lan nua hoac nhap 'exit' de thoat)\033[0m")
                continue
            except EOFError:
                print("\n\033[1;32mTam biet!\033[0m\n")
                break
            except Exception as e:
                print(f"\n  \033[1;31mLoi:\033[0m {e}\n")


def main():
    shell = PCSShell()
    shell.run()


if __name__ == "__main__":
    main()
