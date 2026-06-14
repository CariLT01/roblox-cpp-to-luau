// rbxl.hpp — Roblox API bindings for this freestanding RISC-V environment
//
// Data types (Vector3, Color3, CFrame) and syscall wrappers for Roblox
// Luau VM integration. Heap operations (malloc/free/heapUsed) and
// vector<T> are in heap.hpp; uint8_t is in types.hpp.

#ifndef RBXL_HPP
#define RBXL_HPP

#include "math.hpp"
#include "enums.hpp"

#define RBXL_METHOD_HAS_RETURN_BIT 1 << 0
#define RBXL_METHOD_RETURN_IS_OBJ_BIT 1 << 1
#define RBXL_METHOD_CALL_TARGET_IS_SERVICE_BIT 1 << 2
#define RBXL_METHOD_ARG_1_IS_STRING_BIT 1 << 3
#define RBXL_METHOD_ARG_2_IS_STRING_BIT 1 << 4
#define RBXL_METHOD_RETURN_IS_BUFFER_BIT 1 << 5
#define RBXL_METHOD_ARG_3_IS_STRING_BIT 1 << 6
#define RBXL_METHOD_ARG_4_IS_STRING_BIT 1 << 7
#define RBXL_METHOD_IS_STATIC_BIT 1 << 8
#define RBXL_METHOD_ARG_1_IS_BUFFER_BIT 1 << 9
#define RBXL_METHOD_ARG_2_IS_BUFFER_BIT 1 << 10
#define RBXL_METHOD_ARG_3_IS_BUFFER_BIT 1 << 11
#define RBXL_METHOD_ARG_4_IS_BUFFER_BIT 1 << 12
#define RBXL_METHOD_ARG_1_IS_FUNCTION_BIT 1 << 13
#define RBXL_METHOD_ARG_2_IS_FUNCTION_BIT 1 << 14
#define RBXL_METHOD_ARG_3_IS_FUNCTION_BIT 1 << 15
#define RBXL_METHOD_ARG_4_IS_FUNCTION_BIT 1 << 16



struct Vector3 {
    float x, y, z;
    Vector3() : x(0), y(0), z(0) {}
    Vector3(float x_, float y_, float z_) : x(x_), y(y_), z(z_) {}
};

struct Color3 {
    float r, g, b;
    Color3() : r(0), g(0), b(0) {}
    Color3(float r_, float g_, float b_) : r(r_), g(g_), b(b_) {}
};

// ── UDim2: 4-float 2D size/position (X.Scale, X.Offset, Y.Scale, Y.Offset) ──
struct UDim2 {
    float d[4];

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

    CFrame() {
        for (int i = 0; i < 12; i++) d[i] = 0.0f;
        d[0] = 0.0f; d[1] = 0.0f; d[2] = 0.0f;  // identity position
        d[3] = 1.0f; d[4] = 0.0f; d[5] = 0.0f;   // right
        d[6] = 0.0f; d[7] = 1.0f; d[8] = 0.0f;   // top
        d[9] = 0.0f; d[10] = 0.0f; d[11] = 1.0f; // -look (forward = -look = (0,0,-1), so look = (0,0,1))
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

    // Accessors
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

    // Operations are defined after Vector3 math helpers
};

// Vector3 math helpers used by CFrame
namespace { inline Vector3 v3_cross(const Vector3& a, const Vector3& b) { return Vector3(a.y*b.z - a.z*b.y, a.z*b.x - a.x*b.z, a.x*b.y - a.y*b.x); } }
namespace { inline Vector3 v3_sub(const Vector3& a, const Vector3& b) { return Vector3(a.x-b.x, a.y-b.y, a.z-b.z); } }
namespace { inline Vector3 v3_add(const Vector3& a, const Vector3& b) { return Vector3(a.x+b.x, a.y+b.y, a.z+b.z); } }
namespace { inline Vector3 v3_mul(const Vector3& a, float s) { return Vector3(a.x*s, a.y*s, a.z*s); } }
namespace { inline Vector3 v3_unit(const Vector3& v) { float len = v.x*v.x+v.y*v.y+v.z*v.z; if (len > 0.000001f) { float x2 = len * 0.5f; int i = *(int*)&len; i = 0x5f3759df - (i >> 1); float y = *(float*)&i; y = y * (1.5f - x2 * y * y); y = y * (1.5f - x2 * y * y); return v3_mul(v, y); } return v; } }

// CFrame operations (defined after helpers)
inline CFrame cframe_lookAt(const Vector3& pos, const Vector3& target) {
    Vector3 forward = v3_unit(v3_sub(target, pos));
    Vector3 worldUp(0.0f, 1.0f, 0.0f);
    Vector3 right = v3_unit(v3_cross(forward, worldUp));
    Vector3 up = v3_cross(right, forward);
    return CFrame(pos.x, pos.y, pos.z,
        right.x, up.x, -forward.x,
        right.y, up.y, -forward.y,
        right.z, up.z, -forward.z);
}
inline CFrame cframe_mul(const CFrame& a, const CFrame& b) {
    // New position = a.rotation * b.position + a.position
    float px = a.d[3]*b.d[0] + a.d[4]*b.d[1] + a.d[5]*b.d[2] + a.d[0];
    float py = a.d[6]*b.d[0] + a.d[7]*b.d[1] + a.d[8]*b.d[2] + a.d[1];
    float pz = a.d[9]*b.d[0] + a.d[10]*b.d[1] + a.d[11]*b.d[2] + a.d[2];
    // New rotation = a.rotation * b.rotation
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
    // Rotation inverse = transpose
    float r00=cf.d[3], r01=cf.d[6], r02=cf.d[9];
    float r10=cf.d[4], r11=cf.d[7], r12=cf.d[10];
    float r20=cf.d[5], r21=cf.d[8], r22=cf.d[11];
    // Position = -R^T * T
    float px = -(r00*cf.d[0] + r01*cf.d[1] + r02*cf.d[2]);
    float py = -(r10*cf.d[0] + r11*cf.d[1] + r12*cf.d[2]);
    float pz = -(r20*cf.d[0] + r21*cf.d[1] + r22*cf.d[2]);
    return CFrame(px, py, pz, r00, r01, r02, r10, r11, r12, r20, r21, r22);
}
inline Vector3 cframe_pointToWorld(const CFrame& cf, const Vector3& v) {
    return Vector3(
        cf.d[3]*v.x + cf.d[4]*v.y + cf.d[5]*v.z + cf.d[0],
        cf.d[6]*v.x + cf.d[7]*v.y + cf.d[8]*v.z + cf.d[1],
        cf.d[9]*v.x + cf.d[10]*v.y + cf.d[11]*v.z + cf.d[2]);
}
inline Vector3 cframe_pointToObject(const CFrame& cf, const Vector3& v) {
    return cframe_pointToWorld(cframe_inverse(cf), v);
}
inline Vector3 cframe_vectorToWorld(const CFrame& cf, const Vector3& v) {
    return Vector3(
        cf.d[3]*v.x + cf.d[4]*v.y + cf.d[5]*v.z,
        cf.d[6]*v.x + cf.d[7]*v.y + cf.d[8]*v.z,
        cf.d[9]*v.x + cf.d[10]*v.y + cf.d[11]*v.z);
}
inline Vector3 cframe_vectorToObject(const CFrame& cf, const Vector3& v) {
    // inverse rotation (transpose) * v
    return Vector3(
        cf.d[3]*v.x + cf.d[6]*v.y + cf.d[9]*v.z,
        cf.d[4]*v.x + cf.d[7]*v.y + cf.d[10]*v.z,
        cf.d[5]*v.x + cf.d[8]*v.y + cf.d[11]*v.z);
}

// Creates a CFrame from Euler angles (in radians).
// Rotation order: R = Rz * Ry * Rx (same as Roblox CFrame.fromEulerAnglesXYZ).
inline CFrame cframe_fromEulerAngles(float rx, float ry, float rz) {
    float sx = math::sin(rx);
    float cx = math::cos(rx);
    float sy = math::sin(ry);
    float cy = math::cos(ry);
    float sz = math::sin(rz);
    float cz = math::cos(rz);

    // Right column (d[3], d[6], d[9])
    float r00 = cy * cz;
    float r10 = cy * sz;
    float r20 = -sy;

    // Up column (d[4], d[7], d[10])
    float r01 = sx * sy * cz - cx * sz;
    float r11 = sx * sy * sz + cx * cz;
    float r21 = sx * cy;

    // -Look column (d[5], d[8], d[11])
    float r02 = cx * sy * cz + sx * sz;
    float r12 = cx * sy * sz - sx * cz;
    float r22 = cx * cy;

    return CFrame(0.0f, 0.0f, 0.0f, r00, r01, r02, r10, r11, r12, r20, r21, r22);
}

namespace Rbxl {
    // Syscall 4: Null-terminated String Pointer
    void print(const char* str) {
        asm volatile ("mv a0, %0; li a7, 4; ecall" : : "r"(str) : "a0", "a7");
    }

    // Syscall 5: Integer Value
    void print(int val) {
        asm volatile ("mv a0, %0; li a7, 5; ecall" : : "r"(val) : "a0", "a7");
    }

    // Syscall 6: Boolean Value (0 or 1)
    void print(bool val) {
        asm volatile ("mv a0, %0; li a7, 6; ecall" : : "r"((int)val) : "a0", "a7");
    }

    // Syscall 7: Float Pointer (Passed via RAM pointer to keep tracking unified)
    void print(float val) {
        volatile float v = val;
        volatile float* ptr = &v;
        asm volatile ("mv a0, %0; li a7, 7; ecall" : : "r"(ptr) : "a0", "a7", "memory");
    }

    // Syscall 8: Create a new Part, returns an opaque handle (stored in a0 by VM)
    void* createPart() {
        void* handle = nullptr;
        asm volatile ("li a7, 8; ecall; mv %0, a0" : "=r"(handle) : : "a0", "a7");
        return handle;
    }

    // --- Templated Property Access (float, int, bool, etc.) ---

    template<typename T>
    T getProperty(void* handle, const char* propName);

    template<typename T>
    void setProperty(void* handle, const char* propName, T value);

    // Syscall 9: GetProperty<float> — returns float value as raw bits in a0
    template<>
    float getProperty<float>(void* handle, const char* propName) {
        float result = 0.0f;
        asm volatile (
            "mv a0, %1; mv a1, %2; li a7, 9; ecall; mv %0, a0"
            : "=r"(result)
            : "r"(handle), "r"(propName)
            : "a0", "a1", "a7"
        );
        return result;
    }

    // Syscall 10: SetProperty<float> — pass handle, propName, and float value
    template<>
    void setProperty<float>(void* handle, const char* propName, float value) {
        asm volatile (
            "mv a0, %0; mv a1, %1; mv a2, %2; li a7, 10; ecall"
            :
            : "r"(handle), "r"(propName), "r"(value)
            : "a0", "a1", "a2", "a7"
        );
    }

    // --- Vector3 Property Access (standalone — Vector3 is multi-field) ---

    // Syscall 11: Get Vector3 property — writes x/y/z (as float bits) to *out
    void getPropertyVector3(void* handle, const char* propName, Vector3* out) {
        asm volatile (
            "mv a0, %0; mv a1, %1; mv a2, %2; li a7, 11; ecall"
            :
            : "r"(handle), "r"(propName), "r"(out)
            : "a0", "a1", "a2", "a7", "memory"
        );
    }

    // Syscall 12: Set Vector3 property — set from x,y,z float bits
    void setPropertyVector3(void* handle, const char* propName, float x, float y, float z) {
        asm volatile (
            "mv a0, %0; mv a1, %1; mv a2, %2; mv a3, %3; mv a4, %4; li a7, 12; ecall"
            :
            : "r"(handle), "r"(propName), "r"(x), "r"(y), "r"(z)
            : "a0", "a1", "a2", "a3", "a4", "a7"
        );
    }

    // --- Instance Tree Operations ---

    // Syscall 13: FindFirstChild — returns child handle or null (0) in a0
    void* findFirstChild(void* handle, const char* name) {
        void* result = nullptr;
        asm volatile (
            "mv a0, %1; mv a1, %2; li a7, 13; ecall; mv %0, a0"
            : "=r"(result)
            : "r"(handle), "r"(name)
            : "a0", "a1", "a7"
        );
        return result;
    }

    // Syscall 14: WaitForChild — blocks until child exists, returns handle in a0
    void* waitForChild(void* handle, const char* name) {
        void* result = nullptr;
        asm volatile (
            "mv a0, %1; mv a1, %2; li a7, 14; ecall; mv %0, a0"
            : "=r"(result)
            : "r"(handle), "r"(name)
            : "a0", "a1", "a7"
        );
        return result;
    }

    // Syscall 15: Destroy — destroys the instance
    void destroy(void* handle) {
        asm volatile (
            "mv a0, %0; li a7, 15; ecall"
            :
            : "r"(handle)
            : "a0", "a7"
        );
    }

    // Syscall 16: Clone — returns cloned instance handle in a0
    void* clone(void* handle) {
        void* result = nullptr;
        asm volatile (
            "mv a0, %1; li a7, 16; ecall; mv %0, a0"
            : "=r"(result)
            : "r"(handle)
            : "a0", "a7"
        );
        return result;
    }

    // --- String/Bool Property Access ---

    // Syscall 17: SetProperty<String> — sets a string property
    void setPropertyString(void* handle, const char* propName, const char* value) {
        asm volatile (
            "mv a0, %0; mv a1, %1; mv a2, %2; li a7, 17; ecall"
            :
            : "r"(handle), "r"(propName), "r"(value)
            : "a0", "a1", "a2", "a7"
        );
    }

    // Syscall 18: SetProperty<Bool> — sets a boolean property
    void setPropertyBool(void* handle, const char* propName, bool value) {
        asm volatile (
            "mv a0, %0; mv a1, %1; mv a2, %2; li a7, 18; ecall"
            :
            : "r"(handle), "r"(propName), "r"((int)value)
            : "a0", "a1", "a2", "a7"
        );
    }

    // --- Color3 Property Access ---

    // Syscall 19: Get Color3 property — writes r/g/b (as float bits) to *out
    void getPropertyColor3(void* handle, const char* propName, Color3* out) {
        asm volatile (
            "mv a0, %0; mv a1, %1; mv a2, %2; li a7, 19; ecall"
            :
            : "r"(handle), "r"(propName), "r"(out)
            : "a0", "a1", "a2", "a7", "memory"
        );
    }

    // Syscall 20: Set Color3 property — set from r,g,b float bits
    void setPropertyColor3(void* handle, const char* propName, float r, float g, float b) {
        asm volatile (
            "mv a0, %0; mv a1, %1; mv a2, %2; mv a3, %3; mv a4, %4; li a7, 20; ecall"
            :
            : "r"(handle), "r"(propName), "r"(r), "r"(g), "r"(b)
            : "a0", "a1", "a2", "a3", "a4", "a7"
        );
    }

    // --- Buffer Operations ---

    // Syscall 21: Create a buffer of 'size' bytes, returns opaque handle in a0
    void* createBuffer(unsigned int size) {
        void* handle = nullptr;
        asm volatile (
            "mv a0, %1; li a7, 21; ecall; mv %0, a0"
            : "=r"(handle)
            : "r"(size)
            : "a0", "a7"
        );
        return handle;
    }

    // Syscall 22: Free/destroy a buffer
    void freeBuffer(void* handle) {
        asm volatile (
            "mv a0, %0; li a7, 22; ecall"
            :
            : "r"(handle)
            : "a0", "a7"
        );
    }

    // Syscall 23: Get buffer length in bytes, returns size in a0 (0 if invalid handle)
    unsigned int bufferLen(void* handle) {
        unsigned int result = 0;
        asm volatile (
            "mv a0, %1; li a7, 23; ecall; mv %0, a0"
            : "=r"(result)
            : "r"(handle)
            : "a0", "a7"
        );
        return result;
    }

    // Syscall 24: Read signed 8-bit integer from buffer at offset
    int bufferReadI8(void* handle, unsigned int offset) {
        int result = 0;
        asm volatile (
            "mv a0, %1; mv a1, %2; li a7, 24; ecall; mv %0, a0"
            : "=r"(result)
            : "r"(handle), "r"(offset)
            : "a0", "a1", "a7"
        );
        return result;
    }

    // Syscall 25: Write signed 8-bit integer to buffer at offset
    void bufferWriteI8(void* handle, unsigned int offset, int value) {
        asm volatile (
            "mv a0, %0; mv a1, %1; mv a2, %2; li a7, 25; ecall"
            :
            : "r"(handle), "r"(offset), "r"(value)
            : "a0", "a1", "a2", "a7"
        );
    }

    // Syscall 26: Read signed 32-bit integer from buffer at offset
    int bufferReadI32(void* handle, unsigned int offset) {
        int result = 0;
        asm volatile (
            "mv a0, %1; mv a1, %2; li a7, 26; ecall; mv %0, a0"
            : "=r"(result)
            : "r"(handle), "r"(offset)
            : "a0", "a1", "a7"
        );
        return result;
    }

    // Syscall 27: Write signed 32-bit integer to buffer at offset
    void bufferWriteI32(void* handle, unsigned int offset, int value) {
        asm volatile (
            "mv a0, %0; mv a1, %1; mv a2, %2; li a7, 27; ecall"
            :
            : "r"(handle), "r"(offset), "r"(value)
            : "a0", "a1", "a2", "a7"
        );
    }

    // Syscall 28: Read 32-bit float from buffer at offset (returns raw bits as int)
    float bufferReadF32(void* handle, unsigned int offset) {
        float result = 0.0f;
        asm volatile (
            "mv a0, %1; mv a1, %2; li a7, 28; ecall; mv %0, a0"
            : "=r"(result)
            : "r"(handle), "r"(offset)
            : "a0", "a1", "a7"
        );
        return result;
    }

    // Syscall 29: Write 32-bit float to buffer at offset
    void bufferWriteF32(void* handle, unsigned int offset, float value) {
        asm volatile (
            "mv a0, %0; mv a1, %1; mv a2, %2; li a7, 29; ecall"
            :
            : "r"(handle), "r"(offset), "r"(value)
            : "a0", "a1", "a2", "a7"
        );
    }

    // Syscall 50: buffer.fromstring(str) — returns buffer handle in a0
    void* bufferFromString(const char* str) {
        void* handle = nullptr;
        asm volatile (
            "mv a0, %1; li a7, 50; ecall; mv %0, a0"
            : "=r"(handle)
            : "r"(str)
            : "a0", "a7"
        );
        return handle;
    }

    // Syscall 51: getMethod(handle, methodName) — returns RBXScriptSignal handle in a0
    void* getMethod(void* handle, const char* methodName) {
        void* result = nullptr;
        asm volatile (
            "mv a0, %1; mv a1, %2; li a7, 51; ecall; mv %0, a0"
            : "=r"(result)
            : "r"(handle), "r"(methodName)
            : "a0", "a1", "a7"
        );
        return result;
    }

    // --- Task/Yielding ---

    // Syscall 45: task.wait(n) — yields the VM for n seconds, returns actual time waited
    float taskWait(float seconds) {
        float result = 0.0f;
        asm volatile (
            "mv a0, %1; li a7, 45; ecall; mv %0, a0"
            : "=r"(result)
            : "r"(seconds)
            : "a0", "a7"
        );
        return result;
    }

    // Syscall 33: Get workspace — returns handle to the workspace instance
    void* getWorkspace() {
        void* handle = nullptr;
        asm volatile (
            "li a7, 33; ecall; mv %0, a0"
            : "=r"(handle)
            :
            : "a0", "a7"
        );
        return handle;
    }

    // --- CFrame Property Access ---

    // Syscall 34: Get CFrame property — writes 12 floats (48 bytes) to *out
    void getPropertyCFrame(void* handle, const char* propName, void* out) {
        asm volatile (
            "mv a0, %0; mv a1, %1; mv a2, %2; li a7, 34; ecall"
            :
            : "r"(handle), "r"(propName), "r"(out)
            : "a0", "a1", "a2", "a7", "memory"
        );
    }

    // Syscall 35: Set CFrame property — reads 12 floats (48 bytes) from *src
    void setPropertyCFrame(void* handle, const char* propName, void* src) {
        asm volatile (
            "mv a0, %0; mv a1, %1; mv a2, %2; li a7, 35; ecall"
            :
            : "r"(handle), "r"(propName), "r"(src)
            : "a0", "a1", "a2", "a7", "memory"
        );
    }

    // --- Players Service ---

    // Syscall 36: Get the Players service — returns handle to Players (or null)
    void* getPlayers() {
        void* handle = nullptr;
        asm volatile (
            "li a7, 36; ecall; mv %0, a0"
            : "=r"(handle)
            :
            : "a0", "a7"
        );
        return handle;
    }

    // Syscall 37: Get LocalPlayer from a Players handle — returns Player handle (or null)
    void* getLocalPlayer(void* playersHandle) {
        void* handle = nullptr;
        asm volatile (
            "mv a0, %1; li a7, 37; ecall; mv %0, a0"
            : "=r"(handle)
            : "r"(playersHandle)
            : "a0", "a7"
        );
        return handle;
    }

    // --- Generic Instance Creation ---

    // Syscall 42: Get enum property — returns the enum index as an int in a0
    int getPropertyEnum(void* handle, const char* propName) {
        int result = 0;
        asm volatile (
            "mv a0, %1; mv a1, %2; li a7, 42; ecall; mv %0, a0"
            : "=r"(result)
            : "r"(handle), "r"(propName)
            : "a0", "a1", "a7"
        );
        return result;
    }

    // Syscall 43: Set enum property — pass handle, propName, and enum index
    void setPropertyEnum(void* handle, const char* propName, int enumValue) {
        asm volatile (
            "mv a0, %0; mv a1, %1; mv a2, %2; li a7, 43; ecall"
            :
            : "r"(handle), "r"(propName), "r"(enumValue)
            : "a0", "a1", "a2", "a7"
        );
    }

    // Syscall 44: Set Instance property — pass handle, propName, and target instance handle
    void setPropertyInstance(void* handle, const char* propName, void* targetHandle) {
        asm volatile (
            "mv a0, %0; mv a1, %1; mv a2, %2; li a7, 44; ecall"
            :
            : "r"(handle), "r"(propName), "r"(targetHandle)
            : "a0", "a1", "a2", "a7"
        );
    }

    // Syscall 38: Create an Instance of any type by name — returns handle (or null)
    void* createInstance(const char* typeName) {
        void* handle = nullptr;
        asm volatile (
            "mv a0, %1; li a7, 38; ecall; mv %0, a0"
            : "=r"(handle)
            : "r"(typeName)
            : "a0", "a7"
        );
        return handle;
    }

    // Syscall 47: Generic getService(name) — returns raw handle to any Roblox service instance
    void* getService(const char* name) {
        void* handle = nullptr;
        asm volatile (
            "mv a0, %1; li a7, 47; ecall; mv %0, a0"
            : "=r"(handle)
            : "r"(name)
            : "a0", "a7"
        );
        return handle;
    }
}

// ── Instance: base class for all Roblox instances ──
class Instance {
protected:
    void* h;
public:
    Instance() : h(nullptr) {}
    Instance(void* handle) : h(handle) {}

    bool valid() const { return h != nullptr; }
    void* handle() const { return h; }

    void destroy() { if (h) { Rbxl::destroy(h); h = nullptr; } }
    Instance clone() const { return Instance(Rbxl::clone(h)); }
    Instance findFirstChild(const char* name) const { return Instance(Rbxl::findFirstChild(h, name)); }
    Instance waitForChild(const char* name) const { return Instance(Rbxl::waitForChild(h, name)); }

    // ── Generic typed property access (use on any Instance type) ──

    void setPropertyFloat(const char* name, float v)   { Rbxl::setProperty<float>(h, name, v); }
    float getPropertyFloat(const char* name)            { return Rbxl::getProperty<float>(h, name); }

    void setPropertyVector3(const char* name, const Vector3& v) {
        Rbxl::setPropertyVector3(h, name, v.x, v.y, v.z);
    }
    Vector3 getPropertyVector3(const char* name) {
        Vector3 v; Rbxl::getPropertyVector3(h, name, &v); return v;
    }

    void setPropertyColor3(const char* name, const Color3& c) {
        Rbxl::setPropertyColor3(h, name, c.r, c.g, c.b);
    }
    Color3 getPropertyColor3(const char* name) {
        Color3 c; Rbxl::getPropertyColor3(h, name, &c); return c;
    }

    void setPropertyCFrame(const char* name, const CFrame& cf) {
        Rbxl::setPropertyCFrame(h, name, (void*)cf.d);
    }
    CFrame getPropertyCFrame(const char* name) {
        CFrame cf; Rbxl::getPropertyCFrame(h, name, cf.d); return cf;
    }

    void setPropertyString(const char* name, const char* val) { Rbxl::setPropertyString(h, name, val); }
    void setPropertyBool(const char* name, bool v)             { Rbxl::setPropertyBool(h, name, v); }

    void setPropertyEnum(const char* name, int enumValue)      { Rbxl::setPropertyEnum(h, name, enumValue); }
    int getPropertyEnum(const char* name)                       { return Rbxl::getPropertyEnum(h, name); }

    void setPropertyEnum(const char* name, Rbxl::Enum e)       { Rbxl::setPropertyEnum(h, name, (int)e); }
    Rbxl::Enum getPropertyEnumTyped(const char* name)           { return (Rbxl::Enum)Rbxl::getPropertyEnum(h, name); }

    void setPropertyInstance(const char* name, const Instance& target) { Rbxl::setPropertyInstance(h, name, target.handle()); }
    void setParent(const Instance& parent) { setPropertyInstance("Parent", parent); }

    // ── Convenience methods ──

    void setName(const char* name)   { setPropertyString("Name", name); }
    void setAnchored(bool v)         { setPropertyBool("Anchored", v); }

    static Instance getWorkspace()  { return Instance(Rbxl::getWorkspace()); }
    static Instance getPlayers()    { return Instance(Rbxl::getPlayers()); }
    static Instance getService(const char* name) { return Rbxl::getService(name); }
    Instance getLocalPlayer() const { return Instance(Rbxl::getLocalPlayer(h)); }

    static Instance New(const char* typeName) { return Instance(Rbxl::createInstance(typeName)); }

    // Returns the RBXScriptSignal (or other method-accessible member) for the
    // given name. You can then call callMethod("Connect", ...) on the result.
    Instance getMethod(const char* methodName) const {
        return Instance(Rbxl::getMethod(h, methodName));
    }

    // ── Generic method call (uses syscall 46) ──
    // Register layout: a0=handle, a1=methodName, a2..a6=args, a3=flags
    // flags bits: 0=hasReturn, 1=returnIsObject, 2=isService, 3=arg1IsString,
    //             4=arg2IsString, 5=returnIsBuffer, 6=arg3IsString, 7=arg4IsString,
    //             8=isStaticCall, 9=arg1IsBuffer, 10=arg2IsBuffer, 11=arg3IsBuffer,
    //             12=arg4IsBuffer, 13=arg1IsFunction, 14=arg2IsFunction,
    //             15=arg3IsFunction, 16=arg4IsFunction
    //
    // 0 extra args — methodName + flags only
    void* callMethod(const char* methodName, int flags) const {
        void* result = nullptr;
        asm volatile (
            "mv a0, %1; mv a1, %2; mv a3, %3; li a7, 46; ecall; mv %0, a0"
            : "=r"(result)
            : "r"(h), "r"(methodName), "r"(flags)
            : "a0", "a1", "a3", "a7"
        );
        return result;
    }

    // 1 extra arg (kept as explicit non-template overload for backward compatibility;
    // also shadows the template version below for const char* to guarantee exact match)
    void* callMethod(const char* methodName, const char* arg, int flags) const {
        void* result = nullptr;
        asm volatile (
            "mv a0, %1; mv a1, %2; mv a2, %3; mv a3, %4; li a7, 46; ecall; mv %0, a0"
            : "=r"(result)
            : "r"(h), "r"(methodName), "r"(arg), "r"(flags)
            : "a0", "a1", "a2", "a3", "a7"
        );
        return result;
    }

    // 1 extra arg (generic template — int, float, void*, bool, etc.)
    template<typename A1>
    void* callMethod(const char* methodName, A1 a1, int flags) const {
        void* result = nullptr;
        asm volatile (
            "mv a0, %1; mv a1, %2; mv a2, %3; mv a3, %4; li a7, 46; ecall; mv %0, a0"
            : "=r"(result)
            : "r"(h), "r"(methodName), "r"(a1), "r"(flags)
            : "a0", "a1", "a2", "a3", "a7"
        );
        return result;
    }

    // 2 extra args — a0:h, a1:method, a2:arg1, a3:flags, a4:arg2
    template<typename A1, typename A2>
    void* callMethod(const char* methodName, A1 a1, A2 a2, int flags) const {
        void* result = nullptr;
        asm volatile (
            "mv a0, %1; mv a1, %2; mv a2, %3; mv a3, %4; mv a4, %5; li a7, 46; ecall; mv %0, a0"
            : "=r"(result)
            : "r"(h), "r"(methodName), "r"(a1), "r"(flags), "r"(a2)
            : "a0", "a1", "a2", "a3", "a4", "a7"
        );
        return result;
    }

    // 3 extra args — a0:h, a1:method, a2:arg1, a3:flags, a4:arg2, a5:arg3
    template<typename A1, typename A2, typename A3>
    void* callMethod(const char* methodName, A1 a1, A2 a2, A3 a3, int flags) const {
        void* result = nullptr;
        asm volatile (
            "mv a0, %1; mv a1, %2; mv a2, %3; mv a3, %4; mv a4, %5; mv a5, %6; li a7, 46; ecall; mv %0, a0"
            : "=r"(result)
            : "r"(h), "r"(methodName), "r"(a1), "r"(flags), "r"(a2), "r"(a3)
            : "a0", "a1", "a2", "a3", "a4", "a5", "a7"
        );
        return result;
    }

    // 4 extra args — a0:h, a1:method, a2:arg1, a3:flags, a4:arg2, a5:arg3, a6:arg4
    template<typename A1, typename A2, typename A3, typename A4>
    void* callMethod(const char* methodName, A1 a1, A2 a2, A3 a3, A4 a4, int flags) const {
        void* result = nullptr;
        asm volatile (
            "mv a0, %1; mv a1, %2; mv a2, %3; mv a3, %4; mv a4, %5; mv a5, %6; mv a6, %7; li a7, 46; ecall; mv %0, a0"
            : "=r"(result)
            : "r"(h), "r"(methodName), "r"(a1), "r"(flags), "r"(a2), "r"(a3), "r"(a4)
            : "a0", "a1", "a2", "a3", "a4", "a5", "a6", "a7"
        );
        return result;
    }

    // ── Static method call (uses syscall 46 + isStatic flag bit 8=256) ──
    // Same register layout as callMethod but passes flags|256 so the transpiler
    // emits obj.method(args) instead of obj:method(args) (no implicit self).
    //
    // 0 extra args
    void* callMethodStatic(const char* methodName, int flags) const {
        return callMethod(methodName, flags | 256);
    }

    // 1 extra arg — const char* (shadows template for exact match)
    void* callMethodStatic(const char* methodName, const char* arg, int flags) const {
        return callMethod(methodName, arg, flags | 256);
    }

    // 1 extra arg (generic template)
    template<typename A1>
    void* callMethodStatic(const char* methodName, A1 a1, int flags) const {
        return callMethod(methodName, a1, flags | 256);
    }

    // 2 extra args
    template<typename A1, typename A2>
    void* callMethodStatic(const char* methodName, A1 a1, A2 a2, int flags) const {
        return callMethod(methodName, a1, a2, flags | 256);
    }

    // 3 extra args
    template<typename A1, typename A2, typename A3>
    void* callMethodStatic(const char* methodName, A1 a1, A2 a2, A3 a3, int flags) const {
        return callMethod(methodName, a1, a2, a3, flags | 256);
    }

    // 4 extra args
    template<typename A1, typename A2, typename A3, typename A4>
    void* callMethodStatic(const char* methodName, A1 a1, A2 a2, A3 a3, A4 a4, int flags) const {
        return callMethod(methodName, a1, a2, a3, a4, flags | 256);
    }
};

// ── Part: a physical Part instance ──
class Part : public Instance {
public:
    Part() : Instance() {}
    Part(void* handle) : Instance(handle) {}
    Part(const Instance& other) : Instance(other.handle()) {}

    static Part create() { return Part(Rbxl::createPart()); }

    void setPosition(float x, float y, float z) { setPropertyVector3("Position", Vector3(x, y, z)); }
    Vector3 getPosition() { return getPropertyVector3("Position"); }

    void setSize(float x, float y, float z) { setPropertyVector3("Size", Vector3(x, y, z)); }
    Vector3 getSize() { return getPropertyVector3("Size"); }

    void setColor(float r, float g, float b) { setPropertyColor3("Color", Color3(r, g, b)); }
    Color3 getColor() { return getPropertyColor3("Color"); }

    void setTransparency(float v) { setPropertyFloat("Transparency", v); }
    float getTransparency() { return getPropertyFloat("Transparency"); }

    void setCFrame(const CFrame& cf) { setPropertyCFrame("CFrame", cf); }
    CFrame getCFrame() { return getPropertyCFrame("CFrame"); }
};

#endif // RBXL_HPP
