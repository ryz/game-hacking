# Dungeon Magic: Sword of the Elements (NES, USA) - playbook

Everything an agent needs to play this game efficiently: read it before playing, add to it after every run.
Status of each fact: **verified** (seen in the emulator, with the route) or **source** (manual/FAQ/wiki, not yet
checked). Never delete a fact that turned out wrong: strike it and say what is true.
**ROM text** = read from the ROM's plain-ASCII script (`work/scout/dungeon-magic/strings.txt`, rebuilt with the
one-liner in Emulation notes), not yet seen in play. **code** = read from the disassembly
(`tools/dis6502.py dungeon-magic`), not yet seen in play.

## Identity
| Field | Value |
|---|---|
| Title (EN / original) | Dungeon Magic: Sword of the Elements (title screen, verified); Japanese release by Natsume (Wikipedia; Japanese title not checked) |
| Platform / model used | NES, NTSC (`game.json`); NES 2.0 header, mapper 1 (MMC1), 128 KiB PRG + 128 KiB CHR, 8 KiB battery RAM; CRC32 `1fedecae` |
| Release (region, year) | North America July 1990 (Wikipedia; title screen "(c) Taito 1989"); Japan 10 November 1989 (Wikipedia) |
| Developer / publisher | Natsume / Taito ("Game created & programmed by Natsume", verified) |
| Genre | Real-time first-person dungeon RPG (Wikipedia; compared with Dungeon Master); towns, overworld sections and dungeons on 16x16 grids |
| Players / save system | 1 player; **battery save, written automatically by a night at an inn** (verified: SRAM `$6000-$60xx` and the "NASTUME" signature at `$7F04` appear after the inn; the title then offers CONTINUE YOUR ADVENTURE) |

## Boot sequence
- Power-on: Taito/Natsume credits screen with the animated "Dungeon Magic" logo (f60-f500), then the attract intro
  (tree in a storm, typed text "THE CALM NIGHT IS SHATTERED ... DARCES, THE DARK OVERLORD, HAS RETURNED.") from
  ~f540, then a town panorama (~f1800) (verified, intake sheet + scout).
- Start on the credits screen is ignored; Start during the intro jumps to the title menu (verified).
- `TITLE` = `w600,start,w60,settle` -> title menu (cursor sword blinks): BEGIN A NEW ADVENTURE (only entry with an
  empty battery), CONTINUE YOUR ADVENTURE appears once a save exists (verified). A does nothing here; **Start
  selects**, Down moves (verified).
- `NEWGAME` = `TITLE,start,w600,settle`: no name entry, no character creation. A one-page typed message from the
  old sage ("ONLY WHEN THE FIVE ELEMENTS ARE JOINED WILL DARCES BE DEFEATED.") auto-closes after ~450 frames and
  play starts in Granville (verified). Checkpoint `start`.
- `CONTINUE` = `TITLE,down,start,w300,settle` -> resumes at the inn ("HOW DID YOU SLEEP? WOULD YOU LIKE TO
  CONTINUE THE ADVENTURE?") (verified with `sav:01_start`).

## Controls
| Context | Button | Action | Status |
|---|---|---|---|
| Title menu | Start / Down | choose / move the cursor (A ignored) | verified |
| Field (first-person) | Up | step forward one square (also walks through an opened door) | verified |
| | Left / Right | turn 90 degrees (needs a release between presses: `right:8,right:8` back-to-back counts once; use `right,w30`) | verified |
| | Down | no visible effect in town (no step back seen) | verified (no effect seen) |
| | A | talk to the person in front of you (NPCs wander in real time); open a closed door in front; otherwise the action of the active command icon | verified (talk, door) |
| | B | nothing seen in the field; held B blocks turning | verified (no effect seen) |
| | Start | **pause** (COND STOP); while paused Left/Right choose a command icon: Fight ("Weapons & Armor"), Item, Spell (rune slots), Use ("Use command: open the door & get box"), Camp (weight, food, water) | verified |
| Paused | A / Start | resume with the chosen icon active | verified |
| | Select | open the chosen icon's panel (Spell: the rune slots) | verified (Spell); code: Select sets the "panel open" mode for any icon |
| Spell panel open | Left/Right | move the cursor over the runes | verified |
| | B | add the highlighted rune to the spell (shown top left, up to 3) | verified |
| | Start, then A | resume, then cast the spell (costs HP) | verified (`rune_cast`) |
| Fight icon | A | swing at the monster in front | verified (`battle_win`) |
| Shops / inn | A / B | YES / NO (the window says "B:NO A:YES") | verified |
| Signs | face them | a sign's text shows while you face it ("WANTED: BRAVE WARRIORS..."); turn away to close | verified |

Input timing: default press (hold 8, wait 40) works for turns, steps, menus and shop prompts. Text types at
~4 frames per character; one A per page with `w150` is safe. NPCs move on their own, so frames depend on exact
waits (deterministic, but a different `wN` puts the NPC elsewhere).

## Game structure
- Story (Wikipedia + ROM text): 500 years ago the hero Magi drove out the dark overlord **Darces**; Darces returns to
  the Kingdom of **Granville**. "5 become 1, 1 becomes 5": the hero must find the five elemental swords (Earth,
  Water, Fire, Wind/Sky, Fairy) and join them. The King gives 100 gold and a short sword and sends the hero to find
  **Tores** (ROM text "WE NEED THE SWORD OF TORES ... I WILL GIVE YOU 100 GOLD PIECES AND A SHORT SWORD").
- Places (ROM text): Granville (capital, castle outside the north gate, verified), Gran, Zandor (ruler Taz),
  Deirus (Arianna's teachings), Sull, Selle, the Spring of Sara, Dungeon of Doom (west of town; Ring of Flight),
  a cavern / invisible chamber in the sky (Sky Sword), the Dark Forest (Ice Sword, freed by sky magic), the
  serpents' fire (Fire Sword), an undersea world, Tomb of an ancient warrior (Book of Runes), Wind Cape (Book of
  the Seven Witches, fairy language), the Dragon King's cavern (Armor of the Dragon King).
- Systems (Wikipedia + ROM text): magic from five schools; becoming an apprentice of a school's wizard
  ("WILL YOU BE APPRENTICED IN THE MAGIC ART?") unlocks its runes; spells are 1-3 runes (243 combinations), cost HP
  (no MP); "You cannot use magic in town". Levels are granted by wise men ("HAVE YOUR JOURNEYS MADE YOU WISER?")
  once EXP is enough. Food and water are consumed at camp and at inns. Weight limit (WEIGHT 49.6 shown).
- Town layout (verified, Granville = map 00): 16x16 walled square, gates in the middle of each side (exits to
  overworld sections), buildings entered by facing their door, A to open it, Up to walk in. Granville
  buildings: weapon & armour shop (door at square 73, stand on 74 facing west), inn (93, from 94 facing west),
  item shop (B3, from B4 facing west); ~~the doors at 6C, BC, C6 stayed closed~~ they are wizards' houses and open
  normally (capture 2026-11-18): Earth 34 (from 44 facing north), Water 38 (from 48 north), Fire 6C (from 6B
  east), Wind BC (from BB east), Fairies C6 (from C7 west) (verified).
- Overworld (verified): leaving Granville's north gate puts you on map 25 (a 16x16 field section) at DE; two steps
  north is Granville Castle (map 89, green stone walls).

### Map data (for floor maps in `design/`)
- **Current map: RAM `$0600-$06FF`**, 16x16 cells, row-major, index = position byte (`$YX`) (verified).
- Town and dungeon cells: low nibble = walls (1 north, 2 east, 4 south, 8 west); bits `$10`, `$20`, `$40`, `$80` =
  features (in Granville: `$10` on the four gate squares, `$20` on building squares behind doors, `$80` on the
  street square in front of a door / the sign; `$40` meaning open) (verified for Granville).
- **Decoded (capture 2026-11-18): floor XX is at PRG bank XX>>5, CPU `$A000 + (XX & $1F) * $100`** (the scout's
  `>>4` was wrong for ids >= $80; `tools/maps.py` fixed). Real floors: towns 00-05, forests 40-48 (bank 2),
  castle and dungeons 80-97 (bank 4). Exit tables at `$BA00` of the same bank (towns: 8 bytes per map = pointers
  to door squares, door types 04 weapons/06 items/0A inn/08 wizard, exit squares, exit records; banks 2/4: 4
  bytes per map = exit squares, exit records). Exit record = `[type, map, square, -, owlo, owhi, -, -]`, type 10
  = to the overworld, 14/16/18 = stairs. Everything is drawn by `tools/atlas.py` -> `design/maps/` and indexed in
  `design/maps.md` (with warp tokens per floor).
- **Overworld (decoded):** one 64x96 map at bank 1 `$A000` (64 cells per row; rows 0-63 the continent, 64-95 the
  lower world). `$98/$99` = pointer of the party's overworld cell (`$A000 + row*64 + col`); the "section" id `$95`
  = `$20 + (row/16)*4 + col/16` on the continent, `(row/16)*4 + col/16` (`$10-$17`) in the lower world; `$8A`
  = position inside the section. Cell high nibble = terrain (7 grass, E forest edge, F water, 0 lower ground);
  `xF` = a place (1F town, 0F castle, others dungeon entrances). Which town is entered is decided by `$98/$99`.
- Town and dungeon maps are stored **uncompressed in the ROM**: map 00 (Granville) at PRG offset `$2000` (bank 0
  `$A000`), map 89 (Granville Castle) at PRG `$12900` (bank 4 `$A900`) (verified by matching the RAM block).
  A wall-consistency scan finds map-shaped blocks at PRG `$2000-$25FF` (6 towns, ids 00-05) and `$12100-$137FF`
  (bank 4: ~22 dungeon/castle maps). The loader copies `$A000 + (id & $1F) * $100` from the PRG bank chosen by a
  jump table indexed by `id >> 5` (code, `$DE57` and `$E546` in the fixed bank); the id -> bank table is not
  decoded yet, so match RAM dumps instead.
- Overworld sections (ids `$2x`) use another format (high nibble = terrain type, e.g. `$7x` grass, `$Ex/$Fx`
  water or forest; low nibble = variant) and were **not found verbatim in the ROM** (generated or compressed).
  Use the RAM copy.
- Renderer: `python3 games/dungeon-magic/tools/maps.py ID ... --out DIR` (from ROM) or `--ram dump.bin` (256 bytes
  of `$0600`), `--pos YX` marks the party. Example atlas of maps 00-05, 41-43: `work/scout/dungeon-magic/maps/atlas.png`.

## Shot plan
`shots.txt` holds 41 routed shots in game order (set `main`, 41/41 verified 2026-11-18); planned lines are comments.
- [x] boot, intro, title, continue menu, first control, HUD, plaque, old man's compass, Spell panel
- [x] shops (weapons, items, buying), Item panel, inn welcome and morning (save)
- [x] wizard apprenticeship, "you can use the magic", wise man question, level up
- [x] field and castle, castle cellar, towns 02 and 05, one shot per dungeon (80, 83, 86, 8C, 8F, 95) and forest (40, 43, 46)
- [x] battles: dungeon monster, Fire spell (runes entered, cast), victory, skeleton, field serpent; guardian of 92; game over
- [ ] King (castle doors stay closed), Camp (needs food/water), elemental swords, Darces, ending
- [ ] towns 01, 03, 04 (look like 00/02/05; routes in `design/maps.md`)

## Strategy and walkthrough notes
- Start: talk to the old man (compass), visit the King in Granville Castle (north gate, 2 steps north; 100 gold
  and a short sword, ROM text), buy food and water at the item shop (B4), sleep at the inn (94) to save.
- The game is real time: monsters attack while you stand still; pause with Start before menus.
- Levels come from wise men, not automatically: poke EXP (`$4B-$4C`) or level (`$4A`, source code `004A:09` =
  start at level 9) to skip grinding; keep values plausible (LV 6-9 mid-game, gold under ~3000).
- Spells cost HP: freeze HP (`freeze:004D=..`) while showing magic. All-spells Game Genie `AEEVVUPA` (source,
  untested) as a `rom:` variant.
- Critical path (ROM text, order not verified): Granville -> Tores / Earth Sword (Selle sanctuary sculpture, Dungeon
  of Doom west of town, Ring of Flight) -> Sky Sword (chamber in the sky) -> Ice/Fire Sword (Dark Forest; sky
  magic breaks the ice; Fire of the Serpents) -> Water Sword (Dragon King, Armor of the Dragon King, Book of
  Runes, undersea world) -> Wind Sword (Wind Cape, Book of the Seven Witches) -> back to Granville (castle
  attacked, rescue the King) -> Darces.

## Naming
No name entry: the hero is unnamed and the game starts straight after BEGIN A NEW ADVENTURE (verified). The
owner's name rule (ryz) does not apply.

## Shortcuts
| What | How (tokens / prefix / code) | Source | Status |
|---|---|---|---|
| **Warp to any castle/dungeon floor** | `poke:0095=XX,poke:008A=SQ,poke:008F=SQ,poke:0098=LO,poke:0099=HI,poke:0011=00,poke:0003=TT,w240` (TT 16 for floors 80-97, 18 for forests 40-48; SQ/LO/HI from the floor's incoming stairs record; ready-made tokens per floor in `design/maps.md`) | capture (exit-table decode) | verified (all 33 floors) |
| **Enter any town** | from `@field`: `poke:0095=SEC,poke:008A=SQ,poke:008F=SQ,poke:0098=LO,poke:0099=HI,right,w30,right,w30,up,w240` = stand on the square north of the town (its north-gate exit record) and step south; e.g. town 01 `SEC=25 SQ=29 LO=99 HI=A4`, 02 `24 74 C4 A5`, 03 `27 95 75 A6`, 04 `29 25 95 A8`, 05 `2E 2E AE AC` | capture | verified (01-05; 04 lost to a field monster on the way, freeze HP) |
| Current HP | `$DC` (shown on the left scroll); `$4D` = maximum HP. Freeze in fights with `freeze:00DC=..` and `w10*N` waits | capture | verified |
| Magic schools | `$46` bit mask (Fire = `$04`, row 3 of the panel); poking it is not enough for the panel - also poke the rune tiles of the panel buffer (Fire row: `poke:61CB=60,poke:61CC=67,poke:61CD=68,poke:61CE=69`), or apprentice for real | capture | verified (Fire) |
| Warp inside the current map | `poke:008A=YX,poke:008F=YX` then turn/step (the view redraws on the next turn/step) | scout | verified (Granville, several squares) |
| Gold | `set:0040=N:2` (16-bit, shown on the next redraw) | Action Replay `0040:FF` (source) + scout | verified |
| Level | `poke:004A=N` | Action Replay `004A:09` "start at level 9" (source) | verified (LV display) |
| EXP | `set:004B=N:2` | scout | verified (EXP 5909 shown) |
| Enemy HP | `poke:00DB=00` / `freeze:00DB=00` | Action Replay `00DB:00` (source) | untested |
| All spells | Game Genie `AEEVVUPA` (`rom:` variant) | Almar's Guides via search summary | untested |
| 9999 gold at start | Game Genie `YYYIITAE` + `PGKSGTAG` | same | untested |
| Shop gives gold | Game Genie `AANVXTLT` | same | untested |
| Bonus coins | Controller 2 A twice + Start on controller 1 at the start (GameSpot) | GameSpot | not testable (no controller 2) |
| Save anywhere-ish | any inn night writes the battery save | scout | verified |

### Saves (rom/saves/dungeon-magic/, never committed)
| Name | Contents (progress, party, items) | URL | SHA-1 | Status |
|---|---|---|---|---|
| 01_start (made here) | copy of `games/dungeon-magic/saves/01_start.sav`: Granville inn, LV 0, HP 12, 98 gold | - | see `saves/README.md` | verified (`sav:01_start,CONTINUE`) |
| 02_granville_fire_lv1 (made here) | copy of `games/dungeon-magic/saves/02_granville_fire_lv1.sav`: Granville inn, Fire apprentice, LV 1, HP 15, 397 EXP, 212 gold | - | see `saves/README.md` | verified (`sav:02_granville_fire_lv1,CONTINUE` -> inn morning) |
No downloadable saves found (GameFAQs not reachable).

## RAM map (for `game.json` "ram" watches and pokes)
| Address | Size | Meaning | How found |
|---|---|---|---|
| `$0040` | 2 (LE) | gold | Action Replay code + poke (verified) |
| `$004A` | 1 | level (LV) | Action Replay code + poke (verified) |
| `$004B` | 2 (LE) | EXP | poke (verified) |
| `$004D` | 1 | **maximum** HP (12 at start) | capture: the display follows `$DC` |
| `$00DC` | 1 | current HP (left scroll) | capture (verified: freeze holds the display) |
| `$0046` | 1 | magic schools learned, bit mask (Fire `$04`) | capture: RAM diff of an apprenticeship (verified) |
| `$0043-$0044` | 2 | WEIGHT capacity x10 (`$01F0` = 49.6; minus 2.0 after an apprenticeship) | capture (RAM) |
| `$0003` | 1 | pending transition type (10 overworld, 14/16/18 stairs); written by the exit code with `$95/$8A/$98/$99` | code + warp test (verified) |
| `$0098-$0099` | 2 | overworld pointer of the party (see Map data) | capture (verified) |
| `$0700-$07FF` | 256 | monster/object occupancy grid of the floor (cell = monster slot) | capture (RAM, partly understood) |
| `$0080` | 1 | active command icon 0-4 (Fight, Item, Spell, Use, Camp) | code + watch (verified) |
| `$0017` | 1 | icon * 2, +1 while its panel is open | code + watch (verified) |
| `$007B` | 1 | 1 = paused | code |
| `$008A`, `$008F` | 1 | party position `$YX` (high nibble row 0-F from north, low nibble column) | dump diff (verified; poke both) |
| `$008B` | 1 | facing bitmask (1 north, 2 east?, 4, 8; with `$8C-$8E` the four directions rotated) | dump diff over turns (verified it rotates; exact mapping open) |
| `$0095` | 1 | map id: `$00-$05` towns, `$2x` overworld sections (Granville north field = `$25`), `$89` Granville Castle | watch (verified) |
| `$0600-$06FF` | 256 | current map (see Map data) | dump + ROM match (verified) |
| `$00DB` | 1 | enemy HP (right scroll) | Action Replay; verified (182 for the floor 92 guardian) |
| `$0004` / `$0006` | 1 | joypad 1 newly pressed / held (A $80, B $40, Select $20, Start $10, Up 8, Down 4, Left 2, Right 1) | code |
| `$6000-$60FF`, `$7F00-$7F0F` | - | battery save: a copy of the player block (`$6010` = gold ...), signature `55 AA 55 AA "NASTUME"` at `$7F00` | dump after the inn (verified) |
Food and water counters not found yet (blank at the start).

## Emulation notes
- NTSC, default press. Deterministic; NPCs wander in real time, so their positions depend on the exact waits.
- The status panel does not redraw after a poke until something changes it (HP stayed 12 after `poke:004D`);
  gold/EXP/LV redrew within 30 frames.
- `settle` works on the title (blinking cursor) and in town (NPCs off screen); with an NPC in view it may run its
  300-frame limit.
- Text dump: `python3 -c` over `rom/dungeon-magic.nes` printing runs of printable ASCII (`[ -~]{5,}`); the script
  is plain ASCII, words separated by control bytes.
- Disassembler: `python3 tools/dis6502.py dungeon-magic BANK ADDR [N]` (bank 7 fixed at `$C000`, others at `8000`).

## Checkpoints
| Name | What |
|---|---|
| `title` | title menu, BEGIN A NEW ADVENTURE |
| `start` | first control in Granville (square A7, facing north toward the plaque at 87) |
| `field` | overworld section 25 outside Granville's north gate, castle ahead (warp to 18 + one step) |
| `castle` | Granville Castle entrance (map 89) |
| `d83` | floor 83 after a warp, LV 6 hero, HP frozen |
| `d81_monster` | floor 81: monster in front, Fight active (battle shots start here) |
| `spellpanel` | Granville start, `$46=1F`, Spell panel open, old man in front (compass dialogue) |
| `fire_field` | real Fire apprenticeship, outside the north gate, Spell panel open on the Fire runes |
| `boss92` | floor 92 guardian in front, LV 11 hero with HP frozen |
All four rebuilt from an empty cache and compared with a cache hit: identical frames (2026-11-18).

## Sources
| Source | URL | Used for | Accessed |
|---|---|---|---|
| Wikipedia | https://en.wikipedia.org/wiki/Dungeon_Magic:_Sword_of_the_Elements | release dates, developer, story, magic system, inn save | 2026-11-18 |
| Almar's Guides (Action Replay / Game Genie), via search-result summaries only | https://almarsguides.com/retro/walkthroughs/nes/games/dungeonmagicswordoftheelements/actionreplay/ | `0040`, `004A`, `00DB`, Game Genie codes | 2026-11-18 (site outside the network) |
| GameSpot cheats (search summary) | https://www.gamespot.com/games/dungeon-magic-sword-of-the-elements/cheats/ | bonus coins tip | 2026-11-18 |
| StrategyWiki | https://strategywiki.org/wiki/Dungeon_Magic:_Sword_of_the_Elements/Table_of_Contents | section list only (16x16 maps, 5 swords + final quest); pages 403 | 2026-11-18 |
| RPGClassics shrine | https://shrines.rpgclassics.com/nes/dungeonmagic/magic.shtml | not reachable (outside the network) | 2026-11-18 |
| archive.org NESManuals | (download host refused, 403) | - | 2026-11-18 |
| ROM text | `work/scout/dungeon-magic/strings.txt` | places, story, shop and inn text | 2026-11-18 |

## Open questions
- (capture) Castle doors (5C, 64, 8C, A4, BC; north 45/47) stay shut with A and with the Use icon; the King was
  not reached. The cellar stairs (floor 8A) are in the walled centre room 79.
- (capture) Only one apprenticeship at a time: after Earth, the Water wizard's door did not open; the ROM has
  "I'm sorry, you have already been apprenticed". Further ones come with the swords (source: StrategyWiki summary).
- (capture) Item shop: A buys the highlighted shelf item (a jug, 56 gold) repeatedly; moving along the shelf not
  found. Camp with A did nothing (no food/water bought).
- (capture) The floor 92 guardian takes no damage from a blow (see design/findings.md).
- Map id -> PRG bank table (jump table at `$E552` indexed by `id >> 5`): decode it so every map id can be rendered
  from ROM and warped to; how a map-id warp (`$95` + reload) is triggered cleanly (try poking `$95` and `$8A` just
  before stepping through a gate).
- Overworld format and where it lives in ROM; how the `$2x` sections connect.
- Meaning of cell bits `$40`/`$80` in dungeons (stairs, chests, monsters?); facing values of `$8B`.
- Food and water addresses; HP max; weight.
- Item and monster names are not ASCII in the ROM (custom encoding or graphics): not decoded.
- Whether Down steps back (not seen), what B does in fights; the Fight icon controls in battle.
- Closed doors at Granville 6C, BC, C6 (locked? need the Use icon?).
