"""Identifier obfuscation: scanning, mapping, and source mangling."""

import random
import string

from .constants import LUA_RESERVED


def scan_identifiers(text):
    """Walk Lua source and collect all non-reserved identifiers.
    Skips string contents, comments, and long-string literals."""
    found = set()
    i = 0
    while i < len(text):
        c = text[i]
        if c in ('"', "'"):
            quote = c
            j = i + 1
            while j < len(text):
                if text[j] == '\\':
                    j += 2
                    continue
                if text[j] == quote:
                    j += 1
                    break
                j += 1
            i = j
        elif c == '[' and i + 1 < len(text) and text[i + 1] == '[':
            j = i + 2
            while j + 1 < len(text):
                if text[j] == ']' and text[j + 1] == ']':
                    j += 2
                    break
                j += 1
            i = j
        elif c == '-' and i + 1 < len(text) and text[i + 1] == '-':
            j = text.find('\n', i)
            if j != -1:
                i = j + 1
            else:
                i = len(text)
        elif c.isdigit():
            # Skip numeric literals (decimal, hex 0x..., etc.) to prevent
            # hex suffix like xFFFFFFFF in 0xFFFFFFFF from being treated as an identifier.
            j = i + 1
            if c == '0' and j < len(text) and text[j] in ('x', 'X'):
                j += 1
                while j < len(text) and text[j].isalnum():
                    j += 1
            else:
                while j < len(text) and text[j].isalnum():
                    j += 1
            i = j
        elif c == '.':
            # Skip property accesses after dots (e.g. Enum.b.C, S.reg) --
            # these are not identifiers that should be renamed.
            i += 1
            if i < len(text) and (text[i].isalpha() or text[i] == '_'):
                j = i + 1
                while j < len(text) and (text[j].isalnum() or text[j] == '_'):
                    j += 1
                i = j
        elif c == ':':
            # Skip method names after colons (obj:method(), function obj:method()) --
            # these are not identifiers that should be renamed.
            i += 1
            if i < len(text) and (text[i].isalpha() or text[i] == '_'):
                j = i + 1
                while j < len(text) and (text[j].isalnum() or text[j] == '_'):
                    j += 1
                i = j
        elif c.isalpha() or c == '_':
            j = i + 1
            while j < len(text) and (text[j].isalnum() or text[j] == '_'):
                j += 1
            name = text[i:j]
            if name not in LUA_RESERVED and not name[0].isdigit():
                found.add(name)
            i = j
        else:
            i += 1
    return found


def build_obf_map(identifiers):
    """Generate random short-name mapping for a set of identifiers."""
    rng = random.Random()  # non-deterministic seed each run
    sorted_ids = sorted(identifiers, key=len, reverse=True)
    names = []
    used = set()
    # Pre-compute available single-char names (a-zA-Z minus LUA_RESERVED)
    single_char_pool = [c for c in string.ascii_letters if c not in LUA_RESERVED]
    chars = string.ascii_letters + string.digits
    for _ in sorted_ids:
        if len(names) < len(single_char_pool):
            length = 1
        elif len(names) < len(single_char_pool) + 62 * 62:
            length = 2
        else:
            length = 3
        attempts = 0
        while True:
            name = ''.join(rng.choices(chars, k=length))
            if name[0].isdigit():
                continue
            if name not in used and name not in LUA_RESERVED:
                names.append(name)
                used.add(name)
                break
            attempts += 1
            if attempts > 1000:
                length += 1
                attempts = 0
    return dict(zip(sorted_ids, names))


def obfuscate_source(text, name_map):
    """Replace identifiers in name_map with their obfuscated versions.
    Skips string contents (single/double quoted and long strings) and comments."""
    result = []
    i = 0
    while i < len(text):
        c = text[i]
        if c in ('"', "'"):
            quote = c
            j = i + 1
            while j < len(text):
                if text[j] == '\\':
                    j += 2
                    continue
                if text[j] == quote:
                    j += 1
                    break
                j += 1
            result.append(text[i:j])
            i = j
        elif c == '[' and i + 1 < len(text) and text[i + 1] == '[':
            j = i + 2
            while j + 1 < len(text):
                if text[j] == ']' and text[j + 1] == ']':
                    j += 2
                    break
                j += 1
            result.append(text[i:j])
            i = j
        elif c == '-' and i + 1 < len(text) and text[i + 1] == '-':
            j = text.find('\n', i)
            if j != -1:
                result.append(text[i:j + 1])
                i = j + 1
            else:
                result.append(text[i:])
                i = len(text)
        elif c.isdigit():
            # Skip numeric literals (decimal, hex 0x..., etc.) to prevent
            # hex suffix like xFFFFFFFF in 0xFFFFFFFF from being replaced.
            j = i + 1
            if c == '0' and j < len(text) and text[j] in ('x', 'X'):
                j += 1
                while j < len(text) and text[j].isalnum():
                    j += 1
            else:
                while j < len(text) and text[j].isalnum():
                    j += 1
            result.append(text[i:j])
            i = j
        elif c == '.':
            # Don't replace identifiers after dots (property accesses like Enum.b.C).
            result.append('.')
            i += 1
            if i < len(text) and (text[i].isalpha() or text[i] == '_'):
                j = i + 1
                while j < len(text) and (text[j].isalnum() or text[j] == '_'):
                    j += 1
                result.append(text[i:j])  # keep property name as-is
                i = j
        elif c == ':':
            # Don't replace identifiers after colons (method calls like obj:method()).
            result.append(':')
            i += 1
            if i < len(text) and (text[i].isalpha() or text[i] == '_'):
                j = i + 1
                while j < len(text) and (text[j].isalnum() or text[j] == '_'):
                    j += 1
                result.append(text[i:j])  # keep method name as-is
                i = j
        elif c.isalpha() or c == '_':
            j = i + 1
            while j < len(text) and (text[j].isalnum() or text[j] == '_'):
                j += 1
            name = text[i:j]
            if name in name_map:
                result.append(name_map[name])
            else:
                result.append(name)
            i = j
        else:
            result.append(c)
            i += 1
    return ''.join(result)


def apply_mangling(shared_content, chunks, run_content):
    """Collect all identifiers from raw generated code, build obfuscation map,
    and apply it to shared, chunks, and run content.
    Returns (shared_content, chunks, run_content)."""
    all_ids = set()
    all_ids.update(scan_identifiers(shared_content))
    for chunk in chunks:
        all_ids.update(scan_identifiers(chunk))
    all_ids.update(scan_identifiers(run_content))

    obf_map = build_obf_map(all_ids)

    shared_content = obfuscate_source(shared_content, obf_map)
    chunks = [obfuscate_source(c, obf_map) for c in chunks]
    run_content = obfuscate_source(run_content, obf_map)

    return shared_content, chunks, run_content
