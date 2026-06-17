# cpp-luau-obfs

> **⚠️ Experimental** — This project is a work in progress.

An obfuscation pipeline for Roblox that lets you write your logic in **C++** instead of Luau. Your C++ code gets compiled to a RISC-V virtual machine embedded in Luau — the output is a tangle of opaque closures, integer bit-manipulation, and paged memory access that bears no resemblance to the original source.

## How It Works

```
C++ Source  →  RISC-V Cross-Compile  →  Disassembly  →  Python Transpiler  →  Obfuscated Luau
```

1. **Compile** — Your C++ is cross-compiled to RISC-V machine code using `riscv-none-elf-g++`
2. **Disassemble** — The binary is disassembled to text assembly via `objdump`
3. **Transpile** — A Python transpiler converts the assembly into Luau handler functions that emulate a RISC-V CPU
4. **Minify** — Identifiers are mangled to random short names, comments are stripped, output is minified and split into ModuleScripts

## Features

- Write game logic in C++ with classes, templates, pointers, and smart pointers
- Cross-compile to RISC-V and transpile to obfuscated Luau
- Inter-op with existing Luau via `require()` and Roblox bindings via method calls
- Bundle multiple source files into a single output
- Aggressive compiler optimizations make reconstructing original source extremely difficult
- Paged memory emulation, register-based dispatch, identifier mangling, block merging

## Quick Start

### Prerequisites

- **RISC-V GCC toolchain** at `C:\riscv-gcc\` (or update the path in `pipeline/compile.bat`)
- **Python 3.10+**
- **Roblox Studio**

### Build

```bat
build.bat
```

Options:

```bat
pipeline/compile.bat                    # Server mode (default)
pipeline/compile.bat client             # Client mode
pipeline/compile.bat --validate         # Enable runtime memory validation
pipeline/compile.bat client --validate  # Both
```

The output goes to `dist/` — minified `.lua` files ready to drop into Roblox Studio.

## Writing C++ Code

Place your source files in `src/`. The entry point is `main()`:

```cpp
#include "lib/rbxl.hpp"

int main() {
    LuaObj task = LuaObj::getGlobal("task");
    LuaObj instance = LuaObj::getGlobal("Instance");
    LuaObj partStr = LuaObj::fromString("Part");
    LuaObj workspace = LuaObj::getService("Workspace");

    // Create a Part
    LuaObj part = instance.callMethodStatic("new",
        RBXL_METHOD_ARG_1_IS_OBJECT_BIT | RBXL_METHOD_HAS_RETURN_BIT | RBXL_METHOD_RETURN_IS_OBJ_BIT,
        partStr);

    // Set properties
    part.setPropertyObject("Name", LuaObj::fromString("ObfuscatedPart"));
    part.setPropertyObject("Anchored", LuaObj::fromBool(true));

    Vector3 pos(0.0f, 10.0f, 0.0f);
    part.setPropertyObject("Position", LuaObj::fromHandle(pos.toObject()));
    part.setPropertyObject("Parent", workspace);

    return 0;
}
```

## API Reference

### The Universal Handle API

Everything is a handle — an integer index into `S.OBJECTS`, a single Luau table that stores Roblox Instances, Vector3s, CFrames, buffers, primitives, and function wrappers. Every handle is released automatically via RAII.

### LuaObj — Core Handle Class

```cpp
LuaObj()                    // Null handle
LuaObj(void* handle)        // Wrap a raw handle (takes ownership)
obj.handle()                // Extract raw void* handle
obj.valid()                 // Check if handle is non-null
obj.release()               // Explicitly release (destructor handles auto-release)
```

### Method Calls (flags-first API)

```cpp
// Static call (. syntax, no self): instance.new("Part")
obj.callMethodStatic("MethodName", flags, args...)

// Method call (: syntax, self prepended): part:Destroy()
obj.callMethod("MethodName", flags, args...)

// Direct call: this IS the function handle
obj.callObj(flags, args...)
obj.call(flags)             // Legacy flags-last API, delegates to callObj
obj.call(args..., flags)    // Legacy flags-last (deprecated, use callMethodStatic)
```

**Example:**

```cpp
// Create a Part
LuaObj part = instance.callMethodStatic("new",
    RBXL_METHOD_ARG_1_IS_OBJECT_BIT | RBXL_METHOD_HAS_RETURN_BIT | RBXL_METHOD_RETURN_IS_OBJ_BIT,
    partStr);

// Connect to an event
LuaObj touchedEvent = baseplate.getMethod("Touched");
touchedEvent.callMethod("Connect", RBXL_METHOD_ARG_1_IS_OBJECT_BIT, callbackHandle);

// Call a module function
module.callMethodStatic("Hello", 0);
```

### Property Access

```cpp
LuaObj obj.getPropertyObject("PropertyName")     // Returns any property as a handle
obj.setPropertyObject("PropertyName", value)     // Sets a property from a handle
obj.getMethod("MethodName")                      // Get an event/signal (e.g. "Touched")
```

### Service & Global Lookups

```cpp
LuaObj::getService("ServiceName")     // e.g. "Workspace", "Players", "ReplicatedStorage"
LuaObj::getGlobal("GlobalName")       // e.g. "Instance", "require", "game"
obj.require()                         // Require a ModuleScript
```

### Primitive Conversions (syscalls 66-73)

```cpp
LuaObj::fromFloat(f)     // float → handle
LuaObj::fromInt(i)       // int → handle
LuaObj::fromBool(b)      // bool → handle
LuaObj::fromString(s)    // const char* → handle
LuaObj::fromFunction(fn) // C++ function ptr → callable handle (syscall 74)
LuaObj::fromEnum(idx)    // enum index → handle

obj.toFloat()            // handle → float
obj.toInt()              // handle → int
obj.toBool()             // handle → bool
obj.toString()           // handle → const char*
obj.toEnum()             // handle → enum index
```

### Struct Bridge (syscalls 54-61)

C++ structs ↔ Roblox data types via `readFromObject` / `toObject`:

| Struct | C++ Layout | Roblox Type |
|--------|-----------|-------------|
| `Vector3` | 3× float | `Vector3.new(x, y, z)` |
| `CFrame` | 12× float | `CFrame.new(...)` |
| `Color3` | 3× float | `Color3.new(r, g, b)` |
| `UDim2` | 4× float | `UDim2.new(xs, xo, ys, yo)` |

```cpp
Vector3 v(1.0f, 2.0f, 3.0f);
void* handle = v.toObject();           // C++ struct → OBJECTS handle
LuaObj obj = LuaObj::fromHandle(handle);

Vector3 v2;
v2.readFromObject(obj.handle());       // OBJECTS handle → C++ struct
```

### Buffer (byte arrays)

The `Buffer` struct bridges C++ `uint8_t` arrays ↔ Roblox `buffer` objects. No dedicated buffer syscalls — uses the register-based call path (syscall 65) for raw integer passthrough.

```cpp
Buffer buf;
buf.data[buf.size++] = ...;           // Fill with bytes
void* handle = buf.toObject();        // → OBJECTS handle

Buffer decoded;
decoded.readFromObject(handle);       // OBJECTS handle → C++ uint8_t array
// decoded.data[0..len-1], decoded.size
```

### Memory

```cpp
void* ptr = Rbxl::malloc(size);       // Allocate on virtual heap
Rbxl::free(ptr);                      // Free allocation
int used = Rbxl::heapUsed();          // Bytes allocated
```

### Threading

```cpp
Lua::taskSpawn(funcAddr, args...);    // Spawn a new thread
Lua::taskDefer(funcAddr, args...);    // Defer to next heartbeat
Lua::print(val);                      // Print int, bool, float, or string
```

### Math

```cpp
float rad = math::rad(90.0f);         // Degrees → radians
float s = math::sin(rad);             // Sine
float c = math::cos(rad);             // Cosine
```

### C++ Data Structures

The freestanding environment includes: `vector<T>`, `map<K,V>`, `unique_ptr<T>`, `shared_ptr<T>`, `make_unique<T>()`, `make_shared<T>()`.

### CFrame Operations

```cpp
CFrame(posX, posY, posZ)
CFrame(posX, posY, posZ, r00, r01, r02, r10, r11, r12, r20, r21, r22)
cframe_lookAt(pos, target)
cframe_mul(a, b)
cframe_inverse(cf)
cframe_fromEulerAngles(rx, ry, rz)
cframe_pointToWorld(cf, v)
cframe_pointToObject(cf, v)
cframe_vectorToWorld(cf, v)
cframe_vectorToObject(cf, v)
```

## Architecture

### Two Call Paths

| Path | Syscall | Used by | Args |
|------|---------|---------|------|
| **Payload stack** | 75 | All non-Buffer calls | OBJECTS handles only, any count |
| **Register-based** | 65 | Buffer operations only | Raw ints + handles, up to 5 args |

The payload path (syscall 75) writes `(count, fn_handle, args...)` to a stack-local buffer and passes one pointer. The Luau handler reads the count from the header and loops over OBJECTS handles. No sentinel guards, no arg-type flag bit-twiddling.

Buffer operations use the register path (syscall 65) because they pass raw integers (offsets, sizes) that aren't OBJECTS handles.

### Flags

Only two flags matter for the payload path:

| Bit | Value | Name | Purpose |
|-----|-------|------|---------|
| 0 | 1 | `HAS_RETURN_BIT` | Method returns a value |
| 1 | 2 | `RETURN_IS_OBJ_BIT` | Return value → OBJECTS handle |

All other flags (IS_STRING, IS_BUFFER, IS_FUNCTION, IS_OBJECT, IS_STATIC, ARG_0_IS_SELF) are only used by the register-based path (Buffer).

## Why It's Hard to Reverse-Engineer

- **No source structure** — Output is a flat VM with integer-keyed handler closures. No function names, variable names, or control-flow structures from your C++ code.
- **Identifier mangling** — All generated variable names are replaced with random 1-2 character identifiers.
- **Paged memory emulation** — All memory access goes through 64KB page buffers with bit-shifted addressing.
- **Register-based dispatch** — A while-loop fetches closures from a dispatch table. Each handler returns the next PC address.
- **Chunk splitting** — Handlers are split across multiple ModuleScripts.
- **Block merging** — Sequential instructions are merged into single closures, flattening the control flow graph.

## Caveats

> [!WARNING]
> This project is experimental! Expect bugs with wrong addresses, corrupt register data, and other emulation issues.

- **Performance is slower than native Luau (~5.5x or more)**. Use `require()` for hot paths.
- **Heap limit:** 512 MB max, no defragmentation
- **Template instantiation:** Method calls with >5 args use stack allocation, which works but hasn't been tested at high arg counts
- **Many Roblox data types may not be fully supported yet**
- **Stack/heap distinction:** Objects on the stack are destroyed when the function returns; use `toObject()` and handle ownership explicitly

## Project Structure

```
├── build.bat                          # Top-level build script
├── pipeline/
│   ├── compile.bat                    # Full build pipeline
│   ├── linker.ld                      # RISC-V linker script
│   ├── minify.py                      # Luau minifier
│   ├── cleanup_move.py                # Move output to Roblox project
│   └── transpiler/                    # Python RISC-V → Luau transpiler
│       ├── main.py                    # Entry point
│       ├── asm_parser.py              # Assembly parser
│       ├── blocks.py                  # Block merging
│       ├── builders.py                # Luau module builders (shared.luau, run.luau)
│       ├── generator.py               # Instruction → handler generator
│       ├── obfuscator.py              # Identifier mangling
│       └── handlers/                  # Per-instruction-type handlers
│           ├── alu.py                 # Arithmetic & logic
│           ├── control.py             # Branches & jumps
│           ├── float.py               # Floating-point
│           ├── memory.py              # Loads & stores
│           └── ecall/                 # Roblox API syscalls (including syscall 75 payload)
└── src/
    ├── main_basic.cpp                 # Entry point
    ├── main_image.cpp                 # Image rendering demo
    └── lib/                           # Freestanding C++ headers
        ├── rbxl.hpp                   # LuaObj, Rbxl::call, callObj, structs, Buffer
        ├── heap.hpp                   # Virtual heap + vector<T>
        ├── pointers.hpp               # unique_ptr, shared_ptr
        ├── map.hpp                    # Hash map
        ├── lua.hpp                    # print, taskSpawn, taskDefer
        ├── math.hpp                   # Trig functions
        ├── enums.hpp                  # Roblox Enum table
        └── base64.hpp                 # Base64 decoder via EncodingService
```
