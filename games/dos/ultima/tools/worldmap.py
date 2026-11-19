"""worldmap.py [--png OUT] [--list]: read MAP.BIN (168x156 tiles, 4 bits each, high nibble first) from rom/ultima.zip.

Tiles: 0 water, 1 grass, 2 woods, 3 mountains, 4 castle, 5 landmark (pillar, tower, sign post, grave), 6 town,
7 dungeon entrance. Continent = 2*(y > 77) + (x > 83) (OUT.EXE 0xB956): 0 Lands of Lord British (NW),
1 Lands of the Feudal Lords (NE), 2 Lands of the Dark Unknown (SW), 3 Lands of Danger and Despair (SE).
Location names and coordinates come from OUT.EXE's own tables (ids 1-84: towns 1-32, castles 33-40, landmarks
41-48, dungeons 49-84; x table at data offset 0x18C8, y at 0x191C, name pointers at 0x307E).
--list prints every location (id, type, continent, x, y in hex, name); --png OUT draws the map (4 px per tile).
"""
import io, os, sys, zipfile
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", ".."))
W, H = 168, 156
KIND = {4: "castle", 5: "landmark", 6: "town", 7: "dungeon"}
COL = {0: (40, 40, 160), 1: (60, 150, 60), 2: (20, 90, 20), 3: (140, 140, 140), 4: (255, 255, 255),
       5: (255, 0, 255), 6: (255, 200, 0), 7: (255, 40, 40)}

def _zip(suffix):
    z = zipfile.ZipFile(os.path.join(ROOT, "rom", "ultima.zip"))
    return z.read([n for n in z.namelist() if n.upper().endswith(suffix)][0])

def names():
    """[(id, x, y, name)] for the 84 locations, from OUT.EXE (data segment at file 0x200 + 0xD480)."""
    import struct
    d = _zip("/OUT.EXE")[0x200:]
    D = 0xD480
    out = []
    for i in range(84):
        p = struct.unpack("<H", d[D + 0x307E + 2 * i:D + 0x3080 + 2 * i])[0]
        out.append((i + 1, d[D + 0x18C8 + i], d[D + 0x191C + i], d[D + p:D + p + 40].split(b"\0")[0].decode()))
    return out

def load():
    d = _zip("/MAP.BIN")
    return [[(d[y * 84 + x // 2] >> 4) if x % 2 == 0 else (d[y * 84 + x // 2] & 15) for x in range(W)] for y in range(H)]

def continent(x, y):
    return 2 * (y > 77) + (x > 83)

def locations(m):
    return [(KIND[m[y][x]], continent(x, y), x, y) for y in range(H) for x in range(W) if m[y][x] in KIND]

if __name__ == "__main__":
    m = load()
    if "--list" in sys.argv:
        for i, x, y, n in names():
            print("%2d %-8s %d %02X %02X %s" % (i, KIND.get(m[y][x], m[y][x]), continent(x, y), x, y, n))
    if "--png" in sys.argv:
        from PIL import Image
        im = Image.new("RGB", (W, H))
        for y in range(H):
            for x in range(W):
                im.putpixel((x, y), COL[m[y][x]])
        im.resize((W * 4, H * 4), Image.NEAREST).save(sys.argv[sys.argv.index("--png") + 1])
