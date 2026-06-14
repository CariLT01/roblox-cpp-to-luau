// main.cpp
#include "lib/math.hpp"
#include "lib/base64.hpp"
#include "lib/heap.hpp"
#include "lib/rbxl.hpp"
#include "lib/thread.hpp"
#include "imgData.hpp"

// 'volatile' prevents the compiler from optimizing the loop away at -O3
void delay(volatile int count) {
    while (count > 0) {
        count--;
    }
}

void printFunc(int threadId) {
    for (int i = 0; i < 10; i++) {
        Rbxl::print("Thread");
        Rbxl::print(threadId);
        Rbxl::print(i);
        Rbxl::taskWait(1.0f);
    }
}

void touchedCallback(Instance touchedInst) {
    Rbxl::print("Touched");
}

int main() {



        
    Rbxl::print("The start of the program");
    Rbxl::print("Version 2");

    Instance workspace = Rbxl::getWorkspace();
    Instance baseplate = workspace.findFirstChild("Baseplate");

    Instance touchedEvent = baseplate.getMethod("Touched");
    touchedEvent.callMethod("Connect", (void*)touchedCallback, RBXL_METHOD_ARG_1_IS_FUNCTION_BIT);
    

    //Rbxl::taskSpawn(&printFunc);
    Rbxl::taskSpawn((void*)printFunc, 1);
    Rbxl::taskWait(1.0f);
    Rbxl::taskSpawn((void*)printFunc, 2);

    Rbxl::taskWait(2);
    Rbxl::print("Finished wait! Doing work!");
    Rbxl::taskWait(1);

    vector<uint8_t> decoded;
    base64_decode(imageData, decoded);

    // Print decoded image data as a string (or we could print the length)
    Rbxl::print("Decoded bytes:");
    Rbxl::print((int)decoded.size());
    Rbxl::print("Declaring variables #1");

    int bytesRead = 0;
    Rbxl::print("Declaring variables #2");

    int cursor = 0;

    Rbxl::print("Decoding first varint");

    int imgWidth = decodeVarint(decoded, cursor, &bytesRead);
    Rbxl::print("Increment");
    bytesRead = 0;
    Rbxl::print("Decoding second varint");
    int imgHeight = decodeVarint(decoded, cursor, &bytesRead);
    Rbxl::print("Increment");
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

    


    Rbxl::print("Enter loop");

    while (cursor < decoded.size()) {
        Rbxl::print("header size");
        uint8_t headerSize = decoded[cursor];
        cursor++;

        Rbxl::print("Decode varints");
        int layerIndex = decodeVarint(decoded, cursor, &bytesRead);
        bytesRead = 0;
        int layerDataSize = decodeVarint(decoded, cursor, &bytesRead);
        bytesRead = 0;

        Rbxl::print("Target end cursor calc");
        int targetEndCursor = cursor + layerDataSize;
        Rbxl::print("Enter loop 2");
        Rbxl::print("Cursor, targetEndCursor");
        Rbxl::print(cursor);
        Rbxl::print(targetEndCursor);
        Rbxl::taskWait(0.0f);


        while (cursor < targetEndCursor) {

            //Rbxl::print("Execute task.wait");
            //Rbxl::taskWait(0.0f);

            // Rbxl::print("Decode varints");
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

            // Rbxl::print("Calculate colors");

            int colorR = decoded[cursor];
            int colorG = decoded[cursor + 1];
            int colorB = decoded[cursor + 2];
            int shapeType = decoded[cursor + 3];

            cursor += 4;

            // Rbxl::print("Process shape types");
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
            // Rbxl::print("Define vars");
            const float scale = 10.0f;
            float xP = scale * (1 - (centerX / imgWidth));
            float yP = scale * (1 - (centerY / imgHeight));
            float wP = scale * (width3D / imgWidth);
            float hP = scale * (height3D / imgHeight);
            float zP = -layerIndex * 2;
            
            float rad = math::rad(rotation);
            Part part;
            bool partCreated = false;
            // Rbxl::print("Create part");
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

            // Rbxl::print("Part created enter if");
            if (partCreated) {
                part.setPropertyEnum("Material", Rbxl::Enum::MATERIAL_SMOOTHPLASTIC);
                part.setPropertyBool("Anchored", true);
                part.setPropertyInstance("Parent", Rbxl::getWorkspace());
                part.setPropertyColor3("Color", Color3(colorR / 255.0f, colorG / 255.0f, colorB / 255.0f));
            } else {
                Rbxl::print("No part created. Shape type: ");
                Rbxl::print(shapeType);
            }

        }

    }


    /*volatile int counter = 0;
    
    // Create a Part using the class
    Part myPart = Part::create();
    Rbxl::print("Created Part");
    
    // Set string property (Name)
    myPart.setName("MyPart");
    Rbxl::print("Set Name to MyPart");
    
    // Set bool property (Anchored)
    myPart.setAnchored(true);
    Rbxl::print("Set Anchored to true");
    
    // Set float property (Transparency)
    myPart.setTransparency(0.5f);
    float transp = myPart.getTransparency();
    Rbxl::print("Got Transparency:");
    Rbxl::print(transp);
    
    // Set Vector3 property (Position)
    myPart.setPosition(10.0f, 5.0f, 0.0f);
    Vector3 pos = myPart.getPosition();
    Rbxl::print("Got Position:");
    Rbxl::print(pos.x);
    Rbxl::print(pos.y);
    Rbxl::print(pos.z);
    
    // Set Color3 property (Color)
    myPart.setColor(1.0f, 0.0f, 0.0f);
    Color3 col = myPart.getColor();
    Rbxl::print("Got Color (should be red):");
    Rbxl::print(col.r);
    Rbxl::print(col.g);
    Rbxl::print(col.b);
    
    // Find a child
    Instance child = myPart.findFirstChild("Handle");
    Rbxl::print("FindFirstChild Handle:");
    (void)child;
    
    // Wait for a child
    //Instance waited = myPart.waitForChild("SomeChild");
    Rbxl::print("WaitForChild SomeChild:");
    //(void)waited;
    
    // Clone the part
    Part cloned = myPart.clone();
    Rbxl::print("Cloned part:");
    
    // Destroy the clone
    cloned.destroy();
    Rbxl::print("Destroyed clone");

    // --- Buffer Test ---
    void* buf = Rbxl::createBuffer(16);
    Rbxl::print("Created buffer (16 bytes)");

    unsigned int len = Rbxl::bufferLen(buf);
    Rbxl::print("Buffer length:");
    Rbxl::print((int)len);

    // Write and read i32
    Rbxl::bufferWriteI32(buf, 0, 42);
    int val32 = Rbxl::bufferReadI32(buf, 0);
    Rbxl::print("Buffer readI32 at offset 0:");
    Rbxl::print(val32);

    // Write and read i8
    Rbxl::bufferWriteI8(buf, 4, 127);
    int val8 = Rbxl::bufferReadI8(buf, 4);
    Rbxl::print("Buffer readI8 at offset 4:");
    Rbxl::print(val8);

    // Write and read f32
    Rbxl::bufferWriteF32(buf, 8, 3.14f);
    float valF32 = Rbxl::bufferReadF32(buf, 8);
    Rbxl::print("Buffer readF32 at offset 8:");
    Rbxl::print(valF32);

    // Free the buffer
    Rbxl::freeBuffer(buf);
    Rbxl::print("Freed buffer");

    // --- Virtual Heap Test ---
    unsigned int used0 = Rbxl::heapUsed();
    Rbxl::print("Heap used initially:");
    Rbxl::print((int)used0);

    void* hp = Rbxl::malloc(64);
    Rbxl::print("malloc(64) returned:");
    (void)hp;

    unsigned int used1 = Rbxl::heapUsed();
    Rbxl::print("Heap used after alloc:");
    Rbxl::print((int)used1);

    Rbxl::free(hp);
    Rbxl::print("Freed the heap pointer");

    unsigned int used2 = Rbxl::heapUsed();
    Rbxl::print("Heap used after free:");
    Rbxl::print((int)used2);

    // --- Workspace Test ---
    Instance workspace = Instance::getWorkspace();
    Rbxl::print("Got workspace handle");
    Instance foundInWorkspace = workspace.findFirstChild("Baseplate");
    Rbxl::print("FindFirstChild Baseplate from workspace:");
    (void)foundInWorkspace;

    // --- CFrame Test ---
    CFrame cf1(0.0f, 0.0f, 0.0f);
    CFrame cf2 = cframe_lookAt(Vector3(0.0f, 0.0f, 0.0f), Vector3(10.0f, 0.0f, 0.0f));
    Rbxl::print("CFrame lookAt from origin to (10,0,0):");
    Rbxl::print(cf2.x());
    Rbxl::print(cf2.y());
    Rbxl::print(cf2.z());

    CFrame cfCombined = cframe_mul(cf1, cf2);
    Rbxl::print("CFrame multiply result pos:");
    Rbxl::print(cfCombined.x());
    Rbxl::print(cfCombined.y());
    Rbxl::print(cfCombined.z());

    CFrame cfInv = cframe_inverse(cf2);
    Rbxl::print("CFrame inverse pos:");
    Rbxl::print(cfInv.x());
    Rbxl::print(cfInv.y());
    Rbxl::print(cfInv.z());

    Vector3 wp = cframe_pointToWorld(cf2, Vector3(1.0f, 0.0f, 0.0f));
    Rbxl::print("pointToWorldSpace (1,0,0):");
    Rbxl::print(wp.x);
    Rbxl::print(wp.y);
    Rbxl::print(wp.z);

    // Set CFrame on a part to test property get/set
    myPart.setCFrame(cf2);
    Rbxl::print("Set CFrame on part");
    CFrame gotCFrame = myPart.getCFrame();
    Rbxl::print("Got CFrame from part, position:");
    Rbxl::print(gotCFrame.x());
    Rbxl::print(gotCFrame.y());
    Rbxl::print(gotCFrame.z());

    // --- vector<int> Test ---
    vector<int> vi;
    vi.push_back(10);
    vi.push_back(20);
    vi.push_back(30);
    vi.push_back(40);
    Rbxl::print("vector<int> size:");
    Rbxl::print((int)vi.size());
    Rbxl::print("vector<int> elements:");
    for (unsigned int i = 0; i < vi.size(); i++) {
        Rbxl::print(vi[i]);
    }

    // --- vector<Part> Test ---
    vector<Part> parts;
    Part p1 = Part::create();
    p1.setName("Part1");
    parts.push_back(p1);

    Part p2 = Part::create();
    p2.setName("Part2");
    parts.push_back(p2);

    Part p3 = Part::create();
    p3.setName("Part3");
    parts.push_back(p3);

    Rbxl::print("vector<Part> size:");
    Rbxl::print((int)parts.size());
    Rbxl::print("First part's name set successfully");

    // Cleanup parts in vector
    for (unsigned int i = 0; i < parts.size(); i++) {
        parts[i].destroy();
    }
    Rbxl::print("Destroyed all parts in vector");

    for (int i = 0; i < 3; i++) {
        counter++;
        Rbxl::print("Print things");
        delay(10);
    }*/

    return 0;
}