"""Stand-in for `xxd -i FILE` (C array of a file's bytes on stdout), for building the AppleWin core on a machine
without xxd (part of vim). tools/setup_emu.sh puts it on the PATH as `xxd` only when the real one is missing."""
import re, sys

if len(sys.argv) != 3 or sys.argv[1] != "-i":
    sys.exit("usage: xxd -i FILE")
data = open(sys.argv[2], "rb").read()
name = re.sub(r"[^A-Za-z0-9_]", "_", sys.argv[2])
if name[:1].isdigit():
    name = "__" + name
rows = [", ".join("0x%02x" % b for b in data[i:i + 12]) for i in range(0, len(data), 12)]
sys.stdout.write("unsigned char %s[] = {\n  %s\n};\nunsigned int %s_len = %d;\n" % (
    name, ",\n  ".join(rows), name, len(data)))
