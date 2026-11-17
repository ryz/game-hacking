"""Walk consecutive [w][h][w*h] blocks from known text rects; list untranslated ones (for curation)."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import tbl
ROOT = os.path.join(HERE, "..")
ROM = open(os.path.join(ROOT, "rom", "wizardry_empire_j.gbc"), "rb").read()


def chain(bank, start, stop):
    out, a = [], start
    while a < stop:
        o = bank * 0x4000 + a - 0x4000
        w, h = ROM[o], ROM[o + 1]
        if not (1 <= w <= 20 and 1 <= h <= 18):
            break
        blk = ROM[o + 2:o + 2 + w * h]
        out.append((a, w, h, [tbl.dec(blk[i:i + w]).rstrip() for i in range(0, w * h, w)]))
        a += 2 + w * h
    return out


if __name__ == "__main__":
    done = {(e["bank"], int(e["addr"], 16)) for e in json.load(open(os.path.join(ROOT, "script", "rects.json"), encoding="utf-8"))}
    seeds = sorted(done | {(int(k[:2], 16), int(k[3:], 16)) for k in sys.argv[1:]})
    seen = set()
    for b, a in seeds:
        for (aa, w, h, rows) in chain(b, a, 0x8000):
            if (b, aa) in seen:
                break
            seen.add((b, aa))
            if (b, aa) not in done:
                print('"%d:%04x": %dx%d  %s' % (b, aa, w, h, " | ".join(rows)))
