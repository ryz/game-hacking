"""u2merch.py ROUTE OBJ X,Y : tokens that move object OBJ (after ROUTE) to (X,Y): object x/y, map picture, old square restored."""
import sys, os; HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", "..", "..", "..")); sys.path.insert(0, os.path.join(ROOT, "tools"))
os.chdir(ROOT)
import emu as E
g = E.Game("dos/ultima-2"); m, rest, _ = E.start(g, sys.argv[1])
for t in rest: E.step(m, g, t)
i = int(sys.argv[2]); x, y = [int(v, 16) for v in sys.argv[3].split(",")]
o = bytes(m.peek(0x8FC7, 192)); ox, oy, pic, under = o[i], o[32 + i], o[96 + i], o[128 + i]
m.close()
toks = []
if (ox, oy) != (x, y):
    toks.append("poke:%04X=%02X" % (0xA690 + oy * 64 + ox, under))
    toks.append("poke:%04X=%02X" % (0x8FC7 + i, x)); toks.append("poke:%04X=%02X" % (0x8FE7 + i, y))
    toks.append("poke:%04X=%02X" % (0xA690 + y * 64 + x, pic))
print(",".join(toks))
