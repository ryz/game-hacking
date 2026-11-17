"""Walk a 3D map of Shin Megami Tensei depth-first through a running play.py session and draw what was found.

  python3 games/shin-megami-tensei/tools/explore.py OUTDIR [MAXCELLS] [--name SESSION]

Needs the game.json watches x (7E070C), y (7E070D) and dir (7E040D: 0 north, 1 east, 2 south, 3 west) and
the macros F (step), L, R, T (turn). Start it standing in free 3D movement. For every square it tries the
four directions; after every step B is pressed until the picture stops changing, so text boxes, prompts and rooms that
push the hero back out are passed; their first pages are copied to OUTDIR/ev_X_Y_D_N.png. Writes
OUTDIR/map.txt (squares, open sides, events) and returns to the starting square. The session's route grows by
every step taken: use it to find things, then write a short route by hand from map.txt.
"""
import hashlib, os, re, shutil, subprocess, sys

args = [a for a in sys.argv[1:]]
name = "shin-megami-tensei"
if "--name" in args:
    i = args.index("--name"); name = args[i + 1]; del args[i:i + 2]
out = args[0]
maxcells = int(args[1]) if len(args) > 1 else 60
os.makedirs(out, exist_ok=True)
P = ["python3", "tools/play.py", "--name", name]
DX = {0: (0, -1), 1: (1, 0), 2: (0, 1), 3: (-1, 0)}
log = open(os.path.join(out, "log.txt"), "w")


class Stop(Exception):
    pass


def do(tokens):
    r = subprocess.run(P + ["do", tokens], capture_output=True, text=True).stdout
    png = r.split()[0]
    w = dict((k, int(v)) for k, v in re.findall(r"(\w+)=(\d+)", r))
    h = hashlib.md5(open(png, "rb").read()).hexdigest()
    log.write("%s -> x=%s y=%s dir=%s %s\n" % (tokens, w.get("x"), w.get("y"), w.get("dir"), png)); log.flush()
    return w["x"], w["y"], w["dir"], h, png


def face(d, cur):
    k = (d - cur) % 4
    if k == 0:
        return do("w10")
    r = do({1: "R", 2: "T", 3: "L"}[k])
    if r[2] != d:
        raise Stop("cannot turn to %d at %s (picture %s)" % (d, r[:2], r[4]))
    return r


visited, edges, events = set(), {}, []


def step(x, y, d):
    """One step forward, then B until the picture stops changing (text boxes, rooms that push you back out).
    The pages of whatever opened are kept as ev_X_Y_D_N.png."""
    r = do("F")
    pages = [r[4]]
    for n in range(15):
        r2 = do("b,w90")
        if r2[3] == r[3]:
            break
        pages.append(r2[4]); r = r2
    else:
        raise Stop("event at %d,%d dir %d does not end (see %s)" % (x, y, d, r[4]))
    if len(pages) > 1:
        for n, pg in enumerate(pages[:4]):
            dst = os.path.join(out, "ev_%d_%d_%d_%d.png" % (x, y, d, n)); shutil.copy(pg, dst)
        events.append((x, y, d, "%d pages, ended at %d,%d" % (len(pages) - 1, r[0], r[1])))
    return r


def explore(x, y, cur):
    visited.add((x, y))
    for d in range(4):
        if (x, y, d) in edges:
            continue
        _, _, cur, h0, _ = face(d, cur)
        nx, ny, nd, h1, png = step(x, y, d)
        if (nx, ny) == (x, y):
            edges[(x, y, d)] = None
            cur = nd
            continue
        ex, ey = x + DX[d][0], y + DX[d][1]
        if (nx, ny) != (ex, ey):
            dst = os.path.join(out, "jump_%d_%d_%d.png" % (x, y, d)); shutil.copy(png, dst)
            raise Stop("step from %d,%d dir %d led to %d,%d (see %s)" % (x, y, d, nx, ny, dst))
        edges[(x, y, d)] = (nx, ny); edges[(nx, ny, (d + 2) % 4)] = (x, y)
        cur = nd
        if (nx, ny) not in visited and len(visited) < maxcells:
            cur = explore(nx, ny, cur)
        _, _, cur, _, _ = face((d + 2) % 4, cur)
        bx, by, cur, _, png = step(nx, ny, (d + 2) % 4)
        if (bx, by) != (x, y):
            raise Stop("cannot step back from %d,%d to %d,%d (see %s)" % (nx, ny, x, y, png))
    return cur


def draw():
    if not visited:
        return ""
    xs = [c[0] for c in visited]; ys = [c[1] for c in visited]
    rows = []
    for y in range(min(ys), max(ys) + 1):
        top, mid = "", ""
        for x in range(min(xs), max(xs) + 1):
            if (x, y) in visited:
                top += "+" + ("  " if edges.get((x, y, 0)) else "--")
                mid += (" " if edges.get((x, y, 3)) else "|") + "%X%X" % (x & 15, y & 15)
            else:
                top += "+  "; mid += "   "
        rows += [top, mid]
    return "\n".join(rows)


x, y, cur, _, _ = do("w10")
msg = "complete"
try:
    explore(x, y, cur)
except Stop as e:
    msg = "stopped: %s" % e
text = "%s\n%d squares, start %d,%d\n%s\nevents (x y dir file):\n%s\n" % (
    msg, len(visited), x, y, draw(), "\n".join("%d %d %d %s" % e for e in events))
open(os.path.join(out, "map.txt"), "w").write(text)
print(text)
