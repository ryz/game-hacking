"""Draw a maze floor from the original ROM (Rev 1) as a PNG map, north up.

  python3 tools/designtables/floormap.py 1                 -> docs/design/maps/floor-01.png
  python3 tools/designtables/floormap.py 1 --list          also print every non-plain square (for the floor docs)

Cell format and square types: docs/tech/dungeon.md sections 1-2. Each floor is 16x16; (x, y) with x east, y north,
(0, 0) bottom left; the map wraps at the edges.
"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
CELL, PAD = 36, 26

AREA_TINT = [(232, 232, 232), (206, 224, 247), (212, 238, 208), (250, 238, 200), (240, 214, 230), (220, 214, 245),
             (210, 240, 240), (245, 222, 205)]
ROCK = (70, 70, 70)
# square type -> (label, colour)
TYPES = {2: ("UP", (0, 110, 0)), 3: ("DN", (0, 110, 0)), 4: ("H", (120, 60, 160)), 6: ("G", (190, 0, 0)),
         7: ("B", (0, 90, 160)), 8: ("T", (200, 90, 0)), 9: ("·", (90, 90, 90)), 10: ("E", (0, 90, 160)),
         11: ("E", (0, 90, 160)), 12: ("E", (0, 90, 160)), 13: ("C", (90, 60, 30)), 14: ("E1", (0, 90, 160))}
TRAP = {0x00: "chute", 0x20: "pit", 0x40: "ceiling", 0x60: "rockfall", 0x80: "viper", 0xA0: "spinner"}


def floor_cells(rom, f):
    """f = 1..30 -> {(x, y): (walls, area, type, zone, param)}"""
    i = f - 1
    off = (0x3E + (i >> 4)) * 0x4000 + 0x400 * (i & 15)
    m = rom[off:off + 0x400]
    out = {}
    for y in range(16):
        for x in range(16):
            c = m[(((y ^ 15) << 4) | x) * 4:][:4]
            out[x, y] = (c[0], c[1], c[2] & 0x3F, c[2] >> 6, c[3])
    return out


def label(t, p):
    if t in TYPES:
        lab = TYPES[t][0]
        if t == 8:
            lab = "T" + {0x00: "C", 0x20: "P", 0x40: "F", 0x60: "R", 0x80: "V", 0xA0: "S"}.get(p & 0xE0, "?")
        return lab
    if t >= 15:
        return "E"
    return ""


def draw(cells, out, title):
    from PIL import Image, ImageDraw, ImageFont
    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", 12)
        small = ImageFont.truetype("DejaVuSans.ttf", 9)
    except OSError:
        font = small = ImageFont.load_default()
    W = PAD + 16 * CELL + 8
    H = PAD + 16 * CELL + PAD + 4
    LEG = 100
    im = Image.new("RGB", (W, H + 16 + LEG), (255, 255, 255))
    d = ImageDraw.Draw(im)
    def box(x, y):
        x0 = PAD + x * CELL
        y0 = 18 + (15 - y) * CELL
        return x0, y0, x0 + CELL, y0 + CELL
    d.text((PAD, 2), title, fill=(0, 0, 0), font=font)
    for (x, y), (w, a, t, z, p) in cells.items():
        x0, y0, x1, y1 = box(x, y)
        fill = ROCK if t == 1 else ((255, 255, 255) if a else (225, 225, 225))
        d.rectangle([x0, y0, x1, y1], fill=fill)
        if z == 1:      # damage zone: red hatch
            for k in range(-CELL, CELL, 6):
                d.line([x0 + max(0, k), y0 + max(0, -k), x0 + min(CELL, CELL + k), y0 + min(CELL, CELL - k)], fill=(230, 120, 120))
        if z == 2:      # anti-magic zone: blue dots
            for k in range(4, CELL, 8):
                for j in range(4, CELL, 8):
                    d.point((x0 + k, y0 + j), fill=(60, 60, 200))
        if t != 1 and a:
            d.text((x0 + 2, y1 - 11), str(a), fill=(120, 120, 120), font=small)
        lab = label(t, p)
        if lab:
            col = TYPES.get(t, ("", (0, 90, 160)))[1]
            d.text((x0 + 4, y0 + 8), lab, fill=col, font=font)
    # walls on top of the fills
    for (x, y), (w, a, t, z, p) in cells.items():
        x0, y0, x1, y1 = box(x, y)
        sides = {0: (x0, y0, x1, y0), 1: (x1, y0, x1, y1), 2: (x0, y1, x1, y1), 3: (x0, y0, x0, y1)}
        for dd, (ax, ay, bx, by) in sides.items():
            v = (w >> (2 * dd)) & 3
            if v == 1:
                d.line([ax, ay, bx, by], fill=(0, 0, 0), width=3)
            elif v == 2:    # door: wall with a brown gap
                d.line([ax, ay, bx, by], fill=(0, 0, 0), width=3)
                mx, my = (ax + bx) // 2, (ay + by) // 2
                if ay == by:
                    d.rectangle([mx - 7, my - 3, mx + 7, my + 3], fill=(170, 100, 30))
                else:
                    d.rectangle([mx - 3, my - 7, mx + 3, my + 7], fill=(170, 100, 30))
            elif v == 3:    # special wall: dashed red
                n = 6
                for k in range(0, n, 2):
                    d.line([ax + (bx - ax) * k // n, ay + (by - ay) * k // n,
                            ax + (bx - ax) * (k + 1) // n, ay + (by - ay) * (k + 1) // n], fill=(220, 0, 0), width=3)
    for i in range(16):
        d.text((PAD + i * CELL + CELL // 2 - 4, 18 + 16 * CELL + 4), str(i), fill=(0, 0, 0), font=small)
        d.text((6, 18 + (15 - i) * CELL + CELL // 2 - 5), str(i), fill=(0, 0, 0), font=small)
    d.text((PAD, 18 + 16 * CELL + 16), "x east ->   y north ^   (map wraps at the edges)", fill=(90, 90, 90), font=small)
    ly = 18 + 16 * CELL + 34
    items = [("UP / DN", (0, 110, 0), "stairs up / down"), ("G", (190, 0, 0), "guarded square (fixed fight)"),
             ("H", (120, 60, 160), "hidden spot"), ("E", (0, 90, 160), "event (E1 = one-shot)"),
             ("B", (0, 90, 160), "button panel"), ("C", (90, 60, 30), "corpse")]
    for k, (lab, col, txt) in enumerate(items):
        cx = PAD + (k % 3) * 200
        cy = ly + (k // 3) * 16
        d.text((cx, cy), lab, fill=col, font=font)
        d.text((cx + 64, cy + 2), txt, fill=(0, 0, 0), font=small)
    d.text((PAD, ly + 32), "T..", fill=(200, 90, 0), font=font)
    d.text((PAD + 64, ly + 34), "floor trap: TP pit, TC chute, TF falling ceiling, TR rockfall, TV viper, TS spinner",
           fill=(0, 0, 0), font=small)
    cy = ly + 54
    d.line([PAD, cy + 6, PAD + 24, cy + 6], fill=(0, 0, 0), width=3); d.text((PAD + 30, cy), "wall", fill=(0, 0, 0), font=small)
    d.line([PAD + 80, cy + 6, PAD + 104, cy + 6], fill=(0, 0, 0), width=3)
    d.rectangle([PAD + 85, cy + 3, PAD + 99, cy + 9], fill=(170, 100, 30)); d.text((PAD + 110, cy), "door", fill=(0, 0, 0), font=small)
    for k in range(0, 6, 2):
        d.line([PAD + 160 + 4 * k, cy + 6, PAD + 164 + 4 * k, cy + 6], fill=(220, 0, 0), width=3)
    d.text((PAD + 190, cy), "special wall (probably a hidden door)", fill=(0, 0, 0), font=small)
    d.rectangle([PAD + 400, cy, PAD + 412, cy + 12], fill=ROCK); d.text((PAD + 418, cy), "rock", fill=(0, 0, 0), font=small)
    d.text((PAD, cy + 18), "small grey number = encounter area of the square; grey square = no random fights", fill=(90, 90, 90), font=small)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    im.save(out)


def main(argv):
    f = int(argv[0])
    rom = open(os.path.join(ROOT, "rom", "wizardry_empire_j.gbc"), "rb").read()
    cells = floor_cells(rom, f)
    out = os.path.join(ROOT, "docs", "design", "maps", "floor-%02d.png" % f)
    draw(cells, out, "Floor %d (B%dF)" % (f, f))
    print("wrote", os.path.relpath(out, ROOT))
    if "--list" in argv:
        for (x, y), (w, a, t, z, p) in sorted(cells.items(), key=lambda kv: (-kv[0][1], kv[0][0])):
            if t not in (0, 1, 5) or z:
                print("(%d,%d) type %d zone %d area %d param %d" % (x, y, t, z, a, p))


if __name__ == "__main__":
    main(sys.argv[1:])
