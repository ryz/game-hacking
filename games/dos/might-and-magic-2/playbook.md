# Might and Magic II: Gates to Another World (DOS) - playbook

Everything an agent needs to play this game efficiently: read it before playing, add to it after every run.
Status of each fact: **verified** (seen in the emulator, with the route) or **source** (manual/FAQ/wiki, not yet
checked). Never delete a fact that turned out wrong: strike it and say what is true.
"ROM text" = read from the game's own area texts in memory after a warp (`tools/texts.py`), not from the web.

> **Tools moved (2026-11-20).** Where this playbook says `try.py`, `cachecheck.py` or `screen.py` (copies that
> lived in this game's `tools/`), use the shared tools: `python3 tools/preview.py dos/might-and-magic-2 FILE` (`--frames K` is now
> a `?` mark inside the route or `--timeline N:STEP`; sheets in `work/preview/dos/might-and-magic-2/`), `python3
> tools/cachecheck.py dos/might-and-magic-2` (`--after TOKENS` for a save in the game, `--peek ADDR:LEN` for party tables) and
> `python3 tools/play.py text` / `preview.py --text` for text screens. Pictures are native size
> (`play.py shot --scale N` on demand).

## Read first
- Boot: `TITLE`, `MENU`, `PARTY` (all in `game.json`); checkpoints `start` (party in the inn), `middlegate`
  (street), `vet`/`hero` (strong parties, pokes) and the honest `s_...` chain of set `start` (below).
- Moving: `AT:x:y` + facing + `left` (poke); `WARP:map:x:y` between areas; walking routes from the wall map
  (RAM 161D6, "Walking honestly" below).
- Waits: turn `w100`, step `w150`, menus `w150`, area load `w300`, event prompt `w250`. Keys typed early are kept.
- Traps: the creation roll follows frame timing (anything before `RYZ` changes it); the Middlegate cats fight
  (8,1) is walled in (poke only); a new party has 0 gold; ten Orcs at C2 (2,5) beat a level-1 party.
- Sets: `main` (228, pokes allowed), `start` (52, honest, `work/shots/.../start/shots.txt` -> published).
- Open: hireling hire, Cartographer map, shrines, bashing, own time travel; a won fight with a new party.

## Identity
| Field | Value |
|---|---|
| Title (EN / original) | Might and Magic II: Gates to Another World (title picture "Might and Magic Book Two"; options screen "MIGHT and MAGIC Book Two Gates To Another World!", "Copyright 1989 New World Computing, Inc") (verified) |
| Platform / model used | IBM PC / MS-DOS, `svga-8000` (`game.json`); the game picks its 16-colour (EGA) graphics itself, 320x200 (verified) |
| Release (region, year) | Apple II 1988, MS-DOS 1989 (Wikipedia: 1988-1990 computer ports); this dump is the owner's GOG folder, "IBM Version By Inside Out Software, Inc." "Version 1.01" (About screen, verified) |
| Developer / publisher | New World Computing; design Jon Van Caneghem; IBM version Inside Out Software (John R. Fachini, Douglas Wike, Kurt Boutin); music and sounds Raoul Kraushaar (About screen, verified) |
| Genre | First-person party RPG, 16x16-square areas, text-menu combat, time travel |
| Players / save system | 1 player; roster of 24 characters + hirelings; party of up to 6 created characters + hirelings, 8 at most; **save = sign in at an inn**, which writes `ROSTER.DAT` (8,292 bytes stock, 8,293 once written) (verified) |
| Dump | `rom/might-and-magic-2.zip` (GOG install folder, 117 entries; SHA-1 in `game.json`); programs `MM2.EXE`, `unins000.exe` |

## Boot sequence
Macros (all in `game.json`): `BOOT`, `TITLE`, `MENU`, `RYZ`, `RENAME:letter:name`, `NAMES`, `JOIN`, `PARTY`,
`RESUME`, `AT:x:y`, `FN FE FS FW`, `WARP:map:x:y`, `CAST:member:level:number`, `LIGHT`, `LIT`, `YEAR:n`.
Checkpoints `title`, `menu`, `start`, `signed_in`, `middlegate`, `outdoors`, `cavern`, `combat`: all rebuilt from
an empty cache 2026-11-19, frames and the written `ROSTER.DAT` identical to cache hits (also a sign-in after a
cache hit of `start` against the same keys from power-on: same roster, same frame).
- Intake probe: `work/intake/dos/might-and-magic-2/sheet.png` shows only DOSBox Pure's start menu.
- **verified 2026-11-19: the game needs `loadfix -4`.** Started from the start menu (`w120,enter`) MM2.EXE prints
  "MM2: Not enough memory for 16 color version. Release TSRs and retry." and quits. GOG's own
  `dosboxMM2_single.conf` runs `loadfix -4 mm2.exe` (4 KB of low memory taken before the program: a known
  free-memory check that fails when there is too much). `BOOT` therefore goes through the command line:
  `w120,down,down,enter` ("Go to Command Line"), `type:cd MIGHIC-2\n` (DOSBox Pure's short name of the folder
  "Might and Magic 2"), `type:loadfix -4 mm2.exe\n`. Savestates, checkpoints and the cache work with this
  launch as with a start-menu launch (checked, see above).
- **verified** The game chooses the 16-colour version by itself (no prompt; `.16` files, EGA driver); the `.4`
  files (CGA, 4 colours) are only used when it cannot. With `ega-8000` the frames are the same 320x200 16-colour
  pictures; `vga-8000` gave a 320x400 frame in one emu.py run (not looked into). Keep `svga-8000`.
- **verified** Power-on to title: `TITLE` = `BOOT,w300`: "New World Computing Presents..." logo (about 30 frames
  after the command), then the title picture (pegasus, "Might and Magic Book Two"), animated (tree creature,
  pegasus tail). Any key -> the opening options screen ("S - Start Game, C - Copy Player Disk, A - About Book
  Two, D - Disk 2 - Drive C"); `s` -> **Main Options** (`C` create, `V` view all, `T` transfer, `G` go to town).
  `MENU` = `TITLE,esc,w200,s,w300`.
- **verified** `PARTY` = `MENU,RYZ,NAMES,JOIN` (one `do` from power-on, checkpoint `start`): Middlegate inn,
  party ryz, condi, ebo, cubi, deddo, mnz, facing the door. Stepping out (`up`) shows "The spirit of Corak
  proclaims, ..." with "('Space' to continue)": keys other than Space are swallowed there. Checkpoint
  `middlegate` = `@start,up,w150,space,w150`.
- **verified** Saving: in the inn turn around (`right,w100,right,w200` from `start`): "A jolly old innkeeper ...
  'Will you sign the registry (y/n)?'"; `y` writes ROSTER.DAT and shows the inn list "(1-Middlegate)" with the
  party ticked and "('ESC' to exit to DOS)". Checkpoint `signed_in`, save `saves/01_start.sav`.
  `sav:01_start,RESUME` = power on with that roster, `G` (the last party is already ticked), `Z` = party in the
  inn (verified).
- **verified** The game reads `ROSTER.DAT` of its own folder: the stock roster has the six premade characters of
  `DEFAULT.DAT` (A Sir Felgar H-Orc Knight, B Terwin III Dwarf Paladin, C Sure Valla Archer, D Gene Eric Gnome
  Cleric, E Cassandra Sorcerer, F The Hermit Robber) and, in the hireling records, Sir Hyron, Drog, H K Phooey,
  Thund R. (not available at the start: the hirelings list is empty). `cloud_saves/ROSTER.DAT` (GOG's cloud-save
  overlay, dated 2019-12-11) holds the same six plus the Might and Magic 1 stock party transferred (Crag The
  Hack, Sir Galand, Zenon Iii, Swifty Sarg, Serena, Wizz Bane) and a test character "Asdf": somebody's played
  copy; our launch does not mount it, so the game never sees it. Neither file is committed.

## Controls
Every screen prints its own keys; single keystrokes, Enter only after names and numbers.
| Context | Key | Action | Status |
|---|---|---|---|
| Title | any key | opening options (`s` start, `a` about/credits, `c` copy disks, `d` disk-2 drive) | verified |
| Main Options | `c` / `v` / `t` / `g` | create / view all / transfer from Might and Magic 1 (asks for the path of ROSTER.DTA) / go to town | verified |
| Create | `enter` | re-roll the seven statistics | verified |
| | `a`-`g`, then `a`-`g` | exchange two statistics ("Exchange Stat (A) with stat (A-G)?") | verified |
| | `1`-`8` class (eligible listed), `1`-`5` race, `1`-`3` alignment, `1`-`2` sex, name (10 characters), `enter` saves at once (no Y/N) and rolls the next character | | verified |
| | `esc` | back one step / to the menu | verified |
| View all, inn list | `a`-`x` profile; `space` characters/hirelings | | verified |
| Profile (from menus) | `ctrl>n` rename (type, `enter`), `ctrl>d` delete | rename verified, delete source |
| Inn list | `ctrl>a`.. add/remove (tick), `z` exit into the town (shown as "'Z' to exit" once one member is ticked), `1`-`5` other towns, `esc` to DOS (after sign-in) or menu | add, `z` verified |
| Exploration | `up` / `down` | step forward / back | verified |
| | `left` / `right` | turn 90 degrees (a turn also fires the event of the square, like a step) | verified |
| | `enter` | forward (manual) | source (no visible move in one try; not needed: `up` steps) |
| | `b` bash, `c` controls (sounds, walk beep, disposition Inconspicuous / Average / Aggressive / Thrill Seeker, delay 0-9), `d` dismiss hireling, `e` exchange, `q` quick ref, `r` rest ("Rest here? (Y/N)"), `s` search ("Nothing Here!"), `u` unlock ("Not Locked!"), `p` protect (light, magic, forces), `m` location (coordinates; the map needs a Cartographer), `1`-`6` profile | | all verified; `b` in front of the inn door walks the party out into the street (no locked door was found to bash) |
| Profile (in play) | `q` quick ref, `c` cast, `d` drop, `e` equip, `g` gather (gold, gems), `r` remove, `s` share, `t` trade (gold, gems, food, item), `u` use, `esc` | | all prompts verified |
| Cast | `c`, level, number, `enter` ("'Return' to cast"); the Spell Book shows the known spells | | verified (deddo Light: `CAST:5:1:5`) |
| Prompts | `y` / `n`; `space` continues messages | | verified |
| Encounter | `a` attack, `b` bribe (1 food, 2 gold, 3 gems), `h` hide, `r` run | | all verified: hide failed into combat once, run left the fight and put the party back on the map |
| Combat | `a` attack, `f` fight (target in reach A-E), `s` shoot (any target), `c` cast (level, number, target or Enter), `u` use, `b` block (silent), `r` run (that member leaves the fight alone), `e` exchange (two digits), `v` view (own profile, `v` spell book); `d` opens Controls (delay), `p` protection spells, `q` quick reference; `ctrl>a` quick fight (the member's default action) | | all verified 2026-11-19 (`@vet_cats`); options depend on class and rank: only members 1-2 get attack/fight, members 3+ shoot |

Input timing: the default press works everywhere. The game reads the BIOS keyboard buffer: **a key typed early
is kept for the next screen**; wait for each screen. Waits that worked at 8000 cycles: turn `w100`, step `w150`,
menus and profiles `w150`, town or area load `w300`, event prompt `w250`, stairs and gates `w400`.

## Game structure
- **World of Cron** (verified with `WARP` and the area texts): 60 areas, each 16x16 squares, x east, y north,
  (0,0) south-west. Area ids (hex) and what is in them:
  | Ids | Kind | Areas |
  |---|---|---|
  | 00-04 | towns | 00 Middlegate, 01 Atlantium, 02 Tundara, 03 Vulcania, 04 Sandsobar (inn town selection `1`-`5` = ids 0-4: code) |
  | 05-10, 21-28 | outdoors, a 5x4 grid that wraps around (neighbour table) | row 1: A1 05, B1 06, C1 07, D1 08, E1 21; row 2: A2 09, B2 0A, C2 0B, D2 22, E2 23; row 3: A3 0C, B3 0D, C3 0E, D3 24, E3 25; row 4: A4 0F, B4 10, C4 26, D4 27, E4 28. Middlegate is in C2 (gate at C2 (7,3)), Tundara A1, Vulcania E1, Atlantium A4, Sandsobar E4 (cluebook; texts match: E1 "Vulcania swelters before you", E4 "sits Sandsobar") |
  | 11-20 | caverns (dark) | verified 2026-11-19 by their texts and exits: 11 under Middlegate, 12 under Atlantium ("Exit to Atlantium"), 13 under Tundara, 14 under Vulcania, 15 under Sandsobar, 16 Corak's Cave (Corak's Crypt, Lloyd), 17 under Square Lake (final gate, "Stairs lead back to Square Lake"), 18 Ice Cavern ("Reenter the Tundra"), 19 Sarakin's Mine, 1A Murray's Cavern, 1B the Druids' cavern (Coven Headquarters), 1C the class-quest cavern (Paladins Only, G.H.Q.), 1D Dragon's Dominion, 1E Dawn's Mist (Element Orb), 1F Gemmaker Volcano, 20 Nomadic Rift |
  | 29-2C | elemental planes | 29 Air (Lord Shalwend), 2A Fire (Lord Pyrannaste), 2B Earth (Lord Gralkor), 2C Water (Lord Acwalandar): each has a shrine opened with that element's Disc, giving the Talon (ROM text) |
  | 2D-36 | dungeons below the castles, two levels each (8) + the two wizards' towers | order inferred from texts: lords' dungeons of Hillstone (Slayer), Woodhaven (Hoardall), Pinehurst (Peabody), Luxus Palace (Lamanda); 35 Dark Keep (Ybmug), 36 Tower of Mercy (Yekop) |
  | 37-3B | castles | 37 Hillstone (Lord Slayer), 38 Woodhaven (Lord Hoardall), 39 Pinehurst (inferred), 3A Luxus Palace Royale (Corak's Study), 3B Castle Xabran (the four Discs; list of spell locations) |
- **Time** (verified): Day and Year on the status line; the game starts in year 900; areas change with the
  century (Castle Xabran stands in C2 at (14,8) in year 800, "Ruins of a mighty castle" in 900). Time travel is
  part of the quest (King Kalohn and the Mega Dragon in the 9th century, C4 (14,5): ROM text).
- **Middlegate** (all verified with `tools/scan.py 00`; square, facing):
  | Square | What |
  |---|---|
  | (7,3) S | Middlegate Inn: sign in (start square, party faces N) |
  | (4,4) W | S.J. Blacksmith (Svendegard), sign (5,4) |
  | (4,6) W | Slaughtered Lamb tavern (waitress, drinks), sign (5,6) |
  | (7,7) N | Gateway Temple (cleric), sign (7,6) |
  | (10,7) E | Turkov's Training (squires), sign (9,7) |
  | (1,12) W | Sleepy's Mage Guild enrolment (20 gold); (7,14) N sages sell spells; sign (7,13) |
  | (1,8) W | Lock and Key LTD: locksmith, key 500 gold; sign (2,8) |
  | (0,5) W | The Poorman's Portal: to Sandsobar for 10 gold; sign (1,5) |
  | (14,8) E | Travel Moore: Joan books Murray's Resort Isle, 5,000 gold; sign (13,8) |
  | (0,15) W | Otto Mapper: Cartographer skill, 10 gold; sign (1,15) |
  | (1,9) W | Track and Trail: Pathfinder, 2,000 gold; (3,12) E Edmund's Expeditions: Mountaineering, 2,000 gold |
  | (12,10) S | Brain Detoxification: removes all secondary skills, 100 gold |
  | (10,2) W | Nordon the wizard: "Will you do me a service (y/n)?" |
  | (8,4) S | fountain of clairvoyance; (15,15) Feldecarb Fountain |
  | (13,6) S, (14,6) S, (13,2) | Arena ("Arena Entrance Only", "Exit Only"; "you must have a ticket") |
  | (10,3) N | sign "Skeleton Closet"; (10,4) 13 Skeletons (fixed fight) |
  | (8,1) | 6 Witch's Cats and 4 Rabid Rodents (fixed fight; checkpoint `combat`) |
  | (13,12), (12,14) | Brain Eaters + Merchant; Blood Suckers + Mugger (fixed fights) |
  | (8,0) W | stairs to the cavern (area 11) |
  | (5,15) N | city gates: "Exit (y/n)?" -> C2 (7,3) |
- **Area C2** (`scan.py 0B`, verified): Middlegate portcullis (7,3) S, Guardian Pegasus (7,4) N ("Should you
  discover my name, I will help you once per year. Seek me out in the Ice Tundra"), Corak's Cave entrance
  (5,11) N, cave "Chosen Ones only" (10,7) N (Square Lake), ruins of Castle Xabran (14,8), ferries (5 gold),
  river walker (11,1) W (Walk on Water, 50 gold), fountains, Magic Monster Pit (4,4) S, signposts, orcs.
- **Square Lake (area 17)** (`scan.py 17`, verified): a diagonal of twelve fixed fights from (15,1) to (4,12)
  (Phantasms, Carnage Spirits, Nasty Witches, Gargoyles, Wraiths, Iron Wizards, Guardians, Mummies, Court
  Jesters, Warbots, Mystic Clowns, Alien Probes), 66 Devil Kings at (11,14), a gate at (0,15) E "You shouldn't
  be here until you save the King in the 9th century", a row of joke signs along y=15 ("Hello!" ... "Just
  kidding!" ... "This is IT!!!!!" at (15,15)), Beliaeff's Beastiary sign (1,0).
- **Main quest** (ROM text and cluebook; the end verified 2026-11-19, see "The ending" below): class quests for the Jurors of Mount Farview (D2 (7,0));
  Queen Lamanda's Triple Crown (Black Tickets to the Arena, Monster Bowl and Colosseum); the four Discs in
  Castle Xabran (9th century) open the shrines of the elemental planes, which give the four Talons; King
  Kalohn's Element Orb (in Dawn's Mist cavern); in the 9th century give Kalohn the Orb and the Talons at C4
  (14,5) so he wins against the Mega Dragon; "Return to the tenth century for further instructions at Luxus
  Palace Royale"; then Square Lake (gate at (0,15)). The ending itself (what fires it, its text) is not known
  yet: Wikipedia says the last dungeon ends with the party escaping the planet by spaceship.
- **Characters** (manual, verified on screen where noted): statistics Might, Intellect, Personality, Endurance,
  Speed, Accuracy, Luck; classes Knight, Paladin, Archer, Cleric, Sorcerer, Robber, Ninja, Barbarian (all eight
  listed on the creation screen, verified); races Human, Elf, Dwarf, Gnome, H-Orc; alignment Good, Neutral,
  Evil; secondary skills (two per character: Arms Master ... Soldier, manual); hirelings (pay per day); spell
  levels 1-9, 48 cleric + 48 sorcerer spells.

## The ending (verified 2026-11-19)
1. King Kalohn: year 800, C4 (14,5) facing N with the Element Orb (DF) and the four Talons (DB-DE) in a backpack:
   `@hero,YEAR:08,WARP:26:0E:04,poke:18966=DFDBDCDDDE,up,w250` asks, `y,w300` = he wins; this sets record
   +0x81 bit 02 for every party member (script op `18 00 7F FD 02`). Without the items he dies and the Mega
   Dragon attacks.
2. Square Lake gate: area 17 (0,15) facing E (`LIT,WARP:17:02:02,...,AT:00:0F,FS,left,w250`). It tests +0x81
   bit 20 ("save the King": nothing in the area scripts sets it; the capture pokes it). `MARKS` pokes 0x23 =
   bits 01 (Chosen One: C2 cave and the Devil Kings), 02 (Kalohn), 20 (gate) into all six records.
   Checkpoint `sheltem` = HERO party at the gate.
3. Sheltem (500 HP) and four Elementals (250 HP each); monster HP words at 1A7AA (5 x 2 bytes); the route
   pokes `poke:1A7AA=28002800280028002800` (40 each) and then `BATTLES:2316:11` (the gate zeroes both
   counters at 10C10/10C12: findings) and finishes with `w100,ctrl>a,w150` steps.
4. Control room: type `WAFE` + Enter (fixed code, from 2SMITH.OVL at offset 0x1342: compare with DS:45FC).
5. Cryptogram: the answer is "Preamble" enciphered with a random 26-letter key (DS:584E, physical 1604E);
   the enciphered answer is at physical 160AE (8 letters, case kept): read it with `play.py peek 160AE 9`
   once the cryptogram shows and type it. The route of `ending_answer_typed` gives `Uqkcypvk` (deterministic
   for that route; any change before it changes the key). 15-minute real clock (DS:436/438 ticks).
6. Congratulations, then the inn list; the game writes ROSTER.DAT (save `04_ending`). Each member gets bit 08
   in +0x81 and 50,000,000 experience.

## Shot plan
Target: the whole game to the ending, in the three lenses (see `shots.txt` for the planned ids and how to reach
each; about 150 shots). Reach everything with `WARP` (+ `YEAR` for other centuries, `LIT` for dark areas) and
pokes, then scan the area (`tools/scan.py MAP`) and pick the frames.
Status 2026-11-19: **captured, set `main` 228 shots** (`shots.txt`); every group below is done except where
noted. Not captured: hiring a hireling, the automap of a Cartographer, the shrines of the planes (the disc
prompt did not fire on the first tries), a bashed locked door, time travel by the game's own means.
- [x] Boot and menus: NWC logo, title, opening options, About, Copy Disk, Main Options, View All, hirelings
  list, profile, rename, Transfer prompt (8-10).
- [x] Creation: roll, exchange stat, class, race, alignment, sex, name (6).
- [x] Inn and town: inn list, exit, spirit of Corak, Middlegate street, every Middlegate service (blacksmith
  buy/sell lists, tavern menu and rumor, temple menu, training, mage guild and spell purchase, locksmith,
  portal, travel agent, Otto Mapper, skill trainers, detox, fountains, arena), sign-in (25).
- [x] Exploration commands: controls menu, protect panel, quick ref, rest, search (chest, treasure), bash,
  unlock, location and auto-map with a Cartographer, Wizard Eye / Eagle Eye 5x5 view, dismiss, exchange (12).
- [x] Combat: encounter options, combat screen, attack, fight, shoot, cast (several spell families), block, run,
  hide, bribe, quick fight, victory and experience, treasure, a death, game over (16).
- [x] Each environment once: 5 towns, outdoor terrains (grass, forest, mountains, tundra, desert, swamp, water,
  roads), a cavern, a castle, a dungeon, the four elemental planes, the Dead Zone (D1), Murray's Resort Isle
  (20+).
- [x] Opponents: about 25 groups across the families (Square Lake's twelve, the elemental lords, Mega Dragon,
  Dread Knight, Baron Wilfrey, Dawn, Lich Lord, Devil Kings, Sheltem if met).
- [x] Quest and story: Jurors of Mount Farview, class quest rewards, Nordon / Nordonna, Corak's Soul and Body,
  Castle Xabran discs, shrines and talons, Element Orb, time travel (year change), King Kalohn, Queen Lamanda,
  Triple Crown, Square Lake gate, ending (15).
- [x] Progression: training (level up), spell level gained, secondary skill learned, hireling hired, ageing,
  temple cure (8).
Set `start` (2026-11-20): 52 shots, power-on to the first sign-in, played honestly (see "Set start").
Distinctive for this game: the 16-colour first-person view with full-screen monster pictures in encounters,
time travel by centuries, hirelings, secondary skills, arenas, the 5x4 wrap-around world.

## Set start (honest new game, 2026-11-20)
52 shots, `shots/start/`, checkpoints `s_equipped` .. `s_signed` (`checkpoints.txt`), no pokes or warps: the
`PARTY` macro (create ryz, rename the premades with Ctrl-N, tick six) and then only walking and menus. All verified:
- Equip from the profile: `@start,1,w150,e,w150,a,w150` = Short Sword equipped (checkpoint `s_equipped`).
- Walk inn -> blacksmith (4,4): `up,w150,left,w100,up,w150,left,w100,up,w150,right,w100,up,w150,up,w250` from
  `s_street`. Blacksmith menu: `a` weapons, `c` armor; `esc` from the menu leaves the shop (from a list it goes
  back to the menu). Temple (7,7) and Turkov's Training (10,7) and the gate (5,15): routes in `s_temple`, `s_gate`.
- Every shop, the temple and training are browse-only: all six start with **0 gold, 0 gems, 10 food** (RAM).
- Outside (`s_c2`): `up` meets the Guardian Pegasus (Space continues); the road runs N on x=7 and W on y=7; forest
  (terrain 64) is "Impassable!". No encounter came in ~45 road steps or ~40 steps on the western grass at
  (3,9)-(3,13); stepping S from (2,7) to (2,5) met **ten Orcs** in every timing tried (4 of 4; surprised in one
  timing, options Attack/Bribe/Hide/Run in the `s_orcs` timing). Orcs have 20 HP each; a Flame Arrow did 4.
- Combat: mnz (Sorcerer) knows level-1 spells 2, 4, 5, 6 (spell book in combat: `v,v`); `c,1,4` + target = Flame
  Arrow. Sorcerers in rank 3+ have no Attack; `ctrl>a,w300` steps (quick fight) play a round for everyone.
- Defeat: after 20 such steps "Death Strikes!", `enter,w400` = inn list, all alive (`s_dead`); ticking the six
  again and `z` = in the inn (`s_resume`), the equip undone; sign in = `s_signed`, save `05_start_honest`.
- No encounters in Middlegate's streets (about 60 steps at several timings) and none while resting there
  ("Rest complete, no encounters.", one food per member).

## Walking honestly (wall map)
RAM 16 1D6 (256 bytes, index y*16+x) holds each square's four sides, 2 bits each: bits 7-6 N, 5-4 E, 3-2 S,
1-0 W; 0 and 2 are passable, 1 and 3 are walls ("Solid!"; building doors are event walls). Outdoors the same
block holds terrain codes instead (00 grass, 10/11/17/18 road, 64 forest, 8A water, 21 mountain: read, not all
tested). A breadth-first search over it gave every walking route of set `start` (scratch script, not kept).

## Strategy and walkthrough notes
- **Moving is one token**: `AT:xx:yy,Fd,left,w250` puts the party on a square and fires its event facing the
  direction one turn left of `Fd` (to fire an event that needs facing D, set the facing one turn clockwise of
  D: N needs `FE`, E `FS`, S `FW`, W `FN`). Example: `@middlegate,AT:07:03,FW,left,w250` = inn prompt.
- **Changing area is one token**: `WARP:mm:xx:yy` (hex) from anywhere outdoors or in a town: it writes the
  east-neighbour id of the current area (16 18C), puts the party at x=16 (off the map) and turns, so the game's
  own edge transition loads area `mm` at (0,yy); then it moves the party to (xx,yy) and turns back (same
  facing as before; the landing square's event fires). Verified for all 60 ids (2026-11-19). A fixed fight on
  the landing square starts at once: pick a free square (`tools/scan.py` does).
- **Dark areas** (all caverns, some others): `LIT` (30 light units, shows as "Light (30)" on the Protect panel)
  or `LIGHT` (deddo casts Light, 1 SP, one unit). The view stays dark until the next turn or step.
- **Other centuries**: `YEAR:08` then a `WARP` (the area reloads for that century; the status line shows
  "Year= 800"). Verified with Castle Xabran (C2 (14,8), year 800).
- **Event squares of an area**: `python3 games/dos/might-and-magic-2/tools/scan.py MAP` (about 20 s) tiles the
  frame after every event square and prints the routes; `tools/texts.py MAP` prints the area's texts and event
  table. Run both first in every new area.
- **Fights**: the fixed fights of Middlegate (`@combat` = Witch's Cats and Rabid Rodents at (8,1)); level-1
  characters do not survive the bigger ones. Make the party strong by poking the records (RAM map) with
  realistic values, as for Might and Magic 1 (`VET` there).
- **Party macros** (2026-11-19, generator `work/mm2/mkparty.py` was a scratch script; the values are in
  game.json): `VET` = levels 10-11 (Knight/Robber 576,000-768,000 exp, others per class), HP 41-96, spell level
  5 for deddo and mnz, basic gear equipped in the game (`e,a` per item), 487 battles won; `HERO` = levels 29-32,
  HP 132-287, spell level 9 (casters) / 6, magic gear, 2,316 battles won. Each is `xxxP` (pokes) + `xxxEQ`
  (equips). All six profiles were read on screen (party sheet, try_party). Checkpoints `vet`, `hero`.
- **Experience thresholds** (training screen, exp 0): Knight/Robber level 2 1,500, 11 576,000, 12 768,000,
  32 27,072,000, 33 30,144,000; Paladin/Archer/Sorcerer 10 512,000, 11 704,000, 29 19,520,000, 30 21,056,000,
  31 24,128,000; Cleric 10 384,000, 11 576,000, 30 20,928,000, 31 24,000,000.
- **Find an event**: `python3 games/dos/might-and-magic-2/tools/events.py MAP [REGEX]` prints each event with its
  texts and an `AT` route (faster than scan.py; texts are guessed from the opcodes).
- **Previews**: `tools/try.py FILE --cols N` runs up to ~50 candidate routes in parallel (about 1 minute) and
  tiles them; most of the set was chosen that way, then written into the work shots.txt and shot with
  `shoot.py --only`.
- **Combat turns**: order by speed (at `@combat`: mnz first, then ebo). A sorcerer has no `a` (attack): `a`
  does nothing on its turn; give `b` (block) to pass it (`@combat,a,w300,b,w200` = ebo's options). One early
  try.py run showed ebo after `a,w300,a,w200`; not reproduced (four later runs, cache hit and miss, all mnz).
- **Quests**: many events check class, sex, alignment or quest marks; the Square Lake gate checks the 9th-century
  rescue of King Kalohn. Find the quest-mark bytes in the character records (unknown bytes +2C..+57, see RAM map)
  by diffing a record before and after a quest step, then poke them.

## Naming
Main character **ryz**, then condi, ebo, cubi, deddo, mnz. The game keeps the case as
typed (lower case here; the premade names are mixed case).
- `RYZ` (from Main Options) = create: the first roll after `MENU` from power-on is Might 13, Intellect 17,
  Personality 10, Endurance 16, Speed 10, Accuracy 18, Luck 18 (Knight not eligible); `a`,`b` exchanges Might
  and Intellect (Might 17), then Knight, Human, Good, Male, `type:ryz`, Enter (saves at once), Esc. Result:
  ryz, Human Knight, HP 14, Short Sword in the backpack (verified as one `do` from power-on). The rolls follow
  frame timing: anything changed before `RYZ` changes the statistics.
- `NAMES` = view all, renames B Terwin III -> condi (Dwarf Paladin), C Sure Valla -> ebo (Archer, female),
  F The Hermit -> cubi (Robber), D Gene Eric -> deddo (Gnome Cleric), E Cassandra -> mnz (Sorcerer, female).
  Sir Felgar (A) stays at the inn. The classes follow the Might and Magic 1 party (condi Paladin, ebo Archer,
  cubi Robber, deddo Cleric, mnz Sorcerer).
- `JOIN` = go to town, tick G, B, C, F, D, E (marching order = order ticked), `z`.

## Shortcuts
| What | How (tokens / prefix / code) | Source | Status |
|---|---|---|---|
| Party at the start, saved | `sav:01_start,RESUME` | made here | verified |
| Move in the area | `AT:xx:yy` + `FN/FE/FS/FW` + `left` | RAM | verified (Middlegate, C2, Square Lake) |
| Change area | `WARP:mm:xx:yy` | code (edge transition, see RAM map) | verified (60 ids) |
| Light | `LIT` / `LIGHT` | RAM / manual | verified |
| Century | `YEAR:nn` + `WARP` | RAM | verified (year 800) |
| Gold, gems, food, HP, SP, level, experience, statistics, condition | pokes into the records (RAM map) | RAM | verified on the profile |
| Event scan / area texts | `tools/scan.py`, `tools/texts.py` | tools | verified |
| Debug features, cheat codes | none found (manual has none; TCRF, StrategyWiki and GameFAQs refused the fetch) | - | - |

### Saves (rom/saves/might-and-magic-2/, never committed)
None downloaded (GameFAQs refused automated access). A ROSTER.DAT from the web could be zipped as a `.sav`
(`MIGHIC-2/ROSTER.DAT` inside the ZIP, see `saves/README.md`). Saves made here: `saves/01_start` (new party),
`02_midgame` (VET party), `03_endgame` (HERO party), `04_ending` (after the ending).

## RAM map (for `game.json` "ram" watches and pokes)
Physical addresses; valid for this ZIP, model `svga-8000` and the `loadfix -4` launch. The program's data
segment is at 10800 (DS = 1080): physical = 10800 + offset. Code segment 02FB (physical 2FB0).
| Address | Size | Meaning | How found |
|---|---|---|---|
| 10B92 | 1 | current area id (00-3B); the main loop reloads the area when it differs from the value at the start of a command | dump/diff, disassembly |
| 10B93 / 10B94 | 1 / 1 | party x / y (0-15); x = 10 (16) or FF and y = 10 or FF mean "off the edge": the next command moves to the neighbour area | dump/diff, poke verified |
| 10BCF | 1 | facing as an ASCII letter: 4E N, 45 E, 53 S, 57 W (the master value; the masks below follow it) | dump over four turns; poke verified |
| 161C6 / 161C7 | 1 / 1 | wall mask of the facing (C0 N, 30 E, 0C S, 03 W) / shift (6 N, 4 E, 2 S, 0 W); derived, poking them does nothing | dump |
| 1618B-1618E | 4 | neighbour area ids N, E, S, W of the current area (outdoors; 00 in towns); `WARP` writes 1618C | disassembly (edge routine at code 0xE70E) |
| 16186 | 1 | id of the loaded area (area header 16180-161A0) | read |
| 10B9C / 10B9D | 1 / 1 | area type (0 town, 1 cavern, 2 castle, 3/6 outdoors, 4 elemental plane, 5 dungeon) / outdoors flag | read in all 60 areas |
| 10BCA | 1 | century index: year = 100 x value (09 = 900); takes effect when an area loads | poke verified (08 -> "Year= 800") |
| 10BCC | 1 | counts steps (not the day) | dump |
| 10BD5 | 1 | light units (Protect panel "Light (n)") | dump over two Light casts, poke verified |
| 10C16 | 16 | party: roster slot numbers as 16-bit words, FFFF = empty; count at 10C26 | search |
| 16852 | ... | event table of the loaded area (DS:6052): triples square y*16+x, event number, facing mask (80 N, 40 E, 20 S, 10 W), ended by 00 00 00; scripts and texts follow | disassembly of the event lookup, read in all areas |
| 161D6 | 256 | walls of the loaded town/cavern square by square (2 bits per side, see "Walking honestly"); terrain codes outdoors | read, walked (set start) |
| 162D6 | 256 | per-square property bytes of the area (DS:5AD6, index y*16+x) | disassembly |
| 18620 + 82*n | 130 | roster record n (slot A = 0 ... X = 23; hirelings after): this party = ryz 1892C (G), condi 186A2 (B), ebo 18724 (C), deddo 187A6 (D), mnz 18828 (E), cubi 188AA (F) | name search; spacing checked on four records |
| record +00 | 10 (+1) | name, space padded | read |
| +0B / +0C / +0D / +0E / +0F | 1 each | home town (1 = Middlegate?) / sex (0 M, 1 F) / alignment (0 Good, 1 Neutral, 2 Evil) / race (0 Human, 1 Elf, 2 Dwarf, 3 Gnome, 4 H-Orc) / class (0 Knight, 1 Paladin, 2 Archer, 3 Cleric, 4 Sorcerer, 5 Robber, 6 Ninja, 7 Barbarian) | read against six profiles |
| +10..+15, +27 | 1 each | base Might, Intellect, Personality, Speed, Accuracy, Luck; base Endurance | read |
| +6B..+70, +73 | 1 each | current Might .. Luck, current Endurance (**shown**; poke these and the base) | poke verified |
| +20 / +71 | 1 / 1 | level base / level shown | poke verified |
| +23 / +72 | 1 / 1 | spell level base / shown | poke verified |
| +21 | 1 | age | read |
| +24 | 1 | armor class | read |
| +25 | 1 | food | poke verified |
| +1E | 1 | thievery % | poke verified |
| +26 | 1 | condition bits (00 Good; 01 shows "Cursed", 14 "Asleep") | poke verified |
| +58 / +5A | 2 / 2 | spell points now / maximum | poke verified |
| +5C | 2 | gems | poke verified |
| +5E / +60 / +74 | 2 / 2 / 1 | hit points now / maximum base / maximum shown | poke verified |
| +62 | 4 | experience | poke verified |
| +66 | 4 | gold | poke verified |
| +3A.. | 1 each | items (Short Sword, Large Club seen at +3A as the first backpack item); layout of equipped/backpack/charges not decoded | read |
| +28..+2D / +3A..+3F | 6 / 6 | equipped item ids / backpack item ids (ITEMS.DAT index: 20-byte records, 12-char name, class mask in byte 13, price in 18-19); poke the backpack and equip in the game so AC and damage follow | equip diff, verified |
| +4C | 1 | weapon damage of the equipped weapon (derived) | equip diff |
| +50 | 1 | first secondary skill (1 Arms Master, 2 Athlete, 3 Cartographer ...); the second not located | Otto Mapper diff |
| +51..+56 | 48 bits | spells known, bit n = spell n+1 of the class list (levels hold 7,7,6,6,5,5,4,4,4 spells) | Spell Book on screen |
| +7F / +80 / +81 | 1 each | quest marks; +81: 01 Chosen One, 02 King Kalohn saved, 20 Square Lake gate, 08 Cron saved (ending); +80 bit 20 set by the Bishop of Black Battle | Kalohn diff, gate test, ending code |
| +16..+1C, +2E..+39, +40..+4B | | not decoded (resistances, item bonuses and charges) | - |
| 10C10 / 10C12 | 2 / 2 | battles won / lost (victory screen, ending); zeroed by the Square Lake gate | victory text |
| 1A7AA | 2 x n | hit points of the monsters in the current fight (Sheltem 500) | combat diff |
| 1A60E | ... | the record of the monster on display (name, stats) | read |
| 1604E / 160AE | 26 / 9 | ending cipher key / enciphered answer | ending code |
Code: MM2.EXE at physical 2FB0 (CS 02FB); overlays load at ADC0 (2PLAY.OVL) and F0E0 (the second slot: 2SMITH,
2TEMPLE ...); the ending lives in 2SMITH.OVL (0x1174 onward). ndisasm is installed in the container.
Watches in `game.json`: `map`, `x`, `y`, `face`, `hp1`, `gold1`, `gems1`, `food1` (ryz), `light`, `year`.
Poking a record does not redraw the party window: open and close a profile (`1,w150,esc,w150`) first.

## Emulation notes
- Model `svga-8000`: GOG's `dosboxMM2.conf` says `machine=svga_s3`, `cycles=fixed 8000`, `memsize=32`; DOSBox
  Pure's `svga` is the S3, so the same cycle count gives the speed GOG tuned (like Might and Magic 1 with GOG's
  1500). The difference to the default 7800 is small; the routes are written for 8000.
- `loadfix -4` is required (see Boot). Without it the program quits with "Not enough memory for 16 color
  version".
- RNG follows frame timing: the creation roll depends on everything before `RYZ`.
- The title animates; most game screens settle. Checkpoint routes use fixed waits (`do!`); only `title` ends
  with `settle`.
- **The party window shows "/14"**: the current hit points are drawn with a slash in front ("ryz /14"), not as
  "now/max" (verified with ryz at 9 HP: "/9"). Not an emulation fault (same on `ega-8000`).
- `play.py` frames are 960x600 (3x), `emu.py --out` frames 320x200.

## Checkpoints
| Name | What |
|---|---|
| `title` | title picture, settled |
| `menu` | Main Options |
| `start` | party in the Middlegate inn facing the door (first control) |
| `signed_in` | after signing in: inn list (ROSTER.DAT written; base of `01_start`) |
| `middlegate` | Middlegate street after the spirit of Corak: the base for `AT`, `WARP` and scans |
| `outdoors` | C2 just outside Middlegate's gate |
| `cavern` | cavern under Middlegate, lit (30 light units) |
| `combat` | encounter options of the fixed fight at Middlegate (8,1) |
| `vet` / `hero` | Middlegate street with the VET / HERO party |
| `vet_cats` | VET party at the cats fight, encounter options |
| `vet_cats_r2` | same fight, round 2 (after shoot, spell, exchange, fight, delay, protect, Bless) |
| `sheltem` | HERO party with MARKS at the Square Lake gate: Sheltem's encounter |
| `s_equipped` .. `s_signed` | honest chain of set `start`: sword equipped, street, blacksmith, temple, gate, C2, orcs, defeat, resume, signed in |

## Sources
| Source | URL | Used for | Accessed |
|---|---|---|---|
| Game manual (`Manual.pdf` in the owner's ZIP; text copy `work/scout/might-and-magic-2/manual.txt`, not committed) | - | menus, commands, classes, races, skills, spells (96), save rule, hirelings, time travel | 2026-11-19 |
| Game files and memory (ROM text: `tools/texts.py` -> `work/scout/might-and-magic-2/texts/`) | - | area names, quest chain, Square Lake, shrines, services | 2026-11-19 |
| GOG configuration in the ZIP (`dosboxMM2.conf`, `dosboxMM2_single.conf`) | - | cycles, `loadfix -4` | 2026-11-19 |
| Corak's Travelogue, the Might and Magic II cluebook (archive.org scan, OCR text read through WebFetch) | https://archive.org/details/Might_and_Magic_II_Gates_to_Another_World_Cluebook | towns and their sectors, caverns, castles, dungeons, hirelings and where they wait, main quest outline | 2026-11-19 |
| Wikipedia | https://en.wikipedia.org/wiki/Might_and_Magic_II:_Gates_to_Another_World | release, plot outline, hirelings, skills, ending by spaceship | 2026-11-19 |
| StrategyWiki | https://strategywiki.org/wiki/Might_and_Magic_II:_Gates_to_Another_World | not reachable (HTTP 403) | 2026-11-19 |
| GameFAQs | https://gamefaqs.gamespot.com/pc/564550-might-and-magic-ii-gates-to-another-world/faqs | not reachable (HTTP 403) | 2026-11-19 |
| The Cutting Room Floor | https://tcrf.net/Might_and_Magic_II:_Gates_to_Another_World | not reachable (HTTP 403) | 2026-11-19 |
| archive.org downloads (cluebook PDF/text files) | archive.org download hosts | refused by the proxy (only the archive.org pages work) | 2026-11-19 |
| GOG forum "mm2 roster dat editing information" | gog.com | outside the allowed hosts; not fetched | - |

## Open questions
- ~~What fires the ending~~: settled 2026-11-19, see "The ending". Still open: what sets the gate's bit 20 and
  the Chosen One bit 01 in normal play (no area script writes them; maybe the class quests or Corak).
- ~~Record bytes~~: items, skill 1, spells, marks decoded (RAM map); still open: second skill, item bonuses and
  charges, resistances.
- The day counter; whether `YEAR` alone is enough or the game also keeps a "time travel" timer that sends the
  party back while resting (manual: "your stay in any century is limited").
- The exact cave and dungeon assignment of ids 12-20 and 2D-34 (inferred from texts; confirm on the location
  screen with a Cartographer or from the entrances).
- Hirelings: how they become available (inn lists after quests) and where their records start (24th record?).
