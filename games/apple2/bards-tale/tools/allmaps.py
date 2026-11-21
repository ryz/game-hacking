"""Load every dungeon level of The Bard's Tale (Apple II) with the level warp (checkpoint stairs_hero + macro LV,
playbook "Level warp") and write design/maps/<nn>_<name>.txt (text map, as tools/maps.py) and .png (rendered).
Usage: python3 games/apple2/bards-tale/tools/allmaps.py [ID ...]   (ids hex 00-0F; default all)
Legend: walls white, doors orange (D), secret doors (3) red dashed; U/D stairs up/down, ! special event,
F forced fight (once), T trap (once), k darkness (puts out light), ^ portal up, v portal down (see design/maps/README.md)."""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import emu as E
from PIL import Image, ImageDraw
OUT = os.path.join(HERE, "..", "design", "maps")
# level id -> (index in its dungeon, file name, dungeon name)
LEVELS = {0: (0, "cellar", "Wine cellar"), 1: (1, "sewers1", "Sewers level 1"), 2: (2, "sewers2", "Sewers level 2"),
          3: (3, "sewers3", "Sewers level 3"), 4: (0, "catacombs1", "Catacombs level 1"),
          5: (1, "catacombs2", "Catacombs level 2"), 6: (2, "catacombs3", "Catacombs level 3"),
          7: (0, "castle1", "Harkyn's Castle level 1"), 8: (1, "castle2", "Harkyn's Castle level 2"),
          9: (2, "castle3", "Harkyn's Castle level 3"), 10: (0, "kylearan", "Kylearan's Amber Tower"),
          11: (0, "mangar1", "Mangar's Tower level 1"), 12: (1, "mangar2", "Mangar's Tower level 2"),
          13: (2, "mangar3", "Mangar's Tower level 3"), 14: (3, "mangar4", "Mangar's Tower level 4"),
          15: (4, "mangar5", "Mangar's Tower level 5")}
FL = [(0x01, "U"), (0x02, "D"), (0x04, "!"), (0x80, "F"), (0x10, "T"), (0x08, "k"), (0x40, "^"), (0x20, "v")]
H = {0: "   ", 1: "---", 2: "-D-", 3: "-S-"}
V = {0: " ", 1: "|", 2: "D", 3: "S"}

def text(w, f, title):
    out = [title, "North is up; x = east (columns), y = north (rows). " +
           "U/D stairs up/down, ! special (message/event), F forced fight (once), T trap (once), k darkness, ^ portal up, v portal down"]
    for y in range(21, -1, -1):
        top = "+"; mid = ""
        for x in range(22):
            b = w[y * 22 + x]
            top += H[b & 3] + "+"
            c = "".join(s for k, s in FL if f[y * 22 + x] & k)[:3]
            mid += V[(b >> 6) & 3] + c.center(3)[:3]
        mid += V[(w[y * 22 + 21] >> 4) & 3]
        out += ["   " + top, "%2d %s" % (y, mid)]
    out.append("   +" + "+".join(H[(w[x] >> 2) & 3] for x in range(22)) + "+")
    out.append("    " + "".join("%-4d" % x for x in range(22)))
    return "\n".join(out) + "\n"

def png(w, f, path, title):
    C, M = 24, 24
    im = Image.new("RGB", (22 * C + 2 * M, 22 * C + 2 * M + 16), (16, 16, 24))
    d = ImageDraw.Draw(im)
    d.text((M, 4), title, fill=(255, 255, 255))
    col = {1: (230, 230, 230), 2: (255, 150, 40), 3: (220, 40, 40)}
    def X(x): return M + x * C
    def Y(y): return M + 16 + (21 - y) * C
    for y in range(22):
        for x in range(22):
            fl = f[y * 22 + x]
            if fl & 0x08: d.rectangle([X(x) + 1, Y(y) + 1, X(x) + C - 1, Y(y) + C - 1], fill=(48, 48, 64))
            if fl & 0x80: d.rectangle([X(x) + 1, Y(y) + 1, X(x) + C - 1, Y(y) + C - 1], fill=(90, 20, 20))
            if fl & 0x10: d.rectangle([X(x) + 1, Y(y) + 1, X(x) + C - 1, Y(y) + C - 1], outline=(220, 200, 40))
            s = "".join(t for k, t in FL if fl & k and t not in "k")[:3]
            if s: d.text((X(x) + 4, Y(y) + 6), s, fill=(120, 255, 120))
            b = w[y * 22 + x]
            sides = [(b & 3, (X(x), Y(y), X(x) + C, Y(y))),               # north
                     ((b >> 2) & 3, (X(x), Y(y) + C, X(x) + C, Y(y) + C)),  # south
                     ((b >> 4) & 3, (X(x) + C, Y(y), X(x) + C, Y(y) + C)),  # east
                     ((b >> 6) & 3, (X(x), Y(y), X(x), Y(y) + C))]          # west
            for v, ln in sides:
                if v: d.line(ln, fill=col[v], width=3 if v == 1 else 4)
    for i in range(0, 22, 2):
        d.text((X(i) + 6, Y(-1) + 4), str(i), fill=(150, 150, 150))
        d.text((4, Y(i) + 6), str(i), fill=(150, 150, 150))
    im.save(path)

def main():
    game = E.Game("apple2/bards-tale")
    ids = [int(a, 16) for a in sys.argv[1:]] or sorted(LEVELS)
    os.makedirs(OUT, exist_ok=True)
    for lid in ids:
        idx, fname, title = LEVELS[lid]
        route = "@stairs_hero,KEEPFLAGS,LV:%02X:%d:%02X" % ((idx - 1) & 0xFF, idx, lid)
        emu, rest, _ = E.start(game, route)
        E.play(emu, game, E.expand(game, rest) if rest else [])
        w = emu.peek(0x2F800, 484); f = emu.peek(0x2FA00, 484)
        name = bytes(b & 0x7F for b in emu.peek(0x2FC16, 10)).decode("ascii", "replace").rstrip(" \\")
        lv = emu.peek(0x2FC10, 1)[0]
        t = "%s (level id %02X, in-game name \"%s\", monster level %d)" % (title, lid, name.strip(), lv)
        base = os.path.join(OUT, "%02d_%s" % (lid, fname))
        open(base + ".txt", "w").write(t + "\n" + "route: " + route + "\n" + text(w, f, "")[1:])
        png(w, f, base + ".png", t)
        print(base, t, flush=True)

if __name__ == "__main__":
    main()
