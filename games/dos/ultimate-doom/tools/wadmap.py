"""The Ultimate Doom (DOS 1.9): read the maps in DOOM.WAD (THINGS, LINEDEFS, SIDEDEFS, VERTEXES, SECTORS,
SEGS, SSECTORS, NODES) for capture planning.

  python3 games/dos/ultimate-doom/tools/wadmap.py list                  every map with counts
  python3 games/dos/ultimate-doom/tools/wadmap.py E1M1 [--skill 3] [--grep RE]
      things on that skill (1-2 = ITYTD/HNTR, 3 = HMP (default), 4-5 = UV/NM; multiplayer-only left out
      unless --mp), then exits, secret sectors, doors with keys, switches/specials, the player start
  python3 games/dos/ultimate-doom/tools/wadmap.py E1M1 --png OUT.png [--skill 3] [--scale 0.25]
      plan of the map: one-sided lines white, two-sided grey, specials yellow, exits red, secret sectors
      filled dark blue; things: monsters red, weapons/ammo cyan, health/armor green, powerups magenta,
      keys in their colour, player start white
  python3 games/dos/ultimate-doom/tools/wadmap.py E1M1 --at X Y        sector at a point (BSP walk):
      floor, ceiling, light, special, tag
  python3 games/dos/ultimate-doom/tools/wadmap.py E1M1 --tp X Y ANGLE  poke tokens for the TP macro
      (16.16 fixed x, y, z = floor at that point, angle in BAM)

Coordinates are Doom map units (x east, y north), the same as the player mobj's x/y in RAM >> 16.
The WAD is read from rom/ultimate-doom.zip (DOOM.WAD) or from --wad PATH.
"""
import io, os, re, struct, sys, zipfile

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", ".."))

# type -> (name, kind) for Doom 1 things (kinds: player, monster, weapon, ammo, health, armor, power, key,
# deco, other)
T = {
    1: ("Player 1 start", "player"), 2: ("Player 2 start", "player"), 3: ("Player 3 start", "player"),
    4: ("Player 4 start", "player"), 11: ("Deathmatch start", "player"), 14: ("Teleport destination", "other"),
    3004: ("Zombieman", "monster"), 9: ("Shotgun guy", "monster"), 3001: ("Imp", "monster"),
    3002: ("Demon", "monster"), 58: ("Spectre", "monster"), 3006: ("Lost soul", "monster"),
    3005: ("Cacodemon", "monster"), 3003: ("Baron of Hell", "monster"), 16: ("Cyberdemon", "monster"),
    7: ("Spider Mastermind", "monster"),
    2005: ("Chainsaw", "weapon"), 2001: ("Shotgun", "weapon"), 2002: ("Chaingun", "weapon"),
    2003: ("Rocket launcher", "weapon"), 2004: ("Plasma gun", "weapon"), 2006: ("BFG9000", "weapon"),
    2007: ("Clip", "ammo"), 2048: ("Box of bullets", "ammo"), 2008: ("4 shells", "ammo"),
    2049: ("Box of shells", "ammo"), 2010: ("Rocket", "ammo"), 2046: ("Box of rockets", "ammo"),
    2047: ("Cell charge", "ammo"), 17: ("Cell pack", "ammo"), 8: ("Backpack", "ammo"),
    2011: ("Stimpack", "health"), 2012: ("Medikit", "health"), 2014: ("Health bonus", "health"),
    2015: ("Armor bonus", "armor"), 2018: ("Green armor", "armor"), 2019: ("Blue armor", "armor"),
    2013: ("Soulsphere", "power"), 2022: ("Invulnerability", "power"), 2023: ("Berserk", "power"),
    2024: ("Partial invisibility", "power"), 2025: ("Radiation suit", "power"), 2026: ("Computer map", "power"),
    2045: ("Light amplification", "power"),
    5: ("Blue keycard", "key"), 6: ("Yellow keycard", "key"), 13: ("Red keycard", "key"),
    40: ("Blue skull key", "key"), 39: ("Yellow skull key", "key"), 38: ("Red skull key", "key"),
    2035: ("Barrel", "other"),
}
KEYCOL = {5: (80, 80, 255), 40: (80, 80, 255), 6: (255, 255, 0), 39: (255, 255, 0), 13: (255, 40, 40),
          38: (255, 40, 40)}
EXIT = {11: "exit", 52: "exit (walk)", 197: "exit (shoot)", 51: "secret exit", 124: "secret exit (walk)",
        198: "secret exit (shoot)"}
KEYDOOR = {26: "blue door", 27: "yellow door", 28: "red door", 32: "blue door (stays)",
           33: "red door (stays)", 34: "yellow door (stays)", 99: "blue door switch", 133: "blue door switch",
           134: "red door switch", 135: "red door switch", 136: "yellow door switch", 137: "yellow door switch"}
DOOR = {1: "door", 31: "door (stays open)", 117: "fast door", 118: "fast door (stays)", 46: "door (shoot)"}


def wad(path=None):
    if path:
        return open(path, "rb").read()
    with zipfile.ZipFile(os.path.join(ROOT, "rom", "ultimate-doom.zip")) as z:
        return z.read("DOOM.WAD")


def lumps(data):
    ident, n, off = struct.unpack_from("<4sii", data, 0)
    out = []
    for i in range(n):
        o, s, name = struct.unpack_from("<ii8s", data, off + 16 * i)
        out.append((name.rstrip(b"\0").decode("ascii", "replace"), o, s))
    return out


class Map:
    def __init__(self, data, name):
        ls = lumps(data)
        i = [k for k, (n, _, _) in enumerate(ls) if n == name.upper()][0]
        L = {n: data[o:o + s] for n, o, s in ls[i + 1:i + 11]}
        self.name = name.upper()
        self.things = [struct.unpack_from("<hhhhh", L["THINGS"], k) for k in range(0, len(L["THINGS"]), 10)]
        self.lines = [struct.unpack_from("<hhhhhhh", L["LINEDEFS"], k) for k in range(0, len(L["LINEDEFS"]), 14)]
        self.sides = [struct.unpack_from("<hh8s8s8sh", L["SIDEDEFS"], k) for k in range(0, len(L["SIDEDEFS"]), 30)]
        self.verts = [struct.unpack_from("<hh", L["VERTEXES"], k) for k in range(0, len(L["VERTEXES"]), 4)]
        self.sectors = [struct.unpack_from("<hh8s8shhh", L["SECTORS"], k) for k in range(0, len(L["SECTORS"]), 26)]
        self.segs = [struct.unpack_from("<hhhhhh", L["SEGS"], k) for k in range(0, len(L["SEGS"]), 12)]
        self.ssec = [struct.unpack_from("<hh", L["SSECTORS"], k) for k in range(0, len(L["SSECTORS"]), 4)]
        self.nodes = [struct.unpack_from("<hhhh8h2H", L["NODES"], k) for k in range(0, len(L["NODES"]), 28)]

    def things_on(self, skill=3, mp=False):
        bit = 1 if skill <= 2 else 2 if skill == 3 else 4
        return [t for t in self.things if (t[4] & bit) and (mp or not t[4] & 16)]

    def sector_at(self, x, y):
        n = len(self.nodes) - 1
        while True:
            nx, ny, dx, dy = self.nodes[n][:4]
            right, left = self.nodes[n][12], self.nodes[n][13]
            side = (x - nx) * dy - (y - ny) * dx  # > 0: right (front) side, as R_PointOnSide
            child = right if side > 0 else left
            if child & 0x8000:
                seg = self.segs[self.ssec[child & 0x7FFF][1]]
                line = self.lines[seg[3]]
                sd = line[5] if seg[4] == 0 else line[6]
                return self.sides[sd][5]
            n = child

    def sector_info(self, s):
        f, c, ft, ct, light, special, tag = self.sectors[s]
        return "sector %d floor %d ceiling %d light %d special %d tag %d (%s/%s)" % (
            s, f, c, light, special, tag, ft.rstrip(b"\0").decode(), ct.rstrip(b"\0").decode())

    def line_mid(self, l):
        (x1, y1), (x2, y2) = self.verts[l[0]], self.verts[l[1]]
        return (x1 + x2) // 2, (y1 + y2) // 2


def report(m, skill, mp, grep):
    print("%s on skill %d: %d things, %d lines, %d sectors" % (m.name, skill, len(m.things), len(m.lines), len(m.sectors)))
    for x, y, a, t, f in m.things_on(skill, mp):
        name, kind = T.get(t, ("type %d" % t, "deco"))
        if kind == "deco":
            continue
        s = "%-9s %-22s %6d %6d  angle %3d  flags %d  sector %d" % (kind, name, x, y, a, f, m.sector_at(x, y))
        if not grep or re.search(grep, s, re.I):
            print(s)
    rows = []
    for i, l in enumerate(m.lines):
        sp, tag = l[3], l[4]
        if sp in EXIT:
            rows.append(("exit", "line %d %s at %d %d" % (i, EXIT[sp], *m.line_mid(l))))
        elif sp in KEYDOOR:
            rows.append(("keydoor", "line %d %s at %d %d" % (i, KEYDOOR[sp], *m.line_mid(l))))
        elif sp in DOOR:
            rows.append(("door", "line %d %s at %d %d" % (i, DOOR[sp], *m.line_mid(l))))
        elif sp:
            rows.append(("special", "line %d special %d tag %d at %d %d" % (i, sp, tag, *m.line_mid(l))))
    for i, s in enumerate(m.sectors):
        if s[5] == 9:
            rows.append(("secret", m.sector_info(i)))
    for k, r in rows:
        s = "%-9s %s" % (k, r)
        if not grep or re.search(grep, s, re.I):
            print(s)


def png(m, out, skill, mp, scale):
    from PIL import Image, ImageDraw
    xs = [v[0] for v in m.verts]; ys = [v[1] for v in m.verts]
    x0, y0, x1, y1 = min(xs) - 32, min(ys) - 32, max(xs) + 32, max(ys) + 32
    W, H = int((x1 - x0) * scale), int((y1 - y0) * scale)
    im = Image.new("RGB", (W, H)); d = ImageDraw.Draw(im)
    P = lambda x, y: ((x - x0) * scale, (y1 - y) * scale)
    for l in m.lines:
        a, b = P(*m.verts[l[0]]), P(*m.verts[l[1]])
        col = (110, 110, 110) if l[6] != -1 else (230, 230, 230)
        if l[3] in EXIT:
            col = (255, 0, 0)
        elif l[3] in KEYDOOR:
            col = (255, 140, 0)
        elif l[3]:
            col = (220, 200, 0)
        sec = [m.sides[s][5] for s in (l[5], l[6]) if s != -1]
        if any(m.sectors[s][5] == 9 for s in sec):
            col = (90, 140, 255)
        d.line([a, b], fill=col)
    kc = {"monster": (255, 60, 60), "weapon": (0, 255, 255), "ammo": (0, 160, 160), "health": (0, 220, 0),
          "armor": (0, 220, 0), "power": (255, 0, 255), "player": (255, 255, 255), "other": (120, 80, 40)}
    for x, y, a, t, f in m.things_on(skill, mp):
        name, kind = T.get(t, ("", "deco"))
        if kind == "deco":
            continue
        col = KEYCOL.get(t, kc.get(kind))
        px, py = P(x, y)
        d.rectangle([px - 2, py - 2, px + 2, py + 2], fill=col)
    # grid labels every 512 units
    for gx in range(int(x0 // 512 * 512), int(x1), 512):
        d.text(P(gx, y1 - 8), str(gx), fill=(90, 90, 90))
    for gy in range(int(y0 // 512 * 512), int(y1), 512):
        d.text(P(x0 + 2, gy), str(gy), fill=(90, 90, 90))
    im.save(out)
    print(out, im.size)


def main():
    a = sys.argv[1:]
    def opt(k, n=1, default=None):
        if k in a:
            i = a.index(k); v = a[i + 1:i + 1 + n]; del a[i:i + 1 + n]
            return v if n > 1 else v[0]
        return default
    path = opt("--wad"); skill = int(opt("--skill", default=3)); grep = opt("--grep")
    out = opt("--png"); scale = float(opt("--scale", default=0.25)); at = opt("--at", 2); tp = opt("--tp", 3)
    mp = "--mp" in a
    a = [x for x in a if x != "--mp"]
    data = wad(path)
    if not a or a[0] == "list":
        for n, o, s in lumps(data):
            if re.fullmatch(r"E\dM\d", n):
                m = Map(data, n)
                mons = [t for t in m.things_on(3) if T.get(t[3], ("", ""))[1] == "monster"]
                print("%s things %4d monsters(HMP) %3d lines %4d sectors %3d secrets %d" % (
                    n, len(m.things), len(mons), len(m.lines), len(m.sectors), sum(s[5] == 9 for s in m.sectors)))
        return
    m = Map(data, a[0])
    if at:
        x, y = int(at[0]), int(at[1]); print(m.sector_info(m.sector_at(x, y))); return
    if tp:
        x, y, ang = int(tp[0]), int(tp[1]), float(tp[2])
        z = m.sectors[m.sector_at(x, y)][0]
        bam = int(ang / 360.0 * 2 ** 32) & 0xFFFFFFFF
        h = lambda v: struct.pack("<i", v << 16).hex().upper()
        print("TP:%s:%s:%s:%s" % (h(x), h(y), h(z), struct.pack("<I", bam).hex().upper()))
        return
    if out:
        png(m, out, skill, mp, scale); return
    report(m, skill, mp, grep)


if __name__ == "__main__":
    main()
