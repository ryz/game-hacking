"""Pixel-exact reference screenshots of game screens, English build and original side by side.

  python3 tools/shoot.py SET                       all shots in tools/routes/shots.txt -> work/shots/SET/
  python3 tools/shoot.py SET --list FILE           another shot list (same format)
  python3 tools/shoot.py SET --only title,town     only these ids
  python3 tools/shoot.py SET --rom en|jp|both|ref|all
                                                   default both (jp, en); ref = rom/wizardry_empire_ref.gbc
                                                   (tools/bps.py); all = jp, en and ref (three-way compare)
  python3 tools/shoot.py SET --publish             also copy the set to ../shots/SET/ (committed)

Shot list lines: `id | category | description | tokens` (tokens as in tools/emu.py; `pow` = power on only,
`boot` = power on to the town, `poke` = mark all monsters seen (museum), PARTY = form the 6-member party at the tavern from the town).
category = one of the database categories (CATEGORIES below; docs/capture-guide.md at the repo root).
File names follow the repository's scheme (docs/capture-guide.md "File names"), with the set always written
and the ROM last:  NAME = wizardry-empire_gbc_jp_<category>_<id>.<set>   (wizardry-empire_gbc_jp_menu_camp.rev1-tour.en.png)
SET is lowercase words joined by `-` (rev1-tour). `jp` in the head is the region of the game; the ROM field
says which build the picture shows (jp = original, en = this patch, ref = other patch).
For every shot and ROM: `NAME.<rom>.png` (native 160x144, the emulator's framebuffer: CGB colours expanded
5->8 bit, no colour correction, no filtering), `3x/NAME.<rom>.png` (nearest neighbour, in the 3x/ subfolder), and for both ROMs
`3x/NAME.compare.png` (JP left, EN right). With `--rom all`: `3x/NAME.compare3.png` instead, JP | EN | REF
left to right, each panel labelled at the top ("Original (JP)", "This patch", "Other patch"); same gap and
background as the two-way compare, the panels themselves are the unchanged 3x images. Each shot waits until
the screen is stable (two identical frames 10 frames apart, up to 300 frames) so text has finished typing and
fades are done; the catalogue records whether it settled. Catalogue: `index.md` + `index.json` (id, category,
description, tokens, ROM, commit, ROM SHA-1, settled); with `--rom all` index.md also links the three native
images and the compare3 image of every shot.
--publish copies the native PNGs, the compare / compare3 images and index.md/index.json (and any other .md in
the set folder, e.g. a README.md) to ../shots/SET/ (compare images into its 3x/; the 3x single-ROM images are left out: they are the
native ones enlarged).
"""
import argparse, hashlib, json, os, re, shutil, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
sys.path.insert(0, HERE)
import emu
from tour import PARTY

ROMS = {"en": emu.EN_ROM, "jp": os.path.join(ROOT, "rom", "wizardry_empire_j.gbc"),
        "ref": os.path.join(ROOT, "rom", "wizardry_empire_ref.gbc")}   # reference fan translation (tools/bps.py)
WHICH = {"both": ["jp", "en"], "all": ["jp", "en", "ref"]}             # multi-ROM modes, left to right
LABELS = {"jp": "Original (JP)", "en": "This patch", "ref": "Other patch"}
GAP, BG = 12, (40, 40, 40)                                            # compare images: gap and background
HEAD = "wizardry-empire_gbc_jp"         # <game>_<platform>_<region> of every file name (repo-wide scheme)
# The database categories (same list as tools/shoot.py at the repo root, docs/capture-guide.md). How this game's
# screens map onto them: town/facility menus and prompts = menu; character creation, inn rest, museum, maze
# actions = system; character sheets, spell and item pages = inventory; shop and temple services = shop;
# maze view = gameplay; chests = battle.
CATEGORIES = ["boot", "title", "menu", "options", "cutscene", "gameplay", "hud", "system", "map", "inventory",
              "dialogue", "shop", "battle", "boss", "minigame", "ending", "credits", "gameover", "save", "extra"]


def name(s, set_name, kind):
    """File name of a shot: kind = jp | en | ref | compare | compare3."""
    return "%s_%s_%s.%s.%s.png" % (HEAD, s["category"], s["id"], set_name, kind)


def shots(path):
    out = []
    for line in open(path, encoding="utf-8"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        sid, cat, desc, seq = [x.strip() for x in line.split("|", 3)]
        if cat not in CATEGORIES:
            raise SystemExit("%s: %s: category %r is not one of %s (it is part of the file name)" % (
                path, sid, cat, ", ".join(CATEGORIES)))
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


def compare3(images, roms):
    """JP | EN | REF 3x panels side by side, each with its label in a band above it (same gap/background)."""
    from PIL import Image, ImageDraw, ImageFont
    try:
        font = ImageFont.load_default(size=18)     # Pillow >= 10.1: bundled scalable font, same on every machine
    except TypeError:
        font = ImageFont.load_default()
    w, h, band = images[0].width, images[0].height, 30
    c = Image.new("RGB", (w * len(images) + GAP * (len(images) - 1), h + band), BG)
    d = ImageDraw.Draw(c)
    for i, (im, r) in enumerate(zip(images, roms)):
        x = i * (w + GAP)
        c.paste(im, (x, band))
        tw = d.textlength(LABELS[r], font=font)
        d.text((x + (w - tw) / 2, band / 2), LABELS[r], font=font, fill=(230, 230, 230), anchor="lm")
    return c


def publish(out, pub):
    """Copy a checked set to ../shots/SET/: native PNGs, compare images, index and notes (.md/.json)."""
    os.makedirs(pub, exist_ok=True)
    for f in sorted(os.listdir(out)):
        if os.path.isfile(os.path.join(out, f)) and f.endswith((".md", ".json", ".png")):
            shutil.copy2(os.path.join(out, f), os.path.join(pub, f))
    x3 = os.path.join(out, "3x")            # only the compare images; single-ROM 3x copies are left out
    for f in sorted(os.listdir(x3)) if os.path.isdir(x3) else []:
        if f.endswith((".compare.png", ".compare3.png")):
            os.makedirs(os.path.join(pub, "3x"), exist_ok=True)
            shutil.copy2(os.path.join(x3, f), os.path.join(pub, "3x", f))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("set")
    ap.add_argument("--list", default=os.path.join(HERE, "routes", "shots.txt"))
    ap.add_argument("--only")
    ap.add_argument("--rom", default="both", choices=["en", "jp", "both", "ref", "all"])
    ap.add_argument("--publish", action="store_true")
    a = ap.parse_args()
    if not re.match(r"^[a-z0-9]+(-[a-z0-9]+)*$", a.set):
        raise SystemExit("set name %r must be lowercase a-z0-9 words joined by `-` (it is part of the file names)" % a.set)
    from PIL import Image
    out = os.path.join(ROOT, "work", "shots", a.set)
    os.makedirs(out, exist_ok=True)
    commit = subprocess.run(["git", "-C", ROOT, "rev-parse", "--short", "HEAD"], capture_output=True, text=True).stdout.strip()
    which = WHICH.get(a.rom, [a.rom])
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
                p = os.path.join(out, name(s, a.set, r))
                g.screenshot_png(p, scale=1)
            finally:
                g.close()
            im = Image.open(p).convert("RGB")
            im.save(p)
            big = im.resize((im.width * 3, im.height * 3), Image.NEAREST)
            os.makedirs(os.path.join(out, "3x"), exist_ok=True)
            big.save(os.path.join(out, "3x", name(s, a.set, r)))
            rec["files"][r] = os.path.basename(p)
            rec["rom_sha1"][r] = rom_info(ROMS[r])[:12]
        if len(which) == 2:
            a3 = [Image.open(os.path.join(out, "3x", name(s, a.set, r))) for r in which]
            gap = GAP
            c = Image.new("RGB", (a3[0].width * 2 + gap, a3[0].height), BG)
            c.paste(a3[0], (0, 0))
            c.paste(a3[1], (a3[0].width + gap, 0))
            c.save(os.path.join(out, "3x", name(s, a.set, "compare")))
        elif len(which) == 3:
            a3 = [Image.open(os.path.join(out, "3x", name(s, a.set, r))).convert("RGB") for r in which]
            compare3(a3, which).save(os.path.join(out, "3x", name(s, a.set, "compare3")))
            rec["files"]["compare3"] = "3x/" + name(s, a.set, "compare3")
        cat.append(rec)
        print("%-18s %s" % (s["id"], " ".join("%s:%s" % (r, "ok" if rec["settled"][r] else "NOT SETTLED") for r in which)), flush=True)
    idx = os.path.join(out, "index.json")
    if want and os.path.exists(idx):      # --only: replace those ids in the existing catalogue, keep the rest
        new = {r["id"]: r for r in cat}
        old = json.load(open(idx))
        cat = [new.pop(r["id"], r) for r in old] + list(new.values())
    json.dump(cat, open(idx, "w"), indent=1, ensure_ascii=False)
    three = len(which) == 3
    with open(os.path.join(out, "index.md"), "w", encoding="utf-8") as f:
        f.write("# Reference screenshots - set `%s` (commit `%s`)\n\n" % (a.set, commit))
        if three:
            f.write("File names: `NAME` = `%s_<category>_<id>.%s`. Native 160x144 PNGs (`NAME.<rom>.png`: jp = "
                    "original, en = this patch, ref = other patch), JP|EN|REF 3x nearest "
                    "(`3x/NAME.compare3.png`).\n\n" % (HEAD, a.set))
            f.write("| id | category | description | settled | JP | EN | REF | compare | tokens |\n"
                    "|---|---|---|---|---|---|---|---|---|\n")
        else:
            f.write("File names: `NAME` = `%s_<category>_<id>.%s`. Native 160x144 PNGs (`NAME.<rom>.png`); 3x "
                    "nearest in `3x/`: JP|EN (`3x/NAME.compare.png`).\n\n" % (HEAD, a.set))
            f.write("| id | category | description | settled | tokens |\n|---|---|---|---|---|\n")
        for r in cat:
            settled = ", ".join("%s:%s" % (k, "yes" if v else "no") for k, v in r["settled"].items())
            if three:
                links = " | ".join("[%s](%s)" % (k, r["files"][k]) if k in r["files"] else "-"
                                   for k in ("jp", "en", "ref", "compare3"))
                f.write("| %s | %s | %s | %s | %s | `%s` |\n" % (r["id"], r["category"], r["description"],
                        settled, links, r["tokens"][:120]))
            else:
                f.write("| %s | %s | %s | %s | `%s` |\n" % (r["id"], r["category"], r["description"],
                        settled, r["tokens"][:120]))
    print("catalogue:", os.path.relpath(os.path.join(out, "index.md"), ROOT))
    if a.publish:
        pub = os.path.join(ROOT, "..", "shots", a.set)
        publish(out, pub)
        print("published:", os.path.relpath(pub, ROOT))


if __name__ == "__main__":
    main()
