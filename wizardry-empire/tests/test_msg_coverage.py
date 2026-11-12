"""every typewriter message the code can
point $C1BF/$C1C0 at must be a script/messages.json start (by ADDRESS), including $FC continuations."""
import json, os, re, sys
import pytest
ROOT = os.environ.get("WE_ROOT", os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import tbl
ROM = os.path.join(ROOT, "rom", "wizardry_empire_j.gbc")
MSGS = os.environ.get("WE_MSGS", os.path.join(ROOT, "script", "messages.json"))
pytestmark = pytest.mark.skipif(not os.path.exists(ROM), reason="original ROM not present")

TEXT_BANKS = (0x2D, 0x2E, 0x31)
# 19 `ld [$c1bf],a` that are not `ld a,lo / ld [$c1bf],a / ld a,hi / ld [$c1c0],a`: typewriter-internal saves,
# pointer-table reads (tables in PTR_TABLES) and the HRAM $CE/$CF path. A new one must be classified here.
INDIRECT_SITES = {"00:1E4F", "00:1E87", "00:1EFD",                      # $FC / $FD / $FB: save current pointer
                  "24:51A8", "24:51BE", "24:51D4", "2A:4AB2", "2D:6783", "2D:679F", "2D:67BB", "2D:6858",
                  "2D:7724", "2D:7A13", "32:43E6", "32:4872", "32:4D89", "32:5265",       # tables
                  "24:7908", "24:7986"}                                                     # ldh a,[$ce]/[$cf]
# (code bank, table, text bank, stride, entries): walked to the first entry outside the text, see msgcov.md
PTR_TABLES = [(0x24, 0x50DE, 0x31, 2, 7), (0x2A, 0x76D0, 0x2E, 2, 110), (0x2D, 0x66C5, 0x2D, 2, 32),
              (0x2D, 0x763B, 0x2D, 2, 5), (0x2D, 0x79C9, 0x2D, 3, 12), (0x32, 0x58D6, 0x31, 2, 4),
              (0x32, 0x59CE, 0x31, 2, 4)]
DEBUG = {(0x2D, 0x624A), (0x2D, 0x62BB)}            # debug-mode help, intentionally Japanese
NOT_PRINTED = {(0x31, 0x45AA)}                      # typewriter init default (22:4452 ...), never printed
UNREFERENCED = {(0x31, a) for a in (0x4C9C, 0x4CB3, 0x4CCA, 0x4CE3, 0x4CFC)}   # test strings after 49:4C87
OPER = {0xF3: 3, 0xF4: 2, 0xF8: 4, 0xF7: 1, 0xF9: 1}


def off(b, a):
    return b * 0x4000 + a - 0x4000 if a >= 0x4000 else a


def ba(o):
    return o // 0x4000, o % 0x4000 + (0x4000 if o >= 0x4000 else 0)


def segment(rom, b, a):
    """bytes of the segment at b:a without operands, terminator offset, terminator."""
    i, txt = off(b, a), []
    while rom[i] not in (0xFF, 0xFC):
        txt.append(rom[i]) if rom[i] < 0xF0 else None
        i += 1 + OPER.get(rom[i], 0)
    return bytes(txt), i, rom[i]


def has_japanese(txt):
    return 0 not in txt and any(ord(ch) >= 0x3000 for ch in tbl.dec(txt))   # $00 = name list, not a message


SETTER = re.compile(rb"\x3e([\x2d\x2e\x31])(?:\xea\xc1\xc1|\x21\xc1\xc1\x77)|\xcd\x8d\x27", re.S)


def text_bank(rom, o):
    """$C1C1 at a pointer store: a `ld a,B -> [$C1C1]` up to 16 bytes after the pair, else the nearest one or a
    `call $278D` (window open, sets $31) up to $180 bytes before, else $31 (the window opens' default)."""
    m = re.compile(rb"\x3e([\x2d\x2e\x31])(?:\xea\xc1\xc1|\x21\xc1\xc1\x77)", re.S).search(rom, o + 8, o + 24)
    if m:
        return m.group(1)[0]
    last = None
    for last in SETTER.finditer(rom, max(o - 0x180, o // 0x4000 * 0x4000), o):
        pass
    return last.group(1)[0] if last and last.group(1) else 0x31


def message_roots(rom):
    roots, indirect = {}, set()
    for m in re.finditer(rb"\xea\xbf\xc1", rom):
        o = m.start()
        if rom[o - 2] == 0x3E and rom[o + 3] == 0x3E and rom[o + 5:o + 8] == b"\xea\xc0\xc1":
            ptr = rom[o - 1] | rom[o + 4] << 8
            roots.setdefault((text_bank(rom, o), ptr), []).append("%02X:%04X" % ba(o - 2))
        else:
            indirect.add("%02X:%04X" % ba(o))
    for m in re.finditer(rb"\x3e(.)\xe0\xce\x3e(.)\xe0\xcf", rom[0x24 * 0x4000:0x25 * 0x4000], re.S):
        roots.setdefault((0x31, m.group(1)[0] | m.group(2)[0] << 8), []).append("24:%04X" % (0x4000 + m.start()))
    for cb, t, tb, stride, n in PTR_TABLES:
        for i in range(n):
            o = off(cb, t + stride * i)
            roots.setdefault((tb, rom[o] | rom[o + 1] << 8), []).append("%02X:%04X[%d]" % (cb, t, i))
    return roots, indirect


def test_every_message_pointer_is_in_script():
    rom = open(ROM, "rb").read()[:0x100000]
    msgs = json.load(open(MSGS, encoding="utf-8"))
    starts = {(e["bank"], int(e["addr"], 16)) for e in msgs}
    roots, indirect = message_roots(rom)
    assert indirect <= INDIRECT_SITES, "unclassified $C1BF stores: %s" % sorted(indirect - INDIRECT_SITES)
    problems = []
    todo = [(b, a, "%s" % ",".join(h[:2])) for (b, a), h in roots.items()]
    todo += [(b, a, "script") for b, a in starts]
    seen = set()
    while todo:
        b, a, how = todo.pop()
        if (b, a) in seen or (b, a) in DEBUG | NOT_PRINTED | UNREFERENCED:
            continue
        seen.add((b, a))
        txt, t, term = segment(rom, b, a)
        if (b, a) not in starts and how != "script" and has_japanese(txt):
            problems.append("%d:%04X (%s) %s" % (b, a, how, tbl.dec(txt)[:20]))
        if term == 0xFC and ((b, a) in starts or how != "script"):     # the typewriter goes on after a $FC pause
            todo.append((b, ba(t + 1)[1], "$FC after %d:%04X" % (b, a)))
    assert not problems, "messages missing from messages.json: " + "; ".join(sorted(problems))
