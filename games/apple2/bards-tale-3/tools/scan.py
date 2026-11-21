"""Scan the current map of The Bard's Tale III: from a checkpoint, poke the party onto every square (0009 = north,
000A = east), turn left and right (the game evaluates the square) and group the squares by what the message
window and the picture show. Writes one PNG per group to OUT and prints the groups (east,north).
Usage: python3 games/apple2/bards-tale-3/tools/scan.py CHECKPOINT OUT [WAIT] [W] [H] [EXTRA_ROUTE]"""
import sys, os, hashlib
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", "tools"))
import emu as E
game = E.Game("apple2/bards-tale-3")
cp, out = sys.argv[1], sys.argv[2]
wait = sys.argv[3] if len(sys.argv) > 3 else "w300"
w = int(sys.argv[4]) if len(sys.argv) > 4 else 20
h = int(sys.argv[5]) if len(sys.argv) > 5 else w
extra = sys.argv[6] if len(sys.argv) > 6 else ""
os.makedirs(out, exist_ok=True)
emu, rest, _ = E.start(game, "@" + cp + ("," + extra if extra else ""))
E.play(emu, game, rest)
st = os.path.join(out, "base.state"); emu.save_state(st)
groups = {}
lines = [0x2000 + (r & 7) * 0x400 + ((r >> 3) & 7) * 0x80 + (r >> 6) * 0x28 for r in range(192)]
for x in range(w):
    for y in range(h):
        emu.load_state(st)
        E.play(emu, game, E.expand(game, ["poke:0009=%02X" % y, "poke:000A=%02X" % x, "l", "j", wait]))
        msg = bytes(b for a in lines[8:150] for b in emu.peek(a + 17, 22))
        pic = bytes(b for a in lines[160:170] for b in emu.peek(a + 1, 14))  # location name plate
        k = hashlib.sha1(msg + pic).hexdigest()[:8]
        if k not in groups:
            groups[k] = []
            emu.screen_png(os.path.join(out, "g_%s.png" % k))
        groups[k].append((x, y))
for k, v in sorted(groups.items(), key=lambda kv: len(kv[1])):
    print(k, len(v), " ".join("%d,%d" % a for a in v[:40]))
