# Object Architecture — cpp-luau-obfs

This document explains how the C++ → Luau object system works in detail, covering the full transformation pipeline from typed C++ classes down to obfuscated Luau handler closures.

---

## 1. The Three-Layer Architecture

The project operates across three distinct layers, each with its own execution model and object representation:

```
┌─────────────────────────────────────────────────────────┐
│  LAYER 1: C++ Source (compile-time)                      │
│  - Typed classes: LuaObj, Buffer, Vector3, CFrame, etc.  │
│  - Inline assembly ecall for every API boundary           │
│  - Pointers, templates, value semantics                   │
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

## 2. The Universal Handle API

### 2.1 Core Idea

**Everything is a handle.** There are no typed wrappers at runtime. Every C++ class or value that crosses the boundary gets stored in a single Luau table and identified by an integer:

```lua
S.OBJECTS = {}           -- integer handle → ANYTHING (Instance, Vector3, buffer, function, number, string, ...)
S.NEXT_HANDLE = 1        -- monotonically increasing counter
```

There is only one handle table — `S.OBJECTS`. Buffers, functions, primitives, and Roblox instances all live here. There is no `S.BUFFERS`, no separate buffer syscalls. One table, one counter, one API.

When C++ code calls `LuaObj::getService("Players")`, the flow is:

1. **C++ side:** `Rbxl::getService("Players")` emits `ecall` with `a7=47`, `a0=&"Players"`
2. **Luau handler:** runs `game:GetService("Players")`, stores result in `OBJECTS[S.NEXT_HANDLE]`, writes `S.NEXT_HANDLE` back to `reg[11]` (a0), increments `S.NEXT_HANDLE`
3. **C++ side:** the returned value flows back through a0 register into the `void* h` field

From that point on, every method call, property access, or lifecycle operation passes this integer handle to identify the target object.

### 2.2 Handle Tables

| Table | Key | Value | Purpose |
|-------|-----|-------|---------|
| `S.OBJECTS` | handle (int) | **Anything** — Instance, Vector3, buffer, function wrapper, number, string | **The one true handle table** |
| `S.RODATA` | address (int) | string | Read-only string literals from binary |
| `S.ENUMS` | enum index (int) | Roblox Enum value | Sparse enum cache |
| `S.ALLOCS` | address (int) | size (int) | Active heap allocations |
| `S.FREE_LIST` | address (int) | size (int) | Freed blocks available for reuse |
| `S.THREADS` | thread ID (int) | `{reg, pc}` table | Active spawned threads |
| `S._FUNC_WRAPPERS` | function address (int) | callable Luau function | C++→Luau callback wrappers |
| `S.SERVICE_HANDLES` | service name (string) | handle (int) | Cache for `getService()` lookups |

### 2.3 Handle Lifecycle

```
Creation — all types go through OBJECTS:
  getService()     → OBJECTS[NEXT_HANDLE] = game:GetService(name)
  getGlobal()      → OBJECTS[NEXT_HANDLE] = _G[name]
  getPropertyObject() → OBJECTS[NEXT_HANDLE] = obj[propName]
  toObject()       → OBJECTS[NEXT_HANDLE] = Vector3.new(x,y,z)  (structs)
  toObject()       → OBJECTS[NEXT_HANDLE] = buffer.create(size)  (buffers)
  fromFloat()      → OBJECTS[NEXT_HANDLE] = <number>             (primitives)
  fromInt()        → OBJECTS[NEXT_HANDLE] = <number>
  fromBool()       → OBJECTS[NEXT_HANDLE] = <boolean>
  fromString()     → OBJECTS[NEXT_HANDLE] = <string>
  fromEnum()       → OBJECTS[NEXT_HANDLE] = <EnumItem>
  fromFunction()   → OBJECTS[NEXT_HANDLE] = S.get_function(addr) (callbacks)
  clone()          → OBJECTS[NEXT_HANDLE] = obj:Clone()
  require()        → OBJECTS[NEXT_HANDLE] = require(module)

Destruction:
  releaseObject()  → OBJECTS[handle] = nil          (syscall 64)
  destroy()        → OBJECTS[handle]:Destroy(); OBJECTS[handle] = nil

Collision safety:
  NEXT_HANDLE is monotonically increasing. Handles are never reused, even
  after releaseObject(). This prevents dangling-handle bugs where a stale
  handle could point to a new, unrelated object.
```

### 2.4 A Universal API

The entire system converges on a single primitive operation: **look up a handle in OBJECTS and call a method on it**. This is encapsulated in syscall 65 (`call()`):

```
Everything is:
  1. Created and stored in OBJECTS → returns a handle (integer)
  2. Passed through method call arguments as a handle
  3. Looked up via OBJECTS[handle] at call time
  4. Released by removing from OBJECTS when done
```

Types that live in OBJECTS:
- Roblox Instances (Parts, Scripts, Services, etc.)
- Roblox data types (Vector3, CFrame, Color3, UDim2)
- Luau `buffer` objects (binary data)
- Primitive values (numbers, booleans, strings)
- Enum items
- Function wrappers (C++ callbacks exposed to Luau)

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

    // Generic method call (syscall 65)
    template<typename... Args>
    void* callMethod(const char* methodName, Args... args, int flags);

    template<typename... Args>
    void* callMethodStatic(const char* methodName, Args... args, int flags);

    // Primitive conversions (syscalls 66-73)
    static LuaObj fromFloat(float f);
    static LuaObj fromInt(int i);
    static LuaObj fromBool(bool b);
    static LuaObj fromString(const char* s);
    static LuaObj fromFunction(void* funcAddr);  // syscall 74
    float toFloat() const;
    int toInt() const;
    bool toBool() const;
    const char* toString() const;

    // Enum conversions (syscalls 42-43)
    static LuaObj fromEnum(int enumIndex);
    int toEnum() const;

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

### 3.3 Primitive Conversions

Functions like `LuaObj::fromFloat()` use dedicated syscall numbers (66-73). The transpiler detects them both by syscall number and by **function name**:

```python
# In ecall/__init__.py:
is_from_float = current_func and "fromFloat" in current_func
if is_from_float or tracked_a7_syscall == 66:
    emit_from_float(handler_body)  # Wraps float bits into OBJECTS
```

This dual detection (syscall number + function name) prevents silent failure when the compiler inlines these small inline-asm functions.

---

## 4. Method Call Architecture

### 4.1 Two Call Paths

There are two parallel call paths, selected by the caller:

| Path | Syscall | C++ function | Used by |
|------|---------|-------------|---------|
| **Payload stack** | 75 | `Rbxl::callObj()` / `LuaObj::callObj()` | All non-Buffer calls (Instances, services, modules) |
| **Register-based** | 65 | `Rbxl::call()` | Buffer operations only (raw int passthrough) |

The payload path is the primary API. The register path is retained solely for Buffer operations that pass raw integer arguments that cannot be OBJECTS handles.

### 4.2 Payload Stack Call (syscall 75)

All args are **OBJECTS handles** — no raw ints, no strings, no function addresses. Self-prepend for `callMethod` is handled by including `this->h` as the first user arg.

**Payload format** (stack-local struct, passed by pointer in a0):

```
┌────────────────────────┐
│  word 0: header         │  = (handleCount << 16) | (flags & 0xFFFF)
│  word 1: fn handle      │  = OBJECTS index of the function/method
│  word 2: arg 0 handle   │  = OBJECTS index of first argument
│  ...                    │
│  word N+1: arg N handle │
└────────────────────────┘

handleCount = number of USER args (NOT including fn handle)
flags       = return type flags (bits 0-1 only)
```

**C++ side** — `Rbxl::callObj()` templates (0-5 args):

```cpp
template<typename A1>
void* callObj(void* fnHandle, int flags, const A1& a1) {
    struct _Payload1 { unsigned int header; void* fn; void* a[1]; };
    _Payload1 _p;
    _p.header = (1 << 16) | (flags & 0xFFFF);  // count = 1 user arg
    _p.fn = fnHandle;
    _p.a[0] = _obj_handle(a1);  // extracts void* from LuaObj or passes void* through

    void* result;
    asm volatile("mv a0, %1; li a7, 75; ecall; mv %0, a0"
        : "=r"(result) : "r"(&_p) : "a0", "a7", "memory");
    return result;
}
```

The `_obj_handle()` helper automatically extracts `void*` from `LuaObj` arguments or passes `void*` through unchanged.

**Luau handler** (syscall 75):

```lua
local _payload = reg[11]                              -- a0 = pointer to payload
local _header = read_mem32(_payload)                  -- word 0
local _handleCount = bit32.rshift(_header, 16)        -- number of user args
local _flags = bit32.band(_header, 0xFFFF)            -- return type flags

local _fn = OBJECTS[read_mem32(_payload + 4)]        -- word 1 = fn handle

local _args = {}
for _i = 0, _handleCount - 1 do                       -- words 2..N+1 = arg handles
    local _h = read_mem32(_payload + 8 + _i * 4)
    _args[_i + 1] = OBJECTS[_h]
end

local _hasReturn = bit32.band(_flags, 1) ~= 0
local _returnIsObj = bit32.band(_flags, 2) ~= 0

if _hasReturn then
    local _r = _fn(table.unpack(_args))
    if _returnIsObj then
        OBJECTS[S.NEXT_HANDLE] = _r; reg[11] = S.NEXT_HANDLE; S.NEXT_HANDLE += 1
    else
        reg[11] = _r or 0
    end
else
    _fn(table.unpack(_args))
end
```

**Key properties:**
- **No sentinel guards** — the count in the header tells the handler exactly how many args to read
- **No arg-type flags** — every arg is an OBJECTS handle, no bit-twiddling needed
- **No self-prepend flag** — `callMethod` simply includes `this->h` as the first user arg
- **N-arg ready** — the payload layout naturally supports any number of args

### 4.3 Register-Based Call (syscall 65) — Buffer Only

The original register-based path remains for Buffer operations that pass raw integers:

```
a0 (reg[11]) = callable handle
a1 (reg[12]) = arg 1
a2 (reg[13]) = arg 2
a3 (reg[14]) = flags
a4 (reg[15]) = arg 3
a5 (reg[16]) = arg 4
a6 (reg[17]) = arg 5
```

Buffer code calls `Rbxl::call()` directly (bypassing `LuaObj::callMethodStatic()`):

```cpp
// Buffer::readFromObject:
Rbxl::call(
    bufferLib.getPropertyObject("len").handle(),  // method handle
    objHandle,                                      // arg1 (OBJECTS handle)
    RBXL_METHOD_ARG_1_IS_OBJECT_BIT | RBXL_METHOD_HAS_RETURN_BIT
);

// Buffer::toObject:
Rbxl::call(
    bufferLib.getPropertyObject("writei8").handle(),
    handle, (int)i, (int)data[i],                   // raw int args!
    RBXL_METHOD_ARG_1_IS_OBJECT_BIT
);
```

The syscall 65 handler continues to use the full flag system for arg-type resolution and sentinel guards for unused register slots. This complexity is contained entirely within the Buffer codepath.

### 4.4 API Surface

**`LuaObj` methods for non-Buffer callers:**

```cpp
// Direct call: this->h IS the function handle
obj.callObj(flags)                 // 0 args
obj.callObj(flags, a1)             // 1 arg

// Legacy .call() wrapper (flags-last, delegates to callObj)
obj.call(flags)                    // 0 args
obj.call(a1, flags)                // 1 arg

// Method call: prepends self (this->h) automatically
obj.callMethod("MethodName", flags)       // 0 user args
obj.callMethod("MethodName", flags, a1)   // 1 user arg

// Static method call: no self prepend
obj.callMethodStatic("MethodName", flags)       // 0 user args
obj.callMethodStatic("MethodName", flags, a1)   // 1 user arg
```

Note: `callMethod`/`callMethodStatic` use **flags-first** API. The legacy `.call()` keeps flags-last for backward compatibility.

### 4.5 Function Pointer Wrappers

Functions are stored in OBJECTS via `LuaObj::fromFunction(void* funcAddr)` (syscall 74), which wraps the C++ address in a callable Luau closure and returns a handle. This handle can then be passed through the payload-stack call path just like any other OBJECTS handle.

---

## 5. Buffer Struct — No Buffer Syscalls

### 5.1 Design

The `Buffer` struct replaces the old buffer syscalls (21-29, 50) entirely. It uses only the universal handle API (`getGlobal("buffer")` + `callMethodStatic`) to bridge between C++ `uint8_t` arrays and Roblox `buffer` objects:

```cpp
struct Buffer {
    static const int MAX_SIZE = 65536;  // 64KB
    uint8_t data[MAX_SIZE];
    unsigned int size;

    Buffer() : size(0) {}

    // Read a Roblox buffer object (from OBJECTS) into this C++ array
    void readFromObject(void* objHandle) {
        LuaObj bufferLib = LuaObj::getGlobal("buffer");
        unsigned int len = (unsigned int)(unsigned long)bufferLib.callMethodStatic(
            "len", objHandle,
            RBXL_METHOD_ARG_1_IS_OBJECT_BIT | RBXL_METHOD_HAS_RETURN_BIT
        );
        size = len < MAX_SIZE ? len : MAX_SIZE;
        for (unsigned int i = 0; i < size; i++) {
            int val = (int)(unsigned long)bufferLib.callMethodStatic(
                "readi8", objHandle, (int)i,
                RBXL_METHOD_ARG_1_IS_OBJECT_BIT | RBXL_METHOD_HAS_RETURN_BIT
            );
            data[i] = (uint8_t)val;
        }
        bufferLib.release();
    }

    // Write this C++ array into a new Roblox buffer, store in OBJECTS, return handle
    void* toObject() const {
        LuaObj bufferLib = LuaObj::getGlobal("buffer");
        void* handle = bufferLib.callMethodStatic(
            "create", (int)size,
            RBXL_METHOD_HAS_RETURN_BIT | RBXL_METHOD_RETURN_IS_OBJ_BIT
        );
        for (unsigned int i = 0; i < size; i++) {
            bufferLib.callMethodStatic(
                "writei8", handle, (int)i, (int)data[i],
                RBXL_METHOD_ARG_1_IS_OBJECT_BIT
            );
        }
        bufferLib.release();
        return handle;
    }
};
```

### 5.2 No Buffer Syscalls

The old `Rbxl::createBuffer()`, `Rbxl::freeBuffer()`, `Rbxl::bufferReadI8()`, etc. have been completely removed. The `S.BUFFERS` table no longer exists. Buffer objects created via `Buffer::toObject()` are stored in `S.OBJECTS` just like everything else.

---

## 6. Struct Bridge (syscalls 54-61)

### 6.1 The Problem

C++ types like `Vector3`, `CFrame`, `Color3`, and `UDim2` exist as **plain memory** in the paged VM. But Roblox APIs expect native Luau types (`Vector3.new()`, `CFrame.new()`, etc.). The struct bridge translates between these two worlds.

### 6.2 Bridge Operations

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

### 6.3 C++ Side Implementation

Each struct has two bridge methods implemented with inline assembly:

```cpp
struct Vector3 {
    float x, y, z;

    void readFromObject(void* objHandle) {
        asm volatile (
            "mv a0, %0; mv a1, %1; li a7, 54; ecall"
            : : "r"(objHandle), "r"(this)
            : "a0", "a1", "a7", "memory"
        );
    }

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

### 6.4 Luau Side Implementation

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

---

## 7. Memory Architecture

### 7.1 Paged Memory Model

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

### 7.2 Memory Layout

```
0x00000000 ─ null / unmapped (reads return 0)
    ...
0x80000000 ─ .text section start (code; first page of instruction memory)
0x80000000 + (512MB) ─ initial stack pointer (S.reg[3])
0x81000000 ─ HEAP_BRK (heap start)
    ...      ─ heap grows upward (max 512MB)
0xA0000000 ─ initial SP (top of address space)
```

### 7.3 Heap Allocator

The heap uses a best-fit strategy with coalescing through a `FREE_LIST`:

```lua
-- malloc:
for _addr, _fsize in pairs(FREE_LIST) do
    if _fsize >= _size then
        FREE_LIST[_addr] = nil
        if _fsize > _size then
            FREE_LIST[_addr + _size] = _fsize - _size
        end
        ALLOCS[_addr] = _size
        return _addr
    end
end
ALLOCS[S.HEAP_BRK] = _size
S.HEAP_BRK = S.HEAP_BRK + _size

-- free:
ALLOCS[_ptr] = nil
FREE_LIST[_ptr] = _size
```

`ALLOCS` tracks active allocations (for double-free detection and validation). `FREE_LIST` is a simple free-list — no merging of adjacent free blocks (a known limitation).

---

## 8. The Transpiler: How Handlers Are Generated

### 8.1 Pipeline Overview

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

### 8.2 Compile-Time State Tracking

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
    # ...
```

When an `ecall` is reached, the generator already knows the syscall number and what strings/values are in each argument register. This enables:
- **Method name resolution**: If `a1` contains a pointer to `"SetPrimaryPartCFrame"`, the transpiler generates a direct `_obj:SetPrimaryPartCFrame(...)` call
- **Service name resolution**: If `a2` contains `"Players"`, the service call can be specialized
- **Flag constant folding**: `a3` flags are parsed at transpile time, avoiding runtime bit-shifting

### 8.3 Instruction Handler Categories

| Handler File | Instructions | Example |
|-------------|-------------|---------|
| `alu.py` | `add, sub, mul, div, xor, and, or, sll, srl, sra, slt, sltu, ...` | `reg[5] = bit32.band(reg[3] + reg[4], 0xFFFFFFFF)` |
| `control.py` | `beq, bne, blt, bge, jal, jalr, lui, auipc` | Conditional branches → if/then/else with return targets |
| `float.py` | `fadd.s, fmul.s, fdiv.s, fsqrt.s, feq.s, fcvt.*, ...` | FP ops via `f32_to_bits`/`bits_to_f32` bridge |
| `memory.py` | `lw, sw, lb, sb, flw, fsw` | Paged memory reads/writes |
| `ecall/` | `ecall` (all syscalls) | Roblox API calls, memory ops, threading, struct bridge |

### 8.4 Handler Format

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

### 8.5 Block Merging Optimization

Sequential non-branching instructions are merged into a single closure:

```
BEFORE:                          AFTER:
HANDLERS[0x100] = function()     HANDLERS[0x100] = function()
    reg[5] = reg[5] + 1              reg[5] = reg[5] + 1
    return 0x104                     reg[6] = reg[5] * 2
end                                  reg[7] = reg[6] + reg[8]
HANDLERS[0x104] = function()         return 0x10C
    reg[6] = reg[5] * 2          end
    return 0x108
end
HANDLERS[0x108] = function()
    reg[7] = reg[6] + reg[8]
    return 0x10C
end
```

The final `return` from the last instruction is preserved; intermediate returns are stripped.

---

## 9. Threading Model

### 9.1 taskSpawn (syscall 48)

Each spawned thread gets:
- Its own register table (`_threadReg = table.create(32, 0)`)
- Its own 64KB stack carved from the heap (`S.HEAP_BRK + 65536`)
- Arguments shifted: a1→a0, a2→a1, ..., a7→0
- `ra = 0` so the thread halts on return

```lua
task.spawn(function()
    S.dispatch_thread(_threadReg, _fnAddr)
    S.THREADS[_tid] = nil
end)
```

### 9.2 dispatch_thread with Yield Protection

Each thread calls `S.dispatch_thread()` which runs a dispatch loop with isolated registers and yield detection:

```lua
function S.dispatch_thread(threadReg, startPC)
    local _threadFreg = table.create(32, 0)
    local _pc = startPC
    while _pc and _pc ~= 0 do
        -- Restore thread's registers before each instruction
        for _i = 1, 32 do
            S.reg[_i] = threadReg[_i]
            S.freg[_i] = _threadFreg[_i]
        end
        local _handler = S.HANDLERS[_pc]
        if not _handler then break end

        -- Bump generation counter, snapshot for yield detection
        S._vm_gen = S._vm_gen + 1
        local _myGen = S._vm_gen
        _pc = _handler()

        -- Only save if no other thread ran during our handler
        if S._vm_gen == _myGen then
            for _i = 1, 32 do
                threadReg[_i] = S.reg[_i]
                _threadFreg[_i] = S.freg[_i]
            end
        end
    end
end
```

The `S._vm_gen` generation counter prevents yield-corrupted register saves:
- Before each handler call: `S._vm_gen` is bumped, a snapshot is saved
- If the handler yields (e.g., `task.wait()`), another thread may enter dispatch, bumping `_vm_gen` further
- After the handler returns: if `_vm_gen` changed, the save is skipped because `S.reg` was corrupted during the yield

### 9.3 Main Dispatch Loop Protection

The main dispatch loop in `run.luau` uses the same `_vm_gen`-based yield protection pattern, maintaining its own `_mainReg`/`_mainFreg` backup tables:

```lua
while PC and PC ~= 0 do
    -- Restore main thread registers before each instruction
    for _i = 1, 32 do
        S.reg[_i] = _mainReg[_i]
        S.freg[_i] = _mainFreg[_i]
    end

    local _preGen = S._vm_gen
    PC = handler()

    -- Only save if no other thread ran
    if S._vm_gen == _preGen then
        for _i = 1, 32 do
            _mainReg[_i] = S.reg[_i]
            _mainFreg[_i] = S.freg[_i]
        end
    end
end
```

### 9.4 taskDefer (syscall 49)

Same mechanism as taskSpawn but uses `task.defer()` instead, scheduling execution for the next heartbeat.

---

## 10. Complete Syscall Reference

| # | Function | Args (a0-a6) | Returns (a0) |
|---|----------|-------------|-------------|
| 4 | print(str) | a0=str_ptr | — |
| 5 | print(int) | a0=int | — |
| 6 | print(bool) | a0=int | — |
| 7 | print(float) | a0=ptr | — |
| 30 | malloc | a0=size | a0=ptr |
| 31 | free | a0=ptr | — |
| 32 | heapUsed | — | a0=bytes |
| 39 | rad(deg) | a0=ptr→float | (in-place) |
| 40 | sin(x) | a0=ptr→float | (in-place) |
| 41 | cos(x) | a0=ptr→float | (in-place) |
| 42 | fromEnum | a0=enumIndex | a0=handle |
| 43 | toEnum | a0=handle | a0=index |
| 46 | callMethod (legacy) | a0=h, a1=method, a2=arg1, a3=flags, a4=arg2, a5=arg3, a6=arg4 | a0=result |
| 47 | getService | a0=name_ptr | a0=handle |
| 48 | taskSpawn | a0=fnAddr, a1-a6=args | a0=threadID |
| 49 | taskDefer | a0=fnAddr, a1-a6=args | — |
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
| 65 | call (register) | a0=handle, a1=arg1, a2=arg2, a3=flags, a4=arg3, a5=arg4, a6=arg5 | a0=result |
| 66 | fromFloat | a0=float | a0=handle |
| 67 | fromInt | a0=int | a0=handle |
| 68 | fromBool | a0=int(bool) | a0=handle |
| 69 | fromString | a0=str_ptr | a0=handle |
| 70 | toFloat | a0=handle | a0=float |
| 71 | toInt | a0=handle | a0=int |
| 72 | toBool | a0=handle | a0=int(bool) |
| 73 | toString | a0=handle | a0=str_ptr |
| 74 | fromFunction | a0=funcAddr | a0=handle |
| **75** | **callObj (payload)** | **a0=payloadPtr → {header, fn, args...}** | **a0=result** |
| 67 | fromInt | a0=int | a0=handle |
| 68 | fromBool | a0=int(bool) | a0=handle |
| 69 | fromString | a0=str_ptr | a0=handle |
| 70 | toFloat | a0=handle | a0=float |
| 71 | toInt | a0=handle | a0=int |
| 72 | toBool | a0=handle | a0=int(bool) |
| 73 | toString | a0=handle | a0=str_ptr |
| 74 | **fromFunction** | a0=funcAddr | a0=handle |

> **Removed syscalls:** 21-29 (buffer operations) and 50 (bufferFromString) — buffers now use the universal handle API via `Buffer` struct + syscall 65.

---

## 11. Obfuscation Strategy

After generation, the obfuscator:
1. Scans all generated Luau for identifiers
2. Skips Lua keywords, Roblox globals, property/method names after `.` and `:`
3. Maps remaining identifiers to random 1-2 character names (prioritizing single chars first)
4. Replaces all occurrences across shared.luau, all chunks, and run.luau

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
