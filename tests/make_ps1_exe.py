"""Build a tiny original PlayStation test program (PS-X EXE, loaded at $80010000): it starts the BIOS pad driver
(InitPad/StartPad), sets up a 320x240 NTSC display and then loops: $80100000 counts loop passes, $80100004 holds
the pressed buttons (PlayStation bit order, 1 = held: bit 14 = cross, bit 4 = up), and the whole screen is filled
with red = pass counter, green = low byte of the buttons, blue = high byte. Hand-assembled MIPS, no game data.
  python3 tests/make_ps1_exe.py OUT.exe"""
import struct, sys

R = {"zero": 0, "at": 1, "v0": 2, "a0": 4, "a1": 5, "a2": 6, "a3": 7, "t0": 8, "t1": 9, "t2": 10, "t3": 11,
     "t4": 12, "t5": 13, "s0": 16, "sp": 29, "ra": 31}
BASE = 0x80010000
COUNTER, BUTTONS, PAD1, PAD2 = 0x80100000, 0x80100004, 0x80100100, 0x80100200


def build(region="North America"):
    code, labels, fix = [], {}, []

    def i(op, rs, rt, imm):
        code.append(op << 26 | R[rs] << 21 | R[rt] << 16 | (imm & 0xFFFF))

    def r(funct, rs="zero", rt="zero", rd="zero", sa=0):
        code.append(R[rs] << 21 | R[rt] << 16 | R[rd] << 11 | sa << 6 | funct)

    def li(reg, v):
        i(0x0F, "zero", reg, v >> 16)                   # lui
        i(0x0D, reg, reg, v)                            # ori

    def nop():
        code.append(0)

    def bios(table, fn):                                # call A0/B0/C0 function fn: jalr t2 with t1 in the slot
        li("t2", table)
        r(0x09, "t2", rd="ra")
        i(0x09, "zero", "t1", fn)                       # addiu t1,zero,fn (delay slot)

    li("sp", 0x801FFF00)
    li("a0", PAD1); i(0x09, "zero", "a1", 34); li("a2", PAD2); i(0x09, "zero", "a3", 34)
    bios(0xB0, 0x12)                                    # InitPad(buf1, 34, buf2, 34)
    bios(0xB0, 0x13)                                    # StartPad()
    i(0x09, "zero", "a0", 2)
    code.append(0x0000000C)                             # syscall ExitCriticalSection: interrupts on
    li("s0", 0x1F800000)
    for word in (0x00000000, 0x08000001, 0x05000000, 0x06C60260, 0x07040010, 0x03000000):
        li("t0", word); i(0x2B, "s0", "t0", 0x1814)     # GP1: reset, 320x240 NTSC, start, ranges, display on
    for word in (0xE1000400, 0xE3000000, 0xE403BD3F, 0xE5000000):
        li("t0", word); i(0x2B, "s0", "t0", 0x1810)     # GP0: draw to display, area 0,0-319,239, offset 0
    labels["loop"] = len(code)
    i(0x0F, "zero", "at", COUNTER >> 16)
    i(0x23, "at", "t0", COUNTER & 0xFFFF); nop()        # lw t0,counter (load delay)
    i(0x09, "t0", "t0", 1); i(0x2B, "at", "t0", COUNTER & 0xFFFF)
    i(0x25, "at", "t1", (PAD1 + 2) & 0xFFFF); nop()     # lhu t1,pad1+2 (buttons, 0 = held)
    r(0x27, "t1", "zero", "t1")                         # nor t1,t1,zero
    i(0x0C, "t1", "t1", 0xFFFF)                         # andi
    i(0x2B, "at", "t1", BUTTONS & 0xFFFF)
    i(0x0C, "t0", "t3", 0xFF)                           # t3 = red
    r(0x00, rt="t1", rd="t4", sa=8)                     # sll t4,t1,8: green = low byte, blue = high byte
    r(0x25, "t3", "t4", "t3")                           # or
    li("t4", 0x02000000); r(0x25, "t3", "t4", "t3")     # GP0 02: fill rectangle with colour t3
    i(0x2B, "s0", "t3", 0x1810); i(0x2B, "s0", "zero", 0x1810)
    li("t4", 0x00F00140); i(0x2B, "s0", "t4", 0x1810)  # 320x240
    li("t5", 20000)
    labels["wait"] = len(code)
    i(0x09, "t5", "t5", -1)
    fix.append(len(code)); i(0x05, "t5", "zero", 0)     # bne t5,zero,wait
    nop()
    code.append(0x02 << 26 | ((BASE + 4 * labels["loop"]) >> 2) & 0x3FFFFFF)    # j loop
    nop()
    for at in fix:
        code[at] |= (labels["wait"] - at - 1) & 0xFFFF
    body = b"".join(struct.pack("<I", w) for w in code)
    body += bytes(-len(body) % 0x800)
    head = bytearray(0x800)
    head[0:8] = b"PS-X EXE"
    struct.pack_into("<IIII", head, 0x10, BASE, 0, BASE, len(body))
    struct.pack_into("<II", head, 0x30, 0x801FFF00, 0)
    marker = b"Sony Computer Entertainment Inc. for %s area" % region.encode()
    head[0x4C:0x4C + len(marker)] = marker
    return bytes(head) + body


if __name__ == "__main__":
    open(sys.argv[1], "wb").write(build())
