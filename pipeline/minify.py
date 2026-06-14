"""
minify.py — Luau minifier for RISC-V VM output
Strips comments, minifies whitespace, converts hex literals to decimal.
Usage: python minify.py [input.luau] [output.luau]
       python minify.py --dist dir_path
Defaults: translated.luau -> translated.min.luau
"""
import sys
import os
import glob


def strip_comments_stable(source):
    """
    Remove comments: -- to end of line, and --[[ long comments ]].
    Skips string contents.
    """
    result = []
    i = 0
    while i < len(source):
        c = source[i]
        if c in ('"', "'"):
            # String: pass through unchanged
            quote = c
            j = i + 1
            while j < len(source):
                if source[j] == '\\':
                    j += 2
                    continue
                if source[j] == quote:
                    j += 1
                    break
                j += 1
            result.append(source[i:j])
            i = j
        elif c == '[' and i + 1 < len(source) and source[i+1] == '[':
            # Long string [[ ... ]]: pass through
            j = i + 2
            while j + 1 < len(source):
                if source[j] == ']' and source[j+1] == ']':
                    j += 2
                    break
                j += 1
            result.append(source[i:j])
            i = j
        elif c == '-' and i + 1 < len(source) and source[i+1] == '-':
            # Comment
            if i + 3 < len(source) and source[i+2] == '[' and source[i+3] == '[':
                # Long comment --[[ ... ]]
                j = i + 4
                while j + 1 < len(source):
                    if source[j] == ']' and source[j+1] == ']':
                        j += 2
                        break
                    j += 1
                # Keep the newline after the long comment if there is one
                if j < len(source) and source[j] == '\n':
                    result.append('\n')
                    j += 1
                i = j
            else:
                # Single-line comment: remove to end of line
                j = source.find('\n', i)
                if j != -1:
                    result.append('\n')
                    i = j + 1
                else:
                    i = len(source)
        elif c == '\n':
            result.append('\n')
            i += 1
        else:
            result.append(c)
            i += 1
    return ''.join(result)



def minify_whitespace(source):
    """
    Remove leading whitespace per line, collapse multiple spaces to one.
    Skips string contents.
    """
    lines = source.split('\n')
    out_lines = []
    for line in lines:
        if not line.strip():
            continue  # skip blank lines
        parts = []
        in_str = False
        string_char = None
        in_long_str = False
        skip_next = False
        last_was_space = False
        first_char = True
        i = 0
        while i < len(line):
            c = line[i]
            if skip_next:
                parts.append(c)
                skip_next = False
                last_was_space = False
                i += 1
                continue
            if not in_str and not in_long_str:
                if c in ('"', "'"):
                    in_str = True
                    string_char = c
                    parts.append(c)
                    last_was_space = False
                elif c == '[' and i+1 < len(line) and line[i+1] == '[':
                    in_long_str = True
                    parts.append('[[')
                    i += 2
                    last_was_space = False
                    continue
                elif c.isspace():
                    if not first_char and not last_was_space:
                        parts.append(' ')
                        last_was_space = True
                else:
                    parts.append(c)
                    last_was_space = False
                    first_char = False
            elif in_str:
                if c == '\\':
                    parts.append(c)
                    skip_next = True
                elif c == string_char:
                    in_str = False
                    parts.append(c)
                else:
                    parts.append(c)
                last_was_space = False
            else:  # in_long_str
                parts.append(c)
                if c == ']' and i+1 < len(line) and line[i+1] == ']':
                    parts.append(']')  # second bracket (first was appended above)
                    i += 1
                    in_long_str = False
                last_was_space = False
            # Note: [=[ / ]=] style long brackets are not supported (unused in this codebase)
            i += 1
        out_lines.append(''.join(parts))
    return '\n'.join(out_lines)


def convert_hex_to_dec(source):
    """
    Convert hexadecimal literals (0x...) to decimal numbers.
    Only converts when the decimal is NOT longer than the hex form.
    Skips string contents and long strings.
    """
    result = []
    i = 0
    while i < len(source):
        c = source[i]
        if c in ('"', "'"):
            quote = c
            j = i + 1
            while j < len(source):
                if source[j] == '\\':
                    j += 2
                    continue
                if source[j] == quote:
                    j += 1
                    break
                j += 1
            result.append(source[i:j])
            i = j
        elif c == '[' and i + 1 < len(source) and source[i+1] == '[':
            j = i + 2
            while j + 1 < len(source):
                if source[j] == ']' and source[j+1] == ']':
                    j += 2
                    break
                j += 1
            result.append(source[i:j])
            i = j
        elif (c == '0' and i + 2 < len(source) and source[i+1] in ('x', 'X')
              and (i == 0 or not (source[i-1].isalnum() or source[i-1] == '_'))):
            # Hex literal — read the digits
            j = i + 2
            while j < len(source) and source[j] in '0123456789abcdefABCDEF':
                j += 1
            hex_str = source[i:j]
            try:
                dec_val = int(hex_str, 16)
                dec_str = str(dec_val)
                # Only replace if decimal is not longer
                if len(dec_str) <= len(hex_str):
                    result.append(dec_str)
                else:
                    result.append(hex_str)
            except ValueError:
                result.append(hex_str)
            i = j
        else:
            result.append(c)
            i += 1
    return ''.join(result)


def minify_luau(source):
    # Step 0: Strip comments
    source = strip_comments_stable(source)

    # Step 1: Minify whitespace
    source = minify_whitespace(source)

    # Step 2: Convert hex literals to decimal (where shorter or same length)
    source = convert_hex_to_dec(source)

    return source


def minify_file(input_path, output_path, quiet=False):
    """Minify a single .luau file and write the result."""
    with open(input_path, 'r', encoding='utf-8') as f:
        source = f.read()

    result = minify_luau(source)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("--!native\n")
        f.write(result)

    orig_size = len(source)
    mini_size = len(result)
    pct = 100 * mini_size // orig_size if orig_size else 0
    if not quiet:
        fname = os.path.basename(input_path)
        print(f"  {fname}: {orig_size:,} -> {mini_size:,} chars ({pct}%)")
    return orig_size, mini_size


def minify_directory(dir_path):
    """Minify all .luau files in a directory (skipping already-minified *.min.luau)."""
    luau_files = sorted(glob.glob(os.path.join(dir_path, "*.luau")))
    # Filter out already-minified files
    luau_files = [f for f in luau_files if not f.endswith(".min.luau")]

    if not luau_files:
        print(f"No .luau files found in {dir_path}. Resolves to: {os.path.abspath(dir_path)}")
        return

    print(f"Minifying {len(luau_files)} file(s) in {dir_path}/ ...")
    total_orig = 0
    total_mini = 0
    for fpath in luau_files:
        base = os.path.splitext(fpath)[0]
        out_path = base + ".min.luau"
        orig, mini = minify_file(fpath, out_path)
        total_orig += orig
        total_mini += mini

    if total_orig:
        pct = 100 * total_mini // total_orig
        print(f"\nTotal: {total_orig:,} -> {total_mini:,} chars ({pct}%)")


def main():
    if len(sys.argv) > 1 and sys.argv[1] == '--dist':
        dir_path = sys.argv[2] if len(sys.argv) > 2 else 'dist'
        minify_directory(dir_path)
        return

    input_file = sys.argv[1] if len(sys.argv) > 1 else 'translated.luau'
    output_file = sys.argv[2] if len(sys.argv) > 2 else 'translated.min.luau'

    orig, mini = minify_file(input_file, output_file, quiet=True)
    input_name = os.path.basename(input_file)
    output_name = os.path.basename(output_file)
    pct = 100 * mini // orig if orig else 0
    print(f"Minified: {input_name} -> {output_name}")
    print(f"  {orig:,} -> {mini:,} chars ({pct}%)")


if __name__ == '__main__':
    main()
