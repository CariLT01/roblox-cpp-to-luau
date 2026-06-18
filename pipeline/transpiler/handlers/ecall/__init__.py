"""ecall instruction handler — dispatches to helper functions by syscall/function."""

import re

from ._helpers import (
    _emit_malloc,
    _emit_generic_callmethod,
    _emit_callmethod_return,
    _emit_runtime_callmethod,
)
from .conversions import (
    emit_object_read, emit_object_write,
)


def _handle_ecall(handler_body, current_func, addr_int,
                  tracked_a7_syscall, tracked_a0_literal,
                  tracked_a1_rodata_str, tracked_a2_rodata_str,
                  tracked_a3_literal, tracked_a3_rodata_str,
                  tracked_a4_rodata_str, tracked_a5_literal,
                  tracked_a5_rodata_str, tracked_a2_literal,
                  rodata_addr_table=None,
                  validate=False):
    """Generate ecall handler body based on function context and syscall number."""

    is_malloc = current_func and "malloc" in current_func
    is_free = current_func and "free" in current_func
    is_heap_used = current_func and "heapUsed" in current_func

    is_get_global = current_func and "getGlobal" in current_func
    is_task_spawn = current_func and "taskSpawn" in current_func
    is_task_defer = current_func and "taskDefer" in current_func
    is_call_method = current_func and "callMethod" in current_func
    is_require = current_func and "require" in current_func

    # All type conversions handled by unified objectRead/objectWrite (syscalls 78-79)
    # Type IDs: 0=Vector3, 1=CFrame, 2=Color3, 3=UDim2, 4=float, 5=int, 6=bool, 7=string, 8=function

    ecall_is_halt = False

    # Unified object conversion (syscalls 78-79)
    if tracked_a7_syscall == 78:
        emit_object_read(handler_body)
    elif tracked_a7_syscall == 79:
        emit_object_write(handler_body)

    # Memory operations
    elif is_malloc or tracked_a7_syscall == 30:
        _emit_malloc(handler_body)
    elif is_free or tracked_a7_syscall == 31:
        handler_body.append("        local _ptr = reg[11]")
        if validate:
            handler_body.append("        if _ptr == 0 then")
            handler_body.append("            error('[VM Validation] Attempt to free null pointer')")
            handler_body.append("        elseif not ALLOCS[_ptr] then")
            handler_body.append("            error('[VM Validation] Double-free or free of unallocated pointer 0x' .. string.format('%x', _ptr))")
            handler_body.append("        end")
        handler_body.append("        if _ptr ~= 0 and ALLOCS[_ptr] then")
        handler_body.append("            local _size = ALLOCS[_ptr]")
        handler_body.append("            ALLOCS[_ptr] = nil")
        handler_body.append("            FREE_LIST[_ptr] = _size")
        handler_body.append("        end")
    elif is_heap_used or tracked_a7_syscall == 32:
        handler_body.append("        reg[11] = S.HEAP_BRK - 0x81000000")

    # Enum ↔ OBJECTS bridge (syscalls 42/43)
    # Syscall 42: fromEnum(enumIndex) — converts C++ enum index → OBJECTS handle
    elif tracked_a7_syscall == 42:
        handler_body.append("        local _enumItem = ENUMS[reg[11] + 1]")
        handler_body.append("        if _enumItem then")
        handler_body.append("            OBJECTS[S.NEXT_HANDLE] = _enumItem")
        handler_body.append("            reg[11] = S.NEXT_HANDLE")
        handler_body.append("            S.NEXT_HANDLE = S.NEXT_HANDLE + 1")
        handler_body.append("        else")
        handler_body.append("            warn('[VM] fromEnum: ENUMS[' .. (reg[11] + 1) .. '] is nil (ENUMS table may be empty)')")
        handler_body.append("            reg[11] = 0")
        handler_body.append("        end")
    # Syscall 43: toEnum(handle) — converts OBJECTS handle → C++ enum index
    elif tracked_a7_syscall == 43:
        handler_body.append("        local _obj = OBJECTS[reg[11]]")
        handler_body.append("        if _obj then")
        handler_body.append("            reg[11] = ENUM_TO_INDEX[_obj] or 0")
        handler_body.append("        else")
        handler_body.append("            reg[11] = 0")
        handler_body.append("        end")

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
    elif tracked_a7_syscall == 51:
        handler_body.append("        local _obj = OBJECTS[reg[11]]")
        handler_body.append("        local _propName = RODATA[reg[12]] or '?'")
        handler_body.append("        if _obj then")
        handler_body.append("            local _signal = _obj[_propName]")
        handler_body.append("            if _signal then")
        handler_body.append("                OBJECTS[S.NEXT_HANDLE] = _signal")
        handler_body.append("                reg[11] = S.NEXT_HANDLE")
        handler_body.append("                S.NEXT_HANDLE = S.NEXT_HANDLE + 1")
        handler_body.append("            else")
        handler_body.append("                warn('[VM] getMethod: property \"' .. _propName .. '\" not found on object')")
        handler_body.append("                reg[11] = 0")
        handler_body.append("            end")
        handler_body.append("        else")
        handler_body.append("            warn('[VM] getMethod: OBJECTS[' .. reg[11] .. '] is nil')")
        handler_body.append("            reg[11] = 0")
        handler_body.append("        end")

    # Runtime-dispatched callMethod (must be checked before syscall 46)
    # Only triggers when the ecall IS syscall 46 — prevents catching inlined
    # ecalls from the new callMethod(getPropertyObject→callObj) architecture.
    elif is_call_method and tracked_a7_syscall == 46:
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
        handler_body.append("            if _svc then")
        handler_body.append("                OBJECTS[S.NEXT_HANDLE] = _svc")
        handler_body.append("                S.SERVICE_HANDLES[_svcName] = S.NEXT_HANDLE")
        handler_body.append("                reg[11] = S.NEXT_HANDLE")
        handler_body.append("                S.NEXT_HANDLE = S.NEXT_HANDLE + 1")
        handler_body.append("            else")
        handler_body.append("                warn('[VM] getService: service \"' .. _svcName .. '\" not found')")
        handler_body.append("                reg[11] = 0")
        handler_body.append("            end")
        handler_body.append("        end")

    # Syscall 53: require
    elif is_require or tracked_a7_syscall == 53:
        handler_body.append("        local _obj = OBJECTS[reg[11]]")
        handler_body.append("        if _obj then")
        handler_body.append("            local _result = require(_obj)")
        handler_body.append("            if _result ~= nil then")
        handler_body.append("                OBJECTS[S.NEXT_HANDLE] = _result")
        handler_body.append("                reg[11] = S.NEXT_HANDLE")
        handler_body.append("                S.NEXT_HANDLE = S.NEXT_HANDLE + 1")
        handler_body.append("            else")
        handler_body.append("                warn('[VM] require: module returned nil')")
        handler_body.append("                reg[11] = 0")
        handler_body.append("            end")
        handler_body.append("        else")
        handler_body.append("            warn('[VM] require: OBJECTS[' .. reg[11] .. '] is nil')")
        handler_body.append("            reg[11] = 0")
        handler_body.append("        end")

# Syscall 62: getPropertyObject — returns any property as an object handle
    elif tracked_a7_syscall == 62:
        handler_body.append("        local _obj = OBJECTS[reg[11]]")
        handler_body.append("        local _propName = RODATA[reg[12]] or '?'")
        handler_body.append("        if _obj and _obj[_propName] ~= nil then")
        handler_body.append("            OBJECTS[S.NEXT_HANDLE] = _obj[_propName]")
        handler_body.append("            reg[11] = S.NEXT_HANDLE")
        handler_body.append("            S.NEXT_HANDLE = S.NEXT_HANDLE + 1")
        handler_body.append("        else")
        handler_body.append("            if not _obj then warn('[VM] getPropertyObject: OBJECTS[' .. reg[11] .. '] is nil') end")
        handler_body.append("            reg[11] = 0")
        handler_body.append("        end")

    # Syscall 63: setPropertyObject — sets a property from an OBJECTS handle
    elif tracked_a7_syscall == 63:
        handler_body.append("        local _obj = OBJECTS[reg[11]]")
        handler_body.append("        local _propName = RODATA[reg[12]] or '?'")
        handler_body.append("        local _value = OBJECTS[reg[13]]")
        handler_body.append("        if _obj and _value ~= nil then")
        handler_body.append("            _obj[_propName] = _value")
        handler_body.append("        else")
        handler_body.append("            if not _obj then warn('[VM] setPropertyObject: OBJECTS[' .. reg[11] .. '] is nil') end")
        handler_body.append("            if not _value then warn('[VM] setPropertyObject: OBJECTS[' .. reg[13] .. '] (value) is nil') end")
        handler_body.append("        end")

    # Syscall 64: releaseObject — removes an entry from OBJECTS (non-destructive)
    elif tracked_a7_syscall == 64:
        handler_body.append("        OBJECTS[reg[11]] = nil")

# Syscall 75: payload-stack call — a0 points to a struct in RISC-V memory:
    #   word 0: (handleCount << 16) | (flags & 0xFFFF)
    #   word 1: fn handle (OBJECTS index, always present)
    #   word 2..N+1: argument handles (all OBJECTS indices)
    # All values are OBJECTS handles — no raw ints, no strings, no function wrappers.
    elif tracked_a7_syscall == 75:
        handler_body.append("        local _payload = reg[11]")
        handler_body.append("        local _header = read_mem32(_payload)")
        handler_body.append("        local _handleCount = bit32.rshift(_header, 16)")
        handler_body.append("        local _flags = bit32.band(_header, 0xFFFF)")
        handler_body.append("        local _fn = OBJECTS[read_mem32(_payload + 4)]")
        handler_body.append("        if not _fn then")
        handler_body.append("            warn('[VM] callObj: OBJECTS[payload.fn] is nil')")
        handler_body.append("            reg[11] = 0")
        handler_body.append("        else")
        handler_body.append("            local _args = {}")
        handler_body.append("            for _i = 0, _handleCount - 1 do")
        handler_body.append("                local _h = read_mem32(_payload + 8 + _i * 4)")
        handler_body.append("                _args[_i + 1] = OBJECTS[_h]")
        handler_body.append("            end")
        handler_body.append("            local _hasReturn = bit32.band(_flags, 1) ~= 0")
        handler_body.append("            if _hasReturn then")
        handler_body.append("                local _r = _fn(table.unpack(_args))")
        handler_body.append("                if _r then")
        handler_body.append("                    OBJECTS[S.NEXT_HANDLE] = _r")
        handler_body.append("                    reg[11] = S.NEXT_HANDLE")
        handler_body.append("                    S.NEXT_HANDLE = S.NEXT_HANDLE + 1")
        handler_body.append("                else")
        handler_body.append("                    reg[11] = 0")
        handler_body.append("                end")
        handler_body.append("            else")
        handler_body.append("                _fn(table.unpack(_args))")
        handler_body.append("            end")
        handler_body.append("        end")

    # Syscall 52: getGlobal(name) — wraps the named Lua global in OBJECTS and returns a handle
    elif is_get_global or tracked_a7_syscall == 52:
        # getGlobal is a SHARED function called from multiple call sites with
        # different arguments. Compile-time resolution (via state tracker) only
        # captures the last call site's value, so we MUST use runtime RODATA lookup.
        # The _G mirror in shared.luau (e.g. _G.task = task) ensures _G[name]
        # works even for Roblox built-in globals.
        handler_body.append("        local _globalName = RODATA[reg[11]] or '?'")
        handler_body.append("        OBJECTS[S.NEXT_HANDLE] = _G[_globalName]")
        handler_body.append("        if OBJECTS[S.NEXT_HANDLE] == nil then")
        handler_body.append("            warn('[VM] getGlobal: could not resolve global \"' .. _globalName .. '\" — add _G.' .. _globalName .. ' = ' .. _globalName .. ' to shared.luau')")
        handler_body.append("        end")
        handler_body.append("        reg[11] = S.NEXT_HANDLE")
        handler_body.append("        S.NEXT_HANDLE = S.NEXT_HANDLE + 1")


    else:
        handler_body.append("        print('System Halt: ecall (a7=' .. reg[18] .. ')')")
        handler_body.append("        return nil")
        ecall_is_halt = True

    if not ecall_is_halt:
        handler_body.append(f"        return {addr_int + 4}")
