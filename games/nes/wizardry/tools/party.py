"""Wizardry (NES) party-creation macros.

python3 games/nes/wizardry/tools/party.py          -> prints the macros (JSON) for game.json
python3 games/nes/wizardry/tools/party.py --write  -> writes them into games/nes/wizardry/game.json "macros"

Training Grounds > Create: name keyboard (cursor starts on "1", Select = shift, A types, ret at column 12),
Yes, race, alignment, stats screen, class, Keep Yes. The roll happens when the stats screen opens ($0254-$0259
STR IQ PIE VIT AGI LUC, bonus $025B); the macro pokes each stat one below the target plus 6 bonus points and
presses Right on every row, so every row is redrawn and the bonus ends at 0.
"""
import json, sys
from pathlib import Path

ROWS = ["!@#$%^&*()_+|", "QWERTYUIOP{}", 'ASDFGHJKL:"~', "ZXCVBNM<>?"]
RACES = ["Human", "Elf", "Dwarf", "Gnome", "Hobbit"]
ALIGN = ["Good", "Neutral", "Evil"]
# name, race, alignment, (STR IQ PIE VIT AGI LUC), class index in the eligible list, class
PARTY = [
    ("RYZ",   "Human",  "Good",    (17, 8, 5, 13, 10, 9),   0, "Fighter"),
    ("CONDI", "Dwarf",  "Good",    (16, 7, 10, 15, 7, 6),   0, "Fighter"),
    ("EBO",   "Gnome",  "Good",    (9, 7, 16, 10, 11, 7),   0, "Priest"),
    ("CUBI",  "Hobbit", "Neutral", (7, 7, 7, 9, 16, 15),    0, "Thief"),
    ("DEDDO", "Elf",    "Good",    (7, 17, 10, 8, 11, 6),   0, "Mage"),
    ("MNZ",   "Elf",    "Good",    (7, 15, 14, 7, 10, 6),   2, "Bishop"),
]


def move(r0, c0, r1, c1):
    t = []
    if r1 > r0: t.append(f"down*{r1 - r0}")
    if r1 < r0: t.append(f"up*{r0 - r1}")
    if c1 > c0: t.append(f"right*{c1 - c0}")
    if c1 < c0: t.append(f"left*{c0 - c1}")
    return t


def name_tokens(name, shift):
    # the keyboard's shift state (Select) persists between names for the whole session: power-on = lower case,
    # so only the first name presses Select; MAKE1..MAKE6 must run in order (macro PARTYMAKE)
    t, r, c = (["select,w20"] if shift else []), 0, 0
    for ch in name:
        rr = next(i for i, row in enumerate(ROWS) if ch in row)
        cc = ROWS[rr].index(ch)
        t += move(r, c, rr, cc) + ["a,w20"]
        r, c = rr, cc
    t += move(r, c, 1, 12) + ["a,w60"]       # ret
    return t


def char_macro(name, race, align, stats, cls_idx, shift):
    t = name_tokens(name, shift)
    t += ["a,w60"]                                             # Create this Character? Yes
    t += [f"down*{RACES.index(race)}"] * bool(RACES.index(race)) + ["a,w60"]
    t += [f"down*{ALIGN.index(align)}"] * bool(ALIGN.index(align)) + ["a,w60"]
    # stats screen: poke each stat one below the target and 6 bonus points, then Right on every row
    # (the screen redraws a row only when it is altered; A refuses while bonus points are left)
    t += [",".join(f"poke:{0x254 + i:04X}={v - 1:02X}" for i, v in enumerate(stats)) + ",poke:025B=06"]
    t += ["right,down," * 5 + "right"]
    t += ["a,w60"]                                             # stats: finished
    t += [f"down*{cls_idx}"] * bool(cls_idx) + ["a,w60"]     # class
    t += ["a,w60"]                                             # Keep this Character? Yes
    return ",".join(t)


def macros():
    m = {}
    for i, (name, race, align, stats, ci, cls) in enumerate(PARTY, 1):
        m[f"MAKE{i}"] = "a,w60," + char_macro(name, race, align, stats, ci, i == 1)   # from Training Grounds menu (Create)
    m["PARTYMAKE"] = ",".join(f"MAKE{i}" for i in range(1, len(PARTY) + 1))
    return m


if __name__ == "__main__":
    m = macros()
    if "--write" in sys.argv:
        p = Path(__file__).resolve().parents[1] / "game.json"
        g = json.loads(p.read_text())
        g["macros"].update(m)
        p.write_text(json.dumps(g, indent=2) + "\n")
    print(json.dumps(m, indent=2))
