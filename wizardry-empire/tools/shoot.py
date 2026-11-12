"""Pixel-exact reference screenshots of game screens, English build and original side by side.

  python3 tools/shoot.py SET                       all shots in tools/routes/shots.txt -> work/shots/SET/
  python3 tools/shoot.py SET --list FILE           another shot list (same format)
  python3 tools/shoot.py SET --only title,town     only these ids
  python3 tools/shoot.py SET --rom en|jp|both|ref  default both; ref = rom/wizardry_empire_ref.gbc (tools/bps.py)
  python3 tools/shoot.py SET --publish             also copy the set to docs/shots/SET/ (committed)

Shot list lines: `id | category | description | tokens` (tokens as in tools/emu.py; `pow` = power on only,
`boot` = power on to the town, `poke` = mark all monsters seen (museum), PARTY = form the 6-member party at the tavern from the town).
For every shot and ROM: `<id>.<rom>.png` (native 160x144, the emulator's framebuffer: CGB colours expanded
5->8 bit, no colour correction, no filtering), `<id>.<rom>@3x.png` (nearest neighbour), and for both ROMs
`<id>.compare@3x.png` (JP left, EN right). Each shot waits until the screen is stable (two identical frames
10 frames apart, up to 300 frames) so text has finished typing and fades are done; the catalogue records
whether it settled. Catalogue: `index.md` + `index.json` (id, category, description, tokens, ROM, commit,
ROM SHA-1, settled).
--publish copies the native PNGs, the compare images and index.md/index.json to docs/shots/SET/ (the @3x
single-ROM images are left out: they are the native ones enlarged).
"""
import argparse, hashlib, json, os, shutil, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
sys.path.insert(0, HERE)
import emu
from tour import PARTY

ROMS = {"en": emu.EN_ROM, "jp": os.path.join(ROOT, "rom", "wizardry_empire_j.gbc"),
        "ref": os.path.join(ROOT, "rom", "wizardry_empire_ref.gbc")}   # reference fan translation (tools/bps.py)


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
    """Tokens as tools/emu.py (incl. poke:ADDR=HEX), plus `poke` = mark all monsters seen (museum, $C5AE x21)."""
    for tok in emu.tokens(seq) if isinstance(seq, str) else seq:
        if tok == "poke":
            g.mem_write(0xC5AE, [0xFF] * 21)
        elif tok != "pow" and not emu.step(g, tok):
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
    ap.add_argument("--rom", default="both", choices=["en", "jp", "both", "ref"])
    ap.add_argument("--publish", action="store_true")
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
            g, toks, skip = emu.start(ROMS[r], s["tokens"])     # boot / boot+PARTY from the route cache
            try:
                play(g, toks[skip:])
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
    idx = os.path.join(out, "index.json")
    if want and os.path.exists(idx):      # --only: replace those ids in the existing catalogue, keep the rest
        new = {r["id"]: r for r in cat}
        old = json.load(open(idx))
        cat = [new.pop(r["id"], r) for r in old] + list(new.values())
    json.dump(cat, open(idx, "w"), indent=1, ensure_ascii=False)
    with open(os.path.join(out, "index.md"), "w", encoding="utf-8") as f:
        f.write("# Reference screenshots - set `%s` (commit `%s`)\n\n" % (a.set, commit))
        f.write("Native 160x144 PNGs (`<id>.<rom>.png`), 3x nearest (`@3x`), JP|EN (`compare@3x`).\n\n")
        f.write("| id | category | description | settled | tokens |\n|---|---|---|---|---|\n")
        for r in cat:
            f.write("| %s | %s | %s | %s | `%s` |\n" % (r["id"], r["category"], r["description"],
                    ", ".join("%s:%s" % (k, "yes" if v else "no") for k, v in r["settled"].items()), r["tokens"][:120]))
    print("catalogue:", os.path.relpath(os.path.join(out, "index.md"), ROOT))
    if a.publish:
        pub = os.path.join(ROOT, "docs", "shots", a.set)
        os.makedirs(pub, exist_ok=True)
        for f in os.listdir(out):
            if f.endswith((".md", ".json")) or (f.endswith(".png") and "@3x" not in f) or f.endswith(".compare@3x.png"):
                shutil.copy2(os.path.join(out, f), os.path.join(pub, f))
        print("published:", os.path.relpath(pub, ROOT))


if __name__ == "__main__":
    main()
