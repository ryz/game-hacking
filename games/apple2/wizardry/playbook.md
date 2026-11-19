# Wizardry: Proving Grounds of the Mad Overlord (Apple II) - playbook

Everything an agent needs to play this game efficiently: read it before playing, add to it after every run.
Status of each fact: **verified** (seen in the emulator, with the route) or **source** (manual/FAQ/wiki, not yet
checked). Never delete a fact that turned out wrong: strike it and say what is true.
"disk data" = decoded from the scenario disk image with `tools/maps.py` / `tools/data.py`.
The same game is documented in depth for its DOS port (`games/dos/wizardry/`: playbook, design documents, 208
shot routes). This is the 1981 original: the scenario (floors, items, monsters, spells, quest) is the same data,
the screens, keys, timing and memory are not. Section "The DOS material here" says how to carry routes over.

## Identity
| Field | Value |
|---|---|
| Title (EN / original) | Wizardry: Proving Grounds of the Mad Overlord (title logo "Wizardry"; scenario disk header "PROVING GROUNDS OF THE MAD OVERLORD!") (verified) |
| Version | "VERSION 2.1 OF 22-JAN-82  SER:??????" on the copyright screen (verified); volumes `WBV2.1` (boot) and `WSV2.1` (scenario) |
| Platform / model used | Apple II, `game.json` model `iiplus` (see Emulation notes: on the default `iie` the text comes out in 80-column mode, every second column blank) |
| Release (region, year) | North America, 1981 (copyright screen "COPYRIGHT (C)1981 ... ANDREW GREENBERG, INC & ROBERT WOODHEAD, INC.") |
| Developer / publisher | Andrew Greenberg, Robert Woodhead / Sir-Tech Software (copyright screen; publisher: source, DOS playbook) |
| Genre | First-person party RPG: six adventurers, a castle of text menus, a ten-floor wireframe maze of 20 x 20 squares |
| Players / save system | 1 player; a roster of 20 characters on the scenario disk, written by the game as it goes (character creation, Tavern, leaving the maze, L)eave game); no other save |
| Runtime | Apple Pascal (UCSD p-code): `SYSTEM.PASCAL`, `SYSTEM.STARTUP` (title, menu, utilities) and `WIZARDRY.CODE` on the boot side; `WIZARDRY.CODE`, `SCENARIO.DATA`, `SCENARIO.MESGS` on the scenario side (disk data) |

## The dump: two disk sides
`rom/wizardry.zip` (never committed) = `1 Boot.dsk` + `2 Scenario.dsk`, 140 KiB sector images in DOS 3.3 sector
order (SHA-1s in `game.json` "header"). Owner's upload 2026-11-19.
- **verified** Both are plain sector images that boot and play: no copy-protection failure seen. The serial
  number reads `??????` (a cleaned or cracked copy).
- **verified** The scenario side is **not a factory disk**: its roster is full, 20 characters of an earlier
  player (JIB, JASON, JAKE, GOR, DIRK THE DARING, ROB, STYX, KILLER, HENRY, QUIOP WERT, GIMLI, SAM THE SHAM, WOW!,
  SALA WHO, PAPERBOY, BOB, DUMP, MR.T, SNOPPY, THAYER; levels 9-50, several with the chevron, none with a
  password). "THERE IS NO ROOM LEFT - TRY DELETING" until some are deleted: the macro `WIPE` deletes all 20.
- **verified** No duplicate scenario disk is needed. The game asks "SCENARIO MASTER IN DRV 1, PRESS [RET]" and
  then "MASTER/DUPLICATE IN DRV 1, PRESS [RET]"; the registered scenario image answers both (`disk:2,enter`, then
  `enter`). The emulator plays on private copies and every savestate carries what the game wrote, so the dump
  never changes. U)TILITIES -> M)AKE SCENARIO DISK was not used (its menu: verified; it wants the master in
  drive 2 and a formatted disk in drive 1).
- **verified** `rom/wizardry.zip` is also the path the DOS game's `game.json` names (`games/dos/wizardry/`):
  the Apple II intake replaced the DOS dump in this container. Tools here always say `apple2/wizardry`.

## Boot sequence
Macros (all in `game.json`): `TITLE`, `MENU`, `CASTLE`, `TRAINING`, `DEL:name`, `WIPE`,
`MAKE:name:race:align:stats:class`, `PARTYMAKE`, `ADD:name`, `ADDPARTY`, `PARTY`, `RESUME`, `MAZE`, `MAZE2`,
`WARP:floor:x:y`, `VET`, `GEARPOKE`, `EQUIPALL`, `AMULET`, `HOME`. `CASTLE,TRAINING,WIPE,PARTYMAKE` was run as
one route from power-on (roster checked on screen); the others inside checkpoint routes replayed cold.
- **verified** Power-on: black with a cursor for 15 s (Pascal loading), "PREPARE YOURSELF / FOR THE ULTIMATE / IN
  FANTASY GAMES" from frame ~960, the wizard at his cauldron from ~1200, smoke rising into the Wizardry logo,
  complete at about frame 1900; the logo's colours keep cycling (orange, green), then the screen clears and the
  animation starts over (blank at frame 3000). `TITLE` = `w2100`.
- **verified** Any key on the title: the program reads and re-writes block 0 of the boot disk and **hangs on
  purpose unless the write is refused as write-protected** (p-code at `843C`: UNITREAD, UNITWRITE, `IORESULT <>
  16` -> an endless loop at `8458`: `00 A1 F6`). The emulator has no write protection (docs/emulator/apple2.md,
  "Not supported yet"), so the screen stays black for ever. `MENU` = `TITLE,space,w300,poke:845A=00,w300`: the
  poke turns the loop's backward jump into "go on" once the program sits in it. The address is the same on
  `iie` and `iiplus`. Without the poke nothing past the title can be reached.
  A key during the opening animation goes to the same check at once (the text stays on screen while it hangs).
- **verified** Menu: the copyright text, the version line and `S)TART GAME  U)TILITIES  T)ITLE PAGE`.
  `T` replays the title. `U`: "WIZARDRY UTILITIES - R)ECOVER T)RANSFER B)ACKUP M)AKE SCENARIO DISK U)PDATE
  C)HANGE NAMES L)EAVE" (menu verified, entries not used).
- **verified** `S`: "SCENARIO MASTER IN DRV 1, PRESS [RET]" -> `disk:2,enter`; "MASTER/DUPLICATE IN DRV 1, PRESS
  [RET]" -> `enter`; the Castle about 10 s later. `CASTLE` = `MENU,s,w300,disk:2,enter,w600,enter,w900`. The boot
  disk is not asked for again until L)eave game ("PRESS [RETURN] FOR MORE WIZARDRY", then the master prompt:
  the scenario disk is still in the drive, `enter` twice goes back to the Castle).
- **verified** `PARTY` = `CASTLE,TRAINING,WIPE,PARTYMAKE,enter,w400,g,w300,ADDPARTY,enter,w300`: deletes the 20
  inherited characters, creates the six in the Training Grounds, adds them in the Tavern; ends on the Castle
  menu (checkpoint `start`; about 60 s to build cold, 32,000 frames).
- **verified** `RESUME` = `CASTLE,g,w300,ADDPARTY,enter,w300` after `sav:01_start` or `sav:02_ending` (checkpoints
  `resume`, `resume_end`).
- **verified** `MAZE` (Castle menu, first maze entry of a session) = `e,w300,m,w600,l,w300,n,w200`: Edge of
  Town, Maze, the Camp, L)eave, "STAIRS GOING UP. TAKE THEM (Y/N) ?" N -> floor 1 (0,0) facing north.
  **A second entry in the same session loads longer** (the camp was not ready after `w600`, the keys were
  lost and the party stood on the stairs prompt): use `MAZE2` (`m,w1200`) for every entry after the first.
  `MAZE` is kept as it is because `vmaze` and the Werdna route are built on its timing.

## Controls
Every screen prints its keys: one letter per choice, `[RETURN]` where the text says so. Letters arrive as
capitals. Names (characters, spells, traps) are typed and ended with Return.
| Context | Key | Action | Status |
|---|---|---|---|
| Title | any key | to the menu (after the write-protect check, see Boot) | verified |
| Menu | `s` / `u` / `t` | start game / utilities / title page | verified |
| Disk prompts | `enter` | "... IN DRV 1, PRESS [RET]" | verified |
| Castle | `a` `g` `b` `c` `e` | A)dventurer's Inn, G)ilgamesh' Tavern, B)oltac's Trading Post, Temple of C)ant, E)dge of Town | all verified |
| Tavern | `a` + name + Return + password (Return for none); `r`; digit; Return | add a member by typing the name ("WHO WILL JOIN ? >", then "ENTER PASSWORD >" even when there is none); remove ("WHO WILL LEAVE ([RETURN] EXITS) >"); see a member; leave | a, digit, Return verified; r: prompt verified |
| Inn | digit ("WHO WILL STAY"), then `a`-`e`, Return | stables (free), cots 10, economy 50, merchant 200, royal 500 GP/week; ends with "YOU NEED n MORE EXPERIENCE POINTS TO MAKE LEVEL" or the level-up lines; "PRESS [RETURN] TO LEAVE" | b verified |
| Temple | name + Return | "WHO ARE YOU HELPING ? >" (a typed name, not a list); then "THE DONATION WILL BE n", "WHO WILL TITHE" | first prompt verified |
| Boltac's | digit ("WHO WILL ENTER"), then `b` `s` `u` `i` `l` | buy, sell, uncurse, identify, leave; in the stock `p` purchase ("PURCHASE WHICH ITEM ([RETURN] EXITS) ? >"), `f` forward, `b` back, `s` start, `l` leave; six items per page | b verified, the rest from the screen text |
| Edge of Town | `m` `t` `c` `l` | Maze (only with a party), Training Grounds, Castle, Leave game (writes the roster; "PRESS [RETURN] FOR MORE WIZARDRY") | all verified |
| Training Grounds | name + Return; `*ROSTER` + Return; Return | a new name: "THAT CHARACTER DOES NOT EXIST. DO YOU WANT TO CREATE IT (Y/N) ?"; a known name: "PASSWORD >" (Return for none; a wrong one goes back silently), then I)nspect, D)elete, R)eroll, C)hange class, S)et new password, Return; `*ROSTER` lists the names in use (L)eave); Return alone goes to the Castle | create, delete, inspect, change class (prompt), roster verified |
| Creation | Return twice; `a`-`e`; `a`-`c`; `shift+equals` (+), `minus`, Return, `esc`; class letter; `y`/`n` | password and its repeat (Return for none); race (Human, Elf, Dwarf, Gnome, Hobbit); alignment (Good, Neutral, Evil); bonus points: + and - change the marked score, Return goes to the next score (wraps), Esc goes on when all points are used; the classes the scores allow are listed beside them as they change (A) FIGHTER ...); "KEEP THIS CHARACTER (Y/N)? >" | all verified except `minus` |
| Camp | digit; `r`; `e`; `d`; `l` | inspect; reorder ("REORDERING 1>>": digits); equip (everyone, slot by slot: "SELECT WEAPON FOR RYZ ... WHICH ONE ([RET] FOR NONE) ? >", only slots with a usable item are asked); disband ("CONFIRM (Y/N) ?": leaves the characters in the maze, marked OUT); leave | digit, r (prompt), e, d (prompt), l verified |
| Character sheet | `e` `d` `t` `r` `s` `u` `i` `l` | equip, drop, trade, read spell books (`m`/`p`, `l`), cast spell ("WHAT SPELL ? >" + name; camp only), use item, identify (bishop), leave. In the Tavern/Training only the entries that apply are listed | e, r, s, l verified |
| Maze | `f` or `w` / `l` or `a` / `r` or `d` | forward / turn left / turn right ("OUCH!" in the view when walking into a wall) | verified |
| | `k` | kick: through the door ahead | verified (Werdna's door) |
| | `c` | camp | verified |
| | `s` | status: redraws the party window | key accepted, no change seen |
| | `q` | quick plot on/off | key accepted, no change seen in a still |
| | `t` | "NEW DELAY (1-5000) >": the pause after messages | prompt verified |
| | `i` | inspect: search for bodies ("FOUND: ** NO ONE **  OPTIONS: L)EAVE") | verified |
| Prompts | `y` / `n`; Return | stairs ("STAIRS GOING UP. TAKE THEM (Y/N) ?"); "[RET] FOR MORE" on long messages; elevator buttons `a`-`d` / `a`-`f` or Return | verified (stairs, plaque, elevator prompt) |
| Malor (camp spell) | `n` `s` `e` `w` `u` `d`, Return, `esc` | one square or floor per key press, Return teleports, Esc "chickens out" | verified (17 W, 3 S, 9 U) |
| Battle | `f` `s` `p` `r` `u` (`d` dispell for priests) | fight ("FIGHT AGAINST GROUP# ?" when there are several groups), spell ("SPELL NAME ? >" + name + Return, then "CAST SPELL ON GROUP #?" / "PERSON # ?"), parry, run, use; then "PRESS [RETURN] TO FIGHT, OR GO B)ACK TO REDO OPTIONS" | f, s, p, Return verified |
| Friendly monsters | `f` / `l` | "A FRIENDLY GROUP OF ... THEY HAIL YOU IN WELCOME! YOU MAY F)IGHT OR L)EAVE IN PEACE." | screen verified (Werdna himself, `@werdna_sign,enter,w300,r,w300,w17,k,w600,w1500`) |
| Chest | `o` `c` `l` `i` `d` | open, Calfo, leave, inspect, disarm; "WHO (#) WILL ...?", disarm then "WHAT TRAP >" + name | menu verified; o and l return to the maze |

Input timing: the default press (hold 8, wait 40) works everywhere, and one key at a time (keyboard latch):
wait for the screen, then type. Waits that worked: Castle menus `w300`, a typed name `type:NAME\n,w300`, the
password Return `w400`, creation steps `w300` (`w60` between + and Return), entering the maze `w600` (first
time) / `w1200`, a maze step or turn `w20` (tested 20-120), a stairs change `w600`, battle orders `w150`, a
battle round `w2500`-`w3000`. `type:` works for names. Keys pressed while the disk is busy are lost.

## Game structure
- **Castle** (verified menus): Tavern (party), Inn (rest, level up), Temple (cures), Boltac's (shop), Edge of
  Town (Maze, Training Grounds, Castle, Leave game). Utilities are on the boot menu, not in the Edge of Town.
- **Roster** (disk data): 20 slots, see "The dump". After `WIPE` and `PARTYMAKE` the six are slots 0-5.
- **Maze** (disk data, `design/maps/floors.txt`, rebuilt with `python3 games/apple2/wizardry/tools/maps.py
  --out ...`): ten floors of 20 x 20, x east, y north, (0,0) south-west. **The floors are the DOS port's**,
  wall for wall and special square for special square, with one difference: the floor 2 elevator-type square is
  at (10,9) here, (10,8) on DOS. The DOS playbook's and design documents' coordinates apply.
- **Messages** differ in wording from DOS (floor 2 (14,11): "A PLACARD NEAR THE GROUND READS: "WHEN IT'S NOT
  LIT..."" - verified; Werdna's sign: ""LAIR OF THE EVIL WIZARD WERDNA" THE WIZARD IS **IN**" - verified).
- **Ending** (verified): reaching the Castle with Werdna's amulet (item 94) in a pack: "*** CONGRATULATIONS ***
  YOU HAVE COMPLETED YOUR QUEST AND THE AMULET IS NOW BACK IN THE HANDS OF YOUR BENIFICENT RULER, TREBOR. ...
  BOON OF 250,000 EXPERIENCE POINTS EACH! ... CHEVRON (>) OF THIS RANK EVERMORE. HOWEVER, YOU MUST GIVE UP ALL
  YOUR EQUIPMENT AND MOST OF YOUR MONEY TO PAY FOR YOUR INITIATION. PRESS [RETURN], HONORED ONES". Afterwards
  the sheet reads `RYZ ">" HUMAN G-FIGHTER`, the packs are empty and gold is cut to its last four digits
  (24,817 -> 4,817). DOS: 50,000 G.P. and E.P., equipment kept.
- **Game over** (program text, not seen): "YOUR ENTIRE PARTY HAS BEEN SLAUGHTERED - PRESS RETURN TO LEAVE THE
  CEMETERY"; Malor into rock: "YOU LANDED IN SOLID ROCK ... LOST FOREVER!", into the air above the castle:
  "YOU MATERIALIZED IN MID-AIR AND FELL TO A PAINFUL DEATH!", "YOU APPEARED IN THE CASTLE MOAT".

## The DOS material here (how to carry a DOS route over)
Checked with eight hand-translated routes (2026-11-19): dark square, floor 1 and floor 4 elevators, floor 2
placard, the floor 9 chute and Werdna's plaque, a floor 3 fight room, Werdna's door. No translator script was
written; the rules:
| DOS | Apple II |
|---|---|
| checkpoints `title start edge camp maze1 battle chest vet vmaze werdna_sign werdna ending after_ending resume resume_end gcamp gcastle gmaze gwerdna_sign gwerdna werdna_won final` | same names here (`training` is not a menu here; `gending`, `gafter` = `ending`, `after_ending`: the won fight here is the ungeared veterans') |
| `WARP:FF:XX:YY`, `VET`, `GEARPOKE`, `AMULET`, `HOME`, `EQUIPALL`, `MAZE` | same names and arguments (after `gcastle`: `MAZE2`) |
| position pokes `DA26` x, `DA24` y, `DA20` facing, `DA22` floor | `7330` x, `732E` y, `732A` facing, `732C` floor (words; same values) |
| party record pokes `DCEC + n*D0 + off` (e.g. `DD26` = RYZ's item count, `DDE4` = CONDI's status) | `7390 + n*D0 + off`: subtract `695C` (`73CA`, `7488`); same record layout |
| floor buffer `B646 + off` (the castle-exit poke `B92B`, `B944`, `B960`...) | `5C1A + off`: subtract `5A2C` (not tested here: Malor is the way home) |
| battle groups `D308 + g*F6`, 16-byte monster records, hit points at record +8 | `6E30 + g*124`: words alive, count, then 14-byte records, hit points at record +8 (`6E3C` first monster of group 1) |
| creation pokes `C552`, `C546`, `C36E` | `5BD6` (scores), `5BCA` (rolled values), `5B66` (bonus) |
| maze keys `w a d k c`, `s`, `i` | the same keys work (`f l r` are the printed ones); DOS `o` (hide windows) has no counterpart; `q` and `t` are new |
| waits: step `w60`, menus `w90`-`w150`, floor change `w600` | keep or raise: steps `w20`+, menus `w300`, floor change `w600`, battle round `w2500`+ (DOS routes count `w40` per message: re-time them with `try.py --frames`) |
| Castle `g a t b e` (t = Temple) | `g a c b e` (c = Temple of Cant) |
| Tavern `a` + roster letter | `a` + `type:NAME\n` + `enter` (password) per member: macro `ADD:NAME` |
| Training `c` `i` `r` menu, creation with Up/Down/Enter/Esc | no menu: type the name (`MAKE`, `DEL`); `shift+equals` / `minus`, Return, Esc; `*ROSTER` |
| Edge `u` Utilities | on the boot menu (`@menu,u`) |
| leave a screen with Enter | mostly `l` (camp, sheet, spell books, Boltac's, roster); Return in the Tavern, Inn and at "[RETURN]" prompts |
| Temple: pick by letter | `type:NAME\n` |
| battle `t` take back, Enter to fight | `b` go back, Return to fight; no "take back" inside the orders |
| spell names typed in lower case | type capitals: `type:HALITO\n` |
| random fights: `wK` before the turn in a fight room picks the monsters | the same trick works, with other K (floor 1 (7,1): K = 1 Scruffy men, 3 Orcs + Kobolds, 5 Slimes, 13 Skeletons...); a turn on a fight-room square rolled a fight in 8 of 8 tries on floor 1, 0 of 1 on floor 3 |
Routes that cannot carry over: everything about the DOS loader, `o`, the Training Grounds menu, the 50,000
G.P. reward, items kept after the ending (the DOS `final` party has gear; here it has none).

## Shot plan
Target: the DOS set's coverage (208 shots) replayed here plus what only this version has. Planned ids keep the
DOS ids where the content is the same (`games/dos/wizardry/shots/main/shots.txt`). By category:
- boot/title (6): `boot_prepare` (PREPARE YOURSELF text, `w1100,!`), `title_cauldron` (frame ~1300),
  `title_smoke` (~1700), `title_logo` (`@title`), `menu_copyright` (`@menu`), `menu_utilities` (`@menu,u,w600`).
- menu/system, Castle (about 40): disk prompts (2), castle empty and with party, tavern add / password prompt /
  full party / remove, inn list, inn result, level-up at the inn, temple prompt and a cure (status poke `7488`
  = CONDI dead 5 / ashes 6), Boltac's menu, each stock page (F until it wraps), purchase, sell, identify,
  uncurse (DOS routes with the address rule above), edge of town, leave game ("FOR MORE WIZARDRY").
- Training Grounds (about 15): menu, roster (inherited: `@castle,TRAINING,type:*ROSTER\n`; ours), each creation
  step (name, password, race, alignment, points with the live class list, class, keep), inspect, delete
  confirm, reroll, change class, set password.
- inventory (about 12): sheets of all six classes (veterans with gear: `@gcastle`), mage and priest spell
  books, equip prompts, trade, drop, use, identify by the bishop, DUMAPIC, MALOR's displacement screen.
- gameplay (about 25): one view per floor (`@gmaze,WARP`), doors, darkness, stairs prompts, elevator buttons
  (floors 1 and 4), pit, chute, spinner, teleport, "OUCH!", the signs and messages of every floor (DOS survey:
  one route per special square), camp, reorder, time delay prompt, inspect.
- battle (about 50): encounter start per monster picture (20 pictures on the disk: try `wK` variants on a
  fight square of every floor), orders, group prompt, spell prompt, each message type (swings, spell damage,
  status effects, level drain, dispell, flee, parry), surprised either way, friendly group, victory and E.P.,
  chest menu, each chest command, traps, loot.
- boss (about 12): Werdna's sign, the fight start variants, the won round message by message (`@werdna` +
  the `werdna_won` orders, `try.py --frames`), the lost surprise round (`@werdna_sign,enter,w300,r,w300,k,w600`:
  four dead after Werdna's first spell), friendly Werdna, the amulet in EBO's pack.
- ending (5): Malor screen, stairs with the amulet, Congratulations, the Castle and a sheet with the chevron.
- gameover (2): cemetery (kill the party: status pokes or the lost Werdna round), Malor into rock.
- save/extra (4): utilities entries (change names, transfer prompt), the write-protect loop's black screen is
  not a shot.
How to reach: everything from `@start`, `@vet`, `@gcastle`, `@gmaze` + `WARP`, `@werdna`; nothing needs play.

## Strategy and walkthrough notes
- Cataloguing: never grind. `VET` at the Castle (visible at once on sheets; the Castle list after any menu
  change) makes the party level 13; `WARP` from floor 1 reaches any square; `AMULET` + `HOME` ends the game
  without the fight (checkpoint `ending_poke`).
- **Werdna, the route that wins on screen** (no pokes in the fight; checkpoints `werdna` -> `werdna_won`):
  kick the door with `w1` before `k` (1 UNSEEN ENTITY, 1 W E R D N A, 1 UNSEEN ENTITY, not surprised), orders
  `f,2` `f,2` `s,MALIKTO` `p` `s,TILTOWAIT` `s,LAHALITO,2`, then `w10,enter,w3000`: all three groups die in the
  first round, nobody dies, EBO finds the amulet. Of twelve waits before Return (`w1`..`w12`) only `w10` won
  outright; most others left RYZ stoned or dead with Werdna alive. With no wait before `k` the monsters
  surprise the party and Werdna's first spell kills four.
- **The way home**: DEDDO casts MALOR in camp (`c`, `5`, `s`, `type:MALOR\n`), 17 x `w`, 3 x `s`, 9 x `u`,
  Return: floor 1 (0,0) on the stairs prompt; `y` -> the ending (checkpoints `malor_home`, `ending`).
- Group prompts appear only when there is more than one group; never type a spell name while the spell prompt
  is not open (the letters act as orders).
- The ending takes all items: equip nothing you want to keep on characters who carry the amulet home.

## Naming
Names are typed (`type:RYZ\n`), capitals only. Party made by `PARTYMAKE` with the DOS party's statistics: the
scores are poked on the bonus screen one below the target with 6 bonus points, then real `+` and Return presses
spend them (the class list beside the scores follows).
| Name | Race | Align | Class | STR IQ PIE VIT AGI LUC | HP at L1 (route `start`) | Slot |
|---|---|---|---|---|---|---|
| RYZ | Human | Good | Fighter | 17 8 5 13 10 9 | 9 | 0 |
| CONDI | Dwarf | Good | Fighter | 16 7 10 15 7 6 | 8 | 1 |
| EBO | Gnome | Good | Priest | 9 7 16 10 11 7 | 6 | 2 |
| CUBI | Hobbit | Neutral | Thief | 7 7 7 9 16 15 | 5 | 3 |
| DEDDO | Elf | Good | Mage | 7 17 10 8 11 6 | 3 | 4 |
| MNZ | Elf | Good | Bishop | 7 15 14 7 10 6 | 6 | 5 |
Hit points and starting gold (117-186 seen) are rolled: they follow frame timing (DOS: 8 for everyone).

## Shortcuts
| What | How (tokens / prefix / code) | Source | Status |
|---|---|---|---|
| Past the write-protect check | `poke:845A=00` once the title key has been pressed (`MENU`) | scout (p-code read from memory) | verified |
| Empty roster | `WIPE` (20 x `DEL:NAME`: name, Return for the password, D, Y) | scout | verified |
| Party with chosen statistics | `MAKE` / `PARTYMAKE` | scout (DOS macro, new addresses) | verified |
| Veteran party | `VET` at the Castle: level 13, HP 112 124 71 66 49 58, E.P. 377,512-560,341, gold 5,077-24,817, ages 24-63, all mage spells (DEDDO), all priest spells (EBO), mage 1-4 + priest 1-3 (MNZ) | DOS macro, addresses - `695C` | verified (sheets, spell book, casting) |
| Veterans with gear | `GEARPOKE` at the Castle, then in the first camp `EQUIPALL` (`e` + 18 x `1`): AC -4 -1 3 4 9 7 (checkpoints `gcamp`, `gcastle`, `gmaze`) | DOS macros | verified |
| Warp anywhere (from floor 1) | `WARP:FF:XX:YY` (hex): rewrites floor 1's stairs-down record (special 2 of the floor in play at `5C1A`) to floor FF square (XX,YY), puts the party on (1,10) facing west, turns left and right, steps onto the stairs and answers Y. Arriving on a stairs, sign or elevator square shows its prompt | DOS recipe | verified (floors 1, 2, 3, 4, 9, 10) |
| Werdna's amulet | `AMULET` (item 94 into RYZ's pack: slot 1 must have no items), then `HOME` from floor 1 (0,0) facing north | DOS macros | verified (`ending_poke`) |
| Malor home | see Strategy | game | verified |
| Monster hit points | `6E3C + 14*k + 0x124*g` (word) | dump of two fights | read (slimes 2 3 3, Werdna 87, Vampire Lord 89), not poke-tested |
| Position report in game | DUMAPIC (mage spell, camp) | game | verified |
| Item, monster, roster tables | `python3 games/apple2/wizardry/tools/data.py items|monsters|roster [FILE]` | disk data | item 94 = WERDNA'S AMULET verified in play; monster dice fields are a reading of the record, not checked |
No codes, downloadable saves or debug features were looked for on the web (the DOS scouts found the usual hosts
closed to agents; the disks themselves answered everything needed).

### Saves (`rom/saves/wizardry/`, never committed: whole disk images)
`play.py export` on the Apple II writes a ZIP of the changed disk image (`2 Scenario.dsk`, the whole side:
program, maps and roster). That is game data: every export is moved from `games/apple2/wizardry/saves/` to
`rom/saves/wizardry/` and none is committed (`saves/README.md` keeps the table with routes and SHA-1s). The
committed record is the checkpoint route; rebuild a save with `play.py start apple2/wizardry --route ROUTE`,
`play.py export NAME "..."`, `mv`.
| Name | Contents | Route | SHA-1 (.sav, this build) | Status |
|---|---|---|---|---|
| 01_start | roster RYZ CONDI EBO CUBI DEDDO MNZ, level 1, no equipment; 14 free slots | `@start,e,w300,l,w900` + export | `1515b1cd9b1be035308acad360368725f979c5ff` | verified (`sav:01_start,RESUME` = checkpoint `resume`) |
| 02_ending | the six after the real Werdna fight, Malor and the ending: level 13, chevron, E.P. 631,933-814,762, gold 4,817-9,342, no items | `@final,e,w300,l,w900` + export | `b3d49bc83623739f129213ccc1bb48611f051fd7` | verified (`sav:02_ending,RESUME` = `resume_end`; `data.py roster`) |

### The transfer disk for Wizardry II (`rom/saves/wizardry-2/00_transfer.sav`, never committed)
`python3 games/apple2/wizardry/tools/transfer.py` stores the scenario image of `02_ending.sav`, unchanged, as
`T Wizardry I.dsk` in a new ZIP (fixed date, so the same image gives the same ZIP).
- ZIP SHA-1 `328965cd286e41a74c4e768815924fd09419e549`; image SHA-1 `52c129e55f799fd10b088035d6ef9f1e5ccb224c`
  (143,360 bytes, DOS 3.3 sector order, volume `WSV2.1`).
- On it: the six characters of `02_ending` in slots 0-5 (all OK, in the Castle, not OUT, no passwords, no
  items, chevron), 14 free slots, and the unchanged Wizardry I scenario (maps, monsters, items, program).
- Not tried in Wizardry II (that game's scout): as an extra disk it is `disk:N` with the first number after
  Wizardry II's own disks. Wizardry I's own T)RANSFER utility text says "CHARS MUST BE LIVE & IN CASTLE" and
  "** CHAR HAS NON-XFERRABLE ITEMS **" (program text): both hold for these six.

## RAM map (for `game.json` "ram" watches and pokes)
Addresses in the 64K the program sees (main memory below `C000`); the same on every run of these routes.
Words are little-endian. Local variables live on the Pascal stack: an address marked "stack" is valid only on
the screen named.
| Address | Size | Meaning | How found |
|---|---|---|---|
| `732A` | 2 | facing: 0 N, 1 E, 2 S, 3 W | RAM diff over a turn (verified) |
| `732C` | 2 | floor: 0 castle, 1-10 (65535 seen in the Castle after the ending) | warp (verified) |
| `732E` | 2 | y, 0-19 north | diff over a step + poke (verified) |
| `7330` | 2 | x, 0-19 east | poke + warp (verified) |
| `7390 + n*0xD0` | 208 | party member n (0-5, party order): the character record below; valid in the Castle and the maze | name search, `VET` (verified) |
| `5C1A` | 894 | stack: the floor in play (TMAZE layout, `tools/maps.py`), valid while walking the maze on the first and later entries (checked `vmaze`, `gmaze`); other copies at `5100` (disk buffer) and `7A68` (cache) are not the ones the game reads | match with the disk + warp (verified) |
| `5F1E`, `5F3E`, `5F5E` | 2 each | stack: special 2 of the floor in play (floor 1: the stairs down at (0,10)): AUX0 floor, AUX1 y, AUX2 x (used by `WARP`) | poke + stairs (verified) |
| `5BD6` | 12 | stack, creation: STR IQ PIE VIT AGI LUC (words) | diff over `+` (verified) |
| `5BCA` | 12 | stack, creation: the rolled values (lower limits) | dump (verified by the macro) |
| `5B66` | 2 | stack, creation: bonus points left | diff (verified) |
| `6E30 + g*0x124` | 2+2+14k | battle group g (0-3): alive, count, then 14-byte monster records (hit points at +8); the group's monster definition (158 bytes, names first) at group +0x84 | dumps of two fights (read, not poked) |
| `843C`-`845A` | | SYSTEM.STARTUP's write-protect check while it runs (Boot) | p-code read (verified by the poke) |
| `0058` | 2 | the p-code interpreter's instruction pointer (interpreter code around `9800`) | sampling (used once) |
Character record (208 bytes, the DOS port's layout, re-checked here through `VET`, `AMULET`, `GEARPOKE`, the
roster tool and the sheets):
| Offset | Size | Field |
|---|---|---|
| `+00` / `+10` | 16 / 16 | name / password: length byte + 15 characters |
| `+20` | 2 | OUT (left in the maze) |
| `+22` / `+24` | 2 / 2 | race 1 human 2 elf 3 dwarf 4 gnome 5 hobbit / class 0 fig 1 mag 2 pri 3 thi 4 bis 5 sam 6 lor 7 nin |
| `+26` | 2 | age in weeks |
| `+28` | 2 | status 0 OK 1 afraid 2 asleep 3 paralyzed 4 stoned 5 dead 6 ashes 7 lost (free slot) |
| `+2A` | 2 | alignment 1 good 2 neutral 3 evil |
| `+2C` | 4 | statistics, 5 bits each: STR IQ PIE, then VIT AGI LUC |
| `+34` | 6 | gold: three words 0-9999, low first (the ending keeps only the first) |
| `+3A` / `+3C` | 2 / 64 | items carried / 8 x (equipped, cursed, identified, item number) |
| `+7C` | 6 | E.P., same form |
| `+82` / `+84` | 2 / 2 | highest level / level |
| `+86` / `+88` | 2 / 2 | HP now / max |
| `+8A` | 8 | spells known, bit k = spell k (mage 1-21, priest 22-50) |
| `+92` / `+A0` | 14 / 14 | mage / priest spell points per level |
| `+B0` | 2 | armour class |
| `+CE` | 2 | awards: 1 = chevron (>) |
Disk (block order, `maps.blocks()`): SCENARIO.DATA from block 149; its table of contents gives MAZE at +6
(floor N at byte `13600 + (N-1)*400`), ENEMY +26, REWARD +60, OBJECT +68, CHAR +84 (roster at byte `1D200`,
slot n at `1D200 + (n div 4)*400 + (n mod 4)*D0`), EXP +114.

## Emulation notes
- **Model `iiplus`.** On `iie` (the tools' default) Apple Pascal 1.1 finds the 80-column firmware and switches
  it on: all text shows in 80-column mode with every second column empty ("P R E P A R E"). The II Plus is the
  machine of 1981 and shows 40 columns. Video is the default colour TV: text is white, the maze window's lines
  purple and its text green (hi-res artifact colours), monster pictures in colour.
- **Write protection (backend gap).** See Boot: the title's check needs a write-protected boot disk and the
  backend cannot offer one; routes poke past it. Reproduction: `python3 tools/emu.py apple2/wizardry --seq
  "w2100,space,w3000" --out work/x` stays black; with `poke:845A=00` after the key the menu appears. The
  Tavern's "** WRITE-PROTECT CHEAT! **" (program text) is the opposite check on the scenario disk: not met.
- Text screens (Castle, Training, camp, sheets, shops) are text page 1: `python3
  games/apple2/wizardry/tools/screen.py --name SESSION ["tokens"]` prints them, `tools/try.py FILE --text`
  prints the end screen of many routes run in parallel. The maze, fights and chests are hi-res: look at frames.
- Text screens with a prompt never settle (blinking cursor): `settle` runs its 300 frames. The checkpoint
  routes contain those settles; the fights' outcomes depend on them. Do not edit a macro a checkpoint uses
  (`MAZE2` was added instead of changing `MAZE`).
- RNG follows frame timing: `wK` before the deciding key picks encounters, surprise, and how a round goes.
- A maze entry after the first in a session: `MAZE2`. A key during a disk load is lost without a trace.
- Stack addresses (floor buffer, creation) were the same on every screen entry tried, including the second
  maze entry.
- Pokes to the party records show at once on a sheet; the Castle list redraws on a menu change.

## Checkpoints
| Name | What |
|---|---|
| `title`, `menu`, `castle` | title logo; boot menu; Castle without a party (inherited roster) |
| `start` | Castle, party of six formed, level 1 |
| `edge`, `camp`, `maze1` | Edge of Town; first camp; floor 1 (0,0) facing north |
| `battle`, `chest` | floor 1 (7,1): 3 Slimes; the chest after one round |
| `vet`, `vmaze` | Castle and floor 1 entrance with the veterans |
| `werdna_sign`, `werdna` | floor 10 (17,4) sign; the fight's first orders (veterans, no gear) |
| `werdna_won`, `malor_home`, `ending`, `after_ending`, `final` | the real win; Malor to the stairs; Congratulations; Castle; Castle after a look at RYZ's sheet |
| `ending_poke` | Congratulations by `AMULET` + `HOME` |
| `gcamp`, `gcastle`, `gmaze`, `gwerdna_sign`, `gwerdna` | the veterans with gear: camp, Castle, floor 1, Werdna's sign and fight (Werdna, Vampire Lord, unseen entity; not fought) |
| `resume`, `resume_end` | Castle from `sav:01_start` / `sav:02_ending` (need the files in `rom/saves/wizardry/`) |
Cold check: `python3 games/apple2/wizardry/tools/cachecheck.py` builds every checkpoint from an empty cache and
compares it with a cache hit in a fresh process (frame, memory 0000-BFFF, written disk). Run 2026-11-19:
all 26 checkpoints identical cold, from the cache and against the states of the session that made them
(frames and memory for all; the written disk as well for `start`, `final` and the five `g...` ones).

## Sources
| Source | URL | Used for | Accessed |
|---|---|---|---|
| the disks | `rom/wizardry.zip` | program text (every prompt and message), version, roster, maps, items, monsters, the write-protect check | 2026-11-19 |
| DOS playbook and design documents | `games/dos/wizardry/` | structure, macros, record layout, routes; each fact used here was re-checked on the Apple II or is marked | 2026-11-19 |
| Apple II Might and Magic playbook | `games/apple2/might-and-magic/playbook.md` | how a DOS set was replayed on the Apple II | 2026-11-19 |
No web source was fetched (time went to the emulator; the DOS scout lists the hosts and what they refused).
The manual was not read: the bonus-point keys and all prompts come from the screens.

## Open questions
- Battle hit-point pokes are untested; the monster table's dice fields (`data.py monsters`) are unchecked.
- `s` (status) and `q` (quick plot) in the maze showed no change in a still frame: what they do in motion.
- Temple, Inn level-up, Boltac's purchase/sell/identify/uncurse, trade, drop, use, chest open/disarm/Calfo:
  prompts seen or read in the program, the full flows are the capture's.
- Whether the floor 2 elevator-type square at (10,9) does anything (DOS has it at (10,8)).
- U)TILITIES entries (backup, recover, transfer, update, change names): menu only.
- The fight with the geared veterans (`gwerdna`) was not played; only the ungeared win is recorded.
- Murphy's ghost and the keys of floor 1 (DOS: never triggered): one translated try walked into a wall.
- Wizardry II's import of `00_transfer.sav` is untested.
