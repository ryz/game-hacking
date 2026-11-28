"""Alien vs Predator (Jaguar): honest walking by path search over the level grid in RAM.

  python3 games/jaguar/alien-vs-predator/tools/avpwalk.py ROUTE X,Y [X,Y ...] [--doors 88,80,40,48] [--face ANGLE]

Plays ROUTE, then walks the player cell by cell to each target (breadth-first search over the 64x64 wall
grid at 4FC00, see avpmap.py) with ordinary pad presses only: turns (left:N / right:N) and forward steps
(up:N), each chosen from the position and angle in RAM after the previous token. Prints the tokens to append
to ROUTE (a reproducible route: the emulator is deterministic) and the final position. Walls with ids in
--doors count as passable (doors and bars that open with A: the walker presses A when blocked by one).
--hurt-ok keeps walking when energy falls (acid, a fight); otherwise the walk stops there.
--face ANGLE turns to that angle at the end (0000 east, 4000 north, 8000 west, C000 south).
"""
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', '..', 'tools'))
import emu

G = emu.Game('alien-vs-predator')
DX = {0: (-1, 0), 1: (0, -1), 2: (1, 0), 3: (0, 1)}   # wall byte index: W N E S

def rd(e, a, n):
    return int.from_bytes(bytes(e.peek(a, n)), 'big')

def state(e):
    x = rd(e, 0x2F1CE, 4) / 65536.0
    y = rd(e, 0x2F1D2, 4) / 65536.0
    return x, y, rd(e, 0x2F1D6, 2)

def path(m, start, goal, doors):
    from collections import deque
    cell = lambda x, y: m[(y * 64 + x) * 8:(y * 64 + x) * 8 + 8]
    prev = {start: None}; q = deque([start])
    while q:
        c = q.popleft()
        if c == goal: break
        cc = cell(*c)
        for k, (dx, dy) in DX.items():
            n = (c[0] + dx, c[1] + dy)
            if not (0 <= n[0] < 64 and 0 <= n[1] < 64) or n in prev: continue
            w1 = cc[k]; w2 = cell(*n)[(k + 2) % 4]
            if (w1 and w1 not in doors) or (w2 and w2 not in doors): continue
            if not any(cell(*n)): continue
            prev[n] = c; q.append(n)
    if goal not in prev: return None
    p = [goal]
    while prev[p[-1]] is not None: p.append(prev[p[-1]])
    return p[::-1]

def run(e, toks, out):
    emu.play(e, G, emu.expand(G, emu.split(toks)))
    out.append(toks)

def adiff(want, ang):
    d = (want - ang) & 0xFFFF
    return d - 0x10000 if d >= 0x8000 else d

def turn_to(e, want, out, tol=0x300):
    for _ in range(40):
        d = adiff(want, state(e)[2])
        if abs(d) <= tol: return
        n = max(2, min(12, abs(d) // 420))
        run(e, ('left:%d' if d > 0 else 'right:%d') % n + ',w4', out)

def main():
    a = sys.argv[1:]
    doors = {88, 80, 40, 48}
    if '--doors' in a:
        i = a.index('--doors'); doors = {int(v) for v in a[i + 1].split(',')}; del a[i:i + 2]
    face = None
    hurt_ok = '--hurt-ok' in a
    if hurt_ok: a.remove('--hurt-ok')
    if '--face' in a:
        i = a.index('--face'); face = int(a[i + 1], 16); del a[i:i + 2]
    route, targets = a[0], [tuple(int(v) for v in t.split(',')) for t in a[1:]]
    e, rest, full = emu.start(G, route); emu.play(e, G, rest)
    out = []
    e0 = rd(e, 0x30A6A, 2)
    alive = lambda: hurt_ok or rd(e, 0x30A6A, 2) == e0
    for goal in targets:
        if not alive(): break
        m = bytes(e.peek(0x4FC00, 64 * 64 * 8))
        x, y, ang = state(e)
        p = path(m, (int(x), int(y)), goal, doors)
        if p is None: print('no path to', goal); break
        for c in p[1:]:
            tx, ty = c[0] + 0.5, c[1] + 0.5
            for _ in range(30):
                if not alive():
                    print('energy changed (attack?) near', c); break
                x, y, ang = state(e)
                dist = math.hypot(tx - x, ty - y)
                if dist < 0.3: break
                want = int(math.atan2(-(ty - y), tx - x) / (2 * math.pi) * 65536) & 0xFFFF
                if abs(adiff(want, ang)) > 0x900: turn_to(e, want, out)
                before = (x, y)
                run(e, 'up:%d' % max(4, min(16, int(dist * 20))), out)
                x, y, ang = state(e)
                if math.hypot(x - before[0], y - before[1]) < 0.02:
                    run(e, 'a,w40', out)          # blocked: open the door in front
            else:
                print('stuck near', c, state(e)); break
            if not alive(): break
    if face is not None: turn_to(e, face, out, tol=0x200)
    run(e, 'w20', out)
    x, y, ang = state(e)
    print('end x=%.2f y=%.2f angle=%04X level=%d energy=%d' % (x, y, ang, rd(e, 0x2F5AA, 2), rd(e, 0x30A6A, 2)))
    print(','.join(out))

if __name__ == '__main__':
    main()
