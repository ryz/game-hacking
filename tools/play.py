"""Persistent play session for any registered game: one emulator kept running, driven by short commands
(~1 s each), with capture built in. Every session knows its replayable route, so each snapshot and checkpoint
is reproducible from power-on (states are a cache, routes are the record).

  python3 tools/play.py start GAME [--route "@title"] [--model M]   power on (or start at a checkpoint/route)
  python3 tools/play.py do "right:30,a"      play tokens (tools/emu.py syntax), then settle; prints the
                                             screenshot path, whether it settled, PC and the game.json RAM watch
  python3 tools/play.py do! "a,w5"           same without the final settle (catch a moving frame)
  python3 tools/play.py undo                 back to before the last do (one level)
  python3 tools/play.py shot [PATH]          screenshot only (default work/play/NAME/last.png, 3x)
  python3 tools/play.py snap ID CATEGORY "caption" [--set SET]
                                             capture the current frame for the database: native PNG (+ 3x copy in 3x/) into
                                             work/shots/GAME/SET/ (default set: main), its line (with the full
                                             route) appended to that set's shots.txt and index.json
  python3 tools/play.py recaption ID "caption" [--set SET]    change a shot's caption (no replay)
  python3 tools/play.py unsnap ID [--set SET]                 remove a shot from the working set
  python3 tools/play.py record ID CATEGORY FRAMES "caption" [--every K] [--poster P] [--set SET]
                                             clip: record FRAMES frames from now (every Kth kept, default 2) as
                                             <id>.gif (+ 3x/<id>.gif; poster <id>.png) into the set, route + `rec:N:K`
                                             in its shots.txt; the session moves on by FRAMES frames; prints
                                             work/play/NAME/clip_ID.png (every kept frame, numbered) - pick a
                                             poster still with --poster P (kept frame number; -1 = last)
  python3 tools/play.py checkpoint NAME "description"
                                             save a state and add `NAME | description | route` to
                                             games/GAME/checkpoints.txt (replaces a line of the same name)
  python3 tools/play.py export NAME "description" [--state]
                                             after saving IN THE GAME: write the battery save to
                                             games/GAME/saves/NAME.sav (committed; loads in any emulator as
                                             <rom name>.sav, and in routes as sav:NAME) and document it in
                                             games/GAME/saves/README.md; --state also writes NAME.state
                                             (SameBoy savestate of this exact moment, SameBoy only)
  python3 tools/play.py goto NAME            jump to a checkpoint (built from its route if not cached)
  python3 tools/play.py route                the current route (replay it with emu.py or a shots.txt line)
  python3 tools/play.py status               PC/bank + every game.json "ram" watch value
  python3 tools/play.py peek ADDR [N] | poke ADDR HEX
  python3 tools/play.py find "EXPR" | find reset
                                             RAM search (cheat-search style, narrows each call): e.g. lose a
                                             life, `find "new == old - 1"`; repeat until a few addresses remain
  python3 tools/play.py dump NAME           save work/save RAM to work/play/<session>/dump_NAME.json
  python3 tools/play.py diff A [B]           bytes that differ between dumps A and B (B omitted: RAM now);
                                             e.g. dump before a step, step, `diff before`
  python3 tools/play.py stop

--name N on any command runs a parallel session (default 'main'). Log: work/play/NAME/log.txt.
"""
import json, os, re, shutil, socket, socketserver, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
sys.path.insert(0, HERE)
PLAY = os.path.join(ROOT, "work", "play")


def sdir(name):
    return os.path.join(PLAY, name)


def sock_path(name):
    return os.path.join("/tmp", "gamedb_play_%s_%d.sock" % (name, os.getuid()))


def _pixels(png):
    import io
    from PIL import Image
    return Image.open(io.BytesIO(png)).convert("RGB").tobytes()


def rel(p):
    return os.path.relpath(p, ROOT)


# ------------------------------------------------------------------ server
class Session:
    def __init__(self, slug, route, model, name):
        import emu
        self.E, self.name = emu, name
        self.game = emu.Game(slug)
        self.model = model or self.game.model
        self.dir = sdir(name)
        os.makedirs(self.dir, exist_ok=True)
        route = route or "pow"
        self.emu, rest, _ = emu.start(self.game, route, self.model)
        emu.play(self.emu, self.game, rest)
        toks = emu.split(route)
        self.base = toks[0] if toks and toks[0].startswith("@") else "pow"
        self.toks = [t for t in toks if not t.startswith("@") and t != "pow"]
        self.undo_state = None
        self.n = 0
        # a loaded state has no rendered frame yet: snap refuses until a `do` has run frames
        self.stale = bool(rest == [] and route.split(",")[0].startswith("@"))
        self.meta_mtime = os.path.getmtime(os.path.join(self.game.dir, "game.json"))

    def reload_game(self):
        """Pick up game.json edits (new macros, RAM watches) without restarting the session."""
        p = os.path.join(self.game.dir, "game.json")
        if os.path.getmtime(p) != self.meta_mtime:
            self.game = self.E.Game(self.game.slug)
            self.meta_mtime = os.path.getmtime(p)

    def route(self):
        return ",".join([self.base] + self.toks)

    def watch(self):
        out = []
        for k, v in self.game.ram().items():
            n = int(v.get("size", 1))
            b = self.emu.peek(int(v["addr"], 16), n)
            fmt = v.get("fmt", "le")
            if fmt == "bcd":          # packed BCD, most significant byte first (as most GB games store money)
                out.append("%s=%s" % (k, b.hex().lstrip("0") or "0"))
            elif fmt == "hex":        # as the playbook writes it (coordinates, ids, flags), little-endian
                out.append("%s=$%0*X" % (k, 2 * n, int.from_bytes(b, "little")))
            else:
                out.append("%s=%d" % (k, int.from_bytes(b, "big" if fmt == "be" else "little")))
        r = self.emu.regs()
        return "pc=%s bank=%s  %s" % (r["pc"], r.get("bank"), " ".join(out))

    def shot(self, path=None, scale=3):
        path = path or os.path.join(self.dir, "last.png")
        self.emu.screen_png(path)
        if scale > 1:
            self.E.enlarge(path, path, scale)
        return path

    def do(self, seq, settle=True):
        self.reload_game()
        self.stale = False
        raw = [t for t in self.E.split(seq) if t != "pow"]
        toks = self.E.expand(self.game, raw)
        self.undo_state = os.path.join(self.dir, "undo.state")
        self.emu.save_state(self.undo_state)
        self.undo_toks = list(self.toks)
        self.undo_freezes = list(getattr(self.emu, "freezes", []))
        self.E.play(self.emu, self.game, toks)
        settled = None
        if settle:
            settled, _ = self.E.settle(self.emu, self.game)
            raw = raw + ["settle"]
        self.toks += raw        # the route keeps macro names (readable; follows macro fixes)
        self.n += 1
        p = self.shot(os.path.join(self.dir, "%03d.png" % self.n))
        shutil.copyfile(p, os.path.join(self.dir, "last.png"))
        note = "" if settled is None else ("" if settled else "  (screen still changing: animated?)")
        with open(os.path.join(self.dir, "log.txt"), "a") as f:
            f.write("%03d %s -> %s%s\n" % (self.n, seq, rel(p), note))
        return "%s%s\n%s" % (rel(p), note, self.watch())

    def edit_shot(self, cmd, sid, caption, set_="main"):
        """unsnap: remove a shot from the working set (shots.txt, index.json, its images). recaption: change its
        caption in both files. No replay; index.md and the sheet are rebuilt."""
        import shoot
        d = os.path.join(ROOT, "work", "shots", self.game.slug, set_)
        lst, ip = os.path.join(d, "shots.txt"), os.path.join(d, "index.json")
        if not (os.path.exists(lst) and os.path.exists(ip)):
            return "error: no working set %s" % os.path.relpath(d, ROOT)
        idx = json.load(open(ip, encoding="utf-8"))
        shot = next((s for s in idx["shots"] if s["id"] == sid), None)
        if shot is None:
            return "error: no shot %r in set %s" % (sid, set_)
        lines = open(lst, encoding="utf-8").read().splitlines()
        if cmd == "unsnap":
            idx["shots"] = [s for s in idx["shots"] if s["id"] != sid]
            lines = [l for l in lines if l.split("|")[0].strip() != sid]
            for k in ("file", "file_3x", "clip", "clip_3x"):
                f = shot.get(k) and os.path.join(d, shot[k])
                if f and os.path.exists(f):
                    os.remove(f)
        else:
            if not caption:
                return 'usage: play.py recaption ID "new caption"'
            shot["caption"] = caption
            out = []
            for l in lines:
                parts = [x.strip() for x in l.split("|")]
                if parts[0] == sid and len(parts) >= 4:
                    parts[2] = caption.replace("|", "/")
                    l = " | ".join(parts[:3]) + " | " + "|".join(l.split("|")[3:]).strip()
                out.append(l)
            lines = out
        open(lst, "w", encoding="utf-8").write("\n".join(lines) + "\n")
        json.dump(idx, open(ip, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
        shoot.reindex(self.game, d)
        return "%s %s (%d shots in %s); publish again to update games/%s/shots/%s/" % (
            "removed" if cmd == "unsnap" else "recaptioned", sid, len(idx["shots"]), set_, self.game.slug, set_)

    def snap(self, sid, cat, caption, set_="main"):
        if not re.match(r"^[a-z0-9_]+$", sid):
            return "error: id must be lowercase a-z0-9_ (area_thing)"
        import shoot
        if shoot.check_category(cat):
            return shoot.check_category(cat)
        if self.stale:
            return ("error: the screen is stale after goto/undo/start at a checkpoint (the frame shown is not this "
                    "state's); run `do settle` (or `do! w1`) first, then snap")
        d = os.path.join(ROOT, "work", "shots", self.game.slug, set_)
        os.makedirs(d, exist_ok=True)
        import shoot
        stem = shoot.prefix(set_) + sid
        native = os.path.join(d, "%s.png" % stem)
        before = open(native, "rb").read() if os.path.exists(native) else None
        self.emu.screen_png(native)
        unchanged = before is not None and _pixels(before) == _pixels(open(native, "rb").read())
        self.E.enlarge(native, self.E.x3(native))
        a = self.emu.screen()
        self.emu.save_state(os.path.join(self.dir, "snap.state"))
        self.emu.frames(self.game.settle_step)
        settled = a == self.emu.screen()
        self.emu.load_state(os.path.join(self.dir, "snap.state"))
        route = self.route()
        if not route.endswith(",settle"):
            route += ",!"
        lines = [l for l in (open(os.path.join(d, "shots.txt"), encoding="utf-8").read().splitlines()
                             if os.path.exists(os.path.join(d, "shots.txt")) else [])
                 if not l.startswith(sid + " ")]
        lines.append("%s | %s | %s | %s" % (sid, cat, caption.replace("|", "/"), route))
        open(os.path.join(d, "shots.txt"), "w", encoding="utf-8").write("\n".join(lines) + "\n")
        import shoot
        shoot.index_update(self.game, d, {"id": sid, "category": cat, "caption": caption, "route": route,
                                          "settled": settled, "model": self.model, "source": "play.py snap"})
        return "%s%s%s" % (rel(native), "" if settled else "  (not settled: animated frame, check it)",
                           "  (UNCHANGED: identical to the PNG this id already had)" if unchanged else "")

    def record(self, sid, cat, frames, caption, every=2, set_="main", poster=0):
        if not re.match(r"^[a-z0-9_]+$", sid):
            return "error: id must be lowercase a-z0-9_ (area_thing)"
        import shoot
        if shoot.check_category(cat):
            return shoot.check_category(cat)
        if self.stale:
            return "error: the screen is stale after goto/undo; run `do settle` (or `do! w1`) first"
        import shoot
        d = os.path.join(ROOT, "work", "shots", self.game.slug, set_)
        os.makedirs(d, exist_ok=True)
        self.emu.save_state(os.path.join(self.dir, "undo.state"))
        self.undo_state, self.undo_toks = os.path.join(self.dir, "undo.state"), list(self.toks)
        self.undo_freezes = list(getattr(self.emu, "freezes", []))
        n, k, p = int(frames), int(every), int(poster)
        clip = shoot.clip_files(self.game, self.emu, shoot.prefix(set_) + sid, d, n, k, p)
        kept = clip.pop("_frames")
        tok = "rec:%d:%d" % (n, k) + (":%d" % p if p else "")
        route = self.route() + "," + tok
        self.toks.append(tok)
        sheet_p = os.path.join(self.dir, "clip_%s.png" % sid)
        tmp = []
        for i, png in enumerate(kept):
            t = os.path.join(self.dir, "_clipf_%03d.png" % i)
            open(t, "wb").write(png)
            tmp.append(t)
        self.E.sheet(tmp, sheet_p, cols=8, labels=["%d (f+%d)" % (i, i * k) for i in range(len(tmp))])
        for t in tmp:
            os.remove(t)
        lines = [l for l in (open(os.path.join(d, "shots.txt"), encoding="utf-8").read().splitlines()
                             if os.path.exists(os.path.join(d, "shots.txt")) else [])
                 if not l.startswith(sid + " ")]
        lines.append("%s | %s | %s | %s" % (sid, cat, caption.replace("|", "/"), route))
        open(os.path.join(d, "shots.txt"), "w", encoding="utf-8").write("\n".join(lines) + "\n")
        shoot.index_update(self.game, d, {"id": sid, "category": cat, "caption": caption, "route": route,
                                          "settled": False, "model": self.model, "source": "play.py record",
                                          "clip": clip})
        self.shot()
        return "%s (%d frames kept, %.1f s, poster = kept frame %d; session moved on %s frames)\n" \
               "kept frames, numbered for --poster: %s (re-record after `undo` to change the poster)" % (
                   rel(os.path.join(d, clip["file"])), clip["kept"], clip["seconds"], p, frames, rel(sheet_p))

    def checkpoint(self, name, desc):
        if not re.match(r"^[a-z0-9_]+$", name):
            return "error: checkpoint name must be lowercase a-z0-9_"
        path = os.path.join(self.game.dir, "checkpoints.txt")
        route = self.route()
        if self.base == "@" + name:
            return "error: the session started from @%s; a checkpoint cannot start from itself" % name
        lines = open(path, encoding="utf-8").read().splitlines() if os.path.exists(path) else []
        lines = [l for l in lines if not re.match(r"^%s\s*\|" % re.escape(name), l)]
        lines.append("%s | %s | %s" % (name, desc.replace("|", "/"), route))
        open(path, "w", encoding="utf-8").write("\n".join(lines) + "\n")
        full = self.E.resolve(self.game, "@" + name)
        cp = self.E.cache_path(self.game, full, self.model)
        os.makedirs(os.path.dirname(cp), exist_ok=True)
        self.emu.save_state(cp)
        self.base, self.toks = "@" + name, []
        return "checkpoint %s saved (%d tokens from power-on)" % (name, len(full))

    def export(self, name, desc, state=False):
        if not re.match(r"^[a-z0-9_]+$", name):
            return "error: save name must be lowercase a-z0-9_"
        kib = self.game.meta.get("header", {}).get("ram_kib")
        if not kib:
            return "error: this cartridge has no battery RAM (header ram_kib); use --state only via checkpoint"
        d = os.path.join(self.game.dir, "saves")
        os.makedirs(d, exist_ok=True)
        data = self.emu.battery(kib * 1024)
        if not data.strip(b"\x00") or not data.strip(b"\xff"):
            return ("error: the battery RAM is empty (nothing was saved in the game on this route). Save in the "
                    "game first, then export; nothing written")
        p = os.path.join(d, name + ".sav")
        open(p, "wb").write(data)
        files = "`%s.sav`" % name
        if state:
            self.emu.save_state(os.path.join(d, name + ".state"))
            files += ", `%s.state`" % name
        import hashlib
        readme = os.path.join(d, "README.md")
        head = ("# %s - saves\n\nMade by the agents while playing (owner's rule 2026-11-15: committed so the owner can "
                "jump in). `.sav` = the game's own battery save: copy it next to your ROM as `<rom name>.sav` in any "
                "emulator, then Continue. `.state` = %s savestate of the exact moment (that emulator only). In routes: "
                "`sav:NAME` prefix (power on with that save).\n\n| Save | Files | What it contains | Route at export | "
                "SHA-1 (.sav) | Date |\n|---|---|---|---|---|---|\n" % (self.game.meta["title"], self.emu.emulator))
        lines = open(readme, encoding="utf-8").read().splitlines() if os.path.exists(readme) else head.splitlines()
        lines = [l for l in lines if not l.startswith("| %s |" % name)]
        import datetime
        lines.append("| %s | %s | %s | `%s` | `%s` | %s |" % (name, files, desc.replace("|", "/"), self.route(),
                     hashlib.sha1(data).hexdigest()[:12], datetime.date.today().isoformat()))
        open(readme, "w", encoding="utf-8").write("\n".join(lines) + "\n")
        return "%s (%d KiB)%s - check the in-game save was made before exporting" % (
            rel(p), kib, " + state" if state else "")

    def goto(self, name):
        self.emu.close()        # reopen: the checkpoint may use another ROM variant or save (start() uses the cache)
        self.emu, _, _ = self.E.start(self.game, "@" + name, self.model)
        self.base, self.toks = "@" + name, []
        self.stale = True
        return self.watch()

    def handle(self, cmd, args):
        E, e = self.E, self.emu
        if cmd in ("do", "do!"):
            return self.do(args[0], settle=cmd == "do")
        if cmd == "undo":
            if not self.undo_state:
                return "error: nothing to undo"
            e.load_state(self.undo_state)
            self.toks, self.undo_state = self.undo_toks, None
            e.freezes = self.undo_freezes
            self.stale = True
            return "%s (frame not redrawn yet: `do settle` before a snap)\n%s" % (rel(self.shot()), self.watch())
        if cmd == "shot":
            return rel(self.shot(args[0] if args else None))
        if cmd in ("unsnap", "recaption"):
            set_ = "main"
            if "--set" in args:
                i = args.index("--set")
                set_ = args[i + 1]
                args = args[:i] + args[i + 2:]
            return self.edit_shot(cmd, args[0], args[1] if len(args) > 1 else None, set_)
        if cmd == "snap":
            set_ = "main"
            if "--set" in args:
                i = args.index("--set")
                set_ = args[i + 1]
                args = args[:i] + args[i + 2:]
            return self.snap(args[0], args[1], args[2] if len(args) > 2 else "", set_)
        if cmd == "record":
            every, set_ = "2", "main"
            if "--every" in args:
                i = args.index("--every"); every = args[i + 1]; args = args[:i] + args[i + 2:]
            if "--set" in args:
                i = args.index("--set"); set_ = args[i + 1]; args = args[:i] + args[i + 2:]
            poster = "0"
            if "--poster" in args:
                i = args.index("--poster"); poster = args[i + 1]; args = args[:i] + args[i + 2:]
            return self.record(args[0], args[1], args[2], args[3] if len(args) > 3 else "", every, set_, poster)
        if cmd == "checkpoint":
            return self.checkpoint(args[0], args[1] if len(args) > 1 else "")
        if cmd == "export":
            st = "--state" in args
            args = [a for a in args if a != "--state"]
            return self.export(args[0], args[1] if len(args) > 1 else "", st)
        if cmd == "goto":
            return self.goto(args[0])
        if cmd == "route":
            return self.route()
        if cmd == "status":
            return self.watch()
        if cmd in ("dump", "diff"):
            ranges = getattr(e, "SEARCH", None) or [(0xC000, 0x2000), (0xA000, 0x2000), (0xFF80, 0x7F)]

            def snap():
                return {base + i: v for base, size in ranges for i, v in enumerate(e.peek(base, size))}

            def path(n):
                return os.path.join(sdir(self.name), "dump_%s.json" % n)
            if cmd == "dump":
                json.dump({"%X" % a: v for a, v in snap().items()}, open(path(args[0]), "w"))
                return "dumped %d bytes -> %s" % (sum(n for _, n in ranges), os.path.relpath(path(args[0]), ROOT))
            a = {int(k, 16): v for k, v in json.load(open(path(args[0]))).items()}
            b = {int(k, 16): v for k, v in json.load(open(path(args[1]))).items()} if len(args) > 1 else snap()
            ch = [(k, a[k], b[k]) for k in sorted(a) if k in b and a[k] != b[k]]
            rows = ["%04X  %02X -> %02X  (%d -> %d)" % (k, x, y, x, y) for k, x, y in ch[:80]]
            return "%d bytes differ%s\n%s" % (len(ch), " (first 80)" if len(ch) > 80 else "", "\n".join(rows))
        if cmd == "peek":
            a, n = int(args[0], 16), int(args[1], 0) if len(args) > 1 else 16
            data = e.peek(a, n)
            return "\n".join("%04x  %s" % (a + i, data[i:i + 16].hex(" ")) for i in range(0, n, 16))
        if cmd == "poke":
            e.poke(int(args[0], 16), bytes.fromhex(args[1]))
            self.toks.append("poke:%s=%s" % (args[0].upper(), args[1].upper()))
            return "ok (recorded in the route)"
        if cmd == "find":
            if args[0] == "reset":
                e.ram_search_reset()
                return "search reset"
            r = e.ram_search(args[0], wide="--wide" in args)
            rows = ["%s bank=%s value=%s" % (x["addr"], x.get("bank"), x["value"]) for x in r["results"][:20]]
            return "%d candidates\n%s" % (r["count"], "\n".join(rows))
        if cmd == "ping":
            return "pong"
        return "unknown command %r" % cmd


def serve(name, slug, route, model):
    path = sock_path(name)
    if os.path.exists(path):
        os.remove(path)
    sess = Session(slug, route, model, name)

    class H(socketserver.StreamRequestHandler):
        def handle(self):
            req = json.loads(self.rfile.readline())
            if req["cmd"] == "stop":
                self.wfile.write(b'"stopped"\n')
                sess.emu.close()
                os._exit(0)
            try:
                out = sess.handle(req["cmd"], req["args"])
            except Exception as ex:     # keep the session alive on a bad command
                out = "error: %s" % ex
            self.wfile.write((json.dumps(out) + "\n").encode())

    with socketserver.UnixStreamServer(path, H) as srv:
        open(os.path.join(sdir(name), "ready"), "w").write(str(os.getpid()))
        srv.serve_forever()


# ------------------------------------------------------------------ client
def call(name, cmd, args, timeout=900):
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    s.settimeout(timeout)
    s.connect(sock_path(name))
    s.sendall((json.dumps({"cmd": cmd, "args": args}) + "\n").encode())
    data = b""
    while not data.endswith(b"\n"):
        chunk = s.recv(65536)
        if not chunk:
            break
        data += chunk
    return json.loads(data)


def opt(args, key, default=None):
    if key in args:
        i = args.index(key)
        v = args[i + 1]
        del args[i:i + 2]
        return v
    return default


def main(argv):
    argv = list(argv)
    name = opt(argv, "--name", "main")
    if not argv:
        print(__doc__)
        return 2
    cmd, args = argv[0], argv[1:]
    if cmd == "_serve":
        serve(name, *[None if a == "-" else a for a in args])
        return 0
    if cmd == "start":
        route, model = opt(args, "--route", "-"), opt(args, "--model", "-")
        if not args:
            print("usage: play.py start GAME [--route R] [--model M]")
            return 2
        try:
            call(name, "stop", [], timeout=5)
        except OSError:
            pass
        d = sdir(name)
        os.makedirs(d, exist_ok=True)
        for f in ("ready", "log.txt"):
            if os.path.exists(os.path.join(d, f)):
                os.remove(os.path.join(d, f))
        log = open(os.path.join(d, "server.log"), "w")
        subprocess.Popen([sys.executable, __file__, "--name", name, "_serve", args[0], route, model],
                         stdout=log, stderr=log, start_new_session=True)
        for _ in range(2400):
            if os.path.exists(os.path.join(d, "ready")):
                print(call(name, "shot", []))
                print(call(name, "status", []))
                return 0
            time.sleep(0.25)
        print("server did not start; see", rel(os.path.join(d, "server.log")))
        print(open(os.path.join(d, "server.log")).read()[-2000:])
        return 1
    try:
        out = call(name, cmd, args)
    except OSError:
        print("no session %r running: python3 tools/play.py start GAME" % name)
        return 1
    print(out)
    return 1 if isinstance(out, str) and out.startswith("error") else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
