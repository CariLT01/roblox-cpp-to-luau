/*#include "lib/rbxl.hpp"
#include "lib/pointers.hpp"
#include "lib/crt.hpp"


int main() {

    Lua::print("Begin");

    LuaObj clock = LuaObj::getGlobal("os");

    Lua::print("Begin");

    int begin = (int)(unsigned int)clock.callMethodStatic("clock", RBXL_METHOD_HAS_RETURN_BIT);

    int c = 0;
    for (int i = 0; i < 1000000; i++) {
        c += i;
    }

    Lua::print("counter is:");
    Lua::print(c);

    int end = (int)(unsigned int)clock.callMethodStatic("clock", RBXL_METHOD_HAS_RETURN_BIT);
    int delta = end - begin;
    Lua::print(delta);

    return 0;
}*/