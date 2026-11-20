# Sword of Vermilion - playbook

Everything an agent needs to play this game efficiently: read it before playing, add to it after every run.
Status of each fact: **verified** (seen in the emulator, with the route) or **source** (manual/FAQ/wiki, not yet
checked). Never delete a fact that turned out wrong: strike it and say what is true.

## Read first
- **Start:** `rom/sword-of-vermilion.md` (SHA-1 c18fc75e...), model `ntsc`. `play.py start sword-of-vermilion --route @saved`
  (Wyclif church, game saved) or `@wyclif` (outside Blade's house). `@continue` = the same state via the
  exported save `saves/01_start.sav` and the title's Continue.
- **Macros:** `TITLE` = `w800` (title with cursor; inputs work from ~f300, Start then lands on the title);
  `NAME` types ryz on a fresh keyboard; `NEWGAME` = keyboard, name, Start, the auto-running prologue (no skip)
  to first control (~4500 frames); `PAGE` = `c,w90` (one dialogue page at Normal speed); `CONTINUE` = title ->
  Continue -> Saved Game 1 -> "Your game is ready" -> in front of the priest.
- **Checkpoint chain:** title -> name -> start -> t_door -> t_church -> t_blade_in -> t_blade_room -> blade ->
  wyclif -> tavern -> church -> church_menu -> saved; continue (from the .sav). All 14 reproduce
  (`tools/cachecheck.py`). The routes before `wyclif` are exploratory (they wander); they are correct, not short.
- **Controls:** C = confirm / field command window; B = back/close and delete on the keyboard; Start = title
  choice and ends naming. A: no use found yet.
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
  - The title and most field screens never settle (blinking cursor, animated water/NPCs): "NOT settled" is normal.
- **State:** scouted only. Not reached: the exit from Wyclif to the overworld (south gate tile 0D,2B does not
  lead out; east is a graveyard), the first-person overworld, any battle, the weapon shop interior.

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
| Overworld / caves | D-pad | step forward / turn (first person) | source (Wikipedia), unverified |
| Battle | | sword attack, magic, real-time (source: Wikipedia); buttons unverified | source |
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
Routes in `shots.txt` (12 lines verified by `preview.py`, the rest planned as comments).
- [x] `boot_sega`, `cutscene_intro_tree`, `title_screen`, `menu_name`, `cutscene_prologue_tsarkon` - boot to naming
- [x] `start_wyclif_gate` (gameplay), `dialogue_blade_house`, `env_wyclif_blade_house`, `gameplay_tavern`
- [x] `save_church_menu`, `save_slots`, `menu_continue_slots`
- [ ] `cutscene_blade` - Blade's deathbed pages (from `t_blade_room`, route in `blade`; pick a page with `PAGE`)
- [ ] `hud_field_menu`, `inventory_status`, `inventory_equip` - field window, status, equip (routes in Controls)
- [ ] `shop_weapon` - buy a Bronze Sword in Wyclif (door 09,28; enter with a fresh `up`)
- [ ] `env_wyclif_*` (2-3 plain street views), `env_graveyard`, Blade's grave
- [ ] `env_overworld_*` (3-4), `gameplay_cave_dark` / `gameplay_cave_lit` - first-person views
- [ ] `battle_first`, `battle_attack`, `battle_magic`, `battle_won` - side-view battles (several enemy types)
- [ ] `map_area` (Area Map item), `system_magic` (a spell cast), `system_lantern`
- [ ] `boss_first` - the first boss; `gameover`; `options_message_speed`; later towns (Parma, Watling ...)
Fastest ways: the `saved` checkpoint for town shots; stats by poke (RAM map) before fights; town warps with
the Aries spell once the spell slot RAM is known (Action Replay lists name "All Towns Available With Aries").

## Strategy and walkthrough notes
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
- How to leave Wyclif: the south gate tile (0D,2B) and fresh `down` presses do not exit; east is the graveyard;
  north ends at Blade's house. Try west, the gate with a longer wait, or talk to the gate guard first.
- Real position variables (town and overworld), map id, encounter trigger, battle state, spell list slots.
- Battle buttons; where Message Speed is set; Bronze Sword price; the inn and fortune teller interiors.
- Whether the AR invincibility codes (ROM words) and the Game Genie codes work as `rom:` variants.
