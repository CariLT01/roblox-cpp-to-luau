// main.cpp
#include "lib/crt.hpp"
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

    LuaObj task = (LuaObj) Rbxl::getGlobal("task");

    LuaObj f1f = LuaObj::fromFloat(1.0f);

    for (int i = 0; i < 10; i++) {
        Lua::print("Thread");
        Lua::print(threadId);
        Lua::print(i);
        task.callMethodStatic("wait", RBXL_METHOD_ARG_1_IS_OBJECT_BIT, f1f);
    }
}

__attribute__((noinline))
void touchedCallback(LuaObj touchedInst) {
    Lua::print("Touched");
}

int main() {



    LuaObj task = (LuaObj) Rbxl::getGlobal("task");
        
    Lua::print("The start of the program");
    Lua::print("Version 5");

    Lua::taskSpawn((void*)printFunc, 1);
    Lua::taskSpawn((void*)printFunc, 2);


    LuaObj rs = (LuaObj) Rbxl::getService("ReplicatedStorage");
    LuaObj sharedStr = LuaObj::fromString("Shared");
    LuaObj helloStr = LuaObj::fromString("Hello");
    LuaObj shared = (LuaObj) rs.callMethod("FindFirstChild", RBXL_METHOD_ARG_1_IS_OBJECT_BIT | RBXL_METHOD_HAS_RETURN_BIT | RBXL_METHOD_RETURN_IS_OBJ_BIT, sharedStr);
    LuaObj moduleScript = (LuaObj) shared.callMethod("FindFirstChild", RBXL_METHOD_ARG_1_IS_OBJECT_BIT | RBXL_METHOD_HAS_RETURN_BIT | RBXL_METHOD_RETURN_IS_OBJ_BIT, helloStr);
    LuaObj module = (LuaObj)((LuaObj) Rbxl::getGlobal("require")).call(moduleScript, RBXL_METHOD_ARG_1_IS_OBJECT_BIT | RBXL_METHOD_HAS_RETURN_BIT | RBXL_METHOD_RETURN_IS_OBJ_BIT);
    module.callMethodStatic("Hello", 0);
    Lua::print("Module already called!");




    LuaObj workspace = (LuaObj) Rbxl::getService("Workspace");
    LuaObj baseplateStr = LuaObj::fromString("Baseplate");
    LuaObj baseplate = (LuaObj) workspace.callMethod("FindFirstChild", RBXL_METHOD_ARG_1_IS_OBJECT_BIT | RBXL_METHOD_HAS_RETURN_BIT | RBXL_METHOD_RETURN_IS_OBJ_BIT, baseplateStr);

    
    LuaObj prop = baseplate.getPropertyObject("Position");
    Vector3 pos = Vector3{};
    pos.readFromObject(prop.handle());

    

    Lua::print("Position:");
    Lua::print(pos.x);
    Lua::print(pos.y);
    Lua::print(pos.z);

    pos.x += 5;

    LuaObj objectLua = LuaObj(pos.toObject());
    baseplate.setPropertyObject("Position", objectLua);

    LuaObj touchedEvent = baseplate.getMethod("Touched");
    LuaObj callbackHandle = LuaObj::fromFunction((void*)touchedCallback);
    touchedEvent.callMethod("Connect", RBXL_METHOD_ARG_1_IS_OBJECT_BIT, callbackHandle);



    //Rbxl::taskSpawn(&printFunc);
    //Lua::taskSpawn((void*)printFunc, 1);
    
    LuaObj o1f = LuaObj::fromFloat(1.0f);
    LuaObj o2f = LuaObj::fromFloat(2.0f);
    LuaObj o0f = LuaObj::fromFloat(0.0f);

    task.callMethodStatic("wait", RBXL_METHOD_ARG_1_IS_OBJECT_BIT, o1f);
    //Lua::taskSpawn((void*)printFunc, 2);

    task.callMethodStatic("wait", RBXL_METHOD_ARG_1_IS_OBJECT_BIT, o2f);
    Lua::print("Finished wait! Doing work!");
    
    task.callMethodStatic("wait", RBXL_METHOD_ARG_1_IS_OBJECT_BIT, o1f);

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
        task.callMethodStatic("wait", RBXL_METHOD_ARG_1_IS_OBJECT_BIT, o0f);

        LuaObj instance = (LuaObj)Rbxl::getGlobal("Instance");
        LuaObj partStr = LuaObj::fromString("Part");
        LuaObj wedgePartStr = LuaObj::fromString("WedgePart");


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
            float zP = -layerIndex * 0.01;
            
            Lua::print(rotation);

            float rad = math::rad(rotation);
            bool partCreated = false;
            // Lua::print("Create part");
            LuaObj part;
            if (shapeType == 0) {
                part = (LuaObj) instance.callMethodStatic("new", RBXL_METHOD_ARG_1_IS_OBJECT_BIT | RBXL_METHOD_HAS_RETURN_BIT | RBXL_METHOD_RETURN_IS_OBJ_BIT, partStr);
                Vector3 sizeV3 = Vector3{wP, hP, 0.001};
                LuaObj sizeObj = (LuaObj)sizeV3.toObject();
                part.setPropertyObject("Size", sizeObj);
                CFrame cfRot = cframe_fromEulerAngles(0, 0, rad);
                CFrame cfPos = CFrame(xP, yP, zP);
                CFrame cf = cframe_mul(cfPos, cfRot);
                LuaObj cfObj = (LuaObj)cf.toObject();
                part.setPropertyObject("CFrame", cfObj);
                partCreated = true;
                
            } else if (shapeType == 1) {
                part = (LuaObj) instance.callMethodStatic("new", RBXL_METHOD_ARG_1_IS_OBJECT_BIT | RBXL_METHOD_HAS_RETURN_BIT | RBXL_METHOD_RETURN_IS_OBJ_BIT, partStr);



                part.setPropertyObject("Shape", LuaObj::fromEnum((int)Rbxl::Enum::PARTTYPE_CYLINDER));
                
                Vector3 sizeVec = Vector3{0.0001, wP, hP};
                LuaObj sizeVecObj = (LuaObj)sizeVec.toObject();

                part.setPropertyObject("Size", sizeVecObj);
                CFrame cfPos = CFrame(xP, yP, zP);
                CFrame cfRot1 = cframe_fromEulerAngles(0, math::rad(90), math::rad(180));
                CFrame cfRot2 = cframe_fromEulerAngles(rad, 0, 0);
                CFrame cf = cframe_mul(cfPos, cframe_mul(cfRot1, cfRot2));

                LuaObj cfObj = (LuaObj)cf.toObject();
                part.setPropertyObject("CFrame", cfObj);
                partCreated = true;
            } else if (shapeType == 2) {
                part = (LuaObj) instance.callMethodStatic("new", RBXL_METHOD_ARG_1_IS_OBJECT_BIT | RBXL_METHOD_HAS_RETURN_BIT | RBXL_METHOD_RETURN_IS_OBJ_BIT, wedgePartStr);

                Vector3 sizeVec = Vector3{0.001, wP, hP};
                LuaObj sizeObj = (LuaObj)sizeVec.toObject();

                part.setPropertyObject("Size", sizeObj);

                CFrame cfPos = CFrame(xP, yP, zP);
                CFrame cfRot1 = cframe_fromEulerAngles(0, math::rad(90), math::rad(180));
                CFrame cfRot2 = cframe_fromEulerAngles(rad, 0, 0);
                CFrame cf = cframe_mul(cfPos, cframe_mul(cfRot1, cfRot2));
                LuaObj cfObj = (LuaObj)cf.toObject();
                part.setPropertyObject("CFrame", cfObj);
                partCreated = true;

            }

            // Lua::print("Part created enter if");
            if (partCreated) {
                part.setPropertyObject("Material", LuaObj::fromEnum((int)Rbxl::Enum::MATERIAL_SMOOTHPLASTIC));
                
                LuaObj trueObj = LuaObj::fromBool(true);
                Color3 c = Color3(colorR / 255.0f, colorG / 255.0f, colorB / 255.0f);
                LuaObj colorObj = (LuaObj)c.toObject();
                
                part.setPropertyObject("Anchored", trueObj);
                part.setPropertyObject("Parent", workspace);
                part.setPropertyObject("Color", colorObj);
            } else {
                Lua::print("No part created. Shape type: ");
                Lua::print(shapeType);
            }

        }

    }


    return 0;
}