"""Game-aware emulator layer: games, routes, tokens, checkpoints, settling, contact sheets.

  python3 tools/emu.py GAME --seq "@title,start,w60,a" --out work/x [--save S] [--model M]
      one-shot run: a screenshot per token (NN_token.png), sheet.png, log.txt (token, frame, PC)

GAME is a slug under games/ (games/<slug>/game.json; see tools/intake.py). Paths are relative to gamedb/.

Routes are comma-separated tokens:
  a b start select up down left right   press: hold `press.hold` frames, then wait `press.wait` (game.json,
                                        default 8 / 40)
  KEY+KEY                               press together (b+a)
  KEY>KEY                               held modifier: first alone 4 frames, then both
  KEY:N   KEY+KEY:N                     hold N frames, release, no extra wait (walking, charging)
  TOKEN*n                               repeat (right*3, a:20*4)
  wN                                    wait N frames
  mash:KEY:N                            tap KEY every 8 frames for N frames (skip text, mash through intros)
  poke:ADDR=HEX                         write bytes (poke:C0A2=09)
  settle                                run until the screen is stable (two identical frames `settle.step`
                                        apart, at most `settle.limit` frames); deterministic like any token
  !                                     last token only (shoot.py): take the frame as is, no final settle
                                        (auto-advancing messages, animations caught mid-way)
  pow, shot                             no-ops (power-on marker, extra screenshot)
  NAME                                  macro from game.json "macros" (UPPERCASE), expanded recursively
  @checkpoint                           first token only: start from that checkpoint (games/<slug>/checkpoints.txt)

Checkpoints (`name | description | route`) are built on demand by replaying their route from power-on and cached
per exact ROM and route in work/cache/<slug>/ (savestates are never committed; the route is the source of truth).
Everything is deterministic (fixed seed, fixed boot ROM), so a route always gives the same frames.
"""
import argparse, hashlib, io, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
sys.path.insert(0, HERE)
import platforms  # noqa: E402

GAMES = os.path.join(ROOT, "games")
WORK = os.path.join(ROOT, "work")


# ------------------------------------------------------------------ games
class Game:
    def __init__(self, slug):
        self.slug = slug
        self.dir = os.path.join(GAMES, slug)
        p = os.path.join(self.dir, "game.json")
        if not os.path.exists(p):
            raise SystemExit("no game %r (games/%s/game.json); run tools/intake.py ROM first" % (slug, slug))
        self.meta = json.load(open(p, encoding="utf-8"))
        self.platform = self.meta["platform"]
        self.model = self.meta.get("model")
        self.rom = os.path.join(ROOT, self.meta["rom"])
        self.macros = self.meta.get("macros", {})
        press = self.meta.get("press", {})
        self.hold, self.wait = press.get("hold", 8), press.get("wait", 40)
        st = self.meta.get("settle", {})
        self.settle_step, self.settle_limit = st.get("step", 10), st.get("limit", 300)
        self.keys = platforms.PLATFORMS[self.platform].keys

    def check_rom(self):
        if not os.path.exists(self.rom):
            raise SystemExit("ROM missing: %s (copy your dump there; SHA-1 %s)" % (
                os.path.relpath(self.rom, ROOT), self.meta.get("sha1")))
        sha = hashlib.sha1(open(self.rom, "rb").read()).hexdigest()
        if self.meta.get("sha1") and sha != self.meta["sha1"]:
            raise SystemExit("ROM %s has SHA-1 %s, game.json expects %s" % (self.rom, sha, self.meta["sha1"]))
        return sha

    def checkpoints(self):
        return read_table(os.path.join(self.dir, "checkpoints.txt"), ("name", "description", "route"))

    def ram(self):
        """game.json "ram": {"lives": {"addr": "C0A2", "size": 1, "note": "..."}} -> watch list for status."""
        return self.meta.get("ram", {})


def read_table(path, fields):
    """`a | b | c` lines (# comments, blank lines skipped); the last field takes the rest of the line."""
    out = []
    if not os.path.exists(path):
        return out
    for n, line in enumerate(open(path, encoding="utf-8"), 1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = [x.strip() for x in line.split("|", len(fields) - 1)]
        if len(parts) != len(fields):
            raise SystemExit("%s:%d: expected %d fields (%s)" % (path, n, len(fields), " | ".join(fields)))
        out.append(dict(zip(fields, parts)))
    return out


# ------------------------------------------------------------------ tokens and routes
def split(route):
    return [t.strip() for t in route.split(",") if t.strip()]


def expand(game, toks, depth=0):
    """Expand macros (UPPERCASE names in game.json) recursively."""
    if depth > 20:
        raise ValueError("macro recursion too deep")
    out = []
    for t in toks:
        if t in game.macros:
            out += expand(game, split(game.macros[t]), depth + 1)
        else:
            out.append(t)
    return out


def resolve(game, route, seen=()):
    """Route -> flat token list from power-on (checkpoints and macros expanded). Used for replay and cache keys."""
    toks = expand(game, split(route))
    if toks and toks[0].startswith("@"):
        name = toks[0][1:]
        if name in seen:
            raise ValueError("checkpoint loop: %s" % " -> ".join(seen + (name,)))
        cps = {c["name"]: c for c in game.checkpoints()}
        if name not in cps:
            raise ValueError("unknown checkpoint @%s (games/%s/checkpoints.txt)" % (name, game.slug))
        return resolve(game, cps[name]["route"], seen + (name,)) + toks[1:]
    return toks


KEYTOK = re.compile(r"^([a-z+>]+)(?::(\d+))?$")


def step(emu, game, tok):
    """Play one token. Returns False if it is not a token."""
    n, base = 1, tok
    m = re.match(r"^(.*)\*(\d+)$", tok)
    if m:
        base, n = m.group(1), int(m.group(2))
    for _ in range(n):
        if base in ("pow", "shot", "!"):
            pass
        elif base == "settle":
            settle(emu, game)
        elif re.match(r"^w\d+$", base):
            emu.frames(int(base[1:]))
        elif base.startswith("poke:"):
            addr, data = base[5:].split("=")
            emu.poke(int(addr, 16), bytes.fromhex(data))
        elif base.startswith("mash:"):
            _, key, frames = base.split(":")
            for _ in range(int(frames) // 8):
                emu.input(key.split("+"))
                emu.frames(2)
                emu.input([])
                emu.frames(6)
        else:
            m = KEYTOK.match(base)
            if not m:
                return False
            keys, held = m.group(1), m.group(2)
            if ">" in keys:
                first, then = keys.split(">", 1)
                first, then = first.split("+"), then.split("+")
                if not all(k in game.keys for k in first + then):
                    return False
                emu.input(first)
                emu.frames(4)
                emu.input(first + then)
                emu.frames(int(held) if held else game.hold)
                emu.input([])
                emu.frames(0 if held else game.wait)
                continue
            keys = keys.split("+")
            if not all(k in game.keys for k in keys):
                return False
            emu.input(keys)
            emu.frames(int(held) if held else game.hold)
            emu.input([])
            if not held:
                emu.frames(game.wait)
    return True


def play(emu, game, toks):
    for t in toks:
        if not step(emu, game, t):
            raise ValueError("unknown token %r (keys: %s)" % (t, " ".join(sorted(game.keys))))


def settle(emu, game, step_=None, limit=None):
    """Run until two frames `step` apart are identical (text typed, fade done). Returns (settled, frames run).
    Animated screens never settle: capture anyway and mark them."""
    step_, limit = step_ or game.settle_step, limit or game.settle_limit
    prev, ran = emu.screen(), 0
    while ran < limit:
        emu.frames(step_)
        ran += step_
        cur = emu.screen()
        if cur == prev:
            return True, ran
        prev = cur
    return False, ran


# ------------------------------------------------------------------ opening a game at a route
def open_game(game, model=None, state=None):
    game.check_rom()
    emu = platforms.backend(game.platform).open(game.rom, model=model or game.model, seed=1)
    if state:
        emu.load_state(state)
    return emu


def cache_path(game, toks, model):
    sha = hashlib.sha1(open(game.rom, "rb").read()).hexdigest()[:12]
    key = hashlib.sha1((model + "|" + ",".join(toks)).encode()).hexdigest()[:12]
    return os.path.join(WORK, "cache", game.slug, sha, key + ".state")


def start(game, route, model=None, cache=True):
    """Open the emulator at the end of the route's checkpoint (cached per ROM/model/route), return
    (emu, remaining tokens, full flat route). Without a checkpoint: power-on and all tokens remain."""
    model = model or game.model
    toks = expand(game, split(route))
    if not (toks and toks[0].startswith("@")):
        return open_game(game, model), toks, resolve(game, route)
    base = resolve(game, toks[0])
    rest = toks[1:]
    path = cache_path(game, base, model)
    if not (cache and os.path.exists(path)):
        emu = open_game(game, model)
        play(emu, game, base)
        if cache:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            tmp = "%s.%d.tmp" % (path, os.getpid())
            emu.save_state(tmp)
            os.replace(tmp, path)       # atomic: parallel runs may race
        return emu, rest, base + rest
    return open_game(game, model, path), rest, base + rest


# ------------------------------------------------------------------ images
def enlarge(src, dst, scale=3):
    from PIL import Image
    im = Image.open(src).convert("RGB")
    im.resize((im.width * scale, im.height * scale), Image.NEAREST).save(dst)


def sheet(paths, out, cols=4, labels=None):
    """Contact sheet at native size with an optional caption under each frame."""
    from PIL import Image, ImageDraw
    ims = [Image.open(p).convert("RGB") for p in paths]
    if not ims:
        return
    w, h = max(i.width for i in ims), max(i.height for i in ims)
    lh = 12 if labels else 0
    rows = (len(ims) + cols - 1) // cols
    s = Image.new("RGB", (w * cols, (h + lh) * rows), (32, 32, 32))
    d = ImageDraw.Draw(s)
    for i, im in enumerate(ims):
        x, y = (i % cols) * w, (i // cols) * (h + lh)
        s.paste(im, (x, y))
        if labels:
            d.text((x + 2, y + h), labels[i][:26], fill=(230, 230, 230))
    s.save(out)


# ------------------------------------------------------------------ one-shot run
def run(game, route, out, model=None, save=None):
    os.makedirs(out, exist_ok=True)
    emu, rest, full = start(game, route, model)
    shots, log = [], []
    p = os.path.join(out, "00_start.png")
    emu.screen_png(p)
    shots.append(p)
    for i, tok in enumerate(rest, 1):
        if not step(emu, game, tok):
            sys.exit("unknown token %r" % tok)
        p = os.path.join(out, "%02d_%s.png" % (i, re.sub(r"[^\w.-]", "_", tok)[:24]))
        emu.screen_png(p)
        shots.append(p)
        r = emu.regs()
        log.append("%02d %-14s pc=%s bank=%s" % (i, tok, r["pc"], r.get("bank")))
    sheet(shots, os.path.join(out, "sheet.png"))
    if save:
        os.makedirs(os.path.dirname(os.path.abspath(save)), exist_ok=True)
        emu.save_state(save)
    log.append("route: " + ",".join(full))
    open(os.path.join(out, "log.txt"), "w").write("\n".join(log) + "\n")
    emu.close()
    print("\n".join(log))
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("game")
    ap.add_argument("--seq", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--save")
    ap.add_argument("--model")
    a = ap.parse_args()
    sys.exit(run(Game(a.game), a.seq, a.out, a.model, a.save))
