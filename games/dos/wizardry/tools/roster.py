"""roster.py: list the character roster stored on Wizardry I's scenario disk (SAVE1.DSK).

  python3 games/dos/wizardry/tools/roster.py FILE              a SAVE1.DSK image, a .sav (DOSBox Pure save ZIP) or the game ZIP
  python3 games/dos/wizardry/tools/roster.py --route "@start"   play the route (emu.py tokens) and read the disk
  python3 games/dos/wizardry/tools/roster.py ... --raw          also print every record's words after the name

Layout (verified 2026-11-19, playbook "RAM map" and "Saves"): the roster is 20 records of 208 (0xD0) bytes in
five 1024-byte pages of four records each, from disk offset 0x1D800 (sector 236 of the 320 KB image; slot n at
0x1D800 + (n // 4) * 0x400 + (n % 4) * 0xD0). A record is the Pascal TCHAR of the Apple original: name and
password (length byte + 15 characters), then 16-bit little-endian words. The same records sit in memory while
the game runs (party copies at 0DCEC + member * 0xD0).
Without SAVE1.DSK changes the stock disk holds six pre-made characters (TARKIN SHREEV CURTIS KIMBAL TIVIS MEWO) and
six "LOST" developer names that are free slots.
"""
import io, os, sys, zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", "..", ".."))
ROSTER = 0x1D800
RACES = ["-", "HUMAN", "ELF", "DWARF", "GNOME", "HOBBIT"]
CLASSES = ["FIG", "MAG", "PRI", "THI", "BIS", "SAM", "LOR", "NIN"]
STATUS = ["OK", "AFRAID", "ASLEEP", "PLYZE", "STONED", "DEAD", "ASHES", "LOST"]
ALIGN = ["-", "G", "N", "E"]


def slot_offset(n):
    return ROSTER + (n // 4) * 0x400 + (n % 4) * 0xD0


def w(r, off):
    return int.from_bytes(r[off:off + 2], "little")


def long3(r, off):
    """TWIZLONG: three words, each 0..9999, low first."""
    return w(r, off) + 10000 * w(r, off + 2) + 100000000 * w(r, off + 4)


def attribs(r):
    a, b = w(r, 0x2C), w(r, 0x2E)
    return [(a >> s) & 31 for s in (0, 5, 10)] + [(b >> s) & 31 for s in (0, 5, 10)]


def decode(r):
    n = r[0]
    if not 0 < n < 16:
        return None
    return {
        "name": r[1:1 + n].decode("latin1"), "out": w(r, 0x20), "race": RACES[w(r, 0x22) % 6],
        "class": CLASSES[w(r, 0x24) % 8], "age_weeks": w(r, 0x26), "status": STATUS[w(r, 0x28) % 8],
        "align": ALIGN[w(r, 0x2A) % 4], "stats": attribs(r), "gold": long3(r, 0x34), "items": w(r, 0x3A),
        "exp": long3(r, 0x7C), "maxlev": w(r, 0x82), "level": w(r, 0x84), "hp": w(r, 0x86), "hpmax": w(r, 0x88),
        "mage_sp": [w(r, 0x92 + 2 * i) for i in range(7)], "priest_sp": [w(r, 0xA0 + 2 * i) for i in range(7)],
        "ac": w(r, 0xB0) - (65536 if w(r, 0xB0) > 32767 else 0),
    }


def disk_from(path):
    data = open(path, "rb").read()
    if data[:2] == b"PK":
        z = zipfile.ZipFile(io.BytesIO(data))
        names = [n for n in z.namelist() if n.upper().endswith("SAVE1.DSK")]
        if not names:
            raise SystemExit("%s: no SAVE1.DSK inside (files: %s)" % (path, z.namelist()))
        return z.read(names[0])
    return data


def disk_from_route(route):
    sys.path.insert(0, os.path.join(ROOT, "tools"))
    import emu as E
    g = E.Game("dos/wizardry")
    m, rest, _ = E.start(g, route)
    E.play(m, g, rest)
    zipbytes = m.battery(0)
    m.close()
    if not zipbytes:
        return None
    z = zipfile.ZipFile(io.BytesIO(zipbytes))
    names = [n for n in z.namelist() if n.upper().endswith("SAVE1.DSK")]
    return z.read(names[0]) if names else None


def show(disk, raw=False):
    for n in range(20):
        o = slot_offset(n)
        r = disk[o:o + 0xD0]
        c = decode(r)
        if not c:
            continue
        print("%2d %05X %-15s %s-%s %-6s L%-3d HP %3d/%-3d AC %3d %-6s gold %-9d exp %-9d st %s age %dw out %d items %d"
              % (n, o, c["name"], c["align"], c["class"], c["race"], c["level"], c["hp"], c["hpmax"], c["ac"],
                 c["status"], c["gold"], c["exp"], "/".join(map(str, c["stats"])), c["age_weeks"], c["out"],
                 c["items"]))
        if raw:
            print("   ", " ".join(str(w(r, i)) for i in range(0x20, 0xD0, 2)))


def main():
    a = sys.argv[1:]
    raw = "--raw" in a
    a = [x for x in a if x != "--raw"]
    if a and a[0] == "--route":
        disk = disk_from_route(a[1])
        if disk is None:
            print("nothing written to disk on this route: the stock SAVE1.DSK is in use")
            disk = disk_from(os.path.join(ROOT, "rom", "wizardry.zip"))
    else:
        disk = disk_from(a[0])
    show(disk, raw)


if __name__ == "__main__":
    main()
