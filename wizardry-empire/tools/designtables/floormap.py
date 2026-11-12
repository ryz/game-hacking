"""Draw a maze floor from the original ROM (Rev 1) as a PNG map, north up. Style: docs/design/maps/style-guide.md.

  python3 tools/designtables/floormap.py 1                 -> docs/design/maps/wizardry-empire-floor-01.png
  python3 tools/designtables/floormap.py 1 --list          also print every non-plain square (for the floor docs)
  python3 tools/designtables/floormap.py 1 --out PATH      write somewhere else (previews)

Cell format and square types: docs/tech/dungeon.md sections 1-2. Each floor is 16x16; (x, y) with x east, y north,
(0, 0) bottom left; the map wraps at the edges. Each edge is stored on both of its squares and the game only checks
the side of the square being left, so an edge that is open/door on one side and wall on the other is a one-way door.
"""
import os, sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
GAME = "Wizardry Empire"
PREFIX = "wizardry-empire-"

# ---- layout (px)
CELL = 48           # one square
MARGIN = 28         # outer margin of the image
AXIS = 22           # room for the axis numbers left of / under the grid
HEAD = 58           # title + subtitle above the grid
GRIDW = 16 * CELL

# ---- palette (docs/design/maps/style-guide.md); every symbol is a letter as well as a colour
INK = (0, 0, 0)
ROCK = (70, 70, 70)
FLOOR, NOFIGHT, GRID = (255, 255, 255), (228, 228, 228), (226, 226, 226)
WALL, DOOR, SPECIAL = INK, (170, 100, 30), (220, 0, 0)
DAMAGE, ANTIMAGIC, BOTHZONE = (232, 128, 128), (90, 110, 220), (160, 90, 190)
AREA_TXT, NOTE_TXT, RULE = (160, 160, 160), (95, 95, 95), (200, 200, 200)
GREEN, RED, PURPLE, BLUE, BROWN, ORANGE = (0, 110, 0), (190, 0, 0), (120, 60, 160), (0, 90, 160), (90, 60, 30), (200, 90, 0)
TEAL = (0, 125, 125)
# square type -> (label, colour)
TYPES = {2: ("UP", GREEN), 3: ("DN", GREEN), 4: ("H", PURPLE), 6: ("G", RED), 7: ("B", BLUE), 8: ("T", ORANGE), 9: ("W", TEAL),
         10: ("E", BLUE), 11: ("E", BLUE), 12: ("E", BLUE), 13: ("C", BROWN), 14: ("E1", BLUE)}
TRAPS = {0x00: "C", 0x20: "P", 0x40: "F", 0x60: "R", 0x80: "V", 0xA0: "S"}
STEP = {0: (0, 1), 1: (1, 0), 2: (0, -1), 3: (-1, 0)}     # side -> (dx, dy) in map coordinates (y north)


def warp_dest(rom, p):
    """Warp square param p -> (floor 1-30, x, y): table 20:6F94, 4 bytes [y][x][floor-1][0] (tech dungeon.md 2)."""
    o = 0x20 * 0x4000 + 0x2F94 + 4 * p
    return rom[o + 2] + 1, rom[o + 1], rom[o]


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
    if t == 8:
        return "T" + TRAPS.get(p & 0xE0, "?"), ORANGE
    if t in TYPES:
        return TYPES[t]
    if t >= 15:
        return "E", BLUE
    return "", None


class Painter:
    """Drawing primitives shared by the map and its legend, so both always look the same."""

    def __init__(self, d, fonts):
        self.d = d
        self.f = fonts

    def zone(self, x0, y0, size, z):
        d = self.d
        if z in (1, 3):      # damage zone: diagonal hatch (both marks: purple)
            col = DAMAGE if z == 1 else BOTHZONE
            for k in range(-size, size, 7):
                d.line([x0 + max(0, k), y0 + max(0, -k), x0 + min(size, size + k), y0 + min(size, size - k)], fill=col)
        if z in (2, 3):      # anti-magic zone: dot grid (both marks: purple)
            col = ANTIMAGIC if z == 2 else BOTHZONE
            for k in range(5, size, 8):
                for j in range(5, size, 8):
                    d.rectangle([x0 + k, y0 + j, x0 + k + 1, y0 + j + 1], fill=col)

    def symbol(self, cx, cy, text, col, font="sym"):
        """text centred on (cx, cy) with a white outline"""
        f = self.f[font]
        l, t, r, b = self.d.textbbox((0, 0), text, font=f, stroke_width=2)
        self.d.text((cx - (r - l) // 2 - l, cy - (b - t) // 2 - t), text, fill=col, font=f, stroke_width=2,
                    stroke_fill=(255, 255, 255))

    def wall(self, seg):
        self.d.line(seg, fill=WALL, width=3)

    def special(self, seg):
        ax, ay, bx, by = seg
        n = 6
        for k in range(0, n, 2):
            self.d.line([ax + (bx - ax) * k // n, ay + (by - ay) * k // n,
                         ax + (bx - ax) * (k + 1) // n, ay + (by - ay) * (k + 1) // n], fill=SPECIAL, width=3)

    def door(self, seg, one_way=None, col=DOOR):
        """bar across the wall (brown: door, red: locked door); one_way = side the party may pass towards (arrow)"""
        ax, ay, bx, by = seg
        mx, my = (ax + bx) // 2, (ay + by) // 2
        if col is not None:
            if ay == by:
                self.d.rectangle([mx - 9, my - 3, mx + 9, my + 3], fill=col)
            else:
                self.d.rectangle([mx - 3, my - 9, mx + 3, my + 9], fill=col)
        if one_way is not None:
            dx, dy = STEP[one_way][0], -STEP[one_way][1]          # screen y grows downwards
            tip = (mx + dx * 12, my + dy * 12)
            base = [(mx + dx * 3 - dy * 6, my + dy * 3 - dx * 6), (mx + dx * 3 + dy * 6, my + dy * 3 + dx * 6)]
            self.d.polygon([tip] + base, fill=INK)


def side_kind(cells, xy, dd):
    """What the party meets leaving square xy through side dd: open, wall, door, secret (special wall on a hidden
    spot: 'Ouch!' until the spot's flag is set) or locked (special wall elsewhere: 'It is locked.' until picked)."""
    v = (cells[xy][0] >> (2 * dd)) & 3
    if v == 3:
        return "secret" if cells[xy][2] == 4 else "locked"
    return ("open", "wall", "door")[v]


def edge(cells, xy, dd):
    """Classify the edge between xy and its neighbour in direction dd (both stored sides)."""
    n = ((xy[0] + STEP[dd][0]) & 15, (xy[1] + STEP[dd][1]) & 15)
    a, b = side_kind(cells, xy, dd), side_kind(cells, n, (dd + 2) % 4)
    free = ("open", "door")
    one_way = None
    if (a in free) != (b in free):
        one_way = dd if a in free else (dd + 2) % 4         # always passable this way
    return {"wall": (a, b) != ("open", "open"), "door": "door" in (a, b), "secret": "secret" in (a, b),
            "locked": "locked" in (a, b) and "secret" not in (a, b), "one_way": one_way, "sides": (a, b)}


def marker(d, x0, y0, size):
    """marker square: small grey dot in the middle of the cell"""
    c = size // 2
    d.ellipse([x0 + c - 2, y0 + c - 2, x0 + c + 2, y0 + c + 2], fill=NOTE_TXT)


def fonts():
    from PIL import ImageFont
    def f(name, size):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            return ImageFont.load_default()
    return {"title": f("DejaVuSans-Bold.ttf", 19), "sub": f("DejaVuSans.ttf", 12), "sym": f("DejaVuSans-Bold.ttf", 15),
            "small": f("DejaVuSans.ttf", 11), "head": f("DejaVuSans-Bold.ttf", 12), "text": f("DejaVuSans.ttf", 12)}


def draw(cells, out, floor):
    from PIL import Image, ImageDraw
    F = fonts()
    count = Counter(a for (w, a, t, z, p) in cells.values() if a and t != 1)
    main_area = count.most_common(1)[0][0] if count else 0
    mostly_one = bool(count) and count[main_area] * 5 >= sum(count.values()) * 4   # one area >= 80%: name it once
    if not count:
        sub = "No random fights on this floor."
    elif mostly_one:
        sub = "Random fights: encounter area %d%s." % (main_area, "; other areas numbered in grey" if len(count) > 1 else "")
    else:
        sub = "Random fights: the encounter area of each square is numbered in grey."

    gx, gy = MARGIN + AXIS, MARGIN + HEAD               # grid origin (top left)
    LEG_H = 270
    W = gx + GRIDW + MARGIN
    H = gy + GRIDW + AXIS + 12 + LEG_H + MARGIN
    im = Image.new("RGB", (W, H), (255, 255, 255))
    d = ImageDraw.Draw(im)
    P = Painter(d, F)

    # ---- header
    d.text((gx, MARGIN), "%s - Floor %d (B%dF)" % (GAME, floor, floor), fill=INK, font=F["title"])
    d.text((gx, MARGIN + 28), sub, fill=NOTE_TXT, font=F["sub"])

    def box(x, y):
        x0, y0 = gx + x * CELL, gy + (15 - y) * CELL
        return x0, y0, x0 + CELL, y0 + CELL

    # ---- squares
    for (x, y), (w, a, t, z, p) in cells.items():
        x0, y0, x1, y1 = box(x, y)
        rock = t == 1
        d.rectangle([x0, y0, x1, y1], fill=ROCK if rock else (FLOOR if a else NOFIGHT), outline=ROCK if rock else GRID)
        if rock:
            continue
        P.zone(x0, y0, CELL, z)
        if a and not (mostly_one and a == main_area):
            d.text((x0 + 3, y1 - 14), str(a), fill=AREA_TXT, font=F["small"])
        text, col = label(t, p)
        if text:
            P.symbol(x0 + CELL // 2, y0 + CELL // 2, text, col)

    # ---- edges: walls first, then secret doors, then doors and locked doors (arrow = the way that is always open)
    walls, specials, doors = [], [], []
    for (x, y), (w, a, t, z, p) in cells.items():
        x0, y0, x1, y1 = box(x, y)
        sides = {0: (x0, y0, x1, y0), 1: (x1, y0, x1, y1), 2: (x0, y1, x1, y1), 3: (x0, y0, x0, y1)}
        for dd, seg in sides.items():
            if dd in (2, 3):
                continue                                    # each edge once, from its south/west square
            n = ((x + STEP[dd][0]) & 15, (y + STEP[dd][1]) & 15)
            kind = edge(cells, (x, y), dd)
            if kind["wall"]:
                walls.append(seg)
            if kind["secret"]:
                specials.append(seg)
            if kind["door"] or kind["locked"] or kind["one_way"] is not None:
                doors.append((seg, kind["one_way"], SPECIAL if kind["locked"] else (DOOR if kind["door"] else None)))
    for seg in walls:
        P.wall(seg)
    for seg in specials:
        P.special(seg)
    for seg, one_way, col in doors:
        P.door(seg, one_way, col)
    d.rectangle([gx - 1, gy - 1, gx + GRIDW + 1, gy + GRIDW + 1], outline=INK, width=2)   # frame

    # ---- axes
    for i in range(16):
        l, t, r, b = d.textbbox((0, 0), str(i), font=F["small"])
        d.text((gx + i * CELL + (CELL - (r - l)) // 2, gy + GRIDW + 5), str(i), fill=INK, font=F["small"])
        d.text((gx - 8 - (r - l), gy + (15 - i) * CELL + (CELL - (b - t)) // 2 - t), str(i), fill=INK, font=F["small"])
    note = "x east →   y north ↑   (coordinates as in the game; the map wraps at its edges)"
    d.text((gx, gy + GRIDW + AXIS), note, fill=NOTE_TXT, font=F["small"])

    # ---- legend: three titled groups, every sample drawn with the map's own painter
    ly = gy + GRIDW + AXIS + 22
    d.line([gx, ly, gx + GRIDW, ly], fill=RULE, width=1)
    ly += 10
    colw = GRIDW // 3
    S = 26          # sample cell size

    def sample_cell(x, y, fill=FLOOR, zone=0, sym=None, col=None):
        d.rectangle([x, y, x + S, y + S], fill=fill, outline=(170, 170, 170))
        if zone:
            P.zone(x, y, S, zone)
        if sym:
            P.symbol(x + S // 2, y + S // 2, sym, col, font="head")

    def entry(x, y, text):
        d.text((x + S + 8, y + (S - 14) // 2), text, fill=INK, font=F["text"])

    groups = [
        ("Squares", [("UP", GREEN, "stairs up / DN down"), ("G", RED, "guarded square (fixed fight)"),
                     ("H", PURPLE, "hidden spot"), ("E", BLUE, "event (E1: one-shot)"),
                     ("B", BLUE, "button panel / C corpse"), ("W", TEAL, "warp (moves the party at once)"),
                     ("T", ORANGE, "floor trap (see below)")]),
        ("Walls and doors", ["wall", "door", "one-way door (arrow: way through)", "secret door (found by Search)",
                             "locked door (Pick a lock)"]),
        ("Floor and zones", ["rock", "no random fights", (1, "damage zone (lake)"), (2, "anti-magic zone (magic seal)"),
                             (3, "dark zone (no view)")]),
    ]
    for gi, (head, items) in enumerate(groups):
        x = gx + gi * colw
        d.text((x, ly), head, fill=INK, font=F["head"])
        y = ly + 20
        for item in items:
            if gi == 0:
                sym, col, text = item
                sample_cell(x, y, sym=sym, col=col)
            elif gi == 1:
                text = item
                sample_cell(x, y)
                seg = (x, y, x, y + S)                   # the sample's left edge; arrows point into the cell
                P.wall(seg)
                if text.startswith("door"):
                    P.door(seg)
                elif text.startswith("one-way"):
                    P.door(seg, one_way=1)
                elif text.startswith("locked"):
                    P.door(seg, col=SPECIAL)
                elif text.startswith("secret"):
                    d.line(seg, fill=(255, 255, 255), width=3)
                    P.special(seg)
            elif isinstance(item, str):
                text = item
                sample_cell(x, y, fill=ROCK if text == "rock" else NOFIGHT)
            else:
                z, text = item
                sample_cell(x, y, zone=z)
            entry(x, y, text)
            y += S + 6
    ty = ly + 20 + max(len(items) for _, items in groups) * (S + 6) - 2
    d.text((gx, ty), "Floor traps: TP pit, TC chute, TF falling ceiling, TR rockfall, TV viper, TS spinner.   "
                     "Grey number: encounter area of the square.", fill=NOTE_TXT, font=F["small"])
    os.makedirs(os.path.dirname(out), exist_ok=True)
    im.save(out)


def main(argv):
    f = int(argv[0])
    rom = open(os.path.join(ROOT, "rom", "wizardry_empire_j.gbc"), "rb").read()
    cells = floor_cells(rom, f)
    out = os.path.join(ROOT, "docs", "design", "maps", "%sfloor-%02d.png" % (PREFIX, f))
    if "--out" in argv:
        out = argv[argv.index("--out") + 1]
    draw(cells, out, f)
    print("wrote", os.path.relpath(out, ROOT) if out.startswith(ROOT) else out)
    if "--list" in argv:
        names = {1: "rock", 2: "stairs up", 3: "stairs down", 4: "hidden spot", 6: "guarded square", 7: "button panel",
                 8: "floor trap", 9: "warp", 10: "event A", 11: "event B", 12: "event C", 13: "corpse",
                 14: "one-shot event"}
        trap = {0x00: "chute", 0x20: "pit", 0x40: "falling ceiling", 0x60: "rockfall", 0x80: "viper", 0xA0: "spinner"}
        zones = {1: "damage zone (lake)", 2: "anti-magic zone (magic seal)", 3: "dark zone"}
        count = Counter(a for (w, a, t, z, p) in cells.values() if a and t != 1)
        print("rock squares: %d" % sum(1 for v in cells.values() if v[2] == 1))
        print("encounter areas (squares): " + ", ".join("%d (%d)" % kv for kv in sorted(count.items())))
        print("no-fight open squares: %d" % sum(1 for v in cells.values() if not v[1] and v[2] != 1))
        print("special squares (x,y): type, param, area, zone")
        for (x, y), (w, a, t, z, p) in sorted(cells.items(), key=lambda kv: (-kv[0][1], kv[0][0])):
            if t not in (0, 1, 5) or z:
                kind = names.get(t, "floor-specific event %d" % t if t >= 15 else "type %d" % t)
                if t == 8:
                    kind += " (%s, strength %d)" % (trap.get(p & 0xE0, "?"), p & 0x1F)
                if t == 9:
                    wf, wx, wy = warp_dest(rom, p)
                    kind += " to %s(%d,%d)" % ("" if wf == f else "floor %d " % wf, wx, wy)
                print("  (%d,%d): %s, param %d, area %d%s" % (x, y, kind, p, a, ", " + zones[z] if z else ""))
        diff = rom[0x20 * 0x4000 + 0x3100:][:128]       # 20:7100: difficulty per flag (x5), hidden spots and locks
        print("one-way doors (from -> to, direction; the other way is what the far side says):")
        dirs = "NESW"
        found = []
        for (x, y) in sorted(cells):
            for dd in (0, 1):
                k = edge(cells, (x, y), dd)
                n = ((x + STEP[dd][0]) & 15, (y + STEP[dd][1]) & 15)
                if k["one_way"] is not None:
                    a, b = ((x, y), n) if k["one_way"] == dd else (n, (x, y))
                    back = k["sides"][1] if k["one_way"] == dd else k["sides"][0]
                    print("  (%d,%d) -> (%d,%d) %s; back: %s" % (a + b + (dirs[k["one_way"]], back)))
                for side, sq in zip(k["sides"], ((x, y), n)):
                    if side in ("secret", "locked"):
                        found.append((side, sq, n if sq == (x, y) else (x, y), cells[sq][4]))
        print("secret and locked doors (seen from -> to, flag, difficulty = 5 x table value):")
        for side, sq, to, flag in found:
            what = "noticing difficulty (Search needs no roll)" if side == "secret" else "lock difficulty"
            print("  %s door (%d,%d) -> (%d,%d), flag %d, %s %d" % ((side,) + sq + to + (flag, what, 5 * diff[flag & 127])))
        print("doors (two-way): %d" % doors(cells))
        guards = {}
        for xy, (w, a, t, z, p) in sorted(cells.items()):
            if t == 6:
                guards.setdefault(p, []).append(xy)
        shared = [v for v in guards.values() if len(v) > 1]
        print("guarded squares sharing one once-per-visit mark: " +
              ("; ".join(" + ".join("(%d,%d)" % xy for xy in v) for v in shared) if shared else "none"))
        warps = {}
        for xy, (w, a_, t, z, p) in cells.items():
            if t == 9:
                wf, wx, wy = warp_dest(rom, p)
                if wf == f:
                    warps[xy] = (wx, wy)
        print("on foot from each stairs (one-way doors in their direction, warps followed; secret and locked doors shut / open):")
        for xy, (w, a, t, z, p) in sorted(cells.items()):
            if t in (2, 3):
                shut, opened = reach(cells, xy, False, warps), reach(cells, xy, True, warps)
                stairs = ["%s (%d,%d)" % ("up" if cells[s][2] == 2 else "down", s[0], s[1])
                          for s in sorted(shut) if s != xy and cells[s][2] in (2, 3)]
                print("  %s (%d,%d): %d / %d squares; other stairs reached: %s" % (
                    "up" if t == 2 else "down", xy[0], xy[1], len(shut), len(opened), ", ".join(stairs) or "none"))


def passable(cells, xy, dd, special):
    """Can the party leave square xy through side dd? Only the side being left counts (one-way doors)."""
    side = (cells[xy][0] >> (2 * dd)) & 3
    return side in (0, 2) or (special and side == 3)


def reach(cells, start, special=False, warps=None):
    """Squares reachable on foot from start (rock excluded); special=True treats secret and locked doors as open.
    warps = {(x, y): (x2, y2)} for warp squares leading elsewhere on the same floor: stepping on one moves the
    party there at once (the warp square counts as reached; the party cannot walk on from it)."""
    warps = warps or {}
    seen, todo = {start}, [start]
    while todo:
        x, y = todo.pop()
        for dd, (dx, dy) in STEP.items():
            n = ((x + dx) & 15, (y + dy) & 15)
            if n not in seen and cells[n][2] != 1 and passable(cells, (x, y), dd, special):
                seen.add(n)
                if cells[n][2] == 9:                 # warp: no walking on from it
                    d = warps.get(n)
                    if d is not None and d not in seen:
                        seen.add(d)
                        todo.append(d)
                    continue
                todo.append(n)
    return seen


def doors(cells):
    """Edges that are a door on both sides (one-way doors are listed separately)."""
    n = 0
    for (x, y), v in cells.items():
        for dd in (0, 1):                  # north and east: each edge once
            nx, ny = (x + STEP[dd][0]) & 15, (y + STEP[dd][1]) & 15
            if (v[0] >> (2 * dd)) & 3 == 2 and (cells[nx, ny][0] >> (2 * (dd + 2))) & 3 == 2:
                n += 1
    return n


if __name__ == "__main__":
    main(sys.argv[1:])
