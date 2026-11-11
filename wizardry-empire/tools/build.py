"""Build the English ROM and IPS patch.

  python3 tools/build.py            -> build/wizardry_empire_en.gbc, build/wizardry_empire_en.ips

Steps: verify the original dump, expand to 2 MB, generate VWF font/pool binaries,
insert translated text (tools/insert.py), assemble asm/main.asm, fix header checksums, write IPS.
"""
import hashlib, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
sys.path.insert(0, HERE)
import asm, font, insert, ips  # noqa: E402

ROM_IN = os.path.join(ROOT, "rom", "wizardry_empire_j.gbc")
BUILD = os.path.join(ROOT, "build")
ROM_OUT = os.path.join(BUILD, "wizardry_empire_en.gbc")
IPS_OUT = os.path.join(BUILD, "wizardry_empire_en.ips")
NEW_SIZE = 2 * 1024 * 1024

# Codes $80-$EF: the font's kana half, which the patch no longer loads (see VWF_FontLoad).
POOL = list(range(0x80, 0xF0)) + (  # + the kana in the lower half (also not loaded any more)
    list(range(0x01, 0x20)) + [0x23, 0x24, 0x26, 0x3C, 0x3D, 0x3E, 0x40]
    + list(range(0x5B, 0x61)) + list(range(0x7B, 0x80)))


def check_rom(data):
    want = open(os.path.join(ROOT, "rom.sha1")).read().split()[0]
    got = hashlib.sha1(data).hexdigest()
    if got != want:
        sys.exit("rom/wizardry_empire_j.gbc: SHA-1 %s, expected %s" % (got, want))


def gen_bins():
    f = font.load()
    adv = bytearray(256)
    rows = bytearray(256 * 8)
    for code, (a, r) in f.items():
        adv[code] = a
        rows[code * 8:code * 8 + 8] = bytes(r)
    os.makedirs(BUILD, exist_ok=True)
    open(os.path.join(BUILD, "font_adv.bin"), "wb").write(adv)
    open(os.path.join(BUILD, "font_rows.bin"), "wb").write(rows)
    open(os.path.join(BUILD, "pool.bin"), "wb").write(bytes(POOL))
    flags = bytearray(256)
    for c in POOL:
        flags[c] = 1
    open(os.path.join(BUILD, "poolflags.bin"), "wb").write(flags)


FONT_OFF = 0x4400  # bank 1 $4400: original 8x8 font, code*16
ASCII_FIX = [0x22, 0x27, 0x28, 0x29, 0x2C, 0x3B]  # kana tiles at ASCII punctuation codes


def patch_fixed_font(rom):
    """Fixed-width fallback: draw ASCII punctuation over kana tiles that share the code."""
    f = font.load()
    for c in ASCII_FIX:
        adv, rows = f[c]
        w = adv - 1
        shift = (8 - w) // 2
        tile = bytearray()
        for r in rows:
            tile += bytes([(r >> shift) & 0xFF, 0xFF])
        rom[FONT_OFF + c * 16:FONT_OFF + c * 16 + 16] = tile


def fix_checksums(rom):
    c = 0
    for i in range(0x134, 0x14D):
        c = (c - rom[i] - 1) & 0xFF
    rom[0x14D] = c
    rom[0x14E] = rom[0x14F] = 0
    g = sum(rom) & 0xFFFF
    rom[0x14E], rom[0x14F] = g >> 8, g & 0xFF


def build(rom_in=ROM_IN, out=ROM_OUT, ips_out=IPS_OUT, verbose=True):
    orig = open(rom_in, "rb").read()
    check_rom(orig)
    rom = bytearray(orig) + b"\xff" * (NEW_SIZE - len(orig))
    rom[0x148] = 0x06  # 2 MB
    gen_bins()
    import lint
    if os.environ.get("NO_LINT") != "1":
        items = [(lint.key_of(f, e), lint.text_of(e.get("jp")), lint.text_of(e.get("en"))) for f, e in lint.entries()]
        lerrs, _ = lint.check(items, lint.glossary())
        if lerrs:
            sys.exit("lint errors (python3 tools/lint.py; NO_LINT=1 to skip):\n" + "\n".join(lerrs))
    patch_fixed_font(rom)
    stats = insert.insert_all(rom)
    a = asm.assemble(os.path.join(ROOT, "asm", "main.asm"))
    for off, b, where in a.patches:
        rom[off:off + len(b)] = b
    stats["fixmap entries"] = insert.post_asm(rom, a.sym)
    with open(os.path.splitext(out)[0] + ".sym", "w") as f:  # rgbds-style symbols for the debugger
        for k, (b, v) in sorted(a.sym.items(), key=lambda kv: ((kv[1][0] or 0), kv[1][1])):
            if b is not None:
                f.write("%02x:%04x %s\n" % (b, v, k))
    fix_checksums(rom)
    open(out, "wb").write(rom)
    open(ips_out, "wb").write(ips.make(orig + b"\xff" * (NEW_SIZE - len(orig)), bytes(rom), orig_len=len(orig)))
    if verbose:
        print("wrote", os.path.relpath(out, ROOT), "and", os.path.relpath(ips_out, ROOT))
        for k, v in stats.items():
            print("  %s: %s" % (k, v))
    return rom


if __name__ == "__main__":
    build()
