// main.cpp
#include "lib/math.hpp"
#include "lib/base64.hpp"

#include "lib/heap.hpp"
#include "lib/rbxl.hpp"
#include "imgData.hpp"
#include "lib/lua.hpp"

// 'volatile' prevents the compiler from optimizing the loop away at -O3
void delay(volatile int count) {
    while (count > 0) {
        count--;
    }
}

// __attribute__((noinline)) is required when compiling with -finline-functions:
// these are passed as function pointers (TaskSpawn, Connect) and must remain
// as standalone symbols in the assembly for the transpiler.
__attribute__((noinline))
void printFunc(int threadId) {
    for (int i = 0; i < 10; i++) {
        Lua::print("Thread");
        Lua::print(threadId);
        Lua::print(i);
        Lua::taskWait(1.0f);
    }
}

__attribute__((noinline))
void touchedCallback(LuaObj touchedInst) {
    Lua::print("Touched");
}

int main() {



        
    Lua::print("The start of the program");
    Lua::print("Version 3");

    LuaObj rs = Rbxl::getService("ReplicatedStorage");
    LuaObj moduleScript = (LuaObj) rs.findFirstChild("Shared").findFirstChild("Hello");
    LuaObj module = moduleScript.require();
    module.callMethodStatic("Hello", 0);
    Lua::print("Module already called!");


    LuaObj workspace = Rbxl::getWorkspace();
    PartWrapper baseplate = (PartWrapper) workspace.findFirstChild("Baseplate");

    
    

    LuaObj touchedEvent = baseplate.getMethod("Touched");
    touchedEvent.callMethod("Connect", (void*)touchedCallback, RBXL_METHOD_ARG_1_IS_FUNCTION_BIT);
    

    //Rbxl::taskSpawn(&printFunc);
    Lua::taskSpawn((void*)printFunc, 1);
    Lua::taskWait(1.0f);
    Lua::taskSpawn((void*)printFunc, 2);

    Lua::taskWait(2);
    Lua::print("Finished wait! Doing work!");
    Lua::taskWait(1);

    vector<uint8_t> decoded;
    base64_decode(imageData, decoded);

    // Print decoded image data as a string (or we could print the length)
    Lua::print("Decoded bytes:");
    Lua::print((int)decoded.size());
    Lua::print("Declaring variables #1");

    int bytesRead = 0;
    Lua::print("Declaring variables #2");

    int cursor = 0;

    Lua::print("Decoding first varint");

    int imgWidth = decodeVarint(decoded, cursor, &bytesRead);
    Lua::print("Increment");
    bytesRead = 0;
    Lua::print("Decoding second varint");
    int imgHeight = decodeVarint(decoded, cursor, &bytesRead);
    Lua::print("Increment");
    bytesRead = 0;

    const float scaleFactor = 10.0f;
    float canvasWidth = scaleFactor;
    float canvasHeight = scaleFactor * ((float)imgWidth / imgHeight);

    // --- math::rad, sin, cos test ---
    float rad90 = math::rad(90.0f);
    float sinHalfPi = math::sin(rad90);
    float cosPi = math::cos(math::rad(180.0f));

    // --- cframe_fromEulerAngles test ---
    CFrame eulerCf = cframe_fromEulerAngles(0.0f, rad90, 0.0f);

    


    Lua::print("Enter loop");

    while (cursor < decoded.size()) {
        Lua::print("header size");
        uint8_t headerSize = decoded[cursor];
        cursor++;

        Lua::print("Decode varints");
        int layerIndex = decodeVarint(decoded, cursor, &bytesRead);
        bytesRead = 0;
        int layerDataSize = decodeVarint(decoded, cursor, &bytesRead);
        bytesRead = 0;

        Lua::print("Target end cursor calc");
        int targetEndCursor = cursor + layerDataSize;
        Lua::print("Enter loop 2");
        Lua::print("Cursor, targetEndCursor");
        Lua::print(cursor);
        Lua::print(targetEndCursor);
        Lua::taskWait(0.0f);


        while (cursor < targetEndCursor) {

            //Lua::print("Execute task.wait");
            //Rbxl::taskWait(0.0f);

            // Lua::print("Decode varints");
            int x = decodeVarint(decoded, cursor, &bytesRead);
            bytesRead = 0;
            int y = decodeVarint(decoded, cursor, &bytesRead);
            bytesRead = 0;
            int w = decodeVarint(decoded, cursor, &bytesRead);
            bytesRead = 0;
            int h = decodeVarint(decoded, cursor, &bytesRead);
            bytesRead = 0;
            int rotation = decodeVarint(decoded, cursor, &bytesRead);
            bytesRead = 0;

            // Lua::print("Calculate colors");

            int colorR = decoded[cursor];
            int colorG = decoded[cursor + 1];
            int colorB = decoded[cursor + 2];
            int shapeType = decoded[cursor + 3];

            cursor += 4;

            // Lua::print("Process shape types");
            float centerX, centerY, width3D, height3D;
            if (shapeType == 1) {
                centerX = x;
                centerY = y;
                width3D = w * 2;
                height3D = w * 2;
            } else {
                centerX = x + ((float)w / 2);
                centerY = y + ((float)h / 2);
                width3D = w;
                height3D = h;
            }
            // Lua::print("Define vars");
            const float scale = 10.0f;
            float xP = scale * (1 - (centerX / imgWidth));
            float yP = scale * (1 - (centerY / imgHeight));
            float wP = scale * (width3D / imgWidth);
            float hP = scale * (height3D / imgHeight);
            float zP = -layerIndex * 2;
            
            float rad = math::rad(rotation);
            PartWrapper part;
            bool partCreated = false;
            // Lua::print("Create part");
            if (shapeType == 0) {
                part = Rbxl::createPart();
                part.setPropertyVector3("Size", Vector3(wP, hP, 0.1));
                CFrame cfRot = cframe_fromEulerAngles(0, 0, rad);
                CFrame cfPos = CFrame(xP, yP, zP);
                CFrame cf = cframe_mul(cfPos, cfRot);
                part.setPropertyCFrame("CFrame", cf);
                partCreated = true;
            } else if (shapeType == 1) {
                part = Rbxl::createPart();
                part.setPropertyEnum("Shape", Rbxl::Enum::PARTTYPE_CYLINDER);
                part.setSize(0.1, wP, hP);
                CFrame cfPos = CFrame(xP, yP, zP);
                CFrame cfRot1 = cframe_fromEulerAngles(0, math::rad(90), math::rad(180));
                CFrame cfRot2 = cframe_fromEulerAngles(rad, 0, 0);
                CFrame cf = cframe_mul(cfPos, cframe_mul(cfRot1, cfRot2));
                part.setPropertyCFrame("CFrame", cf);
                partCreated = true;
            } else if (shapeType == 2) {
                part = Rbxl::createInstance("WedgePart");
                part.setPropertyVector3("Size", Vector3(0.1, wP, hP));
                CFrame cfPos = CFrame(xP, yP, zP);
                CFrame cfRot1 = cframe_fromEulerAngles(0, math::rad(90), math::rad(180));
                CFrame cfRot2 = cframe_fromEulerAngles(rad, 0, 0);
                CFrame cf = cframe_mul(cfPos, cframe_mul(cfRot1, cfRot2));
                part.setPropertyCFrame("CFrame", cf);
                partCreated = true;

            }

            // Lua::print("Part created enter if");
            if (partCreated) {
                part.setPropertyEnum("Material", Rbxl::Enum::MATERIAL_SMOOTHPLASTIC);
                part.setPropertyBool("Anchored", true);
                part.setPropertyInstance("Parent", Rbxl::getWorkspace());
                part.setPropertyColor3("Color", Color3(colorR / 255.0f, colorG / 255.0f, colorB / 255.0f));
            } else {
                Lua::print("No part created. Shape type: ");
                Lua::print(shapeType);
            }

        }

    }


    return 0;
}