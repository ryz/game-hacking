"""Build a tiny original PlayStation test disc: one MODE2/2352 data track with an ISO 9660 file system holding
SYSTEM.CNF and SLUS_123.45 (the program of make_ps1_exe.py, named after its serial like a game's), plus the .cue
sheet. The BIOS boots it like a game disc (it reads SYSTEM.CNF, loads the program). No game data.
  python3 tests/make_ps1_disc.py OUT.cue      (writes OUT.cue and OUT.bin)"""
import os, struct, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import make_ps1_exe

SECTOR = 2352
SERIAL = "SLUS_123.45"


def _edc_table():
    t = []
    for i in range(256):
        v = i
        for _ in range(8):
            v = (v >> 1) ^ (0xD8018001 if v & 1 else 0)
        t.append(v)
    return t


EDC = _edc_table()


def edc(data):
    v = 0
    for b in data:
        v = (v >> 8) ^ EDC[(v ^ b) & 0xFF]
    return v


def bcd(n):
    return (n // 10) << 4 | n % 10


def raw_sector(lba, data, submode=0x08):
    """Mode 2 Form 1: sync, header (MSF of lba + 150, mode 2), subheader twice, 2048 bytes, EDC (ECC left 0)."""
    m, s, f = (lba + 150) // 4500, (lba + 150) // 75 % 60, (lba + 150) % 75
    sub = bytes([0, 0, submode, 0]) * 2
    body = sub + data.ljust(2048, b"\0")
    return (b"\x00" + b"\xff" * 10 + b"\x00" + bytes([bcd(m), bcd(s), bcd(f), 2]) + body
            + struct.pack("<I", edc(body)) + bytes(276))


def both16(v):
    return struct.pack("<H", v) + struct.pack(">H", v)


def both32(v):
    return struct.pack("<I", v) + struct.pack(">I", v)


DATE7 = bytes([126, 11, 26, 0, 0, 0, 0])            # 2026-11-26 00:00:00 GMT


def record(name, lba, size, is_dir=False):
    n = len(name)
    r = bytes([0, 0]) + both32(lba) + both32(size) + DATE7 + bytes([2 if is_dir else 0, 0, 0]) + both16(1) \
        + bytes([n]) + name
    r = r + (b"\0" if len(r) % 2 else b"")
    return bytes([len(r)]) + r[1:]


def build(exe=None):
    exe = exe or make_ps1_exe.build()
    cnf = ("BOOT = cdrom:\\SLUS_123.45;1\r\nTCB = 4\r\nEVENT = 10\r\nSTACK = 801FFF00\r\n").encode()
    exe_lba, exe_secs = 22, (len(exe) + 2047) // 2048
    total = exe_lba + exe_secs + 16                     # some padding after the program
    root = (record(b"\0", 20, 2048, True) + record(b"\1", 20, 2048, True)
            + record(b"SLUS_123.45;1", exe_lba, len(exe)) + record(b"SYSTEM.CNF;1", 21, len(cnf)))
    ptable = bytes([1, 0]) + struct.pack("<I", 20) + struct.pack("<H", 1) + b"\0\0"
    mtable = bytes([1, 0]) + struct.pack(">I", 20) + struct.pack(">H", 1) + b"\0\0"
    pvd = bytearray(2048)
    pvd[0:7] = b"\x01CD001\x01"
    pvd[8:40] = b"PLAYSTATION".ljust(32)
    pvd[40:72] = SERIAL.replace(".", "").encode().ljust(32)
    pvd[80:88] = both32(total)
    pvd[120:124], pvd[124:128], pvd[128:132] = both16(1), both16(1), both16(2048)
    pvd[132:140] = both32(len(ptable))
    pvd[140:144], pvd[148:152] = struct.pack("<I", 18), struct.pack(">I", 19)
    pvd[156:190] = record(b"\0", 20, 2048, True)
    for a, b in ((190, 318), (318, 446), (446, 574), (574, 702), (702, 739), (739, 776), (776, 813)):
        pvd[a:b] = b" " * (b - a)
    for a in (813, 830, 847, 864):
        pvd[a:a + 17] = b"0" * 16 + b"\0"
    pvd[881] = 1
    sectors = {16: (bytes(pvd), 0x09), 17: (b"\xffCD001\x01", 0x89), 18: (ptable, 0x89), 19: (mtable, 0x89),
               20: (root, 0x89), 21: (cnf, 0x89)}
    sectors[4] = (b"          Licensed  by          Sony Computer Entertainment Amer  ica ", 0x08)
    for i in range(exe_secs):
        sectors[exe_lba + i] = (exe[i * 2048:(i + 1) * 2048], 0x89 if i == exe_secs - 1 else 0x08)
    return b"".join(raw_sector(l, *sectors.get(l, (b"", 0x08))) for l in range(total))


def cue(bin_name):
    return 'FILE "%s" BINARY\n  TRACK 01 MODE2/2352\n    INDEX 01 00:00:00\n' % bin_name


def write(cue_path):
    base = os.path.splitext(cue_path)[0]
    open(base + ".bin", "wb").write(build())
    open(cue_path, "w").write(cue(os.path.basename(base) + ".bin"))


if __name__ == "__main__":
    write(sys.argv[1])
