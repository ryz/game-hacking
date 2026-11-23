# Quake (DOS, shareware 1.06) - playbook

Everything an agent needs to play this game efficiently: read it before playing, add to it after every run.
Status of each fact: **verified** (seen in the emulator, with the route) or **source** (manual/FAQ/wiki, not yet
checked). Never delete a fact that turned out wrong: strike it and say what is true.

## Read first
- **Start:** `rom/quake.zip` (shareware 1.06, SHA-1 in `game.json`), model `svga-80000`. Boot = DOSBox Pure's
  "Go to Command Line", then `quake -nocdaudio -nosound` (macro `BOOT`). No title screen: the start-up
  console rolls up into attract demo 1 (E1M3); Escape gives the main menu (`MENU`).
- ~~Before any preview/shoot on an empty cache: `qstate.py --warm`~~ No longer needed (coordinator, 2026-11-23):
  `emu.at_checkpoint` now reloads the state it just built, so a cache miss and a hit continue identically
  (checked on `@s_e1m1,up:40,...`: same picture). Still true: a loaded state plus keys is not the flat replay
  (see "Determinism"), so checkpoints stay flat.
- **Every checkpoint route is flat (macros from power-on, no `@parent`)** for the same reason. Keep it so:
  a checkpoint built on `@another` does not reproduce (`cachecheck` says cold/hit DIFFERS).
- **Do not use `play.py undo`/`goto` mid-exploration and then snap:** the snapped route replays without the
  state load in the middle and shows something else. Explore with `preview.py` lines and
  `games/dos/quake/tools/qstate.py --chain ROUTE TOKENS TOKENS ... --png DIR` (one machine, a frame + position
  after every group; this is how the whole start route was found).
- **Checkpoints (all verified, `cachecheck`):** `demo`, `menu`, `s_startmap` (new game, start map spawn),
  `s_hub` (through the Normal slipgate), `s_e1m1` (E1M1 spawn), `s_e1m1_door` (first Grunt in view),
  `s_e1m1_lift` (rode the lift down), `s_e1m1_yard` (Grunt + Rottweiler attack), `s_e1m1_clear` (after the
  fight), `s_e1m1_saved` (saved to slot 1 = `ID1/S0.SAV`; exported as `saves/01_start.sav`).
- **Set `start` is published** (2026-11-23): 35 shots `01_command_line` ... `35_load_menu` in
  `shots/start/` (its `shots.txt` is the source; `--verify` 35/35 from an empty cache). To retake:
  copy it to `work/shots/dos/quake/start/shots.txt`. Lines end in `!`: Quake never settles; keep the `!`.
  Shot routes may be `@checkpoint,keys` (load + keys is reproducible by itself, cold or warm, since the
  2026-11-23 `at_checkpoint` fix); only checkpoint routes must be flat.
- **Movement is key holds:** `up:40` walks ~130 units, `left:46`/`right:46` turn ~90 degrees (1.9-2.0
  degrees per frame, it varies a few degrees with the frame rate, so check the yaw with `qstate.py`),
  `ctrl:8,w40` fires the shotgun once, `a:N`/`z:N` look up/down, `tab:40,!` shows the score overlay.
- **Position and status:** `qstate.py` prints origin, yaw, health, armor, ammo from the player's entity at
  0x371D48 (floats; layout `entvars_t`). Only valid with this BOOT (with sound it was 0x37A638);
  `qstate.py --find ROUTE` finds it again.
- **Map data:** entities of every map (monsters, items, buttons, secrets, level exits, with skill flags) are
  readable from `ID1/PAK0.PAK` (see "Maps"); that is faster than walking around.
- **Traps:** `-nosound` is required (with the Sound Blaster on, a loaded state diverges from the flat run on
  the very next frame). The DOSBox Pure start menu and the blue DOSBox banner are front-end screens (the
  banner shows above the command line in shot 01; acceptable as the DOS boot, do not take more).
- **Open:** first weapon pickup (Nailgun at 112 2352, far into E1M1) and the first secret are not routed
  (dead ends tried: "Strategy" below); armor not picked up; console cheats untested beyond `timedemo`
  (the console opens with the backquote key).
- **Map entities:** `python3 games/dos/quake/tools/ents.py e1m1 "secret|weapon|monster"` (brush boxes too).

## Identity
| Field | Value |
|---|---|
| Title (EN / original) | Quake (shareware version 1.06) |
| Platform / model used | MS-DOS, see `game.json` (`svga-80000`) |
| Release (region, year) | North America; shareware released 22 June 1996 (source: Wikipedia); 1.06 build dated Sep 30 1996 on the start-up console (verified) |
| Developer / publisher | id Software / id Software (shareware; retail by GT Interactive) (source) |
| Genre | first-person shooter, real-time 3D |
| Players / save system | 1 player (multiplayer over IPX/serial/modem not used); save anywhere in 12 slots, files `ID1/S0.SAV`-`S11.SAV`; quicksave F6 (source: CONFIG.CFG binds) |

Dump: `msdos_Quake106_shareware.zip` from archive.org (see `game.json` "source"): QUAKE.EXE, CWSDPMI.EXE,
ID1/PAK0.PAK (stock shareware 1.06, md5 5906e599...), ID1/CONFIG.CFG with stock binds, id's README/HELP/TECHINFO.

## Boot sequence
- Intake probe: `work/intake/dos/quake/sheet.png`: DOSBox Pure's start menu (five programs) waits for a key.
- Starting QUAKE.EXE from that menu (`down*4,enter`) stops on "MSCDEX not loaded, music is disabled. Use
  -nocdaudio ... Press a key." (verified). The command line avoids it and allows the switches:
  `BOOT` = `w120,down*5,enter,w120,type:quake -nocdaudio -nosound\n` (verified).
- After BOOT: frame +10 DOS prompt with "Quake v1.06 / Locked 1 Mb image / Locked 13 Mb data"; +100 the
  start-up console over the Quake backdrop (S3 Trio64 VESA, joystick not found, configs, "3 demo(s) in loop",
  "Playing demo from demo1.dem", level name The Necropolis); +160 demo 1 is playing (verified).
- `DEMO` = `BOOT,w300`; `MENU` = `BOOT,w300,esc,w40` (main menu over the demo, Single Player highlighted);
  `NEWGAME` = `MENU,enter,w40,enter,w600` (Single Player, New Game: the start map, ready to move) (verified).
- `NORMAL` = start map spawn to the episode hub through the Normal hall (walk north, it passes the
  setskill trigger at y 1345-1359 and the slipgate at y 1369-1383) (verified, position 544 1605 24).
- `TOE1` = hub to E1M1: turn west, walk up the stairs to x -54, turn south into the Episode 1 slipgate
  (changelevel e1m1 at x -87..-41, y 1601..1655), wait 200 frames (verified, E1M1 spawn 480 -352 88).
- E1M1: `E1DOOR` (north through the start corridor and the hall, west at y 570 to the sliding door: it opens,
  the first Grunt is in the corridor), `E1GRUNT` (two shotgun shots kill it), `E1LIFT` (walk west onto the
  lift; walking into the red button sends it down), `E1YARD` (north into the open yard: a Grunt and a
  Rottweiler attack, health 100 -> 88), `E1FIGHT` (turn slightly right, three shots), `SAVE0` (F2, Enter on
  slot 1). All verified, see Checkpoints.

## Controls
Stock binds from `ID1/CONFIG.CFG` (source) and what was tried here.
| Context | Key | Action | Status |
|---|---|---|---|
| Play | up / down | forward / back (`+forward`, `+back`) | verified (`up:70` = ~240 units; `down:70` back) |
| | left / right | turn | verified (~1.95 degrees per frame) |
| | ctrl | fire (`+attack`) | verified (`ctrl:8` = one shotgun shot, 1 shell) |
| | space / enter | jump | source (used as `space+up` in NORMAL; no jump-only check) |
| | shift | run (`+speed`) | source |
| | alt | strafe modifier; `,` `.` step left / right | source |
| | a / z (pgdn / del) | look up / down; `end` centre view | verified (a:30 pitch 20.6 up, z:60 back down to -20.6) |
| | 1-8, `/` | choose weapon, next weapon (impulse 10) | source |
| | tab | score overlay (Monsters, Secrets, Time, level name) while held | verified (`tab:40,!`) |
| | c / d | swim down / up | source |
| | escape | menu (pauses single player) | verified |
| | F2 / F3 | save menu / load menu | F2 verified; F3 source |
| | F6 / F9 | quicksave / quickload (`save quick`) | source |
| | F1, F4, F5, F10, F11, F12 | help, options, multiplayer, quit, zoom, screenshot | source |
| | ` (backquote) or ~ | console | verified (typed `timedemo demo1`) |
| Menus | up / down, enter, escape | move, choose, back | verified |
| Customize | enter, backspace | change / clear a bind | seen on screen (verified display) |

Input timing: default press (hold 8, wait 40) works in all menus tried. In play a hold of N frames is
movement/turning for N frames; presses are not lost. A key held across a level load keeps acting in the new
level (the first TOE1 attempt walked on into E1M1): release before the load if the checkpoint should stand
at the spawn.

## Game structure
- Start map (Introduction, `start.bsp`): three skill halls from the spawn: Easy (west, x 209-255), Normal
  (straight north, x 521-567), Hard (east, x 841-887); each ends in a slipgate to the hub (map data). A secret
  Nightmare entrance sits in the hub (trigger at 953-1023, 1921-1935, z -95..63) (map data, not tried).
- Hub: four episode slipgates; only Episode 1 (Dimension of the Doomed) is open in the shareware: walking
  toward the others shows "This is the shareware version. Please register! Call 1-800-IDGAMES today!"
  (verified on screen). E1 slipgate: "Walk into the Slipgate to start playing Quake!" (verified).
- Episode 1 (shareware): E1M1 The Slipgate Complex, E1M2 Castle of the Damned, E1M3 The Necropolis, E1M4 The
  Grisly Grotto, E1M5 Gloom Keep, E1M6 The Door to Chthon, E1M7 The House of Chthon (boss), E1M8 Ziggurat
  Vertigo (secret) (source: pak file list, map names seen in demos: The Necropolis, The Grisly Grotto).
- Attract demos: demo1 (E1M3), demo2 (E1M4), demo3, looping (verified for 1-2 in timedemo runs).

### Maps (read entities from the PAK)
`ID1/PAK0.PAK` holds `maps/*.bsp`; the entity lump lists every monster, item and trigger with its origin and
`spawnflags` (256 = not on Easy, 512 = not on Normal, 1024 = not on Hard, 2048 = not in deathmatch; 768 = Hard
only). Brush entities (doors, buttons, triggers) have `model *N`: the model lump gives their box. A 40-line
reader was used (scratch); worth a `games/dos/quake/tools/` helper if the capture needs it again.
E1M1 on Normal, near the route: Grunt (0 576 24) by the lift button (-67, 561-591), lift (x -63..63, y
513..639, goes down 240), second button at the bottom (81-111, 705-711), yard Grunt (8 1520 -200) and
Rottweiler (88 1520 -200), Green Armor (688 480 80, behind the "Shoot this secret door" panel at 657-719,
49-63, z 49-111), Nailgun (112 2352 16; picking it up triggers a secret door and a Grunt ambush at 193-207,
2305-2431), Quad Damage (544 2480 -88), Biosuit (712 2040 -408), exit to E1M2 (1289-1335, 521-567, z
-279..-129). Six secrets (trigger_secret boxes listed in the map). Level stats on TAB: 23 monsters, 6 secrets
(verified).

## Shot plan
- [x] Set `start`: captured 2026-11-23, 35 shots, published in `shots/start/` (verified 35/35 cold).
  Changes from the scout's 34 lines: ids without the repeated category (`01_command_line`, not
  `01_boot_command_line`); 03 later frame (`BOOT,w160,w20,w20,w20,!`, the old one was nearly black); the
  near-duplicate slipgate shot dropped (the slipgate never gets closer than the hall text frame); added
  `08_help_movement` (Help page 1), `26_e1m1_yard_fire` now the muzzle-flash frame (`@s_e1m1_yard,right:6,
  ctrl:8,!`), `35_load_menu` (slot 1 "The Slipgate Complex kills: 2/23"); `12_env_hub_west` as an env view.
  Frames tried and left out: the lift ride (black for 200 frames), the Grunt firing at the player
  (`@s_e1m1_yard,right:6,w9*10,!`: red flash, health 88 -> 76; a branch where the player does not shoot).
The scout's plan, for reference (ids then still carried the category):
- boot (2): 01 command line, 02 start-up console
- title (2): 03 demo 1 begins, 04 demo play
- menu (3 + 1): 05 main, 06 single player, 07 help/ordering, 29 escape menu in play
- gameplay (17): 08 start spawn, 09 Normal hall text, 10 slipgate, 11 hub arrival, 12 hub west, 13 shareware
  message, 14 E1 slipgate, 15 Loading (category gameplay; a load plaque), 16 E1M1 start, 17-19 three plain
  `env_` views of E1M1, 20 door opens on the Grunt, 23 corpse and backpack, 24 red button
- battle (6): 21 hit, 22 dead, 25 yard attack, 26 fire, 27 after the fight
- hud (1): 28 TAB overlay (Monsters 2/23, Secrets 0/6, Time, level name) with the status bar
- options (3): 30 options, 31 customize controls, 32 video modes
- save (2): 33 save menu, 34 "Saving game to C:/ID1/s0.sav... done."
For `main` later: the console (cheats `god`, `notarget`, `noclip`, `give`, `impulse 9`, `map e1m2` are
standard Quake console commands (source: general knowledge, untested here)), Nightmare hall, more
monsters per level (Knight, Ogre, Fiend, Shambler in later E1 maps), weapons, power-ups (Quad,
Pentagram, Ring, Biosuit), underwater, intermission screen after a level, death screen.

## Strategy and walkthrough notes
- Normal skill: the yard fight costs 12 health with the route as is; the first Grunt dies before it shoots.
- Aim by turning; the shotgun's spread hits at corridor range. A fight is 3-5 `ctrl:8,w30` groups; check
  ammo/health with `qstate.py` instead of looking.
- Enemies react to frame timing: changing a wait before a fight changes who shoots first. Keep the macros.
- E1M1 continues north from the yard toward the Nailgun room; read the map entities.
- **Dead ends (capture 2026-11-23, about 15 calls):** the yard after the fight (-62 1084 -200) is closed at
  x -80 and x 48; north of it a water channel (y ~1150-1310, swimming at z ~-297) ends at a wall: the far
  bank (floor -224, where the yard Grunt and Rottweiler stood at y 1520) is too high to climb out of the
  water (`space+up:60` against it does nothing). The way on is not across the channel from the yard
  surface; try swimming under water along it (`c` swims down) or another exit of the yard. The start hall
  has no way east at floor level (blocked at x 528 at y -230 and y 10, also with a jump).
- **Secrets near the start (map data):** the "Shoot this secret door..." panel (657-719, 49-63, z 49-111)
  has its trigger_secret just south of it (y 33-47) and shells (672 -40 48) behind it, so it is shot from
  the north, from a raised walkway east of the hall (shells 528 720 80, Hard Grunt 648 736 104); the Green
  Armor (688 480 80) is on that walkway too, next to a lift (func_plat 753-831, 481-543, height 400) that
  comes up from below and opens a secret door (737-751) as it passes. How to reach the walkway from the
  start hall was not found: probably from the lower level up that lift.

## Naming
Quake asks for no name in single player (the multiplayer setup has a player name, default "player").

## Shortcuts
| What | How (tokens / prefix / code) | Source | Status |
|---|---|---|---|
| Console | backquote, then type a command and `\n` (`type:map e1m2\n`) | CONFIG.CFG bind | console verified; `map`, `god`, `give`, `noclip`, `notarget`, `impulse 9` untested (fine for `main`, not for `start`) |
| Level select | console `map e1m1`...`e1m8` | source | not tried |
| Saves | `sav:01_start` + Single Player, Load, slot 1 | made here | verified (loads at -62 1084 -200, health 88) |
| Timedemo | console `timedemo demo1` (frame-rate test) | README | verified |

### Saves (rom/saves/quake/, never committed)
None downloaded: a save in the shareware is a short text file and is easier made here.

## RAM map (for `game.json` "ram" watches and pokes)
Floats; `play.py` watches show integers only, so the values are read with `qstate.py` (and listed in
`game.json` "ram" with `fmt hex` for reference).
| Address | Size | Meaning | How found |
|---|---|---|---|
| 371D48 | 90 x 4 | player entity fields (QuakeC `entvars_t`), with BOOT as above | hull pattern mins -16 -16 -24 / maxs 16 16 32 + view height 22 |
| 371D70 | 3 x 4 | origin x y z (field 10) | moves with walking (verified) |
| 371D94 | 3 x 4 | angles (pitch, yaw, roll; field 19) | turning (verified) |
| 371E08 | 4 | health (field 48) | 100 -> 88 when hit (verified) |
| 371E20 | 4 x 4 | shells, nails, rockets, cells (fields 54-57) | 25 -> 24 per shot (verified) |
| 371E30 | 4 | items bits (field 58; 4353 = shotgun + axe + ...) | read |
| 371E94 | 4 | armor value (field 83) | read 0 (not tested with armor) |
Same address in the start map and E1M1 (verified): the entity block is allocated at the same place for
every map. Pokes not tested (the start set needs none).

## Emulation notes
- **Model:** `svga-80000`. `timedemo demo1`: 14.1 fps at 40000 cycles, 28.4 fps at 80000 (comparable to a
  fast Pentium); emulation cost about 0.17 / 0.26 / 0.42 s per 100 frames at 40000 / 80000 / 150000 on this
  host. 80000 keeps play smooth and replays short (E1M1 save route ~3,700 frames, ~10 s). 320x200, no aspect
  decision needed.
- **Determinism:** two power-on replays of the same route give identical memory and frames (verified). A
  loaded state gives identical memory, and identical frames while no key is pressed, but the first key after a
  load leads to a different continuation than the flat run (verified with the menu state: `enter` after the
  load diverges; with sound on it diverges even without keys). The loaded continuation is itself
  reproducible (two loads, same keys, same result). Probably the DOSBox Pure keyboard/event timing (for
  example `doTick` in `Normal_Loop` or the input queue phase) is not part of the core's savestate; turn-based
  DOS games never noticed. Consequences and workarounds (Read first): flat checkpoint routes, warm cache
  before shooting, no undo before snapping. Reported to the coordinator as a platform issue.
- **Screens never settle** (animated torches, the demo, monsters): every shot line ends with `!` or accepts
  "NOT settled". `settle` costs 300 frames and moves the game on: avoid it in routes before keys.
- `-nosound` changes memory layout (entity address moved from 0x37A638 to 0x371D48).
- Level loads are fast (~35 frames); a key held during the load still acts in the new level.

## Checkpoints
| Name | Where |
|---|---|
| demo | attract demo 1 running |
| menu | main menu over the demo |
| s_startmap | start map spawn (544 288 28), facing the Normal hall |
| s_hub | episode hub arrival (544 1605 24), Normal skill |
| s_e1m1 | E1M1 spawn (480 -352 88) |
| s_e1m1_door | door open, first Grunt in view (298 570 24) |
| s_e1m1_lift | Grunt dead, rode the lift down (-47 570 -208) |
| s_e1m1_yard | yard, Grunt and Rottweiler attacking (-62 1072 -200, health 88) |
| s_e1m1_clear | after the yard fight (20 shells) |
| s_e1m1_saved | saved to slot 1 (S0.SAV), the end of the `start` set |

## Sources
| Source | URL | Used for | Accessed |
|---|---|---|---|
| id Software README.TXT, READV106.TXT, HELP.TXT, CONFIG.CFG (in the ZIP) | `rom/quake.zip` | system needs, switches (-nocdaudio, -nosound), binds, version changes | 2026-11-23 |
| Map entity data in ID1/PAK0.PAK | `rom/quake.zip` | start map and E1M1 layout, skill flags, secrets, exits | 2026-11-23 |
| Wikipedia, Quake (video game) | https://en.wikipedia.org/wiki/Quake_(video_game) | release date, publisher, episode name | 2026-11-23 |
| The Cutting Room Floor | https://tcrf.net/Quake | - | 403, unavailable |
| StrategyWiki E1M1 | https://strategywiki.org/wiki/Quake/E1M1:_The_Slipgate_Complex | - | 403, unavailable |

## Open questions
- First weapon pickup (Nailgun, E1M1 112 2352 16) and the first secret are not routed (dead ends in
  "Strategy"); the start set ends with the save after the yard fight.
- Did the yard fight kill the Rottweiler? TAB shows 2 of 23 monsters killed after it (Grunt 1 + one more);
  the dog is never clearly in frame in the start shots, a corpse lies north-west of the player (c7 look-around).
- Console cheats untested; quicksave (F6) and F3 untested.
- Platform: fix the state-load/key timing difference in the core patch (then `@parent` chains would work).
