"""Builders: shared.luau, run.luau, and chunk module content generation."""

from .utils import escape_lua_string


def build_shared_luau(enums_sparse_lines, enum_to_index_lines, rodat_lua_entries, rodata_init_lines,
                      main_address_str, validate=False):
    """Build shared.luau content string.

    If *validate* is True, S.validate_addr() and related helpers are emitted
    for runtime memory-access validation.
    """
    shared_lines = []

    shared_lines.extend([
        "-- Shared VM State Module (shared.luau)",
        "-- Returned S table holds all mutable state shared across chunk modules.",
        "",
        "local S = {}",
        "",
        "-- Register file (32 x 32-bit, 1-based indexing for Luau)",
        "S.reg = table.create(32, 0)",
        "S.reg[3] = 0x80000000 + (512 * 1024 * 1024) -- Stack Pointer (x2) at 0xA0000000",
        "",
        "-- FP Register file (32 x 32-bit float bit patterns, 1-based)",
        "S.freg = table.create(32, 0)",
        "",
        "-- Paged memory (64K pages, demand-allocated)",
        "S.PAGES = {}",
        "local PAGE_SIZE = 65536",
        "",
        "-- Memory access helpers",
        "function S.write_mem32(addr, val)",
        "    local idx = bit32.rshift(addr, 16)",
        "    local offset = bit32.band(addr, 0xFFFF)",
        "    local page = S.PAGES[idx]",
        "    if not page then",
        "        page = buffer.create(PAGE_SIZE)",
        "        S.PAGES[idx] = page",
        "    end",
        "    buffer.writei32(page, offset, val)",
        "end",
        "",
        "function S.read_mem32(addr)",
        "    local idx = bit32.rshift(addr, 16)",
        "    local page = S.PAGES[idx]",
        "    if not page then return 0 end",
        "    return buffer.readi32(page, bit32.band(addr, 0xFFFF))",
        "end",
        "",
        "function S.write_mem8(addr, val)",
        "    local idx = bit32.rshift(addr, 16)",
        "    local offset = bit32.band(addr, 0xFFFF)",
        "    local page = S.PAGES[idx]",
        "    if not page then",
        "        page = buffer.create(PAGE_SIZE)",
        "        S.PAGES[idx] = page",
        "    end",
        "    buffer.writei8(page, offset, val)",
        "end",
        "",
        "function S.read_mem8(addr)",
        "    local idx = bit32.rshift(addr, 16)",
        "    local page = S.PAGES[idx]",
        "    if not page then return 0 end",
        "    return buffer.readi8(page, bit32.band(addr, 0xFFFF))",
        "end",
        "",
        "-- Float <-> bit conversion helpers",
        "local _f32_buf = buffer.create(4)",
        "function S.f32_to_bits(f)",
        "    buffer.writef32(_f32_buf, 0, f)",
        "    return buffer.readi32(_f32_buf, 0)",
        "end",
        "",
        "function S.bits_to_f32(b)",
        "    buffer.writei32(_f32_buf, 0, b)",
        "    return buffer.readf32(_f32_buf, 0)",
        "end",
        "",
        "-- C-string reader (null-terminated string from memory)",
        "function S.read_cstring(ptr)",
        "    if ptr == 0 then return nil end",
        "    local idx = bit32.rshift(ptr, 16)",
        "    local page = S.PAGES[idx]",
        "    if not page then return nil end",
        "    local offset = bit32.band(ptr, 0xFFFF)",
        "    local chars = {}",
        "    local max_offset = buffer.len(page) - 1",
        "    for i = 0, 4095 do",
        "        local cur = offset + i",
        "        if cur > max_offset then break end",
        "        local b = buffer.readi8(page, cur)",
        "        if b == 0 then break end",
        "        chars[#chars + 1] = string.char(b)",
        "    end",
        "    return table.concat(chars)",
        "end",
        "",
        "-- VM object handle pool",
        "S.OBJECTS = {}",
        "S.NEXT_HANDLE = 1",
        "",
        "-- RODATA string table (address -> string)",

        "S.RODATA = {",
    ])
    shared_lines.extend(rodat_lua_entries)
    shared_lines.append("}")
    shared_lines.append("")

    # Pre-populate .rodata memory
    shared_lines.extend(rodata_init_lines)
    if rodata_init_lines:
        shared_lines.append("")

    # Enum tables
    shared_lines.append("-- Enum tables")
    shared_lines.append("S.ENUMS = {}")
    shared_lines.extend(enums_sparse_lines)
    shared_lines.append("")
    shared_lines.append("S.ENUM_TO_INDEX = {}")
    shared_lines.extend(enum_to_index_lines)
    shared_lines.append("")

    # Handlers table
    shared_lines.append("-- Instruction handler dispatch table (populated by chunks)")
    shared_lines.append("S.HANDLERS = {}")
    shared_lines.append("")

    # Heap state
    shared_lines.append("-- Heap allocator state")
    shared_lines.append("S.HEAP_BRK = 0x81000000")
    shared_lines.append("S.FREE_LIST = {}")
    shared_lines.append("S.ALLOCS = {}")
    shared_lines.append("")

    # Thread state
    shared_lines.append("-- Thread state (multi-threading via task.spawn)")
    shared_lines.append("S.THREADS = {}")
    shared_lines.append("S.NEXT_THREAD_ID = 1")
    shared_lines.append("S._vm_gen = 0  -- generation counter: bumped before each dispatch iteration")
    shared_lines.append("")

    # Function wrapper cache: maps C++ function addresses to callable Luau functions.
    # Used by callMethod/callMethodStatic when argNIsFunction flag is set.
    # The wrapper packs arguments into RISC-V registers and dispatches the thread.
    shared_lines.append("-- Function pointer wrappers (for passing C++ functions to Roblox callbacks)")
    shared_lines.append("S._FUNC_WRAPPERS = {}")
    shared_lines.append("function S.get_function(addr)")
    shared_lines.append("    local _cached = S._FUNC_WRAPPERS[addr]")
    shared_lines.append("    if _cached then return _cached end")
    shared_lines.append("    local _wrapper = function(...)")
    shared_lines.append("        -- Save parent VM state so the callback does not corrupt the caller")
    shared_lines.append("        local _parentReg = table.create(32, 0)")
    shared_lines.append("        local _parentFreg = table.create(32, 0)")
    shared_lines.append("        for _i = 1, 32 do")
    shared_lines.append("            _parentReg[_i] = S.reg[_i]")
    shared_lines.append("            _parentFreg[_i] = S.freg[_i]")
    shared_lines.append("        end")
    shared_lines.append("        -- Pack callback arguments into RISC-V registers")
    shared_lines.append("        local _reg = table.create(32, 0)")
    shared_lines.append("        local _args = {...}")
    shared_lines.append("        for _i = 1, #_args do")
    shared_lines.append("            _reg[10 + _i] = _args[_i] or 0  -- a0..aN = RISC-V arguments")
    shared_lines.append("        end")
    shared_lines.append("        _reg[2] = 0   -- ra=0 so the thread halts on return")
    shared_lines.append("        _reg[3] = S.reg[3]  -- inherit stack pointer")
    shared_lines.append("        S.dispatch_thread(_reg, addr)")
    shared_lines.append("        -- Restore parent VM state")
    shared_lines.append("        for _i = 1, 32 do")
    shared_lines.append("            S.reg[_i] = _parentReg[_i]")
    shared_lines.append("            S.freg[_i] = _parentFreg[_i]")
    shared_lines.append("        end")
    shared_lines.append("    end")
    shared_lines.append("    S._FUNC_WRAPPERS[addr] = _wrapper")
    shared_lines.append("    return _wrapper")
    shared_lines.append("end")
    shared_lines.append("")
    # Thread dispatch function: runs the VM dispatch loop with a per-thread register set.
    # Each thread gets its own 64K stack carved from the heap.
    # S.reg/S.freg are shared globals. The thread restores its register state
    # before each instruction.  After the handler returns, it checks whether
    # another thread ran during a yield by comparing S._vm_gen against a
    # snapshot taken before the handler call.  If the counter diverged, the
    # save is SKIPPED because S.reg was corrupted during the yield and
    # threadReg already holds the correct pre-yield state.
    shared_lines.append("-- Thread VM dispatch: runs a new dispatch loop with isolated registers")
    shared_lines.append("function S.dispatch_thread(threadReg, startPC)")
    shared_lines.append("    -- Per-thread floating-point register file")
    shared_lines.append("    local _threadFreg = table.create(32, 0)")
    shared_lines.append("    for _i = 1, 32 do _threadFreg[_i] = S.freg[_i] end")
    shared_lines.append("")
    shared_lines.append("    local _pc = startPC")
    shared_lines.append("    while _pc and _pc ~= 0 do")
    shared_lines.append("        -- Restore this thread's registers before each instruction.")
    shared_lines.append("        -- (After a yield, another thread may have overwritten S.reg/S.freg.)")
    shared_lines.append("        for _i = 1, 32 do")
    shared_lines.append("            S.reg[_i] = threadReg[_i]")
    shared_lines.append("            S.freg[_i] = _threadFreg[_i]")
    shared_lines.append("        end")
    shared_lines.append("        local _handler = S.HANDLERS[_pc]")
    shared_lines.append("        if not _handler then break end")
    shared_lines.append("")
    shared_lines.append("        -- Bump generation counter so other threads know we ran.")
    shared_lines.append("        -- Snapshot it so we can detect if another thread entered")
    shared_lines.append("        -- dispatch while our handler was yielded.")
    shared_lines.append("        S._vm_gen = S._vm_gen + 1")
    shared_lines.append("        local _myGen = S._vm_gen")
    shared_lines.append("        _pc = _handler()")
    shared_lines.append("")
    shared_lines.append("        -- Only save if no other thread ran a dispatch iteration")
    shared_lines.append("        -- during our handler call (which would have bumped _vm_gen).")
    shared_lines.append("        -- If another thread ran, S.reg was corrupted; threadReg has")
    shared_lines.append("        -- the correct pre-yield state for the next restore.")
    shared_lines.append("        if S._vm_gen == _myGen then")
    shared_lines.append("            for _i = 1, 32 do")
    shared_lines.append("                threadReg[_i] = S.reg[_i]")
    shared_lines.append("                _threadFreg[_i] = S.freg[_i]")
    shared_lines.append("            end")
    shared_lines.append("        end")
    shared_lines.append("    end")
    shared_lines.append("end")
    shared_lines.append("")

    # ── Validation helpers (only emitted when --validate is passed) ──
    if validate:
        shared_lines.extend([
            "",
            "-- Memory validation helpers (emitted by --validate)",
            "-- Valid address ranges:",
            "--   Heap:  0x81000000 .. S.HEAP_BRK",
            "--   Stack: 0xA0000000 downward (main), or thread stack from HEAP_BRK",
            "--   Rodata: anywhere pages may exist",
            "function S.validate_addr(addr)",
            "    if addr == 0 then",
            "        error('[VM Validation] Null pointer dereference in memory access')",
            "    end",
            "    -- Null-derived pointers often land in the low page (< 0x1000)",
            "    if addr < 0x1000 then",
            "        error('[VM Validation] Suspect low address 0x' .. string.format('%x', addr) .. ' — likely a null-derived pointer')",
            "    end",
            "end",
            "",
        ])

    # ── Mirror Roblox built-in globals into _G ──
    # In Roblox Luau, _G only contains user-defined globals; built-in globals
    # (task, Instance, game, etc.) are NOT in _G.  getGlobal(syscall 52) falls
    # back to _G[name] when it cannot resolve the name at compile time.  By
    # mirroring these globals into _G, the fallback path works correctly.
    shared_lines.append("-- Mirror Roblox built-in globals into _G (used by getGlobal fallback)")
    shared_lines.append("_G.task = task")
    shared_lines.append("_G.Instance = Instance")
    shared_lines.append("_G.game = game")
    shared_lines.append("_G.workspace = workspace")
    shared_lines.append("_G.Vector3 = Vector3")
    shared_lines.append("_G.CFrame = CFrame")
    shared_lines.append("_G.Color3 = Color3")
    shared_lines.append("_G.UDim2 = UDim2")
    shared_lines.append("_G.require = require")
    shared_lines.append("_G.print = print")
    shared_lines.append("_G.warn = warn")
    shared_lines.append("_G.math = math")
    shared_lines.append("_G.string = string")
    shared_lines.append("_G.table = table")
    shared_lines.append("_G.buffer = buffer")
    shared_lines.append("_G.bit32 = bit32")
    shared_lines.append("")

    shared_lines.append("return S")

    return "\n".join(shared_lines)


def build_run_luau(main_address_int, main_address_str, chunk_count):
    """Build run.luau content string (while-loop dispatch VM)."""
    run_lines = []

    run_lines.extend([
        "-- VM Runner (run.luau)",
        "-- While-loop dispatch: fetches next HANDLERS[PC], executes it, repeats.",
        "",
        "-- Require shared state and all instruction-handler chunks",
        "local S = require(script.Parent.shared)",
    ])

    for n in range(1, chunk_count + 1):
        run_lines.append(f"local chunk_{n} = require(script.Parent[\"chunk_{n}\"])")

    run_lines.append("")

    # Call chunk initialization functions
    run_lines.append("-- Initialize instruction handlers by calling chunk init functions")
    for n in range(1, chunk_count + 1):
        run_lines.append(f"chunk_{n}()")
    run_lines.append("")

    run_lines.extend([
        f"-- Set PC to entry point ({main_address_str})",
        f"local PC = {main_address_int}",
        "",
        "-- Main dispatch loop with yield protection (same pattern as dispatch_thread)",
        "local tracePath = {}",
        "",
        "-- Per-main-thread register backup for yield recovery",
        "local _mainReg = table.create(32, 0)",
        "local _mainFreg = table.create(32, 0)",
        "for _i = 1, 32 do",
        "    _mainReg[_i] = S.reg[_i]",
        "    _mainFreg[_i] = S.freg[_i]",
        "end",
        "",
        "while PC and PC ~= 0 do",
        "    table.insert(tracePath, PC)",
        "",
        "    -- Restore main thread registers before each instruction",
        "    -- (after a yield, spawned threads may have overwritten S.reg/S.freg)",
        "    for _i = 1, 32 do",
        "        S.reg[_i] = _mainReg[_i]",
        "        S.freg[_i] = _mainFreg[_i]",
        "    end",
        "",
        "    local handler = S.HANDLERS[PC]",
        "    if not handler then",
        "        print('VM Halt: No handler for PC 0x' .. string.format('%x', PC))",
        "        break",
        "    end",
        "",
        "    -- Snapshot generation counter to detect if we yielded",
        "    local _preGen = S._vm_gen",
        "    PC = handler()",
        "",
        "    -- Only save if no other thread ran during our handler",
        "    -- (if another thread ran, S.reg was corrupted — skip save)",
        "    if S._vm_gen == _preGen then",
        "        for _i = 1, 32 do",
        "            _mainReg[_i] = S.reg[_i]",
        "            _mainFreg[_i] = S.freg[_i]",
        "        end",
        "    end",
        "end",
        "",
        f'print("VM exited. PC={main_address_str}")',
        'print("Trace (last 100): ")',
        "local toPrint = #tracePath - 100",
        "for i, path in pairs(tracePath) do",
        '    if i > toPrint then',
        '        print("Trace path: " .. tostring(i) .. " at: " .. string.format("%X", path))',
        "    end",
        "end",
    ])

    return "\n".join(run_lines)
