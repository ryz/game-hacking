"""u2map.py [--list] [--png DIR] [--ascii NAME]: read the 64x64 maps of Ultima II (DOS) from rom/ultima-2.zip.

Map files are MAPX<period><map> (Earth: periods 0 Pangea, 1 B.C. 1423, 2 A.D. 1990, 3 Aftermath 2112,
4 Legends; map 0 surface, 1 village, 2 town, 3 castle, 4 tower, 5 dungeon) and MAPG<planet><map> (planet
maps, read while the player is on a planet). 4096 bytes, row-major (y*64 + x); tile id = byte / 4
(names from ULTIMAII.EXE's "IN THE WATER ... ON COBBLE" list and observation). The time-door table is
CS:0x2798 in ULTIMAII.EXE: per period 4 slots of (x, y).
--list: per surface map the squares of villages, towns, towers, castles, dungeons, signs and the doors.
--png DIR: one PNG per map (4 px per tile). --ascii NAME: one map as characters.
"""
import io, os, sys, zipfile
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", ".."))
TILES = ["water", "marsh", "grass", "woods", "mountains", "village", "town", "tower", "castle", "dungeon",
         "sign", "horse", "frigate", "plane", "rocket", "armour", "hole", "cobble"]
CH = "~,.T^vtTCDs" + "hfpra" + "o_"
PERIODS = {0: "Pangea", 1: "B.C. 1423", 2: "A.D. 1990", 3: "Aftermath 2112", 4: "Legends"}


def zfiles():
    z = zipfile.ZipFile(os.path.join(ROOT, "rom", "ultima-2.zip"))
    return {n.split("/")[-1].upper(): z.read(n) for n in z.namelist() if not n.endswith("/")}


def doors():
    exe = zfiles()["ULTIMAII.EXE"][0x200:]
    t = exe[0x2798:0x2798 + 40]
    return {p: [(t[p * 8 + 2 * k], t[p * 8 + 2 * k + 1]) for k in range(4)] for p in range(5)}


def tile(b):
    i = b // 4
    return TILES[i] if i < len(TILES) else "t%02x" % b


def main():
    a = sys.argv[1:]
    F = zfiles()
    if "--list" in a:
        D = doors()
        for name in sorted(F):
            if not name.startswith(("MAPX", "MAPG")) or name[-1] != "0":
                continue
            m = F[name]
            out = {}
            for y in range(64):
                for x in range(64):
                    t = m[y * 64 + x] // 4
                    if 5 <= t <= 10 or t > 10:
                        out.setdefault(tile(m[y * 64 + x]), []).append("(%02X,%02X)" % (x, y))
            per = int(name[4])
            print(name, PERIODS.get(per, "") if name[3] == "X" else "planet %d" % per)
            for k, v in out.items():
                print("   %-9s %s" % (k, " ".join(v)))
            if name[3] == "X":
                print("   doors     " + " ".join("slot%d(%02X,%02X)=%s" % (k, x, y, tile(m[y * 64 + x]))
                                               for k, (x, y) in enumerate(D[per])))
    if "--ascii" in a:
        m = F[a[a.index("--ascii") + 1]]
        for y in range(64):
            print("%02X " % y + "".join(CH[m[y * 64 + x] // 4] if m[y * 64 + x] // 4 < len(CH) else "?" for x in range(64)))
    if "--png" in a:
        from PIL import Image
        COL = [(40, 40, 170), (120, 60, 140), (70, 160, 70), (20, 100, 20), (150, 150, 150), (255, 220, 0),
               (255, 160, 0), (255, 0, 255), (255, 255, 255), (255, 40, 40), (0, 255, 255)]
        d = a[a.index("--png") + 1]
        os.makedirs(d, exist_ok=True)
        for name in sorted(F):
            if not name.startswith(("MAPX", "MAPG")):
                continue
            m = F[name]
            im = Image.new("RGB", (256, 256))
            for y in range(64):
                for x in range(64):
                    t = m[y * 64 + x] // 4
                    c = COL[t] if t < len(COL) else (((m[y * 64 + x] * 37) % 255), 90, 200)
                    for dy in range(4):
                        for dx in range(4):
                            im.putpixel((x * 4 + dx, y * 4 + dy), c)
            im.save(os.path.join(d, name + ".png"))


if __name__ == "__main__":
    main()
