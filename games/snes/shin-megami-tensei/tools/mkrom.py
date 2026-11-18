"""Rebuild the catalogued ROM (rom/shin-megami-tensei.sfc) from the owner's Japanese dump and the two English
translation IPS patches. Neither the dump nor the patches are committed.

  python3 games/snes/shin-megami-tensei/tools/mkrom.py      (run from the repo root)

The two patches were made against different file layouts: smte1 (the translation) expects a ROM with the
512-byte copier header, smte2 (its bug-fix patch) expects one without. So: add a header, apply smte1, remove the
header, apply smte2. SHA-1 values are checked against game.json "source".
"""
import hashlib, json, os, sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import emu  # noqa: E402


def sha(b):
    return hashlib.sha1(b).hexdigest()


def main():
    meta = json.load(open(os.path.join(ROOT, "games", "snes", "shin-megami-tensei", "game.json"), encoding="utf-8"))
    src = meta["source"]
    base = open(os.path.join(ROOT, src["base_copy"]), "rb").read()
    p1 = open(os.path.join(ROOT, src["patches"][0]["copy"]), "rb").read()
    p2 = open(os.path.join(ROOT, src["patches"][1]["copy"]), "rb").read()
    for name, data, want in (("dump", base, src["base_sha1"]), ("smte1", p1, src["patches"][0]["sha1"]),
                             ("smte2", p2, src["patches"][1]["sha1"])):
        if sha(data) != want:
            raise SystemExit("%s has SHA-1 %s, expected %s" % (name, sha(data), want))
    d = bytearray(bytes(512) + base)
    emu.apply_ips(d, p1)
    d = d[512:]
    emu.apply_ips(d, p2)
    if sha(d) != meta["sha1"]:
        raise SystemExit("result has SHA-1 %s, game.json expects %s" % (sha(d), meta["sha1"]))
    out = os.path.join(ROOT, meta["rom"])
    open(out, "wb").write(d)
    print("wrote", os.path.relpath(out, ROOT), sha(d))


if __name__ == "__main__":
    main()
