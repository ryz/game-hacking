"""Build a tiny original Apple II test disk: a 140 KiB DOS-order image whose boot sector (loaded to $0800 by the
Disk II boot ROM) clears the screen, then for every key prints a letter @-O made from the low 4 bits of a counter
that runs while it waits (so timing shows on screen) and the key itself. Hand-assembled 6502, no game data.
python3 tests/make_apple2_disk.py OUT.dsk"""
import sys

BOOT = bytes.fromhex(
    "01"            # 0800 sectors to load
    "BD88C0"        # 0801 LDA $C088,X    drive motor off (X = slot * 16)
    "2089FE"        # 0804 JSR $FE89      SETKBD  input and output back to keyboard and screen
    "2093FE"        # 0807 JSR $FE93      SETVID  (a boot started with PR#6 leaves the output hook on slot 6)
    "2058FC"        # 080A JSR $FC58      HOME
    "A000"          # 080D LDY #0
    "C8"            # 080F INY
    "AD00C0"        # 0810 LDA $C000      keyboard
    "10FA"          # 0813 BPL $080F      no key yet
    "8D10C0"        # 0815 STA $C010      clear the strobe
    "48"            # 0818 PHA
    "98"            # 0819 TYA
    "290F"          # 081A AND #$0F
    "09C0"          # 081C ORA #$C0       @ A B ... O
    "20EDFD"        # 081E JSR $FDED      COUT
    "68"            # 0821 PLA
    "20EDFD"        # 0822 JSR $FDED      COUT: the key
    "4C0D08")       # 0825 JMP $080D


def build(fill=0):
    return BOOT + bytes(256 - len(BOOT)) + bytes([fill]) * (143360 - 256)


if __name__ == "__main__":
    open(sys.argv[1], "wb").write(build())
