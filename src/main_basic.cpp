/*#include "lib/lua.hpp"
#include "lib/rbxl.hpp"

int main() {
    Lua::print("Hello World!");

    LuaObj p = Rbxl::createPart();
    LuaObj wk = Rbxl::getService("Workspace");

    p.setPropertyVector3("Position", Vector3{5.25f, 7.5f, 8.75f});
    p.setPropertyVector3("Orientation", Vector3{45.0f, 47.0f, 51.0f});
    p.setPropertyBool("Anchored", true);
    p.setParent(wk);

    return 0;
}*/