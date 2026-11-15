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
  (a passing full --verify also rebuilds index.md, sheet.png and a sequence's strip/steps from index.json)
  python3 tools/shoot.py GAME SET --model dmg       capture with another model (e.g. a DMG game also in CGB colours)

Shot list lines: `id | category | caption | route` (route: tools/emu.py tokens; may start with @checkpoint).
A route is played exactly, then `settle` is added unless it already ends with `settle` or `!`.
Outputs per shot: <id>.png (native, framebuffer as is: no filter, no colour correction, no scaling),
<id>@3x.png (nearest neighbour). Per set: index.json, index.md, sheet.png (all shots, captioned).
Clips: a route ending in `rec:N[:K[:P]]` records N frames (every Kth kept) from the end of the route: <id>.gif and
<id>@3x.gif at game speed, <id>.png / @3x = the poster (kept frame P, default the first). --verify compares every clip frame.
Sequences: a set named `seq-<action>` is an ordered action (shots in list order = steps): it also gets
strip.png (the steps left to right, numbered and captioned), steps.gif / steps@3x.gif (one still per 1.5 s) and
full.gif / full@3x.gif (all steps stitched in order: stills held 1.5 s, clips played in full at game speed).
"""
import argparse, datetime, hashlib, json, os, shutil, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
sys.path.insert(0, HERE)
import emu as E  # noqa: E402

# Database categories (docs/capture-guide.md). Others are allowed but warned about.
CATEGORIES = ["boot", "title", "menu", "options", "cutscene", "gameplay", "hud", "system", "map", "inventory",
              "dialogue", "shop", "battle", "boss", "minigame", "ending", "credits", "gameover", "save", "extra"]


def prefix(set_name):
    """File-name prefix of a set: sequence sets name every media file after the set (seq-fishing_01_shore.png,
    seq-fishing_full.gif) so files keep their context outside the folder; other sets: none."""
    return set_name + "_" if set_name.startswith("seq-") else ""


def index_update(game, d, entry, rom_sha1=None):
    """Insert/replace one shot in d/index.json and rewrite index.md and sheet.png."""
    p = os.path.join(d, "index.json")
    idx = json.load(open(p, encoding="utf-8")) if os.path.exists(p) else {}
    m = game.meta
    idx["game"] = {k: m.get(k) for k in ("slug", "title", "platform", "model", "sha1", "crc32")}
    idx["set"] = os.path.basename(d)
    shots = {s["id"]: s for s in idx.get("shots", [])}
    entry = dict(entry)
    pfx = prefix(os.path.basename(d))
    entry.setdefault("file", pfx + entry["id"] + ".png")
    entry.setdefault("file_3x", pfx + entry["id"] + "@3x.png")
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
            os.path.join(d, pfx + "sheet.png"), cols=5, labels=[s["id"] for s in idx["shots"]
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
    pfx = prefix(os.path.basename(d))
    st.save(os.path.join(d, pfx + "strip.png"))
    paths = [os.path.join(d, s["file"]) for s in shots]
    E.write_gif(paths, os.path.join(d, pfx + "steps.gif"), hold_ms=1500)
    E.write_gif(paths, os.path.join(d, pfx + "steps@3x.gif"), scale=3, hold_ms=1500)
    full_gif(shots, d)


STILL_MS, FIRST_MS, LAST_MS = 1500, 2000, 3000   # stitched GIF: how long stills stay; the first/last a bit longer


def full_gif(shots, d):
    """full.gif / full@3x.gif: every step stitched in order - stills held STILL_MS, clips played in full at
    game speed (their own frames and delays)."""
    from PIL import Image, ImageSequence
    frames, durs = [], []
    for i, s in enumerate(shots):
        clip = s.get("clip")
        if clip and os.path.exists(os.path.join(d, clip["file"])):
            g = Image.open(os.path.join(d, clip["file"]))
            for f in ImageSequence.Iterator(g):
                frames.append(f.convert("RGB"))
                durs.append(f.info.get("duration", 33))
        else:
            frames.append(Image.open(os.path.join(d, s["file"])).convert("RGB"))
            durs.append(FIRST_MS if i == 0 else LAST_MS if i == len(shots) - 1 else STILL_MS)
    pfx = prefix(os.path.basename(d))
    E.write_gif(frames, os.path.join(d, pfx + "full.gif"), durations=durs)
    E.write_gif(frames, os.path.join(d, pfx + "full@3x.gif"), scale=3, durations=durs)


def write_md(idx, d):
    g = idx["game"]
    out = ["# %s - shots: %s" % (g["title"], idx["set"]), "",
           "Platform %s, model %s, ROM SHA-1 `%s`. %d shots. Contact sheet: [{p}sheet.png]({p}sheet.png).".format(p=prefix(idx["set"])) % (
               g["platform"], g["model"], g["sha1"], len(idx["shots"])), "",
           "| id | category | caption | settled | image |", "|---|---|---|---|---|"]
    for s in idx["shots"]:
        clip = " [gif](%s) [gif 3x](%s)" % (s["clip"]["file"], s["clip"]["file_3x"]) if s.get("clip") else ""
        out.append("| %s | %s | %s | %s | [png](%s) [3x](%s)%s |" % (
            s["id"], s["category"], s.get("caption", ""), "yes" if s.get("settled") else "clip" if clip else "no",
            s["file"], s["file_3x"], clip))
    if idx["set"].startswith("seq-"):
        out += ["", ("Sequence: [{p}full.gif]({p}full.gif) ([3x]({p}full@3x.gif)) = all steps stitched (stills "
                     "held, clips played), [{p}strip.png]({p}strip.png), [{p}steps.gif]({p}steps.gif) "
                     "([3x]({p}steps@3x.gif)) = stills only.").format(p=prefix(idx["set"]))]
    out += ["", "Routes (replay with `tools/shoot.py`) are in `index.json` and `shots.txt`.", ""]
    open(os.path.join(d, "index.md"), "w", encoding="utf-8").write("\n".join(out))


def shoot_one(game, s, d, model, pfx=""):
    """Replay one shot (or clip). Returns settled (bool) for stills, the clip dict for clips."""
    route = s["route"]
    toks = E.split(route)
    rec = E.rec_token(toks[-1]) if toks else None
    if rec:
        e, rest, _ = E.start(game, ",".join(toks[:-1]), model)
        E.play(e, game, rest)
        n, every, poster = rec
        clip = clip_files(game, e, pfx + s["id"], d, n, every, poster, close=True)
        clip.pop("_frames")
        return clip
    if not toks or toks[-1] not in ("settle", "!"):
        route += ",settle"
    e, rest, _ = E.start(game, route, model)
    E.play(e, game, rest)
    native = os.path.join(d, pfx + s["id"] + ".png")
    e.screen_png(native)
    a = e.screen()
    e.frames(game.settle_step)
    settled = a == e.screen()
    e.close()
    E.enlarge(native, os.path.join(d, pfx + s["id"] + "@3x.png"))
    return settled


def clip_files(game, e, sid, d, n, every, poster=0, close=False):
    """Record a clip from the emulator's current state into d: <id>.gif, <id>@3x.gif, poster <id>.png/@3x
    (kept frame number `poster`; 0 = first, -1 = last)."""
    frames = E.record(e, game, n, every)
    if close:
        e.close()
    E.write_gif(frames, os.path.join(d, sid + ".gif"), every)
    E.write_gif(frames, os.path.join(d, sid + "@3x.gif"), every, scale=3)
    open(os.path.join(d, sid + ".png"), "wb").write(frames[poster])
    E.enlarge(os.path.join(d, sid + ".png"), os.path.join(d, sid + "@3x.png"))
    return {"frames": n, "every": every, "kept": len(frames), "poster": poster, "seconds": round(n / E.FPS, 2),
            "file": sid + ".gif", "file_3x": sid + "@3x.gif", "_frames": frames}


def _gif_frames(path):
    from PIL import Image, ImageSequence
    return [f.convert("RGB").tobytes() for f in ImageSequence.Iterator(Image.open(path))]


def check_category(cat):
    if cat not in CATEGORIES:
        return "error: category %r unknown; use one of %s (a clip takes the category of what it shows)" % (
            cat, ", ".join(CATEGORIES))
    return None


def reindex(game, d):
    """Rebuild index.md, sheet.png and (seq-*) strip/steps GIFs from index.json (after hand edits)."""
    p = os.path.join(d, "index.json")
    if not os.path.exists(p):
        return
    idx = json.load(open(p, encoding="utf-8"))
    write_md(idx, d)
    if os.path.basename(d).startswith("seq-"):
        sequence_files(idx, d)
    have = [s for s in idx["shots"] if os.path.exists(os.path.join(d, s["file"]))]
    E.sheet([os.path.join(d, s["file"]) for s in have], os.path.join(d, prefix(os.path.basename(d)) + "sheet.png"), cols=5,
            labels=[s["id"] for s in have])


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
    pfx = prefix(a.set)
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
                r = shoot_one(game, s, t, model, pfx)
                stem = pfx + s["id"]
                old = os.path.join(d, stem + ".png")
                same = os.path.exists(old) and _pixels(old) == _pixels(os.path.join(t, stem + ".png"))
                if same and isinstance(r, dict):
                    g = os.path.join(d, stem + ".gif")
                    same = os.path.exists(g) and _gif_frames(g) == _gif_frames(os.path.join(t, stem + ".gif"))
                if not same:
                    shutil.copyfile(os.path.join(t, stem + ".png"), os.path.join(d, stem + ".replay.png"))
                    bad += 1
                print("%-24s %s" % (s["id"], "ok" if same else "MISMATCH (see %s.replay.png)" % s["id"]), flush=True)
            continue
        r = shoot_one(game, s, d, model, pfx)
        entry = {"id": s["id"], "category": s["category"], "caption": s["caption"], "route": s["route"],
                 "settled": r if isinstance(r, bool) else False, "model": model, "source": "shoot.py"}
        if isinstance(r, dict):
            entry["clip"] = r
        index_update(game, d, entry, sha)
        print("%-24s %s" % (s["id"], "clip %d frames" % r["kept"] if isinstance(r, dict) else
                                     "settled" if r else "NOT settled (animated?)"), flush=True)
    if a.verify:
        print("%d/%d reproduce" % (len(shots) - bad, len(shots)))
        if not bad and not a.only:
            reindex(game, d)        # pick up hand edits of captions/categories in index.json
        return 3 if bad else 0
    print("set: %s" % os.path.relpath(d, ROOT))
    if a.publish:
        if a.set.startswith("seq-"):
            reindex(game, d)            # strip, steps and the stitched full GIF from the current files
        pub = os.path.join(game.dir, "shots", a.set)
        os.makedirs(pub, exist_ok=True)
        idx = json.load(open(os.path.join(d, "index.json"), encoding="utf-8"))
        for s in idx["shots"]:
            for f in (s["file"], s["file_3x"]) + ((s["clip"]["file"], s["clip"]["file_3x"]) if s.get("clip") else ()):
                shutil.copyfile(os.path.join(d, f), os.path.join(pub, f))
        for f in ["index.json", "index.md", "shots.txt"] + [pfx + f for f in (
                "sheet.png", "strip.png", "steps.gif", "steps@3x.gif", "full.gif", "full@3x.gif")]:
            if os.path.exists(os.path.join(d, f)):
                shutil.copyfile(os.path.join(d, f), os.path.join(pub, f))
        print("published: %s (%d shots)" % (os.path.relpath(pub, ROOT), len(idx["shots"])))
    return 0


def _pixels(path):
    from PIL import Image
    return Image.open(path).convert("RGB").tobytes()


if __name__ == "__main__":
    sys.exit(main())
