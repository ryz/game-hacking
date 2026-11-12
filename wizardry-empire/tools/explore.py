"""Walk the maze at random until a battle or another non-maze screen (chest, door message...).

Usage: python3 tools/explore.py ROM STATE OUTDIR [MAXSTEPS=1500] [SEED=7]
Writes OUTDIR/prev.state (before the last step), hit.state + hit_NNN.png when code outside the maze banks
($1F/$20) and the VWF bank ($40) ran, and last.png. Same ROM + state + seed = same walk.
Rev 1: walking into a wall shows 'Ouch!' (31:4592); the key that closes it does not turn, so a bump is
followed by two turn keys. The stairs prompt (31:41FA) is answered No. Moves: up 70%, else a random turn.
(Rewritten 2026-11-12 from the photographer's and playtester's walkers; the old one looped on 'Ouch!'.)
"""
import sys, os, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import emu

rom, st, out = sys.argv[1:4]
maxsteps = int(sys.argv[4]) if len(sys.argv) > 4 else 1500
os.makedirs(out, exist_ok=True)
random.seed(int(sys.argv[5]) if len(sys.argv) > 5 else 7)
g = emu.open_emu(rom, os.path.abspath(st))
MAZE = {31, 32, 64}


def act(k):
    g.input_set([k]); g.run_frames(8); g.input_set([])
    bs = set()
    for _ in range(14):
        g.run_frames(3); bs.add(g.regs()["banks"]["rom"])
    return bs


def msg():
    m = g.mem_read(0xC1BF, 3)
    return m[2], m[0] | m[1] << 8


def hit(i, bs):
    g.screenshot_png(out + "/hit_%03d.png" % i)
    g.snapshot_save(path=os.path.abspath(out + "/hit.state"))
    print(i, "HIT", sorted(bs), flush=True)


for i in range(maxsteps):
    g.snapshot_save(path=os.path.abspath(out + "/prev.state"))
    k = "up" if random.random() < 0.7 else random.choice(["left", "right"])
    bs = act(k)
    b, p = msg()
    if b == 0x31 and 0x41FA <= p <= 0x4240:              # stairs prompt: No
        act("down"); act("a"); g.run_frames(30)
        print(i, "stairs -> No", flush=True)
        continue
    if b == 0x31 and 0x4592 <= p <= 0x4597:              # 'Ouch!': close it, then turn
        t = random.choice(["left", "right"])
        bs |= act(t) | act(t)
    if bs - MAZE:
        hit(i, bs)
        break
g.screenshot_png(out + "/last.png")
g.close()
