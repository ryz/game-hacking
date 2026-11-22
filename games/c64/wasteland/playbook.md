# Wasteland (C64) - playbook

Everything an agent needs to play this game efficiently: read it before playing, add to it after every run.
Status of each fact: **verified** (seen in the emulator, with the route) or **source** (manual/FAQ/wiki, not yet
checked). Never delete a fact that turned out wrong: strike it and say what is true.

## Read first
- **Start:** `python3 tools/play.py start wasteland --route @start` (world map ON the Ranger Center square x55 y62,
  party RYZ, Angela Deth, Thrasher, Snake Vargas, RYZ first, RYZ stats poked). Model `c64` (PAL). Needs
  `rom/wasteland.zip` (9 D64s). Boot from master side 1 (automatic); play happens on the play copy `disk:5`.
- **Captured 2026-11-22:** sets `start` (49, honest) and `main` (124: run 1 62, run 2 added the side 2-4 towns) published; lenses written.
- **WARP (real warp, 2026-11-22 run 2):** `WARP:XX:YY` (hex) moves the party to square XX,YY of the CURRENT map
  (world or town) and redraws (V): pokes $57/$58, the code operands 09EC/09EE/09FB and F408/F409 together.
  Then one step onto an icon or event square. World entries: Quartz `WARP:1D:2C,N`; Needles `WARP:18:20,N`;
  Las Vegas `WARP:17:13,N`; Citadel `WARP:24:31,N`; Darwin `WARP:39:26,N` (through the radiation belt);
  Highpool `WARP:2F:3A,S`; mine shaft (32,52); Savage Village (13,58). Then `w100,y,w1500` -> "INSERT SIDE N."
  -> `disk:6|7|8,w50,return,w2500` (checkpoints `quartz`, `needles`, `vegas`, `citadel`, `darwin`).
- **Hidden locations:** poke Darwin's world entry record `poke:4E7E=XXYYLL` (arrival x, y, location) before
  stepping on Darwin: `0e0107` = Sleeper Base, `101e10` = Base Cochise grounds (checkpoints `sleeper`, `cochise`).
  F40A = current location number. Town specials survey: `work/plan/wasteland/specials.py` (town maps at $3600,
  32x32; 64x64 maps at $3C00) writes one plan line per event square: the fastest way to find a town's content.
- **World map is in RAM:** 64x64 bytes at $3C00 (row-major, x + 64*y): 0 open ground, 1 mountain (blocks),
  2/3 other passable terrain, 6 water, 13 river current (hurts 1 CON each), single values 7-31 are location
  icons (7 Agricultural Center x36 y55, 8 Highpool x47 y59; list below). BFS over it: `work/plan/wasteland/bfs.py`
  (scratch, rebuild from this note). Zero page $55/$56 = map size.
- **Ways out of the Ranger Center:** leave with Start, then walk NORTH from the RC square. The two squares east
  of it are a dead end (mountains); declining a location prompt puts the party back where it came from.
- **Paths (tokens, from `@start` / `@s_world`):** Highpool `N*4,W*2,N,W*6,S,settle,S,w100,settle,y,w2000`;
  Agricultural Center `N*4,W*2,N,W*3,N,W*3,N,W*10,W,w100,y,w2000`; lake `N*4,W*2,N,W*12,S,W,S,W*6`.
- **Highpool (location coords, F408/F409 follow them):** arrive x7 y1; `S*17` to the dorm row; store door
  `S*17,E*4,S*3,E` (interior x26 y27, counter N of x30 y25: `E*3,N*2,N,E,w1500,N,w1500,y,w2000` = shop);
  infirmary at x13 y29 (from x10 y28: `E*3,S`); workshop interior via the infirmary exit `N,W*4,S`; creek:
  `S*18,W*3,S` (slip event, a kid appears).
- **Checkpoints:** `title`, `rangers`, `party`, `start`, `step1`, `fight`, `highpool`, `infirmary`, `workshop`,
  `store`, `shop`, `quartz`, `needles`, `vegas`, `citadel`, `darwin`, `sleeper`, `cochise` (poked chain); `s_party`, `s_world`, `s_won`, `s_highpool` (honest chain of the start set).
- **Keys:** I/J/K/L move; U Use, E Enc, O Order, D Disband, V View, S Save, R Radio, digits = sheet, SPACE =
  roster; Esc = `leftarrow`. Combat R U H E A W L then Y. The W key alone is `w` (Weapon); `wN` is a wait.
- **Money:** `set:F815=1287:3` (RYZ) works on the map; shops and doctors show the pooled money.
- **Traps:** each menu key needs 200-400 frames; location loads ~2000; save ~3000. Leaving a shop/infirmary:
  `leftarrow,w300,leftarrow,w2000,settle,n,w300` (it re-asks "Enter new location": answer N). A save on a
  location square re-asks too: step off first.
- **Determinism:** no divergence seen this run: every checkpoint built on a parent reproduced (start 49/49,
  main from an empty cache).
- **Open:** game over (CON 1 party survived 4 rounds); MORE: in the shop list; Utils Copy/Restart; disk:9 editor;
  NPC talk and shop lists in the later towns; Quartz Emporium not found; Savage Village, mine shaft, Desert Nomads not shot.
- **Saving in a town** asks side 1 then the town's side: `s,w300,y,w3000,disk:5,w50,return,w3000,disk:N,w50,return,w3000`.

## Identity
| Field | Value |
|---|---|
| Title (EN / original) | Wasteland |
| Platform / model used | Commodore 64, PAL (`c64`); see `game.json` |
| Release (region, year) | North America (Electronic Arts), 1988; GameBase64 entry 8515 (source, dispatch) |
| Developer / publisher | Interplay Productions / Electronic Arts; "Written by Alan Pavlish" on the title bar (verified) |
| Genre | Post-apocalyptic party RPG, top-down world and town maps, menu-driven combat |
| Players / save system | 1 player; saves to the play disks (field Save, and automatically when entering/leaving a location, source) |

### The nine disk images (verified by comparing the D64 files, work/scout/c64/wasteland/disks)
| Token | File | What it is |
|---|---|---|
| disk:1 | WASTLND0 | master side 1: boot side (1541-formatted, a loader in the directory track named "PRODOS", "2.0") |
| disk:2-4 | WASTLND1-3 | master sides 2-4 |
| disk:5-8 | WASTLND4-7 | **play copies** of sides 1-4, made by the game's Utils/Copy: identical game data, but no directory track (tracks 17-18 blank) and the copy mark (byte 253 of track 35 sector 14 is 0, D7 on the masters) |
| disk:9 | WASTLND8 | "ASS PRESENTS: WASTELAND EDITOR": a cracker group's character editor, not part of the game; not tried |
The play copies hold the factory state (time 1:08, default party at the Ranger Center), not a previous owner's game.
Side contents (source, Nearly Ultimate Wasteland Guide): side 1 world map and early minor locations, side 2
Quartz and Needles, side 3 Las Vegas and the Citadel, side 4 Sleeper base, Darwin and Base Cochise.

## Boot sequence
- Intake probe `work/intake/c64/wasteland/sheet.png`: black until about f480, then the frame with the
  WASTELAND logo and a "Start Utils / Written by Alan Pavlish" bar; the globe and the EA/Interplay credit lines
  by f1000; "Place: EARTH / Year: 1998 / Status: DEFCON 1" typed f1380-f1800, then more lines ("Computer
  defense initiative activated.") (verified).
- `TITLE` = `w1900` (verified, `title`).
- Title: S = Start, U = Utils (Copy / Restart / Start) (verified).
- Start -> "Use last saved game (Y/N)?" (verified):
  - **Y** -> "Insert side 1. [RETURN]" -> `disk:5`, RETURN -> about 1600 frames -> the world map with "Entering
    Ranger Center. Enter new location (Y/N)?" (the factory save on the copies) -> Y -> about 1600 frames ->
    Ranger Center screen (`NEWGAME`, verified). A master (disk:1) at that prompt is refused ("INSERT SIDE 1."
    again, verified).
  - **N** -> asks for sides 1, 2, 3, 4 in turn (each RETURN about 1500 frames), then side 1 again -> the same
    "Enter new location" prompt with the factory party (`NEWFRESH`, verified). Probably reinitialises the
    sides from the party on disk; use it to start over once a play disk holds a save.
- Continue a saved game: `CONT` (`s,w300,y,w1500,disk:5,w50,return,w2000`): lands on the world map where the
  party was saved (verified with `sav:01_start`).

## Controls
| Context | Key | Action | Status |
|---|---|---|---|
| Title | S / U | Start / Utils | verified |
| Utils | C / R / S | Copy disk sides / Restart (old party into new copies) / Start | menu verified; C, R not tried; E exits copy (source) |
| Yes/no prompts | Y / N | | verified |
| Ranger Center | C / D / S | Create (max 4 rangers: delete first) / Delete (then digit, Y) / Start (to the world map) | verified |
| Creation | SPACE / RETURN | reroll / accept the roll; then name (typed, RETURN), sex M/F, nationality 1-5, skills by digit (RETURN ends), "Keep this char (Y/N)?" | verified |
| Map | I / J / K / L | north / west / south / east (one square per press) | verified (F408/F409) |
| Map | cursor keys, joystick port 2 | nothing | verified (no change) |
| Map | U | Use: "Which player?" (then skill/item/attribute) | prompt verified |
| Map | E | Enc: "This party is not being attacked. Do you want them to execute a battle round (Y/N)?" | verified |
| Map | O | Order: "Order (Y/N)?" Y, then pick players in the new order (last one automatic) | verified (`ORDER4`) |
| Map | D | Disband: "Who wants to disband?" | prompt verified |
| Map | V | View (redraws the map; time passes) | verified, purpose source: view a map from afar |
| Map | S | Save: "Save game (Y/N)?" | verified |
| Map | R | Radio: "Radio (Y/N)?" | prompt verified |
| Map | 1-7 | character sheet; RETURN pages stats -> items -> skills -> back | verified |
| Map | SPACE | show / hide the party roster under the map | verified |
| Anywhere | `leftarrow` (C64 key left of 1) | Esc: cancel / close a window; on the map passes time (clock +4) | verified (the guide calls it "up arrow": wrong for this setup) |
| Combat | R U H E A W L | Run, Use, Hire, Evade, Attack, Weapon, Load/Unjam per member, then "Use these options (Y/N)?" | A, W, Y verified |
| Combat | S | view enemy groups (C64) | source |

Input timing: the default press (hold 8, wait 40) works; give each key 100-300 frames (screens draw slowly),
the macros use `w200`-`w300`. Character screens and the Ranger Center picture animate (`settle` runs out:
normal).

## Game structure
- Ranger Center (party management: create, delete) -> world map (one big map, 64x64 squares; the party starts
  on the Ranger Center square at x55 y62 near the south-east corner; south edge y62 and east edge x62 give
  "You see miles and miles of endless wasteland..." (verified)).
- Locations are entered by stepping onto their icon: "Entering <name>. Enter new location (Y/N)?" (verified for
  the Ranger Center). Towns and buildings are top-down maps with shops, NPCs, libraries, doctors (source).
- Order of play (source, Nearly Ultimate Wasteland Guide): Highpool, Agricultural Center, Desert Nomads, Mine
  Shaft, Savage Village, Quartz, Needles, Las Vegas, Sleeper Base, Darwin Village, Guardian Citadel, Base Cochise.
- Seen on the world map (verified): Highpool icon (figure and pool) at about x47 y59 with a river running east,
  ringed by mountains on the screens seen; a white building with a sign at about x35 y55 (probably the
  Agricultural Center, unconfirmed); a lake on the west side around x26-33 y55-62; "It is very warm." squares
  west of x44.
- Combat: an encounter opens with "From the depths of the wasteland appears a hostile adversary. 3 Animals
  appear at 14 feet. [RETURN]", an animated enemy portrait, then a per-member command menu (verified, `fight`).

## Shot plan
Captured 2026-11-22 (ticked): all but game over, the Utils sub-screens, later towns and the NPC talk.
Targets for `main` (ids, category):
- [x] `title_screen` title (`@title`); `title_globe_credits` boot (intake frame f1200); `title_utils` menu (U)
- [x] `menu_continue` menu ("Use last saved game (Y/N)?"); `menu_insert_side` menu ("Insert side 1")
- [x] `rc_roster` menu (`@rangers`); `rc_create_roll` system; `rc_skills` system; `rc_nationality` menu; `rc_delete` menu
- [x] `world_start` gameplay (`@start`); `env_world_mountains`, `env_world_lake`, `env_world_desert` gameplay
- [x] `hud_world_roster` hud (map + roster + clock + command bar)
- [x] `char_stats`, `char_items`, `char_skills` inventory (digit, RETURN, RETURN)
- [x] `field_use`, `field_order`, `field_radio`, `field_enc` menu (prompts); `map_edge_message` dialogue
- [x] `battle_appears` battle (`@fight`); `battle_menu` battle; `battle_weapon` battle; `battle_round_msgs` battle (timeline); `battle_xp` battle
- [x] `loc_enter_prompt` gameplay ("Enter new location (Y/N)?"); Highpool town, a shop, an NPC talk, the library/doctor (play)
- [x] later towns: Quartz, Needles, Las Vegas, Guardian Citadel, Darwin Village, Sleeper Base, Base Cochise (run 2, by WARP); `menu_insert_side2/3/4`, `save_town`
- [ ] `gameover` (party dead); NPC talk; later shop lists
`start` set: power-on, title, continue prompt, insert side, Ranger Center, create RYZ (roll, name, sex,
nationality, skills), Start, world map, first steps, first save (`SAVE`).

## Strategy and walkthrough notes
- First goals (source): Highpool (west of the Ranger Center), then the Agricultural Center; Quartz is the first big
  town. Four rangers with Clip pistol/Rifle skills; delete the weak pre-made ones only if needed.
- Combat: one group -> A needs no target; ammunition shows in AMM. RYZ starts with fists equipped and a M1911A1
  .45 pistol plus clips in the pack: W, 1 equips it (verified).
- Encounters are random while walking or waiting (one came after 1000 idle frames at the start).
- Poke money and stats rather than grinding (RAM map). Values stay realistic.

## Naming
Main character RYZ (the game takes upper case only, verified with plain and shifted keys). `RYZ` macro: delete
member 1 (Hell Razor), Create, accept the roll, `type:ryz`, M, nationality 1 (U.S.), skills 3 (Clip pistol),
6 (Rifle), 9 (Perception), RETURN, Y. The other three pre-made rangers keep their names (Angela Deth, Thrasher,
Snake Vargas); the owner's names condi/ebo/... would need three more deletes and creates (same macro pattern).

## Shortcuts
| What | How (tokens / prefix / code) | Source | Status |
|---|---|---|---|
| Stats | `poke:F80E=ST,IQ,LK,SP,AGL,DEX,CHR` on a member record (RYZSTATS) | RAM | verified (sheet shows them) |
| Money | `set:F815=6713:3` (record +0x15, 3 bytes, little-endian) | RAM | verified ($=6713 on the sheet) |
| Disk-swap trick | swap a play side for an untouched copy to reset its maps (loot, NPCs) | source (guide) | not tried |
| Character editor | disk:9 "WASTELAND EDITOR" (needs booting from disk 9; the backend always boots disk 1) | dump | not tried |
| Debug / codes | none found (TCRF has no Wasteland C64 page; no C64 codes on gamehacking.org found) | | |

### Saves (rom/saves/c64/wasteland/, never committed)
| Name | Contents | Route | Status |
|---|---|---|---|
| 01_start | play side 1 (WASTLND4 image only) with RYZ, Angela Deth, Thrasher, Snake Vargas one step east of the Ranger Center | made in a live play session (`@step1,SAVE`) | loads: `sav:01_start,TITLE,CONT` -> world map x56 y62, RYZ stats kept (verified) |
The party save lands on track 35 of side 1 (sectors 0-2, 6-8, 12-13), not as plain text.

## RAM map (for `game.json` "ram" watches and pokes)
| Address | Size | Meaning | How found |
|---|---|---|---|
| F400 | 256 | party block; F401-F407 = order (record numbers, 1-based), F408/F409 = x/y on the world map (a copy: writing does not move the party) | diff + poke (verified) |
| F4D1 | 12 | current location name ("Ranger Ctr.") | dump |
| F500 + 0x100*(n-1) | 256 | character record n (record numbers as in F401): name 0x00 (14 bytes, ASCII, 0-terminated), ST IQ LK SP AGL DEX CHR 0x0E-0x14, money 0x15 (3 bytes LE), sex 0x18 (1 = female), max CON 0x1B (2), CON 0x1D (2), skill points 0x20, rank text 0x33 ("Private"), skills 0x80 (pairs: skill number, level), items from about 0xBD (pairs) | dump + pokes (verified: stats, money, CON) |
| 0057/0058 | 1+1 | x/y working copy (zero page); poking it alone does not move the party either | diff |
| 09EC/09EE, 09FB | 1 each | x/y as operands of LDX#/LDY# and LDY# (self-modifying code); with $57/$58 and F408/F409 they make the warp | find + poke (verified, `WARP`) |
| F40A | 1 | current location number (0 world, 1 Quartz, 0C Las Vegas, 15 Darwin, 1A Needles, 23 Citadel, 07 Sleeper Base, 10 Cochise); F40B/F40C world square entered from | dump diff (verified) |
| 4DEA-4E9E | | world entry records `4N XX YY LL` (action, arrival x, y, location), `ff`-separated; Darwin's first at 4E7D; hidden ones `4b 0e 01 07 0a 29`, `4b 10 1e 10 0a 2a` | dump (RAM, poke verified) |
| 3600 / 3C00 | 1024 / 4096 | current map: 32x32 locations at $3600, 64x64 (world, Needles, Las Vegas) at $3C00; values 0 open, 1 wall, others event squares | dump + specials survey (verified) |
Pokes into a record before LEAVE are written with the party (RYZSTATS survives LEAVE and a save/load).

## Emulation notes
- PAL `c64`, default joystick port (unused: keyboard game). No fast loader trouble; loads are 1500-2000 frames
  each at real 1541 speed.
- **Determinism problem (tools, 2026-11-21):** routes replayed from power-on are deterministic (two flat runs
  pixel-identical), and checkpoints themselves reproduce, but play **continued from a loaded state** differs from
  the same route replayed from power-on: `@start,w1000` has "3 Animals" at power-on replay and nothing from the
  cache (`tools/cachecheck.py` "cold/hit DIFFERS from flat (frame, memory)" for `@start,w1000`, `@step1,w1000`,
  `@start,E,s,w300,n,w1000`); in a play session the RYZ roll differed from the replay. Something that drives the
  game's random numbers is not in the savestate. Until the backend is fixed: write chance-dependent checkpoints
  as full routes from power-on, run `cachecheck.py` on every new checkpoint, and expect preview/play results
  from `@checkpoint` routes to differ from shots in encounters and rolls.
- The title screen keeps typing new lines after "Status: DEFCON 1"; `TITLE` stops at f1900.

- 2026-11-22 capture: no divergence between cached and power-on states seen (start set 49/49 and main set
  verified from an empty cache; checkpoints built on parents, including chance-dependent ones such as `s_won`).
  The macro `EVY` mentioned in Capture notes was removed again.

## Checkpoints
`title` -> `rangers` -> `party` is a chain; `start`, `step1` and `fight` are full routes from power-on
(`TITLE,NEWGAME,settle,RYZ,RYZSTATS,LEAVE,ORDER4,settle` + `E` / `w1000`), because built on the cached `party`
or `start` they came out different from the power-on replay in some cachecheck runs and equal in others. All six
reproduce (`python3 tools/cachecheck.py wasteland --flat leaves`, 2026-11-21; run it with `--fix` after any
change, a stale state in your own cache shows as "yours DIFFERS").

## Sources
| Source | URL | Used for | Accessed |
|---|---|---|---|
| Per Jorner, The Nearly Ultimate Wasteland Guide (archive.org text) | https://archive.org/stream/wasteland1walkt/Wasteland%201%20Walkthrough_djvu.txt | C64 notes (play disks, saving, Esc key), location order, disk contents, cheats | 2026-11-21 |
| Web search summary of the C64 reference card (mocagh.org, host not reachable here) | https://mocagh.org/ea/wasteland-refcard.pdf | Utils: copy all four sides, Restart, boot from the original | 2026-11-21 (search snippet only) |
| MobyGames trivia (search snippet) | https://www.mobygames.com/game/c64/wasteland/trivia | two double-sided write-protected disks, play copies | 2026-11-21 |
| comp.emulators.cbm (search snippet) | https://groups.google.com/g/comp.emulators.cbm/c/DKhz1s3uXqE | the copy routine marks the last sector | 2026-11-21 |
| GameFAQs C64 FAQ list | https://gamefaqs.gamespot.com/c64/572212-wasteland/faqs | 16 guides listed; guide pages answer 403 (unavailable) | 2026-11-21 |
| wasteland.fandom.com, mocagh.org | | not reachable from this container (DNS) | 2026-11-21 |

## Open questions
- ~~Highpool's entrance: no world-map decoding yet~~ solved 2026-11-22: the map is the 64x64 grid at $3C00 (Read first).
- ~~A real warp~~ solved 2026-11-22: poke all copies together (macro `WARP`, Read first); $5D/$5E is not a row pointer to poke.
- What the Utils Copy / Restart screens look like; what N at "Use last saved game" writes to the sides.
- The editor on disk:9 (would need a boot from disk 9).
- Hidden RNG state not in savestates (above).

## Capture notes (2026-11-22)
- World map icons in the $3C00 grid (x, y, value): (36,55) 7 Agricultural Center; (47,59) 8 Highpool; (24,30)-(25,31)
  9-12 a 2x2 town; (21-23,16-18) 13-20 a 3x3 place; (57-58,36-37) 28-31 a 2x2 place; (36,48) 27; (32,52) 25;
  (13,58) 26; 13 = river current squares along x25-28; 4/5/14/15 scattered (unidentified).
- Encounters: the honest chain met 4 Animals (Wild Canines) after `w1000*10` at x50 y57 (`s_won`); the poked
  chain meets 3 Animals (Radioactive Vermin) after w1000 at the Ranger Center (`fight`).
- Battle round: orders per conscious ranger, then `y`; give `w2500`-`w3000` for the report. One `y` too many in
  a repeated macro desynchronises the orders (a macro `EVY` = `e,w300,y,w600` repeated stalled at the last ranger; removed).
- Shop: `1,w400` picks the ranger, `b,w600` Buy list, `s,w600` Sell list, a digit buys at once.
- Infirmary: `1,w300` shows the recommendation (Exam $25; Healing for the wounded).
- Highpool workshop: Perception on the cot found nothing (both on it and eastwards).
- Saves: `02_highpool` (rom/saves, honest party after the start set, in Highpool) loads with `sav:02_highpool,TITLE,CONT`.

## Capture notes (2026-11-22, run 2: sides 2-4)
- Location numbers by side (from the Insert prompt with Darwin's record poked): side 1 (no prompt) 08 09 0A 1D 2B 31;
  side 2 01 02-06 1A 1B 1C 1F 20 21 22; side 3 0B 0C 18 19 23 24 26-2A; side 4 07 0D 0F 10-17; 0E, 1E, 25, 2C ask for "side 0" (unused).
- Identification of 07 (Sleeper Base: purple halls, Nailed Wolves, slot doors) and 10 (Base Cochise grounds: "A weapon pod
  rises up from the base dome", robot groups) is by content, not by a name on screen (F4D1 is not updated).
- Quartz specials: six manholes, street signs, Stagecoach Inn (x16 y15), Scott's Bar (x21 y28, rear x22 y29), the graveyard
  ghouls (x27-28 y25-27), closed businesses; the Emporium (bottom left, guide) was not found among them.
- Needles: the 64x64 map's event squares mostly show nothing; only the waste pit (x12 y55) and "Leaving Needles" found.
- Every warp target on the Cochise grounds starts a robot fight (no quiet dome view).
- Saves: `03_quartz` (party saved in Quartz x20 y13), `04_cochise` (party saved on the Cochise grounds); load with
  `sav:NAME,TITLE,CONT` (not tried).
