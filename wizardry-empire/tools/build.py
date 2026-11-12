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
# $CF/$D0 stay with the game: the battle monster panel shows "(n)" with them (symbol glyphs from 1:$40F0).
# $A0 is VRAM1 tile $20 in the split layout: the game writes $20 (space) into cells whose attribute still
# selects VRAM bank 1, so the VWF keeps that tile blank (VWF_FontLoad). $EF = spell-screen cursor arrow.
POOL = [c for c in range(0x80, 0xF0) if c not in (0xA0, 0xCF, 0xD0, 0xEF)] + (  # + the kana in the lower half (also not loaded any more)
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
    assert not any(adv[0x80:]) and not any(rows[0x400:]), "VWF font codes must be < $80"
    open(os.path.join(BUILD, "font_adv.bin"), "wb").write(adv[:0x80])
    open(os.path.join(BUILD, "font_rows.bin"), "wb").write(rows[:0x400])
    open(os.path.join(BUILD, "pool.bin"), "wb").write(bytes(POOL))
    shift = bytearray()                      # VWF Glyph: page 2p = b >> p, page 2p+1 = (b << (8-p)) & $FF
    for p in range(8):
        shift += bytes(b >> p for b in range(256))
        shift += bytes(((b << (8 - p)) & 0xFF) if p else 0 for b in range(256))
    open(os.path.join(BUILD, "shift.bin"), "wb").write(shift)
    flags = bytearray(256)
    for c in POOL:
        flags[c] = 1
    open(os.path.join(BUILD, "poolflags.bin"), "wb").write(flags)
    mask = bytearray(32)                     # TryAlloc1: bit (code & 7) of byte code/8 = code is a VWF slot
    for c in POOL:
        mask[c >> 3] |= 1 << (c & 7)
    open(os.path.join(BUILD, "poolmask.bin"), "wb").write(mask)
    # GC prefilter: a cell code that can be a slot in some layout (code itself, or code|$80 for VRAM1 low codes)
    maybe = bytes(1 if flags[e] or (e < 0x70 and flags[e | 0x80]) else 0 for e in range(256))
    open(os.path.join(BUILD, "maybeslot.bin"), "wb").write(maybe)
    open(os.path.join(BUILD, "card_status.bin"), "wb").write(card_status(adv))


CARD_STATUS = range(0x7574, 0x75A6, 5)   # 26:7574: the card's 10 status words, 5 bytes each (fixtables.json)
CARD_EDGE = 19 * 8                       # right edge of the card's value column (col 18), as Lvl/Age/AC
CARD_ROW = 0x60                          # low byte of the status row ($D060)


def card_status(adv):
    """26:7840 table for CardStatus: per status word 32 bytes = start cell (low byte, row $D06x) + 'Status: <word>'
    right-aligned at CARD_EDGE: led by blank glyphs ($7C 2 px, ' ' 3 px) for the pixel offset, $00.
    The label is the 26:575F inline entry (its own print is skipped in asm/vwf.asm)."""
    import json, text
    en = {int(e["addr"], 16): e["en"] for e in json.load(open(os.path.join(ROOT, "script", "fixtables.json")))
          if e["bank"] == 38}
    label = next(e["en"] for e in json.load(open(os.path.join(ROOT, "script", "inline.json")))
                 if e["bank"] == 38 and e["addr"] == "0x575f")
    out = bytearray()
    for a in CARD_STATUS:
        b = text.encode(label + " " + en[a])
        x = CARD_EDGE - sum(adv[c & 0x7F] for c in b)
        cell, p = divmod(x, 8)
        if p == 1:                       # no 1 px blank: start a cell earlier
            cell, p = cell - 1, 9
        pad = b"\x20" * (p % 2) + b"\x7c" * ((p - 3 * (p % 2)) // 2)
        assert sum(adv[c] for c in pad) == p and 8 <= cell <= 18, (en[a], x)
        rec = bytes([CARD_ROW + cell]) + pad + b + b"\x00"
        assert len(rec) <= 32, en[a]
        out += rec.ljust(32, b"\x00")
    return bytes(out)


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


SYM_OFF = 0x4000  # bank 1 $4000: symbol sheet (64 tiles, codes $C0-$FF) - monster panel "(n) m", automap digits


def patch_symbol_digits(rom):
    """Symbol-sheet digits ($F4-$FD) and the panel's parentheses ($CF/$D0) in the small VWF glyphs (owner's rule:
    the small font for numbers too): digits centred, '(' at the right edge of its tile, ')' at the left, so
    '(1)' reads tight across the three tiles."""
    f = font.load()
    def put(code, ch, align):
        adv, rows = f[ord(ch)]
        w = adv - 1
        x0 = {"c": (8 - w) // 2, "r": 8 - w, "l": 0}[align]
        o = SYM_OFF + (code - 0xC0) * 16
        rom[o:o + 16] = b"".join(bytes([(r >> x0) & 0xFF, 0xFF]) for r in rows)
    for i in range(10):
        put(0xF4 + i, str(i), "c")
    put(0xCF, "(", "r")
    put(0xD0, ")", "l")


AUTOMAP_OFF = 0x18 * 0x4000  # 18:4000: automap tile block (tile codes $80-$D7, BG data at $8800)


def patch_automap_labels(rom):
    """Automap labels in the small VWF glyphs (owner's decision 2026-11-12: the 0-15 axis digits stay 8 px).
    Tiles of the 18:4000 block: $CF 'B' (over the floor number; layouts 23:4D4A / 23:4FFD in asm/main.asm),
    warp panel (layout 23:4FF5): $CE $D1 $D3 = ワープ先 -> 'Warp', $D0 東 -> 'E', $D2 北 -> 'N' (right-aligned
    against the coordinate digit in the next tile)."""
    f = font.load()

    def strip(text):
        cols = []
        for ch in text:
            adv, rows = f[ord(ch)]
            for x in range(adv):
                cols.append([(r >> (7 - x)) & 1 if x < 8 else 0 for r in rows])
        return cols                       # list of columns, each 8 pixel rows

    def tiles(text, codes, align):
        cols = strip(text)
        while cols and not any(cols[-1]):
            cols.pop()                    # drop the trailing spacing column
        width = 8 * len(codes)
        pad = {"l": 1, "c": (width - len(cols)) // 2, "r": width - len(cols)}[align]
        cols = [[0] * 8] * pad + cols + [[0] * 8] * (width - pad - len(cols))
        for i, code in enumerate(codes):
            o = AUTOMAP_OFF + (code - 0x80) * 16
            tile = bytearray()
            for y in range(8):
                m = 0
                for x in range(8):
                    m |= cols[i * 8 + x][y] << (7 - x)
                tile += bytes([m, 0xFF])
            rom[o:o + 16] = tile

    tiles("B", [0xCF], "c")

    # cursor labels, table order of 23:5DB5 (JP: エレベーター かべ イベント のぼり/くだり かいだん まほう ふうじ
    # かいてん ゆか ワープ シュート ピット つりてんじょう らくばん どくへび いずみ みずうみ ダークゾーン), drawn at 23:7100
    # + 128 i as 8 tiles each (asm/main.asm AutoLabel copies one into tiles $90-$97)
    labels = ["Elevator", "Wall", "Event", "Stairs up", "Stairs down", "Magic seal", "Spinner", "Warp", "Chute",
              "Pit", "Ceiling trap", "Rockfall", "Viper", "Spring", "Lake", "Dark zone"]
    for i, text in enumerate(labels):
        cols = strip(text)
        assert len(cols) <= 64, text
        cols = cols + [[0] * 8] * (64 - len(cols))
        o = 0x23 * 0x4000 + 0x3100 + 128 * i
        data = bytearray()
        for k in range(8):
            for y in range(8):
                m = 0
                for x in range(8):
                    m |= cols[k * 8 + x][y] << (7 - x)
                data += bytes([m, 0xFF])
        assert all(b == 0 for b in rom[o:o + 128]), "23:7100 not free"
        rom[o:o + 128] = data
    tiles("Warp", [0xCE, 0xD1, 0xD3], "l")
    tiles("E", [0xD0], "r")
    tiles("N", [0xD2], "r")


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
    patch_symbol_digits(rom)
    patch_automap_labels(rom)
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
