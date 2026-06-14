"""ecall instruction handler — dispatches to helper functions by syscall/function."""

from ._helpers import (
    _emit_new_part, _emit_find_child, _emit_getprop,
    _emit_getprop_vec3, _emit_setprop_vec3,
    _emit_getprop_color3, _emit_setprop_color3,
    _emit_getprop_cframe, _emit_setprop_cframe,
    _emit_malloc, _emit_generic_callmethod,
    _emit_callmethod_return, _emit_runtime_callmethod,
)


def _handle_ecall(handler_body, current_func, addr_int,
                  tracked_a7_syscall, tracked_a0_literal,
                  tracked_a1_rodata_str, tracked_a2_rodata_str,
                  tracked_a3_literal, tracked_a3_rodata_str,
                  tracked_a4_rodata_str, tracked_a5_literal,
                  tracked_a5_rodata_str, tracked_a2_literal):
    """Generate ecall handler body based on function context and syscall number."""

    is_print_str = current_func and "printEPKc" in current_func
    is_print_int = current_func and "printEi" in current_func
    is_print_bool = current_func and "printEb" in current_func
    is_print_float = current_func and "printEf" in current_func
    is_create_part = current_func and "createPart" in current_func
    is_find_first_child = current_func and "findFirstChild" in current_func
    is_wait_for_child = current_func and "waitForChild" in current_func
    is_destroy = current_func and "destroy" in current_func
    is_clone = current_func and "clone" in current_func
    is_getprop_float = current_func and "getPropertyIfEE" in current_func
    is_setprop_float = current_func and "setPropertyIfEE" in current_func
    is_getprop_vec3 = current_func and "getPropertyVector3" in current_func
    is_setprop_vec3 = current_func and "setPropertyVector3" in current_func
    is_setprop_string = current_func and "setPropertyString" in current_func
    is_setprop_bool = current_func and "setPropertyBool" in current_func
    is_getprop_color3 = current_func and "getPropertyColor3" in current_func
    is_setprop_color3 = current_func and "setPropertyColor3" in current_func
    is_create_buffer = current_func and "createBuffer" in current_func
    is_free_buffer = current_func and "freeBuffer" in current_func
    is_buffer_len = current_func and "bufferLen" in current_func
    is_buffer_read_i8 = current_func and "bufferReadI8" in current_func
    is_buffer_write_i8 = current_func and "bufferWriteI8" in current_func
    is_buffer_read_i32 = current_func and "bufferReadI32" in current_func
    is_buffer_write_i32 = current_func and "bufferWriteI32" in current_func
    is_buffer_read_f32 = current_func and "bufferReadF32" in current_func
    is_buffer_write_f32 = current_func and "bufferWriteF32" in current_func
    is_buffer_from_string = current_func and "bufferFromString" in current_func
    is_malloc = current_func and "malloc" in current_func
    is_free = current_func and "free" in current_func
    is_heap_used = current_func and "heapUsed" in current_func
    is_create_instance = current_func and "createInstance" in current_func
    is_get_workspace = current_func and "getWorkspace" in current_func
    is_get_players = current_func and "getPlayers" in current_func
    is_get_local_player = current_func and "getLocalPlayer" in current_func
    is_getprop_cframe = current_func and "getPropertyCFrame" in current_func
    is_setprop_cframe = current_func and "setPropertyCFrame" in current_func
    is_task_wait = current_func and "taskWait" in current_func
    is_task_spawn = current_func and "taskSpawn" in current_func
    is_task_defer = current_func and "taskDefer" in current_func
    is_call_method = current_func and "callMethod" in current_func
    is_get_method = current_func and "getMethod" in current_func

    ecall_is_halt = False

    # Print variants
    if is_print_str:
        handler_body.append("        print(RODATA[reg[11]] or '[string@' .. string.format('0x%x', reg[11]) .. ']')")
    elif is_print_int:
        handler_body.append("        print(reg[11])")
    elif is_print_bool:
        handler_body.append("        print(reg[11] ~= 0)")
    elif is_print_float:
        handler_body.append("        print(bits_to_f32(read_mem32(reg[11])))")

    # Object operations
    elif is_create_part or tracked_a7_syscall == 8:
        _emit_new_part(handler_body)
    elif is_create_instance or tracked_a7_syscall == 38:
        handler_body.append("        local _typeName = RODATA[reg[11]] or 'Part'")
        handler_body.append("        local _obj = Instance.new(_typeName)")
        handler_body.append("        _obj.Parent = workspace")
        handler_body.append("        OBJECTS[S.NEXT_HANDLE] = _obj")
        handler_body.append("        reg[11] = S.NEXT_HANDLE")
        handler_body.append("        S.NEXT_HANDLE = S.NEXT_HANDLE + 1")
    elif is_destroy or tracked_a7_syscall == 15:
        handler_body.append("        local _obj = OBJECTS[reg[11]]")
        handler_body.append("        if _obj then")
        handler_body.append("            _obj:Destroy()")
        handler_body.append("            OBJECTS[reg[11]] = nil")
        handler_body.append("        end")
    elif is_clone or tracked_a7_syscall == 16:
        handler_body.append("        local _obj = OBJECTS[reg[11]]")
        handler_body.append("        if _obj then")
        handler_body.append("            local _cloned = _obj:Clone()")
        handler_body.append("            OBJECTS[S.NEXT_HANDLE] = _cloned")
        handler_body.append("            reg[11] = S.NEXT_HANDLE")
        handler_body.append("            S.NEXT_HANDLE = S.NEXT_HANDLE + 1")
        handler_body.append("        else")
        handler_body.append("            reg[11] = 0")
        handler_body.append("        end")
    elif is_find_first_child or tracked_a7_syscall == 13:
        _emit_find_child(handler_body, "FindFirstChild")
    elif is_wait_for_child or tracked_a7_syscall == 14:
        _emit_find_child(handler_body, "WaitForChild")

    # Property get/set
    elif is_getprop_float or tracked_a7_syscall == 9:
        _emit_getprop(handler_body, "f32_to_bits(_obj[_propName])")
    elif is_setprop_float or tracked_a7_syscall == 10:
        handler_body.append("        local _obj = OBJECTS[reg[11]]")
        handler_body.append("        local _propName = RODATA[reg[12]] or '?'")
        handler_body.append("        if _obj then")
        handler_body.append("            _obj[_propName] = bits_to_f32(reg[13])")
        handler_body.append("        end")
    elif is_getprop_vec3 or tracked_a7_syscall == 11:
        _emit_getprop_vec3(handler_body)
    elif is_setprop_vec3 or tracked_a7_syscall == 12:
        _emit_setprop_vec3(handler_body)
    elif is_getprop_color3 or tracked_a7_syscall == 19:
        _emit_getprop_color3(handler_body)
    elif is_setprop_color3 or tracked_a7_syscall == 20:
        _emit_setprop_color3(handler_body)
    elif is_setprop_string or tracked_a7_syscall == 17:
        handler_body.append("        local _obj = OBJECTS[reg[11]]")
        handler_body.append("        local _propName = RODATA[reg[12]] or '?'")
        handler_body.append("        local _strVal = RODATA[reg[13]] or ''")
        handler_body.append("        if _obj then")
        handler_body.append("            _obj[_propName] = _strVal")
        handler_body.append("        end")
    elif is_setprop_bool or tracked_a7_syscall == 18:
        handler_body.append("        local _obj = OBJECTS[reg[11]]")
        handler_body.append("        local _propName = RODATA[reg[12]] or '?'")
        handler_body.append("        if _obj then")
        handler_body.append("            _obj[_propName] = (reg[13] ~= 0)")
        handler_body.append("        end")

    # CFrame
    elif is_getprop_cframe or tracked_a7_syscall == 34:
        _emit_getprop_cframe(handler_body)
    elif is_setprop_cframe or tracked_a7_syscall == 35:
        _emit_setprop_cframe(handler_body)

    # Buffer operations
    elif is_create_buffer or tracked_a7_syscall == 21:
        handler_body.append("        local _buf = buffer.create(reg[11])")
        handler_body.append("        BUFFERS[S.NEXT_HANDLE] = _buf")
        handler_body.append("        reg[11] = S.NEXT_HANDLE")
        handler_body.append("        S.NEXT_HANDLE = S.NEXT_HANDLE + 1")
    elif is_free_buffer or tracked_a7_syscall == 22:
        handler_body.append("        BUFFERS[reg[11]] = nil")
    elif is_buffer_len or tracked_a7_syscall == 23:
        handler_body.append("        local _buf = BUFFERS[reg[11]]")
        handler_body.append("        reg[11] = _buf and buffer.len(_buf) or 0")
    elif is_buffer_read_i8 or tracked_a7_syscall == 24:
        handler_body.append("        local _buf = BUFFERS[reg[11]]")
        handler_body.append("        reg[11] = _buf and buffer.readi8(_buf, reg[12]) or 0")
    elif is_buffer_write_i8 or tracked_a7_syscall == 25:
        handler_body.append("        local _buf = BUFFERS[reg[11]]")
        handler_body.append("        if _buf then buffer.writei8(_buf, reg[12], reg[13]) end")
    elif is_buffer_read_i32 or tracked_a7_syscall == 26:
        handler_body.append("        local _buf = BUFFERS[reg[11]]")
        handler_body.append("        reg[11] = _buf and buffer.readi32(_buf, reg[12]) or 0")
    elif is_buffer_write_i32 or tracked_a7_syscall == 27:
        handler_body.append("        local _buf = BUFFERS[reg[11]]")
        handler_body.append("        if _buf then buffer.writei32(_buf, reg[12], reg[13]) end")
    elif is_buffer_read_f32 or tracked_a7_syscall == 28:
        handler_body.append("        local _buf = BUFFERS[reg[11]]")
        handler_body.append("        reg[11] = _buf and f32_to_bits(buffer.readf32(_buf, reg[12])) or 0")
    elif is_buffer_write_f32 or tracked_a7_syscall == 29:
        handler_body.append("        local _buf = BUFFERS[reg[11]]")
        handler_body.append("        if _buf then buffer.writef32(_buf, reg[12], bits_to_f32(reg[13])) end")
    elif is_buffer_from_string or tracked_a7_syscall == 50:
        handler_body.append("        local _strVal = RODATA[reg[11]] or ''")
        handler_body.append("        local _buf = buffer.fromstring(_strVal)")
        handler_body.append("        BUFFERS[S.NEXT_HANDLE] = _buf")
        handler_body.append("        reg[11] = S.NEXT_HANDLE")
        handler_body.append("        S.NEXT_HANDLE = S.NEXT_HANDLE + 1")

    # Memory operations
    elif is_malloc or tracked_a7_syscall == 30:
        _emit_malloc(handler_body)
    elif is_free or tracked_a7_syscall == 31:
        handler_body.append("        local _ptr = reg[11]")
        handler_body.append("        if _ptr ~= 0 and ALLOCS[_ptr] then")
        handler_body.append("            local _size = ALLOCS[_ptr]")
        handler_body.append("            ALLOCS[_ptr] = nil")
        handler_body.append("            FREE_LIST[_ptr] = _size")
        handler_body.append("        end")
    elif is_heap_used or tracked_a7_syscall == 32:
        handler_body.append("        reg[11] = S.HEAP_BRK - 0x81000000")

    # Service lookups
    elif is_get_workspace or tracked_a7_syscall == 33:
        handler_body.append("        if not S.WORKSPACE_HANDLE then")
        handler_body.append("            OBJECTS[S.NEXT_HANDLE] = workspace")
        handler_body.append("            S.WORKSPACE_HANDLE = S.NEXT_HANDLE")
        handler_body.append("            S.NEXT_HANDLE = S.NEXT_HANDLE + 1")
        handler_body.append("        end")
        handler_body.append("        reg[11] = S.WORKSPACE_HANDLE")
    elif is_get_players or tracked_a7_syscall == 36:
        handler_body.append("        if not S.PLAYERS_HANDLE then")
        handler_body.append('            local _players = game:GetService("Players")')
        handler_body.append("            OBJECTS[S.NEXT_HANDLE] = _players")
        handler_body.append("            S.PLAYERS_HANDLE = S.NEXT_HANDLE")
        handler_body.append("            S.NEXT_HANDLE = S.NEXT_HANDLE + 1")
        handler_body.append("        end")
        handler_body.append("        reg[11] = S.PLAYERS_HANDLE")
    elif is_get_local_player or tracked_a7_syscall == 37:
        handler_body.append("        local _players = OBJECTS[reg[11]]")
        handler_body.append("        if _players and not S.LOCAL_PLAYER_HANDLE then")
        handler_body.append("            local _player = _players.LocalPlayer")
        handler_body.append("            if _player then")
        handler_body.append("                OBJECTS[S.NEXT_HANDLE] = _player")
        handler_body.append("                S.LOCAL_PLAYER_HANDLE = S.NEXT_HANDLE")
        handler_body.append("                S.NEXT_HANDLE = S.NEXT_HANDLE + 1")
        handler_body.append("            end")
        handler_body.append("        end")
        handler_body.append("        reg[11] = S.LOCAL_PLAYER_HANDLE or 0")

    # Math operations
    elif tracked_a7_syscall == 39:
        handler_body.append("        local _ptr = reg[11]")
        handler_body.append("        local _val = bits_to_f32(read_mem32(_ptr))")
        handler_body.append("        write_mem32(_ptr, f32_to_bits(math.rad(_val)))")
    elif tracked_a7_syscall == 40:
        handler_body.append("        local _ptr = reg[11]")
        handler_body.append("        local _val = bits_to_f32(read_mem32(_ptr))")
        handler_body.append("        write_mem32(_ptr, f32_to_bits(math.sin(_val)))")
    elif tracked_a7_syscall == 41:
        handler_body.append("        local _ptr = reg[11]")
        handler_body.append("        local _val = bits_to_f32(read_mem32(_ptr))")
        handler_body.append("        write_mem32(_ptr, f32_to_bits(math.cos(_val)))")

    # Enum operations
    elif tracked_a7_syscall == 42:
        handler_body.append("        local _obj = OBJECTS[reg[11]]")
        handler_body.append("        local _propName = RODATA[reg[12]] or '?'")
        handler_body.append("        if _obj and _obj[_propName] ~= nil then")
        handler_body.append("            reg[11] = ENUM_TO_INDEX[_obj[_propName]] or 0")
        handler_body.append("        else")
        handler_body.append("            reg[11] = 0")
        handler_body.append("        end")
    elif tracked_a7_syscall == 43:
        handler_body.append("        local _obj = OBJECTS[reg[11]]")
        handler_body.append("        local _propName = RODATA[reg[12]] or '?'")
        handler_body.append("        local _enumItem = ENUMS[reg[13] + 1]")
        handler_body.append("        if _obj and _enumItem then")
        handler_body.append("            _obj[_propName] = _enumItem")
        handler_body.append("        end")
    elif tracked_a7_syscall == 44:
        handler_body.append("        local _obj = OBJECTS[reg[11]]")
        handler_body.append("        local _propName = RODATA[reg[12]] or '?'")
        handler_body.append("        local _targetObj = OBJECTS[reg[13]]")
        handler_body.append("        if _obj and _targetObj then")
        handler_body.append("            _obj[_propName] = _targetObj")
        handler_body.append("        end")

    # Task
    elif is_task_wait or tracked_a7_syscall == 45:
        handler_body.append("        local _duration = bits_to_f32(reg[11])")
        handler_body.append("")
        handler_body.append("        -- Save S.reg/S.freg so other threads don't corrupt us during yield")
        handler_body.append("        local _yr = table.create(32, 0)")
        handler_body.append("        local _yf = table.create(32, 0)")
        handler_body.append("        for _i = 1, 32 do _yr[_i] = S.reg[_i]; _yf[_i] = S.freg[_i] end")
        handler_body.append("")
        handler_body.append("        local _elapsed = task.wait(_duration)")
        handler_body.append("")
        handler_body.append("        -- Restore S.reg/S.freg (other threads may have run)")
        handler_body.append("        for _i = 1, 32 do S.reg[_i] = _yr[_i]; S.freg[_i] = _yf[_i] end")
        handler_body.append("")
        handler_body.append("        reg[11] = f32_to_bits(_elapsed)")

    # Thread spawn (syscall 48: taskSpawn)
    elif is_task_spawn or tracked_a7_syscall == 48:
        handler_body.append("        -- taskSpawn: spawn a new thread at the function address in a0")
        handler_body.append("        -- Arguments (0-6) are in a1-a6; they get shifted so the spawned")
        handler_body.append("        -- function sees its first argument in a0 (standard ABI).")
        handler_body.append("        -- Floating-point args pass through fa0-7 untouched (no shift needed).")
        handler_body.append("        local _fnAddr = reg[11]  -- a0 = function address to spawn")
        handler_body.append("        if _fnAddr ~= 0 then")
        handler_body.append("            -- Create per-thread integer register table (copy parent state)")
        handler_body.append("            local _threadReg = table.create(32, 0)")
        handler_body.append("            for _i = 1, 32 do _threadReg[_i] = S.reg[_i] end")
        handler_body.append("")
        handler_body.append("            -- Shift integer arguments: a1->a0, a2->a1, ..., a7->a6, a7=0")
        handler_body.append("            -- reg[11]=a0, reg[12]=a1, ..., reg[17]=a6, reg[18]=a7")
        handler_body.append("            for _i = 11, 16 do")
        handler_body.append("                _threadReg[_i] = _threadReg[_i + 1]")
        handler_body.append("            end")
        handler_body.append("            _threadReg[17] = 0  -- clear a6 (old arg6 slot; a7 had syscall number 48)")
        handler_body.append("")
        handler_body.append("            -- Zero return address (ra = reg[2]) so the thread halts on exit")
        handler_body.append("            _threadReg[2] = 0")
        handler_body.append("")
        handler_body.append("            -- Allocate 64K stack from heap for this thread")
        handler_body.append("            _threadReg[3] = S.HEAP_BRK + 65536")
        handler_body.append("            S.HEAP_BRK = S.HEAP_BRK + 65536")
        handler_body.append("")
        handler_body.append("            -- Track the thread")
        handler_body.append("            local _tid = S.NEXT_THREAD_ID")
        handler_body.append("            S.NEXT_THREAD_ID = S.NEXT_THREAD_ID + 1")
        handler_body.append("            S.THREADS[_tid] = { reg = _threadReg, pc = _fnAddr }")
        handler_body.append("")
        handler_body.append("            -- Save parent registers and float regs before spawn")
        handler_body.append("            local _parentReg = table.create(32, 0)")
        handler_body.append("            local _parentFreg = table.create(32, 0)")
        handler_body.append("            for _i = 1, 32 do")
        handler_body.append("                _parentReg[_i] = S.reg[_i]")
        handler_body.append("                _parentFreg[_i] = S.freg[_i]")
        handler_body.append("            end")
        handler_body.append("")
        handler_body.append("            -- Spawn the thread via task.spawn")
        handler_body.append("            task.spawn(function()")
        handler_body.append("                S.dispatch_thread(_threadReg, _fnAddr)")
        handler_body.append("                S.THREADS[_tid] = nil  -- thread finished")
        handler_body.append("            end)")
        handler_body.append("")
        handler_body.append("            -- Restore parent registers and float regs (task.spawn does not yield)")
        handler_body.append("            for _i = 1, 32 do")
        handler_body.append("                S.reg[_i] = _parentReg[_i]")
        handler_body.append("                S.freg[_i] = _parentFreg[_i]")
        handler_body.append("            end")
        handler_body.append("")
        handler_body.append("            -- Return thread ID to parent (C++ expects handle in a0)")
        handler_body.append("            reg[11] = _tid")
        handler_body.append("        end")

    # Thread defer (syscall 49: taskDefer)
    elif is_task_defer or tracked_a7_syscall == 49:
        handler_body.append("        -- taskDefer: defer a function to the next heartbeat")
        handler_body.append("        -- Arguments (0-6) are in a1-a6; shifted so the deferred function")
        handler_body.append("        -- sees its first argument in a0 (standard ABI).")
        handler_body.append("        local _fnAddr = reg[11]  -- a0 = function address to defer")
        handler_body.append("        if _fnAddr ~= 0 then")
        handler_body.append("            -- Create per-thread integer register table (copy parent state)")
        handler_body.append("            local _threadReg = table.create(32, 0)")
        handler_body.append("            for _i = 1, 32 do _threadReg[_i] = S.reg[_i] end")
        handler_body.append("")
        handler_body.append("            -- Shift integer arguments: a1->a0, a2->a1, ..., a7->a6, a7=0")
        handler_body.append("            for _i = 11, 16 do")
        handler_body.append("                _threadReg[_i] = _threadReg[_i + 1]")
        handler_body.append("            end")
        handler_body.append("            _threadReg[17] = 0  -- clear a6 (old arg6 slot; a7 had syscall number 49)")
        handler_body.append("")
        handler_body.append("            -- Zero return address (ra = reg[2]) so the thread halts on exit")
        handler_body.append("            _threadReg[2] = 0")
        handler_body.append("")
        handler_body.append("            -- Allocate 64K stack from heap")
        handler_body.append("            _threadReg[3] = S.HEAP_BRK + 65536")
        handler_body.append("            S.HEAP_BRK = S.HEAP_BRK + 65536")
        handler_body.append("")
        handler_body.append("            -- Save parent registers and float regs")
        handler_body.append("            local _parentReg = table.create(32, 0)")
        handler_body.append("            local _parentFreg = table.create(32, 0)")
        handler_body.append("            for _i = 1, 32 do")
        handler_body.append("                _parentReg[_i] = S.reg[_i]")
        handler_body.append("                _parentFreg[_i] = S.freg[_i]")
        handler_body.append("            end")
        handler_body.append("")
        handler_body.append("            -- Defer via task.defer")
        handler_body.append("            task.defer(function()")
        handler_body.append("                S.dispatch_thread(_threadReg, _fnAddr)")
        handler_body.append("            end)")
        handler_body.append("")
        handler_body.append("            -- Restore parent registers and float regs")
        handler_body.append("            for _i = 1, 32 do")
        handler_body.append("                S.reg[_i] = _parentReg[_i]")
        handler_body.append("                S.freg[_i] = _parentFreg[_i]")
        handler_body.append("            end")
        handler_body.append("        end")

    # getMethod (syscall 51): returns an RBXScriptSignal as an object handle
    elif is_get_method or tracked_a7_syscall == 51:
        handler_body.append("        local _obj = OBJECTS[reg[11]]")
        handler_body.append("        local _propName = RODATA[reg[12]] or '?'")
        handler_body.append("        if _obj then")
        handler_body.append("            local _signal = _obj[_propName]")
        handler_body.append("            if _signal then")
        handler_body.append("                OBJECTS[S.NEXT_HANDLE] = _signal")
        handler_body.append("                reg[11] = S.NEXT_HANDLE")
        handler_body.append("                S.NEXT_HANDLE = S.NEXT_HANDLE + 1")
        handler_body.append("            else")
        handler_body.append("                reg[11] = 0")
        handler_body.append("            end")
        handler_body.append("        else")
        handler_body.append("            reg[11] = 0")
        handler_body.append("        end")

    # Runtime-dispatched callMethod (must be checked before syscall 46 —
    # the callMethod function may have a7=46, and the runtime dispatcher
    # is the correct handler for method dispatch inside that function.)
    elif is_call_method:
        _emit_runtime_callmethod(handler_body)

    # Generic callMethod (templated dispatch)
    elif tracked_a7_syscall == 46:
        _emit_generic_callmethod(handler_body, tracked_a3_literal,
                                 tracked_a1_rodata_str, tracked_a2_rodata_str,
                                 tracked_a4_rodata_str, tracked_a5_rodata_str,
                                 tracked_a5_literal, tracked_a2_literal)

    # Syscall 47: getService
    elif tracked_a7_syscall == 47:
        handler_body.append("        local _svcName = RODATA[reg[11]] or '?'")
        handler_body.append("        if not S.SERVICE_HANDLES then S.SERVICE_HANDLES = {} end")
        handler_body.append("        local _cached = S.SERVICE_HANDLES[_svcName]")
        handler_body.append("        if _cached then")
        handler_body.append("            reg[11] = _cached")
        handler_body.append("        else")
        handler_body.append("            local _svc = game:GetService(_svcName)")
        handler_body.append("            OBJECTS[S.NEXT_HANDLE] = _svc")
        handler_body.append("            S.SERVICE_HANDLES[_svcName] = S.NEXT_HANDLE")
        handler_body.append("            reg[11] = S.NEXT_HANDLE")
        handler_body.append("            S.NEXT_HANDLE = S.NEXT_HANDLE + 1")
        handler_body.append("        end")

    # Generic print (syscalls 4-7)
    elif tracked_a7_syscall == 4:
        handler_body.append(f"        print({tracked_a0_literal})")
    elif tracked_a7_syscall == 5:
        handler_body.append(f"        print({tracked_a0_literal})")
    elif tracked_a7_syscall == 6:
        bool_str = "true" if tracked_a0_literal == "1" else "false"
        handler_body.append(f"        print({bool_str})")
    elif tracked_a7_syscall == 7:
        handler_body.append(f"        print({tracked_a0_literal})")

    else:
        handler_body.append("        print('System Halt: ecall (a7=' .. reg[18] .. ')')")
        handler_body.append("        return nil")
        ecall_is_halt = True

    if not ecall_is_halt:
        handler_body.append(f"        return {addr_int + 4}")
