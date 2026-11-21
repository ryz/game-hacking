"""Build a tiny original C64 test disk: a 35-track D64 (170 KiB) with one program, "TEST", that LOAD"*",8,1
and RUN start (a BASIC line 10 SYS2061, then hand-assembled 6502). Once per frame (raster line 250) it
  counts frames in $C000/$C001 (low, high),
  copies the joystick in port 2 ($DC00, active low) to $C002 and shows its bits as the border colour,
  copies the KERNAL's current key ($C5, matrix code; 64 = none) to $C003 and to the background colour.
The KERNAL keeps scanning the keyboard in its interrupt, so keys arrive as on a real machine.
build(name) -> bytes; image() helpers for tests: files(d64) lists the directory.
No game data.
python3 tests/make_c64_d64.py OUT.d64"""
import sys

SIZE = 174848                       # 683 sectors x 256 bytes
TRACKS = 35


def sectors(track):
    return 21 if track <= 17 else 19 if track <= 24 else 18 if track <= 30 else 17


def offset(track, sector):
    return (sum(sectors(t) for t in range(1, track)) + sector) * 256


def program():
    stub = bytes([0x0B, 0x08, 0x0A, 0x00, 0x9E]) + b"2061" + bytes([0x00, 0x00, 0x00])   # 10 SYS2061
    code = bytes([
        0xAD, 0x12, 0xD0,           # 080D w1: lda $d012
        0xC9, 0xFA,                 #          cmp #250
        0xD0, 0xF9,                 #          bne w1
        0xAD, 0x12, 0xD0,           # 0814 w2: lda $d012
        0xC9, 0xFA,                 #          cmp #250
        0xF0, 0xF9,                 #          beq w2
        0xEE, 0x00, 0xC0,           # 081B     inc $c000
        0xD0, 0x03,                 #          bne +3
        0xEE, 0x01, 0xC0,           #          inc $c001
        0xAD, 0x00, 0xDC,           # 0823     lda $dc00
        0x8D, 0x02, 0xC0,           #          sta $c002
        0x49, 0xFF,                 #          eor #$ff
        0x29, 0x0F,                 #          and #$0f
        0x8D, 0x20, 0xD0,           #          sta $d020
        0xA5, 0xC5,                 # 0830     lda $c5
        0x8D, 0x03, 0xC0,           #          sta $c003
        0x8D, 0x21, 0xD0,           #          sta $d021
        0x4C, 0x0D, 0x08,           # 0838     jmp w1
    ])
    return bytes([0x01, 0x08]) + stub + code   # load address $0801


def petscii(name, n=16):
    return name.upper().encode("ascii")[:n].ljust(n, b"\xA0")


def build(name="GAMEDB TEST", disk_id=b"GD", files=(("TEST", None),)):
    """A D64 with the given files (name, PRG bytes; None = the test program), each from track 17 down."""
    img = bytearray(SIZE)
    used = {(18, 0), (18, 1)}
    dirsec = bytearray(256)
    dirsec[0:2] = b"\x00\xFF"
    track = 17
    for i, (fname, data) in enumerate(files):
        data = program() if data is None else data
        chunks = [data[k:k + 254] for k in range(0, len(data), 254)] or [b""]
        assert len(chunks) <= sectors(track), "test files are one track at most"
        first = (track, 0)
        for s, chunk in enumerate(chunks):
            sec = bytearray(256)
            if s + 1 < len(chunks):
                sec[0:2] = bytes([track, s + 1])
            else:
                sec[0:2] = bytes([0, len(chunk) + 1])
            sec[2:2 + len(chunk)] = chunk
            img[offset(track, s):offset(track, s) + 256] = sec
            used.add((track, s))
        e = 2 + i * 32
        dirsec[e] = 0x82                                    # PRG, closed
        dirsec[e + 1:e + 3] = bytes(first)
        dirsec[e + 3:e + 19] = petscii(fname)
        dirsec[e + 28:e + 30] = len(chunks).to_bytes(2, "little")
        track -= 1
    img[offset(18, 1):offset(18, 1) + 256] = dirsec
    bam = bytearray(256)
    bam[0:4] = bytes([18, 1, 0x41, 0])
    for t in range(1, TRACKS + 1):
        bits = 0
        for s in range(sectors(t)):
            if (t, s) not in used:
                bits |= 1 << s
        bam[4 * t:4 * t + 4] = bytes([bin(bits).count("1"), bits & 0xFF, bits >> 8 & 0xFF, bits >> 16 & 0xFF])
    bam[0x90:0xA0] = petscii(name)
    bam[0xA0:0xA2] = b"\xA0\xA0"
    bam[0xA2:0xA4] = disk_id
    bam[0xA4] = 0xA0
    bam[0xA5:0xA7] = b"2A"
    bam[0xA7:0xAB] = b"\xA0" * 4
    img[offset(18, 0):offset(18, 0) + 256] = bam
    return bytes(img)


def files(d64):
    """[(type byte, name)] of the directory (first directory sector chain)."""
    out = []
    t, s = 18, 1
    while t:
        sec = d64[offset(t, s):offset(t, s) + 256]
        for e in range(8):
            ent = sec[e * 32:e * 32 + 32]
            if ent[2]:
                out.append((ent[2], ent[5:21].rstrip(b"\xA0").decode("latin-1")))
        t, s = sec[0], sec[1]
    return out


if __name__ == "__main__":
    open(sys.argv[1], "wb").write(build())
