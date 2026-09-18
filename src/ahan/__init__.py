"""
AHAN — Bahasa Pemrograman Imperatif dengan Sintaks Bahasa Devayan.

AHAN adalah interpreter tree-walking untuk bahasa pemrograman dengan
kata kunci berbahasa Devayan (Simeulue, Aceh).

Contoh penggunaan:

    from ahan import run_file
    run_file("program.ahan")
"""

__version__ = "0.1.0"
__author__ = "AHAN Contributors"
__license__ = "MIT"

from .main import run_code, run_file
from .evaluator import Evaluator
from .lexer import Lexer
from .parser import Parser

__all__ = [
    "run_code",
    "run_file",
    "Evaluator",
    "Lexer",
    "Parser",
    "__version__",
]