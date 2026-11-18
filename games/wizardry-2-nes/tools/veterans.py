"""Build the VETERANS macro (game.json): pokes that turn the level 1 playtest party (roster slots 6-11, both
copies $6400 and $7800 + slot*$60) into a level 11-13 party with gold, E.P., hit points, ages and spells.
Values are chosen to look like a real save (realistic-values rule). Records keep their old check value, so the
pokes hold for the running session; the game rewrites the check value when it saves (Leave Game).

  python3 games/wizardry-2-nes/tools/veterans.py [--write]   print the macro / write it into game.json
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))

def bcd(n, size=6):
    s = "%0*d" % (size * 2, n)
    return s

def le(n):
    return "%02X%02X" % (n & 0xFF, n >> 8)

# slot, gold, ep, hp now, hp max, level, age, mage SP (now/max nibbles x7), cleric SP, mage known x7, cleric known x7
PARTY = [
    (6, 3412, 401236, 110, 112, 12, 19, "00" * 7, "00" * 7, "00" * 7, "00" * 7),           # RYZ fighter
    (7, 1877, 287915, 124, 124, 12, 31, "00" * 7, "00" * 7, "00" * 7, "00" * 7),           # CONDI fighter
    (8, 2209, 301447, 71, 71, 12, 24, "00" * 7, "77665544332200", "00" * 7, "1F0F0F0F3F0F00"),  # EBO priest
    (9, 4136, 253804, 53, 53, 12, 27, "00" * 7, "00" * 7, "00" * 7, "00" * 7),             # CUBI thief
    (10, 1592, 482916, 41, 41, 13, 48, "88776655443322", "00" * 7, "0F0303070F0F07", "00" * 7),  # DEDDO mage
    (11, 973, 167422, 46, 46, 11, 63, "55443322000000", "44332200000000", "0F030303000000", "1F0F0700000000"),  # MNZ bishop
]

# items: (id, equipped) up to 8, AC with that equipment (the game recomputes AC only on Equip)
ITEMS = {
    6: ([(0x1D, 1), (0x18, 1), (0x19, 1), (0x22, 1), (0x2F, 1), (0x0F, 0)], 0xFD),   # RYZ (AC -3, as the game computes it in the maze)
    7: ([(0x12, 1), (0x17, 1), (0x19, 1), (0x0E, 1), (0x10, 0)], 1),             # CONDI
    8: ([(0x13, 1), (0x17, 1), (0x08, 1), (0x0E, 1), (0x0F, 0)], 2),             # EBO
    9: ([(0x47, 1), (0x16, 1), (0x07, 1), (0x15, 0)], 5),                        # CUBI
    10: ([(0x05, 1), (0x09, 1), (0x1C, 0), (0x0F, 0)], 9),                       # DEDDO
    11: ([(0x20, 1), (0x09, 1), (0x1B, 0)], 9),                                  # MNZ
}

def items_poke(r, slot):
    lst, ac = ITEMS[slot]
    flags = "".join("80" if e else "00" for _, e in lst).ljust(16, "0")
    ids = "".join("%02X" % i for i, _ in lst).ljust(16, "0")
    return ["poke:%04X=%02X" % (r + 0x26, ac), "poke:%04X=%s%s%02X" % (r + 0x43, flags, ids, len(lst))]

def macro():
    toks = []
    for slot, gold, ep, hp, hpmax, lvl, age, msp, csp, mk, ck in PARTY:
        for base in (0x6400, 0x7800):
            r = base + slot * 0x60
            toks += ["poke:%04X=%s%s" % (r + 0x11, bcd(gold), bcd(ep)),
                     "poke:%04X=%s%s" % (r + 0x1D, le(hp), le(hpmax)),
                     "poke:%04X=%s%02X" % (r + 0x22, le(lvl), age),
                     "poke:%04X=%s%s%s%s" % (r + 0x27, msp, csp, mk, ck)] + items_poke(r, slot)
    return ",".join(toks)

if __name__ == "__main__":
    m = macro()
    if "--write" in sys.argv:
        p = os.path.join(HERE, "..", "game.json")
        g = json.load(open(p))
        g["macros"]["VETERANS"] = m
        json.dump(g, open(p, "w"), indent=2)
        open(p, "a").write("\n")
    print(m)
