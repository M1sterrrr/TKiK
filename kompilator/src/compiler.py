from __future__ import annotations

from .parser import build_parser
from .codegen import CGenerator


def compile_pascal_to_c(source: str) -> str:
    parser, lexer = build_parser()
    ast = parser.parse(source, lexer=lexer)
    gen = CGenerator()
    return gen.generate(ast)

