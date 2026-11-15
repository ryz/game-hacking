"""gamedb tests: tokens, routes, header identification (no emulator), and the whole pipeline on gbemu's generated
test ROM (skipped when tools/gbemu-cli is not built)."""
import json, os, shutil, subprocess, sys

import pytest

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import emu  # noqa: E402
import platforms  # noqa: E402

SLUG = "zz-selftest"
GBEMU = os.path.join(ROOT, "tools", "gbemu-cli")


class FakeEmu:
    def __init__(self):
        self.log = []

    def input(self, keys):
        self.log.append(("in", tuple(keys)))

    def frames(self, n):
        self.log.append(("f", n))

    def poke(self, addr, data):
        self.log.append(("poke", addr, bytes(data)))


class FakeGame:
    keys = platforms.GameBoy.keys
    hold, wait = 8, 40
    macros = {"TITLE": "w100,start", "NEWGAME": "TITLE,a"}
    slug = "fake"

    def checkpoints(self):
        return [{"name": "title", "description": "", "route": "TITLE,settle"},
                {"name": "w2", "description": "", "route": "@title,right:30"}]


def test_press_hold_chord_mash_poke():
    e, g = FakeEmu(), FakeGame()
    assert emu.step(e, g, "a")
    assert e.log == [("in", ("a",)), ("f", 8), ("in", ()), ("f", 40)]
    e.log = []
    emu.step(e, g, "right:30")
    assert e.log == [("in", ("right",)), ("f", 30), ("in", ())]
    e.log = []
    emu.step(e, g, "select>a")
    assert e.log[:3] == [("in", ("select",)), ("f", 4), ("in", ("select", "a"))]
    e.log = []
    emu.step(e, g, "b+a*2")
    assert e.log.count(("in", ("b", "a"))) == 2
    e.log = []
    emu.step(e, g, "mash:a:80")
    assert e.log.count(("in", ("a",))) == 10
    e.log = []
    emu.step(e, g, "poke:C0A2=0901")
    assert e.log == [("poke", 0xC0A2, b"\x09\x01")]
    assert not emu.step(e, g, "jump")
    assert not emu.step(e, g, "x:10")


def test_macros_and_checkpoints_resolve():
    g = FakeGame()
    assert emu.resolve(g, "NEWGAME,b") == ["w100", "start", "a", "b"]
    assert emu.resolve(g, "@w2,a") == ["w100", "start", "settle", "right:30", "a"]
    with pytest.raises(ValueError):
        emu.resolve(g, "@nope")


def test_gb_header():
    rom = bytearray(0x8000)
    rom[0x134:0x134 + 5] = b"HELLO"
    rom[0x143] = 0x80
    rom[0x146] = 0x03
    rom[0x147] = 0x1B
    rom[0x148] = 0x05
    rom[0x149] = 0x03
    chk = 0
    for b in rom[0x134:0x14D]:
        chk = (chk - b - 1) & 0xFF
    rom[0x14D] = chk
    h = platforms.GameBoy.identify(bytes(rom))
    assert h["header_title"] == "HELLO" and h["platform"] == "gbc" and h["model"] == "cgb"
    assert h["sgb"] and h["cart_type"] == "MBC5+RAM+BATTERY" and h["rom_kib"] == 1024 and h["ram_kib"] == 32
    assert h["header_checksum_ok"]


@pytest.fixture
def selftest(tmp_path):
    maker = os.path.join(GBEMU, "cli", "tests", "make_test_rom.py")
    if not (os.path.exists(platforms.GameBoy.BIN) and os.path.exists(maker)):
        pytest.skip("gbemu-cli not built (sh tools/setup_emu.sh)")
    rom = tmp_path / "t.gb"
    subprocess.run([sys.executable, maker, str(rom), str(tmp_path / "t.json")], check=True, capture_output=True)
    yield rom
    subprocess.run([sys.executable, os.path.join(ROOT, "tools", "play.py"), "--name", SLUG, "stop"],
                   capture_output=True)
    for p in (os.path.join(ROOT, "games", SLUG), os.path.join(ROOT, "work", "shots", SLUG),
              os.path.join(ROOT, "work", "cache", SLUG), os.path.join(ROOT, "work", "intake", SLUG),
              os.path.join(ROOT, "work", "play", SLUG)):
        shutil.rmtree(p, ignore_errors=True)
    if os.path.exists(os.path.join(ROOT, "rom", SLUG + ".gb")):
        os.remove(os.path.join(ROOT, "rom", SLUG + ".gb"))


def run(*args):
    r = subprocess.run([sys.executable] + list(args), cwd=ROOT, capture_output=True, text=True)
    assert r.returncode == 0, r.stdout + r.stderr
    return r.stdout


def test_pipeline(selftest):
    run("tools/intake.py", str(selftest), "--slug", SLUG, "--probe", "120")
    gj = os.path.join(ROOT, "games", SLUG, "game.json")
    meta = json.load(open(gj))
    assert meta["platform"] == "gb" and meta["model"] == "dmg"
    meta["macros"] = {"TITLE": "w120"}
    meta["ram"] = {"joy": {"addr": "C010", "size": 1}}
    json.dump(meta, open(gj, "w"))
    P = ["tools/play.py", "--name", SLUG]
    run(*P, "start", SLUG)
    run(*P, "do", "TITLE")
    assert "saved" in run(*P, "checkpoint", "title", "after boot")
    run(*P, "do", "right:20,a")
    assert run(*P, "route").strip() == "@title,right:20,a,settle"
    run(*P, "snap", "a_shot", "gameplay", "after A")
    assert "candidates" in run(*P, "find", "new == old")
    run(*P, "stop")
    out = run("tools/shoot.py", SLUG, "main", "--verify")
    assert "1/1 reproduce" in out
    run("tools/shoot.py", SLUG, "main", "--publish")
    idx = json.load(open(os.path.join(ROOT, "games", SLUG, "shots", "main", "index.json")))
    s = idx["shots"][0]
    assert s["id"] == "a_shot" and s["route"] == "@title,right:20,a,settle" and s["rom_sha1"] == meta["sha1"]
    from PIL import Image
    assert Image.open(os.path.join(ROOT, "games", SLUG, "shots", "main", "a_shot.png")).size == (160, 144)
