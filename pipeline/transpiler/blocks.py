"""Basic block merging, handler string generation, and chunk splitting."""

from .constants import CHUNK_SIZE


def merge_into_blocks(all_inst_bodies, branch_targets):
    """Merge consecutive non-terminating instructions into basic blocks."""
    blocks = []
    b = 0
    while b < len(all_inst_bodies):
        start_addr = all_inst_bodies[b]['addr']
        merged_lines = []

        while b < len(all_inst_bodies):
            inst = all_inst_bodies[b]

            # Check if this instruction starts a new block (is a branch target)
            if len(merged_lines) > 0 and inst['addr'] in branch_targets:
                break

            if inst['is_term']:
                # Terminator: include full body (with return) and end block
                merged_lines.extend(inst['body_lines'])
                b += 1
                break
            else:
                # Check if the next instruction is a branch target or terminator
                next_is_target = (
                    b + 1 < len(all_inst_bodies)
                    and all_inst_bodies[b + 1]['addr'] in branch_targets
                )

                if next_is_target:
                    # This is the last instruction before a branch target: keep return
                    merged_lines.extend(inst['body_lines'])
                    b += 1
                    break
                else:
                    # Middle of block: strip the return statement (last line)
                    merged_lines.extend(inst['body_lines'][:-1])
                    b += 1

        blocks.append({'start_addr': start_addr, 'lines': merged_lines})

    return blocks


def generate_handler_strings(blocks):
    """Generate complete handler function strings from merged blocks."""
    all_handler_strings = []
    for block in blocks:
        handler_lines = [f"    HANDLERS[{block['start_addr']}] = function()"]
        for line in block['lines']:
            handler_lines.append(line)
        handler_lines.append("    end")
        handler_lines.append("")
        all_handler_strings.append("\n".join(handler_lines))
    return all_handler_strings


def split_into_chunks(all_handler_strings):
    """Split handler strings into chunks with module boilerplate."""
    chunks = []
    for c in range(0, len(all_handler_strings), CHUNK_SIZE):
        chunk_lines = []
        chunk_num = len(chunks) + 1
        chunk_lines.append(f"-- Chunk {chunk_num} -- Instruction handlers")
        chunk_lines.append(
            f"-- Populates S.HANDLERS with closures for {CHUNK_SIZE} instructions."
        )
        chunk_lines.append("")
        chunk_lines.append("local S = require(script.Parent.shared)")
        chunk_lines.append("")
        chunk_lines.append(
            "-- Local aliases for frequently-accessed shared state (performance)"
        )
        chunk_lines.append("local reg = S.reg")
        chunk_lines.append("local OBJECTS = S.OBJECTS")
        chunk_lines.append("local BUFFERS = S.BUFFERS")
        chunk_lines.append("local RODATA = S.RODATA")
        chunk_lines.append("local ENUMS = S.ENUMS")
        chunk_lines.append("local ENUM_TO_INDEX = S.ENUM_TO_INDEX")
        chunk_lines.append("local FREE_LIST = S.FREE_LIST")
        chunk_lines.append("local ALLOCS = S.ALLOCS")
        chunk_lines.append("local PAGES = S.PAGES")
        chunk_lines.append("local freg = S.freg")
        chunk_lines.append("local HANDLERS = S.HANDLERS")
        chunk_lines.append("")
        chunk_lines.append("-- Helper aliases")
        chunk_lines.append("local write_mem32 = S.write_mem32")
        chunk_lines.append("local read_mem32 = S.read_mem32")
        chunk_lines.append("local write_mem8 = S.write_mem8")
        chunk_lines.append("local read_mem8 = S.read_mem8")
        chunk_lines.append("local f32_to_bits = S.f32_to_bits")
        chunk_lines.append("local bits_to_f32 = S.bits_to_f32")
        chunk_lines.append("")
        chunk_lines.append("return function()")
        for handler_str in all_handler_strings[c:c + CHUNK_SIZE]:
            chunk_lines.append(handler_str)
        chunk_lines.append("end")
        chunk_lines.append("")
        chunks.append("\n".join(chunk_lines))
    return chunks
