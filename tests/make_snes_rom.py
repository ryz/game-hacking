"""Build a tiny original SNES test ROM (LoROM, 32 KiB, 8 KiB battery RAM): the whole screen is one colour, blue
normally and red while A is held; $7E0010 counts frames, $7E0011 holds the A button, $7E0012 stays set once A was
pressed, $70:0000 (battery RAM) mirrors the counter. Hand-assembled 65C816 (emulation mode), no game data.
  python3 tests/make_snes_rom.py OUT.sfc"""
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
    emit(0xA9, 0x8F, 0x8D, 0x00, 0x21)                  # lda #$8f; sta $2100 (forced blank)
    emit(0xA9, 0x01, 0x8D, 0x00, 0x42)                  # lda #1; sta $4200 (auto joypad read, no NMI)
    label("loop")
    emit(0xAD, 0x12, 0x42)                              # wait for vblank
    branch(0x10, "loop")                                # bpl
    label("joy")
    emit(0xAD, 0x12, 0x42, 0x29, 0x01)                  # wait until the auto joypad read is done
    branch(0xD0, "joy")                                 # bne
    emit(0xAD, 0x18, 0x42, 0x29, 0x80, 0x85, 0x11)      # lda $4218; and #$80; sta $11  (A button)
    emit(0x05, 0x12, 0x85, 0x12, 0xA5, 0x11)            # ora $12; sta $12; lda $11
    branch(0xF0, "blue")                                # beq
    emit(0xA9, 0x1F, 0xA2, 0x00)                        # red: BGR555 $001f
    jmp("set")
    label("blue")
    emit(0xA9, 0x00, 0xA2, 0x7C)                        # blue: $7c00
    label("set")
    emit(0x48, 0xA9, 0x00, 0x8D, 0x21, 0x21, 0x68)      # pha; lda #0; sta $2121 (CGRAM address 0); pla
    emit(0x8D, 0x22, 0x21, 0x8E, 0x22, 0x21)            # sta $2122; stx $2122 (backdrop colour)
    emit(0xA9, 0x0F, 0x8D, 0x00, 0x21)                  # lda #$0f; sta $2100 (screen on, full brightness)
    emit(0xE6, 0x10, 0xA5, 0x10, 0x8F, 0x00, 0x00, 0x70)  # inc $10; lda $10; sta $700000
    label("end")
    emit(0xAD, 0x12, 0x42)                              # wait for the end of vblank (count once per frame)
    branch(0x30, "end")                                 # bmi
    jmp("loop")
    label("irq")
    emit(0x40)                                          # rti
    for pos, name in fix:
        if name.startswith("abs:"):
            a = 0x8000 + labels[name[4:]]
            code[pos], code[pos + 1] = a & 0xFF, a >> 8
        else:
            code[pos] = (labels[name] - (pos + 1)) & 0xFF
    rom = bytearray(0x8000)
    rom[:len(code)] = code
    h = 0x7FC0
    rom[h:h + 21] = b"GAMEDB SELFTEST".ljust(21)
    rom[h + 0x15:h + 0x1C] = bytes([0x20, 0x02, 0x05, 0x03, 0x01, 0x00, 0x00])   # LoROM, ROM+RAM+battery, 32K, 8K, USA
    irq = 0x8000 + labels["irq"]
    for v in range(0x7FE4, 0x8000, 2):                  # every vector -> rti, then the emulation reset vector
        rom[v], rom[v + 1] = irq & 0xFF, irq >> 8
    rom[0x7FFC], rom[0x7FFD] = 0x00, 0x80
    rom[h + 0x1C:h + 0x20] = b"\xff\xff\x00\x00"
    chk = sum(rom) & 0xFFFF
    rom[h + 0x1C], rom[h + 0x1D] = (chk ^ 0xFFFF) & 0xFF, (chk ^ 0xFFFF) >> 8
    rom[h + 0x1E], rom[h + 0x1F] = chk & 0xFF, chk >> 8
    return bytes(rom)


if __name__ == "__main__":
    open(sys.argv[1], "wb").write(build())
