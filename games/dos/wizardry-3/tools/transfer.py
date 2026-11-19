"""transfer.py: build the Wizardry III transfer save from a Wizardry II save (the run.bat "transfer" step, reproducibly).

  python3 games/dos/wizardry-3/tools/transfer.py [SRC] [OUT]
      SRC  a Wizardry II save ZIP (.sav) holding WIZAR2/SAVE2.DSK, or a SAVE2.DSK image
           default: games/dos/wizardry-2/saves/03_wizardry3_transfer.sav (the six after the Wizardry II ending,
           RYZ with the Mark of Gnilda, the others Knights of the City, with gear, in the Castle)
      OUT  default: games/dos/wizardry-3/saves/00_transfer.sav

The game's own run.bat (menu 2) copies ..\\wizar1\\save1.dsk and ..\\wizar2\\save2.dsk into ..\\wizar3\\. The
loader WIZ3.COM, however, knows only one source file: on the M)ove characters "source scenario disk" prompt it
opens `Save2.Dsk` in its folder (the string in WIZ3.COM; WIZ2.COM opens `Save1.Dsk` at the same place), so a
Wizardry I disk is never read by this loader (playbook, "The loader"). This script writes `WIZAR3/SAVE2.DSK`
into a DOSBox Pure save ZIP (stored, dated 1990-01-01 like the backend's own saves), so `sav:00_transfer` powers
on with the Wizardry II disk next to WIZ3.COM. SAVE2.DSK is copied byte for byte; nothing in it is changed.
"""
import hashlib, io, os, sys, zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", "..", ".."))
SRC = os.path.join(ROOT, "games", "dos", "wizardry-2", "saves", "03_wizardry3_transfer.sav")
OUT = os.path.join(ROOT, "games", "dos", "wizardry-3", "saves", "00_transfer.sav")
DATE = (1990, 1, 1, 0, 0, 0)


def source_disk(path):
    data = open(path, "rb").read()
    if data[:2] == b"PK":
        z = zipfile.ZipFile(io.BytesIO(data))
        names = [n for n in z.namelist() if n.upper().endswith("WIZAR2/SAVE2.DSK") or n.upper() == "SAVE2.DSK"]
        if not names:
            raise SystemExit("%s: no WIZAR2/SAVE2.DSK inside (files: %s)" % (path, z.namelist()))
        data = z.read(names[0])
    if len(data) not in (327680, 655360):
        raise SystemExit("%s: %d bytes, not a Wizardry II scenario disk image" % (path, len(data)))
    return data


def build(disk):
    b = io.BytesIO()
    with zipfile.ZipFile(b, "w", zipfile.ZIP_STORED) as z:
        d = zipfile.ZipInfo("WIZAR3/", DATE)
        d.external_attr = 16                     # directory, as in the backend's save ZIPs
        z.writestr(d, b"")
        z.writestr(zipfile.ZipInfo("WIZAR3/SAVE2.DSK", DATE), disk)
    return b.getvalue()


def main():
    a = sys.argv[1:]
    src = a[0] if a else SRC
    out = a[1] if len(a) > 1 else OUT
    data = build(source_disk(src))
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    if os.path.exists(out) and open(out, "rb").read() == data:
        print("unchanged:", os.path.relpath(out, ROOT))
        return
    open(out, "wb").write(data)
    print("wrote %s (%d bytes, SHA-1 %s)" % (os.path.relpath(out, ROOT), len(data), hashlib.sha1(data).hexdigest()[:12]))


if __name__ == "__main__":
    main()
