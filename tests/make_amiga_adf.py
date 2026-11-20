"""Build a tiny original Amiga test disk: an 880 KiB ADF whose bootblock (run by Kickstart's strap with the
disk in DF0:) switches off interrupts and DMA, then once per frame sets the background colour COLOR00:
  white   while the joystick fire button (port 2) is held
  magenta while the left mouse button (port 1) is held
  else    red/green = the last raw key code from the keyboard, blue = counter & 15
and writes the counter to chip RAM $7F000 (word) and the mouse counters JOY0DAT to $7F002. The counter counts half frames (lines $20 and $120).
build(write=True) first writes the first 512 bytes of the bootblock to sector 2 (byte 1024) of the disk through
trackdisk.device (the request strap leaves in A1), so a test can see a game's disk write. Hand-assembled 68000,
no game data.
python3 tests/make_amiga_adf.py OUT.adf [write]"""
import struct, sys

SIZE = 901120                       # 80 cylinders x 2 heads x 11 sectors x 512 bytes


def code(write=False):
    out, labels, fix = bytearray(), {}, []

    def w(*words):
        for x in words:
            out.extend(struct.pack(">H", x & 0xFFFF))

    def label(name):
        labels[name] = len(out)

    def bra(op, name):              # short branch (8-bit displacement), resolved below
        fix.append((len(out), name))
        w(op << 8)

    if write:                       # A1 = trackdisk IOStdReq, A6 = ExecBase (from strap)
        w(0x2449)                   # movea.l a1,a2
        w(0x357C, 0x0003, 0x001C)   # move.w  #CMD_WRITE,IO_COMMAND(a2)
        w(0x257C, 0x0000, 0x0200, 0x0024)   # move.l #512,IO_LENGTH(a2)
        w(0x41FA, (-12 - (len(out) + 2)) & 0xFFFF)   # lea  bootblock(pc),a0  (code starts at byte 12)
        w(0x2548, 0x0028)           # move.l  a0,IO_DATA(a2)
        w(0x257C, 0x0000, 0x0400, 0x002C)   # move.l #1024,IO_OFFSET(a2)
        w(0x224A, 0x4EAE, 0xFE38)   # movea.l a2,a1 / jsr DoIO(a6)
        w(0x357C, 0x0004, 0x001C)   # move.w  #CMD_UPDATE,IO_COMMAND(a2)   write the track buffer out
        w(0x224A, 0x4EAE, 0xFE38)
        w(0x357C, 0x0009, 0x001C)   # move.w  #TD_MOTOR,IO_COMMAND(a2)
        w(0x42AA, 0x0024)           # clr.l   IO_LENGTH(a2)    motor off
        w(0x224A, 0x4EAE, 0xFE38)
    w(0x4BF9, 0x00DF, 0xF000)       # lea     $DFF000,a5        custom chips
    w(0x3B7C, 0x7FFF, 0x009A)       # move.w  #$7FFF,$9A(a5)    INTENA: all off
    w(0x3B7C, 0x7FFF, 0x0096)       # move.w  #$7FFF,$96(a5)    DMACON: all off (no copper: COLOR00 stays)
    w(0x49F9, 0x00BF, 0xE001)       # lea     $BFE001,a4        CIA A
    w(0x7E00)                       # moveq   #0,d7             frame counter
    w(0x7C00)                       # moveq   #0,d6             last key code
    label("frame")
    label("wait1")
    w(0x0C2D, 0x0020, 0x0006)       # cmp.b   #$20,6(a5)        VHPOSR: line $20 or $120 (twice a frame)
    bra(0x66, "wait1")              # bne.s   wait1
    label("wait2")
    w(0x0C2D, 0x0020, 0x0006)
    bra(0x67, "wait2")              # beq.s   wait2             one pass per frame
    w(0x5247)                       # addq.w  #1,d7
    w(0x082C, 0x0003, 0x0D00)       # btst    #3,$D00(a4)       ICR (read clears it): serial byte in?
    bra(0x67, "nokey")              # beq.s   nokey
    w(0x1C2C, 0x0C00)               # move.b  $C00(a4),d6       SDR: the key byte
    w(0x08EC, 0x0006, 0x0E00)       # bset    #6,$E00(a4)       CRA SPMODE output: KDAT low = handshake
    w(0x303C, 0x00C8)               # move.w  #200,d0
    w(0x51C8, 0xFFFE)               # dbra    d0,*              about 280 microseconds
    w(0x08AC, 0x0006, 0x0E00)       # bclr    #6,$E00(a4)
    w(0x4606)                       # not.b   d6
    w(0xE21E)                       # ror.b   #1,d6             raw key code (bit 7 = key up)
    label("nokey")
    w(0x3006)                       # move.w  d6,d0
    w(0x0240, 0x00FF)               # andi.w  #$FF,d0
    w(0xE948)                       # lsl.w   #4,d0
    w(0x3207)                       # move.w  d7,d1
    w(0x0241, 0x000F)               # andi.w  #$F,d1
    w(0x8041)                       # or.w    d1,d0
    w(0x0814, 0x0007)               # btst    #7,(a4)           /FIR1: joystick fire, port 2
    bra(0x66, "nofire")             # bne.s   nofire
    w(0x303C, 0x0FFF)               # move.w  #$FFF,d0
    label("nofire")
    w(0x0814, 0x0006)               # btst    #6,(a4)           /FIR0: left mouse button, port 1
    bra(0x66, "nomouse")            # bne.s   nomouse
    w(0x303C, 0x0F0F)               # move.w  #$F0F,d0
    label("nomouse")
    w(0x3B40, 0x0180)               # move.w  d0,$180(a5)       COLOR00
    w(0x33C7, 0x0007, 0xF000)       # move.w  d7,$7F000
    w(0x33ED, 0x000A, 0x0007, 0xF002)   # move.w  $A(a5),$7F002   JOY0DAT: mouse counters (Y high, X low)
    bra(0x60, "frame")              # bra.s   frame
    for at, name in fix:
        d = labels[name] - (at + 2)
        assert -128 <= d < 128 and d != 0
        out[at + 1] = d & 0xFF
    return bytes(out)


def checksum(block):
    s = 0
    for (x,) in struct.iter_unpack(">I", block):
        s += x
        if s > 0xFFFFFFFF:
            s = (s & 0xFFFFFFFF) + 1
    return ~s & 0xFFFFFFFF


def build(write=False):
    boot = bytearray(b"DOS\0" + bytes(4) + struct.pack(">I", 880) + code(write))
    boot += bytes(1024 - len(boot))
    boot[4:8] = struct.pack(">I", checksum(bytes(boot)))
    return bytes(boot) + bytes(SIZE - 1024)


if __name__ == "__main__":
    open(sys.argv[1], "wb").write(build(write=sys.argv[2:] == ["write"]))
