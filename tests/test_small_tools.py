import os, sys
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "tools"))
import dis6502  # noqa: E402


def test_modes_branch_and_truncation():
    code = bytes([0xA9, 0x01, 0x8D, 0x00, 0x20, 0xD0, 0xFE, 0x02, 0x4C])
    out = dis6502.dis(code, 0xC000, 6, 0xC000)
    assert out[0].endswith("LDA #$01")
    assert out[1].endswith("STA $2000")
    assert out[2].endswith("BNE $C005")       # branch to itself
    assert out[3].endswith(".db $02")         # illegal opcode
    assert out[4].endswith(".db $4C")         # JMP cut off at the bank end


def test_macro_arguments():
    import emu, pytest

    class G:
        macros = {"WARP": "poke:003D={0},poke:003B={1},left,w30", "GO": "WARP:02:05,up"}
    assert emu.expand(G, emu.split("GO")) == ["poke:003D=02", "poke:003B=05", "left", "w30", "up"]
    assert emu.expand(G, emu.split("set:0040=100:2")) == ["set:0040=100:2"]
    with pytest.raises(ValueError):
        emu.expand(G, emu.split("WARP:02"))


def test_shot_file_names():
    import intake, pytest, shoot
    g = {"slug": "might-and-magic-2", "platform": "nes", "region": "na"}
    assert shoot.stem(g, "main", "battle", "battle_slime") == "might-and-magic-2_nes_na_battle_battle_slime"
    assert shoot.stem(g, "compare-maze", "gameplay", "maze_f1") == "might-and-magic-2_nes_na_gameplay_maze_f1.compare-maze"
    assert shoot.stem(g, "seq-fly", "map", "05_town_map") == "might-and-magic-2_nes_na_map_seq-fly_05_town_map"
    # set `start`: the step number before the area, so a folder listing is the play order
    assert shoot.stem(g, "start", "boot", "01_crack_note") == "might-and-magic-2_nes_na_01_boot_crack_note.start"
    with pytest.raises(SystemExit):
        shoot.stem(g, "start", "boot", "crack_note")        # start ids are numbered
    assert shoot.set_file(g, "main", "sheet.png") == "might-and-magic-2_nes_na_set_sheet.png"
    assert shoot.set_file(g, "seq-fly", "full.gif") == "might-and-magic-2_nes_na_set_seq-fly_full.gif"
    # the first four fields hold no `_`: a name splits back into its parts
    assert shoot.stem(g, "main", "battle", "battle_slime").split("_", 4) == [
        "might-and-magic-2", "nes", "na", "battle", "battle_slime"]
    for bad in (dict(g, region=None), dict(g, slug="wizardry_nes")):
        with pytest.raises(SystemExit):
            shoot.stem(bad, "main", "battle", "x")
    with pytest.raises(SystemExit):
        shoot.stem(g, "jp_tour", "battle", "x")             # set names: words joined by `-`
    with pytest.raises(SystemExit):
        shoot.stem(g, "main", "set", "x")                   # reserved for set files
    assert intake.region_of({"region": "Japan"}) == "jp" and intake.region_of({"region": "PAL"}) == "eu"
    assert intake.region_of({"region": "NTSC"}) is None and intake.region_of({"region": "Overseas"}) is None


def test_lenses_check(tmp_path):
    """tools/lenses.py: shots named in none of the three design lenses and rows without a shot are listed."""
    import json, types
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))
    import lenses
    d = tmp_path / "g"
    (d / "shots" / "main").mkdir(parents=True)
    (d / "design").mkdir()
    shots = [{"id": i, "category": "system", "caption": i, "file": "g_dos_na_system_%s.png" % i}
             for i in ("bash", "bash_wall", "trade", "title")]
    (d / "shots" / "main" / "index.json").write_text(json.dumps({"shots": shots}))
    game = types.SimpleNamespace(dir=str(d))
    assert lenses.check(game)[0] == 2                                   # documents missing
    (d / "design" / "systems.md").write_text(
        "| Group | System | Shots | Status |\n|---|---|---|---|\n| Verbs | Bash | `bash` | shown |\n"
        "| Verbs | Trade | | open |\n| Chance | Hidden roll | none: no screen of its own | described |\n")
    (d / "design" / "interface.md").write_text(
        "| Screen | Shots |\n|---|---|\n| Bash prompt | `bash`, g_dos_na_system_title.png |\n")
    assert lenses.check(game)[0] == 2                                   # content.md still missing
    (d / "design" / "content.md").write_text("| Item | Shots |\n|---|---|\n| Club | `trade` |\n")
    code, out = lenses.check(game)
    text = "\n".join(out)
    assert code == 1 and "systems.md uses 1, interface.md uses 2, content.md uses 1; in two or more: 1" in text
    assert "in no document: bash_wall" in text and "in no document: trade" not in text
    assert "in no document: bash (" not in text                         # `bash` does not count for bash_wall
    assert "systems.md:4 row without a shot or a reason: Verbs" in text and "Hidden roll" not in text


def test_game_tables_match_game_json():
    """README.md and docs/status.md carry the tables tools/gamestable.py writes from the game.json files."""
    import gamestable
    assert gamestable.main(["--check"]) == 0, "run python3 tools/gamestable.py"
    rows = gamestable.games()
    assert all(g["work"] for g in rows) and len({g["id"] for g in rows}) == len(rows)


def test_x3_png_and_gif(tmp_path):
    from PIL import Image
    import x3
    a, b = Image.new("RGB", (8, 6), (255, 0, 0)), Image.new("RGB", (8, 6), (0, 0, 255))
    a.save(tmp_path / "a.png")
    a.save(tmp_path / "c.gif", save_all=True, append_images=[b], duration=[40, 120], loop=0)
    assert x3.main([str(tmp_path)]) == 0
    assert Image.open(tmp_path / "3x" / "a.png").size == (24, 18)
    g = Image.open(tmp_path / "3x" / "c.gif")
    assert g.size == (24, 18) and g.n_frames == 2
    g.seek(1)
    assert g.info["duration"] == 120
    x3.main([str(tmp_path / "a.png"), "--scale", "2", "--out", str(tmp_path / "big")])
    assert Image.open(tmp_path / "big" / "a.png").size == (16, 12)


def test_dis68k_decodes_and_finds_references():
    import importlib.util
    if importlib.util.find_spec("capstone") is None:
        pytest.skip("capstone not installed")
    import dis68k
    code = bytes.fromhex("4A38C818" "4E75")          # tst.b $c818.w ; rts
    ins = list(dis68k.engine().disasm(code, 0x1000))
    assert [i.mnemonic for i in ins] == ["tst.b", "rts"]
    assert dis68k.targets(ins[0].op_str) == [0xFFC818]
    assert "; flag" in dis68k.line(ins[0], {0xFFC818: "flag"})


def test_aspect_rule_rowdoubles_flattened_frames(tmp_path, capsys):
    """game.json "aspect" (owner's rule 2026-11-21, per game): 640x200 is row-doubled with "rowdouble", kept with
    "native", and warned about with no decision; square-pixel frames are never touched; shoot.py spots them."""
    import platforms, shoot
    from PIL import Image

    class Fake(platforms.Libretro):
        def __init__(self, size):
            self.size = size

        def image(self):
            im = Image.new("RGB", self.size)
            im.putpixel((0, 1), (255, 0, 0))
            return im

    e = Fake((640, 200))
    e.aspect = "rowdouble"
    im = e.shaped()
    assert im.size == (640, 400)
    assert im.getpixel((0, 2)) == im.getpixel((0, 3)) == (255, 0, 0) and im.getpixel((0, 1)) == (0, 0, 0)
    e.aspect = "native"
    assert e.shaped().size == (640, 200)
    e.aspect = None
    assert e.shaped().size == (640, 200)
    assert "ask the owner" in capsys.readouterr().err
    sq = Fake((320, 200))
    sq.aspect = "rowdouble"
    assert sq.shaped().size == (320, 200)
    p = tmp_path / "a.png"
    Image.new("RGB", (640, 200)).save(p)
    assert shoot.flattened(str(p))
    Image.new("RGB", (640, 400)).save(p)
    assert not shoot.flattened(str(p))


def test_hirestext_learn_and_read():
    """Hi-res text: a line taught at one place and pixel phase is read back at another (tools/hirestext.py)."""
    import random
    import hirestext as H
    H.H = 8
    rnd = random.Random(5)
    shapes = {ch: bytes([0x00] + [rnd.randrange(1, 0x7F) | 0x01 for _ in range(6)] + [0x00]) for ch in "abcdeHlo"}

    def draw(rows, y, x, text):
        for i, ch in enumerate(text):
            if ch != " ":
                for r, b in enumerate(shapes[ch]):
                    rows[y + r] |= b << (x + 7 * i)

    rows = [0] * 192
    draw(rows, 40, 15, "Hello abc")
    draw(rows, 100, 70, "cab ode")
    font = {}
    rep = H.learn(rows, font, ["Hello abc", "cab ode"])
    assert rep[0].startswith("row  41 x  15") and rep[1].startswith("row 101 x  70"), rep     # top row with ink
    rows2 = [0] * 192
    draw(rows2, 17, 3, "a bead")
    draw(rows2, 150, 141, "Hello")
    assert [(y, H.clean(s)) for y, s in H.read_rows(rows2, font)] == [(18, "a bead"), (151, "Hello")]
    inverse = [r ^ ((1 << 280) - 1) for r in rows2]                 # dark letters on a light window
    assert [H.clean(s) for _, s in H.read_rows(inverse, font)] == ["a bead", "Hello"]
def test_start_ids_repeating_category(tmp_path):
    import json, shoot
    (tmp_path / "index.json").write_text(json.dumps({"shots": [{"id": "02_menu_old"}]}))
    shots = [{"id": "01_boot_logo", "category": "boot"}, {"id": "02_menu_old", "category": "menu"},
             {"id": "03_logo", "category": "boot"}, {"id": "04_menus", "category": "menu"}]
    assert shoot.start_ids_repeating_category(shots, str(tmp_path)) == ["01_boot_logo"]


def test_cachecheck_mem_diff():
    import cachecheck
    a = [(0x100, bytes(64))]
    b = [(0x100, bytes(4) + b"\x01" + bytes(10) + b"\x02" + bytes(40) + b"\x03" + bytes(7))]
    assert cachecheck.mem_diff(a, b, 5) == [[0x104, 0x10F], [0x138, 0x138]]
    assert cachecheck.mem_diff(a, b, 1) == [[0x104, 0x10F]]
