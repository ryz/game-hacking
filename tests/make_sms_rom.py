"""Build a tiny original Master System test ROM (64 KiB, as Genesis Plus GX uses the Sega mapper only above 48 KiB;
cartridge RAM on): the display is off, so the whole screen is the backdrop colour, blue normally and red while button 1 is held; $C010 counts frames, $C011 holds
button 1 ($10 while held), $C012 stays set once button 1 was pressed, $C013 counts Pause presses (NMI), $8000
(cartridge RAM) mirrors the counter. Hand-assembled Z80, no game data. Header: TMR SEGA, export region, product
code 12345, version 1, valid checksum.
  python3 tests/make_sms_rom.py OUT.sms"""
import sys


def build():
    rom = bytearray(0x10000)
    rom[0:3] = b"\xc3\x80\x00"                          # jp $0080
    # NMI (Pause button): push af; ld a,($c013); inc a; ld ($c013),a; pop af; retn
    rom[0x66:0x66 + 11] = bytes([0xF5, 0x3A, 0x13, 0xC0, 0x3C, 0x32, 0x13, 0xC0, 0xF1, 0xED, 0x45])
    code, labels, fix = bytearray(), {}, []

    def emit(*b):
        code.extend(b)

    def jr(op, name):
        emit(op, 0)
        fix.append((len(code) - 1, name))

    def vdp_reg(reg, val):
        emit(0x3E, val, 0xD3, 0xBF, 0x3E, 0x80 | reg, 0xD3, 0xBF)     # ld a,val; out ($bf),a; ld a,$8r; out

    emit(0xF3, 0xED, 0x56, 0x31, 0xF0, 0xDF)            # di; im 1; ld sp,$dff0
    emit(0x3E, 0x08, 0x32, 0xFC, 0xFF)                  # ld a,8; ld ($fffc),a   (cartridge RAM at $8000)
    emit(0xAF, 0x32, 0x10, 0xC0, 0x32, 0x12, 0xC0, 0x32, 0x13, 0xC0)   # xor a; clear $c010, $c012, $c013
    vdp_reg(0, 0x04)                                    # mode 4
    vdp_reg(1, 0x80)                                    # display off, no interrupts
    vdp_reg(7, 0x00)                                    # backdrop = sprite palette entry 0 (CRAM $10)
    labels["loop"] = len(code)
    emit(0xDB, 0xBF, 0xE6, 0x80)                        # in a,($bf); and $80  (vblank flag)
    jr(0x28, "loop")                                    # jr z,loop
    emit(0x21, 0x10, 0xC0, 0x34)                        # ld hl,$c010; inc (hl)
    emit(0x7E, 0x32, 0x00, 0x80)                        # ld a,(hl); ld ($8000),a
    emit(0xDB, 0xDC, 0x2F, 0xE6, 0x10, 0x32, 0x11, 0xC0)   # in a,($dc); cpl; and $10; ld ($c011),a
    emit(0x47, 0x3A, 0x12, 0xC0, 0xB0, 0x32, 0x12, 0xC0)   # ld b,a; ld a,($c012); or b; ld ($c012),a
    emit(0x78, 0xB7, 0x0E, 0x30)                        # ld a,b; or a; ld c,$30 (blue)
    jr(0x28, "set")                                     # jr z,set
    emit(0x0E, 0x03)                                    # ld c,$03 (red)
    labels["set"] = len(code)
    emit(0x3E, 0x10, 0xD3, 0xBF, 0x3E, 0xC0, 0xD3, 0xBF, 0x79, 0xD3, 0xBE)   # CRAM $10 = c
    jr(0x18, "loop")                                    # jr loop
    for at, name in fix:
        d = labels[name] - (at + 1)
        assert -128 <= d < 128
        code[at] = d & 0xFF
    rom[0x80:0x80 + len(code)] = code
    rom[0x7FF0:0x7FF8] = b"TMR SEGA"
    rom[0x7FFC:0x7FFF] = bytes([0x45, 0x23, 0x11])     # product 12345 (BCD, low first; top digit in $7FFE), v1
    rom[0x7FFF] = 0x4E                                  # SMS export, 64 KiB checksum range
    rom[0xC000:0xC004] = b"PG3!"                       # something in the last page
    c = (sum(rom[:0x7FF0]) + sum(rom[0x8000:])) & 0xFFFF
    rom[0x7FFA:0x7FFC] = bytes([c & 0xFF, c >> 8])
    return bytes(rom)


if __name__ == "__main__":
    open(sys.argv[1], "wb").write(build())
