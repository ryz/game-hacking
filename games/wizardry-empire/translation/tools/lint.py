"""Script-wide consistency lint (no ROM needed).

  python3 tools/lint.py            all script/*.json; exit 1 on ERROR
  python3 tools/lint.py --batch work/tl/NAME.json   also lint a batch against the script

Checks
  ERROR  glossary name (People/Places tables) in the Japanese but not its English in the translation
  ERROR  Yes/No choice in the Japanese (lines はい / いいえ) without Yes and No in the English
  ERROR  unbalanced double quotes in one entry
  WARN   the same Japanese translated differently in two places
  WARN   double spaces inside a line, trailing spaces, space before . , ! ?
"""
import argparse, glob, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))


def glossary():
    """JP -> EN from the People and Places tables of glossary.md (names, not common words)."""
    out, sect = {}, None
    for line in open(os.path.join(ROOT, "glossary.md"), encoding="utf-8"):
        if line.startswith("## "):
            sect = line[3:].strip()
            continue
        if sect not in ("People", "Places") or not line.startswith("|") or "---" in line:
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 2 or cells[0] == "JP":
            continue
        jps = [j.strip() for j in cells[0].split("/")]
        ens = [e.strip() for e in re.sub(r"\(.*?\)", "", cells[1]).split("/")]
        for i, j in enumerate(jps):
            if len(j) >= 3:
                out[j.replace(" ", "")] = ens[min(i, len(ens) - 1)] if len(ens) == len(jps) else ens
    return out


def entries():
    for p in sorted(glob.glob(os.path.join(ROOT, "script", "*.json"))):
        for e in json.load(open(p, encoding="utf-8")):
            yield os.path.basename(p), e


def text_of(v):
    return "\n".join(v) if isinstance(v, list) else (v or "")


def key_of(fname, e):
    if "bank" in e:
        return "%s %d:%s" % (fname, e["bank"], str(e.get("addr") or e.get("site"))[2:])
    return "%s #%s" % (fname, e.get("id"))


# Glossary terms that are also part of unrelated words: skip the match inside these (まどうし = wizard).
FALSE_MATCH = {"まどう": ["まどうし", "だいまどうし", "まどうゲート", "まどうのローブ"]}   # 魔導 (sorcery): Magic


def check(items, gl):
    errs, warns = [], []
    seen = {}
    for key, jp, en in items:
        if not en:
            continue
        jpn = jp.replace(" ", "")
        for j, eng in gl.items():
            if j in jpn and not any(f in jpn for f in FALSE_MATCH.get(j, [])):
                opts = eng if isinstance(eng, list) else [eng]
                stem = [o.split()[-1] if len(o.split()) > 1 else o for o in opts]
                if not any(s.lower() in en.lower() for s in stem):
                    errs.append("%s: glossary %s -> %s missing" % (key, j, "/".join(opts)))
        if re.search(r"(^|\n) *はい *\n+ *いいえ", jp) and not ("Yes" in en and "No" in en):
            errs.append("%s: Yes/No choice lost" % key)
        if en.count('"') % 2:
            errs.append("%s: unbalanced quotes" % key)
        for line in en.split("\n"):
            core = re.sub(r"\{[^}]*\}", "", line)
            if "  " in core.strip():
                warns.append("%s: double space in %r" % (key, line))
            if core != core.rstrip():
                warns.append("%s: trailing space in %r" % (key, line))
            if re.search(r" [.,!?]", core):
                warns.append("%s: space before punctuation in %r" % (key, line))
        if len(jp) >= 6:
            prev = seen.setdefault(jp, (key, en))
            if prev[1].strip() != en.strip():
                warns.append("%s: same Japanese as %s, different English (%r vs %r)" % (key, prev[0], en[:40], prev[1][:40]))
    return errs, warns


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--batch")
    ap.add_argument("--quiet", action="store_true", help="errors only")
    a = ap.parse_args()
    items = [(key_of(f, e), text_of(e.get("jp")), text_of(e.get("en"))) for f, e in entries()]
    if a.batch:
        for e in json.load(open(a.batch, encoding="utf-8")):
            items.append(("batch " + e["key"], text_of(e.get("jp")), text_of(e.get("en"))))
    errs, warns = check(items, glossary())
    if not a.quiet:
        for w in warns:
            print("WARN  " + w)
    for x in errs:
        print("ERROR " + x)
    print("lint: %d errors, %d warnings" % (len(errs), len(warns)))
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
