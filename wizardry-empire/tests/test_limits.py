"""Field limits the game does not check."""
import json, os
ROOT = os.path.join(os.path.dirname(__file__), "..")


def test_unidentified_group_names_fit_c50f():
    """Unidentified monster group names (bank-49 table 31:570F, entries 0x570F-0x572D) are copied into the
    13-byte buffer $C50F; $C51C right after it holds the unidentified type index. 13+ characters overwrite it
    and the kill message prints code bytes (crash, playtest 2026-11-12)."""
    bad = []
    for e in json.load(open(os.path.join(ROOT, "script", "lists.json"), encoding="utf-8")):
        if isinstance(e, dict) and "table" in e and 0x570F <= int(e["table"], 16) <= 0x572D:
            if len(e["en"].encode("latin-1")) > 12:
                bad.append((e["table"], e["en"]))
    assert not bad, bad


def _load(name):
    return json.load(open(os.path.join(ROOT, "script", name), encoding="utf-8"))


def test_unidentified_item_types_fit_c54f():
    """Unidentified item type names (lists.json 0x567D-0x56AD) are copied by 0:376D into $C54F (17 bytes);
    $C560 after the 16 characters holds the unidentified class (overflow audit 2026-11-12)."""
    bad = [(e["table"], e["en"]) for e in _load("lists.json")
           if isinstance(e, dict) and "table" in e and 0x567D <= int(e["table"], 16) <= 0x56AD
           and len(e["en"].encode("latin-1")) > 16]
    assert not bad, bad


def test_monster_names_max_12():
    """Monster names: 12 characters (copied to $C50F/$C48F 13 bytes and $DD36 13 bytes)."""
    bad = [(e["id"], e["en"]) for e in _load("monsters.json") if len(e["en"].replace("\n", "")) > 12]
    assert not bad, bad


def test_spell_names_fit_wspell():
    """Full spell names go to wSpell ($D280) with a 31-character cap."""
    bad = [(e["id"], e["en"]) for e in _load("spells.json") if len(e["en"]) > 31]
    assert not bad, bad


def test_rows_fit_wnamebuf():
    """Rect rows, notice lines, inline and fixtable strings pass through the VWF's wNameBuf ($DFC0, 32 bytes
    incl. $00; engine state follows): 31 bytes after encoding (an alignment prefix adds 2)."""
    import re, sys
    sys.path.insert(0, os.path.join(ROOT, "tools"))
    import text
    def size(r):
        pre = 2 if r[:1] in "^>" or re.match(r"@\d+:", r) else 0
        r = re.sub(r"^@\d+:", "", r.lstrip("^>"))
        return pre + len(text.encode(r))
    bad = []   # rect rows reach wNameBuf only through the FixMap raw path (overflow audit): not checked here
    for f in ("inline.json", "fixtables.json"):
        for e in _load(f):
            if size(e["en"]) > 31:
                bad.append((f, e.get("addr"), e["en"]))
    for e in _load("notice.json"):
        for r in e["en"]:
            if size(r) > 31:
                bad.append(("notice", r))
    assert not bad, bad
