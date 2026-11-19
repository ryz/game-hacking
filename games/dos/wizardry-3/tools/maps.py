"""maps.py: the six maze floors of Wizardry III (DOS), decoded from the game disk WIZ3.DSK inside the game ZIP.

  python3 games/dos/wizardry-3/tools/maps.py                    ASCII maps + special squares of all floors
  python3 games/dos/wizardry-3/tools/maps.py 4                  one floor
  python3 games/dos/wizardry-3/tools/maps.py --out games/dos/wizardry-3/design/maps/floors.txt

Same TMAZE format as Wizardry I and II (verified 2026-11-19: the floor-in-play buffer at 0B6E4 and its copy at 0E524
matched WIZ3.DSK for floors 1 and 6; stairs, the floor 1 forks, guardians, statues and riddles seen in play). WIZ3.DSK
holds SCENARIO.DATA at 0x1DA00 (Pascal directory in block 2); its table of contents (BLOFF) puts the maze at block 12:
floor N is a 1024-byte page at 0x1F200 + (N-1) * 0x400. Disk floors are the game's levels 1-6 (the volcano is climbed:
"stairs up" lead to higher numbers); 2 and 4 are the good half, 3 and 5 the evil half, 6 the summit.
  W, S, E, N walls: 4 x 120 bytes, [x][y] 2 bits each: 0 open, 1 wall, 2 door, 3 hidden door (a wall belongs to the
  square it is stored in: moving checks only the square you leave, so one-way doors exist);
  FIGHTS 80 bytes [x][y] 1 bit: fight zone; SQREXTRA 200 bytes [x][y] 4 bits: index 0-15 into the square types;
  SQRETYPE 8 bytes, 16 x 4 bits; AUX0, AUX1, AUX2: 3 x 16 words (stairs/teleport: floor, y, x; floor 0 = the castle).
MESSAGE squares: AUX1 = message number, AUX2 = kind (verified in play): 1 plain text; 2 take an item (AUX0 + 1000);
4 "Will you search (Y/N)?": AUX0 > 0 fight that group, -1000 > AUX0 > -2000 get item -AUX0, AUX0 = -(20000 + 100*A + B)
swap item 1000+A for item 1000+B; 5 lake edge (back off or drown); 9 trap ("Look out!"); 10 riddle (answer in message
AUX0); 11 pay gold (Abdul: price in message AUX0); 13 statue / L'kbreth; 15 / 16 the guardians of the good and evil
halves (floor 4 (7,17), floor 5 (12,10)); 3 and 14 not decoded. FIXED FIGHT: AUX2 = monster group.
Messages are compressed on the disk; the texts were read in play (playbook "Messages"): `MSG` column below.
Map legend: `|` and `--` walls, `D`/`DD` doors, `?`/`??` hidden doors, `.` fight zone, hex digit = special
square index (listed below each map).
"""
import io, os, sys, zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", "..", ".."))
BASE = 0x1F200
MSG = {0: "beach, dark lake with an island", 2: "water's edge: further and you drown", 4: 'sign "Barracks"',
       5: "great fortress, beware of the moat monsters", 9: "L'kbreth's warning: neither good nor evil alone",
       13: "Farewell. May your way be easy. (L'kbreth)", 14: "I'd turn back if I were you", 15: "another direction?",
       16: 'sign "Wine cellar"', 17: "S.E.G. Po'le, Grand Wizard: the wizard is *out*", 22: "dusty desk, letter 'P'",
       26: "woman with a whip: the password? (ABDUL SENT YOU)", 29: "Abdul: tell them Abdul sent you",
       32: "oily black liquid, pool on the floor", 34: "Look out!", 35: "aged monk: your soul for this chest",
       38: "apparition above a murky pool", 41: "Abdul's ethereal taxi, 2500 GP one way", 44: "Temple of the irascible Fung",
       47: "Abdul's taxi, still only 5000 GP", 50: "Abdul sells a magic crystal, 25000 gold", 60: "Abdul's coffer, he vanishes",
       63: "radiant statue holding a crystal sphere", 67: "a graveyard's dark...", 68: "and this trap's a crock...",
       69: "don't go any further, or...", 70: "You have reached the statue.", 71: "riddle (AIR)", 81: "riddle (FIRE)",
       90: "riddle: what card is he? (DEATH)", 96: "riddle (WHEEL)", 101: "riddle: what card am I? (CHARIOT)",
       107: "the Grand Wizard's dining room"}
TYPES = ["NORMAL", "STAIRS", "PIT", "CHUTE", "SPINNER", "DARK", "TELEPORT", "OUCH", "ELEVATOR", "ROCK",
         "FIZZLE (anti-magic)", "MESSAGE", "FIXED FIGHT"]


def disk():
    z = zipfile.ZipFile(os.path.join(ROOT, "rom", "wizardry-3.zip"))
    name = [n for n in z.namelist() if n.upper().endswith("WIZ3.DSK")][0]
    return z.read(name)


def _bits(d, off, row_words, nbits, x, y):
    per = 16 // nbits
    a = off + x * row_words * 2 + (y // per) * 2
    return ((d[a] | d[a + 1] << 8) >> ((y % per) * nbits)) & ((1 << nbits) - 1)


class Floor:
    def __init__(self, d, n):
        self.n, o = n, BASE + (n - 1) * 0x400
        self.d, self.o = d, o
        self.types = [(d[o + 760 + i // 2] >> (4 * (i % 2))) & 15 for i in range(16)]
        self.aux = [[int.from_bytes(d[o + 768 + 32 * a + 2 * i:o + 770 + 32 * a + 2 * i], "little", signed=True)
                     for i in range(16)] for a in range(3)]

    def wall(self, side, x, y):
        return _bits(self.d, self.o + 120 * "WSEN".index(side), 3, 2, x, y)

    def fight(self, x, y):
        return _bits(self.d, self.o + 480, 2, 1, x, y)

    def extra(self, x, y):
        return _bits(self.d, self.o + 560, 5, 4, x, y)

    def ascii(self):
        h = {0: "  ", 1: "--", 2: "DD", 3: "??"}
        v = " |D?"
        out = []
        for y in range(19, -1, -1):
            out.append("+" + "".join(h[self.wall("N", x, y)] + "+" for x in range(20)))
            row = ""
            for x in range(20):
                e = self.extra(x, y)
                row += v[self.wall("W", x, y)] + ("%X" % e if e else ("." if self.fight(x, y) else " ")) + " "
            out.append(row + v[self.wall("E", 19, y)] + "  y=%d" % y)
        out.append("+" + "".join(h[self.wall("S", x, 0)] + "+" for x in range(20)))
        out.append("   " + "".join("%-3d" % x for x in range(20)) + " x")
        return "\n".join(out)

    def specials(self):
        sq = {}
        for x in range(20):
            for y in range(20):
                if self.extra(x, y):
                    sq.setdefault(self.extra(x, y), []).append((x, y))
        rows = []
        for i in sorted(sq):
            t = self.types[i]
            name = TYPES[t] if t < len(TYPES) else str(t)
            a0, a1, a2 = (self.aux[k][i] for k in range(3))
            if t in (1, 6):
                what = "to floor %d (%d,%d)" % (a0, a2, a1) if a0 else "to the castle"
            elif t == 11:
                what = "aux %d %d %d: %s" % (a0, a1, a2, MSG.get(a1, "?"))
            else:
                what = "aux %d %d %d" % (a0, a1, a2)
            cells = sq[i] if len(sq[i]) <= 6 else sq[i][:6] + ["... %d squares" % len(sq[i])]
            rows.append("  %X %-19s %-24s %s" % (i, name, what, " ".join(map(str, cells))) if t != 11 else "  %X %-19s %s\n      %s" % (i, name, what, " ".join(map(str, cells))))
        return "\n".join(rows)


def main():
    a = sys.argv[1:]
    out = None
    if "--out" in a:
        i = a.index("--out"); out = a[i + 1]; del a[i:i + 2]
    floors = [int(x) for x in a] or list(range(1, 7))
    d = disk()
    text = []
    for n in floors:
        f = Floor(d, n)
        text.append("Floor %d\n%s\nSpecial squares (index type destination squares):\n%s\n" % (n, f.ascii(), f.specials()))
    s = "\n".join(text)
    if out:
        os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
        open(out, "w").write(s)
        print(out)
    else:
        print(s)


if __name__ == "__main__":
    main()
