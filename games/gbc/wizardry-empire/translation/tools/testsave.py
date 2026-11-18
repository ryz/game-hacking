"""Test save file with a powerful party: every spell, level 60, stats 20, HP 999, AC -10, gold 999999.

  python3 tools/testsave.py [--state work/states/party/renamed.state] [--out work/sav/wizardry_empire_en.sav]

Takes the cartridge RAM of a state made by tools/party.py for the current build (the six renamed characters ryz ..
mnz in the roster) and rewrites their roster records in both save halves ($A001 working, $B001 backup, $80 each):
Valiant, Avenger, Musashi, Kunoichi (female), Summoner, Bishop - together they know every school: all Mage and
Priest spells for everyone, plus each special class's own school (Summoner: all pacts) - 9 casts at every level of
every school. Then it cold-boots the English build with the file and checks the roster survived.
Load the ROM with this .sav next to it (same base name), form the party at Rose's Tavern. Never commit save files.
"""
import argparse, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
sys.path.insert(0, HERE)
import emu

CLASSES = [9, 10, 11, 12, 13, 4]          # Valiant, Avenger, Musashi, Kunoichi, Summoner, Bishop (characters.md 3.4)
SCHOOL_N = {9: 16, 10: 12, 11: 12, 12: 13, 13: 16, 4: 0}   # spells in the class's own school (characters.md 10.1)


def patch(sram):
    s = bytearray(sram)
    for half in (0x0000, 0x1000):
        for n, cls in enumerate(CLASSES):
            b = half + 1 + 0x80 * n
            r = s[b:b + 0x80]
            r[0x09] = cls
            if cls == 12:
                r[0x0B] = 1                                  # Kunoichi: female
            r[0x0D:0x0F] = (60).to_bytes(2, "little")
            r[0x31:0x38] = b"\xff" * 7                       # Mage 0-27 + Priest 28-55
            r[0x39:0x3C] = ((1 << SCHOOL_N[cls]) - 1).to_bytes(3, "little")
            r[0x3C:0x51] = bytes([9]) * 21                   # casts left, 7 levels x 3 schools
            r[0x51:0x57] = bytes([20]) * 6
            r[0x58] = (-10) & 0xFF
            r[0x59:0x5D] = (999999).to_bytes(4, "little")
            r[0x5D:0x61] = (9999999).to_bytes(4, "little")
            r[0x62:0x64] = (999).to_bytes(2, "little")
            r[0x64:0x66] = (999).to_bytes(2, "little")
            s[b:b + 0x80] = r
    return bytes(s)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--state", default=os.path.join(ROOT, "work", "states", "party", "renamed.state"))
    ap.add_argument("--out", default=os.path.join(ROOT, "work", "sav", "wizardry_empire_en.sav"))
    a = ap.parse_args()
    g = emu.open_emu(emu.EN_ROM, os.path.abspath(a.state))
    sav = patch(g.mem_read(None, 0x2000, region="cart_ram", offset=0))
    g.close()
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    open(a.out, "wb").write(sav)
    g = emu.open_emu(emu.EN_ROM)
    g.mem_write(None, sav, region="cart_ram", offset=0)
    emu.play(g, ["boot"])
    sr = g.mem_read(None, 0x2000, region="cart_ram", offset=0)
    got = [(sr[1 + 0x80 * n + 9], sr[1 + 0x80 * n + 13]) for n in range(6)]
    ok = got == [(c, 60) for c in CLASSES]
    print("wrote", os.path.relpath(a.out, ROOT), "- cold boot:", "roster OK" if ok else "roster CHANGED %r" % got)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
