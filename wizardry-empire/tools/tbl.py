"""Load tbl/*.tbl files and decode bytes for inspection."""
import os
HERE = os.path.dirname(os.path.abspath(__file__))


def load(name="jp"):
    t = {}
    for line in open(os.path.join(HERE, "..", "tbl", name + ".tbl"), encoding="utf-8"):
        line = line.rstrip("\n")
        if not line or line.startswith("#"):
            continue
        k, v = line.split("=", 1)
        t[int(k, 16)] = v
    return t


JP = None


def dec(bs, ctrl=None):
    global JP
    if JP is None:
        JP = load("jp")
    return "".join((ctrl or {}).get(b) or JP.get(b, "{%02X}" % b) for b in bs)
