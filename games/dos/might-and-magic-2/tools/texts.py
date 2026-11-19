"""texts.py [MAP ...]: print the texts of the areas' event data (ROM text, read from memory after a warp).

  python3 games/dos/might-and-magic-2/tools/texts.py            # all 60 areas -> work/scout/might-and-magic-2/texts/
  python3 games/dos/might-and-magic-2/tools/texts.py 0B 11

The area files are compressed on disk (EVENTSI.DAT, EVENTSO.DAT); after a warp the game holds the area's event
table and scripts at physical 16852 (DS:6052) up to the roster at 18620. Strings there end with FF; the
script bytes between them are dropped (runs of 4+ printable characters are kept). One file per area:
texts/MAP.txt, plus the event table (square, event number, facing) at the top.
"""
import os, re, sys
from multiprocessing import Pool
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "tools"))
OUT = os.path.join(ROOT, "work", "scout", "might-and-magic-2", "texts")


def dump(mp):
    import emu as E
    g = E.Game("dos/might-and-magic-2")
    route = "@middlegate" if mp == 0 else "@middlegate,WARP:%02X:08:08" % mp
    m, rest, _ = E.start(g, route)
    for t in rest:
        E.step(m, g, t)
    raw = bytes(m.peek(0x16852, 0x18620 - 0x16852))
    m.close()
    ev = []
    for i in range(0, len(raw) - 2, 3):
        a, b, c = raw[i], raw[i + 1], raw[i + 2]
        if a == b == c == 0:
            break
        ev.append("(%d,%d) ev%02X %s" % (a & 15, a >> 4, b, "".join(d for bit, d in
                  ((0x80, "N"), (0x40, "E"), (0x20, "S"), (0x10, "W")) if c & bit)))
    strs = [s.decode("ascii").replace("@", " ") for s in re.findall(rb"[\x20-\x7e\n]{4,}", raw)]
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "%02X.txt" % mp), "w") as f:
        f.write("area %02X: %d event entries\n%s\n\n" % (mp, len(ev), " ".join(ev)))
        f.write("\n".join(strs) + "\n")
    return mp, len(ev), strs[:3]


if __name__ == "__main__":
    maps = [int(a, 16) for a in sys.argv[1:]] or list(range(60))
    with Pool(4) as p:
        for mp, n, first in p.map(dump, maps, chunksize=1):
            print("%02X %3d %s" % (mp, n, " | ".join(first)[:110]))
