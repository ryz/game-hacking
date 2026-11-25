"""Doom registered 1.1 (DOS, model svga-40000, BOOT with -nosound): play routes and print the player's state.
Copied from games/dos/ultimate-doom/tools/dstate.py; addresses and the player_t layout are 1.1's.

  python3 games/dos/doom/tools/dstate.py "ROUTE" ["ROUTE" ...] [--png DIR]
  python3 games/dos/doom/tools/dstate.py --chain "ROUTE" "TOKENS" "TOKENS" ... [--png DIR]
      one machine: the route, then each TOKENS group in turn (state after each); with --png DIR/NN.png and
      DIR/sheet.png
  python3 games/dos/doom/tools/dstate.py --tp "ROUTE" X Y ANGLE
      the TP macro call (game.json "TP") that puts the player at X Y (map units, z = floor there from the WAD) facing ANGLE
      (degrees, 0 east, 90 north) at the end of ROUTE; append them to that route (then a small move such as
      `up:2`, which relinks the player into the new sector). The mobj address depends on the route.

player_t players[0] sits at physical 0x20B558 in 1.1 (found 2026-11-25: the only pointer to the mobj at the
start position, and the maxammo 200 50 300 50 pattern at +178). 1.1's structs are byte-packed and differ from
the released source: ticcmd/view fields take 10 bytes more (health at +42, not +32) and weaponowned has 8
entries (no super shotgun), so ammo/maxammo/counts move 4 back again. Offsets: +0 mo, +42 health,
+46 armorpoints, +50 armortype, +54 powers[6], +78 cards[6], +122 readyweapon, +126 pendingweapon (9 = none),
+130 weaponowned[8], +162 ammo[4] (clip, shell, cell, rocket), +178 maxammo[4], +210 killcount, +214 itemcount,
+218 secretcount. mobj_t (packed, at any byte address) +12 x, +16 y, +20 z (16.16), +32 angle,
+56 floorz, +60 ceilingz, +88 type, +92 info, +108 health, as in the source; mobjinfo records are 88 bytes (no raisestate).
"""
import os, struct, sys
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "tools"))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
import emu as E

P = 0x20B558
O = dict(health=42, armor=46, armortype=50, powers=54, cards=78, ready=122, owned=130, ammo=162,
         maxammo=178, kills=210, items=214, secrets=218)
WEAPONS = ["fist", "pistol", "shotgun", "chaingun", "rocket", "plasma", "BFG", "chainsaw"]


def mo_addr(emu):
    return struct.unpack("<I", emu.peek(P, 4))[0]


def state(emu):
    p = emu.peek(P, 280)
    hp, ap, at = struct.unpack_from("<iii", p, O["health"])
    pw = struct.unpack_from("<6i", p, O["powers"]); cards = struct.unpack_from("<6i", p, O["cards"])
    w = struct.unpack_from("<i", p, O["ready"])[0]; ammo = struct.unpack_from("<4i", p, O["ammo"])
    k, it, se = struct.unpack_from("<3i", p, O["kills"])
    mo = mo_addr(emu)
    s = "%s hp %d armor %d/%d ammo b%d s%d c%d r%d weapon %s kills %d items %d secrets %d" % (current_map(emu),
        hp, ap, at, ammo[0], ammo[1], ammo[2], ammo[3], WEAPONS[w] if 0 <= w < 8 else w, k, it, se)
    if any(pw):
        s += " powers %s" % (pw,)
    if any(cards):
        s += " cards %s" % (cards,)
    if 0 < mo < 0x1000000:
        m = emu.peek(mo, 112)
        x, y, z = struct.unpack_from("<3i", m, 12); a = struct.unpack_from("<I", m, 32)[0]
        s = "pos %7.1f %7.1f %5.1f angle %5.1f | " % (x / 65536, y / 65536, z / 65536, a / 2 ** 32 * 360) + s
    return s


def tp_tokens(emu, x, y, ang):
    import wadmap
    mo = mo_addr(emu)
    name = current_map(emu)
    m = wadmap.Map(wadmap.wad(), name)
    sec = m.sectors[m.sector_at(x, y)]
    z, c = sec[0], sec[1]
    h = lambda v: struct.pack("<i", v).hex().upper()
    bam = int(ang / 360.0 * 2 ** 32) & 0xFFFFFFFF
    return "TP:%X:%s%s%s:%X:%s:%X:%s%s" % (mo + 12, h(x << 16), h(y << 16), h(z << 16), mo + 32,
                                          struct.pack("<I", bam).hex().upper(), mo + 56, h(z << 16), h(c << 16))


def current_map(emu):
    # gameepisode / gamemap (found by comparing WARP boots; they follow idclev too, see the playbook)
    e = struct.unpack("<i", emu.peek(GAMEEPISODE, 4))[0]
    m = struct.unpack("<i", emu.peek(GAMEMAP, 4))[0]
    return "E%dM%d" % (e, m)


GAMEEPISODE, GAMEMAP = 0x20BAD4, 0x20BAC0  # 1.1 (0x20B9EC / 0x20B9E0 follow idclev but not the exit to the next map)


def main():
    args = sys.argv[1:]
    png = None
    if "--png" in args:
        i = args.index("--png"); png = args[i + 1]; del args[i:i + 2]
        os.makedirs(png, exist_ok=True)
    g = E.Game("dos/doom")
    if args and args[0] == "--tp":
        emu, rest, _ = E.start(g, args[1]); E.play(emu, g, rest)
        print(tp_tokens(emu, int(args[2]), int(args[3]), float(args[4])))
        return
    if args and args[0] == "--chain":
        emu, rest, _ = E.start(g, args[1]); E.play(emu, g, rest)
        frames = []
        for n, toks in enumerate(args[1:]):
            if n:
                E.play(emu, g, E.expand(g, E.split(toks)))
            print("%02d %s | %s" % (n, state(emu), toks[-50:]))
            if png:
                path = os.path.join(png, "%02d.png" % n); emu.image().save(path); frames.append(path)
        if png:
            E.sheet(frames, os.path.join(png, "sheet.png"), cols=4, labels=["%02d" % i for i in range(len(frames))])
        return
    for n, route in enumerate(args):
        emu, rest, _ = E.start(g, route); E.play(emu, g, rest)
        print("%s | %s" % (state(emu), route[-50:]))
        if png:
            emu.image().save(os.path.join(png, "%02d.png" % n))


if __name__ == "__main__":
    main()
