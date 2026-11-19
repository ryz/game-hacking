"""u2objs.py ROUTE [X,Y]: list live objects (x, y, hp, picture, under, type) after the route + ryz position."""
import sys, os; HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", "..", "..", "..")); sys.path.insert(0, os.path.join(ROOT, "tools"))
os.chdir(ROOT)
import emu as E
g = E.Game("dos/ultima-2"); m, rest, _ = E.start(g, sys.argv[1])
for t in rest: E.step(m, g, t)
o = bytes(m.peek(0x8FC7, 192)); p = bytes(m.peek(0x8E90, 2))
print("ryz (%02X,%02X)" % (p[0], p[1]))
for i in range(32):
    if o[96 + i]: print("obj %2d (%02X,%02X) hp %3d pic %02X under %02X type %02X" % (i, o[i], o[32 + i], o[64 + i], o[96 + i], o[128 + i], o[160 + i]))
if len(sys.argv) > 2:
    x0, y0 = [int(v, 16) for v in sys.argv[2].split(",")]
    mp = bytes(m.peek(0xA690, 4096))
    for y in range(y0 - 3, y0 + 4):
        print("%02X " % y + " ".join("%02X" % mp[(y & 63) * 64 + ((x0 + dx) & 63)] for dx in range(-4, 5)))
m.close()
