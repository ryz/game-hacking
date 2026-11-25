#!/usr/bin/env python3
"""Read Wolfenstein 3D maps (GAMEMAPS.WL6 + MAPHEAD.WL6) straight from the game ZIP.

  python3 games/dos/wolfenstein-3d/tools/wlmap.py list                 all 60 maps: number, name, counts
  python3 games/dos/wolfenstein-3d/tools/wlmap.py E1M1                 ASCII map + object list (all skills)
  python3 games/dos/wolfenstein-3d/tools/wlmap.py E1M1 --skill 2       objects present on skill 2 ("Bring 'em on")
  python3 games/dos/wolfenstein-3d/tools/wlmap.py E1M1 --crop 20,40,50,64   x0,y0,x1,y1 (tiles) of the ASCII map
  python3 games/dos/wolfenstein-3d/tools/wlmap.py E1M1 --objects "guard|key|pushwall"   filter the list (regex,
                                                                        case-sensitive: "SS" is not "cross")
  python3 games/dos/wolfenstein-3d/tools/wlmap.py --tp 52.5 44.5 0     route tokens that put the player at tile
                       coordinates X Y (centre = .5) facing ANGLE degrees (0 east, 90 north, 180 west, 270 south);
                       poke them after the level has started (RAM addresses: playbook "RAM map")

Map numbers: map index = (episode-1)*10 + (floor-1); E1M9 = boss floor, E1M10 = secret floor.
Coordinates are tiles (x east, y south, 0-63); the player stands in the middle of a tile. Skill numbers as in
the game: 0 "Can I play, Daddy?", 1 "Don't hurt me.", 2 "Bring 'em on!", 3 "I am Death incarnate!".
Objects with an easy (skill 0-1) code appear on every skill, medium on 2-3, hard on 3 only (WL_GAME.C).

ASCII legend: '#' wall, 'E' elevator switch wall, '|'/'-' door (vertical/horizontal), 'G'/'S' gold/silver
lock door, 'L' elevator door, 'P' pushwall (secret), '^>v<' player start, 'g o s d m' guard officer SS dog
mutant, 'B' boss, 'k' key, '$' treasure, '+' food/first aid/1-up, 'a' ammo, 'W' weapon, 'x' blocking
decoration, '.' floor, ':' ambush floor (enemies wait), ' ' outside.
"""
import argparse
import os
import re
import struct
import sys
import zipfile

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
ZIP = os.path.join(ROOT, 'rom', 'wolfenstein-3d.zip')

STATIC = ["puddle", "green barrel", "table and chairs", "floor lamp", "chandelier", "hanged man",
          "dog food", "red pillar", "tree", "skeleton flat", "sink", "potted plant", "urn", "bare table",
          "ceiling light", "kitchen stuff", "suit of armor", "hanging cage", "skeleton in cage",
          "bones", "gold key", "silver key", "bed", "basket", "food", "first aid", "ammo clip",
          "machine gun", "chain gun", "cross", "chalice", "chest", "crown", "one up", "gibs",
          "barrel", "well", "empty well", "gibs 2", "flag", "call apogee", "junk 1", "junk 2",
          "junk 3", "pots", "stove", "spears", "vines"]
BLOCKING = {1, 2, 3, 5, 7, 8, 10, 11, 12, 13, 16, 17, 18, 22, 35, 36, 37, 39, 40, 45, 46}
BOSSES = {160: "fake Hitler", 178: "Hitler (mech)", 179: "General Fettgesicht", 196: "Dr. Schabbs",
          197: "Gretel Grosse", 214: "Hans Grosse", 215: "Otto Giftmacher", 224: "ghost Blinky",
          225: "ghost Clyde", 226: "ghost Pinky", 227: "ghost Inky"}
DIRS = "ENWS"   # enemy facing: code & 3 -> east, north, west, south


def load(zf, name):
    for n in zf.namelist():
        if n.upper() == name:
            return zf.read(n)
    raise SystemExit("missing " + name)


def carmack(src, outwords):
    out = []
    i = 0
    while len(out) < outwords:
        w = src[i] | src[i + 1] << 8
        i += 2
        hi, cnt = w >> 8, w & 0xFF
        if hi in (0xA7, 0xA8):
            if cnt == 0:
                out.append((hi << 8) | src[i])
                i += 1
            elif hi == 0xA7:
                off = src[i]
                i += 1
                base = len(out) - off
                for k in range(cnt):
                    out.append(out[base + k])
            else:
                off = src[i] | src[i + 1] << 8
                i += 2
                for k in range(cnt):
                    out.append(out[off + k])
        else:
            out.append(w)
    return out[:outwords]


def rlew(words, tag, outwords):
    out = []
    i = 0
    while len(out) < outwords:
        w = words[i]
        i += 1
        if w == tag:
            cnt, val = words[i], words[i + 1]
            i += 2
            out.extend([val] * cnt)
        else:
            out.append(w)
    return out[:outwords]


def maps():
    zf = zipfile.ZipFile(ZIP)
    head = load(zf, 'MAPHEAD.WL6')
    data = load(zf, 'GAMEMAPS.WL6')
    tag = struct.unpack_from('<H', head, 0)[0]
    offs = struct.unpack_from('<100i', head, 2)
    res = []
    for idx, off in enumerate(offs):
        if off <= 0:
            continue
        p = struct.unpack_from('<3i3H2H16s', data, off)
        starts, lens, w, h = p[0:3], p[3:6], p[6], p[7]
        name = p[8].split(b'\0')[0].decode('latin-1')
        planes = []
        for k in range(2):
            raw = data[starts[k]:starts[k] + lens[k]]
            n = struct.unpack_from('<H', raw, 0)[0]
            words = carmack(raw[2:], n // 2)
            planes.append(rlew(words[1:], tag, w * h))
        res.append(dict(idx=idx, name=name, w=w, h=h, walls=planes[0], objs=planes[1]))
    return res


def label(idx):
    return "E%dM%d" % (idx // 10 + 1, idx % 10 + 1)


def enemy(v):
    """(kind, skill_min, patrol, facing) for an enemy code, else None."""
    groups = [("guard", (108, 144, 180)), ("officer", (116, 152, 188)), ("SS", (126, 162, 198)),
              ("dog", (134, 170, 206)), ("mutant", (216, 234, 252))]
    for kind, bases in groups:
        for lvl, b in enumerate(bases):
            if b <= v < b + 8:
                return kind, (0, 2, 3)[lvl], (v - b) >= 4, DIRS[(v - b) & 3]
    return None


def describe(v):
    if 19 <= v <= 22:
        return "player start facing " + "NESW"[v - 19], 0
    if 23 <= v <= 74:
        return STATIC[v - 23], 0
    if v == 98:
        return "pushwall (secret)", 0
    if v == 99:
        return "end-game trigger", 0
    if v == 124:
        return "dead guard", 0
    if v in BOSSES:
        return "boss " + BOSSES[v], 0
    e = enemy(v)
    if e:
        kind, skill, patrol, face = e
        return "%s %s facing %s (skill %d+)" % (kind, "patrol" if patrol else "standing", face, skill), skill
    return "object %d" % v, 0


def char(wall, obj):
    if 19 <= obj <= 22:
        return "^>v<"[obj - 19]
    if obj == 98:
        return 'P'
    e = enemy(obj)
    if e:
        return {"guard": 'g', "officer": 'o', "SS": 's', "dog": 'd', "mutant": 'm'}[e[0]]
    if obj in BOSSES or obj == 99:
        return 'B'
    if 23 <= obj <= 74:
        s = obj - 23
        if s in (20, 21):
            return 'k'
        if s in (29, 30, 31, 32):
            return '$'
        if s in (6, 24, 25, 33):
            return '+'
        if s == 26:
            return 'a'
        if s in (27, 28):
            return 'W'
        if s in BLOCKING:
            return 'x'
    if 1 <= wall <= 63:
        return 'E' if wall == 21 else '#'
    if 90 <= wall <= 101:
        return {0: '|', 1: '-'}[wall & 1] if wall < 92 else {92: 'G', 93: 'G', 94: 'S', 95: 'S'}.get(wall, 'L')
    if wall == 106:
        return ':'
    if wall >= 107:
        return '.'
    return ' '


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('map', nargs='?')
    ap.add_argument('--tp', nargs=3, type=float, metavar=('X', 'Y', 'ANGLE'))
    ap.add_argument('--skill', type=int)
    ap.add_argument('--crop')
    ap.add_argument('--objects', help='regex filter for the object list')
    ap.add_argument('--nomap', action='store_true')
    a = ap.parse_args()
    if a.tp:
        x, y, ang = a.tp
        fx, fy = int(round(x * 65536)), int(round(y * 65536))
        print("poke:4687C=%s,poke:46884=%s,poke:46896=%s" % (
            struct.pack('<ii', fx, fy).hex().upper(), struct.pack('<HH', int(x), int(y)).hex().upper(),
            struct.pack('<H', int(ang) % 360).hex().upper()))
        return
    ms = maps()
    if a.map == 'list':
        for m in ms:
            o = m['objs']
            en = sum(1 for v in o if enemy(v))
            tr = sum(1 for v in o if 52 <= v <= 55)
            pw = o.count(98)
            bs = [BOSSES[v] for v in o if v in BOSSES]
            print("%-6s %-20s enemies %3d treasure %3d pushwalls %2d %s" % (label(m['idx']), m['name'], en, tr, pw,
                                                                            ", ".join(bs)))
        return
    mm = re.match(r'(?i)E(\d)M(\d+)$', a.map)
    idx = (int(mm.group(1)) - 1) * 10 + int(mm.group(2)) - 1 if mm else int(a.map)
    m = [x for x in ms if x['idx'] == idx][0]
    w = m['w']
    x0, y0, x1, y1 = (0, 0, 64, 64) if not a.crop else map(int, a.crop.split(','))
    print("%s %s" % (label(idx), m['name']))
    if not a.nomap:
        print("    " + "".join(str(x // 10) for x in range(x0, x1)))
        print("    " + "".join(str(x % 10) for x in range(x0, x1)))
        for y in range(y0, y1):
            row = []
            for x in range(x0, x1):
                obj = m['objs'][y * w + x]
                if a.skill is not None and enemy(obj) and enemy(obj)[1] > a.skill:
                    obj = 0
                row.append(char(m['walls'][y * w + x], obj))
            print("%2d  %s" % (y, "".join(row)))
    for y in range(64):
        for x in range(64):
            v = m['objs'][y * w + x]
            if not v:
                continue
            d, sk = describe(v)
            if a.skill is not None and sk > a.skill:
                continue
            if a.objects and not re.search(a.objects, d):
                continue
            if not (x0 <= x < x1 and y0 <= y < y1):
                continue
            print("  %2d,%2d  %3d  %s" % (x, y, v, d))


if __name__ == '__main__':
    import signal
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    main()
