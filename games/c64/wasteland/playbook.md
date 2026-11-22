# Wasteland (C64) - playbook

Everything an agent needs to play this game efficiently: read it before playing, add to it after every run.
Status of each fact: **verified** (seen in the emulator, with the route) or **source** (manual/FAQ/wiki, not yet
checked). Never delete a fact that turned out wrong: strike it and say what is true.

## Read first
- **Start:** `python3 tools/play.py start wasteland --route @start` (world map at the Ranger Center, party RYZ,
  Angela Deth, Thrasher, Snake Vargas, ryz first). Model `c64` (PAL). Needs `rom/wasteland.zip` (9 D64s,
  `disk:1`..`disk:9` = WASTLND0..8). Boot is from master side 1 (disk:1, automatic); **play happens on the
  play copy of side 1, `disk:5`** (WASTLND4): the masters (disk:1-4) are refused as play disks.
- **Macros:** `TITLE` (w1900, title with Place/Year/Status typed), `NEWGAME` (title -> Ranger Center screen with
  the four default rangers), `RYZ` (delete Hell Razor, create RYZ), `RYZSTATS` (pokes realistic stats),
  `LEAVE` (Ranger Center Start -> world map), `ORDER4` (put member 4 first), `N S E W` (one step, keys I K L J),
  `SAVE` (field Save), `CONT` (title -> continue a saved game), `NEWFRESH` (title -> new game through the
  N answer, all four sides), `ROLL` (reroll at character creation).
- **Checkpoints:** `title`, `rangers` (Ranger Center, default party), `party` (RYZ created), `start` (world map,
  first control), `step1` (one step east), `fight` (random encounter "3 Animals"); the last three are full
  routes from power-on (see Checkpoints).
- **Keys:** keyboard only (cursor keys and joystick do nothing on the map, verified). Move I/J/K/L =
  north/west/south/east. Field: U Use, E Enc, O Order, D Disband, V View, S Save, R Radio, digits 1-7 = character
  sheet (RETURN pages stats -> items -> skills -> map), SPACE toggles the roster, **Esc = `leftarrow`** (closes
  windows; on the map it passes time). Combat: R)un U)se H)ire E)vade A)ttack W)eapon L)oad/Unjam, then
  "Use these options (Y/N)?" Y.
- **Traps that cost calls:**
  - **Loaded states drift from power-on replays** (random encounters, rolls): `@start,w1000` meets "3 Animals"
    when replayed from power-on but not when built from the cached `start` (cachecheck: memory and frame
    differ). Every checkpoint that depends on chance must be written as a full route from power-on (like
    `fight`), and checked with `cachecheck.py`. See Emulation notes.
  - Character creation rolls change with any timing change: that is why `RYZSTATS` pokes the stats.
  - Names are upper case only (the game shows RYZ; shift does not help).
  - Loads are long and silent: the waits in the macros are measured (`NEWGAME` about 6000 frames).
  - Map positions F408/F409 are a copy: poking them does not move the party (no warp yet).
- **State:** scouted 2026-11-21, nothing captured. Highpool (first town, just west of the Ranger Center) not
  reached yet: it is ringed by mountains on the screens seen; finding its entrance is the capture's first job.

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
Targets for `main` (ids, category):
- [ ] `title_screen` title (`@title`); `title_globe_credits` boot (intake frame f1200); `title_utils` menu (U)
- [ ] `menu_continue` menu ("Use last saved game (Y/N)?"); `menu_insert_side` menu ("Insert side 1")
- [ ] `rc_roster` menu (`@rangers`); `rc_create_roll` system; `rc_skills` system; `rc_nationality` menu; `rc_delete` menu
- [ ] `world_start` gameplay (`@start`); `env_world_mountains`, `env_world_lake`, `env_world_desert` gameplay
- [ ] `hud_world_roster` hud (map + roster + clock + command bar)
- [ ] `char_stats`, `char_items`, `char_skills` inventory (digit, RETURN, RETURN)
- [ ] `field_use`, `field_order`, `field_radio`, `field_enc` menu (prompts); `map_edge_message` dialogue
- [ ] `battle_appears` battle (`@fight`); `battle_menu` battle; `battle_weapon` battle; `battle_round_msgs` battle (timeline); `battle_xp` battle
- [ ] `loc_enter_prompt` gameplay ("Enter new location (Y/N)?"); Highpool town, a shop, an NPC talk, the library/doctor (play)
- [ ] later towns (Quartz, Needles, Las Vegas) by play or by the disk-swap trick (below); `save_prompt` save; `gameover` (party dead)
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
- Highpool's entrance (and every other location's square): no world-map decoding yet; the map is drawn from
  data that is not a plain 64x64 grid in RAM (row pointer $5D/$5E, data around $4B00-$4F00 looked at).
- A real warp: F408/F409 and $57/$58 are copies; find the master position (or the location-entry code).
- What the Utils Copy / Restart screens look like; what N at "Use last saved game" writes to the sides.
- The editor on disk:9 (would need a boot from disk 9).
- Hidden RNG state not in savestates (above).
