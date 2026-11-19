# Might and Magic Book One: The Secret of the Inner Sanctum - playbook

Everything an agent needs to play this game efficiently: read it before playing, add to it after every run.
Status of each fact: **verified** (seen in the emulator, with the route) or **source** (manual/FAQ/wiki, not yet
checked). Never delete a fact that turned out wrong: strike it and say what is true.

## Identity
| Field | Value |
|---|---|
| Title (EN / original) | Might and Magic Book One: Secret of the Inner Sanctum (title pictures, options menu "COPYRIGHT,1986-JON VAN CANEGHEM") (verified) |
| Platform / model used | Apple II, `iie` (enhanced //e, colour TV picture); see `game.json` |
| Release (region, year) | North America, 1986 (title screen); the original version of the game, the DOS port followed in 1987 (source: `games/dos/might-and-magic/playbook.md`) |
| Developer / publisher | New World Computing, Jon Van Caneghem (title screen) |
| Genre | First-person party RPG, 16x16-square maps |
| Players / save system | 1 player; party of up to 6 from the roster; **save = sign in at an inn**, which writes the roster to disk B (verified: gold and food after a meal survive a power-on with the exported save) |

## The dump: four disk sides
`rom/apple2/might-and-magic.zip` (never committed) holds the game's two double-sided disks as four images, in play
order; `game.json` "header" lists their SHA-1s. Owner's uploads 2026-11-18 (TOSEC names):
| Disk | Game calls it | File in the ZIP | From | Holds |
|---|---|---|---|---|
| 1 | Disk A (boot) | `Disk 1 (cracked).nib` | `...[cr](Disk 1 of 4)[nib]` | boot, title, demo scenes |
| 2 | Disk B | `Disk 2.dsk` | `...[b](Disk 2 of 4)` | options menu, roster (the save), the five towns, the cavern below Sorpigal |
| 3 | Disk C | `Disk 3.dsk` | `...[b](Disk 3 of 4)` | the wilderness (verified: outside Sorpigal) |
| 4 | Disk D | `Disk 4.dsk` | `...[b](Disk 4 of 4)` | castles, dungeons and the Astral Plane (verified: every section-3 area loads from it) |
- **verified** The uploaded `[b](Disk 1 of 4).dsk` (SHA-1 1559b116...) does not work: it shows the first title
  picture and then re-reads track $0E, sectors $0C-$0F, forever (watched for 3 minutes of game time; no key
  helps). The `[cr]` nibble image of the same side boots, so that one is disk 1. It opens with a crack screen
  ("Cracked by: The Talisman") that waits for a key.
- **verified** Disk B came with six characters of an earlier player in Sorpigal (Murkler, Scrye, Stealthar,
  Shylea, Twangii, Nightblade; Murkler is a level 2 knight). The inns of towns 2-5 are empty. It is not a
  factory roster.
- The game asks for a side by letter: "INSERT DISK B AND PRESS 'RETURN'" (`D` on that screen toggles between
  one and two drives; one drive is used here). Answer with `disk:N,enter`.

## Boot sequence
Macros (`game.json`): `TITLE`, `MENU`, `TOWN:n`, `AT:xx:yy:oo` + `FN FE FS FW`, `OUTSIDE`. Checkpoints `title`,
`menu`, `sorpigal`, `outdoors`, `after_save`.
- **verified** Power-on: crack screen after about 5 s; any key (`space`) continues to the title picture ("New
  World Computing, Inc. presents Might and Magic"), which stays until a key. `TITLE` = `w600,space,w1800`.
  `esc` there starts the game; `space` shows the second picture ("Book One - Secret of the Inner Sanctum",
  "'ESC' TO START GAME / 'SPACE' FOR SCENES") and then demo pictures that look like gameplay.
  ~~The title ends on the "ESC to start" screen by itself after 25 s~~: it does not, that screen needs `space`.
- **verified** `esc` -> "INSERT DISK B": `MENU` = `TITLE,esc,w300,disk:2,enter,w1200` -> options menu
  (`C` create new characters, `V` view all characters, `#` go to town 1-5).
- **verified** Town number -> the inn's list; `ctrl+a`..`ctrl+f` add or remove a character (`@` marks members,
  "PARTY IS FULL" at six), `x` leaves into the town. `TOWN:1` = Sorpigal with the six roster characters, first
  control at (8,3) facing north.
- **verified** Leaving Sorpigal by the passage outside at (12,0): "A PASSAGE LEADS OUTSIDE, TAKE IT (Y/N)?",
  `y` -> "INSERT DISK C IN DRIVE 1" -> `disk:3,enter` -> wilderness in colour. Macro `OUTSIDE` (from anywhere in
  Sorpigal). The stairs down at (14,0) need no disk change (cavern "DARKNESS" without light, on disk B).
- **verified** Saving: from the start square `down,left,left,up,up` -> "WOULD YOU LIKE TO SIGN IN (Y/N)?", `y`
  writes disk B and returns to the inn's list. `play.py export` gives a ZIP with the whole changed side 2, which
  is game data: keep such saves in `rom/saves/apple2/might-and-magic/` (uncommitted), not in `saves/`.
  `sav:01_signed_in` powers on with it (made 2026-11-18: gold 48 -> 43, food 5 -> 40 on Murkler's sheet).
- Returning to a town from the wilderness will ask for disk B again (not tried).

## The party (2026-11-18, owner's request: wipe the inherited roster, make a new one)
Checkpoints `roster` (roster view after the wipe and creation), `party` (Sorpigal, first control), `signed_in`
(inn list after saving). Save `rom/saves/apple2/might-and-magic/02_ryz_party.sav` (uncommitted): `sav:02_ryz_party`.
- **verified** Delete: options menu `v`, then per character `a,w300,ctrl+d,w200,y,w400` ("ARE YOU SURE (Y/N)?");
  the list closes up, so deleting A six times empties the roster ("NO AVAILABLE CHARACTERS"). `ctrl+n` on the
  same profile re-names.
- **verified** Create: options menu `c`. The screen (40-column text, readable at `0400`) shows seven rolled
  statistics and the classes they allow (1 Knight, 2 Paladin, 3 Archer, 4 Cleric, 5 Sorcerer, 6 Robber);
  `enter` re-rolls. Then class digit, race `1`-`5` (Human, Elf, Dwarf, Gnome, Half-Orc), alignment `1`-`3`
  (Good, Neut, Evil), sex `1`-`2`, `type:NAME,enter`, "SAVE CHARACTER (Y/N)?" `y` (written to disk B at once),
  and the next roll appears; `esc` goes back to the menu.
- **verified** The party made here, in roster order (re-rolls needed on this route in brackets): RYZ human
  knight (1), CONDI dwarf paladin (4), EBO half-orc archer (17), CUBI gnome robber (0), DEDDO human cleric (0),
  MNZ elf sorcerer (7); all good, male. A new character: level 1, age 18, no gold, 10 food, a Club in the
  backpack (RYZ: INT 9 MGT 12 PER 13 END 16 SPD 11 ACY 10 LUC 8, HP 14).
- The rolls follow frame timing: the route in `checkpoints.txt` (`roster`) is the record; any change before a
  roll changes the statistics. Unlike the DOS port's notes, a checkpoint built on the creation route reloads
  cleanly here (9 shots verified from an empty cache and from the cache).
- `sorpigal`, `outdoors`, `after_save` still use the six characters found on the disk (the dump is unchanged).

## Sorpigal and combat (capture run 2026-11-18, set `main`)
- **verified** The event squares are those of the DOS port's table (`games/dos/might-and-magic/playbook.md`):
  blacksmith (6,5) W, market (10,5) E, temple (4,1) N, training (13,11) N, tavern (11,14) E, leprechaun (11,3) W,
  statue (7,1) N, jail sign (6,10) N, stairs (14,0) W, exit (12,0) S. Reach one with `AT:xx:yy:oo`, the facing
  one turn clockwise of the wanted one, `left` (shot routes in `shots/main/shots.txt`).
- **verified** ~~Unlike the DOS port~~ (wrong: the DOS port asks the same; its routes press `y` too) every service first asks a yes/no ("CAN I HELP YOU (Y/N)?", "STEP UP TO THE
  BAR (Y/N)?"): `y,w300` opens the menu. Blacksmith: A buy weapons, B buy armor, C buy misc, D sell item; prices
  as in the DOS notes (Dagger 5 ... Staff 30; Small Shield 10 ... Chain Mail 200; Torch 2 ... Scroll of Fire 300).
  Temple: restore health, uncurse items, restore align, make donation 100. Training: "TRAINING FOR LEVEL 2 NEED
  1500 MORE EXPERIENCE POINTS". Tavern: have a drink, tip bartender, listen for rumors.
- **verified** Statue at (7,1): "ON THIS STONE STATUE OF AN H-ORC ARCHER A PLAQUE READS..." then "IN HONOR OF
  CORAK... FOR HIS MAPPING EXPEDITION OF THE LAND OF VARN AND REDISCOVERY OF THE LOST TOWN OF DUSK".
- **verified** `q` quick reference (hit points, spell points, AC, food, condition), `o` re-order party, `p`
  protect ("SPELLS CURRENTLY ACTIVE"), `r` rest ("REST HERE (Y/N)?" -> "REST COMPLETE: NO ENCOUNTERS!"), `s`
  search ("NOTHING"); on a sheet `c` = "CAST SPELL: LEVEL=".
- **verified** Fixed fight at (3,6) (`AT:03:06:63,FN,left,w400`): monster picture and six Battle Rats, options
  `a` attack, `b` bribe, `r` retreat, `s` surrender. Each of them led into combat on this route. Combat screen:
  round number, monsters A-F (`+` = in melee), party positions, handicap, then "OPTIONS FOR: name" (`a` attack,
  `f` fight, `e` exchange, `r` retreat, `u` use, `b` block; casters also `c` cast; `d` delay, `p` protect).
- ~~Combat stops at CUBI's turn~~ **verified**: it was the turn of the back rank. Only members marked `+` (in
  melee) are offered `a` attack; the others must `b` block (or cast, use, exchange). A fight runs to its end
  with "attack where offered, else block". `ctrl+a` is not a quick-fight key here.
- **verified** Winning: "FOR DEFEATING THE MONSTERS EACH SURVIVOR RECEIVES n EXPERIENCE POINTS" (shot
  `battle_won`). Monsters often run away from a level 20 party, and the fixed fight's monsters depend on the
  party (Battle Rats for level 1, Slither Beasts and Mutant Larvae for the strengthened one).
- **verified** Losing: "name GOES DOWN!!!", then "THE SHADOW OF DEATH HAS FALLEN UPON YOUR PARTY! ... RENEW YOUR
  QUEST FROM THE LAST INN IN WHICH YOU STAYED BY PRESSING 'RETURN'" (shot `gameover`: `@party,LOWHP`, the fight,
  everyone blocks).
- **verified** Title: `space` shows "Book One - Secret of the Inner Sanctum" for a few seconds, then demo scenes
  on each `space`: inn door, cavern, two text pages, a treasure chest, then the first title picture again.
- **verified** Wilderness: "IMPASSABLE" over mountains that block the way.

## Shortcuts for cataloguing (tour 2026-11-18)
| What | How | Status |
|---|---|---|
| Character records | main memory store `2C000 + 80*n` (language card RAM, not mapped while the game waits for a key: use the `2xxxx` addresses). Layout as in the DOS notes: name 0-0F, statistics 15-22 (current/maximum pairs: INT MGT PER END SPD ACY LUC), level 23-24, age 25, experience 27 (4 bytes), spell points 2B and 2D, spell level 2F-30, gems 31, hit points 33/35/37, gold 39 (3 bytes), food 3E, equipped 40-45, backpack 46-4B, quest marks 7D | verified |
| Strong party | `POWER`: statistics 40, level 20, 900 hit points, 300 spell points, spell level 7, 50 gems, 20,000 gold, 40 food for all six. `EQUIP:n` equips backpack item A. Checkpoint `strong` = `@party,POWER`, clubs equipped | verified |
| Gold, experience | `set:2C039=5000:3`, `set:2C027=1600:4` (RYZ; next member +80) | verified |
| Light | `LIGHT` = MNZ casts sorcerer spell 1-6 (`CAST:member:level:number`); cast it before a warp into a cavern, castle or dungeon | verified |
| Change area | `WARP:lo:hi:ss` from anywhere in Sorpigal: rewrites the map id and section of Sorpigal's "passage outside" event (code at `A719`: `LDA #10, STA 80, STA 81, LDA #lo, LDX #hi, LDY #sec, JMP 0878`) and takes it. Ids and sections are those of the DOS port's area table (all 54 tried). Arrival square is (10,10); `poke:A71A=nn` before the warp arrives at (nn,nn) instead. Then `DISK:n` if the game asks | verified |
| Disk after a warp | section 1 (towns, caverns): none, they are on disk B; section 2 (wilderness A1-E4): `DISK:3`; section 3 (castles, dungeons, Astral Plane): `DISK:4` | verified |
| 1 hit point each | `LOWHP` | verified |
| Ending | `WORTHY` (quest marks: record +7D = 5F for all), `LIGHT`, `poke:A71A=06,WARP:1A:0B:03,DISK:4`, `AT:06:07:76,FN,left,w500`: the man in the white coat; `space`: the Inner Sanctum text with the performance total and 500,000 experience; `space`: "INSERT DISK B", back to Sorpigal. Without `WORTHY`: "YOU ARE NOT YET WORTHY FOR TRANSFER. RETURN AFTER DEFEATING THE IMPOSTER." | verified |
- Astral Plane: arriving on (10,10) sends the party back to Sorpigal at once (the game asks for disk D, then B).
- Seen on arrival by warp: encounters with a monster picture (CAVE4: Demon Dogs, Wolverines, Fire Beetles; D3:
  Minor Demons, Killer Bees, a 5 Headed Hydra, Dung Beetles), "A GLOWING POLYHEDRON IS SET ON SIDE 11" (CAVE8),
  "IT'S HOT!" in the desert sectors, "ECTOPLASMIC SLIME SLUSHES BENEATH YOU!" (E4).
- Services used in Sorpigal: training costs 3000 gold at level 20; a drink 1 gold; rumor "ALL PORTALS ARE
  CONNECTED!"; the leprechaun takes 1 gem and puts the party in the chosen town.

## The DOS set replayed here (2026-11-18)
The DOS version's 250 shot routes were translated and replayed on this version: `set:`/`poke:` addresses of the
character records move from `1682C + 80*n` to `2C000 + 80*n`, waits are roughly doubled, a `w100` follows every
key that had no wait, and the macros below take the DOS arguments. 231 of them are in the set under the DOS
ids; the DOS documents' squares, events, shop lists, quests and monster groups all appeared as described.
| Macro / checkpoint | What |
|---|---|
| `WARPX:xx:yy:lo:hi:ss` | area change with an arrival square: a 17-byte routine at `0110` (free stack space) sets x, y, map id and section and jumps to the loader, and Sorpigal's exit at `A719` is made to jump to it; then the exit is taken and `SEC01`/`SEC02`/`SEC03` answer the disk prompt (none, disk 3, disk 4) |
| `DSTRONG`, `DVET` | the DOS set's hit-point boost and its level 7 veteran party (experience, spell points, spell levels, gems) |
| `QA`, `BLK`, `FLAME` | `ctrl+a`, block, and the DOS Flame Arrow opening (kept for the routes; `ctrl+a` did nothing seen here) |
| `blacksmith`, `equipped`, `combat` | RYZ with 1873 gold at the blacksmith; after buying Short Sword and Leather Armor; the fixed fight behind the door CUBI unlocks (three Orcs here) |
| `cave1`, `portsmith`, `algary`, `dusk`, `erliquin`, `wild`, `areaa1`, `areae1`, `alamar`, `doom`, `whitewolf`, `qvl1`, `astral` | the DOS checkpoints of the same names (`wild` = DOS `outdoors`) |
- Combat by hand: only members with a `+` are offered `a`; `f` asks "FIGHT WHICH 'A'-'B'?", `e` "EXCHANGE PLACES
  WITH (1-6)?", `u` "USE WHICH", `c` level, number, `enter`, then "CAST ON: 'A'-'C'?". Messages last about 2 s:
  to catch one, end the route on `do!` (no settle) about 150 frames after the key.
- Seen here and not on DOS: Search after the won Orc fight found an Iron Chest ("IT OPENS! EACH SHARE IS WORTH 3
  GOLD, RYZ FOUND LARGE SHIELD").
- Routes that did not carry over (dropped, listed in `design/systems.md` "Apple II"): missile weapon, Sleep,
  Identify Monster, Fire Ball, a dragon's breath, stoning, the paid bribe.

## Controls
The screen lists its keys. Verified so far: arrows `up`/`down` step forward/back, `left`/`right` turn (also
`enter` forward, `/` back per the on-screen list); `1`-`6` character sheet, `esc` back; `y`/`n` prompts; in
the inn `a`-`f` view, `ctrl+a`-`ctrl+f` add/remove, `x` exit. On screen and not tried: `o` order, `p` protect,
`r` rest, `s` search, `b` bash, `u` unlock, `q` quick reference, `#` view characters. The DOS port's playbook
(`games/dos/might-and-magic/playbook.md`) describes the same game: its town layout and event squares matched
here (inn, market at (10,5) facing east, exit at (12,0), stairs at (14,0)).

Input timing: one key at a time (the Apple II keyboard is a latch): wait for the screen before typing for it.
Loading from disk takes 5-10 s per area: `w600` after a disk change.

## RAM (zero page, verified in Sorpigal and outdoors by walking and turning)
| Address | What |
|---|---|
| `0080` / `0081` | party x (east) / y (north), 0-15 |
| `0082` | y * 16 + x |
| `0085`-`008C` | facing tables; `0085` = C0 north, 30 east, 0C south, 03 west (macros `FN FE FS FW` write all eight bytes) |
`AT:xx:yy:oo` (hex) + a facing macro + a turn moves the party. To fire an event that needs facing D: set the
facing one turn clockwise of D and press `left` (`AT:0C:00:0C,FW,left` = passage outside, which wants south).

## Game structure
Modes, menu tree, areas/levels/worlds in order, what unlocks what. Enough to plan a capture route.

## Shot plan
What this game needs in the database (see `docs/capture-guide.md`): the systems and screens that make it
distinctive. One line per planned shot id; the routes go into `shots.txt`.
- [ ] `title_screen` - title
- [ ] ...

## Strategy and walkthrough notes
How to progress quickly and safely: the critical path, dangerous spots, boss patterns, grinding needs, what to
buy. Keep it to what an agent needs to reach the shot targets.

## Naming
Main character: **ryz** (owner's rule); further party members condi, ebo, cubi, deddo, mnz. Name-entry controls
and the token route that types the name: ...

## Shortcuts
Cataloguing beats fair play: completed saves, passwords, GameShark (`gs:`) and Game Genie (`rom:` variant)
codes, debug menus, level select, sound test, RAM pokes. Values that show on screen stay realistic.
| What | How (tokens / prefix / code) | Source | Status |
|---|---|---|---|

### Saves (rom/saves/apple2/might-and-magic/, never committed)
| Name | Contents (progress, party, items) | URL | SHA-1 | Status |
|---|---|---|---|---|

## RAM map (for `game.json` "ram" watches and pokes)
| Address | Size | Meaning | How found |
|---|---|---|---|

## Emulation notes
Model choice (GB: DMG/CGB/SGB; NES and SNES: ntsc/pal) and why, RNG behaviour, lag, screens that never settle (animations), anything that
broke a route.

## Checkpoints
Named states are in `checkpoints.txt` (built from routes, never committed as files). Describe the important ones
here if their purpose is not obvious from the name.

## Sources
| Source | URL | Used for | Accessed |
|---|---|---|---|

## Open questions
