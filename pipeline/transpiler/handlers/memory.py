"""Load and Store instruction handlers."""

import re

from ..utils import clean_reg, clean_reg_fp


def _handle_load(handler_body, mnemonic, args, addr_int, validate=False):
    rd = clean_reg(args[0]) if mnemonic != "flw" else clean_reg_fp(args[0])
    mem_match = re.match(r"(-?\d+)\((x\d+)\)", args[1])
    if mem_match:
        offset, rs1 = mem_match.group(1), clean_reg(mem_match.group(2))
        addr_expr = f"{rs1} + {offset}"
        v = "S.validate_addr(_a); " if validate else ""
        # x0/zero is hardwired to 0 in RISC-V — never write to reg[1] (load prefetch/discard)
        if rd == "reg[1]":
            pass  # load into x0: discard result, just validate the address if needed
        elif mnemonic == "lw":
            # buffer.readi32 returns signed 32-bit; mask to unsigned to avoid sign-extension
            handler_body.append(f"        do local _a = {addr_expr}; if _a and _a ~= 0 then {v}local _i = bit32.rshift(_a, 16); local _p = PAGES[_i]; {rd} = _p and bit32.band(buffer.readi32(_p, bit32.band(_a, 0xFFFF)), 0xFFFFFFFF) or 0 else {rd} = 0 end end")
        elif mnemonic == "flw":
            handler_body.append(f"        do local _a = {addr_expr}; if _a and _a ~= 0 then {v}local _i = bit32.rshift(_a, 16); local _p = PAGES[_i]; {rd} = _p and buffer.readi32(_p, bit32.band(_a, 0xFFFF)) or 0 else {rd} = 0 end end")
        elif mnemonic == "lb":
            handler_body.append(f"        do local _a = {addr_expr}; if _a and _a ~= 0 then {v}local _i = bit32.rshift(_a, 16); local _p = PAGES[_i]; {rd} = _p and buffer.readi8(_p, bit32.band(_a, 0xFFFF)) or 0 else {rd} = 0 end end")
        elif mnemonic == "lbu":
            handler_body.append(f"        do local _a = {addr_expr}; if _a and _a ~= 0 then {v}local _i = bit32.rshift(_a, 16); local _p = PAGES[_i]; {rd} = bit32.band(_p and buffer.readi8(_p, bit32.band(_a, 0xFFFF)) or 0, 0xFF) else {rd} = 0 end end")
    handler_body.append(f"        return {addr_int + 4}")


def _handle_store(handler_body, mnemonic, args, addr_int, validate=False):
    rs2 = clean_reg(args[0]) if mnemonic != "fsw" else clean_reg_fp(args[0])
    mem_match = re.match(r"(-?\d+)\((x\d+)\)", args[1])
    if mem_match:
        offset, rs1 = mem_match.group(1), clean_reg(mem_match.group(2))
        addr_expr = f"{rs1} + {offset}"
        v = "S.validate_addr(_a); " if validate else ""
        if mnemonic == "sw" or mnemonic == "fsw":
            handler_body.append(f"        do local _a = {addr_expr}; if _a and _a ~= 0 then {v}local _i = bit32.rshift(_a, 16); local _p = PAGES[_i]; if not _p then _p = buffer.create(65536); PAGES[_i] = _p end; buffer.writei32(_p, bit32.band(_a, 0xFFFF), {rs2}) end end")
        elif mnemonic == "sb":
            handler_body.append(f"        do local _a = {addr_expr}; if _a and _a ~= 0 then {v}local _i = bit32.rshift(_a, 16); local _p = PAGES[_i]; if not _p then _p = buffer.create(65536); PAGES[_i] = _p end; buffer.writei8(_p, bit32.band(_a, 0xFFFF), {rs2}) end end")
    handler_body.append(f"        return {addr_int + 4}")
