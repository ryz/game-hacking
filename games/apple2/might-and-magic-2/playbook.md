# Might and Magic II: Gates to Another World (Apple II) - playbook

Everything an agent needs to play this game efficiently: read it before playing, add to it after every run.
Status of each fact: **verified** (seen in the emulator, with the route) or **source** (manual/FAQ/wiki, not yet
checked). Never delete a fact that turned out wrong: strike it and say what is true.
The DOS port is fully documented in `games/dos/might-and-magic-2/` (playbook, design documents, a 228-shot set to
the ending): this is the same game, the original 1988 version. Its area ids, event squares, item ids and
services were all found unchanged here wherever they were tried (below); its RAM addresses do not apply.

## Read first
- **Start:** `python3 tools/play.py --name mm2 start apple2/might-and-magic-2 --route @middlegate` (model `iie`,
  needs `rom/apple2/might-and-magic-2.zip`, six nibble disks). Every checkpoint reproduces cold
  (`python3 tools/cachecheck.py apple2/might-and-magic-2 --flat leaves`, 16/16, 2026-11-20; 26 checkpoints after the capture, all used by verified shots).
- **Disks:** A boot/title (and Sheltem's picture), B roster + the five towns (00-04), C outdoors west (05-10),
  D caverns (11-20, Square Lake 17), E outdoors east + elemental planes (21-2C), F dungeons, towers, castles
  (2D-3B). The game asks "Insert Disk X in Drive 1 and Press 'Return'": answer `DISK:n` (`disk:n,enter,w700`).
  **Never answer a prompt that did not come:** `enter` is also "forward".
- **Party:** `PARTY` (one route from power-on) = ryz (created, Human Knight) + the five premades renamed condi
  (Dwarf Paladin), ebo (Archer), cubi (Robber), deddo (Gnome Cleric), mnz (Elf Sorcerer). Checkpoint `start`
  (inn, first control), `middlegate` (street, the base for everything), `vet` / `hero` (poked parties).
- **Moving:** `AT:x:y` (one hex digit each) + `FN FE FS FW` + `left` fires the square's event facing one turn
  left of the poked facing (N needs `FE`, E `FS`, S `FW`, W `FN`). DOS event squares are valid here:
  `@middlegate,AT:4:4,FN,left,w300` = blacksmith.
- **Changing area:** `WARP:id:x:y` (id two hex digits, x/y one each) from any map square; `WARPD:id:x:y:disk`
  when the area is on another disk than the one in the drive (table above). Landing (8,8)/(7,7) is usually free.
- **Light:** `LIGHT` = deddo casts Light (1 SP, "Light (1)"); `hero` has three. Caverns are "Darkness" without.
- **Traps that cost calls:** the party window (HP column) is not redrawn after a poke: `REDRAW` (exchange 1-2
  twice). Pokes at `0400+` (records) are the mapped page: right in town and outdoors; in combat use `2xxxx`.
  Text page reading (`play.py text`) shows garbage: every screen is hi-res, look at pictures.
  The right panel stays on "Protection" after a cast until `o` (or Esc).
  **Encounters: never `settle` on an encounter screen** (portraits animate, settle runs 300 frames and the
  fight starts: the monsters act first). End encounter checkpoints and shots with a fixed wait or `!`.
- **Century:** `YEAR:08` (= `poke:2F7C9=08`) before a `WARPD` from another disk loads the area in year 800
  (Castle Xabran in C2 (14,7)+up, King Kalohn at C4 (14,4)+up). Never rest there: a rest can reset it to 900.
- **Equipment:** `GEAR` puts Long Sword, Chain Mail, Large Shield, Helm, Crossbow in ryz's backpack, `EQ5`
  opens his profile and equips all five (AC 13).
- **Combat keys:** `a` opens the fight; per member `f` + target letter (fight), `c` level number target
  (no Return), `b` block, `q` quick reference, `v` view, `e` exchange, `d` controls, `p` protection. A fight to
  the end without looking: repeat `a,w300,b,w300` (victory route of `battle_victory`). Monster pictures and
  lists appear ~600 frames after "Encounter!" (they load from disk): shots use `w200*3,!` or `w200*4,!`.
- **State (2026-11-20):** `start` 45 shots and `main` 216 shots published, both verified cold; lenses clean.
  Open: the Sheltem fight (not won, so no ending), Earth/Water plane looks, Unlock, Use, hirelings.

## Identity
| Field | Value |
|---|---|
| Title (EN / original) | Might and Magic II: Gates to Another World (title picture "Might and Magic Book Two"; Main Options "MIGHT and MAGIC Book Two Gates To Another World") (verified) |
| Platform / model used | Apple II, `iie` (enhanced //e, colour TV); see `game.json` |
| Release (region, year) | North America, 1988 ("Copyright,1988 New World Computing,Inc"; About: "Version 1.00") (verified); the first release, the DOS port followed 1989 (Wikipedia) |
| Developer / publisher | New World Computing; About screen: Jon Van Caneghem, Stephen L. Cox, Mark Caldwell, Avril Harrison, Vince DeQuattro (verified) |
| Genre | First-person party RPG, 16x16-square areas, menu combat with monster pictures, time travel |
| Players / save system | 1 player; roster of 24 + hirelings on disk B; party of 6 (+ hirelings); **save = sign the registry at an inn** (writes disk B) (verified) |
| Dump | `rom/apple2/might-and-magic-2.zip`: `1 Disk 1.nib` .. `6 Disk 6.nib` = disks A-F (SHA-1s in `game.json`); boots without a crack screen |

## Boot sequence
Macros in `game.json`: `TITLE`, `OPTIONS`, `MENU`, `RYZ`, `RENAME:letter:name`, `NAMES`, `JOIN`, `PARTY`, `RESUME`.
- Intake probe: `work/intake/apple2/might-and-magic-2/sheet.png`: "New World Computing Presents" (globe), then the
  title picture by ~frame 240.
- **verified** `TITLE` = `w1000`: title picture (pegasus; a small creature animates in the bush). `space` ->
  after ~450 frames the opening options: S Start Game, C Copy Disk, A About Book Two, N Number of Drives = 1
  (two globes turn: never settles). `OPTIONS` = `TITLE,space,w600`.
- **verified** `s` -> "Insert Disk B in Drive 1 and Press 'Return'"; `MENU` = `OPTIONS,s,w600,disk:2,enter,w900`
  -> Main Options (C Create New Characters, V View All Characters, T Transfer Characters, G GO TO TOWNS).
- **verified** Disk B's roster = the six premades of the DOS stock roster: A Sir Felgar K, B Terwin III P, C Sure
  Valla A, D Gene Eric C, E Cassandra S, F The Hermit R, all level 1; hirelings list empty.
- **verified** `PARTY` = `MENU,RYZ,NAMES,JOIN` as one route from power-on (checkpoint `start`): Middlegate inn
  (7,3) facing N. Two `up`: the second shows "The spirit of Corak proclaims, ..." with an animated ghost and
  "('Space' to continue)"; `space`, `up` = the street. Checkpoint `middlegate` (7,5).
- **verified** Saving: from `start` `right,w200,right,w300` -> "A jolly old innkeeper waves his quill ... 'Will you
  sign the registry (y/n)?'"; `y,w600` -> inn list "(1-Middlegate)", party ticked, "'Z' to Exit". Checkpoint
  `signed_in`; export `01_start` (`rom/saves/apple2/might-and-magic-2/01_start.sav`, only `2 Disk 2.nib`
  inside). `sav:01_start,RESUME` = power on with it, `G`, `z`: party in the inn (verified, the ticks are kept).

## Controls
Every screen lists its keys. One key at a time (the Apple II keyboard latch): wait for each screen.
| Context | Key | Action | Status |
|---|---|---|---|
| Title | `space` | opening options | verified |
| Opening options | `s` / `c` / `a` / `n` | start (disk B prompt) / 1-drive disk copy / About (version, credits) / drives | s, c, a verified |
| Main Options | `c` / `v` / `t` / `g` | create / view all / transfer from Book 1 ("Insert MM1 character disk") / go to towns | all verified |
| Create | `enter` | re-roll | source (screen) |
| | `a`-`g` then `a`-`g` | exchange two statistics (`d,b` swaps Endurance and Intellect) | verified |
| | `1`-`8` class (eligible ones numbered), `1`-`5` race, `1`-`3` alignment, `1`-`2` sex, name, `enter` saves at once and rolls the next | | verified |
| View all / inn list | `a`-`x` profile; `space` hirelings; inn: `ctrl+a`.. tick, `z` exit, `1`-`5` other towns | | verified |
| Profile (menus) | `ctrl+n` rename, `ctrl+d` delete | rename verified |
| Exploration | `up` forward (also `enter`), `down` back, `left`/`right` turn (a turn fires the square's event) | | verified |
| | `b` bash, `c` controls (sounds, walk beep, disposition, delay 0-9), `d` dismiss, `e` exchange, `q` quick ref, `r` rest ("Rest complete, no encounters."), `s` search ("Search... Nothing here!"), `u` unlock, `p`/`o` protection / options panel, `1`-`6` profile | | c e q r s p o verified; b d u not seen |
| Profile (play) | `q` `c` cast (level, number, Return) `d` drop `e` equip `g` gather `r` remove `s` share `t` trade `u` use | | c verified (Light `CAST:5:1:5`) |
| Encounter | `a` attack, `b` bribe (1 food, 2 gold, 3 gems), `h` hide, `r` run | | a, b verified |
| Combat | per member: `a` attack (front members), `f` fight, `c` cast, `u` use, `b` block, `r` run, `e` exchange, `v` view; `d` delay, `p` protection, `q` quick | | screens verified; outcome of `a` not seen (see Open questions) |
Input timing: default press works; waits that worked: turn `w200`, step `w300`, event prompt `w300-400`, profile
`w300`, area load or disk change `w600-900`.

## Game structure
Same world as the DOS port (`games/dos/might-and-magic-2/playbook.md`, "Game structure": area table, Middlegate
squares, C2, Square Lake, main quest, ending). Checked here:
- **verified** Area ids 00-3B as on DOS (warp to all 60, each loads or asks for its disk): towns 00-04 (disk B),
  outdoors 05-10 (C) and 21-28 (E), caverns 11-20 (D), elemental planes 29-2C (E), dungeons/towers 2D-36 and
  castles 37-3B (F). Middlegate's gate (5,15) N -> C2 (7,3) with "Insert Disk C".
- **verified** Middlegate squares of the DOS table: inn (7,3), blacksmith Svendegard (4,4) W, Slaughtered Lamb
  tavern (Amber) (4,6) W, temple (7,7) N, training (10,7) E, mage guild (1,12) W (20 gold), locksmith (1,8) W
  (key 500 gold), Poorman's Portal (0,5) W (Sandsobar 10 gold), Otto Mapper (0,15) W (10 gold), Nordon (10,2) W,
  stairs to the cavern (8,0) W ("Stairs to Cavern. Descend (y/n)?"), gates (5,15) N, fixed fight (8,1): 6
  Witch's Cats + 4 Rabid Rodents. C2: Guardian Pegasus (7,4); "Ruins of a mighty castle" at (14,8) in year 900.
- **verified** Square Lake gate (area 17, (0,15) facing E): with a fresh party poked to levels 29-31 (no quest
  marks) it gives Sheltem at once, asking for disk A for his picture: "Sheltem and his Elementals guard the entry
  to the control room. 'Although you may defeat me, you're too late! CRON and all it's VARNs are doomed!'",
  `space` "Encounter!", `space` disk D, then Sheltem, Water, Air, Fire and Earth Elemental. The DOS gate refused
  without the "King saved" mark: **difference** (or the Apple check is elsewhere).
- Year 900 at the start (status line). Item ids are the DOS ones: Element Orb DF, Water/Air/Fire/Earth Talon
  DB-DE (verified by poking the backpack).

## Shot plan
Target: a `main` set like the DOS one (about 150-230 shots), plus `start`. Routes for the lines marked *plan* are
in `shots.txt` (previewed 2026-11-20); the rest need routes. Reach everything with `WARP(D)`, `AT`, the poked
parties and the fixed fights.
- Boot and menus (10): NWC logo (`TITLE` at ~w300), title, opening options, About (credits), Copy Disk, Main
  Options, View All, hirelings list, profile, rename, Transfer prompt. *plan*
- Creation (6): roll, exchange, class, race, alignment/sex, name.
- Inn and Middlegate (25): inn list, sign-in prompt, spirit of Corak, street views, every service of the
  Middlegate table (prompts above, then their menus), fountains, arena, signs. *plan* for the prompts.
- Exploration commands (10): controls, protection panel, quick ref, rest, search, unlock, bash, exchange, cast
  Light, spell book. *plan* for most.
- Combat (15): encounter options, combat screen, attack, fight, cast, block, run, hide, bribe prompt, victory,
  treasure, a death, party wiped (game over). The fixed fight (8,1) and other DOS fixed fights.
- Environments (25): each town (5), outdoors terrains (C2 forest/coast, mountains, desert in E1, tundra,
  swamp, water), cavern (lit and "Darkness"), castle, dungeon, the four planes, Square Lake, Xabran ruins.
- Opponents (20+), quest and story (15: Pegasus, Nordon, Corak, Xabran discs, Kalohn, Sheltem, ending),
  progression (training, level up, skills, hireling).
- Apple II only: the disk prompts (B-F, and A for Sheltem's picture) - one shot.
Distinctive here: the 1988 hi-res art (monster portraits framed in combat, animated ghost/globes), six disks.

### Shot plan status (2026-11-20)
Done: boot and menus, creation, inn and Middlegate (every service of the DOS table), exploration commands but
Unlock and Use, combat (encounter options, every combat key, hits, spells, victory, two defeats), the other
four towns, 12 outdoor views, caverns, dungeons, castles, Air and Fire planes, five bosses, Square Lake fights,
year 800 (Xabran, Kalohn, Mega Dragon), Sheltem's encounter and fight, disk prompts B, C, A.
Missing: the Sheltem victory and the ending, Earth/Water plane looks, hireling, Unlock, Use, level-up at
training (needs experience poke), the arena.

## Strategy and walkthrough notes
- Everything from `@middlegate` or `@hero`: `WARPD` into the area, `AT` to the square, `left` for its event.
- Fights: level-1 parties die in the Sheltem fight in one round (250-point breath). Use `hero`; for ordinary
  fights `vet`. The fixed fight at Middlegate (8,1) (`combat`) is the cheapest combat screen.
- The poked parties have the statistics of level 1 (Might 16 etc.) and no gear: equip by poking the backpack
  (`+4B..+50`, DOS item ids) and `e` in the profile before fight shots.
- Disk prompts appear on area loads and for some monster pictures (Sheltem's is on disk A): look at the frame
  after every new encounter before pressing keys.

## Naming
Main character **ryz**, then condi, ebo, cubi, deddo, mnz (lower case: `type:ryz`; the game keeps case).
- `RYZ` (from Main Options, first roll after `MENU` from power-on: Might 16, Int 15, Per 6, End 4, Spd 17,
  Acy 15, Luc 14): `d,b` swaps Endurance and Intellect, Knight, Human, Good, Male, `type:ryz`, Return. Result:
  ryz Human Knight, HP 14, Large Club in the backpack. The roll follows frame timing: anything changed before
  `RYZ` changes the statistics (and may make the Knight unavailable).
- `NAMES` renames B condi, C ebo, F cubi, D deddo, E mnz (`ctrl+n`, type, Return). Sir Felgar (A) stays.
- `JOIN` ticks G, B, C, F, D, E (marching order ryz, condi, ebo, cubi, deddo, mnz) and `z`.

## Shortcuts
| What | How (tokens / prefix / code) | Source | Status |
|---|---|---|---|
| Party at the start, saved | `sav:01_start,RESUME` | made here | verified |
| Move in the area | `AT:x:y` + `FN/FE/FS/FW` + `left` | RAM | verified (Middlegate, C2, Square Lake) |
| Change area | `WARP:id:x:y`, `WARPD:id:x:y:disk` (patches the forward-key handler at `A16D` to jump to a routine at `0110` that restores it, sets the position and calls the area loader `BB29`) | code | verified (60 ids reach their load or disk prompt; 14 entered) |
| Strong parties | `HERO` (levels 29-31, HP 132-287, SP, gems, gold, ages 29-36), `VET` (levels 10-11); then `REDRAW` | RAM | verified on quick ref and profiles |
| Light | `LIGHT` (cast) | game | verified; a light counter poke was not found |
| Gold, gems, food, HP, SP, level, experience | record pokes (RAM map) | RAM | verified on the profile |
| Century | `YEAR:nn` before a load from another disk (`WARPD`) | RAM | verified (year 800: Xabran, Kalohn) |
| Gear for ryz | `GEAR` then `EQ5` (profile, equip A five times) | RAM + game | verified (AC 13) |
| Debug features, cheat codes | none known (web search found none) | - | - |

### Saves (rom/saves/apple2/might-and-magic-2/, never committed)
| Name | Contents | URL | SHA-1 | Status |
|---|---|---|---|---|
| `01_start` | disk B after signing in: the new party in the Middlegate inn | made here | `saves/README.md` | verified (loads with `RESUME`) |
None downloaded.

## RAM map (for `game.json` "ram" watches and pokes)
`2xxxx` = main 64K as stored (also language-card RAM), plain `xxxx` = what is mapped now (main in town).
| Address | Size | Meaning | How found |
|---|---|---|---|
| `0030` / `0031` | 1 / 1 | party square y*16+x (both copies; `AT` writes both) | find, poke verified |
| `0035`-`003C` | 8 | facing tables; `0035` = C0 N, 30 E, 0C S, 03 W (`FN` .. `FW` write all eight, values as in Apple MM1) | dump, poke verified |
| `0039` | 1 | step delta of the facing (10 N, 01 E, F0 S, FF W) | code (`A213`) |
| `2FA00` | 1 | current area id (00-3B); `2FA05`-`2FA08` neighbours N E S W (outdoors), event table from `2FA20` (square, event, facing mask 80 N 40 E 20 S 10 W) | search, code |
| `0400 + 80*n` | 128 | party member n (0 = ryz ... 5 = mnz; 6-7 hirelings?) in party order (main RAM, text page 1) | name search, profiles |
| +00 / +01 | 1 / 1 | roster slot (ryz 06 = G) / home town | read |
| +02 | 10 | name, high bit set, space padded | read |
| +0C / +0D / +0E / +0F | 1 each | sex / alignment / race / class (codes as DOS: race 2 Dwarf, class 1 Paladin ...) | read |
| +10..+15 | 6 | base Might, Intellect, Personality, Speed, Accuracy, Luck | read |
| +1E | 1 | thievery % | poke verified |
| +20 | 2 | maximum HP (shown) | poke verified |
| +22 / +23 / +24 | 1 each | current Might / Speed / Accuracy (shown) | poke verified |
| +25 | 1 | alignment shown (03 shows "None") | poke |
| +26 / +27 | 1 / 1 | level / spell level (shown) | poke verified |
| +28 | 2 | spell points now (inferred: mnz 7) | read |
| +2A..+2D | 4 | Endurance, Intellect, Personality, Luck (current) | read |
| +2E / +2F | 1 / 1 | level base / age | read, poke verified (age) |
| +31 | 4 | experience | poke verified |
| +35 | 2 | spell points maximum | poke verified |
| +38 | 2 | gems | poke verified |
| +3A / +3C | 2 / 2 | HP now / HP maximum base | poke verified (+3A), read |
| +3E | 3 | gold | poke verified |
| +41 / +42 / +44 | 1 each | armour class / food / Endurance | read |
| +45..+4A / +4B..+50 | 6 / 6 | equipped / backpack item ids (DOS ids) | poke verified |
| +51..+73 | | item bonuses and charges (a poke here showed "Large Club +2"), skills (showed Navigator, Crusader) | poke, not decoded |
| `20283` / `2028E` | 11 / 11 | monster HP low / high bytes during combat (Sheltem 500 = F4/01, elementals FA); a monster that runs away is removed and the arrays close up | search, diff |
| `20299`.. | 11 each | further monster arrays, stride 11: `202A4` (01 08 06 08 08 for Sheltem's group), `202AF` (28 1E 1E 1E 1E: AC?), `202BA` (status: 01 after acting?) | diff, not decoded |
| `2F7C9` | 1 | century: 09 = year 900; the year is printed from tables `F7D4+c` (low) / `F7DE+c` (high) | code at `D6F6`, poke verified (08 = year 800 after a load from another disk) |
| `2F7CA + c` | 1 each | day counter per century (`2F7D3` = days in year 900); four rests = one day | diff, verified |
| `B955`-`B970` | code | rest: outside century 9 a roll may write 09 to `F7C9` and move the party (return to the present) | code read |
| `1050` | code | area load compares `F7C9` with the area's century `FA0F` | code read |
| +43 | 1 | condition (00 good, 40 unconscious) | diff after a fight |
| `A101` | 17 | exploration key table, handlers lo `A112` / hi `A123`: forward = `A16D` | code |
Watches in `game.json`: `yx`, `facing`, `area`, `hp1`, `gold1`. Scratch disassembler used: py65 (`pip install py65`).

## Emulation notes
- Model `iie` (as registered); no problems seen. Boots straight to the logo (no crack screen).
- The opening options and several pictures (globes, spirit, title bush) animate: `settle` reports "still
  changing"; checkpoints end with `settle` anyway and reproduce.
- Text page 1 holds the party records, not text: `play.py text` is useless here.
- RNG follows frame timing (creation rolls, fights).

## Checkpoints
| Name | What |
|---|---|
| `title`, `options`, `menu` | title picture, opening options, Main Options |
| `start` | inn, party, first control |
| `middlegate` | street (7,5): base for `AT`/`WARP` |
| `outdoors` | C2 (7,3) outside the gate, disk C |
| `signed_in` | inn list after signing in (base of `01_start`) |
| `vet`, `hero` | street with the poked parties, window redrawn (`hero` has Light 3) |
| `combat` | Middlegate (8,1) fixed fight, encounter options (level-1 party) |
| `vet_cats` | the same fight met by the VET party (base of the combat shots and the victory) |
| `s_smith`, `s_temple`, `s_training`, `s_gate`, `s_c2`, `s_orcs`, `s_death`, `s_resume`, `s_signed` | set `start`: walked from the inn to the blacksmith, temple, training, gates, C2, the ten Orcs (lost), Death Strikes, resumed, signed in |
| `atlantium`, `cavern`, `plane_air`, `castle` | areas 01, 11 (lit), 29, 37 at (7,7) with `hero` |
| `sheltem`, `sheltem_options` | Square Lake gate: speech; encounter options |

## Sources
| Source | URL | Used for | Accessed |
|---|---|---|---|
| DOS port's playbook and design documents | `games/dos/might-and-magic-2/` | area ids, event squares, item ids, quest and ending | 2026-11-20 |
| Apple II Might and Magic 1 playbook | `games/apple2/might-and-magic/playbook.md` | disk prompts, facing tables, warp idea | 2026-11-20 |
| Wikipedia | https://en.wikipedia.org/wiki/Might_and_Magic_II:_Gates_to_Another_World | Apple II first (1988), ports, time travel (nine centuries, needed for the final boss), spaceship ending | 2026-11-20 |
| Web search (time travel, Apple II) | - | nothing on the in-game method | 2026-11-20 |
| The game (About screen, all screens above) | - | credits, version, texts | 2026-11-20 |

## Open questions
- ~~Century~~ solved 2026-11-20: `2F7C9` (found through the day counter `2F7D3`, which rests advance; the
  printing code indexes the hundreds table with it). A same-disk `WARP` does not redraw the status line; a
  load from another disk does. After an event in year 800 the status line prints 900 again (findings.md).
  The game's texts are not stored as plain or offset-encoded ASCII (searched all 192K).
- **Sheltem fight** (capture run, ~20 calls): monster HP 0 at `20283`/`2028E` makes breath do 0 points, but the
  monsters keep acting and are not removed; party HP and condition frozen (`freeze:2043A=1F01 ... freeze:206C3=00`,
  waits as `w10` chains) keep the party alive, but no party attack ever lowered a monster's HP (also with
  `202AF`=0), and a member who was down when the freeze started (mnz) blocks the round: his turn ignores every
  key. Next: freeze before the first round (from `sheltem_options`, before `a`), give the party weapons
  (`GEAR`-style pokes for all six) and accuracy, or find the victory routine (the code that prints "Victory!").
- Does the Apple gate check any quest mark (DOS bit 20 of record +81)? It opened for an unmarked party.
- Light counter and quest-mark bytes of the record; record bytes +51..+73.
- Hirelings: records 6-7 at `0700`/`0780`?
