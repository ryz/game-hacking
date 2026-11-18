"""Wizardry II: Knight of Diamonds (NES) - maze floors decoded from the ROM (port of games/wizardry-nes/tools/maps.py).

python3 games/wizardry-2-nes/tools/maps.py [--out DIR] [--text] [FLOOR ...]
  -> DIR/floor_NN.png (20x20, north up, 24 px per square) + DIR/atlas.png; --text prints an ASCII map and
     the special-square records. Default DIR: games/wizardry-2-nes/design/maps.

Format (scout 2026-11-18, from the cell fetch at PRG bank 13 (8 KiB, at $A000) $A8B7, which maps bank 9 at $8000):
  RAM: x = $EA (east+), y = $EB (north+), floor = $EC (1-6), facing = $E9 (0 N, 1 E, 2 S, 3 W); 20x20, wrapping.
  PRG bank 9 (8 KiB, file offset $12010): word table at $8000 indexed by floor*2 -> the floor block
  (floor 1 = $800E, then +$4B0 each): WALL grid (400 bytes), FLAG grid (400), ZONE grid (400: an area number
  per square, probably the encounter/room id; not drawn).
  wall byte: 2 bits per side, N = bits 0-1, E = 2-3, S = 4-5, W = 6-7: 0 open, 1 wall, 2 door, 3 secret door
    (masks $A71F = 03 0C 30 C0; doors tested with the high bit, $A723 = 02 08 20 80, as in Wizardry I).
  flag byte: $80 room (fight zone; code $A547), $40 darkness (code bank 7 $9A5D, inferred), $20 special
    square: low 5 bits = record index.
  special records: 16 per floor x 4 bytes (type, a, b, c). ROM originals in PRG bank 4 (8 KiB) at offset $04FB
    + 64*(floor-1) (file offset $84FB...); the game keeps a working copy per floor in battery RAM at
    $6B88 + 65*(floor-1) (pointer table bank 13 $B9AE) and the current floor's at $6E79; one-time events clear
    their record there (type -> 0). Dispatch: bank 13 $B1F6, jump table $B219 (types 00-16).
"""
import sys
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[3]
ROM = ROOT / "rom" / "wizardry-2-nes.nes"
TYPES = {0x01: "S", 0x02: "T", 0x03: "C", 0x04: "K", 0x05: "P", 0x06: "p", 0x07: "R", 0x08: "m",
         0x09: "x", 0x0A: "F", 0x0B: "A", 0x0C: "q", 0x0D: "i", 0x0E: "s", 0x0F: "g", 0x10: "f", 0x11: "1",
         0x12: "2", 0x13: "3", 0x14: "e", 0x15: "o", 0x16: "y"}
# Meanings from a first reading of the handlers (scout 2026-11-18; jump table bank 13 $B219), a/b/c = the
# record's argument bytes; "(code)" = read from the program only, to be checked in play by the capture run.
MEANING = {
    0x00: "nothing (cleared one-time event)",
    0x01: "stairs to (a,b) on floor c (0 = castle); 'Stairs up/down --- Take them?' (cross-checked between floors)",
    0x02: "teleport to (a,b) on floor c, silent (code)",
    0x03: "chute/trapdoor: message, then to (a,b) on floor c (code)",
    0x04: "solid rock / deadly area: every member still alive is set to status 5 (code)",
    0x05: "pit: message, damage to the party (a, b, c dice; code)",
    0x06: "pit without the opening message (code)",
    0x07: "spinner: facing set at random, silent (code)",
    0x08: "message b (c: a second message; code)",
    0x09: "message b, then teleport to (b?,c) or back to the castle when c >= $80 (code)",
    0x0A: "message b, then a fixed fight (group set a; code)",
    0x0B: "message b, then a fight on the next step (alarm-like; code)",
    0x0C: "message chain a..c (stops on a condition; code)",
    0x0D: "one-time: message b, 'Search?' (Yes/No), item (code)",
    0x0E: "message b, Yes/No prompt, then a check against item c (code)",
    0x0F: "guardian fight with monster a unless a condition (item c?) holds (code)",
    0x10: "fixed fight with monster a + random(b) while armed (c = 1; code)",
    0x11: "one-member party only: otherwise message b and back to the castle (code)",
    0x12: "one-member party only, item check (code)",
    0x13: "one-member party only: teleport by a member flag (code)",
    0x14: "party check event: message $BC, loop over the party (code)",
    0x15: "one-time: messages $82/$83/$84/$86 by party size (code; unused on the six floors)",
    0x16: "message b, Yes/No, then event a (code)",
}


def load(floor):
    prg = ROM.read_bytes()[16:16 + 0x20000]
    bank = prg[9 * 0x2000:10 * 0x2000]
    base = (bank[2 * floor] | bank[2 * floor + 1] << 8) - 0x8000
    walls, flags = bank[base:base + 400], bank[base + 400:base + 800]
    spec = prg[4 * 0x2000 + 0x4FB + 64 * (floor - 1):][:64]
    recs = [tuple(spec[4 * i:4 * i + 4]) for i in range(16)]
    return walls, flags, recs


def text(floor):
    walls, flags, recs = load(floor)
    out = [f"Floor {floor} (x east 0-19, y north 0-19; '#' dark, '.' room, letters = specials)"]
    for y in range(19, -1, -1):
        top, mid = "    ", f"{y:2d}  "
        for x in range(20):
            w, f = walls[y * 20 + x], flags[y * 20 + x]
            top += "+" + {0: "  ", 1: "--", 2: "DD", 3: "SS"}[w & 3]
            mid += {0: " ", 1: "|", 2: "D", 3: "S"}[w >> 6 & 3]
            if f & 0x20:
                mid += (TYPES.get(recs[f & 31][0], "?") + "%X" % (f & 31))
            else:
                mid += "##" if f & 0x40 else (" ." if f & 0x80 else "  ")
        out += [top, mid]
    used = sorted({f & 31 for f in flags if f & 0x20})
    for i in used:
        cells = [(k % 20, k // 20) for k in range(400) if flags[k] & 0x20 and flags[k] & 31 == i]
        out.append(f"  record {i:2d}: {' '.join('%02X' % b for b in recs[i])}  at {cells[0]}"
                   + (f" and {len(cells) - 1} more" if len(cells) > 1 else "")
                   + "  " + MEANING.get(recs[i][0], "?"))
    return "\n".join(out)


def draw(floor, cell=24):
    walls, flags, recs = load(floor)
    m = 20
    img = Image.new("RGB", (cell * 20 + 2 * m, cell * 20 + 2 * m + 16), (20, 20, 28))
    d = ImageDraw.Draw(img)
    d.text((m, 2), f"Knight of Diamonds (NES) floor {floor}  - north up, (0,0) bottom left", fill=(230, 230, 230))
    X = lambda x: m + x * cell
    Y = lambda y: m + 12 + (19 - y) * cell
    for y in range(20):
        for x in range(20):
            f = flags[y * 20 + x]
            fill = (60, 60, 60) if f & 0x40 else ((70, 40, 30) if f & 0x80 else (35, 35, 45))
            d.rectangle([X(x), Y(y), X(x) + cell, Y(y) + cell], fill=fill)
            if f & 0x20:
                t = recs[f & 31][0]
                d.text((X(x) + 3, Y(y) + 5), TYPES.get(t, "?") + "%X" % (f & 31), fill=(255, 230, 90))
    for y in range(20):
        for x in range(20):
            w = walls[y * 20 + x]
            x0, y0, x1, y1 = X(x), Y(y), X(x) + cell, Y(y) + cell
            sides = {0: (x0, y0, x1, y0), 1: (x1, y0, x1, y1), 2: (x0, y1, x1, y1), 3: (x0, y0, x0, y1)}
            for s, (a, b, c, e) in sides.items():
                v = w >> (2 * s) & 3
                if v == 1:
                    d.line([a, b, c, e], fill=(235, 235, 235), width=2)
                elif v in (2, 3):
                    col = (90, 200, 255) if v == 2 else (255, 80, 80)
                    d.line([a, b, c, e], fill=(235, 235, 235), width=2)
                    cx, cy = (a + c) // 2, (b + e) // 2
                    d.rectangle([cx - 4, cy - 4, cx + 4, cy + 4], fill=col)
    return img


def main(argv):
    out = ROOT / "games" / "wizardry-2-nes" / "design" / "maps"
    if "--out" in argv:
        out = Path(argv[argv.index("--out") + 1])
        del argv[argv.index("--out"):argv.index("--out") + 2]
    floors = [int(a) for a in argv if a.isdigit()] or list(range(1, 7))
    if "--text" in argv:
        for f in floors:
            print(text(f))
        return
    out.mkdir(parents=True, exist_ok=True)
    imgs = []
    for f in floors:
        im = draw(f)
        im.save(out / f"floor_{f:02d}.png")
        imgs.append(im)
    w, h = imgs[0].size
    cols = min(3, len(imgs))
    atlas = Image.new("RGB", (w * cols, h * ((len(imgs) + cols - 1) // cols)), (0, 0, 0))
    for i, im in enumerate(imgs):
        atlas.paste(im, ((i % cols) * w, (i // cols) * h))
    atlas.save(out / "atlas.png")
    print(out / "atlas.png")


if __name__ == "__main__":
    main(sys.argv[1:])
