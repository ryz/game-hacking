"""Shortest walking route (tokens) on a floor map from the ROM: python3 tools/maze_route.py FLOOR X0 Y0 DIR0 X1 Y1
(env ROUTE_ALLOW=4,6,8 lets it cross special squares)
Map: bank $3E, $4000 + $400*(FLOOR-1), cell = 4 bytes at ((y^15)<<4|x)*4; byte0 = walls, 2 bits per dir
(dir 0 y+1, 1 x+1, 2 y-1, 3 x-1; 0 open, 2 door); byte2&$3F = square type. 'right' = dir+1."""
import sys
from collections import deque
r = open('/home/user/game-translations/wizardry-empire/rom/wizardry_empire_j.gbc', 'rb').read()
f, x0, y0, d0, x1, y1 = map(int, sys.argv[1:7])
import os
WALLS = {0, 2} | ({3} if os.environ.get("ROUTE_W3") else set())
import os; OK = {0, 1, 5} | {int(t, 16) for t in os.environ.get("ROUTE_ALLOW", "").split(",") if t}
m = r[0x3E * 0x4000 + (f - 1) * 0x400:][:0x400]
cell = lambda x, y: m[(((y ^ 15) << 4) | x) * 4:][:4]
D = {0: (0, 1), 1: (1, 0), 2: (0, -1), 3: (-1, 0)}
prev = {(x0, y0): None}; q = deque([(x0, y0)])
while q:
    x, y = q.popleft()
    if (x, y) == (x1, y1): break
    for d, (dx, dy) in D.items():
        if (cell(x, y)[0] >> 2 * d) & 3 not in WALLS: continue
        n = ((x + dx) & 15, (y + dy) & 15)
        if n in prev: continue
        if n != (x1, y1) and cell(*n)[2] & 0x3f not in OK: continue
        prev[n] = ((x, y), d); q.append(n)
path = []; n = (x1, y1)
while prev[n]: p, d = prev[n]; path.append(d); n = p
path.reverse()
toks = []; d = d0
for nd in path:
    t = (nd - d) % 4
    toks += {0: [], 1: ['right'], 2: ['right', 'right'], 3: ['left']}[t]
    toks.append('up'); d = nd
print(','.join(toks))
