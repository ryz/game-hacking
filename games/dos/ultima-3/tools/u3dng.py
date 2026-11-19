"""u3dng.py FILE.ULT [KIND ...]: special squares of an Ultima III (DOS) dungeon file, with an approach for DNG.

  python3 games/dos/ultima-3/tools/u3dng.py FIRE.ULT fountain rod

A dungeon file is 8 levels of 16x16 bytes (y*16 + x, the map wraps), then 144 bytes of level messages. Square
values: 00 open, 80 wall, A0 door, C0 secret door, 10 ladder up, 20 ladder down, 30 both, 40 chest; low nibble
specials 01 Time Lord, 02 fountain, 03 strange wind, 04 trap, 05 rod, 06 gremlins, 08 misty writing.
Prints: level (00-07), square, kind, and an approach `DNG:LL:XX:YY:F` (an open neighbour, facing the square)
so that `ENTER:...,TORCH,DNG:...,up` steps onto it.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from u3town import load
KIND = {1: "timelord", 2: "fountain", 3: "wind", 4: "trap", 5: "rod", 6: "gremlins", 8: "writing"}

def kind(v):
    if v & 0x80: return {0x80: "wall", 0xA0: "door", 0xC0: "secret"}.get(v & 0xE0, "wall")
    if v & 0x0F: return KIND.get(v & 0x0F, "special%02X" % v)
    if v & 0x40: return "chest"
    if v & 0x30: return {0x10: "up", 0x20: "down", 0x30: "updown"}[v & 0x30]
    return "open"

def squares(d):
    for lv in range(8):
        for y in range(16):
            for x in range(16):
                yield lv, x, y, d[lv * 256 + y * 16 + x]

def approach(d, lv, x, y):
    for dx, dy, f in ((0, 1, 0), (-1, 0, 1), (0, -1, 2), (1, 0, 3)):   # stand south facing N, west facing E ...
        ax, ay = (x + dx) % 16, (y + dy) % 16
        if d[lv * 256 + ay * 16 + ax] == 0: return "DNG:%02X:%02X:%02X:%02X" % (lv, ax, ay, f)
    return None

if __name__ == "__main__":
    d = load(sys.argv[1]); want = set(sys.argv[2:])
    for lv, x, y, v in squares(d):
        k = kind(v)
        if k in ("open", "wall") or (want and k not in want): continue
        print("L%d (%X,%X) %-9s %02X %s" % (lv + 1, x, y, k, v, approach(d, lv, x, y)))
