"""Static SM83 disassembler for the ROM (bank-aware, no external deps).

usage: python tools/gbdis.py [--en | --rom PATH] BANK ADDR [COUNT]      e.g. gbdis.py 0 0x1700 40
  default ROM: the Japanese dump (or $WIZ_ROM); --en = the patched build/wizardry_empire_en.gbc (check patched bytes).
       python tools/gbdis.py [--en | --rom PATH] --xref BANK ADDR
  cross-references: every 3-byte instruction whose operand is ADDR (call/jp/ld rr,nn/ld a,[nn]/ld [nn],a ...)
  and every jr to it, found by a byte scan (data can give false hits; each hit is decoded so you can judge).
  An address >= $4000 is only searched in bank 0 and BANK; one < $4000 (or >= $8000, RAM) in every bank.
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


def xref(rom, bank, addr):
    out = []
    banks = range(len(rom) // 0x4000)
    if 0x4000 <= addr < 0x8000:
        banks = sorted({0, bank})
    for b in banks:
        base = 0 if b == 0 else 0x4000
        data = rom[b * 0x4000:(b + 1) * 0x4000]
        for i in range(len(data) - 2):
            op = "%02x" % data[i]
            if op == "cb" or op not in TAB:
                continue
            ln, t = TAB[op]
            pc = base + i
            hit = (ln == 3 and "{w}" in t and data[i + 1] | data[i + 2] << 8 == addr)
            if not hit and ln == 2 and "{r}" in t and (b == bank or b == 0 or addr < 0x4000):
                d = data[i + 1]
                hit = (pc + 2 + (d - 256 if d > 127 else d)) & 0xFFFF == addr
            if hit:
                out.append(dis(rom, b, pc, 1))
    return "\n".join(out)


if __name__ == "__main__":
    args = sys.argv[1:]
    path = os.environ.get("WIZ_ROM", ROM_DEFAULT)
    if args and args[0] == "--en":
        path, args = os.path.join(HERE, "..", "build", "wizardry_empire_en.gbc"), args[1:]
    elif args and args[0] == "--rom":
        path, args = args[1], args[2:]
    rom = open(path, "rb").read()
    if args and args[0] == "--xref":
        print(xref(rom, int(args[1], 0), int(args[2], 0)))
        sys.exit()
    b, a = int(args[0], 0), int(args[1], 0)
    print(dis(rom, b, a, int(args[2], 0) if len(args) > 2 else 32))
