"""The Ultimate Doom: turn a list of goals into key tokens (real key holds, no pokes) by playing them with RAM
feedback, so a route walks and fights like a player and stays a plain token route.

  python3 games/dos/doom/tools/dnav.py "ROUTE" "go X Y; face X Y; fire N; use; wait N; keys TOKS; mons" [--png DIR] [--out FILE]

Commands (separated by ';'):
  path X Y     plan a grid path there (wadmap: walls, steps > 24, low ceilings, hurting floors avoided;
               `pathhurt` allows them, `pathrun` runs) and go along it; doors on the way get a `use`
  go X Y       turn toward X Y and walk there (chunks of at most 40 frames, re-aimed; stops within 20 units)
  run X Y      the same holding Shift (rshift, the key_speed of DEFAULT.CFG)
  face X Y     turn toward the point (within ~2 degrees)
  aim [TYPE]   turn toward the nearest living monster (optionally of mobj type number TYPE)
  fight N [R]  up to N rounds of: aim at the nearest living monster within R units (900), ctrl:20
  fire N       hold Ctrl for N frames (`ctrl:N`), then wait 10
  use          Space (doors, switches), then wait 30
  wait N       wN
  keys TOKS    any tokens as they are (commas allowed inside: write them with '+' between them: keys 1+w20)
  mons         list living monsters (type, x, y, health, distance)
At the end it prints the tokens (to paste into a macro or a shot route) and the state after every command.
Monsters are found by scanning memory for mobjs whose info pointer matches mobjinfo[type] (the player's
mobj gives the table's address).
"""
import math, os, struct, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import dstate as D
E = D.E
import numpy as np

NAMES = {1: "Zombieman", 2: "Shotgun guy", 11: "Imp", 12: "Demon", 13: "Spectre", 15: "Baron",
         16: "Cacodemon", 18: "Lost soul", 19: "Spider Mastermind", 21: "Cyberdemon"}
# 1.9 type numbers (kept as the names' keys, bosskill.py takes them) from the editor numbers in mobjinfo
DOOMED = {3004: 1, 9: 2, 3001: 11, 3002: 12, 58: 13, 3003: 15, 3005: 16, 3006: 18, 7: 19, 16: 21}


def player(emu):
    mo = D.mo_addr(emu)
    m = emu.peek(mo, 112)
    x, y, z = struct.unpack_from("<3i", m, 12)
    a = struct.unpack_from("<I", m, 32)[0]
    return x / 65536, y / 65536, a / 2 ** 32 * 360, mo


def monsters(emu):
    # 1.1: mobjs are packed at any byte address and the type numbers differ from 1.9's, so search
    # both alignments and name a monster by its mobjinfo doomednum (first field).
    mo = D.mo_addr(emu)
    info0 = struct.unpack("<I", emu.peek(mo + 92, 4))[0]  # &mobjinfo[MT_PLAYER = 0]
    base, size = emu._mem()
    lo = 0x100000
    raw = emu.peek(lo, size - lo)
    out = []
    px, py, _, _ = player(emu)
    for al in (0, 1, 2, 3):
        a = np.frombuffer(raw[al:][: (size - lo - al) // 4 * 4], dtype=np.uint32)
        t = a[22:]; inf = a[23:]
        n = min(len(t), len(inf))
        ok = np.nonzero((t[:n] < 140) & (inf[:n] == info0 + t[:n] * 88))[0]
        for i in ok:
            addr = lo + al + 4 * int(i)
            typ = DOOMED.get(struct.unpack("<i", emu.peek(info0 + int(a[i + 22]) * 88, 4))[0])
            hp = struct.unpack("<i", emu.peek(addr + 108, 4))[0]
            if typ in NAMES and hp > 0:
                x, y = struct.unpack("<2i", emu.peek(addr + 12, 8))
                x /= 65536; y /= 65536
                out.append((math.hypot(x - px, y - py), typ, x, y, hp, addr))
    return sorted(out)


def turn_tokens(delta):
    """frames of left/right for a turn of delta degrees (positive = left/counter-clockwise)."""
    d = abs(delta)
    slow = 6 * 1.7578
    tics = d / 1.7578 if d <= slow else 6 + (d - slow) / 3.5156
    frames = max(1, int(round(tics * 2)))
    return ("left:%d" if delta > 0 else "right:%d") % frames


def plan(mapname, start, goal, cell=16, clear=18, allow_hurt=False):
    """Grid path (8-neighbour BFS) from start to goal on the map: a cell is free if no blocking line passes
    within `clear` units (one-sided, ML_BLOCKING, or two-sided with a step > 24 or < 56 headroom; door lines
    count as passable) and its floor does not hurt (specials 4, 5, 7, 11, 16) unless allow_hurt. Returns
    waypoints (straight stretches merged)."""
    import wadmap, collections
    m = wadmap.Map(wadmap.wad(), mapname)
    segs = []
    for l in m.lines:
        (x1, y1), (x2, y2) = m.verts[l[0]], m.verts[l[1]]
        block = l[6] == -1 or (l[2] & 1)
        if not block:
            a, b = m.sectors[m.sides[l[5]][5]], m.sectors[m.sides[l[6]][5]]
            door = l[3] in wadmap.DOOR or l[3] in wadmap.KEYDOOR
            if not door and (abs(a[0] - b[0]) > 24 or min(a[1], b[1]) - max(a[0], b[0]) < 56):
                block = True
        if block:
            segs.append((x1, y1, x2, y2))
    # solid decorations and barrels block like a short wall box (radius ~16-20)
    SOLID = {2035, 2028, 30, 31, 32, 33, 35, 36, 37, 41, 42, 43, 44, 45, 46, 47, 48, 54, 55, 56, 57, 85, 86,
             70, 25, 26, 27, 28, 29, 49}
    for x, y, a_, t, f in m.things_on(3):
        if t in SOLID:
            r = 18
            segs += [(x - r, y - r, x + r, y - r), (x + r, y - r, x + r, y + r), (x + r, y + r, x - r, y + r),
                     (x - r, y + r, x - r, y - r)]
    S = np.array(segs, dtype=float)
    xs = [v[0] for v in m.verts]; ys = [v[1] for v in m.verts]
    gx = np.arange(min(xs), max(xs), cell) + cell / 2; gy = np.arange(min(ys), max(ys), cell) + cell / 2
    X, Y = np.meshgrid(gx, gy)
    P = np.stack([X.ravel(), Y.ravel()], 1)
    free = np.ones(len(P), bool)
    for x1, y1, x2, y2 in S:
        dx, dy = x2 - x1, y2 - y1
        t = np.clip(((P[:, 0] - x1) * dx + (P[:, 1] - y1) * dy) / max(dx * dx + dy * dy, 1e-9), 0, 1)
        d = np.hypot(P[:, 0] - x1 - t * dx, P[:, 1] - y1 - t * dy)
        free &= d > clear
    free = free.reshape(X.shape)
    hurt = {4, 5, 7, 11, 16}
    sec = {}
    def floor_ok(i, j):
        k = (i, j)
        if k not in sec:
            s_ = m.sectors[m.sector_at(gx[j], gy[i])]
            sec[k] = (s_[0], s_[1], s_[5] in hurt)
        return sec[k]
    cell_of = lambda x, y: (int((y - gy[0]) / cell + 0.5), int((x - gx[0]) / cell + 0.5))
    a, b = cell_of(*start), cell_of(*goal)
    prev = {a: None}; q = collections.deque([a])
    while q:
        c = q.popleft()
        if c == b:
            break
        fa = floor_ok(*c)
        for di in (-1, 0, 1):
            for dj in (-1, 0, 1):
                n = (c[0] + di, c[1] + dj)
                if n in prev or not (0 <= n[0] < len(gy) and 0 <= n[1] < len(gx)):
                    continue
                if not free[n] and n != b:
                    continue
                fb = floor_ok(*n)
                if fb[0] - fa[0] > 24 or (fb[2] and not allow_hurt and n != b):
                    continue
                prev[n] = c; q.append(n)
    if b not in prev:
        return None
    path = []; c = b
    while c is not None:
        path.append((float(gx[c[1]]), float(gy[c[0]]))); c = prev[c]
    path.reverse()
    # keep turning points only
    out = [path[0]]
    for i in range(1, len(path) - 1):
        d1 = (path[i][0] - path[i - 1][0], path[i][1] - path[i - 1][1])
        d2 = (path[i + 1][0] - path[i][0], path[i + 1][1] - path[i][1])
        if d1 != d2:
            out.append(path[i])
    out.append(path[-1])
    # drop points closer than 48 units to the previous kept one
    res = [out[0]]
    for p_ in out[1:]:
        if math.hypot(p_[0] - res[-1][0], p_[1] - res[-1][1]) >= 48 or p_ == out[-1]:
            res.append(p_)
    return res[1:]


class Nav:
    def __init__(self, route):
        self.g = E.Game("dos/doom")
        self.emu, rest, _ = E.start(self.g, route)
        E.play(self.emu, self.g, rest)
        self.toks = []

    def do(self, toks):
        t = E.split(toks)
        E.play(self.emu, self.g, E.expand(self.g, t))
        self.toks += t

    def face(self, tx, ty, tol=2.0):
        for _ in range(4):
            x, y, a, _ = player(self.emu)
            want = math.degrees(math.atan2(ty - y, tx - x))
            delta = (want - a + 180) % 360 - 180
            if abs(delta) <= tol:
                return
            self.do(turn_tokens(delta) + ",w4")

    def go(self, tx, ty, run=False):
        last = None; tried_use = False
        for _ in range(60):
            x, y, a, _ = player(self.emu)
            dist = math.hypot(tx - x, ty - y)
            if dist < 20:
                return True
            if last is not None and math.hypot(x - last[0], y - last[1]) < 3:
                if not tried_use:
                    tried_use = True; self.face(tx, ty, tol=2.0); self.do("space,w40"); last = None
                    continue
                print("  stuck at %.0f %.0f going to %d %d" % (x, y, tx, ty))
                return False
            last = (x, y)
            self.face(tx, ty, tol=4.0)
            frames = int(max(4, min(40, dist / (5.5 if run else 3.2))))
            self.do(("rshift+up:%d" if run else "up:%d") % frames + ",w6")
        return False


def main():
    a = sys.argv[1:]
    png = None
    if "--png" in a:
        i = a.index("--png"); png = a[i + 1]; del a[i:i + 2]; os.makedirs(png, exist_ok=True)
    out = None
    if "--out" in a:
        i = a.index("--out"); out = a[i + 1]; del a[i:i + 2]
    nav = Nav(a[0])
    frames = []
    for n, cmd in enumerate(c.strip() for c in a[1].split(";") if c.strip()):
        w = cmd.split()
        if w[0] in ("path", "pathrun", "pathhurt"):
            x, y, _, _ = player(nav.emu)
            wps = plan(D.current_map(nav.emu), (x, y), (float(w[1]), float(w[2])), allow_hurt=w[0] == "pathhurt")
            print("  path:", None if wps is None else " ".join("%d,%d" % p_ for p_ in wps))
            for p_ in wps or []:
                if not nav.go(*p_, run=w[0] == "pathrun"):
                    break
        elif w[0] in ("go", "run"):
            nav.go(float(w[1]), float(w[2]), run=w[0] == "run")
        elif w[0] == "face":
            nav.face(float(w[1]), float(w[2]))
        elif w[0] == "aim":
            ms = [m for m in monsters(nav.emu) if len(w) < 2 or m[1] == int(w[1])]
            if ms:
                nav.face(ms[0][2], ms[0][3], tol=1.5)
        elif w[0] == "fight":
            # up to N rounds: aim at the nearest living monster within R units (default 900), fire 20 frames
            r = float(w[2]) if len(w) > 2 else 900
            for _ in range(int(w[1])):
                ms = [m for m in monsters(nav.emu) if m[0] < r]
                if not ms:
                    break
                nav.face(ms[0][2], ms[0][3], tol=1.5)
                nav.do("ctrl:20,w6")
        elif w[0] == "fire":
            nav.do("ctrl:%s,w10" % w[1])
        elif w[0] == "use":
            nav.do("space,w30")
        elif w[0] == "wait":
            nav.do("w%s" % w[1])
        elif w[0] == "keys":
            nav.do(w[1].replace("+", ","))
        elif w[0] == "mons":
            for d, typ, x, y, hp, addr in monsters(nav.emu):
                print("  %-12s %6.0f %6.0f hp %3d dist %5.0f  mobj %X" % (NAMES[typ], x, y, hp, d, addr))
        print("%02d %-22s %s" % (n, cmd[:22], D.state(nav.emu)))
        if png:
            p = os.path.join(png, "%02d.png" % n); nav.emu.image().save(p); frames.append(p)
    if png:
        E.sheet(frames, os.path.join(png, "sheet.png"), cols=4, labels=["%02d" % i for i in range(len(frames))])
    print("TOKENS:", ",".join(nav.toks)[:300], "..." if len(",".join(nav.toks)) > 300 else "")
    if out:
        open(out, "w").write(",".join(nav.toks) + "\n"); print("tokens written to", out)


if __name__ == "__main__":
    main()
