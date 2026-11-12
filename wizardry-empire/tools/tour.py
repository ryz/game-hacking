"""Run the fixed screen tour (tools/routes/tour.txt) and write one contact sheet per route.

  python3 tools/tour.py               English build -> work/qa/tour_en/<route>/sheet.png
  python3 tools/tour.py --jp          original ROM  -> work/qa/tour_jp/<route>/ (same inputs, for comparison)
  python3 tools/tour.py town_info shop     only these routes
  -j N        parallel routes (default: CPU count)      --no-cache   play boot/PARTY instead of the route cache
Prints one line per route (OK / HUNG) and the sheet paths; exit 1 if any route hung.
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
sys.path.insert(0, HERE)
import emu

PARTY = emu.PARTY


def routes():
    out = []
    for line in open(os.path.join(HERE, "routes", "tour.txt"), encoding="utf-8"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        name, seq = [x.strip() for x in line.split("|", 1)]
        out.append((name, seq.replace("PARTY", PARTY)))
    return out


def main(argv):
    if "-h" in argv or "--help" in argv:
        print(__doc__)
        return 0
    jp = "--jp" in argv
    cache = "--no-cache" not in argv
    jobs = os.cpu_count() or 1
    if "-j" in argv:
        jobs = int(argv[argv.index("-j") + 1])
        argv = argv[:argv.index("-j")] + argv[argv.index("-j") + 2:]
    want = [a for a in argv if not a.startswith("--")]
    rom = os.path.join(ROOT, "rom", "wizardry_empire_j.gbc") if jp else emu.EN_ROM
    base = os.path.join(ROOT, "work", "qa", "tour_jp" if jp else "tour_en")
    todo = [(name, seq, os.path.join(base, name), rom, cache) for name, seq in routes() if not want or name in want]
    if cache and todo:              # make the shared prefix states once before the workers race for them
        for p in emu.PREFIXES:
            emu.start(rom, p)[0].close()
    import multiprocessing
    with multiprocessing.Pool(max(1, min(jobs, len(todo)))) as pool:
        rcs = pool.map(_job, todo)
    bad = 0
    for (name, _, out, _, _), rc in zip(todo, rcs):
        bad += rc != 0
        print("%-10s %s  %s" % (name, "HUNG" if rc else "OK", os.path.relpath(os.path.join(out, "sheet.png"), ROOT)))
    return 1 if bad else 0


def _job(t):
    name, seq, out, rom, cache = t
    import shutil
    shutil.rmtree(out, ignore_errors=True)     # old per-token PNGs would linger (numbering skips cached tokens)
    return _run(seq, out, rom, cache)


def _run(seq, out, rom, cache=True):
    import contextlib, io
    with contextlib.redirect_stdout(io.StringIO()):
        return emu.run(seq, out, rom=rom, cache=cache)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
