"""Usage: python3 games/dos/ultimate-doom/tools/bosskill.py ROUTE TYPE OUTFILE [--go X Y] (capture 2026-11-25, run 2).
With --go: weapon 7, no clipping on, walk to X Y, no clipping off. Then up to 30 rounds: approach to ~400 units, aim, BFG (rockets when cells < 40) until the boss dies"""
import math, struct, sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dnav as N, dstate as D
nav = N.Nav(sys.argv[1]); T = int(sys.argv[2]); rounds = 30
start = len(nav.toks)
if '--go' in sys.argv:
    i = sys.argv.index('--go'); gx, gy = float(sys.argv[i + 1]), float(sys.argv[i + 2]); del sys.argv[i:i + 3]
    nav.do('7,type:idspispopd,w10'); nav.go(gx, gy); nav.do('type:idspispopd,w10')
    print('walked:', D.state(nav.emu))
for r in range(rounds):
    ms = [m for m in N.monsters(nav.emu) if m[1] == T]
    if not ms:
        print("boss gone (dead)"); break
    d, typ, mx, my, hp, ad = ms[0]
    px, py, _, _ = N.player(nav.emu)
    if d > 450:
        k = 380 / d
        nav.go(mx + (px - mx) * k, my + (py - my) * k)
        ms = [m for m in N.monsters(nav.emu) if m[1] == T] or ms
        d, typ, mx, my, hp, ad = ms[0]
    cells = struct.unpack("<i", nav.emu.peek(0x22B2F0, 4))[0]
    wpn = struct.unpack("<i", nav.emu.peek(0x22B2BC, 4))[0]
    want = 6 if cells >= 40 else 4
    if wpn != want:
        nav.do("%d,w30" % (want + 1))
    nav.face(mx, my, tol=1.5)
    nav.do("ctrl:10,w10,w50" if want == 6 else "ctrl:10,w30")
    hp2 = struct.unpack("<i", nav.emu.peek(ad + 108, 4))[0]
    print("round %d dist %.0f boss hp %d -> %d | %s" % (r, d, hp, hp2, D.state(nav.emu)))
    if hp2 <= 0:
        print("boss killed"); break
open(sys.argv[3], "w").write(",".join(nav.toks[start:]) + "\n")
print("tokens written", len(nav.toks) - start)
