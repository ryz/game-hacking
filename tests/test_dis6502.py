import os, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "tools"))
import dis6502  # noqa: E402


def test_modes_branch_and_truncation():
    code = bytes([0xA9, 0x01, 0x8D, 0x00, 0x20, 0xD0, 0xFE, 0x02, 0x4C])
    out = dis6502.dis(code, 0xC000, 6, 0xC000)
    assert out[0].endswith("LDA #$01")
    assert out[1].endswith("STA $2000")
    assert out[2].endswith("BNE $C005")       # branch to itself
    assert out[3].endswith(".db $02")         # illegal opcode
    assert out[4].endswith(".db $4C")         # JMP cut off at the bank end
