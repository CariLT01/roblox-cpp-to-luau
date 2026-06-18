// math.hpp — Basic math utilities for this freestanding RISC-V environment
// (no <cmath> available with -nostdlib)
//
// All functions are inline. No standard library dependencies.
//
// Math functions (rad, sin, cos) use the universal object handle API:
// objectWrite (float→handle) → getGlobal("math") → getPropertyObject(fnName)
// → callObj (payload) → objectRead (handle→float).

#ifndef MATH_HPP
#define MATH_HPP

namespace math {

    // ── Shared helper: calls math.fnName(val) via the universal handle API ──
    // Flow: float→handle (79), getGlobal("math") (52), getPropertyObject(fnName) (62),
    //       callObj(1 arg, return obj) (75), objectRead handle→float (78), release ×4 (64).
    namespace detail {
        inline float _math_op(const char* fnName, float val) {
#ifdef __riscv
            // 1. objectWrite: float → OBJECTS handle
            void* h = nullptr;
            asm volatile("mv a0, %1; li a1, 4; li a7, 79; ecall; mv %0, a0"
                : "=r"(h) : "r"(val) : "a0", "a1", "a7");

            // 2. getGlobal("math")
            void* mathObj = nullptr;
            asm volatile("mv a0, %1; li a7, 52; ecall; mv %0, a0"
                : "=r"(mathObj) : "r"("math") : "a0", "a7");

            // 3. getPropertyObject: math[fnName]
            void* fn = nullptr;
            asm volatile("mv a0, %1; mv a1, %2; li a7, 62; ecall; mv %0, a0"
                : "=r"(fn) : "r"(mathObj), "r"(fnName) : "a0", "a1", "a7");

            // 4. callObj: fn(h) → result handle (1 handle, has return, return is obj)
            unsigned int _p[3];
            _p[0] = (1u << 16) | 1u | 2u;  // 1 handle, bit0=hasReturn, bit1=returnIsObj
            _p[1] = (unsigned int)(unsigned long long)fn;
            _p[2] = (unsigned int)(unsigned long long)h;
            void* rHandle = nullptr;
            asm volatile("mv a0, %1; li a7, 75; ecall; mv %0, a0"
                : "=r"(rHandle) : "r"(_p) : "a0", "a7", "memory");
            void* result = rHandle;  // save for release after objectRead clobbers it

            // 5. objectRead: result handle → float bits
            asm volatile("mv a0, %1; li a1, 4; li a7, 78; ecall; mv %0, a0"
                : "=r"(rHandle) : "r"(rHandle) : "a0", "a1", "a7");

            // 6. Release all handles (including the callObj return handle)
            asm volatile("mv a0, %0; li a7, 64; ecall" : : "r"(h) : "a0", "a7");
            asm volatile("mv a0, %0; li a7, 64; ecall" : : "r"(mathObj) : "a0", "a7");
            asm volatile("mv a0, %0; li a7, 64; ecall" : : "r"(fn) : "a0", "a7");
            asm volatile("mv a0, %0; li a7, 64; ecall" : : "r"(result) : "a0", "a7");

            // Return float via type-pun (asm output is register bits)
            union { void* p; float f; } u;
            u.p = rHandle;
            return u.f;
#else
            (void)fnName;
            return val;
#endif
        }
    }

    // Degrees to radians — delegates to Lua math.rad() via handle API
    inline float rad(float degrees) { return detail::_math_op("rad", degrees); }

    // Sine — delegates to Lua math.sin() via handle API
    inline float sin(float x) { return detail::_math_op("sin", x); }

    // Cosine — delegates to Lua math.cos() via handle API
    inline float cos(float x) { return detail::_math_op("cos", x); }
}

#endif // MATH_HPP
