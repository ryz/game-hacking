"""u2town.py MAP [--quiet]: a town/castle/surface map (MAPX32, mapg93 ...) as characters with its people
(MONX/MONG file of the same number) overlaid, and the people list.

Map: '.' grass 08, '~' water 00, 'T' woods 0C, ',' marsh 04, '^' mountains 10, ' ' floor 78, '#' wall 70,
'=' counter 7C, 'M' merchant tile 68 (a shop: stand at the counter, Transact toward it), '+' 60 door?,
lower-case letters other tiles >= 0x80 (signs, decorations). People: G guard (picture 60), J jester (64),
m merchant (68), K king (6C), X Minax (40), F fighter (F0), C cleric (F4), W wizard (F8), t thief (FC),
digits 1-5 = the talk entries (type 0x81-0x85, the TLK file's lines in order).
Object arrays (DS-relative in RAM, 32 entries each): x 0x137, y 0x157, hit points 0x177, picture 0x197,
tile under 0x1B7, type 0x1D7 (0 still, 1-3 movement, 0x81+ talking person).
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import u2map

PIC = {0x60: "G", 0x64: "J", 0x68: "m", 0x6C: "K", 0x40: "X", 0xF0: "F", 0xF4: "C", 0xF8: "W", 0xFC: "t"}
TCH = {0x08: ".", 0x00: "~", 0x0C: "T", 0x04: ",", 0x10: "^", 0x78: " ", 0x70: "#", 0x7C: "=", 0x68: "M"}


def objects(F, name):
    mon = F.get(name.replace("MAP", "MON"))
    if not mon:
        return []
    out = []
    for i in range(32):
        x, y, hp, pic, under, typ = (mon[i + 32 * k] for k in range(6))
        if pic:
            out.append((i, x, y, hp, pic, under, typ))
    return out


def main():
    name = sys.argv[1].upper()
    F = u2map.zfiles()
    m = F[name]
    grid = [[TCH.get(m[y * 64 + x], chr(ord("a") + (m[y * 64 + x] >> 2) % 26) if m[y * 64 + x] >= 0x80 else "?")
             for x in range(64)] for y in range(64)]
    obs = objects(F, name)
    for i, x, y, hp, pic, under, typ in obs:
        grid[y][x] = str(typ - 0x80) if typ >= 0x81 else PIC.get(pic, "o")
    if "--quiet" not in sys.argv:
        print("    " + "".join("%x" % (x >> 4) for x in range(64)))
        print("    " + "".join("%x" % (x & 15) for x in range(64)))
        for y in range(64):
            print("%02X  %s" % (y, "".join(grid[y])))
    for i, x, y, hp, pic, under, typ in obs:
        print("obj %2d at (%02X,%02X) hp %3d picture %02X %s type %02X" % (i, x, y, hp, pic, PIC.get(pic, "?"), typ))


if __name__ == "__main__":
    main()
