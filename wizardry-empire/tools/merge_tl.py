"""Merge a translation batch (python file defining T = {"BB:AAAA": [rows]}) into script/rects.json,
taking w/h/jp from build/rects_census.jsonl. Usage: merge_tl.py batch.py"""
import json, os, runpy, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
T = runpy.run_path(sys.argv[1])["T"]
census = {"%02x:%s" % (x["bank"], x["addr"][2:]): x for x in map(json.loads, open(os.path.join(ROOT, "build", "rects_census.jsonl")))}
path = os.path.join(ROOT, "script", "rects.json")
cur = {"%02x:%s" % (e["bank"], e["addr"][2:]): e for e in json.load(open(path, encoding="utf-8"))}
for k, rows in T.items():
    b, a = k.split(":")
    key = "%02x:%s" % (int(b), a)
    if key in census:
        c = census[key]
    else:  # not in the census (no direct reference): read the block from the ROM
        import tbl
        rom = open(os.path.join(ROOT, "rom", "wizardry_empire_j.gbc"), "rb").read()
        o = int(b) * 0x4000 + int(a, 16) - 0x4000
        w, h = rom[o], rom[o + 1]
        blk = rom[o + 2:o + 2 + w * h]
        c = {"bank": int(b), "addr": "0x" + a, "w": w, "h": h, "rows": [tbl.dec(blk[i:i + w]) for i in range(0, w * h, w)]}
    cur[key] = {"id": key, "bank": c["bank"], "addr": c["addr"], "w": c["w"], "h": c["h"],
                "jp": [r.rstrip() for r in c["rows"]], "en": rows}
out = sorted(cur.values(), key=lambda e: (e["bank"], e["addr"]))
with open(path, "w", encoding="utf-8") as f:
    f.write("[\n" + ",\n".join(json.dumps(e, ensure_ascii=False) for e in out) + "\n]\n")
print(len(out), "entries")
