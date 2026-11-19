"""Build a tiny original DOS test game: a ZIP with KEYS.COM, which waits for a key (BIOS int 16h), prints a letter
a-p made from the low 4 bits of the BIOS tick counter (so timing shows on screen), then the key; w first creates
the empty file S.DAT (a "save"); q quits. Hand-assembled 8086, no game data.   python3 tests/make_dos_zip.py OUT.zip"""
import io, sys, zipfile

COM = bytes.fromhex(
    "B400CD16"          # 0100 mov ah,0 / int 16h        wait for a key -> al
    "3C717429"          # 0104 cmp al,'q' / je 0131
    "3C77750F"          # 0108 cmp al,'w' / jne 011B
    "B43C31C9BA3601CD21"  # 010C mov ah,3Ch / xor cx,cx / mov dx,0136h / int 21h   create S.DAT
    "89C3B43ECD21"      # 0115 mov bx,ax / mov ah,3Eh / int 21h                     close it
    "50"                # 011B push ax
    "B400CD1A"          # 011C mov ah,0 / int 1Ah        ticks -> cx:dx
    "80E20F80C261"      # 0120 and dl,0Fh / add dl,'a'
    "B402CD21"          # 0126 mov ah,2 / int 21h        print the tick letter
    "5A"                # 012A pop dx
    "B402CD21"          # 012B mov ah,2 / int 21h        print the key
    "EBCF"              # 012F jmp 0100
    "B8004CCD21"        # 0131 mov ax,4C00h / int 21h    exit
    "532E44415400")     # 0136 "S.DAT",0


EXIT = bytes.fromhex("B8004CCD21")      # a second program (exits at once): with two programs DOSBox Pure
                                           # shows its start menu instead of starting the only one


HOLD = bytes.fromhex(   # opens the shipped D.DAT read/write once, then writes every key into it and never closes
    "B8023DBA2E01CD21"  # 0100 mov ax,3D02h / mov dx,012Eh / int 21h   open D.DAT
    "89C3"              # 0108 mov bx,ax                               handle kept in bx
    "B400CD16"          # 010A mov ah,0 / int 16h        wait for a key -> al
    "3C717417"          # 010E cmp al,'q' / je 0129
    "A23401"            # 0112 mov [0134h],al
    "B440B90100BA3401CD21"  # 0115 mov ah,40h / mov cx,1 / mov dx,0134h / int 21h   write 1 byte
    "8A163401B402CD21"  # 011F mov dl,[0134h] / mov ah,2 / int 21h   print the key
    "EBE1"              # 0127 jmp 010A
    "B8004CCD21"        # 0129 mov ax,4C00h / int 21h    exit (DOS closes the file)
    "442E44415400"      # 012E "D.DAT",0
    "00")               # 0134 buffer


def build_hold():
    """HOLD.COM + D.DAT ("........"): a game that keeps its save file open, like the Wizardry loaders."""
    b = io.BytesIO()
    with zipfile.ZipFile(b, "w") as z:
        z.writestr(zipfile.ZipInfo("HOLD.COM", (1990, 1, 1, 0, 0, 0)), HOLD)
        z.writestr(zipfile.ZipInfo("D.DAT", (1990, 1, 1, 0, 0, 0)), b"........")
    return b.getvalue()


def build(menu=False):
    b = io.BytesIO()
    with zipfile.ZipFile(b, "w") as z:
        if menu:
            z.writestr(zipfile.ZipInfo("EXIT.COM", (1990, 1, 1, 0, 0, 0)), EXIT)
        z.writestr(zipfile.ZipInfo("KEYS.COM", (1990, 1, 1, 0, 0, 0)), COM)
    return b.getvalue()


if __name__ == "__main__":
    open(sys.argv[1], "wb").write(build())
