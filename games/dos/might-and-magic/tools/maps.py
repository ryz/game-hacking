"""maps.py ZIP [INDEX|NAME ...] : text maps from MAZEDATA.DTA + event squares from the area's .OVR (read from the owner's ZIP).
Wall byte N<<6|E<<4|S<<2|W (0 open, 1 wall, 2 door, 3 special); row 15 (north) printed first; * = event square."""
import sys, zipfile
z = zipfile.ZipFile(sys.argv[1])
def rd(n):
    for i in z.namelist():
        if i.upper().endswith("/" + n.upper()): return z.read(i)
maze = rd("MAZEDATA.DTA")
NAMES = "SORPIGAL PORTSMIT ALGARY DUSK ERLIQUIN CAVE1 CAVE2 CAVE3 CAVE4 CAVE5 CAVE6 CAVE7 CAVE8 CAVE9 AREAA1 AREAA2 AREAA3 AREAA4 AREAB1 AREAB2 AREAB3 AREAB4 AREAC1 AREAC2 AREAC3 AREAC4 AREAD1 AREAD2 AREAD3 AREAD4 AREAE1 AREAE2 AREAE3 AREAE4 DOOM BLACKRN BLACKRS QVL1 QVL2 RWL1 RWL2 ENF1 ENF2 WHITEW DRAGAD UDRAG1 UDRAG2 UDRAG3 DEMON ALAMAR PP1 PP2 PP3 PP4 ASTRAL".split()
def events(name):
    """OVR = 12-byte header (word 2 code address, word 4 code length, word 6 data address, word 8 data length), 8086 code, data.
    The code starts with the event lookup: cmp al,[bx+OFFSETS] ... cmp bl,[COUNT] ... and al,[bx+MASKS]; the three
    addresses are read from those instructions (Sorpigal: count 25 at data+50, offsets data+51, masks data+75: the
    last offset doubles as the first mask)."""
    d = rd(name + ".OVR")
    if not d: return {}
    data = 12 + (d[4] | d[5] << 8); dbase = d[6] | d[7] << 8
    code = d[12:data]
    i = code.find(b"\x3a\x87"); j = code.find(b"\x3a\x1e", i); k = code.find(b"\x22\x87", j)
    if min(i, j, k) < 0 or k > 130: return {}
    f = lambda o: data + (code[o + 2] | code[o + 3] << 8) - dbase
    offs, cnt, masks = f(i), f(j), f(k)
    n = d[cnt]
    return {d[offs + q]: d[masks + q] for q in range(min(n, masks - offs))}, data
def show(idx):
    w = maze[idx * 512: idx * 512 + 256]; p = maze[idx * 512 + 256: idx * 512 + 512]
    ev = events(NAMES[idx]); ev, base = ev if ev else ({}, None)
    print("== %d %s (event table at OVR offset %s, %d events)" % (idx, NAMES[idx], base, len(ev)))
    ch = {0: " ", 1: "#", 2: "D", 3: "+"}
    for y in range(15, -1, -1):
        top = ""; mid = ""
        for x in range(16):
            b = w[y * 16 + x]
            n, e, s, wv = b >> 6, (b >> 4) & 3, (b >> 2) & 3, b & 3
            c = "*" if (y * 16 + x) in ev else ("." if p[y * 16 + x] & 0x80 else " ")
            top += "+" + {0: "  ", 1: "--", 2: "DD", 3: "=="}[n]
            mid += {0: " ", 1: "|", 2: "D", 3: "!"}[wv] + c + " "
        e = w[y * 16 + 15] >> 4 & 3
        print("   " + top + "+"); print("%2d %s%s" % (y, mid, {0: " ", 1: "|", 2: "D", 3: "!"}[e]))
    print("   " + "".join("+" + {0: "  ", 1: "--", 2: "DD", 3: "=="}[(w[x] >> 2) & 3] for x in range(16)) + "+")
    print("    " + "".join("%-3d" % x for x in range(16)))
    for o, m in sorted(ev.items()):
        print("  event (%d,%d) facing mask %02X %s" % (o & 15, o >> 4, m, "".join(k for k, v in (("N", 0xC0), ("E", 0x30), ("S", 0x0C), ("W", 0x03)) if m & v)))
if __name__ == "__main__":
  for a in sys.argv[2:] or ["0"]:
    show(int(a) if a.isdigit() else NAMES.index(a.upper()))
