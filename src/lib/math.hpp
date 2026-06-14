// math.hpp — Basic math utilities for this freestanding RISC-V environment
// (no <cmath> available with -nostdlib)
//
// All functions are inline. No standard library dependencies.
//
// Math functions (rad, sin, cos) delegate to syscalls that the transpiler
// translates to Lua's fast math library.

#ifndef MATH_HPP
#define MATH_HPP

namespace math {
    // Syscall 39: Degrees to radians — delegates to Lua math.rad()
    inline float rad(float degrees) {
        volatile float v = degrees;
        volatile float* ptr = &v;
        asm volatile ("mv a0, %0; li a7, 39; ecall" : : "r"(ptr) : "a0", "a7", "memory");
        return v;
    }

    // Syscall 40: Sine — delegates to Lua math.sin()
    inline float sin(float x) {
        volatile float v = x;
        volatile float* ptr = &v;
        asm volatile ("mv a0, %0; li a7, 40; ecall" : : "r"(ptr) : "a0", "a7", "memory");
        return v;
    }

    // Syscall 41: Cosine — delegates to Lua math.cos()
    inline float cos(float x) {
        volatile float v = x;
        volatile float* ptr = &v;
        asm volatile ("mv a0, %0; li a7, 41; ecall" : : "r"(ptr) : "a0", "a7", "memory");
        return v;
    }
}

#endif // MATH_HPP
