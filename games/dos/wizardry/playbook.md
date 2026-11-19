# Wizardry: Proving Grounds of the Mad Overlord (DOS) - playbook

Everything an agent needs to play this game efficiently: read it before playing, add to it after every run.
Status of each fact: **verified** (seen in the emulator, with the route) or **source** (manual/FAQ/wiki, not yet
checked). Never delete a fact that turned out wrong: strike it and say what is true.
"disk data" = decoded from the game disk image with `tools/maps.py` / `tools/roster.py`, cross-checked in play.
Same scenario as the NES port (`games/nes/wizardry/`): floor layouts and the quest match, controls and screens
do not.

## Identity
| Field | Value |
|---|---|
| Title (EN / original) | Wizardry: Proving Grounds of the Mad Overlord (title screen "Welcome to the world of Wizardry!", verified) |
| Platform / model used | IBM PC, the 1984 PC booter run from disk images by a 1998 DOS loader; `game.json` model `ega-315` (8088 speed, see Emulation notes) |
| Release (region, year) | Apple II 1981, IBM PC booter April 1984 (Wikipedia, MobyGames); this dump: the 1998 re-release (Ultimate Wizardry Archives style: `wizar1/WIZ1.COM` dated 1998-09-01, `WIZ1.DSK` 1998-07-09, `SAVE1.DSK` 1998-09-09, an empty `.ba1` marker) |
| Developer / publisher | Sir-Tech Software (Andrew Greenberg, Robert Woodhead) (Wikipedia) |
| Genre | First-person party RPG: six adventurers, a castle of menus, a ten-floor wireframe maze of 20 x 20 squares |
| Players / save system | 1 player; roster of 20 characters on the scenario disk image `SAVE1.DSK`, written by the game while playing; the save ZIP only receives it when the program ends (L)eave game), see Saves (verified) |
| Dump | `rom/wizardry.zip`, SHA-1 in `game.json`; one program `wizar1/WIZ1.COM` (starts without the DOSBox Pure menu) |

### The loader WIZ1.COM (read with ndisasm, verified in play)
- Checks for 300 KB free memory, opens `WIZ1.DSK` **read-only** and `SAVE1.DSK` **read/write** in its own folder
  (missing files: "The file WIZ1.DSK is missing or damaged." / "The file SAVE1.DSK cannot be created."; it never
  creates SAVE1.DSK), hooks INT 18h as the game's disk call and INT 16h (keyboard), loads the boot sector of
  WIZ1.DSK to 7C00 and jumps to it.
- Disk call (INT 18h): drive 0 = WIZ1.DSK, drive 1 = SAVE1.DSK; offset = ((cylinder*2+head)*8 + sector-1)*512
  (8 sectors, 2 heads, 512 bytes: 320 KB geometry; SAVE1.DSK is 640 KB, its second half is unused junk).
  Format calls succeed without doing anything; a read of drive 0 track 79 sector 1 switches every later drive-0
  access to SAVE1.DSK (copy-protection/scenario-disk check).
- Keyboard (INT 16h): it compares 8x8 glyphs on the CGA screen with three patterns and types for the player:
  the scenario-disk prompt ("Place duplicate scenario diskette in drive 1, then press Enter" -> Enter), a
  drive question ("2", Enter, Enter) and the game's exit screen (-> back to DOS, "Thanks for playing
  Wizardry!"). **Alt+X or Alt+Q quits to DOS at any time** (code; do not press Alt with X/Q in routes).
- The video mode before the game is restored on exit.
- `SAVE1.DSK` as shipped is a ready scenario disk: a copy of WIZ1.DSK whose six pre-made characters are renamed
  (Tarkin, Shreev, Curtis, Kimbal, Tivis, Mewo instead of Thesus, Tempest, Lysander, Treon, Flamus, Nobal).
  **M)ake scenario disk is not needed**: S)tart game goes straight to the Castle (verified). Not tried: M.

## Boot sequence
Macros (all in `game.json`): `TITLE`, `CASTLE`, `TRAINING`, `MAKE:name:race:align:stats:class`, `PARTYMAKE`,
`ADDPARTY`, `PARTY`, `RESUME`, `MAZE`, `WARP:floor:x:y`, `VET`, `AMULET`, `HOME`. Every macro was run as one
`do` from power-on or inside a checkpoint route replayed cold (see Checkpoints).
- **verified** Power-on: black until about frame 260, then the title (logo, "Welcome to the world of
  Wizardry!", a monster picture that changes every few seconds, "You cannot play without making a scenario
  disk! S)tart game M)ake scenario disk"). `TITLE` = `w400`.
- **verified** `S`: a screen wipe, the loader answers "Place duplicate scenario diskette in drive 1, then press
  Enter" by itself (visible about s+240..270 frames), "Now loading the program into memory ..." (about s+330),
  then the Castle (complete about s+650). `CASTLE` = `TITLE,s,w800`.
- **verified** `PARTY` = `CASTLE,TRAINING,PARTYMAKE,enter,w120,c,w120,g,w120,a,w120,ADDPARTY,enter,w120`: creates
  the six characters in the Training Grounds and adds them in the Tavern; ends on the Castle menu with the
  party (checkpoint `start`, about 3 s of emulation per run).
- **verified** `RESUME` = `CASTLE,g,w120,a,w120,ADDPARTY,enter,w120`: with `sav:01_start` or `sav:02_ending`
  (the roster has them in slots G-L), forms the party (checkpoints `resume`, `resume_end`).
- **verified** `MAZE` (from the Castle menu) = `e,w120,m,w600,enter,w200,n,w120`: Edge of Town, Maze, "One
  moment", Camp, leave camp, "Stairs up, take them (Y/N)?" N -> floor 1 (0,0) facing north.

## Controls
Every screen prints its keys; one keystroke per choice, Enter (drawn as a bent arrow) leaves or confirms.
| Context | Key | Action | Status |
|---|---|---|---|
| Title | `s` / `m` | start game / make scenario disk | s verified; m asks "The disk you inserted has data on it ... Use it (Y/N)?" (verified, N not pressed; `menu_make_scenario`) |
| Castle | `g` `a` `t` `b` `e` | Tavern, Inn, Temple, Boltac's, Edge of Town | all verified |
| Tavern | `a` + letter, `r`, `#` (digit), `d`, Enter | add (roster letter; list closes when six are in), remove, inspect, divvy gold, leave | all verified (divvy shows no message) |
| Inn | digit, then `a`-`e`, `p`, Enter | who stays; stables (free, no healing), cot 10, economy 50, merchant 200, royal suite 500 gp/week; pool gold | verified: resting heals week by week, level-up at the end of the stay |
| Temple | letter, digit (payer), Enter | "Who shall we help?" lists characters not OK (letters A...), "The donation will be N. Who will tithe?" | verified: paralysis 100, dead 250, ashes 500 gold per level |
| Boltac's | digit, then `b` `s` `u` `i` `p`, Enter; in the stock `p` `b` `f` `s` | buy, sell, uncurse, identify, pool gold; purchase, backward, forward (one item), start | all verified: P + digit buys ("Unusable item - buy it (Y/N)?" for the wrong class); S/I/U + digit act at once, no confirmation |
| Edge of Town | `t` `m` `c` `u` `l` | Training, Maze, Castle, Utilities, Leave game (writes the disk, ends the program) | all verified |
| Utilities | `c` `m` `r`, Enter | change name (roster list), move characters ("Insert the source scenario disk into drive 1, then press Enter"), restart an "out" party ("No characters are in the maze") | screens verified; M not carried on |
| Training | `c` `i` `r`, Enter | create, inspect (letter: I)nspect, D)elete, C)hange class, A)lter password), roster | all verified |
| Creation | text + Enter; Enter; `a`-`e`; `a`-`c`; Enter/`up`/`down`/`esc`; class letter; `y`/`n` | name (stored in capitals; "Name already in use - press Enter"), password (empty is fine, no confirmation), race, alignment, bonus points (Enter moves the pointer, Up/Down change, Esc finishes and is refused while bonus is left), class `a`-`h` (only eligible ones listed), keep | all verified |
| Maze | `w` / `a` / `d` | step forward / turn left / turn right ("You can't walk through walls!") | verified |
| | `k` | kick: go through the door in front | verified (Werdna's door) |
| | `c` | camp: `1`-`6` inspect, `r` reorder, `e` equip (every member, slot by slot: digit or Enter), Enter leave | all verified |
| | `o` | hide the command line and party window (full view); `o` again brings the command line back | verified |
| | `s` | status: party window off, view full height; again: back | verified |
| | `i` | search the square for bodies ("Found: * no one *") | verified |
| Character sheet | `r` `t` `p` `s` `e` `d` `i` `u`, Enter | read spell book (M/P), trade (whom, gold, items), pool gold, spell (camp; "Cast on whom (#)?"), equip, drop, identify (bishop), use (camp) | all verified except equip from the sheet |
| Prompts | `y` / `n`, Enter | stairs, keep, signs | verified |
| Battle | `f` (Enter = default) `p` `s` `d` `u` `r` `t` | fight, parry, spell (type the name + Enter), dispell (priest), use item, run, take back; members 4-6 have no Fight; first round of a surprise: no Spell | verified |
| | `1`-`4` | "Fight which group (#)?" when there are several groups; group spells ask too | verified |
| | Enter | "Press Enter to fight, or T)ake back orders" | verified |
| Chest | `o` `c` `l` `i` `d` | open, Calfo, leave alone, inspect, disarm; each asks "Who (#) will ...?"; disarm then wants the trap's name typed | o, i, d, l verified; c not (no level 2 priest in the level 1 party) |
| Cemetery | Enter | leave the cemetery | screen verified |
| Anywhere | Alt+X, Alt+Q | loader: quit to DOS | code |

Input timing: default press (hold 8, wait 40) works everywhere. At 315 cycles the game redraws slowly; waits
that worked: menu `w120`, character-creation steps `w90`-`w120`, step or turn `w60`, entering the maze `w600`,
level change `w600` ("One moment"), battle order `w90`, a battle round with messages `w1200`-`w2400`. Prompts
throw away keys typed before them (inferred), so keep the waits.

## Game structure
- **Castle** (verified menus): Gilgamesh's Tavern (party), Adventurer's Inn (rest, level up: source), Temple of
  Cant (cures), Boltac's Trading Post (shop), Edge of Town (Training Grounds, Maze, Castle, Utilities, Leave
  game).
- **Roster** (disk data): 20 slots; the stock scenario disk has six pre-made level 1 characters (A-F: Tarkin
  N-Fig human, Shreev N-Mag dwarf, Curtis N-Fig human, Kimbal N-Mag gnome, Tivis N-Thi hobbit, Mewo G-Pri
  gnome) and six "lost" developer names (free slots). New characters take the free slots: the party is G-L.
- **Maze** (disk data, `design/maps/floors.txt`, rebuilt with `python3 games/dos/wizardry/tools/maps.py`):
  ten floors of 20 x 20, x east, y north, (0,0) south-west. Floor 1: entrance (0,0) under the stairs up,
  stairs down (0,10) -> floor 2 (12,7), elevator (10,8) floors 1-4, dark band x=9-10, signs (9,12) "Area out of
  bounds" (verified), (9,19), (13,3), (13,5) (Murphy's ghost statue), (13,18), teleport squares (5,9)/(13,4).
  Floor 4: elevator (10,0) floors 4-9, the fixed fight squares (11-12,12-14), the desk room message (11,11)
  (verified). Floor 9: chute (8,2) -> floor 10 (0,0); almost every square teleports back to floor 1. Floor 10:
  a maze of rock with teleport squares; Werdna's sign (17,4) (verified) and his fight (17,3) behind a door
  south of the sign (verified).
- **Ending** (verified): reaching the Castle with Werdna's amulet (item 94) in a pack: "* * Congratulations
  * * You have recovered the amulet and passed the Overlord's test! ... 50,000 G.P. and E.P. ... Wear the
  chevron of rank (>) with honor. Press Enter to receive your reward!!!", then the Castle; the amulet is gone,
  every member shows ">" after the name (checkpoints `ending`, `after_ending`).
- **Game over** (verified): "You are in rock!" (warp into rock), then tombstones "Your entire party has been
  slaughtered. Press Enter to leave the cemetery!".

## Shot plan
Set `main` captured 2026-11-19 (game-capture): 199 shots from power-on to the ending, verified and published
(`shots.txt`, `shots/main/`). The routes were chosen in batches with `tools/try.py` (many candidate routes in
parallel, the last K frames tiled) and written straight into the work shot list; scratch plan files were
`work/cap/wizardry/plan/0N_*.txt`. How each area was reached:
- Castle, Training, Utilities at level 1: `@start`, `@edge`, `@training`; creation shots with the throwaway
  name ZED (elf, bonus poked to 9 at `C36E` on the bonus screen, then real key presses).
- Veterans in the Castle with gear: `@gcastle` (VET + GEARPOKE + EQUIPALL in the first camp, back up the
  stairs). Boltac's, temple (status poked: `DDE4` = CONDI's status 5 dead / 6 ashes), sheet commands.
- Special squares: WARP to the neighbour square, poke the facing, `a,w60,d,w60` (redraw), `w` (or `k` for a
  door), `w400,w600`. Which side is open: the survey helper `work/cap/wizardry/survey.py` (scratch) wrote one
  route per open side from `tools/maps.py`; the routes are in `shots.txt`.
- Random fights: WARP to a fight-zone square, poke the position to a neighbouring fight-zone square,
  `wK,a,w60,d,w300,w900` (a turn on a room square rolls the encounter; K picks the monsters). Floors 1, 3, 8, 9
  answered; floors 2, 4-7, 10 gave nothing on the squares tried (use the walking variant or the fixed fights).
- Battle frames: rounds are long; take a timeline (`try.py --frames 50` over `w40` tokens) and pick the frame
  (`enter,w40*N,!`).
- Werdna: `@gwerdna` and the real fight below (Strategy); ending `@gending`, `@gafter`, `@final`.
Not captured (reasons in the report and design/): Murphy's ghost (floor 1 statues give no search, findings),
R)un succeeding, poison, criticals, Calfo, rescue of bodies, a spinner (no visible effect), Leave game (no
in-game screen: the loader prints "Thanks for playing Wizardry!" in DOS text mode).

## Strategy and walkthrough notes
- Cataloguing: never grind. `VET` (at the Castle, then any menu change to redraw) makes the party level 13
  with realistic HP, E.P., gold, ages and spells; `WARP` from floor 1 reaches any square; `AMULET`+`HOME` ends
  the game.
- **Werdna, the route that wins on screen** (no pokes in the fight): from `@gwerdna` (equipped veterans,
  Werdna shown as **W*E*R*D*N*A** with 1 + 2 unseen entities): round 1 (surprise, no spells) all parry
  (`p,w90` x6, `enter`), `w40*6,w4`, round 2 `f,w90,1,w90,f,w90,1,w90,s,w90,type:litokan\n,w90,2,w90,p,w90,
  s,w90,type:tiltowait\n,w90,s,w90,type:lahalito\n,w90,3,w90,enter` (Deddo's Tiltowait kills Werdna; RYZ is
  drained 2 levels and paralyzed), `w40*55`, round 3 `f,w90,1,w90,s,w90,type:litokan\n,w90,2,w90,f,w90,1,w90,
  s,w90,type:tiltowait\n,w90,s,w90,type:lahalito\n,w90,2,w90,enter` (the guards die), `w40*64` -> checkpoint
  `werdna_won` (CONDI carries the amulet). With `w1` instead of `w4` Werdna casts Tiltowait first and kills
  four members (the `boss_four_dead` shots). Werdna's hit points in that fight: `D314` (71), RAM below.
  Out: the castle-exit poke for (18,3) (Shortcuts), `a,w60,w,w300,y,w600,w600` -> `gending`.
- (older notes) Werdna's fight is not safe even for the veterans: in one timing Tiltowait (Deddo) killed Werdna in round 2
  and the vampires paralyzed Condi and drained Ryz 13 -> 9; in another timing Werdna's own round killed four
  members. Unarmed fighters barely hurt vampires: buy weapons and armour at Boltac's first (`@vet` has
  5,000-25,000 gold each), and try `wN` variations before the first order. Round 1 is usually the surprise
  round (no spells): parry or fight, cast Tiltowait from round 2.
- Monster hit points: found (RAM map, battle records). Poking Werdna's to 1 let a 3-damage hit kill him
  (tested); the published fight needs no poke.
- Group spells and fights ask for a group when there are several; a letter that is not an option is ignored,
  but `t` takes orders back: never type a spell name while the spell prompt is not open (`s` is refused in a
  surprise round and the name's letters then act as commands).
- Level drain: vampires take levels; a drained or dead member stays in the roster; the temple cures for gold.
- Fixed fights on floors 3, 4 and 7 (disk data) start whenever the square is entered.

## Naming
Party made by `PARTYMAKE` (macros `MAKE:name:race:alignment:stats:class`): stats are poked on the bonus screen
(`C552` = six words STR IQ PIE VIT AGI LUC, `C546` = the lower limits, `C36E` = bonus), each one below the
target, bonus 6, then `up,enter` on every row (the screen redraws a row only when it changes) and Esc.
| Name | Race | Align | Class | STR IQ PIE VIT AGI LUC | HP at L1 | Roster slot |
|---|---|---|---|---|---|---|
| RYZ | Human | Good | Fighter | 17 8 5 13 10 9 | 8 | G (6) |
| CONDI | Dwarf | Good | Fighter | 16 7 10 15 7 6 | 8 | H (7) |
| EBO | Gnome | Good | Priest | 9 7 16 10 11 7 | 8 | I (8) |
| CUBI | Hobbit | Neutral | Thief | 7 7 7 9 16 15 | 8 | J (9) |
| DEDDO | Elf | Good | Mage | 7 17 10 8 11 6 | 8 | K (10) |
| MNZ | Elf | Good | Bishop | 7 15 14 7 10 6 | 8 | L (11) |
Names are typed in lower case and shown in capitals. Every new character got 8 HP (also the stock ones):
see `design/findings.md`.

## Shortcuts
| What | How (tokens / prefix / code) | Source | Status |
|---|---|---|---|
| Party creation with chosen statistics | `MAKE` / `PARTYMAKE` (pokes on the bonus screen) | scout | verified |
| Veteran party | `VET` at the Castle with the party formed, then `e,w120,c,w120` to redraw (checkpoint `vet`): level 13, HP 112/124/71/66/49/58, E.P. 377,512-560,341, gold 5,077-24,817, ages 24-63, mage spells all (Deddo), priest spells all (Ebo), bishop mage L1-4 + priest L1-3 | scout | verified (sheet, battle) |
| Warp anywhere (from floor 1) | `WARP:FF:XX:YY` (hex): pokes floor 1's stairs-down record (square (0,10), live floor at `0B646`) to lead to floor FF square (XX,YY), puts the party on (1,10) facing west and takes the stairs; the new floor loads properly ("One moment"); arriving on a stairs or sign square shows its prompt | scout | verified (floors 2, 4, 10) |
| Exit to the castle from any square | poke a square next to the party into stairs to the castle: square index nibble (offset 560 + x*10 + 2*(y div 4), nibble y mod 4) = an unused index i, type nibble (760 + i div 2) = 1, AUX0/1/2 (768/800/832 + 2i) = 0; example in the old `amulet`->`ending` route: `poke:B92B=D0,poke:B944=16,poke:B960=0000,poke:B980=0000,poke:B9A0=0000` for floor 10 (18,3) | scout | verified once (floor 10) |
| Veterans with gear | `GEARPOKE` at the Castle (items unequipped in the six packs), then in the first camp `EQUIPALL` (`e` and 18 times `1,w150`): AC -4 -1 3 4 9 7 (checkpoints `gcamp`, `gcastle`, `gmaze`) | capture | verified |
| Item numbers | pack entry = 4 words (equipped, cursed, identified, item); items 1-100 named in `design/items.md` (read by poking 8 items at a time into RYZ's pack at `DD28` and opening the sheet) | capture | verified |
| Werdna's amulet | `AMULET` (pokes item 94 into Ryz's pack: party slot 1 must have no items), then reach the Castle (`HOME` from floor 1 (0,0) facing north) | scout | verified (ending) |
| Ready characters | the six pre-made characters (Tavern A-F) | stock disk | verified |
| Position report in game | DUMAPIC (mage spell, camp) | game | verified |
No downloadable saves: the 1998 package itself ships a ready SAVE1.DSK. GameFAQs/TCRF/StrategyWiki not tried
(known 403 for scouts), wizardry.wiki.gg outside the network.

### Saves (games/dos/wizardry/saves/, committed; nothing in rom/saves/)
| Name | Contents | Made by | Status |
|---|---|---|---|
| 01_start | the stock roster + ryz condi ebo cubi deddo mnz, level 1, ~100-199 gold, no equipment; party not formed | `@start,e,w120,l,w600` (Leave game) + `play.py export` | verified (`sav:01_start,RESUME`) |
| 03_werdna_beaten | the six after the real Werdna fight and the ending, gear, chevrons, RYZ/CONDI level 11; the transfer source for Wizardry II | `@final,e,w120,l,w600` + export | verified (roster.py) |
| 02_ending | same six after `VET` + the ending: level 13, Chevron of Rank, +50,000 gold and E.P.; Ryz keeps an empty pack entry (count 1, item 0) | `@after_ending,e,w120,l,w600` + export | verified (`sav:02_ending,RESUME`) |
Each `.sav` is DOSBox Pure's save ZIP with `WIZAR1/SAVE1.DSK` (640 KB, stored uncompressed). For the owner:
copy `SAVE1.DSK` over the one in the game folder. For Wizardry II / III: their `run.bat` copies
`..\wizar1\save1.dsk` into their folder; the roster is at disk offset `1D800` (below), `games/dos/wizardry/tools/roster.py
FILE` lists it from a `.sav`, a DSK or the game ZIP.

## RAM map (for `game.json` "ram" watches and pokes)
Physical addresses (DOS segment*16+offset), the same on every boot with this ZIP and model.
| Address | Size | Meaning | How found |
|---|---|---|---|
| `0DA20` | 2 | facing: 0 N, 1 E, 2 S, 3 W (D adds 1) | RAM diff over turns (verified) |
| `0DA22` | 2 | floor: 0 castle, 1-10 | warp (verified) |
| `0DA24` | 2 | y, 0-19 north | diff over a step + poke (verified) |
| `0DA26` | 2 | x, 0-19 east | poke + DUMAPIC (verified) |
| `0DCEC + n*0xD0` | 208 | party member n (0-5, party order) as a full character record (layout below); the game writes these to the roster | name search (verified) |
| `0B646` | 894 | the floor in play (TMAZE layout, `tools/maps.py`); a cache copy at `0E3C4` | match with the disk (verified) |
| `0B94A`, `0B96A`, `0B98A` | 2 each | floor 1 special 2 (stairs down at (0,10)): AUX0 floor, AUX1 y, AUX2 x (used by `WARP`) | poke + stairs (verified) |
| `0C552` | 12 | character creation: STR IQ PIE VIT AGI LUC (words) | find (verified) |
| `0C546` | 12 | creation: the rolled values (lower limits for Down) | dump (verified by the macro) |
| `0C36E` | 2 | creation: bonus points left | find (verified) |
| `01980` | | the loader WIZ1.COM (PSP segment 0188h, CS=0198h); its handles at `01B4A` (WIZ1.DSK) and `01B4C` (SAVE1.DSK) | ndisasm + PC (verified) |
| `0D308` / `0D30A` | 2 / 2 | in battle, group 1: alive count / count; monster records of 16 bytes from `0D30C`, hit points at +8 (Werdna `0D314`, 71 in `@gwerdna`; slimes 3 3 2 2) | dump diff + poke (verified: Werdna poked to 1 died to a 3-damage hit) |
| `0D3FE`, `0D4F4` | 2 | the same for groups 2 and 3 (groups 0xF6 bytes apart; records from `0D402`, `0D4F8`); when a group dies the later groups move up | dump (verified in `@werdna`) |
Character record (208 bytes; on disk and in memory; words little-endian; Pascal TCHAR of the Apple original):
| Offset | Size | Field | Status |
|---|---|---|---|
| `+00` / `+10` | 16 / 16 | name / password: length byte + 15 characters | verified |
| `+20` | 2 | "out" (in the maze when the game was left) | disk data |
| `+22` / `+24` | 2 / 2 | race 1 human 2 elf 3 dwarf 4 gnome 5 hobbit / class 0 fig 1 mag 2 pri 3 thi 4 bis 5 sam 6 lor 7 nin | verified |
| `+26` | 2 | age in weeks (sheet shows years) | verified |
| `+28` | 2 | status 0 OK 1 afraid 2 asleep 3 paralyzed 4 stoned 5 dead 6 ashes 7 lost (free slot) | verified (3, 7) |
| `+2A` | 2 | alignment 1 good 2 neutral 3 evil | verified |
| `+2C` | 4 | statistics, 5 bits each: STR IQ PIE in the first word, VIT AGI LUC in the second | verified |
| `+34` | 6 | gold: three words 0-9999, low first (gold = w0 + 10000*w1 + 10^8*w2) | verified |
| `+3A` / `+3C` | 2 / 64 | items carried / 8 x (equipped, cursed, identified, item number) words | verified (amulet = item 94) |
| `+7C` | 6 | E.P., same three-word form | verified |
| `+82` / `+84` | 2 / 2 | highest level / level | verified |
| `+86` / `+88` | 2 / 2 | HP now / max | verified |
| `+8A` | 8 | spells known, bit k = spell k: mage 1-21 (Halito ... Tiltowait), priest 22-50 (Kalki ... Kadorto) | verified (Halito, Katino, Dios, Badios; casting) |
| `+92` / `+A0` | 14 / 14 | mage / priest spell points per level 1-7 (recomputed by the game in the maze) | verified |
| `+B0` | 2 | armour class | verified (10) |
| `+CE` | 2 | awards: 1 = Chevron of Rank (>) after the ending | verified |
Roster on disk: SAVE1.DSK offset `1D800`, slot n at `1D800 + (n div 4)*0x400 + (n mod 4)*0xD0` (four records per
1024-byte page). Floors: WIZ1.DSK/SAVE1.DSK offset `1EC00 + (floor-1)*0x400`.

## Emulation notes
- **Model `ega-315`.** 315 cycles = 4.77 MHz 8088, the machine the booter was written for: messages stay
  readable (combat lines about 160 frames each), the title parade and screen wipes run at their speed; at the
  default 7800 cycles the disk prompts and messages flash past. The game sets CGA mode 5 (the colour-burst-off
  graphics mode). On a real CGA with an RGB monitor that gives red/cyan/white (machine `cga`: red logo); EGA,
  VGA and SVGA show the mode-4 palette cyan/magenta/white (magenta logo). **`cga` (and `tandy`) are not
  usable:** after a savestate load the palette falls back and every screen turns cyan (tested: frames differ
  between a run and its reloaded state; `ega`, `vga`, `svga` reload exactly). The loader does not care about
  the machine type. If the backend restores the CGA palette one day, `cga-315` is the authentic look (routes
  would need a check).
- **Disk writes (backend):** the loader keeps SAVE1.DSK open for the whole session. The game writes to it while
  playing (counted: one write at the Castle, two per created character, one per Tavern add), but DOSBox Pure
  puts a file into its save ZIP only when the file is closed, so states and `play.py export` see the written
  disk only after L)eave game (the program ends, the loader closes the files). States made earlier carry no
  disk; on a cold load the game still has its roster in memory and writes all of it again on Leave game: cache
  hits and cold rebuilds give the same frames, party memory and written disk (checked for every checkpoint,
  2026-11-19). Do not depend on reading back something the game wrote before a state was made.
- After L)eave game the program has ended: no savestates there (export works); DOSBox Pure shows "Press any key
  to return to start menu".
- Pokes to the party records show on the Castle list only after a menu change (`e,w120,c,w120`).
- A warp lands with the "One moment" box while the floor loads: `WARP` ends with `w600`.
- RNG: random fights and their outcome follow frame timing exactly; editing any earlier wait changes them
  (the first Werdna route broke when `WARP`'s wait changed).

## Checkpoints
| Name | What |
|---|---|
| `title` | title screen |
| `start` | Castle, party of six formed, level 1 |
| `edge`, `training` | Edge of Town; Training Grounds menu |
| `camp` | camp on entering the maze |
| `maze1` | floor 1 (0,0) facing north, first control |
| `battle` | floor 1 (7,1): 4 Slimes, surprised, Ryz's options |
| `chest` | after the Slime fight: the chest menu |
| `vet` | Castle with the veteran party (`VET`) |
| `vmaze` | floor 1 (0,0) with the veterans |
| `werdna_sign` | floor 10 (17,4): Werdna's sign (warped) |
| `werdna` | floor 10 (17,3): Werdna, Vampire Lord, 4 Vampires; Ryz's options |
| `ending` | the Congratulations screen (veterans + `AMULET` + `HOME`) |
| `after_ending` | Castle after the reward (chevrons) |
| `resume`, `resume_end` | Castle, party formed from `sav:01_start` / `sav:02_ending` |
| `gcamp`, `gcastle`, `gmaze` | the veterans with gear (GEARPOKE + EQUIPALL): first camp, Castle, floor 1 entrance (capture 2026-11-19) |
| `gwerdna_sign`, `gwerdna` | floor 10 (17,4) sign and the Werdna fight with the equipped veterans |
| `werdna_won` | after the real Werdna fight (route in Strategy); CONDI has the amulet, RYZ paralyzed |
| `gending`, `gafter` | Congratulations; the Castle after it (RYZ out of the party, paralyzed) |
| `final` | the Castle with all six after the temple cured RYZ (source of save `03_werdna_beaten`) |
All rebuilt from an empty cache and compared with cache hits in fresh processes on 2026-11-19: identical
frames, party records, position and (after Leave game from `start`, `edge`, `vet`, `after_ending`) identical
written disks. Helpers: `work/scout/wizardry/cmp.py` and `build.py` (scratch, not committed).

## Sources
| Source | URL | Used for | Accessed |
|---|---|---|---|
| Wikipedia | https://en.wikipedia.org/wiki/Wizardry:_Proving_Grounds_of_the_Mad_Overlord | release years (Apple 1981, PC booter 1984), races, classes, goal | 2026-11-19 |
| MobyGames (search summary) | https://www.mobygames.com/game/1367 | Ultimate Wizardry Archives: booter games supplied as disk images with a loader that redirects floppy reads | 2026-11-19 |
| Wizardry Archives (search summary) | https://wizardryarchives.com/downloadsw1.html | `.dsk` files are the scenario disks holding the characters; `wiz2.com wiz2.dsk wiz1.dsk` transfer form | 2026-11-19 (host not fetched) |
| PCGamingWiki (search summary) | - | save location `SAVE1.DSK` | 2026-11-19 |
| archive.org item | https://archive.org/details/msdos_Wizardry_1_Proving_Grounds_Of_The_Mad_Overlord_1981_Sir_Tech | exists, no instructions | 2026-11-19 |
| wizardry.wiki.gg | - | outside the session network (not fetched) | 2026-11-19 |
| the loader and disks | `rom/wizardry.zip` | loader behaviour (ndisasm), roster and floor formats | 2026-11-19 |
| NES playbook | `games/nes/wizardry/playbook.md` | same scenario: special squares, Murphy's ghost, item ideas | 2026-11-19 |
The manual (Sir-Tech "Playing Wizardry on your IBM PC & PCjr") was not found on an allowed host.

## Open questions
- ~~Monster hit points in battle~~ found (RAM map). ~~Item names~~ read on screen (`design/items.md`);
  monster names are still encoded on the disk (only those seen in fights are known).
- ~~What `i` does in the maze~~ searches for bodies. M)ake scenario disk: only its Y/N prompt seen.
- Levels at the inn: fighter level 2 at 1000 E.P. (verified); the rest of the table not read.
- ~~Temple prices~~ 100/250/500 gold per level for paralysis/death/ashes (verified).
- The floor 1 statues (13,3), (13,5), (13,18) never ask to search (design/findings.md): the bronze and
  silver keys and Murphy's ghost were not reached. Ideas: the search may need a key item in the party, or a
  different entry (stepping onto the square after a turn on it); decode the message-square handler.
- Utilities M)ove characters: only its first prompt seen (it wants a source disk).
- The second half of SAVE1.DSK (tracks 40-79) holds unrelated junk (Windows code fragments); harmless.
