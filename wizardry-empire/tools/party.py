"""Standard playtest party: rename the six default characters, form the party, save checkpoint states.

  python3 tools/party.py [--rom ROM] [--out work/states/party]

Names (owner's choice): ryz (Fighter), condi (Thief), ebo (Archer), cubi (Priest), deddo (Mage), mnz (Bishop),
renamed in the Training Grounds ("Change name"), so the classes stay the balanced default party.
Writes checkpoint states into <out>/ (plus sheet_*.png for checking):
  renamed.state  town, the six renamed (no party)
  party.state    town, party of six formed at Rose's Tavern, cursor on the tavern
  camp.state     first floor of the maze, Camp open (from Edge of Town > Explore the maze)
  maze.state     first floor of the maze, Camp closed, facing the corridor.
All inputs come from power-on, so the states can be rebuilt for any build.
"""
import argparse, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import emu

NAMES = ["ryz", "condi", "ebo", "cubi", "deddo", "mnz"]   # roster order: Fighter Thief Archer Priest Mage Bishop
ROWS = ["ABCDEFGHIJKLMNO", "PQRSTUVWXYZ!?.'", "abcdefghijklmno", "pqrstuvwxyz -/ ", "0123456789"]


def pos(ch):
    for r, row in enumerate(ROWS):
        if ch in row:
            return r, row.index(ch)
    raise ValueError(ch)


def type_name(g, name):
    """Cursor starts on A (0,0) in a fresh name entry."""
    r, c = 0, 0
    for ch in name:
        r2, c2 = pos(ch)
        for _ in range(abs(r2 - r)):
            emu.press(g, ["down" if r2 > r else "up"], wait=12)
        for _ in range(abs(c2 - c)):
            emu.press(g, ["right" if c2 > c else "left"], wait=12)
        emu.press(g, ["a"], wait=20)
        r, c = r2, c2
    emu.press(g, ["start"], wait=60)


def seq(g, tokens):
    for t in tokens.split(","):
        n = 1
        if "*" in t:
            t, n = t.split("*")
            n = int(n)
        for _ in range(n):
            if t.startswith("w"):
                g.run_frames(int(t[1:]))
            else:
                emu.press(g, [t])


def shot(g, out, name):
    g.screenshot_png(os.path.join(out, "sheet_%s.png" % name), scale=1)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--rom", default=emu.EN_ROM)
    ap.add_argument("--out", default=os.path.join(HERE, "..", "work", "states", "party"))
    ap.add_argument("--only", type=int, default=6, help="rename only the first N (debugging)")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    g = emu.open_emu(a.rom)
    emu.boot(g)
    seq(g, "right,a,w60")                                   # Training Grounds
    seq(g, "down*3,a,w60")                                  # Change name -> character list
    for i, name in enumerate(NAMES[:a.only]):
        seq(g, "down,a,w60" if i else "a,w60")              # the list cursor stays on the last one renamed
        type_name(g, name)
        shot(g, a.out, "rename_%d" % i)
    seq(g, "b,w60,b,w60")                                   # back to town (cursor on the Training Grounds)
    g.snapshot_save(path=os.path.join(a.out, "renamed.state"))
    shot(g, a.out, "town")
    if a.only < 6:
        return
    seq(g, "right*2,a,w60,a,w40" + ",a,w30" * 6 + ",b,w40,b,w40,b,w60")   # Rose's Tavern: add all six
    g.snapshot_save(path=os.path.join(a.out, "party.state"))
    shot(g, a.out, "party")
    seq(g, "left*3,a,w60,a,w150")                            # Edge of Town > Explore the maze -> Camp
    g.snapshot_save(path=os.path.join(a.out, "camp.state"))
    shot(g, a.out, "camp")
    seq(g, "b,w60")
    g.snapshot_save(path=os.path.join(a.out, "maze.state"))
    shot(g, a.out, "maze")
    print("wrote", os.path.relpath(a.out))


if __name__ == "__main__":
    main()
