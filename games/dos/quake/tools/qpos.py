"""Quake (DOS shareware): find standing spots near a point from the map's BSP, and print TP tokens.

  python3 games/dos/quake/tools/qpos.py MAP X Y Z [--dist 150:400] [--n 6] [--eye 22] [--face X,Y,Z]

Searches a ring of spots around (X Y Z) (every 15 degrees, distances from --dist in steps of 50), keeps those
where the player's hull fits (hull 1 of the world model is empty), drops each to the floor, and keeps those
that see the target (no solid leaf on the line from the eye to the point, hull 0). Prints the best --n as
`TP:origin:angles` tokens (game.json macro TP: pokes the player's origin, angles and fixangle) facing the
target, or facing --face. `MAP X Y Z --here [--open]` prints the TP token for that exact spot (dropped to the floor;
--open: facing the longest free line of sight, the six longest listed as yaw:distance).
The player origin is 24 above the floor; a monster's origin is its own (Shambler 32 above its floor).
"""
import math, os, re, struct, sys, zipfile

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", ".."))


def load(mapname):
    z = zipfile.ZipFile(os.path.join(ROOT, "rom", "quake.zip"))
    pak = z.read([x for x in z.namelist() if x.upper().endswith("PAK0.PAK")][0])
    _, off, ln = struct.unpack("<4sii", pak[:12])
    files = {}
    for i in range(ln // 64):
        name, o, s = struct.unpack("<56sii", pak[off + i * 64:off + i * 64 + 64])
        files[name.split(b"\0")[0].decode()] = (o, s)
    o, s = files["maps/%s.bsp" % mapname]
    return pak[o:o + s]


class Bsp:
    def __init__(self, b):
        lump = lambda n: struct.unpack("<ii", b[4 + n * 8:12 + n * 8])
        po, pl = lump(1)
        self.planes = [struct.unpack("<4fi", b[po + i * 20:po + i * 20 + 20]) for i in range(pl // 20)]
        no, nl = lump(5)
        self.nodes = [struct.unpack("<ihh", b[no + i * 24:no + i * 24 + 8]) for i in range(nl // 24)]
        lo, ll = lump(10)
        self.leafs = [struct.unpack("<i", b[lo + i * 28:lo + i * 28 + 4])[0] for i in range(ll // 28)]
        co, cl = lump(9)
        self.clip = [struct.unpack("<ihh", b[co + i * 8:co + i * 8 + 8]) for i in range(cl // 8)]
        mo, _ = lump(14)
        self.head = struct.unpack("<4i", b[mo + 36:mo + 52])

    def _side(self, pn, p):
        nx, ny, nz, d, t = self.planes[pn]
        v = p[t] - d if t < 3 else nx * p[0] + ny * p[1] + nz * p[2] - d
        return 0 if v >= 0 else 1

    def point0(self, p):
        """contents of point p in hull 0 (-1 empty, -2 solid, -3 water, -4 slime, -5 lava, -6 sky)"""
        n = self.head[0]
        while n >= 0:
            pn, c0, c1 = self.nodes[n]
            n = (c0, c1)[self._side(pn, p)]
        return self.leafs[-n - 1]

    def point1(self, p):
        """contents for a player origin at p (hull 1, 32x32x56)"""
        n = self.head[1]
        while n >= 0:
            pn, c0, c1 = self.clip[n]
            n = (c0, c1)[self._side(pn, p)]
        return n

    def fits(self, p):
        return self.point1(p) not in (-2, -6)

    def floor(self, x, y, z, down=400):
        """drop a fitting origin to the floor (None if it falls more than `down`)"""
        if not self.fits((x, y, z)):
            return None
        for dz in range(0, down, 2):
            if not self.fits((x, y, z - dz - 2)):
                return z - dz
        return None

    def sees(self, a, b):
        n = int(max(abs(b[i] - a[i]) for i in range(3)) / 8) + 1
        return all(self.point0([a[i] + (b[i] - a[i]) * k / n for i in range(3)]) != -2 for k in range(1, n))


def tok(x, y, z, yaw, pitch=0.0):
    f3 = lambda *v: struct.pack("<3f", *v).hex().upper()
    return "TP:%s:%s" % (f3(x, y, z), f3(pitch, yaw, 0))


def aim(x, y, z, t, eye=22):
    dx, dy, dz = t[0] - x, t[1] - y, t[2] - (z + eye)
    yaw = math.degrees(math.atan2(dy, dx)) % 360
    pitch = -math.degrees(math.atan2(dz, math.hypot(dx, dy)))   # Quake: positive pitch looks down
    return round(yaw, 1), round(pitch, 1)


def main():
    a = sys.argv[1:]
    opt = lambda k, d: (a[a.index(k) + 1] if k in a else d)
    m = a[0]
    t = tuple(float(v) for v in a[1:4])
    bsp = Bsp(load(m))
    eye = float(opt("--eye", 22))
    face = tuple(float(v) for v in opt("--face", "%g,%g,%g" % t).split(","))
    if "--here" in a:
        z = bsp.floor(t[0], t[1], t[2])
        if z is not None and "--open" in a:
            # face the longest free line of sight from the eye (16-unit steps, up to 2000)
            def reach(yaw):
                c, s_ = math.cos(math.radians(yaw)), math.sin(math.radians(yaw))
                for k in range(1, 125):
                    if bsp.point0((t[0] + c * 16 * k, t[1] + s_ * 16 * k, z + eye)) == -2:
                        return k * 16
                return 2000
            best = sorted(((reach(y), y) for y in range(0, 360, 15)), reverse=True)
            print("open", " ".join("%d:%d" % (y, r) for r, y in best[:6]))
            face = (t[0] + math.cos(math.radians(best[0][1])) * 500, t[1] + math.sin(math.radians(best[0][1])) * 500, z + eye)
        print("here", "no fit" if z is None else tok(t[0], t[1], z, *aim(t[0], t[1], z, face, eye)), z)
        return
    lo, hi = (int(v) for v in opt("--dist", "150:400").split(":"))
    out = []
    for d in range(lo, hi + 1, 50):
        for ang in range(0, 360, 15):
            x = round(t[0] + d * math.cos(math.radians(ang)))
            y = round(t[1] + d * math.sin(math.radians(ang)))
            for z0 in (t[2] + 8, t[2] + 40, t[2] + 80):
                z = bsp.floor(x, y, z0)
                if z is None or abs(z - t[2]) > 120:
                    continue
                if not bsp.sees((x, y, z + eye), face):
                    continue
                out.append((abs(d - (lo + hi) / 2), d, ang, x, y, z))
                break
    out.sort()
    for _, d, ang, x, y, z in out[:int(opt("--n", 6))]:
        print("d%d a%d  %d %d %g  %s" % (d, ang, x, y, z, tok(x, y, z, *aim(x, y, z, face, eye))))
    if not out:
        print("no spot")


if __name__ == "__main__":
    main()
