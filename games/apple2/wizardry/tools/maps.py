"""maps.py: the ten maze floors of Wizardry I (Apple II), decoded from the scenario disk inside the game ZIP.

  python3 games/apple2/wizardry/tools/maps.py                    ASCII maps + special squares of all floors
  python3 games/apple2/wizardry/tools/maps.py 4                   one floor
  python3 games/apple2/wizardry/tools/maps.py --out games/apple2/wizardry/design/maps/floors.txt

Format (the DOS port's, games/dos/wizardry/tools/maps.py; the ten floors decoded here are byte for byte what
this tool prints for DOS, see the playbook): floor N is a 1024-byte page (two Pascal blocks) at offset
0x13600 + (N-1) * 0x400 of the scenario disk read in block order (`blocks()`: a .dsk is in DOS 3.3 sector
order). The page is the Pascal TMAZE:
  W, S, E, N walls: 4 x 120 bytes, [x][y] 2 bits each (8 per word, 3 words per x): 0 open, 1 wall, 2 door,
  3 hidden door; FIGHTS 80 bytes [x][y] 1 bit (16 per word, 2 words per x): fight zone ("room");
  SQREXTRA 200 bytes [x][y] 4 bits (4 per word, 5 words per x): index 0-15 into the square types;
  SQRETYPE 8 bytes, 16 x 4 bits; AUX0, AUX1, AUX2: 3 x 16 words (stairs/teleport: floor, y, x; floor 0 =
  the castle); then the encounter table.
x runs east, y north, (0,0) is the south-west corner. Where the floor in play sits in memory: playbook, RAM map.
Map legend: `|` and `--` walls, `D`/`DD` doors, `?`/`??` hidden doors, `.` fight zone, hex digit = special
square index (listed below each map).
"""
import io, os, sys, zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", "..", ".."))
BASE = 0x13600
TYPES = ["NORMAL", "STAIRS", "PIT", "CHUTE", "SPINNER", "DARK", "TELEPORT", "OUCH", "ELEVATOR", "ROCK",
         "FIZZLE (anti-magic)", "MESSAGE", "FIXED FIGHT"]


def blocks(d):
    """A DOS-order sector image (.dsk) as the 280 Pascal blocks of 512 bytes the game addresses."""
    m = [(0, 14), (13, 12), (11, 10), (9, 8), (7, 6), (5, 4), (3, 2), (1, 15)]
    out = bytearray()
    for b in range(280):
        t = b // 8
        for s in m[b % 8]: out += d[(t * 16 + s) * 256:(t * 16 + s) * 256 + 256]
    return bytes(out)


def disk(path=None):
    """The scenario disk in block order: from the game ZIP, or from PATH (a .dsk, or a .sav ZIP that holds one)."""
    path = path or os.path.join(ROOT, "rom", "wizardry.zip")
    if zipfile.is_zipfile(path):
        z = zipfile.ZipFile(path)
        name = sorted(n for n in z.namelist() if "SCENARIO" in n.upper() or "WIZARDRY I" in n.upper())[0]
        return blocks(z.read(name))
    return blocks(open(path, "rb").read())


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
            else:
                what = "aux %d %d %d" % (a0, a1, a2)
            cells = sq[i] if len(sq[i]) <= 6 else sq[i][:6] + ["... %d squares" % len(sq[i])]
            rows.append("  %X %-19s %-24s %s" % (i, name, what, " ".join(map(str, cells))))
        return "\n".join(rows)


def main():
    a = sys.argv[1:]
    out = None
    if "--out" in a:
        i = a.index("--out"); out = a[i + 1]; del a[i:i + 2]
    floors = [int(x) for x in a] or list(range(1, 11))
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
