@echo off
cd pipeline

set VALIDATE=
set MODE=
set INLINE=

:: Parse args
:parse_args
if "%~1"=="" goto after_parse

if /I "%~1"=="--validate" (
    set VALIDATE=--validate
)

if /I "%~1"=="--inline" (
    set INLINE=-finline-functions
)

if /I "%~1"=="client" (
    set MODE=client
)

if /I "%~1"=="server" (
    set MODE=server
)

shift
goto parse_args

:after_parse

if "%INLINE%"=="" set INLINE=-fno-inline

echo Compiling C++ code

"C:\riscv-gcc\bin\riscv-none-elf-g++.exe" ^
    -ffreestanding ^
    -O3 ^
    %INLINE% ^
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

py pipeline/transpiler_new.py %VALIDATE%

echo Minifying code for production

py pipeline/minify.py --dist ./dist

echo Cleaning up

:: Keep output.asm for debugging
:: del output.asm

cd pipeline
del output.elf
cd ..

echo Moving files for prod

if /I "%MODE%"=="client" goto CLEANUP_CLIENT
goto CLEANUP_SERVER

:CLEANUP_SERVER
py pipeline/cleanup_move.py --makedirs 1
exit /b 0

:CLEANUP_CLIENT
py pipeline/cleanup_move.py --runpath dist/src/client/run --makedirs 1
exit /b 0