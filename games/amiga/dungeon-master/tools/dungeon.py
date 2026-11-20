"""Dungeon Master (Amiga v3.60): read the dungeon from RAM and print floor maps, stairs and creature groups.

  python3 games/amiga/dungeon-master/tools/dungeon.py [ROUTE] [--md]     (default route @saved)

The game keeps the whole dungeon in slow RAM (addresses of the registered A500 boot, the same in every
checkpoint so far; playbook "RAM map"): map descriptors at C779A2 (14 x 16 bytes: square data offset, offset
X/Y, width/height), square bytes at C6E88C (column by column: x * height + y; bits 7-5 type: 0 wall,
1 corridor, 2 pit, 3 stairs (bit 2 = up), 4 door, 5 teleporter, 6 fake wall; bit 4 = things on the square),
cumulative things-per-column at C7764E, first thing of each square at C766D2, creature groups (16 bytes) at
C72AF2, weapons (4 bytes) at C727B6. Map k is level k+1 (map 0 = the Hall of Champions).
Legend: # wall, . corridor, O pit, < stairs up, > stairs down, D door, T teleporter, F fake/hidden wall,
letters a-z on a square = the first creature group there (key printed below the map).
"""
import os, struct, sys
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "tools"))
MAPDATA, DESC, COLCNT, SQFT, GROUPS = 0xC6E88C, 0xC779A2, 0xC7764E, 0xC766D2, 0xC72AF2
CRE = ["Giant Scorpion", "Swamp Slime", "Giggler", "Wizard Eye", "Pain Rat", "Ruster", "Screamer", "Rockpile",
       "Ghost", "Stone Golem", "Mummy", "Black Flame", "Skeleton", "Couatl", "Vexirk", "Magenta Worm", "Trolin",
       "Giant Wasp", "Animated Armour", "Materializer", "Water Elemental", "Oitu", "Demon", "Lord Chaos",
       "Red Dragon", "Lord Order", "Grey Lord"]
CH = {0: "#", 1: ".", 2: "O", 4: "D", 5: "T", 6: "F"}


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    route = args[0] if args else "@saved"
    import emu as E
    g = E.Game("amiga/dungeon-master")
    emu, rest, _ = E.start(g, route)
    E.play(emu, g, rest)
    peek = emu.peek
    word = lambda a: struct.unpack(">H", peek(a, 2))[0]
    maps, col = [], 0
    for k in range(14):
        r = peek(DESC + 16 * k, 16)
        b = struct.unpack(">H", r[8:10])[0]
        m = dict(off=struct.unpack(">H", r[0:2])[0], h=(b >> 11) + 1, w=((b >> 6) & 31) + 1, ox=r[6], oy=r[7], col0=col)
        col += m["w"]
        maps.append(m)
    out = []
    for k, m in enumerate(maps):
        data = peek(MAPDATA + m["off"], m["w"] * m["h"])
        sq = lambda x, y: data[x * m["h"] + y]
        groups, stairs = {}, []
        for x in range(m["w"]):
            idx = word(COLCNT + 2 * (m["col0"] + x))
            for y in range(m["h"]):
                s = sq(x, y)
                if s >> 5 == 3:
                    stairs.append("%s (%d,%d)" % ("up" if s & 4 else "down", x, y))
                if s & 0x10:
                    t = word(SQFT + 2 * idx)
                    idx += 1
                    if (t >> 10) & 15 == 4:
                        r = peek(GROUPS + 16 * (t & 1023), 16)
                        n = ((struct.unpack(">H", r[14:16])[0] >> 5) & 3) + 1
                        groups[(x, y)] = (n, CRE[r[4]] if r[4] < len(CRE) else "?")
        letters = {}
        for i, p in enumerate(sorted(groups)):
            letters[p] = "abcdefghijklmnopqrstuvwxyz"[i % 26]
        out.append("### Level %d (map %d): %d x %d squares, offset (%d,%d)" % (k + 1, k, m["w"], m["h"], m["ox"], m["oy"]))
        out.append("Stairs: " + ", ".join(stairs))
        out.append("```")
        out.append("   " + "".join(str(x // 10) for x in range(m["w"])))
        out.append("   " + "".join(str(x % 10) for x in range(m["w"])))
        for y in range(m["h"]):
            row = ""
            for x in range(m["w"]):
                s = sq(x, y)
                c = CH.get(s >> 5, "?")
                if s >> 5 == 3:
                    c = "<" if s & 4 else ">"
                row += letters.get((x, y), c)
            out.append("%2d %s" % (y, row))
        out.append("```")
        if groups:
            out.append("Creatures (first group on a square, at the moment of the route): " + "; ".join(
                "%s (%d,%d) %d x %s" % (letters[p], p[0], p[1], groups[p][0], groups[p][1]) for p in sorted(groups)))
        out.append("")
    print("\n".join(out))


if __name__ == "__main__":
    main()
