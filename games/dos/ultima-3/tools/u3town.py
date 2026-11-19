"""u3town.py FILE.ULT [FILE ...]: the people of a towne or castle map (Ultima III DOS) with their talk lines.

  python3 games/dos/ultima-3/tools/u3town.py LCB.ULT BRITISH.ULT

Reads the map file from rom/ultima-3.zip. A towne file is the 64x64 map (4096 bytes), then the talk table (8
offsets, then zero-terminated lines, \\n = new line), a sprite block, and five 32-byte object lists at 4096+0x180:
picture (map byte), terrain under it, x, y, talk byte (0x80 merchant, low nibble = talk line number, 0x40 set =
it wanders). Prints: slot, picture, x, y, talk byte, line.
"""
import sys, zipfile, os
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", ".."))
PIC = {0x40: "merchant", 0x44: "jester", 0x48: "guard", 0x4C: "Lord British", 0x50: "fighter", 0x54: "cleric",
       0x58: "wizard", 0x5C: "thief", 0x60: "orc", 0x64: "skeleton", 0x68: "giant", 0x6C: "daemon",
       0x70: "pincher", 0x74: "dragon", 0x78: "balron", 0x28: "horse", 0x2C: "frigate", 0x34: "serpent"}

def load(name):
    z = zipfile.ZipFile(os.path.join(ROOT, "rom", "ultima-3.zip"))
    for n in z.namelist():
        if n.upper().endswith("/" + name.upper()) or n.upper() == name.upper():
            return z.read(n)
    raise SystemExit("no " + name)

def lines(d):
    t = d[4096:]
    offs = [t[2 * i] | t[2 * i + 1] << 8 for i in range(8)]
    out = []
    for o in offs:
        if o >= len(t) or 0 not in t[o:]: out.append(""); continue
        e = t.index(0, o)
        out.append(t[o:e].decode("latin-1").strip("\n").replace("\n", " / "))
    return out

def objects(d):
    b = 4096 + 0x180
    res = []
    for k in range(32):
        pic, under, x, y, talk = (d[b + 32 * j + k] for j in range(5))
        if pic: res.append((k, pic, under, x, y, talk))
    return res

if __name__ == "__main__":
    for f in sys.argv[1:]:
        d = load(f); L = lines(d)
        print("==", f)
        for k, pic, under, x, y, talk in objects(d):
            n = talk & 0x0F
            line = L[n - 1] if 1 <= n <= 8 and not talk & 0x80 else ""
            print("%2d %-12s (%02X,%02X) talk %02X  %s" % (k, PIC.get(pic, "%02X" % pic), x, y, talk, line))
