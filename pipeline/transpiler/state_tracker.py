"""Compile-time state tracking for instruction handler generation."""

import re

from .utils import escape_lua_string


def _track_state(mnemonic, args, rodata_addr_table, rodata_table,
                 tracked_a7_syscall, tracked_a0_literal, tracked_value_type,
                 tracked_a1_literal, tracked_a1_rodata_str,
                 tracked_a2_literal, tracked_a2_rodata_str,
                 tracked_a3_literal, tracked_a3_rodata_str,
                 tracked_a4_literal, tracked_a4_rodata_str,
                 tracked_a5_literal, tracked_a5_rodata_str):
    """Update compile-time state trackers based on current instruction."""
    if mnemonic not in ["li", "addi", "lui"]:
        return (tracked_a7_syscall, tracked_a0_literal, tracked_value_type,
                tracked_a1_literal, tracked_a1_rodata_str,
                tracked_a2_literal, tracked_a2_rodata_str,
                tracked_a3_literal, tracked_a3_rodata_str,
                tracked_a4_literal, tracked_a4_rodata_str,
                tracked_a5_literal, tracked_a5_rodata_str)

    dest_reg = args[0]

    if dest_reg in ["a7", "x17"]:
        clean_imm = args[-1].split('#')[0].strip()
        try:
            tracked_a7_syscall = int(clean_imm)
        except ValueError:
            pass

    elif dest_reg in ["a0", "x10"]:
        tracked_a0_literal, tracked_value_type = _resolve_literal(
            args, mnemonic, rodata_addr_table, rodata_table
        )

    elif dest_reg in ["a1", "x11"]:
        _, tracked_a1_literal, tracked_a1_rodata_str = _resolve_arg_literal(
            args, rodata_addr_table
        )

    elif dest_reg in ["a2", "x12"]:
        _, tracked_a2_literal, tracked_a2_rodata_str = _resolve_arg_literal(
            args, rodata_addr_table
        )

    elif dest_reg in ["a3", "x13"]:
        _, tracked_a3_literal, tracked_a3_rodata_str = _resolve_arg_literal(
            args, rodata_addr_table
        )

    elif dest_reg in ["a4", "x14"]:
        _, tracked_a4_literal, tracked_a4_rodata_str = _resolve_arg_literal(
            args, rodata_addr_table
        )

    elif dest_reg in ["a5", "x15"]:
        _, tracked_a5_literal, tracked_a5_rodata_str = _resolve_arg_literal(
            args, rodata_addr_table
        )

    return (tracked_a7_syscall, tracked_a0_literal, tracked_value_type,
            tracked_a1_literal, tracked_a1_rodata_str,
            tracked_a2_literal, tracked_a2_rodata_str,
            tracked_a3_literal, tracked_a3_rodata_str,
            tracked_a4_literal, tracked_a4_rodata_str,
            tracked_a5_literal, tracked_a5_rodata_str)


def _resolve_literal(args, mnemonic, rodata_addr_table, rodata_table):
    """Resolve a0 register value to a literal string and type."""
    last_arg = args[-1]
    clean_last = last_arg.split('#')[0].strip()

    # Check for address comment (e.g., # 0x80001234 <label>)
    addr_match = re.search(r'#\s*([0-9a-fA-F]+)\s*<', last_arg)
    if addr_match:
        full_addr = int(addr_match.group(1), 16)
        str_val = rodata_addr_table.get(full_addr, None)
        if str_val is not None:
            return '"' + escape_lua_string(str_val) + '"', "string"
        else:
            return str(full_addr), "address"

    # Skip if addi with rs1 != zero and imm == 0 (move between regs)
    if mnemonic == "addi" and clean_last == "0" and args[1] not in ["x0", "zero"]:
        return "nil", "nil"

    # Check for label reference
    label_find = re.search(r"(\.LC\w+|\.L\w+)", clean_last)
    if label_find:
        return rodata_table.get(label_find.group(1), "nil"), "string"

    if clean_last.replace('-', '').isdigit():
        return clean_last, "int"

    return "nil", "nil"


def _resolve_arg_literal(args, rodata_addr_table):
    """Resolve a destination register value for a1-a5."""
    last_arg = args[-1]
    clean_last = last_arg.split('#')[0].strip()
    rodata_str = None

    addr_match = re.search(r'#\s*([0-9a-fA-F]+)\s*<', last_arg)
    if addr_match:
        full_addr = int(addr_match.group(1), 16)
        return str(full_addr), str(full_addr), rodata_addr_table.get(full_addr, None)

    if clean_last.replace('-', '').isdigit():
        try:
            val = int(clean_last)
            rodata_str = rodata_addr_table.get(val, None)
        except ValueError:
            pass
        return clean_last, clean_last, rodata_str

    return "nil", "nil", None
