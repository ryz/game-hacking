"""u2shops.py: every shop counter in the villages and towns of Ultima II (DOS), from the map files.

A shop is a merchant tile (68) behind a counter tile (7C or >= 80, e.g. a sign letter); Transact (T) toward
the counter from the square in front of it opens the shop. Which shop depends only on the quadrant of the
town map (ULTIMAII.EXE 0x1590): town (map 2): x<32,y<32 weapons, x>=32,y<32 armour, x>=32,y>=32 transport
(horses), x<32,y>=32 pub; village (map 1): x<32,y<32 oracle ("time and travel"), x>=32,y<32 food,
x>=32,y>=32 cleric spells, x<32,y>=32 wizard spells. Prints: map, shop, merchant square, stand square,
direction key for T.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import u2map

SHOP = {2: {(0, 0): "weapons", (1, 0): "armour", (1, 1): "transport", (0, 1): "pub"},
        1: {(0, 0): "oracle", (1, 0): "food", (1, 1): "cleric", (0, 1): "wizard"}}
WALK = {0x08, 0x0C, 0x04, 0x70}


def main():
    F = u2map.zfiles()
    for name in sorted(F):
        if not name.startswith(("MAPX", "MAPG")) or name[-1] not in "12":
            continue
        m = F[name]
        kind = int(name[-1])
        for i in range(4096):
            if m[i] != 0x68:
                continue
            x, y = i % 64, i // 64
            for dx, dy, key in ((1, 0, "left"), (-1, 0, "right"), (0, 1, "up"), (0, -1, "down")):
                cx, cy, sx, sy = x + dx, y + dy, x + 2 * dx, y + 2 * dy
                if not (0 <= sx < 64 and 0 <= sy < 64):
                    continue
                c, s = m[cy * 64 + cx], m[sy * 64 + sx]
                if (c == 0x7C or c >= 0x80) and s in WALK:
                    print("%s %-9s merchant (%02X,%02X) stand (%02X,%02X) T,%s" % (
                        name, SHOP[kind][(int(x >= 32), int(y >= 32))], x, y, sx, sy, key))


if __name__ == "__main__":
    main()
