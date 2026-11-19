"""events.py MAP [REGEX]: an area's event scripts with the texts they show and a route that fires each.

  python3 games/dos/might-and-magic-2/tools/events.py 26 kalohn
  python3 games/dos/might-and-magic-2/tools/events.py 00 --dump        # raw scripts and the text list

Plays `@middlegate,WARP:MAP:08:08`, reads the event block at physical 16852 (DS:6052): the event table
(triples square y*16+x, event number, facing mask 80 N / 40 E / 20 S / 10 W, ended by 00 00 00), a 2-byte
length, the scripts (one per event number, each ended by FF) and the texts (ended by FF, '@' = line break).
Script opcodes seen (inferred from many scripts, not traced): 01/02/04/06 NN show text NN (1-based; 04 = sign),
07 wait for Space, 09 yes/no, 10/11 NN conditional jumps, 0C AA PP FF move to area AA square PP (y*16+x),
12 m1..m11 n start a fight with these monster ids (+n more of the first), 14 fight, 15 MM OO BB test record
byte OO+2 of member MM for bits BB, 18 MM OO AND OR change record byte OO+2 (Kalohn: 18 00 7F FD 02 sets
+0x81 bit 02), 22 Y1 Y2 century range test, 2B NN treasure level. Text references are guessed from those
opcodes, so a line may list a neighbouring text too.
"""
import os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "tools"))
CW = {"N": "FE", "E": "FS", "S": "FW", "W": "FN"}


def read(mp):
    import emu as E
    g = E.Game("dos/might-and-magic-2")
    m, rest, _ = E.start(g, "@middlegate" if mp == 0 else "@middlegate,WARP:%02X:08:08" % mp)
    for t in rest:
        E.step(m, g, t)
    d = bytes(m.peek(0x16852, 0x18620 - 0x16852))
    m.close()
    return d


def parse(d):
    i = 0
    while d[i:i + 3] != b"\0\0\0":
        i += 3
    ents = [(d[k] & 15, d[k] >> 4, d[k + 1], d[k + 2]) for k in range(0, i, 3)]
    j = i + 3
    ln = d[j] | d[j + 1] << 8
    scripts = d[j + 2:j + 2 + ln].split(b"\xff")
    texts = [t.decode("latin1").replace("@", " ") for t in d[j + 1 + ln:].split(b"\xff")]
    return ents, scripts, texts


def main():
    a = sys.argv[1:]
    mp = int(a[0], 16)
    rx = re.compile(a[1], re.I) if len(a) > 1 and a[1] != "--dump" else None
    ents, scripts, texts = parse(read(mp))
    if "--dump" in a:
        for n, s in enumerate(scripts):
            print("ev%02X %s" % (n, s.hex(" ")))
        for n, t in enumerate(texts[:120]):
            print("T%02X %s" % (n + 1, t[:150]))
        return
    for n, s in enumerate(scripts):
        refs = [texts[s[i + 1] - 1][:70] for i in range(len(s) - 1)
                if s[i] in (1, 2, 4, 6) and 1 <= s[i + 1] <= len(texts)]
        txt = " / ".join(refs)
        sq = [(x, y, m) for x, y, e, m in ents if e == n]
        if not sq or (rx and not rx.search(txt)):
            continue
        x, y, m = sq[0]
        d = [dd for bit, dd in ((0x80, "N"), (0x40, "E"), (0x20, "S"), (0x10, "W")) if m & bit][0]
        print("ev%02X %s %s | AT:%02X:%02X,%s,left,w250 | %s" % (n, [(p, q) for p, q, _ in sq][:6], d, x, y, CW[d], txt[:200]))


if __name__ == "__main__":
    main()
