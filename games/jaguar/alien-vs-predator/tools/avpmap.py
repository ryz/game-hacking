"""Alien vs Predator (Jaguar): draw the current level's wall grid as text.

  python3 games/jaguar/alien-vs-predator/tools/avpmap.py ROUTE [--raw] [--box X0,Y0,X1,Y1]

The level is a 64x64 grid of 8-byte cells at DRAM 4FC00 (row = y, column = x; bytes 0-3 = wall on the
west, north (y-1), east and south (y+1) side, nonzero = wall or door; bytes 4-7 = texture/object ids).
The player is at word 2F1CE (x) / 2F1D2 (y), fraction in the next word; angle 2F1D6 (4000 = north, y-1).
Output: '@' player, '#' corner, '|' and '-' walls, letters for wall ids (hex low digit of byte 0-3).
--raw prints the 8 bytes of every non-empty cell inside --box.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..', 'tools'))
import emu

def grab(route):
    g = emu.Game('alien-vs-predator')
    e, rest, full = emu.start(g, route)
    emu.play(e, g, rest)
    m = bytes(e.peek(0x4FC00, 64 * 64 * 8))
    p = bytes(e.peek(0x2F1CE, 10))
    lv = bytes(e.peek(0x2F5AA, 2))
    return m, int.from_bytes(p[0:2], 'big'), int.from_bytes(p[4:6], 'big'), int.from_bytes(p[8:10], 'big'), int.from_bytes(lv, 'big')

def main():
    a = sys.argv[1:]
    raw = '--raw' in a
    box = (0, 0, 63, 63)
    if '--box' in a:
        box = tuple(int(v) for v in a[a.index('--box') + 1].split(','))
    route = a[0]
    m, px, py, ang, lv = grab(route)
    cell = lambda x, y: m[(y * 64 + x) * 8:(y * 64 + x) * 8 + 8]
    x0, y0, x1, y1 = box
    print('level %d  player x=%d y=%d angle=%04X' % (lv, px, py, ang))
    if raw:
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                c = cell(x, y)
                if any(c): print('%2d,%2d %s' % (x, y, c.hex(' ')))
        return
    print('    ' + ''.join('%-2d' % (x % 100) if x % 2 == 0 else '  ' for x in range(x0, x1 + 1)))
    for y in range(y0, y1 + 1):
        top = '    '; mid = '%3d ' % y
        for x in range(x0, x1 + 1):
            c = cell(x, y)
            top += '+' + ('-' if c[1] else ' ')
            ch = '@' if (x, y) == (px, py) else ('.' if not any(c[0:4]) and any(c) else (' ' if not any(c) else ':'))
            mid += ('|' if c[0] else ' ') + ch
        print(top); print(mid)

if __name__ == '__main__':
    main()
