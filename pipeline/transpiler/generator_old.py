"""Instruction-to-Lua generation: state tracking and handler body construction."""

import re

from .constants import TERMINATOR_OPS
from .utils import escape_lua_string, clean_reg, clean_reg_fp


def generate_handler_bodies(parsed_instructions, rodata_addr_table, rodata_table, func_map):
    """Generate instruction handler bodies with compile-time state tracking.
    
    Returns list of {'addr': int, 'is_term': bool, 'body_lines': [str]}.
    """
    # Compile-time state trackers
    tracked_a7_syscall = 0
    tracked_a0_literal = "nil"
    tracked_a1_literal = "nil"
    tracked_a2_literal = "nil"
    tracked_a3_literal = "nil"
    tracked_a4_literal = "nil"
    tracked_a5_literal = "nil"
    tracked_value_type = "nil"
    # Resolved rodata strings for callMethod templating
    tracked_a1_rodata_str = None  # resolved method name string
    tracked_a2_rodata_str = None  # resolved service name / arg1 string
    tracked_a3_rodata_str = None  # resolved arg2 / flags string
    tracked_a4_rodata_str = None  # resolved arg3 string
    tracked_a5_rodata_str = None  # resolved arg (for service path, arg1 shifted to a5)

    current_func = None
    all_inst_bodies = []

    for i, (address, mnemonic, args) in enumerate(parsed_instructions):
        addr_int = int(address, 16)

        # --- State tracking ---
        tracked_a7_syscall, tracked_a0_literal, tracked_value_type, \
            tracked_a1_literal, tracked_a1_rodata_str, \
            tracked_a2_literal, tracked_a2_rodata_str, \
            tracked_a3_literal, tracked_a3_rodata_str, \
            tracked_a4_literal, tracked_a4_rodata_str, \
            tracked_a5_literal, tracked_a5_rodata_str = _track_state(
                mnemonic, args, rodata_addr_table, rodata_table,
                tracked_a7_syscall, tracked_a0_literal, tracked_value_type,
                tracked_a1_literal, tracked_a1_rodata_str,
                tracked_a2_literal, tracked_a2_rodata_str,
                tracked_a3_literal, tracked_a3_rodata_str,
                tracked_a4_literal, tracked_a4_rodata_str,
                tracked_a5_literal, tracked_a5_rodata_str,
            )

        # --- Function context tracking ---
        if address in func_map:
            current_func = func_map[address][0]
        elif current_func is not None:
            for faddr, (fname, fnext) in func_map.items():
                if fname == current_func:
                    if addr_int >= int(fnext, 16):
                        current_func = None
                    break

        # --- Build handler body ---
        handler_body = []
        handler_body.append(f"    HANDLERS[{addr_int}] = function()")
        handler_body.append(f"        -- Address: {address} ({mnemonic})")

        # --- ecall handling ---
        if mnemonic == "ecall":
            _handle_ecall(
                handler_body, current_func, addr_int,
                tracked_a7_syscall, tracked_a0_literal,
                tracked_a1_rodata_str, tracked_a2_rodata_str,
                tracked_a3_literal, tracked_a3_rodata_str,
                tracked_a4_rodata_str, tracked_a5_literal,
                tracked_a5_rodata_str, tracked_a2_literal,
            )
        # --- R-Type Math (RV32I + RV32M) ---
        elif mnemonic in ["add", "sub", "xor", "or", "and", "sll", "srl", "sra",
                          "slt", "sltu", "mul", "mulh", "mulhsu", "mulhu",
                          "div", "divu", "rem", "remu"]:
            _handle_rtype(handler_body, mnemonic, args, addr_int)
        # --- RV32F Floating-Point ---
        elif mnemonic in ["fadd.s", "fsub.s", "fmul.s", "fdiv.s", "fsqrt.s",
                          "fsgnj.s", "fsgnjn.s", "fsgnjx.s", "fmin.s", "fmax.s",
                          "feq.s", "flt.s", "fle.s",
                          "fmadd.s", "fmsub.s", "fnmadd.s", "fnmsub.s",
                          "fcvt.s.w", "fcvt.s.wu", "fcvt.w.s", "fcvt.wu.s",
                          "fmv.x.w", "fmv.w.x", "fclass.s"]:
            _handle_fp(handler_body, mnemonic, args, addr_int)
        # --- I-Type ALU Math ---
        elif mnemonic in ["addi", "xori", "ori", "andi", "slli", "srli", "srai",
                          "slti", "sltiu"]:
            _handle_itype(handler_body, mnemonic, args, addr_int)
        # --- Load Operations ---
        elif mnemonic in ["lb", "lw", "lbu", "flw"]:
            _handle_load(handler_body, mnemonic, args, addr_int)
        # --- Store Operations ---
        elif mnemonic in ["sb", "sw", "fsw"]:
            _handle_store(handler_body, mnemonic, args, addr_int)
        # --- Branching & Jumps ---
        elif mnemonic in ["beq", "bne", "blt", "bge", "bltu", "bgeu"]:
            _handle_branch(handler_body, mnemonic, args, addr_int)
        elif mnemonic == "jal":
            _handle_jal(handler_body, args, addr_int)
        elif mnemonic == "jalr":
            _handle_jalr(handler_body, args, addr_int)
        elif mnemonic == "lui":
            _handle_lui(handler_body, args, addr_int)
        elif mnemonic == "auipc":
            _handle_auipc(handler_body, args, addr_int)
        elif mnemonic == "ebreak":
            handler_body.append(f"        print('System Halt: {mnemonic}')")
            handler_body.append("        return nil")

        # Close the handler function and collect body lines for merging
        handler_body.append("    end")
        handler_body.append("")

        # Determine if this instruction is a control-flow terminator
        is_term = mnemonic in TERMINATOR_OPS

        # Extract body lines (skip HANDLERS wrapper line, skip closing "end" and blank)
        body_lines = handler_body[1:-2]
        all_inst_bodies.append({
            'addr': addr_int, 'is_term': is_term, 'body_lines': body_lines
        })

    return all_inst_bodies


# =========================================================================
# State tracking
# =========================================================================

def _track_state(mnemonic, args, rodata_addr_table, rodata_table,
                 tracked_a7_syscall, tracked_a0_literal, tracked_value_type,
                 tracked_a1_literal, tracked_a1_rodata_str,
                 tracked_a2_literal, tracked_a2_rodata_str,
                 tracked_a3_literal, tracked_a3_rodata_str,
                 tracked_a4_literal, tracked_a4_rodata_str,
                 tracked_a5_literal, tracked_a5_rodata_str):
    """Update compile-time state trackers based on current instruction."""
    if mnemonic not in ["li", "addi", "lui"]:
        return (tracked_a7_syscall, tracked_a0_literal, tracked_value_type,
                tracked_a1_literal, tracked_a1_rodata_str,
                tracked_a2_literal, tracked_a2_rodata_str,
                tracked_a3_literal, tracked_a3_rodata_str,
                tracked_a4_literal, tracked_a4_rodata_str,
                tracked_a5_literal, tracked_a5_rodata_str)

    dest_reg = args[0]

    if dest_reg in ["a7", "x17"]:
        clean_imm = args[-1].split('#')[0].strip()
        try:
            tracked_a7_syscall = int(clean_imm)
        except ValueError:
            pass

    elif dest_reg in ["a0", "x10"]:
        tracked_a0_literal, tracked_value_type = _resolve_literal(
            args, mnemonic, rodata_addr_table, rodata_table
        )

    elif dest_reg in ["a1", "x11"]:
        _, tracked_a1_literal, tracked_a1_rodata_str = _resolve_arg_literal(
            args, rodata_addr_table
        )

    elif dest_reg in ["a2", "x12"]:
        _, tracked_a2_literal, tracked_a2_rodata_str = _resolve_arg_literal(
            args, rodata_addr_table
        )

    elif dest_reg in ["a3", "x13"]:
        _, tracked_a3_literal, tracked_a3_rodata_str = _resolve_arg_literal(
            args, rodata_addr_table
        )

    elif dest_reg in ["a4", "x14"]:
        _, tracked_a4_literal, tracked_a4_rodata_str = _resolve_arg_literal(
            args, rodata_addr_table
        )

    elif dest_reg in ["a5", "x15"]:
        _, tracked_a5_literal, tracked_a5_rodata_str = _resolve_arg_literal(
            args, rodata_addr_table
        )

    return (tracked_a7_syscall, tracked_a0_literal, tracked_value_type,
            tracked_a1_literal, tracked_a1_rodata_str,
            tracked_a2_literal, tracked_a2_rodata_str,
            tracked_a3_literal, tracked_a3_rodata_str,
            tracked_a4_literal, tracked_a4_rodata_str,
            tracked_a5_literal, tracked_a5_rodata_str)


def _resolve_literal(args, mnemonic, rodata_addr_table, rodata_table):
    """Resolve a0 register value to a literal string and type."""
    last_arg = args[-1]
    clean_last = last_arg.split('#')[0].strip()

    # Check for address comment (e.g., # 0x80001234 <label>)
    addr_match = re.search(r'#\s*([0-9a-fA-F]+)\s*<', last_arg)
    if addr_match:
        full_addr = int(addr_match.group(1), 16)
        str_val = rodata_addr_table.get(full_addr, None)
        if str_val is not None:
            return '"' + escape_lua_string(str_val) + '"', "string"
        else:
            return str(full_addr), "address"

    # Skip if addi with rs1 != zero and imm == 0 (move between regs)
    if mnemonic == "addi" and clean_last == "0" and args[1] not in ["x0", "zero"]:
        return "nil", "nil"

    # Check for label reference
    label_find = re.search(r"(\.LC\w+|\.L\w+)", clean_last)
    if label_find:
        return rodata_table.get(label_find.group(1), "nil"), "string"

    if clean_last.replace('-', '').isdigit():
        return clean_last, "int"

    return "nil", "nil"


def _resolve_arg_literal(args, rodata_addr_table):
    """Resolve a destination register value for a1-a5."""
    last_arg = args[-1]
    clean_last = last_arg.split('#')[0].strip()
    rodata_str = None

    addr_match = re.search(r'#\s*([0-9a-fA-F]+)\s*<', last_arg)
    if addr_match:
        full_addr = int(addr_match.group(1), 16)
        return str(full_addr), str(full_addr), rodata_addr_table.get(full_addr, None)

    if clean_last.replace('-', '').isdigit():
        try:
            val = int(clean_last)
            rodata_str = rodata_addr_table.get(val, None)
        except ValueError:
            pass
        return clean_last, clean_last, rodata_str

    return "nil", "nil", None


# =========================================================================
# ecall handler
# =========================================================================

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
    is_call_method = current_func and "callMethod" in current_func

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
        handler_body.append("        local _elapsed = task.wait(_duration)")
        handler_body.append("        reg[11] = f32_to_bits(_elapsed)")

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


# =========================================================================
# ecall sub-helpers
# =========================================================================

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
    """Syscall 46: generic templated method call."""
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

            arg_parts = []
            if arg1_is_string:
                arg_parts.append('RODATA[reg[16]] or ""')
            elif tracked_a5_rodata_str is not None or (tracked_a5_literal and tracked_a5_literal != 'nil'):
                arg_parts.append('reg[16]')
            if arg2_is_string:
                arg_parts.append('RODATA[reg[15]] or ""')

            args_str = ', ' + ', '.join(arg_parts) if arg_parts else ''

            if has_return:
                if is_valid_id:
                    handler_body.append(f'            local _r = _svc:{method_name}({args_str[2:]})')
                else:
                    handler_body.append(f'            local _r = _svc[{method_literal}](_svc{args_str})')
                _emit_callmethod_return(handler_body, return_is_obj, return_is_buffer)
            else:
                if is_valid_id:
                    handler_body.append(f'            _svc:{method_name}({args_str[2:]})')
                else:
                    handler_body.append(f'            _svc[{method_literal}](_svc{args_str})')
            handler_body.append('        end')
        else:
            handler_body.append('        local _obj = OBJECTS[reg[11]]')
            handler_body.append('        if _obj then')

            arg_parts = []
            if arg1_is_string:
                arg_parts.append('RODATA[reg[13]] or ""')
            elif tracked_a2_literal != 'nil' and tracked_a2_literal is not None:
                arg_parts.append('reg[13]')
            if arg2_is_string:
                arg_parts.append('RODATA[reg[15]] or ""')

            args_str = ', ' + ', '.join(arg_parts) if arg_parts else ''

            if has_return:
                if is_valid_id:
                    handler_body.append(f'            local _r = _obj:{method_name}({args_str[2:]})')
                else:
                    handler_body.append(f'            local _r = _obj[{method_literal}](_obj{args_str})')
                _emit_callmethod_return(handler_body, return_is_obj, return_is_buffer)
            else:
                if is_valid_id:
                    handler_body.append(f'            _obj:{method_name}({args_str[2:]})')
                else:
                    handler_body.append(f'            _obj[{method_literal}](_obj{args_str})')
            handler_body.append('        end')
    else:
        # Method name not resolved at transpile time
        handler_body.append("        local _obj = OBJECTS[reg[11]]")
        handler_body.append("        local _methodName = RODATA[reg[12]] or '?'")
        handler_body.append("        if _obj and _methodName then")
        handler_body.append("            -- Runtime dynamic dispatch (slower, no templating)")
        handler_body.append("            _obj[_methodName](_obj)")
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


def _emit_runtime_callmethod(handler_body):
    """Runtime-dispatched callMethod (inside callMethod function)."""
    handler_body.append("        local _objHandle = reg[11]")
    handler_body.append("        local _methodName = RODATA[reg[12]] or '?'")
    handler_body.append("        local _arg1Val = reg[13]")
    handler_body.append("        local _flags = reg[14]")
    handler_body.append("        local _hasReturn = bit32.band(_flags, 1) ~= 0")
    handler_body.append("        local _returnIsBuffer = bit32.band(_flags, 32) ~= 0")
    handler_body.append("        local _arg1IsString = bit32.band(_flags, 8) ~= 0")
    handler_body.append("        local _obj = OBJECTS[_objHandle]")
    handler_body.append("        if _obj and _methodName then")
    handler_body.append("            local _arg1 = nil")
    handler_body.append("            if _arg1IsString then local _s = RODATA[_arg1Val] or S.read_cstring(_arg1Val) or ''; _arg1 = buffer.fromstring(_s) end")
    handler_body.append("            if _hasReturn then")
    handler_body.append("                local _r = _obj[_methodName](_obj, _arg1)")
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
    handler_body.append("                _obj[_methodName](_obj, _arg1)")
    handler_body.append("            end")
    handler_body.append("        end")


# =========================================================================
# R-Type Math handlers
# =========================================================================

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


# =========================================================================
# RV32F Floating-Point handlers
# =========================================================================

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
        if mnemonic == "fcvt.w.s":
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
            handler_body.append(f"        {ird} = {frs1}")
        else:
            frd = clean_reg_fp(args[0])
            irs1 = clean_reg(args[1])
            handler_body.append(f"        {frd} = {irs1}")

    # FP Classify
    elif mnemonic == "fclass.s":
        ird = clean_reg(args[0])
        frs1 = clean_reg_fp(args[1])
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


# =========================================================================
# I-Type ALU handlers
# =========================================================================

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


# =========================================================================
# Load/Store handlers
# =========================================================================

def _handle_load(handler_body, mnemonic, args, addr_int):
    rd = clean_reg(args[0]) if mnemonic != "flw" else clean_reg_fp(args[0])
    mem_match = re.match(r"(-?\d+)\((x\d+)\)", args[1])
    if mem_match:
        offset, rs1 = mem_match.group(1), clean_reg(mem_match.group(2))
        addr_expr = f"{rs1} + {offset}"
        if mnemonic == "lw" or mnemonic == "flw":
            handler_body.append(f"        do local _a = {addr_expr}; if _a and _a ~= 0 then local _i = bit32.rshift(_a, 16); local _p = PAGES[_i]; {rd} = _p and buffer.readi32(_p, bit32.band(_a, 0xFFFF)) or 0 else {rd} = 0 end end")
        elif mnemonic == "lb":
            handler_body.append(f"        do local _a = {addr_expr}; if _a and _a ~= 0 then local _i = bit32.rshift(_a, 16); local _p = PAGES[_i]; {rd} = _p and buffer.readi8(_p, bit32.band(_a, 0xFFFF)) or 0 else {rd} = 0 end end")
        elif mnemonic == "lbu":
            handler_body.append(f"        do local _a = {addr_expr}; if _a and _a ~= 0 then local _i = bit32.rshift(_a, 16); local _p = PAGES[_i]; {rd} = bit32.band(_p and buffer.readi8(_p, bit32.band(_a, 0xFFFF)) or 0, 0xFF) else {rd} = 0 end end")
    handler_body.append(f"        return {addr_int + 4}")


def _handle_store(handler_body, mnemonic, args, addr_int):
    rs2 = clean_reg(args[0]) if mnemonic != "fsw" else clean_reg_fp(args[0])
    mem_match = re.match(r"(-?\d+)\((x\d+)\)", args[1])
    if mem_match:
        offset, rs1 = mem_match.group(1), clean_reg(mem_match.group(2))
        addr_expr = f"{rs1} + {offset}"
        if mnemonic == "sw" or mnemonic == "fsw":
            handler_body.append(f"        do local _a = {addr_expr}; if _a and _a ~= 0 then local _i = bit32.rshift(_a, 16); local _p = PAGES[_i]; if not _p then _p = buffer.create(65536); PAGES[_i] = _p end; buffer.writei32(_p, bit32.band(_a, 0xFFFF), {rs2}) end end")
        elif mnemonic == "sb":
            handler_body.append(f"        do local _a = {addr_expr}; if _a and _a ~= 0 then local _i = bit32.rshift(_a, 16); local _p = PAGES[_i]; if not _p then _p = buffer.create(65536); PAGES[_i] = _p end; buffer.writei8(_p, bit32.band(_a, 0xFFFF), {rs2}) end end")
    handler_body.append(f"        return {addr_int + 4}")


# =========================================================================
# Branch/Jump handlers
# =========================================================================

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
    mem_match = re.match(r"(-?\d+)\((x\d+)\)", args[1])
    if mem_match:
        offset, rs1 = mem_match.group(1), clean_reg(mem_match.group(2))
        handler_body.append(f"        local _next_pc = bit32.band({rs1} + {offset}, 0xFFFFFFFF)")
        # x0 (reg[1]) is hardwired to zero in RISC-V — never write to it
        if rd != "reg[1]":
            handler_body.append(f"        {rd} = {(addr_int + 4) & 0xFFFFFFFF}")
        handler_body.append("        return _next_pc")


def _handle_lui(handler_body, args, addr_int):
    rd = clean_reg(args[0])
    imm = args[1]
    handler_body.append(f"        {rd} = {int(imm, 0) * 4096 & 0xFFFFFFFF}")
    handler_body.append(f"        return {addr_int + 4}")


def _handle_auipc(handler_body, args, addr_int):
    rd = clean_reg(args[0])
    imm = args[1]
    handler_body.append(f"        {rd} = {(addr_int + int(imm, 0) * 4096) & 0xFFFFFFFF}")
    handler_body.append(f"        return {addr_int + 4}")

