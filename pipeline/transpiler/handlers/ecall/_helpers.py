"""Shared ecall helper functions for emitting Luau handler code."""

from ...utils import escape_lua_string
import re


def _emit_new_part(handler_body):
    handler_body.append("        local _obj = Instance.new('Part')")
    handler_body.append("        _obj.Parent = workspace")
    handler_body.append("        OBJECTS[S.NEXT_HANDLE] = _obj")
    handler_body.append("        reg[11] = S.NEXT_HANDLE")
    handler_body.append("        S.NEXT_HANDLE = S.NEXT_HANDLE + 1")


def _emit_find_child(handler_body, method_name):
    handler_body.append("        local _obj = OBJECTS[reg[11]]")
    handler_body.append("        local _childName = RODATA[reg[12]] or '?'")
    handler_body.append("        if _obj then")
    handler_body.append(f"            local _child = _obj:{method_name}(_childName)")
    handler_body.append("            if _child then")
    handler_body.append("                OBJECTS[S.NEXT_HANDLE] = _child")
    handler_body.append("                reg[11] = S.NEXT_HANDLE")
    handler_body.append("                S.NEXT_HANDLE = S.NEXT_HANDLE + 1")
    handler_body.append("            else")
    handler_body.append("                reg[11] = 0")
    handler_body.append("            end")
    handler_body.append("        else")
    handler_body.append("            reg[11] = 0")
    handler_body.append("        end")


def _emit_getprop(handler_body, value_expr):
    handler_body.append("        local _obj = OBJECTS[reg[11]]")
    handler_body.append("        local _propName = RODATA[reg[12]] or '?'")
    handler_body.append("        if _obj and _obj[_propName] ~= nil then")
    handler_body.append(f"            reg[11] = {value_expr}")
    handler_body.append("        else")
    handler_body.append("            reg[11] = 0")
    handler_body.append("        end")


def _emit_getprop_vec3(handler_body):
    handler_body.append("        local _obj = OBJECTS[reg[11]]")
    handler_body.append("        local _propName = RODATA[reg[12]] or '?'")
    handler_body.append("        local _outPtr = reg[13]")
    handler_body.append("        if _obj and _obj[_propName] ~= nil then")
    handler_body.append("            local _v = _obj[_propName]")
    handler_body.append("            write_mem32(_outPtr, f32_to_bits(_v.X))")
    handler_body.append("            write_mem32(_outPtr + 4, f32_to_bits(_v.Y))")
    handler_body.append("            write_mem32(_outPtr + 8, f32_to_bits(_v.Z))")
    handler_body.append("        end")


def _emit_setprop_vec3(handler_body):
    handler_body.append("        local _obj = OBJECTS[reg[11]]")
    handler_body.append("        local _propName = RODATA[reg[12]] or '?'")
    handler_body.append("        if _obj then")
    handler_body.append("            _obj[_propName] = Vector3.new(")
    handler_body.append("                bits_to_f32(reg[13]),")
    handler_body.append("                bits_to_f32(reg[14]),")
    handler_body.append("                bits_to_f32(reg[15])")
    handler_body.append("            )")
    handler_body.append("        end")


def _emit_getprop_color3(handler_body):
    handler_body.append("        local _obj = OBJECTS[reg[11]]")
    handler_body.append("        local _propName = RODATA[reg[12]] or '?'")
    handler_body.append("        local _outPtr = reg[13]")
    handler_body.append("        if _obj and _obj[_propName] ~= nil then")
    handler_body.append("            local _c = _obj[_propName]")
    handler_body.append("            write_mem32(_outPtr, f32_to_bits(_c.R))")
    handler_body.append("            write_mem32(_outPtr + 4, f32_to_bits(_c.G))")
    handler_body.append("            write_mem32(_outPtr + 8, f32_to_bits(_c.B))")
    handler_body.append("        end")


def _emit_setprop_color3(handler_body):
    handler_body.append("        local _obj = OBJECTS[reg[11]]")
    handler_body.append("        local _propName = RODATA[reg[12]] or '?'")
    handler_body.append("        if _obj then")
    handler_body.append("            _obj[_propName] = Color3.new(")
    handler_body.append("                bits_to_f32(reg[13]),")
    handler_body.append("                bits_to_f32(reg[14]),")
    handler_body.append("                bits_to_f32(reg[15])")
    handler_body.append("            )")
    handler_body.append("        end")


def _emit_getprop_cframe(handler_body):
    handler_body.append("        local _obj = OBJECTS[reg[11]]")
    handler_body.append("        local _propName = RODATA[reg[12]] or '?'")
    handler_body.append("        local _outPtr = reg[13]")
    handler_body.append("        if _obj and _obj[_propName] ~= nil then")
    handler_body.append("            local _cf = _obj[_propName]")
    handler_body.append("            local _x, _y, _z, _r00, _r01, _r02, _r10, _r11, _r12, _r20, _r21, _r22 = _cf:GetComponents()")
    handler_body.append("            write_mem32(_outPtr + 0, f32_to_bits(_x))")
    handler_body.append("            write_mem32(_outPtr + 4, f32_to_bits(_y))")
    handler_body.append("            write_mem32(_outPtr + 8, f32_to_bits(_z))")
    handler_body.append("            write_mem32(_outPtr + 12, f32_to_bits(_r00))")
    handler_body.append("            write_mem32(_outPtr + 16, f32_to_bits(_r01))")
    handler_body.append("            write_mem32(_outPtr + 20, f32_to_bits(_r02))")
    handler_body.append("            write_mem32(_outPtr + 24, f32_to_bits(_r10))")
    handler_body.append("            write_mem32(_outPtr + 28, f32_to_bits(_r11))")
    handler_body.append("            write_mem32(_outPtr + 32, f32_to_bits(_r12))")
    handler_body.append("            write_mem32(_outPtr + 36, f32_to_bits(_r20))")
    handler_body.append("            write_mem32(_outPtr + 40, f32_to_bits(_r21))")
    handler_body.append("            write_mem32(_outPtr + 44, f32_to_bits(_r22))")
    handler_body.append("        end")


def _emit_setprop_cframe(handler_body):
    handler_body.append("        local _obj = OBJECTS[reg[11]]")
    handler_body.append("        local _propName = RODATA[reg[12]] or '?'")
    handler_body.append("        local _srcPtr = reg[13]")
    handler_body.append("        if _obj then")
    for i in range(12):
        handler_body.append(f"            local _r{i:02d} = bits_to_f32(read_mem32(_srcPtr + {i * 4}))")
    # Fix the variable naming for CFrame constructor
    # We already have _r00 through _r44 above; build the CFrame.new call
    # Actually we need the proper names: x,y,z,r00,r01,r02,r10,r11,r12,r20,r21,r22
    del handler_body[-12:]  # Remove the generic loop lines
    handler_body.append("            local _x = bits_to_f32(read_mem32(_srcPtr + 0))")
    handler_body.append("            local _y = bits_to_f32(read_mem32(_srcPtr + 4))")
    handler_body.append("            local _z = bits_to_f32(read_mem32(_srcPtr + 8))")
    handler_body.append("            local _r00 = bits_to_f32(read_mem32(_srcPtr + 12))")
    handler_body.append("            local _r01 = bits_to_f32(read_mem32(_srcPtr + 16))")
    handler_body.append("            local _r02 = bits_to_f32(read_mem32(_srcPtr + 20))")
    handler_body.append("            local _r10 = bits_to_f32(read_mem32(_srcPtr + 24))")
    handler_body.append("            local _r11 = bits_to_f32(read_mem32(_srcPtr + 28))")
    handler_body.append("            local _r12 = bits_to_f32(read_mem32(_srcPtr + 32))")
    handler_body.append("            local _r20 = bits_to_f32(read_mem32(_srcPtr + 36))")
    handler_body.append("            local _r21 = bits_to_f32(read_mem32(_srcPtr + 40))")
    handler_body.append("            local _r22 = bits_to_f32(read_mem32(_srcPtr + 44))")
    handler_body.append("            _obj[_propName] = CFrame.new(_x, _y, _z, _r00, _r01, _r02, _r10, _r11, _r12, _r20, _r21, _r22)")
    handler_body.append("        end")


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
            elif tracked_a5_rodata_str is not None or (tracked_a5_literal and tracked_a5_literal != 'nil'):
                arg_parts.append('reg[16]')
            if arg2_is_function:
                arg_parts.append('S.get_function(reg[15])')
            elif arg2_is_buffer:
                arg_parts.append('BUFFERS[reg[15]]')
            elif arg2_is_string:
                arg_parts.append('RODATA[reg[15]] or ""')
            elif tracked_a4_rodata_str is not None:
                arg_parts.append('RODATA[reg[15]] or ""')
            if arg3_is_function:
                arg_parts.append('S.get_function(reg[17])')
            elif arg3_is_buffer:
                arg_parts.append('BUFFERS[reg[17]]')
            elif arg3_is_string:
                arg_parts.append('RODATA[reg[17]] or ""')

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
            elif tracked_a2_literal != 'nil' and tracked_a2_literal is not None:
                arg_parts.append('reg[13]')
            if arg2_is_function:
                arg_parts.append('S.get_function(reg[15])')
            elif arg2_is_buffer:
                arg_parts.append('BUFFERS[reg[15]]')
            elif arg2_is_string:
                arg_parts.append('RODATA[reg[15]] or ""')
            elif tracked_a4_rodata_str is not None:
                arg_parts.append('RODATA[reg[15]] or ""')
            if arg3_is_function:
                arg_parts.append('S.get_function(reg[16])')
            elif arg3_is_buffer:
                arg_parts.append('BUFFERS[reg[16]]')
            elif arg3_is_string:
                arg_parts.append('RODATA[reg[16]] or ""')
            if arg4_is_function:
                arg_parts.append('S.get_function(reg[17])')
            elif arg4_is_buffer:
                arg_parts.append('BUFFERS[reg[17]]')
            elif arg4_is_string:
                arg_parts.append('RODATA[reg[17]] or ""')

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
        handler_body.append("            local _arg1IsFn  = bit32.band(_flags, 8192) ~= 0")
        handler_body.append("            local _arg1IsBuf = bit32.band(_flags, 512) ~= 0")
        handler_body.append("            local _arg1IsStr = bit32.band(_flags, 8) ~= 0")
        handler_body.append("            local _arg2IsFn  = bit32.band(_flags, 16384) ~= 0")
        handler_body.append("            local _arg2IsBuf = bit32.band(_flags, 1024) ~= 0")
        handler_body.append("            local _arg2IsStr = bit32.band(_flags, 16) ~= 0")
        handler_body.append("            local _arg3IsFn  = bit32.band(_flags, 32768) ~= 0")
        handler_body.append("            local _arg3IsBuf = bit32.band(_flags, 2048) ~= 0")
        handler_body.append("            local _arg3IsStr = bit32.band(_flags, 64) ~= 0")
        handler_body.append("            local _arg4IsFn  = bit32.band(_flags, 65536) ~= 0")
        handler_body.append("            local _arg4IsBuf = bit32.band(_flags, 4096) ~= 0")
        handler_body.append("            local _arg4IsStr = bit32.band(_flags, 128) ~= 0")
        handler_body.append("            local _isStatic = bit32.band(_flags, 256) ~= 0")
        handler_body.append("            local _args = {}")
        handler_body.append("            if _arg1IsFn then _args[1] = S.get_function(reg[13]) elseif _arg1IsBuf then _args[1] = BUFFERS[reg[13]] elseif _arg1IsStr then _args[1] = RODATA[reg[13]] or '' else _args[1] = reg[13] end")
        handler_body.append("            if _arg2IsFn then _args[2] = S.get_function(reg[15]) elseif _arg2IsBuf then _args[2] = BUFFERS[reg[15]] elseif _arg2IsStr then _args[2] = RODATA[reg[15]] or '' else _args[2] = reg[15] end")
        handler_body.append("            if _arg3IsFn then _args[3] = S.get_function(reg[16]) elseif _arg3IsBuf then _args[3] = BUFFERS[reg[16]] elseif _arg3IsStr then _args[3] = RODATA[reg[16]] or '' else _args[3] = reg[16] end")
        handler_body.append("            if _arg4IsFn then _args[4] = S.get_function(reg[17]) elseif _arg4IsBuf then _args[4] = BUFFERS[reg[17]] elseif _arg4IsStr then _args[4] = RODATA[reg[17]] or '' else _args[4] = reg[17] end")
        handler_body.append("            if _isStatic then")
        handler_body.append("                _obj[_methodName](table.unpack(_args))")
        handler_body.append("            else")
        handler_body.append("                _obj[_methodName](_obj, table.unpack(_args))")
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
        handler_body.append('            reg[11] = _r')


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
    handler_body.append("        local _arg2IsFunction = bit32.band(_flags, 16384) ~= 0")
    handler_body.append("        local _arg2IsBuffer = bit32.band(_flags, 1024) ~= 0")
    handler_body.append("        local _arg2IsString = bit32.band(_flags, 16) ~= 0")
    handler_body.append("        local _arg3IsFunction = bit32.band(_flags, 32768) ~= 0")
    handler_body.append("        local _arg3IsBuffer = bit32.band(_flags, 2048) ~= 0")
    handler_body.append("        local _arg3IsString = bit32.band(_flags, 64) ~= 0")
    handler_body.append("        local _arg4IsFunction = bit32.band(_flags, 65536) ~= 0")
    handler_body.append("        local _arg4IsBuffer = bit32.band(_flags, 4096) ~= 0")
    handler_body.append("        local _arg4IsString = bit32.band(_flags, 128) ~= 0")
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
    handler_body.append("            elseif _arg1IsString then local _s = RODATA[_arg1Val] or ''; _args[#_args + 1] = _s")
    handler_body.append("            else _args[#_args + 1] = _arg1Val end")
    handler_body.append("            -- arg2 in a4 (reg[15])")
    handler_body.append("            if _arg2IsFunction then _args[#_args + 1] = S.get_function(reg[15])")
    handler_body.append("            elseif _arg2IsBuffer then _args[#_args + 1] = BUFFERS[reg[15]]")
    handler_body.append("            elseif _arg2IsString then local _s = RODATA[reg[15]] or ''; _args[#_args + 1] = _s")
    handler_body.append("            else _args[#_args + 1] = reg[15] end")
    handler_body.append("            -- arg3 in a5 (reg[16])")
    handler_body.append("            if _arg3IsFunction then _args[#_args + 1] = S.get_function(reg[16])")
    handler_body.append("            elseif _arg3IsBuffer then _args[#_args + 1] = BUFFERS[reg[16]]")
    handler_body.append("            elseif _arg3IsString then local _s = RODATA[reg[16]] or ''; _args[#_args + 1] = _s")
    handler_body.append("            else _args[#_args + 1] = reg[16] end")
    handler_body.append("            -- arg4 in a6 (reg[17])")
    handler_body.append("            if _arg4IsFunction then _args[#_args + 1] = S.get_function(reg[17])")
    handler_body.append("            elseif _arg4IsBuffer then _args[#_args + 1] = BUFFERS[reg[17]]")
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
    handler_body.append("                    reg[11] = _r")
    handler_body.append("                end")
    handler_body.append("            else")
    handler_body.append("                _obj[_methodName](table.unpack(_args))")
    handler_body.append("            end")
    handler_body.append("        end")
