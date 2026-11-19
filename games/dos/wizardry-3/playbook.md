# Wizardry III: Legacy of Llylgamyn (DOS) - playbook

Everything an agent needs to play this game efficiently: read it before playing, add to it after every run.
Status of each fact: **verified** (seen in the emulator, with the route) or **source** (manual/FAQ/wiki, not yet
checked). Never delete a fact that turned out wrong: strike it and say what is true.
"disk data" = decoded from the disk images with `tools/maps.py` / `tools/roster.py`, cross-checked in play.
Engine, screens and record layout are Wizardry I's and II's (`games/dos/wizardry/`, `games/dos/wizardry-2/`:
read those playbooks too); addresses differ (RAM map). For tools write `dos/wizardry-3`, and give `play.py` a
session name (`--name dos-wizardry-3`).

## Identity
| Field | Value |
|---|---|
| Title (EN / original) | Wizardry III: Legacy of Llylgamyn (title screen "Scenario #3 - The Legacy of Llylgamyn", verified) |
| Platform / model used | IBM PC, the PC booter (WIZ3.DSK boot sector "Wizardry for the IBM-PC", "(C) 1987 RWI, Inc.") run from disk images by a 1998 DOS loader; `game.json` model `ega-315` (8088 speed, as Wizardry I and II) |
| Release (region, year) | Apple II 1983 (Wikipedia); this dump: the 1998 re-release (`wizar3/WIZ3.COM` 1998-09-01, `WIZ3.DSK` 1998-07-09, `SAVE3.DSK` 1998-09-09) plus a `run.bat` menu dated 2019 (not needed, below) and an empty `.ba1` marker named after Wizardry I (ignored) |
| Developer / publisher | Sir-Tech Software (Wikipedia) |
| Genre | First-person party RPG, the third scenario of Wizardry: descendants of the Wizardry I/II heroes climb six wireframe floors of a volcano; floors 2/4 refuse a party with evil members and no good one, 3/5 any party with a good member |
| Players / save system | 1 player; roster of 20 characters on the scenario disk image `SAVE3.DSK`, written while playing (verified); no character creation |
| Dump | `rom/wizardry-3.zip`, SHA-1 in `game.json`; programs `wizar3/run.bat` (start menu entry 1) and `wizar3/WIZ3.COM` (entry 2) |

### The loader WIZ3.COM (read with ndisasm, verified in play)
- WIZ2.COM with other file names (307 differing bytes, all strings, stack and glyph data): opens `WIZ3.DSK` read-only and
  `SAVE3.DSK` read/write, hooks INT 18h (disk) and INT 16h (keyboard), boots WIZ3.DSK; types the scenario-disk
  and drive prompts for the player; Alt+X / Alt+Q quit to DOS (code, as in Wizardry I and II).
- **The M)ove characters source prompt opens `Save2.Dsk`** in its folder (the only source name in WIZ3.COM; WIZ2.COM
  has `Save1.Dsk` at the same place), presses Enter, and closes it on the target prompt. So **the import needs only
  `WIZAR3\SAVE2.DSK` = a Wizardry II scenario disk**; `SAVE1.DSK` is never read (code; the Wizardry II path verified:
  `start`). A Wizardry I disk would have to be copied in as `SAVE2.DSK` and moved with "1) Proving Grounds" (not tried).
- **`run.bat` is not needed**: its "1" runs `wiz3`; its "2" copies `..\wizar1\save1.dsk` and `..\wizar2\save2.dsk`
  into `wizar3\` and prints the steps (E)dge, U)tilities, M)ove characters, then T)raining, I)nspect, L)egate). The
  boot route starts WIZ3.COM from the DOSBox Pure menu (`down`); the copy is done by `tools/transfer.py`.
- `SAVE3.DSK` as shipped is a ready scenario disk holding six level-1 legacy characters: KLINDT (N-FIG dwarf), LEIF
  (G-PRI gnome), ZETT (N-MAG hobbit), VERPA (N-FIG dwarf), SENA (G-PRI elf), GITTER (N-FIG dwarf), slots A-F; slots
  12-19 hold LOST developer test characters (BIT, Z80, 6502, 68000, 8080, CP/M, EPROM, HDA: free slots) (disk data).

## Boot sequence
Macros (all in `game.json`): `TITLE`, `CASTLE`, `IMPORT`, `LEGATE:letter:alignment`, `LEGATEALL`, `ADDPARTY`,
`PARTY`, `RESUME`, `HALF2`, `MAZE`, `WARP:FF:XX:YY`, `WARP5:FF:XX:YY`, `VET`, `VET2`, `WIN`, `PARRY`, and (capture,
2026-11-19) `GEAR`, `EQUIP`, `GEAR2`, `EQUIP2` (Shortcuts). Every scout macro ran inside a checkpoint route rebuilt
from power-on with an empty cache (see Checkpoints).
- **verified** Power-on: DOSBox Pure's start menu (RUN.BAT highlighted, WIZ3.COM below). `TITLE` =
  `w120,down,enter,w300`: logo, "Scenario #3 - The Legacy of Llylgamyn", a monster picture, "You cannot play without
  making a scenario disk! S)tart game M)ake scenario disk" (checkpoint `title`).
- **verified** `CASTLE` = `TITLE,s,w800`: the loader answers the disk prompt, the Castle "Llylgamyn".
- **verified** The import: route prefix `sav:00_transfer` (save built by `tools/transfer.py`: `WIZAR3/SAVE2.DSK` =
  the Wizardry II disk of `games/dos/wizardry-2/saves/03_wizardry3_transfer.sav`). `IMPORT` (Castle) =
  `e,w120,u,w120,m,w200,2,w300,c,w60,d,w60,e,w60,f,w60,k,w60,l,w60,enter,w700,enter,w120`: Edge of Town, Utilities,
  M)ove characters asks "1)Proving Grounds 2)Knight of Diamonds", `2` lists the Wizardry II roster (A CALEB ...
  C RYZ D CONDI E EBO F CUBI ... K DEDDO L MNZ), letters mark with "+", Enter moves them (back at Utilities within
  700 frames), Enter leaves Utilities **to the Castle** (not to the Edge of Town). They land in slots G-L of the
  Wizardry III roster; on SAVE2.DSK they become LOST (a move, not a copy) (verified: `roster.py` on `01_start`).
- **verified** The legacy: `LEGATE:letter:alignment` (Training Grounds menu) = `i,w120,{letter},w200,l,w200,enter,w200,
  {alignment},w200,enter,w200`: I)nspect, the roster letter, L)egate, "The rite of passage ceremony now begins... The
  temple priests link up this ancestral spirit with it's descendant... Press Enter", "Choose an alignment for
  descendant: A) Good B) Neutral C) Evil / Select alignment >" (only the alignments the class allows are listed:
  CUBI the thief gets B and C only), then the character's own menu (L)egate I)nspect D)elete C)hange class A)lter
  password Leave); Enter returns to the Training menu. `LEGATEALL` = `e,w120,t,w120` + LEGATE for G RYZ (b neutral),
  H CONDI (a good), I EBO (a good), J CUBI (b neutral), K DEDDO (a good), L MNZ (a good) + `enter,w200` (to the Castle).
  A second L)egate: "That character is already a legacy!" (verified on KLINDT: the stock six cannot be re-legated).
- **verified** `ADDPARTY` = `g,w120,a,w120,g,w90,h,w90,i,w90,j,w90,k,w90,l,w120,enter,w120`; `PARTY` =
  `CASTLE,IMPORT,LEGATEALL,ADDPARTY` (with `sav:00_transfer`): Castle with RYZ CONDI EBO CUBI DEDDO MNZ (`start`).
- **verified** `RESUME` = `CASTLE,ADDPARTY` with `sav:01_start` or `sav:02_ending` (same slots G-L).
- **verified** `MAZE` (Castle) = `e,w120,m,w600,enter,w200,n,w120`: camp ("Entering the Legacy of Llylgamyn" while it
  loads), leave camp, "Stairs down, take them (Y/N)?" N: floor 1 (0,0) facing north (`maze1`). The castle is *below*
  floor 1: the volcano is climbed, stairs to higher floors say "Stairs up".
- **Characters cannot be created** (verified: Training Grounds = I)nspect a character, R)oster of characters, Leave;
  no C)reate). New characters come only from Wizardry I/II through M)ove + L)egate, or the six stock ones.

## What the legacy keeps (verified: record diff of the six before/after, roster.py, sheets)
- Kept: name, password, race, class (the "caste"), the awards (honors) with a new letter **D** (descendant) added:
  RYZ ">DG" (Chevron of Rank, Mark of Gnilda), the others ">KD" (Knight of the City).
- Reset: level 1 (max level 1), E.P. 0, 8 hit points, age 20 (1,040 weeks), gold 500, no items, AC 10 at the first
  camp, status OK.
- Statistics are rolled again: each comes out near the old value but mostly lower (RYZ 16/9/4/14/9/8 -> 15/8/6/14/6/6
  in `start`; the exact values depend on frame timing: another route gave 15/8/6/12/9/7). Not race minimums.
- Spells: casters keep only their level-1 spell knowledge (EBO priest: the level-1 bits; MNZ bishop: mage and priest
  level 1); spell points 2 at level 1 (sheet "MAGE 0/0/0/0/0/0/0 PRST 0/..." for fighters).
- Alignment: chosen anew within the class rules (manual: "within traditional limitations").

## Controls
Wizardry I/II controls (those playbooks' tables) all apply; differences and checks here.
| Context | Key | Action | Status |
|---|---|---|---|
| Title | `s` / `m` | start game / make scenario disk | s verified; m not tried |
| Castle | `g` `a` `t` `b` `e` | Tavern, Inn, Temple, Boltac's, Edge of Town | all verified |
| Inn | digit, then `a`-`e` (stables free, cot 10, economy 50, merchants 200, royal 500), Enter | rest; level-up page | verified |
| Temple | letter (the roster in need), then the payer's digit, Enter | donation 100/level paralysis, 200 stoning, 250 death | verified |
| Tavern | `a` + letters, `r` + digit, digit, `d`, Enter | add ("* Bad alignment *" when good and evil would mix), remove, inspect, divvy, leave. The add list holds only characters free to join (and only legated ones), lettered A, B ... in roster order; the letters stay fixed while adding (add RYZ CONDI EBO CUBI DEDDO MNZ to an empty party: `g,h,i,j,k,l`; with RYZ in the party CONDI is `g`) | verified |
| Edge of Town | `t` `m` `c` `u` `l` | Training, Maze, Castle, Utilities, Leave game ("Thanks for playing Wizardry!") | all verified |
| Utilities | `c` `m` `r`, Enter | change name, move characters (1 Proving Grounds / 2 Knight of Diamonds, letters, Enter; Esc quits), restart an "out" party; Enter leaves to the Castle | m verified |
| Training | `i` `r`, Enter | inspect (letter -> L)egate I)nspect D)elete C)hange class A)lter password), roster list | i r, L)egate, I)nspect verified |
| Boltac's | digit, `b` `s` `u` `i` `p`; stock `p` `b` `f` `s` | as Wizardry I; stock starts with short sword 30, broadsword 50, mace 60, staff 20, hand axe 30, battle axe 140, dagger 10, flail 300, round shield 40, heater shield 80, mage's robes 30 ... | b, p + digit, f verified |
| Maze | `w` `a` `d`, `k`, `c`, `s`, `i`, `o` | as Wizardry II (command line "C)amp S)tatus I)nspect O)ff A-W-D K"); `k` goes through doors (one-way ones too) | w a d k c verified |
| Camp / sheet | `1`-`6`, `r`, `e`, Enter; sheet `r` `t` `p` `s` `e` `d` `i` `u` | as Wizardry II; E)quip goes slot by slot (weapon, armour, shield, helm, gauntlets: `1` per slot when each holds one item) and then asks "Will you invoke the special power of your X (Y/N)?" for every carried item with a power, in pack order: **this is how the crystals are used**; U)se on them shows nothing | all verified (capture) |
| Battle | `f` (+ group digit) `p` `s` `d` `u` `r` `t`, Enter | as Wizardry II ("Press Enter to fight, or T)ake back orders") | p, Enter verified |
| Prompts | `y` / `n`, Enter | stairs, "Will you search (Y/N)?", chest menu (O)pen C)alfo L)eave alone I)nspect D)isarm) | verified |
| Riddles | text + Enter | "What is your answer ?" | verified (wheel) |
| Ending | `y`, Enter, then `y`/`n` per roster character | "Will you surrender the orb ...?", "Press Enter to assign your stars!", "Award a star to KLINDT (Y/N)?" | verified |

Input timing: the default press works everywhere; waits that work (315 cycles): menu `w120`, Tavern `w90`-`w120`,
step `w60`-`w300`, entering the maze `w600`, a warp `w600`, **floors 5 and 6 reached by real stairs or `WARP` to
floor 5: "One moment" for about 1,200-1,800 frames** (`WARP5` adds `w1300`; keys pressed meanwhile are lost),
guardian fights `w800` after the step, message pages `w150`-`w300`.

## Game structure
- **Castle "Llylgamyn"** (verified menus): as Wizardry I/II. Roster on SAVE3.DSK at 0x1DE00 (RAM map).
- **The volcano** (disk data, `design/maps/floors.txt`, `python3 games/dos/wizardry-3/tools/maps.py`): six floors of
  20 x 20, x east, y north. Floors connect as a fork (verified by warps and stairs):
  | Floor | Admits (verified) | Ways up | Notes |
  |---|---|---|---|
  | 1 | anyone | (19,13) -> 2 (19,0); (19,14) -> 3 (2,2) | entrance (0,0) under the castle stairs; (18,13) L'kbreth's warning; lake squares (kind 5) with a beach and island (1,2)/(2,1); return stairs from 4 (7,7) and 5 (7,6) in the rock area; (19,15) teleport to the castle; large fixed-fight room (8-13, 8-19) |
  | 2 | a party with a good member or without evil ones | (0,19) -> 4 (10,2); (10,8) -> 4 (13,13) | the Grand Wizard S.E.G. Po'le's house (dining room, wine cellar), the desk (7,1) with the Staff of Earth, riddle (4,19) AIR, password (7,11) ABDUL SENT YOU, fixed fights (3,1) and (11,19) |
  | 3 | no good member | (0,1) -> 5 (11,0) | the monk's chest (7,7), the murky pool (10,19), Abdul's taxi (18,19)/(19,0), graveyard warnings (16-17,16-17) |
  | 4 | as floor 2 | (19,14) -> 6 (5,0) | **guardian (7,17): Living Legend / Delf with Gaunt Figures and Delf's Minions -> Crystal of Evil**; riddle (18,11) FIRE; Abdul (12,12) "Tell them Abdul sent you"; oily pool (10,5); traps "Look out!" along x=17-18; mostly dark |
  | 5 | no good member | (0,13) -> 6 (14,0) | **guardian (12,10): Soul Trappers (Hungry Monsters), Crusader Lords, Fighters -> Crystal of Good**; riddle (5,13) CHARIOT; Temple of the irascible Fung (19,9); Abdul's taxi (5000) and crystal sale (25000) (4,8)/(4,7); pits; anti-magic (6,14); mostly dark |
  | 6 | any party except an all-neutral one, and only carrying one of the four quest crystals/orb (items 1001-1004) | - | L'kbreth (8,3) "Farewell. May your way be easy."; three radiant statues (4,5) (12,2) (18,17); three "You have reached the statue" search squares (17,17) (13,2) (4,4); riddles (11,4) WHEEL and (19,17) DEATH; dragon room fight (9-10,4-5) group 77; (5,19) teleport to floor 1 (0,0) |
  A refused party sees "You are forbidden to enter here! Begone!!" and lands in the Castle (verified for good on 3
  and 5, evil on 2 and 4, every party without a crystal on 6, all-neutral with crystals on 6).
  ~~Floors 2/4 refuse any party with an evil member~~ (capture 2026-11-19, poked alignments, `try.py`): floors 2/4
  admit any party with at least one good member (1 good + 3 evil + 2 neutral entered both) and refuse a party
  with evil members and no good one; floors 3/5 refuse any party with a good member (3 good + 1 evil refused);
  all-neutral parties enter all four. The walkthrough's majority rule is wrong too.
- **Alignment rules** (verified): the Tavern refuses to put good and evil together ("* Bad alignment *"); neutrals
  join either. The fork therefore needs two parties: our six (four good, RYZ and CUBI neutral) take floors 2 and 4;
  `HALF2` (RYZ, CUBI + the stock neutrals KLINDT ZETT VERPA GITTER, all neutral) takes 3 and 5 (all-neutral parties
  are admitted on every floor but 6).
- **Quest items** (item number = record + 1000, names from the sheet): 1001 Orb of Earithin, 1002 Neutral Crystal,
  1003 Crystal of Evil, 1004 Crystal of Good, 1005 Ship in Bottle, 1006 Staff of Earth, 1007 Amulet of Air,
  1008 Holy Water, 1009 Rod of Fire, 1010 Gold Medallion, 1011 Orb of Mhuuzfes (cursed). 1000 is the empty item the
  game leaves where the orb was taken (no name, not listed).
- **The quest as verified** (checkpoints `guard_good` ... `after_ending`):
  1. The floor 4 guardian (7,17) with the good party drops the **Crystal of Evil** ("CUBI found: Crystal of Evil");
     the floor 5 guardian (12,10) with the neutral party drops the **Crystal of Good** (both verified, fights won by
     the `WIN` poke; the drop is the same item in every run tried).
  2. Any crystal (or the orb) opens floor 6 to a good or evil party (verified with each; stairs from floor 4 used
     for real in `floor6`).
  3. Floor 6 (17,17) "You have reached the statue." + "Will you search (Y/N)?" Y: the **Neutral Crystal becomes the
     Orb of Earithin** (verified). With the Crystal of Evil or Good there it does nothing. (13,2), the same kind of
     square, turns the Neutral Crystal into the cursed Orb of Mhuuzfes (verified); (4,4) starts a fight (Xeno).
  4. Back in the Castle with the orb in any pack (any party, any way home; `ending` uses the floor 6 (5,19)
     teleport and the floor 1 stairs): "* * Congratulations * * Will you surrender the orb to the sages of
     Llylgamyn (Y/N)?" Y: "* * The gods be praised * * With the Orb of Earithin, the sages of Llylgamyn will be able
     to find out what is causing the disasters that threaten us! In appreciation of your valor, I, Queen Beyki, great
     grand-daughter of Queen Margda, give your party the Star of Llylgamyn, and invite you to select 6 others who also
     deserve this august award!! Press Enter to assign your stars!", then "Award a star to KLINDT (Y/N)?" for the
     roster outside the party until six are chosen, then the Castle (verified).
  5. Each chosen character gets the award "*" and 150,000 E.P.; the party's own records show no new award (verified:
     `roster.py` on `02_ending`). The orb becomes the empty item 1000 in its bearer's pack.
  ~~**Open:** how the Neutral Crystal is made in play~~ **Solved (capture, 2026-11-19, verified, the walkthrough's
  rule):** one character who is good or evil carries both crystals and E)quips (camp or sheet); after the
  slots the game asks to invoke each crystal in pack order; N to the other one, Y to the crystal of his own
  alignment: both crystals become the Neutral Crystal (no message; MNZ, good bishop, in `gneutral`; an evil CONDI
  (poked) with the Crystal of Evil first did the same). Y to the other crystal: "Powers there be ... shall perish
  in flame!" and the bearer is ASHES, crystals gone. A neutral bearer: "Power springs for both extremes ..." and
  the crystals vanish (and 4 maximum HP); one crystal alone: "Nor good nor evil alone ..." and it vanishes.
  The scout's U)se in camp never reaches the power. The set plays it: `gcrystal_good` (RYZ found the Crystal of
  Good) -> `gcrystal_evil` (MNZ found the Crystal of Evil) -> camp, MNZ identifies, RYZ trades -> `gbearer` ->
  `gneutral`. The scout's checkpoints with the poked crystal (`statue`, `orb`, `ending`, `stars`,
  `after_ending`) stay in checkpoints.txt; the set uses the `g*` chain (Checkpoints).
- **Message squares and riddles** (texts read in play by pointing a riddle square at each message number; list in
  `design/messages.md`): riddle answers AIR (floor 2), FIRE (floor 4), CHARIOT (floor 5), WHEEL and DEATH (floor 6);
  password ABDUL SENT YOU (floor 2); Abdul's taxi G2500 (floor 3) and C5000 (floor 5), crystal 25000 (floor 5).
- **Search squares** ("Will you search (Y/N)?", kind 4): floor 2 desk (7,1) gives the Staff of Earth (verified,
  item 1006); floor 3 monk (7,7) and pool (10,19) did nothing for an empty-handed evil party (they swap items:
  decoded as broadsword -> Gold Medallion and Gold Medallion -> Holy Water, inferred from the statue rule).

## Shot plan
Set `main` captured 2026-11-19 (game-capture): 228 shots from power-on to the stars, verified and published
(`shots.txt`, `shots/main/`). Plan files were scratch (`work/cap/wizardry-3/plan/NN_*.txt`, joined in game order
by `work/cap/wizardry-3/assemble.py` into the work `shots.txt`, previewed with `tools/try.py`, shot with
`shoot.py --only`). How each area was reached:
- Title, disk prompt, loading: `@title` + `w20` frames with `!` (15 and 24).
- The import step by step: `sav:00_transfer,CASTLE,e,w120,u,w120,m,w200,2,w300`, letters, `enter` + `w20` x 1/2/4/6
  (removing, insert, moving, "RYZ has been moved"). The legacy: `IMPORT,e,w120,t,w120` + `i,w120,g,w200` + `l`, `enter`.
  "* Bad alignment *": a variant legacy with CUBI evil (`LEGATE:j:c`), then the Tavern adds CONDI (`h`) and CUBI (`i`).
- Castle services with the geared veterans (`@gcastle`): Boltac's pages `b,w200` + `f,w200`; identify fails without
  the gold, then `p` (pool) first; uncurse with a poked cursed Sallet-1 in CUBI's pack
  (`poke:E0F6=0400,poke:E110=0100010001002504`). Inn: stables give RYZ a level; the cot with `@gcured` (HP down).
  Temple: the real cures in the chain (`@ghome2` paralysis, `@ghome1` stoning); dead CONDI and ashed MNZ poked
  (status `+0x28` = 5 / 6, HP `+0x86` = 0) then `e,w120,c,w120,t,w150`.
- Camp: `@gcamp` (after `EQUIP`); sheets `N,w200`, books `r,w150,m|p,w150`, spells typed `s,w150,type:dumapic\n`.
  Identify and trade from `@gcured` (MNZ identifies with `w5` before `i`: other waits gave "You don't have a clue!").
- Maze views: `@gcastle,WARP:...` / `@gcastle2,WARP...` + `a,w60,d,w60`; `gameplay_f*` chosen after comparing views.
- Message squares: `tools/survey.py F --after w400` lines with `@start` replaced by `@gcastle` (floors 1, 2, 4) or
  `@gcastle2` (3, 5); riddle answers `enter,w200,type:X,w30`; searches `enter,w200,y` + `w20` frames.
- Battles: fixed-fight squares from the survey; a full round from `@gbattle` (floor 1 (0,9), Garian Guards) with
  `w40` timelines; random fights met while turning on floors 3 and 6.
- Guardians and the quest: the `g*` chain (Checkpoints), frames by `w40` timelines (`try.py --frames`).
- Death: statuses poked in the maze (`@gcamp,enter,w400,n,w200` + pokes, `c,w200`, Enter -> cemetery).
Not captured: Abdul's crystal sale and coffer on floor 5 (4,7)/(4,8) (no open neighbour; probably his taxi's
destination), the floor 6 dragon room fight (no fight when entered by the (10,3) door, once tried), M)ake scenario
disk after Y, Utilities C)hange name and R)estart past their first screen, the Leave game frame (DOSBox Pure's
overlay), level drain, a friendly group, R)un (the party's run in the Garian fight failed silently: no message).

## Strategy and walkthrough notes
- Cataloguing: never grind. `VET` (our six) and `VET2` (the HALF2 party) make realistic veterans (levels 10-13,
  HP, E.P., spell books copied from Wizardry II, ages 24-25, small gold). They have no gear: buy at Boltac's with
  `poke` gold or poke packs (pack layout in the RAM map; item numbers from `design/items.md`) and E)quip in camp.
- Gear: `GEAR` pokes a Boltac's outfit into the six packs (party order RYZ CONDI EBO CUBI DEDDO MNZ), `EQUIP`
  wears it in the first camp (20 slot answers): AC 1 2 6 7 9 7 (`gcamp`). `GEAR2` + `EQUIP2` do the same for
  KLINDT ZETT VERPA GITTER after `HALF2,VET2` (AC 3 9 4 5; RYZ and CUBI keep theirs).
- Guardians with that gear (verified, capture): floor 5's men silence, paralyze and cast BADIAL; ZETT's MADALTO
  killed the Crusader Lords in round 1, then `WIN` in round 2 (`gguard_evil_r2`). Floor 4: round 1 is a surprise
  round (fight only); DEDDO's TILTOWAIT killed Delf in round 2, the Gaunt Figures stoned RYZ, CONDI and EBO in
  rounds 2-3, `WIN` in round 4 (`gguard_good_r4`). The drops went to RYZ (Crystal of Good) and MNZ (Crystal of
  Evil, unidentified). Fights differ with the waits: the same orders with `w40` steps instead of `w3000` gave
  another battle (RYZ paralyzed, ZETT silenced).
- Guardians: win with `WIN` (all four group counts to 0) during the orders + `PARRY`; the drop follows.
- **The chain played for the set (capture, verified, two `WIN` pokes, no item pokes):** `gcastle` -> `HALF2,VET2,
  GEAR2` -> floor 5 guardian -> Crystal of Good (RYZ) -> floor 5 (18,0) stairs down (door from (17,0)) -> floor 1
  (0,1) -> (0,0) stairs -> Castle (paralyzed CUBI at the Temple, 1300) -> Tavern: the good six again -> floor 4
  guardian -> Crystal of Evil (MNZ) -> floor 4 (7,1) stairs down (from (8,1)) -> floor 1 -> Castle (three stoned:
  2400 + 2200 + 2400) -> camp: MNZ identifies, RYZ trades the Crystal of Good to MNZ -> MNZ E)quip, N, Y -> Neutral
  Crystal -> floor 4 (19,15) by the WARP pokes, step south onto the stairs -> floor 6 (a random ghost fight and a
  teleporter chest on the way) -> (19,18) south into the DEATH riddle -> door west to the radiant statue (18,17) ->
  west to (17,17), search Y -> the orb (MNZ identifies it) -> L'kbreth (8,3) "Farewell" (door from (7,3)) -> (6,19)
  `k` west -> floor 1 (0,0) -> Y -> Congratulations -> Y -> stars -> `gafter`.
- On arrival by stairs, turning (`a`,`d`) shows the arrival square's stairs prompt again: answer `n` first.
- Message boxes stay up until a key: press `enter` before position pokes, or the next key is eaten.
- Old critical path (scout, one item poke): `@vet` -> floor 4 guardian (7,17) -> Crystal of Evil -> floor 4 (19,14) stairs
  up -> floor 6 -> poke the Neutral Crystal over the crystal -> (17,17) search Y -> Orb -> floor 6 (5,19) teleport
  (`k` west from (6,19)) -> floor 1 stairs Y -> Congratulations -> Y -> stars.
- Message squares: arriving by `WARP` (stairs) does not trigger a square; step in from a neighbour: `WARP` next to
  it, `poke:DB6C=0F00` (facing), `a,w60,d,w60` (redraw; may start a random fight: then drop the turn and press `w`
  directly), `w` (or `k` for doors). Walls belong to the square you leave (one-way doors).
- Position pokes inside a floor (`DB72` x, `DB70` y, `DB6C` facing) work at once (used in `chest`, `floor6`,
  `statue`, `ending`); a new floor needs stairs, a teleport or `WARP` from the Castle.
- Dark squares (many on floors 4-6, `floors.txt`) draw the view as a grey fill (seen on floor 5, verified).

## Naming
No naming: characters come from Wizardry II (RYZ CONDI EBO CUBI DEDDO MNZ, named in Wizardry I) or the stock six.

## Shortcuts
| What | How (tokens / prefix / code) | Source | Status |
|---|---|---|---|
| Import + legacy | `sav:00_transfer,PARTY` (checkpoint `start`); `tools/transfer.py [SRC] [OUT]` rebuilds the save from any Wizardry II save | scout | verified |
| Warp anywhere | `WARP:FF:XX:YY` (hex) from the Castle: enters the maze and, at floor 1's "Stairs down" prompt, pokes that staircase (floor 1 special 13, AUX0/1/2 at `0B9FE`/`0BA1E`/`0BA3E`) to lead to floor FF square (XX,YY), then Y. The floor's admission rule still applies. Floor 5: `WARP5` (adds `w1300`) | scout | verified (floors 1-6) |
| Win a fight | `WIN` = group alive counts `0D454`, `0D54A`, `0D640`, `0D736` = 0 during the orders, then `PARRY` (everyone parries, Enter): counts as killed, E.P. and the drop follow | scout | verified (both guardians, chest fight) |
| Veterans | `VET` (party order RYZ CONDI EBO CUBI DEDDO MNZ), `VET2` (RYZ CUBI KLINDT ZETT VERPA GITTER) | scout | verified (sheets) |
| Second party | `HALF2` (Castle, our six formed): remove 6 5 3 2, add KLINDT ZETT VERPA GITTER | scout | verified |
| Any item | pack count `+0x3A`, entries `+0x3C` (4 words: equipped, cursed, identified, item 1000+n) of a party record | scout | verified |
| The orb | an orb (item 1001) in any pack + reaching the Castle = ending | scout | verified |
| Gear | `GEAR` + `EQUIP` (first camp), `GEAR2` + `EQUIP2` (the neutral party) | capture | verified (sheets, AC) |
| Read any message | poke a riddle square's AUX1 (both floor copies) to the number and AUX2 to 1, step in (`tools/msgdump.py`) | scout | verified |
No downloadable saves or codes looked for beyond the sources below (the package ships ready disks).

### Saves (games/dos/wizardry-3/saves/, committed; nothing in rom/saves/)
| Name | Contents | Made by | Status |
|---|---|---|---|
| 00_transfer | only `WIZAR3/SAVE2.DSK` = Wizardry II `03_wizardry3_transfer`'s disk | `tools/transfer.py` | verified (`start`) |
| 01_start | both disks after the import, the legacy and Leave game | `@edge,l,w600` + export | verified (`resume`) |
| 02_ending | after the ending: the six as veterans, the stock six with stars | `@after_ending,e,w120,l,w600` + export | verified (`resume_end`, roster.py) |
| 03_final | after the ending played with the Neutral Crystal made in play: the six veterans in Boltac's gear, the four stock neutrals geared, the stock six with stars | `@gafter,e,w120,l,w600` + export | verified (roster.py) |
List them: `python3 games/dos/wizardry-3/tools/roster.py FILE`.

## RAM map (for `game.json` "ram" watches and pokes)
Physical addresses; most are Wizardry II's + 0xA6 (Wizardry I's + 0x14C).
| Address | Size | Meaning | How found |
|---|---|---|---|
| `0DB6C` | 2 | facing: 0 N, 1 E, 2 S, 3 W | RAM diff over two turns (verified) |
| `0DB6E` | 2 | floor: 0 castle, 1-6 (65535 in the Castle menus) | warp (verified) |
| `0DB70` | 2 | y, 0-19 north | warp + peek (verified) |
| `0DB72` | 2 | x, 0-19 east | warp + poke (verified) |
| `0DE4C + n*0xD0` | 208 | party member n (0-5, party order) as a full character record (Wizardry I layout); `+0x26` age in weeks, `+0x2A` alignment 1 G 2 N 3 E, `+0x34` gold (3 words), `+0x3A` pack count, `+0x3C` 8 entries, `+0x7C` E.P., `+0x84` level, `+0x86`/`+0x88` HP, `+0x8A` spells known, `+0x92`/`+0xA0` spell points, `+0xCE` awards | name search, pokes (verified for all six slots) |
| `0B6E4` | 894 | the floor in play (TMAZE, `tools/maps.py`); a second copy at `0E524` is the one special squares read (poke both); floor 1 special 13 (stairs to the castle) AUX0/AUX1/AUX2 at `0B9FE`/`0BA1E`/`0BA3E` (used by `WARP`) | match with WIZ3.DSK (verified) |
| `0D454` / `0D456` / `0D458` | 2 / 2 / 2 | in battle, group 1: alive count / count / monster number; groups 0xF6 apart (`0D54A`, `0D640`, `0D736`); monster hit points from `0D460` (records 16 bytes) | dump + poke (verified: `WIN`) |
| `01980` | | the loader WIZ3.COM (CS 0198h), as WIZ2.COM | PC (code) |
Character record: as Wizardry I/II; awards word `+0xCE` letters from the game's string ">!$#&*<?BCPKODG@" (bit n =
n-th letter): bit 0 ">" Chevron of Rank, bit 5 "*" Star of Llylgamyn, bit 11 "K" Knight of the City, bit 13 "D"
descendant (every Wizardry III character; L)egate refuses a second time), bit 14 "G" Mark of Gnilda (verified).
Roster on disk: SAVE3.DSK `1DE00` (SCENARIO.DATA at `1DA00`, its table of contents: characters block 2, maze block
12, monsters 24, rewards 40, items 48 (46-byte records, 22 per 1,024 bytes), 104 items, 78 monster records,
24 reward records). Floors: `1F200 + (floor-1)*0x400`.

## Emulation notes
- **Model `ega-315`**, as Wizardry I and II (same CGA booter; frames identical across state loads, Checkpoints).
- Writes through the open SAVE3.DSK reach states at once (backend fix 2026-11-19): every checkpoint gave the same
  disk on a cache hit and an empty-cache rebuild, also after Leave game.
- After Leave game the program has ended ("Thanks for playing Wizardry!"); export works there.
- "One moment" loads of floors 5 and 6 take 1,200-1,800 frames at 315 cycles; keys pressed during the load are lost.
- RNG: random fights and guardian group sizes follow frame timing (the floor 4 guardian group was 4 groups in one
  route, 2 in another); turning (`a`,`d`) can start a fight on a fight-zone square.
- Messages are compressed on the disk (no plain text in WIZ3.DSK): read them in play.

## Checkpoints
| Name | What |
|---|---|
| `title` | title screen |
| `start` | Castle, the imported, legated six formed (from `sav:00_transfer`) |
| `edge`, `training`, `camp`, `maze1` | Edge of Town; Training Grounds (no create); first camp; floor 1 (0,0) |
| `resume`, `resume_end` | Castle, party formed from `sav:01_start` / `sav:02_ending` |
| `half2` | Castle, the all-neutral party for floors 3 and 5 (RYZ CUBI KLINDT ZETT VERPA GITTER) |
| `battle` | floor 1 (15,18): 3 Giant Serpents, RYZ's options |
| `vet`, `vet2` | the two parties as veterans (`VET`, `VET2`) |
| `guard_good`, `crystal_evil` | floor 4 (7,17) guardian; after it, "CUBI found: Crystal of Evil" |
| `chest` | floor 4 (18,14): a chest after a fight |
| `floor6` | floor 6 (5,0), reached by the floor 4 stairs with the Crystal of Evil |
| `statue`, `orb` | floor 6 (17,17) "You have reached the statue." (Neutral Crystal poked); after Y: the Orb |
| `ending`, `stars`, `after_ending` | Congratulations prompt; "The gods be praised" page; Castle after the stars |
| `guard_evil`, `crystal_good` | floor 5 (12,10) guardian with the HALF2 veterans; "CUBI found: Crystal of Good" |
| `gcamp`, `gcastle` | the six veterans geared (`VET,GEAR` + `EQUIP` in the first camp); back in the Castle |
| `gcamp2`, `gcastle2` | the neutral party (`HALF2,VET2,GEAR2` + `EQUIP2`) geared; in the Castle |
| `gguard_evil`, `gguard_evil_r2`, `gcrystal_good` | floor 5 guardian: round 1 options, round 2 (CUBI paralyzed), after the `WIN` round ("RYZ found: Crystal of Good") |
| `ghome2`, `greform` | Castle after the floor 5 trip; CUBI cured, the good six re-formed |
| `gguard_good`, `gguard_good_r2`/`_r3`/`_r4`, `gcrystal_evil` | floor 4 guardian rounds 1-4; "MNZ found: Crystal of Evil" |
| `ghome1`, `gcured` | Castle with three stoned; cured, party re-formed |
| `gbearer`, `gneutral` | camp: MNZ holds both crystals; after the invoke: the Neutral Crystal |
| `gfloor6` | floor 6 (5,0) with the Neutral Crystal |
| `gf6_ghosts`, `gf6_ghosts_r2`, `gchest6`, `gloot6` | floor 6 (19,18) random fight, round 2, the chest, after the loot |
| `gdeath`, `gstatue`, `gorb`, `gorbid` | DEATH answered; "You have reached the statue."; the orb; identified |
| `gfarewell`, `ghomeorb`, `gending`, `gstars`, `gafter` | L'kbreth; floor 1 after the teleport; Congratulations; the Queen; Castle after the stars |
| `gbattle` | floor 1 (0,9) Garian Guards, round 2 options (battle mechanics shots) |
The `g*` checkpoints (capture) were made in a `play.py` session. `gfloor6` first did not reproduce from an empty
cache (coordinator's cold verify 199/228, 2026-11-19): a `play.py do "y,w300!"` had pressed `y` before failing on
the bad token, and that press was not recorded. The route now holds both presses (`...,y,y,w300,w1800,...`) and
the cold replay matches the published frames (fix-up, cold `--verify` below). Lesson: after a `do` that fails on
a token, `undo` before going on, or the session drifts from its route.
Every scout checkpoint was rebuilt from an empty cache and compared with cache hits in fresh processes on 2026-11-19
(`work/scout/wizardry-3/cmp.py`, scratch): identical frames, party records, position and written disks (also after
Leave game from `start`, `resume`, `after_ending`).

## Sources
| Source | URL | Used for | Accessed |
|---|---|---|---|
| Wikipedia | https://en.wikipedia.org/wiki/Wizardry_III:_Legacy_of_Llylgamyn | year, developer, six-level volcano climbed upward, descendants keep name and class, level 1, new alignment | 2026-11-19 |
| Apple II manual (archive.org text) | https://archive.org/stream/sir-tech-wizardry-3-a2-v4-ph/components/wizardry%203%20manual_djvu.txt | rite of passage: caste and honors inherited, alignment within limits, level 1, up to 500 gold, no goods; the orb taken by the dragon L'kbreth to her mountain lair and guarded by good and evil; Disband removed, Pool gold added | 2026-11-19 |
| Search summaries (hosts not fetched: outside the network) | tk421.net, the-spoiler.com, wizardry.wiki.gg, mocagh.org | "no character creation", "trade a Neutral Crystal for the orb at level 6 after a riddle"; the tk421 walkthrough's crystal rule (both crystals, one non-neutral bearer invokes his own: verified in play 2026-11-19); its majority stair rule (wrong, Game structure) | 2026-11-19 |
| the loader and disks | `rom/wizardry-3.zip` | loader (ndisasm), roster, floors, items (on screen), messages (in play) | 2026-11-19 |
| Wizardry I and II DOS work | `games/dos/wizardry/`, `games/dos/wizardry-2/` | engine, controls, record layout, tools | 2026-11-19 |
GameFAQs, TCRF, StrategyWiki: known 403 for agents (not tried); tk421.net, mirror.cyberbits.eu (a textfiles
walkthrough): not resolvable from the session; archive.org download hosts refused (the manual's text page worked).

## Open questions
- ~~How the Neutral Crystal is made~~: solved 2026-11-19 (Game structure, The quest). Still open: Abdul's crystal
  sale on floor 5 (4,8) (25000 gold) and the coffer (4,7) (kind 2, item 1009 the Rod of Fire?): no open neighbour,
  probably reached by his floor 5 taxi.
- The lake on floor 1 (kind 5, AUX0 5: the Ship in Bottle 1005?) and the island (1,2)/(2,1) (kind 13, AUX0 31): not
  tried. Floor 3 (0,0) kind 14 and floor 4 (10,5) kind 3: not decoded.
- ~~The monk and pool swaps~~: verified 2026-11-19 (KLINDT's broadsword -> Gold Medallion -> Holy Water, RAM).
  What the swap items, the Staff of Earth, Amulet of Air and Rod of Fire are for: not known.
- The floor 6 dragon room (9-10,4-5, fixed fight group 77): entered by the (10,3) door, no fight (once tried).
- What the "D" award and the stars change in play; whether the party should have received a star (no award bit
  was set on the party, verified on disk and in memory).
- M)ake scenario disk; Utilities C)hange name and R)estart past their first screen; moving Wizardry I characters.
