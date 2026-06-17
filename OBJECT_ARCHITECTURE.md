# Object Architecture — cpp-luau-obfs

This document explains how the C++ → Luau object system works in detail, covering the full transformation pipeline from typed C++ classes down to obfuscated Luau handler closures.

---

## 1. The Three-Layer Architecture

The project operates across three distinct layers, each with its own execution model and object representation:

```
┌─────────────────────────────────────────────────────────┐
│  LAYER 1: C++ Source (compile-time)                      │
│  - Typed classes: LuaObj, Vector3, CFrame, Color3, UDim2 │
│  - Inline assembly ecall for every API boundary           │
│  - Pointers, smart pointers, templates, value semantics   │
├─────────────────────────────────────────────────────────┤
│  LAYER 2: RISC-V Binary (link-time)                      │
│  - 32-bit RISC-V machine code (RV32IMF)                  │
│  - Registers a0-a7 carry arguments & syscall numbers     │
│  - .rodata holds string constants; .text holds code      │
├─────────────────────────────────────────────────────────┤
│  LAYER 3: Luau Runtime (execution-time)                  │
│  - Python transpiler converts RISC-V → Luau closures     │
│  - Integer handles route to Roblox instances in OBJECTS   │
│  - Paged memory (64KB pages) emulates flat address space │
│  - While(true) dispatch loop runs handler[PC]() each tick │
└─────────────────────────────────────────────────────────┘
```

---

## 2. The Handle System

### 2.1 Core Idea

**Every Roblox object is an integer.** There are no typed wrappers at runtime. A C++ class like `LuaObj` holds a single `void* h` field, which is actually an integer cast to a pointer. This integer indexes into the Luau-side `S.OBJECTS` table:

```lua
S.OBJECTS = {}           -- integer handle → Roblox Instance
S.BUFFERS  = {}          -- integer handle → Luau buffer
S.NEXT_HANDLE = 1        -- monotonically increasing counter
```

When C++ code calls `LuaObj::getService("Players")`, the flow is:

1. **C++ side:** `Rbxl::getService("Players")` emits `ecall` with `a7=47`, `a0=&"Players"`
2. **Luau handler:** runs `game:GetService("Players")`, stores result in `OBJECTS[S.NEXT_HANDLE]`, writes `S.NEXT_HANDLE` back to `reg[11]` (a0), increments `S.NEXT_HANDLE`
3. **C++ side:** the returned value flows back through a0 register into the `void* h` field

From that point on, every method call, property access, or lifecycle operation passes this integer handle to identify the target object.

### 2.2 Handle Tables

| Table | Key | Value | Purpose |
|-------|-----|-------|---------|
| `S.OBJECTS` | handle (int) | Roblox Instance, Vector3, Color3, etc. | All Roblox objects live here |
| `S.BUFFERS` | handle (int) | Luau `buffer` object | Raw memory buffers |
| `S.RODATA` | address (int) | string | Read-only string literals from binary |
| `S.ENUMS` | enum index (int) | Roblox Enum value | Sparse enum cache |
| `S.ALLOCS` | address (int) | size (int) | Active heap allocations |
| `S.FREE_LIST` | address (int) | size (int) | Freed blocks available for reuse |
| `S.THREADS` | thread ID (int) | `{reg, pc}` table | Active spawned threads |
| `S._FUNC_WRAPPERS` | function address (int) | callable Luau function | C++→Luau callback wrappers |

### 2.3 Handle Lifecycle

```
Creation:
  getService()  → OBJECTS[NEXT_HANDLE] = result; return NEXT_HANDLE; NEXT_HANDLE++
  getGlobal()   → OBJECTS[NEXT_HANDLE] = _G[name]; return NEXT_HANDLE; NEXT_HANDLE++
  clone()       → OBJECTS[NEXT_HANDLE] = obj:Clone(); return NEXT_HANDLE; NEXT_HANDLE++
  toObject()    → OBJECTS[NEXT_HANDLE] = Vector3.new(x,y,z); return NEXT_HANDLE; NEXT_HANDLE++

Destruction:
  release()     → OBJECTS[handle] = nil       (syscall 64)
  destroy()     → OBJECTS[handle]:Destroy() + OBJECTS[handle] = nil
  freeBuffer()  → BUFFERS[handle] = nil       (syscall 22)

Transfer:
  When passing from C++ to Luau via method calls, handles flow through registers and
  the transpiler converts them back to OBJECTS dereferences.
```

---

## 3. The LuaObj Class (C++ Side)

### 3.1 Design

`LuaObj` is the base class for all Roblox objects on the C++ side. It is deliberately minimal:

```cpp
class LuaObj {
protected:
    void* h;    // The integer handle, cast to void*
public:
    bool valid() const { return h != nullptr; }
    void* handle() const { return h; }

    // Property access (the ONLY property API exposed to users)
    LuaObj getPropertyObject(const char* name) const;
    void setPropertyObject(const char* name, const LuaObj& value);

    // Service / Global / Method lookups
    static LuaObj getService(const char* name);
    static LuaObj getGlobal(const char* name);
    LuaObj getMethod(const char* methodName) const;
    LuaObj require() const;

    // Generic method call (templated, 0-4 extra args)
    template<typename... Args>
    void* callMethod(const char* methodName, Args... args, int flags);

    template<typename... Args>
    void* callMethodStatic(const char* methodName, Args... args, int flags);

    // Primitive conversions
    static LuaObj fromFloat(float f);
    static LuaObj fromInt(int i);
    static LuaObj fromBool(bool b);
    static LuaObj fromString(const char* s);
    float toFloat() const;
    int toInt() const;
    bool toBool() const;
    const char* toString() const;

    // Lifecycle
    void release();
};
```

### 3.2 How Each Method Crosses the Boundary

Every method in `LuaObj` ultimately calls inline RISC-V assembly:

```cpp
// Pattern: load arguments into a0-a6, syscall number in a7, call ecall
void* getService(const char* name) {
    void* handle = nullptr;
    asm volatile (
        "mv a0, %1; li a7, 47; ecall; mv %0, a0"
        : "=r"(handle) : "r"(name)
        : "a0", "a7"
    );
    return handle;
}
```

The transpiler on the Luau side recognizes syscall 47 and generates the matching handler. This is the **ABI contract** — the C++ code and Luau handlers agree on register layout and syscall numbering.

### 3.3 Primitive Conversions (A Clever Trick)

Functions like `LuaObj::fromFloat()` use an ecall with **a7=0** — the transpiler does NOT use the syscall number to identify them. Instead, it detects them by **function name**:

```python
# In ecall/__init__.py:
is_from_float = current_func and "fromFloat" in current_func
if is_from_float:
    emit_from_float(handler_body)  # Wraps float bits into OBJECTS
```

This works because the C++ compiler emits function labels (`<LuaObj::fromFloat>`) in the assembly, and the transpiler tracks which function it's currently inside via `func_map`.

---

## 4. Method Call Architecture (syscall 46)

### 4.1 The Flag System

Method calls use a **21-bit flag field** that tells the transpiler exactly how to marshal arguments:

| Bit | Value | Name | Meaning |
|-----|-------|------|---------|
| 0 | 1 | `HAS_RETURN` | Method returns a value |
| 1 | 2 | `RETURN_IS_OBJ` | Return value goes into OBJECTS |
| 2 | 4 | `IS_SERVICE` | Call target is a service (arg handling differs) |
| 3 | 8 | `ARG1_IS_STRING` | Arg 1: dereference RODATA for string |
| 4 | 16 | `ARG2_IS_STRING` | Arg 2: dereference RODATA for string |
| 5 | 32 | `RETURN_IS_BUFFER` | Return value goes into BUFFERS |
| 6 | 64 | `ARG3_IS_STRING` | Arg 3: dereference RODATA for string |
| 7 | 128 | `ARG4_IS_STRING` | Arg 4: dereference RODATA for string |
| 8 | 256 | `IS_STATIC` | Use `.` syntax (no implicit `self`) |
| 9 | 512 | `ARG1_IS_BUFFER` | Arg 1: dereference BUFFERS |
| 10 | 1024 | `ARG2_IS_BUFFER` | Arg 2: dereference BUFFERS |
| 11 | 2048 | `ARG3_IS_BUFFER` | Arg 3: dereference BUFFERS |
| 12 | 4096 | `ARG4_IS_BUFFER` | Arg 4: dereference BUFFERS |
| 13 | 8192 | `ARG1_IS_FUNCTION` | Arg 1: wrap as callable Luau thunk |
| 14 | 16384 | `ARG2_IS_FUNCTION` | Arg 2: wrap as callable Luau thunk |
| 15 | 32768 | `ARG3_IS_FUNCTION` | Arg 3: wrap as callable Luau thunk |
| 16 | 65536 | `ARG4_IS_FUNCTION` | Arg 4: wrap as callable Luau thunk |
| 17 | 131072 | `ARG1_IS_OBJECT` | Arg 1: dereference OBJECTS |
| 18 | 262144 | `ARG2_IS_OBJECT` | Arg 2: dereference OBJECTS |
| 19 | 524288 | `ARG3_IS_OBJECT` | Arg 3: dereference OBJECTS |
| 20 | 1048576 | `ARG4_IS_OBJECT` | Arg 4: dereference OBJECTS |

### 4.2 Two Dispatch Strategies

The transpiler uses **compile-time literal tracking** to decide between two code-generation strategies:

#### a) Fast Path — Templated Dispatch

If the transpiler can statically resolve the method name (by tracking `li` instructions that load rodata addresses into `a1`), it generates a direct Luau call:

```lua
-- Tracked: a1_rodata_str = "SetPrimaryPartCFrame"
-- Generates:
local _obj = OBJECTS[reg[11]]
if _obj then
    _obj:SetPrimaryPartCFrame(CFrame.new(...))
end
```

This path is used for most method calls and is the reason the transpiler has extensive `_track_state()` logic.

#### b) Slow Path — Runtime Dispatch

If the method name can't be resolved at transpile time (e.g., computed method names, indirect calls), a runtime dispatch is generated:

```lua
local _obj = OBJECTS[reg[11]]
local _methodName = RODATA[reg[12]] or '?'
local _flags = reg[14]
-- Decode flags bit by bit, build arg array, call _obj[_methodName](...)
```

The slow path pay the cost of bit-twiddling the flags at runtime but is fully general.

### 4.3 Register Layout for syscall 46

```
a0 (reg[11]) = object handle
a1 (reg[12]) = method name pointer (→ RODATA string)
a2 (reg[13]) = arg 1 (or service name if IS_SERVICE flag)
a3 (reg[14]) = flags
a4 (reg[15]) = arg 2 (or arg 1 if IS_SERVICE)
a5 (reg[16]) = arg 3 (or arg 2 if IS_SERVICE)
a6 (reg[17]) = arg 4 (or arg 3 if IS_SERVICE)
```

> **Note:** The service path shifts arguments to make room for the service name in a2. This is a design trade-off: services don't need a separate handle because they're looked up by name at each call site, and the service name occupies the arg1 slot.

### 4.4 Function Pointer Wrappers

When `argNIsFunction` is set, the transpiler wraps the raw integer function address into a callable Luau closure:

```lua
function S.get_function(addr)
    local _cached = S._FUNC_WRAPPERS[addr]
    if _cached then return _cached end
    local _wrapper = function(...)
        -- Save parent VM state
        -- Pack callback args into RISC-V registers
        -- Dispatch thread at 'addr'
        -- Restore parent VM state
    end
    S._FUNC_WRAPPERS[addr] = _wrapper
    return _wrapper
end
```

This allows passing C++ function pointers as callbacks to Roblox events (e.g., `part.Touched:Connect(myHandler)`).

---

## 5. Struct Bridge (syscalls 54–61)

### 5.1 The Problem

C++ types like `Vector3`, `CFrame`, `Color3`, and `UDim2` exist as **plain memory** in the paged VM. But Roblox APIs expect native Luau types (`Vector3.new()`, `CFrame.new()`, etc.). The struct bridge translates between these two worlds.

### 5.2 Bridge Operations

| Syscall | Direction | Type | What It Does |
|---------|-----------|------|-------------|
| 54 | OBJECTS → C++ | Vector3 | Reads `OBJECTS[reg[11]].X/Y/Z` into `*reg[12]` as 3× float32 |
| 55 | C++ → OBJECTS | Vector3 | Reads 3 floats from `*reg[11]`, creates `Vector3.new()`, stores in OBJECTS |
| 56 | OBJECTS → C++ | CFrame | Reads `:GetComponents()` into `*reg[12]` as 12× float32 |
| 57 | C++ → OBJECTS | CFrame | Reads 12 floats from `*reg[11]`, creates `CFrame.new()`, stores in OBJECTS |
| 58 | OBJECTS → C++ | Color3 | Reads `OBJECTS[reg[11]].R/G/B` into `*reg[12]` |
| 59 | C++ → OBJECTS | Color3 | Reads 3 floats from `*reg[11]`, creates `Color3.new()`, stores in OBJECTS |
| 60 | OBJECTS → C++ | UDim2 | Reads 4 scales/offsets from `OBJECTS[reg[11]]` into `*reg[12]` |
| 61 | C++ → OBJECTS | UDim2 | Reads 4 floats from `*reg[11]`, creates `UDim2.new()`, stores in OBJECTS |

### 5.3 C++ Side Implementation

Each struct has two bridge methods implemented with inline assembly:

```cpp
struct Vector3 {
    float x, y, z;

    // Read from Roblox object into this struct
    void readFromObject(void* objHandle) {
        asm volatile (
            "mv a0, %0; mv a1, %1; li a7, 54; ecall"
            : : "r"(objHandle), "r"(this)
            : "a0", "a1", "a7", "memory"
        );
    }

    // Write this struct into a new Roblox object (returns handle)
    void* toObject() const {
        void* handle;
        asm volatile (
            "mv a0, %1; li a7, 55; ecall; mv %0, a0"
            : "=r"(handle) : "r"(this)
            : "a0", "a7", "memory"
        );
        return handle;
    }
};
```

The `"memory"` clobber is critical — it tells the compiler that the inline asm may read/write any memory, preventing reordering around the ecall.

### 5.4 Luau Side Implementation

```lua
-- Syscall 55: C++ struct → Roblox Vector3
local _src = reg[11]
local _x = bits_to_f32(read_mem32(_src + 0))
local _y = bits_to_f32(read_mem32(_src + 4))
local _z = bits_to_f32(read_mem32(_src + 8))
OBJECTS[S.NEXT_HANDLE] = Vector3.new(_x, _y, _z)
reg[11] = S.NEXT_HANDLE
S.NEXT_HANDLE = S.NEXT_HANDLE + 1
```

The bridge is fundamentally a **serialization/deserialization layer** — it copies data fields between paged memory and Roblox typed objects.

---

## 6. Memory Architecture

### 6.1 Paged Memory Model

The VM uses a paged memory system to emulate a flat 32-bit address space in Luau:

```lua
S.PAGES = {}                  -- page_index → buffer(65536)

function S.write_mem32(addr, val)
    local idx = bit32.rshift(addr, 16)       -- upper 16 bits → page index
    local offset = bit32.band(addr, 0xFFFF)  -- lower 16 bits → offset
    local page = S.PAGES[idx]
    if not page then
        page = buffer.create(65536)
        S.PAGES[idx] = page
    end
    buffer.writei32(page, offset, val)
end
```

Each page is 64KB (2^16 bytes). The address is split as:
```
[31:16] → page index   (up to 65536 possible pages = 4GB address space)
[15:0]  → offset within page
```

Pages are **demand-allocated**: writes allocate pages on first access, reads return 0 for unmapped pages.

### 6.2 Memory Layout

```
0x00000000 ─ null / unmapped (reads return 0)
    ...
0x80000000 ─ .text section start (code; first page of instruction memory)
0x80000000 + (512MB) ─ initial stack pointer (S.reg[3])
0x81000000 ─ HEAP_BRK (heap start)
    ...      ─ heap grows upward (max 512MB)
0xA0000000 ─ initial SP (top of address space)
```

### 6.3 Heap Allocator

The heap uses a best-fit strategy with coalescing through a `FREE_LIST`:

```lua
-- malloc:
for _addr, _fsize in pairs(FREE_LIST) do
    if _fsize >= _size then
        -- Use this free block (split if larger)
        FREE_LIST[_addr] = nil
        if _fsize > _size then
            FREE_LIST[_addr + _size] = _fsize - _size
        end
        ALLOCS[_addr] = _size
        return _addr
    end
end
-- No free block fits: bump HEAP_BRK
ALLOCS[S.HEAP_BRK] = _size
S.HEAP_BRK = S.HEAP_BRK + _size

-- free:
ALLOCS[_ptr] = nil
FREE_LIST[_ptr] = _size
```

`ALLOCS` tracks active allocations (for double-free detection and validation). `FREE_LIST` is a simple free-list — no merging of adjacent free blocks (a known limitation).

---

## 7. The Transpiler: How Handlers Are Generated

### 7.1 Pipeline Overview

```
output.asm (RISC-V disassembly)
    │
    ├─ metadata.py ── parses .rodata, function labels, enums
    ├─ asm_parser.py ── extracts instructions → (addr, mnemonic, args)
    │
    ├─ generator.py ── for each instruction:
    │   ├─ _track_state(): record register values at compile-time
    │   ├─ Detect instruction type (R-type, I-type, load, store, branch, etc.)
    │   └─ Generate Luau handler body via handler modules
    │
    ├─ blocks.py ── merge consecutive non-branching instructions
    │
    ├─ builders.py ── wrap handlers in chunk modules + shared state
    │
    └─ obfuscator.py ── mangle identifiers to random 1-2 char names
```

### 7.2 Compile-Time State Tracking

The key innovation in the generator is **compile-time register tracking**. A state machine walks through instructions and records what values are loaded into the argument registers:

```python
def _track_state(mnemonic, args, ...):
    """When an li/addi/lui writes to a0-a5 or a7, record the value."""
    if dest_reg in ["a7", "x17"]:
        tracked_a7_syscall = int(args[-1])    # syscall number
    elif dest_reg in ["a0", "x10"]:
        tracked_a0_literal = resolve_rodata_or_int(args)
    elif dest_reg in ["a1", "x11"]:
        tracked_a1_rodata_str = resolve_rodata_str(args)  # method name!
    # ... a2-a5: arguments
```

When an `ecall` is reached, the generator already knows the syscall number and what strings/values are in each argument register. This enables:
- **Method name resolution**: If `a1` contains a pointer to `"SetPrimaryPartCFrame"`, the transpiler generates a direct `_obj:SetPrimaryPartCFrame(...)` call
- **Service name resolution**: If `a2` contains `"Players"`, the service call can be specialized
- **Flag constant folding**: `a3` flags are parsed at transpile time, avoiding runtime bit-shifting

### 7.3 Instruction Handler Categories

| Handler File | Instructions | Example |
|-------------|-------------|---------|
| `alu.py` | `add, sub, mul, div, xor, and, or, sll, srl, sra, slt, sltu, ...` | `reg[5] = bit32.band(reg[3] + reg[4], 0xFFFFFFFF)` |
| `control.py` | `beq, bne, blt, bge, jal, jalr, lui, auipc` | Conditional branches → if/then/else with return targets |
| `float.py` | `fadd.s, fmul.s, fdiv.s, fsqrt.s, feq.s, fcvt.*, ...` | FP ops via `f32_to_bits`/`bits_to_f32` bridge |
| `memory.py` | `lw, sw, lb, sb, flw, fsw` | Paged memory reads/writes |
| `ecall/` | `ecall` (all syscalls) | Roblox API calls, memory ops, threading, struct bridge |

### 7.4 Handler Format

Every instruction becomes a closure stored by address:

```lua
S.HANDLERS[0x80000100] = function()
    -- Address: 0x80000100 (addi)
    reg[11] = bit32.band(reg[1] + 42, 0xFFFFFFFF)
    return 0x80000104    -- next PC
end
```

The while-loop dispatch in `run.luau` simply:
```lua
while PC and PC ~= 0 do
    local handler = S.HANDLERS[PC]
    if not handler then break end
    PC = handler()  -- returns next PC address
end
```

### 7.5 Block Merging Optimization

Sequential non-branching instructions are merged into a single closure:

```
BEFORE:                          AFTER:
HANDLERS[0x100] = function()     HANDLERS[0x100] = function()
    reg[5] = reg[5] + 1              reg[5] = reg[5] + 1
    return 0x104                     reg[6] = reg[5] * 2
end                                  reg[7] = reg[6] + reg[8]
HANDLERS[0x104] = function()         -- (return from last instruction kept)
    reg[6] = reg[5] * 2              return 0x10C
    return 0x108                 end
end
HANDLERS[0x108] = function()
    reg[7] = reg[6] + reg[8]
    return 0x10C
end
```

The final `return` from the last instruction is preserved; intermediate returns are stripped. This merges sequential operations into fewer dispatch cycles. Branch targets, ecall instructions, and jal/jalr targets break the chain (they must remain individually addressable).

**Tail merging** (currently disabled) goes further: when block A ends with `return <block_B_addr>` and block B has exactly one static predecessor, block B's code is inlined into A, eliminating a dispatch cycle.

---

## 8. Threading Model

### 8.1 taskSpawn (syscall 48)

Each spawned thread gets:
- Its own register table (`_threadReg = table.create(32, 0)`)
- Its own 64KB stack carved from the heap (`S.HEAP_BRK + 65536`)
- Arguments shifted: a1→a0, a2→a1, ..., a7→0
- `ra = 0` so the thread halts on return

```lua
task.spawn(function()
    S.dispatch_thread(_threadReg, _fnAddr)
    S.THREADS[_tid] = nil  -- thread finished
end)
```

### 8.2 dispatch_thread

Each thread calls `S.dispatch_thread()` which:
1. Copies `threadReg` into `S.reg` (owns the globals during timeslice)
2. Runs the standard while-loop dispatch
3. Syncs `S.reg` back to `threadReg` on exit

Because threads temporarily overwrite `S.reg`/`S.freg`, spawning code must save/restore registers before and after `task.spawn()`.

### 8.3 taskDefer (syscall 49)

Same mechanism as taskSpawn but uses `task.defer()` instead, scheduling execution for the next heartbeat.

---

## 9. Complete Syscall Reference

| # | Function | Args (a0-a6) | Returns (a0) |
|---|----------|-------------|-------------|
| 4 | print(str) | a0=str_ptr | — |
| 5 | print(int) | a0=int | — |
| 6 | print(bool) | a0=int | — |
| 7 | print(float) | a0=ptr | — |
| 21 | createBuffer | a0=size | a0=handle |
| 22 | freeBuffer | a0=handle | — |
| 23 | bufferLen | a0=handle | a0=len |
| 24 | bufferReadI8 | a0=handle, a1=offset | a0=val |
| 25 | bufferWriteI8 | a0=handle, a1=offset, a2=val | — |
| 26 | bufferReadI32 | a0=handle, a1=offset | a0=val |
| 27 | bufferWriteI32 | a0=handle, a1=offset, a2=val | — |
| 28 | bufferReadF32 | a0=handle, a1=offset | a0=bits |
| 29 | bufferWriteF32 | a0=handle, a1=offset, a2=bits | — |
| 30 | malloc | a0=size | a0=ptr |
| 31 | free | a0=ptr | — |
| 32 | heapUsed | — | a0=bytes |
| 39 | rad(deg) | a0=ptr→float | (in-place) |
| 40 | sin(x) | a0=ptr→float | (in-place) |
| 41 | cos(x) | a0=ptr→float | (in-place) |
| 46 | callMethod | a0=h, a1=method, a2=arg1, a3=flags, a4=arg2, a5=arg3, a6=arg4 | a0=result |
| 47 | getService | a0=name_ptr | a0=handle |
| 48 | taskSpawn | a0=fnAddr, a1-a6=args | a0=threadID |
| 49 | taskDefer | a0=fnAddr, a1-a6=args | — |
| 50 | bufferFromString | a0=str_ptr | a0=handle |
| 51 | getMethod | a0=handle, a1=name_ptr | a0=handle |
| 52 | getGlobal | a0=name_ptr | a0=handle |
| 53 | require | a0=handle | a0=handle |
| 54 | structReadVec3 | a0=objHandle, a1=destPtr | (writes to dest) |
| 55 | structWriteVec3 | a0=srcPtr | a0=handle |
| 56 | structReadCFrame | a0=objHandle, a1=destPtr | (writes to dest) |
| 57 | structWriteCFrame | a0=srcPtr | a0=handle |
| 58 | structReadColor3 | a0=objHandle, a1=destPtr | (writes to dest) |
| 59 | structWriteColor3 | a0=srcPtr | a0=handle |
| 60 | structReadUDim2 | a0=objHandle, a1=destPtr | (writes to dest) |
| 61 | structWriteUDim2 | a0=srcPtr | a0=handle |
| 62 | getPropertyObject | a0=handle, a1=name_ptr | a0=handle |
| 63 | setPropertyObject | a0=handle, a1=name_ptr, a2=valueHandle | — |
| 64 | releaseObject | a0=handle | — |

---

## 10. Data Flow Walkthrough: A Complete Example

Let's trace what happens when C++ code calls:

```cpp
Part p = Part::create();
p.setName("ObfuscatedPart");
```

### Step 1: `Part::create()`

The C++ expands to something like:
```cpp
LuaObj newPart = LuaObj::callMethodStatic("new", "Part", flags);
```
→ RISC-V: `li a0, "Part"` ; `li a1, "new"` ; `li a3, flags` ; `li a7, 46` ; `ecall`

The transpiler sees method name `"new"` (resolved from rodata), generates:
```lua
local _svc = Instance -- (getGlobal resolves to Instance)
local _r = _svc.new("Part")
OBJECTS[S.NEXT_HANDLE] = _r
reg[11] = S.NEXT_HANDLE
S.NEXT_HANDLE = S.NEXT_HANDLE + 1
return <next_pc>
```

### Step 2: `p.setName("ObfuscatedPart")`

C++: `p.callMethod("Name", "ObfuscatedPart", flags)`
→ RISC-V: `li a0, <p.handle>` ; `li a1, &"Name"` ; `li a2, &"ObfuscatedPart"` ; `li a3, flags` ; `li a7, 46` ; `ecall`

The transpiler resolves method name `"Name"`, generates:
```lua
local _obj = OBJECTS[reg[11]]
if _obj then
    _obj.Name = RODATA[reg[13]] or ""
end
return <next_pc>
```

---

## 11. Obfuscation Strategy

After generation, the obfuscator:
1. Scans all generated Luau for identifiers
2. Skips Lua keywords, Roblox globals, property/method names after `.` and `:`
3. Maps remaining identifiers to random 1-2 character names (prioritizing single chars first)
4. Replaces all occurrences across shared.luau, all chunks, and run.luau

This means the output has no meaningful variable names — every internal name like `_obj`, `_methodName`, `write_mem32` becomes a single random character like `a`, `b`, `X`, `z2`, etc.

---

## 12. Module Splitting

Handlers are split across multiple `chunk_N.luau` ModuleScripts (1000 handlers per chunk by default):

```
shared.luau   — S table (registers, memory, OBJECTS, helpers, etc.)
chunk_1.luau  — S.HANDLERS[0x80000000..0x80000FFF]
chunk_2.luau  — S.HANDLERS[0x80001000..0x80001FFF]
    ...
run.luau      — require() all chunks, run dispatch loop
```

Each chunk `require()`s `shared` to get the `S` table, populates handlers, and returns an init function. `run.luau` calls each chunk's init function, then starts the main dispatch loop at the entry address.
