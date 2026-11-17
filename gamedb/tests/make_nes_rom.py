"""Build a tiny original NES test ROM (NROM, 16 KiB PRG, CHR RAM, battery flag): the whole screen is one colour,
blue normally and red while A is held; $10 counts frames, $11 holds the A button, $12 stays 1 once A was pressed, $6000 (battery RAM) mirrors the
counter. Hand-assembled 6502, no game data.   python3 tests/make_nes_rom.py OUT.nes"""
import sys


def build():
    code, labels, fix = bytearray(), {}, []

    def emit(*b):
        code.extend(b)

    def label(name):
        labels[name] = len(code)

    def branch(op, name):
        emit(op, 0)
        fix.append((len(code) - 1, name))

    def jmp(name):
        emit(0x4C, 0, 0)
        fix.append((len(code) - 2, "abs:" + name))

    emit(0x78, 0xD8, 0xA2, 0xFF, 0x9A)                  # sei; cld; ldx #$ff; txs
    emit(0xA9, 0x00, 0x8D, 0x00, 0x20, 0x8D, 0x01, 0x20)  # lda #0; sta $2000; sta $2001 (rendering off)
    emit(0x2C, 0x02, 0x20)                              # bit $2002
    for n in ("v1", "v2"):                              # two vblanks: PPU warm-up
        label(n)
        emit(0x2C, 0x02, 0x20)
        branch(0x10, n)                                 # bpl
    label("loop")
    emit(0x2C, 0x02, 0x20)                              # wait for vblank
    branch(0x10, "loop")
    emit(0xA9, 0x01, 0x8D, 0x16, 0x40, 0xA9, 0x00, 0x8D, 0x16, 0x40)   # strobe the controller
    emit(0xAD, 0x16, 0x40, 0x29, 0x01, 0x85, 0x11)      # lda $4016; and #1; sta $11  (A button)
    emit(0x05, 0x12, 0x85, 0x12, 0xA5, 0x11)            # ora $12; sta $12; lda $11  ($12 = A was ever pressed)
    branch(0xF0, "blue")                                # beq
    emit(0xA9, 0x16)                                    # lda #$16 (red)
    jmp("set")
    label("blue")
    emit(0xA9, 0x12)                                    # lda #$12 (blue)
    label("set")
    emit(0x48, 0xA9, 0x3F, 0x8D, 0x06, 0x20, 0xA9, 0x00, 0x8D, 0x06, 0x20)   # pha; $2006 = $3f00
    emit(0x68, 0x8D, 0x07, 0x20)                        # pla; sta $2007 (backdrop colour)
    emit(0xA9, 0x00, 0x8D, 0x06, 0x20, 0x8D, 0x06, 0x20)  # $2006 = 0 (so the backdrop is shown, not $3f01)
    emit(0xE6, 0x10, 0xA5, 0x10, 0x8D, 0x00, 0x60)      # inc $10; lda $10; sta $6000
    jmp("loop")
    label("irq")
    emit(0x40)                                          # rti
    for pos, name in fix:
        if name.startswith("abs:"):
            a = 0xC000 + labels[name[4:]]
            code[pos], code[pos + 1] = a & 0xFF, a >> 8
        else:
            code[pos] = (labels[name] - (pos + 1)) & 0xFF
    prg = bytearray(0x4000)
    prg[:len(code)] = code
    irq = 0xC000 + labels["irq"]
    prg[0x3FFA:0x4000] = bytes([irq & 0xFF, irq >> 8, 0x00, 0xC0, irq & 0xFF, irq >> 8])   # NMI, RESET, IRQ
    header = b"NES\x1a" + bytes([1, 0, 0x02, 0x00]) + bytes(8)       # 1x16K PRG, CHR RAM, battery, mapper 0
    return header + bytes(prg)


if __name__ == "__main__":
    open(sys.argv[1], "wb").write(build())
