"""Check relative Markdown links in docs/: the file exists and the #anchor matches a heading (GitHub slugs).

  python3 tools/doclinks.py          prints broken links, exit 1 if any
"""
import glob, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.normpath(os.path.join(HERE, "..", "docs"))


def slug(h):
    s = re.sub(r"[^\w\- ]", "", h.strip().lower(), flags=re.UNICODE)
    return s.replace(" ", "-")


def anchors(path):
    out, seen = set(), {}
    for ln in open(path, encoding="utf-8"):
        m = re.match(r"^#{1,6} (.*)$", ln)
        if m:
            s = slug(m.group(1))
            k = seen.get(s, 0)
            out.add(s if k == 0 else "%s-%d" % (s, k))
            seen[s] = k + 1
    return out


def main():
    bad = 0
    for f in sorted(glob.glob(os.path.join(DOCS, "**", "*.md"), recursive=True)):
        text = open(f, encoding="utf-8").read()
        text = re.sub(r"```.*?```", "", text, flags=re.S)
        for target, anchor in re.findall(r"\]\(([^()#\s]*)(?:#([^()\s]+))?\)", text):
            if re.match(r"^[a-z]+:", target):
                continue
            path = os.path.normpath(os.path.join(os.path.dirname(f), target)) if target else f
            rel = os.path.relpath(f, DOCS)
            if not os.path.exists(path):
                print("%s: missing file %s" % (rel, target)); bad += 1
            elif anchor and path.endswith(".md") and anchor not in anchors(path):
                print("%s: missing anchor %s#%s" % (rel, target, anchor)); bad += 1
    print("broken links:", bad)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
