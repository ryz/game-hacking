"""Render Dungeon Magic 16x16 maps as PNG (walls + special bits).

Map data (playbook "Map data"): the current map is in RAM $0600-$06FF, one byte per cell, row-major (index = $YX,
the same encoding as the position byte $8A). It is copied from CPU $A000 + (id & $1F) * $100 in PRG bank
(id & $E0) >> 4, where id = RAM $95: file offset = 16 + bank * $4000 + $2000 + (id & $1F) * $100.
Cell bits: 1 = wall north, 2 = wall east, 4 = wall south, 8 = wall west; $10/$20/$40/$80 = special features
(doors, signs, events; meaning still open), drawn as coloured dots.

usage: python3 games/nes/dungeon-magic/tools/maps.py ID [ID ...] --out DIR      (ID hex, e.g. 00 41)
       python3 games/nes/dungeon-magic/tools/maps.py --ram FILE.bin --out DIR   (256-byte dump of $0600)
       optional --pos YX marks the party (hex position byte $8A)"""
import argparse, os
from PIL import Image, ImageDraw
ROM = os.path.join(os.path.dirname(__file__), "../../../../rom/dungeon-magic.nes")
C = 14
COL = {0x10: (230, 60, 60), 0x20: (60, 200, 60), 0x40: (60, 120, 255), 0x80: (240, 200, 40)}

def load(mid):
    d = open(ROM, "rb").read()
    off = 16 + ((mid & 0xE0) >> 5) * 0x4000 + 0x2000 + (mid & 0x1F) * 0x100
    return d[off:off + 256]

def render(m, pos=None):
    im = Image.new("RGB", (16 * C + 20, 16 * C + 20), (20, 20, 20)); dr = ImageDraw.Draw(im)
    for i in range(16):
        dr.text((20 + i * C + 3, 2), "%X" % i, fill=(150, 150, 150)); dr.text((4, 20 + i * C + 2), "%X" % i, fill=(150, 150, 150))
    for y in range(16):
        for x in range(16):
            v = m[y * 16 + x]; x0, y0 = 20 + x * C, 20 + y * C
            dr.rectangle([x0, y0, x0 + C - 1, y0 + C - 1], fill=(45, 45, 45))
            w = (230, 230, 230)
            if v & 1: dr.line([x0, y0, x0 + C - 1, y0], fill=w, width=2)
            if v & 2: dr.line([x0 + C - 1, y0, x0 + C - 1, y0 + C - 1], fill=w, width=2)
            if v & 4: dr.line([x0, y0 + C - 1, x0 + C - 1, y0 + C - 1], fill=w, width=2)
            if v & 8: dr.line([x0, y0, x0, y0 + C - 1], fill=w, width=2)
            k = 0
            for bit, col in COL.items():
                if v & bit:
                    dr.rectangle([x0 + 3 + k * 3, y0 + 5, x0 + 4 + k * 3, y0 + 8], fill=col); k += 1
            if pos is not None and pos == y * 16 + x:
                dr.ellipse([x0 + 3, y0 + 3, x0 + C - 4, y0 + C - 4], outline=(255, 0, 255), width=2)
    return im.resize((im.width * 2, im.height * 2), Image.NEAREST)

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("ids", nargs="*"); ap.add_argument("--ram"); ap.add_argument("--out", required=True)
    ap.add_argument("--pos"); a = ap.parse_args(); os.makedirs(a.out, exist_ok=True)
    pos = int(a.pos, 16) if a.pos else None
    if a.ram:
        render(open(a.ram, "rb").read()[:256], pos).save(os.path.join(a.out, "ram_map.png"))
    for s in a.ids:
        mid = int(s, 16); render(load(mid), pos).save(os.path.join(a.out, "map_%02X.png" % mid))
    print("written to", a.out)
