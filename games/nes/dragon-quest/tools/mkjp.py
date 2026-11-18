#!/usr/bin/env python3
"""Rebuild rom/patches/dragon-quest/jp.ips (the `rom:jp` variant): the byte difference that turns the
translated ROM (rom/dragon-quest.nes) back into the Japanese dump (rom/src/dragon-quest-j.nes).
Run from the repo root:  python3 games/nes/dragon-quest/tools/mkjp.py     (neither ROM nor the patch is committed)"""
a = open('rom/dragon-quest.nes', 'rb').read()
b = open('rom/src/dragon-quest-j.nes', 'rb').read()
assert len(a) == len(b)
out, i = bytearray(b'PATCH'), 0
while i < len(a):
    if a[i] != b[i]:
        j = i
        while j < len(a) and j - i < 0xFFFF and a[j] != b[j]:
            j += 1
        out += i.to_bytes(3, 'big') + (j - i).to_bytes(2, 'big') + b[i:j]
        i = j
    else:
        i += 1
open('rom/patches/dragon-quest/jp.ips', 'wb').write(out + b'EOF')
