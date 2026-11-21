"""Print poke tokens that mark every square of the current dungeon level visited (automap bit, byte 4 bit 0),
for a full-automap shot: python3 games/apple2/bards-tale-3/tools/fill.py "@cat_stairs,LV:18:00" (used by map_mountain_full)."""
import sys
import os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", "tools"))
import emu as E
game = E.Game("apple2/bards-tale-3")
route = sys.argv[1]
emu, rest, _ = E.start(game, route); E.play(emu, game, E.expand(game, rest) if rest else [])
h = emu.peek(0x1040, 0x30); w, hh = h[0x1E], h[0x1F]
ptr = lambda k: emu.peek(0x1062 + 2*k, 1)[0] | emu.peek(0x1063 + 2*k, 1)[0] << 8
toks = []; vis = 0
for n in range(hh):
    a = 0x1040 + ptr(n + 1); row = bytearray(emu.peek(a, 5*w))
    for e in range(w):
        vis += row[5*e+4] & 1; row[5*e+4] |= 1
    toks.append("poke:%04X=%s" % (a, row.hex().upper()))
print("# level", bytes(b & 0x7f for b in h[:16]), w, hh, "visited before", vis, file=sys.stderr)
print(",".join(toks))
