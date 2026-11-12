"""Walk the maze at random until the screen leaves the maze code (encounter, stairs prompt, door message...).

Usage: python3 tools/explore.py ROM STATE OUTDIR [MAXSTEPS=300] [SEED=7]
Writes OUTDIR/prev.state (before the last step), hit.state + hit_NNN.png when something other than the maze
banks ($1F/$20) ran, and last.png. Print the inputs with the seed: same ROM + state + seed = same walk.
Rev 1: walking into a wall shows 'Ouch!' (31:4592) until a direction key; the walk then turns.
Note: a HIT is any non-maze code (battle, stairs, door message); look at hit_NNN.png. Moved from
work/triage/battle1/explore.py (2026-11-11).
"""
import sys, os, random, hashlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import emu

rom, st, out = sys.argv[1:4]
maxsteps = int(sys.argv[4]) if len(sys.argv) > 4 else 300
os.makedirs(out, exist_ok=True)
random.seed(int(sys.argv[5]) if len(sys.argv) > 5 else 7)
g = emu.open_emu(rom, st)


def h():
    return hashlib.md5(g.screenshot()).hexdigest()


def act(k):
    g.input_set([k]); g.run_frames(8); g.input_set([])
    bs = set()
    for _ in range(14):
        g.run_frames(3); bs.add(g.regs()["banks"]["rom"])
    return bs


def hit(i, bs):
    g.screenshot_png(out + "/hit_%03d.png" % i)
    g.snapshot_save(path=os.path.abspath(out + "/hit.state"))
    print("HIT", bs)


for i in range(maxsteps):
    before = h()
    g.snapshot_save(path=os.path.abspath(out + "/prev.state"))
    bs = act("up")
    after = h()
    bumped = 0x4592 <= int.from_bytes(g.mem_read(0xC1BF, 2), "little") <= 0x4597   # Rev 1 'Ouch!' (wall)
    print(i, "up", sorted(bs), before != after, flush=True)
    if bs - {31, 32}:
        hit(i, bs); break
    if bumped or before == after or random.random() < 0.25:   # a turn also closes the 'Ouch!' box
        k = random.choice(["left", "right"])
        bs = act(k)
        print(i, k, sorted(bs), flush=True)
        if bs - {31, 32}:
            hit(i, bs); break
g.screenshot_png(out + "/last.png")
g.close()
