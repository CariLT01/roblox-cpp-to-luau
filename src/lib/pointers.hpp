// pointers.hpp — Smart pointers and heap-allocation helpers for this
// freestanding RISC-V environment. No standard library dependencies.

#ifndef POINTERS_HPP
#define POINTERS_HPP

#include "types.hpp"
#include "heap.hpp"

// Placement new/delete — required for freestanding (-nostdlib) environments
// where the standard <new> header is not available.
inline void* operator new(unsigned int, void* ptr) { return ptr; }
inline void  operator delete(void*, void*) {}

// ── unique_ptr<T>: single-owner smart pointer ──
// Non-copyable. Frees the managed object automatically on destruction.
// Uses Rbxl::free() via operator delete.

template<typename T>
class unique_ptr {
    T* p;
public:
    unique_ptr() : p(nullptr) {}
    explicit unique_ptr(T* ptr) : p(ptr) {}

    ~unique_ptr() {
        if (p) {
            p->~T();
            Rbxl::free(p);
        }
    }

    // Accessors
    T* get() const { return p; }
    T& operator*() const { return *p; }
    T* operator->() const { return p; }

    // Boolean conversion
    typedef T* unique_ptr::*bool_type;
    operator bool_type() const { return p ? &unique_ptr::p : 0; }

    // Release ownership (returns raw pointer, caller responsible for cleanup)
    T* release() {
        T* tmp = p;
        p = nullptr;
        return tmp;
    }

    // Replace managed object (frees old, takes ownership of new)
    void reset(T* ptr = nullptr) {
        if (p) {
            p->~T();
            Rbxl::free(p);
        }
        p = ptr;
    }

    // Swap
    void swap(unique_ptr& other) {
        T* tmp = p;
        p = other.p;
        other.p = tmp;
    }

    // Comparison
    bool operator==(const unique_ptr& other) const { return p == other.p; }
    bool operator!=(const unique_ptr& other) const { return p != other.p; }
    bool operator!() const { return !p; }

private:
    // Non-copyable
    unique_ptr(const unique_ptr& other);
    unique_ptr& operator=(const unique_ptr& other);
};

// ── shared_ptr<T>: reference-counted smart pointer ──
// Multiple shared_ptr instances can own the same object. The object is
// destroyed when the last shared_ptr referencing it goes out of scope.

template<typename T>
class shared_ptr {
    T* p;
    unsigned int* rc;

    void _release() {
        if (rc) {
            (*rc)--;
            if (*rc == 0) {
                p->~T();
                Rbxl::free(p);
                Rbxl::free(rc);
            }
        }
        p = nullptr;
        rc = nullptr;
    }

public:
    shared_ptr() : p(nullptr), rc(nullptr) {}

    explicit shared_ptr(T* ptr) : p(ptr), rc(nullptr) {
        if (p) {
            rc = (unsigned int*)Rbxl::malloc(sizeof(unsigned int));
            *rc = 1;
        }
    }

    ~shared_ptr() { _release(); }

    // Copy
    shared_ptr(const shared_ptr& other) : p(other.p), rc(other.rc) {
        if (rc) (*rc)++;
    }

    shared_ptr& operator=(const shared_ptr& other) {
        if (this != &other) {
            _release();
            p = other.p;
            rc = other.rc;
            if (rc) (*rc)++;
        }
        return *this;
    }

    // Accessors
    T* get() const { return p; }
    T& operator*() const { return *p; }
    T* operator->() const { return p; }

    unsigned int use_count() const { return rc ? *rc : 0; }

    // Boolean conversion
    typedef T* shared_ptr::*bool_type;
    operator bool_type() const { return p ? &shared_ptr::p : 0; }

    // Reset
    void reset(T* ptr = nullptr) {
        _release();
        p = ptr;
        rc = nullptr;
        if (p) {
            rc = (unsigned int*)Rbxl::malloc(sizeof(unsigned int));
            *rc = 1;
        }
    }

    void swap(shared_ptr& other) {
        T* tmp_p = p; p = other.p; other.p = tmp_p;
        unsigned int* tmp_rc = rc; rc = other.rc; other.rc = tmp_rc;
    }

    // Comparison
    bool operator==(const shared_ptr& other) const { return p == other.p; }
    bool operator!=(const shared_ptr& other) const { return p != other.p; }
    bool operator!() const { return !p; }
};

// ── Heap allocation helpers ──
// Allocate memory from the virtual heap and construct an object in-place.
// Mirrors the pattern used by vector<T> and map<K,V> in this codebase.

// Allocate raw memory for T (does NOT call constructor)
template<typename T>
T* heap_alloc() {
    return (T*)Rbxl::malloc(sizeof(T));
}

// Free and destroy a heap-allocated object
template<typename T>
void heap_free(T* ptr) {
    if (ptr) {
        ptr->~T();
        Rbxl::free(ptr);
    }
}

// ── Stack-to-heap helpers ──
// Copy a stack-allocated object onto the heap and wrap in a smart pointer.
// The original stack object remains valid (it is copied, not moved).

template<typename T>
unique_ptr<T> move_to_heap(const T& stack_obj) {
    T* ptr = (T*)Rbxl::malloc(sizeof(T));
    if (!ptr) return unique_ptr<T>();
    new (ptr) T(stack_obj);  // copy-construct on heap
    return unique_ptr<T>(ptr);
}

template<typename T>
shared_ptr<T> move_to_shared(const T& stack_obj) {
    T* ptr = (T*)Rbxl::malloc(sizeof(T));
    if (!ptr) return shared_ptr<T>();
    new (ptr) T(stack_obj);  // copy-construct on heap
    return shared_ptr<T>(ptr);
}

// ── make_unique: create a unique_ptr with constructor args ──

template<typename T>
unique_ptr<T> make_unique() {
    T* ptr = (T*)Rbxl::malloc(sizeof(T));
    new (ptr) T();
    return unique_ptr<T>(ptr);
}

template<typename T, typename A1>
unique_ptr<T> make_unique(const A1& a1) {
    T* ptr = (T*)Rbxl::malloc(sizeof(T));
    new (ptr) T(a1);
    return unique_ptr<T>(ptr);
}

template<typename T, typename A1, typename A2>
unique_ptr<T> make_unique(const A1& a1, const A2& a2) {
    T* ptr = (T*)Rbxl::malloc(sizeof(T));
    new (ptr) T(a1, a2);
    return unique_ptr<T>(ptr);
}

// ── make_shared: create a shared_ptr with constructor args ──

template<typename T>
shared_ptr<T> make_shared() {
    T* ptr = (T*)Rbxl::malloc(sizeof(T));
    new (ptr) T();
    return shared_ptr<T>(ptr);
}

template<typename T, typename A1>
shared_ptr<T> make_shared(const A1& a1) {
    T* ptr = (T*)Rbxl::malloc(sizeof(T));
    new (ptr) T(a1);
    return shared_ptr<T>(ptr);
}

template<typename T, typename A1, typename A2>
shared_ptr<T> make_shared(const A1& a1, const A2& a2) {
    T* ptr = (T*)Rbxl::malloc(sizeof(T));
    new (ptr) T(a1, a2);
    return shared_ptr<T>(ptr);
}

#endif // POINTERS_HPP
