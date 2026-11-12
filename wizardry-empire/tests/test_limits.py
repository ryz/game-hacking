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
