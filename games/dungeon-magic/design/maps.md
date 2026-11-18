# Dungeon Magic: Sword of the Elements - maps

## Overview
Every town, castle floor, forest and dungeon floor of the game is a 16 by 16 grid of squares with walls between
them; all 39 are drawn here from the game's own data, so they are complete (no unexplored gaps) **(verified)**:
each floor was loaded in play and the floor in memory matched the stored one (bank 4 floors byte for byte; bank 2
forests and towns entered in play). The outdoors is one 64 by 96 map: a 64 by 64 continent with islands and a
64 by 32 lower world (brown ground) that holds three more dungeons **(verified)** (`overworld.png`, entrances
visited for floors 92 and 95). The screen shows a 16 by 16 window of it ("section"); the number of a section is
what the game reports while you walk **(RAM)**.

- 6 towns (00-05), each a walled square with four gates, an inn, a weapon/armour shop, an item shop and one or
  more wizards' houses; Granville (00) has all five wizards **(verified)** (shots `wizard_apprentice`, town
  door survey of the capture run).
- 1 castle (89, Granville Castle) with a cellar floor below (8A) and a deeper floor (8B) **(verified)**
  (`castle_entrance`, `castle_cellar`).
- 3 forests of 3 floors each (40-42, 43-45, 46-48), drawn as tunnels through trees **(verified)** (`forest_*`).
- 8 dungeons of 3 floors each (80-82, 83-85, 86-88, 8C-8E, 8F-91, 92-94, 95-97; 8B joins the castle to
  nothing else in the tables) **(verified)** (exit tables; one shot per dungeon).

Names: the game shows no place names on screen in the parts visited, so maps are named by number and location.
The story names (Dungeon of Doom, Dark Forest, Wind Cape ...) are not yet tied to numbers **(inferred)**.

## 1. How to read the floor maps
`maps/map_XX.png` (drawn by `../tools/atlas.py`): white lines are walls; a dark filled square is solid (walled
on all four sides: rooms reached through a door, the Granville plaque). Labels:
- **OUT**: gate or exit to the overworld.
- **two hex digits** (blue): stairs to that floor; the arrival square is in `maps/maps.json`.
- Towns: **W** weapon and armour shop, **I** item shop, **N** inn, **M** wizard's house with the element where it
  was seen (Ea Earth, Wa Water, Fi Fire, Wi Wind, Fa Fairies). A building is entered by facing its door from the
  street square in front and pressing A **(verified)**.
- Small coloured dots: further feature marks in the data (red, green, blue, yellow = the four high bits of the
  square). Green marks the square behind a door and yellow the street square in front of it in towns
  **(verified)**; the others are not decoded (chests, traps and fixed monsters are candidates) **(inferred)**.

`maps/overworld.png`: blue water, light green grassland, dark green forest edge, brown lower-world ground; red
squares are towns, yellow squares other places, labelled with the floor numbers whose exits lead there
(`(xx)` = a place no floor exit points to: unvisited). White grid = sections with their numbers.
`maps/atlas.png`: all floors on one sheet.

## 2. All floors
Columns: floor; stairs to other floors; where its exit leads (section, overworld column/row of the place);
town doors; RAM warp tokens that load the floor (cataloguing shortcut, see `../playbook.md`).

| Floor | Stairs to | Exit to the overworld | Town doors | Warp |
|---|---|---|---|---|
| [00](maps/map_00.png) | - | field 25 (30,30) | 73 W, 93 N, B3 I, 34 M, 38 M, 6C M, BC M, C6 M |  |
| [01](maps/map_01.png) | - | field 25 (25,19) | 44 N, B4 M, 77 W, BB I |  |
| [02](maps/map_02.png) | - | field 24 (4,24) | 34 N, 3B I, C4 M, CB W |  |
| [03](maps/map_03.png) | - | field 27 (53,26) | 2A M, 52 W, 78 N, A7 I |  |
| [04](maps/map_04.png) | - | field 29 (21,35) | 65 W, 7A I, 85 N, 9A M |  |
| [05](maps/map_05.png) | - | field 2E (46,51) | D3 M, 32 I, CD W, 2C N |  |
| [40](maps/map_40.png) | 41 | field 2B (57,36) | - | `poke:0095=40,poke:008A=E2,poke:008F=E2,poke:0098=79,poke:0099=A9,poke:0011=00,poke:0003=18,w240` |
| [41](maps/map_41.png) | 40, 42 | field 2B (57,36) | - | `poke:0095=41,poke:008A=12,poke:008F=12,poke:0098=3A,poke:0099=A9,poke:0011=00,poke:0003=18,w240` |
| [42](maps/map_42.png) | 41 | field 2B (57,36) | - | `poke:0095=42,poke:008A=21,poke:008F=21,poke:0098=79,poke:0099=A9,poke:0011=00,poke:0003=18,w240` |
| [43](maps/map_43.png) | 44 |   | - | `poke:0095=43,poke:008A=E6,poke:008F=E6,poke:0098=CC,poke:0099=A9,poke:0011=00,poke:0003=18,w240` |
| [44](maps/map_44.png) | 43, 45 | field 28 (12,40) | - | `poke:0095=44,poke:008A=16,poke:008F=16,poke:0098=CC,poke:0099=A9,poke:0011=00,poke:0003=18,w240` |
| [45](maps/map_45.png) | 44 |   | - | `poke:0095=45,poke:008A=18,poke:008F=18,poke:0098=CC,poke:0099=A9,poke:0011=00,poke:0003=18,w240` |
| [46](maps/map_46.png) | 47, 48 | field 14 (8,89) | - | `poke:0095=46,poke:008A=5E,poke:008F=5E,poke:0098=CC,poke:0099=A9,poke:0011=00,poke:0003=18,w240` |
| [47](maps/map_47.png) | 46 | field 14 (8,89) | - | `poke:0095=47,poke:008A=51,poke:008F=51,poke:0098=CC,poke:0099=A9,poke:0011=00,poke:0003=18,w240` |
| [48](maps/map_48.png) | 46 | field 14 (8,89) | - | `poke:0095=48,poke:008A=13,poke:008F=13,poke:0098=CC,poke:0099=A9,poke:0011=00,poke:0003=18,w240` |
| [80](maps/map_80.png) | 81 | field 20 (12,7) | - | `poke:0095=80,poke:008A=87,poke:008F=87,poke:0098=8C,poke:0099=A1,poke:0011=00,poke:0003=16,w240` |
| [81](maps/map_81.png) | 80, 82 |   | - | `poke:0095=81,poke:008A=89,poke:008F=89,poke:0098=8C,poke:0099=A1,poke:0011=00,poke:0003=16,w240` |
| [82](maps/map_82.png) | 81 |   | - | `poke:0095=82,poke:008A=48,poke:008F=48,poke:0098=8C,poke:0099=A1,poke:0011=00,poke:0003=16,w240` |
| [83](maps/map_83.png) | 84 | field 22 (36,7) | - | `poke:0095=83,poke:008A=89,poke:008F=89,poke:0098=E4,poke:0099=A1,poke:0011=00,poke:0003=16,w240` |
| [84](maps/map_84.png) | 83, 85 |   | - | `poke:0095=84,poke:008A=87,poke:008F=87,poke:0098=E4,poke:0099=A1,poke:0011=00,poke:0003=16,w240` |
| [85](maps/map_85.png) | 84 |   | - | `poke:0095=85,poke:008A=22,poke:008F=22,poke:0098=E4,poke:0099=A1,poke:0011=00,poke:0003=16,w240` |
| [86](maps/map_86.png) | 87 | field 26 (46,22) | - | `poke:0095=86,poke:008A=12,poke:008F=12,poke:0098=AD,poke:0099=A5,poke:0011=00,poke:0003=16,w240` |
| [87](maps/map_87.png) | 86, 88 |   | - | `poke:0095=87,poke:008A=32,poke:008F=32,poke:0098=AD,poke:0099=A5,poke:0011=00,poke:0003=16,w240` |
| [88](maps/map_88.png) | 87, 88 |   | - | `poke:0095=88,poke:008A=42,poke:008F=42,poke:0098=AD,poke:0099=A5,poke:0011=00,poke:0003=16,w240` |
| [89](maps/map_89.png) | 8A | field 25 (30,27) | - | `poke:0095=89,poke:008A=69,poke:008F=69,poke:0098=DD,poke:0099=A6,poke:0011=00,poke:0003=14,w240` |
| [8A](maps/map_8A.png) | 89, 8B |   | - | `poke:0095=8A,poke:008A=89,poke:008F=89,poke:0098=DD,poke:0099=A6,poke:0011=00,poke:0003=16,w240` |
| [8B](maps/map_8B.png) | 8A |   | - | `poke:0095=8B,poke:008A=AA,poke:008F=AA,poke:0098=DD,poke:0099=A6,poke:0011=00,poke:0003=16,w240` |
| [8C](maps/map_8C.png) | 8D | field 2D (23,50) | - | `poke:0095=8C,poke:008A=4F,poke:008F=4F,poke:0098=AD,poke:0099=A5,poke:0011=00,poke:0003=16,w240` |
| [8D](maps/map_8D.png) | 8C, 8E |   | - | `poke:0095=8D,poke:008A=4D,poke:008F=4D,poke:0098=AD,poke:0099=A5,poke:0011=00,poke:0003=16,w240` |
| [8E](maps/map_8E.png) | 8D |   | - | `poke:0095=8E,poke:008A=22,poke:008F=22,poke:0098=AD,poke:0099=A5,poke:0011=00,poke:0003=16,w240` |
| [8F](maps/map_8F.png) | 90 | field 2E (37,51) | - | `poke:0095=8F,poke:008A=0E,poke:008F=0E,poke:0098=AD,poke:0099=A5,poke:0011=00,poke:0003=16,w240` |
| [90](maps/map_90.png) | 8F, 91 |   | - | `poke:0095=90,poke:008A=0C,poke:008F=0C,poke:0098=E5,poke:0099=AC,poke:0011=00,poke:0003=16,w240` |
| [91](maps/map_91.png) | 90 |   | - | `poke:0095=91,poke:008A=10,poke:008F=10,poke:0098=AD,poke:0099=A5,poke:0011=00,poke:0003=16,w240` |
| [92](maps/map_92.png) | 93 | field 11 (23,76) | - | `poke:0095=92,poke:008A=78,poke:008F=78,poke:0098=56,poke:0099=B3,poke:0011=00,poke:0003=16,w240` |
| [93](maps/map_93.png) | 92, 94 |   | - | `poke:0095=93,poke:008A=76,poke:008F=76,poke:0098=56,poke:0099=B3,poke:0011=00,poke:0003=16,w240` |
| [94](maps/map_94.png) | 93 |   | - | `poke:0095=94,poke:008A=39,poke:008F=39,poke:0098=56,poke:0099=B3,poke:0011=00,poke:0003=16,w240` |
| [95](maps/map_95.png) | 96 | field 14 (6,86) | - | `poke:0095=95,poke:008A=95,poke:008F=95,poke:0098=C6,poke:0099=B5,poke:0011=00,poke:0003=16,w240` |
| [96](maps/map_96.png) | 95, 97 |   | - | `poke:0095=96,poke:008A=93,poke:008F=93,poke:0098=C6,poke:0099=B5,poke:0011=00,poke:0003=16,w240` |
| [97](maps/map_97.png) | 96 |   | - | `poke:0095=97,poke:008A=57,poke:008F=57,poke:0098=C6,poke:0099=B5,poke:0011=00,poke:0003=16,w240` |

## 3. Groups (one row per dungeon)
| Floors | Look | Where | Shot |
|---|---|---|---|
| 00 | town, grey stone | Granville, centre of the continent (30,30); the game starts here | `start_granville` |
| 01 | town | north of Granville (25,19), same section 25 | - |
| 02 | town | west coast (4,24) | `town_02` |
| 03 | town | east (53,26) | - |
| 04 | town | south-west of Granville (21,35) | - |
| 05 | town | south (46,51) | `town_05` |
| 89, 8A, 8B | castle: green stone, olive cellar | Granville Castle just north of Granville (30,27); the cellar stairs are in the walled centre room 79 | `castle_entrance`, `castle_cellar` |
| 80-82 | blue stone | north-west island (12,7) | `dungeon_80` |
| 83-85 | rose stone | north island (36,7) | `dungeon_83` |
| 86-88 | cyan stone | north-east (46,22) | `battle_skeleton` |
| 8C-8E | green stone | south-west coast (23,50) | `dungeon_8c` |
| 8F-91 | granite | south (37,51), near town 05 | `dungeon_8f` |
| 92-94 | white stone; a guardian waits on the arrival square of 92 | lower world (23,76) | `boss_guardian` |
| 95-97 | lime stone | lower world (6,86) | `dungeon_95` |
| 40-42 | forest | east island (57,36) | `forest_40` |
| 43-45 | forest (entered at 44) | west (12,40) | `forest_43` |
| 46-48 | forest | lower world (8,89) | `forest_46` |
All rows **(verified)**: floors loaded in play (warp tokens), look from the shots; positions from the exit tables
**(RAM)**.

## Open questions
- How the lower world is reached in normal play (not found yet; candidates: a spell,
  the Ring of Flight or an undersea passage).
- Places `(xx)` on the overworld with no floor exit (2F, 3F, 4F ... cells): the Spring of Sara, the sanctuary,
  caves? Not visited.
- Meaning of the red/blue feature marks on dungeon squares.
- Which story name belongs to which dungeon.
