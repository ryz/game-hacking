"""survey.py AREA [AREA ...] | all : step onto every event square and every fight square of an area, in one process per area.

  python3 games/dos/might-and-magic/tools/survey.py 6 7 8        # caverns 2-4
  python3 games/dos/might-and-magic/tools/survey.py all          # all 55 areas (about 10 minutes on 4 cores)

Unlike scan.py (one emu.py run per square, pictures only) this keeps one emulator per area, reloads a state per
square and reads the encounter list from memory, so the result is text:
  work/scout/dos/might-and-magic/survey/NN_NAME.txt   one line per square: x,y facing kind -> monsters (count x name)
  work/scout/dos/might-and-magic/survey/NN_NAME.png   the frames, labelled (4 columns)
  work/scout/dos/might-and-magic/survey/NN_NAME_view.png   a plain view down a free corridor (the area's wall set)
Squares: the event squares of the area's .OVR (facing from its mask) and the squares whose property byte has
bit 80 without an event entry (random fight squares, entered facing north).
Base route: @equipped, Light (MNZ), WARP to (8,8) of the area. Memory: the encounter list is two arrays of 15: 15E88 number within a group of 16, 15E59 group (1-based);
monster number = (group - 1) * 16 + number (Vampire 124 = group 8, number 12; Okrim 195 = group 12, number 19).
"""
import os, sys, zipfile, tempfile
from multiprocessing import Pool
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "tools")); sys.path.insert(0, HERE)
ZIP = os.path.join(ROOT, "rom", "might-and-magic.zip")
OUT = os.path.join(ROOT, "work", "scout", "dos", "might-and-magic", "survey")
FACE = {"N": "C003300C10FF01F0", "E": "30C00C030110F0FF", "S": "0C3003C0F001FF10", "W": "030CC030FFF01001"}
CW = {"N": "E", "E": "S", "S": "W", "W": "N"}
# (map id, section) per area, playbook table "Areas"
IDS = ["0604:1", "0C03:1", "0203:1", "0802:1", "0B1A:1", "0A11:1", "0001:1", "0C01:1", "0202:1", "0005:1", "051B:1", "0212:1",
       "0601:1", "0A00:1", "0F01:2", "0502:2", "0B02:2", "0103:2", "0A00:2", "0703:2", "0101:2", "0D03:2", "0304:2", "0A11:2",
       "0904:2", "0F04:2", "0505:2", "0B05:2", "0106:2", "0801:2", "0112:2", "0706:2", "0B1A:2", "011B:2", "0706:3", "0F08:3",
       "0508:3", "0F03:3", "0703:3", "0F02:3", "0702:3", "0F04:3", "0704:3", "0A11:3", "0107:3", "0F05:3", "0A00:3", "0705:3",
       "0412:3", "0B07:3", "0F01:3", "0701:3", "0E00:3", "0201:3", "0B1A:3"]

def monsters():
    z = zipfile.ZipFile(ZIP)
    d = z.read(next(n for n in z.namelist() if n.upper().endswith("/MM.EXE")))
    o = d.find(b"FLESH EATER    "); names = {}
    for i in range(195):
        r = d[o + i * 32: o + i * 32 + 32]; names[i + 1] = (r[:15].decode("ascii").rstrip(" \0"), r[31])
    return names

def base_route(idx):
    if idx == 0: return "@equipped,CAST:6:1:6"
    i, s = IDS[idx].split(":")
    return "@equipped,CAST:6:1:6,WARP:08:08:%s:%s:0%s" % (i[2:], i[:2], s)

def survey(idx):
    import emu as E
    from PIL import Image, ImageDraw
    sys.argv = ["maps.py", ZIP]
    import maps
    name = maps.NAMES[idx]; mon = monsters()
    ev = maps.events(name); ev = ev[0] if ev else {}
    walls = maps.maze[idx * 512: idx * 512 + 256]; prop = maps.maze[idx * 512 + 256: idx * 512 + 512]
    g = E.Game("dos/might-and-magic")
    m, rest, _ = E.start(g, base_route(idx))
    for t in rest: E.step(m, g, t)
    st = os.path.join(tempfile.gettempdir(), "mmsurvey_%d_%d.state" % (idx, os.getpid())); m.save_state(st)
    jobs = []
    for o in range(256):
        if o in ev:
            for f, v in (("N", 0xC0), ("E", 0x30), ("S", 0x0C), ("W", 0x03)):
                if ev[o] & v: jobs.append((o, f, "event")); break
        elif prop[o] & 0x80: jobs.append((o, "N", "fight"))
    lines, tiles = [], []
    def visit(o, f, wait=250):
        m.load_state(st)
        m.poke(0x15E68, bytes([o & 15, o >> 4, o])); m.poke(0x15E6D, bytes.fromhex(FACE[CW[f]]))
        m.poke(0x15E80, bytes(24)); m.poke(0x15E59, bytes(15))
        E.step(m, g, "left"); E.step(m, g, "w%d" % wait)
        return m.image().convert("RGB").copy()
    for o, f, kind in jobs:
        im = visit(o, f)
        tier = bytes(m.peek(0x15E59, 15)); low = bytes(m.peek(0x15E88, 15))
        ids = [(b + 16 * (t - 1) if t else b) if b else 0 for b, t in zip(low, tier)]
        txt = ""
        if ids[0]:
            c = {}
            for b in ids:
                if b: c[b] = c.get(b, 0) + 1
            txt = " -> " + ", ".join("%d %s (pic %02X)" % (k, mon.get(b, ("?%02X" % b, 0))[0], mon.get(b, ("", 0))[1]) for b, k in c.items())
        lines.append("%2d,%2d %s %s%s" % (o & 15, o >> 4, f, kind, txt)); tiles.append(("%d,%d %s %s" % (o & 15, o >> 4, f, kind), im))
    # a plain view: a square with two free squares ahead, no events
    step = {"N": 16, "E": 1, "S": -16, "W": -1}; sh = {"N": 6, "E": 4, "S": 2, "W": 0}
    view = None
    for o in list(range(0x88, 256)) + list(range(0x88)):
        for f in "NESW":
            a, b = o + step[f], o + 2 * step[f]
            if not (0 <= b < 256) or (f in "EW" and (o >> 4) != (b >> 4)): continue
            if any(q in ev or prop[q] & 0x80 for q in (o, a, b)): continue
            if (walls[o] >> sh[f]) & 3 or (walls[a] >> sh[f]) & 3: continue
            view = (o, f); break
        if view: break
    os.makedirs(OUT, exist_ok=True)
    stem = os.path.join(OUT, "%02d_%s" % (idx, name))
    if view:
        visit(view[0], view[1], 120).save(stem + "_view.png"); lines.append("view %d,%d %s" % (view[0] & 15, view[0] >> 4, view[1]))
    m.close(); os.remove(st)
    open(stem + ".txt", "w").write("\n".join(lines) + "\n")
    if tiles:
        cols = 4; w, h = 320, 200; rows = (len(tiles) + cols - 1) // cols
        sheet = Image.new("RGB", (cols * w, rows * (h + 12)), (60, 0, 0)); dr = ImageDraw.Draw(sheet)
        for i, (lab, im) in enumerate(tiles):
            px, py = (i % cols) * w, (i // cols) * (h + 12)
            sheet.paste(im, (px, py + 12)); dr.text((px + 2, py), lab, fill=(255, 255, 0))
        sheet.save(stem + ".png")
    return "%02d %s: %d squares" % (idx, name, len(jobs))

if __name__ == "__main__":
    a = sys.argv[1:]
    idxs = list(range(55)) if a == ["all"] else [int(x) for x in a]
    with Pool(4) as p:
        for r in p.imap_unordered(survey, idxs): print(r, flush=True)
