// crt.hpp — Freestanding C++ runtime stubs
// (-nostdlib environment has no __cxa_atexit or __dso_handle)

#ifndef CRT_HPP
#define CRT_HPP

extern "C" {
    void* __dso_handle = 0;
    int __cxa_atexit(void (*)(void*), void*, void*) { return 0; }
}

#endif // CRT_HPP
