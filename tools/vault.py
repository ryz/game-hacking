"""The private vault: game data (ROMs, unpatched dumps, patches, downloaded and exported saves, Kickstarts) kept in
the private repository ryz/game-hacking-r, so a fresh session can restore what this public repository never holds.

  python3 tools/vault.py push GAME [PATH ...] --booted "what the boot check showed" [--frames N] [--route TOKS] [-m MSG]
                                                          smoke-test GAME's ROM, then copy its data from rom/ into
                                                          the vault, commit, push
  python3 tools/vault.py push system/PLATFORM PATH ...    platform files (Amiga Kickstarts: rom/kickstart/...)
  python3 tools/vault.py check GAME [--route TOKS] [--frames N]  the boot check alone (nothing pushed): look at its
                                                          sheet first, then push with what it showed as --booted
  python3 tools/vault.py pull GAME|system/PLATFORM|--all  put the vault's files back where the tools expect them
  python3 tools/vault.py list                             what the vault holds

GAME is the slug or platform/slug (as for play.py). push collects what game.json names: "rom", "source"
base_copy / patch_copy / patches[].copy, plus rom/saves/<platform>/<slug>/ and rom/saves/<slug>/; extra PATHs
(any file under the repository, e.g. games/gbc/wizardry-empire/translation/rom/wizardry_empire_j.gbc) are added.

Only working ROMs go in (owner's rule 2026-11-21). Before a ROM is pushed, push checks that its SHA-1 matches
game.json, powers it on and runs N frames (default 3600; longer for slow loaders), and refuses it when the screen
stays blank or never changes. The pictures go to work/vault/smoke/<platform>/<slug>/sheet.png: look at them, and
say with --booted what the game showed (title, menu...): an emulator that runs is not yet a game that boots. The
result is kept in files.json ("check"). Saves, patches and extra files on their own need no check.

Vault layout (one folder per game, as games/ here):
  <platform>/<slug>/files.json         every file: vault name, local path (relative to this repository), SHA-1, role
  <platform>/<slug>/<file>             the registered ROM (patched if the game has patches), name as in rom/
  <platform>/<slug>/base/<file>        the unpatched dump
  <platform>/<slug>/patches/<file>     patches, under the names they came with
  <platform>/<slug>/saves/<file>       downloaded or exported saves (game data)
  <platform>/<slug>/extra/<file>       anything else given as PATH
  _system/<platform>/...               platform files (Kickstarts), same files.json

The vault checkout: $GAMEDB_VAULT, else ../game-hacking-r next to this repository, else work/vault/ (cloned on
first use). A cloud session must attach the repository first (add_repo ryz/game-hacking-r). push commits straight
to the vault's main branch (owner's rule 2026-11-21). GitHub refuses files over 100 MB: such a file is refused here.
"""
import argparse, hashlib, json, os, shutil, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
URL = os.environ.get("GAMEDB_VAULT_URL", "https://github.com/ryz/game-hacking-r")
BRANCH = "main"
MAX_BYTES = 95 * 1024 * 1024
ROLE_DIRS = {"rom": "", "base": "base", "patch": "patches", "save": "saves", "extra": "extra"}


def sha1(path):
    h = hashlib.sha1()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def git(vault, *args, check=True):
    r = subprocess.run(["git", "-C", vault] + list(args), capture_output=True, text=True)
    if check and r.returncode:
        raise SystemExit("git %s failed in %s:\n%s%s" % (" ".join(args), vault, r.stdout, r.stderr))
    return r


def vault_dir(root=ROOT, clone=True):
    """The vault checkout: $GAMEDB_VAULT, ../game-hacking-r, or work/vault/ (cloned when missing)."""
    for p in (os.environ.get("GAMEDB_VAULT"), os.path.join(os.path.dirname(root), "game-hacking-r"),
              os.path.join(root, "work", "vault")):
        if p and os.path.isdir(os.path.join(p, ".git")):
            return p
    if not clone:
        raise SystemExit("no vault checkout (set GAMEDB_VAULT or clone %s next to this repository)" % URL)
    p = os.path.join(root, "work", "vault")
    os.makedirs(os.path.dirname(p), exist_ok=True)
    r = subprocess.run(["git", "clone", "--depth", "1", URL, p], capture_output=True, text=True)
    if r.returncode:
        raise SystemExit("cannot clone the vault %s:\n%s\nIn a cloud session attach it first "
                         "(add_repo ryz/game-hacking-r)." % (URL, r.stderr))
    return p


def resolve(name, root=ROOT):
    """(vault folder, platform, slug, game.json or None) for GAME or system/PLATFORM."""
    name = name.strip("/")
    if name.startswith("system/"):
        plat = name.split("/", 1)[1]
        return "_system/" + plat, plat, None, None
    games = os.path.join(root, "games")
    if "/" in name:
        plat, slug = name.split("/", 1)
        found = [plat] if os.path.isdir(os.path.join(games, plat, slug)) else []
    else:
        slug = name
        found = sorted(p for p in os.listdir(games) if os.path.isdir(os.path.join(games, p, slug)))
    if not found:
        raise SystemExit("no game %r under games/" % name)
    if len(found) > 1:
        raise SystemExit("game %r exists on %s: say which, e.g. %s/%s" % (name, ", ".join(found), found[0], slug))
    gj = os.path.join(games, found[0], slug, "game.json")
    meta = json.load(open(gj, encoding="utf-8")) if os.path.exists(gj) else None
    return "%s/%s" % (found[0], slug), found[0], slug, meta


def collect(platform, slug, meta, extra, root=ROOT):
    """[(role, local path relative to root)] for one game; warns about named files that are missing."""
    out, missing = [], []

    def want(role, rel):
        if rel and (role, rel) not in out:
            (out if os.path.isfile(os.path.join(root, rel)) else missing).append((role, rel))

    if meta:
        want("rom", meta.get("rom"))
        src = meta.get("source") if isinstance(meta.get("source"), dict) else {}
        want("base", src.get("base_copy"))
        want("patch", src.get("patch_copy"))
        for p in src.get("patches", []):
            want("patch", p.get("copy"))
    if slug:
        for d in ("rom/saves/%s/%s" % (platform, slug), "rom/saves/%s" % slug):
            full = os.path.join(root, d)
            if os.path.isdir(full):
                for f in sorted(os.listdir(full)):
                    if os.path.isfile(os.path.join(full, f)):
                        want("save", d + "/" + f)
    for p in extra:
        rel = os.path.relpath(os.path.abspath(p), root)
        if rel.startswith(".."):
            raise SystemExit("%s is outside the repository: copy it into rom/ (or the game's folder) first" % p)
        want("extra", rel)
    for role, rel in missing:
        print("warning: %s (%s) is not here, not pushed" % (rel, role))
    return [x for x in out if x not in missing]


def smoke(name, frames=3600, every=300, root=ROOT, route=None):
    """Power the game on (then play ROUTE, tokens as for play.py do, for a game that waits at a menu) and run
    FRAMES frames: (distinct pictures, colours in the richest picture, sheet path).
    Refuses a ROM whose SHA-1 differs from game.json, a blank screen and a screen that never changes."""
    sys.path.insert(0, HERE)
    import emu
    from PIL import Image
    g = emu.Game(name)
    g.check_rom()
    out = os.path.join(root, "work", "vault", "smoke", g.id)
    os.makedirs(out, exist_ok=True)
    e = emu.open_game(g)
    paths, seen, colours = [], set(), 0

    def keep(p):
        nonlocal colours
        e.screen_png(p)
        paths.append(p)
        im = Image.open(p).convert("RGB")
        seen.add(hashlib.sha1(im.tobytes()).hexdigest())
        colours = max(colours, len(im.getcolors(1 << 16) or range(1 << 16)))
    try:
        if route:       # `!` in the route takes a picture there: a text game that waits for typing shows its answers
            part, n = [], 0
            for t in emu.expand(g, emu.split(route)) + [None]:
                if t in ("!", None):
                    emu.play(e, g, part)
                    part = []
                    if t:
                        n += 1
                        keep(os.path.join(out, "r%02d.png" % n))
                else:
                    part.append(t)
        for f in range(every, frames + 1, every):
            e.frames(every)
            keep(os.path.join(out, "f%05d.png" % f))
    finally:
        e.close()
    sheet = os.path.join(out, "sheet.png")
    emu.sheet(paths, sheet, cols=6, labels=[os.path.basename(p)[:-4] for p in paths])
    rel = os.path.relpath(sheet, root)
    if colours < 2:
        raise SystemExit("smoke test: the screen stayed blank for %d frames (%s): not pushed" % (frames, rel))
    if len(seen) < 3:
        raise SystemExit("smoke test: only %d different pictures in %d frames (%s): not booting? Not pushed; "
                         "--frames N for a slow loader, --route TOKENS for a game that waits for a key" % (len(seen), frames, rel))
    print("smoke test: %d different pictures, up to %d colours in %d frames; look at %s" % (
        len(seen), colours, frames, rel))
    return len(seen), colours, rel


def load_index(vdir):
    p = os.path.join(vdir, "files.json")
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else {"files": []}


def push(name, extra=(), message=None, root=ROOT, vault=None, remote=True, booted=None, frames=3600, check=smoke,
         route=None):
    vault = vault or vault_dir(root)
    folder, platform, slug, meta = resolve(name, root)
    files = collect(platform, slug, meta, extra, root)
    if not files:
        raise SystemExit("nothing to push for %s" % name)
    vdir = os.path.join(vault, folder)
    index = load_index(vdir)
    by_local = {e["local"]: e for e in index["files"]}
    result = None
    for role, rel in files:
        old = by_local.get(rel)
        if role == "rom" and not (old and old["sha1"] == sha1(os.path.join(root, rel))):
            if not booted:
                raise SystemExit("%s: only working ROMs go into the vault: run the boot check with --booted "
                                 "\"what the game showed\" (after looking at the sheet)" % rel)
            distinct, colours, sheet = check(folder, frames=frames, root=root, **({"route": route} if route else {}))
            result = {"frames": frames, "pictures": distinct, "colours": colours, "booted": booted,
                      "date": time.strftime("%Y-%m-%d")}
            if route:
                result["route"] = route
    changed = []
    for role, rel in files:
        full = os.path.join(root, rel)
        if os.path.getsize(full) > MAX_BYTES:
            raise SystemExit("%s is %d MB: GitHub refuses files over 100 MB; split or compress it first"
                             % (rel, os.path.getsize(full) >> 20))
        sub = ROLE_DIRS[role] if slug else ""
        vname = (sub + "/" if sub else "") + os.path.basename(rel)
        taken = {e["vault"]: e["local"] for e in index["files"]}
        if taken.get(vname, rel) != rel:
            raise SystemExit("vault name %s/%s is already used by %s" % (folder, vname, taken[vname]))
        h = sha1(full)
        old = by_local.get(rel)
        if old and old["sha1"] == h and os.path.exists(os.path.join(vdir, old["vault"])):
            continue
        dst = os.path.join(vdir, vname)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copyfile(full, dst)
        entry = {"vault": vname, "local": rel, "sha1": h, "size": os.path.getsize(full), "role": role}
        if role == "rom" and result:
            entry["check"] = result
        if old:
            index["files"][index["files"].index(old)] = entry
        else:
            index["files"].append(entry)
        by_local[rel] = entry
        changed.append(entry)
    if not changed:
        print("%s: vault already up to date (%d files)" % (folder, len(files)))
        return []
    index["files"].sort(key=lambda e: (list(ROLE_DIRS).index(e["role"]), e["vault"]))
    os.makedirs(vdir, exist_ok=True)
    with open(os.path.join(vdir, "files.json"), "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2)
        f.write("\n")
    git(vault, "add", "--", folder)
    msg = message or "%s: %s" % (folder, ", ".join(e["vault"] for e in changed))
    git(vault, "commit", "-q", "-m", msg)
    for e in changed:
        print("pushed %s -> %s/%s" % (e["local"], folder, e["vault"]))
    if remote:
        for attempt in range(4):
            r = git(vault, "push", "-u", "origin", "HEAD:" + BRANCH, check=False)
            if not r.returncode:
                break
            if "rejected" in r.stderr or "fetch first" in r.stderr:
                git(vault, "pull", "-q", "--rebase", "origin", BRANCH)
                continue
            time.sleep(2 ** (attempt + 1))
        else:
            raise SystemExit("vault push failed (committed locally in %s):\n%s" % (vault, r.stderr))
    return changed


def pull(name, root=ROOT, vault=None, remote=True, force=False):
    vault = vault or vault_dir(root)
    if remote and git(vault, "rev-parse", "--verify", "-q", "HEAD", check=False).returncode == 0:
        git(vault, "pull", "-q", "--ff-only", "origin", BRANCH, check=False)
    if name == "--all":
        folders = sorted(os.path.relpath(d, vault) for d, _, fs in os.walk(vault)
                         if "files.json" in fs and ".git" not in d)
    else:
        folders = [resolve(name, root)[0]]
    done = []
    for folder in folders:
        index = load_index(os.path.join(vault, folder))
        if not index["files"]:
            print("%s: not in the vault" % folder)
            continue
        for e in index["files"]:
            src, dst = os.path.join(vault, folder, e["vault"]), os.path.join(root, e["local"])
            if sha1(src) != e["sha1"]:
                raise SystemExit("vault file %s/%s does not match its SHA-1" % (folder, e["vault"]))
            if os.path.exists(dst):
                if sha1(dst) == e["sha1"]:
                    continue
                if not force:
                    print("kept %s: differs from the vault (pull --force replaces it)" % e["local"])
                    continue
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copyfile(src, dst)
            done.append(e["local"])
            print("pulled %s/%s -> %s" % (folder, e["vault"], e["local"]))
    return done


def listing(vault):
    for d, _, fs in sorted(os.walk(vault)):
        if "files.json" in fs and ".git" not in d:
            index = load_index(d)
            print("%-36s %s" % (os.path.relpath(d, vault), ", ".join(e["vault"] for e in index["files"])))


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("push")
    p.add_argument("game")
    p.add_argument("paths", nargs="*")
    p.add_argument("-m", "--message")
    p.add_argument("--booted", help="what the game showed in the boot check (title, menu...)")
    p.add_argument("--frames", type=int, default=3600, help="frames the boot check runs (default 3600)")
    p.add_argument("--route", help="tokens played after power-on, before the check counts pictures (a game that "
                   "waits at a menu: DOSBox Pure's program menu, a still title); `!` takes a picture at that point (a text "
                   "game that waits for typing: the answers count as pictures)")
    c = sub.add_parser("check", help="the boot check only, nothing pushed: look at the sheet, then push with --booted")
    c.add_argument("game")
    c.add_argument("--frames", type=int, default=3600)
    c.add_argument("--route")
    p = sub.add_parser("pull")
    p.add_argument("game")
    p.add_argument("--force", action="store_true")
    sub.add_parser("list")
    a = ap.parse_args()
    if a.cmd == "check":
        smoke(a.game, frames=a.frames, **({"route": a.route} if a.route else {}))
    elif a.cmd == "push":
        push(a.game, a.paths, a.message, booted=a.booted, frames=a.frames, route=a.route)
    elif a.cmd == "pull":
        pull(a.game, force=a.force)
    else:
        listing(vault_dir())


if __name__ == "__main__":
    main()
