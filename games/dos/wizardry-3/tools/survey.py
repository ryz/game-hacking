"""survey.py FLOOR [x,y ...] [--pre TOKENS] [--ww TOKENS] [--after TOKENS]: try.py lines that step onto each square.

  python3 games/dos/wizardry-3/tools/survey.py 6 17,17 --pre "poke:DE86=0100,poke:DE88=000000000100EA03" > work/x.txt
  python3 games/dos/wizardry-3/tools/try.py work/x.txt --frames 1

Without squares: every message, fight, trap and teleport square of the floor. For each square a neighbour whose wall
towards it is open (or a door: `k`) is chosen; the line warps there from `start` (--pre tokens first, --ww after the
warp, e.g. w1300 for floor 5), sets the facing, redraws (a,d) and steps in, then --after (default w300). Walls
belong to the square they are stored in; this picks neighbours where both sides are open or doors, so one-way
doors (only the leaving square counts in play) are missed: try those by hand.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import maps as M
a = sys.argv[1:]
pre = ''; after = 'w300'; ww = ''
if '--pre' in a: i = a.index('--pre'); pre = a[i+1] + ','; del a[i:i+2]
if '--ww' in a: i = a.index('--ww'); ww = ',' + a[i+1]; del a[i:i+2]
if '--after' in a: i = a.index('--after'); after = a[i+1]; del a[i:i+2]
fl = int(a[0]); d = M.disk(); f = M.Floor(d, fl)
if len(a) > 1:
    sq = [tuple(int(v) for v in s.split(',')) for s in a[1:]]
else:
    sq = sorted({(x, y) for x in range(20) for y in range(20) if f.extra(x, y) and M.TYPES[f.types[f.extra(x, y)]] in ('MESSAGE', 'FIXED FIGHT', 'CHUTE', 'PIT', 'TELEPORT', 'OUCH', 'SPINNER')})
# moves: (dx,dy, facing when moving from neighbour into target, side of target facing neighbour, side of neighbour facing target)
moves = [(0, 1, 2, 'N', 'S'), (0, -1, 0, 'S', 'N'), (1, 0, 3, 'E', 'W'), (-1, 0, 1, 'W', 'E')]
for (x, y) in sq:
    best = None
    for dx, dy, face, ts, ns in moves:
        nx, ny = (x + dx) % 20, (y + dy) % 20
        w1, w2 = f.wall(ts, x, y), f.wall(ns, nx, ny)
        if w1 in (0, 2, 3) and w2 in (0, 2, 3):
            e = f.extra(nx, ny)
            special = e and M.TYPES[f.types[e]] not in ('DARK', 'NORMAL')
            score = (w1 == 0 and w2 == 0) * 2 + (not special)
            if best is None or score > best[0]:
                best = (score, nx, ny, face, 'w' if (w1 == 0 and w2 == 0) else 'k')
    if not best:
        print('# %d,%d no open neighbour' % (x, y)); continue
    _, nx, ny, face, key = best
    print('f%d_%02d_%02d | @start,%sWARP:%02X:%02X:%02X%s,poke:DB6C=%02X00,a,w60,d,w60,%s,%s' % (fl, x, y, pre, fl, nx, ny, ww, face, key, after))
