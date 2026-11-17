"""Game-aware emulator layer: games, routes, tokens, checkpoints, settling, contact sheets.

  python3 tools/emu.py GAME --seq "@title,start,w60,a" --out work/x [--save S] [--model M]
      one-shot run: a screenshot per token (NN_token.png), sheet.png, log.txt (token, frame, PC)

GAME is a slug under games/ (games/<slug>/game.json; see tools/intake.py). Paths are relative to the repo root.

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
  rec:N[:K[:P]]                         clip: record N frames, keeping every Kth (default 2), as an animated GIF
                                        (last token of a shot route: shoot.py / play.py record); elsewhere a plain
                                        wait of N frames, so routes that continue after a clip stay the same;
                                        P = kept frame used as the poster still (default 0 = first; -1 = last)
  pow, shot                             no-ops (power-on marker, extra screenshot)
  NAME                                  macro from game.json "macros" (UPPERCASE), expanded recursively
  @checkpoint                           first token only: start from that checkpoint (games/<slug>/checkpoints.txt)
Shortcuts (cataloguing, not a fair playthrough: use them freely, with realistic values; docs/emulator/README.md):
  set:ADDR=DEC[:N[:bcd|be]]             write a decimal value in N bytes (default 1; little-endian binary,
                                        `bcd` = packed BCD low byte first, `be` = big-endian): set:C0B0=8973:2
  gs:01VVAAAA                           GameShark code: written now and re-written after every token for the
                                        rest of the route, like the device (8n/9n = CGB WRAM bank n)
  freeze:ADDR=HEX / unfreeze            the same for a raw value; unfreeze drops all held values
Route prefixes (start of a route or a checkpoint route only; a route from @checkpoint inherits them):
  rom:NAME                              play a patched copy: game.json "rom_variants" NAME
                                        {"gg": [Game Genie codes], "ips": [paths], "bytes": {"HEXOFF": "HEX"}}
  sav:NAME                              power on with the battery save rom/saves/<slug>/NAME.sav (downloaded or
                                        made; never committed; record its source and SHA-1 in the playbook)

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

    def rom_file(self, variant=None):
        """The ROM to load: the dump, or a patched copy built from game.json "rom_variants" (work/roms/)."""
        self.check_rom()
        if not variant:
            return self.rom
        spec = self.meta.get("rom_variants", {}).get(variant)
        if spec is None:
            raise ValueError("unknown rom variant %r (game.json rom_variants)" % variant)
        data = bytearray(open(self.rom, "rb").read())
        for ips in spec.get("ips", []):
            apply_ips(data, open(os.path.join(ROOT, ips), "rb").read())
        for off, hx in spec.get("bytes", {}).items():
            o = int(off, 16)
            data[o:o + len(bytes.fromhex(hx))] = bytes.fromhex(hx)
        backend = platforms.PLATFORMS[self.platform]
        for code in spec.get("gg", []):
            if not backend.apply_game_genie(data, code):
                print("warning: Game Genie %s patched nothing (compare byte differs: other ROM revision?)" % code,
                      file=sys.stderr)
        out = os.path.join(WORK, "roms", self.slug, variant + os.path.splitext(self.rom)[1])
        os.makedirs(os.path.dirname(out), exist_ok=True)
        if not os.path.exists(out) or open(out, "rb").read() != data:
            open(out, "wb").write(data)
        return out

    def sav_file(self, name):
        """Battery save NAME: games/<slug>/saves/ (made here, committed) first, then rom/saves/<slug>/ (downloaded)."""
        p = os.path.join(self.dir, "saves", name + ".sav")
        if not os.path.exists(p):
            p = os.path.join(ROOT, "rom", "saves", self.slug, name + ".sav")
        if not os.path.exists(p):
            raise SystemExit("save missing: %s (see the playbook Shortcuts for its source)" % os.path.relpath(p, ROOT))
        return p

    def checkpoints(self):
        return read_table(os.path.join(self.dir, "checkpoints.txt"), ("name", "description", "route"))

    def ram(self):
        """game.json "ram": {"lives": {"addr": "C0A2", "size": 1, "fmt": "le|be|bcd", "note": "..."}} -> the
        values every play.py do/status prints (fmt bcd = packed BCD, high byte first, e.g. money)."""
        return self.meta.get("ram", {})


def apply_ips(data, patch):
    """Apply an IPS patch to a bytearray in place (RLE records and truncation extension supported)."""
    if patch[:5] != b"PATCH":
        raise ValueError("not an IPS patch")
    i = 5
    while patch[i:i + 3] != b"EOF":
        off = int.from_bytes(patch[i:i + 3], "big")
        size = int.from_bytes(patch[i + 3:i + 5], "big")
        i += 5
        if size:
            chunk = patch[i:i + size]
            i += size
        else:
            n = int.from_bytes(patch[i:i + 2], "big")
            chunk = patch[i + 2:i + 3] * n
            i += 3
        if off + len(chunk) > len(data):
            data.extend(b"\0" * (off + len(chunk) - len(data)))
        data[off:off + len(chunk)] = chunk
    return data


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


def prefix(toks):
    """Leading rom:/sav: tokens -> ({"rom": NAME, "sav": NAME}, the rest)."""
    opts, i = {}, 0
    while i < len(toks) and toks[i].split(":")[0] in ("rom", "sav") and ":" in toks[i]:
        k, v = toks[i].split(":", 1)
        opts[k] = v
        i += 1
    return opts, toks[i:]


def encode_value(value, n=1, fmt="le"):
    if fmt == "bcd":
        digits = "%0*d" % (n * 2, value)
        if len(digits) > n * 2:
            raise ValueError("%d does not fit %d BCD bytes" % (value, n))
        return bytes(int(digits[j:j + 2], 16) for j in range(len(digits) - 2, -1, -2))
    return value.to_bytes(n, "big" if fmt == "be" else "little")


def apply_freezes(emu):
    for bank, addr, data in getattr(emu, "freezes", []):
        if bank is None:
            emu.poke(addr, data)
        else:
            emu.poke_bank(bank, addr, data)


def hold_value(emu, game, tok):
    """gs:/freeze:/unfreeze bookkeeping (also used to restore held values after loading a cached state)."""
    if not hasattr(emu, "freezes"):
        emu.freezes = []
    if tok == "unfreeze":
        emu.freezes = []
    elif tok.startswith("gs:"):
        bank, addr, v = platforms.PLATFORMS[game.platform].gameshark(tok[3:])
        emu.freezes = [f for f in emu.freezes if f[:2] != (bank, addr)] + [(bank, addr, bytes([v]))]
    elif tok.startswith("freeze:"):
        addr, data = tok[7:].split("=")
        emu.freezes = [f for f in emu.freezes if f[:2] != (None, int(addr, 16))] + \
            [(None, int(addr, 16), bytes.fromhex(data))]
    else:
        return False
    return True


def restore_freezes(emu, game, toks):
    emu.freezes = []
    for t in toks:
        hold_value(emu, game, t)


KEYTOK = re.compile(r"^([a-z+>]+)(?::(\d+))?$")


def step(emu, game, tok):
    """Play one token. Returns False if it is not a token."""
    n, base = 1, tok
    m = re.match(r"^(.*)\*(\d+)$", tok)
    if m:
        base, n = m.group(1), int(m.group(2))
    for _ in range(n):
        if base in ("pow", "shot", "!") or base.startswith(("rom:", "sav:")):
            pass                    # rom:/sav: act at power-on (start()), nothing to do mid-route
        elif hold_value(emu, game, base):
            apply_freezes(emu)
        elif base.startswith("set:"):
            addr, rest = base[4:].split("=")
            parts = rest.split(":")
            n = int(parts[1]) if len(parts) > 1 else 1
            emu.poke(int(addr, 16), encode_value(int(parts[0]), n, parts[2] if len(parts) > 2 else "le"))
        elif base == "settle":
            settle(emu, game)
        elif re.match(r"^w\d+$", base):
            emu.frames(int(base[1:]))
        elif re.match(r"^rec:\d+(:\d+)?(:-?\d+)?$", base):
            emu.frames(int(base.split(":")[1]))
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
        apply_freezes(emu)
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
        apply_freezes(emu)
        ran += step_
        cur = emu.screen()
        if cur == prev:
            return True, ran
        prev = cur
    return False, ran


# ------------------------------------------------------------------ opening a game at a route
def open_game(game, model=None, state=None, opts=None):
    """Power on (opts: {"rom": variant, "sav": name} from the route prefix), optionally load a state."""
    opts = opts or {}
    rom = game.rom_file(opts.get("rom"))
    sav = game.sav_file(opts["sav"]) if opts.get("sav") else None
    emu = platforms.backend(game.platform).open(rom, model=model or game.model, seed=1, sav=sav)
    emu.freezes = []
    if state:
        emu.load_state(state)
    return emu


def cache_path(game, toks, model):
    """Cache file for the state at the end of a flat route: keyed by the exact ROM (dump or variant), the save
    file, the model and the tokens."""
    opts, _ = prefix(toks)
    h = hashlib.sha1(open(game.rom_file(opts.get("rom")), "rb").read())
    if opts.get("sav"):
        h.update(open(game.sav_file(opts["sav"]), "rb").read())
    key = hashlib.sha1((h.hexdigest() + "|" + model + "|" + ",".join(toks)).encode()).hexdigest()[:16]
    return os.path.join(WORK, "cache", game.slug, key + ".state")


def start(game, route, model=None, cache=True):
    """Open the emulator at the end of the route's checkpoint (cached per ROM/model/route), return
    (emu, remaining tokens, full flat route). Without a checkpoint: power-on and all tokens remain."""
    model = model or game.model
    toks = expand(game, split(route))
    if not (toks and toks[0].startswith("@")):
        opts, rest = prefix(toks)
        return open_game(game, model, opts=opts), rest, resolve(game, route)
    base = resolve(game, toks[0])
    rest = toks[1:]
    if prefix(rest)[0]:
        raise ValueError("rom:/sav: must come first in a checkpoint's own route, not after @checkpoint")
    opts, base_toks = prefix(base)
    path = cache_path(game, base, model)
    if not (cache and os.path.exists(path)):
        emu = open_game(game, model, opts=opts)
        play(emu, game, base_toks)
        if cache:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            tmp = "%s.%d.tmp" % (path, os.getpid())
            emu.save_state(tmp)
            os.replace(tmp, path)       # atomic: parallel runs may race
        return emu, rest, base + rest
    emu = open_game(game, model, path, opts)
    restore_freezes(emu, game, base)        # held GameShark values are not part of a savestate
    return emu, rest, base + rest


# ------------------------------------------------------------------ clips
FPS = 59.7275       # Game Boy frame rate


def rec_token(tok):
    """'rec:240:2:30' -> (240, 2, 30) (frames, every, poster index); None if not a rec token."""
    m = re.match(r"^rec:(\d+)(?::(\d+))?(?::(-?\d+))?$", tok)
    return (int(m.group(1)), int(m.group(2) or 2), int(m.group(3) or 0)) if m else None


def record(emu, game, n, every=2):
    """Run n frames from the current state, keeping a frame every `every` frames (the first one included).
    Held GameShark values stay applied. Returns PNG bytes per kept frame."""
    frames = [emu.screen()]
    for _ in range(n // every):
        emu.frames(every)
        apply_freezes(emu)
        frames.append(emu.screen())
    rest = n - (n // every) * every
    if rest:
        emu.frames(rest)
    return frames


def write_gif(frames, path, every=2, scale=1, hold_ms=None, durations=None):
    """Animated GIF from PNG bytes, nearest-neighbour scaled, at game speed (or hold_ms per frame), looping.
    GIF delays are in 10 ms steps: the per-frame delay alternates so the average matches the game's timing."""
    from PIL import Image
    ims = []
    for f in frames:
        im = f if isinstance(f, Image.Image) else Image.open(io.BytesIO(f) if isinstance(f, bytes) else f)
        im = im.convert("RGB")
        if scale > 1:
            im = im.resize((im.width * scale, im.height * scale), Image.NEAREST)
        ims.append(im.convert("P", palette=Image.ADAPTIVE, colors=256))
    if durations:
        durs = list(durations)
    elif hold_ms:
        durs = [hold_ms] * len(ims)
    else:
        per = every * 1000.0 / FPS
        durs, acc = [], 0.0
        for _ in ims:
            acc += per
            d = int(round(acc / 10.0)) * 10 - sum(durs)
            durs.append(max(d, 20))
    ims[0].save(path, save_all=True, append_images=ims[1:], duration=durs, loop=0, optimize=False, disposal=1)


# ------------------------------------------------------------------ images
def enlarge(src, dst, scale=3):
    from PIL import Image
    im = Image.open(src).convert("RGB")
    im.resize((im.width * scale, im.height * scale), Image.NEAREST).save(dst)


def ascii_label(s):
    """Image labels use PIL's default bitmap font: fold accents (Pokémon -> Pokemon), drop what it cannot draw."""
    import unicodedata
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()


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
            d.text((x + 2, y + h), ascii_label(labels[i])[:26], fill=(230, 230, 230))
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
