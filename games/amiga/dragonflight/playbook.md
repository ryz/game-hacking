# Dragonflight - playbook

Everything an agent needs to play this game efficiently: read it before playing, add to it after every run.
Status of each fact: **verified** (seen in the emulator, with the route) or **source** (manual/FAQ/wiki, not yet
checked). Never delete a fact that turned out wrong: strike it and say what is true.

## Read first
- **Start:** `rom/dragonflight.zip` (Disk 1 = CLS crack, Disk 2 = original Disk B; `python3 tools/vault.py pull
  dragonflight`), `rom/kickstart/kick34005.A500`, model `A500`. Checkpoints: `title`, `menu`, `diskb`, `start`
  (Pegana, first control), `world` (land outside Pegana), `pegana_road` (Pegana re-entered from the land),
  `loaded` (Old game from the save `01_start`). Boot to first control is about 12000 frames (real floppy speed).
- **Everything is a mouse click on a poked pointer.** The pointer position is chip RAM `3BCA` (x) / `3BCC` (y),
  game pixels; `PT:XXXX:YYYY` pokes it, `CLK:XXXX:YYYY` pokes + left click + `w60`.
  `python3 games/amiga/dragonflight/tools/at.py SX SY c` turns a pixel of the 720x287 screenshot into the token
  (SX = 2x + 35, SY = y + 15). Do **not** steer with large `mouse:` moves: the game reads the counters only every
  few frames and big moves wrap (the pointer lands anywhere).
- **Icon grid** (bottom right, 3 x 3; the set of icons changes with the place): columns x `00E6`/`0106`/`0127`,
  rows y `008F`/`00A5`/`00B7`. Macros: `MAGIC` (pentagram, "Who should cast ?"), `SPEAK` (town: lips, "Speak to
  WHOM?"), `SHIP` (land: "There is no ship!"), `ENTER` (land: enter the town/place you stand on), `CAMP` (land:
  campfire scene; town: "Not here!"), `SEARCH` (land: eye, "You found nothing"; in town the eye is at `0106:00A5`
  and names what is in front: "It's Housens."), `DISK` (land: save menu), `SAVEGAME`.
  Portraits (2 x 2, top-left of the panel): `BLADUS`, `RINAKLES`, `DOBRANUR`, `ANDARIEL` open the status screen;
  on it `CLK:0101:0055` = Inventory, `CLK:0124:0055` = Spells, `CLK:0124:006E` = back to the map.
- **Moving:** keypad `kp8/kp2/kp6/kp4` (macros `N`, `S`, `E`, `W` = key + `w30`; diagonals `kp7 kp9 kp1 kp3`,
  source: the arrow panel shows eight directions). Right button (`ARROWS`) swaps the icon grid for eight arrows
  and a rest icon; right button again swaps back (seen once). Leaving a town: step off its edge, "Leave this
  place? Left YES Right NO", `mouse1` = yes. `LEAVE` = warp to the town corner + step + yes.
- **Position:** `y` `3BF4`, `x` `3BF6` (words; mirror at `118B2`/`118B4`, poke both: macro `WARP:YYYY:XXXX`).
  A warp is drawn only after the next step. Start in Pegana y `0032` x `0069`; the land outside Pegana y `0060`
  x `00D7`.
- **Party records:** `2A00 + n*0x400` (Bladus, Rinakles, Dobranur, Andariel): +0 HP, +2 max HP, +4 magic, +6 max
  magic, +8 character, +A experience, +22 gold, +26 food (words, verified by pokes on the status screen).
- **Disks:** after a new game's intro the game asks for Disk B (`disk:2`); it stays in DF0: while playing.
  Saving writes to Disk B itself (`SAVEGAME`, "Game saved", about 1500 frames); the crack note's backup copy is
  not needed here (the emulator writes to a private copy of the image). Old game swaps B, A, B (`OLDGAME`).
- **Traps that cost calls:** `play.py` frames often say "still changing" (the message panel and water animate):
  normal. Loads are long: wait, do not click (clicks during a load are lost or act later). A cached checkpoint
  does not continue bit-exactly (Emulation notes): `cachecheck.py` says DIFFERS for every checkpoint although the
  frames match; build shots through the checkpoint chain and verify with `shoot.py --verify`.
- **State:** scouted 2026-11-22: boot, new game, Old game, save, controls, position and party RAM. Not reached:
  a fight (no random encounter in about 150 steps on the land near Pegana), a dungeon, a shop, a dialogue with a
  person, magic in use, the dragon. Their routes are the capture run's first job (see Shot plan).

## Identity
| Field | Value |
|---|---|
| Title (EN / original) | Dragonflight (English; German "Dragonflight" too) |
| Platform / model used | Amiga, `A500` (Kickstart 1.3, 512K chip + 512K slow): **verified** power-on to play, save and load |
| Release (region, year) | Europe, 1990 (Wikipedia: Amiga, Atari ST, MS-DOS) |
| Developer / publisher | Thalion Software (design and art Erik Simon, code Udo Fischer, music Jochen Hippel: Wikipedia) |
| Genre | party RPG: top-down towns and land, first-person dungeons, turn-based grid combat (source) |
| Players / save system | 1 player; one saved game on Disk B (disk icon on the land; Old game on the Main Menu): **verified** |
| Dump | TOSEC `Dragonflight (1990)(Thalion)(Disk 1 of 2)[cr CLS]` + `(Disk 2 of 2)` (original; SHA-1s in `game.json`) |

## Boot sequence
- Intake probe: `work/intake/amiga/dragonflight/sheet.png` (frame every 60 frames, no input).
- **verified** 2026-11-22 on the A500 (`preview.py --timeline` from power-on):
  - Kickstart 1.3 boots Disk 1; the CLASSIC crack intro (vector letters "THE UNTOUCHABLE CLASSIC PRESENTS -
    DRAGONFLIGHT - FROM THALION...") runs from about frame 240. `mouse1:10` at `w300` leaves it.
  - Loading on a blue, then purple screen; raining coloured drops from about +1200, the THALION logo fades in at
    +1800 and is complete at +2100. It waits: `mouse1:10` at +2400.
  - Then the red dragon on a rock spreading its wings (+800 to +1600 after the click), a sun that fills the
    screen (+1800), black, the DRAGONFLIGHT logo (+2600) and the Main Menu (+3400). The two alternate (logo again
    at +4000, menu at +4600). `TITLE` = `w300,mouse1:10,w2400,mouse1:10,w2600` (logo), `MENU` = `TITLE,w900`.
  - Main Menu (keys): `n` New game, `o` Old game, `b` Backup gamedisk (Backup Menu: F Format Disk, C Copy
    Disk, H Help, E Exit to Main Menu), `s` Sequences (asks "Insert backupdisk B! (ESC to cancel)"), `c` Credits
    (black after 300 frames: not followed). "Configuration: 00000" below.
  - `n`: after about 900 frames the sage scene (old man in purple robes in a stone room) with a text scroll of
    five lines and an arrow; a left click per page, four pages (Rings of Stasis, one part of the Great Map,
    Bengiur in Drindil, "Good luck!"). `space`, `esc` and the right button do not turn the page. Then the panel
    alone: "Insert disk B please" (checkpoint `diskb`). `disk:2` -> "Thank You!", loading, "Loading...
    Pegana", the town at +2800 (checkpoint `start`). `NEWGAME` = all of it from the menu.
- Screen modes: title and menus lores (360 wide), the game screen hires (720x287). No interlace on the A500
  (the coordinator saw 720x574 with AROS).

## Controls
| Context | Input | Action | Status |
|---|---|---|---|
| Crack intro, Thalion logo, intro pages | left button | continue / next page | verified |
| Main Menu | `n` `o` `b` `s` `c` | New game, Old game, Backup gamedisk, Sequences, Credits | verified (n, o, b, s); c not followed |
| Town / land | keypad 8 2 6 4 | move north, south, east, west one square ("North", "Blocked" in the scroll) | verified |
| Town / land | keypad 7 9 1 3 | diagonal moves | source (arrow panel), not tried |
| Town / land | right button | swap icon grid <-> direction arrows (8 arrows + "Zz" rest) | verified |
| Town / land | left button on a portrait | status screen of that hero | verified |
| Status screen | `?` / pentagram / hand icons | Inventory (gold, food, items: "01 Torch") / Spells / back | verified |
| Town | pentagram, lips, hand, eye | cast ("Who should cast ?"), speak ("Speak to WHOM?"), use or open ("Nobody at home." at a door), look ("It's Housens.") | verified (prompts only) |
| Land | pentagram, sword, ship, enter, campfire, eye, disk | cast, (sword: not understood, the cell turned into a hand-with-item icon), ship ("There is no ship!"), enter, camp (campfire scene "Camp", "zzz..."), search ("You found nothing"), disk menu | verified except sword |
| Disk menu (land) | top-left disk / top-right disk / bottom-right | load? / save ("Gamesave? Left YES Right NO") / exit | save and exit verified, top-left not tried |
| Yes/No prompts | left / right button | yes / no | verified |
| Waiting | nothing | about every 800 frames a turn passes ("Pass") | verified |

Input timing: the default press (hold 8, wait 40) works for keys and the left button. Clicks need the pointer
poked first (`PT`), then `mouse1`. Keypad steps with `w30` between them all count (20 of 20 seen).

## Game structure
Top-down towns (Pegana, the starting town, is about 0x75 x 0x75 squares) and a top-down land with roads, rivers,
forests and a bridge; towns appear as icons on the land, entered with `ENTER`. The intro names Bengiur in Drindil
as the next contact. Twelve parts of the Great Map to collect; Rings of Stasis revive their bearer. Dungeons
are first-person (game text: Forward, Backward, Turn left/right, Upstairs, Downstairs, Approach, Withdraw,
doors to listen at, chests with traps). Disks: A (program, Disk 1), B (world and save, Disk 2); the game text
also asks for disks C and D, which this dump does not have (two disks only: TOSEC lists 2) - open question.

## Shot plan
Must-haves first; ids are the `main` set. Route status: R = route known (in `shots.txt`), ? = needs finding.
- [R] `boot_crack` boot - CLASSIC crack intro, vector letters (`w300,!`-ish, pick frame)
- [R] `boot_thalion` boot - THALION logo over the raining drops
- [R] `title_dragon` cutscene - the red dragon spreading its wings
- [R] `title_screen` title - DRAGONFLIGHT logo
- [R] `menu_main` menu - Main Menu with its five keys
- [R] `menu_backup` menu - Backup Menu (Format / Copy / Help / Exit)
- [R] `cutscene_sage` cutscene - the sage with the Rings of Stasis, intro page 1 (and page 4 for `start`)
- [R] `env_pegana_square` gameplay - Pegana at the start, nothing happening
- [R] `env_pegana_road` gameplay - Pegana's western road (`@pegana_road`)
- [R] `env_land_river` gameplay - the land outside Pegana, river and road
- [R] `env_land_forest` gameplay - deep forest south of Pegana
- [R] `env_land_bridge` gameplay - bridge and the grey mountain/cave mark to the east (`@world,S*3,E*40,N*10`)
- [R] `hud_land` hud - the full panel on the land (portraits, scroll, 7 icons)
- [R] `system_arrows` system - right-button arrow panel
- [R] `system_camp` system - camp scene
- [R] `inventory_status` inventory - status screen of Bladus
- [R] `inventory_items` inventory - Inventory (gold, food, torch)
- [R] `inventory_spells` inventory - Spells page (empty at the start; a filled one later)
- [R] `save_prompt` save - "Gamesave? Left YES Right NO", and `save_done` "Game saved"
- [R] `menu_oldgame` save - Old game disk prompts / "Game loaded"
- [?] `dialogue_*` dialogue - speak to a townsperson in Pegana (SPEAK, then click the person on the map: pointer
  on the map is untested; the hand icon at a door gave "Nobody at home.")
- [?] `shop_*` shop - a shop or inn in Pegana (houses: try the hand icon at each door, see Strategy)
- [?] `battle_*` battle x 3-5 - grid combat with side view: no encounter found yet
- [?] `gameplay_dungeon_*` gameplay - first-person dungeon views (2-3 places), `env_dungeon_*`
- [?] `system_magic` system - casting a spell; `system_potion` mixing potions; Staff of Stone
- [?] `map_great_map` map - the Great Map part, if the game shows it
- [?] `gameplay_ship` gameplay - on a ship; `gameplay_dragon` - dragon flight if reachable
- [?] `gameover` gameover - the party dead (poke HP 0 before a fight)
- [?] `town_drindil` gameplay - a second town (Drindil)
`start` set: power-on, crack intro, logo, dragon, title, menu, the four sage pages, disk B prompt, Pegana, the
first steps, status/inventory, leaving the town, the land, a camp, the first fight (when found), saving.

## Strategy and walkthrough notes
- No walkthrough was reachable (Sources). Explore Pegana with the hand icon at doors and SPEAK near people (the
  person in white at the south-east of the start square, y 0034 x 0067 area); shops likely sit behind doors.
- For a fight: walk the land away from roads, wait (turns pass), or look for monsters at the grey mountain/cave
  east of Pegana (`@world,S*3,E*40,N*10`). Poke HP high (records above) if the party is weak; values realistic.
- Do not poke the position into a wall square: the game moves you but draws the old view until the next step.

## Naming
The four heroes are fixed and named by the game (Bladus, Rinakles, Dobranur, Andariel); there is no name entry
(verified: none in the new-game route), so the owner's names cannot be used.

## Shortcuts
| What | How (tokens / prefix / code) | Source | Status |
|---|---|---|---|
| Warp in the current map | `WARP:YYYY:XXXX` then one step | RAM | verified (town corner -> leave prompt) |
| Leave a town at once | `LEAVE` | RAM | verified |
| Gold / HP / food / experience | `set:2A22=873:2` etc. (records above) | RAM | verified on the status screen |
| Save and Old game | `SAVEGAME`; `sav:NAME,MENU,OLDGAME` | play | verified |
No cheat codes, saves or debug menus found (no source reachable).

### Saves (rom/saves/amiga/dragonflight/, never committed)
| Name | Contents | URL | SHA-1 | Status |
|---|---|---|---|---|
| `01_start` | new game, party just outside Pegana, saved with the disk icon (export from play.py) | made here | `ae07f47d0aa1` (prefix) | verified: Old game loads it ("Game loaded", same position) |

## RAM map (for `game.json` "ram" watches and pokes)
| Address | Size | Meaning | How found |
|---|---|---|---|
| 3BCA / 3BCC | word / word | pointer x / y (game pixels); poke to place the pointer | find + poke, verified by clicks |
| 3F24 / 3F26 | word | last raw mouse counters (not the pointer) | find |
| 3BF4 / 3BF6 | word / word | party y / x on the current map (mirror 118B2 / 118B4) | find (steps), poke verified |
| 2A00 + n*400 | 0x28+ | hero n: +0 HP, +2 max HP, +4 magic, +6 max magic, +8 character, +A experience, +22 gold, +24 level? (1), +26 food | dump + poke, verified on status screens |
| 062C + n*28 | | the start values of the same records (new-game template; pokes here do nothing) | dump |
| 0D6D1, 11C9E, 20318... | | hero names and game text in plain ASCII (messages, opponents) | dump |

## Emulation notes
- A500 (Kickstart 1.3, 512K + 512K). Loads at real speed: crack intro to Thalion logo about 2400 frames, the
  logo click to the menu about 3400, new game to Pegana about 4000.
- **Savestates do not continue bit-exactly in this game** (scout 2026-11-22): a state saved at any point and
  loaded into a fresh machine gives the same picture but 30-45 different bytes of chip RAM 60 frames later
  (animation buffers at 180C2 and 2525F-253A1 during the title), even at `w100` in the Kickstart boot on the
  `A500` (slow RAM differs there) - not on `A500OG` at `w100`, but again later in the game on `A500OG` and
  `A500ECS`. So `cachecheck.py` reports every checkpoint DIFFERS (cold and hit vs flat). Probably a game
  random source (beam position or CIA timer) that the restore does not reproduce to the cycle. Consequence:
  random outcomes (encounters, combat rolls) may differ between a flat replay and a cached chain; shoot through
  the chain and check with `shoot.py --verify`. Reported to the coordinator as a backend question.
- The pointer is often not drawn in the screenshots (it shows on the panel in the disk menu); clicks still work.
- `w20` vs `w30` between keypad steps: `w30` is safe; not tried shorter.

## Checkpoints
See `checkpoints.txt`. `world` and `pegana_road` start from a poked exit (position only); `loaded` starts from
the exported save `01_start` and needs `rom/saves/amiga/dragonflight/01_start.sav`.

## Sources
| Source | URL | Used for | Accessed |
|---|---|---|---|
| Wikipedia | https://en.wikipedia.org/wiki/Dragonflight_(video_game) | credits, platforms, views, combat style, mouse control | 2026-11-22 |
| Thalion Webshrine | http://thalion.exotica.org.uk/games/dragonflight/df.html | not reachable (host not allowed in this session) | 2026-11-22 |
| GameFAQs | https://gamefaqs.gamespot.com/amiga/952681-dragonflight/faqs | 403 (refuses automated access) | 2026-11-22 |
| archive.org search | advancedsearch "dragonflight" | no manual or guide found | 2026-11-22 |
| Disk 1 text (strings) | `rom/dragonflight.zip` | Backup Menu texts, crack note | 2026-11-22 |
| Game text in RAM | dump of `@start` | commands, messages, opponents | 2026-11-22 |

## Open questions
- Where are fights? No encounter in about 150 land steps near Pegana; are they place-bound or time-bound?
- The land sword icon: what does it do (the cell became a hand-with-item icon)?
- The disk menu's top-left icon (load?) and how SPEAK picks a person (click on the map?).
- Disks C and D in the game text: does the game ever ask for them with this two-disk release?
- Does `c` Credits show anything after a longer wait? Does `s` Sequences play the intro scenes with disk B?
- Manual (controls, spells, map): the Thalion Webshrine has it; ask for the host to be allowed.
