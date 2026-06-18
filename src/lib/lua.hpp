// lua.hpp — Lua standard library bindings for this freestanding RISC-V environment
//
// Functions that map directly to Lua globals / standard libraries:
//   print()         → Lua print()
//   taskSpawn()     → task.spawn()
//   taskDefer()     → task.defer()
//
// All syscalls use the ecall instruction; arguments are marshalled through
// the RISC-V integer registers (a0–a6) and the syscall number in a7.

#ifndef LUA_HPP
#define LUA_HPP

namespace Lua {

    // ── Type-punning helper ──────────────────────────────────────────────
    // Converts any 32-bit value (int, void*, float) to an int for register
    // passing.  The compiler handles float→int via fmv.x.w on hardfloat ABIs.
    template <typename T>
    inline int to_reg(T val) {
        static_assert(sizeof(T) == 4, "Only 32-bit types supported (int, void*, float)");
        union { T in; int out; } u;
        u.in = val;
        return u.out;
    }

    // ── print() — universal handle API, no dedicated syscalls ────────────
    // Converts value → OBJECTS handle (syscall 79), resolves global "print"
    // via getGlobal (syscall 52), calls it via callObj (syscall 75), then
    // releases both handles (syscall 64).

    // Shared implementation: calls global "print" with one OBJECTS handle arg.
    namespace {
        inline void _print_obj(void* handle) {
#ifdef __riscv
            // getGlobal("print")
            void* printFn = nullptr;
            asm volatile("mv a0, %1; li a7, 52; ecall; mv %0, a0"
                : "=r"(printFn) : "r"("print") : "a0", "a7");
            // callObj(printFn, 0, handle)  — payload-based, 1 arg, no return
            unsigned int _p[3];
            _p[0] = (1u << 16) | 0u;                          // 1 handle, flags=0
            _p[1] = (unsigned int)(unsigned long long)printFn; // fn handle
            _p[2] = (unsigned int)(unsigned long long)handle;  // arg handle
            asm volatile("mv a0, %0; li a7, 75; ecall"
                : : "r"(_p) : "a0", "a7", "memory");
            // release both handles
            asm volatile("mv a0, %0; li a7, 64; ecall" : : "r"(handle) : "a0", "a7");
            asm volatile("mv a0, %0; li a7, 64; ecall" : : "r"(printFn) : "a0", "a7");
#else
            (void)handle;
#endif
        }
    }

    inline void print(const char* str) {
#ifdef __riscv
        void* h = nullptr;
        asm volatile("mv a0, %1; li a1, 7; li a7, 79; ecall; mv %0, a0"
            : "=r"(h) : "r"(str) : "a0", "a1", "a7");  // type_id=7 string
        _print_obj(h);
#else
        (void)str;
#endif
    }

    inline void print(int val) {
#ifdef __riscv
        void* h = nullptr;
        asm volatile("mv a0, %1; li a1, 5; li a7, 79; ecall; mv %0, a0"
            : "=r"(h) : "r"(val) : "a0", "a1", "a7");  // type_id=5 int
        _print_obj(h);
#else
        (void)val;
#endif
    }

    inline void print(bool val) {
#ifdef __riscv
        void* h = nullptr;
        asm volatile("mv a0, %1; li a1, 6; li a7, 79; ecall; mv %0, a0"
            : "=r"(h) : "r"((int)val) : "a0", "a1", "a7");  // type_id=6 bool
        _print_obj(h);
#else
        (void)val;
#endif
    }

    inline void print(float val) {
#ifdef __riscv
        void* h = nullptr;
        asm volatile("mv a0, %1; li a1, 4; li a7, 79; ecall; mv %0, a0"
            : "=r"(h) : "r"(val) : "a0", "a1", "a7");  // type_id=4 float
        _print_obj(h);
#else
        (void)val;
#endif
    }

    // ── task.spawn() ─────────────────────────────────────────────────────
    // Syscall 48.  Returns the thread ID (small integer) as void*.

    // 0 arguments
    inline void* taskSpawn(void* func) {
        void* handle = nullptr;
#ifdef __riscv
        asm volatile (
            "mv a0, %1; li a7, 48; ecall; mv %0, a0"
            : "=r"(handle)
            : "r"(func)
            : "a0", "a7"
        );
#endif
        return handle;
    }

    // 1 argument
    template <typename A1>
    inline void* taskSpawn(void* func, A1 arg1) {
        void* handle = nullptr;
#ifdef __riscv
        asm volatile (
            "mv a0, %1; mv a1, %2; li a7, 48; ecall; mv %0, a0"
            : "=r"(handle)
            : "r"(func), "r"(to_reg(arg1))
            : "a0", "a1", "a7"
        );
#endif
        return handle;
    }

    // 2 arguments
    template <typename A1, typename A2>
    inline void* taskSpawn(void* func, A1 arg1, A2 arg2) {
        void* handle = nullptr;
#ifdef __riscv
        asm volatile (
            "mv a0, %1; mv a1, %2; mv a2, %3; li a7, 48; ecall; mv %0, a0"
            : "=r"(handle)
            : "r"(func), "r"(to_reg(arg1)), "r"(to_reg(arg2))
            : "a0", "a1", "a2", "a7"
        );
#endif
        return handle;
    }

    // 3 arguments
    template <typename A1, typename A2, typename A3>
    inline void* taskSpawn(void* func, A1 arg1, A2 arg2, A3 arg3) {
        void* handle = nullptr;
#ifdef __riscv
        asm volatile (
            "mv a0, %1; mv a1, %2; mv a2, %3; mv a3, %4; li a7, 48; ecall; mv %0, a0"
            : "=r"(handle)
            : "r"(func), "r"(to_reg(arg1)), "r"(to_reg(arg2)), "r"(to_reg(arg3))
            : "a0", "a1", "a2", "a3", "a7"
        );
#endif
        return handle;
    }

    // 4 arguments
    template <typename A1, typename A2, typename A3, typename A4>
    inline void* taskSpawn(void* func, A1 arg1, A2 arg2, A3 arg3, A4 arg4) {
        void* handle = nullptr;
#ifdef __riscv
        asm volatile (
            "mv a0, %1; mv a1, %2; mv a2, %3; mv a3, %4; mv a4, %5; "
            "li a7, 48; ecall; mv %0, a0"
            : "=r"(handle)
            : "r"(func), "r"(to_reg(arg1)), "r"(to_reg(arg2)),
              "r"(to_reg(arg3)), "r"(to_reg(arg4))
            : "a0", "a1", "a2", "a3", "a4", "a7"
        );
#endif
        return handle;
    }

    // 5 arguments
    template <typename A1, typename A2, typename A3, typename A4, typename A5>
    inline void* taskSpawn(void* func, A1 arg1, A2 arg2, A3 arg3, A4 arg4,
                           A5 arg5) {
        void* handle = nullptr;
#ifdef __riscv
        asm volatile (
            "mv a0, %1; mv a1, %2; mv a2, %3; mv a3, %4; mv a4, %5; "
            "mv a5, %6; li a7, 48; ecall; mv %0, a0"
            : "=r"(handle)
            : "r"(func), "r"(to_reg(arg1)), "r"(to_reg(arg2)),
              "r"(to_reg(arg3)), "r"(to_reg(arg4)), "r"(to_reg(arg5))
            : "a0", "a1", "a2", "a3", "a4", "a5", "a7"
        );
#endif
        return handle;
    }

    // 6 arguments
    template <typename A1, typename A2, typename A3, typename A4, typename A5,
              typename A6>
    inline void* taskSpawn(void* func, A1 arg1, A2 arg2, A3 arg3, A4 arg4,
                           A5 arg5, A6 arg6) {
        void* handle = nullptr;
#ifdef __riscv
        asm volatile (
            "mv a0, %1; mv a1, %2; mv a2, %3; mv a3, %4; mv a4, %5; "
            "mv a5, %6; mv a6, %7; li a7, 48; ecall; mv %0, a0"
            : "=r"(handle)
            : "r"(func), "r"(to_reg(arg1)), "r"(to_reg(arg2)),
              "r"(to_reg(arg3)), "r"(to_reg(arg4)), "r"(to_reg(arg5)),
              "r"(to_reg(arg6))
            : "a0", "a1", "a2", "a3", "a4", "a5", "a6", "a7"
        );
#endif
        return handle;
    }

    // ── task.defer() ─────────────────────────────────────────────────────
    // Syscall 49.  Defers function to next heartbeat.

    // 0 arguments
    inline void taskDefer(void* func) {
#ifdef __riscv
        asm volatile (
            "mv a0, %0; li a7, 49; ecall"
            :
            : "r"(func)
            : "a0", "a7"
        );
#endif
    }

    // 1 argument
    template <typename A1>
    inline void taskDefer(void* func, A1 arg1) {
#ifdef __riscv
        asm volatile (
            "mv a0, %0; mv a1, %1; li a7, 49; ecall"
            :
            : "r"(func), "r"(to_reg(arg1))
            : "a0", "a1", "a7"
        );
#endif
    }

    // 2 arguments
    template <typename A1, typename A2>
    inline void taskDefer(void* func, A1 arg1, A2 arg2) {
#ifdef __riscv
        asm volatile (
            "mv a0, %0; mv a1, %1; mv a2, %2; li a7, 49; ecall"
            :
            : "r"(func), "r"(to_reg(arg1)), "r"(to_reg(arg2))
            : "a0", "a1", "a2", "a7"
        );
#endif
    }

    // 3 arguments
    template <typename A1, typename A2, typename A3>
    inline void taskDefer(void* func, A1 arg1, A2 arg2, A3 arg3) {
#ifdef __riscv
        asm volatile (
            "mv a0, %0; mv a1, %1; mv a2, %2; mv a3, %3; li a7, 49; ecall"
            :
            : "r"(func), "r"(to_reg(arg1)), "r"(to_reg(arg2)),
              "r"(to_reg(arg3))
            : "a0", "a1", "a2", "a3", "a7"
        );
#endif
    }

    // 4 arguments
    template <typename A1, typename A2, typename A3, typename A4>
    inline void taskDefer(void* func, A1 arg1, A2 arg2, A3 arg3, A4 arg4) {
#ifdef __riscv
        asm volatile (
            "mv a0, %0; mv a1, %1; mv a2, %2; mv a3, %3; mv a4, %4; "
            "li a7, 49; ecall"
            :
            : "r"(func), "r"(to_reg(arg1)), "r"(to_reg(arg2)),
              "r"(to_reg(arg3)), "r"(to_reg(arg4))
            : "a0", "a1", "a2", "a3", "a4", "a7"
        );
#endif
    }

    // 5 arguments
    template <typename A1, typename A2, typename A3, typename A4, typename A5>
    inline void taskDefer(void* func, A1 arg1, A2 arg2, A3 arg3, A4 arg4,
                          A5 arg5) {
#ifdef __riscv
        asm volatile (
            "mv a0, %0; mv a1, %1; mv a2, %2; mv a3, %3; mv a4, %4; "
            "mv a5, %5; li a7, 49; ecall"
            :
            : "r"(func), "r"(to_reg(arg1)), "r"(to_reg(arg2)),
              "r"(to_reg(arg3)), "r"(to_reg(arg4)), "r"(to_reg(arg5))
            : "a0", "a1", "a2", "a3", "a4", "a5", "a7"
        );
#endif
    }

    // 6 arguments
    template <typename A1, typename A2, typename A3, typename A4, typename A5,
              typename A6>
    inline void taskDefer(void* func, A1 arg1, A2 arg2, A3 arg3, A4 arg4,
                          A5 arg5, A6 arg6) {
#ifdef __riscv
        asm volatile (
            "mv a0, %0; mv a1, %1; mv a2, %2; mv a3, %3; mv a4, %4; "
            "mv a5, %5; mv a6, %6; li a7, 49; ecall"
            :
            : "r"(func), "r"(to_reg(arg1)), "r"(to_reg(arg2)),
              "r"(to_reg(arg3)), "r"(to_reg(arg4)), "r"(to_reg(arg5)),
              "r"(to_reg(arg6))
            : "a0", "a1", "a2", "a3", "a4", "a5", "a6", "a7"
        );
#endif
    }

} // namespace Lua

#endif // LUA_HPP
