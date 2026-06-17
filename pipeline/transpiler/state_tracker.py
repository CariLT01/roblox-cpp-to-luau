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

    # Helper: map register name -> (literal, rodata_str) for tracked regs
    _reg_map = {
        "a0": ("lit", "a0"), "x10": ("lit", "a0"),
        "a1": ("lit", "a1"), "x11": ("lit", "a1"),
        "a2": ("lit", "a2"), "x12": ("lit", "a2"),
        "a3": ("lit", "a3"), "x13": ("lit", "a3"),
        "a4": ("lit", "a4"), "x14": ("lit", "a4"),
        "a5": ("lit", "a5"), "x15": ("lit", "a5"),
        "a7": ("syscall", "a7"), "x17": ("syscall", "a7"),
    }

    # Build a lookup of current tracked values
    _tracked_literals = {
        "a0": tracked_a0_literal,
        "a1": tracked_a1_literal,
        "a2": tracked_a2_literal,
        "a3": tracked_a3_literal,
        "a4": tracked_a4_literal,
        "a5": tracked_a5_literal,
        "a7": tracked_a7_syscall,
    }
    _tracked_rodata = {
        "a1": tracked_a1_rodata_str,
        "a2": tracked_a2_rodata_str,
        "a3": tracked_a3_rodata_str,
        "a4": tracked_a4_rodata_str,
        "a5": tracked_a5_rodata_str,
    }

    def _get_tracked(reg):
        """Get the tracked literal value for a named register (only a0-a5, a7)."""
        return _tracked_literals.get(reg, "nil")

    def _get_tracked_rodata(reg):
        """Get the tracked rodata string for a named register."""
        return _tracked_rodata.get(reg, None)

    # Only track addi, lui, and the li pseudo-instruction
    if mnemonic not in ["li", "addi", "lui"]:
        return (tracked_a7_syscall, tracked_a0_literal, tracked_value_type,
                tracked_a1_literal, tracked_a1_rodata_str,
                tracked_a2_literal, tracked_a2_rodata_str,
                tracked_a3_literal, tracked_a3_rodata_str,
                tracked_a4_literal, tracked_a4_rodata_str,
                tracked_a5_literal, tracked_a5_rodata_str)

    dest_reg = args[0]
    src_reg = args[1] if len(args) > 1 else None

    # Check for register move: addi rd, rs, 0 where rs != x0
    is_reg_move = False
    if mnemonic == "addi" and len(args) >= 2:
        clean_imm = args[-1].split('#')[0].strip()
        if clean_imm == "0" and src_reg not in ["x0", "zero"]:
            is_reg_move = True

    # ── Handle register moves: propagate source register's tracked value ──
    if is_reg_move and src_reg:
        src_name = src_reg.replace("x1", "a").replace("x", "")
        if src_name in ["a0", "a1", "a2", "a3", "a4", "a5"]:
            src_lit = _get_tracked(src_name)
            src_rodata = _get_tracked_rodata(src_name)
            if dest_reg in ["a0", "x10"]:
                tracked_a0_literal = src_lit
            elif dest_reg in ["a1", "x11"]:
                tracked_a1_literal = src_lit
                tracked_a1_rodata_str = src_rodata
            elif dest_reg in ["a2", "x12"]:
                tracked_a2_literal = src_lit
                tracked_a2_rodata_str = src_rodata
            elif dest_reg in ["a3", "x13"]:
                tracked_a3_literal = src_lit
                tracked_a3_rodata_str = src_rodata
            elif dest_reg in ["a4", "x14"]:
                tracked_a4_literal = src_lit
                tracked_a4_rodata_str = src_rodata
            elif dest_reg in ["a5", "x15"]:
                tracked_a5_literal = src_lit
                tracked_a5_rodata_str = src_rodata
        # Don't clobber a7 during moves (it's set by li a7, N explicitly)

    # ── Handle immediate loads ──
    else:
        if dest_reg in ["a7", "x17"]:
            clean_imm = args[-1].split('#')[0].strip()
            try:
                tracked_a7_syscall = int(clean_imm)
            except ValueError:
                pass

        elif dest_reg in ["a0", "x10"]:
            new_literal, tracked_value_type = _resolve_literal(
                args, mnemonic, rodata_addr_table, rodata_table
            )
            if new_literal != "nil":
                tracked_a0_literal = new_literal

        elif dest_reg in ["a1", "x11"]:
            _, new_literal, new_rodata = _resolve_arg_literal(
                args, rodata_addr_table
            )
            if new_literal != "nil":
                tracked_a1_literal = new_literal
                tracked_a1_rodata_str = new_rodata

        elif dest_reg in ["a2", "x12"]:
            _, new_literal, new_rodata = _resolve_arg_literal(
                args, rodata_addr_table
            )
            if new_literal != "nil":
                tracked_a2_literal = new_literal
                tracked_a2_rodata_str = new_rodata

        elif dest_reg in ["a3", "x13"]:
            _, new_literal, new_rodata = _resolve_arg_literal(
                args, rodata_addr_table
            )
            if new_literal != "nil":
                tracked_a3_literal = new_literal
                tracked_a3_rodata_str = new_rodata

        elif dest_reg in ["a4", "x14"]:
            _, new_literal, new_rodata = _resolve_arg_literal(
                args, rodata_addr_table
            )
            if new_literal != "nil":
                tracked_a4_literal = new_literal
                tracked_a4_rodata_str = new_rodata

        elif dest_reg in ["a5", "x15"]:
            _, new_literal, new_rodata = _resolve_arg_literal(
                args, rodata_addr_table
            )
            if new_literal != "nil":
                tracked_a5_literal = new_literal
                tracked_a5_rodata_str = new_rodata

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
