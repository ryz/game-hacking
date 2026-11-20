"""The game tables, written from each game's own files so no table is edited by hand.

  python3 tools/gamestable.py            rewrite the tables in README.md and docs/status.md
  python3 tools/gamestable.py --check    exit 1 if a table is out of date (tests, maintenance)

Source per game: games/<platform>/<slug>/game.json "title", "edition" (the release, e.g. "Famicom (English
translation patch)"), "work" (one line: what is here) and "open" (what is still missing); the published sets
(shots/<set>/index.json: shot counts); design/systems.md, interface.md, content.md (the three lenses). Scout
and capture agents keep "work" and "open" current in their game folder; the coordinator runs this tool.
A game that is not registered with the shared tools has a table.json in its folder (title, link, edition,
work, open). The tables sit between `<!-- games:begin -->` and `<!-- games:end -->` in both files.
"""
import glob, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
sys.path.insert(0, HERE)
import lenses  # noqa: E402

BEGIN, END = "<!-- games:begin -->", "<!-- games:end -->"
ORDER = ["gbc", "gb", "nes", "snes", "sms", "dos", "apple2", "amiga"]


def games():
    out = []
    for p in glob.glob(os.path.join(ROOT, "games", "*", "*", "table.json")):
        d = json.load(open(p, encoding="utf-8"))
        d["id"] = os.path.relpath(os.path.dirname(p), os.path.join(ROOT, "games"))
        d["sets"], d["lenses"] = "own tools", "-"
        out.append(d)
    for p in glob.glob(os.path.join(ROOT, "games", "*", "*", "game.json")):
        folder = os.path.dirname(p)
        gid = os.path.relpath(folder, os.path.join(ROOT, "games"))
        if gid.startswith("_") or os.path.basename(folder).startswith("zz-"):
            continue
        m = json.load(open(p, encoding="utf-8"))
        sets = []
        for ip in sorted(glob.glob(os.path.join(folder, "shots", "*", "index.json"))):
            idx = json.load(open(ip, encoding="utf-8"))
            n = len(idx["shots"]) if isinstance(idx, dict) else len(idx)
            name = os.path.basename(os.path.dirname(ip))
            sets.append((name != "main", name, "[%s](../games/%s/shots/%s/index.md) %d" % (name, gid, name, n)))
        main = os.path.join(folder, "shots", "main", "index.json")
        shots = json.load(open(main, encoding="utf-8"))["shots"] if os.path.exists(main) else []
        filled = []
        for n in ("systems", "interface", "content"):       # a copied template names no shot yet
            doc = os.path.join(folder, "design", n + ".md")
            if os.path.exists(doc):
                txt = open(doc, encoding="utf-8").read()
                if any(lenses.mentioned(txt, s) for s in shots):
                    filled.append(n)
        out.append({"id": gid, "title": m.get("title", m["slug"]), "link": "games/%s/playbook.md" % gid,
                    "edition": m.get("edition", m["platform"]), "work": m.get("work", ""), "open": m.get("open", ""),
                    "sets": ", ".join(s[2] for s in sorted(sets)) or "none",
                    "lenses": "yes" if len(filled) == 3 else "no" if not filled else "/".join(filled)})
    key = lambda g: (ORDER.index(g["id"].split("/")[0]) if g["id"].split("/")[0] in ORDER else 99, g["id"])  # noqa: E731
    return sorted(out, key=key)


def cell(s):
    return str(s).replace("|", "/").replace("\n", " ").strip() or "-"


def readme_table(gs):
    rows = ["| Game | Platform | What is here |", "|---|---|---|"]
    for g in gs:
        rows.append("| [%s](%s) | %s | %s |" % (cell(g["title"]), g["link"], cell(g["edition"]), cell(g["work"])))
    return "\n".join(rows)


def status_table(gs):
    rows = ["| Game | Folder | Sets (shots) | Three lenses | Open |", "|---|---|---|---|---|"]
    for g in gs:
        rows.append("| %s | `games/%s/` | %s | %s | %s |" % (cell(g["title"]), g["id"], cell(g["sets"]),
                                                         g["lenses"], cell(g["open"])))
    return "\n".join(rows)


def splice(path, table):
    t = open(path, encoding="utf-8").read()
    if BEGIN not in t or END not in t:
        raise SystemExit("%s has no %s ... %s block" % (os.path.relpath(path, ROOT), BEGIN, END))
    a, b = t.index(BEGIN) + len(BEGIN), t.index(END)
    return t, t[:a] + "\n" + table + "\n" + t[b:]


def main(argv=None):
    args = argv if argv is not None else sys.argv[1:]
    if "-h" in args or "--help" in args:
        print(__doc__)
        return 0
    check = "--check" in args
    gs = games()
    stale = []
    for path, table in ((os.path.join(ROOT, "README.md"), readme_table(gs)),
                        (os.path.join(ROOT, "docs", "status.md"), status_table(gs))):
        old, new = splice(path, table)
        if old != new:
            stale.append(os.path.relpath(path, ROOT))
            if not check:
                open(path, "w", encoding="utf-8").write(new)
    if check and stale:
        print("out of date: %s (run python3 tools/gamestable.py)" % ", ".join(stale))
        return 1
    print("%d games; %s" % (len(gs), ("updated: " + ", ".join(stale)) if stale else "tables up to date"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
