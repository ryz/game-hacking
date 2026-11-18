#!/usr/bin/env python3
"""Return-spell (password) helper for Dragon Quest (Famicom) with the English patch.

The patch keeps the Japanese 64-symbol password grid cell for cell, only the glyphs differ:

    JP grid                EN grid (this ROM)        notation used here for the EN grid
    あいうえお まみむめも    [6 icons] Y Z a b c       r s t u v  Y Z a b c   (r s t u v = the five item icons)
    かきくけこ がぎぐげご    [icon] A B C D 0 1 2 3 4   w A B C D  0 1 2 3 4   (w = the ring-like icon)
    さしすせそ ざじずぜぞ    E F G H I 5 6 7 8 9       E F G H I  5 6 7 8 9
    たちつてと だぢづでど    J K L M N ? ! * , :       J K L M N  ? ! * , :
    なにぬねの らりるれろ    O P Q R S g h i j k       O P Q R S  g h i j k
    はひふへほ ばびぶべぼ    T U V W X m n o p q       T U V W X  m n o p q
    やゆよわ もどる すすむ おわり   d e f l Bok Frw End   d e f l

  pw.py tokens PASSWORD   -> play.py/emu.py tokens that type it (cursor must be on the top-left cell, as on entry)
  pw.py en KANA           -> the same password in EN-grid notation
  pw.py jp ENPASSWORD     -> the same password in kana
PASSWORD may be kana or EN notation; spaces are ignored. 20 symbols.
"""
import sys

JP = ["あいうえおまみむめも", "かきくけこがぎぐげご", "さしすせそざじずぜぞ", "たちつてとだぢづでど",
      "なにぬねのらりるれろ", "はひふへほばびぶべぼ", "やゆよわ"]
EN = ["rstuvYZabc", "wABCD01234", "EFGHI56789", "JKLMN?!*,:", "OPQRSghijk", "TUVWXmnopq", "defl"]
POS = {}
for grid in (JP, EN):
    for r, row in enumerate(grid):
        for c, ch in enumerate(row):
            POS[ch] = (r, c)


def clean(s):
    return [ch for ch in s if not ch.isspace() and ch != "　"]


def tokens(pw, end=True):
    r = c = 0
    out = []
    for ch in clean(pw):
        tr, tc = POS[ch]
        mv = []
        dv = (["down"] * (tr - r)) if tr > r else (["up"] * (r - tr))
        dh = (["right"] * (tc - c)) if tc > c else (["left"] * (c - tc))
        # row 6 has only 4 symbol cells: enter it vertically in the right column, leave it vertically first
        mv = dv + dh if r == 6 else dh + dv
        out += mv + ["a"]
        r, c = tr, tc
    return ",".join(out)


def conv(pw, src, dst):
    flat_s = "".join(src); flat_d = "".join(dst)
    return "".join(flat_d[flat_s.index(ch)] if ch in flat_s else ch for ch in pw)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    cmd, pw = sys.argv[1], " ".join(sys.argv[2:])
    if cmd == "tokens":
        print(tokens(pw))
    elif cmd == "en":
        print(conv(pw, JP, EN))
    elif cmd == "jp":
        print(conv(pw, EN, JP))
    else:
        sys.exit(__doc__)
