# Wizardry II: The Knight of Diamonds (DOS) - playbook

Everything an agent needs to play this game efficiently: read it before playing, add to it after every run.
Status of each fact: **verified** (seen in the emulator, with the route) or **source** (manual/FAQ/wiki, not yet
checked). Never delete a fact that turned out wrong: strike it and say what is true.
"disk data" = decoded from the disk images with `tools/maps.py` / `tools/roster.py`, cross-checked in play.
Engine and screens are Wizardry I's (`games/dos/wizardry/`, read its playbook too): the same menus, keys, record
layout and floor format; addresses differ (RAM map). For tools write `dos/wizardry-2` (the NES port is
`games/nes/wizardry-2/`), and give `play.py` a session name (`--name dos-wizardry-2`).

## Identity
| Field | Value |
|---|---|
| Title (EN / original) | Wizardry II: The Knight of Diamonds (title screen "Scenario #2 - The Knight of Diamonds", verified) |
| Platform / model used | IBM PC, the PC booter run from disk images by a 1998 DOS loader; `game.json` model `ega-315` (8088 speed, as Wizardry I) |
| Release (region, year) | Apple II 1982 (Wikipedia); this dump: the 1998 re-release with a loader (`wizar2/WIZ2.COM` dated 1998-09-01, `WIZ2.DSK` 1998-07-09, `SAVE2.DSK` 1998-09-29, an empty `.ba1` marker) plus a `run.bat` menu dated 2019 (not needed, below) |
| Developer / publisher | Sir-Tech Software (Andrew Greenberg, Robert Woodhead) (Wikipedia) |
| Genre | First-person party RPG, the second scenario of Wizardry: veterans from Wizardry I enter six wireframe floors of 20 x 20 under the Temple of Gnilda |
| Players / save system | 1 player; roster of 20 characters on the scenario disk image `SAVE2.DSK`, written while playing; since the backend fix of 2026-11-19 every write reaches states at once (see Emulation notes) (verified) |
| Dump | `rom/wizardry-2.zip`, SHA-1 in `game.json`; programs `wizar2/run.bat` (start menu entry 1) and `wizar2/WIZ2.COM` (entry 2) |

### The loader WIZ2.COM (read with ndisasm, verified in play)
- Same loader as WIZ1.COM with other file names: checks for 300 KB free, opens `WIZ2.DSK` read-only and
  `SAVE2.DSK` read/write in its folder ("The file WIZ2.DSK is missing or damaged." / "The file SAVE2.DSK cannot
  be created."), hooks INT 18h (disk) and INT 16h (keyboard), boots WIZ2.DSK. Drive 0 = WIZ2.DSK, drive 1 =
  SAVE2.DSK, 320 KB geometry; a read of drive 0 track 79 sector 1 switches drive 0 to SAVE2.DSK.
- Keyboard hook: compares 8x8 glyphs on the CGA screen with patterns and types for the player: the scenario-disk
  prompt (Enter), a drive question ("2", Enter, Enter), the exit screen (back to DOS, "Thanks for playing
  Wizardry!"), and, new in this loader, **the M)ove characters prompts**: on the "source disk" prompt it opens
  `Save1.Dsk` in its folder (read/write, a third handle; while it is open every disk access of the game goes
  to that file) and presses Enter; on the "target disk" prompts it closes it and presses Enter. So **the
  import needs only `WIZAR2\SAVE1.DSK` = a Wizardry I scenario disk**; the player never sees a disk prompt
  (verified: `start`). Missing Save1.Dsk: the open fails and the loader still presses Enter (code; not tried).
- Alt+X / Alt+Q quit to DOS at any time (code, as in Wizardry I).
- **`run.bat` is not needed**: its "1" runs `wiz2`, its "2" copies `..\wizar1\save1.dsk` to `..\wizar2\save1.dsk`
  (a folder this ZIP does not have) and tells the player to use E)dge of town, U)tilities, M)ove characters.
  The boot route starts WIZ2.COM from the DOSBox Pure menu (`down`); the copy is done by `tools/transfer.py`.
- `SAVE2.DSK` as shipped is a ready scenario disk (S)tart game goes to the Castle) holding six pre-made
  veterans: CALEB (L12 dwarf fighter), BOREE (L13 gnome priest), ODDLER (L12 hobbit mage), NAUTUS (L13 dwarf
  fighter), ZIL (L12 elf priest), GUYDOMAN (L12 dwarf fighter), all good, no items, slots A B G H I J; slots
  C-F are LOST (TARKIN, SAC LAMB, PSEUDO FIGHTER, BISH), K-T empty (disk data, verified in the Tavern).

## Boot sequence
Macros (all in `game.json`): `TITLE`, `CASTLE`, `IMPORT`, `ADDPARTY`, `PARTY`, `RESUME`, `MAZE`,
`WARP:FF:XX:YY`, `SOLO`, `KOD`, `STAFF`, `HOME`, `HOMESTAIRS`, `KNIGHTS`, `REFORM`, `WIN` (scout) and
`GEAR`, `EQUIP`, `KODGEAR` (capture, Shortcuts). Every macro was
run as one `do` from power-on or inside a checkpoint route replayed cold (see Checkpoints).
- **verified** Power-on: DOSBox Pure's start menu (RUN.BAT highlighted, WIZ2.COM below). `TITLE` =
  `w120,down,enter,w300`: the logo, "Scenario #2 - The Knight of Diamonds", a monster picture that changes
  (the knight, then a parade of four), "You cannot play without making a scenario disk! S)tart game M)ake
  scenario disk" (complete about 120 frames after Enter).
- **verified** `CASTLE` = `TITLE,s,w800`: a screen wipe, "Place duplicate scenario diskette in drive 1, then
  press Enter" answered by the loader, "Now loading the program into memory", the Castle ("Llylgamyn") about
  s+700 frames.
- **verified** The import (Wizardry I characters): route prefix `sav:00_transfer` (save built by
  `tools/transfer.py`: `WIZAR2/SAVE1.DSK` = the Wizardry I disk of `games/dos/wizardry/saves/03_werdna_beaten.sav`).
  `IMPORT` (from the Castle) = `e,w120,u,w120,m,w200,g,w60,h,w60,i,w60,j,w60,k,w60,l,w60,enter,w700,enter,w120,c,w120`:
  Edge of Town, Utilities, M)ove characters lists the Wizardry I roster (A TARKIN ... G RYZ ... L MNZ),
  letters mark G-L with "+", Enter moves them one by one ("RYZ has been moved", about 100 frames each), back
  to Utilities, Enter, C)astle. They land in the free slots C D E F K L (RYZ CONDI EBO CUBI DEDDO MNZ).
- **verified** `ADDPARTY` = `g,w120,a,w120,c,w90,d,w90,e,w90,f,w90,k,w90,l,w120,enter,w120`; `PARTY` =
  `CASTLE,IMPORT,ADDPARTY` (with `sav:00_transfer`): Castle with the six (checkpoint `start`).
- **verified** `RESUME` = `CASTLE,ADDPARTY` with `sav:01_start` or `sav:02_ending` (same slots).
- **verified** `MAZE` (Castle) = `e,w120,m,w600,enter,w200,n,w120`: camp ("Descending into the ruins under the
  Temple of Gnilda" while it loads), leave camp, "Stairs up, take them (Y/N)?" N: floor 1 (0,0) facing north.
- **Characters cannot be created in Wizardry II**: the Training Grounds offer only I)nspect a character,
  R)oster of characters, Leave (verified, `training`). New parties come only from Wizardry I (M)ove) or the
  six pre-made veterans.

## Controls
Wizardry I's controls (that playbook's table) all apply; differences and checks here.
| Context | Key | Action | Status |
|---|---|---|---|
| Title | `s` / `m` | start game / make scenario disk ("The disk you inserted has data on it. If you use it, the data will be erased! Use it (Y/N)?") | s verified; m prompt verified, not answered |
| Castle | `g` `a` `t` `b` `e` | Tavern, Inn, Temple, Boltac's, Edge of Town | all opened (verified) |
| Tavern | `a` + letters, `r` + digit, digit, `d`, Enter | add (list closes at six), remove ("Remove who (#)?"), inspect, divvy, leave | a, r, digit verified |
| Edge of Town | `t` `m` `c` `u` `l` | Training, Maze, Castle, Utilities, Leave game | all verified |
| Utilities | `c` `m` `r`, Enter | change name, move characters (letters mark, Enter moves, Esc quits), restart an "out" party | m verified (the import) |
| Training | `i` `r`, Enter | inspect, roster (no create) | screen verified |
| Maze | `w` `a` `d`, `k`, `c`, `s`, `i`, `o` | as Wizardry I (command line "C)amp S)tatus I)nspect O)ff A-W-D K") | w a d k c verified |
| Sheet (camp) | `r` `t` `p` `s` `e` `d` `i` `u`, Enter | as Wizardry I; U)se item asks "Use item (#)?"; the staff of Gnilda answers "* Powerless *" | u verified |
| Battle | `f` `p` `s` `d` `u` `r` `t`, Enter | as Wizardry I; no S)pell in a surprise first round | f p verified |
| Riddle squares | text + Enter | "What is your answer ?" / "Your answer ? >" | verified |
| Ending | Enter, then `y`/`n` per roster character | "Press Enter to select your knights!", "Make CONDI a knight (Y/N)?" | verified |

Input timing: the default press (hold 8, wait 40) works everywhere; waits that work (315 cycles): menu
`w120`, Tavern add/remove `w90`-`w120`, step or turn `w60`, entering the maze `w600`, a warp `w600`, a
guardian fight drawn `w600` after the kick, message pages `w300`-`w400`, knight prompts `w150`.

## Game structure
- **Castle "Llylgamyn"** (verified menus): Gilgamesh's Tavern, Adventurer's Inn, Temple of Cant, Boltac's
  Trading Post, Edge of Town (Training Grounds, Maze, Castle, Utilities, Leave game). As Wizardry I.
- **Roster** (disk data): 20 slots on SAVE2.DSK at 0x1D200 (see RAM map); after the import RYZ CONDI EBO CUBI
  (C-F), DEDDO MNZ (K, L) between the six stock veterans.
- **What the import keeps** (verified, record diff and sheets): everything but the items: levels, HP, E.P.,
  gold, age, statistics, spells known and spell points (DEDDO mage 9/9/9/7/5/4/1, EBO priest 9/9/9/7/4/4/2),
  the Chevron of Rank ">"; the item count is set to 0 (packs empty) and the "in use" word to 1. The sheet
  keeps the old AC until the first camp, which shows AC 10 for all. In the Wizardry I disk the six become
  LOST (it is a move, not a copy).
- **Maze** (disk data, `design/maps/floors.txt`, `python3 games/dos/wizardry-2/tools/maps.py`): six floors of
  20 x 20, x east, y north. Each floor's way down is guarded by a fixed fight on the square before the stairs
  (verified, checkpoints `guard1`-`guard5`):
  | Floor | Arrive (from above) | Guardian square: group | Stairs down -> | Piece it carries |
  |---|---|---|---|---|
  | 1 | (0,0) from the castle | (15,2): 1 Magic Armor (77) | (16,2) -> floor 2 (11,10) | KOD's armor (verified: "MNZ found : ARMOR" / "RYZ found : ARMOR", item 129, unidentified) |
  | 2 | (11,10) | (2,6): 1 Magic Shield (75) | (1,6) -> floor 3 (0,0) | KOD's shield (verified: "RYZ found : SHIELD", item 127) |
  | 3 | (0,0) | (14,13): 1 Magic Sword (73) | (13,14) -> floor 4 (7,12) | Hrathnir (verified: "MNZ found : SWORD", item 125) |
  | 4 | (7,12) | (10,4): 1 Magic Helm (74) | (9,4) -> floor 5 (1,18) | KOD's helm (verified: "CONDI found : HELM", item 126) |
  | 5 | (1,18) | (10,9): 2 Magic Gauntlets (76) | (10,10) -> floor 6 (0,0) | KOD's gauntlets (verified: "CUBI found : GAUNTLETS", item 128) |
  | 6 | (0,0) | fixed fights (5,15)-(5,16), (18,18)-(19,19): group 47 | none | - |
  Floor 6 (1,2): the sphinx's riddle (answer **the knight of diamonds**; a wrong answer pushes the party back
  south), (1,3) "The apparition reappears and intones: 'One alone.'", (1,4) teleport to floor 1 (9,9), next to
  Gnilda's temple (9,10). Floor 2 (3,6), next to its guardian, is a second riddle square: "I am a lonely being, scarred by swords ... Tell me,
  what am I?", answer **shield** (verified: the right answer leaves the party on (3,6), a wrong one puts it back on (4,6)).
  Other message squares: floor 1 (11,2); floor 2 (16,3), (3,17), (15,19)/(18,14), (18,10), (18,9); floor 3
  (8,10), (4,10); floor 4 (16,7)-(17,9), (7,13), (6,17); floor 5 (11,8); floor 6 (1,3), (11,17), (13,15),
  (16,13) (the sphinx's three clues, inferred), (5,14). Pits, chutes, teleports, dark areas, rock: maps file.
- **The quest** (verified, checkpoints `gnilda_test` ... `knights`): Gnilda's temple, floor 1 (9,10): with a
  party that does not qualify she speaks ("Hear these, the words of Gnilda ... To obtain my staff, one must
  acquire the five. These are the tests, and shall be the proof, before me presented. This is the will of
  Gnilda." "The apparition slowly fades..."). **One character alone, wearing the five pieces** (Hrathnir, KOD's
  helm, shield, gauntlets, armor equipped) is asked "the answer to the riddle of the sphinx": **the knight of
  diamonds** -> "Behold! The Staff of Gnilda!", the five are taken back, "RYZ got an item" (staff, item 124).
  Carried pieces are not enough, and a party of six with RYZ wearing the five only hears the speech (both
  verified): the test needs one character alone.
- **Ending** (verified): reaching the Castle with the staff, **one character alone in the party**: "* *
  Congratulations * * You have retrieved the Staff of Gnilda, and the city is again safe from the evils of war.
  As a token of our gratitude, we bestow upon you the highest honor it is in our power to present, the 'Mark of
  Gnilda'. Of course, we realize that you were aided by other brave and noble warriors - to these we bestow the
  order of 'Knight of the City'. Press Enter to select your knights!", then "Make NAME a knight (Y/N)?" for every
  other roster character (stock ones too). The staff is taken; the bearer gets "G" and 300,000 E.P. (RYZ
  184,587 -> 484,587), the knights "K", no E.P. A party of six with the staff gets no ending: the staff is just
  taken at the Castle (verified, twice). A poked staff works like the gift (verified: `@start,SOLO,STAFF,HOMESTAIRS`).
- **Game over / cemetery**: as Wizardry I (not seen here).

## Shot plan
Set `main` captured 2026-11-19 (game-capture): 213 shots from power-on to the ending, verified and published
(`shots.txt`, `shots/main/`). Plan files were scratch (`work/cap/wizardry-2/plan/NN_*.txt`, assembled into the
work `shots.txt` in game order, previewed with `tools/try.py`, shot with `shoot.py --only`). How each area was
reached:
- Title, disk prompt, loading: `@title` + `w100`/`w20` frames (`!`).
- The import step by step: `sav:00_transfer,CASTLE,e,w120,u,w120,m,w200`, letters, `enter` + `w20` x N frames
  (removing, insert, moving, "RYZ has been moved").
- Castle with the imported party: `@start`; with gear: `@gcastle` (GEAR + EQUIP, Shortcuts). Boltac's pages
  `b,w200` + `f,w200` x N; identify after `p,w200` (pool gold) because it costs 150,000; temple with CONDI's
  status poked (`DE8A`=5, `DEE8`=0, then `e,w120,c,w120`).
- Message squares: `@gcastle,WARP` to the neighbour, poke the facing (`DAC6`), `a,w60,d,w60`, `w` (or `k`),
  `w400,w600`; one route per square from `work/cap/wizardry-2/survey.py` (scratch: approaches each square from
  an open side, checking both squares' walls: walls are stored per square and can be one-way). Pages with
  `enter,w400`.
- Traps: the same approach; the message frame with `w10` x 4 + `!`.
- Random fights: arriving or turning on a fight-zone square does not always meet a group. What worked:
  floor 2 `WARP:02:00:00,poke:DACA=0100,wK,a,w60,d,w300,w900` (every K tried gave a group), floor 1 arrival on
  (5,7) and (10,8), and on the other floors a real step into a room square from a neighbour:
  `WARP:FF:XX:YY,poke:DAC6=0F00,a,w60,d,w60,wK,w,w300,w900` with K varied (routes in `shots.txt`).
- Battle frames: `enter` then `w40` x N + `!`, N read off a timeline (`try.py --frames 70`).
- Guardians with the equipped party: checkpoints `gguard1`-`gguard5` and the round checkpoints `gguard3r2`,
  `gguard4r2`, `gguard4r3`, `gguard5r2`, `gguard5r3`. Shield, Sword and Helm were beaten for real (Tiltowait);
  the Magic Armor (305 hit points, regenerates, resists spells) and the gauntlets got `poke:D3BA=0800` (and
  `D3CA` for the second gauntlet) during the orders, then real blows killed them.
- Quest end: `@gcastle,WARP:06:01:01,k,w300` (sphinx pages), `@gcastle,WARP:01:09:0A` (Gnilda with six),
  `gtest` -> `ggift` -> `gstaff` -> `gending` -> `gknights` -> `greform` -> `gfinal` -> `final` (one chain; RYZ
  re-equipped at Boltac's and rested at the inn after the ending).
- Death: CONDI's status poked in the maze shows after a camp; all six poked dead + camp + leave -> cemetery.
Not captured: floor 2 (16,3) (no way in), the floor 6 fixed fight group 47, spinners (no visible effect), the
stones, M)ake scenario disk after Y, Utilities C)hange name past its list, "RYZ got an item" after the gift
(not on screen in the frames tried), a dispell result (EBO was slept before acting). Floor views of 4 and 6
were dropped: pixel-identical to floor 1's entrance.

## Strategy and walkthrough notes
- Cataloguing: never grind. The imported party is strong (levels 11-13) but has no items: `GEAR` gives
  (by poke, gold reduced by Boltac's prices) a realistic Boltac's outfit, `EQUIP` wears it in the first camp:
  AC -1 0 3 5 9 5 (checkpoints `gcamp`, `gcastle`, `gmaze`).
- Guardians with that gear (all verified): the Magic Shield dies to Tiltowait in round 1 (it killed EBO
  first); the Magic Sword in round 2 (it decapitated CONDI first); the Magic Helm in round 3 (Lahalito on the
  party); the Magic Armor and the two Magic Gauntlets resist spells: poke their hit points low (`D3BA`,
  `D3CA`). Round 1 is a surprise round in every guardian fight (no S)pell): fight with 1-3, parry with 4-6.
- Critical path (verified in play, shortcuts for the pieces): floors 1-5 guardians -> five pieces (identify:
  MNZ, may fail; Boltac's 150,000) -> one bearer wears all five -> floor 6 (1,2) sphinx: "the knight of
  diamonds" -> (1,3) "One alone." -> (1,4) teleport to floor 1 (9,9) -> remove the others in the Tavern
  (`SOLO`) -> (9,10) answer again -> the staff (Gnilda takes the whole pack) -> floor 1 (0,0) stairs (`HOME`)
  -> Congratulations -> knights.
- Hand the bearer's own gear to a friend before going alone (Gnilda takes everything); in the capture RYZ
  bought new gear at Boltac's afterwards (`gfinal`).
- The pieces regenerate HP ("87+" next to RYZ's hits while he wears them) and give AC -18 ("LO" in the list).

## Naming
No naming: characters come from Wizardry I (RYZ CONDI EBO CUBI DEDDO MNZ, named there) or the stock six.
Utilities C)hange name exists (not used).

## Shortcuts
| What | How (tokens / prefix / code) | Source | Status |
|---|---|---|---|
| Import the Wizardry I party | `sav:00_transfer,PARTY` (checkpoint `start`); `tools/transfer.py [SRC] [OUT]` rebuilds the save from any Wizardry I save | scout | verified |
| Warp anywhere | `WARP:FF:XX:YY` (hex) from the Castle: enters the maze and, at floor 1's "Stairs up" prompt, pokes that staircase (floor 1 special 5, AUX0/1/2 at 0B9D6/0B9F6/0BA16) to lead to floor FF square (XX,YY), then Y | scout | verified (floors 1-6) |
| Win a fight | `WIN` = `poke:D3AE=0000` (group 1's alive count) while giving orders, then Enter: counts as killed (Magic Armor in round 1: "Each survivor gets 5555 E.P.", "RYZ found : ARMOR", "Each survivor gets 0 G.P."; `@guard1,f,w90,f,w90,f,w90,p,w90,p,w90,p,w90,WIN,enter,w100*7`); the finder varies with timing (MNZ in a round-4 win) | scout | verified (piece dropped both times) |
| Lone bearer | `SOLO` (Castle, party formed): Tavern, remove 6, 5, 4, 3, 2 | scout | verified |
| The five pieces | `KOD`: RYZ's pack = Hrathnir, helm, shield, gauntlets, armor, all equipped (pack must be empty) | scout | verified (passes Gnilda's test) |
| The staff | `STAFF`: RYZ's pack = staff of Gnilda (item 124); with `SOLO` and `HOMESTAIRS` the ending | scout | verified |
| Home | `HOME`: from any floor-1 square: poke (0,1) facing south, step onto the stairs, Y | scout | verified |
| Knights | `KNIGHTS`: Enter, then N N Y Y Y N N N N Y Y for CALEB BOREE CONDI EBO CUBI ODDLER NAUTUS ZIL GUYDOMAN DEDDO MNZ (roster order after the import; only in a segment from `@start`) | scout | verified |
| Re-form after the ending | `REFORM`: Tavern add C D E J K (RYZ is still in) | scout | verified |
| Item names | 8 items at a time into RYZ's pack, sheet in the Tavern (`design/items.md`) | scout | verified |
| Gear | `GEAR` (Castle, party formed): Boltac's items in the six packs, unequipped, gold reduced by their prices (RYZ long sword, plate mail, shield+1, helm, gloves of copper; CONDI the same without gloves; EBO anointed mace, chain mail+1, large shield, potion of Dios; CUBI short sword, leather+1, small shield, scroll of Katino; DEDDO staff+2, robes, scroll of Halito; MNZ staff, leather+1, small shield, potion of Latumofis); `EQUIP` in the first camp (`e` + 20 x `1,w150`) | capture | verified |
| The five worn instead of gear | `KODGEAR`: RYZ's pack = the five pieces equipped + long sword, plate mail, shield+1 (8 items) | capture | verified (Gnilda's test) |
| Monster hit points | `poke:D3BA=0800` (group 1, first monster; second at `D3CA`, records 16 bytes) during the orders, then `settle,enter`: the next real hit kills | capture | verified |
| Dead member / party wipe | status +28 (`DDBA`, `DE8A`, `DF5A`, `E02A`, `E0FA`, `E1CA` = 5) and HP +86 = 0, then camp `c,w300`: DEAD in the list; all six + leave camp = cemetery | capture | verified |
No downloadable saves or codes looked for beyond the sources below (the package itself ships ready disks).

### Saves (games/dos/wizardry-2/saves/, committed; nothing in rom/saves/)
| Name | Contents | Made by | Status |
|---|---|---|---|
| 00_transfer | only `WIZAR2/SAVE1.DSK` = Wizardry I `03_werdna_beaten`'s disk (the six after Werdna, in the Castle) | `tools/transfer.py` | verified (`start`) |
| 01_start | both disks after the import + Leave game: SAVE2 roster with the stock six + RYZ CONDI EBO CUBI DEDDO MNZ (L11-13, chevron, no items); SAVE1 with the six LOST | `@start,e,w120,l,w600` + export | verified (`resume`) |
| 02_ending | after the ending: RYZ ">G" 484,587 E.P., the five ">K", AC 10, no items | `@knights,e,w120,l,w600` + export | verified (`resume_end`, roster.py) |
| 03_wizardry3_transfer | the capture's final party after the ending: RYZ L12 ">G" with Boltac's gear, the five ">K" with gear, in the Castle; **the Wizardry III transfer source** | `@final,e,w120,l,w600` + export | verified (roster.py) |
Each `.sav` is DOSBox Pure's save ZIP with `WIZAR2/SAVE2.DSK` and `WIZAR2/SAVE1.DSK` (640 KB each, stored).
For the owner: copy both over the files in the game folder. List them: `python3 games/dos/wizardry-2/tools/roster.py FILE`.
**For Wizardry III** (owner's queue): this game's roster is in `SAVE2.DSK` at disk offset `1D200`, slot n at
`1D200 + (n div 4)*0x400 + (n mod 4)*0xD0` (20 slots of the same 208-byte record as Wizardry I); the six are in
slots 2-5, 10, 11. `02_ending.sav` holds both `SAVE1.DSK` (Wizardry I, the six LOST there) and `SAVE2.DSK`
(the six with ">G"/">K"); a Wizardry III transfer script can take `SAVE2.DSK` from it the way `transfer.py`
takes `SAVE1.DSK`.

## RAM map (for `game.json` "ram" watches and pokes)
Physical addresses; most are Wizardry I's + 0xA6 (same engine, the program sits 0xA6 bytes higher).
| Address | Size | Meaning | How found |
|---|---|---|---|
| `0DAC6` | 2 | facing: 0 N, 1 E, 2 S, 3 W | RAM diff over two turns (verified) |
| `0DAC8` | 2 | floor: 0 castle, 1-6 (65535 seen in the Castle after the ending) | warp (verified) |
| `0DACA` | 2 | y, 0-19 north | step + peek (verified) |
| `0DACC` | 2 | x, 0-19 east | warp (verified) |
| `0DD92 + n*0xD0` | 208 | party member n (0-5) as a full character record (layout: Wizardry I playbook); RYZ's pack count `0DDCC`, entries `0DDCE` (4 words: equipped, cursed, identified, item); HP `0DE18`; awards `0DE60` | name search, pokes (verified) |
| `0B6CC` | 894 | the floor in play (TMAZE, `tools/maps.py`); floor 1 special 5 (stairs to the castle) AUX0/AUX1/AUX2 at `0B9D6`/`0B9F6`/`0BA16` (used by `WARP`) | match with WIZ2.DSK 0x1E600 (verified) |
| `0D3AE` / `0D3B0` | 2 / 2 | in battle, group 1: alive count / count; `0D3B2` its monster number (77 Magic Armor) | peek in `guard1` (verified); poke alive 0 = won (verified) |
| `0D3BA` | 2 | group 1, first monster's hit points; monster records 16 bytes apart (`0D3CA` the second); guardians: Armor 305 (regenerates about 5 a round), Shield 79, Sword 72, Helm 156, Gauntlets 50 each | RAM diff over a 9-damage hit (verified: 310 -> 301; poke 8 + one hit = killed) |
| `0DD92 + n*0xD0 + 0x28` / `+0x86` / `+0x34` | 2 / 2 / 6 | member n status / HP / gold (RYZ `0DDBA`, `0DE18`, `0DDC6`); the party order changes when members die (the dead move back) | pokes (verified) |
| `01980` | | the loader WIZ2.COM (CS 0198h): handles at `01B4A` (WIZ2.DSK), `01B4C` (SAVE2.DSK), `01B50` (Save1.Dsk while moving), flag `01B6F` | ndisasm + PC (code) |
Character record: as Wizardry I (`games/dos/wizardry/playbook.md`), plus: `+20` = 1 while the character is in
the party or just moved (0 in the roster after Leave game); `+CC` = HP regeneration from worn items (1 with the
staff); `+CE` awards: bit 0 ">" Chevron of Rank, bit 11 "K" Knight of the City, bit 14 "G" Mark of Gnilda
(verified: `roster.py` on 02_ending). Roster on disk: SAVE2.DSK `1D200` (above). Floors: WIZ2.DSK/SAVE2.DSK
`1E600 + (floor-1)*0x400`.

## Emulation notes
- **Model `ega-315`**, as Wizardry I (same CGA mode-5 booter; `cga` loses the palette on a state load, see
  dos.md). Frames compared across state loads: identical (Checkpoints).
- **~~Stale disk after a state load~~ fixed 2026-11-19 (backend commit 5310311)**: writes through the open
  SAVE2.DSK reach states at once; `@ending,KNIGHTS,REFORM` from a cached checkpoint gives the same frame as one
  segment from `@start` (coordinator), and the capture's `gknights` -> `greform` -> `final` chain and the
  export of `03_wizardry3_transfer` ran from cached checkpoints. The old rule below is history. Old text: the loader keeps SAVE2.DSK open; the game
  writes roster changes into it (Tavern add/remove, knighting), but DOSBox Pure puts SAVE2.DSK into the save
  ZIP only when a file is closed (the import's Save1.Dsk closes, Leave game). A state therefore carries the disk
  as of the import; the game in memory is right, the disk can be behind. **Wizardry II reads the roster back
  from the disk** (Tavern list, the knight prompts): after `SOLO`, a cache hit of `gnilda_test` listed only
  CALEB BOREE CONDI ODDLER NAUTUS ZIL GUYDOMAN (EBO CUBI DEDDO MNZ missing; cold runs list all) and `@ending,KNIGHTS`
  knighted the wrong characters. `start`, `resume`, `resume_end` and everything that does not read the roster
  after a Tavern change are safe (checked). Rule: a route that changes the party in the Tavern and later reads
  the roster runs in one segment from `@start` (or a `sav:` save), not from a later checkpoint. A backend fix
  (flush writes through open handles) would remove the rule.
- After Leave game the program has ended ("Thanks for playing Wizardry!" in text mode): no states there, export works.
- Pokes to the party records show on the Castle list only after a menu change; the AC of imported characters
  is the Wizardry I value until the first camp recomputes it (10 without items).
- RNG: random fights and their outcome follow frame timing exactly (as Wizardry I); arriving on a fight-zone
  square by warp always met a group.

## Checkpoints
| Name | What |
|---|---|
| `title` | title screen |
| `start` | Castle, the imported six formed (from `sav:00_transfer`) |
| `resume`, `resume_end` | Castle, party formed from `sav:01_start` / `sav:02_ending` |
| `edge`, `training`, `camp`, `maze1` | Edge of Town; Training Grounds (no create); first camp; floor 1 (0,0) |
| `battle` | floor 1 (14,2): 5 Kobold Kings, RYZ's options |
| `guard1` ... `guard5` | the five guardians: Magic Armor, Magic Shield, Magic Sword, Magic Helm, 2 Magic Gauntlets |
| `sphinx` | floor 6 (1,2): the sphinx's riddle, first page |
| `gnilda_test` | floor 1 (9,10): RYZ alone with the five: the answer prompt |
| `staff_gift` | "Behold! The Staff of Gnilda!" |
| `ending` | Congratulations |
| `knights` | Castle after the knighting, party re-formed, AC 10 (built in one segment from `@start`) |
| `gcamp`, `gcastle`, `gmaze` | capture: the party with Boltac's gear (GEAR + EQUIP): first camp, Castle, floor 1 entrance |
| `chest` | capture: floor 2 (0,0), the chest after 3 Rhino beetles |
| `gguard1` ... `gguard5`, `gguard3r2`, `gguard4r2`, `gguard4r3`, `gguard5r2`, `gguard5r3` | capture: the guardian fights with gear, at the options of rounds 1-3 |
| `gtest`, `ggift`, `gstaff`, `gending`, `gknights`, `greform`, `gfinal`, `final` | capture: the ending chain with the equipped party (RYZ alone with KODGEAR, the gift, the staff, Congratulations, knights, re-formed, RYZ re-equipped, after a night at the inn) |
Every checkpoint was rebuilt from an empty cache and compared with cache hits in fresh processes on
2026-11-19 (`work/scout/wizardry-2/cmp.py`, scratch): identical frames, party records, position and written
disks, also after Leave game from `start`, `knights`, `resume_end`. Exception, by design: `@ending,KNIGHTS`
(stale disk, above).

## Sources
| Source | URL | Used for | Accessed |
|---|---|---|---|
| Wikipedia | https://en.wikipedia.org/wiki/Wizardry_II:_The_Knight_of_Diamonds | year, developer, six levels, import requirement, staff for the armour (says "six" pieces; the game says five: "one must acquire the five") | 2026-11-19 |
| Data Crystal (NES port notes) | https://datacrystal.tcrf.net/wiki/Wizardry:_Knight_of_Diamonds_(NES)/Notes | the NES port's piece names and item/monster list (port differs: pieces on other squares) | 2026-11-19 |
| Search summaries (not fetched: hosts outside the network) | the-spoiler.com, tk421.net (Wizardry II walkthrough), hardcoregaming101.net | riddle answer "the knight of diamonds" (confirmed in play), 250,000 xp for the bearer (the game gives 300,000 here) | 2026-11-19 |
| the loader and disks | `rom/wizardry-2.zip` | loader (ndisasm), roster, floors, items (on screen) | 2026-11-19 |
| Wizardry I DOS work | `games/dos/wizardry/` | engine, controls, record layout, tools | 2026-11-19 |
GameFAQs, TCRF, StrategyWiki: known 403 for agents (not tried); wizardry.wiki.gg, the-spoiler.com, tk421.net:
not resolvable from the session.

## Open questions
- ~~The floor 2 riddle at (3,6)~~ answer **shield** (verified). Floor 2 (16,3) (kind 9): no way in found.
- ~~Do guardians 2-5 drop their pieces?~~ yes, all five verified (items 125-129). Floor 6 group 47 not fought.
- ~~Monster hit points~~ `0D3BA` (verified). ~~Boltac's stock~~ Wizardry I's (design/items.md).
- The "one alone" rule: party of one (verified both ways at the temple and the Castle); nothing else tried.
- The duplicate item names (114/122, 115/123, 120/121): still unknown.
- M)ake scenario disk after Y, Utilities C)hange name past the list: not tried. What the sage's 100,000 buy
  and other wishes at the well.
