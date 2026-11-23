"""Read text that an Apple II game draws on the hi-res screen, with a font table taught once per game.

  python3 tools/hirestext.py learn SLUG --route ROUTE "a line on that screen" ["another line" ...] [--at Y:X]
                                                         [--height N]  (cell height of a new font, default 8)
  python3 tools/hirestext.py read SLUG --route ROUTE [--raw]   (--raw: keep words of unknown cells)
  python3 tools/hirestext.py ignore SLUG --route ROUTE Y:X [Y:X ...]   cells that are not text (frames)
  python3 tools/hirestext.py show SLUG                    list the glyphs the font table knows

Many Apple II games (Bard's Tale, Might and Magic II) print messages in their own font on the hi-res screen,
where `play.py text` sees only the leftovers of the text page. Their letters sit in 7-pixel columns: one character
cell = 7 pixels wide (at any pixel phase per line) and 8 rows high (another height per font: --height). This reader cuts the shown hi-res page into such cells
at every row offset, looks each cell up in the game's table `games/<platform>/<slug>/font.json` (normal or
inverse: dark on light reads too) and keeps the rows that read as text. Unknown glyphs print as `?`.

Teach a font: take a screen whose text you can read from the picture (a message window), pass its lines
exactly (spaces included). `learn` finds where each line stands (blank and non-blank cells must match the
spaces), checks that one letter never has two shapes, and adds the glyphs. Teach more screens until
`read` shows no `?`. Once `font.json` exists, `play.py text` and `preview.py --text` read the hi-res screen for
that game. Letters on a pitch other than 7 pixels or proportional fonts are not supported (`learn` finds no place).
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))


def row_addr(page, y):
    return page + ((y & 7) << 10) + (((y >> 3) & 7) << 7) + (y >> 6) * 40


def page_rows(emu, page):
    """The 192 rows of a hi-res page as 280-bit integers, bit x = pixel x from the left; main RAM as stored."""
    mem = bytes(emu.peek(0x20000 + page, 0x2000))
    out = []
    for y in range(192):
        v = 0
        for i, b in enumerate(mem[row_addr(0, y):row_addr(0, y) + 40]):
            v |= (b & 0x7F) << (7 * i)
        out.append(v)
    return out


def px(rows, y, x):
    return rows[y] >> x & 1


def shown_page(emu):
    """0x2000 or 0x4000: the page whose pixels match the picture on screen (the soft switches cannot be read)."""
    im = emu.image().convert("L")
    sx, sy = im.width / 280, im.height / 192
    best = None
    for page in (0x2000, 0x4000):
        rows = page_rows(emu, page)
        score = 0
        for y in range(0, 192, 3):
            for x in range(0, 280, 2):
                on = px(rows, y, x)
                lit = im.getpixel((int(x * sx + sx / 2), int(y * sy + sy / 2))) > 96
                score += on == lit
        if best is None or score > best[0]:
            best = (score, page)
    return best[1]


H = 8          # cell height of the font in use: font.json "height" (load_font sets it), default 8


def cell(rows, y, x):
    """The 7-pixel-wide cell whose left edge is pixel x."""
    return bytes(rows[y + i] >> x & 0x7F for i in range(H))


def span_ink(rows, y, x0, n):
    """Any pixel set in row y from pixel x0 over n cells (frames of inverse windows count as ink too)."""
    m = (rows[y] >> x0) & ((1 << (7 * n)) - 1)
    return m not in (0, (1 << (7 * n)) - 1)


def blank(key):
    return all(b == 0 for b in key) or all(b == 0x7F for b in key)


def inv(key):
    return bytes(b ^ 0x7F for b in key)


def font_path(game_dir):
    return os.path.join(game_dir, "font.json")


def load_font(path, height=None):
    global H
    if not os.path.exists(path):
        H = height or 8
        return None
    d = json.load(open(path, encoding="utf-8"))
    H = d.get("height", 8)
    return {bytes.fromhex(k): v for k, v in d["glyphs"].items()}


def look(font, key):
    """The character of a cell: " " blank, "" ignored (a frame taught with `ignore`), None unknown."""
    if blank(key):
        return " "
    c = font.get(key)
    return c if c is not None else font.get(inv(key))


def read_rows(rows, font):
    """Lines of text on the page: [(y, string)], top to bottom."""
    cand = []
    for y, phase in [(y, p) for y in range(0, 193 - H) for p in range(7)]:
        s, known, unknown = [], 0, 0
        for col in range((280 - phase) // 7):
            c = look(font, cell(rows, y, phase + 7 * col))
            if c is None:
                unknown += 1
                s.append("?")
            else:
                known += c not in (" ", "")
                s.append(c)
        if known >= 3 or (known >= 2 and known > unknown):
            cand.append((known - unknown, y, (" " * phase if phase > 3 else "") + "".join(s)))
    taken, out = [], []
    for score, y, s in sorted(cand, key=lambda t: (-t[0], t[1])):
        if all(abs(y - t) >= H for t in taken):
            taken.append(y)
            out.append((y, s.rstrip()))
    return sorted(out)


def clean(s):
    """Drop words made only of unknown cells and runs of 3+ at the line's ends (pictures, frames)."""
    import re
    line = " ".join(w for w in s.split(" ") if w.strip("?"))
    return re.sub(r"\?{3,}$", "", re.sub(r"^\?{3,}", "", line)).strip()    # 3+ unknown cells at a line's ends: picture


def read(emu, font, raw=False):
    """The text lines on the shown hi-res page (play.py text, preview.py --text)."""
    lines = [s if raw else clean(s) for _, s in read_rows(page_rows(emu, shown_page(emu)), font)]
    return [l for l in lines if l]


def find_line(rows, text, at=None, font=None):
    """Places (y, x) where the cells match the text's spaces, best first: known letters agree, then the cells'
    top row holds ink (so a glyph always gets the same key), then blank rows above and below."""
    n, places = len(text), []
    ys = [at[0]] if at else range(0, 193 - H)
    for y in ys:
        xs = [at[1]] if at else range(0, 281 - 7 * n)
        for c0 in xs:
            if not span_ink(rows, y + H // 2, c0, n) and not span_ink(rows, y + 1, c0, n):
                continue
            keys = [cell(rows, y, c0 + 7 * i) for i in range(n)]
            if any(blank(k) != (ch == " ") for k, ch in zip(keys, text)):
                continue
            seen, ok = {}, True
            for k, ch in zip(keys, text):
                if ch != " " and seen.setdefault(ch, k) != k:
                    ok = False
                    break
            if not ok or len(set(seen.values())) != len(seen):
                continue
            agree = 0
            for k, ch in zip(keys, text):
                c = look(font, k) if font and ch != " " else None
                if c is not None and c != ch:
                    ok = False
                    break
                agree += c == ch
            if not ok:
                continue
            ink = [i for i in range(H) if span_ink(rows, y + i, c0, n)]
            top = bool(ink) and ink[0] == 0 and not (y and span_ink(rows, y - 1, c0, n))
            gap = sum(1 for yy in (y - 1, y + H) if 0 <= yy < 192 and not span_ink(rows, yy, c0, n))
            places.append((-agree, -top, -gap, y, c0))  # known letters agree, then top-aligned cells, line gaps
    return [(y, c) for _, _, _, y, c in sorted(places)]


def learn(rows, font, lines, at=None):
    report = []
    for text in lines:
        places = find_line(rows, text, at, font)
        if not places:
            report.append("not found: %r (byte-aligned 7x8 cells? exact text and spaces?)" % text)
            continue
        y, c0 = places[0]
        new = 0
        for i, ch in enumerate(text):
            if ch == " ":
                continue
            k = cell(rows, y, c0 + 7 * i)
            old = look(font, k)
            if old not in (None, ch) or old == "":
                raise SystemExit("glyph clash at row %d x %d: %r is already %r" % (y, c0 + 7 * i, ch, old))
            if old is None:
                font[k] = ch
                new += 1
        report.append("row %3d x %3d: %r (%d new glyphs%s)" % (
            y, c0, text, new, ", %d other places fit" % (len(places) - 1) if len(places) > 1 else ""))
    return report


def save_font(path, font):
    json.dump({"cell": "7 pixels wide (one byte), byte-aligned", "height": H, "glyphs": {k.hex(): v for k, v in sorted(font.items(), key=lambda t: t[1])}},
              open(path, "w", encoding="utf-8"), indent=0, ensure_ascii=False)
    open(path, "a").write("\n")


def main():
    a = sys.argv[1:]
    if len(a) < 2 or a[0] not in ("learn", "read", "show", "ignore"):
        raise SystemExit(__doc__)
    sys.path.insert(0, HERE)
    import emu as E
    game = E.Game(a[1])
    path = font_path(game.dir)
    hgt = None
    if "--height" in a:                     # a new font's cell height (default 8; kept in font.json)
        hgt = int(a[a.index("--height") + 1])
        a = a[:a.index("--height")] + a[a.index("--height") + 2:]
    if hgt and os.path.exists(path) and json.load(open(path, encoding="utf-8")).get("height", 8) != hgt:
        raise SystemExit("%s has another cell height: delete it to start over" % os.path.relpath(path, ROOT))
    font = load_font(path, hgt) or {}
    if a[0] == "show":
        print("%d glyphs: %s" % (len(font), "".join(sorted(font.values()))))
        return
    if "--route" not in a:
        raise SystemExit("--route ROUTE is needed")
    i = a.index("--route")
    route = a[i + 1]
    rest = [x for x in a[2:i] + a[i + 2:] if x != "--raw"]
    at = None
    if "--at" in rest:
        j = rest.index("--at")
        at = tuple(int(v) for v in rest[j + 1].split(":"))
        rest = rest[:j] + rest[j + 2:]
    e, toks, _ = E.start(game, route)
    E.play(e, game, toks)
    page = shown_page(e)
    rows = page_rows(e, page)
    if a[0] == "ignore":
        for spec in rest:
            y, col = (int(v) for v in spec.split(":"))          # Y:X, X in pixels
            k = cell(rows, y, col)
            if blank(k):
                print("row %d x %d is blank: nothing to ignore" % (y, col))
            elif look(font, k) not in (None, ""):
                raise SystemExit("row %d x %d is the glyph %r, not a frame" % (y, col, look(font, k)))
            else:
                font[k] = ""
                print("row %d x %d: ignored from now on" % (y, col))
        save_font(path, font)
    if a[0] == "learn":
        for line in learn(rows, font, rest, at):
            print(line)
        save_font(path, font)
        print("%s: %d glyphs" % (os.path.relpath(path, ROOT), len(font)))
    print("page %04X:" % page)
    for y, s in read_rows(rows, font):
        print("%3d |%s" % (y, s if "--raw" in a else clean(s)))
    e.close()


if __name__ == "__main__":
    main()
