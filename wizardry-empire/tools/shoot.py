"""Pixel-exact reference screenshots of game screens, English build and original side by side.

  python3 tools/shoot.py SET                       all shots in tools/routes/shots.txt -> work/shots/SET/
  python3 tools/shoot.py SET --list FILE           another shot list (same format)
  python3 tools/shoot.py SET --only title,town     only these ids
  python3 tools/shoot.py SET --rom en|jp|both      default both

Shot list lines: `id | category | description | tokens` (tokens as in tools/emu.py; `pow` = power on only,
`boot` = power on to the town, PARTY = form the 6-member party at the tavern from the town).
For every shot and ROM: `<id>.<rom>.png` (native 160x144, the emulator's framebuffer: CGB colours expanded
5->8 bit, no colour correction, no filtering), `<id>.<rom>@3x.png` (nearest neighbour), and for both ROMs
`<id>.compare@3x.png` (JP left, EN right). Each shot waits until the screen is stable (two identical frames
10 frames apart, up to 300 frames) so text has finished typing and fades are done; the catalogue records
whether it settled. Catalogue: `index.md` + `index.json` (id, category, description, tokens, ROM, commit,
ROM SHA-1, settled).
"""
import argparse, hashlib, json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
sys.path.insert(0, HERE)
import emu
from tour import PARTY

ROMS = {"en": emu.EN_ROM, "jp": os.path.join(ROOT, "rom", "wizardry_empire_j.gbc")}


def shots(path):
    out = []
    for line in open(path, encoding="utf-8"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        sid, cat, desc, seq = [x.strip() for x in line.split("|", 3)]
        out.append({"id": sid, "category": cat, "description": desc, "tokens": seq.replace("PARTY", PARTY)})
    return out


def play(g, seq):
    for tok in (t.strip() for t in seq.split(",") if t.strip()):
        n, base = 1, tok
        if "*" in tok:
            base, n = tok.split("*")
            n = int(n)
        for _ in range(n):
            if base == "pow":
                pass
            elif base == "boot":
                emu.boot(g)
            elif base.startswith("w") and base[1:].isdigit():
                g.run_frames(int(base[1:]))
            elif all(k in emu.KEYS for k in base.split("+")):
                emu.press(g, base.split("+"))
            else:
                raise ValueError("unknown token %r" % tok)


def settle(g, step=10, limit=300):
    prev = g.screenshot()
    for _ in range(limit // step):
        g.run_frames(step)
        cur = g.screenshot()
        if cur == prev:
            return True
        prev = cur
    return False


def rom_info(path):
    sha = hashlib.sha1(open(path, "rb").read()).hexdigest()
    return sha


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("set")
    ap.add_argument("--list", default=os.path.join(HERE, "routes", "shots.txt"))
    ap.add_argument("--only")
    ap.add_argument("--rom", default="both", choices=["en", "jp", "both"])
    a = ap.parse_args()
    from PIL import Image
    out = os.path.join(ROOT, "work", "shots", a.set)
    os.makedirs(out, exist_ok=True)
    commit = subprocess.run(["git", "-C", ROOT, "rev-parse", "--short", "HEAD"], capture_output=True, text=True).stdout.strip()
    which = ["jp", "en"] if a.rom == "both" else [a.rom]
    want = set(a.only.split(",")) if a.only else None
    cat = []
    for s in shots(a.list):
        if want and s["id"] not in want:
            continue
        rec = dict(s, commit=commit, files={}, settled={}, rom_sha1={})
        for r in which:
            g = emu.open_emu(ROMS[r])
            try:
                play(g, s["tokens"])
                rec["settled"][r] = settle(g)
                p = os.path.join(out, "%s.%s.png" % (s["id"], r))
                g.screenshot_png(p, scale=1)
            finally:
                g.close()
            im = Image.open(p).convert("RGB")
            im.save(p)
            big = im.resize((im.width * 3, im.height * 3), Image.NEAREST)
            big.save(os.path.join(out, "%s.%s@3x.png" % (s["id"], r)))
            rec["files"][r] = os.path.basename(p)
            rec["rom_sha1"][r] = rom_info(ROMS[r])[:12]
        if len(which) == 2:
            a3 = [Image.open(os.path.join(out, "%s.%s@3x.png" % (s["id"], r))) for r in which]
            gap = 12
            c = Image.new("RGB", (a3[0].width * 2 + gap, a3[0].height), (40, 40, 40))
            c.paste(a3[0], (0, 0))
            c.paste(a3[1], (a3[0].width + gap, 0))
            c.save(os.path.join(out, "%s.compare@3x.png" % s["id"]))
        cat.append(rec)
        print("%-18s %s" % (s["id"], " ".join("%s:%s" % (r, "ok" if rec["settled"][r] else "NOT SETTLED") for r in which)), flush=True)
    json.dump(cat, open(os.path.join(out, "index.json"), "w"), indent=1, ensure_ascii=False)
    with open(os.path.join(out, "index.md"), "w", encoding="utf-8") as f:
        f.write("# Reference screenshots - set `%s` (commit `%s`)\n\n" % (a.set, commit))
        f.write("Native 160x144 PNGs (`<id>.<rom>.png`), 3x nearest (`@3x`), JP|EN (`compare@3x`).\n\n")
        f.write("| id | category | description | settled | tokens |\n|---|---|---|---|---|\n")
        for r in cat:
            f.write("| %s | %s | %s | %s | `%s` |\n" % (r["id"], r["category"], r["description"],
                    ", ".join("%s:%s" % (k, "yes" if v else "no") for k, v in r["settled"].items()), r["tokens"][:120]))
    print("catalogue:", os.path.relpath(os.path.join(out, "index.md"), ROOT))


if __name__ == "__main__":
    main()
