# Might and Magic Book One: The Secret of the Inner Sanctum (DOS) - playbook

Everything an agent needs to play this game efficiently: read it before playing, add to it after every run.
Status of each fact: **verified** (seen in the emulator, with the route) or **source** (manual/FAQ/wiki, not yet
checked). Never delete a fact that turned out wrong: strike it and say what is true.

## Identity
| Field | Value |
|---|---|
| Title (EN / original) | Might and Magic Book One: Secret of the Inner Sanctum (title pictures "Might and Magic" and "Book One - Secret of the Inner Sanctum"; options menu "MIGHT AND MAGIC / SECRET OF THE INNER SANCTUM", "COPR. 1986,1987-JON VAN CANEGHEM") (verified) |
| Platform / model used | IBM PC / MS-DOS, `svga-1500` (`game.json`); the game draws 320x200 in four-colour CGA style |
| Release (region, year) | Apple II 1986, MS-DOS port 1987 (Wikipedia); this dump is the owner's GOG folder (manual "SECOND EDITION", (c)1987) |
| Developer / publisher | New World Computing (design and programming Jon Van Caneghem: manual credits) |
| Genre | First-person party RPG ("a fantasy role-playing simulation"), 16x16-square maps, text-menu combat |
| Players / save system | 1 player; party of 1-6 from a roster of up to 18 characters; **save = sign in at an inn**, which writes `ROSTER.DTA` (2,304 bytes = 18 records of 127 bytes + 18 more bytes); no other save, no passwords (verified) |

## Boot sequence
Macros (all in `game.json`): `BOOT`, `TITLE` = `BOOT,w900`, `MENU` = `TITLE,esc,w90,enter,w200`, `TOWN:n` (stock party),
`RYZ`, `RENAME:letter:name`, `NAMES`, `JOIN`, `PARTY` (see Naming), `AT` / `FN FE FS FW` (move, see Shortcuts), `QA`.
Checkpoints `title`, `menu`, `start`: rebuilt from an empty cache 2026-11-18, frames identical to cache hits.
- Intake probe: `work/intake/dos/might-and-magic/sheet.png` (frame every 60 frames, no input).
- **verified 2026-11-18** DOSBox Pure's start menu lists GRAPHSET.EXE, MM.EXE, unins000.exe: `BOOT` =
  `w120,down,enter,w300` runs MM.EXE and ends on the animated title (320x200, 4 colours).
- **verified** The title needs about 10 s before it shows "'ESC' TO START GAME / 'SPACE' FOR SCENES". Space (or
  any other key) steps through a slideshow of demo scenes that look like gameplay (party list, COMMANDS panel)
  but are pictures. ESC -> "ARE YOU READY? THEN PRESS ENTER!" -> Enter -> options menu (`C` create characters,
  `V` view all characters, `#` go to town 1-5). `MENU` = `BOOT,w900,esc,w90,enter,w200`.
- **verified** Keys typed too early stay in the keyboard buffer and are used by the next screen: wait for a
  screen before typing for it.
- **verified** Town number -> the inn's character list (the roster ships with six characters: Crag the Hack,
  Sir Galand, Zenon III, Swifty Sarg, Serena, Wizz Bane). Ctrl+A..F adds or removes a character, X leaves the
  inn into the town. `TOWN:1` = menu, town 1 (Sorpigal), all six added, exit: first control, facing a corridor.
- **verified** In town: arrow keys move and turn, `1`-`6` open a character sheet, ESC goes back. The other
  commands are listed on screen (O order, P protect, R rest, S search, B bash, U unlock, Q quick reference).
- Model `svga-1500`: 1500 cycles is the value in GOG's own DOSBox configuration for this game.
- **verified 2026-11-18** Saving: the inn door is the square behind the start position (from `@sorpigal`:
  `down`, turn around with `left,left`, `up,up`; the sign reads "THE INN OF SORPIGAL"). Stepping in asks "WOULD
  YOU LIKE TO SIGN IN (Y/N)?"; `y` writes ROSTER.DTA and returns to the inn's character list, ESC from there is
  the options menu. Checkpoint `after_save`, save `saves/01_signed_in.sav`; `sav:01_signed_in` powers on with it.
  Savestates and checkpoints carry the written file (see "Saves" in `docs/emulator/dos.md`).
- **verified** On a character sheet `R` + slot number unequips an item into the backpack; `D` discards only
  from the backpack.

## Controls
Every screen prints its own keys; all input is single keystrokes (no Enter needed except after names and numbers).
| Context | Key | Action | Status |
|---|---|---|---|
| Title | `esc` | "ARE YOU READY? THEN PRESS ENTER!" | verified |
| | `space` | next demo picture (slideshow) | verified |
| Options menu | `c` / `v` / `1`-`5` | create characters / view all characters / go to town n | verified |
| Create | `enter` | re-roll the seven statistics | verified |
| | `1`-`6` | class (only the eligible ones are listed), then race `1`-`5`, alignment `1`-`3`, sex `1`-`2` | verified |
| | letters, `enter` | name (up to 15 characters, shown in capitals), then `y`/`n` "SAVE CHARACTER (Y/N)?" | verified |
| | `esc` | "start over" (back to the roll); from the roll, back to the menu | verified |
| View all / inn list | `a`-`r` | character profile | verified |
| Profile (from the menu) | `ctrl>n` / `ctrl>d` | re-name (type, `enter`) / delete ("ARE YOU SURE") | rename verified, delete source (manual) |
| Inn list | `ctrl>a`.. | add/remove that character (an `@` marks members; marching order = order added) | verified |
| | `x` | exit the inn into the town (needs 1+ member) | verified |
| | `esc` | back to the options menu (party disbanded) | verified |
| Exploration | `up` (or `enter`) / `down` (or `/`) | step forward / back | `up`, `down` verified; `enter`, `/` source (manual) |
| | `left` / `right` | turn 90 degrees | verified |
| | `o` | order: type the six old positions in their new order (`esc` aborts) | prompt verified |
| | `p` | protect: active party spells | verified |
| | `r` | rest (uses 1 food each, restores HP/SP) | prompt verified, resting source |
| | `s` | search the square (after a fight: treasure) | verified ("SEARCH: NOTHING") |
| | `b` | bash a locked door | verified (gas trap, door gave way: `bash_trap`) |
| | `u`, then `1`-`6` | unlock: that character picks the lock (Robber) | verified (CUBI, Sorpigal (3,7) south door) |
| | `q` | quick reference: HP, SP, AC, food, condition of all six; `1`-`6` opens a profile | verified |
| | `1`-`6` | character profile | verified |
| | `v` | sound on/off (not on the list) | source (manual) |
| Profile (in play) | `c` cast (level, number), `d` discard, `e` equip (`a`-`f`), `g` gather, `r` remove (`1`-`6`), `s` share, `t` trade, `u` use, `q` quick ref, `esc` | all verified (round 2) |
| Prompts (shops, stairs, statues, inn) | `y` / `n` | answer | verified |
| Shop menus | `a`-`f` | pick the entry / buy that item | verified (blacksmith) |
| | `g` / `1`-`6` / `esc` | gather the party's gold on the shopper / other character / back | listed on screen, not pressed |
| Encounter | `a` attack, `b` bribe, `r` retreat, `s` surrender | (only when the party is not surprised) | all verified; bribe accepted once, surrender never |
| Combat | `a` | attack monster A | source (manual); listed on screen |
| | `ctrl>a` | quick fight: attack / shoot / block, whichever applies | verified (macro `QA`) |
| | `f` fight (pick the monster), `s` shoot (no target prompt), `b` block, `e` exchange places, `r` retreat, `u` use | | all pressed (round 2); block and retreat print nothing |
| | `c`, level digit, number digit, target letter | cast a combat spell | verified (MNZ: `c,1,4,a` Flame Arrow) |
| | `d` + `0`-`9` | message delay (5 default) | source (manual) |
| | `p`, `q`, `1`-`6` | protect, quick ref, profile (do not use the turn) | listed on screen |

Input timing: the default press works everywhere. The game reads the BIOS keyboard buffer, so nothing is lost,
but **a key typed early is kept for the next screen**: always wait first. Waits that worked at 1500 cycles:
step or turn `w80` (`w60` is enough for turns), opening a list/profile `w100`-`w150`, a shop or event prompt
`w150`-`w250`, town or roster loading `w150`-`w200`, taking stairs or an exit `w400`. Combat messages last about
100 frames at delay 5 and then vanish: sample them (`play.py sample "w10" 12`) or raise the delay.

## Game structure
- **Options menu** (verified): `C` create new characters, `V` view all characters, `#` go to town (1 Sorpigal,
  2 Portsmith, 3 Algary, 4 Dusk, 5 Erliquin: manual). New and stock characters all start in town 1; a character
  is found at the inn of the town where it last signed in.
- **Character creation** (verified): seven statistics rolled 3-18 (Intellect, Might, Personality, Endurance,
  Speed, Accuracy, Luck); eligible classes listed (seen over ~25 rolls: Knight needs Might 12+, Cleric
  Personality 12+, Sorcerer Intellect 12+, Archer Intellect and Accuracy 12+, Paladin Might, Personality and
  Endurance 12+, Robber always: inferred, limits not probed exactly); race Human, Elf, Dwarf, Gnome, Half-Orc
  (changes statistics); alignment Good, Neut, Evil; sex; name; save. A new character has level 1, age 18, 0 gold,
  10 food, a Club in the backpack. Stock characters have 60 experience, 18 food, equipped gear.
- **Town** = one 16x16 map of corridors and doors (verified, Sorpigal). Services are event squares that fire when
  the party stands on the square facing a given way; a sign ("A SIGN ABOVE THE DOOR READS:") is its own event
  one square before. Sorpigal, x east, y north, (0,0) south-west (all verified with `tools/scan.py`):
  | Square, facing | What |
  |---|---|
  | (8,3) S | The Inn of Sorpigal: "WOULD YOU LIKE TO SIGN IN (Y/N)?" (start square; party starts facing N) |
  | (6,5) W | B and B Blacksmiths: A buy weapons, B buy armor, C buy misc, D sell item |
  | (10,5) E | Eulards Fine Foods (market): "ALL YOU CAN EAT! 5 GP/EA WILL YOU PAY (Y/N)?" |
  | (4,1) N | Temple Moonshadow: A restore health, B uncurse items, C restore align, D make donation 100 |
  | (13,11) N | Otto's Training (Worg the guildmaster): "TRAINING FOR LEVEL 2, NEED 1500 MORE EXPERIENCE POINTS" / "COST 25 GOLD, A) COMMENCE TRAINING" |
  | (11,14) E | Ye Olde Hogge Tavern: A have a drink, B tip bartender, C listen for rumors |
  | (11,3) W | leprechaun: travel to a town 1-5 for 1 gem |
  | (14,0) W | stairs going down (a dark dungeon level: "DARKNESS" without light) |
  | (12,0) S | passage outside (outdoors: mountains and forest) |
  | (6,10) N | sign "JAIL, KEEP OUT!" |
  | (7,1) N, (0,2) W, (0,4) W, (2,4) E, (0,6) W, (0,9) S, (10,12) E, (14,14) W | statues ("SEARCH IT (Y/N)?": a line of lore each) |
  | (3,6), entered from (3,7) through a locked door | a fixed encounter (Poltergeists or Vampire Bats seen) |
- **Maps**: `MAZEDATA.DTA` holds 55 maps of 512 bytes (256 wall bytes + 256 property bytes), the same layout
  as the NES port documents: wall byte `N<<6 | E<<4 | S<<2 | W` (0 open, 1 wall, 2 door, 3 special), square
  index `y*16+x` (verified for Sorpigal against RAM and the 3-D view). Property bit 80 marks squares with an
  event or a fixed encounter (Sorpigal: every listed event square has it; (3,6) has it without an event entry
  and holds a fight). Each area has an `.OVR` file (8086 code + data: event squares, facing masks, texts).
  `python3 games/dos/might-and-magic/tools/maps.py rom/might-and-magic.zip 0` prints a text map with event
  squares. The map order in the file is assumed to be towns, CAVE1-9, AREAA1-E4, then castles and dungeons
  (index 0 = Sorpigal verified; the rest inferred, not checked).
- **World** (source: manual + NES port, not checked on DOS): five towns, each with caverns below; 20 outdoor
  sectors A1-E4 of the land of VARN; castles (Doom, Blackridge North/South, White Wolf, Alamar), dungeons
  (Quivering Forest, Raven's Wood, Enchanted Forest, Dragadune, the Demon's stronghold), a four-level "PP" area
  (NES: City of Gold) and the Astral Plane. The area files in the ZIP have these names: ALAMAR, ALGARY, AREAA1-E4,
  ASTRAL, BLACKRN, BLACKRS, CAVE1-9, DEMON, DOOM, DRAGAD, DUSK, ENF1-2, ERLIQUIN, PORTSMIT, PP1-4, QVL1-2, RWL1-2,
  SORPIGAL, UDRAG1-3, WHITEW (verified: file list).
- **Encounters** (verified): either the party is surprised (straight into combat) or an encounter screen shows
  the monster's picture, the list of monsters and Attack / Bribe / Retreat / Surrender. Combat is a text screen:
  round number, the 2x3 party formation (`+` = can fight hand to hand), monster list A.. with "(WOUNDED)",
  handicap line ("MONSTER +3" / "PARTY +4"), then per character "OPTIONS FOR: name". Victory: "FOR DEFEATING THE
  MONSTERS EACH SURVIVOR RECEIVES 75 EXPERIENCE POINTS." Search afterwards for treasure.
- **Magic**: 47 Cleric + 47 Sorcerer spells in 7 levels, cast by level and number (manual Appendix B; the full
  list with costs is in `work/scout/dos/might-and-magic/manual.txt` after extracting the manual, lines 811-1445).
  Level 1 Sorcerer: 1 Awaken, 2 Detect Magic, 3 Energy Blast, 4 Flame Arrow, 5 Leather Skin, 6 Light, 7 Location,
  8 Sleep. Level 1 Cleric: 1 Awaken, 2 Bless, 3 Blind, 4 First Aid, 5 Light, 6 Power Cure, 7 Protection from Fear,
  8 Turn Undead (source; Flame Arrow verified).
- **Levels**: experience from fights and quests, then pay for training in a town (verified: level 2 at 1500
  experience for a Knight, 25 gold; level 3 at 3000; level 8 at 96000, so doubling). New spell levels every other level (manual).

## Shot plan
The plan and the record is `shots.txt` (113 routed lines, all captured and verified 2026-11-18; open targets as
comments at its end). Done: [x] title and demo scenes, [x] menus and roster, [x] creation steps, [x] all
Sorpigal services, [x] exploration commands (order, protect, rest, unlock, cast, location), [x] combat from the
encounter options to victory, spell, shooting, search, [x] level-up, [x] death and game over, [x] lit cavern
with its events and monsters, [x] wilderness (C2, A1, E1), [x] towns 2-5, [x] castles Alamar, Doom, White Wolf,
[x] Quivering Forest, [x] Astral Plane and the ending text. Round 2 (250 shots): [x] bash, unlock results, traps, [x] trade, share, gather, discard, use, remove, equip refused, [x] temple cure, donation, raise price,
[x] tavern drink and rumor, market, training refused, selling, [x] all statues, trap door, leprechaun trip, [x] combat orders and spells, conditions,
[x] 30 more groups incl. Demon Lord, Lich, Dark Rider, dragons, [x] every terrain and wall look, [x] all 55 areas surveyed.
Open: [ ] a surprised party, [ ] Search finding treasure, [ ] rest interrupted, [ ] accepted surrender, [ ] item used in combat, [ ] the impostor.
Distinctive for this version: the text-and-wireframe look in four colours, creation by re-rolling, everything
driven by letter keys, the encounter options (bribe, surrender), handicap line.

## Strategy and walkthrough notes
- Use `@start` (custom party, nothing bought), `@equipped` (RYZ with sword and armor, 1833 gold) or `@combat`.
- **Moving around a town is one token**: `AT:xx:yy:oo,Fd,left,w250` puts the party on a square and fires its
  event (see Shortcuts). `python3 games/dos/might-and-magic/tools/scan.py AREA @checkpoint` visits every event
  square of the area the party is in and tiles the results (24 squares in ~20 s): run it first in every new area.
- **Fights**: the fixed encounter at Sorpigal (3,6) (`@combat`); elsewhere squares with property bit 80 and no
  event entry (`maps.py` prints them as `.`). The monsters depend on timing (Poltergeists with one route, Vampire
  Bats with another). `QA*6` blocks finish a level-1 fight; level-1 characters lose 1-5 HP per hit.
- **Money, levels, HP**: poke the party records (RAM map). Level-up: set experience, go to training, `a`.
  Verified: `@equipped,set:16853=1685:4,AT:0D:0B:BD,FE,left,w250,y,w300` -> "COST 25 GOLD / A) COMMENCE TRAINING".
- **Death / game over**: not tried. Suggested: in `@combat` set every member's HP (record +33) to 1 and block.
- **Dark areas** need Light (Sorcerer 1-6 / Cleric 1-5, 1 SP) or a Torch (blacksmith misc, 2 gold) (manual; the
  dungeon below Sorpigal shows "DARKNESS" instead of the view: verified).
- **Other towns**: `TOWN:n`-style entry only works when characters are lodged there. Fastest: poke gems on a
  character (record +31) and use the leprechaun at Sorpigal (11,3), then sign in at that town's inn (not tried).
- Main quest (Wikipedia, not checked): find the Inner Sanctum; unmask Sheltem, who poses as King Alamar; the
  ending leads through the Gates to Another World. The NES port's route (Eye of Goros to Castle Alamar, Soul
  Maze, Astral Plane) is in `games/nes/might-and-magic/playbook.md`: source (NES port), not checked on DOS.

## Naming
Main character **RYZ**, then CONDI, EBO, CUBI, DEDDO, MNZ (the game shows names in capitals).
- `RYZ` (from the options menu) = create: five re-rolls (`enter,w60` x5) give Intellect 16, Might 15,
  Personality 7, Endurance 17, Speed 14, Accuracy 8, Luck 11 when run right after `MENU` from power-on; Knight,
  Human, Good, Male, `type:ryz`, save, back to the menu (verified as one `do` from power-on). The rolls follow
  frame timing: any change before it changes the statistics.
- `NAMES` = view all, `RENAME:b:condi` (Sir Galand, Dwarf Paladin), `RENAME:c:ebo` (Zenon III, Half-Orc Archer),
  `RENAME:d:cubi` (Swifty Sarg, Gnome Robber), `RENAME:e:deddo` (Serena, Human Cleric), `RENAME:f:mnz` (Wizz Bane,
  Elf Sorcerer). Crag the Hack (slot A) stays at the inn.
- `JOIN` = town 1, add G, B, C, D, E, F (RYZ first), exit. `PARTY` = `MENU,RYZ,NAMES,JOIN` (checkpoint `created`).
- **`start` uses the saved roster instead** (`pow,sav:02_ryz_party,MENU,JOIN`), because a state built on the
  creation route gains one more RYZ in the roster every time it is loaded from the cache (see Emulation notes).
  Creation shots: play `RYZ` from `@menu` and capture before the save prompt is answered, or answer it and do
  not build further checkpoints on that route.

## Shortcuts
| What | How (tokens / prefix / code) | Source | Status |
|---|---|---|---|
| Saved custom party | route prefix `sav:02_ryz_party` (roster with RYZ + renamed stock characters) | made here | verified |
| Stock party in Sorpigal | `TOWN:1` / `@sorpigal` | made here | verified |
| Move inside the current map | `AT:xx:yy:oo` (hex x, y and `oo` = y*16+x), then a facing macro `FN` `FE` `FS` `FW`, then a turn or step to redraw. To fire an event that needs facing D: set the facing one turn clockwise of D and press `left` (`AT:08:03:38,FW,left,w150` = inn prompt) | RAM | verified (Sorpigal: 24 squares) |
| Gold | `set:16865=1873:3` (RYZ; other members +7F each) | RAM | verified (profile and shop show it) |
| Experience / level-up | `set:16853=1685:4`, then training | RAM | verified |
| Fast fights | `QA` = `ctrl>a,w200` (game's own quick-fight key) | manual | verified |
| Leave a town | Sorpigal (12,0) facing S, `y` | scan | verified (outdoor view) |
| Change area (any of the 55) | `WARP:xx:yy:lo:hi:ss` **from anywhere in Sorpigal**: rewrites the operands of Sorpigal's own "passage outside" event (x, y, map id low, map id high, section) and takes that exit, so the game's map loader does the change. Ids and sections: table "Areas" below. Example `WARP:01:0C:03:0C:01` = Portsmith (1,12) | code of SORPIGAL.OVR | verified (17 areas) |
| Light | `CAST:6:1:6` (MNZ casts Light; `CAST:member:level:number`). Needed in caverns and, after a WARP, in sectors A-1 and E-1 and the castles (they showed DARKNESS without it) | manual | verified |
| Event squares of an area | `python3 games/dos/might-and-magic/tools/scan.py N "@equipped,CAST:6:1:6,WARP:..."` -> `work/scout/dos/might-and-magic/scan_N.png` | tools | verified (0-5, 14, 23, 30, 34, 37, 43, 44, 49, 50, 54) |
| Whole party at 1 HP | `LOWHP` (then `BLK*24` in `@combat` = game over) | RAM | verified |
| Ending | `@astral` (Astral Plane, `WORTHY` = every member's record +7D set to 5F: bit 40 "impostor defeated", bits 1F projectors), then `AT:06:07:76,FN,left,w300` | code of ASTRAL.OVR | verified |
| Combat spell / to victory | `FLAME` (attack, MNZ casts Flame Arrow at A); `@combat,FLAME,w240,QA*14` = victory screen | play | verified |
| Debug features, cheat codes | none found (manual has none; TCRF and StrategyWiki refused the fetch) | - | - |

### Areas (map loader table in the program, verified 2026-11-18)
The loader takes a 16-bit map id and a section; it searches the id table from the section's first entry
(section 0 or 1: entry 0; section 2: entry 14; section 3: entry 34), so the same id can name different maps.
Entry number = map number in `MAZEDATA.DTA` = `maps.py`/`scan.py` index (the order the scout assumed is right).
`WARP` wants low byte, high byte, section.
| # | Area | id | sec | # | Area | id | sec | # | Area | id | sec |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | Sorpigal | 0604 | 1 | 19 | B2 | 0703 | 2 | 38 | QVL2 | 0703 | 3 |
| 1 | Portsmith | 0C03 | 1 | 20 | B3 | 0101 | 2 | 39 | RWL1 | 0F02 | 3 |
| 2 | Algary | 0203 | 1 | 21 | B4 | 0D03 | 2 | 40 | RWL2 | 0702 | 3 |
| 3 | Dusk | 0802 | 1 | 22 | C1 | 0304 | 2 | 41 | ENF1 | 0F04 | 3 |
| 4 | Erliquin | 0B1A | 1 | 23 | C2 | 0A11 | 2 | 42 | ENF2 | 0704 | 3 |
| 5 | CAVE1 | 0A11 | 1 | 24 | C3 | 0904 | 2 | 43 | White Wolf | 0A11 | 3 |
| 6 | CAVE2 | 0001 | 1 | 25 | C4 | 0F04 | 2 | 44 | Dragadune | 0107 | 3 |
| 7 | CAVE3 | 0C01 | 1 | 26 | D1 | 0505 | 2 | 45 | UDRAG1 | 0F05 | 3 |
| 8 | CAVE4 | 0202 | 1 | 27 | D2 | 0B05 | 2 | 46 | UDRAG2 | 0A00 | 3 |
| 9 | CAVE5 | 0005 | 1 | 28 | D3 | 0106 | 2 | 47 | UDRAG3 | 0705 | 3 |
| 10 | CAVE6 | 051B | 1 | 29 | D4 | 0801 | 2 | 48 | DEMON | 0412 | 3 |
| 11 | CAVE7 | 0212 | 1 | 30 | E1 | 0112 | 2 | 49 | Alamar | 0B07 | 3 |
| 12 | CAVE8 | 0601 | 1 | 31 | E2 | 0706 | 2 | 50 | PP1 | 0F01 | 3 |
| 13 | CAVE9 | 0A00 | 1 | 32 | E3 | 0B1A | 2 | 51 | PP2 | 0701 | 3 |
| 14 | A1 | 0F01 | 2 | 33 | E4 | 011B | 2 | 52 | PP3 | 0E00 | 3 |
| 15 | A2 | 0502 | 2 | 34 | Doom | 0706 | 3 | 53 | PP4 | 0201 | 3 |
| 16 | A3 | 0B02 | 2 | 35 | Blackridge N | 0F08 | 3 | 54 | Astral | 0B1A | 3 |
| 17 | A4 | 0103 | 2 | 36 | Blackridge S | 0508 | 3 | | | | |
| 18 | B1 | 0A00 | 2 | 37 | QVL1 | 0F03 | 3 | | | | |
The leprechaun's destinations (its own table): Sorpigal (8,5), Portsmith (1,12), Algary (11,13), Dusk (12,8),
Erliquin (4,6), all section 1. Sorpigal's stairs lead to id 0A11 section 1 (CAVE1) at the same x, y; its
passage outside to 0A11 section 2 (C2) at (10,10). A WARP to a square that is not an entrance works, but the
view can be dark (cast Light first) and the party may stand in a wall cell.

### Saves (rom/saves/might-and-magic/, never committed)
None downloaded: GameFAQs/StrategyWiki not reachable; a `ROSTER.DTA` from the web could be zipped as a `.sav`
(see `saves/README.md` for the layout) if the owner finds one. Saves made here are in `saves/`
(`01_signed_in`, `02_ryz_party`).
| Name | Contents (progress, party, items) | URL | SHA-1 | Status |
|---|---|---|---|---|

## RAM map (for `game.json` "ram" watches and pokes)
Physical addresses; valid for this ZIP and model `svga-1500` (the load address depends on both).
| Address | Size | Meaning | How found |
|---|---|---|---|
| 15E68 | 1 | party x (0-15, east) | dump/diff over steps; poke verified |
| 15E69 | 1 | party y (0-15, north) | same |
| 15E6A | 1 | square index y*16+x (poke it together with x and y) | same |
| 15E6C | 1 | wall byte of the current square | read (44 in an east-west corridor) |
| 15E6D-15E70 | 4 | wall masks for forward, left, right, back (N C0, E 30, S 0C, W 03) | diff over turns |
| 15E71-15E74 | 4 | square-index steps for forward, left, right, back (N 10, E 01, S F0, W FF) | same; facing poke = all 8 bytes, verified |
| 1682C + 80*n | 128 | party member n (0-5): ~~1682C + 7F*n, 127 bytes~~ the records in memory are 0x80 apart (names at 1682C, 168AC, 1692C, 169AC, 16A2C, 16AAC: read 2026-11-18 round 2); the 127-byte layout below is right inside each | search for the name |
| record +00 | 16 | name (capitals, zero padded) | read |
| +10..+14 | 5 | sex (1 male, 2 female), alignment at creation, alignment (1 good, 2 neutral, 3 evil), race (1 human, 2 elf, 3 dwarf, 4 gnome, 5 half-orc), class (1 knight, 2 paladin, 3 archer, 4 cleric, 5 sorcerer, 6 robber) | read against the profiles of six characters |
| +15..+22 | 14 | seven statistics, two bytes each (base, current): Int, Mgt, Per, End, Spd, Acy, Luc | read |
| +23, +24 | 2 | level (base, current) | read |
| +25 | 1 | age | read |
| +27 | 4 | experience | poke verified (RYZ 16853) |
| +2B / +2D | 2 / 2 | spell points now / maximum | read (MNZ 5/5) |
| +2F, +30 | 2 | spell level (base, current) | read |
| +31 | 2 | gems | read (0), not poked |
| +33 / +35 / +37 | 2 each | hit points now / second copy of the maximum / maximum | read after a fight (10, 15, 15); not poked |
| +39 | 3 | gold | poke verified (RYZ 16865) |
| +3D | 1 | armor class shown | read |
| +3E | 1 | food | read |
| +3F | 1 | condition bits: 01 asleep, 02 blinded, 04 silenced, 08 diseased, 10 poisoned, 20 paralyzed, 40 unconscious; with 80 set: C0 dead, A0 stone, E0 dead and stone, FF eradicated (80 alone shows nothing) | poked, read off the quick reference (round 2) |
| +40..+45 / +46..+4B | 6 / 6 | equipped items / backpack items (item numbers: 01 Club) | read |
| +7E | 1 | roster slot of this member (0 = A) | read |
| 16224 | 127 | one-record buffer for roster reads (the roster itself stays on disk) | search |
| +7D | 1 | quest marks: bits 01-10 astral projectors 1-5 used, bit 40 impostor defeated, bit 80 (FF) ending already awarded | code of ASTRAL.OVR; ending verified with 5F |
| 12368 | 2 | current map number * 512 (offset of the map in MAZEDATA.DTA); 12369 = map number * 2 (watch `map`) | loader code; read in 6 areas |
| 12362 / 12364 | 2 / 2 | the loaded area's data address (C940) and its event entry (F4A1) | loader code |
| 11013-11024 | - | Sorpigal's "passage outside" handler while Sorpigal is loaded: x at 11017, y at 1101C, id low 1101E, id high 11020, section 11023 (what `WARP` pokes) | disassembly |
Segments (this ZIP, `svga-1500`): program code at 01A80 (the area overlay's code at offset F48F = physical
10F0F), data at 12230 (x = offset 3C38; the overlay's data at offset C940 = physical 1EB70). An `.OVR` file is a
14-byte header (code address, code length, data address, data length), code, data; the data starts with the
event tables: count at C972, square indexes at C973, then facing masks, then handler addresses.
| 15E88 / 15E59 | 15 / 15 | encounter list while the encounter screen shows: number within a group of 16 / group (1-based); monster number = (group - 1) * 16 + number (Poltergeist 11 = group 1 number 11, Vampire 124 = 8/12, Okrim 195 = 12/19). In combat 15E88.. holds pointers to 32-byte monster records instead (2E80, 2EA0, ... in the data segment) | dumps at known groups (round 2) |
Watches in `game.json`: `x`, `y`, `hp1`, `gold1`, `food1` (RYZ), `map`. Monster hit points in combat: not located (the 32-byte records at data offset 2E80 are the place to look).
Program tables in MM.EXE (file offsets): monsters 195 x 32 bytes from the name "FLESH EATER" (name 15, then statistics; bytes 22-23 experience, last byte picture number 00-4B); items 255 x 24 bytes from 19B2A (name 14, flags, ..., price big-endian in bytes 20-21); `MM.RSM` is a symbol list of the program's routines (encounter, bash, trade, monhp ...).

## Emulation notes
- Model `svga-1500` (GOG's own cycle count). About 70 frames per second; `play.py` runs ~1500 frames per second
  of host time, so long waits are cheap.
- Text screens have a blinking cursor only at input prompts; the title animates. Use `do!` / a final `!` and
  fixed waits everywhere: no route in this playbook uses `settle`.
- RNG follows frame timing: the creation rolls, the encounter at (3,6) and whether the party is surprised all
  change with any earlier wait.
- **Fixed in the backend 2026-11-18 (coordinator):** the note below was true for the scout run. A cached state
  replayed the whole route (not only the program launch) on the saved disk, so the creation ran twice. The
  launch log now ends where MM.EXE starts; the scout's reproduction gives A-G on a cache miss and on a cache
  hit, identical frames. `created` can be built on again; `start` keeps its `sav:` route.
- ~~**Checkpoints built on a route that creates a character corrupt the roster on a cache hit**~~ (tool problem,
  reported 2026-11-18): `python3 tools/emu.py dos/might-and-magic --seq "@created,left,w60,left,w150,y,w250"`
  from a cached `created` shows A-G plus `H) RYZ` at the inn (a second, fresh RYZ); the same keys from power-on
  (`PARTY,left,...`) show A-G only; a checkpoint two levels deep showed H and I. Loading a cached state seems
  to replay the route's inputs on a disk that already holds the written roster, so "create character" runs again.
  Renames and sign-ins are harmless when replayed. Workaround used here: `start` powers on with the saved
  roster (`sav:02_ryz_party`) and only forms the party; with it a sign-in after a cached `@combat` shows A-G.
- After a shop the party faces away from the counter (blacksmith entered facing west, left facing east).
- Screenshots are 960x600 from `play.py`, 320x200 from `emu.py --out` frames.

## Checkpoints
Capture run 2026-11-18 added: `cave1` (lit cavern below Sorpigal), `portsmith`, `algary`, `dusk`, `erliquin`,
`outdoors` (C2), `areaa1`, `areae1`, `alamar`, `doom`, `whitewolf`, `qvl1`, `astral` (all through `WARP`, the
dark ones with Light cast first). Save `03_portsmith_inn` (signed in at town 2).
`title`, `menu`, `start` (custom party from `sav:02_ryz_party`), `created` (same party built by the creation
route: use only for creation shots), `blacksmith` (shop prompt), `equipped` (after buying and equipping),
`combat` (encounter screen at (3,6)); the first scout's `sorpigal` (stock party) and `after_save`.

## Sources
| Source | URL | Used for | Accessed |
|---|---|---|---|
| Game manual, second edition (c)1987 (`Manual.pdf` in the owner's ZIP; text copy `work/scout/dos/might-and-magic/manual.txt`, not committed) | - | controls, commands, classes, races, statistics, all 94 spells, save rule | 2026-11-18 |
| `Readme.txt` in the ZIP | - | nothing beyond the copyright (3DO, 1997 re-release) | 2026-11-18 |
| Game files in the ZIP (`MAZEDATA.DTA`, `*.OVR`, `ROSTER.DTA`) | - | map layout, event squares, texts of Sorpigal, record size | 2026-11-18 |
| Wikipedia | https://en.wikipedia.org/wiki/Might_and_Magic_Book_One:_The_Secret_of_the_Inner_Sanctum | release years, platforms, plot outline | 2026-11-18 |
| NES port in this database | `games/nes/might-and-magic/` | world structure, map byte layout (hint only; "source (NES port)") | 2026-11-18 |
| The Cutting Room Floor | https://tcrf.net/Might_and_Magic_Book_One:_The_Secret_of_the_Inner_Sanctum_(DOS) | not reachable (HTTP 403) | 2026-11-18 |
| StrategyWiki | https://strategywiki.org/wiki/Might_and_Magic_Book_One:_The_Secret_of_the_Inner_Sanctum | not reachable (HTTP 403) | 2026-11-18 |
| GameFAQs, Data Crystal, gamehacking.org | - | not tried (time box) | - |

## Capture run 2026-11-18 (what was learned)
- The set was built by writing shot lines (`id | category | caption | route`) into the work set's `shots.txt` and
  running `shoot.py dos/might-and-magic main --only ids` (a 20-shot batch takes ~15 s), exploring first with
  parallel `emu.py --seq ... --out work/x/NAME` runs (one frame per token). `play.py` was only needed for
  `unsnap` and `export`.
- **`tools/maps.py` read the event tables two bytes early until this run** (header is 14 bytes, not 12): every
  list had two bogus first squares and lacked the last two. Fixed; the scans of areas 1-5, 14, 23, 30, 34, 37,
  43, 44, 49, 50 made before the fix miss two squares each (Astral was re-read by hand: the ending square).
- Frames that work: spell result right after the target letter (`...,a,!`); Ctrl-A's message right after the
  key (`ctrl>a,!`); training result right after `a`; chest result `1,w200,4,w150`; title second picture
  `pow,BOOT,w280`. `shoot.py` and `emu.py --out` frames can differ by a few frames on animated screens (title):
  pick such frames with `shoot.py --only` variants.
- Casting outside combat: profile, `c`, level, number, **Enter**. Chest options ask "WHO WILL TRY 1-6?".
- Encounter groups depend on timing (`@outdoors,w70,...` gave Strangling Vines, without the wait Snakes).
- Level-1 characters at 1 HP "go down" one by one; the sixth gives the game-over text (`BLK*24`).
- Dead ends: a Key Card (item FD placed in RYZ's backpack, `poke:16873=FD`) with marks 5F was still "REJECTED"
  at the Astral door; not understood (the ending square was reached by position poke instead).
- Not done: surprised party, bash, trade, temple cure of a wounded character, tavern rumor text, statues other
  than one, the 34 areas not scanned, walking between areas.

## Capture run 2026-11-18, round 2 (what was learned)
- **Tools** (in `tools/` of this game): `survey.py N.. | all` keeps one emulator per area, steps onto every event
  and fight square and writes the monster groups as text plus a labelled sheet and one plain view per area to
  `work/scout/dos/might-and-magic/survey/` (all 55 areas: ~10 minutes); `try.py FILE --frames K [--crop ..]
  [--peek A:N]` plays a file of `name | route` lines in parallel and tiles the last K frames (crop
  `0,172,320,200` = the combat message lines: 27 frames of ten fights fit one sheet). Frame `#k` of a try sheet
  is the frame after the k-th of the last K tokens: count the tokens before copying a route (an off-by-one
  cost a reshoot here).
- **Macros**: `STRONG` (hit points 64, 71, 58, 49, 53, 44, all three copies, right addresses), `GO:lo:hi:ss` (Light
  + WARP to (8,8) of an area). `LOWHP` and `WORTHY` were written for 127-byte spacing: for members 2-6 they hit
  the byte before the intended one (`LOWHP` sets hit points to 0 and gems to 256, not hit points to 1; the shots
  made with them still reproduce and say what they show). Not changed, so the round-1 routes stay as they were.
- **Mechanics routes that work** (all from `@equipped` unless said): locked door `AT:03:07:73,FW,left,w80` then
  `b` (gas trap, door opens), `u,w100,4` (Robber: success), `u,w100,1` (Knight: blade trap); trade
  `1,w100,t,w150,2,w150,2,w150,type:250,w60,enter`; share/gather `s`/`g` + `1`-`3`; use `u` + letter (+ target);
  herbs/potion: buy at `AT:06:05:56,FN,left,w250,y,w150,c,w150,d|e`; First Aid `5,c,1,4,enter,1`; temple with a
  wounded shopper `set:1685F=4:2`; rumor = tip twice, then `c`; bribe that is accepted:
  `...u,w100,4,w200,w21,up,w250,b` (Guardsmen + Gnomes).
- **Combat frames**: `@combat,a,w300` = MNZ's options; order per round MNZ, EBO, RYZ, CUBI, monsters, DEDDO,
  CONDI. Cast result right after the last key (`enter,!` / target letter + `w20`). Monster actions: `a` then
  `w60` steps; give `b` (block) to pass a character's prompt.
- **Encounter timing**: the room at Sorpigal (3,6) gives another group for every extra wait before `up`
  (w9 Goblins, w21 Guardsmen + Gnomes, ...); none of 40 waits gave a surprised party.
- **Dead ends**: Search after two won fights found nothing; 7 rests were never interrupted; selling an item
  (letter at the sell list) changed nothing on screen in two tries; Scroll of Fire in combat ran out of sync;
  Sorpigal (5,15) is silent from all four sides.
- `shoot.py --verify` of all 242 as one background job was killed after ~190 shots (exit 137, cause not found);
  in the foreground 26 shots verify in 40 s. Renaming a shot or changing its category leaves the old PNG in the
  work set: `play.py unsnap OLDID --set main` (needs a running session).
- `VET` = `STRONG` + level 7 for all six, experience 57730-71344 (level 8 needs 96000: the trainer's own number), DEDDO 34 and
  MNZ 38 spell points at spell level 4, 9 and 14 gems. Spells seen with it: playbook design/characters.md section 8.
- Saves `04_sorpigal_equipped` (signed in after shopping) and `05_sorpigal_level7` (the `VET` party with gold, for the owner's own tests of higher spells).

## Open questions
- ~~Current area number in RAM and a clean way to change area by poke~~: solved 2026-11-18, see `WARP` and the Areas table.
- Monster hit points in RAM (to end fights at once); death and the game-over screen.
- ~~Whether the order of the 55 maps in `MAZEDATA.DTA` is the one `maps.py` assumes~~: yes (the loader's own table).
- ~~Sorpigal (1,0) and (8,1) have event entries that showed nothing~~: not events (maps.py offset error); the real extra squares are (5,8) and (5,15), not visited.
- ~~The leprechaun without a gem ended at a blacksmith sign view~~: its code moves a party without gems to Sorpigal (8,5).
- Exact class requirements and what each race changes; item number list; experience table beyond level 3.
- Quest route on DOS (everything about the main quest here comes from Wikipedia or the NES port).
