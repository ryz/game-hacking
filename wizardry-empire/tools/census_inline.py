"""Find text written by straight-line code, one character per instruction group:
  A: 3e xx 12 13   ld a,xx / ld [de],a / inc de
  B: 3e xx 22      ld a,xx / ld [hli],a
  C: 36 xx 23      ld [hl],xx / inc hl
Runs of >= 2 characters with at least one kana are reported (JSON lines)."""
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import tbl
from census_rects import KANA

ROM = open(os.path.join(HERE, "..", "rom", "wizardry_empire_j.gbc"), "rb").read()
PATS = {"de": (rb"(?:\x3e.\x12\x13)", 4), "hli": (rb"(?:\x3e.\x22)", 3), "hl": (rb"(?:\x36.\x23)", 3)}


def scan():
    out = []
    for b in range(64):
        s = ROM[b * 0x4000:(b + 1) * 0x4000]
        base = 0x4000 if b else 0
        for kind, (p, step) in PATS.items():
            for m in re.finditer(p + b"{2,}", s, re.S):
                chars = bytes(s[m.start() + 1 + i] for i in range(0, m.end() - m.start(), step))
                if sum(c in KANA for c in chars) < 1:
                    continue
                out.append({"bank": b, "addr": "0x%04x" % (base + m.start()), "kind": kind, "n": len(chars),
                            "jp": tbl.dec(chars)})
    return out


if __name__ == "__main__":
    for r in scan():
        print(json.dumps(r, ensure_ascii=False))
