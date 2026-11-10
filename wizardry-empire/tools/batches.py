"""Translation batches for the translator/reviewer agents.

  python3 tools/batches.py split msg  NAME --bank 45 [--start 0x4000 --end 0x8000]   untranslated messages
  python3 tools/batches.py split rect NAME --seed 38:6f25 [--seed ...]                untranslated rect chains
  python3 tools/batches.py check NAME     validate work/tl/NAME.json (every entry needs "en")
  python3 tools/batches.py pairs NAME     work/tl/NAME.pairs.txt for the reviewer
  python3 tools/batches.py merge NAME     copy into script/messages.json / script/rects.json

Batch file work/tl/NAME.json: a list of entries
  {"key": "45:4466", "kind": "msg", "jp": "...", "maxpx": 144, "en": ""}
  {"key": "38:6f25", "kind": "rect", "w": 7, "h": 1, "jp": ["row", ...], "en": []}
The checks are the build's own (tools/insert.py), so a batch that passes `check` builds.
"""
import argparse, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
sys.path.insert(0, HERE)
import census_msgs, chain_rects, insert, text  # noqa: E402

TL = os.path.join(ROOT, "work", "tl")
TOKEN = re.compile(r"\{F[38][^}]*\}")


def path(name, ext=".json"):
    return os.path.join(TL, name + ext)


def done_keys(fname):
    p = os.path.join(ROOT, "script", fname)
    if not os.path.exists(p):
        return set()
    return {"%d:%s" % (e["bank"], e["addr"][2:].lower()) for e in json.load(open(p, encoding="utf-8"))}


def split_msg(name, bank, start, end):
    done = done_keys("messages.json")
    s = census_msgs.bank_bytes(bank)
    starts = sorted({0x4000 + i + 1 for i, x in enumerate(s) if x == 0xFF} | {0x4000})
    out = []
    for a in starts:
        if not start <= a < end:
            continue
        key = "%d:%04x" % (bank, a)
        if key in done:
            continue
        jp, ln = census_msgs.decode_msg(bank, a)
        if not jp or ln < 3 or "□" in jp or not re.search(r"[぀-ヿ]", jp):
            continue
        out.append({"key": key, "kind": "msg", "jp": jp, "maxpx": 144, "en": ""})
    return out


def split_rect(name, seeds):
    done = done_keys("rects.json")
    out = []
    banks = {int(sd.split(":")[0]) for sd in seeds}
    # every translated rect in the same bank also starts a chain (blocks come in several runs)
    seeds = list(seeds) + sorted(k for k in done if int(k.split(":")[0]) in banks)
    for sd in seeds:
        b, a = sd.split(":")
        for (aa, w, h, rows) in chain_rects.chain(int(b), int(a, 16), 0x8000):
            key = "%d:%04x" % (int(b), aa)
            if key in done or any(e["key"] == key for e in out):
                continue
            out.append({"key": key, "kind": "rect", "w": w, "h": h, "jp": rows, "en": []})
    return out


def check_entry(e):
    """Returns a list of error strings."""
    errs = []
    if not e.get("en"):
        return ["%s: no English" % e["key"]]
    b, a = e["key"].split(":")
    if e["kind"] == "rect":
        ent = {"id": e["key"], "w": e["w"], "h": e["h"], "en": e["en"]}
        try:
            insert.layout_rows(ent)
        except (ValueError, KeyError) as x:
            errs.append(str(x))
    else:
        jt = sorted(TOKEN.findall(e["jp"]))
        et = sorted(TOKEN.findall(e["en"]))
        if jt != et:
            errs.append("%s: insert codes differ: jp %s en %s" % (e["key"], jt, et))
        try:
            insert.check_msg_width({"bank": b, "addr": a, "en": e["en"]}, e.get("maxpx", 144))
            insert.encode_msg(e["en"])
        except ValueError as x:
            errs.append(str(x))
        if ("はい" in e["jp"]) != ("Yes" in e["en"]):
            errs.append("%s: Yes/No choice must be kept ({col:N}Yes / {col:N}No)" % e["key"])
    if re.search(r"[぀-ヿ＀-￯]", json.dumps(e["en"], ensure_ascii=False)):
        errs.append("%s: Japanese/fullwidth characters in the English" % e["key"])
    return errs


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", choices=["split", "check", "pairs", "merge"])
    ap.add_argument("a1")
    ap.add_argument("a2", nargs="?")
    ap.add_argument("--bank", type=int)
    ap.add_argument("--start", default="0x4000")
    ap.add_argument("--end", default="0x8000")
    ap.add_argument("--seed", action="append", default=[])
    o = ap.parse_args()
    os.makedirs(TL, exist_ok=True)
    if o.cmd == "split":
        kind, name = o.a1, o.a2
        ents = split_msg(name, o.bank, int(o.start, 16), int(o.end, 16)) if kind == "msg" else split_rect(name, o.seed)
        with open(path(name), "w", encoding="utf-8") as f:
            f.write("[\n" + ",\n".join(json.dumps(e, ensure_ascii=False) for e in ents) + "\n]\n")
        print("%d entries -> %s" % (len(ents), os.path.relpath(path(name), ROOT)))
        return
    name = o.a1
    ents = json.load(open(path(name), encoding="utf-8"))
    if o.cmd == "check":
        errs = [x for e in ents for x in check_entry(e)]
        print("\n".join("ERROR " + x for x in errs) if errs else "OK (%d entries)" % len(ents))
        sys.exit(1 if errs else 0)
    if o.cmd == "pairs":
        with open(path(name, ".pairs.txt"), "w", encoding="utf-8") as f:
            for e in ents:
                jp = e["jp"] if isinstance(e["jp"], str) else " | ".join(e["jp"])
                en = e["en"] if isinstance(e["en"], str) else " | ".join(e["en"])
                f.write(">> %s [%s]\nJP: %s\nEN: %s\n\n" % (e["key"], e["kind"], jp.replace("\n", " / "), en.replace("\n", " / ")))
        print(os.path.relpath(path(name, ".pairs.txt"), ROOT))
        return
    if o.cmd == "merge":
        errs = [x for e in ents for x in check_entry(e)]
        if errs:
            sys.exit("\n".join(errs))
        for fname, kind in (("messages.json", "msg"), ("rects.json", "rect")):
            p = os.path.join(ROOT, "script", fname)
            cur = json.load(open(p, encoding="utf-8"))
            idx = {"%d:%s" % (x["bank"], x["addr"][2:].lower()): i for i, x in enumerate(cur)}
            for e in ents:
                if e["kind"] != kind:
                    continue
                b, a = e["key"].split(":")
                rec = {"bank": int(b), "addr": "0x" + a, "jp": e["jp"], "en": e["en"]}
                if kind == "rect":
                    rec = {"id": "%02x:%s" % (int(b), a), "bank": int(b), "addr": "0x" + a, "w": e["w"], "h": e["h"],
                           "jp": e["jp"], "en": e["en"]}
                if e["key"] in idx:
                    cur[idx[e["key"]]] = rec
                else:
                    cur.append(rec)
            cur.sort(key=lambda x: (x["bank"], x["addr"]))
            with open(p, "w", encoding="utf-8") as f:
                f.write("[\n" + ",\n".join(json.dumps(x, ensure_ascii=False) for x in cur) + "\n]\n")
        print("merged %d entries" % len(ents))


if __name__ == "__main__":
    main()
