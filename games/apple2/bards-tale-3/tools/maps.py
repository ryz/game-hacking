"""Write a decoded map of every dungeon level of The Bard's Tale III (Apple II) to design/maps/:
LL_<name>.txt (text) and LL_<name>.png (rendered). Each level is loaded like tools/levels.py does it (checkpoint
`cat_stairs`, $0D=1, $1052=LEVEL, take the stairs; side B inserted when the game asks).
Square format (RAM, verified against the automap and the screen): 5 bytes per square, rows from the top
(north) down, row N at $1040 + word[$1062 + 2*(N+1)]; byte 0 high nibble = north side, low nibble = east side,
byte 1 high = south, low = west; side & 3: 1 wall, 2 door, 3 other (secret door or special wall); bit 3 = side
already drawn on the automap. Bytes 2-3 are square flags (meaning only partly known: 01 in byte 2 = stairs up
at the catacombs arrival); byte 4 bit 0 = visited (automap). Events (messages, fights, gates) come from a list
of their own and do not show here.
Usage: python3 games/apple2/bards-tale-3/tools/maps.py [LEVEL_HEX ...]   (default: all 61 levels)"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import emu as E
from PIL import Image, ImageDraw
OUT = os.path.join(HERE, "..", "design", "maps")
ALL = list(range(0x00, 0x3D))
H = {0: "   ", 1: "---", 2: "-D-", 3: "-S-"}
V = {0: " ", 1: "|", 2: "D", 3: "S"}


def decode(emu):
    h = emu.peek(0x1040, 0x30)
    name = bytes(b & 0x7F for b in h[:16]).decode("ascii", "replace").split("\x7f")[0].strip()
    w, hh = h[0x1E], h[0x1F]
    ptr = lambda k: emu.peek(0x1062 + 2 * k, 1)[0] | emu.peek(0x1063 + 2 * k, 1)[0] << 8
    sq = {}
    for n in range(hh):
        row = emu.peek(0x1040 + ptr(n + 1), 5 * w)
        for e in range(w):
            sq[(n, e)] = row[5 * e:5 * e + 5]
    return name, w, hh, sq, h


def side(b, which):
    v = {"N": b[0] >> 4, "E": b[0] & 15, "S": b[1] >> 4, "W": b[1] & 15}[which]
    return v & 3


def text(name, lid, w, hh, sq, where):
    out = ["%s (level %02X, %s, %dx%d)" % (name, lid, where, w, hh),
           "North is up; columns = east, rows = north. Walls | ---, doors D, other S (secret door or special wall);",
           "cell text: flag byte 2 in hex when not zero, + = flag byte 3 set, * = visited (automap bit), nothing else."]
    for n in range(hh - 1, -1, -1):
        top, mid = "+", ""
        for e in range(w):
            b = sq[(n, e)]
            top += H[side(b, "N")] + "+"
            c = ("%02X" % b[2] if b[2] else "") + ("+" if b[3] else "")
            c = c or ("*" if b[4] & 1 else "")
            mid += V[side(b, "W")] + c.center(3)[:3]
        mid += V[side(sq[(n, w - 1)], "E")]
        out += ["   " + top, "%2d %s" % (n, mid)]
    out.append("   +" + "+".join(H[side(sq[(0, e)], "S")] for e in range(w)) + "+")
    out.append("    " + "".join("%-4d" % e for e in range(w)))
    return "\n".join(out) + "\n"


def png(name, lid, w, hh, sq, path, where):
    C, M = 22, 26
    im = Image.new("RGB", (w * C + 2 * M, hh * C + 2 * M + 16), (16, 16, 24))
    d = ImageDraw.Draw(im)
    d.text((M, 4), "%s (level %02X, %s)" % (name, lid, where), fill=(255, 255, 255))
    col = {1: (230, 230, 230), 2: (255, 150, 40), 3: (220, 40, 40)}
    X = lambda e: M + e * C
    Y = lambda n: M + 16 + (hh - 1 - n) * C
    for (n, e), b in sq.items():
        if b[2] or b[3]:
            d.rectangle([X(e) + 2, Y(n) + 2, X(e) + C - 2, Y(n) + C - 2], fill=(60, 40, 90))
        for v, ln in [(side(b, "N"), (X(e), Y(n), X(e) + C, Y(n))), (side(b, "S"), (X(e), Y(n) + C, X(e) + C, Y(n) + C)),
                      (side(b, "E"), (X(e) + C, Y(n), X(e) + C, Y(n) + C)), (side(b, "W"), (X(e), Y(n), X(e), Y(n) + C))]:
            if v:
                d.line(ln, fill=col[v], width=2 if v == 1 else 3)
    for i in range(0, max(w, hh), 2):
        if i < w: d.text((X(i) + 5, Y(-1) + 4), str(i), fill=(150, 150, 150))
        if i < hh: d.text((4, Y(i) + 5), str(i), fill=(150, 150, 150))
    im.save(path)


def main():
    game = E.Game("apple2/bards-tale-3")
    ids = [int(a, 16) for a in sys.argv[1:]] or ALL
    os.makedirs(OUT, exist_ok=True)
    emu, rest, _ = E.start(game, "@cat_stairs")
    E.play(emu, game, rest)
    st = os.path.join(ROOT, "work", "bt3_maps_base.state")
    emu.save_state(st)
    index = []
    for lid in ids:
        emu.load_state(st)
        E.play(emu, game, E.expand(game, ["poke:000D=01", "poke:1052=%02X" % lid, "y", "w1200"]))
        where = "dungeon disk side A"
        if emu.peek(0x03, 1)[0] != lid + 0x27 or (emu.peek(0x1040, 1)[0] == 0xC3 and lid != 0x28):
            where = "dungeon disk side B"
            E.play(emu, game, E.expand(game, ["disk:4", "space", "w1500"]))
        if emu.peek(0x03, 1)[0] != lid + 0x27:
            print("%02X not loaded" % lid, flush=True)
            continue
        name, w, hh, sq, h = decode(emu)
        slug = "".join(c if c.isalnum() else "-" for c in name.lower()).strip("-")
        base = os.path.join(OUT, "%02X_%s" % (lid, slug))
        open(base + ".txt", "w").write(text(name, lid, w, hh, sq, where) +
                                       "route: @cat_stairs,%s:%02X:<index>\n" % ("LV" if "A" in where[-1] else "LVB", lid))
        png(name, lid, w, hh, sq, base + ".png", where)
        index.append("| %02X | %s | %s | %dx%d | [txt](%s) [png](%s) |" % (lid, name, where[-6:], w, hh,
                     os.path.basename(base) + ".txt", os.path.basename(base) + ".png"))
        print(base, name, w, hh, flush=True)
    open(os.path.join(OUT, "index.part.md"), "w").write("\n".join(index) + "\n")


if __name__ == "__main__":
    main()
