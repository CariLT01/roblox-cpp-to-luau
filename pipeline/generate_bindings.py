#!/usr/bin/env python3
"""generate_bindings.py — Auto-generate C++ class bindings from the Roblox API dump.

Downloads the API dump, parses all classes, and generates:
  1. A C++ header (generated_bindings.hpp) with per-class wrappers
  2. A report (unimplemented.txt) listing methods that cannot be implemented

Usage:
    python pipeline/generate_bindings.py                    # uses api_dump.json in cwd
    python pipeline/generate_bindings.py path/to/API-Dump.json
    python pipeline/generate_bindings.py --download         # fetch from GitHub first
"""

import json
import os
import sys
import re
from collections import defaultdict
from datetime import datetime

# ─── Roblox type → C++ type mapping ───────────────────────────────────────────

# Types passable as a SINGLE 32-bit register through callMethod (syscall 46).
# Multi-register types (Vector3, CFrame, etc.) are NOT supported because
# callMethod only has registers a0-a6 for handle+method+flags+4 args.
SUPPORTED_PARAM_TYPES = {
    "float":        ("float",       "float"),
    "double":       ("float",       "float"),
    "int":          ("int",         "int"),
    "int64":        ("int",         "int"),
    "bool":         ("bool",        "int"),
    "string":       ("const char*", "string"),
    "Content":      ("const char*", "string"),
    "ContentId":    ("const char*", "string"),
    "ProtectedString": ("const char*", "string"),
    "BinaryString": ("const char*", "string"),
    # Single-register value types
    "BrickColor":   ("int",         "int"),
    # Instance types (passed as void* handle — fits in one register)
    "Instance":     ("LuaObj",      "object"),
}

# Everything is a handle now. All property getters return LuaObj.
SUPPORTED_RETURN_TYPES = {
    "float":        ("LuaObj", "object"),
    "double":       ("LuaObj", "object"),
    "int":          ("LuaObj", "object"),
    "int64":        ("LuaObj", "object"),
    "bool":         ("LuaObj", "object"),
    "string":       ("LuaObj", "object"),
    "Content":      ("LuaObj", "object"),
    "ContentId":    ("LuaObj", "object"),
    "BinaryString": ("LuaObj", "object"),
    "Vector3":      ("LuaObj", "object"),
    "Vector2":      ("LuaObj", "object"),
    "CFrame":       ("LuaObj", "object"),
    "Color3":       ("LuaObj", "object"),
    "UDim2":        ("LuaObj", "object"),
    "BrickColor":   ("LuaObj", "object"),
    "Ray":          ("LuaObj", "object"),
    "Rect":         ("LuaObj", "object"),
    "Instance":     ("LuaObj", "object"),
    "Enum":         ("LuaObj", "object"),
}

# Multi-register struct types that CANNOT be passed through callMethod registers
MULTI_REG_PARAM_TYPES = {
    "Vector3", "Vector2", "CFrame", "Color3", "UDim2", "UDim",
    "Ray", "Rect", "NumberRange", "NumberSequence", "ColorSequence",
    "TweenInfo", "PhysicalProperties", "Faces", "Axes",
    "Vector2int16", "Vector3int16",
}

# Types that are fundamentally unsupported
UNSUPPORTED_CONTAINER_TYPES = {
    "Tuple", "Variant", "Array", "Map", "Dictionary",
    "Instances", "Objects", "Objects[Instance]", "function",
    "SharedTable", "thread", "buffer", "any",
}

# Enum type names (populated at runtime from the API dump)
ENUM_TYPE_NAMES = set()


# ─── Classification helpers ───────────────────────────────────────────────────

def normalize_type_name(name):
    """Strip optional markers like '?' from type names."""
    return name.rstrip('?') if name else ""


def classify_param_type(type_name, type_category=""):
    """Return (cpp_type, tag) for a parameter type, or None if unsupported."""
    clean = normalize_type_name(type_name)
    if type_category == "Enum" or clean in ENUM_TYPE_NAMES:
        return ("LuaObj", "object")
    if type_category == "Class":
        return ("LuaObj", "object")
    if clean in MULTI_REG_PARAM_TYPES:
        return None  # can't pass through registers
    if clean in UNSUPPORTED_CONTAINER_TYPES:
        return None
    return SUPPORTED_PARAM_TYPES.get(clean)


def classify_return_type(type_name, type_category=""):
    """Return (cpp_type, tag) for a return type, or None if unsupported."""
    clean = normalize_type_name(type_name)
    if type_category == "Enum" or clean in ENUM_TYPE_NAMES:
        return ("LuaObj", "object")
    if type_category == "Class":
        return (safe_cpp_name(clean), "object")  # specific class, not generic LuaObj
    if clean in UNSUPPORTED_CONTAINER_TYPES:
        return None
    return SUPPORTED_RETURN_TYPES.get(clean)


def get_type_name(type_obj):
    """Safely extract type name from a type object."""
    if type_obj is None:
        return ""
    if isinstance(type_obj, dict):
        return type_obj.get("Name", "")
    if isinstance(type_obj, list):
        return "Tuple"  # multi-return
    return str(type_obj)


def get_type_category(type_obj):
    """Safely extract type category."""
    if isinstance(type_obj, dict):
        return type_obj.get("Category", "")
    return ""


# ─── C++ name helpers ─────────────────────────────────────────────────────────

def safe_cpp_name(name):
    name = re.sub(r'[^a-zA-Z0-9_]', '_', name)
    if name and name[0].isdigit():
        name = '_' + name
    return name


def method_name_to_cpp(name):
    cpp = safe_cpp_name(name)
    if cpp and cpp[0].isupper():
        cpp = cpp[0].lower() + cpp[1:]
    return cpp


# ─── API dump parsing ─────────────────────────────────────────────────────────

def parse_api_dump(dump):
    classes = dump.get("Classes", [])
    enum_items = dump.get("Enums", [])

    for enum in enum_items:
        ENUM_TYPE_NAMES.add(enum.get("Name", ""))

    class_map = {}
    for cls in classes:
        name = cls["Name"]
        super_name = cls.get("Superclass", "")
        members = cls.get("Members", [])

        props, funcs, cbs, evts = [], [], [], []
        for m in members:
            mt = m.get("MemberType", "")
            if mt == "Property":   props.append(m)
            elif mt == "Function": funcs.append(m)
            elif mt == "Callback": cbs.append(m)
            elif mt == "Event":    evts.append(m)

        class_map[name] = {
            "name": name,
            "superclass": super_name,
            "properties": props,
            "functions": funcs,
            "callbacks": cbs,
            "events": evts,
        }
    return class_map


def collect_inherited_functions(class_map, target_class):
    """Collect inherited functions, deduplicating by (origin_class, name)."""
    result = []  # (func, origin_class)
    current = target_class
    seen = set()
    while current and current in class_map:
        cls = class_map[current]
        for func in cls["functions"]:
            key = (current, func["Name"])
            if key not in seen:
                seen.add(key)
                result.append((func, current))
        current = cls["superclass"]
    return result


# ─── Method analysis ──────────────────────────────────────────────────────────

def analyze_function(func, is_static=False):
    """Analyze a function. Returns (ok, reason, info_dict)."""
    name = func["Name"]
    security = func.get("Security", "None")
    tags = func.get("Tags", [])

    if "Deprecated" in tags:
        return False, "deprecated", None
    if security not in ("None",):
        return False, f"security:{security}", None

    params = func.get("Parameters", [])
    if isinstance(params, list) and params and isinstance(params[0], list):
        params = params[0] if params else []

    if len(params) > 4:
        return False, f"too_many_args:{len(params)}/4", None

    # Return type
    ret_type_obj = func.get("ReturnType", {})
    ret_name = get_type_name(ret_type_obj)
    ret_cat = get_type_category(ret_type_obj)
    has_return = bool(ret_name) and ret_name.lower() not in ("void", "null", "none")

    ret_class = None
    return_is_obj = False
    return_is_buffer = False

    if has_return:
        ret_class = classify_return_type(ret_name, ret_cat)
        if ret_class is None:
            return False, f"unsupported_return:{ret_name}", None
        if ret_class[1] == "object":
            return_is_obj = True
        if ret_name == "buffer":
            return_is_buffer = True

    # Parameters
    param_infos = []
    for p in params:
        p_name = p.get("Name", "")
        p_type_obj = p.get("Type", {})
        p_type_name = get_type_name(p_type_obj)
        p_type_cat = get_type_category(p_type_obj)

        p_class = classify_param_type(p_type_name, p_type_cat)
        if p_class is None:
            # Check if it's specifically a multi-reg type for a clearer reason
            clean = normalize_type_name(p_type_name)
            if clean in MULTI_REG_PARAM_TYPES:
                return False, f"multi_reg_type:{clean}({p_name})", None
            return False, f"unsupported_param:{p_type_name}({p_name})", None
        param_infos.append({
            "name": p_name,
            "type_name": p_type_name,
            "cpp_type": p_class[0],
            "tag": p_class[1],
        })

    # Build flags for syscall 46
    # arg string bits: arg1=3, arg2=4, arg3=6, arg4=7
    # arg object bits: arg1=17, arg2=18, arg3=19, arg4=20
    arg_string_bits = [3, 4, 6, 7]
    arg_object_bits = [17, 18, 19, 20]

    flags = 0
    if has_return:
        flags |= (1 << 0)
        if return_is_obj:
            flags |= (1 << 1)
        if return_is_buffer:
            flags |= (1 << 5)
    if is_static:
        flags |= (1 << 8)

    for i, pi in enumerate(param_infos):
        if i >= 4:
            break
        if pi["tag"] == "string":
            flags |= (1 << arg_string_bits[i])
        if pi["tag"] == "object":
            flags |= (1 << arg_object_bits[i])

    # Build C++ signature
    cpp_params = [f"{pi['cpp_type']} {safe_cpp_name(pi['name'])}" for pi in param_infos]
    ret_cpp = ret_class[0] if has_return and ret_class else "void"
    method_cpp_name = method_name_to_cpp(name)

    return True, "", {
        "name": name,
        "cpp_name": method_cpp_name,
        "ret_cpp": ret_cpp,
        "params": param_infos,
        "cpp_params": cpp_params,
        "flags": flags,
        "has_return": has_return,
        "return_is_obj": return_is_obj,
        "is_static": is_static,
    }


# ─── C++ code generation ─────────────────────────────────────────────────────

def flags_to_macro_expr(flags):
    """Convert an integer flags value to a C++ macro expression string.

    Uses the RBXL_METHOD_* defines from rbxl.hpp to produce a readable,
    self-documenting default value for the flags parameter.
    """
    if flags == 0:
        return "0"
    FLAG_BIT_MACROS = {
        0:  "RBXL_METHOD_HAS_RETURN_BIT",
        1:  "RBXL_METHOD_RETURN_IS_OBJ_BIT",
        2:  "RBXL_METHOD_CALL_TARGET_IS_SERVICE_BIT",
        3:  "RBXL_METHOD_ARG_1_IS_STRING_BIT",
        4:  "RBXL_METHOD_ARG_2_IS_STRING_BIT",
        5:  "RBXL_METHOD_RETURN_IS_BUFFER_BIT",
        6:  "RBXL_METHOD_ARG_3_IS_STRING_BIT",
        7:  "RBXL_METHOD_ARG_4_IS_STRING_BIT",
        8:  "RBXL_METHOD_IS_STATIC_BIT",
        9:  "RBXL_METHOD_ARG_1_IS_BUFFER_BIT",
        10: "RBXL_METHOD_ARG_2_IS_BUFFER_BIT",
        11: "RBXL_METHOD_ARG_3_IS_BUFFER_BIT",
        12: "RBXL_METHOD_ARG_4_IS_BUFFER_BIT",
        13: "RBXL_METHOD_ARG_1_IS_FUNCTION_BIT",
        14: "RBXL_METHOD_ARG_2_IS_FUNCTION_BIT",
        15: "RBXL_METHOD_ARG_3_IS_FUNCTION_BIT",
        16: "RBXL_METHOD_ARG_4_IS_FUNCTION_BIT",
        17: "RBXL_METHOD_ARG_1_IS_OBJECT_BIT",
        18: "RBXL_METHOD_ARG_2_IS_OBJECT_BIT",
        19: "RBXL_METHOD_ARG_3_IS_OBJECT_BIT",
        20: "RBXL_METHOD_ARG_4_IS_OBJECT_BIT",
    }
    parts = []
    for bit, macro in sorted(FLAG_BIT_MACROS.items()):
        if flags & (1 << bit):
            parts.append(macro)
    return " | ".join(parts)

def build_call_args(info):
    """Build argument list for callMethod invocation."""
    parts = []
    for pi in info["params"]:
        pname = safe_cpp_name(pi["name"])
        if pi["tag"] == "string":
            parts.append(f"(const char*){pname}")
        elif pi["tag"] == "object":
            parts.append(f"{pname}.handle()")
        else:
            parts.append(pname)
    return ", ".join(parts) + ", " if parts else ""


def generate_class(cls_name, class_data, class_map, unimpl_dedup):
    """Generate C++ class code. Returns (header_text, impl_count)."""
    super_name = class_data["superclass"]
    cpp_class = safe_cpp_name(cls_name)

    parent = "LuaObj"
    if cls_name in ("Instance", "Object"):
        # Instance and Object are the two root classes — both extend LuaObj directly.
        parent = "LuaObj"
    elif super_name and super_name != cls_name and super_name != "<<<ROOT>>>":
        parent = safe_cpp_name(super_name)

    lines = []
    lines.append(f"// ── {cls_name} (inherits {parent}) ──")
    lines.append(f"class {cpp_class} : public {parent} {{")
    lines.append("public:")
    lines.append(f"    {cpp_class}() : {parent}() {{}}")
    lines.append(f"    {cpp_class}(void* handle) : {parent}(handle) {{}}")
    lines.append(f"    {cpp_class}(const {parent}& other) : {parent}(other.handle()) {{}}")

    impl_count = 0

    # Analyze own functions only (inherited methods come from LuaObj/Instance base)
    for func in class_data["functions"]:
        ok, reason, info = analyze_function(func, is_static=False)
        if not ok:
            dedup_key = (cls_name, func["Name"], reason)
            if dedup_key not in unimpl_dedup:
                unimpl_dedup.add(dedup_key)
            continue

        impl_count += 1
        params_str = ", ".join(info["cpp_params"])
        flags_expr = flags_to_macro_expr(info["flags"])
        if params_str:
            params_str += ", "
        params_str += f"int flags = {flags_expr}"

        ret = info["ret_cpp"]
        call_args = build_call_args(info)
        lines.append("")
        lines.append(f"    // {info['name']}()")

        if info["has_return"]:
            if info["return_is_obj"]:
                lines.append(f"    {ret} {info['cpp_name']}({params_str}) const {{")
                lines.append(f"        return {ret}(callMethod(\"{info['name']}\", {call_args}flags));")
            elif ret == "float":
                lines.append(f"    {ret} {info['cpp_name']}({params_str}) const {{")
                lines.append(f"        int _raw = (int)(unsigned int)callMethod(\"{info['name']}\", {call_args}flags);")
                lines.append(f"        return bits_to_f32_c(_raw);")
            elif ret == "bool":
                lines.append(f"    {ret} {info['cpp_name']}({params_str}) const {{")
                lines.append(f"        return (int)(unsigned int)callMethod(\"{info['name']}\", {call_args}flags) != 0;")
            else:
                lines.append(f"    {ret} {info['cpp_name']}({params_str}) const {{")
                lines.append(f"        return ({ret})(unsigned int)callMethod(\"{info['name']}\", {call_args}flags);")
        else:
            lines.append(f"    void {info['cpp_name']}({params_str}) const {{")
            lines.append(f"        callMethod(\"{info['name']}\", {call_args}flags);")
        lines.append(f"    }}")

    # Property accessors (own properties only)
    for prop in class_data["properties"]:
        p_name = prop["Name"]
        security = prop.get("Security", "None")
        tags = prop.get("Tags", [])
        if security not in ("None",):
            continue
        if "Deprecated" in tags or "Hidden" in tags or "NotScriptable" in tags:
            continue

        vtype_obj = prop.get("ValueType", {})
        vtype_name = get_type_name(vtype_obj)
        vtype_cat = get_type_category(vtype_obj)
        getter = classify_return_type(vtype_name, vtype_cat)
        if getter is None:
            continue

        cpp_name = safe_cpp_name(p_name)
        if cpp_name and cpp_name[0].isupper():
            cpp_name = cpp_name[0].lower() + cpp_name[1:]

        # Everything is a handle — all property getters use getPropertyObject
        lines.append(f"    LuaObj get_{cpp_name}() const {{ return getPropertyObject(\"{p_name}\"); }}")

    lines.append("};")
    lines.append("")
    return "\n".join(lines), impl_count


def generate_bindings(api_dump_path, output_dir):
    """Main generation function."""
    print(f"Loading API dump from {api_dump_path}...")
    with open(api_dump_path, "r", encoding="utf-8") as f:
        dump = json.load(f)

    class_map = parse_api_dump(dump)
    print(f"Found {len(class_map)} classes, {len(ENUM_TYPE_NAMES)} enum types")

    total_funcs = sum(len(c["functions"]) for c in class_map.values())
    total_props = sum(len(c["properties"]) for c in class_map.values())
    total_evts = sum(len(c["events"]) for c in class_map.values())
    print(f"Total: {total_funcs} functions, {total_props} properties, {total_evts} events")

    # Generate class headers
    unimpl_dedup = set()  # (class, method, reason) for deduplication
    class_headers = []
    total_impl = 0

    # Topological sort: parent classes must be fully defined before children.
    # Alphabetical ordering would break inheritance (e.g. BasePart before PVInstance).
    def _topo_sort(class_map):
        """Sort class names so every parent appears before its children."""
        # Compute inheritance depth for each class
        depth_cache = {}
        def _depth(name):
            if name in depth_cache:
                return depth_cache[name]
            if name not in class_map:
                depth_cache[name] = 0
                return 0
            sup = class_map[name].get("superclass", "")
            d = 1 + _depth(sup) if sup and sup != "<<<ROOT>>>" else 1
            depth_cache[name] = d
            return d
        for name in class_map:
            _depth(name)
        # Sort by depth (parents first), then alphabetically for stability
        return sorted(class_map.keys(), key=lambda n: (depth_cache.get(n, 0), n))

    sorted_classes = _topo_sort(class_map)

    for cls_name in sorted_classes:
        cls = class_map[cls_name]
        header, count = generate_class(cls_name, cls, class_map, unimpl_dedup)
        class_headers.append(header)
        total_impl += count

    # Collect unimplemented by reason
    unimpl_by_reason = defaultdict(list)
    for cls_name, method_name, reason in unimpl_dedup:
        unimpl_by_reason[reason].append((cls_name, method_name))

    total_unimpl = len(unimpl_dedup)

    # Write header
    os.makedirs(output_dir, exist_ok=True)
    header_path = os.path.join(output_dir, "generated_bindings.hpp")

    with open(header_path, "w", encoding="utf-8") as f:
        f.write("// ═══════════════════════════════════════════════════════════════\n")
        f.write("// AUTO-GENERATED by generate_bindings.py — DO NOT EDIT\n")
        f.write(f"// Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"// Classes: {len(class_map)}\n")
        f.write("// ═══════════════════════════════════════════════════════════════\n\n")
        f.write("#ifndef GENERATED_BINDINGS_HPP\n")
        f.write("#define GENERATED_BINDINGS_HPP\n\n")
        f.write("#include \"rbxl.hpp\"\n\n")
        f.write("// LuaObj is the base handle class (defined in rbxl.hpp)\n\n")
        f.write("// Float bit-punning helper (Luau f32_to_bits / bits_to_f32 equivalent)\n")
        f.write("static inline float bits_to_f32_c(int bits) {\n")
        f.write("    union { int i; float f; } u; u.i = bits; return u.f;\n")
        f.write("}\n")
        f.write("static inline int f32_to_bits_c(float f) {\n")
        f.write("    union { int i; float f; } u; u.f = f; return u.i;\n")
        f.write("}\n\n")

        # Forward declarations
        f.write("// LuaObj API (defined in rbxl.hpp):\n")
        f.write("//   getPropertyObject(name)       — returns handle for ANY property\n")
        f.write("//   setPropertyObject(name, val)  — sets property from a handle\n")
        f.write("//   callMethod(name, args, flags) — syscall 46\n")
        f.write("//   getService(name)              — syscall 47\n")
        f.write("//   getGlobal(name)               — syscall 52\n")
        f.write("//   getMethod(name)               — syscall 51\n")
        f.write("//   require()                     — syscall 53\n")
        f.write("//   release()                     — syscall 64\n")
        f.write("//\n")
        f.write("// Struct bridge (on Vector3, CFrame, Color3, UDim2):\n")
        f.write("//   readFromObject(handle)        — syscalls 54/56/58/60\n")
        f.write("//   toObject()                    — syscalls 55/57/59/61\n")
        f.write("*/\n\n")
        f.write("// Forward declarations\n")
        for cls_name in sorted_classes:
            cpp = safe_cpp_name(cls_name)
            if cpp == "LuaObj":
                continue
            f.write(f"class {cpp};\n")
        f.write("\n")

        # Silence clangd false-positive: on 64-bit hosts, void* -> unsigned int
        # truncation is flagged, but the target is 32-bit RISC-V where
        # sizeof(void*) == sizeof(unsigned int).
        f.write("#ifdef __clang__\n")
        f.write("#pragma clang diagnostic push\n")
        f.write("#pragma clang diagnostic ignored \"-Wpointer-to-int-cast\"\n")
        f.write("#endif\n\n")

        for h in class_headers:
            f.write(h)
            f.write("\n")

        f.write("#ifdef __clang__\n")
        f.write("#pragma clang diagnostic pop\n")
        f.write("#endif\n\n")

        f.write("#endif // GENERATED_BINDINGS_HPP\n")

    print(f"\nGenerated: {header_path}")

    # Write report
    report_path = os.path.join(output_dir, "unimplemented.txt")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(f"Unimplemented Methods Report\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"{'=' * 60}\n\n")
        f.write(f"Total unique unimplemented: {total_unimpl}\n\n")

        for reason in sorted(unimpl_by_reason.keys()):
            entries = unimpl_by_reason[reason]
            f.write(f"\n--- {reason} ({len(entries)} methods) ---\n")
            for cls_name, method_name in sorted(entries):
                f.write(f"  {cls_name}::{method_name}\n")

    print(f"Generated: {report_path}")

    # Summary
    print(f"\n{'=' * 60}")
    print(f"Summary:")
    print(f"  Classes: {len(class_map)}")
    print(f"  Implementable: {total_impl} methods")
    print(f"  Unimplementable: {total_unimpl} unique methods")
    print(f"\n  Unimplemented by reason:")
    for reason in sorted(unimpl_by_reason.keys()):
        print(f"    {reason}: {len(unimpl_by_reason[reason])}")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Generate C++ bindings from Roblox API dump")
    parser.add_argument("input", nargs="?", default="api_dump.json",
                        help="Path to API-Dump.json (default: api_dump.json)")
    parser.add_argument("--output", "-o", default="src/lib",
                        help="Output directory (default: src/lib)")
    parser.add_argument("--download", action="store_true",
                        help="Download API dump from GitHub first")
    args = parser.parse_args()

    if args.download:
        import urllib.request
        url = "https://raw.githubusercontent.com/CloneTrooper1019/Roblox-Client-Tracker/roblox/API-Dump.json"
        print(f"Downloading API dump from {url}...")
        urllib.request.urlretrieve(url, args.input)
        print(f"Saved to {args.input}")

    if not os.path.exists(args.input):
        print(f"Error: {args.input} not found. Use --download to fetch it.")
        sys.exit(1)

    generate_bindings(args.input, args.output)


if __name__ == "__main__":
    main()
