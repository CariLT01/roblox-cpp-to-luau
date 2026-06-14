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
