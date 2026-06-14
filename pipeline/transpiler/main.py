"""Orchestrator: parse_asm_to_modules, file I/O, and main entry point."""

import os

from .constants import OUT_DIR
from .metadata import (
    parse_enums, parse_rodata_bytes, parse_rodata_labels,
    find_main_address, parse_function_labels,
    build_rodata_lua_entries, build_rodata_init_lines,
)
from .asm_parser import parse_instructions, collect_branch_targets
from .generator import generate_handler_bodies
from .blocks import merge_into_blocks, generate_handler_strings, split_into_chunks
from .builders import build_shared_luau, build_run_luau
from .obfuscator import apply_mangling


def parse_asm_to_modules(asm_text):
    """Parse RISC-V assembly and generate split ModuleScript outputs.

    Returns a dict:
      {
        'shared': str,           -- content for shared.luau
        'chunks': [str, ...],    -- content for chunk_1.luau, chunk_2.luau, ...
        'run': str,              -- content for run.luau
      }
    """
    # --- Metadata parsing ---
    enums_sparse_lines = parse_enums()
    rodata_bytes, rodata_addr_table = parse_rodata_bytes(asm_text)
    rodata_table = parse_rodata_labels(asm_text)
    main_address_str, main_address_int = find_main_address(asm_text)
    func_map = parse_function_labels(asm_text)
    rodat_lua_entries = build_rodata_lua_entries(rodata_addr_table)
    rodata_init_lines = build_rodata_init_lines(rodata_bytes)

    # --- Assembly parsing ---
    parsed_instructions = parse_instructions(asm_text)
    branch_targets = collect_branch_targets(parsed_instructions)

    # --- Instruction → Lua generation ---
    all_inst_bodies = generate_handler_bodies(
        parsed_instructions, rodata_addr_table, rodata_table, func_map
    )

    # --- Block merging and chunking ---
    blocks = merge_into_blocks(all_inst_bodies, branch_targets)
    all_handler_strings = generate_handler_strings(blocks)
    chunks = split_into_chunks(all_handler_strings)

    # --- Build output modules ---
    shared_content = build_shared_luau(
        enums_sparse_lines, rodat_lua_entries, rodata_init_lines, main_address_str
    )
    run_content = build_run_luau(main_address_int, main_address_str, len(chunks))

    # --- Auto-mangle ---
    shared_content, chunks, run_content = apply_mangling(
        shared_content, chunks, run_content
    )

    # --- Write output files ---
    _write_output(shared_content, chunks, run_content)

    return {'shared': shared_content, 'chunks': chunks, 'run': run_content}


def _write_output(shared_content, chunks, run_content):
    """Write shared.luau, chunk_N.luau files, and run.luau to OUT_DIR."""
    os.makedirs(OUT_DIR, exist_ok=True)

    # Write shared.luau
    shared_path = os.path.join(OUT_DIR, "shared.luau")
    with open(shared_path, "w", encoding="utf-8") as f:
        f.write("--!native\n")
        f.write(shared_content)

    # Write chunk_N.luau files
    for n, chunk_content in enumerate(chunks, 1):
        chunk_path = os.path.join(OUT_DIR, f"chunk_{n}.luau")
        with open(chunk_path, "w", encoding="utf-8") as f:
            f.write("--!native\n")
            f.write(chunk_content)

    # Write run.luau
    run_path = os.path.join(OUT_DIR, "run.luau")
    with open(run_path, "w", encoding="utf-8") as f:
        f.write("--!native\n")
        f.write(run_content)


def main():
    """CLI entry point: read input.asm, transpile, write output."""
    input_file = "output.asm"
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found. Run compile.bat first to generate it.")
        return

    with open(input_file, "r", encoding="utf-8") as f:
        input_asm = f.read()

    modules = parse_asm_to_modules(input_asm)

    chunk_count = len(modules['chunks'])
    shared_size = len(modules['shared'])
    run_size = len(modules['run'])
    total_size = shared_size + run_size + sum(len(c) for c in modules['chunks'])

    print(f"Transpilation complete.")
    print(f"  {chunk_count} chunk(s)")
    print(f"  shared.luau: {shared_size:,} chars")
    print(f"  run.luau: {run_size:,} chars")
    print(f"  total: {total_size:,} chars")
    print(f"  Output: {OUT_DIR}/")
