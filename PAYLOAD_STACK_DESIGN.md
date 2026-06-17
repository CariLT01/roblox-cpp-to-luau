# Payload Stack — N-arg syscall 65 (Design)

## Problem

The current syscall 65 (`call()`) uses 5 RISC-V registers (a1-a6) to pass arguments. This limits calls to
**0-5 extra args** and requires:

-   **6 template overloads** in `Rbxl::call` (0-arg through 5-arg)
-   **~30 LuaObj-aware overloads** to extract handles pre-asm
-   **Sentinel guards** (`4294967295`) to skip template-zeroed registers in fewer-arg calls
-   **Bit-twiddling per arg position** in the Luau handler

All of this complexity exists solely because we're multiplexing register slots.

## Solution

A single bump-allocated "payload stack" per VM thread. Instead of passing args in registers,
we write them sequentially into a pre-allocated memory buffer and pass one pointer. The
"allocation" is just advancing a pointer; "free" is subtracting from it.

### Payload format

```
┌──────────────────────┐  ← _payloadBase (fixed, 8KB buffer per thread)
│  header: count<<16|flags │  ← _payloadSP starts here
│  handle[0] = fn/method  │  ← OBJECTS handle for the callable
│  handle[1] = arg1       │
│  ...                    │
│  handle[N] = argN       │
└──────────────────────┘

header layout:
  bits [31:16] = arg_count   (number of handles after fn, 0-65535)
  bits [15:0]  = flags       (return type bits: HAS_RETURN, RETURN_IS_OBJ, etc.)

ALL values are OBJECTS handles. No raw ints, no RODATA strings, no function addresses.
Everything is pre-converted to a handle before the call.
```

### C++ side — single variadic `call()`

```cpp
// One template replaces all 0-5 arg overloads
template<typename... Args>
void* call(void* fnHandle, int flags, const Args&... args) {
    // "Allocate" on payload stack: header + fn + N args
    int count = sizeof...(args);                    // N user args
    int* sp = (int*)_payloadSP;                     // current SP
    sp[0] = (count << 16) | (flags & 0xFFFF);       // header
    sp[1] = (int)(unsigned long)fnHandle;            // fn/method handle
    int* p = sp + 2;
    // Fold: for each arg, extract handle and write
    (void)(int[]){ (*(p++) = (int)(unsigned long)extractHandle(args), 0)... };

    void* result;
    asm volatile("mv a0, %1; li a7, 65; ecall; mv %0, a0"
        : "=r"(result) : "r"(_payloadBase) : "a0", "a7");

    _payloadSP = (uint8_t*)_payloadBase;  // "free" — reset to base
    return result;
}
```

`extractHandle()` returns `void*` for `LuaObj` (via `.handle()`) and passes `void*` through
unchanged for raw handles. The fold expression writes each handle sequentially.

For `callMethod` (self-prepend): the count includes `this->h` at index 0 automatically.
No special flag needed — the Luau handler doesn't distinguish method calls from static calls.

### Luau side — simple loop

```lua
-- Syscall 65: payload-based call
local _payloadAddr = reg[11]
local _header = read_mem32(_payloadAddr)
local _argCount = bit32.rshift(_header, 16)
local _flags = bit32.band(_header, 0xFFFF)

local _fnOffset = _payloadAddr + 4
local _fn = OBJECTS[read_mem32(_fnOffset)]

local _args = {}
for _i = 0, _argCount - 1 do
    local _handle = read_mem32(_payloadAddr + 8 + _i * 4)
    _args[_i + 1] = OBJECTS[_handle]
end

local _hasReturn = bit32.band(_flags, 1) ~= 0
local _returnIsObj = bit32.band(_flags, 2) ~= 0

if _hasReturn then
    local _r = _fn(table.unpack(_args))
    if _returnIsObj then
        if _r then OBJECTS[S.NEXT_HANDLE] = _r; reg[11] = S.NEXT_HANDLE; S.NEXT_HANDLE = S.NEXT_HANDLE + 1
        else reg[11] = 0 end
    else
        reg[11] = _r or 0
    end
else
    _fn(table.unpack(_args))
end
```

No per-position flag bit-twiddling. No sentinel guards. Just a header read + loop.

### What goes away

| Removed | Lines saved |
|---------|------------|
| 0-5 arg `Rbxl::call` templates | ~100 |
| ~30 LuaObj-aware overloads in `Rbxl::` namespace | ~120 |
| `_argNIsFn`/`_argNIsHandle`/`_argNIsStr` per-position flags | ~40 |
| Sentinel guards (`if reg[N] ~= 4294967295`) | ~8 |
| `_selfPrepended` branch — method calls just prepend handle at index 0 | ~30 |
| `IS_STATIC_BIT`, `IS_SELF_BIT`, `IS_FUNCTION_BIT`, `IS_STRING_BIT` flags | — |

Total: **~300 lines removed** from the syscall 65 handler and Rbxl namespace.

### What stays the same

-   **Buffer operations** (`writei8`/`readi8`/`len`/`create`) — keep current register path
-   **All other syscalls** (62-64, 66-74, etc.) — unchanged
-   **`main_image.cpp` call sites** — already pass OBJECTS handles, no changes needed
-   **Primitive conversions** (fromFloat/fromInt/fromString) — unchanged

### Implementation plan

1.  **`builders.py`** — add `S._payloadBase` (8KB buffer) and `S._payloadSP` to shared.luau
2.  **`rbxl.hpp`** — replace 0-5 arg `Rbxl::call` templates with single variadic version;
    remove all LuaObj-aware overloads in `Rbxl::` namespace
3.  **`rbxl.hpp`** — update `LuaObj::call`/`callMethod`/`callMethodStatic` to use new API
4.  **`ecall/__init__.py`** — replace syscall 65 handler with payload-based loop
5.  **`main_image.cpp`** — verify no changes needed (all args are already OBJECTS handles)
6.  **`base64.hpp`** — *no changes* (Buffer keeps register path)
7.  **Compile, transpile, review, test**
