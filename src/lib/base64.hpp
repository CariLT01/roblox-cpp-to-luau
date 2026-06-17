// base64.hpp — Base64 decoder using Roblox's EncodingService
//
// Uses LuaObj::getService("EncodingService") (cached) + LuaObj::callMethod("Base64Decode").
// All functions are inline; no standard library dependencies.
// Requires "types.hpp" for uint8_t, "heap.hpp" for vector<T>, and "rbxl.hpp" for LuaObj.
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
    Lua::print("Call to base64 decode");
    if (!input || !input[0]) return 0;

    // Cache the EncodingService instance (static, only fetched once)
    static LuaObj encodingSvc;
    if (!encodingSvc.valid()) {
        encodingSvc = LuaObj::getService("EncodingService");
    }

    // Build an input buffer from the base64 string using Buffer struct
    Buffer inputBuf;
    {
        const char* p = input;
        while (*p && inputBuf.size < Buffer::MAX_SIZE) {
            inputBuf.data[inputBuf.size++] = (uint8_t)*p++;
        }
    }
    LuaObj inputBufHandle = LuaObj(inputBuf.toObject());

    // Call EncodingService:Base64Decode — input is the buffer handle, output is a buffer
    // flags: hasReturn(1) | returnIsObj(2) | arg1IsObj(131072) = 131075
    void* decodedBuf = encodingSvc.callMethod("Base64Decode", 131075, inputBufHandle);

    Lua::print("Reading buffer into vector");

    // Read decoded bytes using Buffer struct
    Buffer decoded;
    decoded.readFromObject(decodedBuf);
    Lua::print("The length of the buffer is:");
    Lua::print(static_cast<int>(decoded.size));
    output.clear();
    for (unsigned int i = 0; i < decoded.size; i++) {
        output.push_back(decoded.data[i]);
    }
    return decoded.size;
}

#endif // BASE64_HPP
