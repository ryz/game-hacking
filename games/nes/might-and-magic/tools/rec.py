"""Character-record poke builder for Might and Magic (NES).

Records: $6F00 + $80*slot (slot 0 = hero, 1-15 = fellows), check byte +$7F = sum(+$00..+$7E) mod 256.
Reads a RAM dump made by `play.py --name S dump NAME` (work/play/S/dump_NAME.json), applies field changes and
prints `poke:` tokens (changed bytes + the fixed check byte) to paste into a route.

  python3 games/nes/might-and-magic/tools/rec.py work/play/mm/dump_x.json SLOT field=value [field=value ...]

Fields (little-endian numbers; verified on the View pages unless noted):
  lev (+$13 current, +$14 max)      exp (+$17..+$19)            mp (+$1B/+$1C current, +$1D/+$1E max)
  splev (+$1F/+$20 spell level)     hp (+$23/+$24 current, +$25/+$26 max, +$27/+$28 base)
  gold (+$29..+$2B)                 gems (+$21/+$22)            food (+$2F)
  int mig per end spe acc luc (stat pairs +$05..+$12, current and max set together)
  age (+$15)                        byte:OFF=HEX (raw byte, OFF in hex)
"""
import json, sys

STATS = ["int", "mig", "per", "end", "spe", "acc", "luc"]


def le(v, n):
    return [(v >> (8 * i)) & 0xFF for i in range(n)]


def build(rec, changes):
    r = list(rec)
    for c in changes:
        k, v = c.split("=", 1)
        if k.startswith("byte:"):
            r[int(k[5:], 16)] = int(v, 16)
            continue
        n = int(v)
        if k == "lev":
            r[0x13] = r[0x14] = n
        elif k == "exp":
            r[0x17:0x1A] = le(n, 3)
        elif k == "mp":
            r[0x1B:0x1D] = le(n, 2); r[0x1D:0x1F] = le(n, 2)
        elif k == "splev":
            r[0x1F] = r[0x20] = n
        elif k == "hp":
            r[0x23:0x25] = le(n, 2); r[0x25:0x27] = le(n, 2); r[0x27:0x29] = le(n, 2)
        elif k == "gold":
            r[0x29:0x2C] = le(n, 3)
        elif k == "gems":
            r[0x21:0x23] = le(n, 2)
        elif k == "food":
            r[0x2F] = n
        elif k == "age":
            r[0x15] = n
        elif k in STATS:
            i = 5 + 2 * STATS.index(k)
            r[i] = r[i + 1] = n
        else:
            raise SystemExit("unknown field " + k)
    r[0x7F] = sum(r[:0x7F]) & 0xFF
    return r


def tokens(base, old, new):
    out, i = [], 0
    while i < 128:
        if old[i] != new[i]:
            j = i
            while j < 128 and old[j] != new[j]:
                j += 1
            out.append("poke:%04X=%s" % (base + i, "".join("%02X" % b for b in new[i:j])))
            i = j
        else:
            i += 1
    return out


def main():
    d = json.load(open(sys.argv[1]))
    slot = int(sys.argv[2])
    base = 0x6F00 + 0x80 * slot
    old = [d.get("%04X" % (base + i), d.get("%04x" % (base + i), 0)) for i in range(128)]
    new = build(old, sys.argv[3:])
    print(",".join(tokens(base, old, new)))


if __name__ == "__main__":
    main()
