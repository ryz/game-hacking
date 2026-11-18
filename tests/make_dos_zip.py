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


def build():
    b = io.BytesIO()
    with zipfile.ZipFile(b, "w") as z:
        z.writestr(zipfile.ZipInfo("KEYS.COM", (1990, 1, 1, 0, 0, 0)), COM)
    return b.getvalue()


if __name__ == "__main__":
    open(sys.argv[1], "wb").write(build())
