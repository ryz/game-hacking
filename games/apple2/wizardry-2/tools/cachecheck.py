"""cachecheck.py [NAME ...]: every checkpoint from an empty cache against a cache hit (frames, memory, disks).

  python3 games/apple2/wizardry-2/tools/cachecheck.py            all checkpoints in checkpoints.txt (about 25 min)

Pass 1 moves work/cache/apple2/wizardry-2 aside and builds every checkpoint cold (each one replays its whole
route from power-on in its own process, four at a time). Pass 2 loads each from the new cache in a fresh
process. After `w60` both must give the same frame, the same main memory 0000-BFFF and the same written disk
images. If a cache from before exists it is compared too (pass 0), then removed. Prints one line per
checkpoint (hashes, then floor, square, each member's item numbers and awards) and writes the frame of each
checkpoint to work/scout/apple2/wizardry-2/cc_NAME.png for a look; exit 1 on any difference.
"""
import hashlib, os, shutil, sys
from multiprocessing import Pool
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "tools"))
CACHE = os.path.join(ROOT, "work", "cache", "apple2", "wizardry-2")


def probe(name):
    import emu as E
    g = E.Game("apple2/wizardry-2")
    try:
        m, rest, _ = E.start(g, "@" + name)
        E.step(m, g, "w60")
        f = hashlib.sha1(m.image().convert("RGB").tobytes()).hexdigest()[:10]
        r = hashlib.sha1(bytes(m.peek(0, 0xC000))).hexdigest()[:10]
        try:
            import io, zipfile
            z = m.battery(0)
            z = z if isinstance(z, (bytes, bytearray)) else open(z, "rb").read()
            zz = zipfile.ZipFile(io.BytesIO(z))
            d = hashlib.sha1(b"".join(zz.read(n) for n in sorted(zz.namelist()))).hexdigest()[:10]
        except Exception as e:
            d = "n/a:%s" % type(e).__name__
        info = []
        for n in range(6):
            b = 0x737E + n * 0xD0
            rec = bytes(m.peek(b, 0xD0))
            if not 0 < rec[0] < 16: continue
            cnt = min(rec[0x3A], 8)
            info.append("%s:%s%s" % (rec[1:1 + rec[0]].decode("latin1"), ",".join(str(rec[0x3C + 8 * i + 6]) for i in range(cnt)) or "-",
                        "".join(c for bit, c in ((0, ">"), (11, "K"), (14, "G")) if int.from_bytes(rec[0xCE:0xD0], "little") >> bit & 1)))
        pos = bytes(m.peek(0x730E, 8))
        info = "F%d (%d,%d) %s" % (pos[2], pos[6], pos[4], " ".join(info))
        m.save(os.path.join(ROOT, "work", "scout", "apple2", "wizardry-2", "cc_%s.png" % name)) if False else m.image().convert("RGB").resize((280, 192)).save(os.path.join(ROOT, "work", "scout", "apple2", "wizardry-2", "cc_%s.png" % name))
        m.close()
        return name, (f, r, d, info)
    except Exception as e:
        return name, ("ERROR %r" % (e,),)


def main():
    names = sys.argv[1:] or [l.split("|")[0].strip() for l in open(os.path.join(HERE, "..", "checkpoints.txt")) if l.strip() and not l.startswith("#")]
    old = None
    if os.path.isdir(CACHE):
        with Pool(4) as p: old = dict(p.map(probe, names, chunksize=1))
        shutil.rmtree(CACHE)
    with Pool(4) as p: cold = dict(p.map(probe, names, chunksize=1))
    with Pool(4) as p: hit = dict(p.map(probe, names, chunksize=1))
    bad = 0
    for n in names:
        ok = cold[n] == hit[n] and (old is None or old[n] == cold[n]) and not cold[n][0].startswith("ERROR")
        bad += not ok
        print("%-14s %s  cold %s  hit %s%s" % (n, "same" if ok else "DIFFERENT", " ".join(cold[n]), " ".join(hit[n]), "" if old is None else "  before %s" % " ".join(old[n])))
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
