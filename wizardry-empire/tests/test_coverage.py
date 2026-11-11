"""Text-copy coverage checks against the original ROM (skipped without rom/).

Lessons from the Camp status word (2026-11-11): a copy the fix_sites() pattern misses, reading a second copy of a
translated table, shows raw kana in the English build. These tests fail when such a case appears unhandled.
"""
import json, os, re, sys
import pytest
ROOT = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, os.path.join(ROOT, "tools"))
import insert

ROM = os.path.join(ROOT, "rom", "wizardry_empire_j.gbc")
pytestmark = pytest.mark.skipif(not os.path.exists(ROM), reason="original ROM not present")
HANDLED_IN_ASM = {(42, 0x4A29)}   # element name copy, patched in asm/main.asm (Stub_Fix db 3)
NEVER_READ = {(39, 0x4004)}       # "OK" record of the party-list status table: the printer never selects it


def rom():
    return open(ROM, "rb").read()


def addr(o):
    return (o // 0x4000, o % 0x4000 + (0x4000 if o >= 0x4000 else 0))


def test_short_copies_are_hooked():
    """Unrolled copies ending in `ld a,[hli] / ld [de],a` (no `ld a,[hl]`) are not matched by fix_sites():
    each must be an EXTRA_FIX_SITES entry, a SKIP_FIX_SITES entry or patched in asm."""
    d = rom()[:0x100000]
    covered = {(b, a) for b, a, *_ in insert.EXTRA_FIX_SITES} | HANDLED_IN_ASM
    covered |= {addr(o) for o in insert.SKIP_FIX_SITES}
    missing = []
    for m in re.finditer(rb"(?:\x2a\x12\x13)+\x2a\x12(?!\x13)", d):
        pre = d[m.start() - 8:m.start()]
        if any(pre[i] == 0x21 and pre[i + 2] >= 0x80 for i in range(len(pre) - 2)):
            continue  # RAM source: data, not text
        if addr(m.start()) not in covered:
            missing.append("%02X:%04X" % addr(m.start()))
    assert not missing, "unhooked text copies: " + ", ".join(missing)


def test_translated_tables_have_no_unhandled_copies():
    """A table translated in fixtables.json must not exist byte-for-byte elsewhere unless that copy is
    translated too (39:4004 duplicates 38:754D)."""
    d = rom()[:0x100000]
    fx = json.load(open(os.path.join(ROOT, "script", "fixtables.json"), encoding="utf-8"))
    keys = {(e["bank"], int(e["addr"], 16)) for e in fx}
    by_bank = {}
    for b, a in keys:
        by_bank.setdefault(b, []).append(a)
    problems = []
    for b, addrs in by_bank.items():
        addrs.sort()
        runs = [[addrs[0]]]
        for a in addrs[1:]:
            runs[-1].append(a) if a - runs[-1][-1] <= 8 else runs.append([a])
        for r in runs:
            lo = b * 0x4000 + r[0] - 0x4000
            hi = b * 0x4000 + r[-1] - 0x4000 + 4
            for m in re.finditer(re.escape(d[lo:hi]), d):
                if m.start() == lo:
                    continue
                cb, ca = addr(m.start())
                shift = ca - r[0]
                if not all((cb, a + shift) in keys or (cb, a + shift) in NEVER_READ for a in r):
                    problems.append("%02X:%04X copies %02X:%04X" % (cb, ca, b, r[0]))
    assert not problems, "; ".join(problems)
