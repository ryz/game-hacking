"""worldmap.py [--png OUT] [--list]: read MAP.BIN (168x156 tiles, 4 bits each, high nibble first) from rom/ultima.zip.

Tiles: 0 water, 1 grass, 2 woods, 3 mountains, 4 castle, 5 landmark (pillar, tower, sign post, grave), 6 town,
7 dungeon entrance. Continent = 2*(y > 77) + (x > 83) (OUT.EXE 0xB956): 0 Lands of Lord British (NW),
1 Lands of the Feudal Lords (NE), 2 Lands of the Dark Unknown (SW), 3 Lands of Danger and Despair (SE).
--list prints every location (type, continent, x, y in hex); --png draws the map (2 px per tile).
"""
import io, os, sys, zipfile
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", ".."))
W, H = 168, 156
KIND = {4: "castle", 5: "landmark", 6: "town", 7: "dungeon"}
COL = {0: (40, 40, 160), 1: (60, 150, 60), 2: (20, 90, 20), 3: (140, 140, 140), 4: (255, 255, 255),
       5: (255, 0, 255), 6: (255, 200, 0), 7: (255, 40, 40)}

def load():
    z = zipfile.ZipFile(os.path.join(ROOT, "rom", "ultima.zip"))
    name = [n for n in z.namelist() if n.upper().endswith("/MAP.BIN")][0]
    d = z.read(name)
    return [[(d[y * 84 + x // 2] >> 4) if x % 2 == 0 else (d[y * 84 + x // 2] & 15) for x in range(W)] for y in range(H)]

def continent(x, y):
    return 2 * (y > 77) + (x > 83)

def locations(m):
    return [(KIND[m[y][x]], continent(x, y), x, y) for y in range(H) for x in range(W) if m[y][x] in KIND]

if __name__ == "__main__":
    m = load()
    if "--list" in sys.argv:
        for k, c, x, y in locations(m):
            print("%-8s %d %02X %02X" % (k, c, x, y))
    if "--png" in sys.argv:
        from PIL import Image
        im = Image.new("RGB", (W, H))
        for y in range(H):
            for x in range(W):
                im.putpixel((x, y), COL[m[y][x]])
        im.resize((W * 4, H * 4), Image.NEAREST).save(sys.argv[sys.argv.index("--png") + 1])
