"""Constants and configuration for the Luau transpiler."""

OUT_DIR = "dist"  # output subdirectory for generated .luau files

# Lua identifiers that must NOT be mangled (keywords, builtins, Roblox globals)
LUA_RESERVED = {
    # Keywords
    "and", "break", "do", "else", "elseif", "end", "false", "for", "function",
    "goto", "if", "in", "local", "nil", "not", "or", "repeat", "return",
    "then", "true", "until", "while",
    # Lua standard globals
    "assert", "collectgarbage", "dofile", "error", "getfenv", "getmetatable",
    "ipairs", "load", "loadfile", "loadstring", "module", "next", "pairs", "pcall",
    "print", "rawequal", "rawget", "rawlen", "rawset", "require", "select",
    "setfenv", "setmetatable", "tonumber", "tostring", "type", "unpack", "xpcall",
    "_G", "_VERSION",
    # Luau builtins
    "bit32", "buffer", "task", "typeof", "table", "string", "math", "coroutine",
    "os", "debug", "utf8",
    # Roblox globals
    "game", "workspace", "script", "plugin", "shared",
    "Instance", "Vector3", "Vector2", "CFrame", "Color3", "BrickColor", "Enum",
    "Ray", "Region3", "UDim", "UDim2", "Rect", "Axes", "Faces",
    "NumberRange", "NumberSequence", "NumberSequenceKeypoint",
    "ColorSequence", "ColorSequenceKeypoint", "PhysicalProperties",
    "TweenInfo", "Random", "DateTime", "PathWaypoint",
    "CatalogSearchParams", "OverlapParams", "RaycastParams",
    # bit32 methods (accessed via bit32.band etc.)
    "band", "bor", "bxor", "bnot", "lshift", "rshift", "arshift",
    # buffer methods
    "create", "fromstring", "len", "readi8", "readi32", "readf32",
    "writei8", "writei32", "writef32",
    # math methods
    "floor", "ceil", "sqrt", "abs", "sin", "cos", "rad", "min", "max", "huge", "pi",
    # table / string methods
    "concat", "format", "char",
    # Roblox constructors
    "new",
    # Roblox Instance methods
    "Destroy", "Clone", "FindFirstChild", "WaitForChild", "GetComponents",
    "GetService", "GetChildren", "wait",
    # Roblox Instance properties
    "Parent", "LocalPlayer", "X", "Y", "Z", "R", "G", "B",
    # VM shared-state names that cross module boundaries (must not be mangled)
    "ENUMS", "ENUM_TO_INDEX",
}

# RISC-V integer register ABI name → index mapping
REG_ABI_MAP = {
    'zero': 0, 'ra': 1, 'sp': 2, 'gp': 3, 'tp': 4, 't0': 5, 't1': 6, 't2': 7,
    's0': 8, 'fp': 8, 's1': 9, 'a0': 10, 'a1': 11, 'a2': 12, 'a3': 13, 'a4': 14,
    'a5': 15, 'a6': 16, 'a7': 17, 's2': 18, 's3': 19, 's4': 20, 's5': 21,
    's6': 22, 's7': 23, 's8': 24, 's9': 25, 's10': 26, 's11': 27,
    't3': 28, 't4': 29, 't5': 30, 't6': 31,
}

# RISC-V floating-point register ABI name → index mapping
FP_REG_ABI_MAP = {
    'ft0': 0, 'ft1': 1, 'ft2': 2, 'ft3': 3, 'ft4': 4, 'ft5': 5,
    'ft6': 6, 'ft7': 7, 'fs0': 8, 'fs1': 9, 'fa0': 10, 'fa1': 11,
    'fa2': 12, 'fa3': 13, 'fa4': 14, 'fa5': 15, 'fa6': 16, 'fa7': 17,
    'fs2': 18, 'fs3': 19, 'fs4': 20, 'fs5': 21,
    'fs6': 22, 'fs7': 23, 'fs8': 24, 'fs9': 25, 'fs10': 26, 'fs11': 27,
    'ft8': 28, 'ft9': 29, 'ft10': 30, 'ft11': 31,
}

# Maximum instructions per chunk module
CHUNK_SIZE = 1000

# Instructions that change control flow (can't merge past them)
TERMINATOR_OPS = {"beq", "bne", "blt", "bge", "bltu", "bgeu", "jal", "jalr", "ecall", "ebreak", "ret"}
