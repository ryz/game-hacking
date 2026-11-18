# Wizardry: Proving Grounds of the Mad Overlord (NES, USA) - playbook

Everything an agent needs to play this game efficiently: read it before playing, add to it after every run.
Status of each fact: **verified** (seen in the emulator, with the route) or **source** (manual/FAQ/wiki, not yet
checked). Never delete a fact that turned out wrong: strike it and say what is true.
**code** = read from the disassembly (`python3 tools/dis6502.py wizardry-nes BANK ADDR [N]`), not yet seen in play.

## Identity
| Field | Value |
|---|---|
| Title (EN / original) | Wizardry: Proving Grounds of the Mad Overlord (title screen, verified); Famicom original ウィザードリィ (1987, ASCII) |
| Platform / model used | NES, NTSC (`game.json`); NES 2.0 header, mapper 1 (MMC1), 128 KiB PRG + 128 KiB CHR, 8 KiB battery RAM; CRC32 `e59540af` |
| Release (region, year) | North America July 1990; Famicom 22 December 1987 (Wikipedia) |
| Developer / publisher | Game Studio / Nexoft (copyright page, verified); licensed from Sir-Tech and Andrew Greenberg via ASCII |
| Genre | First-person party dungeon RPG: six adventurers, a castle (menus) and a 10-floor maze of 20x20 squares |
| Players / save system | 1 player; **battery save**: the roster lives in battery RAM; Edge of Town > Leave Game is the save point ("*Caution* Turn Power switch off while pressing Reset switch") (verified: exported `01_party` reloads with the roster) |

## Boot sequence
- Power-on: NEXOFT logo (f60-f120), title with the animated Wizardry logo and "Start Game / Select Switch" from
  ~f180, attract copyright page from ~f1560 (intake sheet).
- `TITLE` = `w300` -> title menu, cursor on Start Game; `settle` works there (verified, checkpoint `title`).
- Start Game -> the copyright page (waits for a press) -> Start -> Castle menu. `CASTLE` = `TITLE,start,w60,start,w60`
  (verified). No intro, no name entry before the castle: characters are made in the Training Grounds.
- Select Switch (title, `down,start`) -> options: MAZE SOLID/LINE (wall drawing), MUSIC ON/OFF, SOUND ON/OFF,
  RETURN TO TITLE (verified; controls inside not tried).
- `PARTY` = `CASTLE,TRAINING,PARTYMAKE,b,w30,ADDPARTY`: creates the six playtest characters and puts them in the
  party; ends on the Castle menu (verified, checkpoint `castle`).
- `MAZE` (from the Castle menu) = Edge of Town > Maze > "Entering Proving Grounds of the Mad Overlord" > Camp
  (opens automatically) > B > "Stairs up. Take them?" No -> floor 1 at (0,0) facing north (verified, `start`).

## Controls
| Context | Button | Action | Status |
|---|---|---|---|
| Title | Up/Down, Start | choose Start Game / Select Switch | verified |
| Menus (castle, tavern, camp, battle) | Up/Down, A | move cursor (wraps), choose | verified |
| | B | back one menu (Tavern -> Castle; Castle -> Edge of Town; Training Grounds -> Castle) | verified |
| Name keyboard | D-pad, A | move the arrow (it sits under the key), type the key | verified |
| | Select | **shift** (lower case / symbols <-> upper case); the state persists between names for the whole session | verified |
| | B | delete the last letter | verified |
| | "ret" key (column 12, rows 2-3) | finish the name; empty name = cancel | verified |
| Stats screen | Up/Down, Right/Left, A | choose stat, add/remove bonus points, finished (refused while points are left) | verified |
| Maze | Up | step forward (stops with "Ouch!" at walls **and** doors) | verified + code |
| | Left / Right | turn 90 degrees | verified |
| | Down | turn around (code: jump table entry) | code |
| | A | step forward **through doors** (walls: "Ouch!") | verified + code (`$D1B6`) |
| | B | Camp: Inspect / Reorder / Equip / Leave | verified |
| | Start | hide/show the party window (full-screen view) | verified + code (`$D2E7`) |
| | Select | maze menu: Quit (leaves the party "out" in the maze, back to the castle) / Search / Set Timer / Leave | verified |
| Elevator / prompts | A, Up/Down, B | button choice, B leaves | verified |
| Battle | A, Up/Down | per member: Fight / Parry / Spell / Dispell / Run / Take back (by class), then "Fight / Take back orders" | verified |
| | (menus) | **each member's option cursor is remembered between rounds**: look before pressing A (orders shifted twice) | verified |
| Spell menu (battle) | Down / A | Down pages spell levels L1..L7 ("Cleric Spell L5(3)" = 3 casts left), A enters the list, A casts; group target next | verified |
| Battle messages | A | every message waits for A (`a,w40` per message; some chain without a press) | verified |
| Boltac's buy list | Down / A | Down scrolls the stock one line; A -> "Purchase which?" with a cursor | verified |
Joypad: `$14` = newly pressed (A $80, B $40, Select $20, Start $10, Up 8, Down 4, Left 2, Right 1) (code, `$D16D`).

Input timing: the default press (hold 8, wait 40) works everywhere tried; menu cursors move once per press
(`down*6` is exact). Temple text types out ("MURMUR - CHANT - PRAY - INVOKE": wait ~180 frames). Ending credits scroll by themselves.

## Game structure
- Castle: Gilgamesh's Tavern (Add / Remove / Inspect / Divvy Gold / Leave: forming the party), Adventurer's Inn,
  Boltac's Trading Post, Temple of Cant, Edge of Town (Training Grounds, Maze, Restart an "Out" party, Leave Game,
  Castle) (verified menus).
- Inn (verified): Stables free, Cot 10, Economy 50, Merchant 200, Royal suite 500 gp/week; resting with enough
  E.P. makes the level ("You made the next Level!", stat changes, hit points; shot `inn_levelup`); a full-HP
  rest cost nothing (gold unchanged).
- Boltac's (verified): Buy / Sell / Uncurse / Identify / Pool Gold; long sword 25, short sword 15, anointed mace
  30, anointed flail 150, staff 10, dagger 5, shields 20/40, robes 15, leather 50, chain 90, breast plate 200,
  plate 750, helm 100, potion of Curing 500 (scroll down for more); sells at half price; buying prints the typo
  "* Just want you needed *".
- Temple (verified): lists roster characters **not in the party** whose status is bad ("Who shall we help?":
  dead 250, paralyzed 100, ashed 500 gold at level 1), then "Who will tithe?" from the party; a dead character
  was "cured". Nobody to help -> the Temple entry returns to the Castle menu at once.
- Total party kill: tombstones with the six names, then the Castle with an empty party (members stay in the
  maze, not in the Tavern list) (verified, shot `gameover`).
- Ending (verified): walk up the floor 1 stairs with Werdna's amulet -> "Congratulations", 50,000 G.P. and E.P.,
  the Chevron of Rank, then a scrolling staff roll (checkpoint `ending`).
- Training Grounds: Create / Inspect / Delete / Change Name / Change Class / Leave (verified). Create: name ->
  "Create this Character?" -> race (Human Elf Dwarf Gnome Hobbit) -> alignment (Good Neutral Evil) -> bonus
  points -> class (only eligible classes listed) -> "Keep this Character?" (verified).
- Classes on screen: Fig(hter), Mag(e), Cle(ric) = Priest, Thi(ef), **Wiz(ard) = Bishop** (the US NES names; MNZ
  made with Bishop requirements shows "Wiz" and starts with Mage spells), Samurai, Lord, Ninja (source, not
  seen yet).
- The roster ships with six pre-made level 1 characters: FIGHTER1, FIGHTER2, CLERIC1, THIEF1, MAGE1, MAGE2
  (verified on a fresh battery).
- Maze: 10 floors of 20x20 squares, wrapping at the edges; floor 1 entrance at (0,0) under the stairs up to the
  castle. Elevators: floor 1-4 at (10,8) (buttons A-D, verified), floors 4-9 at (10,0) (ROM data). Werdna on
  floor 10 (record type $22 at (17,4), ROM data). Fixed encounter on floor 1 at (9,13) (Murphy's ghost in the
  original; ROM data, not seen).
- Random encounters: the first one came 3 steps north of the entrance ("A friendly group of Skeletons" in one
  timing, "5 Small humanoids" / "You surprised the monsters" in the play.py timing) (verified).

### Maze data (for floor maps in `design/maps/`)
Decoded from the cell fetch (code: fixed bank `$D3E0` calls PRG bank 4 `$8000` with x in `$6E`, y in `$6F`):
- **PRG bank 4** (16 KiB, file offset `$10010`) holds three word tables indexed by floor*2: `$805C` wall grid,
  `$8070` flag grid, `$8084` special table. Floor 1 walls `$9A40`, then every `$190`; flags `$A9E0`, then every
  `$1D0`; specials = flags + 400.
- Grids: 20x20 bytes, index `y*20 + x` (x east, y north; (0,0) south-west).
- **Wall byte**: 2 bits per side, N bits 0-1, E 2-3, S 4-5, W 6-7: 0 open, 1 wall, 2 door, 3 door (probably
  hidden). Up stops at any non-zero side; A passes sides with the high bit set (code `$D1B6`/`$D1EF`).
- **Flag byte**: `$80` room (fight zone), `$40` darkness (view not drawn: code `$D3E5`), `$20` special, low
  nibble = record index.
- **Wall value 3 = secret door**: drawn as a wall, A walks through (verified floor 1 (2,18) west).
- **Special record** (4 bytes `type a b c`): `00` stairs to (x=a, y=b, floor c; floor 0 = castle) - floor 1 (0,10)
  `00 0C 07 02` leads to floor 2 (12,7), whose record leads back (verified by cross-reference); `02` teleport to
  (a,b,c); `08` elevator, floors a-b (verified: floor 4 (10,8) shows the A-D buttons). All 19 types decoded from the
  handlers (jump table `$D70E`): meanings in `tools/maps.py` MEANING and `design/maps.md` (04 message, 06
  message + castle, 0A search item, 0C search fight, 0E pit a d b, 10 spinner, 12 fixed fight, 14 barrier needs
  item b, 16 alarm, 18 anti-magic, 1A rock (party dies), 1C chute, 1E castle, 20 gift item, 22 Werdna sign,
  24 Werdna fight).
- **Floor init**: fixed fights / guardians (types 12, 24) are armed in a bitmap at `$0540` (4 bytes per row)
  only when a floor is entered by stairs, elevator, chute or teleport (`$DD10` loop). A poke-warp keeps the old
  floor's bitmap: warp to a stairs/elevator/chute first (checkpoints `f4`, `f10`).
- Renderer: `python3 games/wizardry-nes/tools/maps.py` -> `design/maps/floor_NN.png` + `atlas.png` (walls white,
  doors blue, hidden doors red, darkness grey, rooms brown, specials as type letter + record index); `--text`
  prints ASCII maps and the record list (`design/maps/floors.txt`). Done for all 10 floors (scout); the capture run
  checks them in play and writes `design/maps.md` with the record meanings.

## Shot plan (capture run 2026-11-18: 70 shots in `main`)
`shots.txt` holds 17 routed shots (verified frames for all routes by `emu.py`, not yet through `shoot.py`) and
commented plans:
- [x] boot NEXOFT logo, title, options (Select Switch), copyright page
- [x] castle menu, Edge of Town, name keyboard, tavern roster, character sheet (Inspect)
- [x] maze start, full view (Start), maze menu (Select), camp, elevator, battle options
- [x] race / stats / class screens of character creation
- [x] Boltac's shop (buy, armor page, sell), inn (rooms, level up), temple (list, cure)
- [x] battle: spell casting (cleric, mage, Tiltowait), damage, victory (EXP/gold), chest/trap/loot; pit, chute
- [x] Murphy's ghost (floor 1 (13,5) statue, not (9,13)), floor 4 fixed fight, Werdna fight, amulet, ending, credits
- [x] game over (party wiped), party member killed, Leave Game save page
- [ ] still open: Identify with an unidentified item, spinner/teleport effect shots, DUMAPIC, camp spell casting,
  LINE wall mode (options), alarm square, a random encounter victory with the level 1 party

## Strategy and walkthrough notes
- Level 1 characters die fast: poke levels/HP in the roster records (realistic values, see RAM map) and give
  gold for Boltac's before deep floors. Levels are gained by resting at the inn (source: series rule).
- Warp anywhere: `poke:003D=FLOOR,poke:003B=X,poke:003C=Y,poke:003E=DIR,left,w30,right,w30` (the turn redraws the
  view; verified for floor 1 and floor 4). Stepping onto a special square triggers it (elevator verified).
- Encounters are frame-timing dependent: vary the `wN` before the last step to get a different group.
- After `sav:01_party` the party is not formed: `CASTLE,ADDPARTY` (the roster order is the same).

## Naming
Party of six, created by `PARTYMAKE` (macros `MAKE1`..`MAKE6`, generated by `games/wizardry-nes/tools/party.py`;
run them in order in one session because of the persistent shift state):
| Name | Race | Alignment | Class | STR IQ PIE VIT AGI LUC | HP at L1 |
|---|---|---|---|---|---|
| RYZ | Human | Good | Fighter | 17 8 5 13 10 9 | 13 |
| CONDI | Dwarf | Good | Fighter | 16 7 10 15 7 6 | 9 |
| EBO | Gnome | Good | Cleric (Priest) | 9 7 16 10 11 7 | 9 |
| CUBI | Hobbit | Neutral | Thief | 7 7 7 9 16 15 | 5 |
| DEDDO | Elf | Good | Mage | 7 17 10 8 11 6 | 3 |
| MNZ | Elf | Good | Wizard (Bishop) | 7 15 14 7 10 6 | 8 |
Stats are cheated: on the stats screen the macro pokes each stat one below its target plus 6 bonus points
(`$0254-$0259`, `$025B`) and presses Right on every row (the screen redraws a row only when it changes; A is
refused while bonus points are left) (verified).

## Shortcuts
| What | How (tokens / prefix / code) | Source | Status |
|---|---|---|---|
| Warp (floor, x, y, facing) | `poke:003D=F,poke:003B=X,poke:003C=Y,poke:003E=D,left,w30,right,w30` | scout | verified |
| Character stats at creation | `$0254-$0259` + bonus `$025B` on the stats screen (see Naming) | scout | verified |
| Infinite bonus points at creation | Action Replay `025B:63` | Almar's Guides (search summary) | address verified (bonus) |
| Roster edits (gold, level, HP) | poke the record in battery RAM, see RAM map | scout | verified (Inspect) |
| Game Genie: free Boltac items, max EXP/gold after battles ("Perfect code" `YYYTUY`), stats 99 | Almar's Guides pages (codes not readable: host outside the network) | search summaries | untested |
| Veteran party | `sav:01_party,CASTLE,VETERANS,ADDPARTY` = checkpoint `veterans` (VETERANS pokes level, HP, E.P., gold, age, stats, spell points, spells known; record offsets in the RAM map) | capture | verified |
| One-hit fights | in battle `poke:7BE4=01,...` (monster HP low bytes, slots 6/15/24/33 + n) | capture | verified |
| Fixed fights after a warp | arrive by stairs/elevator/chute first (floor init), e.g. `@f4`, `@f10` | capture | verified |
| Pre-made characters | FIGHTER1 ... MAGE2 in the roster on a fresh battery | scout | verified |

### Saves (rom/saves/wizardry-nes/, never committed)
| Name | Contents (progress, party, items) | URL | SHA-1 | Status |
|---|---|---|---|---|
| 01_party (made here) | copy of `games/wizardry-nes/saves/01_party.sav`: roster with the playtest party, level 1 | - | see `saves/README.md` | verified (`sav:01_party,CASTLE` -> Tavern Add lists them) |
No downloadable saves looked for (GameFAQs not reachable from earlier scouts).

## RAM map (for `game.json` "ram" watches and pokes)
| Address | Size | Meaning | How found |
|---|---|---|---|
| `$003B` | 1 | x, 0-19 east | RAM watch + poke (verified) |
| `$003C` | 1 | y, 0-19 north | watch over steps (verified) |
| `$003D` | 1 | floor (0 in town, 1-10) | watch + poke warp (verified) |
| `$003E` | 1 | facing 0 N, 1 E, 2 S, 3 W (Left subtracts 1) | dump diff over turns (verified) |
| `$0045` | 1 | party window hidden flag (Start) | code |
| `$0264` | 1 | wall byte of the current square (`$0264-$0272` view cells) | code |
| `$0273-$0276` | 4 | special record of the square in front / under the party | code |
| `$0014` | 1 | joypad newly pressed | code |
| `$0254-$0259`, `$025B` | 1 each | character being created: STR IQ PIE VIT AGI LUC, bonus points | dump + poke (verified) |
| `$6000 + slot*$100` | 256 | roster record, 20 slots (`$6000-$73FF`); slots 0-5 pre-made, 6-11 RYZ..MNZ | dump (verified) |
| record `+$13-$18` | 6 | **gold**, packed BCD big-endian (12 digits) | poke + Inspect (verified) |
| record `+$19-$1E` | 6 | **E.P.**, packed BCD big-endian | poke + Inspect, Inn level-up (verified) |
| record `+$1F/$20`, `+$21/$22` | 2+2 | **HP now / max, big-endian** (hi, lo) | poke (verified: 1805 shown for 07 0D) |
| record `+$23/$24` | 2 | level, big-endian | poke + Inspect (verified) |
| record `+$25` | 1 | status: 0 OK, 3 paralyzed ("P-lyze"), 5 dead, 6 ashed | Temple list (verified) |
| record `+$26`, `+$28` | 1 each | age in years, AC | Inspect (verified) |
| record `+$29-$2F` / `+$37-$3D` | 7 / 7 | mage spell points now / max (L1-L7) | Inspect (verified) |
| record `+$30-$36` / `+$3E-$44` | 7 / 7 | cleric spell points now / max | Inspect, battle "L5(3)" (verified) |
| record `+$45-$4B` | 7 | spells known, 50 bits: mage 0-20 (Halito..Tiltowait), cleric 21-49 (Kalki..Kadorto), bit 0 = `+$45` bit 0 | Read Spell (verified) |
| record `+$54-$5B`, `+$5C` | 8, 1 | item ids (01 long sword, 08 large shield), item count | Boltac buy (verified) |
| record `+$62` bit 0 | | amulet holder flag (Werdna checks) | code `$D9DA` |
| `$7BB4 + i` (42 per table) | | combatants: 0-5 party, 6/15/24/33 + n monster groups; `$7BB4` status, `$7BDE` HP lo, `$7C08` HP hi | peek (verified; HP 1 = one-hit kills) |
| `$0540` | 80 | fixed-fight bitmap of the floor (set on floor entry) | code `$DD10`/`$DD6E` |
| `$0282`, `$02A8` | 1 each | anti-magic flag (spells fizzle), alarm flag | code |
| record `+$01`, `+$02` | | name length, name (8 bytes, space padded) | dump |
| record `+$0A-$0C` | 3 | race, class, alignment ids (tentative) | dump |
| record `+$0D-$12` | 6 | STR IQ PIE VIT AGI LUC | dump (matches the creation values) |
| ~~record `+$15-$18` gold~~ | | gold is `+$13-$18` (above) | |
| ~~record `+$20` / `+$22` HP little-endian~~ | | big-endian at `+$1F/$20`, `+$21/$22` (only low bytes were poked before) | |
| ~~record `+$24` level (2)~~ | | level `+$23/$24` big-endian | |
| `$7400-$74FF` | | party/game state in battery RAM (not decoded) | dump |
| `$7500-$7BFF` | | screen text buffers (battery RAM used as work RAM) | dump |
Roster pokes survive Leave Game and a power cycle (no checksum rejected `02_veterans`).

## Emulation notes
- NTSC, default press. Deterministic; encounters depend on exact frame timing (play.py and emu.py routes with
  the same tokens can meet different monsters because of the recorded `settle` steps; use the recorded route).
- The copyright page and the options screen are drawn with a horizontal offset on some frames (seen at `w60`
  and `w120`): pick the wait by eye for those shots.
- Pokes to stats/gold do not redraw the screen until the game redraws that part (stats screen: change the row).
- The status window sometimes leaves a strip of the previous screen at the bottom of Inspect (one line "MNZ
  G-Wiz 10"): pick another wait or accept.
- `play.py --name wiz` leaves old numbered PNGs in `work/play/wiz/` from earlier sessions: read the path `do`
  prints, never guess a number (the capture run read stale scout frames for ~10 calls).
- `play.py` uses `--name wiz` in this scout; helper `work/scout/wizardry-nes/steps.py` (groups -> tiled sheet) and
  `ramdiff.py` (dump/diff 0000-07FF + 6000-7FFF).

## Checkpoints
| Name | What |
|---|---|
| `title` | title menu, Start Game |
| `castle` | Castle menu, playtest party formed, level 1, no equipment |
| `start` | floor 1 (0,0) facing north, first control in the maze |
| `battle` | floor 1 (0,3): 5 Small humanoids, RYZ's options |
| `veterans` | Castle menu, `sav:01_party` + macro `VETERANS` (levels 10-13, spells, gold) + party formed |
| `vstart` | floor 1 (0,0) with the veterans |
| `f4elev` / `f4` | floor 4 elevator after button D (menu still open) / after B: floor 4 initialised |
| `f4fight` | floor 4 (12,13) guardian fight, RYZ's options |
| `murphy` | floor 1 (13,5): fight with the Unseen entity after searching the statue |
| `f10` | floor 10 (0,0) after the floor 9 chute and the plaque |
| `werdna_door` | floor 10 (17,4) after Werdna's sign |
| `amulet` | floor 10 (17,3) after Werdna's fight (DEDDO holds the amulet) |
| `ending` | ending text (floor 1 stairs up with the amulet) |
The first four rebuilt from an empty cache and compared with a cache hit: identical frames (2026-11-18).

## Sources
| Source | URL | Used for | Accessed |
|---|---|---|---|
| Wikipedia | https://en.wikipedia.org/wiki/Wizardry:_Proving_Grounds_of_the_Mad_Overlord | NES developer, publisher, release dates | 2026-11-18 |
| Almar's Guides (search-result summaries only) | https://almarsguides.com/retro/walkthroughs/nes/games/WizardryProvingGroundsoftheMadOverlord/ActionReplay/ | `025B:63` bonus points; Game Genie code list exists (shop, stats, perfect code) | 2026-11-18 (host outside the network) |
| TCRF (search summary) | https://tcrf.net/Wizardry:_Proving_Grounds_of_the_Mad_Overlord_(NES) | Japanese version had language switches and Turbo File support removed in the US release | 2026-11-18 (page 403) |
| ROM code | `tools/dis6502.py wizardry-nes` | maze format, controls, specials | 2026-11-18 |

## Open questions
- ~~Special types 04-24~~ decoded (design/maps.md); not all seen in play (teleport, alarm, anti-magic, rock).
- ~~Wall value 3~~ secret door (verified).
- Item numbers -> names (items 61/62/63 on floor 1; the amulet); item flags (equipped/cursed/unidentified) not
  found, so Identify was not shot.
- Poking monster status 5 does not end a fight (group counts live elsewhere); poke HP to 1 instead.
- The party list in `$7400`.
- Game Genie codes from Almar's Guides (needs the host or a mirror).
