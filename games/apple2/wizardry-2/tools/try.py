"""try.py FILE [--frames K] [--peek ADDR:LEN ...] [--text] [--out NAME] [--cols N] [--crop x0,y0,x1,y1]: run many candidate routes in parallel, one sheet.

  python3 games/apple2/wizardry-2/tools/try.py work/x/cand.txt --frames 2 --peek 6DCA:6

FILE holds lines `name | route` (emu.py tokens; `#` comments). Each route is played in its own process (as
tools/emu.py does, checkpoint cache included); the frames after the last K tokens are tiled into
work/scout/apple2/wizardry-2/try_NAME.png with the line's name as label, and the RAM blocks asked for with --peek are printed as hex
per line (after the last token); --text prints the 40x24 text screen instead (castle, shops, sheets). --crop keeps a part of every frame (x0,y0,x1,y1 in 280x192 pixels). Use it to pick waits and to compare variants; then put the route that works
into the set's shots.txt and shoot it with tools/shoot.py --only (frames can differ by a few on animations).
"""
import os, sys
from multiprocessing import Pool
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "tools"))

def run(job):
    import emu as E
    from PIL import Image
    name, route, k, peeks = job
    g = E.Game("apple2/wizardry-2")
    try:
        m, rest, _ = E.start(g, route)
        frames = []
        for i, tok in enumerate(rest):
            if not E.step(m, g, tok): return name, None, "unknown token %r" % tok
            if i >= len(rest) - k:
                frames.append(m.image().convert("RGB").copy() if hasattr(m, "image") else None)
        if peeks and peeks[0][0] == "text":
            mem = bytes(m.peek(0x400, 0x400)); rows = []
            for r in range(24):
                b = 0x80 * (r % 8) + 0x28 * (r // 8)
                rows.append("".join(chr(c & 0x7F) if 32 <= (c & 0x7F) < 127 else chr((c & 0x3F) + 64) if (c & 0x7F) < 32 else " " for c in mem[b:b + 40]).rstrip())
            while rows and not rows[-1]: rows.pop()
            m.close(); return name, frames, "\n    |" + "\n    |".join(rows)
        pk = " ".join("%s=%s" % (a, bytes(m.peek(int(a, 16), n)).hex()) for a, n in peeks)
        m.close()
        return name, frames, pk
    except Exception as e:
        return name, None, "ERROR %r" % (e,)

def main():
    a = sys.argv[1:]; k = 1; peeks = []; out = None; cols = 4; crop = None
    while "--crop" in a: i = a.index("--crop"); crop = tuple(int(v) for v in a[i + 1].split(",")); del a[i:i + 2]
    while "--frames" in a: i = a.index("--frames"); k = int(a[i + 1]); del a[i:i + 2]
    while "--cols" in a: i = a.index("--cols"); cols = int(a[i + 1]); del a[i:i + 2]
    while "--out" in a: i = a.index("--out"); out = a[i + 1]; del a[i:i + 2]
    if "--text" in a: a.remove("--text"); peeks.append(("text", 0))
    while "--peek" in a:
        i = a.index("--peek"); ad, n = a[i + 1].split(":"); peeks.append((ad, int(n))); del a[i:i + 2]
    jobs = []
    for line in open(a[0]):
        line = line.strip()
        if not line or line.startswith("#"): continue
        p = [x.strip() for x in line.split("|")]
        jobs.append((p[0], p[-1], k, peeks))
    with Pool(4) as pool: res = pool.map(run, jobs, chunksize=1)
    from PIL import Image, ImageDraw
    tiles = []
    for name, frames, pk in res:
        print("%-28s %s" % (name, pk if frames is not None else pk))
        for j, f in enumerate(frames or []):
            if f is not None: tiles.append(("%s%s" % (name, "" if k == 1 else " #%d" % (j + 1)), f))
    if not tiles: return
    tiles = [(l, im if im.size == (280, 192) else im.resize((280, 192))) for l, im in tiles]
    if crop: tiles = [(l, im.crop(crop)) for l, im in tiles]
    w, h = tiles[0][1].size; rows = (len(tiles) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * w, rows * (h + 12)), (60, 0, 0)); dr = ImageDraw.Draw(sheet)
    for i, (lab, im) in enumerate(tiles):
        px, py = (i % cols) * w, (i // cols) * (h + 12)
        sheet.paste(im, (px, py + 12)); dr.text((px + 2, py), lab[:50], fill=(255, 255, 0))
    p = os.path.join(ROOT, "work", "scout", "apple2", "wizardry-2", "try_%s.png" % (out or os.path.splitext(os.path.basename(a[0]))[0]))
    os.makedirs(os.path.dirname(p), exist_ok=True); sheet.save(p); print(p)

if __name__ == "__main__":
    main()
