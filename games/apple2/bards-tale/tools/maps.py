"""Draw the loaded dungeon level of The Bard's Tale (Apple II) as text: walls from 2F800 (22x22 bytes, index
y*22+x, y = north coordinate at 0000, x = east coordinate at 0001; per byte bits 7-6 west, 5-4 east, 3-2 south,
1-0 north: 0 open, 1 wall, 2 door, 3 = secret door (unverified)), flags from 2FA00 (same index:
01 stairs up, 02 stairs down, 04 special event, 08 darkness, 10 trap, 20 portal down, 40 portal up, 80 forced fight - see playbook), name at 2FC16.
Usage: python3 games/apple2/bards-tale/tools/maps.py ROUTE      (e.g. @cellar_parker)   North is up."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", "tools"))
import emu as E
game = E.Game("apple2/bards-tale")
emu, rest, _ = E.start(game, sys.argv[1])
E.play(emu, game, E.expand(game, rest) if rest else [])
w = emu.peek(0x2F800, 484); f = emu.peek(0x2FA00, 484)
name = bytes(b & 0x7F for b in emu.peek(0x2FC16, 10)).decode("ascii", "replace").rstrip(" \\")
py, px = emu.peek(0, 2)
print("%s  level byte 2FC10=%d  party at x=%d y=%d" % (name, emu.peek(0x2FC10, 1)[0], px, py))
FL = {0x01: "U", 0x02: "D", 0x04: "!", 0x08: "k", 0x10: "T", 0x20: "v", 0x40: "^", 0x80: "F"}
H = {0: "   ", 1: "---", 2: "-D-", 3: "-S-"}
V = {0: " ", 1: "|", 2: "D", 3: "S"}
for y in range(21, -1, -1):
    top = "+"; mid = ""
    for x in range(22):
        b = w[y * 22 + x]
        top += H[b & 3] + "+"
        c = "".join(v for k, v in FL.items() if f[y * 22 + x] & k)[:2]
        if (x, y) == (px, py): c = "@"
        mid += V[(b >> 6) & 3] + c.center(3)[:3]
    mid += V[(w[y * 22 + 21] >> 4) & 3]
    print("   " + top); print("%2d %s" % (y, mid))
print("   " + "+" + "+".join(H[(w[x] >> 2) & 3] for x in range(22)) + "+")
print("    " + "".join("%-4d" % x for x in range(22)))
