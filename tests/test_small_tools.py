import os, sys

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
