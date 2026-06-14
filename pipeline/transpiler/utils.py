"""Utility functions for the Luau transpiler."""


def escape_lua_string(s):
    """Escape a string for safe use inside a Lua double-quoted string literal."""
    result = []
    for ch in s:
        if ch == '\\':
            result.append('\\\\')
        elif ch == '"':
            result.append('\\"')
        elif ch == '\n':
            result.append('\\n')
        elif ch == '\r':
            result.append('\\r')
        elif ch == '\t':
            result.append('\\t')
        elif ch == '\0':
            result.append('\\0')
        elif ord(ch) < 32 or ord(ch) >= 127:
            result.append(f'\\x{ord(ch):02x}')
        else:
            result.append(ch)
    return ''.join(result)


def clean_reg(reg_str):
    """Map RISC-V register name to Luau reg[] array index (1-based)."""
    from .constants import REG_ABI_MAP

    reg_str = reg_str.strip()
    if reg_str.startswith('x'):
        reg_num = int(reg_str[1:])
    else:
        reg_num = REG_ABI_MAP.get(reg_str, 0)
    return f"reg[{reg_num + 1}]"


def clean_reg_fp(reg_str):
    """Map RISC-V FP register name to Luau freg[] array index (1-based)."""
    from .constants import FP_REG_ABI_MAP

    reg_str = reg_str.strip()
    if reg_str.startswith('f'):
        reg_num = int(reg_str[1:])
    else:
        reg_num = FP_REG_ABI_MAP.get(reg_str, 0)
    return f"freg[{reg_num + 1}]"
