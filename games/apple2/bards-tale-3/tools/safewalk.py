"""Walk without random fights in The Bard's Tale III: from a route, play steps "tok,tok;tok,..." one by one; before each
step try waits (w0, w10 ... ~w400) until the location plate under the view (UnterBrae, Big Slath ...) is unchanged
60 frames after the step, i.e. no fight began. Prints the chosen tokens per step, positions (north east facing) and
the whole route. Usage: python3 games/apple2/bards-tale-3/tools/safewalk.py @checkpoint "l,w60;i,w60;k,w60"
Used for seq-dungeon-walk and seq-automap (2026-11-21)."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", "tools"))
import emu as E
game = E.Game("apple2/bards-tale-3")
base, steps = sys.argv[1], sys.argv[2].split(";")
emu, rest, _ = E.start(game, base); E.play(emu, game, rest)
lines = [0x2000 + (r & 7) * 0x400 + ((r >> 3) & 7) * 0x80 + (r >> 6) * 0x28 for r in range(192)]
plate = lambda: bytes(b for a in lines[98:110] for b in emu.peek(a + 1, 14))
ref = plate()
import tempfile; st = os.path.join(tempfile.mkdtemp(), "g.state")
out = []
for s in steps:
    parts = s.split(",")
    emu.save_state(st)
    for extra in [0, 10, 20, 30, 45, 5, 15, 25, 35, 50, 70, 90] + list(range(100, 400, 7)):
        emu.load_state(st)
        toks = ([] if not extra else ["w%d" % extra]) + parts
        E.play(emu, game, E.expand(game, toks))
        # look a bit ahead too: fights can show up during the next wait
        emu.save_state(st + "2")
        E.play(emu, game, ["w60"])
        ok = plate() == ref
        emu.load_state(st + "2")
        if ok: break
    else:
        print("NO SAFE WAIT for", s); sys.exit(1)
    out.append(",".join(toks))
    print(s, "->", ",".join(toks), "pos", emu.peek(9,1)[0], emu.peek(10,1)[0], emu.peek(11,1)[0], flush=True)
print("ROUTE", base + "," + ",".join(out))
