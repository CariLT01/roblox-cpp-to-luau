"""Luau RISC-V VM Transpiler.

Usage:
    python -m transpiler           # reads output.asm, writes to dist/
    python -m transpiler input.asm # reads specified asm file
"""

from .main import main, parse_asm_to_modules

__all__ = ['main', 'parse_asm_to_modules']
