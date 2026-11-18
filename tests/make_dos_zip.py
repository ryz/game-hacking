"""Build a tiny original DOS test game: a ZIP with KEYS.COM, which waits for a key (BIOS int 16h), prints a letter
a-p made from the low 4 bits of the BIOS tick counter (so timing shows on screen), then the key; q quits.
Hand-assembled 8086, no game data.   python3 tests/make_dos_zip.py OUT.zip"""
import io, sys, zipfile

COM = bytes.fromhex(
    "B400CD16"          # 0100 mov ah,0 / int 16h        wait for a key -> al
    "3C717416"          # 0104 cmp al,'q' / je 011E
    "50"                # 0108 push ax
    "B400CD1A"          # 0109 mov ah,0 / int 1Ah        ticks -> cx:dx
    "80E20F80C261"      # 010D and dl,0Fh / add dl,'a'
    "B402CD21"          # 0113 mov ah,2 / int 21h        print the tick letter
    "5A"                # 0117 pop dx
    "B402CD21"          # 0118 mov ah,2 / int 21h        print the key
    "EBE2"              # 011C jmp 0100
    "B8004CCD21")       # 011E mov ax,4C00h / int 21h    exit


def build():
    b = io.BytesIO()
    with zipfile.ZipFile(b, "w") as z:
        z.writestr(zipfile.ZipInfo("KEYS.COM", (1990, 1, 1, 0, 0, 0)), COM)
    return b.getvalue()


if __name__ == "__main__":
    open(sys.argv[1], "wb").write(build())
