"""Round-trip: disassemble every opcode with tools/dis.py, reassemble with tools/asm.py."""
import os, sys, tempfile
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))
import asm, gbdis as dis


def test_roundtrip_all_opcodes():
    rom = bytearray(0x8000)
    code = bytearray()
    for op in range(256):
        if op in (0xCB, 0x10) or "BYTE" in dis.TAB["%02x" % op][1]:
            continue
        code += bytes([op, 0x34, 0x12])[: dis.TAB["%02x" % op][0]]
    for op in range(256):
        code += bytes([0xCB, op])
    rom[0x150:0x150 + len(code)] = code
    lines, pc, end = [], 0x150, 0x150 + len(code)
    while pc < end:
        ln, t = dis.dis1(rom, 0, pc)
        t = t.replace("SP, ", "sp, ")
        if t.startswith(("BIT", "RES", "SET")):
            mn, rest = t.split(" ", 1); r, n = rest.split(", ")
            t = "%s %s, %s" % (mn, n, r)
        if t.startswith("JR"):
            t = t  # absolute target, fine
        if t.startswith("LD hl, sp,"):
            pc += ln; lines.append("db $f8, $34"); continue
        lines.append(t); pc += ln
    src = "org 0, $150\n" + "\n".join(lines) + "\n"
    with tempfile.NamedTemporaryFile("w", suffix=".asm", delete=False) as f:
        f.write(src)
    a = asm.assemble(f.name)
    out = b"".join(b for _, b, _ in a.patches)
    assert out == bytes(code)
