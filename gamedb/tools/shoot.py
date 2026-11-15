"""Replay a shot list and build the database set: pixel-exact PNGs, @3x copies, catalogue, contact sheet.

  python3 tools/shoot.py GAME [SET]                 replay work/shots/GAME/SET/shots.txt (default set: main;
                                                    falls back to the plan games/GAME/shots.txt)
  python3 tools/shoot.py GAME SET --list FILE       another shot list
  python3 tools/shoot.py GAME SET --only id,id      only these ids (merged into the existing index)
  python3 tools/shoot.py GAME SET --verify          replay into a temp dir and compare with the PNGs already in
                                                    the set (e.g. made with play.py snap): proves every route
                                                    reproduces its frame; exit 3 on a mismatch
  python3 tools/shoot.py GAME SET --publish         copy the set to games/GAME/shots/SET/ (committed)
  python3 tools/shoot.py GAME SET --model dmg       capture with another model (e.g. a DMG game also in CGB colours)

Shot list lines: `id | category | caption | route` (route: tools/emu.py tokens; may start with @checkpoint).
A route is played exactly, then `settle` is added unless it already ends with `settle` or `!`.
Outputs per shot: <id>.png (native, framebuffer as is: no filter, no colour correction, no scaling),
<id>@3x.png (nearest neighbour). Per set: index.json, index.md, sheet.png (all shots, captioned).
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
    E.sheet([os.path.join(d, s["file"]) for s in idx["shots"] if os.path.exists(os.path.join(d, s["file"]))],
            os.path.join(d, "sheet.png"), cols=5, labels=[s["id"] for s in idx["shots"]
                                                          if os.path.exists(os.path.join(d, s["file"]))])


def write_md(idx, d):
    g = idx["game"]
    out = ["# %s - shots: %s" % (g["title"], idx["set"]), "",
           "Platform %s, model %s, ROM SHA-1 `%s`. %d shots. Contact sheet: [sheet.png](sheet.png)." % (
               g["platform"], g["model"], g["sha1"], len(idx["shots"])), "",
           "| id | category | caption | settled | image |", "|---|---|---|---|---|"]
    for s in idx["shots"]:
        out.append("| %s | %s | %s | %s | [png](%s) [3x](%s) |" % (
            s["id"], s["category"], s.get("caption", ""), "yes" if s.get("settled") else "no", s["file"],
            s["file_3x"]))
    out += ["", "Routes (replay with `tools/shoot.py`) are in `index.json` and `shots.txt`.", ""]
    open(os.path.join(d, "index.md"), "w", encoding="utf-8").write("\n".join(out))


def shoot_one(game, s, d, model):
    route = s["route"]
    toks = E.split(route)
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


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("game")
    ap.add_argument("set", nargs="?", default="main")
    ap.add_argument("--list")
    ap.add_argument("--only")
    ap.add_argument("--verify", action="store_true")
    ap.add_argument("--publish", action="store_true")
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
    sha = game.check_rom()
    bad = 0
    for s in shots:
        if s["category"] not in CATEGORIES:
            print("warning: %s: category %r not in %s" % (s["id"], s["category"], ", ".join(CATEGORIES)))
        if a.verify:
            with tempfile.TemporaryDirectory() as t:
                shoot_one(game, s, t, model)
                old = os.path.join(d, s["id"] + ".png")
                same = os.path.exists(old) and _pixels(old) == _pixels(os.path.join(t, s["id"] + ".png"))
                if not same:
                    shutil.copyfile(os.path.join(t, s["id"] + ".png"), os.path.join(d, s["id"] + ".replay.png"))
                    bad += 1
                print("%-24s %s" % (s["id"], "ok" if same else "MISMATCH (see %s.replay.png)" % s["id"]), flush=True)
            continue
        settled = shoot_one(game, s, d, model)
        index_update(game, d, {"id": s["id"], "category": s["category"], "caption": s["caption"],
                               "route": s["route"], "settled": settled, "model": model,
                               "source": "shoot.py"}, sha)
        print("%-24s %s" % (s["id"], "settled" if settled else "NOT settled (animated?)"), flush=True)
    if a.verify:
        print("%d/%d reproduce" % (len(shots) - bad, len(shots)))
        return 3 if bad else 0
    print("set: %s" % os.path.relpath(d, ROOT))
    if a.publish:
        pub = os.path.join(game.dir, "shots", a.set)
        os.makedirs(pub, exist_ok=True)
        idx = json.load(open(os.path.join(d, "index.json"), encoding="utf-8"))
        for s in idx["shots"]:
            for f in (s["file"], s["file_3x"]):
                shutil.copyfile(os.path.join(d, f), os.path.join(pub, f))
        for f in ("index.json", "index.md", "sheet.png", "shots.txt"):
            if os.path.exists(os.path.join(d, f)):
                shutil.copyfile(os.path.join(d, f), os.path.join(pub, f))
        print("published: %s (%d shots)" % (os.path.relpath(pub, ROOT), len(idx["shots"])))
    return 0


def _pixels(path):
    from PIL import Image
    return Image.open(path).convert("RGB").tobytes()


if __name__ == "__main__":
    sys.exit(main())
