# Maps - Devil Buster, the Tokyo overworld, the towns

Pictures in `maps/` are stitched from the game's own screen: the party is warped (RAM) to a grid of positions during
a map transition, the sprites are hidden and the centre 8 x 7 squares of every frame are pasted together
(`work/capture/mt2/mapgrab.py`, round 2). One square = 16 x 16 pixels; the picture's top-left square is given per map.
Event squares come from the overhead event table in the ROM (file offset 0x7DAB-0x7F40, entries `x y event`) and were
each stepped on (sheets `work/capture/mt2/dbs_dn/`, `work/capture/mt2/scan1/`) **(RAM, verified per square below)**.

Warp tokens (game.json macros, see the playbook): `@db_f1_back,DBEV:X:Y1` fires the Devil Buster event at X,Y (Y1 =
Y + 1, the square below; the party steps up onto it); `@overworld_demons,TOWNEV:X:Y1` the same for town squares.

## Devil Buster (`maps/devil_buster.png`, top-left square 50,08; area byte 02, floor 1 area 03)
The game inside the game is one overhead map: ten 16 x 16 blocks, two columns (x 50-5F and 68-77) and five rows
(y 08, 20, 38, 50, 68). Eight of them are mazes; the two grey blocks at 50,50 and 50,68 are stone temples (statues,
blue orbs) that the stairs list leads to but that are not reached in normal play.
| Block (top-left) | Floor | Connections (stairs, from the warp table at ROM 0x744D) |
|---|---|---|
| 50,08 | 1 (start 51,08; **Micon town**, "8F of the Daedalus Tower") | 57,0C <-> 6F,0C (floor 2) |
| 68,08 | 2 | 76,0C <-> 5E,24 (floor 3) |
| 50,20 | 3 | 5E,20 <-> 76,20; a stairs maze of five more pairs to floor 4: 59,27/71,27, 54,2A/6C,2A, 56,2A/6E,2A, 51,2D/69,2D, 5E,2D/76,2D |
| 68,20 | 4 | (see floor 3) |
| 50,38 | 5 | 56,3B <-> 6E,3B (floor 6) |
| 68,38 | 6 | 6E,42 <-> 6E,5A (floor 7) |
| 68,50 | 7 | 6C,5A <-> 6C,72 (floor 8) |
| 68,68 | 8 | 76,67 -> 5B,7F (grey temple): the stairs square is inside the top wall, never walkable (findings) |

Event squares (event id in brackets; all **verified** by stepping on them, round 2):
| Square | Event | What happens |
|---|---|---|
| 5E,08 | 8F | **fusion master**: "CHILDREN.." FUSE TWO / HELP / ... / STATUS / LEAVE (shots `fusion_*`) |
| 59,0C | 8E | healer "I CAN HEAL." (price per hero) |
| 53,0E | 15 | Micon's elder: "QUIT THIS GAME" / LEAVE |
| 53,11 | 16 | "TREASURE!" chest ("CHECK?" YES/NO) |
| 58,11 | 04 | shop "BUY OR SELL?": DAGGER 100, COPPER AXE 200, KRIS 400, BROAD EDGE 1500, FT SUIT 200, SHIN MAIL 400, KEVLAR 900, IRONHEAD 600 |
| 52,2C | 25 | the fallen **god statue**: "OFFER AN ITEM TO THE STATUE?" -> S.ORB -> Pazuzu is freed (end of Devil Buster) |
| 76,23 | 24 | **Taurus** (boss): "HEY BRATS! DIE!" then the battle; drops the S.ORB |
| 55,11 / 6B,11 / 59,0A / 76,0A / 5B,2C / 56,11 / 70,11 / 72,14 / 6A,1F / 5D,2C / 54,2C | 17-21 | townsfolk and wall writing: Micon town, no talking to demons at full moon, fusion explained, MAG feeds demons, "TAURUS MUST BE KILLED!", allies' skills, INT/LUK, "TAURUS HOLDS THE S.ORB", "OFFER THE S.ORB TO THE FALLEN GOD STATUE", enemies target the first party member |
| 5A,11 72,11 5A,29 72,29 5A,41 72,41 72,59 72,71 | 23 | "A JAMMED ELEVATOR.." (one per floor) |
| 5B,3A / 76,3A / 6E,52 / 6B,3D / 6A,67 | 79 7E 7F 8B 97 | NPCs with untranslated lines (floors 5-8) |
| 6B,5C / 72,52 | 7D | a trap: the party is sent back to the start 51,08 |
| 76,6A | 98 | Cerberus speaks (untranslated), YES/NO |
| 6A,6A | 37 | a door picture with an untranslated line |

## Tokyo overworld (`maps/overworld.png`, top-left square 00,07; area byte 01/04)
Red wasteland roads cross a ring of green hills, rocks, ice fields, purple ruins and a dark swamp; purple holes are cave
entrances (0E,2F and 1C,2B lead to the first cave **(verified)**). Doors from the warp table (overworld -> town map,
area 05): 47,13 -> 09,58; 3C,42 -> 27,54; 17,13 -> 5D,73; 11,2B -> 5B,7E (the settlement with the armour shop and the
save totem, shot `village`); 0B,3F -> 58,56. Exits back: 09,D8 -> 47,13; 27,D4 -> 3C,42; 5D,73 -> 17,13; 5B,7E ->
11,2B; 58,56 -> 0B,3F; 77,97 -> 20,2C (area 06).

## Towns (`maps/towns.png`, top-left square 00,07; area byte 05)
All towns and building interiors share one overhead map with area byte 05. Event squares found by stepping on them
(**verified**, round 2):
| Square | Event | What |
|---|---|---|
| 59,7F | 46 | save **totem**: LEAVE / SAVE / Teleport (DATA1/DATA2, "RECORDED.") |
| 5D,7F | 0E | armour shop (BOD / HELM / GLOVE / BOOT; IRON SUIT 1800, Fire Guard 15000, Dragon Mail 40000) |
| 5D,6F, 0B,D7, 2B,D9, 3D,D7 | 47 48 49 4A | further totems |
| 59,6F | 08 | gun shop "FOR WHOM?" |
| 2B,BF | 5A | weapon shop "CHOOSE ONE." (names in kana; 4800, 660, 250, 300, 250) |
| 55,C3 | 4B | registry man "YO." REGISTER / LISTEN / LEAVE (shot `registry`) |
| 51,C7 | 4C | a woman, "NEED HELP?" YES/NO |
| 55,C7 | 4D | slot machine "WANT TO PLAY SLOTS? ... TRY IT." |
| 59,C7 | 4E | Mr. Nandi from India, gambling for 1 tin card |
| 59,BF | 4F | "WELCOME TO THE DREAM DRUGSTORE" |
| 55,BF | 28 | bar: SUPA MILK 10, MAG FIZZ 32, M TONIC 40 |
| 0BD7 area, 0FD7, 0DDD, 3FDD | 69 6A 22 ... | NPCs in untranslated text (one names Beelzebub) |
The names of the towns are untranslated labels (shown in kana) and are not identified yet.

## Not mapped yet
The first-person mazes (caves, the shelter floors B1-B4): their walls are not drawn overhead; the shelter B4 event
squares are listed in the playbook (soldier 04,05; gate guards; stairs 00,02 0F,07 0F,0F).
