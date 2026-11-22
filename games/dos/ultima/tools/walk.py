"""walk.py: honest walking routes for Ultima I (DOS), no position pokes.

  python3 games/dos/ultima/tools/walk.py town X Y [--name ultima] [--ok 1,3e,...]
      Walk the running play.py session (inside a town or castle) to square X,Y (hex), a few steps per
      `play.py do`, re-planning around the people (table 19C1C) after each chunk; a guard or the jester on
      the way costs a pass ("space") and a new plan. Prints each chunk and its status line.
  python3 games/dos/ultima/tools/walk.py over X0 Y0 X1 Y1
      Print the overworld tokens (grass and woods only, from MAP.BIN) from X0,Y0 to X1,Y1 (hex), for a
      `play.py do` or a route. Monsters can still block: look at the frame after every 10 steps.

Walkable town squares (map buffer 17AFE + map * 0x2AC, column-major x*18+y): 01 floor, 3E/36/3A/38/3C/3D
the customer side of the transport/armour/weapon/food/magic/pub counters, 3F the pub door, 34/35 the
castle courtyard beside the pools. Default: all of them.
"""
import collections
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
DIRS = (('up', (0, -1)), ('down', (0, 1)), ('left', (-1, 0)), ('right', (1, 0)))


def bfs(start, goal, free):
    prev = {start: None}
    q = collections.deque([start])
    while q:
        c = q.popleft()
        if c == goal:
            break
        for d, (dx, dy) in DIRS:
            n = (c[0] + dx, c[1] + dy)
            if n not in prev and (n == goal or free(n)):
                prev[n] = (c, d)
                q.append(n)
    if goal not in prev:
        return None
    path, c = [], goal
    while prev[c]:
        c, d = prev[c]
        path.append(d)
    return path[::-1]


def play(args, name):
    return subprocess.run(['python3', 'tools/play.py'] + args + ['--name', name], capture_output=True,
                          text=True, cwd=ROOT).stdout


def peek(addr, n, name):
    out = []
    for line in play(['peek', '%X' % addr, str(n)], name).splitlines():
        p = line.split()
        if len(p) > 1 and re.fullmatch(r'[0-9a-f]{5}', p[0]):
            out += [int(t, 16) for t in p[1:]]
    return out


def town(tx, ty, name, ok):
    for _ in range(40):
        lvl = peek(0x19C92, 2, name)[0]
        grid = peek(0x17AFE + lvl * 0x2AC, 684, name)
        pos = peek(0x19C8E, 4, name)
        here = (pos[0], pos[2])
        if here == (tx, ty):
            print('arrived')
            return
        pp = peek(0x19C1C, 128, name)
        people = {(pp[i + 4], pp[i + 6]) for i in range(0, 128, 8)
                  if (pp[i + 2] | pp[i + 3] << 8) != 0xFFFF and (pp[i] | pp[i + 1])}
        path = bfs(here, (tx, ty), lambda n: 0 <= n[0] < 38 and 0 <= n[1] < 18
                   and grid[n[0] * 18 + n[1]] in ok and n not in people)
        toks = ','.join(t + ',w30' for t in path[:3]) if path else 'space,w30'
        print(toks, '|', play(['do', toks], name).strip().splitlines()[-1][:110])
    print('not arrived')


def over(x0, y0, x1, y1):
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import worldmap
    m = worldmap.load()
    path = bfs((x0, y0), (x1, y1), lambda n: m[n[1]][n[0]] in (1, 2))
    print(len(path), ','.join(t + ',w30' for t in path))


if __name__ == '__main__':
    a = sys.argv[1:]
    name = a[a.index('--name') + 1] if '--name' in a else 'ultima'
    ok = {int(v, 16) for v in (a[a.index('--ok') + 1] if '--ok' in a else '1,3e,36,3a,38,3c,3d,3f,34,35').split(',')}
    if a and a[0] == 'town':
        town(int(a[1], 16), int(a[2], 16), name, ok)
    elif a and a[0] == 'over':
        over(*[int(v, 16) for v in a[1:5]])
    else:
        print(__doc__)
