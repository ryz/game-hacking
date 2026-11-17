"""Find [w][h][w*h tiles] text blocks in the original ROM and the code/data that points at them.

Prints candidates as JSON lines. A block counts as text when most bytes are kana/latin/space and
there is at least one kana. References: 16-bit pointers to the block inside the same bank
(pointer tables or `ld hl/de/bc, nn`, or `ld a, lo / ldh [$b8] ... ld a, hi / ldh [$b9]`).
"""
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import tbl

ROM = open(os.path.join(HERE, "..", "rom", "wizardry_empire_j.gbc"), "rb").read()
KANA = set(range(0x01, 0x20)) | {0x22, 0x23, 0x24, 0x26, 0x27, 0x28, 0x29, 0x2C, 0x3C, 0x3D, 0x3E, 0x40} \
    | set(range(0x5B, 0x61)) | set(range(0x7B, 0xF0))
OK = KANA | {0x20, 0x21, 0x2A, 0x2B, 0x2D, 0x2E, 0x2F, 0x3A, 0x3F, 0xF0} | set(range(0x30, 0x3A)) \
    | set(range(0x41, 0x5B)) | set(range(0x61, 0x7B))


def score(blk, w):
    rows = [blk[i:i + w] for i in range(0, len(blk), w)]
    if not all(all(b in OK for b in r) for r in rows):
        return 0
    k = sum(b in KANA for b in blk)
    if k < 3:
        return 0
    nonsp = [b for b in blk if b != 0x20]
    if len(set(nonsp)) < max(3, len(nonsp) // 4):
        return 0
    small = sum(0x02 <= b <= 0x0A or 0xA7 <= b <= 0xAF for b in nonsp)
    if small > len(nonsp) * 0.25:
        return 0
    run = 1
    for a, b in zip(blk, blk[1:]):
        run = run + 1 if a == b and a != 0x20 else 1
        if run > 2 and a not in (0x2D, 0xB0, 0xF3):
            return 0
    for r in rows:  # a row must not start with a small kana / long-vowel mark
        t = r.lstrip(b" ")
        if t and (0x02 <= t[0] <= 0x0A or t[0] in (0xB0, 0xA1)):
            return 0
    return k / len(blk)


def refs(bank, addr):
    lo, hi = addr & 0xFF, addr >> 8
    s = ROM[bank * 0x4000:(bank + 1) * 0x4000] if bank else ROM[:0x4000]
    out = []
    for m in re.finditer(re.escape(bytes([lo, hi])), s):
        out.append(m.start())
    # split form: 3e lo e0 b8 ... 3e hi e0 b9
    for m in re.finditer(re.escape(bytes([0x3E, lo, 0xE0, 0xB8])), s):
        if bytes([0x3E, hi, 0xE0, 0xB9]) in s[m.start():m.start() + 12]:
            out.append(m.start() + 1)
    return out


def scan():
    res = []
    for bank in range(64):
        base = bank * 0x4000
        s = ROM[base:base + 0x4000]
        i = 0
        while i < len(s) - 4:
            w, h = s[i], s[i + 1]
            if 1 <= w <= 20 and 1 <= h <= 18 and w * h >= 2 and i + 2 + w * h <= len(s):
                blk = s[i + 2:i + 2 + w * h]
                sc = score(blk, w)
                if sc >= 0.25:
                    addr = (0x4000 if bank else 0) + i
                    r = refs(bank, addr)
                    if r:
                        res.append({"bank": bank, "addr": "0x%04x" % addr, "w": w, "h": h, "nref": len(r),
                                    "rows": [tbl.dec(blk[k:k + w]) for k in range(0, len(blk), w)]})
                        i += 2 + w * h
                        continue
            i += 1
    return res


if __name__ == "__main__":
    for r in scan():
        print(json.dumps(r, ensure_ascii=False))
