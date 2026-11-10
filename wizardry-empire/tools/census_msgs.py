"""Find typewriter messages: code sites `ld a,LO / ld [$c1bf],a / ld a,HI / ld [$c1c0],a`.
The text bank comes from the nearest preceding `ld a,B / ld [$c1c1],a` (or `ld hl,$c1c1 / ld [hl],a`)
in the same bank, else the code's own bank. Prints JSON lines {bank, addr, sites, jp}."""
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import tbl

ROM = open(os.path.join(HERE, "..", "rom", "wizardry_empire_j.gbc"), "rb").read()
CTRL = {0xFD: "\n", 0xFA: "{FA}"}


def bank_bytes(b):
    return ROM[b * 0x4000:(b + 1) * 0x4000]


def decode_msg(bank, addr, limit=400):
    s = bank_bytes(bank)
    o = addr - (0x4000 if bank else 0)
    out = []
    i = o
    while i < len(s) and i - o < limit:
        c = s[i]
        if c == 0xFF:
            return "".join(out), i - o + 1
        if c == 0xFD:
            out.append("\n")
        elif c == 0xF4:
            out.append("{F4 %02X %02X}" % (s[i + 1], s[i + 2])); i += 2
        elif c == 0xF3:
            out.append("{F3 %02X %02X%02X}" % (s[i + 1], s[i + 3], s[i + 2])); i += 3
        elif c == 0xF8:
            out.append("{F8 %02X %02X %02X%02X}" % (s[i + 1], s[i + 2], s[i + 4], s[i + 3])); i += 4
        elif c in (0xFA, 0xFE, 0xFB, 0xF9, 0xF7, 0xF6, 0xFC, 0xF5):
            out.append("{%02X}" % c)
            if c in (0xF9, 0xF7):
                out.append("{%02X}" % s[i + 1]); i += 1
        else:
            out.append(tbl.dec(bytes([c])))
        i += 1
    return None, 0


HIRA = set(range(0x01, 0x20)) | {0x40} | set(range(0x5B, 0x61)) | set(range(0x7B, 0xA1))


def plaus(bank, addr):
    s = bank_bytes(bank)
    o = addr - 0x4000
    seg = []
    for c in s[o:o + 300]:
        if c == 0xFF:
            break
        seg.append(c)
    else:
        return 0
    if not seg:
        return 0
    txt = [c for c in seg if c < 0xF3]
    if not txt:
        return 0.1
    h = sum(c in HIRA for c in txt)
    sp = sum(c == 0x20 for c in txt)
    return (h + sp) / len(txt) if h >= 2 or len(txt) < 4 else 0


def guess_bank(addr, own):
    best, bb = plaus(own, addr), own
    for b in range(1, 64):
        p = plaus(b, addr)
        if p > best + 0.15:
            best, bb = p, b
    return bb


def sites():
    found = {}
    for b in range(64):
        s = bank_bytes(b)
        base = 0x4000 if b else 0
        for m in re.finditer(rb"\x3e(.)\xea\xbf\xc1\x3e(.)\xea\xc0\xc1", s, re.S):
            lo, hi = m.group(1)[0], m.group(2)[0]
            addr = lo | hi << 8
            # bank: look back up to 64 bytes for a c1c1 store
            back = s[max(0, m.start() - 64):m.start()]
            tb = None
            for mm in re.finditer(rb"\x3e(.)\xea\xc1\xc1|\x3e(.)\x21\xc1\xc1\x77", back, re.S):
                tb = (mm.group(1) or mm.group(2))[0]
            if tb is None:
                tb = guess_bank(addr, b)
            if addr < 0x4000:
                continue
            found.setdefault((tb, addr), []).append("%02x:%04x" % (b, base + m.start()))
    return found


if __name__ == "__main__":
    for (tb, addr), st in sorted(sites().items()):
        if tb >= 64:
            continue
        txt, ln = decode_msg(tb, addr)
        print(json.dumps({"bank": tb, "addr": "0x%04x" % addr, "len": ln, "sites": st, "jp": txt}, ensure_ascii=False))
