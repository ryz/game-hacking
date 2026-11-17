"""Register a ROM as a game: identify it, copy it into rom/, create games/<slug>/ from the template, and film the
first seconds after power-on so the boot sequence is visible without playing.

  python3 tools/intake.py PATH/TO/ROM.gbc [--slug SLUG] [--title "Title"] [--model dmg|cgb|sgb] [--probe 1800]

Writes (never overwrites existing files in games/<slug>/):
  rom/<slug>.<ext>                       the dump (gitignored)
  games/<slug>/game.json                 identity (SHA-1, CRC32, header), platform, model, macros, ram, press/settle
  games/<slug>/playbook.md               controls/structure/strategy, filled by the game-scout skill
  games/<slug>/checkpoints.txt           named states as routes
  games/<slug>/shots.txt                 the shot plan
  games/<slug>/design/                   the design reference (README with notation, findings.md)
  work/intake/<slug>/probe_NNNN.png + sheet.png    a frame every 60 frames from power-on, no input
Then: python3 tools/emu.py SLUG --seq "pow,w300,start" --out work/x  to find the boot inputs.
"""
import argparse, hashlib, json, os, re, shutil, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
sys.path.insert(0, HERE)
import platforms  # noqa: E402

TEMPLATE = os.path.join(ROOT, "games", "_template")


def slugify(s):
    s = re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
    return s or "game"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("rom")
    ap.add_argument("--slug")
    ap.add_argument("--title", help="display title (default: header title)")
    ap.add_argument("--model", help="capture model override (gb: dmg|cgb|sgb|agb)")
    ap.add_argument("--probe", type=int, default=1800, help="frames to film after power-on (0 = skip)")
    a = ap.parse_args()

    data = open(a.rom, "rb").read()
    pname, cls = platforms.by_extension(a.rom)
    info = cls.identify(data)
    platform = info.pop("platform", pname)
    model = a.model or info.pop("model", None)
    info.pop("model", None)
    slug = a.slug or slugify(info.get("header_title") or os.path.splitext(os.path.basename(a.rom))[0])
    ext = os.path.splitext(a.rom)[1].lower()
    rom_rel = "rom/%s%s" % (slug, ext)
    os.makedirs(os.path.join(ROOT, "rom"), exist_ok=True)
    dst = os.path.join(ROOT, rom_rel)
    if os.path.abspath(a.rom) != os.path.abspath(dst):
        shutil.copyfile(a.rom, dst)

    gdir = os.path.join(ROOT, "games", slug)
    os.makedirs(gdir, exist_ok=True)
    gj = os.path.join(gdir, "game.json")
    if os.path.exists(gj):
        meta = json.load(open(gj, encoding="utf-8"))
        sha = hashlib.sha1(data).hexdigest()
        if meta.get("sha1") != sha:
            print("warning: games/%s/game.json has SHA-1 %s, this ROM is %s (another revision?)" % (
                slug, meta.get("sha1"), sha))
    else:
        meta = {
            "slug": slug,
            "title": a.title or info.get("header_title") or slug,
            "platform": platform,
            "model": model,
            "rom": rom_rel,
            "sha1": hashlib.sha1(data).hexdigest(),
            "crc32": platforms.crc32(data),
            "size": len(data),
            "header": info,
            "press": {"hold": 8, "wait": 40},
            "settle": {"step": 10, "limit": 300},
            "macros": {},
            "ram": {},
        }
        json.dump(meta, open(gj, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
        open(gj, "a").write("\n")
    for dirpath, _, files in os.walk(TEMPLATE):
        for f in files:
            src = os.path.join(dirpath, f)
            p = os.path.join(gdir, os.path.relpath(src, TEMPLATE))
            if not os.path.exists(p):
                os.makedirs(os.path.dirname(p), exist_ok=True)
                txt = open(src, encoding="utf-8").read()
                txt = txt.replace("{{TITLE}}", meta["title"]).replace("{{SLUG}}", slug)
                open(p, "w", encoding="utf-8").write(txt)
    print(json.dumps({k: meta[k] for k in ("slug", "title", "platform", "model", "sha1")}, indent=2))
    print("header:", json.dumps(meta["header"]))

    if a.probe:
        sys.path.insert(0, HERE)
        import emu
        g = emu.Game(slug)
        out = os.path.join(ROOT, "work", "intake", slug)
        os.makedirs(out, exist_ok=True)
        e = emu.open_game(g)
        paths = []
        for f in range(60, a.probe + 1, 60):
            e.frames(60)
            p = os.path.join(out, "probe_%04d.png" % f)
            e.screen_png(p)
            paths.append(p)
        e.close()
        emu.sheet(paths, os.path.join(out, "sheet.png"), cols=6,
                  labels=["f%d" % int(os.path.basename(p)[6:10]) for p in paths])
        print("probe:", os.path.relpath(os.path.join(out, "sheet.png"), ROOT))


if __name__ == "__main__":
    main()
