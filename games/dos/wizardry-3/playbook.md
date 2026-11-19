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
| Genre | First-person party RPG, the third scenario of Wizardry: descendants of the Wizardry I/II heroes climb six wireframe floors of a volcano; floors 2/4 admit no evil character, 3/5 no good one |
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
`PARTY`, `RESUME`, `HALF2`, `MAZE`, `WARP:FF:XX:YY`, `WARP5:FF:XX:YY`, `VET`, `VET2`, `WIN`, `PARRY`. Every macro ran
inside a checkpoint route rebuilt from power-on with an empty cache (see Checkpoints).
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
| Castle | `g` `a` `t` `b` `e` | Tavern, Inn, Temple, Boltac's, Edge of Town | g b e verified |
| Tavern | `a` + letters, `r` + digit, digit, `d`, Enter | add ("* Bad alignment *" when good and evil would mix), remove, inspect, divvy, leave | a r digit verified |
| Edge of Town | `t` `m` `c` `u` `l` | Training, Maze, Castle, Utilities, Leave game ("Thanks for playing Wizardry!") | all verified |
| Utilities | `c` `m` `r`, Enter | change name, move characters (1 Proving Grounds / 2 Knight of Diamonds, letters, Enter; Esc quits), restart an "out" party; Enter leaves to the Castle | m verified |
| Training | `i` `r`, Enter | inspect (letter -> L)egate I)nspect D)elete C)hange class A)lter password), roster list | i r, L)egate, I)nspect verified |
| Boltac's | digit, `b` `s` `u` `i` `p`; stock `p` `b` `f` `s` | as Wizardry I; stock starts with short sword 30, broadsword 50, mace 60, staff 20, hand axe 30, battle axe 140, dagger 10, flail 300, round shield 40, heater shield 80, mage's robes 30 ... | b, p + digit, f verified |
| Maze | `w` `a` `d`, `k`, `c`, `s`, `i`, `o` | as Wizardry II (command line "C)amp S)tatus I)nspect O)ff A-W-D K"); `k` goes through doors (one-way ones too) | w a d k c verified |
| Camp / sheet | `1`-`6`, `r`, `e`, Enter; sheet `r` `t` `p` `s` `e` `d` `i` `u` | as Wizardry II; U)se on the crystals shows nothing (tried in camp) | inspect verified |
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
  | 2 | no evil member | (0,19) -> 4 (10,2); (10,8) -> 4 (13,13) | the Grand Wizard S.E.G. Po'le's house (dining room, wine cellar), the desk (7,1) with the Staff of Earth, riddle (4,19) AIR, password (7,11) ABDUL SENT YOU, fixed fights (3,1) and (11,19) |
  | 3 | no good member | (0,1) -> 5 (11,0) | the monk's chest (7,7), the murky pool (10,19), Abdul's taxi (18,19)/(19,0), graveyard warnings (16-17,16-17) |
  | 4 | no evil member | (19,14) -> 6 (5,0) | **guardian (7,17): Living Legend / Delf with Gaunt Figures and Delf's Minions -> Crystal of Evil**; riddle (18,11) FIRE; Abdul (12,12) "Tell them Abdul sent you"; oily pool (10,5); traps "Look out!" along x=17-18; mostly dark |
  | 5 | no good member | (0,13) -> 6 (14,0) | **guardian (12,10): Soul Trappers (Hungry Monsters), Crusader Lords, Fighters -> Crystal of Good**; riddle (5,13) CHARIOT; Temple of the irascible Fung (19,9); Abdul's taxi (5000) and crystal sale (25000) (4,8)/(4,7); pits; anti-magic (6,14); mostly dark |
  | 6 | any party except an all-neutral one, and only carrying one of the four quest crystals/orb (items 1001-1004) | - | L'kbreth (8,3) "Farewell. May your way be easy."; three radiant statues (4,5) (12,2) (18,17); three "You have reached the statue" search squares (17,17) (13,2) (4,4); riddles (11,4) WHEEL and (19,17) DEATH; dragon room fight (9-10,4-5) group 77; (5,19) teleport to floor 1 (0,0) |
  A refused party sees "You are forbidden to enter here! Begone!!" and lands in the Castle (verified for good on 3
  and 5, evil on 2 and 4, every party without a crystal on 6, all-neutral with crystals on 6).
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
  **Open:** how the Neutral Crystal is made in play. Tried without effect: the three radiant statues and L'kbreth
  (8,3) with each crystal, both crystals, equipped, U)sed in camp, with good, evil, neutral and mixed (poked)
  parties. The statue squares say "In one hand it holds a shining crystal sphere. The other hand is empty." The
  route therefore pokes the Neutral Crystal (`statue`); see Open questions.
- **Message squares and riddles** (texts read in play by pointing a riddle square at each message number; list in
  `design/messages.md`): riddle answers AIR (floor 2), FIRE (floor 4), CHARIOT (floor 5), WHEEL and DEATH (floor 6);
  password ABDUL SENT YOU (floor 2); Abdul's taxi G2500 (floor 3) and C5000 (floor 5), crystal 25000 (floor 5).
- **Search squares** ("Will you search (Y/N)?", kind 4): floor 2 desk (7,1) gives the Staff of Earth (verified,
  item 1006); floor 3 monk (7,7) and pool (10,19) did nothing for an empty-handed evil party (they swap items:
  decoded as broadsword -> Gold Medallion and Gold Medallion -> Holy Water, inferred from the statue rule).

## Shot plan
Set `main`, to be captured by game-capture. Ids, category, what; routes start from the checkpoints named. About
120 shots planned (counts by category at the end). Lines are in `shots.txt` as comments until shot.
- Boot and front end: `title_screen` title (`@title`); `menu_make_scenario` (title `m`); loading/"Place duplicate
  scenario diskette" frames (`@title,s,w100!`); `menu_castle_start` (`@start`).
- Transfer and legacy (seq-legacy, the distinctive system): `menu_edge`, `menu_utilities`, `menu_move_scenario`
  (1 Proving Grounds / 2 Knight of Diamonds), `menu_move_list`, `menu_move_marked`, `menu_move_moving`
  (`sav:00_transfer,CASTLE,...` step by step), `menu_training`, `menu_training_list`, `inventory_ancestor_sheet`
  (RYZ L12 ">G" before the rite), `menu_char_options` (L)egate ...), `dialogue_rite` ("The rite of passage ceremony
  now begins"), `menu_alignment` (A/B/C), `menu_alignment_thief` (B/C only for CUBI), `inventory_descendant_sheet`
  (RYZ L1 ">DG"), `menu_already_legacy` ("That character is already a legacy!", KLINDT), `menu_roster` (Training
  R)oster), `menu_tavern_bad_alignment` ("* Bad alignment *").
- Castle: `menu_tavern`, `menu_tavern_party`, `menu_inn`, `menu_temple`, `shop_boltac`, `shop_boltac_stock`
  (2 pages), `shop_buy`, `inventory_sheet_gear` (castle), `hud_castle_party`.
- Maze basics: `camp_menu`, `camp_equip`, `gameplay_maze_f1_start` (`@maze1`), `gameplay_wall`, `gameplay_door`,
  `gameplay_status_off`, `gameplay_full_view`, `gameplay_inspect`, `gameplay_stairs_up` (floor 1 (19,13)),
  `gameplay_one_moment` (floor 5 load).
- Floors (one view each, compare views before snapping: wireframes repeat): `gameplay_f2`, `gameplay_f3`,
  `gameplay_f4_dark`, `gameplay_f5`, `gameplay_f6`; `gameplay_forbidden` ("You are forbidden to enter here!
  Begone!!", good party on the floor 3 stairs: `@start,WARP:01:13:0E,y,w100` + frames).
- Message squares (one each, routes from `tools/survey.py` + `tools/try.py`, see Strategy):
  floor 1 L'kbreth's warning (18,13), beach (1,2), water's edge, barracks (2,19), fortress and moat (1,17); floor 2
  dining room (18,12), wine cellar (12,19), S.E.G. Po'le (2,1), desk (7,1) + "Will you search" + found Staff of
  Earth, riddle AIR (4,19) question/answer, password woman (7,11); floor 3 "I'd turn back" (2,3), "another
  direction" (3,2), monk (7,7), murky pool (10,19), Abdul's taxi (18,19), graveyard lines (16-17,16-17); floor 4 oily
  liquid (10,5), Abdul (12,12), "Look out!" trap (17,1), riddle FIRE (18,11); floor 5 Temple of Fung (19,9), Abdul's
  crystal offer (4,8, two pages), taxi 5000 (0,2), riddle CHARIOT (5,13); floor 6 radiant statue (4,5), L'kbreth
  "Farewell" (8,3), riddles WHEEL (11,4) and DEATH (19,17).
- Battles: `battle_f1_serpents` (`@battle`), 6-8 more random groups on floors 1-6 (warp onto fight zones, vary the
  wait), `battle_spell` (S)pell with the veterans), `battle_result_xp`, `battle_chest` (`@chest`), `battle_chest_open`,
  `battle_found_item`, `boss_guardian_good` (`@guard_good`), `boss_guardian_good_won` ("CUBI found: Crystal of
  Evil", `@crystal_evil` frames), `boss_guardian_evil` (`@guard_evil`), `boss_guardian_evil_won`, `boss_dragon_room`
  (floor 6 (9,4) group 77), `battle_xeno` (floor 6 (4,4) search fight).
- Quest end (seq-orb, from `@floor6`): `inventory_crystals` (camp sheet with the Crystal of Evil and of Good),
  `gameplay_f6_arrival`, `dialogue_statue_reached` (`@statue`), `dialogue_search`, `inventory_orb` (camp sheet with
  the Orb of Earithin), `gameplay_teleport_home`, `ending_congratulations` (`@ending`), `ending_gods_praised`
  (`@stars`), `ending_award_star` ("Award a star to KLINDT"), `menu_castle_after_ending` (`@after_ending`),
  `inventory_star_sheet` (KLINDT with "*D" after the ending, Tavern/Training inspect from `@resume_end`).
- Game over: `gameover_party_dead` (a level-1 party killed by the floor 4 guardian: `@start,WARP:04:07:12,
  poke:DB6C=0200,a,w60,d,w60,w,w800` then let it fight), `menu_temple_dead`.
- Items and content: `inventory_quest_items` (sheet with 1001-1008 poked in camp), one sheet per item family
  (weapons, armour, magic items, curse: Orb of Mhuuzfes from (13,2)), `inventory_spellbook` (R)ead with the veterans).
Counts (approximate): boot/title 3, menu 25, shop 4, gameplay 20, dialogue 30, battle 12, boss 6, inventory 10,
ending 5, gameover 2, hud 1, map 0 (no automap; floor maps are in design/maps).

## Strategy and walkthrough notes
- Cataloguing: never grind. `VET` (our six) and `VET2` (the HALF2 party) make realistic veterans (levels 10-13,
  HP, E.P., spell books copied from Wizardry II, ages 24-25, small gold). They have no gear: buy at Boltac's with
  `poke` gold or poke packs (pack layout in the RAM map; item numbers from `design/items.md`) and E)quip in camp.
- Guardians: win with `WIN` (all four group counts to 0) during the orders + `PARRY`; the drop follows.
- Critical path (verified, one poke): `@vet` -> floor 4 guardian (7,17) -> Crystal of Evil -> floor 4 (19,14) stairs
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
| Read any message | poke a riddle square's AUX1 (both floor copies) to the number and AUX2 to 1, step in (`tools/msgdump.py`) | scout | verified |
No downloadable saves or codes looked for beyond the sources below (the package ships ready disks).

### Saves (games/dos/wizardry-3/saves/, committed; nothing in rom/saves/)
| Name | Contents | Made by | Status |
|---|---|---|---|
| 00_transfer | only `WIZAR3/SAVE2.DSK` = Wizardry II `03_wizardry3_transfer`'s disk | `tools/transfer.py` | verified (`start`) |
| 01_start | both disks after the import, the legacy and Leave game | `@edge,l,w600` + export | verified (`resume`) |
| 02_ending | after the ending: the six as veterans, the stock six with stars | `@after_ending,e,w120,l,w600` + export | verified (`resume_end`, roster.py) |
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
Every checkpoint was rebuilt from an empty cache and compared with cache hits in fresh processes on 2026-11-19
(`work/scout/wizardry-3/cmp.py`, scratch): identical frames, party records, position and written disks (also after
Leave game from `start`, `resume`, `after_ending`).

## Sources
| Source | URL | Used for | Accessed |
|---|---|---|---|
| Wikipedia | https://en.wikipedia.org/wiki/Wizardry_III:_Legacy_of_Llylgamyn | year, developer, six-level volcano climbed upward, descendants keep name and class, level 1, new alignment | 2026-11-19 |
| Apple II manual (archive.org text) | https://archive.org/stream/sir-tech-wizardry-3-a2-v4-ph/components/wizardry%203%20manual_djvu.txt | rite of passage: caste and honors inherited, alignment within limits, level 1, up to 500 gold, no goods; the orb taken by the dragon L'kbreth to her mountain lair and guarded by good and evil; Disband removed, Pool gold added | 2026-11-19 |
| Search summaries (hosts not fetched: outside the network) | tk421.net, the-spoiler.com, wizardry.wiki.gg, mocagh.org | "no character creation", "trade a Neutral Crystal for the orb at level 6 after a riddle" (the trade itself not found in play) | 2026-11-19 |
| the loader and disks | `rom/wizardry-3.zip` | loader (ndisasm), roster, floors, items (on screen), messages (in play) | 2026-11-19 |
| Wizardry I and II DOS work | `games/dos/wizardry/`, `games/dos/wizardry-2/` | engine, controls, record layout, tools | 2026-11-19 |
GameFAQs, TCRF, StrategyWiki: known 403 for agents (not tried); tk421.net, mirror.cyberbits.eu (a textfiles
walkthrough): not resolvable from the session; archive.org download hosts refused (the manual's text page worked).

## Open questions
- **How the Neutral Crystal is made** (needed for the statue): not by the statues (4,5)/(12,2)/(18,17) or L'kbreth
  (8,3) in any variant tried (crystals carried, both, equipped, U)sed; good, evil, neutral, poked mixed parties).
  Leads: Abdul's crystal sale on floor 5 (4,8) (25000 gold, then the coffer (4,7) "kind 2" gives item 1009 the Rod of
  Fire? not reached: (4,8) is entered only one way, probably by his taxi), the floor 6 riddles (answered, no visible
  effect), message kinds 13/15/16 not decoded; the source summary says L'kbreth trades the orb for the Neutral
  Crystal after a riddle. Decoding the SPECIALS p-code segment of WIZ3.DSK would settle it.
- The lake on floor 1 (kind 5, AUX0 5: the Ship in Bottle 1005?) and the island (1,2)/(2,1) (kind 13, AUX0 31): not
  tried. Floor 3 (0,0) kind 14 and floor 4 (10,5) kind 3: not decoded.
- The monk (floor 3 (7,7)) and pool (10,19) swaps (inferred broadsword -> Gold Medallion -> Holy Water): not tried
  with the items.
- What the "D" award and the stars change in play; whether the party should have received a star (no award bit
  was set on the party, verified on disk and in memory).
- M)ake scenario disk; Utilities C)hange name and R)estart past their first screen; moving Wizardry I characters.
