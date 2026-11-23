"""Quake (DOS shareware 1.06): play routes and print the player's state from the server entity (floats).

  python3 games/dos/quake/tools/qstate.py "ROUTE" ["ROUTE" ...] [--png DIR]
  python3 games/dos/quake/tools/qstate.py --warm     build every checkpoint into the cache (do this before
      preview.py / shoot.py on an empty cache: see the playbook, "Determinism")
  python3 games/dos/quake/tools/qstate.py --chain "ROUTE" "TOKENS" "TOKENS" ... [--png DIR]
      one machine: the route, then each TOKENS group in turn (state and frame after each); with --png also
      DIR/sheet.png (all frames, labelled)

Prints per route: origin x y z, angles (pitch yaw roll), health, armor, ammo (shells nails rockets cells),
items bits. The player's entvars_t (QuakeC fields, 4-byte floats) sits at physical 0x371D48 with model
svga-80000, the stock ZIP and BOOT (`-nocdaudio -nosound`; with sound it was 0x37A638) (found 2026-11-23 in `start` by the hull pattern mins -16 -16 -24 / maxs 16 16 32).
--png DIR writes the last frame of each route as DIR/NN.png.
"""
import os, struct, sys
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "tools"))
os.chdir(ROOT)
import emu as E

V = 0x371D48
FIELDS = {"origin": (10, 3), "velocity": (16, 3), "angles": (19, 3), "health": (48, 1), "shells": (54, 4),
          "items": (58, 1), "armor": (83, 1), "frags": (49, 1)}


def find_player(emu):
    """Scan memory for the player's entvars_t: mins -16 -16 -24, maxs 16 16 32 at fields 33-38 and
    view_ofs 0 0 22 at fields 62-64. Returns the physical address or None."""
    import numpy as np
    base, size = emu._mem()
    f = np.frombuffer(emu.peek(0, size), dtype=np.float32)
    pat = np.array([-16, -16, -24, 16, 16, 32], dtype=np.float32)
    for i in np.nonzero(f == -16)[0]:
        if np.array_equal(f[i:i + 6], pat) and i >= 33 and f[i - 33 + 64] == 22:
            return int(i - 33) * 4
    return None


def state(emu):
    raw = emu.peek(V, 90 * 4)
    f = struct.unpack("<90f", raw)
    o = {k: f[i:i + n] for k, (i, n) in FIELDS.items()}
    return ("pos %7.1f %7.1f %7.1f  yaw %6.1f pitch %5.1f  hp %g  armor %g  ammo s%g n%g r%g c%g  items %d"
            % (*o["origin"], o["angles"][1], o["angles"][0], o["health"][0], o["armor"][0], *o["shells"],
               int(o["items"][0])))


def main():
    args = sys.argv[1:]
    png = None
    if "--png" in args:
        i = args.index("--png"); png = args[i + 1]; del args[i:i + 2]
        os.makedirs(png, exist_ok=True)
    g = E.Game("dos/quake")
    if args and args[0] == "--warm":
        # build every checkpoint into the cache from power-on (each one's own process): a shot taken right
        # after a cache miss continues the live run, which differs from every later run that loads the state
        import subprocess
        for c in g.checkpoints():
            subprocess.run([sys.executable, os.path.abspath(__file__), "@" + c["name"]], check=True)
        return
    if args and args[0] == "--find":
        emu, rest, _ = E.start(g, args[1])
        E.play(emu, g, rest)
        a = find_player(emu)
        print("player entvars at", None if a is None else "%X" % a)
        return
    if args and args[0] == "--chain":
        emu, rest, _ = E.start(g, args[1])
        E.play(emu, g, rest)
        frames = []
        for n, toks in enumerate(args[1:]):
            if n:
                E.play(emu, g, E.expand(g, E.split(toks)))
            print("%02d %s | %s" % (n, state(emu), toks[-60:]))
            if png:
                path = os.path.join(png, "%02d.png" % n)
                emu.image().save(path); frames.append(path)
        if png:
            E.sheet(frames, os.path.join(png, "sheet.png"), cols=4, labels=["%02d" % i for i in range(len(frames))])
        print("full route:", ",".join(args[1:]))
        return
    for n, route in enumerate(args):
        emu, rest, _ = E.start(g, route)
        E.play(emu, g, rest)
        print("%02d %s | %s" % (n, state(emu), route[-60:]))
        if png:
            emu.image().save(os.path.join(png, "%02d.png" % n))


if __name__ == "__main__":
    main()
