"""Wizardry II: Knight of Diamonds (NES) - roster records in battery RAM and their checksum.

Roster: 20 records of $60 bytes at $6400 + slot*$60 (slots 0-5 = the pre-made FIGHTER1..MAGE2), a second copy at
$7800 + slot*$60; $6B80 = number of characters, $6B81 = party size, $6B82.. = party slot numbers.
Every record ends with a 16-bit check value at +$5E/+$5F (a nibble-table CRC, code in PRG bank 4 (8 KiB) at
$8D8C/$8DB4, tables $8DDE-$8E2D). At power-on (code $8D42) a record whose check fails is emptied (byte 0 = 0),
so a poke into a record must rewrite +$5E/+$5F: this tool prints the poke tokens with the new check value.

python3 games/nes/wizardry-2-nes/tools/roster.py check SRAM.bin           -> verifies every record of a battery dump
python3 games/nes/wizardry-2-nes/tools/roster.py edit IN.sav OUT.sav SLOT:OFF=HEX[,OFF=HEX...] [SLOT:...]
    -> writes a new battery save with the records changed and their check values fixed (both copies), e.g.
       `... edit games/nes/wizardry-2-nes/saves/01_party.sav rom/saves/wizardry-2-nes/rich.sav 6:11=000000001873`
python3 games/nes/wizardry-2-nes/tools/roster.py pokes SRAM.bin SLOT OFF=HEX[,OFF=HEX...]
    -> poke tokens for the changed record (both copies). NOTE: `play.py poke` into $6000-$7FFF is dropped while
       the game keeps the MMC3 RAM disabled (nearly always; peeks read $6x open bus), so use `edit` + `sav:NAME`.

Record offsets (scout 2026-11-18, from dumps of the six new characters): +0 in-use/location (02 seen), +1 name
length, +2..+9 name (ASCII, space padded), +$0A race/class/alignment (packed, not decoded), +$0B..+$10 STR IQ PIE
VIT AGI LUC, +$11..+$16 gold (packed BCD, big-endian: 00 00 00 00 04 22 = 422), +$17..+$1C E.P. (BCD, same),
+$1D/+$1E HP now and +$1F/+$20 HP max (little-endian), +$22 level (tentative), +$26 AC (0A = 10; tentative).
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
ROM = ROOT / "rom" / "wizardry-2-nes.nes"
BASES = (0x6400, 0x7800)


def tables():
    b = ROM.read_bytes()[16:][4 * 0x2000:5 * 0x2000]          # PRG bank 4 (8 KiB) at $8000
    t = lambda a: b[a - 0x8000:a - 0x8000 + 16]
    return t(0x8DDE), t(0x8DEE), t(0x8DFE), t(0x8E0E), t(0x8E1E)


def crc(rec, T=None):
    """The game's check over a 96-byte record: 0 when the record is valid."""
    DE, EE, FE, E0, E1 = T or tables()
    s0, s1 = 0xFF ^ rec[0], 0xFF ^ rec[1]
    for y in range(2, 0x60):
        s2 = rec[y]
        x = s0 >> 4
        s1 ^= EE[x]
        s2 ^= FE[x]
        x = DE[x] ^ s0
        s0, s1 = E0[x] ^ s1, E1[x] ^ s2
    return s0, s1


def fix(rec):
    """Return the record with +$5E/+$5F rewritten the way the game does (zero them, run the check, store)."""
    r = bytearray(rec)
    r[0x5E] = r[0x5F] = 0
    r[0x5E], r[0x5F] = crc(r)
    return bytes(r)


def main(argv):
    T = tables()
    s = Path(argv[1]).read_bytes()
    if argv[0] == "check":
        for slot in range(20):
            for base in BASES:
                o = base - 0x6000 + slot * 0x60
                rec = s[o:o + 0x60]
                if rec[0]:
                    name = rec[2:2 + rec[1]].decode("ascii", "replace")
                    ok = crc(rec, T) == (0, 0) and fix(rec) == rec
                    print(f"${base + slot * 0x60:04X} slot {slot:2d} {name:8s} {'ok' if ok else 'BAD'}")
        return
    if argv[0] == "edit":
        out = bytearray(s)
        for spec in argv[3:]:
            slot, kvs = spec.split(":", 1)
            slot = int(slot)
            for base in BASES:
                o = base - 0x6000 + slot * 0x60
                rec = bytearray(out[o:o + 0x60])
                if not rec[0]:
                    continue
                for kv in kvs.split(","):
                    k, v = kv.split("=")
                    data = bytes.fromhex(v)
                    rec[int(k, 16):int(k, 16) + len(data)] = data
                out[o:o + 0x60] = fix(rec)
        Path(argv[2]).write_bytes(bytes(out))
        print(argv[2])
        return
    slot = int(argv[2])
    o = 0x400 + slot * 0x60
    rec = bytearray(s[o:o + 0x60])
    for kv in argv[3].split(","):
        k, v = kv.split("=")
        data = bytes.fromhex(v)
        rec[int(k, 16):int(k, 16) + len(data)] = data
    rec = fix(rec)
    old = s[o:o + 0x60]
    toks = []
    for base in BASES:
        a = base + slot * 0x60
        toks += [f"poke:{a + i:04X}={rec[i]:02X}" for i in range(0x60) if rec[i] != old[i]]
    print(",".join(toks))


if __name__ == "__main__":
    main(sys.argv[1:])
