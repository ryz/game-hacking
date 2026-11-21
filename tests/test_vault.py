"""tools/vault.py: push a game's data into a vault (a local bare repository as remote), pull it into a fresh tree."""
import json, os, subprocess, sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "tools"))
import vault  # noqa: E402


def sh(*args, cwd=None):
    subprocess.run(list(args), cwd=cwd, check=True, capture_output=True)


def tree(root, files, meta):
    os.makedirs(os.path.join(root, "games", "nes", "demo"))
    json.dump(meta, open(os.path.join(root, "games", "nes", "demo", "game.json"), "w"))
    for rel, data in files.items():
        os.makedirs(os.path.dirname(os.path.join(root, rel)), exist_ok=True)
        open(os.path.join(root, rel), "wb").write(data)


def test_push_pull_roundtrip(tmp_path):
    bare = tmp_path / "remote.git"
    sh("git", "init", "-q", "--bare", "-b", "main", str(bare))
    vdir = tmp_path / "vault"
    sh("git", "clone", "-q", str(bare), str(vdir))
    for k, v in (("user.name", "t"), ("user.email", "t@example.invalid")):
        sh("git", "-C", str(vdir), "config", k, v)
    meta = {"rom": "rom/demo.nes", "source": {"base_copy": "rom/src/demo-base.nes",
            "patches": [{"copy": "rom/patches/demo/fix.ips"}, {"copy": "rom/patches/demo/gone.ips"}]}}
    files = {"rom/demo.nes": b"patched", "rom/src/demo-base.nes": b"dump", "rom/patches/demo/fix.ips": b"PATCH",
             "rom/saves/nes/demo/a.sav": b"save"}
    a = tmp_path / "a"
    tree(str(a), files, meta)
    done = vault.push("demo", root=str(a), vault=str(vdir))
    assert sorted(e["vault"] for e in done) == ["base/demo-base.nes", "demo.nes", "patches/fix.ips", "saves/a.sav"]
    assert vault.push("demo", root=str(a), vault=str(vdir)) == []          # unchanged: nothing new
    out = subprocess.run(["git", "-C", str(bare), "log", "--oneline", "main"], capture_output=True, text=True).stdout
    assert out.count("\n") == 1

    b = tmp_path / "b"
    tree(str(b), {}, meta)
    v2 = tmp_path / "vault2"
    sh("git", "clone", "-q", str(bare), str(v2))
    got = vault.pull("demo", root=str(b), vault=str(v2))
    assert sorted(got) == sorted(files)
    for rel, data in files.items():
        assert open(os.path.join(b, rel), "rb").read() == data
    open(os.path.join(b, "rom/demo.nes"), "wb").write(b"local edit")
    assert vault.pull("demo", root=str(b), vault=str(v2)) == []             # a differing local file is kept
    assert vault.pull("demo", root=str(b), vault=str(v2), force=True) == ["rom/demo.nes"]


def test_outside_path_refused(tmp_path):
    a = tmp_path / "a"
    tree(str(a), {"rom/demo.nes": b"x"}, {"rom": "rom/demo.nes"})
    other = tmp_path / "elsewhere.bin"
    other.write_bytes(b"y")
    with pytest.raises(SystemExit):
        vault.collect("nes", "demo", {"rom": "rom/demo.nes"}, [str(other)], root=str(a))
