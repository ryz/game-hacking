"""Check a game's checkpoints: does every cached state equal a replay of its route from power-on?

  python3 tools/cachecheck.py GAME                   every checkpoint in games/PLATFORM/GAME/checkpoints.txt
  python3 tools/cachecheck.py GAME NAME ...          these checkpoints (and, built on the way, the ones they start from)
  python3 tools/cachecheck.py GAME --flat leaves     power-on reference only for checkpoints nothing else builds
                                                     on (each covers its whole chain; much faster on long chains)
  python3 tools/cachecheck.py GAME --after "q,w200"  tokens played after every checkpoint before comparing
                                                     (default w60); e.g. save in the game to compare what
                                                     reaches the disk or the battery

Four states of every checkpoint are compared, each in a fresh process:
  flat    the whole route replayed from power-on, no cache (the reference; tools/emu.py at_checkpoint cache=False)
  cold    built into an empty cache, each checkpoint from the state of the one before (how shoot.py builds them)
  hit     loaded from that cache
  yours   loaded from your cache work/cache/PLATFORM/GAME, where it has the state (left alone otherwise;
          --fix deletes the files that differ, so the next run rebuilds them)
After the --after tokens they must agree in the frame, in memory (the backend's RAM search ranges) and in the
save data the game has written (battery RAM or files). One line per checkpoint: `same`, or which state
DIFFERS in what. Exit 1 on any difference. Your cache is never wiped: cold and hit use a temporary one.
Sheet of every checkpoint's frame for a look (labels = names): work/cachecheck/PLATFORM/GAME/sheet.png
(pages of 30: sheet_2.png ...). Look at it: a checkpoint that reproduces can still stand on the wrong screen.
  --peek ADDR:LEN     print these bytes (hex) per checkpoint (party table, position); several allowed
  --jobs N            processes (default 4, or the CPU count if lower)
"""
import argparse, hashlib, os, shutil, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
sys.path.insert(0, HERE)
import emu as E  # noqa: E402


def probe(job):
    """(name, mode) -> hashes of frame / memory / save data after the --after tokens, the frame, the peeks."""
    game_id, model, name, mode, cache_dir, after, peeks = job
    try:
        E.CACHE_DIR = None if mode == "yours" else cache_dir
        game = E.Game(game_id)
        if mode == "yours":
            if not os.path.exists(E.checkpoint_cache(game, name, model)):
                return name, mode, None, None, ""
        emu, _ = E.at_checkpoint(game, name, model, cache=mode != "flat")
        E.play(emu, game, E.expand(game, E.split(after)))
        png = emu.screen()
        from PIL import Image
        import io
        frame = hashlib.sha1(Image.open(io.BytesIO(png)).convert("RGB").tobytes()).hexdigest()[:10]
        ranges = getattr(emu, "SEARCH", None) or [(0xC000, 0x2000), (0xA000, 0x2000), (0xFF80, 0x7F)]
        h = hashlib.sha1()
        for base, size in ranges:
            h.update(bytes(emu.peek(base, size)))
        mem = h.hexdigest()[:10]
        try:
            kib = game.meta.get("header", {}).get("ram_kib") or 0
            data = emu.battery(kib * 1024) if (kib or getattr(emu, "FILE_SAVES", False)) else b""
            data = data if isinstance(data, (bytes, bytearray)) else open(data, "rb").read()
            if data[:2] == b"PK":               # a ZIP of files: compare the contents, not the archive bytes
                import zipfile
                z = zipfile.ZipFile(io.BytesIO(data))
                data = b"".join(n.encode() + z.read(n) for n in sorted(z.namelist()))
            save = hashlib.sha1(bytes(data)).hexdigest()[:10] if data else "-"
        except Exception as e:
            save = "n/a:" + type(e).__name__
        pk = " ".join("%s=%s" % (a, bytes(emu.peek(int(a, 16), n)).hex()) for a, n in peeks)
        emu.close()
        return name, mode, (frame, mem, save), png, pk
    except BaseException as e:
        return name, mode, ("ERROR %s: %s" % (type(e).__name__, e),), None, ""
    finally:
        E.CACHE_DIR = None              # jobs=1 runs in this process: leave the module as it was


def chain(game, names):
    """The named checkpoints plus every checkpoint they start from, in checkpoints.txt order."""
    cps = {c["name"]: c for c in game.checkpoints()}
    want = set()
    for n in names:
        while n and n not in want:
            if n not in cps:
                raise SystemExit("unknown checkpoint %r (games/%s/checkpoints.txt)" % (n, game.id))
            want.add(n)
            first = E.split(cps[n]["route"])[:1]
            n = first[0][1:] if first and first[0].startswith("@") else None
    return [n for n in cps if n in want]


def leaves(game, names):
    cps = {c["name"]: c for c in game.checkpoints()}
    parents = {E.split(cps[n]["route"])[0][1:] for n in names
               if E.split(cps[n]["route"])[:1] and E.split(cps[n]["route"])[0].startswith("@")}
    return [n for n in names if n not in parents]


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("game")
    ap.add_argument("names", nargs="*")
    ap.add_argument("--flat", choices=["all", "leaves", "none"], default="all")
    ap.add_argument("--after", default="w60")
    ap.add_argument("--peek", action="append", default=[])
    ap.add_argument("--fix", action="store_true")
    ap.add_argument("--model")
    ap.add_argument("--jobs", type=int, default=min(4, os.cpu_count() or 1))
    a = ap.parse_args(argv)
    game = E.Game(a.game)
    game.check_rom()
    model = a.model or game.model
    names = chain(game, a.names or [c["name"] for c in game.checkpoints()])
    if not names:
        raise SystemExit("no checkpoints in games/%s/checkpoints.txt" % game.id)
    peeks = [(p.split(":")[0], int(p.split(":")[1])) for p in a.peek]
    flat = {"all": names, "leaves": leaves(game, names), "none": []}[a.flat]
    tmp = tempfile.mkdtemp(prefix="cachecheck_")
    import multiprocessing

    def run(mode, which):
        jobs = [(game.id, model, n, mode, tmp, a.after, peeks) for n in which]
        if a.jobs > 1 and len(jobs) > 1:
            with multiprocessing.get_context("fork").Pool(min(a.jobs, len(jobs))) as pool:
                res = pool.map(probe, jobs, chunksize=1)
        else:
            res = [probe(j) for j in jobs]
        return {r[0]: r for r in res}
    try:
        got = {"flat": run("flat", flat), "cold": run("cold", names), "hit": run("hit", names),
               "yours": run("yours", names)}
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    out = os.path.join(ROOT, "work", "cachecheck", game.id)
    os.makedirs(out, exist_ok=True)
    bad, stale, tiles = 0, [], []
    for n in names:
        ref_mode = "flat" if n in got["flat"] else "cold"
        ref = got[ref_mode][n][2]
        diffs = []
        for mode in ("flat", "cold", "hit", "yours"):
            r = got[mode].get(n)
            if r is None or r[2] is None or mode == ref_mode:
                continue
            if r[2] != ref:
                what = [k for k, x, y in zip(("frame", "memory", "save"), r[2], ref) if x != y] or [r[2][0]]
                diffs.append("%s DIFFERS from %s (%s)" % (mode, ref_mode, ", ".join(what)))
                if mode == "yours":
                    stale.append(n)
        if ref[0].startswith("ERROR"):
            diffs.append(ref[0])
        bad += bool(diffs)
        have = got["yours"][n][2] is not None
        print("%-18s %s  %s%s%s" % (n, "same" if not diffs else "; ".join(diffs), " ".join(ref),
                                     "" if have else "  (not in your cache)",
                                     ("  " + got["cold"][n][4]) if got["cold"][n][4] else ""), flush=True)
        if got["cold"][n][3]:
            tiles.append((n, got["cold"][n][3], None))
    if tiles:
        import preview
        for p in preview.draw(tiles, os.path.join(out, "sheet"), 5, 30, 1, None):
            print(os.path.relpath(p, ROOT))
    if stale:
        if a.fix:
            for n in stale:
                os.remove(E.checkpoint_cache(game, n, model))
            print("removed %d stale state(s) from your cache: %s" % (len(stale), " ".join(stale)))
        else:
            print("your cache holds %d state(s) that their routes do not produce: %s (--fix deletes them)" % (
                len(stale), " ".join(stale)))
    print("%d/%d checkpoints reproduce (%s reference: %d)" % (len(names) - bad, len(names), "power-on", len(flat)))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
