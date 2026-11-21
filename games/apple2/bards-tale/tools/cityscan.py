"""Scan Skara Brae (30x30) or a dungeon level (SIZE 22): from a city checkpoint, poke the party onto every square (0000 = north coordinate,
0001 = east coordinate), press J (turn left: the game evaluates the square) and group the squares by what the
message window and the picture show. Writes one PNG per group to OUT and prints the groups.
Usage: python3 games/apple2/bards-tale/tools/cityscan.py CHECKPOINT OUT [WAIT] [SIZE] [EXTRA_ROUTE]"""
import sys, os, hashlib
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", "tools"))
import emu as E
game = E.Game("apple2/bards-tale")
cp, out = sys.argv[1], sys.argv[2]
wait = sys.argv[3] if len(sys.argv) > 3 else "w300"
size = int(sys.argv[4]) if len(sys.argv) > 4 else 30
extra = sys.argv[5] if len(sys.argv) > 5 else ""
os.makedirs(out, exist_ok=True)
emu, rest, _ = E.start(game, "@" + cp + ("," + extra if extra else ""))
E.play(emu, game, rest)
st = os.path.join(out, "base.state"); emu.save_state(st)
groups = {}
for x in range(size):
    for y in range(size):
        emu.load_state(st)
        E.play(emu, game, E.expand(game, ["poke:0000=%02X" % y, "poke:0001=%02X" % x, "j", wait]))
        scr = emu.peek(0x2000, 0x2000)
        # message window: hi-res bytes 20..37 of every line; picture: bytes 1..13
        lines = [0x2000 + (r & 7) * 0x400 + ((r >> 3) & 7) * 0x80 + (r >> 6) * 0x28 for r in range(192)]
        msg = bytes(b for a in lines[20:150] for b in emu.peek(a + 20, 17))
        k = hashlib.sha1(msg).hexdigest()[:8]
        pos = emu.peek(0, 2)
        if k not in groups:
            groups[k] = []
            emu.screen_png(os.path.join(out, "g_%s.png" % k))
        groups[k].append((x, y, pos[1], pos[0]))
for k, v in sorted(groups.items(), key=lambda kv: len(kv[1])):
    print(k, len(v), " ".join("%d,%d" % (a[0], a[1]) for a in v[:40]))
