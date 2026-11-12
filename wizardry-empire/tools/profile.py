"""Sampling profiler for one transition of a tour route (tools/routes/tour.txt): stop every N instructions and
count the routine (bank $40 = VWF symbols from build/*.sym; bank 0 by 16-byte block; other banks as game code).
usage: python3 tools/profile.py ROUTE AT [FRAMES=30] [N=400]   (AT = the key token index, see work/qa/perf/*/perf.json)"""
import sys, bisect, collections
sys.path.insert(0, 'tools')
import emu
from tour import routes
name, at = sys.argv[1], int(sys.argv[2])
nfr = int(sys.argv[3]) if len(sys.argv) > 3 else 30
step = int(sys.argv[4]) if len(sys.argv) > 4 else 400
syms = {}
for l in open('build/wizardry_empire_en.sym'):
    b, rest = l.split(':', 1); a, n = rest.split()
    if '.' in n: continue
    syms.setdefault(int(b, 16), []).append((int(a, 16), n))
for v in syms.values(): v.sort()
def name_of(bank, pc):
    if pc < 0x4000:
        return '00:%03X0' % (pc >> 4)
    lst = syms.get(bank, [])
    i = bisect.bisect_right([a for a, _ in lst], pc) - 1
    return ('%02X:' % bank) + (lst[i][1] if i >= 0 else '%04X' % pc)
g, toks, skip = emu.start(emu.EN_ROM, dict(routes())[name]); toks = toks[skip:]
emu.play(g, toks[:at])
g.input_set([toks[at]])
cnt = collections.Counter(); fr0 = emu.frame_counter(g); total = 0
while True:
    r = g.run_until(addr="$fffe", max_instructions=step)
    total += 1
    if total == 40: g.input_set([])
    pc = int(r['pc'], 16); bank = g.mem_read(0xFF9E, 1)[0]
    cnt[name_of(bank, pc) if bank == 0x40 or pc < 0x4000 else '%02X:game' % bank] += 1
    if (emu.frame_counter(g) - fr0) % 256 >= nfr: break
print('samples', total)
for n, c in cnt.most_common(25): print('%5.1f%%  %s' % (100.0 * c / total, n))
