"""Shared tooling tests: tokens, routes, header identification (no emulator), and the whole pipeline on gbemu's generated
test ROM (skipped when tools/gbemu-cli is not built) and on a generated NES test ROM (skipped when the Mesen
core is not built), a generated SNES test ROM (skipped when the Mesen-S core is not built), a generated DOS
test program (skipped when the DOSBox Pure core is not built) and a generated Apple II test disk (skipped when
the AppleWin core is not built)."""
import json, os, re, shutil, subprocess, sys

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
    from PIL import Image
    run("tools/intake.py", str(selftest), "--slug", SLUG, "--region", "na", "--probe", "120")
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
    name = "zz-selftest_gb_na_gameplay_%s.png"          # <game>_<platform>_<region>_<category>_<id>
    assert "oops" not in open(os.path.join(d, "shots.txt")).read() and not os.path.exists(os.path.join(d, name % "oops"))
    run(*P, "snap", "moved", "menu", "category changes")
    run(*P, "snap", "moved", "gameplay", "category changed: the file follows it")
    assert os.path.exists(os.path.join(d, name % "moved")) and not os.path.exists(os.path.join(d, "3x"))
    assert not [f for f in os.listdir(d) if "_menu_" in f]
    # the same picture under a second id: said at once, not at the final verify
    assert "IDENTICAL picture to: a_shot, moved" in run(*P, "snap", "twin", "gameplay", "the same frame again")
    run(*P, "unsnap", "twin")
    # pictures are native size unless asked for (an enlarged one costs several times more to look at)
    assert Image.open(os.path.join(ROOT, run(*P, "shot").strip())).size == (160, 144)
    assert Image.open(os.path.join(ROOT, run(*P, "shot", "--scale", "2").strip())).size == (320, 288)
    assert re.search(r"call=\d+ pc=", run(*P, "status"))                     # budgets are counted in calls
    run(*P, "unsnap", "moved")
    run(*P, "stop")
    out = run("tools/shoot.py", SLUG, "main", "--verify")
    assert "1/1 reproduce" in out
    run("tools/shoot.py", SLUG, "main", "--publish-only")
    idx = json.load(open(os.path.join(ROOT, "games", "gb", SLUG, "shots", "main", "index.json")))
    s = idx["shots"][0]
    assert s["id"] == "a_shot" and s["route"] == "@title,right:20,a,settle" and s["rom_sha1"] == meta["sha1"]
    pub = os.path.join(ROOT, "games", "gb", SLUG, "shots", "main")
    assert Image.open(os.path.join(pub, name % "a_shot")).size == (160, 144)
    assert s["file"] == name % "a_shot" and "file_3x" not in s and idx["game"]["region"] == "na"
    assert len(s["pixel_sha1"]) == 40 and not os.path.exists(os.path.join(pub, "3x"))
    assert "3x/" not in open(os.path.join(pub, "index.md")).read()
    # enlarged copies on demand: tools/x3.py, into 3x/ next to the originals (ignored by git)
    run("tools/x3.py", pub)
    assert Image.open(os.path.join(pub, "3x", name % "a_shot")).size == (480, 432)
    shutil.rmtree(os.path.join(pub, "3x"))
    assert os.path.exists(os.path.join(pub, "zz-selftest_gb_na_set_sheet.png"))    # set files: area field `set`
    # a category changed by hand in index.json, or a set made before the scheme: the next run renames the files
    work = os.path.join(ROOT, "work", "shots", "gb", SLUG, "main")
    wi = json.load(open(os.path.join(work, "index.json")))
    wi["shots"][0]["category"] = "menu"
    json.dump(wi, open(os.path.join(work, "index.json"), "w"))
    lines = open(os.path.join(work, "shots.txt")).read().replace("a_shot | gameplay", "a_shot | menu")
    open(os.path.join(work, "shots.txt"), "w").write(lines)
    out = run("tools/shoot.py", SLUG, "main", "--verify")
    assert "renamed" in out and "1/1 reproduce" in out
    assert os.path.exists(os.path.join(work, "zz-selftest_gb_na_menu_a_shot.png"))
    run("tools/shoot.py", SLUG, "main", "--publish-only")
    assert sorted(f for f in os.listdir(pub) if f.endswith(".png")) == [
        "zz-selftest_gb_na_menu_a_shot.png", "zz-selftest_gb_na_set_sheet.png"]      # the old name is removed


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
    run("tools/intake.py", str(selftest), "--slug", SLUG, "--region", "na", "--probe", "0")
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
    run("tools/intake.py", str(selftest), "--slug", SLUG, "--region", "na", "--probe", "0")
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
    run("tools/intake.py", str(selftest), "--slug", SLUG, "--region", "na", "--probe", "0")
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
    for name in ("gameplay_seq-test_s01_start.png", "gameplay_seq-test_s02_clip.gif",
                 "gameplay_seq-test_s02_clip.png", "gameplay_seq-test_s03_after.png", "set_seq-test_strip.png",
                 "set_seq-test_steps.gif", "set_seq-test_full.gif", "set_seq-test_sheet.png"):
        assert os.path.exists(os.path.join(pub, "zz-selftest_gb_na_" + name)), name    # sequence ids carry the set name
    assert not os.path.exists(os.path.join(pub, "3x"))                      # enlarged copies only on demand
    assert not [f for f in os.listdir(pub) if f.endswith((".png", ".gif")) and "_seq-test_" not in f]
    idx = json.load(open(os.path.join(pub, "index.json")))
    clip = [s for s in idx["shots"] if s["id"] == "s02_clip"][0]["clip"]
    assert clip["frames"] == 60 and clip["every"] == 3 and clip["kept"] == 21 and clip["poster"] == -1
    from PIL import Image
    full = Image.open(os.path.join(pub, "zz-selftest_gb_na_set_seq-test_full.gif"))
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
    run("tools/intake.py", str(nes_selftest), "--slug", NES_SLUG, "--region", "na", "--probe", "120")
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
    im = Image.open(os.path.join(ROOT, "games", "nes", NES_SLUG, "shots", "main",
                                 "zz-selftest-nes_nes_na_gameplay_held_a.png")).convert("RGB")
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
    run("tools/intake.py", str(snes_selftest), "--slug", SNES_SLUG, "--region", "na", "--probe", "120")
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
    im = Image.open(os.path.join(ROOT, "games", "snes", SNES_SLUG, "shots", "main",
                                 "zz-selftest-snes_snes_na_gameplay_held_a.png")).convert("RGB")
    assert im.size == (256, 224) and im.getpixel((10, 10)) == (0, 0, 255)
    d = os.path.join(ROOT, "games", "snes", SNES_SLUG, "saves")
    assert os.path.getsize(os.path.join(d, "early.sav")) == 8192
    assert "Mesen-S" in open(os.path.join(d, "README.md")).read()
    g = emu.Game(SNES_SLUG)
    e, rest, _ = emu.start(g, "sav:early")
    assert e.peek(0x700000, 1)[0] == open(os.path.join(d, "early.sav"), "rb").read()[0] != 0
    e.close()


# ------------------------------------------------------------------ Master System (Genesis Plus GX libretro core)
SMS_SLUG = "zz-selftest-sms"


@pytest.fixture
def sms_selftest(tmp_path):
    if not os.path.exists(platforms.Sms.SO):
        pytest.skip("Genesis Plus GX core not built (sh tools/setup_emu.sh sms)")
    sys.path.insert(0, os.path.dirname(__file__))
    import make_sms_rom
    rom = tmp_path / "t.sms"
    rom.write_bytes(make_sms_rom.build())
    yield rom
    subprocess.run([sys.executable, os.path.join(ROOT, "tools", "play.py"), "--name", SMS_SLUG, "stop"],
                   capture_output=True)
    for sub in ("games/sms", "work/shots/sms", "work/cache/sms", "work/intake/sms", "work/play"):
        shutil.rmtree(os.path.join(ROOT, sub, SMS_SLUG), ignore_errors=True)
    if os.path.exists(os.path.join(ROOT, "rom", SMS_SLUG + ".sms")):
        os.remove(os.path.join(ROOT, "rom", SMS_SLUG + ".sms"))


def test_sms_header_and_cheats():
    sys.path.insert(0, os.path.dirname(__file__))
    import make_sms_rom
    S = platforms.Sms
    rom = make_sms_rom.build()
    h = S.identify(rom)
    assert h["platform"] == "sms" and h["model"] == "ntsc" and h["region"] == "Export"
    assert h["header_checksum_ok"] and h["product_code"] == "12345" and h["version"] == 1 and h["rom_kib"] == 64
    jp = bytearray(rom)
    jp[0x7FFF] = 0x3E
    h2 = S.identify(bytes(jp))
    assert h2["region"] == "Japan" and h2["model"] == "ntsc-j" and h2["header_checksum_ok"]
    bad = bytearray(rom)
    bad[0x100] ^= 1
    assert not S.identify(bytes(bad))["header_checksum_ok"]
    assert S.identify(bytes(0x8000)) == {"header": False, "rom_kib": 32, "ram_kib": 32, "battery": h["battery"],
                                         "platform": "sms", "model": "ntsc"}     # most Japanese cartridges
    gg = bytearray(rom)
    gg[0x7FFF] = 0x6E
    with pytest.raises(SystemExit):
        S.identify(bytes(gg))                                       # Game Gear: not set up
    assert platforms.by_extension("x/GAME.SMS")[0] == "sms"
    assert S.gameshark("00C0-2509") == (None, 0xC025, 0x09)         # Pro Action Replay
    assert S.game_genie("3A7-6DF-E66") == platforms.GameBoy.game_genie("3A7-6DF-E66")
    small = bytearray(0x8000)                                       # no paging: the address is the offset
    assert S.game_genie("3A7-6D8") == (0x776D, 0x3A, None)
    assert S.apply_game_genie(small, "3A7-6D8") == [0x776D] and small[0x776D] == 0x3A
    paged = bytearray(0x10000)
    addr, value, cmp_ = S.game_genie("3A7-6DF-E66")
    for o in range(addr & 0x3FFF, len(paged), 0x4000):
        paged[o] = cmp_
    paged[(addr & 0x3FFF) + 0x4000] = 0                             # page 1 holds something else
    offs = S.apply_game_genie(paged, "3A7-6DF-E66")
    assert offs == [o for o in range(addr & 0x3FFF, 0x10000, 0x4000) if o != (addr & 0x3FFF) + 0x4000]
    assert all(paged[o] == value for o in offs)
    with pytest.raises(ValueError):
        S.apply_game_genie(bytearray(0x10000), "3A7-6DF")            # paged game, no compare byte


def test_sms_backend(sms_selftest, tmp_path):
    from PIL import Image
    import io
    e = platforms.Sms().open(str(sms_selftest))
    e.frames(30)
    img = lambda x: Image.open(io.BytesIO(x.screen())).convert("RGB")
    assert img(e).size == (256, 192) and img(e).getpixel((100, 100)) == (0, 0, 255)
    assert 25 <= e.peek(0xC010, 1)[0] <= 30 and e.peek(0xC012, 1) == b"\x00" and e.peek(0xC100, 1) == b"\x00"
    assert e.peek(0x0000, 3) == b"\xc3\x80\x00" and 0x80 <= int(e.regs()["pc"], 16) < 0x100
    e.input(["b1"])
    e.frames(5)
    assert img(e).getpixel((100, 100)) == (255, 0, 0) and e.peek(0xC011, 1) == b"\x10"
    e.input(["pause"]); e.frames(3); e.input([]); e.frames(3)
    assert e.peek(0xC013, 1) == b"\x01"                             # Pause is the NMI
    st = str(tmp_path / "x.state")
    e.save_state(st)
    shot, count = e.screen(), e.peek(0xC010, 1)
    b = platforms.Sms().open(str(sms_selftest))                     # two games at once; state keeps the frame
    b.load_state(st)
    assert b.screen() == shot and b.peek(0xC010, 1) == count
    assert b.battery(0) == e.battery(0) and b.battery(0)[0] == count[0]    # the state carries cartridge RAM
    e.frames(10); b.frames(10)
    assert e.screen() == b.screen() and e.peek(0xC010, 1) == b.peek(0xC010, 1)
    b.close()
    e.ram_search("new == old")
    e.frames(3)
    assert [x["addr"] for x in e.ram_search("new == old + 3")["results"]] == ["c010"]
    e.poke(0xC010, b"\x80")
    e.frames(1)
    assert e.peek(0xC010, 1) == b"\x81" and e.peek(0x8000, 1) == b"\x81"   # cartridge RAM mapped at 8000
    assert e.battery(0)[0] == 0x81 and len(e.battery(0)) == 0x8000
    with pytest.raises(ValueError):
        e.poke(0x0100, b"\x00")                                     # ROM
    sav = tmp_path / "x.sav"
    sav.write_bytes(e.battery(0))
    e.close()
    j = platforms.Sms().open(str(sms_selftest), model="ntsc-j", sav=str(sav))
    assert j.peek(0xC100, 1) == b"\xf0" and j.battery(0)[0] == 0x81    # Japanese console: RAM starts at F0
    j.close()


def test_sms_pipeline(sms_selftest):
    run("tools/intake.py", str(sms_selftest), "--slug", SMS_SLUG, "--region", "na", "--probe", "120")
    gj = os.path.join(ROOT, "games", "sms", SMS_SLUG, "game.json")
    meta = json.load(open(gj))
    assert meta["platform"] == "sms" and meta["model"] == "ntsc"
    meta["macros"] = {"TITLE": "w60"}
    meta["ram"] = {"b1": {"addr": "C012", "size": 1}}
    json.dump(meta, open(gj, "w"))
    P = ["tools/play.py", "--name", SMS_SLUG]
    run(*P, "start", SMS_SLUG)
    run(*P, "do", "TITLE")
    assert "saved" in run(*P, "checkpoint", "title", "after boot")
    run(*P, "do", "b1+right:20,poke:C020=2A")
    assert "b1=16" in run(*P, "status")                             # the sticky button-1 byte
    assert "2a" in run(*P, "peek", "C020", "1")
    run(*P, "snap", "held_b1", "gameplay", "after button 1 was held")
    assert "candidates" in run(*P, "find", "new == old")
    assert "early.sav" in run(*P, "export", "early", "frame counter in cartridge RAM", "--state")
    run(*P, "stop")
    assert "1/1 reproduce" in run("tools/shoot.py", SMS_SLUG, "main", "--verify")
    run("tools/shoot.py", SMS_SLUG, "main", "--publish-only")
    from PIL import Image
    im = Image.open(os.path.join(ROOT, "games", "sms", SMS_SLUG, "shots", "main",
                                 "zz-selftest-sms_sms_na_gameplay_held_b1.png")).convert("RGB")
    assert im.size == (256, 192) and im.getpixel((10, 10)) == (0, 0, 255)
    d = os.path.join(ROOT, "games", "sms", SMS_SLUG, "saves")
    assert os.path.getsize(os.path.join(d, "early.sav")) == 0x8000
    assert "Genesis Plus GX" in open(os.path.join(d, "README.md")).read()
    g = emu.Game(SMS_SLUG)
    e, rest, _ = emu.start(g, "sav:early")
    assert e._sram()[0] == open(os.path.join(d, "early.sav"), "rb").read()[0] != 0
    e.close()


# ------------------------------------------------------------------ Mega Drive / Genesis (Genesis Plus GX core)
MD_SLUG = "zz-selftest-md"


@pytest.fixture
def md_selftest(tmp_path):
    if not os.path.exists(platforms.MegaDrive.SO):
        pytest.skip("Genesis Plus GX core not built (sh tools/setup_emu.sh md)")
    sys.path.insert(0, os.path.dirname(__file__))
    import make_md_rom
    rom = tmp_path / "t.md"
    rom.write_bytes(make_md_rom.build())
    yield rom
    subprocess.run([sys.executable, os.path.join(ROOT, "tools", "play.py"), "--name", MD_SLUG, "stop"],
                   capture_output=True)
    for sub in ("games/md", "work/shots/md", "work/cache/md", "work/intake/md", "work/play", "work/roms"):
        shutil.rmtree(os.path.join(ROOT, sub, MD_SLUG), ignore_errors=True)
    if os.path.exists(os.path.join(ROOT, "rom", MD_SLUG + ".md")):
        os.remove(os.path.join(ROOT, "rom", MD_SLUG + ".md"))


def test_md_header_and_cheats():
    sys.path.insert(0, os.path.dirname(__file__))
    import make_md_rom
    M = platforms.MegaDrive
    rom = make_md_rom.build()
    h = M.identify(rom)
    assert h["platform"] == "md" and h["model"] == "ntsc" and h["region"] == "Japan, North America, Europe"
    assert h["header_checksum_ok"] and h["product_code"] == "GM 12345678-01" and h["rom_kib"] == 128
    assert h["header_title"] == "GAMEDB SELFTEST" and not h["six_button"] and "200001-203FFF" in h["battery"]
    for reg, region, model in ((b"J  ", "Japan", "ntsc-j"), (b"E  ", "Europe", "pal"), (b"4  ", "North America", "ntsc"),
                               (b"9  ", "Japan, Europe", "ntsc-j")):
        r = bytearray(rom)
        r[0x1F0:0x1F3] = reg
        assert (M.identify(bytes(r))["region"], M.identify(bytes(r))["model"]) == (region, model)
    bad = bytearray(rom)
    bad[0x300] ^= 1
    assert not M.identify(bytes(bad))["header_checksum_ok"]
    assert M.identify(bytes(0x8000))["header"] is False
    with pytest.raises(SystemExit):
        M.identify(bytes(8) + b"\xaa\xbb" + bytes(0x4200 - 10))          # interleaved .smd dump
    assert platforms.by_extension("x/GAME.MD")[0] == "md" and platforms.by_extension("x/g.gen")[0] == "md"
    assert platforms.by_extension("x/g.bin")[0] == "md"
    assert M.gameshark("FF0200:1234") == (None, 0xFF0200, b"\x12\x34")     # even address: the word
    assert M.gameshark("FF0301:0056") == (None, 0xFF0301, b"\x56")         # odd address: the byte
    with pytest.raises(ValueError):
        M.gameshark("FF0301:1234")
    # Game Genie: same decoding as the core (checked against retro_cheat_set on the test ROM)
    assert M.game_genie("RFAA-A6VR") == (0x402E, 0x4E71, None)
    assert M.game_genie("BBCA-ABCD") == (0x4442, 0x8008, None)
    r = bytearray(rom)
    assert M.apply_game_genie(r, "RFAA-A6VR") == [0x402E] and r[0x402E:0x4030] == b"\x4e\x71"
    with pytest.raises(ValueError):
        M.game_genie("RFAA-A6VI")                                   # I is not a Game Genie letter


def test_md_backend(md_selftest, tmp_path):
    from PIL import Image
    import io
    M = platforms.MegaDrive
    e = M().open(str(md_selftest))
    e.frames(30)
    img = lambda x: Image.open(io.BytesIO(x.screen())).convert("RGB")
    assert img(e).size == (320, 224) and img(e).getpixel((100, 100)) == (0, 0, 238)
    assert 25 <= e.peek(0xFF0010, 1)[0] <= 30 and e.peek(0xFF0012, 1) == b"\x00"
    assert e.peek(0, 8) == bytes.fromhex("00fffe0000000200") and e.peek(0x10000, 4) == b"PG2!"
    assert 0x200 <= int(e.regs()["pc"], 16) < 0x300 and len(e.regs()["pc"]) == 6
    e.input(["a"])
    e.frames(5)
    assert img(e).getpixel((100, 100)) == (238, 0, 0) and e.peek(0xFF0011, 1) == b"\x01"
    for key, bit in (("start", 2), ("b", 4), ("c", 8), ("up", 0x10), ("down", 0x20), ("left", 0x40), ("right", 0x80)):
        e.input([key])
        e.frames(2)
        assert e.peek(0xFF0011, 1)[0] == bit, key
    e.input([])
    e.frames(2)
    assert e.peek(0xFF0011, 2) == b"\x00\xff"
    with pytest.raises(ValueError):
        e.peek(0xC00004, 1)                                         # VDP: never read by peek (side effects)
    st = str(tmp_path / "x.state")
    e.save_state(st)
    shot, count = e.screen(), e.peek(0xFF0010, 1)
    b = M().open(str(md_selftest))                                  # two games at once; state keeps the frame
    b.load_state(st)
    assert b.screen() == shot and b.peek(0xFF0010, 1) == count
    assert b.battery(0) == e.battery(0) and b.battery(0)[1] == count[0]    # the state carries cartridge RAM
    e.frames(10); b.frames(10)
    assert e.screen() == b.screen() and e.peek(0xFF0010, 1) == b.peek(0xFF0010, 1)
    b.close()
    with pytest.raises(SystemExit):
        platforms.Sms().open(str(md_selftest)).load_state(st)      # another platform's state: refused
    e.ram_search("new == old")
    e.frames(3)
    assert [x["addr"] for x in e.ram_search("new == old + 3")["results"]] == ["ff0010"]
    e.poke(0xFF0010, b"\x80")
    e.frames(1)
    assert e.peek(0xFF0010, 1) == b"\x81" and e.peek(0x200001, 1) == b"\x81"   # cartridge RAM mapped at 200000
    assert e.battery(0)[1] == 0x81 and len(e.battery(0)) == 0x10000 and e.battery(0)[2] == 0xFF
    e.poke(0xFF0100, b"\x12\x34")
    e.ram_search_reset()
    e.poke(0xFF0100, b"\x12\x35")
    assert "ff0100" in [x["addr"] for x in e.ram_search("new == old + 1", wide=True)["results"]]   # big-endian
    e.poke(0xA00010, b"\x56")
    assert e.peek(0xA02010, 1) == b"\x56"                           # Z80 RAM, mirrored
    with pytest.raises(ValueError):
        e.poke(0x000200, b"\x00")                                   # ROM
    sav = tmp_path / "x.sav"
    sav.write_bytes(e.battery(0))
    e.close()
    j = M().open(str(md_selftest), model="pal", sav=str(sav))
    assert j.battery(0)[1] == 0x81
    j.frames(50)
    assert 45 <= j.peek(0xFF0010, 1)[0] <= 50                      # the counter starts again; the save is there
    j.close()


def test_md_pipeline(md_selftest):
    run("tools/intake.py", str(md_selftest), "--slug", MD_SLUG, "--region", "na", "--probe", "120")
    gj = os.path.join(ROOT, "games", "md", MD_SLUG, "game.json")
    meta = json.load(open(gj))
    assert meta["platform"] == "md" and meta["model"] == "ntsc" and meta["header"]["product_code"] == "GM 12345678-01"
    meta["macros"] = {"TITLE": "w60"}
    meta["ram"] = {"pad": {"addr": "FF0012", "size": 1}, "w": {"addr": "FF0040", "size": 2, "fmt": "hex"},
                   "n": {"addr": "FF0040", "size": 2}}
    meta["rom_variants"] = {"gg": {"gg": ["RFAA-A6VR"]}}
    json.dump(meta, open(gj, "w"))
    P = ["tools/play.py", "--name", MD_SLUG]
    run(*P, "start", MD_SLUG)
    run(*P, "do", "TITLE")
    assert "saved" in run(*P, "checkpoint", "title", "after boot")
    run(*P, "do", "a+right:20,poke:FF0020=2A,gs:FF0030:1234,set:FF0040=4660:2")
    st = run(*P, "status")
    assert "pad=129" in st                                          # the sticky pad byte: A and right
    assert "w=$1234" in st and "n=4660" in st                       # 68000: big-endian by default
    assert "2a" in run(*P, "peek", "FF0020", "1")
    assert "12 34" in run(*P, "peek", "FF0030", "2")
    run(*P, "snap", "held_a", "gameplay", "after button A was held")
    assert "candidates" in run(*P, "find", "new == old")
    assert "early.sav" in run(*P, "export", "early", "frame counter in cartridge RAM", "--state")
    run(*P, "stop")
    assert "1/1 reproduce" in run("tools/shoot.py", MD_SLUG, "main", "--verify")
    run("tools/shoot.py", MD_SLUG, "main", "--publish-only")
    from PIL import Image
    im = Image.open(os.path.join(ROOT, "games", "md", MD_SLUG, "shots", "main",
                                 "zz-selftest-md_md_na_gameplay_held_a.png")).convert("RGB")
    assert im.size == (320, 224) and im.getpixel((10, 10)) == (0, 0, 238)
    d = os.path.join(ROOT, "games", "md", MD_SLUG, "saves")
    assert os.path.getsize(os.path.join(d, "early.sav")) == 0x10000
    assert "Genesis Plus GX" in open(os.path.join(d, "README.md")).read()
    g = emu.Game(MD_SLUG)
    e, rest, _ = emu.start(g, "sav:early")
    assert e._sram()[1] == open(os.path.join(d, "early.sav"), "rb").read()[1] != 0xFF
    e.close()
    e, rest, _ = emu.start(g, "rom:gg")
    assert e.peek(0x402E, 2) == b"\x4e\x71"
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


def test_dos_state_carries_writes_to_open_file(tmp_path):
    """A game that keeps its save file open (Wizardry I-III loaders): writes through the open handle reach the
    state's files at once, not only when the file is closed (core patch: GamedbMarkWritten)."""
    if not os.path.exists(platforms.Dos.SO):
        pytest.skip("DOSBox Pure core not built (sh tools/setup_emu.sh dos)")
    sys.path.insert(0, os.path.dirname(__file__))
    import make_dos_zip
    rom = tmp_path / "h.zip"
    rom.write_bytes(make_dos_zip.build_hold())
    st1, st2 = str(tmp_path / "1.state"), str(tmp_path / "2.state")
    e = platforms.Dos().open(str(rom))
    e.frames(120)
    e.input(["x"]); e.frames(4); e.input([]); e.frames(30)
    e.save_state(st1)
    assert platforms.Dos._files(e.battery(0)).get("D.DAT") == b"x......."
    e.input(["y"]); e.frames(4); e.input([]); e.frames(30)          # same handle, already marked once
    e.save_state(st2)
    assert platforms.Dos._files(e.battery(0)).get("D.DAT") == b"xy......"
    e.close()
    f = platforms.Dos().open(str(rom))                                  # fresh machine
    f.frames(5)
    f.load_state(st1)
    assert platforms.Dos._files(f.battery(0)).get("D.DAT") == b"x......."
    f.load_state(st2)
    assert platforms.Dos._files(f.battery(0)).get("D.DAT") == b"xy......"
    f.close()


def test_dos_start_menu_states(tmp_path):
    """Two programs in the ZIP: the core shows its start menu and makes no states there. A state taken in the
    menu is an input log; one taken in the program loads into a machine that is still in the menu (a new
    process loading a cached checkpoint) and continues exactly like the run that made it."""
    if not os.path.exists(platforms.Dos.SO):
        pytest.skip("DOSBox Pure core not built (sh tools/setup_emu.sh dos)")
    sys.path.insert(0, os.path.dirname(__file__))
    import make_dos_zip
    rom = tmp_path / "menu.zip"
    rom.write_bytes(make_dos_zip.build(menu=True))
    menu, prog = str(tmp_path / "menu.state"), str(tmp_path / "prog.state")

    def play(e):
        e.type_text("abc")
        e.frames(33)
        return e.screen(), e.peek(0x46C, 4)

    a = platforms.Dos().open(str(rom))
    a.frames(120)
    assert not a.c.L.retro_gamedb_running()                             # start menu: EXIT.COM, KEYS.COM
    a.save_state(menu)
    assert open(menu, "rb").read().startswith(platforms.Dos.BOOTLOG)
    a.input(["down"]); a.frames(8); a.input([]); a.frames(40)
    a.input(["enter"]); a.frames(8); a.input([]); a.frames(100)
    assert a.c.L.retro_gamedb_running() and a._log is None
    a.save_state(prog)
    assert open(prog, "rb").read().startswith(platforms.Dos.STATE)
    shot, want = a.screen(), play(a)
    for pre in (0, 3, 50):                                              # fresh, warming up, sitting in the menu
        b = platforms.Dos().open(str(rom))
        b.frames(pre)
        b.load_state(prog)
        assert b.screen() == shot and play(b) == want, pre
        b.close()
    a.load_state(menu)                                                  # back to the menu by replay
    assert not a.c.L.retro_gamedb_running() and a._ran == 120
    a.input(["down"]); a.frames(8); a.input([]); a.frames(40)
    a.input(["enter"]); a.frames(8); a.input([]); a.frames(100)
    assert a.screen() == shot and play(a) == want
    a.close()


def test_dos_text_screen_and_change_token(dos_selftest):
    e = _dos_boot(dos_selftest)
    e.type_text("Hi")
    lines = e.text()
    assert len(lines) == 25 and "H" in lines[0] and "i" in lines[0] and lines[0] == lines[0].rstrip()
    g = type("G", (), {"settle_limit": 300})()
    e.freezes = []
    e.input(["x"])
    ran = emu.changed(e, g, after=5)                                    # the key shows up: the picture changes
    e.input([])
    assert 5 < ran < 60 and "x" in e.text()[0]
    e.close()


def test_dos_pipeline(dos_selftest):
    run("tools/intake.py", str(dos_selftest), "--slug", DOS_SLUG, "--region", "na", "--probe", "150")
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
    route = run(*P, "route")
    # a bad token after a good one: `do` fails and rolls back, so the press of x is neither in the machine nor
    # in the route (it was both missing from the route and in the machine before: Wizardry III, 2026-11-19);
    # the verify below would see the extra key in the snaps
    r = subprocess.run([sys.executable] + P + ["do", "x,w30!"], cwd=ROOT, capture_output=True, text=True)
    assert r.returncode != 0 and "unknown token" in (r.stdout + r.stderr)
    assert run(*P, "route") == route
    run(*P, "do", "w,w30")                                              # KEYS.COM writes S.DAT: a save
    assert run(*P, "route").startswith("@prompt,")
    run(*P, "export", "s1", "after w")
    row = [l for l in open(os.path.join(ROOT, "games", "dos", DOS_SLUG, "saves", "README.md")) if l.startswith("| s1 |")]
    assert "@prompt" not in row[0] and "BOOT" in row[0]                 # the route from power-on, macros kept
    run(*P, "snap", "typed", "gameplay", "keys typed, tick letters between them")
    assert "G" in run(*P, "text").splitlines()[0]                       # the screen as text
    run(*P, "snap", "typed_again", "gameplay", "the same frame a second time")
    run(*P, "snap", "typed_third", "gameplay", "x" * 90)
    run(*P, "stop")
    out = run("tools/shoot.py", DOS_SLUG, "main", "--verify")
    assert "3/3 reproduce" in out and "check: identical pictures: typed, typed_again, typed_third" in out
    assert "check: caption has 90 characters (limit 80): typed_third" in out
    r = subprocess.run([sys.executable, "tools/shoot.py", DOS_SLUG, "main", "--publish-only"], cwd=ROOT,
                       capture_output=True, text=True)
    assert r.returncode == 4 and "not published" in r.stdout            # identical pictures are refused
    assert "removed typed_third" in run("tools/play.py", "unsnap", "typed_third", "--game", "dos/" + DOS_SLUG)
    work = os.path.join(ROOT, "work", "shots", "dos", DOS_SLUG, "main")
    lines = [l for l in open(os.path.join(work, "shots.txt")).read().splitlines() if not l.startswith("typed_again")]
    open(os.path.join(work, "shots.txt"), "w").write("\n".join(lines) + "\n")
    assert "pruned 1: typed_again" in run("tools/shoot.py", DOS_SLUG, "main", "--prune")
    assert not [f for f in os.listdir(work) if "typed_again" in f or "typed_third" in f]
    out = run("tools/shoot.py", DOS_SLUG, "main", "--publish-only")
    assert "published" in out and "lenses: 1 shots: systems.md uses 0" in out    # the template documents
    from PIL import Image
    im = Image.open(os.path.join(ROOT, "games", "dos", DOS_SLUG, "shots", "main",
                                 "zz-selftest-dos_dos_na_gameplay_typed.png")).convert("RGB")
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
    for sub in ("games/apple2", "work/shots/apple2", "work/cache/apple2", "work/intake/apple2", "work/play",
                "work/preview/apple2", "work/cachecheck/apple2"):
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
    assert e.text()[0][1::2] == "Hi1!Ab, 2+2=4" and len(e.text()) == 24    # the text page as text (play.py text)
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
    e.poke(0x2C010, b"\x42")                                             # language card RAM behind the ROM
    assert e.peek(0x2C010, 1) == b"\x42" and e.peek(0xD010, 1) != b"\x42" and e.peek(0x20300, 2) == b"\x5a\xa5"
    e.poke(0x20301, b"\x11")                                             # main store, page mapped right now
    assert e.peek(0x300, 2) == b"\x5a\x11"
    e.frames(2)
    assert e.peek(0x300, 2) == b"\x5a\x11" and e.peek(0x2C010, 1) == b"\x42"
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
    import zipfile
    extra = str(tmp_path / "extra.sav")                                  # a save with a disk of another name
    with zipfile.ZipFile(extra, "w") as zz:
        zz.writestr("T Transfer.dsk", bytes(143360))
    x = platforms.Apple2().open(z, sav=extra)
    assert x.disks == ["Side A.dsk", "Side B.dsk", "T Transfer.dsk"]     # an extra disk after the game's own
    x.disk(3, drive=2)
    assert x.drives[:2] == ["Side A.dsk", "T Transfer.dsk"] and x.battery(0) == b""
    x.close()
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


def test_apple2_write_protect(tmp_path):
    """Model wpN: disk N is write-protected, also after a savestate load (boot disks that check it: Wizardry)."""
    if not os.path.exists(platforms.Apple2.SO) or not os.path.exists(A2_DOS33):
        pytest.skip("AppleWin core not built (sh tools/setup_emu.sh apple2)")
    st = str(tmp_path / "x.state")
    e = platforms.Apple2().open(A2_DOS33, model="iie-wp1")
    e.frames(600)
    e.save_state(st)
    for again in (False, True):
        if again:
            e.load_state(st)
        e.type_text('10 PRINT "HI"\nSAVE GAMEDB\n')
        e.frames(400)
        assert "WRITE PROTECTED" in "\n".join(_a2_row(e, r) for r in range(24)) and e.battery(0) == b""
    e.close()


def test_apple2_colour_after_state_load(tmp_path):
    """Colour pictures drawn after a state load equal those of the run that made the state (the core rebuilt
    its colour tables on a load with leftover filter memory: some colours were off by 1; found with Might and
    Magic, 2026-11-18)."""
    if not os.path.exists(platforms.Apple2.SO) or not os.path.exists(A2_DOS33):
        pytest.skip("AppleWin core not built (sh tools/setup_emu.sh apple2)")
    st = str(tmp_path / "x.state")
    a = platforms.Apple2().open(A2_DOS33)
    a.frames(600)
    a.save_state(st)
    b = platforms.Apple2().open(A2_DOS33)
    b.load_state(st)
    for e in (a, b):
        e.type_text("HGR:FOR C=1 TO 7:HCOLOR=C:HPLOT C*30,0 TO C*30+60,150:NEXT\n")
        e.frames(200)
    im = a.image().convert("RGB")
    assert len(im.getcolors(100000)) > 4                                # a colour picture
    assert a.screen() == b.screen()
    a.close()
    b.close()


def test_apple2_pipeline(a2_selftest, tmp_path):
    z = _a2_zip(str(tmp_path / (A2_SLUG + ".zip")))
    run("tools/intake.py", z, "--slug", A2_SLUG, "--region", "na", "--probe", "120")
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
    im = Image.open(os.path.join(ROOT, "games", "apple2", A2_SLUG, "shots", "main",
                                 "zz-selftest-apple2_apple2_na_gameplay_typed.png")).convert("RGB")
    assert im.size == (560, 384) and im.crop((0, 0, 200, 16)).getextrema()[0][1] > 100


# ------------------------------------------------------------------ checkpoint chains, parallel runs, previews
# On the Apple II test disk: every key prints a letter made from a counter that runs while the program waits,
# so the picture and the memory record the exact timing of a route (the GB test ROM shows a still picture).
def _chain_game(a2_selftest, tmp_path):
    """The test disk registered with a chain of three checkpoints and six shots (s6 repeats the picture of s2)."""
    run("tools/intake.py", _a2_zip(str(tmp_path / (A2_SLUG + ".zip"))), "--slug", A2_SLUG, "--region", "na",
        "--probe", "0")
    d = os.path.join(ROOT, "games", "apple2", A2_SLUG)
    open(os.path.join(d, "checkpoints.txt"), "w").write(
        "one | first | BOOT,h\ntwo | second | @one,i,w33\nthree | third | @two,x,y,w21\n")
    meta = json.load(open(os.path.join(d, "game.json")))
    meta["macros"] = {"BOOT": "w200,disk:2,6,ctrl+p,enter,w200"}        # side B holds the test program
    json.dump(meta, open(os.path.join(d, "game.json"), "w"))
    work = os.path.join(ROOT, "work", "shots", "apple2", A2_SLUG, "main")
    os.makedirs(work, exist_ok=True)
    open(os.path.join(work, "shots.txt"), "w").write("".join(
        "s%d | gameplay | shot %d | %s\n" % (i, i, r) for i, r in enumerate(
            ["@three", "@one,a", "@two,b,w10", "@three,c", "@three,d,w7,e", "@one,a,w1"], 1)))
    return emu.Game(A2_SLUG), work


def test_checkpoint_chain_builds_once(a2_selftest, tmp_path, monkeypatch):
    g, _ = _chain_game(a2_selftest, tmp_path)
    cache = os.path.join(ROOT, "work", "cache", "apple2", A2_SLUG)
    boots = []
    real = emu.open_game
    monkeypatch.setattr(emu, "open_game", lambda *a, **k: (boots.append(k.get("state") or (a[2:3] or [None])[0]), real(*a, **k))[1])
    e, rest, full = emu.start(g, "@three,w5")           # empty cache: one power-on, every link cached on the way
    emu.play(e, g, rest)
    cold = e.screen()
    assert _a2_row(e)[1::2] == "HIXY"                   # four keys, a timing letter before each
    e.close()
    assert boots == [None] and full[-8:] == ["w200", "h", "i", "w33", "x", "y", "w21", "w5"]
    assert len([f for f in os.listdir(cache) if f.endswith(".state")]) == 3
    e, rest, _ = emu.start(g, "@three,w5")              # cache hit: the state of `three` itself
    emu.play(e, g, rest)
    assert e.screen() == cold and len(boots) == 2 and boots[1].endswith(".state")
    e.close()
    e, rest, _ = emu.start(g, "@three,w5", cache=False) # the reference: the flat route from power-on, no file read
    emu.play(e, g, rest)
    assert e.screen() == cold and boots[2] is None
    e.close()
    os.remove(emu.cache_path(g, emu.resolve(g, "@three"), g.model))
    e, rest, _ = emu.start(g, "@three,w5")              # only the last link is missing: built from the state of `two`
    emu.play(e, g, rest)
    assert e.screen() == cold and boots[3] == emu.cache_path(g, emu.resolve(g, "@two"), g.model)
    e.close()


def test_parallel_shoot_verify_and_duplicates(a2_selftest, tmp_path):
    SLUG = A2_SLUG
    g, work = _chain_game(a2_selftest, tmp_path)
    out = run("tools/shoot.py", SLUG, "main", "--jobs", "3")           # empty cache, three processes
    assert len(re.findall(r"^s\d +settled$", out, re.M)) == 6
    idx = json.load(open(os.path.join(work, "index.json")))
    assert [s["id"] for s in idx["shots"]] == ["s1", "s2", "s3", "s4", "s5", "s6"]      # list order, not finish order
    assert os.path.exists(os.path.join(work, "zz-selftest-apple2_apple2_na_set_sheet.png"))
    assert len({s["pixel_sha1"] for s in idx["shots"]}) == 5                           # s6 repeats s2
    first = {s["id"]: s["pixel_sha1"] for s in idx["shots"]}
    shutil.rmtree(os.path.join(ROOT, "work", "cache", "apple2", SLUG))
    assert "6/6 reproduce" in run("tools/shoot.py", SLUG, "main", "--verify", "--jobs", "4")     # cold, parallel
    assert "6/6 reproduce" in run("tools/shoot.py", SLUG, "main", "--verify", "--jobs", "1")     # warm, serial
    # the order of the set is the order of its own list
    lines = open(os.path.join(work, "shots.txt")).read().splitlines()
    open(os.path.join(work, "shots.txt"), "w").write("\n".join(lines[::-1]) + "\n")
    assert "6/6 reproduce" in run("tools/shoot.py", SLUG, "main", "--verify")
    idx = json.load(open(os.path.join(work, "index.json")))
    assert [s["id"] for s in idx["shots"]] == ["s6", "s5", "s4", "s3", "s2", "s1"]
    assert {s["id"]: s["pixel_sha1"] for s in idx["shots"]} == first
    # a new shot that repeats a picture is reported by the run that makes it
    open(os.path.join(work, "shots.txt"), "a").write("s7 | gameplay | s1 again | @three,w1\n")
    out = run("tools/shoot.py", SLUG, "main", "--only", "s7")
    dup = [l for l in out.splitlines() if l.startswith("check: identical pictures")]
    assert len(dup) == 1 and "s7" in dup[0] and "s1" in dup[0]         # s2 = s6 is not this run's news
    r = subprocess.run([sys.executable, "tools/shoot.py", SLUG, "main", "--publish-only"], cwd=ROOT,
                       capture_output=True, text=True)
    assert r.returncode == 4 and "not published" in r.stdout
    # a set without a working list falls back to its published list, not to the plan of main
    r = subprocess.run([sys.executable, "tools/shoot.py", SLUG, "other"], cwd=ROOT, capture_output=True, text=True)
    assert r.returncode != 0 and "no shot list for set 'other'" in r.stderr


def test_preview_and_cachecheck(a2_selftest, tmp_path):
    from PIL import Image
    SLUG = A2_SLUG
    g, work = _chain_game(a2_selftest, tmp_path)
    run("tools/shoot.py", SLUG, "main", "--only", "s1,s2")
    plan = os.path.join(ROOT, "work", "preview", "apple2", SLUG, "plan.txt")
    os.makedirs(os.path.dirname(plan), exist_ok=True)
    open(plan, "w").write("# candidates\n"
                          "like_s1 | gameplay | the frame of s1 | @three\n"
                          "marks | @one,?,right:20,?,a\n"
                          "broken | @one,nosuchkey\n")
    r = subprocess.run([sys.executable, "tools/preview.py", SLUG, plan, "--set", "main", "--peek", "0024:1"],
                       cwd=ROOT, capture_output=True, text=True)
    assert r.returncode == 1 and "broken" in r.stdout and "ERROR" in r.stdout          # one bad line, the rest shown
    line = [l for l in r.stdout.splitlines() if l.startswith("like_s1")][0]
    assert "= shot s1" in line and "0024=08" in line and " settled" in line                                     # shoot.py would give this frame
    out = os.path.join(ROOT, "work", "preview", "apple2", SLUG, "plan")
    assert Image.open(out + ".png").size[0] == 4 * 562                                 # native tiles, four per row
    assert sorted(os.listdir(out)) == ["like_s1.png", "marks.png", "marks__1.png", "marks__2.png"]
    idx = {s["id"]: s for s in json.load(open(os.path.join(work, "index.json")))["shots"]}
    import shoot
    assert shoot.pixel_sha1(os.path.join(out, "like_s1.png")) == idx["s1"]["pixel_sha1"]
    # text screens are read as text, without a picture to look at
    o = run("tools/preview.py", SLUG, "-r", "typed | @three,z", "--text")
    row = [l for l in o.splitlines() if l.startswith("|")][0]
    assert row[2::2] == "HIXYZ" and ".png" not in o
    # a timeline: frame +k is the route followed by k waits, as printed
    o = run("tools/preview.py", SLUG, "-r", "t | @two,a,!", "--timeline", "3:10", "--out", "tl")
    assert "frame +K = @two,a,w10*(K/10),!" in o
    e, rest, _ = emu.start(g, "@two,a,w10*2,!")
    emu.play(e, g, rest)
    tl = os.path.join(ROOT, "work", "preview", "apple2", SLUG, "tl", "t_+20.png")
    assert Image.open(tl).convert("RGB").tobytes() == Image.open(__import__("io").BytesIO(e.screen())).convert("RGB").tobytes()
    e.close()
    # cachecheck: every checkpoint from power-on, built in a chain, and loaded gives the same machine
    o = run("tools/cachecheck.py", SLUG)
    assert "3/3 checkpoints reproduce" in o and o.count(" same ") == 3
    assert os.path.exists(os.path.join(ROOT, "work", "cachecheck", "apple2", SLUG, "sheet.png"))
    # a state in the cache that its route does not produce (a session that drifted) is found and removed
    cp2, cp3 = (emu.cache_path(g, emu.resolve(g, "@" + n), g.model) for n in ("two", "three"))
    shutil.copyfile(cp2, cp3)
    r = subprocess.run([sys.executable, "tools/cachecheck.py", SLUG, "three", "--flat", "leaves", "--fix"],
                       cwd=ROOT, capture_output=True, text=True)
    assert r.returncode == 1 and "yours DIFFERS" in r.stdout and "removed 1 stale" in r.stdout
    assert not os.path.exists(cp3) and os.path.exists(cp2)
    assert "3/3 checkpoints reproduce" in run("tools/cachecheck.py", SLUG, "three", "--flat", "leaves")



# ------------------------------------------------------------------ Amiga (PUAE libretro core)
AM_SLUG = "zz-selftest-amiga"
AM_MODEL = "A1200-aros"         # the free Kickstart built into the core; it boots bootblocks on A1200-class machines


@pytest.fixture
def am_selftest(tmp_path):
    if not os.path.exists(platforms.Amiga.SO):
        pytest.skip("PUAE core not built (sh tools/setup_emu.sh amiga)")
    sys.path.insert(0, os.path.dirname(__file__))
    import make_amiga_adf
    rom = tmp_path / "t.adf"
    rom.write_bytes(make_amiga_adf.build())
    yield rom
    subprocess.run([sys.executable, os.path.join(ROOT, "tools", "play.py"), "--name", AM_SLUG, "stop"],
                   capture_output=True)
    for sub in ("games/amiga", "work/shots/amiga", "work/cache/amiga", "work/intake/amiga", "work/play"):
        shutil.rmtree(os.path.join(ROOT, sub, AM_SLUG), ignore_errors=True)
    if os.path.exists(os.path.join(ROOT, "rom", AM_SLUG + ".zip")):
        os.remove(os.path.join(ROOT, "rom", AM_SLUG + ".zip"))


def _am_zip(path, write=False):
    """Two disks: a blank one first (does not boot), the test program second."""
    import zipfile
    sys.path.insert(0, os.path.dirname(__file__))
    import make_amiga_adf
    with zipfile.ZipFile(path, "w") as z:
        z.writestr("Disk 1.adf", bytes(make_amiga_adf.SIZE))
        z.writestr("Disk 2.adf", make_amiga_adf.build(write))
    return path


def _am_colour(e):
    """COLOR00 of the test program as 12-bit RGB (24-bit picture: 4-bit channel * 17)."""
    r, g, b = e.image().convert("RGB").getpixel((100, 100))
    assert r % 17 == g % 17 == b % 17 == 0
    return (r // 17) << 8 | (g // 17) << 4 | b // 17


def _am_counter(e):
    return int.from_bytes(e.peek(0x7F000, 2), "big")


def test_amiga_identify(tmp_path):
    import gzip
    sys.path.insert(0, os.path.dirname(__file__))
    import make_amiga_adf, make_apple2_disk, make_dos_zip
    adf = make_amiga_adf.build()
    h = platforms.Amiga.identify(adf)
    assert h["platform"] == "amiga" and h["model"] == "A500"
    assert h["disks"][0]["kind"] == "3.5 inch DD floppy, 880 KiB" and h["disks"][0]["boot"] == "AmigaDOS OFS"
    vol = bytearray(adf)
    vol[880 * 512 + 432:880 * 512 + 437] = b"\x04Test"                  # root block: volume name
    h = platforms.Amiga.identify(bytes(vol))
    assert h["header_title"] == "Test" and h["disks"][0]["volume"] == "Test"
    assert platforms.Amiga.identify(gzip.compress(adf))["disks"][0]["boot"] == "AmigaDOS OFS"   # .adz
    assert "not an AmigaDOS disk" in platforms.Amiga.identify(bytes(901120))["disks"][0]["boot"]
    z = _am_zip(str(tmp_path / "two.zip"))
    h = platforms.Amiga.identify(open(z, "rb").read())
    assert [d["name"] for d in h["disks"]] == ["Disk 1.adf", "Disk 2.adf"] and len(h["disks"][1]["sha1"]) == 40
    assert platforms.by_extension(z)[0] == "amiga"                       # a ZIP of Amiga floppy images
    d = tmp_path / "dos.zip"
    d.write_bytes(make_dos_zip.build())
    assert platforms.by_extension(str(d))[0] == "dos"
    import zipfile
    with zipfile.ZipFile(str(tmp_path / "a2.zip"), "w") as zz:
        zz.writestr("A.dsk", make_apple2_disk.build())
    assert platforms.by_extension(str(tmp_path / "a2.zip"))[0] == "apple2"
    assert platforms.by_extension("x/GAME.ADF")[0] == "amiga" and platforms.by_extension("x/g.adz")[0] == "amiga"
    assert {"a", "1", "enter", "esc", "up", "f10", "help", "lamiga", "ramiga", "joyup", "fire", "fire2",
            "mouse1", "mouse2"} <= platforms.Amiga.keys
    assert not {"f11", "f12", "pageup"} & platforms.Amiga.keys


def test_amiga_kickstart_lookup(tmp_path, monkeypatch):
    """A real Kickstart is found in rom/kickstart/ by PUAE's file name or the Amiga Forever name; a missing one
    is reported with what to supply."""
    monkeypatch.setattr(platforms.Amiga, "KICKDIR", str(tmp_path))
    with pytest.raises(SystemExit, match="kick34005.A500.*A500-aros"):
        platforms.Amiga.kickstart("A500")
    (tmp_path / "amiga-os-310-a1200.rom").write_bytes(bytes(524288))
    assert platforms.Amiga.kickstart("A1200").endswith("amiga-os-310-a1200.rom")
    (tmp_path / "kick34005.A500").write_bytes(bytes(262144))
    assert platforms.Amiga.kickstart("A500OG").endswith("kick34005.A500")


def test_amiga_backend(am_selftest, tmp_path):
    e = platforms.Amiga().open(str(am_selftest), model=AM_MODEL)
    e.frames(300)
    assert e.image().size[1] == 287 and _am_counter(e) > 100 and _am_colour(e) >> 4 == 0     # running, no key yet
    assert e.regs()["pc"] < "001000"                                     # the bootblock runs in chip RAM
    e.input(["fire"]); e.frames(4)
    assert _am_colour(e) == 0xFFF                                        # joystick fire, port 2
    e.input(["mouse1"]); e.frames(4)
    assert _am_colour(e) == 0xF0F                                        # left mouse button, port 1
    x, y = e.peek(0x7F003, 1)[0], e.peek(0x7F002, 1)[0]                  # JOY0DAT counters
    e.mouse(10, -3); e.frames(2)
    assert (e.peek(0x7F003, 1)[0], e.peek(0x7F002, 1)[0]) == ((x + 10) & 0xFF, (y - 3) & 0xFF)   # 1 unit = 1 count
    x = e.peek(0x7F003, 1)[0]
    e.mouse(400, 0); e.frames(2)
    assert (e.peek(0x7F003, 1)[0] - x) & 0xFF < 250                       # 120 counts a frame, not all at once
    e.frames(10)
    assert e.peek(0x7F003, 1)[0] == (x + 400) & 0xFF                      # ... but all of it arrives
    e.input(["a"]); e.frames(8); e.input([]); e.frames(8)
    assert _am_colour(e) >> 4 == 0xA0                                    # raw key code: A up ($20 | $80)
    e.type_text("1")
    assert _am_colour(e) >> 4 == 0x81                                    # 1 up ($01 | $80)
    st = str(tmp_path / "x.state")
    e.save_state(st)
    shot = e.screen()
    e.poke(0x7F010, b"\x5a\xa5")
    assert e.peek(0x7F010, 2) == b"\x5a\xa5"
    assert e.peek(0xF80000, 2) == b"\x11\x14"                            # Kickstart ROM (AROS) is readable
    with pytest.raises(ValueError):
        e.poke(0xF80000, b"\x00")                                        # ROM
    with pytest.raises(ValueError):
        e.poke(0xDFF180, b"\x00\x00")                                    # custom chips: not memory
    assert e.peek(0xDFF006, 2) == b"\0\0"                                # read without side effects: 0
    e.load_state(st)
    assert e.screen() == shot
    e.frames(1)
    assert e.peek(0x7F010, 2) != b"\x5a\xa5"
    assert e.ram_search("new == old")["count"] > 0
    e.close()
    with pytest.raises(SystemExit, match="unknown Amiga model"):
        platforms.Amiga().open(str(am_selftest), model="A3000")
    n = platforms.Amiga().open(str(am_selftest), model=AM_MODEL + "-ntsc")
    n.frames(300)
    assert n.image().size[1] < 287                                       # 60 Hz machine: fewer lines
    n.close()


def test_amiga_same_route_same_frames(am_selftest, tmp_path):
    """Nothing depends on the host: two power-ons give the same pictures and chip RAM, and a run continued after
    save_state equals one loaded from that state, into a machine that has not run yet or one that is busy
    (the core used to emulate frames inside its state load: the loaded run was a frame ahead)."""
    st = str(tmp_path / "x.state")

    def boot():
        e = platforms.Amiga().open(str(am_selftest), model=AM_MODEL)
        e.frames(300)
        return e

    def play(e):
        out = []
        for k, w in zip(("g", "fire", "m", "mouse1", "e"), (3, 17, 5, 29, 11)):
            e.input([k]); e.frames(3); e.input([]); e.frames(w)
            out.append((e.screen(), _am_counter(e)))
        return out, e.peek(0, 0x80000)

    a, b = boot(), boot()
    assert a.screen() == b.screen() and a.peek(0, 0x80000) == b.peek(0, 0x80000)
    assert play(a) == play(b)
    a.save_state(st)
    c = platforms.Amiga().open(str(am_selftest), model=AM_MODEL)
    c.load_state(st)
    assert c.screen() == a.screen()
    assert c.peek(0, 0x80000) == a.peek(0, 0x80000) and c.regs() == a.regs()     # loaded at once, before a frame
    c.save_state(str(tmp_path / "y.state"))                             # not run since the load: same state
    assert open(st, "rb").read() == open(str(tmp_path / "y.state"), "rb").read()
    b.input(["fire"]); b.frames(7)
    b.load_state(st)
    want = play(a)
    assert play(c) == want and play(b)[0][0] == want[0][0]
    for e in (a, b, c):
        e.close()


def test_amiga_disks(am_selftest, tmp_path):
    """Disk swaps, and games that save by writing to a floppy: a savestate keeps the machine, the backend
    stores the blocks written so far next to it, and the export is the written images."""
    z = _am_zip(str(tmp_path / "two.zip"), write=True)
    e = platforms.Amiga().open(z, model=AM_MODEL + "-df1")
    assert e.disks == ["Disk 1.adf", "Disk 2.adf"] and e.drives == ["Disk 1.adf", None]
    e.frames(150)
    assert _am_counter(e) == 0xFFFF                                      # blank disk: nothing runs
    e.disk(2)                                                            # the boot screen notices the swap
    e.frames(400)
    assert e.drives == ["Disk 2.adf", None] and _am_counter(e) > 100
    e.disk(1, drive=2)
    assert e.drives == ["Disk 2.adf", "Disk 1.adf"]
    e.disk(1)                                                            # a disk is in one drive at a time
    assert e.drives == ["Disk 1.adf", None]
    e.disk(2)
    with pytest.raises(ValueError):
        e.disk(3)
    with pytest.raises(ValueError):
        e.disk(1, drive=3)                                               # -df1: drives 1 and 2 only
    sav = e.battery(0)
    import io, zipfile
    written = zipfile.ZipFile(io.BytesIO(sav)).read("Disk 2.adf")
    assert written[1024:1536] == written[:512]                           # the program wrote its own bootblock
    st = str(tmp_path / "w.state")
    e.save_state(st)
    f = platforms.Amiga().open(z, model=AM_MODEL + "-df1")               # fresh machine, pristine disks
    assert f.battery(0) == b""
    f.load_state(st)
    assert f.drives == ["Disk 2.adf", None] and f.battery(0) == sav
    f.frames(10)
    assert f.screen() == (e.frames(10) or e.screen())
    open(str(tmp_path / "x.sav"), "wb").write(sav)
    g = platforms.Amiga().open(z, model=AM_MODEL, sav=str(tmp_path / "x.sav"))   # power on with the export
    assert g.battery(0) == sav
    with pytest.raises(RuntimeError, match="2 drives"):
        g.load_state(st)
    for x in (e, f, g):
        x.close()


def test_amiga_pipeline(am_selftest, tmp_path):
    z = _am_zip(str(tmp_path / (AM_SLUG + ".zip")))
    run("tools/intake.py", z, "--slug", AM_SLUG, "--region", "eu", "--model", AM_MODEL, "--probe", "120")
    gj = os.path.join(ROOT, "games", "amiga", AM_SLUG, "game.json")
    meta = json.load(open(gj))
    assert meta["platform"] == "amiga" and meta["model"] == AM_MODEL and meta["rom"].endswith(".zip")
    assert [d["name"] for d in meta["header"]["disks"]] == ["Disk 1.adf", "Disk 2.adf"]
    meta["macros"] = {"BOOT": "w100,disk:2,w400"}
    meta["ram"] = {"counter": {"addr": "7F000", "size": 2, "fmt": "be"}}
    json.dump(meta, open(gj, "w"))
    P = ["tools/play.py", "--name", AM_SLUG]
    run(*P, "start", AM_SLUG)
    run(*P, "do", "BOOT")
    assert "saved" in run(*P, "checkpoint", "ready", "test program running")
    run(*P, "do!", "fire:4,type:a,w10")
    assert "counter=" in run(*P, "status")
    run(*P, "snap", "key", "gameplay", "key A released: background colour from its key code")
    run(*P, "stop")
    assert "1/1 reproduce" in run("tools/shoot.py", AM_SLUG, "main", "--verify")
    run("tools/shoot.py", AM_SLUG, "main", "--publish-only")
    from PIL import Image
    im = Image.open(os.path.join(ROOT, "games", "amiga", AM_SLUG, "shots", "main",
                                 "zz-selftest-amiga_amiga_eu_gameplay_key.png")).convert("RGB")
    r, g, b = im.getpixel((100, 100))
    assert (r, g) == (0xA * 17, 0)                                       # A up: $A0 -> red A, green 0
