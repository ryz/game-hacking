"""One-command check: build, tests, screen tour, pixel diff against the accepted baseline.

  python3 tools/check.py              build + pytest + tour (parallel, route cache) + diff vs the baseline
  python3 tools/check.py --accept     after looking at the diff: make the current tour the new baseline
  python3 tools/check.py --no-build   skip the build (e.g. only re-run the tour)
  python3 tools/check.py --shots SET  also shoot tools/routes/shots.txt into work/shots/SET (EN only)

Baseline: work/qa/tour_baseline/ (per-token PNGs of the last accepted tour). Diff output: work/qa/check/
  changed.txt   one line per changed or new/missing frame
  diff.png      old | new | changed pixels (red) for every changed frame, 2x
Exit status: 0 = all passed and no frame changed, 1 = a step failed or a route hung, 3 = frames changed (look
at diff.png, then --accept if the change is intended).
"""
import glob, os, shutil, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
TOUR = os.path.join(ROOT, "work", "qa", "tour_en")
BASE = os.path.join(ROOT, "work", "qa", "tour_baseline")
OUT = os.path.join(ROOT, "work", "qa", "check")


def step(name, cmd):
    t = time.time()
    r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    ok = r.returncode == 0
    tail = (r.stdout + r.stderr).strip().splitlines()[-3:]
    print("%-6s %-4s %5.1fs  %s" % (name, "ok" if ok else "FAIL", time.time() - t, " | ".join(tail)))
    return ok


def frames(d):
    return {os.path.relpath(f, d) for f in glob.glob(os.path.join(d, "*", "[0-9]*.png"))}


def diff():
    from PIL import Image, ImageChops
    os.makedirs(OUT, exist_ok=True)
    new, old = frames(TOUR), frames(BASE)
    lines, tiles = [], []
    for f in sorted(new | old):
        if f not in old:
            lines.append("new      " + f)
            continue
        if f not in new:
            lines.append("missing  " + f)
            continue
        a = Image.open(os.path.join(BASE, f)).convert("RGB")
        b = Image.open(os.path.join(TOUR, f)).convert("RGB")
        box = ImageChops.difference(a, b).getbbox()
        if box:
            lines.append("changed  %s  bbox=%s" % (f, box))
            mask = ImageChops.difference(a, b).convert("L").point(lambda v: 255 if v else 0)
            red = Image.composite(Image.new("RGB", b.size, (255, 0, 0)), b.point(lambda v: v // 3), mask)
            row = Image.new("RGB", (a.width * 3 + 8, a.height), (255, 255, 255))
            for k, im in enumerate((a, b, red)):
                row.paste(im, (k * (a.width + 4), 0))
            tiles.append(row)
    open(os.path.join(OUT, "changed.txt"), "w").write("\n".join(lines) + ("\n" if lines else ""))
    if tiles:
        w, h = tiles[0].size
        sheet = Image.new("RGB", (w, (h + 4) * len(tiles)), (255, 255, 255))
        for k, t in enumerate(tiles):
            sheet.paste(t, (0, k * (h + 4)))
        sheet.resize((sheet.width * 2, sheet.height * 2), Image.NEAREST).save(os.path.join(OUT, "diff.png"))
    elif os.path.exists(os.path.join(OUT, "diff.png")):
        os.remove(os.path.join(OUT, "diff.png"))
    return lines


def main(argv):
    if "--accept" in argv:
        shutil.rmtree(BASE, ignore_errors=True)
        shutil.copytree(TOUR, BASE)
        print("baseline <- %s (%d frames)" % (os.path.relpath(TOUR, ROOT), len(frames(BASE))))
        return 0
    py = sys.executable
    ok = True
    if "--no-build" not in argv:
        ok = step("build", [py, "tools/build.py"])
        if not ok:
            return 1
    ok &= step("tests", [py, "-m", "pytest", "-q", "tests"])
    ok &= step("tour", [py, "tools/tour.py"])
    if "--shots" in argv:
        ok &= step("shots", [py, "tools/shoot.py", argv[argv.index("--shots") + 1], "--rom", "en"])
    if not os.path.isdir(BASE):
        print("no baseline yet: python3 tools/check.py --accept")
        return 0 if ok else 1
    lines = diff()
    print("diff   %d frame(s) changed/new/missing vs %s%s" % (
        len(lines), os.path.relpath(BASE, ROOT), "  -> work/qa/check/diff.png, changed.txt" if lines else ""))
    for l in lines[:20]:
        print("       " + l)
    if not ok:
        return 1
    return 3 if lines else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
