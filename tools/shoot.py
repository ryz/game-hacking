"""Replay a shot list and build the database set: pixel-exact PNGs, catalogue, contact sheet.

  python3 tools/shoot.py GAME [SET]                 replay work/shots/PLATFORM/GAME/SET/shots.txt (default set: main;
                                                    falls back to the published games/PLATFORM/GAME/shots/SET/shots.txt,
                                                    for main also to the plan games/PLATFORM/GAME/shots.txt)
  python3 tools/shoot.py GAME SET --list FILE       another shot list
  python3 tools/shoot.py GAME SET --only id,id      only these ids (merged into the existing index); lists the
                                                    new shots whose picture another shot of the set already has
  python3 tools/shoot.py GAME SET --jobs N          shots are replayed in N processes (default: 4, or the CPU
                                                    count if lower; 1 = in this process). Checkpoints are built once
                                                    and shared (tools/emu.py), also from an empty cache
  python3 tools/shoot.py GAME SET --verify          replay into a temp dir and compare with the PNGs already in
                                                    the set (e.g. made with play.py snap): proves every route
                                                    reproduces its frame; exit 3 on a mismatch
  python3 tools/shoot.py GAME SET --publish         replay the set, then copy it to games/PLATFORM/GAME/shots/SET/ (committed)
  python3 tools/shoot.py GAME SET --publish-only    copy without replaying (right after a passing --verify)
  (a passing full --verify also rebuilds index.md, sheet.png and a sequence's strip/steps from index.json)
  python3 tools/shoot.py GAME SET --prune           drop shots the work set's shots.txt no longer lists (after
                                                    deleting a line or renaming an id by hand): entries and files
Checks a replay cannot make (--verify lists them, --publish refuses identical pictures, exit 4, unless
--allow-duplicates): still shots with identical pixels (not in seq-* sets), captions over 80 characters. After publishing `main` the
three design lenses are checked (tools/lenses.py). Contact sheets hold 100 shots: sheet.png, sheet2.png ...
  python3 tools/shoot.py GAME SET --model dmg       capture with another model (e.g. a DMG game also in CGB colours)

Shot list lines: `id | category | caption | route` (route: tools/emu.py tokens; may start with @checkpoint).
A route is played exactly, then `settle` is added unless it already ends with `settle` or `!`.
File names say what a file shows without its folder (docs/capture-guide.md, "File names"):
  <game>_<platform>_<region>_<area>_<id>[.<set>].png      might-and-magic_nes_na_battle_battle_sprites.png
game, platform, region = game.json "slug", "platform", "region"; area = the shot's category; id = the shot id (in
a `seq-<action>` set: `seq-<action>_<id>`); `.<set>` for every set but `main` and `seq-*`. Set `start`: ids are
`NN_<step>` in play order and the number goes before the area: <game>_<platform>_<region>_<NN>_<area>_<step>.start.png.
Below, NAME is that name.
Outputs per shot: NAME.png (native, framebuffer as is: no filter, no colour correction, no scaling). Enlarged
copies are made on demand, never by default: python3 tools/x3.py FOLDER|FILE ... Per set: index.json, index.md and the contact
sheet <game>_<platform>_<region>_set_sheet[.<set>].png (all shots, captioned; `set` in the area field = a file about the whole set).
Clips: a route ending in `rec:N[:K[:P]]` records N frames (every Kth kept) from the end of the route: NAME.gif
at game speed, NAME.png = the poster (kept frame P, default the first). --verify compares every clip frame.
Sequences: a set named `seq-<action>` is an ordered action (shots in list order = steps): it also gets
..._set_seq-<action>_strip.png (the steps left to right, numbered and captioned), ..._steps.gif (one still
per 1.5 s) and ..._full.gif (all steps stitched in order: stills held 1.5 s, clips played in full at game speed).
The order of a set is the order of its own shots.txt (edit the list, then --verify or --publish-only).
A set made before a change of the scheme, of a category or of game.json is renamed to it on the next run.
"""
import argparse, datetime, hashlib, json, os, re, shutil, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
sys.path.insert(0, HERE)
import emu as E  # noqa: E402

# Database categories (docs/capture-guide.md). Others are allowed but warned about.
CATEGORIES = ["boot", "title", "menu", "options", "cutscene", "gameplay", "hud", "system", "map", "inventory",
              "dialogue", "shop", "battle", "boss", "minigame", "ending", "credits", "gameover", "save", "extra"]


REGIONS = ["jp", "na", "eu"]     # game.json "region": where the registered dump was released (not its language)
SHEET_PAGE = 100                 # shots per contact sheet; a bigger set gets sheet2.png, sheet3.png ...
SET_FILES = ("sheet.png", "strip.png", "steps.gif", "full.gif") + tuple(     # files about a whole set (area `set`)
    "sheet%d.png" % n for n in range(2, 21))
CAPTION_MAX = 80                 # docs/capture-guide.md, Quality rules
LIST = ("id", "category", "caption", "route")


def prefix(set_name):
    """Sequence sets put the set name in front of every id (seq-fishing_01_shore): the steps are one action."""
    return set_name + "_" if set_name.startswith("seq-") else ""


def suffix(set_name):
    """`.<set>` for sets that share ids with the main set (compare-maze); none for main and seq-* sets."""
    return "" if set_name == "main" or set_name.startswith("seq-") else "." + set_name


def head(g, set_name):
    """<game>_<platform>_<region> from game.json (or the "game" block of an index.json). No field holds a `_`."""
    if g.get("region") not in REGIONS:
        raise SystemExit("games/%s/%s/game.json needs \"region\": one of %s (where the dump was released; "
                         "a translated Japanese ROM is jp)" % (g["platform"], g["slug"], ", ".join(REGIONS)))
    for what, v in (("slug", g["slug"]), ("platform", g["platform"]), ("set name", set_name)):
        if not re.match(r"^[a-z0-9]+(-[a-z0-9]+)*$", v):
            raise SystemExit("error: %s %r must be lowercase a-z0-9 words joined by `-` (it is part of the "
                             "shot file names)" % (what, v))
    return "%s_%s_%s" % (g["slug"], g["platform"], g["region"])


def stem(g, set_name, category, sid):
    """File name of a shot without the extension: <game>_<platform>_<region>_<area>_<id>[.<set>].
    Set `start` (played in order): ids are `NN_<step>` and the step number goes before the area, so a folder
    listing is the play order: <game>_<platform>_<region>_<NN>_<area>_<step>.start."""
    if not re.match(r"^[a-z]+$", category) or category == "set":
        raise SystemExit("error: %s: category %r must be one lowercase word, not `set` (it is the area field of "
                         "the file name)" % (sid, category))
    if set_name == "start":
        m = re.match(r"^(\d{2,3})_(.+)$", sid)
        if not m:
            raise SystemExit("error: %s: ids in the set `start` are numbered in play order: 01_<step>, 02_<step> "
                             "... (docs/capture-guide.md, \"Sets\")" % sid)
        return "%s_%s_%s_%s%s" % (head(g, set_name), m.group(1), category, m.group(2), suffix(set_name))
    return "%s_%s_%s%s%s" % (head(g, set_name), category, prefix(set_name), sid, suffix(set_name))


def set_file(g, set_name, name):
    """File name of a file about the whole set (name: sheet.png, strip.png, steps.gif, full.gif)."""
    base, ext = os.path.splitext(name)
    return "%s_set_%s%s%s%s" % (head(g, set_name), prefix(set_name), base, suffix(set_name), ext)


def game_block(game):
    return {k: game.meta.get(k) for k in ("slug", "title", "platform", "region", "model", "sha1", "crc32")}


def files_of(s):
    """Every file of an index entry, relative to the set folder."""
    return ([s["file"]] if s.get("file") else []) + (
        [s["clip"]["file"]] if s.get("clip") and s["clip"].get("file") else [])


def name_entry(g, set_name, s):
    """Set the file names of an index entry to the scheme. Returns [(old, new)] for the names that changed."""
    st = stem(g, set_name, s["category"], s["id"])
    old = files_of(s)
    s["file"] = st + ".png"
    s.pop("file_3x", None)          # sets made before 2026-11-20 listed a 3x copy per shot (now on demand: x3.py)
    if s.get("clip"):
        s["clip"]["file"] = st + ".gif"
        s["clip"].pop("file_3x", None)
    return [(o, n) for o, n in zip(old, files_of(s)) if o != n] if len(old) == len(files_of(s)) else []


def normalize(game, d, move=os.replace):
    """Rename the files of the set in folder d to the scheme and write its index.json: sets made before the scheme,
    a category changed by hand in index.json, a region or slug changed in game.json. Returns the number of renames."""
    p = os.path.join(d, "index.json")
    if not os.path.exists(p):
        return 0
    idx = json.load(open(p, encoding="utf-8"))
    set_name, g = os.path.basename(d), game_block(game)
    had_3x = any("file_3x" in x for s in idx.get("shots", []) for x in (s, s.get("clip") or {}))
    moves = [m for s in idx.get("shots", []) for m in name_entry(g, set_name, s)]
    known = {f for s in idx.get("shots", []) for f in files_of(s)}
    for f in SET_FILES:
        new = set_file(g, set_name, f)
        for f_old in os.listdir(d):
            # an older name of the same set file: sheet.png, seq-x_sheet.png, <other head>_set_...sheet.png
            if f_old != new and f_old not in known and (
                    f_old == prefix(set_name) + f or f_old.endswith("_set_" + new.split("_set_", 1)[1])):
                moves.append((f_old, new))
    n = 0
    for o, new in moves:
        if os.path.exists(os.path.join(d, o)):
            move(os.path.join(d, o), os.path.join(d, new))
            n += 1
    if n or had_3x or idx.get("game") != g:
        idx["game"] = g
        json.dump(idx, open(p, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
        write_md(idx, d)
    return n


def list_order(game, idx, d=None):
    """Sort idx["shots"] by the set's own shots.txt in folder d (the order the list is written in = game order);
    a set without a list of its own follows the game's shots.txt. Ids not in the list keep their place at the end."""
    lst = os.path.join(d, "shots.txt") if d else ""
    if not os.path.exists(lst):
        lst = os.path.join(game.dir, "shots.txt")
    if not os.path.exists(lst):
        return idx
    pos = {r["id"]: i for i, r in enumerate(E.read_table(lst, LIST))}
    shots = idx.get("shots", [])
    idx["shots"] = sorted(shots, key=lambda x: (x["id"] not in pos, pos.get(x["id"], 0), shots.index(x)))
    return idx


def index_update(game, d, entry, rom_sha1=None, finish=True):
    """Insert/replace one shot in d/index.json and rewrite index.md and sheet.png (finish=False: only
    index.json; a batch calls reindex() once at its end instead of drawing the sheets after every shot)."""
    p = os.path.join(d, "index.json")
    idx = json.load(open(p, encoding="utf-8")) if os.path.exists(p) else {}
    m = game.meta
    idx["game"] = game_block(game)
    idx["set"] = os.path.basename(d)
    shots = {s["id"]: s for s in idx.get("shots", [])}
    entry = dict(entry)
    name_entry(idx["game"], idx["set"], entry)
    for f in set(files_of(shots.get(entry["id"], {}))) - set(files_of(entry)):
        if os.path.exists(os.path.join(d, f)):      # the id had another category (or no clip) before
            os.remove(os.path.join(d, f))
    entry["rom_sha1"] = rom_sha1 or m.get("sha1")
    entry["captured"] = datetime.date.today().isoformat()
    if os.path.exists(os.path.join(d, entry["file"])) and "clip" not in entry:
        entry["pixel_sha1"] = pixel_sha1(os.path.join(d, entry["file"]))
    shots[entry["id"]] = entry
    order = [s["id"] for s in idx.get("shots", [])]
    if entry["id"] not in order:
        order.append(entry["id"])
    idx["shots"] = [shots[i] for i in order]
    list_order(game, idx, d)
    json.dump(idx, open(p, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    if not finish:
        return
    write_md(idx, d)
    if os.path.basename(d).startswith("seq-"):
        sequence_files(idx, d)
    sheets(idx, d)


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
    name = lambda f: os.path.join(d, set_file(idx["game"], idx["set"], f))  # noqa: E731
    st.save(name("strip.png"))
    paths = [os.path.join(d, s["file"]) for s in shots]
    E.write_gif(paths, name("steps.gif"), hold_ms=1500)
    full_gif(shots, d, name("full.gif"))


STILL_MS, FIRST_MS, LAST_MS = 1500, 2000, 3000   # stitched GIF: how long stills stay; the first/last a bit longer


def full_gif(shots, d, out):
    """full.gif: every step stitched in order - stills held STILL_MS, clips played in full at
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
    E.write_gif(frames, out, durations=durs)


def write_md(idx, d):
    g = idx["game"]
    sf = lambda f: set_file(g, idx["set"], f)  # noqa: E731
    out = ["# %s - shots: %s" % (g["title"], idx["set"]), "",
           "Platform %s, region %s, model %s, ROM SHA-1 `%s`. %d shots. Contact sheet: [%s](%s). Native "
           "size; enlarged copies on demand with `python3 tools/x3.py <this folder>`. File names: "
           "`<game>_<platform>_<region>_%s%s.png`." % (
               g["platform"], g["region"], g["model"], g["sha1"], len(idx["shots"]), sf("sheet.png"),
               sf("sheet.png"), "<NN>_<category>_<step>" if idx["set"] == "start" else "<category>_<id>",
               suffix(idx["set"])), "",
           "| id | category | caption | settled | image |", "|---|---|---|---|---|"]
    for s in idx["shots"]:
        clip = " [gif](%s)" % s["clip"]["file"] if s.get("clip") else ""
        out.append("| %s | %s | %s | %s | [png](%s)%s |" % (
            s["id"], s["category"], s.get("caption", ""), "yes" if s.get("settled") else "clip" if clip else "no",
            s["file"], clip))
    if idx["set"].startswith("seq-"):
        out += ["", ("Sequence: [{f}]({f}) = all steps stitched (stills held, clips played), "
                     "[{s}]({s}), [{g}]({g}) = stills only.").format(
                         f=sf("full.gif"), s=sf("strip.png"), g=sf("steps.gif"))]
    out += ["", "Routes (replay with `tools/shoot.py`) are in `index.json` and `shots.txt`.", ""]
    open(os.path.join(d, "index.md"), "w", encoding="utf-8").write("\n".join(out))


def shoot_one(game, s, d, model, set_name="main"):
    """Replay one shot (or clip) into d. Returns settled (bool) for stills, the clip dict for clips."""
    st = stem(game.meta, set_name, s["category"], s["id"])
    route = s["route"]
    toks = E.split(route)
    rec = E.rec_token(toks[-1]) if toks else None
    if rec:
        e, rest, _ = E.start(game, ",".join(toks[:-1]), model)
        E.play(e, game, rest)
        n, every, poster = rec
        clip = clip_files(game, e, st, d, n, every, poster, close=True)
        clip.pop("_frames")
        return clip
    if not toks or toks[-1] not in ("settle", "!"):
        route += ",settle"
    e, rest, _ = E.start(game, route, model)
    E.play(e, game, rest)
    native = os.path.join(d, st + ".png")
    e.screen_png(native)
    a = e.screen()
    e.frames(game.settle_step)
    settled = a == e.screen()
    e.close()
    return settled


def clip_files(game, e, sid, d, n, every, poster=0, close=False):
    """Record a clip from the emulator's current state into d: NAME.gif and the poster NAME.png
    (sid = NAME, see stem(); kept frame number `poster`; 0 = first, -1 = last)."""
    frames = E.record(e, game, n, every)
    if close:
        e.close()
    E.write_gif(frames, os.path.join(d, sid + ".gif"), every)
    open(os.path.join(d, sid + ".png"), "wb").write(frames[poster])
    return {"frames": n, "every": every, "kept": len(frames), "poster": poster, "seconds": round(n / E.FPS, 2),
            "file": sid + ".gif", "_frames": frames}


def _gif_frames(path):
    from PIL import Image, ImageSequence
    return [f.convert("RGB").tobytes() for f in ImageSequence.Iterator(Image.open(path))]


def check_category(cat):
    if cat not in CATEGORIES:
        return "error: category %r unknown; use one of %s (a clip takes the category of what it shows)" % (
            cat, ", ".join(CATEGORIES))
    return None


def sheets(idx, d):
    """Contact sheet(s) of the set: sheet.png holds the first SHEET_PAGE shots, sheet2.png the next ... (a
    sheet of several hundred shots is too tall to look at). Pages no longer needed are deleted."""
    have = [s for s in idx["shots"] if os.path.exists(os.path.join(d, s["file"]))]
    pages = [have[i:i + SHEET_PAGE] for i in range(0, len(have), SHEET_PAGE)] or [[]]
    for n in range(1, 21):
        out = os.path.join(d, set_file(idx["game"], idx["set"], "sheet.png" if n == 1 else "sheet%d.png" % n))
        if n <= len(pages) and pages[n - 1]:
            E.sheet([os.path.join(d, s["file"]) for s in pages[n - 1]], out, cols=5,
                    labels=[s["id"] for s in pages[n - 1]])
        elif n > 1 and os.path.exists(out):
            os.remove(out)


def quality(idx, d):
    """Problems a replay cannot see (docs/capture-guide.md, Quality rules): shots with identical pixels, and
    captions over CAPTION_MAX characters. Returns (duplicate groups, long captions) as lists of text lines."""
    dup = ["identical pictures: " + ", ".join(ids) for ids in same_pictures(idx, d)]
    long_ = ["caption has %d characters (limit %d): %s" % (len(s["caption"]), CAPTION_MAX, s["id"])
             for s in idx["shots"] if len(s["caption"]) > CAPTION_MAX]
    return dup, long_


def pixel_sha1(path):
    return hashlib.sha1(_pixels(path)).hexdigest()


def same_pictures(idx, d, fresh=False):
    """Groups of shot ids whose stills have identical pixels. A sequence repeats frames on purpose (a clip's
    poster is the step before or after it), so seq-* sets and clips are left out. The hash kept in index.json
    ("pixel_sha1", written when a shot is made) is used unless fresh=True (hand-replaced files)."""
    if str(idx.get("set", "")).startswith("seq-"):
        return []
    same = {}
    for s in idx["shots"]:
        p = os.path.join(d, s["file"])
        if os.path.exists(p) and "clip" not in s:
            h = s.get("pixel_sha1") if not fresh else None
            same.setdefault(h or pixel_sha1(p), []).append(s["id"])
    return [ids for ids in same.values() if len(ids) > 1]


def twins(d, sid):
    """Other shots of the working set in folder d with the same picture as shot sid (play.py snap, --only)."""
    p = os.path.join(d, "index.json")
    if not os.path.exists(p):
        return []
    return [i for ids in same_pictures(json.load(open(p, encoding="utf-8")), d) if sid in ids for i in ids if i != sid]


def prune(game, d):
    """Drop shots from the working set that its shots.txt no longer lists (a line deleted or an id renamed by
    hand): index entry and files. Returns the ids removed."""
    p, lst = os.path.join(d, "index.json"), os.path.join(d, "shots.txt")
    if not (os.path.exists(p) and os.path.exists(lst)):
        return []
    listed = {r["id"] for r in E.read_table(lst, LIST)}
    idx = json.load(open(p, encoding="utf-8"))
    gone = [s for s in idx["shots"] if s["id"] not in listed]
    for s in gone:
        for f in files_of(s):
            if os.path.exists(os.path.join(d, f)):
                os.remove(os.path.join(d, f))
    if gone:
        idx["shots"] = [s for s in idx["shots"] if s["id"] in listed]
        json.dump(idx, open(p, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
        reindex(game, d)
    return [s["id"] for s in gone]


def reindex(game, d):
    """Rebuild index.md, sheet.png and (seq-*) strip/steps GIFs from index.json (after hand edits)."""
    p = os.path.join(d, "index.json")
    if not os.path.exists(p):
        return
    normalize(game, d)              # a category edited by hand changes the file name
    idx = json.load(open(p, encoding="utf-8"))
    list_order(game, idx, d)
    json.dump(idx, open(p, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    write_md(idx, d)
    if os.path.basename(d).startswith("seq-"):
        sequence_files(idx, d)
    sheets(idx, d)


def _job(job):
    """One shot in a worker process (--jobs): replay it into its folder, or for --verify into a temp folder and
    compare with the set. Returns (shot, result): settled / clip dict, or for --verify True / False."""
    game_id, s, d, model, set_name, verify = job
    game = E.Game(game_id)
    if not verify:
        return s, shoot_one(game, s, d, model, set_name)
    with tempfile.TemporaryDirectory() as t:
        r = shoot_one(game, s, t, model, set_name)
        st = stem(game.meta, set_name, s["category"], s["id"])
        old = os.path.join(d, st + ".png")
        same = os.path.exists(old) and _pixels(old) == _pixels(os.path.join(t, st + ".png"))
        if same and isinstance(r, dict):
            g = os.path.join(d, st + ".gif")
            same = os.path.exists(g) and _gif_frames(g) == _gif_frames(os.path.join(t, st + ".gif"))
        if not same:
            shutil.copyfile(os.path.join(t, st + ".png"), os.path.join(d, st + ".replay.png"))
        return s, same


def run_jobs(jobs, n):
    """Results of _job in list order. n > 1: n worker processes, each replaced after 25 shots so an emulator
    core that leaks cannot grow without bound; the checkpoint cache is shared and built once (emu._lock)."""
    if n <= 1 or len(jobs) <= 1:
        for j in jobs:
            yield _job(j)
        return
    import multiprocessing
    with multiprocessing.get_context("fork").Pool(min(n, len(jobs)), maxtasksperchild=25) as pool:
        for r in pool.imap(_job, jobs, chunksize=1):
            yield r


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("game")
    ap.add_argument("set", nargs="?", default="main")
    ap.add_argument("--list")
    ap.add_argument("--only")
    ap.add_argument("--verify", action="store_true")
    ap.add_argument("--publish", action="store_true")
    ap.add_argument("--publish-only", action="store_true",
                    help="copy the work set to games/PLATFORM/GAME/shots/SET/ without replaying (after a passing --verify)")
    ap.add_argument("--prune", action="store_true",
                    help="remove shots the work set's shots.txt no longer lists (index entries and files), then stop")
    ap.add_argument("--allow-duplicates", action="store_true",
                    help="publish although some shots have identical pixels (say why in the report)")
    ap.add_argument("--model")
    ap.add_argument("--jobs", type=int, default=min(4, os.cpu_count() or 1),
                    help="replay in this many processes (default: 4, or the CPU count if lower)")
    a = ap.parse_args()
    game = E.Game(a.game)
    model = a.model or game.model
    d = os.path.join(ROOT, "work", "shots", game.id, a.set)
    os.makedirs(d, exist_ok=True)
    head(game.meta, a.set)              # fails early when game.json has no region or the set name does not fit
    if normalize(game, d):
        print("renamed the working set to the current file names")
    if a.prune:
        gone = prune(game, d)
        print("pruned %d: %s" % (len(gone), " ".join(gone)) if gone else "nothing to prune")
        return 0
    lst = a.list or os.path.join(d, "shots.txt")
    if not os.path.exists(lst):         # a new container: the published set's own list, for main also the plan
        lst = os.path.join(game.dir, "shots", a.set, "shots.txt")
    if not os.path.exists(lst) and a.set == "main":
        lst = os.path.join(game.dir, "shots.txt")
    if not os.path.exists(lst):
        raise SystemExit("no shot list for set %r: %s (or --list FILE)" % (a.set, os.path.relpath(
            os.path.join(d, "shots.txt"), ROOT)))
    shots = E.read_table(lst, LIST)
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
        stem(game.meta, a.set, s["category"], s["id"])      # a bad category or id stops the run before it starts
    jobs = [(game.id, s, d, model, a.set, a.verify) for s in shots]
    for s, r in run_jobs(jobs, a.jobs):
        if a.verify:
            bad += not r
            print("%-24s %s" % (s["id"], "ok" if r else "MISMATCH (see %s.replay.png)" % stem(
                game.meta, a.set, s["category"], s["id"])), flush=True)
            continue
        entry = {"id": s["id"], "category": s["category"], "caption": s["caption"], "route": s["route"],
                 "settled": r if isinstance(r, bool) else False, "model": model, "source": "shoot.py"}
        if isinstance(r, dict):
            entry["clip"] = r
        index_update(game, d, entry, sha, finish=False)
        print("%-24s %s" % (s["id"], "clip %d frames" % r["kept"] if isinstance(r, dict) else
                                     "settled" if r else "NOT settled (animated?)"), flush=True)
    if shots and not a.verify:
        reindex(game, d)                # index.md, sheets, sequence files: once per batch, not once per shot
        if a.only:                      # a new shot that repeats a picture: say so now, not at the final verify
            idx = json.load(open(os.path.join(d, "index.json"), encoding="utf-8"))
            for ids in same_pictures(idx, d):
                if set(ids) & {s["id"] for s in shots}:
                    print("check: identical pictures: " + ", ".join(ids))
    if a.verify:
        print("%d/%d reproduce" % (len(shots) - bad, len(shots)))
        if not bad and not a.only:
            reindex(game, d)        # pick up hand edits of captions/categories in index.json
        if not a.only and os.path.exists(os.path.join(d, "index.json")):
            dup, long_ = quality(json.load(open(os.path.join(d, "index.json"), encoding="utf-8")), d)
            for line in dup + long_:
                print("check: " + line)
            if dup:
                print("check: %d group(s) of identical pictures: retake or drop before publishing" % len(dup))
        return 3 if bad else 0
    print("set: %s" % os.path.relpath(d, ROOT))
    if a.publish:
        reindex(game, d)                # game order from shots.txt; seq-: strip, steps, full GIF
        pub = os.path.join(game.dir, "shots", a.set)
        idx = json.load(open(os.path.join(d, "index.json"), encoding="utf-8"))
        dup, long_ = quality(idx, d)
        for line in dup + long_:
            print("check: " + line)
        if dup and not a.allow_duplicates:
            print("not published: %d group(s) of identical pictures (retake or drop one of each, or "
                  "--allow-duplicates)" % len(dup))
            return 4
        os.makedirs(pub, exist_ok=True)
        for s in idx["shots"]:
            for f in files_of(s):
                os.makedirs(os.path.dirname(os.path.join(pub, f)), exist_ok=True)
                shutil.copyfile(os.path.join(d, f), os.path.join(pub, f))
        keep = {set_file(idx["game"], a.set, f) for f in SET_FILES}
        for f in ["index.json", "index.md", "shots.txt"] + sorted(keep):
            if os.path.exists(os.path.join(d, f)):
                shutil.copyfile(os.path.join(d, f), os.path.join(pub, f))
        for s in idx["shots"]:
            keep |= set(files_of(s))
        for f in os.listdir(pub):       # images of shots no longer in the index (unsnapped, renamed)
            if f.endswith((".png", ".gif")) and f not in keep:
                os.remove(os.path.join(pub, f))
                print("removed stale %s" % f)
        print("published: %s (%d shots)" % (os.path.relpath(pub, ROOT), len(idx["shots"])))
        if a.set == "main":             # the three lenses index the published main set
            import lenses
            code, lines = lenses.check(game, a.set)
            print("lenses: " + ("\nlenses: ".join(lines[:12]) + ("\nlenses: ... %d more lines" % (len(lines) - 12)
                                                                  if len(lines) > 12 else "")))
    return 0


def _pixels(path):
    from PIL import Image
    return Image.open(path).convert("RGB").tobytes()


if __name__ == "__main__":
    sys.exit(main())
