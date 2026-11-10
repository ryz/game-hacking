"""Insert translated text from script/*.json into the expanded ROM.

Rect blocks (script/rects.json): the original [w][h][w*h tiles]... block keeps its size and position;
its first 5 bytes become [w|$80][h][bank][ptr lo][ptr hi] pointing at the English rows
(rendered by the VWF, asm/vwf.asm VWF_Rect). Entries with an empty "en" are left untouched.
"""
import glob, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
sys.path.insert(0, HERE)
import text

FIRST_TEXT_BANK = 0x41
LAST_TEXT_BANK = 0x7F


class Space:
    """Bump allocator over the new banks (never crosses a bank boundary)."""

    def __init__(self, rom, first=FIRST_TEXT_BANK, last=LAST_TEXT_BANK):
        self.rom, self.bank, self.pos, self.last = rom, first, 0x4000, last

    def put(self, data):
        if self.pos + len(data) > 0x8000:
            self.bank += 1
            self.pos = 0x4000
            if self.bank > self.last:
                raise RuntimeError("out of text space")
        off = self.bank * 0x4000 + self.pos - 0x4000
        self.rom[off:off + len(data)] = data
        bank, addr = self.bank, self.pos
        self.pos += len(data)
        return bank, addr


def rom_off(bank, addr):
    return addr if addr < 0x4000 else bank * 0x4000 + addr - 0x4000


def layout_rows(entry):
    """List of English rows -> encoded bytes with alignment."""
    w_px = entry["w"] * 8
    rows = entry["en"] if isinstance(entry["en"], list) else entry["en"].split("\n")
    align = entry.get("align", "left")
    out = []
    for r in rows:
        a = align[len(out)] if isinstance(align, list) else align
        if r.startswith("^"):
            r, a = r[1:], "center"
        elif r.startswith(">"):
            r, a = r[1:], "right"
        import re as _re
        m = _re.match(r"@(\d+):", r)
        if m:  # place at the original cell column
            r = "{x:%d}" % (int(m.group(1)) * 8) + r[m.end():]
        pw = text.width(r)
        if pw > w_px:
            raise ValueError("%s: row %r is %d px, box is %d px" % (entry["id"], r, pw, w_px))
        pre = b""
        if a == "center" and pw < w_px:
            x = (w_px - pw) // 2
            if x:
                pre = bytes([0xFC, x])
        elif a == "right" and pw < w_px:
            pre = bytes([0xFC, w_px - pw])
        out.append(pre + text.encode(r))
    if len(out) > entry["h"]:
        raise ValueError("%s: %d rows, box has %d" % (entry["id"], len(out), entry["h"]))
    return b"\xfd".join(out) + b"\xff"


def insert_rects(rom, space, entries):
    n = 0
    for e in entries:
        if not e.get("en"):
            continue
        o = rom_off(e["bank"], int(e["addr"], 16))
        assert rom[o] == e["w"] and rom[o + 1] == e["h"], (e["id"], rom[o], rom[o + 1])
        if e["w"] * e["h"] < 3 or e.get("fixed"):
            # too small for the redirect header: ASCII in place, original fixed 8 px glyphs
            rows = e["en"]
            assert len(rows) <= e["h"] and all(len(r) <= e["w"] for r in rows), e["id"]
            data = b"".join(r.ljust(e["w"]).encode("ascii") for r in rows).ljust(e["w"] * e["h"], b" ")
            rom[o + 2:o + 2 + len(data)] = data
            n += 1
            continue
        b, a = space.put(layout_rows(e))
        rom[o:o + 5] = bytes([e["w"] | 0x80, e["h"], b, a & 0xFF, a >> 8])
        n += 1
    return n


def encode_msg(en):
    """Typewriter text: '\n' = $FD newline, {F8 ...}/{F3 ...}/{hh} raw bytes, ends with $FF."""
    import re
    out = bytearray()
    for part in re.split(r"(\{[^}]*\})", en):
        if part.startswith("{") and part.endswith("}"):
            tok = part[1:-1].split()
            if tok[0].startswith("col:"):  # move the typewriter to cell column N of this row
                out += bytes([0xF4, int(tok[0][4:]), 0xFF])
                continue
            if tok[0] in ("F3", "F4", "F8"):
                vals = []
                for t in tok[1:]:
                    v = int(t, 16)
                    if len(t) == 4:  # pointers are written big-endian in the script
                        vals += [v & 0xFF, v >> 8]
                    else:
                        vals.append(v)
                out += bytes([int(tok[0], 16)] + vals)
                continue
        if part:
            out += text.encode(part)
    return bytes(out) + b"\xff"


def check_msg_width(e, maxpx):
    import re
    plain = re.sub(r"\{F[38][^}]*\}", "WWWWWWWW", e["en"])  # names/numbers: assume 8 wide chars
    for line in plain.split("\n"):
        col = re.match(r"\{col:(\d+)\}", line)
        line = re.sub(r"\{[^}]*\}", "", line)
        if text.width(line) + (int(col.group(1)) * 8 if col else 0) > maxpx:
            raise ValueError("%s:%s line %r is %d px > %d" % (e["bank"], e["addr"], line, text.width(line), maxpx))


def insert_msgs(rom, space, entries):
    n = 0
    for e in entries:
        if not e.get("en"):
            continue
        o = rom_off(e["bank"], int(e["addr"], 16))
        check_msg_width(e, e.get("maxpx", 144))
        olen = rom.index(b"\xff", o) - o + 1
        if olen < 4 or e.get("inplace"):
            data = encode_msg(e["en"])
            if len(data) > olen:
                raise ValueError("%s:%s in-place text longer than the original (%d > %d)" % (e["bank"], e["addr"], len(data), olen))
            rom[o:o + len(data)] = data
            n += 1
            continue
        b, a = space.put(encode_msg(e["en"]))
        rom[o:o + 4] = bytes([0xF2, b, a & 0xFF, a >> 8])
        n += 1
    return n


ITEM_BANK, ITEM_SIZE, ITEM_NAME = 40, 40, 18


def insert_items(rom, entries):
    """Item names live in the 40-byte item records (bank 40), 18-byte $00-padded field: in place."""
    for e in entries:
        o = ITEM_BANK * 0x4000 + e["id"] * ITEM_SIZE
        data = text.encode(e["en"])
        assert len(data) < ITEM_NAME, e
        rom[o:o + ITEM_NAME] = data.ljust(ITEM_NAME, b"\x00")
    return len(entries)


MON_BANK, MON_BASE, MON_SIZE, MON_NAME, MON_FIELD = 57, 0x4840, 64, 0x20, 13


def insert_monsters(rom, entries):
    """Monster names: 64-byte records in bank 57, name at +$20, 12 chars + $00, in place."""
    for e in entries:
        o = MON_BANK * 0x4000 + MON_BASE - 0x4000 + e["id"] * MON_SIZE + MON_NAME
        data = text.encode(e["en"])
        assert len(data) <= MON_FIELD - 1, e
        rom[o:o + MON_FIELD] = data.ljust(MON_FIELD, b"\x00")
    return len(entries)


def insert_templates(rom, entries):
    """Default characters (bank 46, $80-byte records): 8-byte name field, in place."""
    for e in entries:
        o = 46 * 0x4000 + e["id"] * 0x80
        data = text.encode(e["en"])
        assert len(data) <= 7, e
        rom[o:o + 8] = data.ljust(8, b"\x00")
    return len(entries)


def insert_inline(rom, space, entries):
    """Text stored by straight-line code (ld a,X / ld [de],a / inc de or ld [hli],a runs):
    the whole run becomes rst $38 + db bank(|$80 for HL) + dw text, then a jr over the rest."""
    for e in entries:
        o = rom_off(e["bank"], int(e["addr"], 16))
        n = e["len"]
        assert n >= 4 and rom[o] == 0x3E, e
        b, a = space.put(text.encode(e["en"]) + b"\x00")
        code = bytes([0xFF, b | (0x80 if e["kind"] == "hli" else 0), a & 0xFF, a >> 8])
        rest = n - 4
        if rest >= 2:
            code += bytes([0x18, rest - 2]) + b"\x00" * (rest - 2)
        else:
            code += b"\x00" * rest
        rom[o:o + n] = code
        if e.get("hl"):
            assert rom[o - 3] == 0x21, e
            v = int(e["hl"], 16)
            rom[o - 2:o] = bytes([v & 0xFF, v >> 8])
    return len(entries)


FIX_RE = None


def fix_sites(rom):
    """Unrolled copies (ld a,[hli] / ld [de],a / inc de)* + ld a,[hl] / ld [de],a in the original banks."""
    import re
    out = []
    for m in re.finditer(rb"(?:\x2a\x12\x13)+\x7e\x12", bytes(rom[:0x100000])):
        n = (m.end() - m.start() - 2) // 3 + 1
        out.append((m.start(), m.end() - m.start(), n))
    return out


def insert_fix_sites(rom):
    for o, ln, n in fix_sites(rom):
        rom[o:o + ln] = (bytes([0xCD, 0, 0, n]) + b"\x00" * ln)[:ln]  # call target patched after asm
    return len(fix_sites_cache)


def fixmap_entries(space, rom):
    """(src bank, src addr) -> English, from translated rect rows (rects double as lookup tables)."""
    import re
    ents = []
    for e in load("rects.json"):
        if not e.get("en") or e.get("fixed") or e["w"] * e["h"] < 3:
            continue
        rows = e["en"] if isinstance(e["en"], list) else e["en"].split("\n")
        base = int(e["addr"], 16) + 2
        for r, row in enumerate(rows):
            row = re.sub(r"^[\^>]|^@\d+:", "", row)
            row = re.sub(r"\{x:\d+\}", " ", row)
            if not row.strip():
                continue
            b, a = space.put(text.encode(row) + b"\x00")
            ents.append((e["bank"], base + r * e["w"], b, a))
    return ents


def load(name):
    p = os.path.join(ROOT, "script", name)
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else []


def insert_all(rom):
    space = Space(rom)
    stats = {}
    stats["rects"] = insert_rects(rom, space, load("rects.json"))
    stats["messages"] = insert_msgs(rom, space, load("messages.json"))
    stats["items"] = insert_items(rom, load("items.json"))
    stats["monsters"] = insert_monsters(rom, load("monsters.json"))
    stats["templates"] = insert_templates(rom, load("templates.json"))
    stats["inline"] = insert_inline(rom, space, load("inline.json"))
    global fix_sites_cache, fixmap_cache
    fix_sites_cache = fix_sites(rom)
    fixmap_cache = fixmap_entries(space, rom)
    stats["fixed copies"] = len(fix_sites_cache)
    stats["text space used"] = "bank $%02X + $%04X" % (space.bank, space.pos - 0x4000)
    return stats


def post_asm(rom, sym):
    """Patch what needs assembled addresses: Stub_Fix calls and the FixMap contents."""
    tgt = sym["Stub_Fix"][1]
    for o, ln, n in fix_sites_cache:
        rom[o:o + ln] = (bytes([0xCD, tgt & 0xFF, tgt >> 8, n]) + b"\x00" * ln)[:ln]
    b, a = sym["FixMap"]
    o = b * 0x4000 + a - 0x4000
    assert len(fixmap_cache) <= 400
    data = b"".join(bytes([sb, sa & 0xFF, sa >> 8, tb, ta & 0xFF, ta >> 8]) for sb, sa, tb, ta in fixmap_cache)
    rom[o:o + len(data)] = data
    return len(fixmap_cache)
