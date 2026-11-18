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
