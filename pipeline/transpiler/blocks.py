"""Basic block merging, handler string generation, and chunk splitting."""

import re

from .constants import CHUNK_SIZE

# ── Regexes for parsing block exit (last return statement) ──
# Handles both decimal (return 2147483700) and hex (return 0x7FFD874)
_RETURN_DIRECT_RE = re.compile(
    r'\s*return\s+((?:0x[0-9a-fA-F]+)|\d+)\s*$'
)
_RETURN_NIL_RE = re.compile(r'\s*return\s+nil\s*$')
_RETURN_INDIRECT_RE = re.compile(r'\s*return\s+_next_pc\s*$')


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

                if next_is_target or b + 1 == len(all_inst_bodies):
                    # Last instruction of block (end of file or before branch target):
                    # keep the return statement so the VM dispatch loop continues.
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


# ── Tail merging: inline single-predecessor blocks to skip dispatch cycles ──

def tail_merge_blocks(blocks, address_taken):
    """Merge blocks that unconditionally jump to a single-predecessor target.

    TEMPORARILY DISABLED for debugging premature VM exit with --inline.
    """
    return blocks


def _tail_merge_pass(blocks, address_taken):
    """One pass of tail merging.  Returns (changed, new_blocks)."""
    # Parse exit info for all blocks
    exit_info = {}
    for block in blocks:
        exit_info[block['start_addr']] = _parse_block_exit(block['lines'])

    # Build predecessor map (which blocks statically jump to which)
    preds = {b['start_addr']: set() for b in blocks}
    for block in blocks:
        src = block['start_addr']
        for tgt in exit_info.get(src, {}).get('targets', []):
            if tgt in preds:
                preds[tgt].add(src)

    addr_to_block = {b['start_addr']: b for b in blocks}
    merged = set()

    for block in blocks:
        addr = block['start_addr']
        if addr in merged:
            continue

        info = exit_info.get(addr)
        if not info or info['type'] != 'direct':
            continue

        target = info['targets'][0]

        # ── Safety checks ──
        if target == addr:                         # self-loop
            continue
        if target not in addr_to_block:            # target block not found
            continue
        if target in merged:                       # already merged this pass
            continue
        if target in address_taken:                # reachable via jalr
            continue
        if len(preds.get(target, set())) != 1:     # multiple static predecessors
            continue
        if addr not in preds.get(target, set()):   # not actually a predecessor
            continue

        # Safe to merge: inline target's code into this block
        target_block = addr_to_block[target]
        _merge_block_into(block, target_block)
        merged.add(target)

        # Update exit_info for the modified block (its return line changed)
        exit_info[addr] = _parse_block_exit(block['lines'])

    if not merged:
        return False, list(blocks)

    # Filter out merged blocks
    new_blocks = [b for b in blocks if b['start_addr'] not in merged]
    return True, new_blocks


def _parse_block_exit(lines):
    """Parse the exit (last return statement) of a block.

    Returns {'type': 'direct'|'conditional'|'indirect'|'halt'|'unknown',
             'targets': [int]}
    """
    if not lines:
        return {'type': 'unknown', 'targets': []}

    last_line = lines[-1]

    # Direct unconditional jump: return <number>  or  return 0xHEX
    m = _RETURN_DIRECT_RE.match(last_line)
    if m:
        return {'type': 'direct', 'targets': [int(m.group(1), 0)]}

    # Halt: return nil
    if _RETURN_NIL_RE.match(last_line):
        return {'type': 'halt', 'targets': []}

    # Indirect jump: return _next_pc
    if _RETURN_INDIRECT_RE.match(last_line):
        return {'type': 'indirect', 'targets': []}

    # Conditional branch: multi-line if/then/else/end
    if last_line.strip() == 'end' and len(lines) >= 4:
        targets = []
        found_if = False
        for i in range(len(lines) - 2, -1, -1):
            line = lines[i]
            m = _RETURN_DIRECT_RE.match(line)
            if m:
                targets.append(int(m.group(1), 0))
            if line.strip().startswith('if '):
                found_if = True
                break
        if found_if:
            return {'type': 'conditional', 'targets': targets}

    return {'type': 'unknown', 'targets': []}


def _merge_block_into(source_block, target_block):
    """Inline target_block's code into source_block, replacing source's return."""
    source_lines = source_block['lines']
    target_lines = target_block['lines']

    # Strip the terminating return from source (last line for direct jumps)
    source_body = _strip_return(source_lines)

    # Append all of target's lines (including its own return)
    source_body.extend(target_lines)

    source_block['lines'] = source_body


def _strip_return(lines):
    """Remove the terminating return statement(s) from a block's lines.

    For simple unconditional jumps: removes the last line (return <number>).
    For conditional branches: removes the entire if/else/end block.
    """
    if not lines:
        return list(lines)

    last_line = lines[-1].strip()

    if last_line == 'end':
        # Conditional branch: find matching 'if' and remove that entire block
        depth = 1
        for i in range(len(lines) - 2, -1, -1):
            stripped = lines[i].strip()
            if stripped == 'end':
                depth += 1
            elif stripped.startswith('if '):
                depth -= 1
                if depth == 0:
                    return lines[:i]
        # Fallback: couldn't find matching if
        return lines[:-1]
    else:
        # Simple return: remove last line
        return lines[:-1]
