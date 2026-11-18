"""Dungeon Magic floor maps and overworld atlas, drawn from the ROM (no emulator needed).

Writes into OUT (default games/nes/dungeon-magic/design/maps/):
  map_XX.png   one per town (00-05), forest floor (40-48) and dungeon/castle floor (80-97), 16x16 squares:
               walls, gates/exits to the field (OUT), stairs to other floors (arrow + floor id), shop/inn/wizard
               doors in towns (W weapons, I items, N inn, M wizard + element), other feature bits as small dots.
  overworld.png  the 64x96 overworld (surface 64x64 + lower region 64x32) with towns, castle and dungeon
               entrances labelled, and the 16x16 section grid with section ids.
  atlas.png    all floors on one sheet.
  maps.json    the decoded exit tables (for design/maps.md and warps).

Data (playbook "Map data"): floor XX = 256 bytes at PRG bank XX>>5, CPU $A000 + (XX & $1F) * $100. Cell low nibble =
walls (1 N, 2 E, 4 S, 8 W). Exit tables at $BA00 of the same bank: towns 8 bytes per map (pointers to a door list,
door types, exit squares, exit records), other banks 4 bytes per map (exit squares, exit records). Exit record =
[type 10 field / 14, 16 or 18 stairs, target map, target square, -, overworld pointer lo, hi, -, -].
Overworld: bank 1 $A000, 64 cells per row; high nibble terrain, xF = a place (1F town, 0F castle, others dungeons).

usage: python3 games/nes/dungeon-magic/tools/atlas.py [--out DIR]
"""
import argparse, json, os
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
ROM = os.path.join(HERE, "../../../../rom/dungeon-magic.nes")
TOWNS = list(range(0x00, 0x06))
FOREST = list(range(0x40, 0x49))
DUNGEON = list(range(0x80, 0x98))
ALL = TOWNS + FOREST + DUNGEON
DOOR = {0x04: "W", 0x06: "I", 0x0A: "N", 0x08: "M"}
# wizard schools seen in play (capture 2026-11-18); others not visited
SCHOOL = {(0x00, 0x34): "Ea", (0x00, 0x38): "Wa", (0x00, 0x6C): "Fi", (0x00, 0xBC): "Wi", (0x00, 0xC6): "Fa",
          (0x01, 0xB4): "Fi", (0x02, 0xC4): "Wa", (0x05, 0xD3): "Wi"}

D = None


def prg(bank, addr, n):
    o = bank * 0x4000 + (addr - 0x8000)
    return D[o:o + n]


def word(bank, addr):
    b = prg(bank, addr, 2)
    return b[0] | b[1] << 8


def floor(mid):
    return prg(mid >> 5, 0xA000 + (mid & 0x1F) * 0x100, 256)


def table_pointers(bank):
    """Every pointer of the bank's exit table ($BA00), to bound each list."""
    if bank == 0:
        return [word(0, 0xBA00 + t * 8 + i) for t in range(6) for i in (0, 2, 4, 6)]
    ids = [m for m in ALL if m >> 5 == bank]
    return [word(bank, 0xBA00 + (m & 0x1F) * 4 + i) for m in ids for i in (0, 2)]


def exits(mid):
    """[(square, type, target map, target square, overworld pointer)], doors [(square, type)]"""
    bank = mid >> 5
    if bank == 0:
        base = 0xBA00 + (mid & 0xF) * 8
        p30, p32, p34, p36 = (word(0, base + i) for i in (0, 2, 4, 6))
        n = 4
        doors = [(s, t) for s, t in zip(prg(0, p30, 8), prg(0, p32, 8)) if t in DOOR]
    else:
        base = 0xBA00 + (mid & 0x1F) * 4
        p34, p36 = word(bank, base), word(bank, base + 2)
        n = 8
        doors = []
    # a list ends where the next table of the bank starts
    ptrs = sorted(set(table_pointers(bank)))
    nxt = lambda p: min([q for q in ptrs if q > p] + [p + 64])
    n = min(n, nxt(p34) - p34, (nxt(p36) - p36) // 8)
    out = []
    sq = prg(bank, p34, n)
    for i in range(n):
        r = prg(bank, p36 + i * 8, 8)
        if r[0] not in (0x10, 0x14, 0x16, 0x18):
            continue
        if r[0] != 0x10 and (r[1] not in ALL or r[1] == mid and r[2] == sq[i]):
            continue
        if r[0] == 0x10 and not 0xA000 <= (r[4] | r[5] << 8) < 0xB800:
            continue
        out.append({"square": sq[i], "type": r[0], "map": r[1], "to": r[2], "ow": r[4] | r[5] << 8})
    if bank == 0:
        doors = doors[:4] if mid else doors      # town tables run on into the gate list
        doors = [(s, t) for s, t in doors if floor(mid)[s] & 0x20]
    return out, doors


C = 22


def render(mid):
    m = floor(mid)
    ex, doors = exits(mid)
    im = Image.new("RGB", (16 * C + 24, 16 * C + 40), (16, 16, 16))
    dr = ImageDraw.Draw(im)
    dr.text((4, 2), "map %02X" % mid, fill=(255, 220, 80))
    oy = 18
    for i in range(16):
        dr.text((24 + i * C + 8, oy - 2 + 4), "%X" % i, fill=(140, 140, 140))
        dr.text((6, oy + 16 + i * C + 5), "%X" % i, fill=(140, 140, 140))
    oy += 16
    for y in range(16):
        for x in range(16):
            v = m[y * 16 + x]
            x0, y0 = 24 + x * C, oy + y * C
            dr.rectangle([x0, y0, x0 + C - 1, y0 + C - 1], fill=(48, 48, 56))
            if (v & 0x0F) == 0x0F:
                dr.rectangle([x0, y0, x0 + C - 1, y0 + C - 1], fill=(30, 30, 30))
            w = (235, 235, 235)
            if v & 1: dr.line([x0, y0, x0 + C - 1, y0], fill=w, width=2)
            if v & 2: dr.line([x0 + C - 1, y0, x0 + C - 1, y0 + C - 1], fill=w, width=2)
            if v & 4: dr.line([x0, y0 + C - 1, x0 + C - 1, y0 + C - 1], fill=w, width=2)
            if v & 8: dr.line([x0, y0, x0, y0 + C - 1], fill=w, width=2)
            k = 0
            for bit, col in ((0x10, (230, 70, 70)), (0x20, (70, 200, 70)), (0x40, (80, 130, 255)), (0x80, (240, 200, 40))):
                if v & bit:
                    dr.rectangle([x0 + 3 + k * 4, y0 + C - 6, x0 + 5 + k * 4, y0 + C - 4], fill=col)
                    k += 1
    def label(sq, text, col):
        x0, y0 = 24 + (sq & 15) * C, oy + (sq >> 4) * C
        dr.rectangle([x0 + 2, y0 + 2, x0 + C - 3, y0 + C - 8], fill=(0, 0, 0))
        dr.text((x0 + 3, y0 + 2), text, fill=col)
    for e in ex:
        if e["type"] == 0x10:
            label(e["square"], "OUT", (255, 120, 120))
        else:
            label(e["square"], "%02X" % e["map"], (120, 220, 255))
    for s, t in doors:
        label(s, DOOR[t] + SCHOOL.get((mid, s), "")[:2] if t == 8 else DOOR[t], (140, 255, 140))
    return im.resize((im.width * 2, im.height * 2), Image.NEAREST)


TERRAIN = {0x0: (92, 70, 50), 0x7: (90, 170, 80), 0xE: (40, 110, 60), 0xF: (50, 90, 190)}


def overworld(places):
    o = 0x4000 + 0x2000
    S = 8
    im = Image.new("RGB", (64 * S + 40, 96 * S + 20), (0, 0, 0))
    dr = ImageDraw.Draw(im)
    for y in range(96):
        for x in range(64):
            v = D[o + y * 64 + x]
            col = TERRAIN.get(v >> 4, (150, 150, 150))
            sh = 0.75 + 0.25 * ((v & 7) / 7)
            col = tuple(int(c * sh) for c in col)
            if (v & 0x0F) == 0x0F and (v >> 4) not in (0x7, 0xE, 0xF):
                col = (255, 60, 60) if v == 0x1F else (255, 230, 40)
            dr.rectangle([20 + x * S, 10 + y * S, 20 + x * S + S - 1, 10 + y * S + S - 1], fill=col)
    for sy in range(6):
        for sx in range(4):
            sid = (0x20 + sy * 4 + sx) if sy < 4 else (sy * 4 + sx)
            x0, y0 = 20 + sx * 16 * S, 10 + sy * 16 * S
            dr.rectangle([x0, y0, x0 + 16 * S - 1, y0 + 16 * S - 1], outline=(255, 255, 255))
            dr.text((x0 + 2, y0 + 1), "%02X" % sid, fill=(255, 255, 255))
    for y in range(96):
        for x in range(64):
            v = D[o + y * 64 + x]
            if (v & 0x0F) == 0x0F and (v >> 4) not in (0x7, 0xE, 0xF) and (x, y) not in places:
                places[(x, y)] = "(%02X)" % v
    for (x, y), text in places.items():
        dr.text((20 + x * S + S + 1, 10 + y * S - 2), text, fill=(255, 255, 255))
    return im


def main():
    global D
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(HERE, "../design/maps"))
    a = ap.parse_args()
    D = open(ROM, "rb").read()[16:]
    os.makedirs(a.out, exist_ok=True)
    data = {}
    places = {}
    ims = []
    for mid in ALL:
        ex, doors = exits(mid)
        data["%02X" % mid] = {"exits": [{k: ("%02X" % v if k != "ow" else "%04X" % v) for k, v in e.items()} for e in ex],
                              "doors": [{"square": "%02X" % s, "kind": DOOR[t]} for s, t in doors]}
        im = render(mid)
        im.save(os.path.join(a.out, "map_%02X.png" % mid))
        ims.append(im)
        for e in ex:
            if e["type"] == 0x10:
                cell = e["ow"] - 0xA000
                x, y = cell % 64, cell // 64
                # the place itself is the neighbouring xF cell
                for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                    v = D[0x6000 + (y + dy) * 64 + x + dx] if 0 <= y + dy < 96 and 0 <= x + dx < 64 else 0
                    if (v & 0x0F) == 0x0F and (v >> 4) not in (0x7, 0xE, 0xF):
                        key = (x + dx, y + dy)
                        if key not in places:
                            places[key] = "%02X" % mid
                        elif ("%02X" % mid) not in places[key]:
                            places[key] += "," + "%02X" % mid
                        data["%02X" % mid]["overworld_cell"] = [x + dx, y + dy]
                        break
    overworld(places).save(os.path.join(a.out, "overworld.png"))
    cols = 8
    w, h = ims[0].width // 2, ims[0].height // 2
    sheet = Image.new("RGB", (cols * w, ((len(ims) + cols - 1) // cols) * h), (0, 0, 0))
    for i, im in enumerate(ims):
        sheet.paste(im.resize((w, h)), ((i % cols) * w, (i // cols) * h))
    sheet.save(os.path.join(a.out, "atlas.png"))
    json.dump(data, open(os.path.join(a.out, "maps.json"), "w"), indent=1)
    print("written", len(ims), "floors + overworld to", a.out)


if __name__ == "__main__":
    main()
