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


def test_cheat_formats():
    GB = platforms.GameBoy
    assert GB.gameshark("0109A2C0") == (None, 0xC0A2, 0x09)
    assert GB.gameshark("9163D0DA") == (1, 0xDAD0, 0x63)
    assert GB.gameshark("8205B3A0") == (2, 0xA0B3, 0x05)

    def encode(addr, value, cmp_=None):          # inverse of the SameBoy decoder
        d = "%02X%03X%X" % (value, addr & 0xFFF, (addr >> 12) ^ 0xF)
        if cmp_ is None:
            return d[:3] + "-" + d[3:]
        x = cmp_ ^ 0xBA
        g = ((x << 2) | (x >> 6)) & 0xFF
        return "%s-%s-%X0%X" % (d[:3], d[3:], g >> 4, g & 0xF)
    for addr, val, cmp_ in [(0x4ABC, 0x00, 0x3D), (0x0150, 0xC9, None), (0x7FFF, 0x12, 0xBA)]:
        assert GB.game_genie(encode(addr, val, cmp_)) == (addr, val, cmp_)
    rom = bytearray(0x10000)
    rom[0x0ABC] = 0x3D           # bank 0 copy: not touched (address is in the switchable bank)
    rom[0x4000 + 0x0ABC] = 0x3D  # bank 1
    rom[0x8000 + 0x0ABC] = 0x11  # bank 2: compare differs
    rom[0xC000 + 0x0ABC] = 0x3D  # bank 3
    assert GB.apply_game_genie(rom, encode(0x4ABC, 0x00, 0x3D)) == [0x4ABC, 0xCABC]
    assert rom[0x8ABC] == 0x11 and rom[0x0ABC] == 0x3D


def test_values_ips_prefix_freezes():
    assert emu.encode_value(8973, 2) == bytes([0x0D, 0x23])
    assert emu.encode_value(8973, 2, "be") == bytes([0x23, 0x0D])
    assert emu.encode_value(8973, 3, "bcd") == bytes([0x73, 0x89, 0x00])
    data = bytearray(b"\0" * 8)
    emu.apply_ips(data, b"PATCH" + b"\0\0\2\0\2AB" + b"\0\0\6\0\0\0\4Z" + b"EOF")
    assert bytes(data) == b"\0\0AB\0\0ZZZZ"
    assert emu.prefix(["rom:gg", "sav:end", "a"]) == ({"rom": "gg", "sav": "end"}, ["a"])
    e, g = FakeEmu(), FakeGame()
    g.platform = "gb"
    emu.step(e, g, "gs:0109A2C0")
    e.log = []
    emu.step(e, g, "w10")
    assert e.log == [("f", 10), ("poke", 0xC0A2, b"\x09")]      # held value re-written after the token
    emu.step(e, g, "unfreeze")
    e.log = []
    emu.step(e, g, "w10")
    assert e.log == [("f", 10)]
    emu.step(e, g, "set:C0B0=8973:2")
    assert e.log[-1] == ("poke", 0xC0B0, bytes([0x0D, 0x23]))


def test_rom_variant_and_set(selftest):
    run("tools/intake.py", str(selftest), "--slug", SLUG, "--probe", "0")
    gj = os.path.join(ROOT, "games", SLUG, "game.json")
    meta = json.load(open(gj))
    meta["rom_variants"] = {"patched": {"bytes": {"7FF0": "AB"}}}
    json.dump(meta, open(gj, "w"))
    g = emu.Game(SLUG)
    p = g.rom_file("patched")
    assert open(p, "rb").read()[0x7FF0] == 0xAB and "work/roms" in p
    e, rest, _ = emu.start(g, "rom:patched,w60,set:C200=8973:2,gs:015555C2")
    emu.play(e, g, rest)
    assert e.peek(0xC200, 2) == bytes([0x0D, 0x23]) and e.peek(0xC255, 1) == b"\x55"
    e.close()
