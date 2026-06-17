"""Instruction-to-Lua generation: state tracking and handler body construction."""

from .constants import TERMINATOR_OPS
from .state_tracker import _track_state
from .handlers.ecall import _handle_ecall
from .handlers.alu import _handle_rtype, _handle_itype
from .handlers.float import _handle_fp
from .handlers.memory import _handle_load, _handle_store
from .handlers.control import _handle_branch, _handle_jal, _handle_jalr, _handle_lui, _handle_auipc


def generate_handler_bodies(parsed_instructions, rodata_addr_table, rodata_table,
                            func_map, validate=False):
    """Generate instruction handler bodies with compile-time state tracking.

    If *validate* is True, memory load/store and heap operations emit extra
    runtime checks (null-pointer, double-free, etc.).

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
                rodata_addr_table,
                validate=validate
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
            _handle_load(handler_body, mnemonic, args, addr_int, validate)
        # --- Store Operations ---
        elif mnemonic in ["sb", "sw", "fsw"]:
            _handle_store(handler_body, mnemonic, args, addr_int, validate)
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
        # --- ret pseudo-instruction (jalr zero, 0(ra)) ---
        elif mnemonic == "ret":
            # ret is jalr zero, 0(ra) — equivalent to return _next_pc with ra as base
            handler_body.append("        local _next_pc = bit32.band(reg[2] + 0, 0xFFFFFFFF)")
            handler_body.append("        return _next_pc")
        # --- Catch-all for unrecognized instructions ---
        else:
            handler_body.append(f"        print('System Halt: Unrecognized instruction {mnemonic} at {address}')")
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
