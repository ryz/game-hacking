"""Build a tiny original Mega Drive test ROM (128 KiB, battery RAM in the header at 200001-203FFF): the display is
off, so the whole screen is the backdrop colour, blue normally and red while button A is held. The V-blank
interrupt wakes the main loop once a frame: FF0010 counts frames, FF0011 holds the pad (bit 0 A, 1 Start, 2 B, 3 C,
4 up, 5 down, 6 left, 7 right; set while held), FF0012 keeps every bit that was ever set, 200001 (cartridge RAM)
mirrors the counter. Hand-assembled 68000, no game data. Header: SEGA MEGA DRIVE, product GM 12345678-01, regions
JUE, three-button pad, valid checksum.
  python3 tests/make_md_rom.py OUT.md"""
import struct
import sys


def w(*words):
    return b"".join(struct.pack(">H", x) for x in words)


def l(x):
    return struct.pack(">I", x)


def build():
    rom = bytearray(0x20000)
    rom[0:4] = l(0x00FFFE00)                            # initial stack pointer
    rom[4:8] = l(0x200)                                 # reset: start
    for v in range(2, 64):
        rom[v * 4:v * 4 + 4] = l(0x3F0)          # every other vector: rte at 0x3F0 (below)

    def text(at, s, n):
        rom[at:at + n] = s.encode("ascii").ljust(n, b" ")
    text(0x100, "SEGA MEGA DRIVE", 16)
    text(0x110, "(C)TEST 2026.NOV", 16)
    text(0x120, "GAMEDB SELFTEST", 48)
    text(0x150, "GAMEDB SELFTEST", 48)
    text(0x180, "GM 12345678-01", 14)
    text(0x190, "J", 16)                                # three-button pad
    rom[0x1A0:0x1A8] = l(0) + l(len(rom) - 1)
    rom[0x1A8:0x1B0] = l(0xFF0000) + l(0xFFFFFF)
    rom[0x1B0:0x1BC] = b"RA\xf8\x20" + l(0x200001) + l(0x203FFF)   # battery RAM, odd bytes
    text(0x1BC, "", 12)
    text(0x1C8, "", 40)
    text(0x1F0, "JUE", 16)

    code = bytearray()
    code += w(0x46FC, 0x2700)                           # move.w #$2700,sr
    code += w(0x1039) + l(0xA10001)                     # move.b $A10001,d0   (version register)
    code += w(0x0200, 0x000F)                           # andi.b #$0F,d0
    code += w(0x670A)                                   # beq.s +10            (no TMSS)
    code += w(0x23FC) + b"SEGA" + l(0xA14000)           # move.l #'SEGA',$A14000
    for reg in (0x8004, 0x8124, 0x8C81, 0x8700, 0x8F02):   # VDP: mode 5, display off + V-int, H40, backdrop 0
        code += w(0x33FC, reg) + l(0xC00004)            # move.w #reg,$C00004
    code += w(0x13FC, 0x0040) + l(0xA10009)             # move.b #$40,$A10009  (pad 1: TH is an output)
    code += w(0x13FC, 0x0040) + l(0xA10003)             # move.b #$40,$A10003  (TH high)
    code += w(0x23FC) + l(0) + l(0xFF0010)              # move.l #0,$FF0010
    code += w(0x46FC, 0x2500)                           # move.w #$2500,sr     (level 6 = V-int on)
    loop = len(code)
    code += w(0x4E72, 0x2500)                           # stop #$2500          (wait for V-int)
    code += w(0x5239) + l(0xFF0010)                     # addq.b #1,$FF0010
    code += w(0x13F9) + l(0xFF0010) + l(0x200001)       # move.b $FF0010,$200001
    code += w(0x13FC, 0x0000) + l(0xA10003)             # move.b #0,$A10003    (TH low)
    code += w(0x4E71, 0x4E71)                           # nop; nop
    code += w(0x1239) + l(0xA10003)                     # move.b $A10003,d1    (x0SA00DU, low = pressed)
    code += w(0x13FC, 0x0040) + l(0xA10003)             # move.b #$40,$A10003  (TH high)
    code += w(0x4E71, 0x4E71)                           # nop; nop
    code += w(0x1439) + l(0xA10003)                     # move.b $A10003,d2    (x1CBRLDU)
    code += w(0x4601, 0x4602)                           # not.b d1; not.b d2
    code += w(0x1602)                                   # move.b d2,d3
    code += w(0x0201, 0x0030, 0xE809)                   # andi.b #$30,d1; lsr.b #4,d1   -> bit 0 A, bit 1 Start
    code += w(0x0203, 0x0030, 0xE40B)                   # andi.b #$30,d3; lsr.b #2,d3   -> bit 2 B, bit 3 C
    code += w(0x8203)                                   # or.b d3,d1
    code += w(0x0202, 0x000F, 0xE90A)                   # andi.b #$0F,d2; lsl.b #4,d2   -> bits 4-7 UDLR
    code += w(0x8202)                                   # or.b d2,d1
    code += w(0x13C1) + l(0xFF0011)                     # move.b d1,$FF0011
    code += w(0x8339) + l(0xFF0012)                     # or.b d1,$FF0012
    code += w(0x23FC) + l(0xC0000000) + l(0xC00004)     # move.l #$C0000000,$C00004  (CRAM write, colour 0)
    code += w(0x303C, 0x0E00)                           # move.w #$0E00,d0     (blue)
    code += w(0x0801, 0x0000)                           # btst #0,d1           (A held?)
    code += w(0x6704)                                   # beq.s +4
    code += w(0x303C, 0x000E)                           # move.w #$000E,d0     (red)
    code += w(0x33C0) + l(0xC00000)                     # move.w d0,$C00000
    d = loop - (len(code) + 2)
    assert -128 <= d < 0
    code += w(0x6000 | (d & 0xFF))                    # bra.s loop
    assert len(code) < 0x1F0
    rom[0x200:0x200 + len(code)] = code
    rom[0x3F0:0x3F2] = w(0x4E73)                        # rte
    rom[0x10000:0x10004] = b"PG2!"                     # something past 64 KiB
    chk = sum(struct.unpack(">%dH" % ((len(rom) - 0x200) // 2), rom[0x200:])) & 0xFFFF
    rom[0x18E:0x190] = w(chk)
    return bytes(rom)


if __name__ == "__main__":
    open(sys.argv[1], "wb").write(build())
