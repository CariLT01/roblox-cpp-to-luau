// lua.hpp — Lua standard library bindings for this freestanding RISC-V environment
//
// Functions that map directly to Lua globals / standard libraries:
//   print()         → Lua print()
//   taskWait()      → task.wait()
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

    // ── print() ──────────────────────────────────────────────────────────

    // Syscall 4: print(const char*)
    inline void print(const char* str) {
        asm volatile ("mv a0, %0; li a7, 4; ecall" : : "r"(str) : "a0", "a7");
    }

    // Syscall 5: print(int)
    inline void print(int val) {
        asm volatile ("mv a0, %0; li a7, 5; ecall" : : "r"(val) : "a0", "a7");
    }

    // Syscall 6: print(bool)
    inline void print(bool val) {
        asm volatile ("mv a0, %0; li a7, 6; ecall" : : "r"((int)val) : "a0", "a7");
    }

    // Syscall 7: print(float) — passed via RAM pointer
    inline void print(float val) {
        volatile float v = val;
        volatile float* ptr = &v;
        asm volatile ("mv a0, %0; li a7, 7; ecall" : : "r"(ptr) : "a0", "a7", "memory");
    }

    // ── task.wait() ──────────────────────────────────────────────────────

    // Syscall 45: task.wait(seconds) — yields for n seconds, returns elapsed
    inline float taskWait(float seconds) {
        float result = 0.0f;
        asm volatile (
            "mv a0, %1; li a7, 45; ecall; mv %0, a0"
            : "=r"(result)
            : "r"(seconds)
            : "a0", "a7"
        );
        return result;
    }

    // ── task.spawn() ─────────────────────────────────────────────────────
    // Syscall 48.  Returns the thread ID (small integer) as void*.

    // 0 arguments
    inline void* taskSpawn(void* func) {
        void* handle = nullptr;
        asm volatile (
            "mv a0, %1; li a7, 48; ecall; mv %0, a0"
            : "=r"(handle)
            : "r"(func)
            : "a0", "a7"
        );
        return handle;
    }

    // 1 argument
    template <typename A1>
    inline void* taskSpawn(void* func, A1 arg1) {
        void* handle = nullptr;
        asm volatile (
            "mv a0, %1; mv a1, %2; li a7, 48; ecall; mv %0, a0"
            : "=r"(handle)
            : "r"(func), "r"(to_reg(arg1))
            : "a0", "a1", "a7"
        );
        return handle;
    }

    // 2 arguments
    template <typename A1, typename A2>
    inline void* taskSpawn(void* func, A1 arg1, A2 arg2) {
        void* handle = nullptr;
        asm volatile (
            "mv a0, %1; mv a1, %2; mv a2, %3; li a7, 48; ecall; mv %0, a0"
            : "=r"(handle)
            : "r"(func), "r"(to_reg(arg1)), "r"(to_reg(arg2))
            : "a0", "a1", "a2", "a7"
        );
        return handle;
    }

    // 3 arguments
    template <typename A1, typename A2, typename A3>
    inline void* taskSpawn(void* func, A1 arg1, A2 arg2, A3 arg3) {
        void* handle = nullptr;
        asm volatile (
            "mv a0, %1; mv a1, %2; mv a2, %3; mv a3, %4; li a7, 48; ecall; mv %0, a0"
            : "=r"(handle)
            : "r"(func), "r"(to_reg(arg1)), "r"(to_reg(arg2)), "r"(to_reg(arg3))
            : "a0", "a1", "a2", "a3", "a7"
        );
        return handle;
    }

    // 4 arguments
    template <typename A1, typename A2, typename A3, typename A4>
    inline void* taskSpawn(void* func, A1 arg1, A2 arg2, A3 arg3, A4 arg4) {
        void* handle = nullptr;
        asm volatile (
            "mv a0, %1; mv a1, %2; mv a2, %3; mv a3, %4; mv a4, %5; "
            "li a7, 48; ecall; mv %0, a0"
            : "=r"(handle)
            : "r"(func), "r"(to_reg(arg1)), "r"(to_reg(arg2)),
              "r"(to_reg(arg3)), "r"(to_reg(arg4))
            : "a0", "a1", "a2", "a3", "a4", "a7"
        );
        return handle;
    }

    // 5 arguments
    template <typename A1, typename A2, typename A3, typename A4, typename A5>
    inline void* taskSpawn(void* func, A1 arg1, A2 arg2, A3 arg3, A4 arg4,
                           A5 arg5) {
        void* handle = nullptr;
        asm volatile (
            "mv a0, %1; mv a1, %2; mv a2, %3; mv a3, %4; mv a4, %5; "
            "mv a5, %6; li a7, 48; ecall; mv %0, a0"
            : "=r"(handle)
            : "r"(func), "r"(to_reg(arg1)), "r"(to_reg(arg2)),
              "r"(to_reg(arg3)), "r"(to_reg(arg4)), "r"(to_reg(arg5))
            : "a0", "a1", "a2", "a3", "a4", "a5", "a7"
        );
        return handle;
    }

    // 6 arguments
    template <typename A1, typename A2, typename A3, typename A4, typename A5,
              typename A6>
    inline void* taskSpawn(void* func, A1 arg1, A2 arg2, A3 arg3, A4 arg4,
                           A5 arg5, A6 arg6) {
        void* handle = nullptr;
        asm volatile (
            "mv a0, %1; mv a1, %2; mv a2, %3; mv a3, %4; mv a4, %5; "
            "mv a5, %6; mv a6, %7; li a7, 48; ecall; mv %0, a0"
            : "=r"(handle)
            : "r"(func), "r"(to_reg(arg1)), "r"(to_reg(arg2)),
              "r"(to_reg(arg3)), "r"(to_reg(arg4)), "r"(to_reg(arg5)),
              "r"(to_reg(arg6))
            : "a0", "a1", "a2", "a3", "a4", "a5", "a6", "a7"
        );
        return handle;
    }

    // ── task.defer() ─────────────────────────────────────────────────────
    // Syscall 49.  Defers function to next heartbeat.

    // 0 arguments
    inline void taskDefer(void* func) {
        asm volatile (
            "mv a0, %0; li a7, 49; ecall"
            :
            : "r"(func)
            : "a0", "a7"
        );
    }

    // 1 argument
    template <typename A1>
    inline void taskDefer(void* func, A1 arg1) {
        asm volatile (
            "mv a0, %0; mv a1, %1; li a7, 49; ecall"
            :
            : "r"(func), "r"(to_reg(arg1))
            : "a0", "a1", "a7"
        );
    }

    // 2 arguments
    template <typename A1, typename A2>
    inline void taskDefer(void* func, A1 arg1, A2 arg2) {
        asm volatile (
            "mv a0, %0; mv a1, %1; mv a2, %2; li a7, 49; ecall"
            :
            : "r"(func), "r"(to_reg(arg1)), "r"(to_reg(arg2))
            : "a0", "a1", "a2", "a7"
        );
    }

    // 3 arguments
    template <typename A1, typename A2, typename A3>
    inline void taskDefer(void* func, A1 arg1, A2 arg2, A3 arg3) {
        asm volatile (
            "mv a0, %0; mv a1, %1; mv a2, %2; mv a3, %3; li a7, 49; ecall"
            :
            : "r"(func), "r"(to_reg(arg1)), "r"(to_reg(arg2)),
              "r"(to_reg(arg3))
            : "a0", "a1", "a2", "a3", "a7"
        );
    }

    // 4 arguments
    template <typename A1, typename A2, typename A3, typename A4>
    inline void taskDefer(void* func, A1 arg1, A2 arg2, A3 arg3, A4 arg4) {
        asm volatile (
            "mv a0, %0; mv a1, %1; mv a2, %2; mv a3, %3; mv a4, %4; "
            "li a7, 49; ecall"
            :
            : "r"(func), "r"(to_reg(arg1)), "r"(to_reg(arg2)),
              "r"(to_reg(arg3)), "r"(to_reg(arg4))
            : "a0", "a1", "a2", "a3", "a4", "a7"
        );
    }

    // 5 arguments
    template <typename A1, typename A2, typename A3, typename A4, typename A5>
    inline void taskDefer(void* func, A1 arg1, A2 arg2, A3 arg3, A4 arg4,
                          A5 arg5) {
        asm volatile (
            "mv a0, %0; mv a1, %1; mv a2, %2; mv a3, %3; mv a4, %4; "
            "mv a5, %5; li a7, 49; ecall"
            :
            : "r"(func), "r"(to_reg(arg1)), "r"(to_reg(arg2)),
              "r"(to_reg(arg3)), "r"(to_reg(arg4)), "r"(to_reg(arg5))
            : "a0", "a1", "a2", "a3", "a4", "a5", "a7"
        );
    }

    // 6 arguments
    template <typename A1, typename A2, typename A3, typename A4, typename A5,
              typename A6>
    inline void taskDefer(void* func, A1 arg1, A2 arg2, A3 arg3, A4 arg4,
                          A5 arg5, A6 arg6) {
        asm volatile (
            "mv a0, %0; mv a1, %1; mv a2, %2; mv a3, %3; mv a4, %4; "
            "mv a5, %5; mv a6, %6; li a7, 49; ecall"
            :
            : "r"(func), "r"(to_reg(arg1)), "r"(to_reg(arg2)),
              "r"(to_reg(arg3)), "r"(to_reg(arg4)), "r"(to_reg(arg5)),
              "r"(to_reg(arg6))
            : "a0", "a1", "a2", "a3", "a4", "a5", "a6", "a7"
        );
    }

} // namespace Rbxl

#endif // LUA_HPP
