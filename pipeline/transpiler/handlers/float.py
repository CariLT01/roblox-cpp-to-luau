"""RV32F Floating-Point instruction handlers."""

from ..utils import clean_reg, clean_reg_fp


def _handle_fp(handler_body, mnemonic, args, addr_int):
    # FP Arithmetic
    if mnemonic in ["fadd.s", "fsub.s", "fmul.s", "fdiv.s"]:
        frd = clean_reg_fp(args[0])
        frs1 = clean_reg_fp(args[1])
        frs2 = clean_reg_fp(args[2])
        if mnemonic == "fadd.s":
            handler_body.append(f"        {frd} = f32_to_bits(bits_to_f32({frs1}) + bits_to_f32({frs2}))")
        elif mnemonic == "fsub.s":
            handler_body.append(f"        {frd} = f32_to_bits(bits_to_f32({frs1}) - bits_to_f32({frs2}))")
        elif mnemonic == "fmul.s":
            handler_body.append(f"        {frd} = f32_to_bits(bits_to_f32({frs1}) * bits_to_f32({frs2}))")
        elif mnemonic == "fdiv.s":
            handler_body.append(f"        {frd} = f32_to_bits(bits_to_f32({frs1}) / bits_to_f32({frs2}))")

    # FP Sign Injection
    elif mnemonic in ["fsgnj.s", "fsgnjn.s", "fsgnjx.s"]:
        frd = clean_reg_fp(args[0])
        frs1 = clean_reg_fp(args[1])
        frs2 = clean_reg_fp(args[2])
        if mnemonic == "fsgnj.s":
            handler_body.append(f"        {frd} = bit32.bor(bit32.band({frs1}, 0x7FFFFFFF), bit32.band({frs2}, 0x80000000))")
        elif mnemonic == "fsgnjn.s":
            handler_body.append(f"        {frd} = bit32.bor(bit32.band({frs1}, 0x7FFFFFFF), bit32.band(bit32.bxor({frs2}, 0x80000000), 0x80000000))")
        elif mnemonic == "fsgnjx.s":
            handler_body.append(f"        {frd} = bit32.bxor({frs1}, bit32.band({frs2}, 0x80000000))")

    # FP Min/Max
    elif mnemonic in ["fmin.s", "fmax.s"]:
        frd = clean_reg_fp(args[0])
        frs1 = clean_reg_fp(args[1])
        frs2 = clean_reg_fp(args[2])
        handler_body.append(f"        local _fa = bits_to_f32({frs1}); local _fb = bits_to_f32({frs2})")
        if mnemonic == "fmin.s":
            handler_body.append("        if _fa ~= _fa then _fa = _fb elseif _fb ~= _fb then _fa = _fa elseif _fa == 0 and _fb == 0 and 1/_fa > 0 then _fa = _fb end")
            handler_body.append(f"        {frd} = f32_to_bits(math.min(_fa, _fb))")
        else:
            handler_body.append("        if _fa ~= _fa then _fa = _fb elseif _fb ~= _fb then _fa = _fa elseif _fa == 0 and _fb == 0 and 1/_fa < 0 then _fa = _fb end")
            handler_body.append(f"        {frd} = f32_to_bits(math.max(_fa, _fb))")

    # FP Compare
    elif mnemonic in ["feq.s", "flt.s", "fle.s"]:
        ird = clean_reg(args[0])
        frs1 = clean_reg_fp(args[1])
        frs2 = clean_reg_fp(args[2])
        # x0/zero is hardwired to 0 in RISC-V — never write to reg[1]
        if ird == "reg[1]":
            pass
        else:
            handler_body.append(f"        local _fa = bits_to_f32({frs1}); local _fb = bits_to_f32({frs2})")
            if mnemonic == "feq.s":
                handler_body.append(f"        if _fa ~= _fa or _fb ~= _fb then {ird} = 0 elseif _fa == _fb then {ird} = 1 else {ird} = 0 end")
            elif mnemonic == "flt.s":
                handler_body.append(f"        if _fa ~= _fa or _fb ~= _fb then {ird} = 0 elseif _fa < _fb then {ird} = 1 else {ird} = 0 end")
            elif mnemonic == "fle.s":
                handler_body.append(f"        if _fa ~= _fa or _fb ~= _fb then {ird} = 0 elseif _fa <= _fb then {ird} = 1 else {ird} = 0 end")

    # FP Fused Multiply-Add
    elif mnemonic in ["fmadd.s", "fmsub.s", "fnmadd.s", "fnmsub.s"]:
        frd = clean_reg_fp(args[0])
        frs1 = clean_reg_fp(args[1])
        frs2 = clean_reg_fp(args[2])
        frs3 = clean_reg_fp(args[3])
        handler_body.append(f"        local _fa = bits_to_f32({frs1}); local _fb = bits_to_f32({frs2}); local _fc = bits_to_f32({frs3})")
        if mnemonic == "fmadd.s":
            handler_body.append(f"        {frd} = f32_to_bits(_fa * _fb + _fc)")
        elif mnemonic == "fmsub.s":
            handler_body.append(f"        {frd} = f32_to_bits(_fa * _fb - _fc)")
        elif mnemonic == "fnmadd.s":
            handler_body.append(f"        {frd} = f32_to_bits(-_fa * _fb + _fc)")
        elif mnemonic == "fnmsub.s":
            handler_body.append(f"        {frd} = f32_to_bits(-_fa * _fb - _fc)")

    # FP Sqrt
    elif mnemonic == "fsqrt.s":
        frd = clean_reg_fp(args[0])
        frs1 = clean_reg_fp(args[1])
        handler_body.append(f"        {frd} = f32_to_bits(math.sqrt(bits_to_f32({frs1})))")

    # FP <-> Int Conversion
    elif mnemonic in ["fcvt.s.w", "fcvt.s.wu"]:
        frd = clean_reg_fp(args[0])
        irs1 = clean_reg(args[1])
        if mnemonic == "fcvt.s.w":
            handler_body.append(f"        local _s = if {irs1} >= 0x80000000 then {irs1} - 0x100000000 else {irs1}")
            handler_body.append(f"        {frd} = f32_to_bits(_s)")
        else:
            handler_body.append(f"        local _u = {irs1}")
            handler_body.append(f"        if _u < 0x80000000 then {frd} = f32_to_bits(_u) else {frd} = f32_to_bits(_u - 0x100000000 + 4294967296) end")
    elif mnemonic in ["fcvt.w.s", "fcvt.wu.s"]:
        ird = clean_reg(args[0])
        frs1 = clean_reg_fp(args[1])
        # x0/zero is hardwired to 0 in RISC-V — never write to reg[1]
        if ird == "reg[1]":
            pass
        elif mnemonic == "fcvt.w.s":
            handler_body.append(f"        local _v = bits_to_f32({frs1})")
            handler_body.append(f"        if _v ~= _v then {ird} = 0x7FFFFFFF")
            handler_body.append(f"        elseif _v >= 2147483648 then {ird} = 0x7FFFFFFF")
            handler_body.append(f"        elseif _v < -2147483648 then {ird} = 0x80000000")
            handler_body.append(f"        elseif _v >= 0 then {ird} = bit32.band(math.floor(_v), 0xFFFFFFFF)")
            handler_body.append(f"        else {ird} = bit32.band(math.ceil(_v), 0xFFFFFFFF) end")
        else:
            handler_body.append(f"        local _v = bits_to_f32({frs1})")
            handler_body.append(f"        if _v ~= _v or _v >= 4294967296 or _v < 0 then {ird} = 0xFFFFFFFF")
            handler_body.append(f"        else {ird} = bit32.band(math.floor(_v), 0xFFFFFFFF) end")

    # FP <-> Int Bitwise Move
    elif mnemonic in ["fmv.x.w", "fmv.w.x"]:
        if mnemonic == "fmv.x.w":
            ird = clean_reg(args[0])
            frs1 = clean_reg_fp(args[1])
            # x0/zero is hardwired to 0 in RISC-V — never write to reg[1]
            if ird != "reg[1]":
                handler_body.append(f"        {ird} = {frs1}")
        else:
            frd = clean_reg_fp(args[0])
            irs1 = clean_reg(args[1])
            handler_body.append(f"        {frd} = {irs1}")

    # FP Classify
    elif mnemonic == "fclass.s":
        ird = clean_reg(args[0])
        frs1 = clean_reg_fp(args[1])
        # x0/zero is hardwired to 0 in RISC-V — never write to reg[1]
        if ird == "reg[1]":
            pass
        else:
            handler_body.append(f"        local _v = bits_to_f32({frs1}); local _b = {frs1}")
            handler_body.append(f"        if _v ~= _v then {ird} = bit32.lshift(1, 9)")
            handler_body.append(f"        elseif _v == math.huge then {ird} = bit32.lshift(1, 7)")
            handler_body.append(f"        elseif _v == -math.huge then {ird} = bit32.lshift(1, 0)")
            handler_body.append(f"        elseif _v == 0 then")
            handler_body.append(f"            if bit32.band(_b, 0x80000000) ~= 0 then {ird} = bit32.lshift(1, 3) else {ird} = bit32.lshift(1, 4) end")
            handler_body.append(f"        elseif math.abs(_v) < 1.1754943508222875e-38 then")
            handler_body.append(f"            if _v > 0 then {ird} = bit32.lshift(1, 5) else {ird} = bit32.lshift(1, 2) end")
            handler_body.append(f"        else")
            handler_body.append(f"            if _v > 0 then {ird} = bit32.lshift(1, 6) else {ird} = bit32.lshift(1, 1) end")
            handler_body.append(f"        end")

    handler_body.append(f"        return {addr_int + 4}")
