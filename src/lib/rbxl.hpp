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

// ── callMethod flags ─────────────────────────────────────────────────────────
#define RBXL_METHOD_HAS_RETURN_BIT            (1 << 0)
#define RBXL_METHOD_RETURN_IS_OBJ_BIT         (1 << 1)
#define RBXL_METHOD_CALL_TARGET_IS_SERVICE_BIT (1 << 2)
#define RBXL_METHOD_ARG_1_IS_STRING_BIT       (1 << 3)
#define RBXL_METHOD_ARG_2_IS_STRING_BIT       (1 << 4)
#define RBXL_METHOD_RETURN_IS_BUFFER_BIT      (1 << 5)
#define RBXL_METHOD_ARG_3_IS_STRING_BIT       (1 << 6)
#define RBXL_METHOD_ARG_4_IS_STRING_BIT       (1 << 7)
#define RBXL_METHOD_IS_STATIC_BIT             (1 << 8)
#define RBXL_METHOD_ARG_1_IS_BUFFER_BIT       (1 << 9)
#define RBXL_METHOD_ARG_2_IS_BUFFER_BIT       (1 << 10)
#define RBXL_METHOD_ARG_3_IS_BUFFER_BIT       (1 << 11)
#define RBXL_METHOD_ARG_4_IS_BUFFER_BIT       (1 << 12)
#define RBXL_METHOD_ARG_1_IS_FUNCTION_BIT     (1 << 13)
#define RBXL_METHOD_ARG_2_IS_FUNCTION_BIT     (1 << 14)
#define RBXL_METHOD_ARG_3_IS_FUNCTION_BIT     (1 << 15)
#define RBXL_METHOD_ARG_4_IS_FUNCTION_BIT     (1 << 16)
#define RBXL_METHOD_ARG_1_IS_OBJECT_BIT       (1 << 17)
#define RBXL_METHOD_ARG_2_IS_OBJECT_BIT       (1 << 18)
#define RBXL_METHOD_ARG_3_IS_OBJECT_BIT       (1 << 19)
#define RBXL_METHOD_ARG_4_IS_OBJECT_BIT       (1 << 20)
#define RBXL_METHOD_ARG_0_IS_SELF_BIT         (1 << 21)  // callMethod prepends self; a1=object, user args start at a2


// ── C++ struct types (math on heap, bridge to/from OBJECTS) ──────────────────

struct Vector3 {
    float x, y, z;
    Vector3() : x(0), y(0), z(0) {}
    Vector3(float x_, float y_, float z_) : x(x_), y(y_), z(z_) {}

    // Syscall 54: Read Vector3 from OBJECTS[handle] into *this (OBJECTS → C++ struct)
    void readFromObject(void* objHandle) {
        asm volatile (
            "mv a0, %0; mv a1, %1; li a7, 54; ecall"
            :
            : "r"(objHandle), "r"(this)
            : "a0", "a1", "a7", "memory"
        );
    }
    // Syscall 55: Store this Vector3 into OBJECTS, return handle (C++ struct → OBJECTS)
    void* toObject() const {
        void* handle;
        asm volatile (
            "mv a0, %1; li a7, 55; ecall; mv %0, a0"
            : "=r"(handle)
            : "r"(this)
            : "a0", "a7", "memory"
        );
        return handle;
    }
};

struct Color3 {
    float r, g, b;
    Color3() : r(0), g(0), b(0) {}
    Color3(float r_, float g_, float b_) : r(r_), g(g_), b(b_) {}

    // Syscall 58: Read Color3 from OBJECTS[handle] into *this
    void readFromObject(void* objHandle) {
        asm volatile (
            "mv a0, %0; mv a1, %1; li a7, 58; ecall"
            :
            : "r"(objHandle), "r"(this)
            : "a0", "a1", "a7", "memory"
        );
    }
    // Syscall 59: Store this Color3 into OBJECTS, return handle
    void* toObject() const {
        void* handle;
        asm volatile (
            "mv a0, %1; li a7, 59; ecall; mv %0, a0"
            : "=r"(handle)
            : "r"(this)
            : "a0", "a7", "memory"
        );
        return handle;
    }
};

// ── UDim2: 4-float 2D size/position (X.Scale, X.Offset, Y.Scale, Y.Offset) ──
struct UDim2 {
    float d[4];

    // Syscall 60: Read UDim2 from OBJECTS[handle] into *this
    void readFromObject(void* objHandle) {
        asm volatile (
            "mv a0, %0; mv a1, %1; li a7, 60; ecall"
            :
            : "r"(objHandle), "r"(this)
            : "a0", "a1", "a7", "memory"
        );
    }
    // Syscall 61: Store this UDim2 into OBJECTS, return handle
    void* toObject() const {
        void* handle;
        asm volatile (
            "mv a0, %1; li a7, 61; ecall; mv %0, a0"
            : "=r"(handle)
            : "r"(this)
            : "a0", "a7", "memory"
        );
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

    // Syscall 56: Read CFrame from OBJECTS[handle] into *this
    void readFromObject(void* objHandle) {
        asm volatile (
            "mv a0, %0; mv a1, %1; li a7, 56; ecall"
            :
            : "r"(objHandle), "r"(this)
            : "a0", "a1", "a7", "memory"
        );
    }
    // Syscall 57: Store this CFrame into OBJECTS, return handle
    void* toObject() const {
        void* handle;
        asm volatile (
            "mv a0, %1; li a7, 57; ecall; mv %0, a0"
            : "=r"(handle)
            : "r"(this)
            : "a0", "a7", "memory"
        );
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

    // ── Math Operations ──

    // Syscall 39: rad — convert degrees to radians in-place at *ptr
    void rad(void* ptr) {
        asm volatile ("mv a0, %0; li a7, 39; ecall" : : "r"(ptr) : "a0", "a7", "memory");
    }

    // Syscall 40: sin — replace *ptr with sin(*ptr)
    void sin(void* ptr) {
        asm volatile ("mv a0, %0; li a7, 40; ecall" : : "r"(ptr) : "a0", "a7", "memory");
    }

    // Syscall 41: cos — replace *ptr with cos(*ptr)
    void cos(void* ptr) {
        asm volatile ("mv a0, %0; li a7, 41; ecall" : : "r"(ptr) : "a0", "a7", "memory");
    }

    // ── Object Property Access (the ONLY two property syscalls) ──

    // Syscall 62: getPropertyObject(handle, propName) — returns any property as an object handle
    void* getPropertyObject(void* handle, const char* propName) {
        void* result = nullptr;
        asm volatile ("mv a0, %1; mv a1, %2; li a7, 62; ecall; mv %0, a0" : "=r"(result) : "r"(handle), "r"(propName) : "a0", "a1", "a7");
        return result;
    }

    // Syscall 63: setPropertyObject(handle, propName, valueHandle) — sets a property from an OBJECTS handle
    void setPropertyObject(void* handle, const char* propName, void* valueHandle) {
        asm volatile ("mv a0, %0; mv a1, %1; mv a2, %2; li a7, 63; ecall" : : "r"(handle), "r"(propName), "r"(valueHandle) : "a0", "a1", "a2", "a7");
    }

    // Syscall 64: releaseObject(handle) — removes an entry from OBJECTS without destroying the Instance
    void releaseObject(void* handle) {
        asm volatile ("mv a0, %0; li a7, 64; ecall" : : "r"(handle) : "a0", "a7");
    }

    // ── Enum ↔ OBJECTS bridge (syscalls 42/43) ──

    // Syscall 42: fromEnum(enumIndex) — converts C++ enum index → OBJECTS handle
    // Looks up ENUMS[index + 1], stores the Roblox EnumItem in OBJECTS, returns handle.
    void* fromEnum(int enumIndex) {
        void* handle = nullptr;
        asm volatile ("mv a0, %1; li a7, 42; ecall; mv %0, a0" : "=r"(handle) : "r"(enumIndex) : "a0", "a7");
        return handle;
    }

    // Syscall 43: toEnum(handle) — converts OBJECTS handle → C++ enum index
    // Looks up OBJECTS[handle] in ENUM_TO_INDEX, returns the index.
    int toEnum(void* handle) {
        int result = 0;
        asm volatile ("mv a0, %1; li a7, 43; ecall; mv %0, a0" : "=r"(result) : "r"(handle) : "a0", "a7");
        return result;
    }

    // ── Service / Global / Method Lookups ──

    // Syscall 47: getService(name) — returns raw handle to any Roblox service instance
    void* getService(const char* name) {
        void* handle = nullptr;
        asm volatile ("mv a0, %1; li a7, 47; ecall; mv %0, a0" : "=r"(handle) : "r"(name) : "a0", "a7");
        return handle;
    }

    // Syscall 52: getGlobal(name) — returns the named Lua global as a handle
    void* getGlobal(const char* name) {
        void* handle = nullptr;
        asm volatile ("mv a0, %1; li a7, 52; ecall; mv %0, a0" : "=r"(handle) : "r"(name) : "a0", "a7");
        return handle;
    }

    // Syscall 51: getMethod(handle, methodName) — returns RBXScriptSignal handle
    void* getMethod(void* handle, const char* methodName) {
        void* result = nullptr;
        asm volatile ("mv a0, %1; mv a1, %2; li a7, 51; ecall; mv %0, a0" : "=r"(result) : "r"(handle), "r"(methodName) : "a0", "a1", "a7");
        return result;
    }

    // Syscall 53: require — requires a ModuleScript instance, returns handle
    void* require(void* moduleHandle) {
        void* handle = nullptr;
        asm volatile ("mv a0, %1; li a7, 53; ecall; mv %0, a0" : "=r"(handle) : "r"(moduleHandle) : "a0", "a7");
        return handle;
    }

    // Syscall 65: call(handle, flags, args...) — calls OBJECTS[handle] as a function
    // Register layout: a0=handle, a1=arg1, a2=arg2, a3=flags, a4=arg3, a5=arg4, a6=arg5

    // 0 extra args — set unused arg regs to -1 sentinel so the handler can skip them
    void* call(void* handle, int flags) {
        void* result = nullptr;
        asm volatile (
            "mv a0, %1; mv a3, %2; addi a1, x0, -1; addi a2, x0, -1; addi a4, x0, -1; addi a5, x0, -1; addi a6, x0, -1; li a7, 65; ecall; mv %0, a0"
            : "=r"(result) : "r"(handle), "r"(flags)
            : "a0", "a1", "a2", "a3", "a4", "a5", "a6", "a7"
        );
        return result;
    }

    // 1 extra arg — set unused a2, a4, a5, a6 to -1 sentinel
    template<typename A1>
    void* call(void* handle, const A1& a1, int flags) {
        void* result = nullptr;
        asm volatile (
            "mv a0, %1; mv a1, %2; mv a3, %3; addi a2, x0, -1; addi a4, x0, -1; addi a5, x0, -1; addi a6, x0, -1; li a7, 65; ecall; mv %0, a0"
            : "=r"(result) : "r"(handle), "r"(a1), "r"(flags)
            : "a0", "a1", "a2", "a3", "a4", "a5", "a6", "a7"
        );
        return result;
    }

    // 2 extra args — set unused a4, a5, a6 to -1 sentinel
    template<typename A1, typename A2>
    void* call(void* handle, const A1& a1, const A2& a2, int flags) {
        void* result = nullptr;
        asm volatile (
            "mv a0, %1; mv a1, %2; mv a2, %3; mv a3, %4; addi a4, x0, -1; addi a5, x0, -1; addi a6, x0, -1; li a7, 65; ecall; mv %0, a0"
            : "=r"(result) : "r"(handle), "r"(a1), "r"(a2), "r"(flags)
            : "a0", "a1", "a2", "a3", "a4", "a5", "a6", "a7"
        );
        return result;
    }

    // 3 extra args — set unused a5, a6 to -1 sentinel
    template<typename A1, typename A2, typename A3>
    void* call(void* handle, const A1& a1, const A2& a2, const A3& a3, int flags) {
        void* result = nullptr;
        asm volatile (
            "mv a0, %1; mv a1, %2; mv a2, %3; mv a3, %5; mv a4, %4; addi a5, x0, -1; addi a6, x0, -1; li a7, 65; ecall; mv %0, a0"
            : "=r"(result) : "r"(handle), "r"(a1), "r"(a2), "r"(a3), "r"(flags)
            : "a0", "a1", "a2", "a3", "a4", "a5", "a6", "a7"
        );
        return result;
    }

    // 4 extra args — set unused a6 to -1 sentinel
    template<typename A1, typename A2, typename A3, typename A4>
    void* call(void* handle, const A1& a1, const A2& a2, const A3& a3, const A4& a4, int flags) {
        void* result = nullptr;
        asm volatile (
            "mv a0, %1; mv a1, %2; mv a2, %3; mv a3, %6; mv a4, %4; mv a5, %5; addi a6, x0, -1; li a7, 65; ecall; mv %0, a0"
            : "=r"(result) : "r"(handle), "r"(a1), "r"(a2), "r"(a3), "r"(a4), "r"(flags)
            : "a0", "a1", "a2", "a3", "a4", "a5", "a6", "a7"
        );
        return result;
    }

    // 5 extra args (needed by callMethod with 4 user args + self) — all regs used
    template<typename A1, typename A2, typename A3, typename A4, typename A5>
    void* call(void* handle, const A1& a1, const A2& a2, const A3& a3, const A4& a4, const A5& a5, int flags) {
        void* result = nullptr;
        asm volatile (
            "mv a0, %1; mv a1, %2; mv a2, %3; mv a3, %7; mv a4, %4; mv a5, %5; mv a6, %6; li a7, 65; ecall; mv %0, a0"
            : "=r"(result) : "r"(handle), "r"(a1), "r"(a2), "r"(a3), "r"(a4), "r"(a5), "r"(flags)
            : "a0", "a1", "a2", "a3", "a4", "a5", "a6", "a7"
        );
        return result;
    }

}

// ── Forward declarations of LuaObj-aware call() overloads ──
// These MUST be visible before LuaObj's member functions so that
// Rbxl::call(h, luaObj, ...) resolves to these overloads (which extract
// the inner void* handle) rather than the base templates (which would
// try to pass the class object through a register constraint).

namespace Rbxl {
    // -- all-LuaObj (non-template) --
    inline void* call(void* handle, const LuaObj& a1, int flags);
    inline void* call(void* handle, const LuaObj& a1, const LuaObj& a2, int flags);
    inline void* call(void* handle, const LuaObj& a1, const LuaObj& a2, const LuaObj& a3, int flags);
    inline void* call(void* handle, const LuaObj& a1, const LuaObj& a2, const LuaObj& a3, const LuaObj& a4, int flags);
    inline void* call(void* handle, const LuaObj& a1, const LuaObj& a2, const LuaObj& a3, const LuaObj& a4, const LuaObj& a5, int flags);

    // -- partial templates (one LuaObj position) --
    // 2 args
    template<typename A2> inline void* call(void* handle, const LuaObj& a1, const A2& a2, int flags);
    template<typename A1> inline void* call(void* handle, const A1& a1, const LuaObj& a2, int flags);

    // 3 args
    template<typename A2, typename A3> inline void* call(void* handle, const LuaObj& a1, const A2& a2, const A3& a3, int flags);
    template<typename A1, typename A3> inline void* call(void* handle, const A1& a1, const LuaObj& a2, const A3& a3, int flags);
    template<typename A1, typename A2> inline void* call(void* handle, const A1& a1, const A2& a2, const LuaObj& a3, int flags);

    // 4 args
    template<typename A2, typename A3, typename A4> inline void* call(void* handle, const LuaObj& a1, const A2& a2, const A3& a3, const A4& a4, int flags);
    template<typename A1, typename A3, typename A4> inline void* call(void* handle, const A1& a1, const LuaObj& a2, const A3& a3, const A4& a4, int flags);
    template<typename A1, typename A2, typename A4> inline void* call(void* handle, const A1& a1, const A2& a2, const LuaObj& a3, const A4& a4, int flags);
    template<typename A1, typename A2, typename A3> inline void* call(void* handle, const A1& a1, const A2& a2, const A3& a3, const LuaObj& a4, int flags);

    // 5 args
    template<typename A2, typename A3, typename A4, typename A5> inline void* call(void* handle, const LuaObj& a1, const A2& a2, const A3& a3, const A4& a4, const A5& a5, int flags);
    template<typename A1, typename A3, typename A4, typename A5> inline void* call(void* handle, const A1& a1, const LuaObj& a2, const A3& a3, const A4& a4, const A5& a5, int flags);
    template<typename A1, typename A2, typename A4, typename A5> inline void* call(void* handle, const A1& a1, const A2& a2, const LuaObj& a3, const A4& a4, const A5& a5, int flags);
    template<typename A1, typename A2, typename A3, typename A5> inline void* call(void* handle, const A1& a1, const A2& a2, const A3& a3, const LuaObj& a4, const A5& a5, int flags);
    template<typename A1, typename A2, typename A3, typename A4> inline void* call(void* handle, const A1& a1, const A2& a2, const A3& a3, const A4& a4, const LuaObj& a5, int flags);
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
        void* handle;
        asm volatile("mv a0, %1; li a7, 66; ecall; mv %0, a0" : "=r"(handle) : "r"(f) : "a0", "a7");
        return LuaObj(handle);
    }
    static LuaObj fromInt(int i) {
        void* handle;
        asm volatile("mv a0, %1; li a7, 67; ecall; mv %0, a0" : "=r"(handle) : "r"(i) : "a0", "a7");
        return LuaObj(handle);
    }
    static LuaObj fromBool(bool b) {
        void* handle;
        asm volatile("mv a0, %1; li a7, 68; ecall; mv %0, a0" : "=r"(handle) : "r"((int)b) : "a0", "a7");
        return LuaObj(handle);
    }
    static LuaObj fromString(const char* s) {
        void* handle;
        asm volatile("mv a0, %1; li a7, 69; ecall; mv %0, a0" : "=r"(handle) : "r"(s) : "a0", "a7");
        return LuaObj(handle);
    }
    // Syscall 74: fromFunction(void* funcAddr) — wraps a C++ function address
    // in a callable Luau function and stores it in OBJECTS, returning a handle.
    // The handle can then be used with call() / callMethod() / callMethodStatic()
    // just like any other object handle.
    static LuaObj fromFunction(void* funcAddr) {
        void* handle;
        asm volatile("mv a0, %1; li a7, 74; ecall; mv %0, a0" : "=r"(handle) : "r"(funcAddr) : "a0", "a7");
        return LuaObj(handle);
    }

    float toFloat() const {
        float result;
        asm volatile("mv a0, %1; li a7, 70; ecall; mv %0, a0" : "=r"(result) : "r"(h) : "a0", "a7");
        return result;
    }
    int toInt() const {
        int result;
        asm volatile("mv a0, %1; li a7, 71; ecall; mv %0, a0" : "=r"(result) : "r"(h) : "a0", "a7");
        return result;
    }
    bool toBool() const {
        int result;
        asm volatile("mv a0, %1; li a7, 72; ecall; mv %0, a0" : "=r"(result) : "r"(h) : "a0", "a7");
        return result != 0;
    }
    const char* toString() const {
        void* result;
        asm volatile("mv a0, %1; li a7, 73; ecall; mv %0, a0" : "=r"(result) : "r"(h) : "a0", "a7");
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

    // ── .call() — invokes OBJECTS[handle] as a callable function ──
    // Passes args directly; no implicit self.
    // callMethod prepends self explicitly; callMethodStatic does not.

    // 0 extra args
    void* call(int flags) const {
        return Rbxl::call(h, flags);
    }
    // 1 extra arg
    template<typename A1>
    void* call(const A1& a1, int flags) const {
        return Rbxl::call(h, a1, flags);
    }
    // 2 extra args
    template<typename A1, typename A2>
    void* call(const A1& a1, const A2& a2, int flags) const {
        return Rbxl::call(h, a1, a2, flags);
    }
    // 3 extra args
    template<typename A1, typename A2, typename A3>
    void* call(const A1& a1, const A2& a2, const A3& a3, int flags) const {
        return Rbxl::call(h, a1, a2, a3, flags);
    }
    // 4 extra args
    template<typename A1, typename A2, typename A3, typename A4>
    void* call(const A1& a1, const A2& a2, const A3& a3, const A4& a4, int flags) const {
        return Rbxl::call(h, a1, a2, a3, a4, flags);
    }
    // 5 extra args (needed by callMethod with 4 user args + self)
    template<typename A1, typename A2, typename A3, typename A4, typename A5>
    void* call(const A1& a1, const A2& a2, const A3& a3, const A4& a4, const A5& a5, int flags) const {
        return Rbxl::call(h, a1, a2, a3, a4, a5, flags);
    }

    // ── Method call (getPropertyObject + .call) ──
    // callMethod: prepends self (this->h) as first arg, then user args
    // callMethodStatic: no self prepended

    // 0 extra args
    void* callMethod(const char* methodName, int flags) const {
        return getPropertyObject(methodName).call(h, flags | RBXL_METHOD_ARG_0_IS_SELF_BIT);
    }

    // 1 extra arg — const char* (exact match, shadows template)
    void* callMethod(const char* methodName, const char* arg, int flags) const {
        return getPropertyObject(methodName).call(h, arg, flags | RBXL_METHOD_ARG_0_IS_SELF_BIT);
    }

    // 1 extra arg (generic template)
    template<typename A1>
    void* callMethod(const char* methodName, const A1& a1, int flags) const {
        return getPropertyObject(methodName).call(h, a1, flags | RBXL_METHOD_ARG_0_IS_SELF_BIT);
    }

    // 2 extra args
    template<typename A1, typename A2>
    void* callMethod(const char* methodName, const A1& a1, const A2& a2, int flags) const {
        return getPropertyObject(methodName).call(h, a1, a2, flags | RBXL_METHOD_ARG_0_IS_SELF_BIT);
    }

    // 3 extra args
    template<typename A1, typename A2, typename A3>
    void* callMethod(const char* methodName, const A1& a1, const A2& a2, const A3& a3, int flags) const {
        return getPropertyObject(methodName).call(h, a1, a2, a3, flags | RBXL_METHOD_ARG_0_IS_SELF_BIT);
    }

    // 4 extra args
    template<typename A1, typename A2, typename A3, typename A4>
    void* callMethod(const char* methodName, const A1& a1, const A2& a2, const A3& a3, const A4& a4, int flags) const {
        return getPropertyObject(methodName).call(h, a1, a2, a3, a4, flags | RBXL_METHOD_ARG_0_IS_SELF_BIT);
    }

    // ── Static method call (getPropertyObject + .call, no self) ──

    // 0 extra args
    void* callMethodStatic(const char* methodName, int flags) const {
        return getPropertyObject(methodName).call(flags | 256);
    }
    // 1 extra arg — const char* (exact match)
    void* callMethodStatic(const char* methodName, const char* arg, int flags) const {
        return getPropertyObject(methodName).call(arg, flags | 256);
    }
    // 1 extra arg (generic template)
    template<typename A1>
    void* callMethodStatic(const char* methodName, const A1& a1, int flags) const {
        return getPropertyObject(methodName).call(a1, flags | 256);
    }
    // 2 extra args
    template<typename A1, typename A2>
    void* callMethodStatic(const char* methodName, const A1& a1, const A2& a2, int flags) const {
        return getPropertyObject(methodName).call(a1, a2, flags | 256);
    }
    // 3 extra args
    template<typename A1, typename A2, typename A3>
    void* callMethodStatic(const char* methodName, const A1& a1, const A2& a2, const A3& a3, int flags) const {
        return getPropertyObject(methodName).call(a1, a2, a3, flags | 256);
    }
    // 4 extra args
    template<typename A1, typename A2, typename A3, typename A4>
    void* callMethodStatic(const char* methodName, const A1& a1, const A2& a2, const A3& a3, const A4& a4, int flags) const {
        return getPropertyObject(methodName).call(a1, a2, a3, a4, flags | 256);
    }
};

// ── Buffer: fixed-size byte array bridging C++ ↔ Luau buffer objects ──────
// Uses the universal handle API (getGlobal + callMethodStatic) — no buffer syscalls.
struct Buffer {
    static const int MAX_SIZE = 65536;  // 64KB, same as a memory page
    uint8_t data[MAX_SIZE];
    unsigned int size;

    Buffer() : size(0) {}

    // Read a Luau buffer object (stored in OBJECTS) into this C++ array.
    void readFromObject(void* objHandle) {
        LuaObj bufferLib = LuaObj::getGlobal("buffer");

        // Call buffer.len(bufHandle) to get the size
        unsigned int len = (unsigned int)(unsigned long)bufferLib.callMethodStatic(
            "len",
            objHandle,
            RBXL_METHOD_ARG_1_IS_OBJECT_BIT | RBXL_METHOD_HAS_RETURN_BIT
        );
        size = len < MAX_SIZE ? len : MAX_SIZE;

        // Read bytes one by one: buffer.readi8(bufHandle, i)
        // Only arg1 is a handle; offset (int)i passes as raw register value.
        for (unsigned int i = 0; i < size; i++) {
            int val = (int)(unsigned long)bufferLib.callMethodStatic(
                "readi8",
                objHandle,
                (int)i,
                RBXL_METHOD_ARG_1_IS_OBJECT_BIT | RBXL_METHOD_HAS_RETURN_BIT
            );
            data[i] = (uint8_t)val;
        }

        bufferLib.release();
    }

    // Write this C++ array into a new Luau buffer object, store in OBJECTS, return handle.
    void* toObject() const {
        LuaObj bufferLib = LuaObj::getGlobal("buffer");

        // Create buffer: buffer.create(size) — size is raw int, no OBJECTS flag.
        void* handle = bufferLib.callMethodStatic(
            "create",
            (int)size,
            RBXL_METHOD_HAS_RETURN_BIT | RBXL_METHOD_RETURN_IS_OBJ_BIT
        );

        // Write bytes: buffer.writei8(bufHandle, i, data[i])
        // Only arg1 is a handle; offset and value are raw ints.
        for (unsigned int i = 0; i < size; i++) {
            bufferLib.callMethodStatic(
                "writei8",
                handle,
                (int)i,
                (int)data[i],
                RBXL_METHOD_ARG_1_IS_OBJECT_BIT
            );
        }

        bufferLib.release();
        return handle;
    }
};

// ── Rbxl::call overloads for LuaObj arguments ───────────────────────────────
//
// GCC's RISC-V backend rejects class-typed inputs for the "r" register
// operand constraint ("impossible constraint in 'asm'" / "non-memory input
// N must stay in memory"). The call() templates above take their user args
// by `const T&` and pass them through `"r"` to the ecall wrapper. When a
// LuaObj is passed, the class object cannot live in a single register, so
// template instantiation with A1=LuaObj (or A2=LuaObj, etc.) fails to
// compile.
//
// To keep call() usable with LuaObj args without rewriting the ecall
// template body, define non-template overloads that pre-extract the inner
// handle (a void* primitive) and forward into the existing templates with
// LuaObj positions substituted by void*. Non-template overloads are
// preferred by overload resolution over the function templates, so these
// are selected whenever the corresponding user arg position is a LuaObj.
//
// Non-template "all-LuaObj" overloads are still needed at each arity to
// resolve partial-ordering ambiguity between the partial templates below
// when multiple LuaObj positions appear in a single call.

namespace Rbxl {

// 1 extra arg, A1=LuaObj (non-template beats the function template)
inline void* call(void* handle, const LuaObj& a1, int flags) {
    return call<void*>(handle, a1.handle(), flags);
}

// 2 extra args, A1=LuaObj, A2=LuaObj
inline void* call(void* handle, const LuaObj& a1, const LuaObj& a2, int flags) {
    return call<void*, void*>(handle, a1.handle(), a2.handle(), flags);
}
// 2 extra args, A1=LuaObj
template<typename A2>
inline void* call(void* handle, const LuaObj& a1, const A2& a2, int flags) {
    return call<void*, A2>(handle, a1.handle(), a2, flags);
}
// 2 extra args, A2=LuaObj
template<typename A1>
inline void* call(void* handle, const A1& a1, const LuaObj& a2, int flags) {
    return call<A1, void*>(handle, a1, a2.handle(), flags);
}

// 3 extra args, A1=A2=A3=LuaObj
inline void* call(void* handle, const LuaObj& a1, const LuaObj& a2, const LuaObj& a3, int flags) {
    return call<void*, void*, void*>(handle, a1.handle(), a2.handle(), a3.handle(), flags);
}
// 3 extra args, A1=LuaObj
template<typename A2, typename A3>
inline void* call(void* handle, const LuaObj& a1, const A2& a2, const A3& a3, int flags) {
    return call<void*, A2, A3>(handle, a1.handle(), a2, a3, flags);
}
// 3 extra args, A2=LuaObj
template<typename A1, typename A3>
inline void* call(void* handle, const A1& a1, const LuaObj& a2, const A3& a3, int flags) {
    return call<A1, void*, A3>(handle, a1, a2.handle(), a3, flags);
}
// 3 extra args, A3=LuaObj
template<typename A1, typename A2>
inline void* call(void* handle, const A1& a1, const A2& a2, const LuaObj& a3, int flags) {
    return call<A1, A2, void*>(handle, a1, a2, a3.handle(), flags);
}

// 4 extra args, A1=A2=A3=A4=LuaObj
inline void* call(void* handle, const LuaObj& a1, const LuaObj& a2, const LuaObj& a3, const LuaObj& a4, int flags) {
    return call<void*, void*, void*, void*>(handle, a1.handle(), a2.handle(), a3.handle(), a4.handle(), flags);
}
// 4 extra args, A1=LuaObj
template<typename A2, typename A3, typename A4>
inline void* call(void* handle, const LuaObj& a1, const A2& a2, const A3& a3, const A4& a4, int flags) {
    return call<void*, A2, A3, A4>(handle, a1.handle(), a2, a3, a4, flags);
}
// 4 extra args, A2=LuaObj
template<typename A1, typename A3, typename A4>
inline void* call(void* handle, const A1& a1, const LuaObj& a2, const A3& a3, const A4& a4, int flags) {
    return call<A1, void*, A3, A4>(handle, a1, a2.handle(), a3, a4, flags);
}
// 4 extra args, A3=LuaObj
template<typename A1, typename A2, typename A4>
inline void* call(void* handle, const A1& a1, const A2& a2, const LuaObj& a3, const A4& a4, int flags) {
    return call<A1, A2, void*, A4>(handle, a1, a2, a3.handle(), a4, flags);
}
// 4 extra args, A4=LuaObj
template<typename A1, typename A2, typename A3>
inline void* call(void* handle, const A1& a1, const A2& a2, const A3& a3, const LuaObj& a4, int flags) {
    return call<A1, A2, A3, void*>(handle, a1, a2, a3, a4.handle(), flags);
}

// 5 extra args, A1=A2=A3=A4=A5=LuaObj
inline void* call(void* handle, const LuaObj& a1, const LuaObj& a2, const LuaObj& a3, const LuaObj& a4, const LuaObj& a5, int flags) {
    return call<void*, void*, void*, void*, void*>(handle, a1.handle(), a2.handle(), a3.handle(), a4.handle(), a5.handle(), flags);
}
// 5 extra args, A1=LuaObj
template<typename A2, typename A3, typename A4, typename A5>
inline void* call(void* handle, const LuaObj& a1, const A2& a2, const A3& a3, const A4& a4, const A5& a5, int flags) {
    return call<void*, A2, A3, A4, A5>(handle, a1.handle(), a2, a3, a4, a5, flags);
}
// 5 extra args, A2=LuaObj
template<typename A1, typename A3, typename A4, typename A5>
inline void* call(void* handle, const A1& a1, const LuaObj& a2, const A3& a3, const A4& a4, const A5& a5, int flags) {
    return call<A1, void*, A3, A4, A5>(handle, a1, a2.handle(), a3, a4, a5, flags);
}
// 5 extra args, A3=LuaObj
template<typename A1, typename A2, typename A4, typename A5>
inline void* call(void* handle, const A1& a1, const A2& a2, const LuaObj& a3, const A4& a4, const A5& a5, int flags) {
    return call<A1, A2, void*, A4, A5>(handle, a1, a2, a3.handle(), a4, a5, flags);
}
// 5 extra args, A4=LuaObj
template<typename A1, typename A2, typename A3, typename A5>
inline void* call(void* handle, const A1& a1, const A2& a2, const A3& a3, const LuaObj& a4, const A5& a5, int flags) {
    return call<A1, A2, A3, void*, A5>(handle, a1, a2, a3, a4.handle(), a5, flags);
}
// 5 extra args, A5=LuaObj
template<typename A1, typename A2, typename A3, typename A4>
inline void* call(void* handle, const A1& a1, const A2& a2, const A3& a3, const A4& a4, const LuaObj& a5, int flags) {
    return call<A1, A2, A3, A4, void*>(handle, a1, a2, a3, a4, a5.handle(), flags);
}

} // namespace Rbxl

#endif // RBXL_HPP
