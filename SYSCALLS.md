# SYSCALLS.md — RISC-V Ecall Reference

All syscalls use `ecall` with the syscall number in `a7`. Arguments are passed in `a0`–`a6`, return values in `a0`.

**Active syscalls: 18**

---

## Memory (30–32)

| # | Name | C++ Function | Returns | Behavior |
|---|------|-------------|---------|----------|
| **30** | malloc | `Rbxl::malloc(unsigned int)` | `a0` = heap pointer | Allocates `a0` bytes from virtual heap |
| **31** | free | `Rbxl::free(void*)` | — | Frees the pointer at `a0` |
| **32** | heapUsed | `Rbxl::heapUsed()` | `a0` = bytes used | Returns current heap usage |

Defined in: `src/lib/heap.hpp`

---

## Math (none — now uses universal handle API)

Math functions (`rad`, `sin`, `cos`) were migrated off dedicated syscalls 39–41.
They now use the universal handle chain:
`objectWrite(79, type_id=4) → getGlobal("math")(52) → getPropertyObject(fnName)(62) → callObj(75) → objectRead(78, type_id=4) → release×4(64)`.

Defined in: `src/lib/math.hpp` (shared `_math_op` helper), `src/lib/rbxl.hpp` (in-place `void*` wrappers)

---

## Enum Bridge (42–43)

| # | Name | C++ Function | a0 | Returns | Behavior |
|---|------|-------------|----|---------|----------|
| **42** | fromEnum | `Rbxl::fromEnum(int)` | `a0` = enum index | `a0` = OBJECTS handle | Wraps `ENUMS[a0 + 1]` in OBJECTS |
| **43** | toEnum | `Rbxl::toEnum(void*)` | `a0` = OBJECTS handle | `a0` = enum index | Looks up `ENUM_TO_INDEX[OBJECTS[a0]]` |

Defined in: `src/lib/rbxl.hpp`

---

## Threading (48–49)

| # | Name | C++ Function | a0–a6 | Returns | Behavior |
|---|------|-------------|-------|---------|----------|
| **48** | taskSpawn | `Lua::taskSpawn(void*, args...)` | `a0` = fn addr, `a1-a6` = args | `a0` = thread ID | Spawns fn in new coroutine via `task.spawn` |
| **49** | taskDefer | `Lua::taskDefer(void*, args...)` | `a0` = fn addr, `a1-a6` = args | — | Defers fn via `task.defer` |

Both shift args so the spawned function sees its first arg in `a0` (standard ABI).
8 template overloads each (0–6 args). Defined in: `src/lib/lua.hpp`

---

## Object Lookup (47, 51–53)

| # | Name | C++ Function | a0 | a1 | Returns | Behavior |
|---|------|-------------|----|----|---------|----------|
| **47** | getService | `Rbxl::getService(const char*)` | `a0` = service name ptr | — | `a0` = OBJECTS handle | `game:GetService(RODATA[a0])`, cached |
| **51** | getMethod | `Rbxl::getMethod(void*, const char*)` | `a0` = obj handle | `a1` = method name ptr | `a0` = OBJECTS handle | `OBJECTS[a0][RODATA[a1]]` → OBJECTS |
| **52** | getGlobal | `Rbxl::getGlobal(const char*)` | `a0` = global name ptr | — | `a0` = OBJECTS handle | `_G[RODATA[a0]]` → OBJECTS |
| **53** | require | `Rbxl::require(void*)` | `a0` = module handle | — | `a0` = OBJECTS handle | `require(OBJECTS[a0])` → OBJECTS |

Defined in: `src/lib/rbxl.hpp`

---

## Object Lifecycle (62–64)

| # | Name | C++ Function | a0 | a1 | a2 | Returns | Behavior |
|---|------|-------------|----|----|----|---------|----------|
| **62** | getPropertyObject | `Rbxl::getPropertyObject(void*, const char*)` | `a0` = obj handle | `a1` = prop name ptr | — | `a0` = OBJECTS handle | `OBJECTS[a0][RODATA[a1]]` → OBJECTS |
| **63** | setPropertyObject | `Rbxl::setPropertyObject(void*, const char*, void*)` | `a0` = obj handle | `a1` = prop name ptr | `a2` = value handle | — | `OBJECTS[a0][RODATA[a1]] = OBJECTS[a2]` |
| **64** | releaseObject | `Rbxl::releaseObject(void*)` | `a0` = obj handle | — | — | — | `OBJECTS[a0] = nil` |

Defined in: `src/lib/rbxl.hpp`

---

## Call (46, 75)

| # | Name | C++ Function | Format | Behavior |
|---|------|-------------|--------|----------|
| **46** | callMethod (runtime) | `LuaObj::callMethod` | Register-based | Runtime-dispatched method call (only triggers inside callMethod function context) |
| **75** | callObj (payload) | `Rbxl::callObj(fnHandle, flags, args...)` | Payload-stack | `a0` points to a memory buffer: `[header(4B) | fnHandle(4B) | argHandles...]`. All args are OBJECTS handles. Returns are always wrapped in OBJECTS (`flags & 1` = has return). Variadic template. |

Defined in: `src/lib/rbxl.hpp` (75), `pipeline/transpiler/handlers/ecall/__init__.py` (46, 75)

---

## Object Conversion (78–79)

Unified type conversion syscalls. Replaces old syscalls 54–61 (structs), 66–73 (primitives), and 74 (fromFunction).

**Register layout (both):**
- `a0` = primary input (OBJECTS handle for read, source value for write)
- `a1` = type_id (0–8)

Struct reads additionally use `a2` = destination memory pointer.

### Type IDs

| ID | Type | Kind | Read Behavior | Write Behavior |
|----|------|------|---------------|----------------|
| **0** | Vector3 | struct | `OBJECTS[a0]` → memory at `a2` (3 floats: X,Y,Z) | Memory at `a0` → `Vector3.new()` → OBJECTS handle |
| **1** | CFrame | struct | `OBJECTS[a0]:GetComponents()` → memory at `a2` (12 floats) | Memory at `a0` → `CFrame.new()` → OBJECTS handle |
| **2** | Color3 | struct | `OBJECTS[a0]` → memory at `a2` (3 floats: R,G,B) | Memory at `a0` → `Color3.new()` → OBJECTS handle |
| **3** | UDim2 | struct | `OBJECTS[a0]` → memory at `a2` (4 floats: XS,XO,YS,YO) | Memory at `a0` → `UDim2.new()` → OBJECTS handle |
| **4** | float | primitive | Returns `f32_to_bits(OBJECTS[a0])` in `a0` | Wraps `bits_to_f32(a0)` in OBJECTS, returns handle |
| **5** | int | primitive | Returns `OBJECTS[a0]` in `a0` | Wraps `a0` in OBJECTS, returns handle |
| **6** | bool | primitive | Returns 1 if `OBJECTS[a0]` is truthy, else 0 | Wraps `(a0 ~= 0)` in OBJECTS, returns handle |
| **7** | string | primitive | Copies `OBJECTS[a0]` (string) to heap, returns heap ptr | Wraps `RODATA[a0]` (rodata string) in OBJECTS |
| **8** | function | write-only | — | `S.get_function(a0)` → wraps in callable Luau function, stores in OBJECTS |

| # | Name | C++ Functions | a0 | a1 | [a2] | Returns |
|---|------|-------------|----|----|------|---------|
| **78** | objectRead | `readFromObject()`, `toFloat()`, `toInt()`, `toBool()`, `toString()` | OBJECTS handle | type_id | dst ptr (structs) | value in `a0` |
| **79** | objectWrite | `toObject()`, `fromFloat()`, `fromInt()`, `fromBool()`, `fromString()`, `fromFunction()` | source value | type_id | — | OBJECTS handle in `a0` |

C++ methods in: `src/lib/rbxl.hpp`
Python handler: `pipeline/transpiler/handlers/ecall/conversions.py`

---

## Syscall Number Map (sorted)

```
 30  malloc
 31  free
 32  heapUsed
 42  fromEnum
 43  toEnum
 46  callMethod (runtime)
 47  getService
 48  taskSpawn
 49  taskDefer
 51  getMethod
 52  getGlobal
 53  require
 62  getPropertyObject
 63  setPropertyObject
 64  releaseObject
 75  callObj (payload)
 78  objectRead
 79  objectWrite
```

## Removed Syscalls

These were consolidated or replaced in prior refactors:

| Old # | Purpose | Replaced By |
|-------|---------|-------------|
| 4–7   | print (per-type) | objectWrite + getGlobal + callObj |
| 39–41 | rad/sin/cos (per-type) | objectWrite + getGlobal + getPropertyObject + callObj + objectRead |
| 54–61 | struct read/write (per-type) | 78–79 |
| 65 | call register-based (Buffer) | 75 (callObj) |
| 66–73 | primitive from/to (per-type) | 78–79 |
| — | RETURN_IS_OBJ_BIT flag | removed (returns always OBJECTS now) |
| 74 | fromFunction | 79 (type_id=8) |
| 76–77 | structRead/structWrite (interim) | 78–79 |

## File Reference

| File | Syscalls |
|------|----------|
| `src/lib/lua.hpp` | 48–49 (defines); also calls 52, 64, 75, 79 via print → `_print_obj` |
| `src/lib/heap.hpp` | 30–32 |
| `src/lib/math.hpp` | 52, 62, 64, 75, 78–79 (via `_math_op` helper) |
| `src/lib/rbxl.hpp` | 42–43, 47, 51–53, 62–64, 75, 78–79 |
| `pipeline/transpiler/handlers/ecall/__init__.py` | 46, 47, 51, 53, 62–64, 75, 78–79 (dispatches) |
| `pipeline/transpiler/handlers/ecall/conversions.py` | 78–79 (type handling) |
