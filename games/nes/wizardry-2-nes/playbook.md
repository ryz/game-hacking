# Wizardry II: Knight of Diamonds - The Second Scenario (NES, USA) - playbook

Everything an agent needs to play this game efficiently: read it before playing, add to it after every run.
Status of each fact: **verified** (seen in the emulator, with the route) or **source** (manual/FAQ/wiki, not yet
checked). Never delete a fact that turned out wrong: strike it and say what is true.

## Identity
| Field | Value |
|---|---|
| Title (EN / original) | Wizardry: Knight of Diamonds - The Second Scenario (US NES; title screen "The Knight of Diamonds", verified); Famicom original ウィザードリィIII ダイヤモンドの騎士 (Wizardry III: Diamond no Kishi, Data Crystal) |
| Platform / model used | NES, NTSC (`game.json`); NES 2.0 header, mapper 4 (MMC3), 128 KiB PRG + 128 KiB CHR, 8 KiB battery RAM; CRC32 `10cd0310` ("Wizardry - The Knight of Diamonds (U) [!]" on Data Crystal) |
| Release (region, year) | North America April 1992 (NESCartDB / Data Crystal; HonestGamers says October 1992); Famicom 3 September 1990 (Data Crystal); copyright page 1991 (verified) |
| Developer / publisher | Programmed by Game Studio, published by ASCII Entertainment Software; Andrew Greenberg / Sir-Tech (copyright page, verified) |
| Genre | First-person party dungeon RPG: six adventurers, the castle of Llylgamyn (menus), six maze floors of 20x20 squares ("the Ruins under the Temple of Gnilda") |
| Players / save system | 1 player; **battery save**: the roster lives in battery RAM; Edge of Town > Leave Game is the save point ("* CAUTION * Turn Power switch off while pressing Reset-switch", "[A] to more Wizardry") (verified: exported `01_party` reloads) |

Same engine as `games/nes/wizardry-nes/` (Game Studio): same menus, keys, wall format and record layout of the special
squares, but **every RAM address, the name keyboard and the map location differ** (MMC3 with 8 KiB banks).
No character import: the NES version creates new characters in the Training Grounds (no Transfer option in
Training Grounds or Edge of Town) and ships six pre-made level 1 characters (verified; the PC original imported a
Wizardry I party, the Famicom one used the Turbo File).

## Boot sequence
- Power-on: ASCII logo (f60-f240), copyright page (f300-f840, waits by itself, presses ignored), then the title
  scrolls in horizontally; **Start is ignored until the scroll ends** (at f900 the title is still moving and a
  Start there is lost, verified with emu.py runs at w900/w1000/w1100).
- `TITLE` = `w1000` -> title menu "Start game / Select switch", logo animating (verified, checkpoint `title`).
- `CASTLE` = `TITLE,start,w120` -> Castle menu "Llylgamyn" (Start goes straight there; no copyright page in between,
  unlike Wizardry I) (verified).
- Select switch (title, `down,start,w60`): MAZE SOLID/LINE, MUSIC ON/OFF, SOUND ON/OFF, RETURN TO TITLE (verified,
  same as Wizardry I).
- `PARTY` = `CASTLE,TRAINING,PARTYMAKE,b,w60,b,w60,ADDPARTY`: creates the six playtest characters, forms the party,
  ends on the Castle menu (verified in one `do` from power-on, checkpoint `castle`).
- `MAZE` (from the Castle menu) = Edge of Town > Maze > "Descending into the Ruins under the Temple of Gnilda" > Camp
  opens > B > "Stairs up --- Take them?" No -> floor 1 (0,0) facing north (verified, checkpoint `start`).
- Macros need their waits: the same tokens typed as separate `do` calls (with settles) and as one `do` behave
  differently (CASTLE with `w60` instead of `w120` lost the B press; use the macros as written).

## Controls
| Context | Button | Action | Status |
|---|---|---|---|
| Title | Up/Down, Start | Start game / Select switch | verified |
| Menus (castle, tavern, camp) | Up/Down, A | move cursor, choose | verified |
| | B | back one menu (Training Grounds -> Edge of Town -> Castle; Tavern -> Castle) | verified |
| Name keyboard | D-pad, A | move the arrow, type the key; 4 rows x 13: `0-9 ! ? #` / `A-J $ % &` / `K-T / ( )` / `U-Z . - + : End`; starts on "0", **upper case**, cursor back on "0" for every new name | verified |
| | Select | lower case / symbols page (`a-z`, card suits, quotes) | verified |
| | B | delete the last letter | verified |
| | End (row 4, column 12) | finish the name | verified |
| | Right at a row end | continues on the next row (linear cursor) | verified |
| Stats screen | Up/Down, Right/Left, A | choose stat, add/remove bonus points, finished (refused while points are left) | verified |
| Maze | Up | step forward (walls and doors stop it) | verified |
| | A | step forward through a door | verified (floor 1 (5,4) -> (5,5)) |
| | Left / Right | turn 90 degrees | verified |
| | Start | hide/show the party window | verified (window toggled) |
| | B / Select | Camp / maze menu (Quit, Search, Set Timer, Leave: ROM text) | Camp verified; Select source (ROM text, same as Wizardry I) |
| Stairs prompt | Up/Down, A | Yes / No | verified |
Joypad dispatch in the maze: bank 13 $A586 (jump table at $A5A6 by button bit), as in Wizardry I (code).

Input timing: the default press (hold 8, wait 40) works everywhere tried; typing letters needs only `a,w20`.

## Game structure
- Castle "Llylgamyn": Gilgamesh's Tavern (Add / Remove / Inspect / Divvy Gold / Leave), Adventurer's Inn (Stables
  free, Cot 10, Economy 50, Merchant 200, Royal Suite 500 GP/week, Pool Gold, Leave), Boltac's Trading Post,
  Temple of Cant, Edge of Town (Training Grounds, Maze, Restart an "OUT" party, Leave Game, Castle) (verified menus).
- Training Grounds: Create / Inspect / Delete / Change Name / Change Class / Leave (verified). Create: name ->
  "Create this character?" -> race (Human Elf Dwarf Gnome Hobbit) -> alignment (Good Neutral Evil) -> bonus points
  -> class (eligible list) -> "Keep this character?" (verified, identical to Wizardry I).
- Roster on a fresh battery: FIGHTER1, FIGHTER2, CLERIC1, THIEF1, MAGE1, MAGE2, all level 1 (verified).
- Maze: 6 floors of 20x20 squares, wrapping. Floor 1 (0,0) stairs up to the castle; stairs down at floor 1 (5,5)
  -> floor 2 (5,5) (verified) and (16,2) -> floor 2 (16,2) (ROM data); full connection list in
  `design/maps.md`.
- Story (ROM text): Gnilda's staff was taken back; the party must collect the regalia of the legendary Knight of
  Diamonds ("one must acquire the five, and get over seven barriers") and present it in her temple to receive
  "the staff of Gnilda". Notable texts: a wishing well ("Wishes: 5000 G.P."), a sage asking 100,000 gold, an old
  man trading keys (black/red/master key), "Officers only!" door with an orc, "One alone." (one-member passage on
  floor 6, special types 11-13), "Reset backed up data?" (save menu text).
- All strings of the ROM: `work/scout/wizardry-2-nes/strings.txt` (scratch, regenerate with a 6-byte ASCII scan;
  text is plain ASCII).

### Maze data (for floor maps in `design/maps/`)
Decoded from the cell fetch (code: bank 13 $A8B7 maps PRG bank 9 at $8000; position in $EA/$EB/$EC):
- **PRG bank 9** (8 KiB, file offset `$12010`): word table at `$8000` indexed by floor*2 -> floor block (floor 1
  `$800E`, then +`$4B0`): wall grid 400 bytes, flag grid 400, zone grid 400 (area numbers, not drawn).
- Grids 20x20, index `y*20 + x` (x east, y north; (0,0) south-west). Wall byte and flag byte as in Wizardry I
  (2 bits per side N/E/S/W: 0 open, 1 wall, 2 door, 3 secret door; flag `$80` room, `$40` darkness, `$20` special,
  low 5 bits = record) (code; walls and doors verified at floor 1 (5,5): doors W, N, E as drawn).
- **Special records**: ROM originals in **PRG bank 4** (8 KiB) at offset `$04FB` + 64*(floor-1) (16 records x 4
  bytes: type a b c); working copies in battery RAM `$6B88` + 65*(floor-1), current floor at `$6E79`; one-time
  events clear their record (type 0). Types 00-16, dispatch bank 13 `$B1F6`, jump table `$B219`: 01 stairs to
  (a,b,c) (verified), 02 teleport, 03 chute, 04 rock/death, 05/06 pit, 07 spinner, 08 message, 09 message +
  castle/teleport, 0A message + fight, 0B alarm, 0C-0E message/search/prompt events, 0F guardian fight, 10 fixed
  fight, 11-13 one-member passage, 14 party check, 16 prompt event (code; meanings in `tools/maps.py`).
- Renderer: `python3 games/nes/wizardry-2-nes/tools/maps.py` -> `design/maps/floor_NN.png` + `atlas.png`; `--text`
  -> `design/maps/floors.txt` (done for all 6 floors).

## Shot plan
Captured 2026-11-18: 91 shots in `shots.txt` (game order), published in `shots/main/`.
- [x] boot: ASCII logo, copyright page; title; options (Select switch)
- [x] castle menu, Edge of Town, Training Grounds, name keyboard, race/alignment/stats/class screens, tavern roster
  (pre-made + playtest), character sheet (Inspect), spell books
- [x] inn rooms + level-up, Boltac's (buy, bought, stock), temple + cure
- [x] maze: start, "Descending into the Ruins" text, stairs prompt, camp, maze menu (Select), full view (Start)
- [x] battle: guardian, two groups, orders, spells (mage, cleric, enemy), melee, victory (E.P.), guardian item,
  chest + inspect + trap + loot + gold, poisoned, member killed, party wiped (game over)
- [x] story events: Gnilda's apparition, "Officers only!", wishing well, sage, key traders, "One alone.", barriers,
  floor 5 rock, fountain, regalia, the staff of Gnilda ending, Knights, credits, Mark of Gnilda
- [ ] not taken: LINE wall mode, Boltac's Sell/Identify, darkness square, spinner, Dispell, item use, level drain

## Strategy and walkthrough notes
- Level 1 characters die fast: use the veteran party (`@veterans`: macro `VETERANS` from
  `tools/veterans.py`, levels 11-13, gold, spells, equipment; poked before `ADDPARTY` so the castle list shows
  it) or the save `02_veterans`. ~~Battery RAM is unreachable for `poke`~~: since 2026-11-18 pokes reach it.
- Special squares: `work/capture/wizardry-2-nes/scan.py FLOOR` (scratch, see Emulation notes) warps next to every
  record of a floor (special table poked into `$6E79`), steps in and logs texts + positions. Shot routes for
  events are made the same way (`mk.py`): `@vstart,poke:00EC=F,poke:00EA=X,poke:00EB=Y,poke:00E9=D,
  poke:6E79=<64-byte table of the floor>,left,w30,right,w30,settle,up` (`a` through a door).
- Random fights: step from a corridor into a room square (flag $80) on floors 2/4 (`enc.py`); floor 2 (14,5) ->
  (14,4) facing S meets 7 Women in Robes + 2 Men at Arms (`@robes`).
- One-hit kills / deaths: battle HP low bytes at `$03BA + i` (0-5 party, 6-14 group 1, 15-23 group 2, ...);
  poke party HP to 1 before the round for deaths and a wipe (`gameover`).
- Ending: RYZ alone wearing ids 7D-81 equipped (`@knight`), floor 6 (1,1) facing N, A three times (doors) ->
  floor 1 Gnilda's room, staff; stairs up at floor 1 (0,0) -> Congratulations.
- Warp: `poke:00EC=FLOOR,poke:00EA=X,poke:00EB=Y,poke:00E9=DIR,left,w30,right,w30` (the turn redraws the view;
  verified on floor 1). Step onto the special square with Up (or A through a door) to trigger it.
- A poke to a different floor keeps the old floor's special table in `$6E79` (copied at floor entry, code
  `$B1D0`): arrive by stairs/teleport (e.g. `@f2`) and warp within the floor.
- Encounters depend on frame timing (as in Wizardry I): vary the `wN` before the last step.
- After `sav:01_party` the party is not formed: `CASTLE,ADDPARTY`.

## Naming
Party of six, created by `PARTYMAKE` (macros `MAKE1`..`MAKE6`, generated by `python3
games/nes/wizardry-2-nes/tools/party.py --write`; each starts and ends on the Training Grounds menu):
| Name | Race | Alignment | Class | STR IQ PIE VIT AGI LUC | HP at L1 |
|---|---|---|---|---|---|
| RYZ | Human | Good | Fighter | 17 8 5 13 10 9 | 11 |
| CONDI | Dwarf | Good | Fighter | 16 7 10 15 7 6 | 12 |
| EBO | Gnome | Good | Cleric (Priest) | 9 7 16 10 11 7 | 11 |
| CUBI | Hobbit | Neutral | Thief | 7 7 7 9 16 15 | 4 |
| DEDDO | Elf | Good | Mage | 7 17 10 8 11 6 | 4 |
| MNZ | Elf | Good | Wizard (Bishop) | 7 15 14 7 10 6 | 4 |
Stats are cheated: on the stats screen the macro pokes each stat one below its target plus 6 bonus points
(`$004D-$0052`, bonus `$0040`; zero page, so pokes work) and presses Right on every row (verified: Training
Grounds Inspect lists all six with the right race/class).

## Shortcuts
| What | How (tokens / prefix / code) | Source | Status |
|---|---|---|---|
| Warp (floor, x, y, facing) | `poke:00EC=F,poke:00EA=X,poke:00EB=Y,poke:00E9=D,left,w30,right,w30` | scout + Data Crystal RAM map | verified (floor 1) |
| Character stats at creation | `$004D-$0052` + bonus `$0040` on the stats screen | scout | verified |
| Roster edits (gold, HP, level, E.P.) | `python3 games/nes/wizardry-2-nes/tools/roster.py edit IN.sav OUT.sav SLOT:OFF=HEX,...` (fixes the check value) -> `sav:OUT` | scout | verified (gold 1873, HP 85 shown by Inspect) |
| Pre-made characters | FIGHTER1 ... MAGE2 on a fresh battery | scout | verified |
| Veteran party | `VETERANS` macro before `ADDPARTY` (`@veterans`), or `sav:02_veterans,CASTLE,ADDPARTY` | capture | verified |
| Regalia / ending | `@knight` (RYZ alone with Hrathnir + KOD's helmet/shield/gauntlets/armor equipped) | capture | verified |
| Game Genie / Action Replay codes | none looked up (time box); GameFAQs cheats page not tried | - | open |

### Saves (rom/saves/wizardry-2-nes/, never committed)
| Name | Contents (progress, party, items) | URL | SHA-1 | Status |
|---|---|---|---|---|
| 01_party (made here, committed in `saves/`) | roster with the playtest party, level 1 | - | see `saves/README.md` | verified (`sav:01_party,CASTLE,ADDPARTY` -> party formed, Inspect) |
| 02_veterans, 03_regalia, 04_ending (committed) | see `saves/README.md` | - | - | verified (all 12 characters reload) |
| test_rich (scratch) | 01_party with RYZ at 1873 gold, 85/85 HP (`roster.py edit`) | - | - | verified, delete or replace |
No downloadable saves looked for.

## Extra sets
- `compare-maze` (11 shots, list `games/nes/wizardry-2-nes/shots-compare-maze.txt`, owner's request 2026-11-18): the
  options screen with LINE and five maze views (floors 1, 2, 4, 5, 6) in SOLID and LINE; side by side in
  `design/maze-solid-vs-line.png`. LINE draws thin white outlines (Wizardry I: brown bricks outlined). The LINE
  drawing takes different CPU time, so a view next to a random fight can meet it in one mode only: floor 2 uses
  the `f2` checkpoint for that reason. Rebuild: `python3 tools/shoot.py wizardry-2-nes compare-maze --list
  games/nes/wizardry-2-nes/shots-compare-maze.txt --publish`.

## RAM map (for `game.json` "ram" watches and pokes)
| Address | Size | Meaning | How found |
|---|---|---|---|
| `$6DA3` | 1 | Select switch MAZE: 1 SOLID, 0 LINE (battery RAM; Wizardry I uses $7ABC, 1/2); poke, then turn left/right to redraw | play.py diff over the option (verified, set `compare-maze`) |
| `$00EA` | 1 | x, 0-19 east | step diff + code `$A6FB` + Data Crystal (verified) |
| `$00EB` | 1 | y, 0-19 north | same (verified) |
| `$00EC` | 1 | floor (0 castle, 1-6) | same (verified: 2 after the stairs) |
| `$00E9` | 1 | facing 0 N, 1 E, 2 S, 3 W | turn diff + code (verified) |
| `$00ED-$00EF` | 3 | previous x, y, floor (pushed back to after a fight/run) | code `$8707`, Data Crystal |
| `$00C3`, `$00CF` | 1 each | wall byte / flag byte of the current square (`$C3-$CE`, `$CF-$DA` view cells) | code `$A8EE` |
| `$00C4-$00C6` | 3 | arguments a b c of the special record being run | code `$B204` |
| `$0040`, `$0043-$004B`, `$004D-$0052` | | creation: bonus points, name length + name, STR..LUC (`$0053-$0058` race base values) | dump + poke (verified) |
| `$6400 + slot*$60` | 96 | roster record, 20 slots; second copy at `$7800 + slot*$60` for the made characters | battery dump (verified) |
| record `+$01`, `+$02-$09` | 1, 8 | name length, name (ASCII, space padded) | dump |
| record `+$0A` | 1 | race/class/alignment packed (RYZ 00, CONDI 40, EBO 68, CUBI 8D, DEDDO 24, MNZ 30) | dump |
| record `+$0B-$10` | 6 | STR IQ PIE VIT AGI LUC | dump (matches creation) |
| record `+$11-$16` | 6 | **gold**, packed BCD big-endian | edited save + Inspect (verified) |
| record `+$17-$1C` | 6 | E.P., packed BCD big-endian (tentative, 0 at level 1) | dump |
| record `+$1D/$1E`, `+$1F/$20` | 2+2 | **HP now / max, little-endian** (the castle party list is built when the party is formed: poke before `ADDPARTY`) | edited save + Inspect (verified) |
| record `+$22`, `+$23`, `+$24`, `+$25`, `+$26` | 1 each | level, **status** (0 OK, 3 P-lyze, 5 dead, 6 ashed), age in years, ?, AC (signed; the maze recomputes it) | Inspect + Temple (verified) |
| record `+$27-$2D`, `+$2E-$34` | 7 + 7 | mage / cleric spell points per level, high nibble now, low nibble max | Inspect (verified) |
| record `+$35-$3B`, `+$3C-$42` | 7 + 7 | mage / cleric spells known, one byte per level, bit n = n-th spell of the level | Read Spell (verified) |
| record `+$43-$4A`, `+$4B-$52`, `+$53` | 8, 8, 1 | item flags ($80 equipped, $20 unidentified), item ids, item count | Inspect (verified) |
| record `+$58` bit 1 | | has won the regalia trial (type 13 sends the member to floor 6 (3,3) instead) | code bank 13 `$B84E` |
| item ids | | 01 long sword ... 0E helm, 16 padded leather, 17 shiny chain, 18 sturdy plate, 19 iron shield, 1D sword of swishes, 22 helm of hardiness, 2F gloves of copper, 47 dagger of speed, 7C staff of Gnilda, 7D Hrathnir, 7E KOD's helmet, 7F KOD's shield, 80 KOD's gauntlets, 81 KOD's armor, 82 corroded key, 83 gory badge, 84 weird emblem, 85 key of ebony, 86 key of cloister, 87 mithril key, 88 master key, 89 demon's stone | Inspect (verified) |
| `$7800 + slot*$60` | 96 | backup copy of each record (poke both when editing a castle record) | dump |
| `$0390 + i`, `$03BA + i`, `$03E4 + i` | | battle tables: status?, HP low, HP high (i: 0-5 party, groups of 9 from 6) | dump + poke (verified: deaths) |
| record `+$5E/$5F` | 2 | check value (CRC, `tools/roster.py`); a bad record is emptied at power-on (code `$8D42`) | code bank 4 `$8D8C` (port verified on 18 records) |
| `$6B80`, `$6B81`, `$6B82-` | | roster count, party size, party slot numbers | dump |
| `$6B88 + 65*(floor-1)` | 65 each | working special tables per floor | dump = ROM bank 4 `$84FB` tables |
| `$6E79` | 64 | current floor's special table | code `$B1E0` |

## Emulation notes
- NTSC, default press. Deterministic.
- ~~**Battery RAM (`$6000-$7FFF`) is not reachable with `play.py peek/poke/dump`**~~ (fixed 2026-11-18: pokes
  reach it; a poked record survives a power cycle only if the game saves it again, i.e. it is in the party at
  Leave Game) - old note:: the game keeps the MMC3 RAM
  disabled except while it accesses it, so peeks return open bus (`$6E` at `$6Exx`) and pokes are dropped
  (verified: a gold poke in the castle did nothing). Read it with `play.py export` or a script calling the
  backend's `battery()` (`work/scout/wizardry-2-nes/sram.py ROUTE OUT.bin`); change it with `tools/roster.py edit`
  and `sav:NAME`.
- **Inputs right after a menu closes are lost**: a route that ends on a menu that just opened/closed (e.g. `b,w60`
  out of the tavern) may drop the first presses of the next `do`; end checkpoints with an extra `w30` or start
  the next route with `w30` (the first `knight` route ended in the Tavern menu and sent MAZE into the Inn).
- Routes recorded after `play.py undo` were not reliable here (ending shots re-made with explicit tokens).
- Capture helpers (scratch, `work/capture/wizardry-2-nes/`): `steps.py` (session do-groups -> sheet), `add.py`
  (shot line = another shot's route + tokens), `mk.py` (event shot by warp), `scan.py`, `enc.py`, `order.py`.
- The party window is hidden after the floor-2 stairs prompt (checkpoint `f2`); Start shows it.
- The title logo keeps animating (settle may stop at any phase); the `title` checkpoint replays identically.
- play.py sessions used: `--name wiz2` (checkpoints), `wiz2b` (save tests), `wiz2c` (helper
  `work/scout/wizardry-2-nes/steps.py`).

## Checkpoints
| Name | What |
|---|---|
| `title` | title menu, Start game |
| `castle` | Castle menu, playtest party formed, level 1, no equipment |
| `start` | floor 1 (0,0) facing north, first control in the maze |
| `f2` | floor 2 (5,5) facing north after the stairs down from floor 1 (5,5) |
| `veterans` | Castle, veteran party (levels 11-13, `VETERANS`) formed |
| `vstart` | floor 1 (0,0) with the veterans |
| `kobold` | floor 1 (19,10): guardian Kobold King, RYZ's options |
| `eyes` | floor 4 (1,4): 2 Evil Eyes (no Spell order) |
| `robes` | floor 2 (14,4): 7 Women in Robes + 2 Men at Arms |
| `knight` | Castle from save 02_veterans: RYZ alone wearing the five regalia pieces |
| `finale` | Castle after the ending and credits, RYZ's Inspect with the Mark of Gnilda |
The first four rebuilt from an empty cache and compared with a cache hit: identical frames (2026-11-18).

## Sources
| Source | URL | Used for | Accessed |
|---|---|---|---|
| Data Crystal | https://datacrystal.tcrf.net/wiki/Wizardry_II:_Knight_of_Diamonds_(NES) | release dates, mapper, Japanese title | 2026-11-18 |
| Data Crystal RAM map | https://datacrystal.tcrf.net/wiki/Wizardry_II:_Knight_of_Diamonds_(NES)/RAM_map | $E9-$EF position/facing, $C3-$C7 view walls (confirms the scout's own finding) | 2026-11-18 |
| Search summaries (NESCartDB, HonestGamers, Hardcore Gaming 101) | https://nescartdb.com/profile/view/1156 | US release April 1992 (HonestGamers: October 1992); Famicom Turbo File transfer removed | 2026-11-18 |
| ROM text and code | `tools/dis6502.py wizardry-2-nes BANK ADDR --bank-kib 8` | maze format, specials, roster check value, story texts | 2026-11-18 |
| Wizardry I scout/capture | `games/nes/wizardry-nes/playbook.md` | engine layout to port | 2026-11-18 |

## Open questions
- (2026-11-18 capture) answered: special types (see `design/maps.md`), status/level/spell/item offsets, regalia
  ids, the ending. Still open: types 06/07 effects, floor 5 barrier item, what the well/sage give.
- ~~Special types 03-16: meanings are a first reading of the handlers (marked "(code)" in `tools/maps.py`); check in
  play, especially type 04 (158 squares on floor 5: deadly rock or something else?) and 0C-0F/14/16.
- Message numbers in the records (`b`) -> texts: the message table was not found (text is ASCII in banks 0-1;
  the printer starts at bank 13 `$A97B`).
- Record `+$0A` packing, level/E.P./age/spell offsets: confirm with an edited save (as done for gold and HP).
- Which fixed fights/guardians arm on floor entry (Wizardry I used a bitmap set by stairs/elevator arrival).
- Monster and item tables (names, ids), the Knight's regalia item ids.
- Game Genie codes (GameFAQs cheats page not tried).
