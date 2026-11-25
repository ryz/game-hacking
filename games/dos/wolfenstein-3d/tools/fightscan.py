"""Fight scan: play PREFIX (flat route), then repeat CYCLE tokens N times; log health/ammo/lives/score per cycle
and save one PNG per cycle (frame k = route `PREFIX,CYCLE*k,!` with CYCLE as a macro). usage: fightscan.py OUTDIR "PREFIX" "CYCLE" N"""
import sys, os
sys.path.insert(0, "/home/user/game-hacking/tools")
import emu as E
out, prefix, cycle, n = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4])
os.makedirs(out, exist_ok=True)
game = E.Game("dos/wolfenstein-3d")
emu, rest, full = E.start(game, prefix)
E.play(emu, game, rest)
ctoks = E.expand(game, E.split(cycle))
def rd(a, n=2):
    return int.from_bytes(bytes(emu.peek(a, n)), "little")
log = []
for k in range(n + 1):
    if k:
        E.play(emu, game, ctoks)
    h, am, lv, sc = rd(0x44924), rd(0x44926), rd(0x44922), rd(0x4491A, 4)
    p = os.path.join(out, "%03d.png" % k)
    emu.screen_png(p)
    log.append("%03d health=%d ammo=%d lives=%d score=%d map=%d" % (k, h, am, lv, sc, rd(0x44914)))
open(os.path.join(out, "log.txt"), "w").write("\n".join(log) + "\n")
print("\n".join(log))
