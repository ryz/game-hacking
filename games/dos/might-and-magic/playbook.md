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
| | `b` | bash a locked door | source (manual) |
| | `u`, then `1`-`6` | unlock: that character picks the lock (Robber) | verified (CUBI, Sorpigal (3,7) south door) |
| | `q` | quick reference: HP, SP, AC, food, condition of all six; `1`-`6` opens a profile | verified |
| | `1`-`6` | character profile | verified |
| | `v` | sound on/off (not on the list) | source (manual) |
| Profile (in play) | `c` cast (level, number), `d` discard, `e` equip (`a`-`f`), `g` gather, `r` remove (`1`-`6`), `s` share, `t` trade, `u` use, `q` quick ref, `esc` | equip, remove verified; the rest source (manual) |
| Prompts (shops, stairs, statues, inn) | `y` / `n` | answer | verified |
| Shop menus | `a`-`f` | pick the entry / buy that item | verified (blacksmith) |
| | `g` / `1`-`6` / `esc` | gather the party's gold on the shopper / other character / back | listed on screen, not pressed |
| Encounter | `a` attack, `b` bribe, `r` retreat, `s` surrender | (only when the party is not surprised) | attack verified, rest source |
| Combat | `a` | attack monster A | source (manual); listed on screen |
| | `ctrl>a` | quick fight: attack / shoot / block, whichever applies | verified (macro `QA`) |
| | `f` fight (pick the monster), `s` shoot, `b` block, `e` exchange places, `r` retreat, `u` use | | listed on screen, not pressed |
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
  experience for a Knight, 25 gold; level 3 at 3000). New spell levels every other level (manual).

## Shot plan
The plan is `shots.txt`: routed lines are routes that were run during the scout (frames looked at), commented
lines are targets with the method. By category: title 2, menu 3, system 10 (creation, roster, unlock, rest,
training/level-up, leprechaun, statue), gameplay 8 (Sorpigal views, signs, darkness, outdoors, other towns),
shop 5 (blacksmith lists, market, temple, tavern), inventory 3, hud 1, dialogue 2, battle 7, map 1, save 2,
gameover 1, extra 2. Distinctive for this version: the text-and-wireframe look in four colours, creation by
re-rolling, everything driven by letter keys, the encounter options (bribe, surrender), handicap line.

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
| Change area by poke | not found: the current area number and the game's pending-transition variables are not located | - | open |
| Debug features, cheat codes | none found (manual has none; TCRF and StrategyWiki refused the fetch) | - | - |

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
| 1682C + 7F*n | 127 | party member n (0-5) record, same layout as a `ROSTER.DTA` record | search for the name |
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
| +3F | 1 | condition (0 good) | read |
| +40..+45 / +46..+4B | 6 / 6 | equipped items / backpack items (item numbers: 01 Club) | read |
| +7E | 1 | roster slot of this member (0 = A) | read |
| 16224 | 127 | one-record buffer for roster reads (the roster itself stays on disk) | search |
Watches in `game.json`: `x`, `y`, `hp1`, `gold1`, `food1` (RYZ). Monster hit points in combat: not located.

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

## Open questions
- Current area number in RAM and a clean way to change area by poke (the NES port's pending-area trick has no
  known DOS equivalent yet); until then other areas are reached through exits, stairs and the leprechaun.
- Monster hit points in RAM (to end fights at once); death and the game-over screen.
- Whether the order of the 55 maps in `MAZEDATA.DTA` is the one `maps.py` assumes (only Sorpigal is confirmed).
- Sorpigal (1,0) and (8,1) have event entries that showed nothing in the scan (other facings or conditions?).
- The leprechaun was only seen up to its prompt; pressing `2` without a gem ended at a blacksmith sign view,
  not understood.
- Exact class requirements and what each race changes; item number list; experience table beyond level 3.
- Quest route on DOS (everything about the main quest here comes from Wikipedia or the NES port).
