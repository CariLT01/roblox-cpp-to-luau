// rbxl.hpp — Roblox API bindings for this freestanding RISC-V environment
//
// Everything is a handle. Only two property syscalls: getPropertyObject / setPropertyObject.
// Struct types (Vector3, CFrame, Color3, UDim2) have readFromObject / toObject bridge.
// Primitives go through OBJECTS table as handles too.
// No PartWrapper, no lifecycle syscalls — all done via callMethod or getPropertyObject.

#pragma once

#ifndef RBXL_HPP
#define RBXL_HPP

#include "heap.hpp"
#include "lua.hpp"
#include "math.hpp"
#include "enums.hpp"

// ── callObj flags (payload-based call, syscall 75) ──────────────────────────
//
// callObj uses a payload buffer: [header(4B) | fnHandle(4B) | argHandles...]
// The header encodes (handleCount << 16) | (flags & 0xFFFF).
// Only bit 0 is meaningful; all other flags were for the removed
// register-based call (syscall 65) and are now dead.
// All return values are always OBJECTS handles.
//
#define RBXL_METHOD_HAS_RETURN_BIT            (1 << 0)  // call returns a value (always an OBJECTS handle)


// ── C++ struct types (math on heap, bridge to/from OBJECTS) ──────────────────

struct Vector3 {
    float x, y, z;
    Vector3() : x(0), y(0), z(0) {}
    Vector3(float x_, float y_, float z_) : x(x_), y(y_), z(z_) {}

    // objectRead 78: Read Vector3 (type_id=0) from OBJECTS[handle] into *this
    void readFromObject(void* objHandle) {
#ifdef __riscv
        asm volatile (
            "mv a0, %0; li a1, 0; mv a2, %1; li a7, 78; ecall"
            :
            : "r"(objHandle), "r"(this)
            : "a0", "a1", "a2", "a7", "memory"
        );
#endif
    }
    // objectWrite 79: Store this Vector3 (type_id=0) into OBJECTS, return handle
    void* toObject() const {
        void* handle = nullptr;
#ifdef __riscv
        asm volatile (
            "mv a0, %1; li a1, 0; li a7, 79; ecall; mv %0, a0"
            : "=r"(handle)
            : "r"(this)
            : "a0", "a1", "a7", "memory"
        );
#endif
        return handle;
    }
};

struct Color3 {
    float r, g, b;
    Color3() : r(0), g(0), b(0) {}
    Color3(float r_, float g_, float b_) : r(r_), g(g_), b(b_) {}

    // objectRead 78: Read Color3 (type_id=2) from OBJECTS[handle] into *this
    void readFromObject(void* objHandle) {
#ifdef __riscv
        asm volatile (
            "mv a0, %0; li a1, 2; mv a2, %1; li a7, 78; ecall"
            :
            : "r"(objHandle), "r"(this)
            : "a0", "a1", "a2", "a7", "memory"
        );
#endif
    }
    // objectWrite 79: Store this Color3 (type_id=2) into OBJECTS, return handle
    void* toObject() const {
        void* handle = nullptr;
#ifdef __riscv
        asm volatile (
            "mv a0, %1; li a1, 2; li a7, 79; ecall; mv %0, a0"
            : "=r"(handle)
            : "r"(this)
            : "a0", "a1", "a7", "memory"
        );
#endif
        return handle;
    }
};

// ── UDim2: 4-float 2D size/position (X.Scale, X.Offset, Y.Scale, Y.Offset) ──
struct UDim2 {
    float d[4];

    // objectRead 78: Read UDim2 (type_id=3) from OBJECTS[handle] into *this
    void readFromObject(void* objHandle) {
#ifdef __riscv
        asm volatile (
            "mv a0, %0; li a1, 3; mv a2, %1; li a7, 78; ecall"
            :
            : "r"(objHandle), "r"(this)
            : "a0", "a1", "a2", "a7", "memory"
        );
#endif
    }
    // objectWrite 79: Store this UDim2 (type_id=3) into OBJECTS, return handle
    void* toObject() const {
        void* handle = nullptr;
#ifdef __riscv
        asm volatile (
            "mv a0, %1; li a1, 3; li a7, 79; ecall; mv %0, a0"
            : "=r"(handle)
            : "r"(this)
            : "a0", "a1", "a7", "memory"
        );
#endif
        return handle;
    }

    UDim2() {
        d[0] = 0.0f; d[1] = 0.0f; d[2] = 0.0f; d[3] = 0.0f;
    }
    UDim2(float xScale, float xOffset, float yScale, float yOffset) {
        d[0] = xScale; d[1] = xOffset; d[2] = yScale; d[3] = yOffset;
    }

    float xScale()  const { return d[0]; }
    float xOffset() const { return d[1]; }
    float yScale()  const { return d[2]; }
    float yOffset() const { return d[3]; }
};

struct CFrame {
    float d[12];

    // objectRead 78: Read CFrame (type_id=1) from OBJECTS[handle] into *this
    void readFromObject(void* objHandle) {
#ifdef __riscv
        asm volatile (
            "mv a0, %0; li a1, 1; mv a2, %1; li a7, 78; ecall"
            :
            : "r"(objHandle), "r"(this)
            : "a0", "a1", "a2", "a7", "memory"
        );
#endif
    }
    // objectWrite 79: Store this CFrame (type_id=1) into OBJECTS, return handle
    void* toObject() const {
        void* handle = nullptr;
#ifdef __riscv
        asm volatile (
            "mv a0, %1; li a1, 1; li a7, 79; ecall; mv %0, a0"
            : "=r"(handle)
            : "r"(this)
            : "a0", "a1", "a7", "memory"
        );
#endif
        return handle;
    }

    CFrame() {
        for (int i = 0; i < 12; i++) d[i] = 0.0f;
        d[0] = 0.0f; d[1] = 0.0f; d[2] = 0.0f;
        d[3] = 1.0f; d[4] = 0.0f; d[5] = 0.0f;
        d[6] = 0.0f; d[7] = 1.0f; d[8] = 0.0f;
        d[9] = 0.0f; d[10] = 0.0f; d[11] = 1.0f;
    }
    CFrame(float px, float py, float pz) {
        for (int i = 0; i < 12; i++) d[i] = 0.0f;
        d[0] = px; d[1] = py; d[2] = pz;
        d[3] = 1.0f; d[7] = 1.0f; d[11] = 1.0f;
    }
    CFrame(float px, float py, float pz,
           float r00, float r01, float r02,
           float r10, float r11, float r12,
           float r20, float r21, float r22) {
        d[0] = px; d[1] = py; d[2] = pz;
        d[3] = r00; d[4] = r01; d[5] = r02;
        d[6] = r10; d[7] = r11; d[8] = r12;
        d[9] = r20; d[10] = r21; d[11] = r22;
    }

    void pos(float& x, float& y, float& z) const { x = d[0]; y = d[1]; z = d[2]; }
    float x() const { return d[0]; }
    float y() const { return d[1]; }
    float z() const { return d[2]; }

    Vector3 getPosition() const { return Vector3(d[0], d[1], d[2]); }
    Vector3 getLookVector() const { return Vector3(-d[5], -d[8], -d[11]); }
    Vector3 getRightVector() const { return Vector3(d[3], d[6], d[9]); }
    Vector3 getUpVector() const { return Vector3(d[4], d[7], d[10]); }
    Vector3 getXVector() const { return Vector3(d[3], d[6], d[9]); }
    Vector3 getYVector() const { return Vector3(d[4], d[7], d[10]); }
    Vector3 getZVector() const { return Vector3(-d[5], -d[8], -d[11]); }
};

// Vector3 math helpers used by CFrame
namespace { inline Vector3 v3_cross(const Vector3& a, const Vector3& b) { return Vector3(a.y*b.z - a.z*b.y, a.z*b.x - a.x*b.z, a.x*b.y - a.y*b.x); } }
namespace { inline Vector3 v3_sub(const Vector3& a, const Vector3& b) { return Vector3(a.x-b.x, a.y-b.y, a.z-b.z); } }
namespace { inline Vector3 v3_add(const Vector3& a, const Vector3& b) { return Vector3(a.x+b.x, a.y+b.y, a.z+b.z); } }
namespace { inline Vector3 v3_mul(const Vector3& a, float s) { return Vector3(a.x*s, a.y*s, a.z*s); } }
namespace { inline Vector3 v3_unit(const Vector3& v) { float len = v.x*v.x+v.y*v.y+v.z*v.z; if (len > 0.000001f) { float x2 = len * 0.5f; int i = *(int*)&len; i = 0x5f3759df - (i >> 1); float y = *(float*)&i; y = y * (1.5f - x2 * y * y); y = y * (1.5f - x2 * y * y); return v3_mul(v, y); } return v; } }

inline CFrame cframe_lookAt(const Vector3& pos, const Vector3& target) {
    Vector3 forward = v3_unit(v3_sub(target, pos));
    Vector3 worldUp(0.0f, 1.0f, 0.0f);
    Vector3 right = v3_unit(v3_cross(forward, worldUp));
    Vector3 up = v3_cross(right, forward);
    return CFrame(pos.x, pos.y, pos.z, right.x, up.x, -forward.x, right.y, up.y, -forward.y, right.z, up.z, -forward.z);
}
inline CFrame cframe_mul(const CFrame& a, const CFrame& b) {
    float px = a.d[3]*b.d[0] + a.d[4]*b.d[1] + a.d[5]*b.d[2] + a.d[0];
    float py = a.d[6]*b.d[0] + a.d[7]*b.d[1] + a.d[8]*b.d[2] + a.d[1];
    float pz = a.d[9]*b.d[0] + a.d[10]*b.d[1] + a.d[11]*b.d[2] + a.d[2];
    float r00 = a.d[3]*b.d[3] + a.d[4]*b.d[6] + a.d[5]*b.d[9];
    float r01 = a.d[3]*b.d[4] + a.d[4]*b.d[7] + a.d[5]*b.d[10];
    float r02 = a.d[3]*b.d[5] + a.d[4]*b.d[8] + a.d[5]*b.d[11];
    float r10 = a.d[6]*b.d[3] + a.d[7]*b.d[6] + a.d[8]*b.d[9];
    float r11 = a.d[6]*b.d[4] + a.d[7]*b.d[7] + a.d[8]*b.d[10];
    float r12 = a.d[6]*b.d[5] + a.d[7]*b.d[8] + a.d[8]*b.d[11];
    float r20 = a.d[9]*b.d[3] + a.d[10]*b.d[6] + a.d[11]*b.d[9];
    float r21 = a.d[9]*b.d[4] + a.d[10]*b.d[7] + a.d[11]*b.d[10];
    float r22 = a.d[9]*b.d[5] + a.d[10]*b.d[8] + a.d[11]*b.d[11];
    return CFrame(px, py, pz, r00, r01, r02, r10, r11, r12, r20, r21, r22);
}
inline CFrame cframe_inverse(const CFrame& cf) {
    float r00=cf.d[3], r01=cf.d[6], r02=cf.d[9];
    float r10=cf.d[4], r11=cf.d[7], r12=cf.d[10];
    float r20=cf.d[5], r21=cf.d[8], r22=cf.d[11];
    float px = -(r00*cf.d[0] + r01*cf.d[1] + r02*cf.d[2]);
    float py = -(r10*cf.d[0] + r11*cf.d[1] + r12*cf.d[2]);
    float pz = -(r20*cf.d[0] + r21*cf.d[1] + r22*cf.d[2]);
    return CFrame(px, py, pz, r00, r01, r02, r10, r11, r12, r20, r21, r22);
}
inline Vector3 cframe_pointToWorld(const CFrame& cf, const Vector3& v) {
    return Vector3(cf.d[3]*v.x + cf.d[4]*v.y + cf.d[5]*v.z + cf.d[0], cf.d[6]*v.x + cf.d[7]*v.y + cf.d[8]*v.z + cf.d[1], cf.d[9]*v.x + cf.d[10]*v.y + cf.d[11]*v.z + cf.d[2]);
}
inline Vector3 cframe_pointToObject(const CFrame& cf, const Vector3& v) {
    return cframe_pointToWorld(cframe_inverse(cf), v);
}
inline Vector3 cframe_vectorToWorld(const CFrame& cf, const Vector3& v) {
    return Vector3(cf.d[3]*v.x + cf.d[4]*v.y + cf.d[5]*v.z, cf.d[6]*v.x + cf.d[7]*v.y + cf.d[8]*v.z, cf.d[9]*v.x + cf.d[10]*v.y + cf.d[11]*v.z);
}
inline Vector3 cframe_vectorToObject(const CFrame& cf, const Vector3& v) {
    return Vector3(cf.d[3]*v.x + cf.d[6]*v.y + cf.d[9]*v.z, cf.d[4]*v.x + cf.d[7]*v.y + cf.d[10]*v.z, cf.d[5]*v.x + cf.d[8]*v.y + cf.d[11]*v.z);
}
inline CFrame cframe_fromEulerAngles(float rx, float ry, float rz) {
    float sx = math::sin(rx); float cx = math::cos(rx);
    float sy = math::sin(ry); float cy = math::cos(ry);
    float sz = math::sin(rz); float cz = math::cos(rz);
    float r00 = cy * cz, r10 = cy * sz, r20 = -sy;
    float r01 = sx * sy * cz - cx * sz, r11 = sx * sy * sz + cx * cz, r21 = sx * cy;
    float r02 = cx * sy * cz + sx * sz, r12 = cx * sy * sz - sx * cz, r22 = cx * cy;
    return CFrame(0.0f, 0.0f, 0.0f, r00, r01, r02, r10, r11, r12, r20, r21, r22);
}


// Forward declaration needed by call() overloads that take const LuaObj&
class LuaObj;

// ── Rbxl namespace: raw syscall wrappers ──────────────────────────────────────

namespace Rbxl {

    // ── Math Operations (universal handle API) ──
    // Calls math.rad()/sin()/cos() via: read float → objectWrite (79) →
    // getGlobal("math") (52) → getPropertyObject (62) → callObj (75) →
    // objectRead (78) → write float back.

    void rad(void* ptr) {
        float val = *(float*)ptr;
        *(float*)ptr = math::detail::_math_op("rad", val);
    }

    void sin(void* ptr) {
        float val = *(float*)ptr;
        *(float*)ptr = math::detail::_math_op("sin", val);
    }

    void cos(void* ptr) {
        float val = *(float*)ptr;
        *(float*)ptr = math::detail::_math_op("cos", val);
    }

    // ── Object Property Access (the ONLY two property syscalls) ──

    // Syscall 62: getPropertyObject(handle, propName) — returns any property as an object handle
    void* getPropertyObject(void* handle, const char* propName) {
        void* result = nullptr;
#ifdef __riscv
        asm volatile ("mv a0, %1; mv a1, %2; li a7, 62; ecall; mv %0, a0" : "=r"(result) : "r"(handle), "r"(propName) : "a0", "a1", "a7");
#endif
        return result;
    }

    // Syscall 63: setPropertyObject(handle, propName, valueHandle) — sets a property from an OBJECTS handle
    void setPropertyObject(void* handle, const char* propName, void* valueHandle) {
#ifdef __riscv
        asm volatile ("mv a0, %0; mv a1, %1; mv a2, %2; li a7, 63; ecall" : : "r"(handle), "r"(propName), "r"(valueHandle) : "a0", "a1", "a2", "a7");
#endif
    }

    // Syscall 64: releaseObject(handle) — removes an entry from OBJECTS without destroying the Instance
    void releaseObject(void* handle) {
#ifdef __riscv
        asm volatile ("mv a0, %0; li a7, 64; ecall" : : "r"(handle) : "a0", "a7");
#endif
    }

    // ── Enum ↔ OBJECTS bridge (syscalls 42/43) ──

    // Syscall 42: fromEnum(enumIndex) — converts C++ enum index → OBJECTS handle
    // Looks up ENUMS[index + 1], stores the Roblox EnumItem in OBJECTS, returns handle.
    void* fromEnum(int enumIndex) {
        void* handle = nullptr;
#ifdef __riscv
        asm volatile ("mv a0, %1; li a7, 42; ecall; mv %0, a0" : "=r"(handle) : "r"(enumIndex) : "a0", "a7");
#endif
        return handle;
    }

    // Syscall 43: toEnum(handle) — converts OBJECTS handle → C++ enum index
    // Looks up OBJECTS[handle] in ENUM_TO_INDEX, returns the index.
    int toEnum(void* handle) {
        int result = 0;
#ifdef __riscv
        asm volatile ("mv a0, %1; li a7, 43; ecall; mv %0, a0" : "=r"(result) : "r"(handle) : "a0", "a7");
#endif
        return result;
    }

    // ── Service / Global / Method Lookups ──

    // Syscall 47: getService(name) — returns raw handle to any Roblox service instance
    void* getService(const char* name) {
        void* handle = nullptr;
#ifdef __riscv
        asm volatile ("mv a0, %1; li a7, 47; ecall; mv %0, a0" : "=r"(handle) : "r"(name) : "a0", "a7");
#endif
        return handle;
    }

    // Syscall 52: getGlobal(name) — returns the named Lua global as a handle
    void* getGlobal(const char* name) {
        void* handle = nullptr;
#ifdef __riscv
        asm volatile ("mv a0, %1; li a7, 52; ecall; mv %0, a0" : "=r"(handle) : "r"(name) : "a0", "a7");
#endif
        return handle;
    }

    // Syscall 51: getMethod(handle, methodName) — returns RBXScriptSignal handle
    void* getMethod(void* handle, const char* methodName) {
        void* result = nullptr;
#ifdef __riscv
        asm volatile ("mv a0, %1; mv a1, %2; li a7, 51; ecall; mv %0, a0" : "=r"(result) : "r"(handle), "r"(methodName) : "a0", "a1", "a7");
#endif
        return result;
    }

    // Syscall 53: require — requires a ModuleScript instance, returns handle
    void* require(void* moduleHandle) {
        void* handle = nullptr;
#ifdef __riscv
        asm volatile ("mv a0, %1; li a7, 53; ecall; mv %0, a0" : "=r"(handle) : "r"(moduleHandle) : "a0", "a7");
#endif
        return handle;
    }

    // ── Syscall 75: payload-stack call — all args are OBJECTS handles ──
    // Writes (count<<16|flags, fnHandle, args...) to a stack-local buffer and
    // passes its address via a0.  The Luau handler reads the payload through
    // read_mem32 and constructs the call.
    //
    // All args MUST be void* (OBJECTS handles).  Callers with LuaObj args should
    // use LuaObj::callObj() which extracts handles automatically.

    // Helper: identity for void* (handles); .handle() for LuaObj
    inline void* _obj_handle(void* h) { return h; }
    inline void* _obj_handle(const void* h) { return const_cast<void*>(h); }
    inline void* _obj_handle(const class LuaObj& obj);  // defined after LuaObj

    // Single variadic template — supports any number of OBJECTS handle args.
    // Uses a stack-local buffer (via __builtin_alloca) and fold expressions
    // to write header + fn + N handles sequentially.
    template<typename... Args>
    void* callObj(void* fnHandle, int flags, const Args&... args) {
        constexpr int N = sizeof...(Args);
        const int totalSize = 8 + N * 4;  // header(4) + fn(4) + N handles(4 each)

        unsigned int* p = (unsigned int*)__builtin_alloca(totalSize);
        p[0] = (((unsigned int)N) << 16) | ((unsigned int)flags & 0xFFFF);
        p[1] = (unsigned int)(uintptr_t)fnHandle;
        int i = 2;
        ((p[i++] = (unsigned int)(uintptr_t)_obj_handle(args)), ...);

        void* result = nullptr;
#ifdef __riscv
        asm volatile("mv a0, %1; li a7, 75; ecall; mv %0, a0"
            : "=r"(result) : "r"(p) : "a0", "a7", "memory");
#endif
        return result;
    }

}

// ── LuaObj: base handle class for ALL Roblox objects ──────────────────────────
// Everything is a handle. No typed property accessors — use getPropertyObject
// and setPropertyObject for ALL property access. Struct types use readFromObject /
// toObject bridge.

class LuaObj {
protected:
    void* h;
public:
    LuaObj() : h(nullptr) {}
    explicit LuaObj(void* handle) : h(handle) {}

    // RAII: auto-release the OBJECTS handle on destruction.
    ~LuaObj() { release(); }

    // Non-copyable — handles represent unique ownership (like unique_ptr).
    LuaObj(const LuaObj&) = delete;
    LuaObj& operator=(const LuaObj&) = delete;

    // Movable — transfers ownership, source becomes nullptr.
    LuaObj(LuaObj&& other) noexcept : h(other.h) { other.h = nullptr; }
    LuaObj& operator=(LuaObj&& other) noexcept {
        if (this != &other) {
            release();
            h = other.h;
            other.h = nullptr;
        }
        return *this;
    }

    bool valid() const { return h != nullptr; }
    // noipa prevents GCC's ISRA (interprocedural scalar replacement of
    // aggregates) from creating .isra.0 clones that pass the raw handle
    // value instead of a const LuaObj& — the clones would call handle()
    // on the raw value, treating it as a this pointer ("lw a0,0(a0)").
    __attribute__((noipa))
    void* handle() const { return h; }

    // ── Object lifecycle ──
    // Release this handle from OBJECTS without destroying the underlying object.
    // Also callable explicitly for early release; destructor handles auto-release.
    void release() { if (h) { Rbxl::releaseObject(h); h = nullptr; } }

    // Create a LuaObj from a raw handle
    static LuaObj fromHandle(void* h) { return LuaObj(h); }

    // ── Enum conversions (syscalls 42/43) ──
    // Convert a C++ enum index (e.g. (int)Rbxl::Enum::PARTTYPE_CYLINDER) to an OBJECTS handle.
    // The handle can then be used with setPropertyObject / getPropertyObject.
    static LuaObj fromEnum(int enumIndex) { return LuaObj(Rbxl::fromEnum(enumIndex)); }
    static LuaObj fromEnum(Rbxl::Enum e) { return fromEnum((int)e); }
    // Convert an OBJECTS handle back to a C++ enum index.
    int toEnum() const { return Rbxl::toEnum(h); }

    // ── Primitive conversions (no new syscalls — transpiler detects by function name) ──

    static LuaObj fromFloat(float f) {
        void* handle = nullptr;
#ifdef __riscv
        asm volatile("mv a0, %1; li a1, 4; li a7, 79; ecall; mv %0, a0" : "=r"(handle) : "r"(f) : "a0", "a1", "a7");
#endif
        return LuaObj(handle);
    }
    static LuaObj fromInt(int i) {
        void* handle = nullptr;
#ifdef __riscv
        asm volatile("mv a0, %1; li a1, 5; li a7, 79; ecall; mv %0, a0" : "=r"(handle) : "r"(i) : "a0", "a1", "a7");
#endif
        return LuaObj(handle);
    }
    static LuaObj fromBool(bool b) {
        void* handle = nullptr;
#ifdef __riscv
        asm volatile("mv a0, %1; li a1, 6; li a7, 79; ecall; mv %0, a0" : "=r"(handle) : "r"((int)b) : "a0", "a1", "a7");
#endif
        return LuaObj(handle);
    }
    static LuaObj fromString(const char* s) {
        void* handle = nullptr;
#ifdef __riscv
        asm volatile("mv a0, %1; li a1, 7; li a7, 79; ecall; mv %0, a0" : "=r"(handle) : "r"(s) : "a0", "a1", "a7");
#endif
        return LuaObj(handle);
    }
    // objectWrite 79: fromFunction(type_id=8) — wraps C++ function address
    // in a callable Luau function, stores in OBJECTS, returns handle.
    static LuaObj fromFunction(void* funcAddr) {
        void* handle = nullptr;
#ifdef __riscv
        asm volatile("mv a0, %1; li a1, 8; li a7, 79; ecall; mv %0, a0" : "=r"(handle) : "r"(funcAddr) : "a0", "a1", "a7");
#endif
        return LuaObj(handle);
    }

    float toFloat() const {
        float result = 0.0f;
#ifdef __riscv
        asm volatile("mv a0, %1; li a1, 4; li a7, 78; ecall; mv %0, a0" : "=r"(result) : "r"(h) : "a0", "a1", "a7");
#endif
        return result;
    }
    int toInt() const {
        int result = 0;
#ifdef __riscv
        asm volatile("mv a0, %1; li a1, 5; li a7, 78; ecall; mv %0, a0" : "=r"(result) : "r"(h) : "a0", "a1", "a7");
#endif
        return result;
    }
    bool toBool() const {
        int result = 0;
#ifdef __riscv
        asm volatile("mv a0, %1; li a1, 6; li a7, 78; ecall; mv %0, a0" : "=r"(result) : "r"(h) : "a0", "a1", "a7");
#endif
        return result != 0;
    }
    const char* toString() const {
        void* result = nullptr;
#ifdef __riscv
        asm volatile("mv a0, %1; li a1, 7; li a7, 78; ecall; mv %0, a0" : "=r"(result) : "r"(h) : "a0", "a1", "a7");
#endif
        return (const char*)result;
    }

    // ── Property access (the ONLY property API) ──
    LuaObj getPropertyObject(const char* name) const { return LuaObj(Rbxl::getPropertyObject(h, name)); }
    // noipa prevents GCC's ISRA from scalarizing the const LuaObj& into a
    // raw handle — the isra.0 clone would call handle() on the raw value as
    // if it were a this pointer, which the transpiled VM simulates faithfully
    // (loading from unmapped memory → 0 → OBJECTS[0] = nil).
    __attribute__((noipa))
    void setPropertyObject(const char* name, const LuaObj& value) const { Rbxl::setPropertyObject(h, name, value.handle()); }

    // ── Service / Global / Method lookups ──
    static LuaObj getService(const char* name)   { return LuaObj(Rbxl::getService(name)); }
    static LuaObj getGlobal(const char* name)    { return LuaObj(Rbxl::getGlobal(name)); }
    LuaObj getMethod(const char* methodName) const { return LuaObj(Rbxl::getMethod(h, methodName)); }
    LuaObj require() const                       { return LuaObj(Rbxl::require(h)); }

    // ── .callObj() — payload-based call (syscall 75) ──
    // Invokes OBJECTS[handle] as a callable function.  All args MUST be
    // OBJECTS handles (void*).  LuaObj args are auto-extracted via _obj_handle().
    //
    // For callMethod (self-prepend): pass this->h as the first arg.
    // For callMethodStatic: omit self.

    template<typename... Args>
    void* callObj(int flags, const Args&... args) const {
        return Rbxl::callObj(h, flags, args...);
    }

    // ── Method call (getPropertyObject + callObj) ──
    // callMethod: prepends self (this->h) as first arg, then user args
    // callMethodStatic: no self prepended
    // Flags go FIRST in the new API (different from the legacy .call() API).

    template<typename... Args>
    void* callMethod(const char* methodName, int flags, const Args&... args) const {
        return getPropertyObject(methodName).callObj(flags, h, args...);
    }

    // ── Static method call (getPropertyObject + callObj, no self) ──

    template<typename... Args>
    void* callMethodStatic(const char* methodName, int flags, const Args&... args) const {
        return getPropertyObject(methodName).callObj(flags, args...);
    }
};

// ── Buffer: fixed-size byte array bridging C++ ↔ Luau buffer objects ──────
// Uses the universal handle API: LuaObj::getGlobal + getPropertyObject + callObj.
// Raw ints (offsets, sizes, byte values) are converted to OBJECTS handles via
// LuaObj::fromInt / toInt.
struct Buffer {
    static const int MAX_SIZE = 65536;  // 64KB, same as a memory page
    uint8_t data[MAX_SIZE];
    unsigned int size;

    Buffer() : size(0) {}

    // Read a Luau buffer object (stored in OBJECTS) into this C++ array.
    void readFromObject(void* objHandle) {
        LuaObj bufferLib = LuaObj::getGlobal("buffer");

        // buffer.len(objHandle)
        {
            LuaObj result = LuaObj::fromHandle(
                bufferLib.getPropertyObject("len").callObj(
                    RBXL_METHOD_HAS_RETURN_BIT,
                    objHandle
                )
            );
            unsigned int len = (unsigned int)result.toInt();
            size = len < MAX_SIZE ? len : MAX_SIZE;
        }

        // buffer.readi8(objHandle, offset) per byte
        LuaObj readi8Fn = bufferLib.getPropertyObject("readi8");
        for (unsigned int i = 0; i < size; i++) {
            LuaObj result = LuaObj::fromHandle(
                readi8Fn.callObj(
                    RBXL_METHOD_HAS_RETURN_BIT,
                    objHandle,
                    LuaObj::fromInt((int)i).handle()
                )
            );
            data[i] = (uint8_t)result.toInt();
        }

        bufferLib.release();
    }

    // Write this C++ array into a new Luau buffer object, store in OBJECTS, return handle.
    void* toObject() const {
        LuaObj bufferLib = LuaObj::getGlobal("buffer");

        // buffer.create(size)
        void* handle = bufferLib.getPropertyObject("create").callObj(
            RBXL_METHOD_HAS_RETURN_BIT,
            LuaObj::fromInt((int)size).handle()
        );

        // buffer.writei8(handle, offset, byte) per byte
        LuaObj writei8Fn = bufferLib.getPropertyObject("writei8");
        for (unsigned int i = 0; i < size; i++) {
            writei8Fn.callObj(
                0,  // no return
                handle,
                LuaObj::fromInt((int)i).handle(),
                LuaObj::fromInt((int)data[i]).handle()
            );
        }

        bufferLib.release();
        return handle;
    }
};

// ── _obj_handle(const LuaObj&) — defined after LuaObj class ──
namespace Rbxl {
    inline void* _obj_handle(const LuaObj& obj) { return obj.handle(); }
}

#endif // RBXL_HPP
