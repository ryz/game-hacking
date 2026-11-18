"""Wizardry: Proving Grounds of the Mad Overlord (NES) - maze floors decoded from the ROM.

python3 games/wizardry-nes/tools/maps.py [--out DIR] [--text] [FLOOR ...]
  -> DIR/floor_NN.png (20x20, north up, 24 px per square) + DIR/atlas.png; --text prints an ASCII map and
     the special-square records. Default DIR: games/wizardry-nes/design/maps.

Format (read from the cell fetch at PRG bank 4 $8000, called from the fixed bank $D3E0; scout 2026-11-18):
  bank 4 (16 KiB at $8000) holds three tables indexed by floor*2 (floor = RAM $3D, 1-10):
    $805C  pointer to the floor's WALL grid      (floor 1 = $9A40, then +$190 each)
    $8070  pointer to the floor's FLAG grid      (floor 1 = $A9E0, then +$1D0 each)
    $8084  pointer to the floor's SPECIAL table  (= flag grid + 400)
  grids are 20x20 bytes, row-major, index y*20 + x (x = RAM $3B east+, y = RAM $3C north+, both wrap at 20).
  wall byte: 2 bits per side, N = bits 0-1, E = 2-3, S = 4-5, W = 6-7: 0 open, 1 wall, 2 door, 3 door
    (3 = probably a hidden door; Up stops at any non-zero side, A walks through sides with the high bit set).
  flag byte: $80 room (fight zone), $40 darkness (view not drawn), $20 special square: low nibble = record
    index into the special table (16 records of 4 bytes: type, a, b, c).
  special types (even, jump table at $D70E for 00-14): 00 stairs to (a=x, b=y, c=floor; floor 0 = castle),
    02 teleport to (a, b, c), 08 elevator (a-b = floor range), others tentative: 04 message/event, 0A/0C item or
    message events, 0E pit (damage), 10 spinner, 12 chute, 14 fixed encounter, 16-24 boss/special events,
    18/1A large areas (floor 5, 8, 10 fields), 1C chute to floor 10.
"""
import sys
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[3]
ROM = ROOT / "rom" / "wizardry-nes.nes"
TYPES = {0x00: "S", 0x02: "T", 0x04: "m", 0x06: "x", 0x08: "E", 0x0A: "i", 0x0C: "f", 0x0E: "P",
         0x10: "R", 0x12: "F", 0x14: "B", 0x16: "A", 0x18: "Z", 0x1A: "K", 0x1C: "C", 0x1E: "O", 0x20: "G",
         0x22: "W", 0x24: "W"}
# Meanings decoded from the handlers (jump table $D70E, fixed bank) and checked in play where noted
# (capture run 2026-11-18). a, b, c = the record's three argument bytes.
MEANING = {
    0x00: "stairs to (a,b) on floor c (0 = castle); asks 'Take them?'",
    0x02: "teleport to (a,b) on floor c (0 = castle), silent",
    0x04: "message a (waits for a button)",
    0x06: "message a, then the party is sent back to the castle",
    0x08: "elevator: buttons for floors a..b",
    0x0A: "message a (if the party lacks item b), 'Will you search?': finds item b",
    0x0C: "message a, 'Will you search?': fight with monster b",
    0x0E: "pit: members failing an agility roll take a d b damage",
    0x10: "spinner: facing set at random, silent",
    0x12: "fixed fight with monster a (+ random 0..b-1) while not yet beaten on this visit",
    0x14: "barrier: without item b, message a and pushed back",
    0x16: "alarm: message a, the next step brings a fight",
    0x18: "anti-magic area: party spells fizzle until the next stairs/teleport",
    0x1A: "solid rock: the whole party dies (lost), back to the castle",
    0x1C: "chute: 'A chute!', then to (a,b) on floor c",
    0x1E: "back to the castle at once",
    0x20: "message a (if the party lacks item b), then gives item b",
    0x22: "Werdna's sign: message a (another text once the amulet is held)",
    0x24: "Werdna's fight (monster a, b once the amulet is held) while not yet beaten",
}


def load(floor):
    bank = ROM.read_bytes()[16:][4 * 0x4000:5 * 0x4000]
    w16 = lambda a: bank[a - 0x8000] | bank[a - 0x7FFF] << 8
    walls = bank[w16(0x805C + 2 * floor) - 0x8000:][:400]
    flags = bank[w16(0x8070 + 2 * floor) - 0x8000:][:400]
    spec = bank[w16(0x8084 + 2 * floor) - 0x8000:][:64]
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
                mid += (TYPES.get(recs[f & 15][0], "?") + "%X" % (f & 15))
            else:
                mid += "##" if f & 0x40 else (" ." if f & 0x80 else "  ")
        out += [top, mid]
    used = sorted({f & 15 for f in flags if f & 0x20})
    for i in used:
        cells = [(k % 20, k // 20) for k in range(400) if flags[k] & 0x20 and flags[k] & 15 == i]
        out.append(f"  record {i:2d}: {' '.join('%02X' % b for b in recs[i])}  at {cells[0]}"
                   + (f" and {len(cells) - 1} more" if len(cells) > 1 else "")
                   + "  " + MEANING.get(recs[i][0], "?"))
    return "\n".join(out)


def draw(floor, cell=24):
    walls, flags, recs = load(floor)
    m = 20
    img = Image.new("RGB", (cell * 20 + 2 * m, cell * 20 + 2 * m + 16), (20, 20, 28))
    d = ImageDraw.Draw(img)
    d.text((m, 2), f"Wizardry (NES) floor {floor}  - north up, (0,0) bottom left", fill=(230, 230, 230))
    X = lambda x: m + x * cell
    Y = lambda y: m + 12 + (19 - y) * cell
    for y in range(20):
        for x in range(20):
            f = flags[y * 20 + x]
            fill = (60, 60, 60) if f & 0x40 else ((70, 40, 30) if f & 0x80 else (35, 35, 45))
            d.rectangle([X(x), Y(y), X(x) + cell, Y(y) + cell], fill=fill)
            if f & 0x20:
                t = recs[f & 15][0]
                d.text((X(x) + 3, Y(y) + 5), TYPES.get(t, "?") + "%X" % (f & 15), fill=(255, 230, 90))
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
    out = ROOT / "games" / "wizardry-nes" / "design" / "maps"
    if "--out" in argv:
        out = Path(argv[argv.index("--out") + 1])
        del argv[argv.index("--out"):argv.index("--out") + 2]
    floors = [int(a) for a in argv if a.isdigit()] or list(range(1, 11))
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
    cols = min(5, len(imgs))
    atlas = Image.new("RGB", (w * cols, h * ((len(imgs) + cols - 1) // cols)), (0, 0, 0))
    for i, im in enumerate(imgs):
        atlas.paste(im, ((i % cols) * w, (i // cols) * h))
    atlas.save(out / "atlas.png")
    print(out / "atlas.png")


if __name__ == "__main__":
    main(sys.argv[1:])
