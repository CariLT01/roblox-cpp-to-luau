@echo off

cd pipeline


echo Compiling C++ code

"C:\riscv-gcc\bin\riscv-none-elf-g++.exe" ^
    -ffreestanding ^
    -O3^
    -fno-inline ^
    -fno-threadsafe-statics ^
    -march=rv32imf ^
    -mabi=ilp32 ^
    -fno-exceptions ^
    -fno-rtti ^
    -nostdlib ^
    -T linker.ld ../src/*.cpp ^
    -o output.elf ^
    -lgcc

echo Generating Assembly

"C:\riscv-gcc\bin\riscv-none-elf-objdump.exe" ^
    -d ^
    -s ^
    -M numeric,no-aliases ^
    output.elf > output.asm



cd ..


echo Transpiling code to Lua

move pipeline\output.asm output.asm

py pipeline/transpiler_new.py

echo Minifying code for production

py pipeline/minify.py --dist ./dist

echo Cleaning up

del output.asm

cd pipeline

del output.elf

cd ..

echo Moving files for prod

py pipeline/cleanup_move.py