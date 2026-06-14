"""R-Type (RV32I + RV32M) and I-Type ALU instruction handlers."""

from ..utils import clean_reg


def _handle_rtype(handler_body, mnemonic, args, addr_int):
    rd, rs1, rs2 = clean_reg(args[0]), clean_reg(args[1]), clean_reg(args[2])

    # RV32I basic ops
    if mnemonic == "add":
        handler_body.append(f"        {rd} = bit32.band({rs1} + {rs2}, 0xFFFFFFFF)")
    elif mnemonic == "sub":
        handler_body.append(f"        {rd} = bit32.band({rs1} - {rs2}, 0xFFFFFFFF)")
    elif mnemonic == "xor":
        handler_body.append(f"        {rd} = bit32.bxor({rs1}, {rs2})")
    elif mnemonic == "or":
        handler_body.append(f"        {rd} = bit32.bor({rs1}, {rs2})")
    elif mnemonic == "and":
        handler_body.append(f"        {rd} = bit32.band({rs1}, {rs2})")
    elif mnemonic == "sll":
        handler_body.append(f"        {rd} = bit32.lshift({rs1}, bit32.band({rs2}, 31))")
    elif mnemonic == "srl":
        handler_body.append(f"        {rd} = bit32.rshift({rs1}, bit32.band({rs2}, 31))")
    elif mnemonic == "sra":
        handler_body.append(f"        {rd} = bit32.arshift({rs1}, bit32.band({rs2}, 31))")
    elif mnemonic == "slt":
        handler_body.append(f"        local _s1 = if {rs1} > 0x7FFFFFFF then {rs1} - 0x100000000 else {rs1}")
        handler_body.append(f"        local _s2 = if {rs2} > 0x7FFFFFFF then {rs2} - 0x100000000 else {rs2}")
        handler_body.append(f"        {rd} = if _s1 < _s2 then 1 else 0")
    elif mnemonic == "sltu":
        handler_body.append(f"        {rd} = if {rs1} < {rs2} then 1 else 0")

    # RV32M Multiply
    elif mnemonic == "mul":
        handler_body.append(f"        local _a_lo = bit32.band({rs1}, 0xFFFF)")
        handler_body.append(f"        local _a_hi = bit32.rshift({rs1}, 16)")
        handler_body.append(f"        local _b_lo = bit32.band({rs2}, 0xFFFF)")
        handler_body.append(f"        local _b_hi = bit32.rshift({rs2}, 16)")
        handler_body.append("        local _low = _a_lo * _b_lo")
        handler_body.append("        local _mid = _a_lo * _b_hi + _a_hi * _b_lo + bit32.rshift(_low, 16)")
        handler_body.append(f"        {rd} = bit32.band(bit32.band(_low, 0xFFFF) + bit32.lshift(bit32.band(_mid, 0xFFFF), 16), 0xFFFFFFFF)")
    elif mnemonic == "mulhu":
        handler_body.append(f"        local _a_lo = bit32.band({rs1}, 0xFFFF)")
        handler_body.append(f"        local _a_hi = bit32.rshift({rs1}, 16)")
        handler_body.append(f"        local _b_lo = bit32.band({rs2}, 0xFFFF)")
        handler_body.append(f"        local _b_hi = bit32.rshift({rs2}, 16)")
        handler_body.append("        local _low = _a_lo * _b_lo")
        handler_body.append("        local _mid = _a_lo * _b_hi + _a_hi * _b_lo + bit32.rshift(_low, 16)")
        handler_body.append(f"        {rd} = bit32.band(_a_hi * _b_hi + bit32.rshift(_mid, 16), 0xFFFFFFFF)")
    elif mnemonic == "mulh":
        handler_body.append(f"        local _s1 = if {rs1} >= 0x80000000 then {rs1} - 0x100000000 else {rs1}")
        handler_body.append(f"        local _s2 = if {rs2} >= 0x80000000 then {rs2} - 0x100000000 else {rs2}")
        handler_body.append("        local _u1 = bit32.band(if _s1 < 0 then -_s1 else _s1, 0xFFFFFFFF)")
        handler_body.append("        local _u2 = bit32.band(if _s2 < 0 then -_s2 else _s2, 0xFFFFFFFF)")
        handler_body.append("        local _a_lo = bit32.band(_u1, 0xFFFF)")
        handler_body.append("        local _a_hi = bit32.rshift(_u1, 16)")
        handler_body.append("        local _b_lo = bit32.band(_u2, 0xFFFF)")
        handler_body.append("        local _b_hi = bit32.rshift(_u2, 16)")
        handler_body.append("        local _low = _a_lo * _b_lo")
        handler_body.append("        local _mid = _a_lo * _b_hi + _a_hi * _b_lo + bit32.rshift(_low, 16)")
        handler_body.append("        local _prod = _a_hi * _b_hi + bit32.rshift(_mid, 16)")
        handler_body.append("        if (_s1 < 0) ~= (_s2 < 0) then")
        handler_body.append(f"            {rd} = bit32.band(-_prod, 0xFFFFFFFF)")
        handler_body.append("        else")
        handler_body.append(f"            {rd} = bit32.band(_prod, 0xFFFFFFFF)")
        handler_body.append("        end")
    elif mnemonic == "mulhsu":
        handler_body.append(f"        local _s1 = if {rs1} >= 0x80000000 then {rs1} - 0x100000000 else {rs1}")
        handler_body.append("        local _u1 = bit32.band(if _s1 < 0 then -_s1 else _s1, 0xFFFFFFFF)")
        handler_body.append(f"        local _u2 = {rs2}")
        handler_body.append("        local _a_lo = bit32.band(_u1, 0xFFFF)")
        handler_body.append("        local _a_hi = bit32.rshift(_u1, 16)")
        handler_body.append("        local _b_lo = bit32.band(_u2, 0xFFFF)")
        handler_body.append("        local _b_hi = bit32.rshift(_u2, 16)")
        handler_body.append("        local _low = _a_lo * _b_lo")
        handler_body.append("        local _mid = _a_lo * _b_hi + _a_hi * _b_lo + bit32.rshift(_low, 16)")
        handler_body.append("        local _prod = _a_hi * _b_hi + bit32.rshift(_mid, 16)")
        handler_body.append("        if _s1 < 0 then")
        handler_body.append(f"            {rd} = bit32.band(-_prod, 0xFFFFFFFF)")
        handler_body.append("        else")
        handler_body.append(f"            {rd} = bit32.band(_prod, 0xFFFFFFFF)")
        handler_body.append("        end")

    # RV32M Divide
    elif mnemonic == "divu":
        handler_body.append(f"        if {rs2} ~= 0 then")
        handler_body.append(f"            {rd} = math.floor({rs1} / {rs2})")
        handler_body.append("        else")
        handler_body.append(f"            {rd} = 0xFFFFFFFF")
        handler_body.append("        end")
    elif mnemonic == "div":
        handler_body.append(f"        if {rs2} ~= 0 then")
        handler_body.append(f"            local _s1 = if {rs1} >= 0x80000000 then {rs1} - 0x100000000 else {rs1}")
        handler_body.append(f"            local _s2 = if {rs2} >= 0x80000000 then {rs2} - 0x100000000 else {rs2}")
        handler_body.append("            local _q = _s1 / _s2")
        handler_body.append("            if _q >= 0 then")
        handler_body.append(f"                {rd} = bit32.band(math.floor(_q), 0xFFFFFFFF)")
        handler_body.append("            else")
        handler_body.append(f"                {rd} = bit32.band(math.ceil(_q), 0xFFFFFFFF)")
        handler_body.append("            end")
        handler_body.append("        else")
        handler_body.append(f"            {rd} = 0xFFFFFFFF")
        handler_body.append("        end")
    elif mnemonic == "remu":
        handler_body.append(f"        if {rs2} ~= 0 then")
        handler_body.append(f"            {rd} = {rs1} % {rs2}")
        handler_body.append("        else")
        handler_body.append(f"            {rd} = {rs1}")
        handler_body.append("        end")
    elif mnemonic == "rem":
        handler_body.append(f"        if {rs2} ~= 0 then")
        handler_body.append(f"            local _s1 = if {rs1} >= 0x80000000 then {rs1} - 0x100000000 else {rs1}")
        handler_body.append(f"            local _s2 = if {rs2} >= 0x80000000 then {rs2} - 0x100000000 else {rs2}")
        handler_body.append("            local _q = _s1 / _s2")
        handler_body.append("            if _q >= 0 then _q = math.floor(_q) else _q = math.ceil(_q) end")
        handler_body.append(f"            {rd} = bit32.band(_s1 - _q * _s2, 0xFFFFFFFF)")
        handler_body.append("        else")
        handler_body.append(f"            {rd} = {rs1}")
        handler_body.append("        end")

    handler_body.append(f"        return {addr_int + 4}")


def _handle_itype(handler_body, mnemonic, args, addr_int):
    rd, rs1 = clean_reg(args[0]), clean_reg(args[1])
    imm = args[2]
    clean_imm = imm.split('#')[0].strip()
    if "%lo" in clean_imm or "%hi" in clean_imm:
        clean_imm = "0"

    if mnemonic == "addi":
        handler_body.append(f"        {rd} = bit32.band({rs1} + {clean_imm}, 0xFFFFFFFF)")
    elif mnemonic == "xori":
        handler_body.append(f"        {rd} = bit32.bxor({rs1}, {clean_imm})")
    elif mnemonic == "ori":
        handler_body.append(f"        {rd} = bit32.bor({rs1}, {clean_imm})")
    elif mnemonic == "andi":
        handler_body.append(f"        {rd} = bit32.band({rs1}, {clean_imm})")
    elif mnemonic == "slli":
        handler_body.append(f"        {rd} = bit32.lshift({rs1}, bit32.band({clean_imm}, 31))")
    elif mnemonic == "srli":
        handler_body.append(f"        {rd} = bit32.rshift({rs1}, bit32.band({clean_imm}, 31))")
    elif mnemonic == "srai":
        handler_body.append(f"        {rd} = bit32.arshift({rs1}, bit32.band({clean_imm}, 31))")
    elif mnemonic == "slti":
        handler_body.append(f"        local _s1 = if {rs1} > 0x7FFFFFFF then {rs1} - 0x100000000 else {rs1}")
        handler_body.append(f"        local _imm_val = {clean_imm}")
        handler_body.append("        local _s2 = if _imm_val > 0x7FFFFFFF then _imm_val - 0x100000000 else _imm_val")
        handler_body.append(f"        {rd} = if _s1 < _s2 then 1 else 0")
    elif mnemonic == "sltiu":
        handler_body.append(f"        {rd} = if {rs1} < {clean_imm} then 1 else 0")

    handler_body.append(f"        return {addr_int + 4}")
