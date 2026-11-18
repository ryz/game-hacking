"""Might and Magic (NES) map renderer.

Maps: 55 slots of 0x200 bytes from file offset 0x32010 (PRG 8 KiB bank 25 at $8000.. onwards):
  +0x000 wall map, 256 bytes, cell index y*16+x (x east, y north, (0,0) south-west).
         byte = N<<6 | E<<4 | S<<2 | W: 0 open, 1 wall, 2 door, 3 map-type specific (ornament / trees / water...)
  +0x100 property map, 256 bytes: 80 event, 40 blocked N, 20 dark, 10 blocked E, 08 no camp,
         04 blocked S, 02 anti-magic, 01 blocked W (Data Crystal flag names; bit order checked against walls).
RAM: current map $6200 (walls), $6300 (properties); map id $009E = slot + 1; x $009F, y $00A0, y*16+x $00A1,
facing $00A2 (0 N, 1 E, 2 S, 3 W).

usage: python3 games/might-and-magic/tools/maps.py [--rom ROM] [--out DIR] [--text]
Files: NN_name.png with NN = area id in hex (01-37); varn_atlas.png; maps.txt; exits: exits(rom).
"""
import argparse, os, sys
from PIL import Image, ImageDraw

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
BASE = 0x32010
NAMES = ["Sorpigal", "Portsmith", "Algary", "Dusk", "Erliquin",
         "Sorpigal Cavern", "C2 Cave", "Portsmith Cavern", "Erliquin Cavern", "Dusk Cavern",
         "Korin Bluffs", "Volcano", "Square Puzzle Cave", "White Wolf Cave"] + \
        ["Varn %s%d" % (c, r) for c in "ABCDE" for r in (1, 2, 3, 4)] + \
        ["Castle Doom", "Castle White Wolf", "Castle Alamar", "Castle Blackridge North",
         "Castle Blackridge South", "Castle Dragadune", "Dragadune Dungeon 1", "Dragadune Dungeon 2",
         "Dragadune Dungeon 3", "Enchanted Forest F1", "Enchanted Forest F2", "Wizard's Lair F1",
         "Wizard's Lair F2", "Raven's Wood F1", "Raven's Wood F2", "City of Gold F1", "City of Gold F2",
         "City of Gold F3", "City of Gold F4", "Astral Plane", "Soul Maze"]
BLOCK = {0: 0x40, 1: 0x10, 2: 0x04, 3: 0x01}
C = 20  # pixels per cell
OUTDOOR = range(14, 34)                 # slots of VARN A1..E4 (area ids 0F-22)
DESERT = {0x1B, 0x1C, 0x1F, 0x20}       # area ids whose type 3 is desert (orange sky), elsewhere water (verified D1)
# Outdoor side types (verified by walking into them, see design/maps.md): 1 forest ("Too dense!" where blocked),
# 2 mountains ("Impassable!"), 3 water ("Cannot swim!") or desert ("It's hot... You're lost!!!", passable).
TERRAIN = {1: (40, 140, 40), 2: (130, 100, 70), 3: (60, 110, 220)}
SAND = (225, 180, 90)


def exits(rom):
    """Warps coded in the area scripts: list of (from_area, to_area, x, y) - the arrival square in to_area.
    Area script = entry E of bank B (JMP table at $8000), pairs (B, E) per area at bank 29 $A1B7; a warp is
    LDA #area STA $9D LDA #x STA $9F LDA #y STA $A0."""
    prg = rom[16:]
    t = 29 * 0x2000 + 0x01B7
    def jmp(b, e):
        o = b * 0x2000 + e * 3
        return prg[o + 1] | prg[o + 2] << 8
    out = []
    for a in range(1, 0x38):
        b, e = prg[t + 2 * (a - 1)], prg[t + 2 * (a - 1) + 1]
        d = prg[b * 0x2000:(b + 1) * 0x2000]
        start = jmp(b, e)
        starts = sorted(set(jmp(b, k) for k in range(12) if d[k * 3] == 0x4C))
        end = min([s for s in starts if s > start] + [0xA000])
        for i in range(start - 0x8000, end - 0x8000 - 10):
            if d[i] == 0xA9 and d[i + 2:i + 4] == b"\x85\x9d" and d[i + 4] == 0xA9 and d[i + 6:i + 8] == b"\x85\x9f" \
                    and d[i + 8] == 0xA9 and d[i + 10:i + 12] == b"\x85\xa0" and 1 <= d[i + 1] <= 0x37:
                if d[i + 5] < 16 and d[i + 9] < 16:
                    out.append((a, d[i + 1], d[i + 5], d[i + 9]))
    return out


def load(rom, slot):
    o = BASE + slot * 0x200
    return rom[o:o + 256], rom[o + 256:o + 512]


def render(walls, props, title, area=0, arrivals=()):
    W = 16 * C + 40
    im = Image.new("RGB", (W, W + 16), (255, 255, 255))
    outdoor = 0x0F <= area <= 0x22
    d = ImageDraw.Draw(im)
    ox, oy = 24, 16
    d.text((4, 2), title, fill=(0, 0, 0))
    for y in range(16):
        for x in range(16):
            i = y * 16 + x
            b, p = walls[i], props[i]
            x0, y0 = ox + x * C, oy + (15 - y) * C
            if p & 0x20:
                d.rectangle([x0, y0, x0 + C, y0 + C], fill=(200, 200, 200))
            sides = {(b >> (6 - 2 * s)) & 3 for s in range(4)}
            if outdoor and len(sides) == 1 and 0 not in sides:   # a square surrounded by one terrain: fill it
                v = sides.pop()
                d.rectangle([x0, y0, x0 + C, y0 + C], fill=SAND if v == 3 and area in DESERT else TERRAIN[v])
            if p & 0x80:
                d.rectangle([x0 + 6, y0 + 6, x0 + C - 6, y0 + C - 6], fill=(220, 40, 40))
            if p & 0x02:
                d.text((x0 + 2, y0 + 1), "a", fill=(0, 0, 200))
            seg = {0: ((x0, y0), (x0 + C, y0)), 1: ((x0 + C, y0), (x0 + C, y0 + C)),
                   2: ((x0, y0 + C), (x0 + C, y0 + C)), 3: ((x0, y0), (x0, y0 + C))}
            for s in range(4):
                v = (b >> (6 - 2 * s)) & 3
                blk = bool(p & BLOCK[s])
                if v == 0 and not blk:
                    continue
                (a1, a2) = seg[s]
                col = {0: (120, 0, 160), 1: (0, 0, 0), 2: (150, 90, 0), 3: (0, 120, 0)}[v]
                if outdoor and v:
                    col = SAND if v == 3 and area in DESERT else TERRAIN[v]
                if blk:
                    d.line([a1, a2], fill=col, width=3)
                else:  # passable door / opening with a wall graphic
                    mx, my = (a1[0] + a2[0]) // 2, (a1[1] + a2[1]) // 2
                    d.line([a1, a2], fill=col, width=1)
                    d.rectangle([mx - 2, my - 2, mx + 2, my + 2], fill=col)
        d.text((4, oy + (15 - y) * C + 5), "%X" % y, fill=(100, 100, 100))
    for src, x, y in arrivals:   # arrival square of a warp coded in area `src`'s script
        x0, y0 = ox + x * C, oy + (15 - y) * C
        d.ellipse([x0 + 3, y0 + 3, x0 + C - 3, y0 + C - 3], outline=(0, 90, 200), width=2)
        d.text((x0 + 4, y0 + 4), "%02X" % src, fill=(0, 60, 160))
    for x in range(16):
        d.text((ox + x * C + 7, oy + 16 * C + 2), "%X" % x, fill=(100, 100, 100))
    return legend(im, outdoor, area in DESERT)


def legend(im, outdoor, desert):
    """Append a legend strip under a render."""
    rows = [((0, 0, 0), "wall"), ((150, 90, 0), "door (box = passable)"), ((0, 120, 0), "ornament (type 3)"),
            ((120, 0, 160), "invisible barrier"), ((220, 40, 40), "event square"), ((200, 200, 200), "dark"),
            ((0, 90, 200), "arrival from area NN (exit)")]
    if outdoor:
        rows = [((0, 0, 0), "edge / wall"), (TERRAIN[1], "forest"), (TERRAIN[2], "mountains"),
                (SAND if desert else TERRAIN[3], "desert" if desert else "water"), ((220, 40, 40), "event square"),
                ((0, 90, 200), "arrival from area NN (exit)")]
    W, H = im.size
    out = Image.new("RGB", (W, H + 14 * ((len(rows) + 1) // 2) + 6), (255, 255, 255))
    out.paste(im, (0, 0))
    d = ImageDraw.Draw(out)
    for k, (col, txt) in enumerate(rows):
        x, y = 4 + (k % 2) * (W // 2), H + 4 + 14 * (k // 2)
        d.rectangle([x, y + 2, x + 10, y + 10], fill=col)
        d.text((x + 14, y), txt, fill=(0, 0, 0))
    return out


def header_name(rom, slot):
    """Area name from the 78-byte map header at 0x38E7E + 0x4E*slot (game text: 0-9, A-Z = 0A-23, a-z = 40-59)."""
    o = 0x38E7E + slot * 0x4E
    out = ""
    for b in rom[o:o + 13]:
        if b == 0xFF:
            break
        out += (str(b) if b < 10 else chr(55 + b) if b < 0x24 else chr(b + 0x21) if 0x40 <= b < 0x5A
                else " " if b == 0xFE else ":" if b == 0x2C else "-" if b == 0x26 else "?")
    return out.strip()


def text(walls, props):
    out = []
    for y in range(15, -1, -1):
        out.append(" ".join("%02X.%02X" % (walls[y * 16 + x], props[y * 16 + x]) for x in range(16)))
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rom", default=os.path.join(ROOT, "rom", "might-and-magic.nes"))
    ap.add_argument("--out", default=os.path.join(ROOT, "games", "might-and-magic", "design", "maps"))
    ap.add_argument("--text", action="store_true")
    a = ap.parse_args()
    rom = open(a.rom, "rb").read()
    os.makedirs(a.out, exist_ok=True)
    txt = []
    arr = {}
    for src, dst, x, y in exits(rom):
        arr.setdefault(dst, set()).add((src, x, y))
    for f in os.listdir(a.out):
        if f.endswith(".png") and f[:2].isalnum() and f[2] == "_":
            os.remove(os.path.join(a.out, f))
    for slot, name in enumerate(NAMES):
        w, p = load(rom, slot)
        fn = "%02X_%s.png" % (slot + 1, name.lower().replace("'", "").replace(" ", "_"))
        render(w, p, "%02X %s" % (slot + 1, name), slot + 1, sorted(arr.get(slot + 1, ()))).save(os.path.join(a.out, fn))
        if a.text:
            txt.append("## %02X %s - in-game label \"%s\" (slot %d, file 0x%05X)\n%s\n"
                       % (slot + 1, name, header_name(rom, slot), slot, BASE + slot * 0x200, text(w, p)))
    # overworld atlas: sector letters A..E are columns (west -> east), numbers 1..4 rows (north -> south).
    # Chosen from the data: neighbouring edges agree 219/256 (E-W) and 215/240 (N-S) this way, ~25% the other way.
    # Confirmed by walking (2026-11-18): B2 south edge -> B3, B3 east edge -> C3, C3 east edge -> D3.
    tiles = [render(*load(rom, 14 + c * 4 + r), "Varn %s%d" % ("ABCDE"[c], r + 1), 15 + c * 4 + r,
                    sorted(arr.get(15 + c * 4 + r, ()))) for r in range(4) for c in range(5)]
    tw, th = tiles[0].size
    atlas = Image.new("RGB", (tw * 5, th * 4), (255, 255, 255))
    for i, t in enumerate(tiles):
        atlas.paste(t, ((i % 5) * tw, (i // 5) * th))
    atlas.save(os.path.join(a.out, "varn_atlas.png"))
    if a.text:
        open(os.path.join(a.out, "maps.txt"), "w").write("\n".join(txt))
    print("wrote", len(NAMES), "maps to", a.out)


if __name__ == "__main__":
    main()
