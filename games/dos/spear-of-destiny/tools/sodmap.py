#!/usr/bin/env python3
"""Read Spear of Destiny maps (m1/GAMEMAPS.SOD + m1/MAPHEAD.SOD) straight from the game ZIP.

Built on games/dos/wolfenstein-3d/tools/wlmap.py (same Carmack/RLEW format, same ASCII legend); Spear's
static objects 48-51 (marble pillar, 25-clip box, truck, the Spear) and its bosses replace Wolfenstein's.

  python3 games/dos/spear-of-destiny/tools/sodmap.py list               all 21 floors: number, map index, name, counts
  python3 games/dos/spear-of-destiny/tools/sodmap.py 1 --skill 2        floor 1 (1-21): ASCII map + objects on skill 2
  python3 games/dos/spear-of-destiny/tools/sodmap.py 5 --objects "boss|key"   filter the object list (regex)
  python3 games/dos/spear-of-destiny/tools/sodmap.py 5 --crop 20,40,50,64     x0,y0,x1,y1 (tiles)
  python3 games/dos/spear-of-destiny/tools/sodmap.py --tp 29.5 57.5 0   route tokens: teleport (playbook RAM map)

Floor N = map index N-1 (`spear tedlevel N-1`). Skills as in wlmap.py (0 Daddy .. 3 Death incarnate).
Extra legend: '*' floor code 107 = secret-elevator tile (Use on the switch while standing here goes to a
secret floor), 'B' boss / spectre, 'W' weapon or the Spear itself.
"""
import argparse
import os
import re
import struct
import sys
import zipfile

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'games', 'dos', 'wolfenstein-3d', 'tools'))
import wlmap  # noqa: E402

ZIP = os.path.join(ROOT, 'rom', 'spear-of-destiny.zip')
TP_ADDR = ("475B2", "475BA", "475CC")   # player x/y (16.16), tile x/y, angle (playbook RAM map)

STATIC = list(wlmap.STATIC)
STATIC[15] = "gibs (blocking)"
STATIC[40] = "red light"
STATIC[44] = "gibs (blocking)"
STATIC += ["marble pillar", "25-clip box", "truck", "SPEAR OF DESTINY"]
wlmap.STATIC = STATIC
wlmap.BLOCKING = (wlmap.BLOCKING - {40}) | {15, 44, 48, 50}
wlmap.BOSSES = {106: "spectre (ghost)", 107: "Angel of Death", 125: "Trans Grosse", 142: "Ubermutant",
                143: "Barnacle Wilhelm", 161: "Death Knight"}


def maps():
    zf = zipfile.ZipFile(ZIP)
    head = wlmap.load(zf, 'M1/MAPHEAD.SOD')
    data = wlmap.load(zf, 'M1/GAMEMAPS.SOD')
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
            words = wlmap.carmack(raw[2:], n // 2)
            planes.append(wlmap.rlew(words[1:], tag, w * h))
        res.append(dict(idx=idx, name=name, w=w, h=h, walls=planes[0], objs=planes[1]))
    return res


def char(wall, obj):
    if obj == 74:
        return 'W'
    if obj == 72:
        return 'a'
    c = wlmap.char(wall, obj)
    if wall == 107 and c == '.':
        return '*'
    return c


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
        print("poke:%s=%s,poke:%s=%s,poke:%s=%s" % (
            TP_ADDR[0], struct.pack('<ii', fx, fy).hex().upper(), TP_ADDR[1],
            struct.pack('<HH', int(x), int(y)).hex().upper(), TP_ADDR[2],
            struct.pack('<H', int(ang) % 360).hex().upper()))
        print("TP:%s:%s:%s" % (struct.pack('<ii', fx, fy).hex().upper(),
                               struct.pack('<HH', int(x), int(y)).hex().upper(),
                               struct.pack('<H', int(ang) % 360).hex().upper()))
        return
    ms = maps()
    if a.map == 'list':
        for m in ms:
            o = m['objs']
            en = sum(1 for v in o if wlmap.enemy(v))
            tr = sum(1 for v in o if 52 <= v <= 55)
            pw = o.count(98)
            bs = sorted({wlmap.BOSSES[v] for v in o if v in wlmap.BOSSES})
            sp = " +SPEAR" if 74 in o else ""
            alt = " secret-exit" if 107 in m['walls'] else ""
            print("floor %2d (map %2d) %-16s enemies %3d treasure %3d pushwalls %2d %s%s%s" % (
                m['idx'] + 1, m['idx'], m['name'], en, tr, pw, ", ".join(bs), sp, alt))
        return
    idx = int(a.map) - 1
    m = [x for x in ms if x['idx'] == idx][0]
    w = m['w']
    x0, y0, x1, y1 = (0, 0, 64, 64) if not a.crop else map(int, a.crop.split(','))
    print("floor %d (map %d) %s" % (idx + 1, idx, m['name']))
    if not a.nomap:
        print("    " + "".join(str(x // 10) for x in range(x0, x1)))
        print("    " + "".join(str(x % 10) for x in range(x0, x1)))
        for y in range(y0, y1):
            row = []
            for x in range(x0, x1):
                obj = m['objs'][y * w + x]
                if a.skill is not None and wlmap.enemy(obj) and wlmap.enemy(obj)[1] > a.skill:
                    obj = 0
                row.append(char(m['walls'][y * w + x], obj))
            print("%2d  %s" % (y, "".join(row)))
    for y in range(64):
        for x in range(64):
            v = m['objs'][y * w + x]
            if not v:
                continue
            d, sk = wlmap.describe(v)
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
