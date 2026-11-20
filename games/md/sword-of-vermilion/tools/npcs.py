#!/usr/bin/env python3
"""List the townspeople of the current town: tile, whether they moved, and their line.

  python3 games/md/sword-of-vermilion/tools/npcs.py "ROUTE" [--watch N:STEP]

ROUTE ends inside a town. Each person is two 16x16 objects (head, feet) from FFD0E0, 0x40 apart: byte 0 bit 7 =
in use, +0x0E world x, +0x12 world y (pixels, tile*16+8), +0x1C line pointer (ROM text). The hero is FFD020
(same fields; its tile is FFC606/FFC608). --watch samples N more times STEP frames apart and marks who moved:
stand next to a still person, face them, then `c,w40,c,w150` (Talk).
--plan CP prints one Talk route per person within 15 tiles (plan-file lines `id | route`, starting at @CP, which
must be the state ROUTE ends in): a BFS over the town collision grid, FF2000 (a 64x64 window of 8-pixel cells,
one word each, 128 bytes per row; high nibble 0, 2, 3, E or F = open; a 16-pixel tile is cell (2x+1, 2y+1), the
window wraps every 32 tiles, so only nearby tiles are valid), people's tiles blocked. It prefers standing left
or right of the person (side by side), then below.
"""
import os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
sys.path.insert(0, os.path.join(ROOT, "tools"))
os.chdir(ROOT)
import emu as E

ROM = None


def people(em):
    out = []
    for i in range(48):
        a = 0xFFD0E0 + i * 0x40
        b = em.peek(a, 0x40)
        if not (b[0] & 0x80):
            continue
        w = lambda o: int.from_bytes(b[o:o + 2], "big")
        p = int.from_bytes(b[0x1C:0x20], "big")
        t = ROM[p:p + 60].split(b"\xff")[0].replace(b"\xfe", b" ").decode("latin1") if 0 < p < len(ROM) else ""
        out.append((i, (w(0x0E) - 8) // 16, (w(0x12) - 8) // 16, t))
    return out


DIRS = {"up": (0, -1), "down": (0, 1), "left": (-1, 0), "right": (1, 0)}


def open_tile(grid, x, y):
    cx, cy = (2 * x + 1) % 64, (2 * y + 1) % 64
    v = int.from_bytes(grid[cy * 128 + cx * 2:cy * 128 + cx * 2 + 2], "big") >> 12
    return v in (0, 2, 3, 14, 15)


def plan(em, cp, who, name):
    from collections import deque
    grid = em.peek(0xFF2000, 0x2000)
    h = em.peek(0xFFC606, 4)
    hx, hy = int.from_bytes(h[:2], "big"), int.from_bytes(h[2:], "big")
    blocked = {(x, y) for _, x, y, _ in who}
    prev = {(hx, hy): None}
    q = deque([(hx, hy)])
    while q:
        x, y = q.popleft()
        for d, (dx, dy) in DIRS.items():
            n = (x + dx, y + dy)
            if n in prev or n in blocked or abs(n[0] - hx) > 15 or abs(n[1] - hy) > 15:
                continue
            if open_tile(grid, *n):
                prev[n] = ((x, y), d)
                q.append(n)
    for i, x, y, t in who:
        for sx, sy, face in ((x + 1, y, "left"), (x - 1, y, "right"), (x, y + 1, "up")):
            if (sx, sy) not in prev:
                continue
            steps, c = [], (sx, sy)
            while prev[c]:
                c, d = prev[c]
                steps.append(d)
            steps.reverse()
            runs = []
            for d in steps:
                if runs and runs[-1][0] == d:
                    runs[-1][1] += 1
                else:
                    runs.append([d, 1])
            toks = ["%s:%d,w10,settle" % (d, 16 * n) for d, n in runs]
            print("%s_%d | @%s,%s%s:4,w10,settle,c,w40,c,w150" % (name, i, cp, "".join(t + "," for t in toks), face))
            break


def main():
    global ROM
    args = sys.argv[1:]
    watch = (0, 0)
    if "--watch" in args:
        k = args.index("--watch")
        n, s = args[k + 1].split(":")
        watch = (int(n), int(s))
        del args[k:k + 2]
    cp = None
    if "--plan" in args:
        k = args.index("--plan")
        cp = args[k + 1]
        del args[k:k + 2]
    g = E.Game("sword-of-vermilion")
    ROM = open(g.rom_file(), "rb").read()
    em, rest, _ = E.start(g, args[0])
    E.play(em, g, rest)
    hero = em.peek(0xFFC606, 4)
    print("hero tile", int.from_bytes(hero[:2], "big"), int.from_bytes(hero[2:], "big"), "town", em.peek(0xFFC40C, 2).hex())
    first = people(em)
    if cp:
        plan(em, cp, first, cp.split(",")[0].replace("m_", ""))
        return
    seen = {i: {(x, y)} for i, x, y, _ in first}
    for _ in range(watch[0]):
        E.play(em, g, ["w%d" % watch[1]])
        for i, x, y, _ in people(em):
            seen.setdefault(i, set()).add((x, y))
    for i, x, y, t in first:
        moved = "moves" if len(seen[i]) > 1 else "still"
        print("%2d  %2d,%2d  %s  %s" % (i, x, y, moved, t))


if __name__ == "__main__":
    main()
