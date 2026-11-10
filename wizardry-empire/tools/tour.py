"""Run the fixed screen tour (tools/routes/tour.txt) and write one contact sheet per route.

  python3 tools/tour.py               English build -> work/qa/tour_en/<route>/sheet.png
  python3 tools/tour.py --jp          original ROM  -> work/qa/tour_jp/<route>/ (same inputs, for comparison)
  python3 tools/tour.py town_info shop     only these routes
Prints one line per route (OK / HUNG) and the sheet paths; exit 1 if any route hung.
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
sys.path.insert(0, HERE)
import emu

PARTY = "right*3,a,w60,a,w40" + ",a,w30" * 6 + ",b,w40,b,w40,b,w60"


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
    jp = "--jp" in argv
    want = [a for a in argv if not a.startswith("--")]
    rom = os.path.join(ROOT, "rom", "wizardry_empire_j.gbc") if jp else emu.EN_ROM
    base = os.path.join(ROOT, "work", "qa", "tour_jp" if jp else "tour_en")
    bad = 0
    for name, seq in routes():
        if want and name not in want:
            continue
        out = os.path.join(base, name)
        rc = _run(seq, out, rom)
        bad += rc != 0
        print("%-10s %s  %s" % (name, "HUNG" if rc else "OK", os.path.relpath(os.path.join(out, "sheet.png"), ROOT)))
    return 1 if bad else 0


def _run(seq, out, rom):
    import contextlib, io
    with contextlib.redirect_stdout(io.StringIO()):
        return emu.run(seq, out, rom=rom)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
