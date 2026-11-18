# Pokémon Blue Version - playbook

Everything an agent needs to play this game efficiently: read it before playing, add to it after every run.
Status of each fact: **verified** (seen in the emulator, with the route) or **source** (manual/FAQ/wiki, not yet
checked). Never delete a fact that turned out wrong: strike it and say what is true.

## Identity
| Field | Value |
|---|---|
| Title (EN / original) | Pokémon Blue Version / Pocket Monsters Ao (the Western Blue is built on the Japanese Blue engine with Red/Green's Pokémon distribution) (source: Wikipedia) |
| ROM | No-Intro "Pokemon - Blue Version (USA, Europe) (SGB Enhanced)", CRC32 d6da8a1a, SHA-1 d7037c83..., header `POKEMON BLUE`, MBC3+RAM+BATTERY, 1 MiB, 32 KiB SRAM, version 0 |
| Platform / model used | Game Boy, `dmg` (see `game.json`); SGB-enhanced (see Emulation notes) |
| Release (region, year) | North America 1998-09-28, Europe 1999 (Japan: Blue 1996) (source) |
| Developer / publisher | Game Freak / Nintendo (title screen: "©'95.'96.'98 GAME FREAK inc." verified) |
| Genre | Turn-based monster-collecting RPG, top-down overworld |
| Players / save system | 1 player; link cable for trades/battles (2 players). One battery save slot (START > SAVE, anywhere in the field) |

## Boot sequence
Verified 2026-11-15 (all macros in `game.json`):
- Copyright f~180, Game Freak logo f~420-660, intro fight (Gengar vs Nidorino) f~720-1200, title from ~f1320.
- `TITLE` = `w1400,settle` -> title screen (the Pokémon next to the player cycles every few seconds).
- Title: START -> white fade -> main menu (needs `w60` after the press; settle can stop on the white frame).
  Main menu: NEW GAME / OPTION (no save) or CONTINUE / NEW GAME / OPTION (save present).
- `NEWGAME` = `INTRO,NAME_RYZ,RIVAL_RED,mash:a:300,settle,mash:a:150,w300,settle` from the title:
  - `INTRO`: start, Oak's speech with measured `mash:a` blocks, ends on the player name menu (NEW NAME / BLUE / GARY / JOHN).
  - `NAME_RYZ`: NEW NAME, SELECT (lower case), types r-y-z, START. Text: "Right! So your name is ryz!".
  - `RIVAL_RED`: rival speech, picks the first default name RED (menu NEW NAME / RED / ASH / JACK).
  - then the shrink animation and the bedroom.
  **Never mash A past "First, what is your name?"**: the naming keyboard types A's (seen: "AAAAAAA").
- `CONTINUE` = `start,w200,a,w200,a,w200,settle` from the title with a save (verified with `sav:02_late_game_test`).
- Checkpoints: `title`, `start` (bedroom, first control, map 38 y6 x3), `late` (RAM recipe + Indigo Plateau lobby).

## Controls
| Context | Button | Action | Status |
|---|---|---|---|
| Title | Start / A | main menu | verified (Start) |
| Field | D-pad | walk; one tile = hold 16 frames (`right:16`), a press while facing elsewhere turns + walks | verified |
| Field | A | talk / examine (facing) | verified (nurse, Cable Club) |
| Field | B | cancel; hold-to-run does not exist (Bicycle item is the fast mode) | verified (B closes menus) |
| Field | Start | menu: POKéDEX (after getting it), POKéMON, ITEM, <player>, SAVE, OPTION, EXIT; cursor position is remembered | verified |
| Field | Select | register/swap items in lists (source) | source |
| Name entry | D-pad/A, B, Select, Start | move/type, delete, toggle upper/lower case, finish | verified (Select, A, Start) |
| Party menu | A | sub-menu: field moves (SURF, STRENGTH...), STATS, SWITCH, CANCEL | verified |
| Summary | A | page 1 (stats) -> page 2 (EXP, moves) -> close | verified, but see timing |
| Battle | A/B, D-pad | FIGHT/PKMN/ITEM/RUN 2x2 menu; A picks, B backs out; FIGHT/move cursors are remembered, so repeated `a,w50,settle` keeps using the same move | verified |

Input timing: default press (hold 8 / wait 40) works in menus, dialogue and naming. Dialogue at MEDIUM speed
ignores A while a line is typing; use `mash:a:N` in measured blocks or set FAST text (`FASTTEXT` macro,
`poke:D355=01`; verified on the OPTION screen). Summary screen: the first A after it opened was ignored twice; `w120,a:20` worked.
Door mats/exits need a D-pad press onto the mat in the exit direction (`down:16`).
**Wild encounters need held walking**: 18 single-tile `up:16`/`down:16` taps in Route 1 grass gave no battle, even
with `poke:D887=FF` (grass rate max); `down:64` (one 4-tile hold) started one at once. Use long holds + D887=FF.
**After `goto`, `snap` captures a black frame** (no frame rendered yet): always `do "settle"` (or any token) first.
~~New macros need a session restart~~ (fixed 2026-11-15: game.json is re-read on every `do`).
**Start-menu and party cursors are remembered** (also inside checkpoints): after a checkpoint the START cursor may
sit on ITEM or ryz, the party cursor on PIDGEOT. Look before pressing `down*N`.
**Mashing into battles/menus**: `mash:a:300` blocks after a Gym Leader/Champion talk run straight into the
battle; take one block at a time and peek D057.
**emu.py vs play.py timing for `!` frames**: an animation frame found with `tools/emu.py` (per-token PNGs)
did not appear at the same `wN` in play.py (Safari rock: emu showed the rock at `w30`, play/shoot.py never);
pick animation frames in play.py (shoot.py reproduces play.py).

## Game structure
- Start: Pallet Town (bedroom 2F -> 1F -> outside). Walking into Route 1 grass triggers Oak -> his lab -> starter
  (Bulbasaur/Charmander/Squirtle) -> first rival battle -> Viridian Mart parcel -> Pokédex. (source)
- 8 gyms in order: Brock (Pewter, Rock), Misty (Cerulean, Water), Lt. Surge (Vermilion, Electric), Erika
  (Celadon, Grass), Koga (Fuchsia, Poison), Sabrina (Saffron, Psychic), Blaine (Cinnabar, Fire), Giovanni
  (Viridian, Ground). Then Route 22/23 badge gates, Victory Road, Indigo Plateau: Elite Four (Lorelei, Bruno,
  Agatha, Lance) and the Champion (rival), Hall of Fame, credits. Post-game: Cerulean Cave (Mewtwo). (source)
- Key dungeons/areas: Viridian Forest, Mt. Moon, S.S. Anne (HM01 Cut), Rock Tunnel (Flash), Pokémon Tower
  (Silph Scope from Rocket Hideout under Game Corner), Silph Co., Safari Zone (HM03 Surf, Gold Teeth -> HM04
  Strength), Seafoam Islands, Pokémon Mansion, Power Plant. Fly is HM02 (Route 16 house). (source)
- Map ids: `work/scout/pokemon-blue/pokered/constants/map_constants.asm` (pret); key ones: Pallet $00, Viridian
  $01, Pewter $02, Cerulean $03, Indigo Plateau $09, Red's house 1F $25 / 2F $26, Oak's lab $28, Viridian Forest
  $33, Pewter Gym $36, Mt. Moon 1F $3B, Celadon Game Corner $87, Pokémon Tower 1F $8E, Safari Zone center $DC,
  Silph Co 1F $B5, Indigo lobby $AE, Lorelei $F5, Bruno $F6, Agatha $F7, Lance $71, Champion $78, Hall of Fame $76.

## Shot plan
Main set ~45 shots (`shots.txt` has the planned ids; lines with routes are ready). Method per target:
| Group | Shots | Method |
|---|---|---|
| boot/title/menus | boot_gamefreak, intro_fight, title_screen, menu_main, options | routes exist (intro frames: `do!` + `wN`) |
| new game | oak_intro, oak_name_menu, naming_player, naming_rival, start_room | `NEWGAME` pieces (routes exist) |
| early story | pallet_town, oak_lab_choose, battle_rival_first | **play** from `@start` (short, ~5 min) |
| overworld | route/town/cave/forest/building, ss_anne, pokemon_tower, silph_co | `MID`/`LATE` + **door warp** (below) |
| services | pokecenter_nurse/heal (done in scout), mart_buy, pc_bills | warp to a town's Center/Mart ($29/$2A, $3A/$38...) |
| menus with data | start_menu, pokedex_list, pokedex_entry, party_screen, summary_stats, summary_moves, bag_items, trainer_card, save_prompt, town_map, fly_map | `@late` (all verified reachable in scout) |
| battle | wild (grass), menu, moves, catch, level up, learn move, evolution, trainer intro, gym leader | play in grass after a warp to a route; set a party member's EXP just below the next level for level-up / learnset / evolution levels |
| field moves | surfing, fishing, bicycle, cut_tree | `@late` + warp next to water/tree; party already has SURF/CUT/FLY/STRENGTH/FLASH, bag has SUPER ROD and BICYCLE |
| minigames | safari_zone, game_corner | warp; Safari needs the gate script (open question), Game Corner needs COIN CASE item + coins |
| bosses/ending | gym_brock, elite_four (Lorelei), champion, hall_of_fame, credits | `@late` walk into Lorelei's room (lobby warp at y0 x8); later rooms by warp. The Hall of Fame/credits need a Champion win (play; LATE party is strong enough for Lorelei-type fights, untested) |
| gameover | blackout | lose a battle (e.g. MID party vs a strong trainer, or poke HP to 1) |
| link | cable_club (done) | Cable Club desk in any Center; a trade screen needs a partner: not reachable alone |

Sequences 2026-11-15 (third run): `seq-fishing` (15 steps: shore -> START -> ITEM -> SUPER ROD -> USE -> cast
clip -> bite -> battle clip -> hooked SHELLDER -> battle menu, + nibble branch) and `seq-fly` (9 steps: Vermilion
-> START -> PIDGEOT -> FLY -> map -> To LAVENDER -> take-off clip -> landing clip -> Lavender), both verified.

Status 2026-11-15, second run (main set, 92 shots, all verified): added the Pewter Gym (walk, Brock talk,
battle, badge), move learning (2), evolution (2), Indigo Plateau outside, Fly map, Surf, fishing (bite +
battle), bicycle, Cut, Viridian Forest, Mt. Moon, Safari (gate, center, battle, rock), Game Corner (hall + 3
slot screens), S.S. Anne, Pokémon Tower + ghost, Silph Co., Champion (room, battle, defeat, Oak), Hall of
Fame (room, entry, record, dex rating), credits (2) + THE END, PC menu + item storage. Open: a trainer
"!" encounter, BILL's PC box with Pokémon, Safari BAIT, stone evolution, Rocket Hideout.

Status 2026-11-15 (first run, main set, 50 shots): done - boot, intro, title, main menu, Oak intro, naming x2, bedroom,
Pallet, Oak stop, lab (preview/choose/received), first rival battle (intro, menu, moves, level-up, defeat),
Route 1 grass, wild battle, ball throw, failed + successful catch, Pokédex entry/list/area, start menu, party +
sub-menu, summary x2, trainer card, bag, town map, Elite Four room/talk/battle/defeat, move animation, super
effective, blackout, Mart, nurse, heal, Cable Club, save, options. Open: learn move, evolution, gym leader in
a gym, cave/forest, Surf, fishing, bicycle, Cut, Fly map, Safari, Game Corner, S.S. Anne, Tower, Silph,
Champion, Hall of Fame, credits, PC.

## Strategy and walkthrough notes
- Verified 2026-11-15 (capture run): early game played from `@start` in ~15 min of commands:
  `TO_DOOR,EXIT` -> Pallet; `down:16,right:16*4,down:16*2` (pallet_town view); north via x10 (`right:16,up:16*8`,
  `right:16,up:16*2`) triggers Oak; `FASTTEXT,mash:a:300`, `mash:a:400,w200` -> lab. In the lab mash only in
  short blocks (dialogue continues after free control seems to return). Squirtle is the middle ball: stand at
  y4 x7, `up,a`. Nickname prompt: `down,a` (NO). **The rival battle triggers only at y6**: the shelves block
  y5->y6 at x7, go `down:16,left:16*2,down:16` (x5). Checkpoints `lab_starter`, `lab_after_rival`.
- First rival battle: Squirtle vs Bulbasaur L5 (TACKLE 3 dmg, crits 4); `poke:CFE6=0003` (enemy HP) shortens it.
  Win: 67 EXP -> L6 level-up box (natural), 175 money, party healed afterwards.
- Catching on Route 1: bag `poke:D31D=010405FF` (5 POKé BALLs), `poke:D887=FF`, hold-walk in grass; Pidgey L3.
  Catch result depends on the press frame: from `route1_pidgey_ball` `w5,a` catches, `a` (w0) fails.
- **Elite Four by warp**: the lobby girl blocks the passage to Lorelei; instead re-point the lobby exit:
  `@late_lobby,poke:D3B1=00F5,poke:D3B5=00F5,down:16*3,EXIT` -> Lorelei's room (the room script walks you in).
  `right:16,up:16*3,up,a` talks to her. Raichu THUNDERBOLT (switch to it first) beats all five with `a,w50,settle`
  loops once `poke:D355=41` (SET style: no "change POKéMON?" prompt that A would answer YES). ~75 loops.
- Blackout: Lorelei's AI stalls (REST, misses) against a 1-HP Blastoise; a field blackout is faster:
  `@late_lobby` + party HP 0 (D198, D1C4, D1F0, D21C, D248 = 0000), D16C=0001, D16F=08 (poison), `left:16*4`.
  Money halves; respawn outside Indigo Plateau (map 9).
- Do not play the story: build states with the RAM recipes (`MID` ~3 badges, `LATE` 8 badges) and warp.
- For early-story shots (Oak, starter, first rival battle) play from `@start`: go downstairs, out, north into
  Route 1 grass; Oak walks you to the lab. Choose Squirtle (the LATE party assumes a Squirtle start). (source)
- Warping into a gym and talking to the leader starts the real battle as long as the EVENT_BEAT_<leader> flag is
  clear (the recipes do not set them) (source: pret event constants; untested in battle).
- Type chart basics for quick wins with the LATE party: Blastoise Surf/Ice Beam, Raichu Thunderbolt, Kadabra
  Psychic (Psychic is dominant in Gen 1). (source, general)
- Battles at MEDIUM text are slow: use `FASTTEXT`; battle animations can be turned off with `poke:D355=81` but keep
  them ON for move-animation shots.

- **Gym battles (verified 2026-11-15)**: `BROCK` macro (mkrecipe.py preset `brock`: Butterfree/Squirtle L15 one
  battle short of L16, Pidgey L12, Pikachu L10, 0 badges, 1386 money, 1:52, Pewter Gym trainer flag set) from
  `@start`, then `TO_DOOR`, door warp `poke:D3B1=0036,poke:D3B5=0036,poke:D365=02,poke:D719=02`, `EXIT` ->
  Pewter Gym entrance (checkpoint `pewter_gym`). `up:16*9` -> y4 (Brock in view), `up:16*2,up,a` talks. One
  Brock battle gives: Butterfree learns STUN SPORE (forget HARDEN: `down*2,a`), switch to Squirtle at the
  SHIFT prompt (`a`, `down,a`), WATER GUN (`down*3`) one-shots Onix, badge text, then Squirtle evolves.
  `poke:CFE6=0005` before an attack shortens the Geodude fight. Same pattern for other leaders: a preset +
  the gym's map id (Cerulean $41, Vermilion $5C, Celadon $86, Fuchsia $9D, Saffron $B2, Cinnabar $A6, Viridian $2D).
- **Field moves (verified)**: from `@indigo_outside` PIDGEOT > FLY (party slot 2) -> town map; `up*5` = VERMILION
  CITY (order Pallet, Viridian, Pewter, Cerulean, ?, Vermilion). In Vermilion (`@vermilion`, x11 y4 by the
  Center): `down:16*2,left:16` faces the water: SURF (Blastoise) or ITEM > SUPER ROD (11th bag item);
  bite or nibble depends on the frame (`a,w30,w1,a` bites, `w2` does not). BICYCLE is the first bag item
  (`right:8` = one tile on the bike). The Cut tree beside the gym: bike `right:8*6,down:8*4`,
  `right:8*2,down:8*6`, `down:8*5`, `left:8*3` -> x15 y17 facing down (checkpoint `vermilion_tree`), Victreebel
  is party slot 5.
- **Warp targets that worked from the lobby exit** (`@late_lobby,poke:D3B1=WWMM,poke:D3B5=WWMM,down:16*3,EXIT`):
  Viridian Forest `0433` (south entrance), Mt. Moon `003B`, Safari gate `009C` (walk `up:16*3`: the fee script
  runs at y2; YES costs 500), Game Corner `0087`, S.S. Anne 1F `005F` (gangway), Pokémon Tower 3F `0090`,
  Silph Co. 1F `00B5` / 3F `00D0`, Champion's room `0078`.
- **Champion/Hall of Fame/credits (verified)**: the warped-in Champion's room has no walk-in script; poke its
  script number `D64C=01` (wChampionsRoomCurScript = wGameProgressFlags D5F0 + 92) and the game walks ryz up
  and starts the speech (checkpoint `champion_talk`). Also poke the starters `D715=99` (rival Bulbasaur),
  `D717=B1` (player Squirtle) so the rival's team matches. Battle: `poke:D355=C1` (SET, no animations),
  `freeze:D015=00AC` (Blastoise HP), then blocks `poke:CFE6=0001,mash:a:300,settle`; SURF runs out of PP
  before Venusaur: pick ICE BEAM (`down,a`). After the win, `mash:a:300` blocks run Oak's speech, the Hall of
  Fame and the credits (`w3000`, `w6000` reach THE END). The game saves itself at the Hall of Fame.
- **Game Corner**: bag `poke:D31D=14,poke:D344=4501FF` (COIN CASE as 20th item), coins `poke:D5A4=1283` (BCD).
  From the entrance `up:16*3,left,a` = a machine; YES -> bet menu; `a` bets 3, `a,w30,a,w30,a` stops the reels.
- **Pokémon Tower ghost**: remove the SILPH SCOPE (13th bag item: `poke:D336=0B03`, ANTIDOTE x3 instead), warp to
  3F, `poke:D887=FF,up:64`.
- **PC**: met-Bill events `poke:D7F1=01,poke:D7F2=30` (else "SOMEONE's PC"), stored items at D53A (count,
  pairs, FF). Indigo lobby PC: stand at x15 y8 facing up (PCs work only facing up).

## Naming
Player **ryz** (lower case: SELECT toggles the keyboard case), rival **RED** (first default offered). Keyboard:
9 columns x 5 rows + "lower case/UPPER CASE" line; letters a-i row 1, j-r row 2, s-z row 3. Route (from the
NEW NAME press, cursor on "a"): `select,down,right*8,a,down,left*2,a,right,a,start` (macro `NAME_RYZ`). Default
player names offered in Blue: BLUE, GARY, JOHN; rival: RED, ASH, JACK. (verified)

## Shortcuts
Cataloguing beats fair play. Values that show on screen stay realistic.
| What | How (tokens / prefix / code) | Source | Status |
|---|---|---|---|
| Fast text | `FASTTEXT` = `poke:D355=01` (bits 0-3 text delay 1/3/5, bit 6 battle style SET, bit 7 animations off) | pret wram + OPTION screen | verified |
| Late-game state | `LATE` macro (from `@start`): party of 6 L42-52 with computed stats, Pokédex 71/104, 19 bag items, 48215 money, 8 badges, all towns visited (Fly), play time 27:47, flags got starter/Pokédex/parcel/town map | generated by `work/scout/pokemon-blue/mkrecipe.py` from pret constants + ROM base stats | verified: party screen, summary p1+p2, Pokédex list, bag, trainer card, save screen, Center heal; battle and Fly not tested |
| EXP fix for LATE | `LATE_EXP` macro (after `LATE`): the scout's mkrecipe.py swapped growth groups 3/5 (medium slow/slow) and let the in-level fraction exceed 100% for slots 5-6, so LATE's EXP showed "741376 to L53" on summary page 2. LATE_EXP rewrites the six EXP values inside each level (Blastoise 134665 -> 7012 to L53, verified). `MID` has the same bug (not fixed: add MID_EXP if used) | computed here | verified (summary_moves) |
| Gym state (Brock) | `BROCK` macro: see Strategy "Gym battles" | `games/gb/pokemon-blue/tools/mkrecipe.py ... brock` | verified (whole Brock battle, badge, evolution, save 04) |
| Mid-game state | `MID` macro: 4 Pokémon L22-27, 3 badges, 3172 money, 19/31 dex, Cut HM + TM28 | same script | generated, not shown on screen yet |
| Warp to any map | stand next to a door/warp, poke its warp entry, step on it: warp *k* of the current map is `wWarpEntries` D3AF+4k = (y, x, dest warp id, dest map); poke D3AF+4k+2 = warp id, +3 = map. Also poke `wLastMap` D365 = the outdoor map you "came from" so exits work, and `wLastBlackoutMap` D719 for whiteouts. From the start room: `TO_DOOR` (walk to the house door on 1F), `poke:D3B1=WWMM,poke:D3B5=WWMM`, `EXIT` | pret wram.asm | verified: house door -> Pewter Gym ($36), exit -> Pewter City (D365=02); -> Indigo lobby ($AE) |
| Battery save load | `sav:NAME` + `TITLE,CONTINUE` | tools | verified with 02_late_game_test |
| GameShark codes | not researched (lists on GameFAQs are 403 here); the RAM map above covers the needs | - | open |
| Debug features | Gen 1 has leftover debug code (TCRF) but no menu reachable without patching | TCRF (403 here) | not tried |

### Saves (games/gb/pokemon-blue/saves/ are ours and committed; rom/saves/pokemon-blue/ = working copies)
| Name | Contents (progress, party, items) | URL | SHA-1 | Status |
|---|---|---|---|---|
| 01_start | ryz in bedroom, new game, rival RED, no Pokémon, 3000 money (exported by play.py, + .state) | made here | see `saves/README.md` | verified saved message |
| 02_late_game_test | LATE recipe at Indigo Plateau lobby: 8 badges, 48215, 27:47, dex 71, party BLASTOISE 52 / PIDGEOT 47 / RAICHU 45 / SNORLAX 46 / VICTREEBEL 44 / KADABRA 42 (+ .state) | made here | see `saves/README.md` | verified: loads, CONTINUE puts you in the lobby |
| 03_starter_lab | Oak's lab after the first rival battle: Squirtle L6, 3175 money, 0:02 | made here | see `saves/README.md` | verified saved message |
| 04_pewter_boulderbadge | Pewter Gym after Brock: BOULDERBADGE, WARTORTLE L16 (just evolved), BUTTERFREE L16, PIDGEY L12, PIKACHU L10, 2772 money, dex 9, 1:55 | made here | see `saves/README.md` | verified saved message |
| 06_hall_of_fame | saved by the game at the Hall of Fame: LATE party, Blastoise L54, 54650 money, dex 105/71, 27:51 | made here | see `saves/README.md` | verified: CONTINUE -> Pallet Town |
| 05_elite_four_lorelei | LATE party after beating Lorelei, in her room: 53759 money, Raichu L47 (SET battle style) | made here | see `saves/README.md` | saved via START > SAVE (message not re-checked) |
| downloads | Project Pokémon hosts Blue/Red saves (e.g. "Pokemon Red completed pokedex with Mew") - not needed, the recipe is better | https://projectpokemon.org/home/files/file/5585-pokemon-red-completed-pokedex-with-mew/ | - | not fetched |

## RAM map (for `game.json` "ram" watches and pokes)
Addresses for the US/EU Red/Blue (pret pokered). Status verified = read/poked here with a visible result.
| Address | Size | Meaning | How found |
|---|---|---|---|
| D057 | 1 | wIsInBattle (0 field, 1 wild, 2 trainer) | verified (1 Route 1, 2 rival/Lorelei) |
| D015 | 2 | player's active battle Pokémon HP (be) | verified (poked to 1) |
| CFE6 | 2 | enemy battle Pokémon HP (be); CFE5 species, CFF3 level | verified (poke shortens battles) |
| D887 | 1 | wGrassRate: wild encounter chance per step /256 (Route 1 = 25); FF = every held step | verified |
| D16B+44k+14 | 3 | party member k EXP (be) | verified (LATE_EXP) |
| D16B+44k+4 | 1 | party member k status (08 = poison) | verified (blackout route) |
| D158 | 11 | player name (charset A=80, a=A0, end 50) | verified ("ryz" = B1 B8 B9 50) |
| D163 | 1+7 | party count, species list (internal ids), FF | verified (poke -> party screen) |
| D16B | 6x44 | party structs (species, HP be, level, status, types, catch, moves x4, OT id, exp 3 be, stat exp x5, DVs, PP x4, level, max HP, atk, def, spd, spc; all words big-endian) | verified (summary screens) |
| D273 / D2B5 | 6x11 | OT names / nicknames | verified |
| D2F7 / D30A | 19 / 19 | Pokédex owned / seen bitfields (bit = dex no - 1) | verified (dex list, 71 / 104) |
| D31D | 1+2n+1 | bag: count, (item, qty) pairs, FF; max 20 | verified |
| D347 | 3 | money, BCD big-endian (048215) | verified (trainer card) |
| D34A | 11 | rival name | verified ("RED") |
| D355 | 1 | options | verified |
| D356 | 1 | badges bitfield (bit0 Boulder ... bit7 Earth) | verified (trainer card) |
| D359 | 2 | player ID (also written as OT id by the recipe: 20017) | verified (summary IDNo) |
| D35E | 1 | current map | verified |
| D361 / D362 | 1 / 1 | Y / X tile | verified |
| D365 | 1 | wLastMap (where "outside" exits lead) | verified (gym exit -> Pewter) |
| D3AE / D3AF | 1 / 4n | number of warps / warp entries of the current map | verified |
| D700 | 1 | walk/bike/surf state (0 foot, 1 bike, 2 surf) | verified (1 on the bike) |
| D53A | 1+2n+1 | PC item storage: count, (item, qty), FF (new game: POTION x1) | verified (pc_items) |
| D5A4 | 2 | Game Corner coins, BCD (1283 -> "CREDIT 1283") | verified |
| D5F0 | ~120 | map script numbers (wGameProgressFlags): Oak's lab D5F0, Pewter Gym D5FC, Hall of Fame D64B, Champion's room D64C | verified (D5F0, D64C) |
| D715 / D717 | 1 / 1 | rival's / player's starter (internal id; Squirtle game: 99 / B1) | verified (lab_after_rival) |
| D70B | 2 | towns visited (Fly list) | verified: LATE's value offers Lavender etc. (seq-fly) |
| D719 | 1 | last blackout map (where you respawn) | source |
| D747 | 320 | event flags (index from pret event_constants; byte D747+n/8, bit n%8) | verified indirectly (EVENT_GOT_POKEDEX -> POKéDEX in start menu) |
| DA41 / DA43 / DA44 | 1 each | play time hours / minutes / seconds | verified (trainer card 27:47) |
Watches in `game.json`: map, y, x, party, badges, battle (money is BCD: read with `peek D347 3`).

## Emulation notes
- Model `dmg` (grey). The game is SGB-enhanced; `--model sgb` **does not work** here now: after the boot the
  screen shows SGB transfer garbage (border tile data) and stays there (route `w2400,settle`, pc=20b4, 160x144
  output, `work/scout/pokemon-blue/sgbtest/`). Probably the game's SGB handshake never completes in gbemu-cli;
  a tools question for the coordinator.
- **Sequences/clips (third run)**: fishing outcome is fixed by the frame of A on USE: from `@seqfish_use`
  (USE/TOSS open) `a` = nibble, `w1,a` = bite (SHELLDER L15; the old `@vermilion_rod,a,w30,w1,a` route gives
  KRABBY), `w2,a`/`w3,a` = nibble. The bite text appears ~4 s after "used SUPER ROD!" (`w1,a,w20` + 240 + `w30`).
  Fly from `@vermilion`: the START cursor is already on POKéMON and the party cursor on PIDGEOT, so
  `start,a,a,a` opens the map; it opens on PALLET TOWN, `up*4` = LAVENDER (checkpoint `seqfly_lavender`).
  After A: field is back after ~34 frames, take-off ~210 frames, white ~50 frames, landing ~190 frames.
  A clip's poster (and its frame in strip.png/steps.gif) is the clip's FIRST frame: start the recording after
  white fades (`do! "a:8,wN"` then `record`), otherwise the strip shows a blank step.
- Settle can stop on all-white fade frames (title -> menu, Oak transitions): add `w60` after such presses.
- Deterministic: same route -> same intro timing; NEWGAME's `mash` block lengths are measured, keep them.
- The play-time counter runs (seconds at DA44); exported saves show whatever was poked plus the real minutes.

## Checkpoints
- Added 2026-11-15 (third run, sequences): `seqfish_use` (Vermilion harbour, SUPER ROD USE/TOSS open),
  `seqfish_bite` ("Oh! It's a bite!"), `seqfly_lavender` (Vermilion, FLY map on To LAVENDER TOWN).
- Added 2026-11-15 (second run): `nurse_yesno`, `pewter_gym`, `brock_*` (battle, learned, onix, proof, evolving,
  saved), `indigo_outside`, `fly_select`, `vermilion*` (surf, rod, tree, cutmenu), `mtmoon`, `safari_gate`,
  `safari_in`, `safari_battle`, `game_corner`, `slots`, `tower3`, `champion_room`, `champion_talk`,
  `champion_battle`, `champion_won`, `oak_lecture`, `hof_pidgeot`, `hof_kadabra`, `credits`, `pc_menu`.
- `title` (title screen), `start` (bedroom, first control after naming), `late` (LATE recipe, Indigo Plateau lobby by
  the entrance, FAST text). Build other states from `@late`/`@start` + warp.
- Added 2026-11-15: `lab_starter` (Squirtle chosen, free control), `lab_after_rival` (rival beaten, Squirtle L6),
  `route1_pidgey_ball` (wild Pidgey, bag open), `late_menu` (LATE, START menu open), `late_lobby` (LATE + LATE_EXP,
  3 steps into the lobby: **use this for late-game work**), `lorelei_room`, `lorelei_battle`, `lorelei_tbolt`,
  `lorelei_won`, `lobby_nurse`.

## Sources
| Source | URL | Used for | Accessed |
|---|---|---|---|
| pret/pokered disassembly | https://github.com/pret/pokered (ram/wram.asm, constants/*, data/moves/moves.asm, macros/ram.asm) | RAM layout, map/item/move/species/event ids, PP; copies in `work/scout/pokemon-blue/pokered/` | 2026-11-15 |
| Data Crystal RAM map | https://datacrystal.tcrf.net/wiki/Pokemon_Red:RAM_map | address cross-check (search snippets only; WebFetch DNS fails here) | 2026-11-15 |
| Glitch City wiki | https://glitchcity.info/wiki/Roaming_items | D35E current map, D347 money (snippet) | 2026-11-15 |
| Project Pokémon | https://projectpokemon.org/home/files/file/5585-pokemon-red-completed-pokedex-with-mew/ | save downloads exist (not used) | 2026-11-15 |
| Wikipedia | https://en.wikipedia.org/wiki/Pok%C3%A9mon_Red_and_Blue | release facts, structure | 2026-11-15 (knowledge, not fetched) |
| TCRF, GameFAQs | tcrf.net, gamefaqs.gamespot.com | unavailable (403 bot protection / WebFetch DNS) | 2026-11-15 |

## Open questions
- ~~Battles with the recipe party not yet run~~ verified: the LATE party beats Lorelei (Raichu alone). ~~Fly with D70B not tested~~ verified: Vermilion -> Lavender (seq-fly).
- ~~Safari Zone by warp~~ answered: warp into the gate ($9C) and walk up; the fee script works (verified).
- ~~Champion/Hall of Fame by warp~~ answered: warp + `D64C=01` (verified, see Strategy).
- SGB model output (see Emulation notes).
- Summary screen: why the first A press was ignored (timing during the cry?).
- Hide/show object flags (wToggleableObjectFlags; address not verified) are untouched by the recipe: story NPCs/items appear as in a new game in
  warped-to areas (e.g. Rockets in Celadon). Check each area shot for consistency.
