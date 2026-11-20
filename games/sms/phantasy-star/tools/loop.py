"""Seamless looping GIFs of first-person movement: hold a direction from a route, record every frame, find the
first stretch where the picture sequence repeats exactly (checked over two cycles), and write one cycle as a GIF
at game timing. Walking down a corridor whose far end is out of view repeats every step (37 frames); holding a
turn repeats every full rotation (194 frames), or every quarter turn (48 frames) where the neighbouring
corridors look the same, as at the crossroads used here.

  python3 games/sms/phantasy-star/tools/loop.py            all loops in LOOPS -> games/sms/phantasy-star/shots/loops/
  python3 games/sms/phantasy-star/tools/loop.py ID ...     only these

Deterministic: the same route gives the same GIF; the set's index.md lists every route."""
import hashlib, io, json, os, sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import emu  # noqa: E402

GAME = "sms/phantasy-star"
OUT = os.path.join(ROOT, "games", "sms", "phantasy-star", "shots", "loops")
NAME = "phantasy-star_sms_na_gameplay_loop_%s.loops.gif"
# id: (route to the start, held key, caption). Waits chosen so no encounter starts while recording.
LOOPS = {
    "walk_blue": ("@start,PARTY4,INV4,DUN:16:E4:00,settle,w2", "up",
                  "Walking down a long blue corridor (one step, loops seamlessly)"),
    "walk_red": ("@start,PARTY4,INV4,DUN:2B:ED:00,settle,w4", "up",
                 "Walking down a long red corridor (one step, loops seamlessly)"),
    "turn_blue": ("@start,PARTY4,INV4,DUN:16:64:00,settle", "right",
                  "Turning on the spot at a blue crossroads: endless turning (corridor to identical corridor)"),
    "turn_yellow": ("@start,PARTY4,INV4,DUN:25:AC:00,settle", "right",
                    "Turning on the spot at a yellow crossroads: endless turning (corridor to identical corridor)"),
}
MAX = 900


def cycle(frames):
    """(start, period) of the first exactly repeating stretch (two cycles) that moves (two pictures or more),
    starting on a picture change."""
    h = [hashlib.md5(f).digest() for f in frames]
    for p in range(12, len(h) // 2 + 1):
        for i in range(1, len(h) - 2 * p + 1):
            if h[i] != h[i - 1] and h[i:i + p] == h[i + p:i + 2 * p] \
                    and len(set(h[i:i + p])) > 1:
                return i, p
    raise SystemExit("no repeating cycle within %d frames" % len(frames))


def render(lid):
    route, key, caption = LOOPS[lid]
    g = emu.Game(GAME)
    e, rest, _ = emu.start(g, route)
    emu.play(e, g, rest)
    e.input([key])
    frames = []
    for _ in range(MAX):
        frames.append(e.screen())
        e.frames(1)
        if e.peek(0xC441, 1)[0]:
            raise SystemExit("%s: an encounter started while recording; change the wait in the route" % lid)
    e.input([])
    e.close()
    i, p = cycle(frames)
    one = frames[i:i + p]
    durs, runs = [], []                               # runs of the same picture -> one GIF frame each
    for f in one:
        if runs and runs[-1][0] == f:
            runs[-1][1] += 1
        else:
            runs.append([f, 1])
    acc, done = 0.0, 0
    for _, n in runs:                                 # GIF delays in 10 ms steps, error carried over
        acc += n * 1000.0 / 59.92
        d = int(round(acc / 10.0)) * 10 - done
        durs.append(d)
        done += d
    path = os.path.join(OUT, NAME % lid)
    emu.write_gif([r[0] for r in runs], path, durations=durs)
    poster = path[:-4] + ".png"
    open(poster, "wb").write(runs[0][0])
    return {"id": lid, "caption": caption, "route": route, "hold": key, "cycle_start": i, "frames": p,
            "pictures": len(runs), "seconds": round(p / 59.92, 2), "file": os.path.basename(path),
            "sha1": hashlib.sha1(open(path, "rb").read()).hexdigest()}


def main():
    ids = sys.argv[1:] or list(LOOPS)
    idx_path = os.path.join(OUT, "index.json")
    idx = {r["id"]: r for r in json.load(open(idx_path))} if os.path.exists(idx_path) else {}
    for lid in ids:
        idx[lid] = render(lid)
        print("%-12s %3d frames (%s s), %d pictures, from frame %d" % (
            lid, idx[lid]["frames"], idx[lid]["seconds"], idx[lid]["pictures"], idx[lid]["cycle_start"]))
    rows = [idx[k] for k in LOOPS if k in idx]
    json.dump(rows, open(idx_path, "w"), indent=1)
    md = ["# Phantasy Star (Master System): looping movement clips", "",
          "Seamless loops of first-person movement, one cycle each at game timing (made by "
          "`games/sms/phantasy-star/tools/loop.py`: hold the key from the route, record every frame, keep the "
          "first cycle that repeats exactly twice). The poster `.png` is the first picture of the cycle.", "",
          "| Clip | Caption | Length | Route, held key |", "|---|---|---|---|"]
    for r in rows:
        md.append("| ![%s](%s) | %s | %d frames, %s s | `%s`, hold `%s` |" % (
            r["id"], r["file"], r["caption"], r["frames"], r["seconds"], r["route"], r["hold"]))
    open(os.path.join(OUT, "index.md"), "w").write("\n".join(md) + "\n")


if __name__ == "__main__":
    main()
