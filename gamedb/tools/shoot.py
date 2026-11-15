"""Replay a shot list and build the database set: pixel-exact PNGs, @3x copies, catalogue, contact sheet.

  python3 tools/shoot.py GAME [SET]                 replay work/shots/GAME/SET/shots.txt (default set: main;
                                                    falls back to the plan games/GAME/shots.txt)
  python3 tools/shoot.py GAME SET --list FILE       another shot list
  python3 tools/shoot.py GAME SET --only id,id      only these ids (merged into the existing index)
  python3 tools/shoot.py GAME SET --verify          replay into a temp dir and compare with the PNGs already in
                                                    the set (e.g. made with play.py snap): proves every route
                                                    reproduces its frame; exit 3 on a mismatch
  python3 tools/shoot.py GAME SET --publish         replay the set, then copy it to games/GAME/shots/SET/ (committed)
  python3 tools/shoot.py GAME SET --publish-only    copy without replaying (right after a passing --verify)
  python3 tools/shoot.py GAME SET --model dmg       capture with another model (e.g. a DMG game also in CGB colours)

Shot list lines: `id | category | caption | route` (route: tools/emu.py tokens; may start with @checkpoint).
A route is played exactly, then `settle` is added unless it already ends with `settle` or `!`.
Outputs per shot: <id>.png (native, framebuffer as is: no filter, no colour correction, no scaling),
<id>@3x.png (nearest neighbour). Per set: index.json, index.md, sheet.png (all shots, captioned).
Clips: a route ending in `rec:N[:K]` records N frames (every Kth kept) from the end of the route: <id>.gif and
<id>@3x.gif at game speed, <id>.png / @3x = the first frame (poster). --verify compares every clip frame.
Sequences: a set named `seq-<action>` is an ordered action (shots in list order = steps): it also gets
strip.png (the steps left to right, numbered and captioned) and steps.gif / steps@3x.gif (one step per 1.5 s).
"""
import argparse, datetime, hashlib, json, os, shutil, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
sys.path.insert(0, HERE)
import emu as E  # noqa: E402

# Database categories (docs/capture-guide.md). Others are allowed but warned about.
CATEGORIES = ["boot", "title", "menu", "options", "cutscene", "gameplay", "hud", "system", "map", "inventory",
              "dialogue", "shop", "battle", "boss", "minigame", "ending", "credits", "gameover", "save", "extra"]


def index_update(game, d, entry, rom_sha1=None):
    """Insert/replace one shot in d/index.json and rewrite index.md and sheet.png."""
    p = os.path.join(d, "index.json")
    idx = json.load(open(p, encoding="utf-8")) if os.path.exists(p) else {}
    m = game.meta
    idx["game"] = {k: m.get(k) for k in ("slug", "title", "platform", "model", "sha1", "crc32")}
    idx["set"] = os.path.basename(d)
    shots = {s["id"]: s for s in idx.get("shots", [])}
    entry = dict(entry)
    entry.setdefault("file", entry["id"] + ".png")
    entry.setdefault("file_3x", entry["id"] + "@3x.png")
    entry["rom_sha1"] = rom_sha1 or m.get("sha1")
    entry["captured"] = datetime.date.today().isoformat()
    shots[entry["id"]] = entry
    order = [s["id"] for s in idx.get("shots", [])]
    if entry["id"] not in order:
        order.append(entry["id"])
    idx["shots"] = [shots[i] for i in order]
    json.dump(idx, open(p, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    write_md(idx, d)
    if os.path.basename(d).startswith("seq-"):
        sequence_files(idx, d)
    E.sheet([os.path.join(d, s["file"]) for s in idx["shots"] if os.path.exists(os.path.join(d, s["file"]))],
            os.path.join(d, "sheet.png"), cols=5, labels=[s["id"] for s in idx["shots"]
                                                          if os.path.exists(os.path.join(d, s["file"]))])


def sequence_files(idx, d):
    """strip.png + steps.gif for seq-* sets: the steps in order."""
    from PIL import Image, ImageDraw
    shots = [s for s in idx["shots"] if os.path.exists(os.path.join(d, s["file"]))]
    if not shots:
        return
    ims = [Image.open(os.path.join(d, s["file"])).convert("RGB") for s in shots]
    w, h = ims[0].size
    cols = min(len(ims), 4)
    rows = (len(ims) + cols - 1) // cols
    cap = 24
    st = Image.new("RGB", (w * cols, (h + cap) * rows), (32, 32, 32))
    dr = ImageDraw.Draw(st)
    for i, (im, s) in enumerate(zip(ims, shots)):
        x, y = (i % cols) * w, (i // cols) * (h + cap)
        st.paste(im, (x, y))
        dr.text((x + 2, y + h + 1), ("%d. %s" % (i + 1, s["id"]))[:26], fill=(240, 240, 240))
        dr.text((x + 2, y + h + 12), E.ascii_label(s.get("caption", ""))[:26], fill=(180, 180, 180))
    st.save(os.path.join(d, "strip.png"))
    paths = [os.path.join(d, s["file"]) for s in shots]
    E.write_gif(paths, os.path.join(d, "steps.gif"), hold_ms=1500)
    E.write_gif(paths, os.path.join(d, "steps@3x.gif"), scale=3, hold_ms=1500)


def write_md(idx, d):
    g = idx["game"]
    out = ["# %s - shots: %s" % (g["title"], idx["set"]), "",
           "Platform %s, model %s, ROM SHA-1 `%s`. %d shots. Contact sheet: [sheet.png](sheet.png)." % (
               g["platform"], g["model"], g["sha1"], len(idx["shots"])), "",
           "| id | category | caption | settled | image |", "|---|---|---|---|---|"]
    for s in idx["shots"]:
        clip = " [gif](%s) [gif 3x](%s)" % (s["clip"]["file"], s["clip"]["file_3x"]) if s.get("clip") else ""
        out.append("| %s | %s | %s | %s | [png](%s) [3x](%s)%s |" % (
            s["id"], s["category"], s.get("caption", ""), "yes" if s.get("settled") else "clip" if clip else "no",
            s["file"], s["file_3x"], clip))
    if idx["set"].startswith("seq-"):
        out += ["", "Sequence: [strip.png](strip.png), [steps.gif](steps.gif) ([3x](steps@3x.gif))."]
    out += ["", "Routes (replay with `tools/shoot.py`) are in `index.json` and `shots.txt`.", ""]
    open(os.path.join(d, "index.md"), "w", encoding="utf-8").write("\n".join(out))


def shoot_one(game, s, d, model):
    """Replay one shot (or clip). Returns settled (bool) for stills, the clip dict for clips."""
    route = s["route"]
    toks = E.split(route)
    rec = E.rec_token(toks[-1]) if toks else None
    if rec:
        e, rest, _ = E.start(game, ",".join(toks[:-1]), model)
        E.play(e, game, rest)
        return clip_files(game, e, s["id"], d, *rec, close=True)
    if not toks or toks[-1] not in ("settle", "!"):
        route += ",settle"
    e, rest, _ = E.start(game, route, model)
    E.play(e, game, rest)
    native = os.path.join(d, s["id"] + ".png")
    e.screen_png(native)
    a = e.screen()
    e.frames(game.settle_step)
    settled = a == e.screen()
    e.close()
    E.enlarge(native, os.path.join(d, s["id"] + "@3x.png"))
    return settled


def clip_files(game, e, sid, d, n, every, close=False):
    """Record a clip from the emulator's current state into d: <id>.gif, <id>@3x.gif, poster <id>.png/@3x."""
    frames = E.record(e, game, n, every)
    if close:
        e.close()
    E.write_gif(frames, os.path.join(d, sid + ".gif"), every)
    E.write_gif(frames, os.path.join(d, sid + "@3x.gif"), every, scale=3)
    open(os.path.join(d, sid + ".png"), "wb").write(frames[0])
    E.enlarge(os.path.join(d, sid + ".png"), os.path.join(d, sid + "@3x.png"))
    return {"frames": n, "every": every, "kept": len(frames), "seconds": round(n / E.FPS, 2),
            "file": sid + ".gif", "file_3x": sid + "@3x.gif"}


def _gif_frames(path):
    from PIL import Image, ImageSequence
    return [f.convert("RGB").tobytes() for f in ImageSequence.Iterator(Image.open(path))]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("game")
    ap.add_argument("set", nargs="?", default="main")
    ap.add_argument("--list")
    ap.add_argument("--only")
    ap.add_argument("--verify", action="store_true")
    ap.add_argument("--publish", action="store_true")
    ap.add_argument("--publish-only", action="store_true",
                    help="copy the work set to games/GAME/shots/SET/ without replaying (after a passing --verify)")
    ap.add_argument("--model")
    a = ap.parse_args()
    game = E.Game(a.game)
    model = a.model or game.model
    d = os.path.join(ROOT, "work", "shots", game.slug, a.set)
    os.makedirs(d, exist_ok=True)
    lst = a.list or os.path.join(d, "shots.txt")
    if not os.path.exists(lst):
        lst = os.path.join(game.dir, "shots.txt")
    shots = E.read_table(lst, ("id", "category", "caption", "route"))
    if a.only:
        want = set(a.only.split(","))
        shots = [s for s in shots if s["id"] in want]
    own = os.path.join(d, "shots.txt")
    if os.path.abspath(lst) != os.path.abspath(own) and not (a.only or a.verify):
        shutil.copyfile(lst, own)       # the set keeps the list it was shot from
    if a.publish_only:
        shots, a.publish = [], True     # skip the replay loop, go straight to the copy
    sha = game.check_rom()
    bad = 0
    for s in shots:
        if s["category"] not in CATEGORIES:
            print("warning: %s: category %r not in %s" % (s["id"], s["category"], ", ".join(CATEGORIES)))
        if a.verify:
            with tempfile.TemporaryDirectory() as t:
                r = shoot_one(game, s, t, model)
                old = os.path.join(d, s["id"] + ".png")
                same = os.path.exists(old) and _pixels(old) == _pixels(os.path.join(t, s["id"] + ".png"))
                if same and isinstance(r, dict):
                    g = os.path.join(d, s["id"] + ".gif")
                    same = os.path.exists(g) and _gif_frames(g) == _gif_frames(os.path.join(t, s["id"] + ".gif"))
                if not same:
                    shutil.copyfile(os.path.join(t, s["id"] + ".png"), os.path.join(d, s["id"] + ".replay.png"))
                    bad += 1
                print("%-24s %s" % (s["id"], "ok" if same else "MISMATCH (see %s.replay.png)" % s["id"]), flush=True)
            continue
        r = shoot_one(game, s, d, model)
        entry = {"id": s["id"], "category": s["category"], "caption": s["caption"], "route": s["route"],
                 "settled": r if isinstance(r, bool) else False, "model": model, "source": "shoot.py"}
        if isinstance(r, dict):
            entry["clip"] = r
        index_update(game, d, entry, sha)
        print("%-24s %s" % (s["id"], "clip %d frames" % r["kept"] if isinstance(r, dict) else
                                     "settled" if r else "NOT settled (animated?)"), flush=True)
    if a.verify:
        print("%d/%d reproduce" % (len(shots) - bad, len(shots)))
        return 3 if bad else 0
    print("set: %s" % os.path.relpath(d, ROOT))
    if a.publish:
        pub = os.path.join(game.dir, "shots", a.set)
        os.makedirs(pub, exist_ok=True)
        idx = json.load(open(os.path.join(d, "index.json"), encoding="utf-8"))
        for s in idx["shots"]:
            for f in (s["file"], s["file_3x"]) + ((s["clip"]["file"], s["clip"]["file_3x"]) if s.get("clip") else ()):
                shutil.copyfile(os.path.join(d, f), os.path.join(pub, f))
        for f in ("index.json", "index.md", "sheet.png", "shots.txt", "strip.png", "steps.gif", "steps@3x.gif"):
            if os.path.exists(os.path.join(d, f)):
                shutil.copyfile(os.path.join(d, f), os.path.join(pub, f))
        print("published: %s (%d shots)" % (os.path.relpath(pub, ROOT), len(idx["shots"])))
    return 0


def _pixels(path):
    from PIL import Image
    return Image.open(path).convert("RGB").tobytes()


if __name__ == "__main__":
    sys.exit(main())
