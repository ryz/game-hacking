# Sword of Vermilion - playbook

Everything an agent needs to play this game efficiently: read it before playing, add to it after every run.
Status of each fact: **verified** (seen in the emulator, with the route) or **source** (manual/FAQ/wiki, not yet
checked). Never delete a fact that turned out wrong: strike it and say what is true.

## Read first
- **Start:** `rom/sword-of-vermilion.md` (SHA-1 c18fc75e...), model `ntsc`. `play.py start sword-of-vermilion --route @field`
  (overworld outside Wyclif, Bronze Sword readied), `@battle` (first battle), `@saved` (Wyclif church, game
  saved) or `@wyclif` (outside Blade's house). `@continue` = the same state via the
  exported save `saves/01_start.sav` and the title's Continue.
- **Macros:** `TITLE` = `w800` (title with cursor; inputs work from ~f300, Start then lands on the title);
  `NAME` types ryz on a fresh keyboard; `NEWGAME` = keyboard, name, Start, the auto-running prologue (no skip)
  to first control (~4500 frames); `PAGE` = `c,w90` (one dialogue page at Normal speed); `CONTINUE` = title ->
  Continue -> Saved Game 1 -> "Your game is ready" -> in front of the priest.
- **Overworld macros:** `FWD` = `up:8,w40` (one step forward), `TL` / `TR` = `left:8,w60` / `right:8,w60` (turn 90 degrees).
- **Checkpoint chain:** title -> name -> start -> t_door -> t_church -> t_blade_in -> t_blade_room -> blade ->
  wyclif -> tavern -> church -> church_menu -> saved; continue (from the .sav); wyclif -> t_north_road;
  tavern -> t_south_west -> overworld (no weapon); t_south_west -> weapon_shop -> shop_list -> sword -> field
  -> battle -> escaped. All 23 reproduce
  (`tools/cachecheck.py`). The routes before `wyclif` are exploratory (they wander); they are correct, not short.
- **Controls:** C = confirm / field command window / **sword swing in battle** (one swing per press: holding
  C does nothing); B = back/close and delete on the keyboard; Start = title choice and ends naming. A and B do
  nothing in battle. Overworld: up = step forward, left/right = turn. Battle: D-pad moves freely; **walking off
  the left (or right) edge escapes** (verified left).
- **Leaving Wyclif:** the south gate (tile 0D,2B) after Blade has spoken: stand on it, then a fresh `down`
  (`w20,down:32,w300`). Before Blade it does nothing. A man by the well (west of the inn) says "Be sure to buy
  armor, a weapon, and a shield before you leave the village."
- **First battle:** `@field,FWD*8,TR,FWD*7,w100`: a green slime appears on the road at step 3 after the turn and
  meets the prince at step 7; side-view battle with about eight slimes. Without a weapon (or pressing only
  A/B) the prince dies in ~600 frames and is revived at the Wyclif church with half his money ("Arise, brave
  warrior! Our world needs you! But half your money ...").
- **Traps that cost calls:**
  - **Doors and stairs fire only on a fresh press** made while standing on the door/stair tile: walk onto it,
    then `w20,up:16` (or the direction of the exit) again. Holding the direction into the door does nothing.
  - **Every door in Wyclif is locked** ("Sorry, you can't open that!") until Blade has spoken; Blade's house
    is the only open doorway at first (top-left of the village, tile 09,0B; Blade is upstairs: ladder at the
    top-left of the ground floor, out again: upstairs top tile + `left`, then the front door at the bottom).
  - Town movement: 16 frames per tile; `play.py` settles between calls change routes: a route typed into
    `preview.py` can stop elsewhere than the same keys in `play.py` (seen leaving the tavern). Copy routes
    from `play.py route` / checkpoints.txt.
  - Text types slowly at Normal speed and C does not complete a page; `mash` lost pages. Use `PAGE*N`.
  - Position pokes (FFC606/FFC608) are overwritten at once: the real position lives elsewhere (open).
  - **Shop dialogs:** after a purchase "Anything else for you today?" Yes returns to Buy / Sell / Stop with the
    cursor where it was: a blind `down,c` sold the sword offer ("Is 30 kims all right?"). Look before each step.
  - A state loaded mid-battle (`@battle`) and played on to a lost battle differed in memory from the same route
    replayed from power-on (same picture): the death/revival is a shot route (`gameover_revived`), not a
    checkpoint. Re-verify such shots with `shoot.py --verify`.
  - The title and most field screens never settle (blinking cursor, animated water/NPCs): "NOT settled" is normal.
- **State:** captured 2026-11-20: sets `start` (35, honest, to the first save), `main` (96) and `seq-aries` (7: Aries
  cast -> fade -> Wyclif gate, with a clip) published and verified. Reached: Parma, the Ring of Wisdom (old man,
  cave south of Wyclif), the Cave of Troy entrance map. Not reached: a boss, Watling, the ending, message speed.
- **Maps (round 3):** one flag byte per map, FFC820 + y*16 + x (map x/y = FFC666/FFC668; Wyclif's south map is
  (0,7), Parma (1,4)). Poke the byte *before* entering the map (inside a town, or before crossing an edge): the
  panel is drawn on map entry, not on a step. Mirror of Atlas (item 0x23) = all 256 flags; Titania's Mirror
  (0x1E) = current outdoor map; Griffin Wing (0x1D) = fade to Wyclif's gate. Item Use recipe:
  `poke:FFC443=01,poke:FFC444=00XX,c,w30,down,w20,c,w40,c,w60,settle,c,w120` (one more `c,w120` for the result).
- **Story flags:** FFC720 = Blade has spoken, FFC818 = Ring of Wisdom received; a town picks its people's line
  table on entry from these (ROM 0x1EB0C for Wyclif), so poke them before entering. `m_ring` gets the ring
  honestly (old man at window (18,20) of the cave, via `m_cave_inner`); `m_map_gift` (ring flag poked, from
  `@overworld`) has the man by the well give the Parma route map (5 maps).
- **Any enemy group:** `poke:FFC68B=NN` (0-0x55) right before the step that starts the encounter, e.g.
  `@field,FWD*8,TR,FWD*6,poke:FFC68B=24,freeze:FFC62C=0021,FWD,w10*16,!`. 0x56 and above crash. At `m_strong`
  the group is fixed earlier (the poke before the last step did nothing). FFC0A4 looks like a mode byte
  (0 title, 1 name, 9 interior, 10 overworld, 11 battle, 12 cave) but poking it changes nothing.
- **Main-set chain (capture 2026-11-20):** `m_strong` (from `@battle`: EXP poked to 2417, battle won with HP frozen
  -> level 5, 162 HP, 3424 kims) -> `m_cave1` (cave south of Wyclif, dark) -> `m_cave_lit` (2 Herbs, Candle, Lantern
  poked, Lantern used) -> `m_cave_door`/`m_cave_inner`/`m_cave_chest`/`m_cave_west`; `m_strong` -> `m_north1` ->
  `m_north2` -> `m_parma` -> `m_parma_inn`, `m_inn_offer`; `m_magic_shop` -> `m_magic_list` -> `m_spells_bought` ->
  `m_ferros_ready` -> `m_parma_out` -> `m_battle_parma` (Ferros readied), `m_east1` -> `m_cave2_gate` -> `m_cave2_lit`.
  Start set: `s_saved` (first battle lost honestly, revived, saved in Saved Game 1).
- **Walking the overworld and caves without looking:** the current 16x16 map sits in a 48x32 window of bytes at
  FF9000 (row-major, 48 wide; 0 = open road/floor, 1 trees, 2 hills/water, 5 cave wall, 0F town, other values =
  special squares: town/cave entrances, barred doors 6). `tools/go.py @CP 16 16 TX TY` (game folder) does a BFS
  and prints a route, fighting battles on the way (SW macro, HP frozen). The window offset of the current map is
  usually (16,16) but the window re-centres when a map edge is crossed: re-dump and re-plan at each new map.
- **Battle:** `SW` = `up:10,c,w2,down:10,c,w2` (swing while dodging). A = cast the readied spell (Ferros 1 MP).
  Battle flag: FFC550 = FF during a battle. Level-ups happen when the battle ends; the status window opens itself.
- **Traps (capture):** menu cursor moves right after `c,w60` are dropped: put `settle` before `down*N` (Aries, Lantern).
  The walker's battles sometimes end by the prince being pushed off the edge (an escape, no EXP).

## Identity
| Field | Value |
|---|---|
| Title (EN / original) | Sword of Vermilion / Vermilion (ヴァーミリオン) (verified: title screen; header domestic title "VERMILION") |
| Platform / model used | Sega Genesis, model `ntsc` (header region North America) |
| Dump | 640 KiB, SHA-1 `c18fc75e0c5fa0e98c8664903e978ec4f73ef5d2`, CRC32 `ea1bc9ab`, product GM 00005502-00, header copyright "(C)SEGA 1990.SEP", checksum ok. Not matched against No-Intro (no reachable list); the 1990 US cartridge (USA, Europe in No-Intro naming, per code lists "USA/Europe") |
| Release (region, year) | Japan 1989-12-16, North America 1990-11-10, Europe 1990 (source: Wikipedia) |
| Developer / publisher | Sega AM2 / Sega; director Hiroshi Hamagaki, producer Yu Suzuki, music Hiroshi Kawaguchi, Yasuhiro Takagi (source: Wikipedia) |
| Genre | Action RPG: top-down towns, first-person overworld and caves, side-view real-time battles and boss fights (source: Wikipedia) |
| Players / save system | 1 player; battery RAM 200001-203FFF (odd bytes), three slots "Saved Game 1-3", saved at churches (verified) |

## Boot sequence
- Intake probe: `work/intake/md/sword-of-vermilion/sheet.png`: SEGA logo (~f60-180), black, tree on the cliff
  scrolls in, sword in the stone, lightning (~f660), title letters fly in, title with Start/Continue from ~f780
  (cursor blinks). No attract mode within 30 s.
- `TITLE` = `w800` (verified). Start at ~f300 jumps to the title animation (not to the menu).
- On the title: `start` chooses (C and A do nothing there, verified). Start -> name keyboard at once (no
  confirm). Continue: `down,start` -> slot list "Select a number and press Button C." (empty slots show
  level 4096) -> `c` -> "Your game is ready! Please press button C." -> `c` -> in the church where you saved.
- Name keyboard (verified): 10 columns, rows `A-J`, `K-T`, `U-Z`, `a-j`, `k-t`, `u-z`, `0-9`, `- _ , . ' / .`,
  `END`; cursor starts on A; C enters a letter, B deletes, Start ends the name. **Moving skips blank squares**:
  `down` from `r` (column 7) jumps over the short `u-z` row to `7`. `NAME` = `down*4,right*7,c,left*3,down,c,right,c` (r, y, z).
- `NEWGAME` = `start,w120,NAME,start,w60,w4400` (verified as one `do` from power-on): the prologue (Tsarkon
  invades Excalabria, Erik's castle falls, Blade flees with the baby and the Ring of Wisdom, "Eighteen years
  have passed") runs by itself, ~4000 frames; Start and C do not skip it. First control at the south gate
  of Wyclif, tile (0D,2B).

## Controls
| Context | Button | Action | Status |
|---|---|---|---|
| Title | `start` | choose Start / Continue | verified |
| Title | `up`/`down` | cursor | verified (`down` -> Continue) |
| Keyboard | D-pad / `c` / `b` / `start` | move / enter letter / delete / finish | verified |
| Town | D-pad | walk, 16 frames per tile, hold to keep walking | verified |
| Town | walk onto a door, then press the direction again | enter a house; same for stairs and ladders | verified |
| Town | `c` | field command window: Talk Magic / Item Equip / Str Seek / Open Take (cursor 2 columns) | verified |
| Field window | `c` / `b` | choose / close (B closes the window after a message) | verified |
| Talk | stand next to a person, facing them | dialogue box; `c` per page | verified |
| Str | | status: Name, Condition, Level, EXP, Next level EXP, HP MHP, MP MMP, STR AC, INT DEX, LUK KIM | verified |
| Equip | | Put on / Remove / Stop -> Weapon / Shield / Armor ("You don't have the proper equipment!" with none) | verified |
| Open | | doors/chests: "There's nothing to open here!", "Sorry, you can't open that!" | verified |
| Seek | | "You searched carefully, but you didn't notice anything unusual." | verified |
| Church (Talk to the priest across the altar) | | Remove a curse / Apply poison balm / Save your game / Stop -> slot 1-3 | verified |
| Overworld | `up` / `down` | step forward / back (`FWD` = `up:8,w40`; ~40 frames per step) | verified (`up`); `down` source (GameFAQs via search snippet) |
| Overworld | `left` / `right` | turn 90 degrees (`left:8,w60`) | verified |
| Overworld | `c` | field command window (same as in town) | source; not tried here |
| Overworld | walk onto the town square | enter the town (two right turns + steps back from `@overworld` re-entered Wyclif) | verified |
| Battle | D-pad | move the prince anywhere on the field (real time) | verified |
| Battle | `c` | sword swing, one per press (mashing C killed a slime: EXP +1, KIM +2) | verified |
| Battle | `a` / `b` | nothing seen (the prince died while mashing them) | verified |
| Battle | walk off the left/right edge | escape to the overworld | verified (left) |
| Battle | magic | button unknown (no spell owned yet) | open |
| Shop | Talk to the keeper across the counter | Buy / Sell / Stop -> list with prices -> "Is X OK?" Yes/No -> "Anything else for you today?" | verified |
| `a` | | no effect found on the title or in town | verified (title) |
| Second pad A+B+C+Start | | hidden menu (source: Sega Retro via search snippet); not testable: the md backend has no second pad | unverified |

Input timing: the default press (hold 8, wait 40) works in menus, the keyboard and the church. Doors/stairs
need a separate press after arriving (see Read first). Dialogue: `PAGE` = `c,w90` per page at Normal speed.

## Game structure
(source: Wikipedia unless tagged; ROM text = strings in this dump)
- Story: Tsarkon of Cartahena destroyed Erik V's Excalabria; Blade saved the infant prince and the Ring of
  Wisdom and raised him in Wyclif (verified: prologue). On his deathbed Blade tells the prince his origin, that
  he hid the Ring of Wisdom in a cave near the village, gives 200 kims (verified: `blade`).
- Towns (ROM text, table at 0x1FC0B): Wyclif, Parma, Watling, Deepdale, Stow, Keltwick, Malaga, Barrow,
  Tadcaster, Helwig, Swaffham, Excalabria, Hastings, Cartahena. Early places (ROM text): Peak Cave? (source:
  walkthrough snippet "path to Peak Cave"), Cave of Troy east of Parma, Watling east of the cave.
- Rings (ROM text): Wisdom, Sky, Wind, Fire, Water, Earth, Sun, Power; "Sixteen Rings" item.
- Weapons (ROM text): Bronze, Iron, Sharp, Long, Silver, Prime, Golden, Mirage, Platinum, Diamond, Graphite,
  Royal, Ultimate Sword, Sword of Vermilion; cursed: Dark, Death, Barbarian, Critical Sword. Shields and armour
  tables follow (Leather Shield ... Knight Shield, Leather Armor ... Old Nick Armor).
- Magic (ROM text): Aero, Aerios, Volti, Voltio, Voltios, Ferros, Copperos, Mercurios, Argentos, Hydro, Hydrios,
  Chrono, Chronios, Terrafissi, Aries (town warp: "All towns available with Aries" code name), Extrios,
  Inaudios, Luminos, Sangua, Sanguia, Sanguio, Sanguios, Toxios.
- Items (ROM text): Area Map, Herbs, Candle, Lantern, Poison Balm, Alarm Clock, ... keys, crystals, Griffin Wing,
  Titania's Mirror, Mirror of Atlas, Mega Blast. Caves are dark: Candle/Lantern light them (ROM text).
- Gear menus (ROM text): Gear (Combat), Gear (Magic), Gear (Item), Rings.
- Overworld maps are 16x16 each; Wyclif: inn, a man outside the inn gives the map to Parma, save at the
  church, carry two Herbs (source: TheStarbird walkthrough, seen only as a search snippet).
- Wyclif layout (verified, tile x,y): Blade's house door (09,0B); tavern door (0C,13) south-east of it
  (the house with the sign that looks like "DY"; inside the sign reads TAVERN-like); fortune teller
  (crystal-ball sign) south of the tavern; inn further south (INN sign); church door (20,13) on the north-east (enter from (20,14)); weapon shop (crossed swords)
  door (09,28) by the south gate; graveyard with crosses east of the stream (~(23,25)).

## Shot plan
Routes in `shots.txt` (22 lines verified by `preview.py`, the rest planned as comments).
- [x] `boot_sega`, `cutscene_intro_tree`, `title_screen`, `menu_name`, `cutscene_prologue_tsarkon` - boot to naming
- [x] `start_wyclif_gate` (gameplay), `dialogue_blade_house`, `env_wyclif_blade_house`, `gameplay_tavern`
- [x] `save_church_menu`, `save_slots`, `menu_continue_slots`
- [x] `hud_field_menu`, `inventory_status`, `shop_weapon`, `inventory_equip` (round 2)
- [x] `env_overworld_road`, `env_overworld_trees`, `gameplay_encounter_slime`, `battle_first`, `battle_attack`,
  `gameover_revived` (round 2)
- [x] `cutscene_blade_deathbed` (2026-11-20) - Blade's deathbed pages (from `t_blade_room`, route in `blade`; pick a page with `PAGE`)
- [ ] `env_wyclif_*` (2-3 plain street views), `env_graveyard`, Blade's grave
- [x] more `env_overworld_*` (other maps), `gameplay_cave_dark` / `gameplay_cave_lit` - first-person views
- [x] `battle_magic`, `battle_levelup` (won), blue slimes, goblins (2026-11-20); `battle_escape` not shot (same frame as a road) - more battles (several enemy types)
- [x] `system_aries_towns`, `system_lantern`; area maps (2026-11-20 round 3: `map_*`, mirrors, map gift); travel (`system_aries_arrival`, `system_griffin_wing`, set `seq-aries`)
- [x] presentations: intro (`cutscene_intro_rise`, `cutscene_title_letters`), all four prologue pages, battle start fade, Ring of Wisdom scene
- [ ] Sangua cast; town entry/exit and cave entry are plain fades (`seq-aries` 06 shows one), not shot separately
- [ ] `boss_first` - the first boss (Cave of Troy guardians? trigger unknown); ending (text at ROM 0x17722, staff 0x179CA; trigger unknown); `options_message_speed`; Watling ...
Fastest ways: the `saved` checkpoint for town shots; stats by poke (RAM map) before fights; town warps with
the Aries spell once the spell slot RAM is known (Action Replay lists name "All Towns Available With Aries").

## Strategy and walkthrough notes
- Round 2 (verified): Wyclif weapon shop prices: Bronze Sword 100, Leather Shield 50, Small Shield 80, Leather
  Armor 200, Bronze Armor 400 kims; selling the Bronze Sword gives 30. With Blade's 200 kims buy the sword and
  the Leather Shield (`@sword` bought only the sword). Readying the sword: STR 4 -> 0x20 in RAM (STR word
  FFC634 = 0020 after readying; status screen value not read).
- First enemies: green slimes in packs of 6-8 on the road south of Wyclif (verified); they hit for about 3 HP.
  For battle shots freeze HP (`freeze:FFC62C=0021`, re-applied per token: use `w10*N`, not one long wait).
- Source (search snippets): the Ring of Wisdom cave is south of the village; "follow the path north from Wyclif
  to reach Parma"; the man behind the weapon shop gives the map to Parma; fight near the village until a level-up.
- Opening (verified): from `start` go to Blade's house (top-left, the only open doorway), up the ladder, talk to
  Blade (stand below-left of the bed: `@t_blade_room` route), `PAGE*16`; 200 kims. Then every door opens.
- Buy a weapon first: Equip shows no gear at the start. Bronze Sword price unknown (open).
- Source tips (snippet): get the map to Parma from the man outside the inn, carry two Herbs, save at the church;
  "go west to gain experience" (ROM text, Parma); lanterns last a whole cave, candles do not (ROM text).
- Values are safe to poke (BCD for KIM/EXP); keep them realistic (e.g. KIM 473, EXP 62 tested).

## Naming
Main character **ryz**: `NAME` (see Boot sequence). Only one name is asked. Shift/case: lowercase is its own
rows, nothing persists.

## Shortcuts
| What | How (tokens / prefix / code) | Source | Status |
|---|---|---|---|
| Money | `poke:FFC620=00000473` (4-byte BCD) | AR code FFC620/FFC622 (search snippet) | verified (status screen KIM 473) |
| EXP | `poke:FFC624=00000062` (4-byte BCD); max EXP code FFC624:00FF "levels to 31 on the overworld" | snippet | verified (EXP 62 shown); level-up unverified |
| HP / MHP | `FFC62C` / `FFC62E` words, binary | AR 270F codes | read verified (33/33), poke untested |
| MP / MMP, STR, AC, INT, DEX, LUK | words at FFC630, FFC632, FFC634, FFC636, FFC638, FFC63A, FFC63C | AR list (snippet lists LUCK at FFC63E) | read verified at FFC630-FFC63C (1,1,4,8,7,103,6); FFC63E = 0 |
| Caves always lit | `gs:FFC560:0001` | AR (snippet) | unverified |
| Invincible | Game Genie/ROM `01A242:4A78`, `01A20E:4A78` (ROM word patches) | snippet | unverified (needs a `rom:` variant with a raw word patch) |
| Infinite HP GG | `AL4T-AA74` | snippet | unverified |
| Hidden menu | A+B+C+Start on pad 2 | Sega Retro (snippet) | not testable (no pad 2) |

### Saves (rom/saves/sword-of-vermilion/, never committed)
| Name | Contents (progress, party, items) | URL | SHA-1 | Status |
|---|---|---|---|---|
| none downloaded | GameFAQs refused (403) | - | - | - |
Own export: `games/md/sword-of-vermilion/saves/01_start.sav` (Saved Game 1: ryz level 1, 200 kims, Wyclif church),
loaded by `@continue` (verified).

## RAM map (for `game.json` "ram" watches and pokes)
| Address | Size | Meaning | How found |
|---|---|---|---|
| FFC606 / FFC608 | 2 / 2 | town tile x / y (hex) | diff over steps, verified; poking them does not move the prince |
| FFC60D | 1 | facing: 0 up, 2 left, 4 down, 6 right | verified |
| FFC600 / FFC602 / FFC604-05 | | derived: 2x+1, 2y+1, y and 4x+130 (scroll helpers?) | observed |
| FFC620 | 4 | KIM (money), packed BCD | verified by poke |
| FFC624 | 4 | EXP, BCD | verified by poke |
| FFC628 | 4 | Next level EXP, BCD (90 at level 1) | read |
| FFC62C / FFC62E | 2 / 2 | HP / MHP | read |
| FFC630 / FFC632 | 2 / 2 | MP / MMP | read |
| FFC634-FFC63C | 2 each | STR, AC, INT, DEX, LUK | read |
| FFC64C | 4+ | name, ASCII, FF-terminated ("ryz") | read |
| FFC662 / FFC664 | 2 / 2 | overworld square x / y within the current 16x16 map (hex); facing is FFC60D (0 N, 2 W, 4 S, 6 E) | diff over a step (round 2); the map number is open |
| FFC443 / FFC444 | 2 + 2 each | item count word FFC442, then words: high byte flags (00), low byte = item index (0 Herbs, 1 Candle, 2 Lantern, 3 Poison Balm, ... table at ROM 0x25DB4) | poke + Item list, verified |
| FFC462 / FFC464 | 2 + 2 each | spell count, then words: high byte 02 = combat spell (Ferros 0205), 00 = field spell (Sangua 0012); low byte = spell index (0 Aero, 2 Volti, 5 Ferros, 0E Aries, 12 Sangua) | bought in Parma, verified |
| FFC482 / FFC484 | 2 + 2 each | weapon count, then words (Bronze Sword 0400, 8400 when readied: bit 15 = readied) | diff, verified |
| FFC640 | 2 | level minus 1 | level-up diff, verified |
| FFC550 | 1 | FF during a battle | diff, verified |
| FF9000 | 0x600 | map window 48x32 (overworld/cave), see Read first | verified |
| FFC666 / FFC668 | 2 / 2 | current map x / y in the 16x16 grid of maps (outside); in a cave they keep the overworld map | peek at checkpoints, verified |
| FFC820 | 256 | owned-map flags, FF = owned, index y*16 + x; the Mirror of Atlas sets all | Mirror diff, verified by poke |
| FFC55F | 1 | set to FF by a mirror use (meaning unknown) | diff |
| FFC720 / FFC818 | 1 / 1 | story flags: Blade has spoken / Ring of Wisdom received (choose the town line tables) | ROM table 0x1EB0C + poke, verified |
| FFC68B | 1 | enemy group type of the next encounter (0 green slime, 1 blue slime, 0x0A goblins, ... 0x55) | diff over three battles, verified by poke |
| FFC0A4 | 1 | mode-like byte (0 title, 1 name, 6 town start, 9 interior, 10 overworld, 11 battle, 12 cave, 0x18 at a ladder); writes ignored | diff |
| FFC685 | 1 | counts steps and turns on the overworld (reset by a battle); encounter counter? | diff, unconfirmed |
| 200001 ... (odd bytes) | | Saved Game 1 starts with the name | peek after saving |

## Emulation notes
- Model `ntsc`; picture 320x224 for the game, **256x224 for the name keyboard** (H32).
- Battery RAM: the save at 200001 (odd bytes) shows in `peek`; `play.py export` wrote a 64 KiB .sav and
  `sav:01_start` + Continue loads it (verified). cachecheck compares it (hash 05d9f5334d at `saved`).
- Screens rarely settle (blinking cursor, NPCs walking): use explicit waits; checkpoints end with `settle`
  harmlessly.
- Prologue and dialogue speed: "Message Speed Fast / Normal / Slow" exists (ROM text) but where it is set is
  open (not Start on the field: untested).

## Checkpoints
| Name | What |
|---|---|
| title, name, start | boot, keyboard, first control |
| t_door, t_church, t_blade_in, t_blade_room | exploration path to Blade's house (wandering routes) |
| blade | Blade's room after his last words, 200 kims |
| wyclif | outside Blade's house, doors now open |
| tavern | tavern interior |
| church, church_menu, saved | church, priest's menu, after Saved Game 1 |
| continue | the same via `sav:01_start` and Continue |
| t_north_road | the road along the north edge of Wyclif (dead end both ways) |
| t_south_west | south-west corner of Wyclif inside the fence, west of the weapon shop |
| overworld | first-person overworld just outside the south gate, no weapon, 200 kims |
| weapon_shop, shop_list, sword | weapon shop door, Buy list, Bronze Sword bought and readied (100 kims) |
| field | overworld outside the south gate with the sword |
| battle | first battle (green slimes), ~100 frames after the transition |
| escaped | the same battle left by the left edge, back on the overworld (HP 27/33) |
| m_map_gift, m_map_out | Wyclif after the man by the well gave the Parma route map (ring flag poked); outside the gate with the area map in the panel |
| m_ring | cave south of Wyclif, Ring of Wisdom received from the old man (honest, from `m_cave_inner`) |
| m_strong ... m_cave2_lit | main-set chain, see Read first |

## Sources
| Source | URL | Used for | Accessed |
|---|---|---|---|
| Wikipedia | https://en.wikipedia.org/wiki/Sword_of_Vermilion | release, staff, story, views | 2026-11-20 |
| Search snippets: almarsguides AR/GG lists, 53lu / etherealgames AR lists | https://almarsguides.com/retro/walkthroughs/genesis/games/swordofvermilion/actionreplay/ | RAM addresses (KIM, EXP, stats, caves lit) | 2026-11-20 (site itself unreachable: host not allowed) |
| Search snippet: Sega Retro hidden content, TCRF save error text | https://segaretro.org/Sword_of_Vermilion/Hidden_content | pad-2 hidden menu | 2026-11-20 |
| Search snippet: speedrun.com any% guide | https://www.speedrun.com/sword_of_vermilion/guides/797nr | "go to the house top-left", equip sword outside | 2026-11-20 |
| Search snippet: TheStarbird FAQ (GameFAQs mirror) | gopherproxy (host not allowed) | 16x16 maps, Wyclif tips | 2026-11-20 |
| Japanese manual (archive.org) via snippet | https://archive.org/download/SEGAGenesisMegaDriveManuals/Vermilion%20%28Japan%29.pdf | C = commands, 8 commands, church save | 2026-11-20 |
| ROM text | `strings` over the dump (`work/scout/sword-of-vermilion/strings.txt`) | names of towns, items, magic, menus | 2026-11-20 |
| Unavailable | gamefaqs (403), tcrf.net (403), strategywiki (403), datacrystal (no page), archive.org file hosts and almarsguides/gopherproxy (not allowed) | - | 2026-11-20 |

## Open questions
- ~~How to leave Wyclif~~ solved in round 2: the south gate opens after Blade has spoken (fresh `down` on 0D,2B).
- Is there a victory/reward screen after the last enemy of a battle? (not reached: mashing C alone stalls with
  slimes around; move toward them between swings).
- Why `@battle` + 600 frames of losing differs in memory between a loaded state and a flat replay (backend?).
- Real position variables (town and overworld), map id, encounter trigger, battle state, spell list slots.
- Battle buttons; where Message Speed is set; Bronze Sword price; the inn and fortune teller interiors.
- Whether the AR invincibility codes (ROM words) and the Game Genie codes work as `rom:` variants.

## Capture 2026-11-20 (notes)
- Cave south of Wyclif (overworld square 7,13 of the map below Wyclif's): one 16x16 map, entrance ladder, two barred
  doors (Open raises the bars), one chest with a Candle. No boss and no Ring of Wisdom found there.
- Road to Parma: from the gate west/north along the road, two maps north; Parma's entrance is a special square
  (value 0x11) at window (23,5) of that map. Enemies: green and blue slimes near Wyclif, goblins near Parma.
- Parma: inn 13 kims (east street, INN sign); magic shop (house with a wand sign, door 16,12 from the south lane):
  Ferros 500, Sangua 800. Church: big stone building east of the main street (not entered).
- East of Parma: a stone cave entrance on the overworld (`m_cave2_gate`), same stone tile set inside; a special
  square value 2 at window (30,16) not reached (the walker got lost when the window re-centred).
- No in-game save was made after Parma (no church visited there); `saves/01_start.sav` is still the only export.

## Capture 2026-11-20 round 3 (maps and presentations)
- Wyclif people: 14 per phase, three tables at ROM 0x2D424 (before Blade), 0x2D45C (after), 0x2D494 (ring). Index 1
  says "There's a ring in a cave south of here. Here's a map to guide you." after Blade (not found on foot: people
  wander); index 3 is the man by the well west of the inn (`m_map_gift`).
- Cave south of Wyclif: money chest at window (18,27) (route in shots `system_open_money`), the ring keeper at
  (18,20). Cave of Troy (map 3,4): one map; the special square 2 at (29,16) is a ladder up seen from (28,16); its
  chests and the treasure not explored.
- NPCs walk: a Talk route only reproduces with the exact waits; the dialogue shot replays from `@overworld`.
- Dead ends for the boss/ending: no 68000 disassembler in the container (installing capstone was refused); the
  encounter byte above 0x55 crashes (0x81 gives a green screen); FFC0A4 writes are ignored.
