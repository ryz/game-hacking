# Deep Dungeon III: Yuushi e no Tabi (Famicom, Japan) - playbook

Everything an agent needs to play this game efficiently: read it before playing, add to it after every run.
Status of each fact: **verified** (seen in the emulator, with the route) or **source** (manual/FAQ/wiki, not yet
checked). Never delete a fact that turned out wrong: strike it and say what is true.

## Identity
| Field | Value |
|---|---|
| Title (EN / original) | Deep Dungeon III: Yuushi e no Tabi ("Journey to Become a Hero"); title screen 勇士への旅 (verified); box title ディープダンジョンIII 勇士への旅. Also spelled "Yuushi he no Tabi" / "Yūshi heno Tabi". Japanese only, no translation patch supplied (two partial fan translations exist: KingMike, MrRichard999, per Data Crystal) |
| Platform / model used | Famicom cartridge, NTSC (`game.json`); NES 2.0 header, mapper 1 (MMC1), 256 KiB PRG (16 x 16 KiB), CHR RAM, 8 KiB battery RAM; CRC32 `3c6f7ff0` ("Deep Dungeon III - Yuushi e no Tabi (Japan)" on Data Crystal) |
| Release (region, year) | Japan, 13 May 1988 (Wikipedia, Data Crystal); the title screen says (c)1987 (verified) |
| Developer / publisher | Developed by HummingBird Soft (title screen, verified), published by Square (Wikipedia, Data Crystal). The first Deep Dungeon on cartridge (I and II were Disk System) |
| Genre | First-person party dungeon RPG: one swordsman hero + up to three companions, towns and four dungeons of square-grid floors (32x32 squares) |
| Players / save system | 1 player; **battery save**: three party slots; save at an inn with "ぼうけんのきろく" (adventure record) (verified: exported `01_start` reloads with `sav:01_start,CONTINUE`) |

## Boot sequence
- Power-on: kana prologue on black (f60-f240: "ゆうけんしを ゆめみて、ひとりのけんしが たびだった。たびの とちゅう
  かれは、ディリージュに たちよった‥‥" - "Dreaming of becoming a hero, a lone swordsman set out. On his way he
  stopped at Dirige"), two triangles join into a star (f300-f480), title from f540 (PUSH START greys in), attract
  text scroll from ~f1020 (verified, `work/intake/deep-dungeon-3/sheet.png`).
- `TITLE` = `w660` -> title screen, static (verified, checkpoint `title`).
- Title Start -> main menu: キャラクターをつくる (create characters) / キャラクターをけす (erase characters) /
  ぼうけんをはじめる (begin adventure) (verified).
- `NEWGAME` = `PARTY,BEGIN` (all macros in `game.json`) -> the inn of Dirige with the new party (verified as one
  `do` from power-on, checkpoint `start`).
  - `PARTY`: create menu -> party slot 1 -> hero name りず -> member 2 hunter こんでい -> member 3 priest えぼ ->
    member 4 magician きゅび -> back at the main menu.
  - `BEGIN`: begin adventure -> slot 1 -> inn.
- `SAVE` (inn menu, cursor on the first line) = record the adventure; `OUT` = go outside (checkpoint `town`).

## Controls
| Context | Button | Action | Status |
|---|---|---|---|
| Title | Start | main menu | verified |
| Title menus (main menu, party slots, class choice) | Up/Down or Select | move cursor | verified (Select moves down) |
| | **Start** | confirm (A does nothing in these menus) | verified |
| Name keyboard | D-pad | move; wraps at the edges, **blank squares and the short bottom row are skipped** | verified |
| | A | type the letter / おわり (end) | verified |
| | B | delete the last letter | verified |
| Inn and in-game menus, prompts | A / B | confirm / cancel | verified |
| Town and dungeon | Up | step forward (into a wall: "いたい! かべに ぶつかってしまった。" "Ouch! Bumped into a wall.") | verified |
| | Left / Right | turn 90 degrees | verified |
| | Down | turn around (source: usual for the series) | unverified |
| | A | open the door ahead / enter the building | verified (inn door) |
| | B | field menu: どうぐ (items), じゅもん (spells), しらべる (search), つよさ (status), はなす (talk) | verified |
| | Start, Select | nothing seen in town | verified (no reaction) |
| Battle | Up/Down, A | first menu たたかう (fight) / にげる (run); per member たたかう / じゅもん (spell) / みをまもる (defend) / どうぐ (item) / にげる; then a target among the enemy sprites | verified (fight -> target) |

Input timing: the default press (hold 8, wait 40) works everywhere tried; keyboard and menus took one press per
token. Presses while a page is drawing were not a problem in the macros (each tested as one `do`).

## Game structure
- **Party:** the hero is always a swordsman (けんし) and cannot be changed; up to three companions, each a hunter
  (かりゅうど, "ranger" in English sources), priest (そうりょ) or magician (まほうつかい), or "つくらない" (create
  none) (verified). Companions can be dismissed at the inn (パーティーからはずす) and only replaced by pre-made
  characters met in the dungeons (Wikipedia). **Game over when the swordsman dies** (Wikipedia).
- **Level-ups:** stat points are allocated by the player; random encounters stop when the party is far above the
  local monsters' level; weapons can be fumbled in battle; monsters drop gold (only series entry with gold drops)
  (Wikipedia, unverified).
- **World (ROM, verified by warping):** one town grid (several towns packed into a 32x48 grid) and four dungeon
  "areas" of 32x32 floors, area number in RAM `7003`, floor in `7004`:
  | Area (`7003`) | Floors | Walls | Name (ROM text, inferred mapping) |
  |---|---|---|---|
  | 1 | 2 | green | ちか, the underground below Dirige ("このちかは ひがしのまちアイルに つづいている" - leads to the eastern town Ail) |
  | 2 | 4 | orange brick | どうくつ, the cave ("どうくつのなかは ふくざつだ。まよったら『サークレット』をつかえ" - use the Circlet if lost) |
  | 3 | 6 | purple | とう, the tower ("とうのいりぐち まちにでますか?" - tower entrance) |
  | 4 | 4 | green/rooms | しろ, the castle (regular rooms of statues; "しろにいるまものが このせかいをつくったらしい") |
  | 5 | - | blue | towns: Dirige ディリージュ (south-west), Ail アイル (east), an unnamed north town (verified, `design/maps.md` section 5) |
  | 6 | - | - | **the ending** (princess, staff roll, "the End"; verified by warping, shots `ending_*`) |
  Area names verified 2026-11-18: the tower and castle entrances name themselves (Ail building 7, north town building 8).
  An NPC line (ROM text) says "とう、どうくつ、しろ‥‥それぞれ ぬしがいる" (tower, cave, castle each have a master).
- Town stairs (8, table in bank 9 $8C32): town squares with "くだるかいだんが ある" lead to area 1 or 2 floor 1
  (ROM: town (1,25) -> area 1 (1,1); (30,1) -> area 2 (1,1); full list in `design/maps.md`).
- Inn (やどにとまる "stay", 4 gold at level 1; ぼうけんのきろく save; パーティーのくみかえ reorder;
  パーティーからはずす remove; そとにでる go out) (verified).

## Shot plan
`shots.txt` holds the full main set in game order (74 shots, capture run 2026-11-18, all verified). Done in that run:
town life (shops of three towns, temple, magic hall, information seller, inn stay), field items/spells, battle flow
(target, spell, round, victory, level-up and bonus points, game over by the swordsman's death), one view per dungeon,
22 event squares (prison, monument, pit trap, sword in the rock, companion joining), masters Zosem and Barzas, the
ending and staff roll. Still open: the castle master (not found by the event scan), a mid-game battle with
equipment, more of Ail/north town (temple, item shop), the triangle tablets and orbs as items.
The scout's original plan, for reference:
- [x] `prologue_text` cutscene, `title_screen`, `menu_main`, `party_slots`, `name_entry`, `class_select`
- [x] `inn_menu` shop, `inn_save` save, `town_inn_door`, `field_menu`, `status_ryz`, `stairs_down_cave`,
  `battle_skeletons`, `battle_commands`
- [ ] `hud_dungeon` - a long dungeon corridor with the party panel (area 1, `@area1` then turn/walk)
- [ ] one gameplay view per area: `area1_underground` (green), `area2_cave` (orange), `area3_tower` (purple),
  `area4_castle` (statue rooms) - warp (Shortcuts), pick a square with a deep view from `design/maps/`
- [ ] towns: a second town (Ail), shops (numbered buildings 1-8 in the town grid: enter with A at a door), temple
  or healer, `npc_talk` (はなす) dialogue
- [ ] `spell_menu` (じゅもん: the priest or magician), `item_menu` (どうぐ), `battle_spell`, `battle_victory`
  (gold + EX), `level_up` (stat allocation, a series feature: poke EX next to a level)
- [ ] events: a chest / item square (`0x01`-`0x1B` squares in `design/maps/`), a pre-made companion met in a dungeon,
  a message square
- [ ] bosses: the masters (ぬし) of underground/cave/tower/castle - find their event squares (likely the high event
  numbers on the last floor of each area) and warp next to them
- [ ] `gameover` (let the swordsman die: poke his HP to 1 in a battle)
- [ ] `map` category: none in-game seen yet (an item may show "ちか 2かい きた" - area/floor/facing text exists in the
  ROM: ちか ちじょう まち ほうこう かい きた ひがし みなみ にし); the drawn floor maps live in `design/maps/`

## Strategy and walkthrough notes
- Level 1 party: HP 15 / 12 / 9 / 6; skeletons (がいこつ) come in threes on area 1 floor 1. For screenshots of
  battles, use the `battle` checkpoint; for winning, freeze HP (`freeze:` on the HP bytes, RAM map) rather than
  grinding.
- Encounters depend on frame timing: the `battle` checkpoint is reproducible through `play.py` routes; the same
  keys typed into `emu.py` without the `settle` steps meet nothing (seen).
- Warps (below) skip all travel. After a warp the view is drawn correctly (full reload).

## Naming
Hiragana-only keyboard (no katakana, no Latin), names up to 5 squares; a voiced sound mark takes its own square
(り す ゛ = りず). Owner's names as typed:
| Member | Class | Name | Macro |
|---|---|---|---|
| hero (RYZ) | swordsman けんし (fixed) | りず | `RYZ` |
| CONDI | hunter かりゅうど | こんでい (no small ぃ on the keyboard) | `CONDI` |
| EBO | priest そうりょ | えぼ | `EBO` |
| CUBI | magician まほうつかい | きゅび | `CUBI` |
Only four members exist (hero + three), so DEDDO and MNZ are not used. Keyboard layout (row, column), 10 per row:
あいうえおかきくけこ / さしすせそたちつてと / なにぬねのはひふへほ / まみむめもや_ゆ_よ / らりるれろわをん゛゜ /
ゃゅょっー おわり (おわり = end, column 5). Each name macro starts on あ (cursor resets per name); `KBD` / `b,w20`
before each name is a harmless pad (delete on an empty name).

## Shortcuts
| What | How (tokens / prefix / code) | Source | Status |
|---|---|---|---|
| Warp helper (scratch, rebuild from here) | `sh work/capture/dd3/w.sh AREA FLOOR X Y FACING "extra tokens" [ID CAT "caption"]` = `@warp` + the warp tokens below + `poke:006F=FACING,left,right,w30` (+ `up,w150` to step into the square ahead) | capture run | verified (all event shots) |
| Veteran party | macro `VET` (level 5, 643 gold); checkpoint `vets` = save `02_veterans` at the inn | RAM | verified (status, battle, reload) |
| Ending | `@warp,poke:7003=06,poke:7004=00,poke:00EE=01,poke:00EF=01,a,w150,...` then `w3100` princess, `w5880` credits, `w9100` the End (use `do!`) | warp | verified |
| Warp to any area/floor/square | `@warp` (or from `@town`: `WARP_A2`), then `poke:7003=AREA,poke:7004=FLOOR-1,poke:00EE=X,poke:00EF=Y,a,w120` - the area-2 down stairs do `7004+1` and a full reload by `7003` | ROM code (bank 2 $8E4A) | verified (area 4 floor 4 (5,5), area 3 floor 6 (14,14)) |
| Move on the current floor | `poke:00EE=X,poke:00EF=Y,poke:006F=F0` then `left,right` (forces a redraw) | RAM | verified (town) |
| Enter a dungeon | from `@town`: `poke:00EE=01,poke:00EF=1A,poke:006F=00,left,right,w30,up,w60,a,w120` -> area 1 floor 1 | ROM stairs table | verified (checkpoint `area1`) |
| Game Genie / Pro Action Replay codes | none found (almarsguides lists "cheat codes", outside the network) | - | - |
Within area 1 (and other areas' own stairs) the stairs do `7004+-1` and reload only the current bank's map:
poking `7003` there does **not** switch the area (seen: map RAM stayed area 1). Use the area-2 stairs.

### Saves (rom/saves/deep-dungeon-3/, never committed)
| Name | Contents (progress, party, items) | URL | SHA-1 | Status |
|---|---|---|---|---|
| none | GameFAQs (403 from here) has no save section known | - | - | - |
Own exported save: `games/nes/deep-dungeon-3/saves/01_start.sav` (new party at the first inn, see `saves/README.md`).

## RAM map (for `game.json` "ram" watches and pokes)
| Address | Size | Meaning | How found |
|---|---|---|---|
| `00EE` | 1 | x (0-31, east +) | RAM diff over steps, map code $FD73 (verified) |
| `00EF` | 1 | y (0-31; 0-47 in towns; north -) | map code $FD73 (verified) |
| `006F` | 1 | facing x 16: `00` north, `10` east, `20` south, `30` west | RAM diff over turns (verified) |
| `7000` | 1 | party size (4) | battery RAM (RAM) |
| `7001` | 2 | gold, little-endian (100 = `64 00`) | battery RAM (RAM, on screen 100) |
| `7003` | 1 | area: 1 underground, 2 cave, 3 tower, 4 castle, 5 town (6 = bank 11, unknown) | bank-select code $F530 (verified by warps) |
| `7004` | 1 | floor in the area (town: 1) | code $F549 (verified) |
| `7005` / `7006` | 1 / 1 | saved x / y (inn position at start: 13,39) | battery RAM (RAM) |
| `7010` + 0x40*n | 0x40 | character n (0-3): **+0 level** (0 = empty slot), +1..+5 name (game encoding, `C9` = ゛), **+6/+7 EX** (LE), +8/+9 HP, +A/+B max HP, +C MP, +D max MP, +E ST, +10 AC, +12 AG, +13 LK, **+14.. items** (one id per slot; lamp = `2D`), +29 class (1 swordsman; 7 shows "たたかう"), +28 status (`20` after death) | status-page probes (verified 2026-11-18) |
| `7000` | 1 | party size: poke `7000=03,70D0=00` to free the fourth slot (companions can then join) | verified (shot `companion_joins`) |
| `7110`.. | | party slot 1 save copy (same layout as `7000`) | battery RAM (RAM) |
| `6100-66FF` | 0x600 | current map grid: square (x,y) at `$6100 + y*32 + x` | code $FD73, matched against ROM (verified) |
| `6C00`.. | | another copy of the party block | battery RAM (RAM) |
Text encoding (Data Crystal TBL, confirmed on names): `D0`-`FE` hiragana あ..っ, `A7`-`C3` katakana, `C9` ゛,
`CA` ゜, `90`-`99` digits, `8F` space; helper `work/scout/deep-dungeon-3/tbl.py` (scratch).

## Maps
Floor data are raw grids in ROM (no compression), drawn by `tools/maps.py` into `design/maps/` (16 floors + the town
grid, PNG + `grids.md`); format and square codes in `design/maps.md`. Dungeon floor F of area A: bank per the table
in `design/maps.md`, `$9800` (odd F) / `$9C00` (even F), 32x32 bytes; towns bank 9 `$9700`, 32x48.

## Emulation notes
- NTSC, no issues seen. `status` PC is always `ffb3` (frame-wait loop).
- PRG ROM cannot be poked (`poke 8C52` had no effect): warps go through RAM only.
- The `area1` checkpoint keeps the up-stairs message text in the message window after the prompt is dismissed.

## Checkpoints
| Name | What |
|---|---|
| `title` | title screen, static |
| `start` | inn of Dirige, new party, before saving |
| `town` | outside the inn after saving (the save is in the state's battery RAM) |
| `area1` | area 1 floor 1 (1,1) after the town stairs |
| `warp` | area 2 floor 1 (30,1) on the down-stairs prompt: the warp base |
| `battle` | three skeletons on area 1 floor 1 (2,2) |
All six rebuilt from an empty cache and compared with a cache hit: identical frames (2026-11-18).

## Sources
| Source | URL | Used for | Accessed |
|---|---|---|---|
| Wikipedia "Deep Dungeon" | https://en.wikipedia.org/wiki/Deep_Dungeon | release date, developer/publisher, party/classes, game-over rule, level-up, gold | 2026-11-18 |
| Data Crystal | https://datacrystal.tcrf.net/wiki/Deep_Dungeon_III:_Yuushi_e_no_Tabi | cartridge data, dump name, translations; `/TBL` text table | 2026-11-18 |
| StrategyWiki ToC | https://strategywiki.org/wiki/Deep_Dungeon_III:_Yuushi_heno_Tabi/Table_of_Contents | 403 (unavailable); search summary: map pages for underground, tower, cave, castle | 2026-11-18 |
| GameFAQs | https://gamefaqs.gamespot.com/nes/578444-deep-dungeon-iii-yuushi-e-no-tabi/faqs | 403 (unavailable); an ASchultz FAQ exists (search summary) | 2026-11-18 |
| MobyGames | mobygames.com | outside the network (search summary only: opening inn in a town) | 2026-11-18 |
| ROM text and code | `rom/deep-dungeon-3.nes` | place names, area/floor layout, stairs tables, map format | 2026-11-18 |

## Capture notes (2026-11-18)
- Leaving a shop takes longer than `w120`: pokes in the same `do` are overwritten (the party lands elsewhere). Make
  each building shot from `@town` instead of chaining shops.
- After arriving in town by the underground stairs the stairs prompt stays and blocks input (seen once): avoid.
- Freezing HP does not save the swordsman (the hit and the death check fall inside one wait); use stronger records.
- Skeletons hit the level-5 swordsman for 28: give him "defend" (みをまもる) and let the magician's Spear kill them.
- The battle/round text and ending text scroll by themselves: shots use `do!` + fixed waits.
- Event scanner (scratch): `work/capture/dd3/scan.py AREA FLOORS [PER]` warps next to each event square, steps in and
  tiles the screens (one square per number per floor; `ALL=1` all four sides; `ONLY="x,y;x,y"`).

## Open questions
- ~~Which building is which~~: answered (`design/maps.md` section 5). ~~Event squares~~: per floor in section 7
  (one side tried each). ~~Level/EX~~: record +0 / +6. ~~Area 6~~: the ending.
- Monster HP in battle (not found: `0720`-`0746` hold round data); the castle master's square.
- Does Down turn around in the field? Map/compass item ("ちか 2かい きた" text)?
- ~~Area names are inferred~~: confirmed by the tower and castle entrance prompts and the wall texts (2026-11-18).
