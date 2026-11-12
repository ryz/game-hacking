"""Minimal two-pass SM83 assembler (rgbds-flavoured syntax, no external deps).
Code running past the end of its bank ($3FFF / $7FFF) is an error.

Directives:
  org BANK, ADDR        set output position (ADDR is the CPU address; bank 0 for $0000-$3FFF)
  NAME equ EXPR         constant
  db a, b, "str"        bytes ("str" is raw ASCII)
  dw a, b               little-endian words
  ds N[, FILL]          reserve N bytes (FILL default 0)
  incbin "path"         raw file (relative to the .asm file)
  assert EXPR[, "msg"]  checked in pass 2
Labels: `name:` (global), `.x` (local to the last global label). `@` = current address.
Expressions are Python expressions: $hex, %bin, bank(label), low(x), high(x).
Encoding comes from tools/sm83_optab.json (generated from gbemu's SameBoy disassembler).
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
_TAB = json.load(open(os.path.join(HERE, "sm83_optab.json")))

REGS = {"a", "b", "c", "d", "e", "h", "l", "af", "bc", "de", "hl", "sp", "[hl]", "[bc]", "[de]",
        "[hli]", "[hld]", "[c]", "nz", "z", "nc"}
# reverse table: normalised template -> (prefix bytes, placeholder kind or None)
REV = {}
for k, (ln, t) in _TAB.items():
    if k == "cb" or "CORRUPTED" in t or ".BYTE" in t:
        continue
    op = bytes.fromhex(k)
    t = t.lower()
    kind = None
    for ph in ("{w}", "{b}", "{r}"):
        if ph in t:
            kind = ph[1]
            t = t.replace(ph, "#")
    mn_, _, ops_ = t.partition(" ")
    t = mn_ + " " + ops_.replace(" ", "")
    if t.startswith(("bit ", "res ", "set ")):  # table writes "BIT a, 7" -> normalise to "bit 7,a"
        m = re.match(r"(bit|res|set) (.+),(\d)$", t)
        t = "%s %s,%s" % (m.group(1), m.group(3), m.group(2))
    REV.setdefault(t, (op, kind))
REV["stop "] = (b"\x10\x00", None)


class AsmError(Exception):
    pass


def _split_ops(s):
    out, depth, cur, q = [], 0, "", False
    for ch in s:
        if ch == '"':
            q = not q
        if ch in "([" and not q:
            depth += 1
        if ch in ")]" and not q:
            depth -= 1
        if ch == "," and depth == 0 and not q:
            out.append(cur.strip()); cur = ""
        else:
            cur += ch
    if cur.strip():
        out.append(cur.strip())
    return out


class Assembler:
    def __init__(self):
        self.sym = {}
        self.patches = []  # (rom_offset, bytes, srcline)

    # ---------------- expressions
    def ev(self, e, final):
        e = e.strip()
        e = re.sub(r"\$([0-9a-fA-F]+)", r"0x\1", e)
        e = re.sub(r"(?<![\w.])%([01]+)", r"0b\1", e)
        e = e.replace("@", "__here__")
        e = re.sub(r"bank\(\s*(\.?[A-Za-z_][\w.]*)\s*\)", lambda m: "B(%r)" % (self.glob + m.group(1) if m.group(1).startswith(".") else m.group(1)), e)

        def rep(m):
            n = m.group(0)
            if n.startswith("'"):
                return n
            if n in ("B", "low", "high", "__here__", "len") or re.match(r"0[xb][0-9a-fA-F]+$", n) or n.isdigit():
                return n
            full = self.glob + n if n.startswith(".") else n
            return "S[%r]" % full
        e2 = re.sub(r"'[^']*'|\.?[A-Za-z_][\w.]*|0[xb][0-9a-fA-F]+", rep, e)
        S = _Syms(self, final)
        try:
            return eval(e2, {"S": S, "B": S.bank_of, "low": lambda v: v & 0xFF,
                             "high": lambda v: (v >> 8) & 0xFF, "__here__": self.pc})
        except _Undef:
            if final:
                raise AsmError("undefined symbol in %r" % e)
            return 0

    # ---------------- encoding
    def encode(self, mn, ops, final):
        mn = mn.lower()
        if mn == "ldh":  # accept ldh [$ff00+n]/[$ffnn] too
            pass
        norm, val = [], None
        for o in ops:
            ol = o.lower().replace(" ", "")
            ol = {"[hl+]": "[hli]", "[hl-]": "[hld]", "[$ff00+c]": "[c]", "[0xff00+c]": "[c]"}.get(ol, ol)
            if ol in REGS:
                norm.append(ol)
            elif mn == "rst":
                norm.append("$%02x" % self.ev(o, final))
            elif mn in ("bit", "res", "set") and not norm:
                norm.append(str(self.ev(o, final)))
            elif ol.startswith("[") and ol.endswith("]"):
                norm.append("[#]"); val = o.strip()[1:-1]
            else:
                norm.append("#"); val = o
        key = mn + " " + ",".join(norm)
        if key not in REV:
            raise AsmError("cannot encode: %s %s" % (mn, ", ".join(ops)))
        op, kind = REV[key]
        if kind is None:
            return op
        v = self.ev(val, final)
        if kind == "w":
            return op + bytes([v & 0xFF, (v >> 8) & 0xFF])
        if kind == "b":
            if mn == "ldh":
                v &= 0xFF
            if final and not -128 <= v <= 255:
                raise AsmError("byte out of range: %s" % val)
            return op + bytes([v & 0xFF])
        # relative
        d = v - (self.pc + 2)
        if final and not -128 <= d <= 127:
            raise AsmError("jr out of range (%d)" % d)
        return op + bytes([d & 0xFF])

    # ---------------- passes
    def run(self, path, final):
        self.bank, self.pc, self.glob = 0, 0, ""
        self._file(path, final)

    def _emit(self, b, final, line):
        end = self.pc + len(b)
        if b and (self.pc < 0x4000 < end or 0x4000 <= self.pc < 0x8000 < end):
            raise AsmError("code runs past the end of its bank ($%04X-$%04X)" % (self.pc, end - 1))
        if final:
            if self.pc < 0x4000:
                off = self.pc
            else:
                off = self.bank * 0x4000 + (self.pc - 0x4000)
            self.patches.append((off, bytes(b), line))
        self.pc += len(b)

    def _file(self, path, final):
        base = os.path.dirname(os.path.abspath(path))
        for ln, raw in enumerate(open(path, encoding="utf-8"), 1):
            where = "%s:%d" % (os.path.basename(path), ln)
            line = _strip_comment(raw).strip()
            if not line:
                continue
            try:
                self._line(line, final, base, where)
            except AsmError as e:
                raise AsmError("%s: %s\n    %s" % (where, e, raw.rstrip()))

    def _line(self, line, final, base, where):
        m = re.match(r"^(\.?[A-Za-z_][\w.]*):{1,2}\s*(.*)$", line)
        if m:
            name = m.group(1)
            if not name.startswith("."):
                self.glob = name
            full = self.glob + name if name.startswith(".") else name
            self.sym[full] = (self.bank, self.pc)
            line = m.group(2).strip()
            if not line:
                return
        m = re.match(r"^([A-Za-z_]\w*)\s+equ\s+(.+)$", line, re.I)
        if m:
            self.sym[m.group(1)] = (None, self.ev(m.group(2), final))
            return
        parts = line.split(None, 1)
        mn = parts[0].lower()
        rest = parts[1] if len(parts) > 1 else ""
        ops = _split_ops(rest)
        if mn == "org":
            self.bank, self.pc = self.ev(ops[0], True), self.ev(ops[1], True)
        elif mn == "db":
            out = bytearray()
            for o in ops:
                if o.startswith('"'):
                    out += o[1:-1].encode("ascii")
                else:
                    out.append(self.ev(o, final) & 0xFF)
            self._emit(out, final, where)
        elif mn == "dw":
            out = bytearray()
            for o in ops:
                v = self.ev(o, final); out += bytes([v & 0xFF, (v >> 8) & 0xFF])
            self._emit(out, final, where)
        elif mn == "ds":
            n = self.ev(ops[0], True); f = self.ev(ops[1], True) if len(ops) > 1 else 0
            self._emit(bytes([f]) * n, final, where)
        elif mn == "incbin":
            self._emit(open(os.path.join(base, ops[0].strip('"')), "rb").read(), final, where)
        elif mn == "include":
            self._file(os.path.join(base, ops[0].strip('"')), final)
        elif mn == "assert":
            if final and not self.ev(ops[0], True):
                raise AsmError("assert failed: %s" % (ops[1] if len(ops) > 1 else ops[0]))
        else:
            self._emit(self.encode(mn, ops, final), final, where)


def _strip_comment(s):
    q = False
    for i, ch in enumerate(s):
        if ch == '"':
            q = not q
        elif ch == ";" and not q:
            return s[:i]
    return s


class _Undef(Exception):
    pass


class _Syms:
    def __init__(self, a, final):
        self.a, self.final = a, final

    def __getitem__(self, k):
        if k not in self.a.sym:
            raise _Undef(k)
        return self.a.sym[k][1]

    def bank_of(self, name):
        if name not in self.a.sym:
            if self.final:
                raise AsmError("bank(): undefined %s" % name)
            return 0
        return self.a.sym[name][0]


def assemble(path, extra_syms=None):
    a = Assembler()
    if extra_syms:
        for k, v in extra_syms.items():
            a.sym[k] = v
    a.run(path, False)
    a.patches = []
    a.run(path, True)
    return a


if __name__ == "__main__":
    a = assemble(sys.argv[1])
    for off, b, w in a.patches[:50]:
        print("%06x %s  %s" % (off, b.hex(), w))
