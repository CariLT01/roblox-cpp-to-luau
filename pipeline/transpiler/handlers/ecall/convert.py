"""convert.py — Type conversion helpers for primitive ↔ OBJECTS bridge.

These emit Luau code that the transpiler inlines when it detects
specific function names (toFloat, fromFloat, etc.) on LuaObj.
No new ecall syscalls — the existing function-name detection
mechanism (like printEPKc) is used instead.
"""


def emit_from_float(handler_body):
    """LuaObj::fromFloat(float) — wrap float bits (in reg[11]) into OBJECTS."""
    handler_body.append("        OBJECTS[S.NEXT_HANDLE] = bits_to_f32(reg[11])")
    handler_body.append("        reg[11] = S.NEXT_HANDLE")
    handler_body.append("        S.NEXT_HANDLE = S.NEXT_HANDLE + 1")


def emit_to_float(handler_body):
    """LuaObj::toFloat() — extract float bits from OBJECTS[reg[11]]."""
    handler_body.append("        local _v = OBJECTS[reg[11]]")
    handler_body.append("        reg[11] = _v and f32_to_bits(_v) or 0")


def emit_from_int(handler_body):
    """LuaObj::fromInt(int) — wrap int (in reg[11]) into OBJECTS."""
    handler_body.append("        OBJECTS[S.NEXT_HANDLE] = reg[11]")
    handler_body.append("        reg[11] = S.NEXT_HANDLE")
    handler_body.append("        S.NEXT_HANDLE = S.NEXT_HANDLE + 1")


def emit_to_int(handler_body):
    """LuaObj::toInt() — extract int from OBJECTS[reg[11]]."""
    handler_body.append("        local _v = OBJECTS[reg[11]]")
    handler_body.append("        reg[11] = _v or 0")


def emit_from_bool(handler_body):
    """LuaObj::fromBool(bool) — wrap bool (in reg[11]) into OBJECTS."""
    handler_body.append("        OBJECTS[S.NEXT_HANDLE] = (reg[11] ~= 0)")
    handler_body.append("        reg[11] = S.NEXT_HANDLE")
    handler_body.append("        S.NEXT_HANDLE = S.NEXT_HANDLE + 1")


def emit_to_bool(handler_body):
    """LuaObj::toBool() — extract bool from OBJECTS[reg[11]]."""
    handler_body.append("        local _v = OBJECTS[reg[11]]")
    handler_body.append("        reg[11] = (_v and _v ~= false and _v ~= 0) and 1 or 0")


def emit_from_string(handler_body):
    """LuaObj::fromString(const char*) — wrap rodata string into OBJECTS."""
    handler_body.append("        OBJECTS[S.NEXT_HANDLE] = RODATA[reg[11]] or ''")
    handler_body.append("        reg[11] = S.NEXT_HANDLE")
    handler_body.append("        S.NEXT_HANDLE = S.NEXT_HANDLE + 1")


def emit_to_string(handler_body):
    """LuaObj::toString() — extract string from OBJECTS[reg[11]], write to heap."""
    handler_body.append("        local _s = OBJECTS[reg[11]]")
    handler_body.append("        if _s and _s ~= '' then")
    handler_body.append("            local _len = #_s")
    handler_body.append("            local _ptr = S.HEAP_BRK")
    handler_body.append("            S.HEAP_BRK = S.HEAP_BRK + _len + 1")
    handler_body.append("            for _i = 1, _len do")
    handler_body.append("                write_mem8(_ptr + _i - 1, string.byte(_s, _i))")
    handler_body.append("            end")
    handler_body.append("            write_mem8(_ptr + _len, 0)  -- null terminator")
    handler_body.append("            reg[11] = _ptr")
    handler_body.append("        else")
    handler_body.append("            reg[11] = 0")
    handler_body.append("        end")
