"""Address map from the Japanese v1.0 dump (rom/wizardry_empire_j_v10.gbc) to Rev 1 (rom/wizardry_empire_j.gbc).

Each 16 KB bank is aligned with difflib (matching blocks >= MIN bytes). map_addr(bank, addr) returns the Rev 1
address of the same byte, or None when the byte lies in a changed region. The map is cached in build/revmap.json.

  python3 tools/revmap.py BANK ADDR      # one lookup (hex or decimal)
"""
import difflib, json, os, sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
V10 = os.path.join(ROOT, "rom", "wizardry_empire_j_v10.gbc")     # the old base (v1.0, SHA-1 041c1251...)
REV1 = os.path.join(ROOT, "rom", "wizardry_empire_j.gbc")         # the base since 2026-11-12: Rev 1
CACHE = os.path.join(ROOT, "build", "revmap.json")
MIN = 8
_blocks = None


def _build():
    a, b = open(V10, "rb").read(), open(REV1, "rb").read()
    out = {}
    for bank in range(len(a) // 0x4000):
        A, B = a[bank * 0x4000:(bank + 1) * 0x4000], b[bank * 0x4000:(bank + 1) * 0x4000]
        if A == B:
            out[bank] = [[0, 0, 0x4000]]
            continue
        sm = difflib.SequenceMatcher(None, A, B, autojunk=False)
        out[bank] = [[m.a, m.b, m.size] for m in sm.get_matching_blocks() if m.size >= MIN]
    return out


def blocks():
    global _blocks
    if _blocks is None:
        if os.path.exists(CACHE) and os.path.getmtime(CACHE) > max(os.path.getmtime(V10), os.path.getmtime(REV1)):
            _blocks = {int(k): v for k, v in json.load(open(CACHE)).items()}
        else:
            _blocks = _build()
            os.makedirs(os.path.dirname(CACHE), exist_ok=True)
            json.dump(_blocks, open(CACHE, "w"))
    return _blocks


def map_addr(bank, addr, length=1):
    """v1.0 bank:addr (CPU address, $0000-$7FFF) -> Rev 1 address, or None if any of the `length` bytes changed."""
    off = addr if bank == 0 else addr - 0x4000
    for a0, b0, n in blocks()[bank]:
        if a0 <= off and off + length <= a0 + n:
            r = b0 + off - a0
            return r if bank == 0 else r + 0x4000
    return None


if __name__ == "__main__":
    b, a = (int(x, 0) for x in sys.argv[1:3])
    r = map_addr(b, a)
    print("%02X:%04X -> %s" % (b, a, "changed" if r is None else "%04X" % r))
