"""Preview candidate routes before they become shots: many routes in parallel, one sheet (or the text screens).

  python3 tools/preview.py GAME FILE                  every line of FILE: `name | route`, or a shot list line
                                                      `id | category | caption | route` (# comments)
  python3 tools/preview.py GAME -r "name | route" -r "@town,up*3"     routes on the command line
  python3 tools/preview.py GAME FILE --only id,id     some lines of FILE
  python3 tools/preview.py GAME FILE --timeline 12:40 after each route 12 more frames, 40 frames apart (messages
                                                      that advance by themselves, battles, animations): frame
                                                      +k is the route `ROUTE,w40*k,!`, printed ready to copy
  python3 tools/preview.py GAME FILE --text           print the text screen of every frame instead of drawing
                                                      it (DOS text modes, Apple II text page): no picture to look at

Every route is played exactly as tools/shoot.py plays a shot (same checkpoint cache, final `settle` unless the
route ends with `settle` or `!`), so the frame shown is the frame the shot will have: write the lines of a
plan in shot-list format, preview them, fix what the sheet shows, then append the good lines to the working
set's shots.txt and run `shoot.py GAME SET --only id,id`. One call shows what would take one `play.py do`
and one look per route.
  ?                    token inside a route: take a frame here too (label `name ?1`, `?2`, ...); it is not part
                       of the route. Also after a token with a space: `a ?,w30 ?` = `a,?,w30,?`
  --timeline N[:STEP]  STEP defaults to 40 frames. The route is played without its final settle first.
  --peek ADDR:LEN      (LEN decimal or 0x..) print these bytes (hex) at every `?` mark, at every --timeline frame (`+K ADDR=..`) and after the last token of every route; several allowed
  --crop x0,y0,x1,y1   keep this part of every frame on the sheet (a message line, a status window)
  --scale N            enlarge the tiles (nearest neighbour); default 1 = native size
  --cols N             tiles per row (default 4); --page N tiles per sheet (default 24; then NAME_2.png ...)
  --set SET            also say when a frame is identical to a shot the working set SET already has
  --out NAME           name of the sheet (default: the file's name, or `routes`); a path gives its base name
  --jobs N             processes (default 4, or the CPU count if lower)
Output: work/preview/PLATFORM/GAME/NAME.png (labels above the tiles), every frame also at native size in
work/preview/PLATFORM/GAME/NAME/<label>.png. Per route one text line: its label(s), `settled` or not, the
--peek bytes, and `= other` when two frames of the batch are the same picture.
"""
import argparse, hashlib, io, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
sys.path.insert(0, HERE)
import emu as E  # noqa: E402


def read_lines(path):
    """[(name, route)] from a candidate file (`name | route`) or a shot list (`id | category | caption | route`)."""
    out = []
    for n, line in enumerate(sys.stdin if path == "-" else open(path, encoding="utf-8"), 1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = [x.strip() for x in line.split("|", 3)]
        if len(parts) == 1:
            parts = ["line%d" % n] + parts
        if len(parts) == 3:
            raise SystemExit("%s:%d: expected `name | route` or `id | category | caption | route`" % (path, n))
        out.append((parts[0], parts[-1]))
    return out


def run(job):
    """Play one route. Returns (name, [(label, png bytes, text lines or None)], info text, error or None)."""
    game_id, model, name, route, timeline, peeks, want_text = job
    try:
        game = E.Game(game_id)
        toks = []
        for t in E.split(route):                    # `X ?` = `X,?` (a mark glued to its token)
            m = re.match(r"^(.*\S)\s+\?$", t)
            toks += [m.group(1), "?"] if m else [t]
        rec = bool(toks) and E.rec_token(toks[-1]) is not None
        if rec:                                     # a clip: show the frame it starts on
            toks = toks[:-1]
        final = not timeline and not rec and not (toks and toks[-1] in ("settle", "!"))
        if timeline and toks and toks[-1] == "!":
            toks = toks[:-1]
        marks = [i for i, t in enumerate(toks) if t == "?"]
        emu, rest, _ = E.start(game, ",".join(t for t in toks if t != "?"), model)
        frames, info = [], []

        def grab(label):
            frames.append((label, emu.screen(), emu.text() if want_text and hasattr(emu, "text") else None))
        n_marks = sum(1 for t in E.expand(game, toks) if t == "?")
        if n_marks != len(marks):
            return name, [], "", "a `?` inside a macro is not supported"
        # positions of the marks among the expanded tokens: expand each stretch between marks on its own
        plan, k = [], 0
        stretch = []
        for t in toks:
            if t == "?":
                plan.append(("play", stretch)); stretch = []
                k += 1
                plan.append(("mark", k))
            else:
                stretch.append(t)
        plan.append(("play", stretch))
        first = True
        for kind, v in plan:
            if kind == "mark":
                grab("%s ?%d" % (name, v))
                for addr, n in peeks:       # values along the route, not only at its end
                    info.append("?%d %s=%s" % (v, addr, bytes(emu.peek(int(addr, 16), n)).hex()))
                continue
            seg = E.expand(game, v)
            if first and seg and seg[0].startswith("@"):
                seg = seg[1:]
            if first:
                seg = E.prefix(seg)[1]              # rom:/sav: acted at power-on
            first = False
            E.play(emu, game, seg)
        settled = None
        if final:
            E.play(emu, game, ["settle"])
        if timeline:
            n, step = timeline
            def at(k):
                grab("%s +%d" % (name, k))
                if peeks:
                    info.append("+%d %s" % (k, " ".join("%s=%s" % (addr, bytes(emu.peek(int(addr, 16), m)).hex())
                                                        for addr, m in peeks)))
            at(0)
            for i in range(1, n + 1):
                E.play(emu, game, ["w%d" % step])
                at(i * step)
            info.append("frame +K = %s,w%d*(K/%d),!" % (",".join(t for t in toks if t != "?"), step, step))
        else:
            a = emu.screen()
            grab(name)
            if not rec:
                emu.frames(game.settle_step)
                settled = a == emu.screen()
                info.append("settled" if settled else "NOT settled (animated?)")
        for addr, n in peeks:
            info.append("%s=%s" % (addr, bytes(emu.peek(int(addr, 16), n)).hex()))
        emu.close()
        return name, frames, "  ".join(info), None
    except BaseException as e:       # SystemExit from a missing ROM or save included: report it per route
        return name, [], "", "%s: %s" % (type(e).__name__, e)


def safe(label):
    return re.sub(r"[^\w.+-]", "_", label)


def draw(tiles, out, cols, page, scale, crop):
    """Sheets of `page` tiles with the label above each tile. Returns the paths written."""
    from PIL import Image, ImageDraw
    from collections import Counter
    ims = []
    for label, png, _ in tiles:
        im = Image.open(io.BytesIO(png)).convert("RGB")
        if crop:
            im = im.crop(crop)
        if scale > 1:
            im = im.resize((im.width * scale, im.height * scale), Image.NEAREST)
        ims.append((label, im))
    paths = []
    for p in range(0, len(ims), page):
        part = ims[p:p + page]
        w, h = Counter(im.size for _, im in part).most_common(1)[0][0]
        w = max(w, 96)
        c = min(cols, len(part))
        rows = (len(part) + c - 1) // c
        sheet = Image.new("RGB", (c * (w + 2), rows * (h + 14)), (40, 0, 0))
        dr = ImageDraw.Draw(sheet)
        for i, (label, im) in enumerate(part):
            if im.width > w or im.height > h:
                f = min(w / im.width, h / im.height)
                im = im.resize((max(1, int(im.width * f)), max(1, int(im.height * f))), Image.BOX)
            x, y = (i % c) * (w + 2), (i // c) * (h + 14)
            sheet.paste(im, (x, y + 13))
            dr.text((x + 2, y + 1), E.ascii_label(label)[:max(8, w // 6)], fill=(255, 255, 0))
        path = out + (".png" if p == 0 else "_%d.png" % (p // page + 1))
        sheet.save(path)
        paths.append(path)
    return paths


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("game")
    ap.add_argument("file", nargs="?")
    ap.add_argument("-r", "--route", action="append", default=[])
    ap.add_argument("--only")
    ap.add_argument("--timeline")
    ap.add_argument("--text", action="store_true")
    ap.add_argument("--peek", action="append", default=[])
    ap.add_argument("--crop")
    ap.add_argument("--scale", type=int, default=1)
    ap.add_argument("--cols", type=int, default=4)
    ap.add_argument("--page", type=int, default=24)
    ap.add_argument("--set")
    ap.add_argument("--out")
    ap.add_argument("--model")
    ap.add_argument("--jobs", type=int, default=min(4, os.cpu_count() or 1))
    a = ap.parse_args(argv)
    game = E.Game(a.game)
    game.check_rom()
    lines = read_lines(a.file) if a.file else []
    for i, r in enumerate(a.route, 1):
        name, _, route = r.rpartition("|")
        lines.append((name.split("|")[0].strip() or "r%d" % i, route.strip()))
    if a.only:
        want = set(a.only.split(","))
        lines = [l for l in lines if l[0] in want]
    if not lines:
        raise SystemExit("no routes: give a FILE or -r \"name | route\"")
    timeline = None
    if a.timeline:
        n, _, step = a.timeline.partition(":")
        timeline = (int(n), int(step or 40))
    peeks = [(p.split(":")[0], int(p.split(":")[1], 0)) for p in a.peek]     # LEN: 16 or 0x10
    crop = tuple(int(v) for v in a.crop.split(",")) if a.crop else None
    jobs = [(game.id, a.model or game.model, name, route, timeline, peeks, a.text) for name, route in lines]
    if a.jobs > 1 and len(jobs) > 1:
        import multiprocessing
        with multiprocessing.get_context("fork").Pool(min(a.jobs, len(jobs))) as pool:
            res = pool.map(run, jobs, chunksize=1)
    else:
        res = [run(j) for j in jobs]
    out = os.path.join(ROOT, "work", "preview", game.id,
                       (a.out and os.path.splitext(os.path.basename(a.out.rstrip("/")))[0]) or (os.path.splitext(os.path.basename(a.file))[0] if a.file and a.file != "-" else "routes"))
    os.makedirs(out, exist_ok=True)
    known = {}
    if a.set:                                       # pictures the working set already has
        import json, shoot
        d = os.path.join(ROOT, "work", "shots", game.id, a.set)
        if os.path.exists(os.path.join(d, "index.json")):
            for s in json.load(open(os.path.join(d, "index.json"), encoding="utf-8"))["shots"]:
                if "clip" not in s and os.path.exists(os.path.join(d, s["file"])):
                    known.setdefault(s.get("pixel_sha1") or shoot.pixel_sha1(os.path.join(d, s["file"])), "shot " + s["id"])
    tiles, bad = [], 0
    from PIL import Image
    for name, frames, info, err in res:
        if err:
            bad += 1
            print("%-28s ERROR %s" % (name, err))
            continue
        notes = []
        for label, png, text in frames:
            open(os.path.join(out, safe(label) + ".png"), "wb").write(png)
            h = hashlib.sha1(Image.open(io.BytesIO(png)).convert("RGB").tobytes()).hexdigest()
            if h in known and known[h] != label:
                notes.append("%s = %s" % (label if len(frames) > 1 else "picture", known[h]))
            known.setdefault(h, label)
        print("%-28s %s%s" % (name, info, ("  " + "; ".join(notes)) if notes else ""))
        for label, png, text in frames:
            if a.text and text is not None:
                print("--- %s" % label)
                print("\n".join("|" + l for l in text))
            else:
                tiles.append((label, png, text))
    if tiles:
        for p in draw(tiles, out, a.cols, a.page, a.scale, crop):
            print(os.path.relpath(p, ROOT))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
