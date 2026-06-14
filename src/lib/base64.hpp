// base64.hpp — Base64 decoder using Roblox's EncodingService
//
// Uses Instance::getService("EncodingService") (cached) + Instance::callMethod("Base64Decode").
// All functions are inline; no standard library dependencies.
// Requires "types.hpp" for uint8_t, "heap.hpp" for vector<T>, and "rbxl.hpp" for Instance.
//
// Usage:
//   vector<uint8_t> decoded;
//   base64_decode(imageData, decoded);  // imageData is a null-terminated base64 string
//   // decoded[0..n-1] has the raw bytes

#ifndef BASE64_HPP
#define BASE64_HPP

#include "types.hpp"
#include "heap.hpp"
#include "rbxl.hpp"

// Decodes a null-terminated base64 string into raw bytes using Roblox's EncodingService.
// Returns the number of bytes decoded, or 0 on failure.
inline unsigned int base64_decode(const char* input, vector<uint8_t>& output) {
    Rbxl::print("Call to base64 decode");
    if (!input || !input[0]) return 0;

    // Cache the EncodingService instance (static, only fetched once)
    static Instance encodingSvc;
    if (!encodingSvc.valid()) {
        encodingSvc = Instance::getService("EncodingService");
    }

    // Call EncodingService:Base64Decode via Instance::callMethod
    // flags: hasReturn(1) | returnIsBuffer(32) | arg1IsBuffer(512) = 545
    void* buf = encodingSvc.callMethod("Base64Decode", Rbxl::bufferFromString(input), 545);

    Rbxl::print("Reading buffer into vector");

    // Read decoded bytes from the buffer into our vector
    unsigned int len = Rbxl::bufferLen(buf);
    Rbxl::print("The length of the buffer is:");
    Rbxl::print(static_cast<int>(len));
    output.clear();
    for (unsigned int i = 0; i < len; i++) {
        if (i % 1000 == 0) {
            Rbxl::print("Progress:");
            Rbxl::print(static_cast<int>(i));
            Rbxl::taskWait(0.1f);
        } 
        output.push_back((uint8_t)Rbxl::bufferReadI8(buf, i));
    }

    // Free the buffer
    Rbxl::freeBuffer(buf);
    return len;
}

#endif // BASE64_HPP
