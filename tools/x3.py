"""Enlarged copies of shots, on demand (owner's rule 2026-11-20: sets hold native pictures only).

  python3 tools/x3.py games/nes/wizardry/shots/main            every PNG and GIF of the folder -> <folder>/3x/
  python3 tools/x3.py FILE.png FILE.gif ...                    single files -> 3x/ next to each
  python3 tools/x3.py FOLDER --scale 2 --out work/big          another factor, another folder

Nearest neighbour, integer factor (default 3), same file names; GIFs keep their frame timing. The `3x/`
folders of the database sets are ignored by git (.gitignore): make them where you need them, do not commit them.
"""
import argparse, os, sys


def enlarge(src, dst, scale):
    from PIL import Image, ImageSequence
    os.makedirs(os.path.dirname(dst) or ".", exist_ok=True)
    im = Image.open(src)
    if src.lower().endswith(".gif"):
        frames, durs = [], []
        for f in ImageSequence.Iterator(im):
            durs.append(f.info.get("duration", 33))
            f = f.convert("RGB")
            frames.append(f.resize((f.width * scale, f.height * scale), Image.NEAREST).convert(
                "P", palette=Image.ADAPTIVE, colors=256))
        frames[0].save(dst, save_all=True, append_images=frames[1:], duration=durs, loop=0, optimize=False,
                       disposal=1)
    else:
        im = im.convert("RGB")
        im.resize((im.width * scale, im.height * scale), Image.NEAREST).save(dst)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--scale", type=int, default=3)
    ap.add_argument("--out")
    a = ap.parse_args(argv)
    n = 0
    for p in a.paths:
        files = sorted(os.path.join(p, f) for f in os.listdir(p)) if os.path.isdir(p) else [p]
        for f in files:
            if os.path.isfile(f) and f.lower().endswith((".png", ".gif")):
                out = a.out or os.path.join(os.path.dirname(f), "%dx" % a.scale)
                enlarge(f, os.path.join(out, os.path.basename(f)), a.scale)
                n += 1
    print("%d file(s) enlarged %dx" % (n, a.scale))
    return 0


if __name__ == "__main__":
    sys.exit(main())
