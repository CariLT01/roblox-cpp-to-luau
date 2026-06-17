"""Shared ecall helper functions for emitting Luau handler code."""

from ...utils import escape_lua_string
import re


def _emit_malloc(handler_body):
    handler_body.append("        local _size = reg[11]")
    handler_body.append("        if _size == 0 then reg[11] = 0 else")
    handler_body.append("            local _found = false")
    handler_body.append("            for _addr, _fsize in pairs(FREE_LIST) do")
    handler_body.append("                if _fsize >= _size then")
    handler_body.append("                    FREE_LIST[_addr] = nil")
    handler_body.append("                    if _fsize > _size then")
    handler_body.append("                        FREE_LIST[_addr + _size] = _fsize - _size")
    handler_body.append("                    end")
    handler_body.append("                    reg[11] = _addr")
    handler_body.append("                    ALLOCS[_addr] = _size")
    handler_body.append("                    _found = true")
    handler_body.append("                    break")
    handler_body.append("                end")
    handler_body.append("            end")
    handler_body.append("            if not _found then")
    handler_body.append("                reg[11] = S.HEAP_BRK")
    handler_body.append("                ALLOCS[S.HEAP_BRK] = _size")
    handler_body.append("                S.HEAP_BRK = S.HEAP_BRK + _size")
    handler_body.append("            end")
    handler_body.append("        end")


def _emit_generic_callmethod(handler_body, tracked_a3_literal,
                             tracked_a1_rodata_str, tracked_a2_rodata_str,
                             tracked_a4_rodata_str, tracked_a5_rodata_str,
                             tracked_a5_literal, tracked_a2_literal):
    """Syscall 46: generic templated method call.
    
    Register layout:
      a0 (reg[11]) = handle
      a1 (reg[12]) = methodName ptr
      a2 (reg[13]) = arg1
      a3 (reg[14]) = flags
      a4 (reg[15]) = arg2
      a5 (reg[16]) = arg3
      a6 (reg[17]) = arg4
    
    Flags bits:
      0 (1)    = hasReturn
      1 (2)    = returnIsObject
      2 (4)    = isService
      3 (8)    = arg1IsString
      4 (16)   = arg2IsString
      5 (32)   = returnIsBuffer
      6 (64)   = arg3IsString
      7 (128)  = arg4IsString
      8 (256)  = isStaticCall (. syntax, no implicit self)
      9 (512)  = arg1IsBuffer
      10 (1024)= arg2IsBuffer
      11 (2048)= arg3IsBuffer
      12 (4096)= arg4IsBuffer
      13 (8192)= arg1IsFunction
      14 (16384)=arg2IsFunction
      15 (32768)=arg3IsFunction
      16 (65536)=arg4IsFunction
      17 (131072)=arg1IsObject
      18 (262144)=arg2IsObject
      19 (524288)=arg3IsObject
      20 (1048576)=arg4IsObject
    """
    flags = 0
    try:
        flags = int(tracked_a3_literal) if tracked_a3_literal.replace('-', '').isdigit() else 0
    except (ValueError, AttributeError):
        pass
    has_return = bool(flags & 1)
    return_is_obj = bool(flags & 2)
    is_service = bool(flags & 4)
    arg1_is_string = bool(flags & 8)
    arg2_is_string = bool(flags & 16)
    return_is_buffer = bool(flags & 32)
    arg3_is_string = bool(flags & 64)
    arg4_is_string = bool(flags & 128)
    is_static = bool(flags & 256)
    arg1_is_buffer = bool(flags & 512)
    arg2_is_buffer = bool(flags & 1024)
    arg3_is_buffer = bool(flags & 2048)
    arg4_is_buffer = bool(flags & 4096)
    arg1_is_function = bool(flags & 8192)
    arg2_is_function = bool(flags & 16384)
    arg3_is_function = bool(flags & 32768)
    arg4_is_function = bool(flags & 65536)
    arg1_is_object = bool(flags & 131072)   # 1 << 17
    arg2_is_object = bool(flags & 262144)   # 1 << 18
    arg3_is_object = bool(flags & 524288)   # 1 << 19
    arg4_is_object = bool(flags & 1048576)  # 1 << 20

    method_name = tracked_a1_rodata_str

    if method_name:
        method_literal = '"' + escape_lua_string(method_name) + '"'
        is_valid_id = re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', method_name) is not None

        if is_service:
            svc_name = tracked_a2_rodata_str
            if svc_name:
                handler_body.append(f'        local _svc = game:GetService("{escape_lua_string(svc_name)}")')
            else:
                handler_body.append('        local _svc = game:GetService(RODATA[reg[13]] or "?")')
            handler_body.append('        if _svc then')

            # Service path: arg1 is in a5 (reg[16]), arg2 in a4 (reg[15])
            # arg3 in a6 (reg[17]), arg4 can't be passed (a7 used for syscall)
            arg_parts = []
            if arg1_is_function:
                arg_parts.append('S.get_function(reg[16])')
            elif arg1_is_buffer:
                arg_parts.append('BUFFERS[reg[16]]')
            elif arg1_is_string:
                arg_parts.append('RODATA[reg[16]] or ""')
            elif arg1_is_object:
                arg_parts.append('OBJECTS[reg[16]]')
            elif tracked_a5_rodata_str is not None or (tracked_a5_literal and tracked_a5_literal != 'nil'):
                arg_parts.append('reg[16]')
            if arg2_is_function:
                arg_parts.append('S.get_function(reg[15])')
            elif arg2_is_buffer:
                arg_parts.append('BUFFERS[reg[15]]')
            elif arg2_is_string:
                arg_parts.append('RODATA[reg[15]] or ""')
            elif arg2_is_object:
                arg_parts.append('OBJECTS[reg[15]]')
            elif tracked_a4_rodata_str is not None:
                arg_parts.append('RODATA[reg[15]] or ""')
            if arg3_is_function:
                arg_parts.append('S.get_function(reg[17])')
            elif arg3_is_buffer:
                arg_parts.append('BUFFERS[reg[17]]')
            elif arg3_is_string:
                arg_parts.append('RODATA[reg[17]] or ""')
            elif arg3_is_object:
                arg_parts.append('OBJECTS[reg[17]]')

            args_str = ', ' + ', '.join(arg_parts) if arg_parts else ''

            if has_return:
                if is_valid_id:
                    if is_static:
                        handler_body.append(f'            local _r = _svc.{method_name}({args_str[2:]})')
                    else:
                        handler_body.append(f'            local _r = _svc:{method_name}({args_str[2:]})')
                else:
                    if is_static:
                        handler_body.append(f'            local _r = _svc[{method_literal}]({args_str[2:]})')
                    else:
                        handler_body.append(f'            local _r = _svc[{method_literal}](_svc{args_str})')
                _emit_callmethod_return(handler_body, return_is_obj, return_is_buffer)
            else:
                if is_valid_id:
                    if is_static:
                        handler_body.append(f'            _svc.{method_name}({args_str[2:]})')
                    else:
                        handler_body.append(f'            _svc:{method_name}({args_str[2:]})')
                else:
                    if is_static:
                        handler_body.append(f'            _svc[{method_literal}]({args_str[2:]})')
                    else:
                        handler_body.append(f'            _svc[{method_literal}](_svc{args_str})')
            handler_body.append('        end')
        else:
            # Normal object path: a0=handle, a1=method, a2=arg1, a3=flags, a4=arg2, a5=arg3, a6=arg4
            handler_body.append('        local _obj = OBJECTS[reg[11]]')
            handler_body.append('        if _obj then')

            arg_parts = []
            if arg1_is_function:
                arg_parts.append('S.get_function(reg[13])')
            elif arg1_is_buffer:
                arg_parts.append('BUFFERS[reg[13]]')
            elif arg1_is_string:
                arg_parts.append('RODATA[reg[13]] or ""')
            elif arg1_is_object:
                arg_parts.append('OBJECTS[reg[13]]')
            elif tracked_a2_literal != 'nil' and tracked_a2_literal is not None:
                arg_parts.append('reg[13]')
            if arg2_is_function:
                arg_parts.append('S.get_function(reg[15])')
            elif arg2_is_buffer:
                arg_parts.append('BUFFERS[reg[15]]')
            elif arg2_is_string:
                arg_parts.append('RODATA[reg[15]] or ""')
            elif arg2_is_object:
                arg_parts.append('OBJECTS[reg[15]]')
            elif tracked_a4_rodata_str is not None:
                arg_parts.append('RODATA[reg[15]] or ""')
            if arg3_is_function:
                arg_parts.append('S.get_function(reg[16])')
            elif arg3_is_buffer:
                arg_parts.append('BUFFERS[reg[16]]')
            elif arg3_is_string:
                arg_parts.append('RODATA[reg[16]] or ""')
            elif arg3_is_object:
                arg_parts.append('OBJECTS[reg[16]]')
            if arg4_is_function:
                arg_parts.append('S.get_function(reg[17])')
            elif arg4_is_buffer:
                arg_parts.append('BUFFERS[reg[17]]')
            elif arg4_is_string:
                arg_parts.append('RODATA[reg[17]] or ""')
            elif arg4_is_object:
                arg_parts.append('OBJECTS[reg[17]]')

            args_str = ', ' + ', '.join(arg_parts) if arg_parts else ''

            if has_return:
                if is_valid_id:
                    if is_static:
                        handler_body.append(f'            local _r = _obj.{method_name}({args_str[2:]})')
                    else:
                        handler_body.append(f'            local _r = _obj:{method_name}({args_str[2:]})')
                else:
                    if is_static:
                        handler_body.append(f'            local _r = _obj[{method_literal}]({args_str[2:]})')
                    else:
                        handler_body.append(f'            local _r = _obj[{method_literal}](_obj{args_str})')
                _emit_callmethod_return(handler_body, return_is_obj, return_is_buffer)
            else:
                if is_valid_id:
                    if is_static:
                        handler_body.append(f'            _obj.{method_name}({args_str[2:]})')
                    else:
                        handler_body.append(f'            _obj:{method_name}({args_str[2:]})')
                else:
                    if is_static:
                        handler_body.append(f'            _obj[{method_literal}]({args_str[2:]})')
                    else:
                        handler_body.append(f'            _obj[{method_literal}](_obj{args_str})')
            handler_body.append('        end')
    else:
        # Method name not resolved at transpile time
        handler_body.append("        local _obj = OBJECTS[reg[11]]")
        handler_body.append("        local _methodName = RODATA[reg[12]] or '?'")
        handler_body.append("        local _flags = reg[14]")
        handler_body.append("        if _obj and _methodName then")
        handler_body.append("            -- Runtime dynamic dispatch (slower, no templating)")
        handler_body.append("            local _hasReturn = bit32.band(_flags, 1) ~= 0")
        handler_body.append("            local _returnIsObj = bit32.band(_flags, 2) ~= 0")
        handler_body.append("            local _returnIsBuffer = bit32.band(_flags, 32) ~= 0")
        handler_body.append("            local _arg1IsFn  = bit32.band(_flags, 8192) ~= 0")
        handler_body.append("            local _arg1IsBuf = bit32.band(_flags, 512) ~= 0")
        handler_body.append("            local _arg1IsStr = bit32.band(_flags, 8) ~= 0")
        handler_body.append("            local _arg1IsObj = bit32.band(_flags, 131072) ~= 0")
        handler_body.append("            local _arg2IsFn  = bit32.band(_flags, 16384) ~= 0")
        handler_body.append("            local _arg2IsBuf = bit32.band(_flags, 1024) ~= 0")
        handler_body.append("            local _arg2IsStr = bit32.band(_flags, 16) ~= 0")
        handler_body.append("            local _arg2IsObj = bit32.band(_flags, 262144) ~= 0")
        handler_body.append("            local _arg3IsFn  = bit32.band(_flags, 32768) ~= 0")
        handler_body.append("            local _arg3IsBuf = bit32.band(_flags, 2048) ~= 0")
        handler_body.append("            local _arg3IsStr = bit32.band(_flags, 64) ~= 0")
        handler_body.append("            local _arg3IsObj = bit32.band(_flags, 524288) ~= 0")
        handler_body.append("            local _arg4IsFn  = bit32.band(_flags, 65536) ~= 0")
        handler_body.append("            local _arg4IsBuf = bit32.band(_flags, 4096) ~= 0")
        handler_body.append("            local _arg4IsStr = bit32.band(_flags, 128) ~= 0")
        handler_body.append("            local _arg4IsObj = bit32.band(_flags, 1048576) ~= 0")
        handler_body.append("            local _isStatic = bit32.band(_flags, 256) ~= 0")
        handler_body.append("            local _args = {}")
        handler_body.append("            if not _isStatic then _args[1] = _obj end")
        handler_body.append("            if _arg1IsFn then _args[#_args + 1] = S.get_function(reg[13]) elseif _arg1IsBuf then _args[#_args + 1] = BUFFERS[reg[13]] elseif _arg1IsObj then _args[#_args + 1] = OBJECTS[reg[13]] elseif _arg1IsStr then local _s = RODATA[reg[13]] or ''; _args[#_args + 1] = _s else _args[#_args + 1] = reg[13] end")
        handler_body.append("            if _arg2IsFn then _args[#_args + 1] = S.get_function(reg[15]) elseif _arg2IsBuf then _args[#_args + 1] = BUFFERS[reg[15]] elseif _arg2IsObj then _args[#_args + 1] = OBJECTS[reg[15]] elseif _arg2IsStr then local _s = RODATA[reg[15]] or ''; _args[#_args + 1] = _s else _args[#_args + 1] = reg[15] end")
        handler_body.append("            if _arg3IsFn then _args[#_args + 1] = S.get_function(reg[16]) elseif _arg3IsBuf then _args[#_args + 1] = BUFFERS[reg[16]] elseif _arg3IsObj then _args[#_args + 1] = OBJECTS[reg[16]] elseif _arg3IsStr then local _s = RODATA[reg[16]] or ''; _args[#_args + 1] = _s else _args[#_args + 1] = reg[16] end")
        handler_body.append("            if _arg4IsFn then _args[#_args + 1] = S.get_function(reg[17]) elseif _arg4IsBuf then _args[#_args + 1] = BUFFERS[reg[17]] elseif _arg4IsObj then _args[#_args + 1] = OBJECTS[reg[17]] elseif _arg4IsStr then local _s = RODATA[reg[17]] or ''; _args[#_args + 1] = _s else _args[#_args + 1] = reg[17] end")
        handler_body.append("            if _hasReturn then")
        handler_body.append("                local _r = _obj[_methodName](table.unpack(_args))")
        handler_body.append("                if _returnIsBuffer then")
        handler_body.append("                    BUFFERS[S.NEXT_HANDLE] = _r")
        handler_body.append("                    reg[11] = S.NEXT_HANDLE")
        handler_body.append("                    S.NEXT_HANDLE = S.NEXT_HANDLE + 1")
        handler_body.append("                elseif _returnIsObj then")
        handler_body.append("                    if _r then")
        handler_body.append("                        OBJECTS[S.NEXT_HANDLE] = _r")
        handler_body.append("                        reg[11] = S.NEXT_HANDLE")
        handler_body.append("                        S.NEXT_HANDLE = S.NEXT_HANDLE + 1")
        handler_body.append("                    else")
        handler_body.append("                        reg[11] = 0")
        handler_body.append("                    end")
        handler_body.append("                else")
        handler_body.append("                    reg[11] = _r or 0")
        handler_body.append("                end")
        handler_body.append("            else")
        handler_body.append("                _obj[_methodName](table.unpack(_args))")
        handler_body.append("            end")
        handler_body.append("        end")


def _emit_callmethod_return(handler_body, return_is_obj, return_is_buffer):
    if return_is_obj:
        handler_body.append('            if _r then')
        handler_body.append('                OBJECTS[S.NEXT_HANDLE] = _r')
        handler_body.append('                reg[11] = S.NEXT_HANDLE')
        handler_body.append('                S.NEXT_HANDLE = S.NEXT_HANDLE + 1')
        handler_body.append('            else')
        handler_body.append('                reg[11] = 0')
        handler_body.append('            end')
    elif return_is_buffer:
        handler_body.append('            BUFFERS[S.NEXT_HANDLE] = _r')
        handler_body.append('            reg[11] = S.NEXT_HANDLE')
        handler_body.append('            S.NEXT_HANDLE = S.NEXT_HANDLE + 1')
    else:
        handler_body.append('            reg[11] = _r or 0')


# ── Struct ↔ OBJECTS table bridge ──────────────────────────────────────────────

def _emit_struct_read_vec3(handler_body):
    """Syscall 54: Read Vector3 from OBJECTS[reg[11]] into *reg[12]."""
    handler_body.append("        local _v = OBJECTS[reg[11]]")
    handler_body.append("        if _v then")
    handler_body.append("            local _out = reg[12]")
    handler_body.append("            write_mem32(_out + 0, f32_to_bits(_v.X))")
    handler_body.append("            write_mem32(_out + 4, f32_to_bits(_v.Y))")
    handler_body.append("            write_mem32(_out + 8, f32_to_bits(_v.Z))")
    handler_body.append("        end")


def _emit_struct_write_vec3(handler_body):
    """Syscall 55: Store *reg[11] as Vector3 in OBJECTS, return handle."""
    handler_body.append("        local _src = reg[11]")
    handler_body.append("        local _x = bits_to_f32(read_mem32(_src + 0))")
    handler_body.append("        local _y = bits_to_f32(read_mem32(_src + 4))")
    handler_body.append("        local _z = bits_to_f32(read_mem32(_src + 8))")
    handler_body.append("        OBJECTS[S.NEXT_HANDLE] = Vector3.new(_x, _y, _z)")
    handler_body.append("        reg[11] = S.NEXT_HANDLE")
    handler_body.append("        S.NEXT_HANDLE = S.NEXT_HANDLE + 1")


def _emit_struct_read_cframe(handler_body):
    """Syscall 56: Read CFrame from OBJECTS[reg[11]] into *reg[12]."""
    handler_body.append("        local _cf = OBJECTS[reg[11]]")
    handler_body.append("        if _cf then")
    handler_body.append("            local _out = reg[12]")
    handler_body.append("            local _x, _y, _z, _r00, _r01, _r02, _r10, _r11, _r12, _r20, _r21, _r22 = _cf:GetComponents()")
    handler_body.append("            write_mem32(_out + 0, f32_to_bits(_x))")
    handler_body.append("            write_mem32(_out + 4, f32_to_bits(_y))")
    handler_body.append("            write_mem32(_out + 8, f32_to_bits(_z))")
    handler_body.append("            write_mem32(_out + 12, f32_to_bits(_r00))")
    handler_body.append("            write_mem32(_out + 16, f32_to_bits(_r01))")
    handler_body.append("            write_mem32(_out + 20, f32_to_bits(_r02))")
    handler_body.append("            write_mem32(_out + 24, f32_to_bits(_r10))")
    handler_body.append("            write_mem32(_out + 28, f32_to_bits(_r11))")
    handler_body.append("            write_mem32(_out + 32, f32_to_bits(_r12))")
    handler_body.append("            write_mem32(_out + 36, f32_to_bits(_r20))")
    handler_body.append("            write_mem32(_out + 40, f32_to_bits(_r21))")
    handler_body.append("            write_mem32(_out + 44, f32_to_bits(_r22))")
    handler_body.append("        end")


def _emit_struct_write_cframe(handler_body):
    """Syscall 57: Store *reg[11] as CFrame in OBJECTS, return handle."""
    handler_body.append("        local _src = reg[11]")
    handler_body.append("        local _x = bits_to_f32(read_mem32(_src + 0))")
    handler_body.append("        local _y = bits_to_f32(read_mem32(_src + 4))")
    handler_body.append("        local _z = bits_to_f32(read_mem32(_src + 8))")
    handler_body.append("        local _r00 = bits_to_f32(read_mem32(_src + 12))")
    handler_body.append("        local _r01 = bits_to_f32(read_mem32(_src + 16))")
    handler_body.append("        local _r02 = bits_to_f32(read_mem32(_src + 20))")
    handler_body.append("        local _r10 = bits_to_f32(read_mem32(_src + 24))")
    handler_body.append("        local _r11 = bits_to_f32(read_mem32(_src + 28))")
    handler_body.append("        local _r12 = bits_to_f32(read_mem32(_src + 32))")
    handler_body.append("        local _r20 = bits_to_f32(read_mem32(_src + 36))")
    handler_body.append("        local _r21 = bits_to_f32(read_mem32(_src + 40))")
    handler_body.append("        local _r22 = bits_to_f32(read_mem32(_src + 44))")
    handler_body.append("        OBJECTS[S.NEXT_HANDLE] = CFrame.new(_x, _y, _z, _r00, _r01, _r02, _r10, _r11, _r12, _r20, _r21, _r22)")
    handler_body.append("        reg[11] = S.NEXT_HANDLE")
    handler_body.append("        S.NEXT_HANDLE = S.NEXT_HANDLE + 1")


def _emit_struct_read_color3(handler_body):
    """Syscall 58: Read Color3 from OBJECTS[reg[11]] into *reg[12]."""
    handler_body.append("        local _c = OBJECTS[reg[11]]")
    handler_body.append("        if _c then")
    handler_body.append("            local _out = reg[12]")
    handler_body.append("            write_mem32(_out + 0, f32_to_bits(_c.R))")
    handler_body.append("            write_mem32(_out + 4, f32_to_bits(_c.G))")
    handler_body.append("            write_mem32(_out + 8, f32_to_bits(_c.B))")
    handler_body.append("        end")


def _emit_struct_write_color3(handler_body):
    """Syscall 59: Store *reg[11] as Color3 in OBJECTS, return handle."""
    handler_body.append("        local _src = reg[11]")
    handler_body.append("        local _r = bits_to_f32(read_mem32(_src + 0))")
    handler_body.append("        local _g = bits_to_f32(read_mem32(_src + 4))")
    handler_body.append("        local _b = bits_to_f32(read_mem32(_src + 8))")
    handler_body.append("        OBJECTS[S.NEXT_HANDLE] = Color3.new(_r, _g, _b)")
    handler_body.append("        reg[11] = S.NEXT_HANDLE")
    handler_body.append("        S.NEXT_HANDLE = S.NEXT_HANDLE + 1")


def _emit_struct_read_udim2(handler_body):
    """Syscall 60: Read UDim2 from OBJECTS[reg[11]] into *reg[12]."""
    handler_body.append("        local _u = OBJECTS[reg[11]]")
    handler_body.append("        if _u then")
    handler_body.append("            local _out = reg[12]")
    handler_body.append("            write_mem32(_out + 0, f32_to_bits(_u.X.Scale))")
    handler_body.append("            write_mem32(_out + 4, f32_to_bits(_u.X.Offset))")
    handler_body.append("            write_mem32(_out + 8, f32_to_bits(_u.Y.Scale))")
    handler_body.append("            write_mem32(_out + 12, f32_to_bits(_u.Y.Offset))")
    handler_body.append("        end")


def _emit_struct_write_udim2(handler_body):
    """Syscall 61: Store *reg[11] as UDim2 in OBJECTS, return handle."""
    handler_body.append("        local _src = reg[11]")
    handler_body.append("        local _xs = bits_to_f32(read_mem32(_src + 0))")
    handler_body.append("        local _xo = bits_to_f32(read_mem32(_src + 4))")
    handler_body.append("        local _ys = bits_to_f32(read_mem32(_src + 8))")
    handler_body.append("        local _yo = bits_to_f32(read_mem32(_src + 12))")
    handler_body.append("        OBJECTS[S.NEXT_HANDLE] = UDim2.new(_xs, _xo, _ys, _yo)")
    handler_body.append("        reg[11] = S.NEXT_HANDLE")
    handler_body.append("        S.NEXT_HANDLE = S.NEXT_HANDLE + 1")


def _emit_runtime_callmethod(handler_body):
    """Runtime-dispatched callMethod (inside callMethod function).
    
    Register layout:
      a0 (reg[11]) = handle
      a1 (reg[12]) = methodName ptr  
      a2 (reg[13]) = arg1
      a3 (reg[14]) = flags
      a4 (reg[15]) = arg2
      a5 (reg[16]) = arg3
      a6 (reg[17]) = arg4
    """
    handler_body.append("        local _objHandle = reg[11]")
    handler_body.append("        local _methodName = RODATA[reg[12]] or '?'")
    handler_body.append("        local _arg1Val = reg[13]")
    handler_body.append("        local _flags = reg[14]")
    handler_body.append("        local _hasReturn = bit32.band(_flags, 1) ~= 0")
    handler_body.append("        local _returnIsBuffer = bit32.band(_flags, 32) ~= 0")
    handler_body.append("        local _arg1IsFunction = bit32.band(_flags, 8192) ~= 0")
    handler_body.append("        local _arg1IsBuffer = bit32.band(_flags, 512) ~= 0")
    handler_body.append("        local _arg1IsString = bit32.band(_flags, 8) ~= 0")
    handler_body.append("        local _arg1IsObject = bit32.band(_flags, 131072) ~= 0")
    handler_body.append("        local _arg2IsFunction = bit32.band(_flags, 16384) ~= 0")
    handler_body.append("        local _arg2IsBuffer = bit32.band(_flags, 1024) ~= 0")
    handler_body.append("        local _arg2IsString = bit32.band(_flags, 16) ~= 0")
    handler_body.append("        local _arg2IsObject = bit32.band(_flags, 262144) ~= 0")
    handler_body.append("        local _arg3IsFunction = bit32.band(_flags, 32768) ~= 0")
    handler_body.append("        local _arg3IsBuffer = bit32.band(_flags, 2048) ~= 0")
    handler_body.append("        local _arg3IsString = bit32.band(_flags, 64) ~= 0")
    handler_body.append("        local _arg3IsObject = bit32.band(_flags, 524288) ~= 0")
    handler_body.append("        local _arg4IsFunction = bit32.band(_flags, 65536) ~= 0")
    handler_body.append("        local _arg4IsBuffer = bit32.band(_flags, 4096) ~= 0")
    handler_body.append("        local _arg4IsString = bit32.band(_flags, 128) ~= 0")
    handler_body.append("        local _arg4IsObject = bit32.band(_flags, 1048576) ~= 0")
    handler_body.append("        local _isStatic = bit32.band(_flags, 256) ~= 0")
    handler_body.append("        local _obj = OBJECTS[_objHandle]")
    handler_body.append("        if _obj and _methodName then")
    handler_body.append("            -- Always push all 4 args unconditionally (safe fallback; Luau")
    handler_body.append("            -- silently ignores extras. The templated dispatch handles counts precisely.)")
    handler_body.append("            local _args = {}")
    handler_body.append("            if not _isStatic then _args[1] = _obj end")
    handler_body.append("            -- arg1 in a2 (reg[13])")
    handler_body.append("            if _arg1IsFunction then _args[#_args + 1] = S.get_function(_arg1Val)")
    handler_body.append("            elseif _arg1IsBuffer then _args[#_args + 1] = BUFFERS[_arg1Val]")
    handler_body.append("            elseif _arg1IsObject then _args[#_args + 1] = OBJECTS[_arg1Val]")
    handler_body.append("            elseif _arg1IsString then local _s = RODATA[_arg1Val] or ''; _args[#_args + 1] = _s")
    handler_body.append("            else _args[#_args + 1] = _arg1Val end")
    handler_body.append("            -- arg2 in a4 (reg[15])")
    handler_body.append("            if _arg2IsFunction then _args[#_args + 1] = S.get_function(reg[15])")
    handler_body.append("            elseif _arg2IsBuffer then _args[#_args + 1] = BUFFERS[reg[15]]")
    handler_body.append("            elseif _arg2IsObject then _args[#_args + 1] = OBJECTS[reg[15]]")
    handler_body.append("            elseif _arg2IsString then local _s = RODATA[reg[15]] or ''; _args[#_args + 1] = _s")
    handler_body.append("            else _args[#_args + 1] = reg[15] end")
    handler_body.append("            -- arg3 in a5 (reg[16])")
    handler_body.append("            if _arg3IsFunction then _args[#_args + 1] = S.get_function(reg[16])")
    handler_body.append("            elseif _arg3IsBuffer then _args[#_args + 1] = BUFFERS[reg[16]]")
    handler_body.append("            elseif _arg3IsObject then _args[#_args + 1] = OBJECTS[reg[16]]")
    handler_body.append("            elseif _arg3IsString then local _s = RODATA[reg[16]] or ''; _args[#_args + 1] = _s")
    handler_body.append("            else _args[#_args + 1] = reg[16] end")
    handler_body.append("            -- arg4 in a6 (reg[17])")
    handler_body.append("            if _arg4IsFunction then _args[#_args + 1] = S.get_function(reg[17])")
    handler_body.append("            elseif _arg4IsBuffer then _args[#_args + 1] = BUFFERS[reg[17]]")
    handler_body.append("            elseif _arg4IsObject then _args[#_args + 1] = OBJECTS[reg[17]]")
    handler_body.append("            elseif _arg4IsString then local _s = RODATA[reg[17]] or ''; _args[#_args + 1] = _s")
    handler_body.append("            else _args[#_args + 1] = reg[17] end")
    handler_body.append("            if _hasReturn then")
    handler_body.append("                local _r = _obj[_methodName](table.unpack(_args))")
    handler_body.append("                if _returnIsBuffer then")
    handler_body.append("                    BUFFERS[S.NEXT_HANDLE] = _r")
    handler_body.append("                    reg[11] = S.NEXT_HANDLE")
    handler_body.append("                    S.NEXT_HANDLE = S.NEXT_HANDLE + 1")
    handler_body.append("                elseif bit32.band(_flags, 2) ~= 0 then")
    handler_body.append("                    if _r then")
    handler_body.append("                        OBJECTS[S.NEXT_HANDLE] = _r")
    handler_body.append("                        reg[11] = S.NEXT_HANDLE")
    handler_body.append("                        S.NEXT_HANDLE = S.NEXT_HANDLE + 1")
    handler_body.append("                    else")
    handler_body.append("                        reg[11] = 0")
    handler_body.append("                    end")
    handler_body.append("                else")
    handler_body.append("                    reg[11] = _r or 0")
    handler_body.append("                end")
    handler_body.append("            else")
    handler_body.append("                _obj[_methodName](table.unpack(_args))")
    handler_body.append("            end")
    handler_body.append("        end")
