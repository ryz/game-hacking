"""68000 disassembler for a registered Mega Drive or Atari Jaguar game (or a ROM path), built on capstone.

  python3 tools/dis68k.py SLUG|ROM ADDR [N]          N instructions from ROM address ADDR (hex; default 40)
  python3 tools/dis68k.py SLUG|ROM --xref ADDR [ADDR ...]
                                                     every instruction that names ADDR (a RAM variable such as
                                                     FFC818 or a ROM table), from a linear sweep of the whole ROM

Mega Drive: the cartridge is mapped at 000000, so ROM offsets are CPU addresses. RAM addresses FF8000-FFFFFF are
also reached by absolute-short operands (`$c818.w` = FFC818); --xref finds both forms.
Jaguar (a registered game, or a .j64/.jag path): the cartridge is mapped at 800000, so ADDR is a CPU address
(802000 = the usual entry point); RAM is 000000-1FFFFF. A linear sweep also decodes
data as code: check each hit by disassembling the routine around it. Names of `game.json` "ram" watches are
added as comments. Needs `pip install capstone` (tools/setup_emu.sh md or jaguar installs it).
"""
import json, os, re, sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    import capstone
except ImportError:
    raise SystemExit("capstone missing: pip install capstone (or sh tools/setup_emu.sh md)")


BASE = {"md": (0, 0x200), "jaguar": (0x800000, 0x802000)}     # platform -> (where the ROM is mapped, code start)


def load(arg):
    """(rom bytes, {address: watch name}, platform)"""
    if os.path.exists(arg):
        jag = os.path.splitext(arg)[1].lower() in (".j64", ".jag")
        return open(arg, "rb").read(), {}, "jaguar" if jag else "md"
    import emu
    g = emu.Game(arg)
    if g.platform not in BASE:
        raise SystemExit("%s is a %s game; dis68k.py is for md and jaguar" % (arg, g.platform))
    names = {int(v["addr"], 16): k for k, v in g.meta.get("ram", {}).items() if isinstance(v, dict) and "addr" in v}
    return open(g.rom, "rb").read(), names, g.platform


def engine():
    md = capstone.Cs(capstone.CS_ARCH_M68K, capstone.CS_MODE_BIG_ENDIAN | capstone.CS_MODE_M68K_000)
    md.skipdata = True
    return md


def targets(op_str):
    """Addresses an operand string names: $xxxx.w (sign-extended), $xxxxxx(.l), branch targets."""
    out = []
    for m in re.finditer(r"\$([0-9a-f]+)(\.[wl])?", op_str):
        v, size = int(m.group(1), 16), m.group(2)
        if size == ".w" and v >= 0x8000:
            v |= 0xFF0000
        out.append(v & 0xFFFFFF)
    return out


def line(ins, names):
    raw = " ".join("%02X" % b for b in ins.bytes[:8])
    s = "%06X  %-23s %-8s %s" % (ins.address, raw, ins.mnemonic, ins.op_str)
    hit = [names[a] for a in targets(ins.op_str) if a in names]
    return s + ("   ; " + ", ".join(hit) if hit else "")


def main(argv):
    if len(argv) < 2:
        print(__doc__); return 2
    rom, names, platform = load(argv[0])
    base, start = BASE[platform]
    md = engine()
    if argv[1] == "--xref":
        want = set()
        for a in argv[2:]:
            v = int(a, 16) & 0xFFFFFF
            if platform == "md" and len(a) <= 4 and v >= 0x8000:   # C400 means RAM FFC400 (absolute-short form)
                print("; %s taken as %06X (RAM)" % (a, v | 0xFF0000))
                v |= 0xFF0000
            want.add(v)
        n = 0
        for ins in md.disasm(rom[start - base:], start):
            if ins.mnemonic.startswith("."):
                continue
            if want & set(targets(ins.op_str)):
                print(line(ins, names)); n += 1
        print("%d references" % n)
        return 0
    addr = int(argv[1], 16)
    count = int(argv[2], 0) if len(argv) > 2 else 40
    if not 0 <= addr - base < len(rom):
        raise SystemExit("%06X is not in the ROM (%06X-%06X)" % (addr, base, base + len(rom) - 1))
    for i, ins in enumerate(md.disasm(rom[addr - base:], addr)):
        if i >= count:
            break
        print(line(ins, names))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
