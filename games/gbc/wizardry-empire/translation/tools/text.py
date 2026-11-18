"""English text encoding for the VWF (tbl/en.tbl) and pixel measuring."""
import os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import font, tbl

_EN = None
_FONT = None
CTRL = {"x": 0xFC, "n": 0xFD, "end": 0xFF}


def en_table():
    global _EN
    if _EN is None:
        _EN = {v: k for k, v in tbl.load("en").items()}
    return _EN


def encode(s):
    """str -> bytes. '\\n' = $FD row break, {x:N} = $FC N (pixel x), {hh} = raw byte."""
    t = en_table()
    out = bytearray()
    i = 0
    while i < len(s):
        ch = s[i]
        if ch == "{":
            j = s.index("}", i)
            tok = s[i + 1:j]
            if tok.startswith("x:"):
                out += bytes([0xFC, int(tok[2:])])
            elif re.fullmatch(r"[0-9A-Fa-f]{2}", tok):
                out.append(int(tok, 16))
            else:
                raise ValueError("unknown token {%s} in %r" % (tok, s))
            i = j + 1
            continue
        if ch == "\n":
            out.append(0xFD)
        elif ch in t:
            out.append(t[ch])
        else:
            raise ValueError("no code for %r in %r" % (ch, s))
        i += 1
    return bytes(out)


def width(s):
    """Pixel width of a single row of plain text (no controls)."""
    global _FONT
    if _FONT is None:
        _FONT = font.load()
    w = 0
    bs = encode(s)
    i = 0
    while i < len(bs):
        b = bs[i]
        if b == 0xFC:
            w = max(w, bs[i + 1]); i += 2; continue
        if b in _FONT:
            w += _FONT[b][0]
        i += 1
    return w
