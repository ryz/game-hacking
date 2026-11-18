"""Register a ROM as a game: identify it, copy it into rom/, create games/<platform>/<slug>/ from the template, and film the
first seconds after power-on so the boot sequence is visible without playing.

  python3 tools/intake.py PATH/TO/ROM.gbc [--slug SLUG] [--title "Title"] [--region jp|na|eu] [--model dmg|cgb|sgb]
                         [--probe 1800] [--patch PATCH[:auto|headered|unheadered] ...]

--slug is the short normalized game name (lowercase words joined by `-`, no platform in it: might-and-magic-2);
--region is where the dump was released (a translated Japanese ROM is jp). Both are part of every shot file name
(tools/shoot.py). The region is read from the header where the header says it (Game Boy: Japan; SNES: country
code; NES: PAL = eu); otherwise --region is required.

--patch (repeatable, applied in order; IPS, BPS, UPS via tools/patch.py): ROM is then the unpatched dump. The
patched ROM is what gets registered and played; the dump goes to rom/src/<slug>-base.<ext>, the patches to
rom/patches/<slug>/, and game.json "source" records names, SHA-1s and layouts (rebuild: tools/patch.py).

Writes (never overwrites existing files in games/<platform>/<slug>/):
  rom/<slug>.<ext>                       the dump, or the patched ROM with --patch (gitignored)
  games/<platform>/<slug>/game.json                 identity (SHA-1, CRC32, header), platform, model, macros, ram, press/settle
  games/<platform>/<slug>/playbook.md               controls/structure/strategy, filled by the game-scout skill
  games/<platform>/<slug>/checkpoints.txt           named states as routes
  games/<platform>/<slug>/shots.txt                 the shot plan
  games/<platform>/<slug>/design/                   the design reference (README with notation, findings.md)
  work/intake/<platform>/<slug>/probe_NNNN.png + sheet.png    a frame every 60 frames from power-on, no input
Then: python3 tools/emu.py SLUG --seq "pow,w300,start" --out work/x  to find the boot inputs.
"""
import argparse, hashlib, json, os, re, shutil, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
sys.path.insert(0, HERE)
import platforms  # noqa: E402
import patch  # noqa: E402

TEMPLATE = os.path.join(ROOT, "games", "_template")


def slugify(s):
    s = re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
    return s or "game"


def region_of(info):
    """jp / na / eu from a header's "region" where it is certain, else None (GB "Overseas" and NES "NTSC" are not)."""
    r = info.get("region")
    if r == "Japan":
        return "jp"
    if r in ("North America", "Canada"):
        return "na"
    if r in ("PAL", "Europe", "Sweden/Scandinavia", "Finland", "Denmark", "France", "Netherlands", "Spain",
             "Germany", "Italy"):
        return "eu"
    return None


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("rom")
    ap.add_argument("--slug")
    ap.add_argument("--title", help="display title (default: header title)")
    ap.add_argument("--region", choices=["jp", "na", "eu"],
                    help="where the dump was released (default: from the header, where it says so)")
    ap.add_argument("--model", help="capture model override (gb: dmg|cgb|sgb|agb)")
    ap.add_argument("--probe", type=int, default=1800, help="frames to film after power-on (0 = skip)")
    ap.add_argument("--patch", action="append", default=[], metavar="PATCH[:LAYOUT]",
                    help="IPS/BPS/UPS patch to apply to ROM before registering (repeatable, in order)")
    a = ap.parse_args()

    data = open(a.rom, "rb").read()
    base, applied = data, []
    for spec in a.patch:
        path, _, layout = spec.partition(":")
        pdata = open(path, "rb").read()
        data, used, kind = patch.apply(data, pdata, os.path.splitext(a.rom)[1], layout or "auto")
        applied.append((path, pdata, used, kind))
        print("patched: %s (%s, %s layout)" % (os.path.basename(path), kind, used))
    pname, cls = platforms.by_extension(a.rom)
    info = cls.identify(data)
    platform = info.pop("platform", pname)
    model = a.model or info.pop("model", None)
    info.pop("model", None)
    slug = a.slug or slugify(info.get("header_title") or os.path.splitext(os.path.basename(a.rom))[0])
    if slug != slugify(slug):
        raise SystemExit("error: slug %r must be lowercase a-z0-9 words joined by `-` (e.g. %s)" % (slug, slugify(slug)))
    old = os.path.join(ROOT, "games", platform, slug, "game.json")
    region = a.region or (json.load(open(old, encoding="utf-8")).get("region") if os.path.exists(old) else None) \
        or region_of(info)
    if not region:
        raise SystemExit("error: the header does not say where this dump was released: add --region jp|na|eu "
                         "(a translated Japanese ROM is jp)")
    ext = os.path.splitext(a.rom)[1].lower()
    rom_rel = "rom/%s%s" % (slug, ext)
    os.makedirs(os.path.join(ROOT, "rom"), exist_ok=True)
    dst = os.path.join(ROOT, rom_rel)
    source = None
    if applied:
        open(dst, "wb").write(data)
        base_rel = "rom/src/%s-base%s" % (slug, ext)
        os.makedirs(os.path.join(ROOT, "rom", "src"), exist_ok=True)
        open(os.path.join(ROOT, base_rel), "wb").write(base)
        os.makedirs(os.path.join(ROOT, "rom", "patches", slug), exist_ok=True)
        source = {
            "note": "%s is the dump with the patches below applied in order. Rebuild: python3 tools/patch.py "
                    "%s %s %s. Nothing of this is committed." % (rom_rel, base_rel, rom_rel, " ".join(
                        "rom/patches/%s/%s:%s" % (slug, os.path.basename(p), u) for p, _, u, _ in applied)),
            "base_sha1": hashlib.sha1(base).hexdigest(),
            "base_name": os.path.basename(a.rom),
            "base_copy": base_rel,
            "patches": [],
        }
        for p, pdata, used, kind in applied:
            copy = "rom/patches/%s/%s" % (slug, os.path.basename(p))
            if os.path.abspath(p) != os.path.join(ROOT, copy):
                shutil.copyfile(p, os.path.join(ROOT, copy))
            source["patches"].append({"name": os.path.basename(p), "format": kind,
                                      "sha1": hashlib.sha1(pdata).hexdigest(), "copy": copy, "layout": used})
    elif os.path.abspath(a.rom) != os.path.abspath(dst):
        shutil.copyfile(a.rom, dst)

    gdir = os.path.join(ROOT, "games", platform, slug)       # the folder is the platform in game.json
    os.makedirs(gdir, exist_ok=True)
    gj = os.path.join(gdir, "game.json")
    if os.path.exists(gj):
        meta = json.load(open(gj, encoding="utf-8"))
        sha = hashlib.sha1(data).hexdigest()
        if meta.get("sha1") != sha:
            print("warning: games/%s/%s/game.json has SHA-1 %s, this ROM is %s (another revision?)" % (
                platform, slug, meta.get("sha1"), sha))
    else:
        meta = {
            "slug": slug,
            "title": a.title or info.get("header_title") or slug,
            "platform": platform,
            "region": region,
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
        if source:
            meta["source"] = source
        json.dump(meta, open(gj, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
        open(gj, "a").write("\n")
    for dirpath, _, files in os.walk(TEMPLATE):
        for f in files:
            src = os.path.join(dirpath, f)
            p = os.path.join(gdir, os.path.relpath(src, TEMPLATE))
            if not os.path.exists(p):
                os.makedirs(os.path.dirname(p), exist_ok=True)
                txt = open(src, encoding="utf-8").read()
                txt = txt.replace("{{TITLE}}", meta["title"]).replace("{{SLUG}}", slug).replace("{{PLATFORM}}", platform)
                open(p, "w", encoding="utf-8").write(txt)
    print(json.dumps({k: meta.get(k) for k in ("slug", "title", "platform", "region", "model", "sha1")}, indent=2))
    print("header:", json.dumps(meta["header"]))

    if a.probe:
        sys.path.insert(0, HERE)
        import emu
        g = emu.Game(platform + "/" + slug)
        out = os.path.join(ROOT, "work", "intake", platform, slug)
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
