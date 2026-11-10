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


def load(name):
    p = os.path.join(ROOT, "script", name)
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else []


def insert_all(rom):
    space = Space(rom)
    stats = {}
    stats["rects"] = insert_rects(rom, space, load("rects.json"))
    stats["messages"] = insert_msgs(rom, space, load("messages.json"))
    stats["text space used"] = "bank $%02X + $%04X" % (space.bank, space.pos - 0x4000)
    return stats
