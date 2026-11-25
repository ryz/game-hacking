# Usage: python3 games/dos/doom/tools/dpick.py PLANFILE ID K NEWID CATEGORY CAPTION (K = the K-th ? mark, 0 = final frame)
import sys
# usage: pick.py PLANFILE ID K NEWID CATEGORY CAPTION   (K = 0 for the final frame)
f, sid, k, nid, cat, cap = sys.argv[1:7]
for l in open(f):
    p = [x.strip() for x in l.split("|")]
    if p[0] != sid: continue
    toks = p[3].split(",")
    out = []; n = 0
    for t in toks:
        if t == "?":
            n += 1
            if n == int(k): break
            continue
        if t == "!": continue
        out.append(t)
    print("%s | %s | %s | %s,!" % (nid, cat, cap, ",".join(out)))
