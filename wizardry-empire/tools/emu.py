"""Drive the gbemu-cli emulator: run an input sequence, take screenshots, save a contact sheet and a state.

  python3 tools/emu.py --out work/qa/run1 --seq "boot,right*3,a,w60,a"            # patched build from power-on
  python3 tools/emu.py --out work/qa/run2 --state work/states/x.state --seq "a,w30"
  python3 tools/emu.py --rom rom/wizardry_empire_j.gbc ...                          # the original, for comparison

Sequence tokens (comma separated, KEY*n repeats):
  a b start select up down left right   press (8 frames) then wait 40 frames
  KEY+KEY                               press together
  wN                                    wait N frames
  boot                                  power on and go through logo/title/mode select to the town (~1100 frames)
  shot                                  extra screenshot (one is taken after every token anyway)
Outputs in --out: NN_token.png per token, sheet.png (all shots), log.txt (token, frame, PC, ROM bank), and
end.state if --save is given. Exit status 2 if the CPU looks hung (same PC/frame counter for 120 frames).
Mapper/RAM facts for scripts: docs/re/text.md. Python client: tools/gbemu-cli/cli/py/gbemu.py.
"""
import argparse, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
sys.path.insert(0, os.path.join(HERE, "gbemu-cli", "cli", "py"))
from gbemu import GBEmu  # noqa: E402

BIN = os.path.join(HERE, "gbemu-cli", "build", "gbemu")
EN_ROM = os.path.join(ROOT, "build", "wizardry_empire_en.gbc")
KEYS = {"a", "b", "start", "select", "up", "down", "left", "right"}


def open_emu(rom=EN_ROM, state=None, seed=1, turbo=True):
    """Turbo = no real-time pacing (same frames, ~7x faster; checked 2026-11-12). turbo=False for timing work."""
    g = GBEmu(BIN)
    g.load_rom(rom, model="cgb", seed=seed)
    if turbo:
        g.cmd("turbo", on=True)
    if state:
        g.snapshot_load(path=state)
    return g


def press(g, keys, hold=8, wait=40):
    g.input_set(keys)
    g.run_frames(hold)
    g.input_set([])
    g.run_frames(wait)


def boot(g):
    """Power-on -> logos -> title -> mode select -> town (cursor on the Edge of Town)."""
    g.run_frames(750)
    for _ in range(4):
        g.input_tap("start")
        g.run_frames(60)
    press(g, ["b"], hold=6, wait=60)
    g.run_frames(60)        # the town's info box is drawn after the fade; inputs before that are lost


def frame_counter(g):
    return g.mem_read(0xC00A, 1)[0]


def hung(g):
    """True if the VBlank counter ($C00A) does not move for 120 frames."""
    c0 = frame_counter(g)
    g.run_frames(120)
    return frame_counter(g) == c0


def sheet(paths, out, cols=4, scale=2):
    from PIL import Image
    ims = [Image.open(p) for p in paths]
    if not ims:
        return
    w, h = ims[0].size
    rows = (len(ims) + cols - 1) // cols
    s = Image.new("RGB", (w * cols, h * rows), (255, 0, 0))
    for i, im in enumerate(ims):
        s.paste(im, ((i % cols) * w, (i // cols) * h))
    s = s.resize((s.width * scale // 2, s.height * scale // 2))
    s.save(out)


def run(seq, out, rom=EN_ROM, state=None, save=None):
    os.makedirs(out, exist_ok=True)
    g = open_emu(rom, state)
    shots, log = [], []
    for i, tok in enumerate(t.strip() for t in seq.split(",") if t.strip()):
        n = 1
        base = tok
        if "*" in tok:
            base, n = tok.split("*")
            n = int(n)
        for _ in range(n):
            if base == "boot":
                boot(g)
            elif base == "shot":
                pass
            elif base.startswith("w") and base[1:].isdigit():
                g.run_frames(int(base[1:]))
            elif all(k in KEYS for k in base.split("+")):
                press(g, base.split("+"))
            else:
                sys.exit("unknown token %r" % tok)
        p = os.path.join(out, "%02d_%s.png" % (i, tok.replace("*", "x").replace("+", "_")))
        g.screenshot_png(p, scale=1)
        shots.append(p)
        r = g.regs()
        log.append("%02d %-12s pc=%s bank=%02d" % (i, tok, r["pc"], r["banks"]["rom"]))
    sheet(shots, os.path.join(out, "sheet.png"))
    if save:
        os.makedirs(os.path.dirname(os.path.abspath(save)), exist_ok=True)
        g.snapshot_save(path=os.path.abspath(save))
    is_hung = hung(g)
    if is_hung:
        r = g.regs()
        log.append("HUNG: frame counter stopped; pc=%s bank=%02d backtrace=%s" % (
            r["pc"], r["banks"]["rom"], [(e["addr"], e["bank"]) for e in g.backtrace()["entries"][:6]]))
    open(os.path.join(out, "log.txt"), "w").write("\n".join(log) + "\n")
    g.close()
    print("\n".join(log))
    return 2 if is_hung else 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--rom", default=EN_ROM)
    ap.add_argument("--state")
    ap.add_argument("--seq", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--save")
    a = ap.parse_args()
    sys.exit(run(a.seq, a.out, a.rom, a.state, a.save))
