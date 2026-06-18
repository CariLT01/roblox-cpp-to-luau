"""conversions.py — Unified object ↔ C++ value bridge (syscalls 78/79).

Consolidates all struct conversions (old syscalls 54-61, then 76-77) AND
primitive conversions (old syscalls 66-73) into two syscalls:

  Syscall 78: objectRead  — OBJECTS handle → C++ value
  Syscall 79: objectWrite — C++ value → OBJECTS handle

Register layout (same for read and write):
  a0 = primary input (objHandle for read, src/value for write)
  a1 = type_id
  a2 = dst pointer for struct reads (0 / unused for primitives)

Type IDs:
  0 = Vector3 (multi-float, memory-backed)
  1 = CFrame   (multi-float, memory-backed, uses GetComponents on read)
  2 = Color3   (multi-float, memory-backed)
  3 = UDim2    (multi-float, memory-backed)
  4 = float    (register passthrough)
  5 = int      (register passthrough)
  6 = bool     (register passthrough)
  7 = string   (pointer passthrough: rodata addr → OBJECTS, OBJECTS → heap)
  8 = function (fromFunction: wraps C++ address into callable Luau function)
"""

# ── Type registry ─────────────────────────────────────────────────────────────

CONVERSION_TYPES = {
    # ── Struct types (memory-backed) ───────────────────────────────────────
    0: {
        "kind": "struct",
        "name": "Vector3",
        "field_count": 3,
        "read_fields":    [("X", 0), ("Y", 4), ("Z", 8)],
        "write_offsets":  [0, 4, 8],
        "write_vars":     ["_x", "_y", "_z"],
        "write_ctor":     "Vector3.new(_x, _y, _z)",
    },
    1: {
        "kind": "struct",
        "name": "CFrame",
        "field_count": 12,
        "read_is_cframe": True,
        "write_offsets":  [0, 4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 44],
        "write_vars":     ["_x", "_y", "_z", "_r00", "_r01", "_r02",
                           "_r10", "_r11", "_r12", "_r20", "_r21", "_r22"],
        "write_ctor":     "CFrame.new(_x, _y, _z, _r00, _r01, _r02, "
                          "_r10, _r11, _r12, _r20, _r21, _r22)",
    },
    2: {
        "kind": "struct",
        "name": "Color3",
        "field_count": 3,
        "read_fields":    [("R", 0), ("G", 4), ("B", 8)],
        "write_offsets":  [0, 4, 8],
        "write_vars":     ["_r", "_g", "_b"],
        "write_ctor":     "Color3.new(_r, _g, _b)",
    },
    3: {
        "kind": "struct",
        "name": "UDim2",
        "field_count": 4,
        "read_fields":    [("X.Scale", 0), ("X.Offset", 4),
                           ("Y.Scale", 8), ("Y.Offset", 12)],
        "write_offsets":  [0, 4, 8, 12],
        "write_vars":     ["_xs", "_xo", "_ys", "_yo"],
        "write_ctor":     "UDim2.new(_xs, _xo, _ys, _yo)",
    },

    # ── Primitive types (register-based) ───────────────────────────────────
    4: {
        "kind": "primitive",
        "name": "float",
        "read_luau":  "local _v = OBJECTS[reg[11]]; "
                       "reg[11] = _v and f32_to_bits(_v) or 0",
        "write_luau": "OBJECTS[S.NEXT_HANDLE] = bits_to_f32(reg[11]); "
                       "reg[11] = S.NEXT_HANDLE; "
                       "S.NEXT_HANDLE = S.NEXT_HANDLE + 1",
    },
    5: {
        "kind": "primitive",
        "name": "int",
        "read_luau":  "local _v = OBJECTS[reg[11]]; reg[11] = _v or 0",
        "write_luau": "OBJECTS[S.NEXT_HANDLE] = reg[11]; "
                       "reg[11] = S.NEXT_HANDLE; "
                       "S.NEXT_HANDLE = S.NEXT_HANDLE + 1",
    },
    6: {
        "kind": "primitive",
        "name": "bool",
        "read_luau":  "local _v = OBJECTS[reg[11]]; "
                       "reg[11] = (_v and _v ~= false and _v ~= 0) and 1 or 0",
        "write_luau": "OBJECTS[S.NEXT_HANDLE] = (reg[11] ~= 0); "
                       "reg[11] = S.NEXT_HANDLE; "
                       "S.NEXT_HANDLE = S.NEXT_HANDLE + 1",
    },
    7: {
        "kind": "primitive",
        "name": "string",
        "read_luau":  "local _s = OBJECTS[reg[11]]; "
                       "if _s and _s ~= '' then "
                       "local _len = #_s; "
                       "local _ptr = S.HEAP_BRK; "
                       "S.HEAP_BRK = S.HEAP_BRK + _len + 1; "
                       "for _i = 1, _len do "
                       "write_mem8(_ptr + _i - 1, string.byte(_s, _i)) "
                       "end; "
                       "write_mem8(_ptr + _len, 0); "
                       "reg[11] = _ptr "
                       "else reg[11] = 0 end",
        "write_luau": "OBJECTS[S.NEXT_HANDLE] = RODATA[reg[11]] or ''; "
                       "reg[11] = S.NEXT_HANDLE; "
                       "S.NEXT_HANDLE = S.NEXT_HANDLE + 1",
    },
    8: {
        "kind": "primitive",
        "name": "function",
        "read_luau":  None,  # function read is not used
        "write_luau": "local _wrapper = S.get_function(reg[11]); "
                       "OBJECTS[S.NEXT_HANDLE] = _wrapper; "
                       "reg[11] = S.NEXT_HANDLE; "
                       "S.NEXT_HANDLE = S.NEXT_HANDLE + 1",
    },
}

# Aliases
TYPE_VECTOR3   = 0
TYPE_CFRAME    = 1
TYPE_COLOR3    = 2
TYPE_UDIM2     = 3
TYPE_FLOAT     = 4
TYPE_INT       = 5
TYPE_BOOL      = 6
TYPE_STRING    = 7
TYPE_FUNCTION  = 8

STRUCT_TYPE_IDS = {0, 1, 2, 3}


# ── Public API ────────────────────────────────────────────────────────────────

def emit_object_read(handler_body, type_id=None):
    """Syscall 78: objectRead — OBJECTS handle → C++ value.

    a0 (reg[11]) = objHandle  — OBJECTS index to read from
    a1 (reg[12]) = type_id    — what kind of value
    a2 (reg[13]) = dst ptr    — memory destination for structs (unused for primitives)
    Returns a0 = result value (for primitives; structs write to memory)

    If type_id is provided (compile-time known), generates specialized code.
    Otherwise generates runtime dispatch on reg[12] (a1).
    """
    if type_id is not None:
        info = CONVERSION_TYPES[type_id]
        if info["kind"] == "struct":
            handler_body.append("        local _obj = OBJECTS[reg[11]]  -- a0 = objHandle")
            handler_body.append("        local _out = reg[13]  -- a2 = dst pointer")
            _emit_struct_read_typed(handler_body, info)
        else:
            handler_body.append(f"        -- objectRead({info['name']})")
            handler_body.append(f"        {info['read_luau']}")
    else:
        handler_body.append("        local _typeId = reg[12]  -- a1 = type_id")
        handler_body.append("        local _obj = OBJECTS[reg[11]]  -- a0 = objHandle")
        handler_body.append("        if _typeId <= 3 then  -- struct types")
        handler_body.append("            local _out = reg[13]  -- a2 = dst pointer for structs")
        handler_body.append("            if _typeId == 0 then  -- Vector3")
        _emit_struct_read_typed(handler_body, CONVERSION_TYPES[0], indent="                ")
        handler_body.append("            elseif _typeId == 1 then  -- CFrame")
        _emit_struct_read_typed(handler_body, CONVERSION_TYPES[1], indent="                ")
        handler_body.append("            elseif _typeId == 2 then  -- Color3")
        _emit_struct_read_typed(handler_body, CONVERSION_TYPES[2], indent="                ")
        handler_body.append("            elseif _typeId == 3 then  -- UDim2")
        _emit_struct_read_typed(handler_body, CONVERSION_TYPES[3], indent="                ")
        handler_body.append("            end")
        handler_body.append("        else  -- primitive types")
        handler_body.append("            if _typeId == 4 then  -- float")
        handler_body.append(f"                {CONVERSION_TYPES[4]['read_luau']}")
        handler_body.append("            elseif _typeId == 5 then  -- int")
        handler_body.append(f"                {CONVERSION_TYPES[5]['read_luau']}")
        handler_body.append("            elseif _typeId == 6 then  -- bool")
        handler_body.append(f"                {CONVERSION_TYPES[6]['read_luau']}")
        handler_body.append("            elseif _typeId == 7 then  -- string")
        handler_body.append(f"                {CONVERSION_TYPES[7]['read_luau']}")
        handler_body.append("            end")
        handler_body.append("        end")


def _emit_struct_read_typed(handler_body, info, indent=""):
    """Emit read code for a specific struct type."""
    if info.get("read_is_cframe"):
        handler_body.append(f"{indent}        if _obj then")
        handler_body.append(f"{indent}            local _x, _y, _z, "
                           f"_r00, _r01, _r02, _r10, _r11, _r12, "
                           f"_r20, _r21, _r22 = _obj:GetComponents()")
        for var_name, offset in zip(info["write_vars"], info["write_offsets"]):
            handler_body.append(f"{indent}            write_mem32(_out + {offset}, f32_to_bits({var_name}))")
        handler_body.append(f"{indent}        end")
    else:
        handler_body.append(f"{indent}        if _obj then")
        for field, offset in info["read_fields"]:
            handler_body.append(f"{indent}            write_mem32(_out + {offset}, f32_to_bits(_obj.{field}))")
        handler_body.append(f"{indent}        end")


def emit_object_write(handler_body, type_id=None):
    """Syscall 79: objectWrite — C++ value → OBJECTS handle.

    a0 (reg[11]) = src/value  — memory ptr for structs, register value for primitives
    a1 (reg[12]) = type_id    — what kind of value
    Returns a0 = OBJECTS handle

    If type_id is provided (compile-time known), generates specialized code.
    Otherwise generates runtime dispatch on reg[12] (a1).
    """
    if type_id is not None:
        info = CONVERSION_TYPES[type_id]
        if info["kind"] == "struct":
            handler_body.append("        local _src = reg[11]  -- a0 = source memory")
            _emit_struct_write_typed(handler_body, info)
        else:
            handler_body.append(f"        -- objectWrite({info['name']})")
            handler_body.append(f"        {info['write_luau']}")
    else:
        handler_body.append("        local _src = reg[11]  -- a0 = source / value")
        handler_body.append("        local _typeId = reg[12]  -- a1 = type_id")
        handler_body.append("        if _typeId <= 3 then  -- struct types")
        handler_body.append("            if _typeId == 0 then  -- Vector3")
        _emit_struct_write_typed(handler_body, CONVERSION_TYPES[0], indent="                ")
        handler_body.append("            elseif _typeId == 1 then  -- CFrame")
        _emit_struct_write_typed(handler_body, CONVERSION_TYPES[1], indent="                ")
        handler_body.append("            elseif _typeId == 2 then  -- Color3")
        _emit_struct_write_typed(handler_body, CONVERSION_TYPES[2], indent="                ")
        handler_body.append("            elseif _typeId == 3 then  -- UDim2")
        _emit_struct_write_typed(handler_body, CONVERSION_TYPES[3], indent="                ")
        handler_body.append("            end")
        handler_body.append("        else  -- primitive types")
        handler_body.append("            if _typeId == 4 then  -- float")
        handler_body.append(f"                {CONVERSION_TYPES[4]['write_luau']}")
        handler_body.append("            elseif _typeId == 5 then  -- int")
        handler_body.append(f"                {CONVERSION_TYPES[5]['write_luau']}")
        handler_body.append("            elseif _typeId == 6 then  -- bool")
        handler_body.append(f"                {CONVERSION_TYPES[6]['write_luau']}")
        handler_body.append("            elseif _typeId == 7 then  -- string")
        handler_body.append(f"                {CONVERSION_TYPES[7]['write_luau']}")
        handler_body.append("            elseif _typeId == 8 then  -- function")
        handler_body.append(f"                {CONVERSION_TYPES[8]['write_luau']}")
        handler_body.append("            end")
        handler_body.append("        end")


def _emit_struct_write_typed(handler_body, info, indent=""):
    """Emit write code for a specific struct type."""
    for var_name, offset in zip(info["write_vars"], info["write_offsets"]):
        handler_body.append(f"{indent}        local {var_name} = bits_to_f32(read_mem32(_src + {offset}))")
    handler_body.append(f"{indent}        OBJECTS[S.NEXT_HANDLE] = {info['write_ctor']}")
    handler_body.append(f"{indent}        reg[11] = S.NEXT_HANDLE")
    handler_body.append(f"{indent}        S.NEXT_HANDLE = S.NEXT_HANDLE + 1")
