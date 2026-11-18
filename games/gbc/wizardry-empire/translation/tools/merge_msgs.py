"""Merge a message batch (python file with M = {"aaaa": [lines]}, BANK) into script/messages.json.
Japanese comes from the ROM; leading newlines and any Yes/No tail are taken from the Japanese."""
import json, os, re, runpy, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import census_msgs as c
ROOT = os.path.join(HERE, "..")


def yn_tail(jp):
    m = re.search(r"\n[ \n]*?( *)はい\n+( *)いいえ\n?$", jp)
    if not m:
        return None, jp
    head = jp[:m.start()]
    seg = jp[m.start():]
    seg = re.sub(r"( *)はい", lambda mm: "{col:%d}Yes" % len(mm.group(1)), seg)
    seg = re.sub(r"( *)いいえ", lambda mm: "{col:%d}No" % len(mm.group(1)), seg)
    return seg, head


def build(jp, lines):
    tail, head = yn_tail(jp)
    lead = len(head) - len(head.lstrip("\n"))
    sep = "\n\n"
    if "\n\n" not in head.strip("\n") and "\n" in head.strip("\n"):
        sep = "\n"  # the original is single spaced
    while lines and lines[0] == "":
        lines = lines[1:]
    body = lines[0] if lines else ""
    for ln in lines[1:]:
        body += "\n" if ln == "" else sep + ln
    return "\n" * lead + body + (tail or "")


def main(path, bank):
    M = runpy.run_path(path)["M"]
    out_path = os.path.join(ROOT, "script", "messages.json")
    cur = {(e["bank"], e["addr"]): e for e in json.load(open(out_path, encoding="utf-8"))}
    for a, lines in M.items():
        jp, _ = c.decode_msg(bank, int(a, 16))
        key = (bank, "0x" + a)
        cur[key] = {"bank": bank, "addr": "0x" + a, "jp": jp, "en": build(jp, lines)}
    out = sorted(cur.values(), key=lambda e: (e["bank"], e["addr"]))
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("[\n" + ",\n".join(json.dumps(e, ensure_ascii=False) for e in out) + "\n]\n")
    print(len(out), "messages")


if __name__ == "__main__":
    main(sys.argv[1], int(sys.argv[2]))
