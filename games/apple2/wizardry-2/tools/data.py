"""data.py [items|monsters|roster|toc] [FILE] [--raw]: tables on the Wizardry II (Apple II) scenario disk (also reads a Wizardry I disk).

  python3 games/apple2/wizardry-2/tools/data.py items             the 130 item records of the game ZIP's scenario disk
  python3 games/apple2/wizardry-2/tools/data.py monsters          the 78 monster records
  python3 games/apple2/wizardry-2/tools/data.py roster FILE       the 20 character slots of FILE: a .dsk (DOS 3.3
                                                                sector order), a .sav ZIP that holds one, or the game ZIP

SCENARIO.DATA is a Pascal file from block 148 of the scenario disk (found through the directory) (blocks of 512 bytes; maps.blocks() turns
the sector image into block order). Its first block is a table of contents: the game name, then four arrays of
eight words for the record kinds ZERO, MAZE, ENEMY, REWARD, OBJECT, CHAR, SPCCHRS, EXP: records per two
blocks, records on the disk, an unused array, block offset inside the file. Records never cross a 1024-byte
pair of blocks. On this disk: MAZE 1 per pair from block +6 (6 floors), ENEMY 6 per pair from +18 (78,
158 bytes), REWARD from +44, OBJECT 13 per pair from +52 (130, 78 bytes), CHAR 4 per pair from +72 (20, 208
bytes), EXP at +112. Character record layout: playbook, RAM map (the DOS port's is the same).
"""
import os, struct, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import maps

KINDS = ["ZERO", "MAZE", "ENEMY", "REWARD", "OBJECT", "CHAR", "SPCCHRS", "EXP"]
RACES = ["-", "HUMAN", "ELF", "DWARF", "GNOME", "HOBBIT"]
CLASSES = ["FIG", "MAG", "PRI", "THI", "BIS", "SAM", "LOR", "NIN"]
STATUS = ["OK", "AFRAID", "ASLEEP", "PLYZE", "STONED", "DEAD", "ASHES", "LOST"]
ALIGN = ["-", "G", "N", "E"]
OBJTYPE = ["weapon", "armor", "shield", "helmet", "gauntlet", "special", "misc"]


def toc(d):
    FILE0 = maps.file_block(d) * 512
    w = struct.unpack("<32H", d[FILE0 + 42:FILE0 + 42 + 64])
    return {k: dict(per2b=w[i], count=w[8 + i], block=w[24 + i]) for i, k in enumerate(KINDS)}


def records(d, kind, size):
    t = toc(d)[kind]; FILE0 = maps.file_block(d) * 512
    for n in range(t["count"]):
        o = FILE0 + t["block"] * 512 + (n // t["per2b"]) * 1024 + (n % t["per2b"]) * size
        yield n, o, d[o:o + size]


def pstr(r, o):
    return r[o + 1:o + 1 + min(r[o], 15)].decode("latin1")


def w(r, o):
    return int.from_bytes(r[o:o + 2], "little")


def long3(r, o):
    return w(r, o) + 10000 * w(r, o + 2) + 100000000 * w(r, o + 4)


def main():
    a = sys.argv[1:]; raw = "--raw" in a
    if raw: a.remove("--raw")
    what = a[0] if a else "items"
    d = maps.disk(a[1] if len(a) > 1 else None)
    if what == "toc":
        for k, v in toc(d).items(): print(k, v)
    elif what == "items":
        for n, o, r in records(d, "OBJECT", 78):
            print("%3d %-15s (%-15s) %-8s price %-7d%s" % (n, pstr(r, 0), pstr(r, 16), OBJTYPE[w(r, 32)] if w(r, 32) < 7 else w(r, 32), long3(r, 44),
                  "  " + " ".join("%d" % x for x in struct.unpack("<23H", r[32:78])) if raw else ""))
    elif what == "monsters":
        for n, o, r in records(d, "ENEMY", 158):
            print("%3d %-15s (%-15s) %s" % (n, pstr(r, 32), pstr(r, 0), " ".join("%d" % x for x in struct.unpack("<47H", r[64:158])) if raw else
                  "pic %d group %dd%d+%d  HP %dd%d+%d  class %d  AC %d" % (w(r, 64), w(r, 66), w(r, 68), w(r, 70), w(r, 72), w(r, 74), w(r, 76), w(r, 78), struct.unpack("<h", r[80:82])[0])))
    elif what == "roster":
        for n, o, r in records(d, "CHAR", 208):
            st = w(r, 0x28)
            if st == 7 or not r[0] or r[0] > 15: print("%2d  (free)" % n); continue
            a1, a2 = w(r, 0x2C), w(r, 0x2E)
            stats = [a1 & 31, a1 >> 5 & 31, a1 >> 10 & 31, a2 & 31, a2 >> 5 & 31, a2 >> 10 & 31]
            items = [w(r, 0x3C + 8 * i + 6) for i in range(min(w(r, 0x3A), 8))]
            print("%2d  %-15s %s-%s %-6s L%-3d HP %d/%d AC %d age %d %s gold %d EP %d stats %s items %s%s%s" % (
                n, pstr(r, 0), ALIGN[w(r, 0x2A) & 3], CLASSES[w(r, 0x24) & 7], RACES[w(r, 0x22)] if w(r, 0x22) < 6 else "?", w(r, 0x84),
                w(r, 0x86), w(r, 0x88), struct.unpack("<h", r[0xB0:0xB2])[0], w(r, 0x26) // 52, STATUS[st] if st < 8 else st, long3(r, 0x34),
                long3(r, 0x7C), stats, items, ("  awards " + "".join(c for b, c in ((0, ">"), (11, "K"), (14, "G")) if w(r, 0xCE) >> b & 1)) if w(r, 0xCE) else "", "  OUT" if w(r, 0x20) else ""))
    else:
        print(__doc__)


if __name__ == "__main__":
    main()
