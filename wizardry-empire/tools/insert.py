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

    def __init__(self, rom, first=FIRST_TEXT_BANK, last=LAST_TEXT_BANK, start=0x4000):
        self.rom, self.bank, self.pos, self.last = rom, first, start, last

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
        # 5-byte header must fit in the tile block, or (blocks with an attribute block, "attrs": true)
        # in tiles + attributes with the last attribute byte untouched
        room = e["w"] * e["h"] * (2 if e.get("attrs") else 1)
        if room < 3 + (1 if e.get("attrs") else 0) or e.get("fixed"):
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
    if e.get("autowrap"):  # wrapped at run time by {FA}: char-count look-ahead, never overflows with the VWF
        return
    plain = re.sub(r"\{F[38][^}]*\}", "WWWWWWWW", e["en"])  # names/numbers: assume 8 wide chars
    for line in plain.split("\n"):
        col = re.match(r"\{col:(\d+)\}", line)
        line = re.sub(r"\{[^}]*\}", "", line)
        if text.width(line) + (int(col.group(1)) * 8 if col else 0) > maxpx:
            raise ValueError("%s:%s line %r is %d px > %d" % (e["bank"], e["addr"], line, text.width(line), maxpx))


OPERANDS = {0xF3: 3, 0xF4: 2, 0xF8: 4, 0xF7: 1, 0xF9: 1, 0xF2: 3}


def msg_terminator(rom, o):
    """Offset of the $FF/$FC that ends the message starting at o (control-code operands skipped)."""
    i = o
    while True:
        c = rom[i]
        if c in (0xFF, 0xFC):
            return i
        i += 1 + OPERANDS.get(c, 0)


def insert_msgs(rom, space, entries, home=None):
    """Each original message start becomes $F2 bank lo hi -> English. The English ends with
    $F2 back to the original terminator ($FF or $FC), so the game itself ends/pauses the message
    in the original text bank ($C1C1) - required for $FC-chained segments (battle text, bank 49).
    `home` maps a bank to a Space inside that bank: its English stays in the same text bank, because
    {F3 ..} inserts read their string pointer from the current text bank (bank-49 battle verbs)."""
    home = home or {}
    n = 0
    for e in entries:
        if not e.get("en"):
            continue
        bank, o = e["bank"], rom_off(e["bank"], int(e["addr"], 16))
        check_msg_width(e, e.get("maxpx", 144))
        t = msg_terminator(rom, o)
        body = encode_msg(e["en"])[:-1]          # without the $FF
        if t - o < 4 or e.get("inplace"):
            data = body + bytes([rom[t]])
            if len(data) > t - o + 1:
                raise ValueError("%s:%s in-place text longer than the original (%d > %d)" % (bank, e["addr"], len(data), t - o + 1))
            rom[o:o + len(data)] = data
            n += 1
            continue
        ta = (t - bank * 0x4000 + 0x4000) if bank else t
        b, a = home.get(bank, space).put(body + bytes([0xF2, bank, ta & 0xFF, ta >> 8]))
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
    """Unrolled copies (ld a,[hli] / ld [de],a / inc de)* + ld a,[hl] / ld [de],a in the original banks
    whose source is a ROM table (text). Copies whose source is set by `ld hl,$8000+` just before are data
    (gold, EXP, HP between RAM buffers) and must stay untouched."""
    import re
    out = []
    data = bytes(rom[:0x100000])
    for m in re.finditer(rb"(?:\x2a\x12\x13)+\x7e\x12", data):
        if m.start() in SKIP_FIX_SITES:
            continue
        pre = data[m.start() - 8:m.start()]
        if any(pre[i] == 0x21 and pre[i + 2] >= 0x80 for i in range(len(pre) - 2)):
            continue
        n = (m.end() - m.start() - 2) // 3 + 1
        out.append((m.start(), m.end() - m.start(), n, b""))
    for bank, addr, ln, n, tail in EXTRA_FIX_SITES:
        out.append((rom_off(bank, addr), ln, n, tail))
    return out


# Text copies the pattern above misses: (bank, addr, bytes replaced, n chars).
# 38:5667 gender (2a 12 13 2a 12 13 2a 12: ends in ld a,[hli]; the next instruction reloads HL).
# Tail bytes follow the 4-byte call: Stub_Fix leaves HL at src+n-1, copies ending in ld a,[hli] leave src+n.
# 38:6111 class names in the create/class lists (6 x ld a,[hli]/ld [de],a; the loop needs HL = src+6).
EXTRA_FIX_SITES = [(38, 0x5667, 8, 3, b""), (38, 0x6111, 17, 6, b"\x23")]
# Matched by the pattern but not text: 2A:4A31 copies the element's attributes (handled in asm/main.asm).
SKIP_FIX_SITES = {42 * 0x4000 + 0x4A31 - 0x4000}


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
    for e in load("fixtables.json"):   # plain lookup tables (no rect header) read by Stub_Fix sites
        if e.get("en"):
            b, a = space.put(text.encode(e["en"]) + b"\x00")
            ents.append((e["bank"], int(e["addr"], 16), b, a))
    return ents


LIST_BANK, LIST_FREE = 49, 0x5726   # bank 49 $5726-$7FFF is unused (zeros) in the original


def insert_lists(rom, space, entries):
    """Bank-49 string table (49:55C3-5723, read with the text bank = 49, e.g. via {F3 31 C6E3}):
    English $00-terminated strings go into bank 49's free space and the table entries are repointed."""
    new = {}
    for e in entries:
        b, a = space.put(text.encode(e["en"]) + b"\x00")
        t = rom_off(LIST_BANK, int(e["table"], 16))
        assert rom[t] | rom[t + 1] << 8 == int(e["ptr"], 16), e
        rom[t:t + 2] = bytes([a & 0xFF, a >> 8])
        new[int(e["ptr"], 16)] = a
    for e in load("lists50.json"):          # strings only the bank-50 table points at (party-list statuses)
        b, a = space.put(text.encode(e["en"]) + b"\x00")
        new[int(e["ptr"], 16)] = a
    # bank 50 keeps its own copy of the command/status word pointers (32:57DB, 28 entries; the battle party
    # panel's action column reads it): repoint the entries that point at the same bank-49 strings
    o = rom_off(50, 0x57DB)
    for k in range(28):
        v = rom[o + 2 * k] | rom[o + 2 * k + 1] << 8
        if v in new:
            rom[o + 2 * k:o + 2 * k + 2] = bytes([new[v] & 0xFF, new[v] >> 8])
    return len(entries)


def insert_chests(rom, space, entries):
    """Chest names: bank-37 code loads a bank-49 string pointer as immediates
    (ld a,lo / ld [$C6E5],a / ld a,hi / ld [$C6E6],a) for {F3 31 C6E5} in 49:5277. English goes into
    bank-49 free space and both immediates are patched."""
    for e in entries:
        o = rom_off(e["bank"], int(e["site"], 16))
        p = int(e["ptr"], 16)
        assert rom[o] == 0x3E and rom[o + 1] == p & 0xFF and rom[o + 6] == p >> 8, e
        b, a = space.put(text.encode(e["en"]) + b"\x00")
        rom[o + 1], rom[o + 6] = a & 0xFF, a >> 8
    return len(entries)


def insert_titles(rom, space, entries):
    """Character titles: 12-byte records in bank 43 (14 classes x 10 tiers, table 2B:5F4F), copied by 2B:5FB8
    to a RAM rect at $C632 that is blitted with $1770. asm/main.asm NOPs out the [w=12][h=1] writes, so the
    record itself is the rect header: [$8C][$01][bank][ptr] -> English, right-aligned in 96 px."""
    seen = {}
    for e in entries:
        o = rom_off(e["bank"], int(e["addr"], 16))
        if e["en"] not in seen:
            seen[e["en"]] = space.put(layout_rows({"w": 12, "h": 1, "en": [">" + e["en"]]}))
        b, a = seen[e["en"]]
        rom[o:o + 5] = bytes([0x8C, 0x01, b, a & 0xFF, a >> 8])
    return len(entries)


NAME_LATIN, NAME_PAGES = 0x70C3, (0x6FDF, 0x7051)   # bank 38: Latin page, hiragana and katakana pages


def insert_name_charts(rom):
    """Name entry: 3 pages of 6 rects (17x1) in bank 38; the typed code is read from the chart and END works
    by position. The kana pages become copies of the Latin page ('・', a VWF slot now, -> apostrophe)."""
    o = rom_off(38, NAME_LATIN)
    latin = bytes(rom[o:o + 6 * 19]).replace(b"\xa5", b"'")
    for p in NAME_PAGES:
        q = rom_off(38, p)
        assert rom[q] == 17 and rom[q + 1] == 1
        rom[q:q + len(latin)] = latin
    rom[o:o + len(latin)] = latin
    # typed codes come from per-page tables (row*15 + col, $FF end): kana 85 entries, Latin 70
    lt = rom_off(38, 0x655D)
    codes = bytes(rom[lt:lt + 70]).replace(b"\xa5", b"'")
    rom[lt:lt + 70] = codes
    for t in (0x64B1, 0x6507):
        q = rom_off(38, t)
        assert rom[q + 85] == 0xFF
        rom[q:q + 86] = codes + b" " * 15 + b"\xff"
    return len(NAME_PAGES) + 1


SPELL_BANK, SPELL_BASE, SPELL_SIZE, SPELL_NAME = 36, 0x6C38, 16, 11
spell_names_cache = []


def insert_spells(rom, space, entries):
    """Spells: 16-byte records at 36:6C38, name = bytes 0-10 ($00-padded). The record gets a fallback name
    (<= 11 chars); the full English goes to text space and into SpellNames (VWF bank, filled in post_asm),
    which 0:24CF copies to wSpell for messages and the spell list."""
    global spell_names_cache
    spell_names_cache = [None] * 125
    for e in entries:
        o = rom_off(SPELL_BANK, SPELL_BASE) + e["id"] * SPELL_SIZE
        short = e.get("short", e["en"])[:SPELL_NAME]
        rom[o:o + SPELL_NAME] = text.encode(short).ljust(SPELL_NAME, b"\x00")[:SPELL_NAME]
        spell_names_cache[e["id"]] = space.put(text.encode(e["en"]) + b"\x00")
    return len(entries)


def load(name):
    p = os.path.join(ROOT, "script", name)
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else []


def insert_all(rom):
    space = Space(rom)
    stats = {}
    stats["rects"] = insert_rects(rom, space, load("rects.json"))
    b49 = Space(rom, LIST_BANK, LIST_BANK, LIST_FREE)
    stats["messages"] = insert_msgs(rom, space, load("messages.json"), {LIST_BANK: b49})
    stats["items"] = insert_items(rom, load("items.json"))
    stats["monsters"] = insert_monsters(rom, load("monsters.json"))
    stats["templates"] = insert_templates(rom, load("templates.json"))
    stats["lists"] = insert_lists(rom, b49, load("lists.json"))
    stats["chests"] = insert_chests(rom, b49, load("chests.json"))
    stats["titles"] = insert_titles(rom, space, load("titles.json"))
    stats["name charts"] = insert_name_charts(rom)
    stats["spells"] = insert_spells(rom, space, load("spells.json"))
    stats["bank 49 free used"] = "$%04X of $%04X" % (b49.pos - LIST_FREE, 0x8000 - LIST_FREE)
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
    for o, ln, n, tail in fix_sites_cache:
        rom[o:o + ln] = (bytes([0xCD, tgt & 0xFF, tgt >> 8, n]) + tail + b"\x00" * ln)[:ln]
    b, a = sym["FixMap"]
    o = b * 0x4000 + a - 0x4000
    assert len(fixmap_cache) <= 600
    data = b"".join(bytes([sb, sa & 0xFF, sa >> 8, tb, ta & 0xFF, ta >> 8]) for sb, sa, tb, ta in fixmap_cache)
    rom[o:o + len(data)] = data
    for n in load("notice.json"):
        b, a = sym["NoticeRows"]
        o = b * 0x4000 + a - 0x4000
        assert len(n["en"]) <= 8 and len(n["rows"]) == len(n["en"]) and n["col"] == 2
        for i, r in enumerate(n["rows"]):
            rom[o + i] = r
        b, a = sym["NoticeText"]
        o = b * 0x4000 + a - 0x4000
        for i, line in enumerate(n["en"]):
            d = text.encode(line) + b"\x00"
            assert len(d) <= 28 and text.width(line) <= 128, line
            rom[o + 28 * i:o + 28 * i + len(d)] = d
    b, a = sym["SpellNames"]
    o = b * 0x4000 + a - 0x4000
    for i, v in enumerate(spell_names_cache):
        if v:
            rom[o + 3 * i:o + 3 * i + 3] = bytes([v[0], v[1] & 0xFF, v[1] >> 8])
    return len(fixmap_cache)
