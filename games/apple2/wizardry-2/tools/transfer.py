"""transfer.py [SAVE] [OUT]: make the character-transfer disk for Wizardry III (Apple II) from an exported save.

  python3 games/apple2/wizardry-2/tools/transfer.py
      rom/saves/apple2/wizardry-2/02_ending.sav -> rom/saves/apple2/wizardry-3/00_transfer.sav

The export (`play.py export`) is a ZIP holding the written scenario image as `2 Disk 2.dsk` (and the Wizardry I
disk `T Wizardry I.dsk`, which is skipped). The next scenario takes its party from a Wizardry II scenario disk;
the Apple II backend adds an image in a `sav:` ZIP whose name is not one of the game's own disks as an extra
disk (docs/emulator/apple2.md, "Extra disks"). So the image is stored again, unchanged, under the name
`T Wizardry II.dsk` (fixed date, deflated: the same input gives the same SHA-1). Prints the SHA-1s and the
roster on the disk. Both files are game data: never committed.
"""
import hashlib, os, sys, zipfile
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", "..", ".."))
sys.path.insert(0, HERE)


def main():
    a = sys.argv[1:]
    src = a[0] if a else os.path.join(ROOT, "rom", "saves", "apple2", "wizardry-2", "02_ending.sav")
    out = a[1] if len(a) > 1 else os.path.join(ROOT, "rom", "saves", "apple2", "wizardry-3", "00_transfer.sav")
    z = zipfile.ZipFile(src)
    name = [n for n in z.namelist() if "DISK 2" in n.upper()][0]
    img = z.read(name)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as o:
        o.writestr(zipfile.ZipInfo("T Wizardry II.dsk", (1986, 1, 1, 0, 0, 0)), img, zipfile.ZIP_DEFLATED)
    print("%s\n  image SHA-1 %s (%d bytes, from %s in %s)\n  ZIP SHA-1   %s" % (
        out, hashlib.sha1(img).hexdigest(), len(img), name, src, hashlib.sha1(open(out, "rb").read()).hexdigest()))
    import data, maps
    sys.argv = ["data.py", "roster", out]
    data.main()


if __name__ == "__main__":
    main()
