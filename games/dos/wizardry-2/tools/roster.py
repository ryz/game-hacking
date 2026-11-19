"""roster.py: list the character rosters on Wizardry II's disks (SAVE2.DSK, and the Wizardry I SAVE1.DSK next to it).

  python3 games/dos/wizardry-2/tools/roster.py FILE         a .sav (DOSBox Pure save ZIP), a SAVE2.DSK image or the game ZIP
  python3 games/dos/wizardry-2/tools/roster.py FILE --raw   also the record's words after the name

Layout (verified 2026-11-19, playbook "RAM map" and "Saves"): the same 208-byte (0xD0) character record as Wizardry I
(decoded by `games/dos/wizardry/tools/roster.py`), 20 slots, four per 1024-byte page; in SAVE2.DSK the roster starts
at 0x1D200 (slot n at 0x1D200 + (n // 4) * 0x400 + (n % 4) * 0xD0), in a Wizardry I SAVE1.DSK at 0x1D800.
Awards word +0xCE: bit 0 Chevron of Rank ">" (Wizardry I), bit 11 Knight of the City "K", bit 14 Mark of Gnilda
"G" (Wizardry II ending). Status LOST = free slot (a character moved away is left as LOST on the source disk).
"""
import io, os, sys, zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "games", "dos", "wizardry", "tools"))
import roster as W1  # noqa: E402  (record decoder shared with Wizardry I)

BASES = {"SAVE2.DSK": 0x1D200, "SAVE1.DSK": 0x1D800}
AWARDS = [(0, ">"), (11, "K"), (14, "G")]


def disks(path):
    data = open(path, "rb").read()
    if data[:2] != b"PK":
        name = os.path.basename(path).upper()
        return {name if name in BASES else "SAVE2.DSK": data}
    z = zipfile.ZipFile(io.BytesIO(data))
    out = {}
    for n in z.namelist():
        base = n.split("/")[-1].upper()
        if base in BASES and not n.upper().startswith("WIZAR1/"):
            out[base] = z.read(n)
    return out


def main():
    a = sys.argv[1:]
    raw = "--raw" in a
    a = [x for x in a if x != "--raw"]
    if not a:
        raise SystemExit(__doc__)
    for name, d in sorted(disks(a[0]).items(), reverse=True):
        base = BASES[name]
        print("%s (roster at %X)" % (name, base))
        for n in range(20):
            off = base + (n // 4) * 0x400 + (n % 4) * 0xD0
            rec = d[off:off + 0xD0]
            r = W1.decode(rec)
            if not r:
                continue
            aw = int.from_bytes(rec[0xCE:0xD0], "little")
            marks = "".join(c for b, c in AWARDS if aw >> b & 1)
            print("%2d %5X %-15s %s-%s %-6s L%-3d HP %3d/%-3d AC %3d %-6s gold %-9d exp %-9d items %d out %d %s" % (
                n, off, r["name"], r["align"], r["class"], r["race"], r["level"], r["hp"], r["hpmax"], r["ac"],
                r["status"], r["gold"], r["exp"], r["items"], r["out"], marks))
            if raw:
                print("      " + " ".join("%04x" % int.from_bytes(rec[i:i + 2], "little") for i in range(0x20, 0xD0, 2)))


if __name__ == "__main__":
    main()
