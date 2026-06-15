# cpp-luau-obfs

> **⚠️ Experimental** — This project is a work in progress. The Roblox bindings have no type safety yet; method calls go through raw `callMethod` / `callMethodStatic` with manual flag arguments.

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

1. Inter-op with existing Lua logic using require(), and hook onto Roblox bindings using .callMethod(), callMethodStatic().
2. Ability to use C++ features, like pointers, smart pointers, classes, and templating.
3. Bundle different files and classes into a single giant bundle.
4. Makes reconstructing the original source code hard due to aggressive optimizations done by the compiler.
5. Uses native code to speed up the emulation (still slower than native luau)

## CAVEATS

> [!WARNING]
> This project is experimental! Expect bugs with wrong addresses, registries containing corrupt data, and other issues with emulation.

- **Performance will be slower due to emulation (x5.5 or more)**. Use inter-opping with require() for hot paths.
- **Maximum 4 arguments for callMethod, callMethodStatic**
- No typing support for Roblox methods as of right now
- Many data types may not be supported yet
- Separation between heap and stack like in regular C++; make sure to be careful when passing data between threads or functions. Objects allocated on the stack may be deleted or out of scope, causing you to read garbage when trying to read it later.
- Use smart pointers or make sure to manually free objects on heap to prevent memory leak (max: 512 MB)

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
    Part p = Part::create();
    p.setName("ObfuscatedPart");
    p.setPosition(0, 10, 0);
    p.setSize(4, 1, 4);
    p.setColor(0.2f, 0.6f, 1.0f);
    p.setAnchored(true);

    Instance workspace = Instance::getWorkspace();
    Instance model = workspace.waitForChild("MyModel");
    if (model.valid()) {
        model.destroy();
    }

    return 0;
}
```

## Available APIs

### Roblox Instances

| C++ API | Description |
|---------|-------------|
| `Instance::New(type)` | Create any Instance by type name |
| `Part::create()` | Create a Part |
| `inst.destroy()` | Destroy an instance |
| `inst.clone()` | Clone an instance |
| `inst.findFirstChild(name)` | FindFirstChild |
| `inst.waitForChild(name)` | WaitForChild |
| `inst.require()` | Require a ModuleScript |

### Property Access

| C++ API | Description |
|---------|-------------|
| `inst.getPropertyFloat(name)` / `setPropertyFloat(name, val)` | Float properties |
| `inst.getPropertyVector3(name)` / `setPropertyVector3(name, v)` | Vector3 properties |
| `inst.getPropertyColor3(name)` / `setPropertyColor3(name, c)` | Color3 properties |
| `inst.getPropertyCFrame(name)` / `setPropertyCFrame(name, cf)` | CFrame properties |
| `inst.setPropertyString(name, val)` | String properties |
| `inst.setPropertyBool(name, val)` | Bool properties |
| `inst.getPropertyEnum(name)` / `setPropertyEnum(name, val)` | Enum properties |
| `inst.setPropertyInstance(name, target)` | Instance properties |

### Services & Globals

| C++ API | Description |
|---------|-------------|
| `Instance::getWorkspace()` | Get workspace |
| `Instance::getPlayers()` | Get Players service |
| `inst.getLocalPlayer()` | Get LocalPlayer |
| `Instance::getService(name)` | Get any service by name |
| `Instance::getGlobal(name)` | Get a Lua global as a handle |

### Method Calls (Untyped)

> **Note:** These are raw method calls with no type checking. You pass method names as strings and manually specify flags for argument types and return types.

```cpp
// :Method() syntax — passes self implicitly
inst.callMethod("Connect", callbackFn, RBXL_METHOD_ARG_1_IS_FUNCTION_BIT);

// .Method() syntax — static call, no implicit self
inst.callMethodStatic("GetService", "Players",
    RBXL_METHOD_HAS_RETURN_BIT | RBXL_METHOD_RETURN_IS_OBJ_BIT | RBXL_METHOD_ARG_1_IS_STRING_BIT);
```

| C++ API | Description |
|---------|-------------|
| `inst.callMethod(name, args..., flags)` | Method call (`:` syntax) |
| `inst.callMethodStatic(name, args..., flags)` | Static call (`.` syntax) |
| `inst.getMethod(name)` | Get a method/signal (e.g., `.Touched`) |

### Buffers

`Rbxl::createBuffer(size)`, `Rbxl::freeBuffer(handle)`, `Rbxl::bufferLen(handle)`, `Rbxl::bufferReadI8/I32/F32(handle, offset)`, `Rbxl::bufferWriteI8/I32/F32(handle, offset, value)`, `Rbxl::bufferFromString(str)`

### Memory

`Rbxl::malloc(size)`, `Rbxl::free(ptr)`, `Rbxl::heapUsed()`

### Threading

`Lua::taskWait(seconds)`, `Lua::taskSpawn(func, args...)`, `Lua::taskDefer(func, args...)`

### Utilities

`Lua::print(val)`, `math::rad(deg)`, `math::sin(x)`, `math::cos(x)`

### C++ Data Structures

The freestanding environment includes: `vector<T>`, `map<K,V>`, `unique_ptr<T>`, `shared_ptr<T>`, `make_unique<T>()`, `make_shared<T>()`, and a `CFrame` class with operations like `cframe_lookAt`, `cframe_mul`, `cframe_inverse`, `cframe_fromEulerAngles`.

## Why It's Hard to Reverse-Engineer

- **No source structure** — Output is a flat VM with integer-keyed handler closures. No function names, variable names, or control-flow structures from your C++ code.
- **Identifier mangling** — All generated variable names are replaced with random 1-2 character identifiers.
- **Paged memory emulation** — All memory access goes through 64KB page buffers with bit-shifted addressing.
- **Register-based dispatch** — A while-loop fetches closures from a dispatch table. Each handler returns the next PC address.
- **Chunk splitting** — Handlers are split across multiple ModuleScripts.
- **Tail merging** — Blocks are inlined to skip dispatch cycles, flattening the control flow graph.

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
│       ├── blocks.py                  # Block merging & tail merging
│       ├── builders.py                # Luau module builders
│       ├── generator.py               # Instruction → handler generator
│       ├── obfuscator.py              # Identifier mangling
│       └── handlers/                  # Per-instruction-type handlers
│           ├── alu.py                 # Arithmetic & logic
│           ├── control.py             # Branches & jumps
│           ├── float.py               # Floating-point
│           ├── memory.py              # Loads & stores
│           └── ecall/                 # Roblox API syscalls
└── src/
    ├── main.cpp                       # Your C++ code goes here
    └── lib/                           # Freestanding C++ headers
        ├── rbxl.hpp                   # Roblox API bindings (Instance, Part, CFrame, etc.)
        ├── heap.hpp                   # Virtual heap + vector<T>
        ├── pointers.hpp               # unique_ptr, shared_ptr
        ├── map.hpp                    # Hash map
        ├── lua.hpp                    # print, taskWait, taskSpawn, taskDefer
        ├── math.hpp                   # Trig functions
        ├── enums.hpp                  # Roblox Enum table
        └── ...
```
