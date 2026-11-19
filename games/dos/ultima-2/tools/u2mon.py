"""u2mon.py ROUTE slot:x:y:pic:hp[:type] ... : pokes that put surface/town monsters (reads the tiles under them after ROUTE)."""
import sys, os; HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", "..", "..", "..")); sys.path.insert(0, os.path.join(ROOT, "tools"))
os.chdir(ROOT)
import emu as E
g = E.Game("dos/ultima-2"); m, rest, _ = E.start(g, sys.argv[1])
for t in rest: E.step(m, g, t)
mp = bytes(m.peek(0xA690, 4096)); m.close()
toks = []
for spec in sys.argv[2:]:
    p = spec.split(":"); s = int(p[0]); x, y, pic, hp = [int(v, 16) for v in p[1:5]]; ty = int(p[5], 16) if len(p) > 5 else 3
    a = 0xA690 + y * 64 + x
    toks += ["poke:%04X=%02X" % (0x8FC7 + s, x), "poke:%04X=%02X" % (0x8FE7 + s, y), "poke:%04X=%02X" % (0x9007 + s, hp),
             "poke:%04X=%02X" % (0x9027 + s, pic), "poke:%04X=%02X" % (0x9047 + s, mp[a - 0xA690]), "poke:%04X=%02X" % (0x9067 + s, ty),
             "poke:%04X=%02X" % (a, pic)]
print(",".join(toks))
