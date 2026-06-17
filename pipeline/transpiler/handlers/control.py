"""Branch, Jump, LUI, and AUIPC instruction handlers."""

import re

from ..utils import clean_reg


def _handle_branch(handler_body, mnemonic, args, addr_int):
    rs1, rs2 = clean_reg(args[0]), clean_reg(args[1])
    target = args[2].split()[0]
    if not target.startswith("0x"):
        target = "0x" + target

    if mnemonic == "beq":
        cond = f"{rs1} == {rs2}"
    elif mnemonic == "bne":
        cond = f"{rs1} ~= {rs2}"
    elif mnemonic == "bltu":
        cond = f"{rs1} < {rs2}"
    elif mnemonic == "bgeu":
        cond = f"{rs1} >= {rs2}"
    elif mnemonic in ["blt", "bge"]:
        handler_body.append(f"        local _s1 = if {rs1} > 0x7FFFFFFF then {rs1} - 0x100000000 else {rs1}")
        handler_body.append(f"        local _s2 = if {rs2} > 0x7FFFFFFF then {rs2} - 0x100000000 else {rs2}")
        op = "<" if mnemonic == "blt" else ">="
        cond = f"_s1 {op} _s2"

    handler_body.append(f"        if {cond} then")
    handler_body.append(f"            return {target}")
    handler_body.append("        else")
    handler_body.append(f"            return {addr_int + 4}")
    handler_body.append("        end")


def _handle_jal(handler_body, args, addr_int):
    rd = clean_reg(args[0])
    target = args[1].split()[0]
    if not target.startswith("0x"):
        target = "0x" + target
    # x0 (reg[1]) is hardwired to zero in RISC-V — never write to it
    if rd != "reg[1]":
        handler_body.append(f"        {rd} = {(addr_int + 4) & 0xFFFFFFFF}")
    handler_body.append(f"        return {target}")


def _handle_jalr(handler_body, args, addr_int):
    rd = clean_reg(args[0])
    mem_match = re.match(r"(-?\d+)\((\w+)\)", args[1])
    if mem_match:
        offset, rs1 = mem_match.group(1), clean_reg(mem_match.group(2))
        handler_body.append(f"        local _next_pc = bit32.band({rs1} + {offset}, 0xFFFFFFFF)")
        # x0 (reg[1]) is hardwired to zero in RISC-V — never write to it
        if rd != "reg[1]":
            handler_body.append(f"        {rd} = {(addr_int + 4) & 0xFFFFFFFF}")
        handler_body.append("        return _next_pc")
    else:
        # Malformed jalr operand — halt with diagnostic
        handler_body.append(f"        print('System Halt: jalr with unrecognized operand format: ' .. '{args[1]}')")
        handler_body.append("        return nil")


def _handle_lui(handler_body, args, addr_int):
    rd = clean_reg(args[0])
    imm = args[1]
    # x0/zero is hardwired to 0 in RISC-V — never write to reg[1]
    if rd != "reg[1]":
        handler_body.append(f"        {rd} = {int(imm, 0) * 4096 & 0xFFFFFFFF}")
    handler_body.append(f"        return {addr_int + 4}")


def _handle_auipc(handler_body, args, addr_int):
    rd = clean_reg(args[0])
    imm = args[1]
    # x0/zero is hardwired to 0 in RISC-V — never write to reg[1]
    if rd != "reg[1]":
        handler_body.append(f"        {rd} = {(addr_int + int(imm, 0) * 4096) & 0xFFFFFFFF}")
    handler_body.append(f"        return {addr_int + 4}")
