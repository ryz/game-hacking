"""Every WRAM variable of the VWF (asm/vwf.asm 'equ $Dxxx') stays out of the tile shadows of pool codes
($D000 + code*16, bank 7): a variable there is overwritten whenever that slot's tile is drawn."""
import os, re, sys
ROOT = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, os.path.join(ROOT, "tools"))
import build

BANK6 = {"wVer", "wHIdx", "wHIdx2", "wStamp", "wPL_codes", "wPL_attrs",   # WRAM bank 6, not shadows
         "PL_ROW0"}                                                     # bank-3 screen buffer address


def test_vars_outside_pool_shadows():
    src = open(os.path.join(ROOT, "asm", "vwf.asm")).read()
    bad = []
    for name, val in re.findall(r"^(\w+)\s+equ\s+\$(d[0-9a-f]{3})\b", src, re.M | re.I):
        a = int(val, 16)
        if name in BANK6 or not (0xD000 <= a < 0xDF00) or name in ("qHead", "qTail"):
            continue
        code = (a - 0xD000) // 16
        if code in build.POOL:
            bad.append("%s $%04X (code $%02X)" % (name, a, code))
    assert not bad, bad
