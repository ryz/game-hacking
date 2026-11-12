"""Frame-time and flicker measurement for every key press of the tour routes (tools/routes/tour.txt).

  python3 tools/perf.py                 English build and the original ROM, all routes -> work/qa/perf/
  python3 tools/perf.py --en | --jp     one ROM only            python3 tools/perf.py town_info inn   some routes
  python3 tools/perf.py report          compare the last EN and JP runs (work/qa/perf/report.md)
  -j N  parallel routes (default: CPU count)      --rom PATH  measure another build as "en" (A/B tests)

Per transition (one key press plus the wN tokens right after it) every frame is captured, as 20 x 18 cells of
8 x 8 pixels. With B = the screen before the press and F = the screen at the end of the window:
  react   first frame (counted from the press) that differs from B
  settle  first frame from which the screen equals F (the transition's length)
  odd     frames that show a cell equal to neither B nor F (wrong letters, half-drawn boxes, typing)
  cells   the most such cells in one frame
Typing animations count as odd in both ROMs; compare EN with JP. Each EN transition with odd frames gets a strip
of its distinct frames (work/qa/perf/en/<route>/NN_<token>.png).
"""
import io, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
sys.path.insert(0, HERE)
import emu
from tour import routes

OUT = os.path.join(ROOT, "work", "qa", "perf")
JP_ROM = os.path.join(ROOT, "rom", "wizardry_empire_j.gbc")


def cells(png):
    from PIL import Image
    im = Image.open(io.BytesIO(png)).convert("RGB")
    raw = im.tobytes()
    w = 160 * 3
    out = []
    for cy in range(18):
        for cx in range(20):
            out.append(b"".join(raw[(cy * 8 + y) * w + cx * 24:(cy * 8 + y) * w + cx * 24 + 24] for y in range(8)))
    return out


def measure(frames, before):
    final = frames[-1]
    react = next((i for i, f in enumerate(frames) if f != before), None)
    settle = 0
    for i, f in enumerate(frames):
        if f != final:
            settle = i + 1
    odd, most = 0, 0
    for f in frames:
        n = sum(1 for c, b, e in zip(f, before, final) if c != b and c != e)
        if n:
            odd += 1
            most = max(most, n)
    return {"react": react, "settle": settle, "odd": odd, "cells": most}


def run_route(job):
    name, seq, rom, tag = job
    out = os.path.join(OUT, tag, name)
    os.makedirs(out, exist_ok=True)
    g, toks, skip = emu.start(rom, seq)
    toks = toks[skip:]
    res = []
    i = 0
    while i < len(toks):
        tok = toks[i]
        base, n = (tok.split("*") + ["1"])[:2] if "*" in tok else (tok, "1")
        keys = base.split("+")
        if not all(k in emu.KEYS for k in keys):
            emu.step(g, tok)
            i += 1
            continue
        waits = []
        j = i + 1
        while j < len(toks) and toks[j].startswith("w") and toks[j][1:].isdigit():
            waits.append(int(toks[j][1:]))
            j += 1
        for rep in range(int(n)):
            before_png = g.screenshot()
            before = cells(before_png)
            pngs = []
            g.input_set(keys)
            for f in range(8):
                g.run_frames(1)
                pngs.append(g.screenshot())
            g.input_set([])
            for f in range(40 + (sum(waits) if rep == int(n) - 1 else 0)):
                g.run_frames(1)
                pngs.append(g.screenshot())
            frames = [cells(p) for p in pngs]
            m = measure(frames, before)
            m.update(step=len(res), token=base, at=i)
            res.append(m)
            if tag != "jp" and m["odd"]:
                strip(pngs, before_png, os.path.join(out, "%02d_%s.png" % (m["step"], base)))
        i = j
    g.close()
    json.dump(res, open(os.path.join(out, "perf.json"), "w"), indent=0)
    return name, len(res)


def strip(pngs, before_png, path):
    """Distinct consecutive frames (the frame number above each), 2x."""
    from PIL import Image, ImageDraw
    seq, last = [], before_png
    for k, p in enumerate(pngs):
        if p != last:
            seq.append((k, p))
            last = p
    seq = [(-1, before_png)] + seq[:23]
    im = Image.new("RGB", (len(seq) * 164, 156), (60, 60, 60))
    d = ImageDraw.Draw(im)
    for n, (k, p) in enumerate(seq):
        im.paste(Image.open(io.BytesIO(p)).convert("RGB"), (n * 164 + 2, 12))
        d.text((n * 164 + 4, 0), "before" if k < 0 else "f%d" % k, fill=(255, 255, 0))
    im.resize((im.size[0] * 2, im.size[1] * 2), Image.NEAREST).save(path)


def report():
    rows = []
    for name, _ in routes():
        try:
            en = json.load(open(os.path.join(OUT, "en", name, "perf.json")))
            jp = json.load(open(os.path.join(OUT, "jp", name, "perf.json")))
        except OSError:
            continue
        for e, j in zip(en, jp):
            rows.append((name, e, j))
    tot = {k: [sum(r[1][k] for r in rows), sum(r[2][k] for r in rows)] for k in ("settle", "odd")}
    lines = ["# Perf report (EN vs JP, every key press of the tour routes)", "",
             "Transitions: %d. Total frames to settle: EN %d, JP %d. Frames with odd cells: EN %d, JP %d." % (
                 len(rows), tot["settle"][0], tot["settle"][1], tot["odd"][0], tot["odd"][1]), "",
             "Worst first (by extra settle frames + extra odd frames over JP):", "",
             "| route | step | key | react EN/JP | settle EN/JP | odd EN/JP | max odd cells EN |", "|---|---|---|---|---|---|---|"]
    rows.sort(key=lambda r: -((r[1]["settle"] - r[2]["settle"]) + (r[1]["odd"] - r[2]["odd"])))
    for name, e, j in rows:
        if (e["settle"], e["odd"]) == (j["settle"], j["odd"]):
            continue
        lines.append("| %s | %d | %s | %s/%s | %d/%d | %d/%d | %d |" % (
            name, e["step"], e["token"], e["react"], j["react"], e["settle"], j["settle"], e["odd"], j["odd"], e["cells"]))
    open(os.path.join(OUT, "report.md"), "w").write("\n".join(lines) + "\n")
    print("\n".join(lines[:12]))
    print("...", os.path.relpath(os.path.join(OUT, "report.md"), ROOT))


def main(argv):
    if "-h" in argv or "--help" in argv:
        print(__doc__)
        return 0
    if argv[:1] == ["report"]:
        report()
        return 0
    jobs = os.cpu_count() or 1
    if "-j" in argv:
        jobs = int(argv[argv.index("-j") + 1])
        argv = argv[:argv.index("-j")] + argv[argv.index("-j") + 2:]
    en_rom = emu.EN_ROM
    if "--rom" in argv:
        en_rom = os.path.abspath(argv[argv.index("--rom") + 1])
        argv = argv[:argv.index("--rom")] + argv[argv.index("--rom") + 2:]
    tags = ["en"] if "--en" in argv else ["jp"] if "--jp" in argv else ["en", "jp"]
    want = [a for a in argv if not a.startswith("--")]
    todo = []
    for tag in tags:
        rom = JP_ROM if tag == "jp" else en_rom
        for p in emu.PREFIXES:
            emu.start(rom, p)[0].close()
        todo += [(name, seq, rom, tag) for name, seq in routes() if not want or name in want]
    import multiprocessing
    with multiprocessing.Pool(max(1, min(jobs, len(todo)))) as pool:
        for name, n in pool.imap_unordered(run_route, todo):
            print("%-10s %d transitions" % (name, n), flush=True)
    if tags == ["en", "jp"]:
        report()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
