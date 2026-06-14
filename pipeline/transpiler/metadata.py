"""Metadata parsing: enums.hpp, rodata sections, function address labels."""

import glob
import json
import os
import re

from .utils import escape_lua_string


def parse_enums():
    """Parse enums.hpp and scan C++ sources for used enums.
    Returns list of Lua lines for the ENUMS table (sparse)."""
    enum_hpp_index = {}
    try:
        with open("enums.hpp", "r") as f:
            in_enum = False
            idx = 0
            for line in f:
                line = line.strip()
                if "enum class Enum" in line:
                    in_enum = True
                    continue
                if in_enum:
                    if line == "};":
                        break
                    if line and not line.startswith("//"):
                        name = line.rstrip(",").strip()
                        if name:
                            enum_hpp_index[name] = idx
                            idx += 1
    except FileNotFoundError:
        pass

    used_indices = set()
    for src_path in glob.glob("*.cpp") + glob.glob("*.hpp"):
        try:
            with open(src_path, "r") as f:
                content = f.read()
                for m in re.finditer(r'Rbxl::Enum::(\w+)', content):
                    member_name = m.group(1)
                    if member_name in enum_hpp_index:
                        used_indices.add(enum_hpp_index[member_name])
        except FileNotFoundError:
            pass

    enums_sparse_lines = []
    if used_indices and enum_hpp_index:
        try:
            with open(os.path.join("..", "enum", "data.json"), "r") as f:
                data_entries = json.load(f)
            for enum_idx in sorted(used_indices):
                if enum_idx < len(data_entries):
                    enums_sparse_lines.append(
                        f"    S.ENUMS[{enum_idx + 1}] = {data_entries[enum_idx]}"
                    )
        except (FileNotFoundError, json.JSONDecodeError):
            pass

    return enums_sparse_lines


def parse_rodata_bytes(asm_text):
    """Pass 0: parse Section Contents (.rodata bytes from objdump -s).
    Returns (rodata_bytes: dict, rodata_addr_table: dict)."""
    rodata_bytes = {}
    in_rodata = False
    for line in asm_text.splitlines():
        if "Contents of section" in line and "rodata" in line:
            in_rodata = True
            continue
        if in_rodata:
            if not line.strip() or line.startswith("Contents"):
                in_rodata = False
                continue
            stripped = line.strip()
            tokens = stripped.split()
            try:
                addr = int(tokens[0], 16)
                byte_idx = 0
                for t in tokens[1:]:
                    if re.match(r'^[0-9a-fA-F]+$', t):
                        for j in range(0, len(t), 2):
                            byte_hex = t[j:j + 2]
                            if len(byte_hex) == 2:
                                rodata_bytes[addr + byte_idx] = int(byte_hex, 16)
                                byte_idx += 1
                    else:
                        break
            except (ValueError, IndexError):
                pass

    # Build address->string map from rodata bytes
    rodata_addr_table = {}
    sorted_addrs = sorted(rodata_bytes.keys())
    i = 0
    while i < len(sorted_addrs):
        addr = sorted_addrs[i]
        byte_val = rodata_bytes[addr]
        if 32 <= byte_val < 127:
            start_addr = addr
            str_chars = []
            cur = addr
            while cur in rodata_bytes:
                b = rodata_bytes[cur]
                if b == 0:
                    rodata_addr_table[start_addr] = ''.join(str_chars)
                    break
                str_chars.append(chr(b) if 32 <= b < 127 else '?')
                cur += 1
            while i < len(sorted_addrs) and sorted_addrs[i] <= cur:
                i += 1
            continue
        i += 1

    return rodata_bytes, rodata_addr_table


def parse_rodata_labels(asm_text):
    """Pass 1: extract .string / .float literals from assembly directives.
    Returns dict of label -> value."""
    rodata_table = {}
    current_label = None
    for line in asm_text.splitlines():
        label_match = re.match(r"^\s*(\.LC\w+|\.L\w+):", line)
        if label_match:
            current_label = label_match.group(1)
        elif current_label:
            if ".string" in line:
                str_content = re.findall(r'"([^"]*)"', line)
                if str_content:
                    rodata_table[current_label] = f'"{str_content[0]}"'
            elif ".float" in line:
                float_val = line.split(".float")[-1].strip()
                rodata_table[current_label] = float_val
    return rodata_table


def find_main_address(asm_text):
    """Find entry main address. Returns ('0x80000000', 0x80000000) as default."""
    main_address_str = "0x80000000"
    main_address_int = 0x80000000
    for line in asm_text.splitlines():
        if "<main>:" in line:
            raw = line.split()[0]
            main_address_str = "0x" + raw
            main_address_int = int(raw, 16)
            break
    return main_address_str, main_address_int


def parse_function_labels(asm_text):
    """Pass 1.5: extract function address ranges for context-aware ecall.
    Returns dict of addr -> (name, next_addr)."""
    func_labels = []
    func_re = re.compile(r"^\s*([0-9a-fA-F]+)\s+<(\S+)>:")
    for line in asm_text.splitlines():
        m = func_re.match(line)
        if m:
            func_labels.append(("0x" + m.group(1), m.group(2)))
    func_map = {}
    for idx, (addr, name) in enumerate(func_labels):
        next_addr = func_labels[idx + 1][0] if idx + 1 < len(func_labels) else "0xFFFFFFFF"
        func_map[addr] = (name, next_addr)
    return func_map


def build_rodata_lua_entries(rodata_addr_table):
    """Build RODATA Lua table entry lines from address->string map."""
    rodat_lua_entries = []
    for addr, s in sorted(rodata_addr_table.items()):
        rodat_lua_entries.append(
            f'    [0x{addr:08x}] = "{escape_lua_string(s)}",'
        )
    return rodat_lua_entries


def build_rodata_init_lines(rodata_bytes):
    """Build .rodata memory pre-population lines for direct page buffer writes."""
    rodata_init_lines = []
    if not rodata_bytes:
        return rodata_init_lines

    page_groups = {}  # page_idx -> [(offset, word_val), ...]
    done = set()
    for addr in sorted(rodata_bytes.keys()):
        if addr in done:
            continue
        base = addr & ~3
        word_val = 0
        for off in range(4):
            b = rodata_bytes.get(base + off, 0)
            word_val |= (b << (off * 8))
            done.add(base + off)

        page_idx = base >> 16
        offset = base & 0xFFFF
        page_groups.setdefault(page_idx, []).append((offset, word_val))

    rodata_init_lines.append("")
    rodata_init_lines.append(
        "-- Pre-populate .rodata memory for float constant reads (lw instructions)"
    )
    for page_idx in sorted(page_groups.keys()):
        writes = page_groups[page_idx]
        rodata_init_lines.append("do")
        rodata_init_lines.append(f"    local page = S.PAGES[{page_idx}]")
        rodata_init_lines.append("    if not page then")
        rodata_init_lines.append("        page = buffer.create(65536)")
        rodata_init_lines.append(f"        S.PAGES[{page_idx}] = page")
        rodata_init_lines.append("    end")
        for offset, word_val in writes:
            rodata_init_lines.append(f"    buffer.writei32(page, {offset}, {word_val})")
        rodata_init_lines.append("end")

    return rodata_init_lines
