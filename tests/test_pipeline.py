"""Shared tooling tests: tokens, routes, header identification (no emulator), and the whole pipeline on gbemu's generated
test ROM (skipped when tools/gbemu-cli is not built) and on a generated NES test ROM (skipped when the Mesen
core is not built), a generated SNES test ROM (skipped when the Mesen-S core is not built), a generated DOS
test program (skipped when the DOSBox Pure core is not built) and a generated Apple II test disk (skipped when
the AppleWin core is not built)."""
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
    slug, id = "fake", "gb/fake"

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


def test_prefix_skips_pow():
    assert emu.prefix(["pow", "sav:x", "rom:y", "a"]) == ({"sav": "x", "rom": "y"}, ["a"])
    assert emu.prefix(["sav:x", "a"]) == ({"sav": "x"}, ["a"])
    assert emu.prefix(["pow", "a"]) == ({}, ["pow", "a"])


def test_macro_repeat():
    assert emu.expand(FakeGame(), ["TITLE*2", "a*2"]) == ["w100", "start", "w100", "start", "a*2"]


def test_macros_and_checkpoints_resolve():
    g = FakeGame()
    assert emu.resolve(g, "NEWGAME,b") == ["w100", "start", "a", "b"]
    assert emu.resolve(g, "@w2,a") == ["w100", "start", "settle", "right:30", "a"]
    with pytest.raises(ValueError):
        emu.resolve(g, "@nope")


def test_find_game_by_slug_or_platform_slug():
    assert emu.find_game("pokemon-blue") == ("gb", "pokemon-blue")
    assert emu.find_game("nes/might-and-magic") == ("nes", "might-and-magic")
    g = emu.Game("dungeon-magic")
    assert g.id == "nes/dungeon-magic" and g.platform == "nes" and g.dir.endswith("games/nes/dungeon-magic")
    with pytest.raises(SystemExit, match="dos, nes"):                       # same slug on two platforms
        emu.find_game("might-and-magic")
    with pytest.raises(SystemExit):
        emu.find_game("no-such-game")
    with pytest.raises(SystemExit):
        emu.find_game("snes/might-and-magic")
    for folder in sorted(os.listdir(os.path.join(ROOT, "games"))):         # the folder is the platform
        for slug in sorted(os.listdir(os.path.join(ROOT, "games", folder))):
            gj = os.path.join(ROOT, "games", folder, slug, "game.json")
            if folder != "_template" and os.path.exists(gj):
                assert json.load(open(gj))["platform"] == folder, gj


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
    for p in (os.path.join(ROOT, "games", "gb", SLUG), os.path.join(ROOT, "work", "shots", "gb", SLUG),
              os.path.join(ROOT, "work", "cache", "gb", SLUG), os.path.join(ROOT, "work", "intake", "gb", SLUG),
              os.path.join(ROOT, "work", "play", SLUG)):
        shutil.rmtree(p, ignore_errors=True)
    if os.path.exists(os.path.join(ROOT, "rom", SLUG + ".gb")):
        os.remove(os.path.join(ROOT, "rom", SLUG + ".gb"))


NES_SLUG = "zz-selftest-nes"


@pytest.fixture
def nes_selftest(tmp_path):
    if not os.path.exists(platforms.Nes.SO):
        pytest.skip("Mesen core not built (sh tools/setup_emu.sh nes)")
    sys.path.insert(0, os.path.dirname(__file__))
    import make_nes_rom
    rom = tmp_path / "t.nes"
    rom.write_bytes(make_nes_rom.build())
    yield rom
    subprocess.run([sys.executable, os.path.join(ROOT, "tools", "play.py"), "--name", NES_SLUG, "stop"],
                   capture_output=True)
    for sub in ("games/nes", "work/shots/nes", "work/cache/nes", "work/intake/nes", "work/play"):
        shutil.rmtree(os.path.join(ROOT, sub, NES_SLUG), ignore_errors=True)
    if os.path.exists(os.path.join(ROOT, "rom", NES_SLUG + ".nes")):
        os.remove(os.path.join(ROOT, "rom", NES_SLUG + ".nes"))


def run(*args):
    r = subprocess.run([sys.executable] + list(args), cwd=ROOT, capture_output=True, text=True)
    assert r.returncode == 0, r.stdout + r.stderr
    return r.stdout


def test_pipeline(selftest):
    run("tools/intake.py", str(selftest), "--slug", SLUG, "--probe", "120")
    gj = os.path.join(ROOT, "games", "gb", SLUG, "game.json")
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
    assert "UNCHANGED" in run(*P, "snap", "a_shot", "gameplay", "after A")
    assert "candidates" in run(*P, "find", "new == old")
    run(*P, "snap", "oops", "gameplay", "wrong caption")
    assert "recaptioned" in run(*P, "recaption", "oops", "right caption")
    d = os.path.join(ROOT, "work", "shots", "gb", SLUG, "main")
    assert "| right caption |" in open(os.path.join(d, "shots.txt")).read()
    assert "right caption" in open(os.path.join(d, "index.md")).read()
    assert "removed" in run(*P, "unsnap", "oops")
    assert "oops" not in open(os.path.join(d, "shots.txt")).read() and not os.path.exists(os.path.join(d, "oops.png"))
    run(*P, "stop")
    out = run("tools/shoot.py", SLUG, "main", "--verify")
    assert "1/1 reproduce" in out
    run("tools/shoot.py", SLUG, "main", "--publish-only")
    idx = json.load(open(os.path.join(ROOT, "games", "gb", SLUG, "shots", "main", "index.json")))
    s = idx["shots"][0]
    assert s["id"] == "a_shot" and s["route"] == "@title,right:20,a,settle" and s["rom_sha1"] == meta["sha1"]
    from PIL import Image
    pub = os.path.join(ROOT, "games", "gb", SLUG, "shots", "main")
    assert Image.open(os.path.join(pub, "a_shot.png")).size == (160, 144)
    assert Image.open(os.path.join(pub, "3x", "a_shot.png")).size == (480, 432)    # same name, 3x/ subfolder
    assert s["file_3x"] == "3x/a_shot.png" and not [f for f in os.listdir(pub) if "@3x" in f]
    assert "(3x/a_shot.png)" in open(os.path.join(pub, "index.md")).read()


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
    gj = os.path.join(ROOT, "games", "gb", SLUG, "game.json")
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


def test_export_save(selftest):
    data = bytearray(open(selftest, "rb").read())
    data[0x147], data[0x149] = 0x1B, 0x02          # MBC5+RAM+BATTERY, 8 KiB
    chk = 0
    for b in data[0x134:0x14D]:
        chk = (chk - b - 1) & 0xFF
    data[0x14D] = chk
    open(selftest, "wb").write(data)
    run("tools/intake.py", str(selftest), "--slug", SLUG, "--probe", "0")
    P = ["tools/play.py", "--name", SLUG]
    run(*P, "start", SLUG)
    run(*P, "do", "w60")
    r = subprocess.run([sys.executable, *P, "export", "early", "nothing saved"], cwd=ROOT, capture_output=True,
                       text=True)
    assert r.returncode != 0 and "battery RAM is empty" in r.stdout        # refused: nothing was saved
    assert not os.path.exists(os.path.join(ROOT, "games", "gb", SLUG, "saves", "early.sav"))
    run(*P, "do", "gs:802A00A0,w2")                                 # writes cartridge RAM bank 0
    out = run(*P, "export", "early", "After power-on, one byte written", "--state")
    assert "early.sav" in out
    run(*P, "stop")
    d = os.path.join(ROOT, "games", "gb", SLUG, "saves")
    assert os.path.getsize(os.path.join(d, "early.sav")) == 8192
    assert os.path.exists(os.path.join(d, "early.state"))
    assert "| early | `early.sav`, `early.state` |" in open(os.path.join(d, "README.md")).read()
    g = emu.Game(SLUG)
    e, rest, _ = emu.start(g, "sav:early,w10")
    emu.play(e, g, rest)
    e.close()


def test_clip_and_sequence(selftest):
    run("tools/intake.py", str(selftest), "--slug", SLUG, "--probe", "0")
    P = ["tools/play.py", "--name", SLUG]
    run(*P, "start", SLUG)
    run(*P, "do", "w30")
    run(*P, "snap", "s01_start", "gameplay", "Start", "--set", "seq-test")
    bad = subprocess.run([sys.executable] + P + ["record", "s02_clip", "clip", "60", "Clip", "--set", "seq-test"],
                         cwd=ROOT, capture_output=True, text=True)
    assert bad.returncode == 1 and "error: category 'clip' unknown" in bad.stdout
    out = run(*P, "record", "s02_clip", "gameplay", "60", "Clip", "--every", "3", "--poster", "-1", "--set", "seq-test")
    assert "frames kept" in out and "poster = kept frame -1" in out
    run(*P, "do", "a")
    run(*P, "snap", "s03_after", "gameplay", "After A", "--set", "seq-test")
    run(*P, "stop")
    d = os.path.join(ROOT, "work", "shots", "gb", SLUG, "seq-test")
    assert open(os.path.join(d, "shots.txt")).read().count("rec:60:3:-1") == 2  # the clip, and the step after it
    assert "3/3 reproduce" in run("tools/shoot.py", SLUG, "seq-test", "--verify")
    run("tools/shoot.py", SLUG, "seq-test", "--publish-only")
    pub = os.path.join(ROOT, "games", "gb", SLUG, "shots", "seq-test")
    for f in ("s01_start.png", "s02_clip.gif", "3x/s02_clip.gif", "s02_clip.png", "3x/s03_after.png", "strip.png",
              "steps.gif", "3x/steps.gif", "full.gif", "3x/full.gif", "sheet.png"):
        sub, name = os.path.split(f)                                        # 3x copies in the 3x/ subfolder
        assert os.path.exists(os.path.join(pub, sub, "seq-test_" + name)), f  # sequence files carry the set name
    assert not [f for f in os.listdir(pub) if f.endswith((".png", ".gif")) and not f.startswith("seq-test_")]
    idx = json.load(open(os.path.join(pub, "index.json")))
    clip = [s for s in idx["shots"] if s["id"] == "s02_clip"][0]["clip"]
    assert clip["frames"] == 60 and clip["every"] == 3 and clip["kept"] == 21 and clip["poster"] == -1
    from PIL import Image
    full = Image.open(os.path.join(pub, "seq-test_full.gif"))
    total = 0
    for i in range(full.n_frames):
        full.seek(i)
        total += full.info["duration"]
    clip_ms = 60 * 1000 / 59.7275
    assert abs(total - (2000 + clip_ms + 3000)) < 60, total     # first still + clip at game speed + last still


# ------------------------------------------------------------------ NES (Mesen libretro core)
def test_nes_header_and_game_genie():
    sys.path.insert(0, os.path.dirname(__file__))
    import make_nes_rom
    h = platforms.Nes.identify(make_nes_rom.build())
    assert h["platform"] == "nes" and h["model"] == "ntsc" and h["mapper"] == 0 and h["prg_kib"] == 16
    assert h["battery"] and h["ram_kib"] == 8 and h["chr_kib"] == 0
    nes2 = bytearray(b"NES\x1a" + bytes([2, 1, 0x12, 0x48, 0x10, 0, 0x70, 0, 1, 0, 0, 0]))
    h = platforms.Nes.identify(bytes(nes2))
    assert h["format"] == "NES 2.0" and h["mapper"] == 0x41 and h["submapper"] == 1 and h["region"] == "PAL"
    assert h["model"] == "pal" and h["ram_kib"] == 8
    N = platforms.Nes
    assert N.game_genie("SXIOPO") == (0x91D9, 0xAD, None)           # nesdev wiki examples
    assert N.game_genie("ZEXPYGLA") == (0x94A7, 0x02, 0x03)
    rom = bytearray(b"NES\x1a" + bytes([4, 0, 0, 0]) + bytes(8) + bytes(0x10000))
    rom[16 + 0x14A7], rom[16 + 0x34A7], rom[16 + 0x54A7] = 3, 3, 9
    assert N.apply_game_genie(rom, "ZEXPYGLA") == [16 + 0x14A7, 16 + 0x34A7] and rom[16 + 0x14A7] == 2
    with pytest.raises(ValueError):
        N.apply_game_genie(rom, "SXIOPO")                           # 6 letters, bank-switched: ambiguous
    small = bytearray(b"NES\x1a" + bytes([1, 0, 0, 0]) + bytes(8) + bytes(0x4000))
    assert N.apply_game_genie(small, "SXIOPO") == [16 + 0x11D9] and small[16 + 0x11D9] == 0xAD


def test_nes_backend(nes_selftest, tmp_path):
    from PIL import Image
    import io
    e = platforms.Nes().open(str(nes_selftest))
    e.frames(30)
    px = lambda: Image.open(io.BytesIO(e.screen())).convert("RGB").getpixel((100, 100))
    blue = px()
    assert blue[2] > 200 and e.peek(0x11, 1) == b"\x00" and e.regs()["pc"].startswith("c0")
    assert e.peek(0xFFFC, 2) == b"\x00\xc0"                        # PRG through the mapper
    e.input(["a"])
    e.frames(5)
    red = px()
    assert red[0] > 150 and red[2] < 100 and e.peek(0x11, 1) == b"\x01"
    st = str(tmp_path / "x.state")
    e.save_state(st)
    count = e.peek(0x10, 1)[0]
    e.input([])
    e.frames(5)
    assert px() == blue
    e.ram_search("new == old")
    e.frames(3)
    r = e.ram_search("new == old + 3")
    assert [x["addr"] for x in r["results"]] == ["0010", "6000"]
    e.poke(0x10, b"\x80")
    e.frames(1)
    assert e.peek(0x10, 1) == b"\x81" and e.battery(0)[0] == 0x81 and len(e.battery(0)) == 8192
    e2 = platforms.Nes().open(str(nes_selftest))                    # two games at once in one process
    e2.load_state(st)
    assert e2.peek(0x10, 1)[0] == count and e.peek(0x10, 1) == b"\x81"
    e2.close()
    e.close()


def test_nes_state_keeps_frame_and_timing(nes_selftest, tmp_path):
    """A screenshot never advances emulation: played straight and loaded from a state give the same picture and
    the same frame count (a cached checkpoint must equal a freshly built one)."""
    st = str(tmp_path / "x.state")
    a = platforms.Nes().open(str(nes_selftest))
    assert a.peek(0x10, 1) == b"\x00" and a.screen() and a.peek(0x10, 1) == b"\x00"     # power-on picture: no frame run
    a.input(["a"])
    a.frames(40)
    a.save_state(st)
    shot, count = a.screen(), a.peek(0x10, 1)
    b = platforms.Nes().open(str(nes_selftest))
    b.load_state(st)
    assert b.screen() == shot and b.peek(0x10, 1) == count          # red frame kept, nothing emulated
    a.input([]); b.input([])
    a.frames(10); b.frames(10)
    assert a.screen() == b.screen() and a.peek(0x10, 1) == b.peek(0x10, 1)
    a.close()
    b.close()


def test_nes_pipeline(nes_selftest):
    run("tools/intake.py", str(nes_selftest), "--slug", NES_SLUG, "--probe", "120")
    gj = os.path.join(ROOT, "games", "nes", NES_SLUG, "game.json")
    meta = json.load(open(gj))
    assert meta["platform"] == "nes" and meta["model"] == "ntsc"
    meta["macros"] = {"TITLE": "w60"}
    meta["ram"] = {"joy": {"addr": "0012", "size": 1}}
    json.dump(meta, open(gj, "w"))
    P = ["tools/play.py", "--name", NES_SLUG]
    run(*P, "start", NES_SLUG)
    run(*P, "do", "TITLE")
    assert "saved" in run(*P, "checkpoint", "title", "after boot")
    run(*P, "do", "a+right:20")
    assert "joy=1" in run(*P, "status")
    run(*P, "snap", "held_a", "gameplay", "after A was held")
    assert "candidates" in run(*P, "find", "new == old")
    assert "early.sav" in run(*P, "export", "early", "frame counter in battery RAM", "--state")
    run(*P, "stop")
    assert "1/1 reproduce" in run("tools/shoot.py", NES_SLUG, "main", "--verify")
    run("tools/shoot.py", NES_SLUG, "main", "--publish-only")
    from PIL import Image
    im = Image.open(os.path.join(ROOT, "games", "nes", NES_SLUG, "shots", "main", "held_a.png")).convert("RGB")
    assert im.size == (256, 240) and im.getpixel((10, 10))[2] > 200
    d = os.path.join(ROOT, "games", "nes", NES_SLUG, "saves")
    assert os.path.getsize(os.path.join(d, "early.sav")) == 8192
    assert "Mesen" in open(os.path.join(d, "README.md")).read()
    g = emu.Game(NES_SLUG)
    e, rest, _ = emu.start(g, "sav:early")
    assert e.peek(0x6000, 1)[0] == open(os.path.join(d, "early.sav"), "rb").read()[0] != 0
    e.close()


# ------------------------------------------------------------------ SNES (Mesen-S libretro core)
SNES_SLUG = "zz-selftest-snes"


@pytest.fixture
def snes_selftest(tmp_path):
    if not os.path.exists(platforms.Snes.SO):
        pytest.skip("Mesen-S core not built (sh tools/setup_emu.sh snes)")
    sys.path.insert(0, os.path.dirname(__file__))
    import make_snes_rom
    rom = tmp_path / "t.sfc"
    rom.write_bytes(make_snes_rom.build())
    yield rom
    subprocess.run([sys.executable, os.path.join(ROOT, "tools", "play.py"), "--name", SNES_SLUG, "stop"],
                   capture_output=True)
    for sub in ("games/snes", "work/shots/snes", "work/cache/snes", "work/intake/snes", "work/play"):
        shutil.rmtree(os.path.join(ROOT, sub, SNES_SLUG), ignore_errors=True)
    if os.path.exists(os.path.join(ROOT, "rom", SNES_SLUG + ".sfc")):
        os.remove(os.path.join(ROOT, "rom", SNES_SLUG + ".sfc"))


def test_snes_header_and_cheats():
    sys.path.insert(0, os.path.dirname(__file__))
    import make_snes_rom
    S = platforms.Snes
    rom = make_snes_rom.build()
    h = S.identify(rom)
    assert h["platform"] == "snes" and h["model"] == "ntsc" and h["header_title"] == "GAMEDB SELFTEST"
    assert h["mapping"] == "LoROM" and h["cart_type"] == "ROM+RAM+BATTERY" and h["ram_kib"] == 8
    assert h["header_checksum_ok"] and not h["copier_header"]
    smc = bytes(512) + rom                                          # copier header
    h2 = S.identify(smc)
    assert h2["copier_header"] and h2["header_title"] == "GAMEDB SELFTEST" and h2["header_checksum_ok"]
    hi = bytearray(0x10000)                                         # HiROM, PAL region
    hi[0xFFC0:0xFFD5] = b"HIROM TEST".ljust(21)
    hi[0xFFD5:0xFFDA] = bytes([0x21, 0x00, 0x06, 0x00, 0x02])
    hi[0xFFDC:0xFFE0] = b"\xff\xff\x00\x00"
    hi[0xFFFC:0xFFFE] = b"\x00\x80"
    c = sum(hi) & 0xFFFF
    hi[0xFFDC:0xFFE0] = bytes([(c ^ 0xFFFF) & 0xFF, (c ^ 0xFFFF) >> 8, c & 0xFF, c >> 8])
    h3 = S.identify(bytes(hi))
    assert h3["mapping"] == "HiROM" and h3["model"] == "pal" and h3["region"] == "Europe" and h3["ram_kib"] == 0
    # Game Genie: decoded against the documented bit layout (encoded ijklqrst opabcduv wxefghmn -> a..x)
    lay = "ijklqrstopabcduvwxefghmn"
    for code in ("DD62-6DAD", "C2A7-0F6D", "1DF6-A4E3"):
        n = [platforms.SNES_GG.index(ch) for ch in code.replace("-", "")]
        enc = 0
        for d in n[2:]:
            enc = enc << 4 | d
        bits = {lay[i]: (enc >> (23 - i)) & 1 for i in range(24)}
        addr = 0
        for ch in "abcdefghijklmnopqrstuvwx":
            addr = addr << 1 | bits[ch]
        assert S.game_genie(code) == (addr, n[0] << 4 | n[1], None)
    assert S.gameshark("7E0DBE05") == (None, 0x7E0DBE, 0x05)        # Pro Action Replay
    lo = bytearray(rom)
    assert S.rom_offset(lo, 0x008123) == 0x0123 and S.rom_offset(smc, 0x808123) == 512 + 0x0123
    assert S.rom_offset(hi, 0xC01234) == 0x1234 and S.rom_offset(hi, 0x00FFC0) == 0xFFC0
    with pytest.raises(ValueError):
        S.rom_offset(lo, 0x7E0010)


def test_snes_backend(snes_selftest, tmp_path):
    from PIL import Image
    import io
    e = platforms.Snes().open(str(snes_selftest))
    assert e.peek(0x7E0010, 1) == b"\x00" and e.screen() and e.peek(0x7E0010, 1) == b"\x00"   # no frame run
    e.frames(30)
    img = lambda x: Image.open(io.BytesIO(x.screen())).convert("RGB")
    assert img(e).size == (256, 224) and img(e).getpixel((100, 100)) == (0, 0, 255)
    # core options are applied: power-on RAM is zero (the core's default is random), so the counter is exact
    assert e.peek(0x7E0012, 1) == b"\x00" and 25 <= e.peek(0x7E0010, 1)[0] <= 30
    assert e.peek(0x7E0011, 1) == b"\x00" and e.peek(0x000011, 1) == b"\x00" and e.regs()["pc"].startswith("0080")
    assert e.peek(0x008000, 2) == b"\x78\xd8"                      # ROM through the mapping
    e.input(["a"])
    e.frames(5)
    assert img(e).getpixel((100, 100)) == (255, 0, 0) and e.peek(0x7E0011, 1) == b"\x80"
    st = str(tmp_path / "x.state")
    e.save_state(st)
    shot, count = e.screen(), e.peek(0x7E0010, 1)
    b = platforms.Snes().open(str(snes_selftest))                   # two games at once; state keeps the frame
    b.load_state(st)
    assert b.screen() == shot and b.peek(0x7E0010, 1) == count
    e.input([]); b.input([])
    e.frames(10); b.frames(10)
    assert e.screen() == b.screen() and e.peek(0x7E0010, 1) == b.peek(0x7E0010, 1)
    b.close()
    e.ram_search("new == old")
    e.frames(3)
    assert [x["addr"] for x in e.ram_search("new == old + 3")["results"]] == ["7e0010"]
    e.poke(0x7E0010, b"\x80")
    e.frames(1)
    assert e.peek(0x7E0010, 1) == b"\x81" and e.battery(0)[0] == 0x81 and len(e.battery(0)) == 8192
    assert e.peek(0x700000, 1) == b"\x81"                           # battery RAM where LoROM maps it
    e.close()


def test_snes_pipeline(snes_selftest):
    run("tools/intake.py", str(snes_selftest), "--slug", SNES_SLUG, "--probe", "120")
    gj = os.path.join(ROOT, "games", "snes", SNES_SLUG, "game.json")
    meta = json.load(open(gj))
    assert meta["platform"] == "snes" and meta["model"] == "ntsc" and meta["title"] == "GAMEDB SELFTEST"
    meta["macros"] = {"TITLE": "w60"}
    meta["ram"] = {"joy": {"addr": "7E0012", "size": 1}}
    json.dump(meta, open(gj, "w"))
    P = ["tools/play.py", "--name", SNES_SLUG]
    run(*P, "start", SNES_SLUG)
    run(*P, "do", "TITLE")
    assert "saved" in run(*P, "checkpoint", "title", "after boot")
    run(*P, "do", "a+l:20,poke:7E0020=2A")
    assert "joy=128" in run(*P, "status")                           # exactly the A bit: RAM started at zero
    assert "2a" in run(*P, "peek", "7E0020", "1")
    run(*P, "snap", "held_a", "gameplay", "after A was held")
    assert "candidates" in run(*P, "find", "new == old")
    assert "early.sav" in run(*P, "export", "early", "frame counter in battery RAM", "--state")
    run(*P, "stop")
    assert "1/1 reproduce" in run("tools/shoot.py", SNES_SLUG, "main", "--verify")
    run("tools/shoot.py", SNES_SLUG, "main", "--publish-only")
    from PIL import Image
    im = Image.open(os.path.join(ROOT, "games", "snes", SNES_SLUG, "shots", "main", "held_a.png")).convert("RGB")
    assert im.size == (256, 224) and im.getpixel((10, 10)) == (0, 0, 255)
    d = os.path.join(ROOT, "games", "snes", SNES_SLUG, "saves")
    assert os.path.getsize(os.path.join(d, "early.sav")) == 8192
    assert "Mesen-S" in open(os.path.join(d, "README.md")).read()
    g = emu.Game(SNES_SLUG)
    e, rest, _ = emu.start(g, "sav:early")
    assert e.peek(0x700000, 1)[0] == open(os.path.join(d, "early.sav"), "rb").read()[0] != 0
    e.close()


# ------------------------------------------------------------------ DOS (DOSBox Pure libretro core)
DOS_SLUG = "zz-selftest-dos"
DOS_BOOT = "w120,enter,w60"         # start menu (one program: KEYS.COM), Enter runs it


@pytest.fixture
def dos_selftest(tmp_path):
    if not os.path.exists(platforms.Dos.SO):
        pytest.skip("DOSBox Pure core not built (sh tools/setup_emu.sh dos)")
    sys.path.insert(0, os.path.dirname(__file__))
    import make_dos_zip
    rom = tmp_path / "t.zip"
    rom.write_bytes(make_dos_zip.build())
    yield rom
    subprocess.run([sys.executable, os.path.join(ROOT, "tools", "play.py"), "--name", DOS_SLUG, "stop"],
                   capture_output=True)
    for sub in ("games/dos", "work/shots/dos", "work/cache/dos", "work/intake/dos", "work/play"):
        shutil.rmtree(os.path.join(ROOT, sub, DOS_SLUG), ignore_errors=True)
    if os.path.exists(os.path.join(ROOT, "rom", DOS_SLUG + ".zip")):
        os.remove(os.path.join(ROOT, "rom", DOS_SLUG + ".zip"))


def _dos_boot(rom):
    e = platforms.Dos().open(str(rom))
    e.frames(120)
    e.input(["enter"]); e.frames(4); e.input([]); e.frames(60)
    return e


def test_dos_identify():
    sys.path.insert(0, os.path.dirname(__file__))
    import make_dos_zip
    h = platforms.Dos.identify(make_dos_zip.build())
    assert h["platform"] == "dos" and h["programs"] == ["KEYS.COM"] and h["model"] == "svga-7800"
    assert platforms.by_extension("x/GAME.ZIP")[0] == "dos"
    assert {"a", "1", "f10", "enter", "esc", "kp8", "shift", "mouse1"} <= platforms.Dos.keys


def test_dos_backend(dos_selftest, tmp_path):
    e = _dos_boot(dos_selftest)
    assert e.peek(0x449, 1) == b"\x03"                              # BIOS data area: 80x25 text mode
    assert e.peek(0x417, 1) == b"\x00" and ":" in e.regs()["pc"]
    blank = e.screen()
    e.input(["shift"]); e.frames(6)
    assert e.peek(0x417, 1) == b"\x02"                              # left shift held, seen by the BIOS
    e.input([]); e.frames(6)
    assert e.peek(0x417, 1) == b"\x00"
    e.type_text("Hi!")
    typed = e.screen()
    assert typed != blank
    st = str(tmp_path / "x.state")
    e.save_state(st)
    ticks = e.peek(0x46C, 4)
    e.input(["x"]); e.frames(4); e.input([]); e.frames(20)
    assert e.screen() != typed and e.peek(0x46C, 4) != ticks
    e.poke(0x4F0, b"\x5a")                                          # inter-application area: free RAM
    assert e.peek(0x4F0, 1) == b"\x5a"
    e.load_state(st)
    assert e.screen() == typed and e.peek(0x46C, 4) == ticks and e.peek(0x4F0, 1) == b"\x00"
    e.close()


def test_dos_same_route_same_frames(dos_selftest, tmp_path):
    """The emulated clock and timing do not depend on the host: two power-ons give the same pictures and the
    same BIOS ticks, and a run continued after save_state equals one loaded from that state."""
    st = str(tmp_path / "x.state")

    def play(e):
        e.type_text("abc")
        e.frames(33)
        return e.screen(), e.peek(0x46C, 4), e.peek(0x400, 0x100)

    a, b = _dos_boot(dos_selftest), _dos_boot(dos_selftest)
    assert a.screen() == b.screen() and a.peek(0x46C, 4) == b.peek(0x46C, 4)
    assert play(a) == play(b)
    a.save_state(st)
    b.close()
    c = platforms.Dos().open(str(dos_selftest))
    c.frames(5)
    c.load_state(st)
    assert c.screen() == a.screen()
    assert play(a) == play(c)
    a.close()
    c.close()


def test_dos_state_carries_written_files(dos_selftest, tmp_path):
    """A savestate holds the machine, not the disk: the backend stores the files the game wrote with the state
    and puts them back on load (in the same machine and in a fresh one), and they export as the save."""
    before, after = str(tmp_path / "before.state"), str(tmp_path / "after.state")
    e = _dos_boot(dos_selftest)
    e.save_state(before)
    assert e.battery(0) == b""
    e.input(["w"]); e.frames(6); e.input([]); e.frames(30)             # KEYS.COM creates S.DAT
    assert list(platforms.Dos._files(e.battery(0))) == ["S.DAT"]
    e.save_state(after)
    shot = e.screen()
    # the launch stored with a state ends where the program started: it must not repeat the route's writes
    assert e._log is None and not any(k == "i" and "w" in v for k, v in e._launch)
    e.load_state(before)                                                # back to before the save: file gone
    assert e.battery(0) == b""
    e.load_state(after)
    assert list(platforms.Dos._files(e.battery(0))) == ["S.DAT"] and e.screen() == shot
    sav = tmp_path / "x.sav"
    sav.write_bytes(e.battery(0))
    e.close()
    f = platforms.Dos().open(str(dos_selftest))                         # fresh machine, nothing written
    f.load_state(after)
    assert list(platforms.Dos._files(f.battery(0))) == ["S.DAT"] and f.screen() == shot
    f.close()
    g = platforms.Dos().open(str(dos_selftest), sav=str(sav))           # power on with the exported save
    g.frames(30)
    assert list(platforms.Dos._files(g.battery(0))) == ["S.DAT"]
    g.close()


def test_dos_pipeline(dos_selftest):
    run("tools/intake.py", str(dos_selftest), "--slug", DOS_SLUG, "--probe", "150")
    gj = os.path.join(ROOT, "games", "dos", DOS_SLUG, "game.json")
    meta = json.load(open(gj))
    assert meta["platform"] == "dos" and meta["model"] == "svga-7800" and meta["rom"].endswith(".zip")
    meta["macros"] = {"BOOT": DOS_BOOT}
    meta["ram"] = {"shift": {"addr": "0417", "size": 1}}
    json.dump(meta, open(gj, "w"))
    P = ["tools/play.py", "--name", DOS_SLUG]
    run(*P, "start", DOS_SLUG)
    run(*P, "do", "BOOT")
    assert "saved" in run(*P, "checkpoint", "prompt", "KEYS.COM waiting for a key")
    run(*P, "do", "type:Go 1,f,1,w20")
    assert "shift=0" in run(*P, "status")
    run(*P, "snap", "typed", "gameplay", "keys typed, tick letters between them")
    run(*P, "stop")
    assert "1/1 reproduce" in run("tools/shoot.py", DOS_SLUG, "main", "--verify")
    run("tools/shoot.py", DOS_SLUG, "main", "--publish-only")
    from PIL import Image
    im = Image.open(os.path.join(ROOT, "games", "dos", DOS_SLUG, "shots", "main", "typed.png")).convert("RGB")
    assert im.size == (640, 400) and im.crop((0, 0, 200, 16)).getextrema()[0][1] > 100


# ------------------------------------------------------------------ Apple II (AppleWin libretro core)
A2_SLUG = "zz-selftest-apple2"
A2_DOS33 = os.path.join(ROOT, "tools", "applewin", "bin", "DOS 3.3 System Master - 680-0210-A.dsk")


def _a2_zip(path):
    """Two sides: an empty disk first (does not boot), the test program second."""
    import zipfile
    sys.path.insert(0, os.path.dirname(__file__))
    import make_apple2_disk
    with zipfile.ZipFile(path, "w") as z:
        z.writestr("Side A.dsk", bytes(143360))
        z.writestr("Side B.dsk", make_apple2_disk.build())
    return path


@pytest.fixture
def a2_selftest(tmp_path):
    if not os.path.exists(platforms.Apple2.SO):
        pytest.skip("AppleWin core not built (sh tools/setup_emu.sh apple2)")
    sys.path.insert(0, os.path.dirname(__file__))
    import make_apple2_disk
    rom = tmp_path / "t.dsk"
    rom.write_bytes(make_apple2_disk.build())
    yield rom
    subprocess.run([sys.executable, os.path.join(ROOT, "tools", "play.py"), "--name", A2_SLUG, "stop"],
                   capture_output=True)
    for sub in ("games/apple2", "work/shots/apple2", "work/cache/apple2", "work/intake/apple2", "work/play"):
        shutil.rmtree(os.path.join(ROOT, sub, A2_SLUG), ignore_errors=True)
    if os.path.exists(os.path.join(ROOT, "rom", A2_SLUG + ".zip")):
        os.remove(os.path.join(ROOT, "rom", A2_SLUG + ".zip"))


def _a2_row(e, row=0):
    """A text row as ASCII (screen codes: high bit set = normal video)."""
    return bytes(c & 0x7F for c in e.peek(0x400 + (row % 8) * 0x80 + (row // 8) * 0x28, 40)).decode().rstrip()


def test_apple2_identify(tmp_path):
    sys.path.insert(0, os.path.dirname(__file__))
    import make_apple2_disk, make_dos_zip
    h = platforms.Apple2.identify(make_apple2_disk.build())
    assert h["platform"] == "apple2" and h["model"] == "iie" and "140 KiB" in h["disks"][0]["kind"]
    z = _a2_zip(str(tmp_path / "two.zip"))
    h = platforms.Apple2.identify(open(z, "rb").read())
    assert [d["name"] for d in h["disks"]] == ["Side A.dsk", "Side B.dsk"] and len(h["disks"][1]["sha1"]) == 40
    assert platforms.by_extension(z)[0] == "apple2"                      # a ZIP of disk images
    d = tmp_path / "dos.zip"
    d.write_bytes(make_dos_zip.build())
    assert platforms.by_extension(str(d))[0] == "dos"                    # any other ZIP
    assert platforms.by_extension("x/GAME.WOZ")[0] == "apple2" and platforms.by_extension("x/g.po")[0] == "apple2"
    assert {"a", "1", "enter", "esc", "left", "ctrl", "shift", "openapple", "joyup", "f"} <= platforms.Apple2.keys
    assert "f1" not in platforms.Apple2.keys


def test_apple2_backend(a2_selftest, tmp_path):
    e = platforms.Apple2().open(str(a2_selftest))
    e.frames(120)
    assert e.image().size == (560, 384) and _a2_row(e) == "" and e.regs()["pc"].startswith("08")
    assert e.peek(0xFBB3, 1) == b"\x06" and e.peek(0xFBC0, 1) == b"\xe0"    # machine ID bytes in ROM: enhanced //e
    for keys in (["h"], ["shift", "i"], ["1"], ["shift", "1"]):
        e.input(keys); e.frames(8); e.input([]); e.frames(20)
    assert _a2_row(e)[1::2] == "Hi1!"                                    # every second character is a timing letter
    e.type_text("Ab, 2+2=4")
    assert _a2_row(e)[1::2] == "Hi1!Ab, 2+2=4"
    typed = e.screen()
    st = str(tmp_path / "x.state")
    e.save_state(st)
    e.input(["x"]); e.frames(8); e.input([]); e.frames(20)
    assert e.screen() != typed
    e.poke(0x300, b"\x5a\xa5")
    assert e.peek(0x300, 2) == b"\x5a\xa5" and e.peek(0x300, 2, bank=0) == b"\x5a\xa5"
    with pytest.raises(ValueError):
        e.poke(0xF800, b"\x00")                                          # ROM
    e.poke(0x10300, b"\x77")                                             # auxiliary memory
    assert e.peek(0x10300, 1) == b"\x77" and e.peek(0x300, 1, bank=1) == b"\x77" and e.peek(0x300, 1) == b"\x5a"
    e.load_state(st)
    assert e.screen() == typed and e.peek(0x300, 2) != b"\x5a\xa5"
    assert e.ram_search("new == old")["count"] == 0xC000
    e.close()
    with pytest.raises(SystemExit, match="unknown Apple II model"):
        platforms.Apple2().open(str(a2_selftest), model="iigs")
    m = platforms.Apple2().open(str(a2_selftest), model="iiplus-green-joy")
    m.frames(120)
    assert m.peek(0xFBB3, 1) == b"\xea"                                  # machine ID byte: II Plus
    m.close()


def test_apple2_same_route_same_frames(a2_selftest, tmp_path):
    """Nothing depends on the host: two power-ons give the same pictures and memory, and a run continued after
    save_state equals one loaded from that state into a machine that has not run yet (the test program prints a
    letter that depends on the exact cycle a key arrives)."""
    st = str(tmp_path / "x.state")

    def boot():
        e = platforms.Apple2().open(str(a2_selftest))
        e.frames(120)
        return e

    def play(e):
        for k, w in zip("gamedb", (3, 17, 5, 29, 11, 7)):
            e.input([k]); e.frames(3); e.input([]); e.frames(w)
        return e.screen(), e.peek(0, 0xC000)

    a, b = boot(), boot()
    assert a.screen() == b.screen() and a.peek(0, 0xC000) == b.peek(0, 0xC000)
    assert play(a) == play(b)
    a.save_state(st)
    b.close()
    c = platforms.Apple2().open(str(a2_selftest))
    c.load_state(st)
    assert c.screen() == a.screen()
    assert play(a) == play(c)
    a.close()
    c.close()


def test_apple2_disk_swap(a2_selftest, tmp_path):
    z = _a2_zip(str(tmp_path / "two.zip"))
    e = platforms.Apple2().open(z)
    assert e.disks == ["Side A.dsk", "Side B.dsk"] and e.drives[:2] == ["Side A.dsk", None]
    e.frames(200)
    assert not e.regs()["pc"].startswith("08") and _a2_row(e, 2)[:1] == "*"     # no boot code: the monitor
    st = str(tmp_path / "a.state")
    e.save_state(st)
    e.disk(2)
    e.type_text("6")                                                     # monitor prompt: 6 Ctrl-P = boot slot 6
    e.input(["ctrl", "p"]); e.frames(8); e.input([]); e.frames(8)
    e.type_text("\n")
    e.frames(200)
    assert e.drives[:2] == ["Side B.dsk", None] and e.regs()["pc"].startswith("08")
    e.disk(1, drive=2)
    assert e.drives[:2] == ["Side B.dsk", "Side A.dsk"]
    e.disk(1)                                                            # a disk is in one drive at a time
    assert e.drives[:2] == ["Side A.dsk", None]
    with pytest.raises(ValueError):
        e.disk(3)
    e.load_state(st)                                                     # the state knows which disk was in
    assert e.drives[:2] == ["Side A.dsk", None]
    e.frames(200)
    assert not e.regs()["pc"].startswith("08")
    e.close()


def test_apple2_state_carries_disk_writes(tmp_path):
    """Apple II games save by writing to the floppy. A savestate keeps the machine; the backend stores the
    changed parts of the disk images with it and puts them back on load. Uses the DOS 3.3 master that comes
    with the AppleWin source (never committed)."""
    if not os.path.exists(platforms.Apple2.SO) or not os.path.exists(A2_DOS33):
        pytest.skip("AppleWin core not built (sh tools/setup_emu.sh apple2)")
    import io, zipfile
    before, after = str(tmp_path / "before.state"), str(tmp_path / "after.state")

    def catalog(e):
        e.type_text("CATALOG\n")
        out = ""
        for _ in range(3):
            e.frames(200)
            out += "\n".join(_a2_row(e, r) for r in range(24))
            e.type_text(" ")                                             # next page
        e.frames(200)
        return out

    e = platforms.Apple2().open(A2_DOS33)
    e.frames(600)
    e.save_state(before)
    assert e.battery(0) == b""
    e.type_text('10 PRINT "HI"\nSAVE GAMEDB\n')
    e.frames(400)
    sav = e.battery(0)
    assert zipfile.ZipFile(io.BytesIO(sav)).namelist() == ["disk.dsk"]
    e.save_state(after)
    assert os.path.getsize(after) < 200000                              # changed blocks only, not the image
    assert "GAMEDB" in catalog(e)
    e.load_state(before)                                                # back to before the save
    assert e.battery(0) == b"" and "GAMEDB" not in catalog(e)
    e.close()
    f = platforms.Apple2().open(A2_DOS33)                               # fresh machine, pristine disk
    f.load_state(after)
    assert f.battery(0) == sav and "GAMEDB" in catalog(f)
    f.close()
    (tmp_path / "x.sav").write_bytes(sav)
    g = platforms.Apple2().open(A2_DOS33, sav=str(tmp_path / "x.sav"))  # power on with the exported save
    g.frames(600)
    assert "GAMEDB" in catalog(g)
    g.close()


def test_apple2_pipeline(a2_selftest, tmp_path):
    z = _a2_zip(str(tmp_path / (A2_SLUG + ".zip")))
    run("tools/intake.py", z, "--slug", A2_SLUG, "--probe", "120")
    gj = os.path.join(ROOT, "games", "apple2", A2_SLUG, "game.json")
    meta = json.load(open(gj))
    assert meta["platform"] == "apple2" and meta["model"] == "iie" and meta["rom"].endswith(".zip")
    assert [d["name"] for d in meta["header"]["disks"]] == ["Side A.dsk", "Side B.dsk"]
    meta["macros"] = {"BOOT": "w200,disk:2,6,ctrl+p,enter,w200"}
    meta["ram"] = {"cursor": {"addr": "0024", "size": 1}}
    json.dump(meta, open(gj, "w"))
    P = ["tools/play.py", "--name", A2_SLUG]
    run(*P, "start", A2_SLUG)
    run(*P, "do", "BOOT")
    assert "saved" in run(*P, "checkpoint", "ready", "test program waiting for a key")
    run(*P, "do", "type:GO 1,f,shift+1,w20")
    assert "cursor=12" in run(*P, "status")                             # six keys, two characters each
    run(*P, "snap", "typed", "gameplay", "keys typed, timing letters between them")
    run(*P, "stop")
    assert "1/1 reproduce" in run("tools/shoot.py", A2_SLUG, "main", "--verify")
    run("tools/shoot.py", A2_SLUG, "main", "--publish-only")
    from PIL import Image
    im = Image.open(os.path.join(ROOT, "games", "apple2", A2_SLUG, "shots", "main", "typed.png")).convert("RGB")
    assert im.size == (560, 384) and im.crop((0, 0, 200, 16)).getextrema()[0][1] > 100
