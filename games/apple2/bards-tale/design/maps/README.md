# The Bard's Tale (Apple II) - dungeon maps

The game has no automap **(verified: no map command; the only position help is the spell SCSI, Scry Site,
shot `spell_scsi`)**. These maps are decoded from the level data the game loads, one file pair per level:
`NN_name.txt` (text, North up) and `NN_name.png` (drawn). They are reference pictures, not shots: the shot sets
hold emulator pictures only. Made by `python3 games/apple2/bards-tale/tools/allmaps.py [ID ...]` (loads every
level with the level warp, playbook "Level warp"; about 2 minutes for all 16). **(RAM)**

| File | Level | In-game name | Monster level | Notes |
|---|---|---|---|---|
| 00_cellar | Wine cellar (under the Scarlet Bard) | Cellars | 0 | stairs down at 7,18 |
| 01_sewers1 .. 03_sewers3 | Sewers 1-3 | Sewers | 1, 1, 2 | the city portal (1,1) leads to Sewers level 3 (walls identical, verified) |
| 04_catacombs1 .. 06_catacombs3 | Catacombs 1-3 (Mad God's temple, name TARJAN) | Catacombs | 2, 3, 3 | |
| 07_castle1 .. 09_castle3 | Harkyn's Castle 1-3 | Castle | 3, 4, 4 | goes up |
| 10_kylearan | Kylearan's Amber Tower | Tower | 5 | Kylearan at 17,13, crystal statue 4,1, silver triangle 2,20 |
| 11_mangar1 .. 15_mangar5 | Mangar's Tower 1-5 | The Tower | 5, 6, 6, 7, 7 | Mangar's antechamber at 10,20 of level 5 |

Mangar's Tower is on the same dungeon disk as the others: the game never asked for disk 4 (`4 Dungeon 2.dsk`)
in any route of this capture **(verified)**.

## Legend
Coordinates: x east (columns 0-21), y north (rows 0-21, 0 = south edge); the levels wrap at the edges **(RAM)**.
- Walls: `---` / `|` wall, `-D-` / `D` door, `-S-` / `S` the fourth wall value (secret door, unverified).
  PNG: white wall, orange door, red the fourth value.
- `U` / `D` stairs up / down; `!` a special square (inscription, magic mouth, voice, riddle, NPC, fixed event);
  `F` forced fight (a random group, once: the square is cleared after the fight); `T` trap (once; tripwire,
  "TRAP! ... a stone block to fall"); `k` darkness ("Darkness!" puts out the light; PNG: grey square);
  `^` / `v` portal up / down (taken with the keys E and D, falling through a floor portal hurts without
  levitation) **(RAM: code at A769-A79x and A80C-A8A3 of the dungeon module; inferred for the portal keys)**.

## Open questions
- The fourth wall value (`S`) has not been walked into; secret door is the usual meaning.
- Portal squares were read from the code, not taken in play.
