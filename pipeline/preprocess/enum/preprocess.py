import json
data = {}

with open("data.json") as f:
    data = json.load(f)


inner_code = []

for en in data:
    enum_name: str = en
    cpp_enum_name = enum_name.replace(".","_").upper().removeprefix("ENUM_")
    inner_code.append(f"        {cpp_enum_name}")

inner_code_str = ",\n".join(inner_code)

code = f"""
namespace Rbxl {{
    enum class Enum : int {{
{inner_code_str}
    }};
}};
"""

with open("output.hpp", "w") as f:
    f.write(code)
    
lua_code = ", ".join(data)
with open("output.luau", "w") as f:
    f.write(f"""local enums={{{lua_code}}}""")
# Also write to obf_src/ so transpiler_new.py can find it for ENUMS table
with open("../obf_src/enums.luau", "w") as f:
    f.write(f"""local enums={{{lua_code}}}""")
