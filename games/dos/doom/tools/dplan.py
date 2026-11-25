# Moved from work/plan (capture 2026-11-25). Usage: python3 games/dos/doom/tools/dplan.py SPEC OUT
"""Generate Doom main-set plan lines: prefix route, TP to a spot facing a point, dnav commands, raw suffix.
Spec lines:  id | category | caption | PREFIX | X Y ANG|@MX,MY | CMDS (dnav: go/face/aim/fight/fire/keys/wait, ';') | SUFFIX
X Y '-' = no teleport. Output: plan lines (route = PREFIX,TP...,cmd tokens,SUFFIX) on stdout, state on stderr.
"""
import math, os, sys, multiprocessing as mp
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", ".."))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)


def autospot(mapname, mx, my, dmin=180, dmax=620):
    """a point dmin..dmax from the monster: same height band, 32 units from walls, nothing solid between,
    no other monster within 160; returns 'X Y @MX,MY'."""
    import wadmap
    m = wadmap.Map(wadmap.wad(), mapname)
    ms = m.sectors[m.sector_at(mx, my)]
    walls = []
    for l in m.lines:
        (x1, y1), (x2, y2) = m.verts[l[0]], m.verts[l[1]]
        if l[6] == -1:
            walls.append((x1, y1, x2, y2, True))
        else:
            a_, b_ = m.sectors[m.sides[l[5]][5]], m.sectors[m.sides[l[6]][5]]
            if min(a_[1], b_[1]) - max(a_[0], b_[0]) < 56 or max(a_[0], b_[0]) > ms[0] + 40:
                walls.append((x1, y1, x2, y2, False))
    def cross(p, q, w):
        (ax, ay), (bx, by) = p, q
        cx, cy, dx, dy = w[:4]
        d = (bx - ax) * (dy - cy) - (by - ay) * (dx - cx)
        if d == 0: return False
        t = ((cx - ax) * (dy - cy) - (cy - ay) * (dx - cx)) / d
        u = ((cx - ax) * (by - ay) - (cy - ay) * (bx - ax)) / d
        return 0 < t < 1 and 0 < u < 1
    def dseg(px, py, w):
        x1, y1, x2, y2 = w[:4]; dx, dy = x2 - x1, y2 - y1
        t = max(0, min(1, ((px - x1) * dx + (py - y1) * dy) / max(dx * dx + dy * dy, 1e-9)))
        return math.hypot(px - x1 - t * dx, py - y1 - t * dy)
    mons = [(x, y) for x, y, a_, t, f in m.things_on(3) if t in (3004, 9, 3001, 3002, 58, 3006, 3005, 3003, 16, 7)]
    for d in range(int(dmax), int(dmin) - 1, -32):
        for k in range(24):
            an = k * 15
            px, py = mx + d * math.cos(math.radians(an)), my + d * math.sin(math.radians(an))
            try:
                s_ = m.sectors[m.sector_at(px, py)]
            except Exception:
                continue
            if s_[1] - s_[0] < 72 or abs(s_[0] - ms[0]) > 40 or s_[5] in (4, 5, 7, 11, 16):
                continue
            if any(dseg(px, py, w) < 34 for w in walls):
                continue
            if any(cross((px, py), (mx, my), w) for w in walls):
                continue
            if any(math.hypot(px - x, py - y) < 160 and math.hypot(mx - x, my - y) > 200 for x, y in mons) or any(math.hypot(px - x, py - y) < 180 for x, y in mons):
                continue
            return "%d %d @%d,%d" % (px, py, mx, my)
    raise SystemExit("no spot near %d %d" % (mx, my))


_W = {}
def walls_of(mapname):
    if mapname not in _W:
        import wadmap
        m = wadmap.Map(wadmap.wad(), mapname); ws = []
        for l in m.lines:
            (x1, y1), (x2, y2) = m.verts[l[0]], m.verts[l[1]]
            if l[6] == -1:
                ws.append((x1, y1, x2, y2))
            else:
                a_, b_ = m.sectors[m.sides[l[5]][5]], m.sectors[m.sides[l[6]][5]]
                if min(a_[1], b_[1]) - max(a_[0], b_[0]) < 40:
                    ws.append((x1, y1, x2, y2))
        _W[mapname] = ws
    return _W[mapname]


def los(mapname, p, q):
    (ax, ay), (bx, by) = p, q
    for cx, cy, dx, dy in walls_of(mapname):
        d = (bx - ax) * (dy - cy) - (by - ay) * (dx - cx)
        if d == 0: continue
        t = ((cx - ax) * (dy - cy) - (cy - ay) * (dx - cx)) / d
        u = ((cx - ax) * (by - ay) - (cy - ay) * (bx - ax)) / d
        if 0 < t < 1 and 0 < u < 1: return False
    return True


def visible(nav, N, D, r):
    px, py, _, _ = N.player(nav.emu); mp_ = D.current_map(nav.emu)
    return [m for m in N.monsters(nav.emu) if m[0] < r and los(mp_, (px, py), (m[2], m[3]))]


def one(spec):
    import dnav as N, dstate as D
    f = [s.strip() for s in spec.split("|")]
    sid, cat, cap, prefix, spot, cmds = f[:6]
    suffix = f[6] if len(f) > 6 else ""
    nav = N.Nav(prefix)
    if spot != "-":
        if spot.startswith("auto"):
            spot = autospot(D.current_map(nav.emu), *[float(v) for v in spot.split()[1:]])
        x, y, a = spot.split(None, 2)
        x, y = int(x), int(y)
        if a.startswith("@"):
            mx, my = [float(v) for v in a[1:].split(",")]
            a = math.degrees(math.atan2(my - y, mx - x)) % 360
        nav.do(D.tp_tokens(nav.emu, x, y, float(a)))
    for cmd in (c.strip() for c in cmds.split(";") if c.strip()):
        w = cmd.split()
        if w[0] in ("go", "run"):
            nav.go(float(w[1]), float(w[2]), run=w[0] == "run")
        elif w[0] in ("path", "pathhurt"):
            px, py, _, _ = N.player(nav.emu)
            for p_ in N.plan(D.current_map(nav.emu), (px, py), (float(w[1]), float(w[2])), allow_hurt=w[0] == "pathhurt") or []:
                if not nav.go(*p_):
                    break
        elif w[0] == "face":
            nav.face(float(w[1]), float(w[2]))
        elif w[0] == "aim":
            ms = [m for m in N.monsters(nav.emu) if len(w) < 2 or m[1] == int(w[1])]
            if ms:
                nav.face(ms[0][2], ms[0][3], tol=1.5)
        elif w[0] == "fight":
            r = float(w[2]) if len(w) > 2 else 900
            for _ in range(int(w[1])):
                ms = [m for m in N.monsters(nav.emu) if m[0] < r]
                if not ms or D.state(nav.emu).find(" hp 0 ") >= 0:
                    break
                nav.face(ms[0][2], ms[0][3], tol=1.5)
                nav.do("ctrl:20,w6")
        elif w[0] == "seek":   # seek N R: wait up to N frames for a visible monster within R, face it
            for _ in range(int(w[1]) // 10):
                v = visible(nav, N, D, float(w[2]))
                if v:
                    nav.face(v[0][2], v[0][3], tol=1.5); break
                nav.do("w10")
        elif w[0] == "hp":   # hp TYPE VALUE: set every living monster of that type to VALUE health
            import struct as _s
            for m in N.monsters(nav.emu):
                if m[1] == int(w[1]):
                    nav.do("poke:%X=%s" % (m[5] + 108, _s.pack("<i", int(w[2])).hex().upper()))
        elif w[0] == "tp":
            nav.do(D.tp_tokens(nav.emu, int(w[1]), int(w[2]), float(w[3])))
        elif w[0] == "aimv":
            v = visible(nav, N, D, 2000)
            if v: nav.face(v[0][2], v[0][3], tol=1.5)
        elif w[0] == "fire":
            nav.do("ctrl:%s,w10" % w[1])
        elif w[0] == "wait":
            nav.do("w%s" % w[1])
        elif w[0] == "keys":
            nav.do(w[1].replace("+", ","))
        elif w[0] == "mons":
            for d, typ, x_, y_, hp, addr in N.monsters(nav.emu)[:6]:
                sys.stderr.write("  %s %s %.0f %.0f hp %d dist %.0f\n" % (sid, N.NAMES[typ], x_, y_, hp, d))
    st = D.state(nav.emu)
    route = prefix + "," + ",".join(nav.toks) + ("," + suffix if suffix else "")
    return "%s | %s | %s | %s" % (sid, cat, cap, route), "%s: %s" % (sid, st)


if __name__ == "__main__":
    specs = [l.rstrip("\n") for l in open(sys.argv[1]) if l.strip() and not l.startswith("#")]
    out = open(sys.argv[2], "w")
    for sp in specs:
        try:
            line, st = one(sp)
        except SystemExit as e:
            sys.stderr.write("FAIL %s: %s\n" % (sp[:20], e)); continue
        out.write(line + "\n"); out.flush(); sys.stderr.write(st + "\n")
