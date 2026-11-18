"""Check a game's three design lenses against its published shot set.

  python3 tools/lenses.py GAME [SET]      (GAME = slug or platform/slug; SET default main)

design/systems.md (game design), design/interface.md (UI/UX) and design/content.md (variety of content) are
the three indexes over a game's shots (docs/capture-guide.md, "Three lenses"). This lists:
  - shots mentioned in no document (by id in backticks, or by file name),
  - how many shots each document uses and how many are used by two or more,
  - table rows whose Shots cell is empty and that give no reason (a row may say "none: <why>").
Exit 0 = clean, 1 = something listed, 2 = a document or the set is missing.
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import emu  # noqa: E402

DOCS = ("systems.md", "interface.md", "content.md")


def mentioned(text, shot):
    """True when the document names the shot: its file name, or its id as a whole word in backticks."""
    if shot["file"] in text:
        return True
    return re.search(r"`[^`\n]*(?<![A-Za-z0-9_])%s(?![A-Za-z0-9_])[^`\n]*`" % re.escape(shot["id"]), text) is not None


def empty_rows(text):
    """(line number, first cell) of table rows with a Shots column that is empty."""
    out, col = [], None
    for n, line in enumerate(text.splitlines(), 1):
        if not line.startswith("|"):
            col = None
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if col is None:
            col = cells.index("Shots") if "Shots" in cells else -1
            continue
        if col < 0 or set(line) <= set("|-: ") or col >= len(cells):
            continue
        if not cells[col] and any(cells):
            out.append((n, cells[0] or cells[1] if len(cells) > 1 else cells[0]))
    return out


def check(game, set_="main"):
    idx = os.path.join(game.dir, "shots", set_, "index.json")
    if not os.path.exists(idx):
        return 2, ["no published set: %s" % os.path.relpath(idx, emu.ROOT)]
    shots = json.load(open(idx, encoding="utf-8"))["shots"]
    lines, texts = [], {}
    for d in DOCS:
        p = os.path.join(game.dir, "design", d)
        if not os.path.exists(p):
            return 2, ["missing: %s (template: games/_template/design/%s)" % (os.path.relpath(p, emu.ROOT), d)]
        texts[d] = open(p, encoding="utf-8").read()
    used = {d: {s["id"] for s in shots if mentioned(t, s)} for d, t in texts.items()}
    count = {s["id"]: sum(s["id"] in u for u in used.values()) for s in shots}
    lines.append("%d shots: %s; in two or more: %d" % (
        len(shots), ", ".join("%s uses %d" % (d, len(used[d])) for d in DOCS), sum(c > 1 for c in count.values())))
    unused = [s for s in shots if not count[s["id"]]]
    bad = bool(unused)
    for s in unused:
        lines.append("in no document: %s (%s) %s" % (s["id"], s["category"], s["caption"][:70]))
    for d, t in texts.items():
        for n, name in empty_rows(t):
            bad = True
            lines.append("%s:%d row without a shot or a reason: %s" % (d, n, name[:60]))
    return (1 if bad else 0), lines


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    code, out = check(emu.Game(sys.argv[1]), sys.argv[2] if len(sys.argv) > 2 else "main")
    print("\n".join(out))
    sys.exit(code)
