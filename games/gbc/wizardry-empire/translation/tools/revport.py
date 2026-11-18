"""One-shot v1.0 -> Rev 1 migration of script/*.json addresses (2026-11-12), kept for the record.

Every address field is mapped with tools/revmap.py over the whole original block (rect incl. attributes,
message up to $FF, string up to $00), so an entry only moves when its Japanese bytes are identical in Rev 1.
Entries that do not map are left unchanged and listed in work/rev1/unmapped.json for manual work.
  python3 tools/revport.py [--dry]
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import revmap

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
V10 = open(revmap.V10, "rb").read()


def off(b, a):
    return a if a < 0x4000 else b * 0x4000 + a - 0x4000


def until(b, a, term, maxn=2000):
    o = off(b, a)
    n = 0
    while n < maxn and V10[o + n] != term:
        n += 1
    return n + 1


def mp(b, a, n):
    return revmap.map_addr(b, a, n)


def h(v):
    return "0x%04x" % v


def port(name, fn):
    p = os.path.join(ROOT, "script", name)
    raw = open(p, encoding="utf-8").read()
    data = json.loads(raw)
    bad = []
    for e in data:
        r = fn(e)
        if r:
            bad.append(r)
    one_per_line = raw.lstrip().startswith("[\n{") or raw.split("\n")[1].startswith("{")
    return p, data, bad, one_per_line


def rect(e):
    b, a = e["bank"], int(e["addr"], 16)
    n = 2 + e["w"] * e["h"] * (2 if e.get("attrs") else 1)
    m = mp(b, a, n) or (mp(b, a, 2 + e["w"] * e["h"]) if e.get("attrs") else None)
    if m is None:
        return ("rect", e["id"])
    e["addr"] = h(m)
    e["id"] = "%02x:%04x" % (b, m)


def msg(e):
    b, a = e["bank"], int(e["addr"], 16)
    m = mp(b, a, until(b, a, 0xFF))
    if m is None:
        return ("msg", "%02x:%04x" % (b, a))
    e["addr"] = h(m)


def plain(field, length):
    def f(e):
        b, a = e["bank"], int(e[field], 16)
        m = mp(b, a, length(e, b, a))
        if m is None:
            return (field, "%02x:%04x" % (b, a))
        e[field] = h(m)
    return f


def fixt(e):
    return plain("addr", lambda e, b, a: 4 if b == 42 else 5)(e)


REV1 = open(revmap.REV1, "rb").read()


def find_near(bank, pat, near, check=None):
    """Rev 1 address in `bank` of the byte pattern closest to `near` (optional check(addr))."""
    base = bank * 0x4000                      # file offset of the bank; CPU address = offset - base + $4000
    hits, i = [], REV1.find(pat, base, base + 0x4000)
    while i >= 0:
        a = i - base + 0x4000
        if check is None or check(i):
            hits.append(a)
        i = REV1.find(pat, i + 1, base + 0x4000)
    return min(hits, key=lambda a: abs(a - near)) if hits else None


def inline(e):
    return plain("addr", lambda e, b, a: e.get("len", 3))(e)


def chest(e):
    """site = ld a,lo ... ld a,hi (bank 37) for a bank-49 string at ptr: map the string, find the immediates."""
    p = int(e["ptr"], 16)
    m = mp(49, p, until(49, p, 0x00, 64))
    if m is None:
        return ("ptr", "31:%04x" % p)
    site = find_near(e["bank"], bytes([0x3E, m & 0xFF]), int(e["site"], 16),
                     lambda i: REV1[i + 5] == 0x3E and REV1[i + 6] == m >> 8)
    if site is None:
        return ("site", e["site"])
    e["ptr"], e["site"] = h(m), h(site)


def lst(bank):
    """Bank-49 strings (ptr) and, for lists.json, the table slot that points at them (found by value)."""
    def f(e):
        p = int(e["ptr"], 16)
        m = mp(49, p, until(49, p, 0x00, 64))
        if m is None:
            return ("ptr", "31:%04x" % p)
        if "table" in e:
            t = find_near(49, bytes([m & 0xFF, m >> 8]), int(e["table"], 16))
            if t is None:
                return ("table", e["table"])
            e["table"] = h(t)
        e["ptr"] = h(m)
    return f


def notice(e):
    return plain("site", lambda e, b, a: 8)(e)


def titles(e):
    return plain("addr", lambda e, b, a: 12)(e)


JOBS = [("rects.json", rect), ("messages.json", msg), ("fixtables.json", fixt), ("inline.json", inline),
        ("chests.json", chest), ("lists.json", lst(49)), ("lists50.json", lst(50)), ("notice.json", notice),
        ("titles.json", titles)]

if __name__ == "__main__":
    dry = "--dry" in sys.argv
    allbad = {}
    for name, fn in JOBS:
        p, data, bad, opl = port(name, fn)
        allbad[name] = bad
        print("%-15s %4d entries, %3d unmapped %s" % (name, len(data), len(bad), bad[:6]))
        if not dry:
            if opl:
                txt = "[\n" + ",\n".join(json.dumps(e, ensure_ascii=False) for e in data) + "\n]\n"
            else:
                txt = json.dumps(data, ensure_ascii=False, indent=1) + "\n"
            open(p, "w", encoding="utf-8").write(txt)
    os.makedirs(os.path.join(ROOT, "work", "rev1"), exist_ok=True)
    json.dump(allbad, open(os.path.join(ROOT, "work", "rev1", "unmapped.json"), "w"), indent=1)
