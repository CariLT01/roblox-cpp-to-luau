"""Assembly parsing: instruction extraction, branch targets, entry point."""

import re


def parse_instructions(asm_text):
    """Parse all RISC-V instructions from assembly text.
    Returns list of (address, mnemonic, args_list)."""
    inst_pattern = re.compile(
        r"^\s*([0-9a-fA-F]+):\s+[0-9a-fA-F]+\s+(\S+)(?:\s+(.*))?$"
    )
    lines = asm_text.splitlines()
    parsed_instructions = []
    for line in lines:
        match = inst_pattern.match(line)
        if match:
            address = "0x" + match.group(1)
            mnemonic = match.group(2)
            args_str = match.group(3) or ""
            args = [arg.strip() for arg in args_str.split(',') if arg.strip()]
            parsed_instructions.append((address, mnemonic, args))
    return parsed_instructions


def collect_branch_targets(parsed_instructions):
    """Collect set of branch/jump target addresses for basic block merging."""
    branch_targets = set()
    for address, mnemonic, args in parsed_instructions:
        addr_int = int(address, 16)
        if mnemonic in ["beq", "bne", "blt", "bge", "bltu", "bgeu", "jal"]:
            target_str = args[-1].split()[0]
            if not target_str.startswith("0x"):
                target_str = "0x" + target_str
            target_addr = int(target_str, 16)
            branch_targets.add(target_addr)
    # First instruction is always a block start
    if parsed_instructions:
        branch_targets.add(int(parsed_instructions[0][0], 16))
    return branch_targets


def collect_address_taken(parsed_instructions):
    """Collect addresses that are stored in registers (potential jalr targets).

    When a `jal`, `jalr`, `lui`, `auipc`, or `li` pseudo-instruction writes an
    address into a register, that address could later be used by `jalr` as a
    jump target.  Blocks at those addresses must NOT be deleted by tail merging.
    """
    address_taken = set()
    for address, mnemonic, args in parsed_instructions:
        addr_int = int(address, 16)
        if mnemonic in ["jal", "jalr"]:
            # Return address (addr+4) stored in rd — must keep this block alive.
            # Skip if rd is x0/zero (unconditional jump without link).
            if len(args) >= 1 and args[0] not in ("x0", "zero"):
                address_taken.add((addr_int + 4) & 0xFFFFFFFF)
            # Also protect the jump TARGET — other code paths (e.g. jalr)
            # may reference this address, so the block must not be deleted.
            if mnemonic == "jal" and len(args) >= 2:
                target_str = args[1].split()[0]
                if not target_str.startswith("0x"):
                    target_str = "0x" + target_str
                try:
                    address_taken.add(int(target_str, 16) & 0xFFFFFFFF)
                except ValueError:
                    pass
        elif mnemonic == "lui":
            # rd = imm * 4096 (upper immediate load)
            try:
                imm_str = args[1].split("#")[0].strip()
                imm = int(imm_str, 0)
                address_taken.add((imm * 4096) & 0xFFFFFFFF)
            except (ValueError, IndexError):
                pass
        elif mnemonic == "auipc":
            # rd = addr + imm * 4096 (PC-relative upper immediate)
            try:
                imm_str = args[1].split("#")[0].strip()
                imm = int(imm_str, 0)
                address_taken.add((addr_int + imm * 4096) & 0xFFFFFFFF)
            except (ValueError, IndexError):
                pass
        elif mnemonic == "addi" and len(args) >= 2 and args[1] in ("x0", "zero"):
            # li pseudo-instruction: rd = imm
            imm_str = args[-1].split("#")[0].strip()
            try:
                imm = int(imm_str, 0)
                address_taken.add(imm & 0xFFFFFFFF)
            except ValueError:
                pass
        # Branch targets — blocks that are the target of any branch or jump
        # must not be deleted, since they may also be reached via jalr or other
        # dynamic paths not captured by the static predecessor map.
        if mnemonic in ("beq", "bne", "blt", "bge", "bltu", "bgeu"):
            target_str = args[-1].split()[0]
            if not target_str.startswith("0x"):
                target_str = "0x" + target_str
            try:
                address_taken.add(int(target_str, 16) & 0xFFFFFFFF)
            except ValueError:
                pass
    return address_taken
