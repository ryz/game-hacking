"""Rebuild every checkpoint with an empty cache and compare frame and written disk with a cache hit.
Run: python3 games/dos/ultima-2/tools/cachecheck.py (about 3 min). Also: Q (save) after cache hits of `fight`, `ring` (after the planet X trip) and `earth_2112` vs the same keys
from power-on (whole chain expanded, no checkpoint)."""
import os, sys, shutil, hashlib
ROOT = "/home/user/game-hacking"
sys.path.insert(0, os.path.join(ROOT, "tools"))
os.chdir(ROOT)
import emu as E

g = E.Game("dos/ultima-2")
CACHE = os.path.join(ROOT, "work", "cache", "dos", "ultima-2")
CP = {}
for l in open("games/dos/ultima-2/checkpoints.txt"):
    if l.strip() and not l.startswith("#"):
        p = [x.strip() for x in l.split("|")]
        CP[p[0]] = p[-1]

def expand(route):
    t = route.split(",", 1)
    if t[0].startswith("@"):
        return expand(CP[t[0][1:]]) + ("," + t[1] if len(t) > 1 else "")
    return route

def run(route, cache=True):
    m, rest, _ = E.start(g, route, cache=cache)
    for t in rest:
        E.step(m, g, t)
    img = m.image().convert("RGB").tobytes()
    files = m._files(m._disk())
    m.close()
    return hashlib.sha1(img).hexdigest()[:12], {k: hashlib.sha1(v).hexdigest()[:8] for k, v in files.items() if not k.endswith("/")}

names = list(CP)
extra = {"q_fight": "@fight,q,w300", "q_ring": "@ring,LEAVE,q,w300", "q_earth": "@earth_2112,q,w300"}
hit = {n: run("@%s,w2" % n) for n in names}
for k, r in extra.items():
    hit[k] = run(r)
bak = CACHE + ".bak"
if os.path.exists(bak):
    shutil.rmtree(bak)
if os.path.exists(CACHE):
    shutil.move(CACHE, bak)
miss = {n: run("@%s,w2" % n) for n in names}
for k, r in extra.items():
    miss[k] = run(expand(r), cache=False)
ok = True
for n in names + list(extra):
    same = hit[n] == miss[n]
    ok &= same
    print("%-14s %s  hit %s  miss %s" % (n, "same" if same else "DIFFERENT", hit[n], miss[n]))
print("ALL OK" if ok else "MISMATCH")
