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
        pw = text.width(r)
        if pw > w_px:
            raise ValueError("%s: row %r is %d px, box is %d px" % (entry["id"], r, pw, w_px))
        a = align[len(out)] if isinstance(align, list) else align
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
        assert e["w"] * e["h"] >= 3, e["id"]
        b, a = space.put(layout_rows(e))
        rom[o:o + 5] = bytes([e["w"] | 0x80, e["h"], b, a & 0xFF, a >> 8])
        n += 1
    return n


def load(name):
    p = os.path.join(ROOT, "script", name)
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else []


def insert_all(rom):
    space = Space(rom)
    stats = {}
    stats["rects"] = insert_rects(rom, space, load("rects.json"))
    stats["text space used"] = "bank $%02X + $%04X" % (space.bank, space.pos - 0x4000)
    return stats
