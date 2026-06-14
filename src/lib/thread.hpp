// thread.hpp — Multi-threading operations for this freestanding RISC-V environment
// Translates to task.spawn() in the Luau transpiler.
// Syscall 48: task.spawn(functionAddress, args...) — spawns a new thread
// Syscall 49: task.defer(functionAddress, args...)  — defers to next heartbeat
//
// Each spawned thread gets its own 64K stack from the heap, an isolated register
// file, and up to 6 arguments shifted so the spawned function sees its first
// argument in a0 (standard RISC-V calling convention).
//
// Supports any 32-bit argument type — int, void*, float — via template overloads.
// Captureless C++ lambdas work via the `+lambda` trick:
//     auto work = []() { ... };
//     Rbxl::taskSpawn((void*)+work);
//
// Float arguments are bit-cast to int via to_reg<T>(); the C++ compiler
// automatically emits fmv.x.w for hardfloat ABIs and does nothing for softfloat.
// The spawned function should cast back: float val; *(int*)&val = a0;

#ifndef THREAD_HPP
#define THREAD_HPP

namespace Rbxl {

    // ── Type-punning helper ──────────────────────────────────────────────
    // Safely converts any 32-bit value (int, void*, float) to an int for
    // register passing. The compiler handles float→int via fmv.x.w when
    // targeting hardfloat ABIs; does nothing for softfloat.
    template <typename T>
    inline int to_reg(T val) {
        static_assert(sizeof(T) == 4, "Only 32-bit types supported (int, void*, float)");
        union { T in; int out; } u;
        u.in = val;
        return u.out;
    }

    // ── taskSpawn: 0 arguments ─────────────────────────────────────────
    // Returns the thread ID (small integer) stored as void* for the C++ caller.
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

    // ── taskSpawn: 1 argument ──────────────────────────────────────────
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

    // ── taskSpawn: 2 arguments ─────────────────────────────────────────
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

    // ── taskSpawn: 3 arguments ─────────────────────────────────────────
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

    // ── taskSpawn: 4 arguments ─────────────────────────────────────────
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

    // ── taskSpawn: 5 arguments ─────────────────────────────────────────
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

    // ── taskSpawn: 6 arguments ─────────────────────────────────────────
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

    // ── taskDefer: 0 arguments ─────────────────────────────────────────
    inline void taskDefer(void* func) {
        asm volatile (
            "mv a0, %0; li a7, 49; ecall"
            :
            : "r"(func)
            : "a0", "a7"
        );
    }

    // ── taskDefer: 1 argument ──────────────────────────────────────────
    template <typename A1>
    inline void taskDefer(void* func, A1 arg1) {
        asm volatile (
            "mv a0, %0; mv a1, %1; li a7, 49; ecall"
            :
            : "r"(func), "r"(to_reg(arg1))
            : "a0", "a1", "a7"
        );
    }

    // ── taskDefer: 2 arguments ─────────────────────────────────────────
    template <typename A1, typename A2>
    inline void taskDefer(void* func, A1 arg1, A2 arg2) {
        asm volatile (
            "mv a0, %0; mv a1, %1; mv a2, %2; li a7, 49; ecall"
            :
            : "r"(func), "r"(to_reg(arg1)), "r"(to_reg(arg2))
            : "a0", "a1", "a2", "a7"
        );
    }

    // ── taskDefer: 3 arguments ─────────────────────────────────────────
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

    // ── taskDefer: 4 arguments ─────────────────────────────────────────
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

    // ── taskDefer: 5 arguments ─────────────────────────────────────────
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

    // ── taskDefer: 6 arguments ─────────────────────────────────────────
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

#endif // THREAD_HPP
