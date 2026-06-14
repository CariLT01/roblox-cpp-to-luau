OUTPUT_ARCH( "riscv" )
ENTRY(_start)

MEMORY
{
  /* Define your emulator's 512 MB RAM block.
     0x80000000 is the start address, 512M is the length. */
  RAM (xrw) : ORIGIN = 0x80000000, LENGTH = 512M
}

SECTIONS
{
  /* 1. Executable Code */
  .text : {
    *(.text.init)    /* Assembly startup code goes here first */
    *(.text .text.*)  /* All your compiled C++ functions */
  } > RAM

  /* 2. Read-Only Data (String literals, constants) */
  .rodata : {
    *(.rodata .rodata.*)
  } > RAM

  /* 3. Initialized Global Variables */
  .data : {
    *(.data .data.*)
  } > RAM

  /* 4. Uninitialized Global Variables (Cleared to 0 at boot) */
  .bss : {
    _bss_start = .;
    *(.bss .bss.*)
    *(COMMON)
    _bss_end = .;
  } > RAM

  /* 5. Define the Stack Pointer Symbol.
     Calculates to the very end of your 512 MB space:
     0x80000000 + 512 MB = 0xA0000000 */
  _stack_top = ORIGIN(RAM) + LENGTH(RAM);
}