"""Load every dungeon level of The Bard's Tale III through the stairs code and report what it holds.
From the checkpoint `cat_stairs` (catacombs arrival, "take the stairs up?") it pokes $0D=1 and $1052=LEVEL,
answers Y (the game loads level file LEVEL+$27 = $03), inserts the other dungeon side if asked, then reads the
level header at $1040 (name, level list, exit, monster file, size, row pointers) and counts visited squares
(byte 4 bit 0 of each 5-byte square). Writes OUT/LL.png (arrival) and OUT/LL_map.png (automap, `?`).
Usage: python3 games/apple2/bards-tale-3/tools/levels.py OUT [FIRST LAST]"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", "tools"))
import emu as E
game = E.Game("apple2/bards-tale-3")
out = sys.argv[1]
first = int(sys.argv[2], 16) if len(sys.argv) > 2 else 0
last = int(sys.argv[3], 16) if len(sys.argv) > 3 else 0x41
os.makedirs(out, exist_ok=True)
emu, rest, _ = E.start(game, "@cat_stairs")
E.play(emu, game, rest)
st = os.path.join(out, "base.state"); emu.save_state(st)
for lv in range(first, last + 1):
    emu.load_state(st)
    E.play(emu, game, E.expand(game, ["poke:000D=01", "poke:1052=%02X" % lv, "y", "w1200"]))
    side = "A"
    if emu.peek(0x03, 1)[0] != lv + 0x27 or emu.peek(0x1040, 1)[0] == 0xC3 and lv != 0x28:
        side = "B"
        E.play(emu, game, E.expand(game, ["disk:4", "space", "w1500"]))
    z = emu.peek(0, 16)
    h = emu.peek(0x1040, 0x30)
    name = bytes(b & 0x7F for b in h[:16]).decode("ascii", "replace").rstrip("\x7f")
    w, hh = h[0x1E], h[0x1F]
    rows = [h[0x22 + 2 * k] | h[0x23 + 2 * k] << 8 for k in range(min(hh + 1, 7))]
    ok = w and hh and all(rows[k] - rows[k + 1] == 5 * w for k in range(len(rows) - 1))
    base = 0x1040 + (emu.peek(0x1062 + 2 * hh, 1)[0] | emu.peek(0x1063 + 2 * hh, 1)[0] << 8)
    sq = emu.peek(base, 5 * w * hh) if ok else b""
    vis = sum(1 for i in range(w * hh) if sq[5 * i + 4] & 1) if ok else -1
    emu.screen_png(os.path.join(out, "%02X.png" % lv))
    E.play(emu, game, E.expand(game, ["shift+slash", "w300"]))
    emu.screen_png(os.path.join(out, "%02X_map.png" % lv))
    print("%02X side %s $03=%02X name=%-16r flags=%02X levels=%s exit=%02X,%02X city %02X mon=%02X size=%dx%d rows %s visited %d/%d" % (
        lv, side, z[3], name, h[0x10], " ".join("%02X" % b for b in h[0x12:0x1A]), h[0x1A], h[0x1B], h[0x1C], h[0x1D],
        w, hh, "ok" if ok else "BAD", vis, w * hh), flush=True)
