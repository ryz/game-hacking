# Might and Magic: Secret of the Inner Sanctum (NES, USA) - playbook

Everything an agent needs to play this game efficiently: read it before playing, add to it after every run.
Status of each fact: **verified** (seen in the emulator, with the route) or **source** (manual/FAQ/wiki, not yet
checked). Never delete a fact that turned out wrong: strike it and say what is true.

## Identity
| Field | Value |
|---|---|
| Title (EN / original) | Might and Magic: Secret of the Inner Sanctum (US NES; title screen "Might and Magic", copyright page "Might and Magic book 1") (verified) |
| Platform / model used | NES, NTSC (`game.json`); NES 2.0 header, mapper 4 (MMC3), 256 KiB PRG + 256 KiB CHR, 8 KiB battery RAM; CRC32 `ab3dc7a6` |
| Release (region, year) | North America 1992 (dispatch); copyright page: original (c)1987 New World Computing, NES source code (c)1991 G-Amusements (verified) |
| Developer / publisher | NES version G-Amusements Co., Ltd.; published by American Sammy Corp.; original New World Computing (copyright page, verified) |
| Genre | First-person party RPG on 16x16-square maps: towns, caves, outdoor VARN, castles, dungeons |
| Players / save system | 1 player; **battery save**: sign in at an inn ("Push A button and save your adventure.") (verified: `01_party` reloads with the party); one slot, Continue on the title |

The NES version names only the hero (a Knight); the other five party members are **fellows** picked from a
fixed roster of fifteen at the inns (Member > Add), each living in one town (verified).

## Boot sequence
- Power-on: "Licensed by Nintendo" (f60-f240), copyright page (f300-f480), black, title with star field and
  "Continue / New Game" from ~f660 (intake sheet, verified).
- `TITLE` = `w700` -> title, cursor on Continue (verified, checkpoint `title`; the stars animate, `settle` never
  stops there: use `!` or exact waits).
- `NEWGAME` = `TITLE,right,a,w400,a,w200`: New Game -> owl animation -> "Welcome to our town Sorpigal." (A) ->
  "What is your name?" keyboard (verified).
- `RYZ` = `b,b,b,down,right*7,a,w20,right*7,a,w20,right,a,w20,down,a,w60`: types RYZ and ENTER. The three B
  presses are padding: the first presses on the keyboard are dropped (a varying number), and B (delete) on an
  empty name is harmless (verified: name bytes `1B 22 23` at $7F00).
- `START` = `NEWGAME,RYZ,a,w90,a,w60`: "Be careful! This town is quite dangerous..." -> Sorpigal (8,5) facing
  north, "GO AHEAD FIGHTERS!" (verified, checkpoint `start`).
- `CONTINUE` = `TITLE,a,w300`: loads the battery save (verified with `sav:01_party`: the party of six, Sorpigal
  (8,5) facing north).
- Party: `@start,NAMES,INN,SIGNIN,FELLOWS,...` (route of checkpoint `party`, see Naming).

## Controls
| Context | Button | Action | Status |
|---|---|---|---|
| Title | Left/Right, A | Continue / New Game | verified |
| Name keyboard | Left/Right | move along a row of 20 (wraps); cursor starts at column 0 of row 0 | verified (code bank 12 $97AA) |
| | Up/Down | row 0 `0-9 A-J`, row 1 `K-Z . , - space`, row 2 ENTER (wraps) | verified |
| | A | type the letter (ENTER on row 2 finishes; refused while empty); 6 letters max | verified |
| | B | delete the last letter | verified |
| Exploration | Up | step forward | verified |
| | Down | step back (not through doors) | verified |
| | Left / Right | turn 90 degrees | verified |
| | B | step forward (same as Up) | verified ((8,5) -> (8,4)) |
| | A | menu: Search, Open, Row, Camp, Speed, Cast, Use, View, Prot, Cancel (two columns: left Search..Speed, right Cast..Cancel; cursor starts on Search every time) | verified |
| | Camp | "Rest here?" - **No opens the item menu** Equip, Remove, Trade, Drop, Share (Equip: Who? -> item -> WHERE? slot) | verified (capture; handler bank 22 $853A) |
| | View | five pages per member (A pages on, B back): profile, stats, HP/MP/gems/gold/food, equipped, backpack | verified |
| | Select | automap (visited squares; "Darkness..." in dark areas) | verified |
| | Start | redraw the view / close messages | verified (code bank 29 $A4AC) |
| Inn | Up, A | sign-in prompt: Up toggles No -> Yes | verified |
| | A / B | menus Member (Add, Remove, View, Quit), Rest, View, Cancel / back | verified |
| Battle | A, D-pad | Attack, Bribe, Run, Giveup; then per member Auto, Fight, (Cast or Shoot), Block, Row, Use, View, Prot, Run; each member acts right after its order | verified (capture) |
| Shops | Up, A | prompt Yes/No ("Can I help you?"), then the service menu; B leaves sub-menus | verified |
Joypad dispatch in exploration: bank 29 $A304 (bit order Right, Left, Down, Up, Start, Select, B, A) (code).

Input timing: input waits for a change of the pad state, so the default press works, but **a press that comes
while a sign or prompt is still being drawn is lost**: after turning to face a shop/inn door the sign text eats
the next press; prompts need ~300 frames (`w300`) before Up toggles Yes/No; the name keyboard drops its first
presses (padding Bs). Use one action per `do` while exploring, or long waits in macros.

## Game structure
- Towns (ids 01-05): Sorpigal, Portsmith, Algary, Dusk, Erliquin: inn, blacksmith, food, temple, training,
  signs (ROM text: "THE INN OF SORPIGAL", "B AND B BLACKSMITHS", "EULARD'S FINE FOODS", "INN OF PORTSMITH",
  "THE INN OF ALGARY", "THE INN OF ERLIQUIN"...).
- Inn: "Would you like to sign in?" -> Yes saves -> Member (Add / Remove / View / Quit), Rest, View, Cancel
  (verified). Fellows of another town show "Another town" and cannot be added ("Wrong choice").
- Fellows (roster slot, name, class, home town; verified in RAM + Add list): 1 Rigel Wizard Sorpigal, 2 Sage
  Robber Sorpigal, 3 Sonja Knight Sorpigal, 4 Lilac Wizard Sorpigal, 5 Vyrana Cleric Sorpigal, 6 Azalea Archer
  Erliquin, 7 Kirie Cleric Erliquin, 8 Flint Robber Erliquin, 9 Jhared Knight Erliquin, 10 Bulzai Archer
  Algary, 11 Zora Wizard Algary, 12 Thorak Cleric Algary, 13 Tikra Knight Portsmith, 14 Charob Robber
  Portsmith, 15 Hammer Paladin Dusk. Class abbreviations on screen: KN PA AR CL WI RO.
- Areas: 55 maps (towns, caves, VARN A1-E4, castles, dungeons, City of Gold "P-PEEK", Astral Plane, Soul Maze):
  `design/maps.md`.
- Story (ROM text): rumours ("The King is in seclusion.", "The Inner Sanctum is a myth.", "The canine has the
  Key."), the impostor king; ending text "Welcome to your Inner Sanctum ... transfer to another World ... Gates
  to Another World" (file 0x14FCA). All decoded strings: `work/scout/might-and-magic/strings.txt` (scratch;
  regenerate with `work/scout/might-and-magic/strings.py`; text encoding below).

### Map data (for floor maps in `design/maps/`)
- 55 slots of 0x200 bytes from file offset `0x32010` (PRG 8 KiB banks 25-28), slot = area id - 1: 256-byte
  wall map + 256-byte property map, square index `y*16 + x` (x east, y north, (0,0) south-west) (verified:
  RAM $6200 after a warp equals slot 5; Sorpigal = slot 0).
- Wall byte: `N<<6 | E<<4 | S<<2 | W`, 0 open, 1 wall, 2 door, 3 per-area type (ornament / outdoors terrain).
  Property byte: 80 event, 40 blocked N, 20 dark, 10 blocked E, 08 no camp, 04 blocked S, 02 anti-magic,
  01 blocked W (flag names Data Crystal, bit positions checked: blocked bits match wall type 1 in caves 100%).
- Map headers: 78 bytes per area from `0x38E7E` (area label, then palettes/music/encounter data, not decoded).
- Exits are code, not data: each area's event script compares $A1 (y*16+x) and sets $9D (target), $9F/$A0
  (banks 0-10, pattern `LDA #map STA $9D LDA #x STA $9F LDA #y STA $A0 JSR $F817`). Script of area N = entry E
  (JMP table at $8000) of PRG bank B, with (B, E) pairs at bank 29 $A1B7 + 2*(N-1) (decoded 2026-11-18;
  `maps.py exits()`; table in `design/maps.md` section 5). $9D codes $80+ open services (80 inn, 81 blacksmith,
  82 market, 83 tavern, 84 temple, 85 training, 8C guild).
- Outdoor terrain: side value 1 forest, 2 mountains, 3 water (desert in D1 D2 E1 E2); the blocked bits decide
  passing (`design/maps.md` section 4, verified).
- Renderer: `python3 games/might-and-magic/tools/maps.py --text` -> `design/maps/NN_name.png` (55),
  `varn_atlas.png`, `maps.txt` (done).

## Shot plan
Capture 2026-11-18: main set of ~90 shots in `shots.txt` (game order). Done: town life (inn, blacksmith, market,
temple, training + level-up, guild, tavern + rumour, leprechaun, camp/items, view pages, automap), combat (orders,
targets, both spell lists, hit/kill, Flame, victory, chest + trap + loot, deaths, game over), world (4 towns,
5 VARN sectors + desert/water messages, Dusk cave, Volcano, 4 castles, Dragadune, Enchanted Forest, City of Gold,
Soul Maze, cavern portal), ending (Inner Sanctum, 5 pages). Not done: the Castle Alamar boss (see Strategy).
Scout's plan (kept for history): 16 routed shots in `shots.txt` (boot, title, owl intro, naming, first control, sign, inn sign-in/save/menu/
fellows/party, exploration menu, automap, cavern); the rest are commented plan lines there:
- [ ] inventory: View character sheet; camp menu; equipment
- [ ] battle (3-5): command menu, member orders, attack messages, victory with gold/experience, treasure chest;
  random encounters come by themselves in Sorpigal (a Rabid Jackal after a few steps from `@start`)
- [ ] shops: B and B Blacksmiths, Eulard's Fine Foods, temple, training (doors around Sorpigal (8,5): east
  food, west blacksmith; walk in)
- [ ] gameplay per area type: the other four towns (warp 02-05), VARN outdoors (0F-22), a castle (23-27),
  Dragadune / Enchanted Forest / Quiv / Raven's Wood dungeons, City of Gold, Astral Plane, Soul Maze
- [ ] boss (Castle Alamar), Inner Sanctum ending text, game over (poke party HP to 1 before a fight)
Reach: everything by warp (below) from `@party`; boss/ending need the event squares found with the maps.

## Strategy and walkthrough notes
- **Capture checkpoints** (2026-11-18): `town` (street, pocket gold), `bought` (blacksmith, RYZ with Short Sword +
  Scale Armor), `fight` (level-1 fight in Sorpigal), `vets` (level 9 party saved at the inn = `saves/02_veterans`),
  `cavefight` / `cavefight2` / `chest` (cavern fight and its chest), `worthy`, `sanctum` (ending start).
- **Event scan** (the fastest way to learn an area): warp next to every event square facing it, step in,
  screenshot (`work/mm/scan4.py AREA @base "up,w300"` in the capture run; rebuild from this description: four
  approaches per square, facing poke `poke:00A2=`, `WARP_GO`, `up,w300`). Many events need a given facing.
- **Fights on demand**: warp onto a fight square, e.g. Sorpigal (5,3) (goblins + skeletons) or Sorpigal Cavern
  (1,1) (Wolverines + Savage Shrews: `@cavefight`). Monster HP are bytes at $03F0.. (one per list slot); poke them to
  1 each turn (`poke:03F0=010101010101,a,w150` loops) to end fights quickly. Party HP to 1 (record +$23) gives a
  game over in ~19 such loops.
- Battle and story messages type out: catch the frame with `do! "w20"` steps and snap; menus that close fast
  ("RYZ gets an item") need `a,w120` exactly.
- **Ending**: from any checkpoint warp onto Astral Plane (6,7) facing west:
  `poke:009D=36,poke:009F=06,poke:00A0=07,poke:00A2=03000102,WARP_GO,w300`, then `a,w300` per page.
- **Facing in event scripts**: the script's facing code is not $A2: the Inner Sanctum code tests 0 and fires
  with $A2 = 3 (west); the "not worthy" square tests 1 and fires with $A2 = 2. Map exits by experiment.
- Boss (not done): the impostor King Alamar is in Castle Alamar (ROM text "The omnipotent King Alamar speaks",
  bank 3 near file 0x07642); the true king's message mentions the Eye of Goros. Event scan of Castle Alamar in
  the capture run did not show the throne fight within budget.
- **Warp** (verified on 06, 0B, 0F, 23, 30): `poke:009D=ID,poke:009F=X,poke:00A0=Y,a,w60,b,w180` (macro
  `WARP_GO` = `a,w60,b,w180`). The A press opens the exploration menu, whose handler does not clear the
  pending area $9D; B closes it and the main loop loads area ID at (X,Y) (code bank 29 $A0A9/$A12A). Facing is
  kept. Poking $9E alone only swaps graphics (wrong map, wrong label).
- Check the target square in `design/maps/maps.txt` (open, no event) before warping; step onto red squares to
  trigger their events.
- Level 1 fellows die fast: poke HP/levels in the character records (layout below; fix the check byte) before
  long fights, or freeze HP.
- Random encounters happen while walking and even when turning in Sorpigal; for routes that must not fight,
  keep waits fixed (RNG follows frames).

## Naming
- Hero: **RYZ** (the only name the game asks for), Knight (fixed class) (verified).
- Fellows renamed to the owner's standard party by pokes into the name table before Member > Add (macro
  `NAMES`; the game keeps the names in battery RAM and they survive power-off, verified with `01_party`):
  | Slot | Party name | Fellow (original name) | Class | Race / sex / alignment |
  |---|---|---|---|---|
  | 2 | CONDI | Hammer (slot 15, home Dusk) | Paladin | (record: human?) male |
  | 3 | EBO | Vyrana (slot 5) | Cleric | human female good (verified card) |
  | 4 | CUBI | Sage (slot 2) | Robber | |
  | 5 | DEDDO | Rigel (slot 1) | Wizard (sorcerer) | elf male neutral (verified card) |
  | 6 | MNZ | Azalea (slot 6, home Erliquin) | Archer | female |
- Hammer and Azalea do not live in Sorpigal: `NAMES` also pokes their home town to Sorpigal (record +$6F = 01)
  and fixes their check byte (+$7F = sum of bytes +$00..+$7E, mod 256).
- `FELLOWS` (from the inn menu): Member, then Add five times with cursor moves down 15 / up 10 / up 3 / up 1 /
  down 5 (the Add cursor stays where it was).
- Stats are the fellows' own (level 1, not rolled; no cheat needed).
- Party checkpoint route: `@start,NAMES,INN,SIGNIN,FELLOWS`, b, b, then re-enter the counter square and sign
  in again to save (route in `checkpoints.txt`).

## Shortcuts
| What | How (tokens / prefix / code) | Source | Status |
|---|---|---|---|
| Warp to any area/square | `poke:009D=ID,poke:009F=X,poke:00A0=Y,WARP_GO` | scout (code) | verified |
| Face a direction | `poke:00A2=DDEEFFGG` (facing, right, back, left: e.g. south `02030001`) then Up | scout | verified |
| Rename fellows | name table $7F00 + 16*slot (text code, FF end) | scout | verified |
| Move a fellow to this town | record +$6F = town (1 Sorpigal, 2 Portsmith, 3 Algary, 4 Dusk, 5 Erliquin), fix +$7F | scout | verified |
| Game Genie / debug menu | none found (Data Crystal lists no codes; TCRF, GameFAQs blocked) | - | - |
| Fixer hack | "Might and Magic Fixer" by Reiska (bug-fix hack, Data Crystal); not used (not supplied by the owner) | Data Crystal | source |

### Saves (rom/saves/might-and-magic/, never committed)
| Name | Contents (progress, party, items) | URL | SHA-1 | Status |
|---|---|---|---|---|
| none downloaded | GameFAQs blocked (403) | - | - | - |
Own exports: `saves/01_party.sav` (party of six, level 1, Sorpigal), `saves/02_veterans.sav` (level 9 party,
gold and gems, Sorpigal inn; poked records survive the reload, checked 2026-11-18); see `saves/README.md`.
Record pokes: `python3 games/might-and-magic/tools/rec.py DUMP.json SLOT field=value ...` prints poke tokens with
the fixed check byte (dump with `play.py dump NAME`).

## RAM map (for `game.json` "ram" watches and pokes)
| Address | Size | Meaning | How found |
|---|---|---|---|
| $009D | 1 | pending area id (1-$37 = load that area at $9F/$A0 when the main loop sees it; $40-$49 = event codes) | code, verified |
| $009E | 1 | current area id (slot + 1; 01 Sorpigal) | Data Crystal "location", verified |
| $009F / $00A0 / $00A1 | 1 each | x, y (0-15, y north), y*16+x | Data Crystal, verified |
| $00A2-$00A5 | 4 | facing, right, back, left (0 N, 1 E, 2 S, 3 W) | Data Crystal + diff, verified |
| $00A6 | 1 | party size | inferred (1 after naming) |
| $00A7-$00AC | 6 | party member roster slots | Data Crystal |
| $028F-$0294, $028C | 6+1 | name entry buffer, length; $02A4 column, $028B row | code, verified |
| $6200 / $6300 | 256 each | current area walls / properties | Data Crystal, verified |
| $6880 + $20*(id-1) | 32 each | automap (visited squares) per area | Data Crystal |
| $03F0-$03F5 | 6 | monster hit points in battle (list order; poke 01 to end a fight) | find + verified |
| $6F00 + $80*slot (more) | | +$15 age, +$17..+$19 experience (3 bytes LE), +$1B/+$1C MP current, +$1D/+$1E MP max, +$1F/+$20 spell level, +$21/+$22 gems, +$23/+$24 HP current, +$25/+$26 HP max, +$27/+$28 HP base, +$29..+$2B gold (3 bytes LE), +$2F food, +$31..+$36 equipped item ids, +$37..+$3C backpack item ids, +$43.. backpack charges; hero only: +$61..+$64 quest bytes (copied to $75..$78 when a script loads the hero), +$72..+$77 party roster/size | View pages + pokes (verified); item ids: 01 Club, 05 Short Sword, 7B Scale Armor |
| $6F00 + $80*slot | 128 | character records (slot 0 hero, 1-15 fellows): +0 sex (1 M, 2 F), +1/+2 alignment (1 good, 2 neutral, 3 evil), +3 race, +4 class (1 KN, 2 PA, 3 AR, 4 CL, 5 WI, 6 RO), +5..+$12 seven stats as current/max pairs (Intellect, Might, Personality, Endurance, Speed, Accuracy, Luck), +$13/$14 level, +$6F home town, +$7F check byte = sum(+0..+$7E) mod 256 | RAM + Data Crystal; check byte verified on 16 records |
| $7F00 + $10*slot | 16 | names (text code, $FF end) | verified |
Text code: `0-9` = 00-09, `A-Z` = 0A-23, `a-z` = 40-59, space FE, line end FF, `-` 26, `.` 24, `,` 25, `"` 7A/7B.

## Emulation notes
- NTSC, default press (hold 8, wait 40) works; lost presses come from screen drawing, not from timing (above).
- `settle` never stops on the title (stars) and on screens with a blinking cursor (Yes/No box): use `!`/waits.
- Checkpoints `title`, `start`, `party`, `cavern` rebuilt from an empty cache give identical frames (2026-11-18).
- Battery RAM: the save is the whole 8 KiB at $6000; records carry a check byte (see RAM map); whether a bad
  check byte is repaired or wiped at power-on was not tested (poked records were fixed before saving).

## Checkpoints
- `title`, `start` (RYZ alone, Sorpigal (8,5) N), `party` (party of six, inn counter (8,3), saved),
  `cavern` (warp example: Sorpigal Cavern (1,14)); capture: `town`, `bought`, `fight`, `vets`, `cavefight`,
  `cavefight2`, `chest`, `worthy`, `sanctum` (see Strategy).

## Sources
| Source | URL | Used for | Accessed |
|---|---|---|---|
| Data Crystal RAM map | https://datacrystal.tcrf.net/wiki/Might_and_Magic:_Secret_of_the_Inner_Sanctum/RAM_map | position, area, roster, automap, map RAM | 2026-11-18 |
| Data Crystal ROM map | https://datacrystal.tcrf.net/wiki/Might_and_Magic:_Secret_of_the_Inner_Sanctum/ROM_map | map and header offsets, area names (its map list is shifted from slot 6 on; the header list is right) | 2026-11-18 |
| Data Crystal Maps / main page | https://datacrystal.tcrf.net/wiki/Might_and_Magic:_Secret_of_the_Inner_Sanctum/Maps | property flag names; Fixer hack | 2026-11-18 |
| GameFAQs, StrategyWiki | gamefaqs.gamespot.com, strategywiki.org | - | 403 (unavailable) |
| NES Adventurer's Guide (cluebook) | mocagh.org/nwc/mm1nes-cluebook.pdf | - | host outside the network |
| ROM text and code | this ROM | controls, menus, names, warp, save | 2026-11-18 |

## Open questions
- ~~Outdoor terrain types and the VARN layout~~ (done 2026-11-18: maps.md sections 3-4).
- Castle Alamar boss fight square and its condition; the "not worthy" square's test.
- Map header fields after the label (encounters, music, palettes).
- ~~Exits between areas~~ (coded warps tabled in maps.md; run-time exits such as stairs not tabled).
- Does a bad record check byte get wiped at power-on? (poked records were fixed, so not needed yet)
- B in exploration also steps forward: is it really "forward" or "forward ignoring something"? (code $A4CF not read)
