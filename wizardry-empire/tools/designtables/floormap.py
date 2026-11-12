"""Draw a maze floor from the original ROM (Rev 1) as a PNG map, north up. Style: docs/design/maps/style-guide.md.

  python3 tools/designtables/floormap.py 1                 -> docs/design/maps/floor-01.png
  python3 tools/designtables/floormap.py 1 --list          also print every non-plain square (for the floor docs)

Cell format and square types: docs/tech/dungeon.md sections 1-2. Each floor is 16x16; (x, y) with x east, y north,
(0, 0) bottom left; the map wraps at the edges.
"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
CELL, PAD, TOP = 48, 30, 44     # cell size, left margin, space above the grid (title + subtitle)

# Palette (docs/design/maps/style-guide.md). Every symbol is a letter as well as a colour (readable without colour).
ROCK = (70, 70, 70)
FLOOR, NOFIGHT, GRID = (255, 255, 255), (228, 228, 228), (226, 226, 226)
WALL, DOOR, SPECIAL = (0, 0, 0), (170, 100, 30), (220, 0, 0)
DAMAGE, ANTIMAGIC, BOTHZONE = (232, 128, 128), (90, 110, 220), (160, 90, 190)
AREA_TXT, NOTE_TXT = (130, 130, 130), (90, 90, 90)
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
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", 15)
        small = ImageFont.truetype("DejaVuSans.ttf", 11)
        tfont = ImageFont.truetype("DejaVuSans-Bold.ttf", 17)
    except OSError:
        font = small = tfont = ImageFont.load_default()
    from collections import Counter
    count = Counter(a for (w, a, t, z, p) in cells.values() if a and t != 1)
    open_squares = sum(count.values())
    main_area = count.most_common(1)[0][0] if count else 0
    # one area covering >= 80% of the open squares: name it once and number only the exceptions
    mostly_one = bool(count) and count[main_area] * 5 >= open_squares * 4
    W = PAD + 16 * CELL + 10
    GRID_H = TOP + 16 * CELL
    LEG = 150
    im = Image.new("RGB", (W, GRID_H + 30 + LEG), (255, 255, 255))
    d = ImageDraw.Draw(im)

    def box(x, y):
        x0 = PAD + x * CELL
        y0 = TOP + (15 - y) * CELL
        return x0, y0, x0 + CELL, y0 + CELL

    def zone(x0, y0, z):
        if z in (1, 3):      # damage zone: diagonal hatch (both marks: purple)
            col = DAMAGE if z == 1 else BOTHZONE
            for k in range(-CELL, CELL, 7):
                d.line([x0 + max(0, k), y0 + max(0, -k), x0 + min(CELL, CELL + k), y0 + min(CELL, CELL - k)], fill=col)
        if z in (2, 3):      # anti-magic zone: dot grid (both marks: purple)
            col = ANTIMAGIC if z == 2 else BOTHZONE
            for k in range(5, CELL, 8):
                for j in range(5, CELL, 8):
                    d.rectangle([x0 + k, y0 + j, x0 + k + 1, y0 + j + 1], fill=col)

    d.text((PAD, 4), title, fill=(0, 0, 0), font=tfont)
    if not count:
        sub = "no random fights"
    elif mostly_one:
        sub = "random fights: encounter area %d%s" % (main_area, ", other areas numbered in grey" if len(count) > 1 else "")
    else:
        sub = "random fights: the encounter area of each square is numbered in grey"

    d.text((PAD, 25), sub, fill=NOTE_TXT, font=small)
    for (x, y), (w, a, t, z, p) in cells.items():
        x0, y0, x1, y1 = box(x, y)
        d.rectangle([x0, y0, x1, y1], fill=ROCK if t == 1 else (FLOOR if a else NOFIGHT), outline=ROCK if t == 1 else GRID)
        if t != 1:
            zone(x0, y0, z)
        if t != 1 and a and not (mostly_one and a == main_area):
            d.text((x0 + 3, y1 - 14), str(a), fill=AREA_TXT, font=small)
        lab = label(t, p)
        if lab:
            col = TYPES.get(t, ("", (0, 90, 160)))[1]
            d.text((x0 + 5, y0 + 6), lab, fill=col, font=font, stroke_width=2, stroke_fill=(255, 255, 255))
    for (x, y), (w, a, t, z, p) in cells.items():     # walls on top of the fills
        x0, y0, x1, y1 = box(x, y)
        sides = {0: (x0, y0, x1, y0), 1: (x1, y0, x1, y1), 2: (x0, y1, x1, y1), 3: (x0, y0, x0, y1)}
        for dd, (ax, ay, bx, by) in sides.items():
            v = (w >> (2 * dd)) & 3
            if v in (1, 2):
                d.line([ax, ay, bx, by], fill=WALL, width=3)
            if v == 2:      # door: a brown bar across the wall
                mx, my = (ax + bx) // 2, (ay + by) // 2
                if ay == by:
                    d.rectangle([mx - 9, my - 3, mx + 9, my + 3], fill=DOOR)
                else:
                    d.rectangle([mx - 3, my - 9, mx + 3, my + 9], fill=DOOR)
            elif v == 3:    # special wall: dashed red
                n = 6
                for k in range(0, n, 2):
                    d.line([ax + (bx - ax) * k // n, ay + (by - ay) * k // n,
                            ax + (bx - ax) * (k + 1) // n, ay + (by - ay) * (k + 1) // n], fill=SPECIAL, width=3)
    for i in range(16):
        d.text((PAD + i * CELL + CELL // 2 - 4, GRID_H + 4), str(i), fill=(0, 0, 0), font=small)
        d.text((8, TOP + (15 - i) * CELL + CELL // 2 - 6), str(i), fill=(0, 0, 0), font=small)
    d.text((PAD, GRID_H + 18), "x east ->   y north ^   (the map wraps at its edges)", fill=NOTE_TXT, font=small)
    # legend (always complete, so every map reads the same)
    ly = GRID_H + 38
    items = [("UP / DN", (0, 110, 0), "stairs up / down"), ("G", (190, 0, 0), "guarded square (fixed fight)"),
             ("H", (120, 60, 160), "hidden spot"), ("E", (0, 90, 160), "event (E1 = one-shot)"),
             ("B", (0, 90, 160), "button panel"), ("C", (90, 60, 30), "corpse")]
    for k, (lab, col, txt) in enumerate(items):
        cx = PAD + (k % 3) * 260
        cy = ly + (k // 3) * 20
        d.text((cx, cy), lab, fill=col, font=font)
        d.text((cx + 78, cy + 3), txt, fill=(0, 0, 0), font=small)
    d.text((PAD, ly + 40), "T..", fill=(200, 90, 0), font=font)
    d.text((PAD + 78, ly + 43), "floor trap: TP pit, TC chute, TF falling ceiling, TR rockfall, TV viper, TS spinner",
           fill=(0, 0, 0), font=small)
    cy = ly + 68
    d.line([PAD, cy + 7, PAD + 28, cy + 7], fill=WALL, width=3)
    d.text((PAD + 34, cy + 1), "wall", fill=(0, 0, 0), font=small)
    d.line([PAD + 90, cy + 7, PAD + 118, cy + 7], fill=WALL, width=3)
    d.rectangle([PAD + 95, cy + 4, PAD + 113, cy + 10], fill=DOOR)
    d.text((PAD + 124, cy + 1), "door", fill=(0, 0, 0), font=small)
    for k in range(0, 6, 2):
        d.line([PAD + 180 + 5 * k, cy + 7, PAD + 185 + 5 * k, cy + 7], fill=SPECIAL, width=3)
    d.text((PAD + 214, cy + 1), "special wall (probably a hidden door)", fill=(0, 0, 0), font=small)
    d.rectangle([PAD + 470, cy, PAD + 484, cy + 14], fill=ROCK)
    d.text((PAD + 490, cy + 1), "rock", fill=(0, 0, 0), font=small)
    cy += 24
    for k, (z, txt) in enumerate([(1, "damage zone"), (2, "anti-magic zone (inferred)"), (3, "both marks (no known effect)")]):
        x0 = PAD + k * 230
        d.rectangle([x0, cy, x0 + CELL, cy + 16], fill=FLOOR, outline=GRID)
        sub_im = Image.new("RGB", (CELL, CELL), FLOOR)
        dd2 = ImageDraw.Draw(sub_im)
        d2_save = d
        d = dd2
        zone(0, 0, z)
        d = d2_save
        im.paste(sub_im.crop((0, 0, CELL, 16)), (x0, cy))
        d.rectangle([x0, cy, x0 + CELL, cy + 16], outline=(160, 160, 160))
        d.text((x0 + CELL + 6, cy + 2), txt, fill=(0, 0, 0), font=small)
    cy += 24
    d.rectangle([PAD, cy, PAD + 14, cy + 14], fill=NOFIGHT, outline=GRID)
    d.text((PAD + 20, cy + 1), "grey square = no random fights", fill=NOTE_TXT, font=small)
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
