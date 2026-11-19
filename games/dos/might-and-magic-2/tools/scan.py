"""scan.py MAP [BASE_ROUTE] [--x]: visit every event square of one area and tile what happens.

  python3 games/dos/might-and-magic-2/tools/scan.py 00
  python3 games/dos/might-and-magic-2/tools/scan.py 0B "@middlegate,WARP:0B:08:08"

MAP is the area id in hex (00-3B, playbook "Areas"). BASE_ROUTE ends with the party in that area (default:
`@middlegate,WARP:MAP:08:08`; dark areas need Light first). The script plays BASE_ROUTE once, reads the area's
event table from memory (DS:6052 = physical 16852: triples square y*16+x, event number, facing mask
80 N / 40 E / 20 S / 10 W, ended by 00 00 00), then for every entry puts the party on the square facing the
first allowed direction (AT + facing one turn clockwise + `left`, which fires the event like a step) and
takes the frame after `w250`. Writes work/scout/might-and-magic-2/scan_MAP.png (labels: x,y facing event)
and prints one route per entry, ready for shots.txt.
"""
import os, sys
from multiprocessing import Pool
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "tools"))
GAME = "dos/might-and-magic-2"
TABLE = 0x16852
# facing to press `left` from, so that the turn ends facing the wanted direction
CW = {"N": "FE", "E": "FS", "S": "FW", "W": "FN"}


def play(route, peek=None):
    import emu as E
    g = E.Game(GAME)
    m, rest, _ = E.start(g, route)
    for tok in rest:
        if not E.step(m, g, tok):
            raise SystemExit("unknown token %r" % tok)
    img = m.image().convert("RGB").copy()
    data = bytes(m.peek(peek[0], peek[1])) if peek else None
    m.close()
    return img, data


def entries(raw):
    out = []
    for i in range(0, len(raw) - 2, 3):
        sq, ev, mask = raw[i], raw[i + 1], raw[i + 2]
        if sq == ev == mask == 0:
            break
        out.append((sq & 15, sq >> 4, ev, mask))
    return out


def job(a):
    label, route = a
    try:
        img, _ = play(route)
        return label, route, img
    except Exception as e:
        return label, route, None


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    mp = args[0].upper()
    base = args[1] if len(args) > 1 else "@middlegate,WARP:%s:08:08" % mp
    _, raw = play(base, (TABLE, 0x300))
    jobs = []
    for x, y, ev, mask in entries(raw):
        for bit, d in ((0x80, "N"), (0x40, "E"), (0x20, "S"), (0x10, "W")):
            if mask & bit:
                break
        route = "%s,AT:%02X:%02X,%s,left,w250" % (base, x, y, CW[d])
        jobs.append(("(%d,%d) %s ev%02X m%02X" % (x, y, d, ev, mask), route))
    with Pool(4) as pool:
        res = pool.map(job, jobs, chunksize=1)
    from PIL import Image, ImageDraw
    tiles = [(l, im if im.size == (320, 200) else im.resize((320, 200))) for l, r, im in res if im is not None]
    for l, r, im in res:
        print("%-24s %s" % (l, r if im is not None else "FAILED " + r))
    if not tiles:
        return
    cols = 5
    rows = (len(tiles) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * 320, rows * 212), (60, 0, 0))
    dr = ImageDraw.Draw(sheet)
    for i, (lab, im) in enumerate(tiles):
        px, py = (i % cols) * 320, (i // cols) * 212
        sheet.paste(im, (px, py + 12))
        dr.text((px + 2, py), lab, fill=(255, 255, 0))
    p = os.path.join(ROOT, "work", "scout", "might-and-magic-2", "scan_%s.png" % mp)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    sheet.save(p)
    print(p)


if __name__ == "__main__":
    main()
