"""shops.py [--castles]: enter every town (or castle) from checkpoint `mid` and print where to stand for each shop.

  python3 games/dos/ultima/tools/shops.py

For each place: id, name, map number (RAM 19C92) and one customer-side square next to a counter per shop kind
(`TPOS2:x:y`, then `t,w100,b,w100`). Read from the town map buffer 17AFE + n*0x2AC (column-major, x*18 + y);
shop floor squares 3E transport, 36 armour, 3A weapons, 38 food, 3C magic, 3D pub; counters 0B-10. In castles
the 3C/3D squares are prison cells, not shops. Capture 2026-11-19: towns n, n+8, n+16, n+24 share a plan.
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "tools")); sys.path.insert(0, HERE)
from multiprocessing import Pool
import worldmap as W
SHOP = {0x3e: "transport", 0x36: "armour", 0x3a: "weapons", 0x38: "food", 0x3c: "magic", 0x3d: "pub"}

def run(job):
    import emu as E
    i, x, y, n = job
    g = E.Game("dos/ultima")
    m, rest, _ = E.start(g, "@mid,GO:%02X:%02X" % (x, y))
    for t in rest:
        E.step(m, g, t)
    lv = m.peek(0x19C92, 1)[0]
    b = bytes(m.peek(0x17AFE + lv * 0x2AC, 0x2AC)); m.close()
    out = {}
    for tx in range(1, 37):
        for ty in range(1, 17):
            v = b[tx * 18 + ty]
            near = [b[(tx + dx) * 18 + ty + dy] for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))]
            if v in SHOP and any(0x0b <= c <= 0x10 for c in near):
                out.setdefault(SHOP[v], "%02X:%02X" % (tx, ty))
    return i, n, lv, out

if __name__ == "__main__":
    names = W.names()
    jobs = names[32:40] if "--castles" in sys.argv else names[:32]
    with Pool(4) as p:
        for r in p.map(run, jobs):
            print(json.dumps(r))
