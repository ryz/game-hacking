"""Static SM83 disassembler for the ROM (bank-aware, no external deps).

usage: python tools/gbdis.py BANK ADDR [COUNT]      e.g. gbdis.py 0 0x1700 40
Opcode table (tools/sm83_optab.json) was generated from gbemu's SameBoy disassembler.
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
TAB = json.load(open(os.path.join(HERE, "sm83_optab.json")))
ROM_DEFAULT = os.path.join(HERE, "..", "rom", "wizardry_empire_j.gbc")


def off(bank, addr):
    return addr if addr < 0x4000 else bank * 0x4000 + (addr - 0x4000)


def dis1(rom, bank, addr):
    o = off(bank, addr)
    op = rom[o]
    if op == 0xCB:
        ln, t = TAB["cb%02x" % rom[o + 1]]
        return 2, t
    ln, t = TAB["%02x" % op]
    if ln == 3:
        t = t.replace("{w}", "$%04x" % (rom[o + 1] | rom[o + 2] << 8))
    elif ln == 2:
        b = rom[o + 1]
        t = t.replace("{b}", "$%02x" % b).replace("{r}", "$%04x" % ((addr + 2 + (b - 256 if b > 127 else b)) & 0xFFFF))
    return ln, t


def dis(rom, bank, addr, n):
    out = []
    for _ in range(n):
        ln, t = dis1(rom, bank, addr)
        o = off(bank, addr)
        out.append("%02x:%04x  %-9s %s" % (bank if addr >= 0x4000 else 0, addr, rom[o:o + ln].hex(), t))
        addr += ln
    return "\n".join(out)


if __name__ == "__main__":
    rom = open(os.environ.get("WIZ_ROM", ROM_DEFAULT), "rb").read()
    b, a = int(sys.argv[1], 0), int(sys.argv[2], 0)
    print(dis(rom, b, a, int(sys.argv[3], 0) if len(sys.argv) > 3 else 32))
