"""Drive the gbemu-cli emulator: run an input sequence, take screenshots, save a contact sheet and a state.

  python3 tools/emu.py --out work/qa/run1 --seq "boot,right*3,a,w60,a"            # patched build from power-on
  python3 tools/emu.py --out work/qa/run2 --state work/states/x.state --seq "a,w30"
  python3 tools/emu.py --rom rom/wizardry_empire_j.gbc ...                          # the original, for comparison

Sequence tokens (comma separated, KEY*n repeats):
  a b start select up down left right   press (8 frames) then wait 40 frames
  KEY+KEY                               press together
  KEY>KEY                               hold the first 4 frames, then both (held modifier, e.g. select>a)
  wN                                    wait N frames
  boot                                  power on and go through logo/title/mode select to the town (~1100 frames)
  shot                                  extra screenshot (one is taken after every token anyway)
  PARTY                                 the 6-member party formed at the tavern (expands to tokens)
  poke:ADDR=HEX                         write bytes, e.g. poke:C88C=80 (member 1 poisoned)
Route cache: a route starting with `boot` or `boot,PARTY` loads that prefix's end state from
work/cache/<rom sha1>/ (made on first use, per exact ROM), so only its last prefix token gets a screenshot.
--no-cache plays it. Scripts: g, toks, skip = emu.start(rom, seq); emu.play(g, toks[skip:]).
Outputs in --out: NN_token.png per token, sheet.png (all shots), log.txt (token, frame, PC, ROM bank), and
end.state if --save is given. Exit status 2 if the CPU looks hung (VBlank counter $C00A unchanged for 120 frames).
Turbo (no real-time pacing) is the default in open_emu(); turbo=False for timing work.
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
# Form the standard 6-member party at the tavern from the town (routes write it as PARTY).
PARTY = "right*3,a,w60,a,w40" + ",a,w30" * 6 + ",b,w40,b,w40,b,w60"
CACHE = os.path.join(ROOT, "work", "cache")
# Route prefixes whose end state is cached per ROM (start()): power-on to the town, and the town with the party.
PREFIXES = ["boot", "boot," + PARTY]


def open_emu(rom=EN_ROM, state=None, seed=1, turbo=True):
    """Turbo = no real-time pacing (same frames, ~7x faster; checked 2026-11-12). turbo=False for timing work."""
    g = GBEmu(BIN)
    g.load_rom(rom, model="cgb", seed=seed)
    if turbo:
        g.cmd("turbo", on=True)
    if state:
        g.snapshot_load(path=state)
    return g


def tokens(seq):
    """'boot,PARTY,a*2' -> ['boot', <PARTY tokens>, 'a*2'] (PARTY expanded)."""
    return [t.strip() for t in seq.replace("PARTY", PARTY).split(",") if t.strip()]


def _rom_key(rom):
    import hashlib
    return hashlib.sha1(open(rom, "rb").read()).hexdigest()[:12]


def start(rom=EN_ROM, seq="", state=None, cache=True):
    """Open the emulator for a route. When the route starts with a PREFIXES entry (and no state is given), load
    the cached end state of that prefix for this exact ROM (work/cache/<rom sha1>/), creating it on first use.
    Returns (g, toks, skip): toks = the route's tokens, skip = how many of them the cache already played.
    Same frames as playing them: the prefix is deterministic (seed 1); tour A/B checked 2026-11-12."""
    import hashlib
    toks = tokens(seq)
    if state or not cache:
        return open_emu(rom, state), toks, 0
    best = None
    for p in PREFIXES:
        pt = tokens(p)
        if toks[:len(pt)] == pt and (best is None or len(pt) > len(best)):
            best = pt
    if not best:
        return open_emu(rom), toks, 0
    d = os.path.join(CACHE, _rom_key(rom))
    path = os.path.join(d, hashlib.sha1(",".join(best).encode()).hexdigest()[:10] + ".state")
    if not os.path.exists(path):
        os.makedirs(d, exist_ok=True)
        g = open_emu(rom)
        play(g, best)
        tmp = "%s.%d.tmp" % (path, os.getpid())
        g.screenshot_png(tmp + ".png", scale=1)     # a loaded state has no rendered frame: keep the prefix's shot
        os.replace(tmp + ".png", path[:-6] + ".png")
        g.snapshot_save(path=tmp)
        os.replace(tmp, path)       # atomic: parallel runs may race to create it
        g.close()
    g = open_emu(rom, path)
    g.prefix_png = path[:-6] + ".png"
    return g, toks, len(best)


def step(g, tok):
    """Play one token (KEY*n repeats): boot, wN, KEY, KEY+KEY, KEY>KEY. False if unknown."""
    n, base = 1, tok
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
        elif chord_token(base):
            chord(g, *chord_token(base))
        elif base.startswith("poke:"):         # poke:C88C=80 or poke:C880=0102 (hex address = hex bytes)
            addr, data = base[5:].split("=")
            g.mem_write(int(addr, 16), list(bytes.fromhex(data)))
        else:
            return False
    return True


def play(g, toks):
    for t in (tokens(toks) if isinstance(toks, str) else toks):
        if not step(g, t):
            raise ValueError("unknown token %r" % t)


def press(g, keys, hold=8, wait=40):
    g.input_set(keys)
    g.run_frames(hold)
    g.input_set([])
    g.run_frames(wait)


def chord(g, first, then, lead=4, hold=8, wait=40):
    """Hold `first` alone for `lead` frames, then `first`+`then` (a held modifier: Select and A pressed on the same
    frame register as A only). Token: `select>a`."""
    g.input_set(first)
    g.run_frames(lead)
    g.input_set(first + then)
    g.run_frames(hold)
    g.input_set([])
    g.run_frames(wait)


def chord_token(base):
    """'select>a' -> (['select'], ['a']); None if not a chord token."""
    if ">" not in base:
        return None
    a, b = base.split(">", 1)
    first, then = a.split("+"), b.split("+")
    return (first, then) if all(k in KEYS for k in first + then) else None


def boot(g):
    """Power-on -> logos -> title -> mode select -> town (cursor on the Edge of Town)."""
    g.run_frames(750)
    for _ in range(4):
        g.input_tap("start")
        g.run_frames(60)
    press(g, ["b"], hold=6, wait=60)
    g.run_frames(60)        # the town's info box is drawn after the fade; inputs before that are lost


def loops(g, frames=120):
    """Main-loop passes in `frames` frames (count-only breakpoint on 0:07C5). Town/camp idle is 360 per 120 frames on
    the original; a VWF cache that misses every pass shows as 72-90 (speed checks, docs/re/vwf.md)."""
    bid = g.break_add(0x07C5, stop=False)
    g.run_frames(frames)
    n = next(b["hits"] for b in g.break_list() if b.get("id") == bid)
    g.break_del(bid)
    return n


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


def run(seq, out, rom=EN_ROM, state=None, save=None, cache=True):
    os.makedirs(out, exist_ok=True)
    g, toks, skip = start(rom, seq, state, cache)
    shots, log = [], []
    for i, tok in enumerate(toks):
        if i < skip - 1:
            continue                # played by the cached prefix: only its last token gets a screenshot
        if i >= skip and not step(g, tok):
            sys.exit("unknown token %r" % tok)
        p = os.path.join(out, "%02d_%s.png" % (i, tok.replace("*", "x").replace("+", "_").replace(">", "-")))
        if i == skip - 1:
            import shutil
            shutil.copyfile(g.prefix_png, p)
        else:
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
    ap.add_argument("--no-cache", action="store_true")
    a = ap.parse_args()
    sys.exit(run(a.seq, a.out, a.rom, a.state, a.save, not a.no_cache))
