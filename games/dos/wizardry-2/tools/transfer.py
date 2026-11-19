"""transfer.py: build the Wizardry II transfer save from a Wizardry I save (the run.bat "transfer" step, reproducibly).

  python3 games/dos/wizardry-2/tools/transfer.py [SRC] [OUT]
      SRC  a Wizardry I save ZIP (.sav) holding WIZAR1/SAVE1.DSK, or a SAVE1.DSK image
           default: games/dos/wizardry/saves/03_werdna_beaten.sav (the six after the real Werdna fight and the ending)
      OUT  default: games/dos/wizardry-2/saves/00_transfer.sav

The game's own run.bat (menu 2) copies ..\\wizar1\\save1.dsk to ..\\wizar2\\save1.dsk; the loader WIZ2.COM opens
`Save1.Dsk` in its folder only while the game shows the M)ove characters "source scenario disk" prompt (playbook,
"The loader"). This script writes the same file into a DOSBox Pure save ZIP (folder `WIZAR2/`, stored, dated
1990-01-01 like the backend's own saves), so `sav:00_transfer` powers on with the Wizardry I disk next to WIZ2.COM.
SAVE1.DSK is copied byte for byte; nothing in it is changed.
"""
import io, os, sys, zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", "..", ".."))
SRC = os.path.join(ROOT, "games", "dos", "wizardry", "saves", "03_werdna_beaten.sav")
OUT = os.path.join(ROOT, "games", "dos", "wizardry-2", "saves", "00_transfer.sav")
DATE = (1990, 1, 1, 0, 0, 0)


def source_disk(path):
    data = open(path, "rb").read()
    if data[:2] == b"PK":
        z = zipfile.ZipFile(io.BytesIO(data))
        names = [n for n in z.namelist() if n.upper().endswith("WIZAR1/SAVE1.DSK") or n.upper() == "SAVE1.DSK"]
        if not names:
            raise SystemExit("%s: no WIZAR1/SAVE1.DSK inside (files: %s)" % (path, z.namelist()))
        data = z.read(names[0])
    if len(data) not in (327680, 655360):
        raise SystemExit("%s: %d bytes, not a Wizardry I scenario disk image" % (path, len(data)))
    return data


def build(disk):
    b = io.BytesIO()
    with zipfile.ZipFile(b, "w", zipfile.ZIP_STORED) as z:
        d = zipfile.ZipInfo("WIZAR2/", DATE)
        d.external_attr = 16                     # directory, as in the backend's save ZIPs
        z.writestr(d, b"")
        z.writestr(zipfile.ZipInfo("WIZAR2/SAVE1.DSK", DATE), disk)
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
    import hashlib
    print("wrote %s (%d bytes, SHA-1 %s)" % (os.path.relpath(out, ROOT), len(data), hashlib.sha1(data).hexdigest()[:12]))


if __name__ == "__main__":
    main()
