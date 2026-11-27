"""Build a tiny original Atari Jaguar test cartridge (1 MiB .j64, entered at 802000 through the universal header's
vector at 800404): the video is a plain background colour (RGB16), blue normally and red while button A is held.
The 68000 polls the vertical counter once a frame: 100000 counts frames (long), 100004 holds the pad as a mask of
the core's button slots (bit 0 up, 1 down, 2 left, 3 right, 4 *, 5 7, 6 4, 7 1, 8 0, 9 8, 10 5, 11 2, 12 #, 13 9,
14 6, 15 3, 16 A, 17 B, 18 C, 19 Option, 20 Pause; set while held), 100008 keeps every bit that was ever set. The
variables live at 1 MiB: with this program running, longs near 001004 lost their upper bits each frame (cause not
traced, 2026-11-27). ROM offset 10000 holds "JAG!".
Hand-assembled 68000 (checked with GNU as), no game data.
  python3 tests/make_jaguar_rom.py OUT.j64"""
import struct
import sys


def w(*words):
    return b"".join(struct.pack(">H", x) for x in words)


def l(x):
    return struct.pack(">I", x)


def build():
    rom = bytearray(0x100000)
    rom[0x400:0x408] = l(0x04040404) + l(0x802000)      # universal header: ROM width/speed, entry vector
    code = bytearray()
    code += w(0x46FC, 0x2700)                           # move.w #$2700,sr
    code += w(0x4BF9) + l(0x100000)                     # lea $100000,a5
    code += w(0x4295, 0x42AD, 4, 0x42AD, 8)             # clr.l (a5); clr.l 4(a5); clr.l 8(a5)
    code += w(0x33FC, 0x06C7) + l(0xF00028)             # move.w #$06C7,VMODE  (video on, RGB16, background on)
    main = len(code)
    code += w(0x7800, 0x7A00)                           # moveq #0,d4 (mask); moveq #0,d5 (row * 4)
    code += w(0x41FA, 0x008A)                           # lea rows(pc),a0
    row = len(code)
    code += w(0x3018)                                   # move.w (a0)+,d0      (row select, joypads on)
    code += w(0x33C0) + l(0xF14000)                     # move.w d0,JOYSTICK
    code += w(0x4E71, 0x4E71)                           # nop; nop
    code += w(0x3239) + l(0xF14000)                     # move.w JOYSTICK,d1   (bits 8-11: four keys, low = held)
    code += w(0x3439) + l(0xF14002)                     # move.w JOYBUTS,d2    (bit 1: A/B/C/Option, bit 0: Pause)
    code += w(0x2618)                                   # move.l (a0)+,d3      (this row's fire-button bit)
    code += w(0x4641, 0xE049)                           # not.w d1; lsr.w #8,d1
    code += w(0x0281) + l(0xF)                          # andi.l #$F,d1
    code += w(0xEBA9, 0x8881)                           # lsl.l d5,d1; or.l d1,d4
    code += w(0x0802, 0x0001, 0x6602, 0x8883)           # btst #1,d2; bne.s +2; or.l d3,d4
    code += w(0x4A45, 0x660A)                           # tst.w d5; bne.s +10  (Pause: row 0 only)
    code += w(0x0802, 0x0000, 0x6604, 0x08C4, 0x0014)   # btst #0,d2; bne.s +4; bset #20,d4
    code += w(0x5845, 0x0C45, 0x0010)                   # addq.w #4,d5; cmpi.w #16,d5
    code += w(0x6600 | ((row - (len(code) + 2)) & 0xFF))   # bne.s row
    code += w(0x2B44, 0x0004, 0x89AD, 0x0008)           # move.l d4,4(a5); or.l d4,8(a5)
    code += w(0x303C, 0x07C0)                           # move.w #$07C0,d0     (blue)
    code += w(0x0804, 0x0010, 0x6704)                   # btst #16,d4; beq.s +4
    code += w(0x303C, 0xF800)                           # move.w #$F800,d0     (red)
    code += w(0x33C0) + l(0xF00058)                     # move.w d0,BG
    for branch in (0x65F0, 0x64F0):                     # wait for VC >= 200, then for VC < 200: one frame
        code += w(0x3039) + l(0xF00006)                 # move.w VC,d0
        code += w(0x0240, 0x07FF, 0x0C40, 200)          # andi.w #$7FF,d0; cmpi.w #200,d0
        code += w(branch)                               # bcs.s / bcc.s back
    code += w(0x5295)                                   # addq.l #1,(a5)
    code += w(0x6000, (main - (len(code) + 2)) & 0xFFFF)   # bra.w main
    assert len(code) == 0xAC                            # rows: right after the code (lea above)
    for sel, fire in ((0x817E, 16), (0x817D, 17), (0x817B, 18), (0x8177, 19)):
        code += w(sel) + l(1 << fire)                   # rows 0-3 of port 1: fire A, B, C, Option
    rom[0x2000:0x2000 + len(code)] = code
    rom[0x10000:0x10004] = b"JAG!"
    return bytes(rom)


if __name__ == "__main__":
    open(sys.argv[1], "wb").write(build())
