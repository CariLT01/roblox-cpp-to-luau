// heap.hpp — Virtual heap operations and vector<T> dynamic array
// for this freestanding RISC-V environment. No standard library dependencies.



#ifndef HEAP_HPP
#define HEAP_HPP

#include "types.hpp"

namespace Rbxl {
    // Syscall 30: Allocate 'size' bytes from the virtual heap, returns pointer or null (0)
    void* malloc(unsigned int size) {
        void* ptr = nullptr;
#ifdef __riscv
        asm volatile (
            "mv a0, %1; li a7, 30; ecall; mv %0, a0"
            : "=r"(ptr)
            : "r"(size)
            : "a0", "a7"
        );
#endif
        return ptr;
    }

    // Syscall 31: Free a previously allocated heap pointer
    void free(void* ptr) {
#ifdef __riscv
        asm volatile (
            "mv a0, %0; li a7, 31; ecall"
            :
            : "r"(ptr)
            : "a0", "a7"
        );
#endif
    }

    // Syscall 32: Get current virtual heap usage in bytes
    unsigned int heapUsed() {
        unsigned int result = 0;
#ifdef __riscv
        asm volatile (
            "li a7, 32; ecall; mv %0, a0"
            : "=r"(result)
            :
            : "a0", "a7"
        );
#endif
        return result;
    }
}

// ── vector<T>: simple dynamic array using the virtual heap ──
template<typename T>
class vector {
    T* d;
    unsigned int sz;
    unsigned int cap;
public:
    vector() : d(nullptr), sz(0), cap(0) {}
    ~vector() { if (d) Rbxl::free(d); }

    void push_back(const T& value) {
        if (sz >= cap) {
            unsigned int nc = cap ? cap * 2 : 4;
            T* nd = (T*)Rbxl::malloc(nc * sizeof(T));
            for (unsigned int i = 0; i < sz; i++) nd[i] = d[i];
            if (d) Rbxl::free(d);
            d = nd;
            cap = nc;
        }
        d[sz] = value;
        sz++;
    }

    void pop_back() { if (sz > 0) sz--; }
    void clear() { sz = 0; }

    T& operator[](unsigned int i) { return d[i]; }
    const T& operator[](unsigned int i) const { return d[i]; }

    unsigned int size() const { return sz; }
    bool empty() const { return sz == 0; }

    T* begin() { return d; }
    T* end() { return d + sz; }
    const T* begin() const { return d; }
    const T* end() const { return d + sz; }
};


int decodeVarint(const vector<uint8_t>& data, int& index, int* bytesRead) {
    int result = 0;
    int shift = 0;

    while (index < data.size()) {
        int byte = data[index++];

        result |= static_cast<int>(byte & 0x7F) << shift;

        // If MSB is not set, this is the last byte

        *bytesRead += 1;

        if ((byte & 0x80) == 0) {
            return result;
        }

        shift += 7;

        // Safety check (varint should not exceed 10 bytes for 64-bit)
        if (shift >= 64) {
            
        }
    }

    return result;

}

#endif // HEAP_HPP
