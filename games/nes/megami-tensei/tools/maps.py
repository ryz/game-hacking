"""Megami Tensei (Famicom) labyrinth maps from the ROM -> design/maps/*.png + grids.md.

Usage: python3 games/nes/megami-tensei/tools/maps.py [--rom rom/megami-tensei.nes] [--out games/nes/megami-tensei/design/maps]

Format (design/maps.md, "How the maps are stored"):
- The whole labyrinth is ONE 128x64 grid of squares; the party position $0780/$0781 is global (x 0-127, y 0-63).
  The grid is stored at $8004 with PRG bank 10 at $8000 and bank 11 at $A000 (file offset 0x14014), one byte per
  square, row-major (128 bytes a row). Byte = four 2-bit walls: bits 7-6 north, 5-4 east, 3-2 south, 1-0 west;
  0 open, 1 wall, 3 door (2 unused). A side that is a door from one square and a wall from the other is a one-way door.
- Block table (fixed bank $CB7D, 16x8 bytes): one byte per 8x8 block, high nibble = floor (1-8 = 1F-8F, 9 = B1,
  A = B2), low nibble = section ($0782). 0E/0F = split into 4x4 sub-blocks (table $CBFD; 0E from x $60, 0F from x $50).
  A square is part of the floor whose (floor, section) equals ($055D, $0782); anything else reads as solid.
- Special-square lists per section (bank 9, pointer table $AAF5, 14 pointers = 0x1C bytes per section):
  +08 stairs up, +0A stairs down (5 bytes: x y -> x2 y2, section after); +10 elevators (header: n bytes of floor
  names, then x y section floor); +12 locked doors (x y key ?); +14 fixed encounters (x y id, id 0F = the
  section's tyrant); +16 events (6 bytes: x y a b c d; a b = 20 6C chest, 07 xx message); +0C/+0E 6-byte warps
  (x y -> x2 y2 ..); +18 7-byte records (x y d x2 y2 ..; moving-floor / turn squares, not confirmed).
"""
import argparse, os
from collections import defaultdict
from PIL import Image, ImageDraw

SECTION_BOSS = {0: 'Tyrant Minotaur', 1: 'Tyrant Medusa', 2: 'Tyrant Loki', 3: 'Tyrant Hecate', 4: 'Tyrant Set',
                5: 'Dark Lord Lucifer'}


def floor_name(f):
    return {9: 'B1', 10: 'B2'}.get(f, '%dF' % f)


class Rom:
    def __init__(self, path):
        self.d = open(path, 'rb').read()[16:16 + 0x40000]

    def bank(self, n, addr):
        return self.d[n * 0x2000 + (addr & 0x1FFF)]

    def grid(self):
        def rd(a):
            return self.bank(10 if a < 0xA000 else 11, a)
        return [[rd(0x8004 + y * 128 + x) for x in range(128)] for y in range(64)]

    def owner(self):
        """(x, y) -> block byte (floor << 4 | section)."""
        blk = [self.bank(31 if False else 30, 0xCB7D + i) for i in range(128)]
        sub = [self.bank(30, 0xCBFD + i) for i in range(64)]
        own = {}
        for y in range(64):
            for x in range(128):
                v = blk[x // 8 + (y & 0xF8) * 2]
                if v & 0x0F == 0x0E:
                    v = sub[(x - 0x60) // 4 + (y & 0xFC)]
                elif v & 0x0F == 0x0F:
                    v = sub[(x - 0x50) // 4 + (y & 0xFC)]
                own[(x, y)] = v
        return own

    def r9(self, a):
        return self.bank(8 if a < 0xA000 else 9, a)

    def lst(self, section, cat, size, term=0xFF):
        i = section * 0x1C + cat
        p = self.r9(0xAAF5 + i) | self.r9(0xAAF6 + i) << 8
        out = []
        while self.r9(p) != term and len(out) < 200:
            out.append(tuple(self.r9(p + k) for k in range(size)))
            p += size
        return out

    def elevators(self, section):
        i = section * 0x1C + 0x10
        p = self.r9(0xAAF5 + i) | self.r9(0xAAF6 + i) << 8
        n = self.r9(p)
        names = []
        for k in range(0, n, 2):
            a, b = self.r9(p + 1 + k), self.r9(p + 2 + k)
            names.append(('B%d' % b) if a == 0x9B else ('%dF' % a))
        p += 1 + n
        out = []
        while self.r9(p) != 0xFF and len(out) < 20:
            out.append(tuple(self.r9(p + k) for k in range(4)))
            p += 4
        return names, out


def specials(rom):
    """section -> {(x, y): [(kind, text)]}"""
    sp = defaultdict(lambda: defaultdict(list))
    for s in range(6):
        for (x, y, x2, y2, a) in rom.lst(s, 0x08, 5):
            sp[s][(x, y)].append(('U', 'stairs up -> (%d,%d)%s' % (x2, y2, '' if a == s else ' section %d' % a)))
        for (x, y, x2, y2, a) in rom.lst(s, 0x0A, 5):
            sp[s][(x, y)].append(('D', 'stairs down -> (%d,%d)%s' % (x2, y2, '' if a == s else ' section %d' % a)))
        names, els = rom.elevators(s)
        for (x, y, a, f) in els:
            sp[s][(x, y)].append(('E', 'elevator (%s), this stop %s' % (' '.join(names), floor_name(f))))
        for (x, y, k, z) in rom.lst(s, 0x12, 4):
            sp[s][(x, y)].append(('L', 'locked door (key %02X %02X)' % (k, z)))
        for (x, y, i) in rom.lst(s, 0x14, 3):
            if i == 0x0F:
                sp[s][(x, y)].append(('B', 'BOSS: %s' % SECTION_BOSS[s]))
            else:
                sp[s][(x, y)].append(('F', 'fixed encounter %02X' % i))
        for r in rom.lst(s, 0x16, 6):
            x, y, a, b, c, d = r
            if (a, b) == (0x20, 0x6C):
                sp[s][(x, y)].append(('C', 'chest (%02X %02X)' % (c, d)))
            elif a == 0x07:
                sp[s][(x, y)].append(('M', 'message/NPC %02X%02X (%02X %02X)' % (a, b, c, d)))
            else:
                sp[s][(x, y)].append(('?', 'event %02X %02X %02X %02X' % (a, b, c, d)))
        for cat in (0x0C, 0x0E):
            for (x, y, x2, y2, a, b) in rom.lst(s, cat, 6):
                sp[s][(x, y)].append(('W', 'warp -> (%d,%d) (%02X %02X)' % (x2, y2, a, b)))
        for (x, y, d, x2, y2, a, b) in rom.lst(s, 0x18, 7):
            sp[s][(x, y)].append(('T', 'trap/turn square %02X -> (%d,%d) %02X %02X' % (d, x2, y2, a, b)))
    return sp


COL = {'U': (40, 200, 40), 'D': (0, 120, 0), 'E': (60, 140, 255), 'L': (200, 60, 60), 'B': (255, 0, 160),
       'F': (250, 170, 40), 'C': (240, 220, 40), 'M': (120, 220, 220), '?': (190, 140, 255), 'W': (255, 120, 255),
       'T': (170, 170, 170)}


def draw_floor(G, own, key, sq, sp, path, title):
    xs = [x for x, y in sq]; ys = [y for x, y in sq]
    x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
    S = 18 if max(x1 - x0, y1 - y0) < 40 else 13; L = 30; T = 30
    w, h = x1 - x0 + 1, y1 - y0 + 1
    im = Image.new("RGB", (max(L + w * S + 10, 440), T + h * S + 10), (25, 25, 25))
    d = ImageDraw.Draw(im)
    d.text((4, 2), title, fill=(255, 255, 0))
    for i in range(w):
        if (x0 + i) % 2 == 0 or w <= 16:
            d.text((L + i * S + 2, 16), '%d' % (x0 + i), fill=(160, 160, 160))
    for j in range(h):
        d.text((2, T + j * S + 4), '%2d' % (y0 + j), fill=(160, 160, 160))
    sset = set(sq)
    for (x, y) in sq:
        px, py = L + (x - x0) * S, T + (y - y0) * S
        d.rectangle([px, py, px + S - 1, py + S - 1], fill=(225, 225, 215))
    for (x, y) in sq:
        v = G[y][x]
        px, py = L + (x - x0) * S, T + (y - y0) * S
        sides = {'N': (v >> 6) & 3, 'E': (v >> 4) & 3, 'S': (v >> 2) & 3, 'W': v & 3}
        seg = {'N': (px, py, px + S - 1, py), 'S': (px, py + S - 1, px + S - 1, py + S - 1),
               'W': (px, py, px, py + S - 1), 'E': (px + S - 1, py, px + S - 1, py + S - 1)}
        for k, c in sides.items():
            a, b, cc, dd = seg[k]
            if c == 1:
                d.line([a, b, cc, dd], fill=(0, 0, 0), width=2)
            elif c in (2, 3):
                d.line([a, b, cc, dd], fill=(0, 0, 0), width=2)
                mx, my = (a + cc) // 2, (b + dd) // 2
                d.rectangle([mx - 3, my - 3, mx + 3, my + 3], fill=(150, 80, 20))
        marks = sp.get((x, y), [])
        if marks:
            k = marks[0][0]
            d.rectangle([px + 3, py + 3, px + S - 4, py + S - 4], fill=COL[k])
            d.text((px + 6, py + 4), k, fill=(0, 0, 0))
    im.save(path)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--rom', default='rom/megami-tensei.nes')
    ap.add_argument('--out', default='games/nes/megami-tensei/design/maps')
    a = ap.parse_args()
    rom = Rom(a.rom)
    G = rom.grid(); own = rom.owner(); sp = specials(rom)
    floors = defaultdict(list)
    for (x, y), v in own.items():
        floors[v].append((x, y))
    os.makedirs(a.out, exist_ok=True)
    txt = ['# Megami Tensei floor grids (generated by tools/maps.py)', '',
           'Per floor: special squares (x,y global = $0780/$0781). Walls are in the PNGs.', '']
    order = sorted(floors, key=lambda v: (v & 15, -((v >> 4) if (v >> 4) < 9 else 8 - (v >> 4))))
    for v in order:
        sec, fl = v & 15, v >> 4
        if sec > 5 or fl == 0:
            continue
        sq = floors[v]
        name = 's%d_%s' % (sec, floor_name(fl))
        mine = {p: sp[sec][p] for p in sq if p in sp[sec]}
        xs = [x for x, y in sq]; ys = [y for x, y in sq]
        draw_floor(G, own, v, sq, mine, os.path.join(a.out, name + '.png'),
                   'Megami Tensei section %d %s  x %d-%d y %d-%d (%d squares)' % (sec, floor_name(fl), min(xs), max(xs), min(ys), max(ys), len(sq)))
        txt.append('## %s (section %d, floor %s; $055D=%02X $0782=%02X) - %d squares, x %d-%d, y %d-%d' % (
            name, sec, floor_name(fl), fl, sec, len(sq), min(xs), max(xs), min(ys), max(ys)))
        for p in sorted(mine, key=lambda p: (p[1], p[0])):
            for k, t in mine[p]:
                txt.append('- (%d,%d) %s %s' % (p[0], p[1], k, t))
        txt.append('')
    open(os.path.join(a.out, 'grids.md'), 'w').write('\n'.join(txt) + '\n')
    print('floors', len([v for v in floors if (v & 15) <= 5 and v >> 4]))


if __name__ == '__main__':
    main()
