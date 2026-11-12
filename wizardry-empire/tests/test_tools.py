"""Tool helpers that need no ROM: route tokens, held-modifier tokens, route-cache prefixes."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))
import emu  # noqa: E402


def test_tokens_expand_party():
    t = emu.tokens("boot, PARTY ,a*2,,w30")
    assert t[0] == "boot" and t[-2:] == ["a*2", "w30"]
    assert t[1:-2] == emu.tokens(emu.PARTY)


def test_chord_token():
    assert emu.chord_token("select>a") == (["select"], ["a"])
    assert emu.chord_token("b+select>a+up") == (["b", "select"], ["a", "up"])
    assert emu.chord_token("select+a") is None and emu.chord_token("x>a") is None


def test_prefixes_are_route_prefixes():
    # the longer prefix must extend the shorter one, so a PARTY route always uses the deepest cached state
    a, b = (emu.tokens(p) for p in emu.PREFIXES)
    assert b[:len(a)] == a and len(b) > len(a)
