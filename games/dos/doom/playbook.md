# Doom (DOS, registered 1.1) - playbook

Everything an agent needs to play this game efficiently: read it before playing, add to it after every run.
Status of each fact: **verified** (seen in the emulator, with the route) or **source** (manual/FAQ/wiki, not yet
checked). Never delete a fact that turned out wrong: strike it and say what is true.

## Read first
- **Start:** `rom/doom.zip` (vault; folder `DOOM/`), model `svga-40000`. Boot = DOSBox Pure "Go to Command
  Line" (7th entry: `down*6`), `cd doom`, `doom -nosound` (macro `BOOT`; start-up text "DOOM Operating System
  v1.1", "commercial version"). Frames 320x200 (the start-up text is text mode). No DEFAULT.CFG: built-in defaults.
- **Macros:** `TITLE` (BOOT+90), `MENU`, `NEWGAME` (Episode 1, Hurt me plenty, E1M1, **default reduced view**),
  `BIGVIEW` (`=` once: full-width view over the status bar, the size of 1.9's default and of the sets),
  `LEVEL:E:M` (= `WARP`: `doom -nosound -skill 3 -episode E`, then `idclevEM` and `=`; any map E1M1-E3M9,
  pistol start), `ARMS` (iddqd + idkfa, armor 143, ammo 137/38/212/27, wait 300), `GOD`, `IDKFA`,
  `SAVE1:NAME`, `TP:...` (from `tools/dstate.py --tp`). Honest E1M1: `NEWGAME,BIGVIEW,E1DOOR,E1FIGHT1,
  E1ZIGZAG,E1ARMOR,E1EXIT,E1TALLY` (new key holds made by `tools/dnav.py`: 1.9's route does not fit 1.1's E1M1).
- **Checkpoints (17, all flat):** `title`, `menu`, `s_e1m1` (reduced view), `s_e1m1_view`, `s_e1m1_door`,
  `s_e1m1_fight1`, `s_e1m1_zigzag`, `s_e1m1_armor`, `s_e1m1_exit` (tally), `s_e1m2`, `s_saved` (save
  `saves/01_start.sav`), `m_e1m1`, `m_e1m8`, `m_e2m1`, `m_e2m8`, `m_e3m1`, `m_e3m8`.
- **Determinism:** cachecheck: frames and memory agree for all 17 (cold == hit); 16 report "DIFFERS (save)"
  only because 1.1 creates an empty folder `C:\DOOMDATA` at every start and a state does not carry an empty
  folder (s_saved, with a file in it, is "same"). Shots on any checkpoint reproduce.
- **Plans:** `shots.txt`: `main` 28 active lines (menus, Read This!, help, automap, five powers, cheats, env
  starts; previewed) + a comment list of what remains (weapons, monsters, bosses, end texts, face stages,
  death); `start` 31 `#start ` lines (power-on to "game saved." at E1M2, previewed in full).
- **Tools** (`tools/`, copied from ultimate-doom and changed for 1.1): `wadmap.py` (reads `DOOM/DOOM.WAD`
  from `rom/doom.zip`), `dstate.py` (1.1 player_t offsets, map at 20BAC0), `dnav.py` (mobjs searched at
  every byte alignment, mobjinfo records 88 bytes, monsters named by editor number), `bosskill.py` (1.1
  cells/weapon addresses), `dplan.py`, `dpick.py` (unchanged). Usage lines as in ultimate-doom's playbook.
- **Keys:** arrows move/turn, `ctrl` fire, `space` use, `rshift` run, `alt+arrows` strafe, `1`-`7` weapons, `tab`
  automap, `esc` menu, `f1` order page then (Enter) help page, `equals`/`minus` view size. `w30` = wait.
- **Traps:** `-warp E M` does nothing without `-devparm` in 1.1 (and `-devparm` is not wanted in shots): use
  `LEVEL`. `-skill N` alone starts E1M1 at once (autostart). Every 1.1 address differs from 1.9 (player_t at
  20B558 and byte-packed: conversion in RAM map); never copy a 1.9 `poke`/`set`/`TP` line. Menu presses after
  ~BOOT+300 land in the title-to-demo wipe: use short presses (`TITLE,esc:4,w6,...`) for deep menu shots.
  The help key F1 first shows the order page. Saves go to `C:\DOOMDATA\`, not the game folder.
- **Open:** every action line of `main` (weapons, monsters, bosses, end texts E1-E3, death, face stages);
  sound on not tried; `menu_skill_*` skull rows to be read on the capture sheet.

## Differences from The Ultimate Doom 1.9
| Area | 1.1 (this game) | Ultimate Doom 1.9 | Status |
|---|---|---|---|
| Start-up | "DOOM Operating System v1.1", "commercial version", heap 0xd9b000 | "The Ultimate DOOM Startup v1.9" | verified |
| Boot | ZIP folder `DOOM/`: `cd doom` first; menu entry 7 is the command line | entry 10 | verified |
| Parameters | `-nosound`, `-nosfx`, `-nomusic`, `-skill`, `-episode`, `-timedemo`, `-playdemo`, `-record`, `-devparm`, `-file`, `-wart`, `-loadgame`, `-config`, `-deathmatch`; **`-warp` needs `-devparm`** | `-warp E M` alone | verified (EXE strings; warp tried with and without) |
| Level start | `LEVEL:E:M` = `-skill 3 -episode E` + `idclevEM` (same frame as `-devparm -warp`) | `-warp` | verified |
| View | default reduced window with a border; `=` once gives 1.9's full-width view | full width by default | verified |
| Episodes | three (no Thy Flesh Consumed); 27 maps | four, 36 maps | verified |
| Skills | four: no Nightmare! | five | verified |
| Maps | E1M1 differs (452 lines, 2 secrets, "blue armor" thing called MegaArmor), also E1M4, E1M5, E1M8, E2M2, E2M4-E2M7, E3M6 map data; E2M3, E3M2, E3M5 identical; things in E3M3 differ | | verified (lump compare) |
| F1 | order page ("To order DOOM: call 1-800-IDGAMES, $40.00") first, Enter: help page; Read This! menu shows the same two | help pages | verified |
| Intermission | Hangar tally with Time and Par (:30) | same | verified |
| Saves | `C:\DOOMDATA\DOOMSAV0.DSG` .. `5` (folder made at every start) | `DOOMSAVn.DSG` in the game folder | verified slot 0 |
| Cheats | iddqd, idkfa, idbehold(v s i r a l), iddt, idspispopd, idchoppers, idmypos, idclev all work; idclip does nothing | same (idclip is Doom II) | verified |
| RAM | player_t 20B558, byte-packed, health +42, weaponowned[8]; mobjinfo 88 bytes; mobjs at any byte address | 22B24C, health +32, aligned | verified |
| Speed | `-timedemo demo1`: 1077 gametics; 20000 cycles 26 fps, 40000 49 fps, 60000 69 fps | 37 fps at 40000 (demo of 1710 tics) | verified |

## Identity
| Field | Value |
|---|---|
| Title (EN / original) | Doom (registered version 1.1; in-game "DOOM") |
| Platform / model used | MS-DOS, `svga-40000` (see `game.json`) |
| Release (region, year) | North America; v1.1 dated 10 December 1993 (files in the ZIP); Doom first released 10 December 1993 (source: Wikipedia) |
| Developer / publisher | id Software / id Software |
| Genre | first-person shooter, real-time 2.5D |
| Players / save system | 1 player here; save anywhere, 6 named slots (verified slot 0) |

Dump: built from the owner's original install disks (`game.json` "source"), DOOM.WAD md5 981b03e6... = registered 1.1.

## Boot sequence
- Vault probe: `w120,enter` runs DOOM\DOOM.EXE from the start menu (title, then the demo in a reduced window).
- `BOOT` = `w120,down*6,enter,w120,type:cd doom\n,w30,type:doom -nosound\n` (verified). Start-up text, title
  from about +60 to +300, then the melt wipe into the attract demo (verified: +300 title, +400 demo).
- `TITLE` = `BOOT,w90`; `MENU` = `TITLE,esc,w20`; `NEWGAME` = `MENU,enter,w20,enter,w20,enter,w120`
  (verified: E1M1 at 1056 -3616 facing north, 6 monsters = Hurt me plenty).
- `WARP:E:M` / `LEVEL:E:M` = `...type:doom -nosound -skill 3 -episode E\n,w300,type:idclevEM,w20,equals,w280`
  (verified E1M1, E1M7, E1M8, E2M2, E2M3, E2M8, E3M1, E3M3, E3M5, E3M8).

## Controls
Keys are the built-in defaults (no DEFAULT.CFG in the ZIP); the help page lists them (verified on screen).
| Context | Key | Action | Status |
|---|---|---|---|
| Play | up / down | forward / back | verified (dnav routes) |
| | left / right | turn | verified (1.9's turn table holds: dnav turns land within 2 degrees) |
| | rshift + arrow | run | source (help page "Shift + arrow"; key_speed default right Shift) |
| | alt + left/right | strafe | source (help page) |
| | ctrl | fire | verified |
| | space | use: doors, switches | verified (door 1536 -2496, exit switch) |
| | 1-7 | weapons | source (help page; 1 = fist/chainsaw) |
| | tab | automap | verified |
| | = / - | view size | verified (= once: full-width view) |
| | esc | main menu | verified |
| | F1 | order page, Enter: help page | verified |
| | F2-F11 | save, load, volume, detail, quicksave, end game, messages, quickload, quit, gamma | source (help page) |
| Menus | up / down, enter, esc | move, choose, back | verified |
| Save name | letters, enter | type the slot name | verified (`type:ryz`) |
| Intermission | space | skip the count / continue | verified (E1TALLY) |

Input timing: default press (hold 8, wait 40) works in menus and play; nothing lost.

## Game structure
- Three episodes of 8 maps + secret map 9 (E1-E3, `wadmap.py list`). Bosses: two Barons of Hell in E1M8,
  Cyberdemon E2M8, Spider Mastermind E3M8 (same map data as 1.9 except E1M8: re-check positions with wadmap).
- Main menu: New Game, Options, Load Game, Save Game, Read This!, Quit Game (verified). Options: End Game,
  Messages, Graphic Detail, Screen Size, Mouse Sensitivity, Sound Volume (verified). Save Game outside a game:
  "You can't save if you aren't playing! press a key." (verified). Load Game: six slots (verified).
- Level end: exit switch -> tally (Kills, Items, Secret, Time, Par) -> "Entering <next map>" -> next map;
  health, armor, ammo carry over (verified E1M1 -> E1M2).
- E1M1 on Hurt me plenty (1.1 WAD): zombiemen 2272 -2432, 2272 -2352, 2912 -2816, 3056 -3584; imps 3440 -3472
  (ledge), 3008 -4416; blue armor (MegaArmor) 1824 -3280 in the nukage pool; shotgun 3264 -3936 in secret
  sector 27; green armor -224 -3232; exit switch 2912 -4768; 2 secrets.

## Shot plan
See `shots.txt`. `start` (31, previewed): boot 1, title 1, menus 3, gameplay 13 (melt, reduced and full view,
start room, door, zigzag room, MegaArmor, exit switch, tally counting and done, E1M2), battle 6 (third
zombieman, hit flash, nukage zombieman, ledge imp, imp fireball, imp hit), map 2 (automap, Entering Nuclear
Plant), options 2, help 2 (order page, keys), save 3. `main` (28 previewed): title, menus 7 (main, episode,
skill x4), Read This! 2, quit, load, save refused, help, automap 2, powers 5, cheats 2, env 6. To plan: see the
comment block in `shots.txt` (weapons x8, monsters, bosses, three end texts, face stages, death, pickups).

## Strategy and walkthrough notes
- The ultimate-doom recipes (playbook "Strategy") apply, with 1.1 addresses: E1M8 barons (re-check: E1M8's
  map data differs), E2M8/E3M8 boss kills with `tools/bosskill.py` (BFG, `set:` cells at 20B602), face stages
  in E1M3 without god (1.1 E1M3 differs only in LINEDEFS), E3M3 corridor for weapons (things differ in 1.1:
  check with `wadmap.py E3M3`).
- E1M1 honest route (dnav goals, 2026-11-25): `path 1536 -2530; face 1536 -2490; use` | `wait 30; fight 14 800;
  path 2536 -2664; fight 8 900; path 2808 -2808; fight 8 900` | `path 3050 -3600; fight 6 600; fight 10 600` |
  `path 3264 -3900` (no path: the shotgun secret is not taken) `; pathhurt 1824 -3280` | `pathhurt 2072 -3800;
  path 2304 -4032; path 3008 -4080; fight 10 700; path 2880 -4416; path 3008 -4600; path 2950 -4768; face 2900
  -4768; use; wait 120`. Ends with kills 6/6, health 100, armor 190.
- dnav: `fight` without line of sight wastes bullets (the planner does not check sight); the path planner
  finds no way out of the nukage pool: use `pathhurt` for the first leg.

## Naming
Only the save slot name: `ryz`.

## Shortcuts
| What | How | Source | Status |
|---|---|---|---|
| Level select | `LEVEL:E:M` (`-skill 3 -episode E`, `idclevEM`) | EXE strings, tried | verified |
| `-devparm -warp E M` | works, but devparm mode | tried | verified (not used) |
| iddqd | "Degreelessness Mode On" | cheat | verified |
| idkfa | "Very Happy Ammo Added": weapons, 200 bullets, 200% armor, six keys | cheat | verified |
| idclevEM | change level (pistol start) | cheat | verified (idclev23, 35, 39, 17) |
| idbehold / v s i r a l | prompt "inVuln, Str, Inviso, Rad, Allmap, or Lite-amp"; "Power-up Toggled" | cheat | verified (prompt, v, s, i, r, a, l) |
| iddt | automap: map, then things | cheat | verified |
| idspispopd | "No Clipping Mode ON" | cheat | verified |
| idchoppers | chainsaw, "... doesn't suck - GM" | cheat | verified |
| idmypos | angle and x,y in hex | cheat | verified |
| idclip | nothing (Doom II) | cheat | verified |
| Save | `sav:01_start` + `TITLE,esc,w20,down*2,w10,enter,w30,enter,w100` (load slot 1) | made here | verified (E1M2, hp 100, armor 190) |
| Timedemo | `doom -nosound -timedemo demo1`: "timed 1077 gametics in N realtics" | id | verified |

### Saves (rom/saves/doom/, never committed)
None downloaded.

## RAM map (for `game.json` "ram" watches and pokes)
Physical addresses with `svga-40000` and `BOOT`. 1.1's structs are byte-packed and differ from the released
source (`tools/dstate.py` docstring).
| Address | Size | Meaning | How found |
|---|---|---|---|
| 20B558 | 4 | players[0].mo (pointer to the player's mobj; route-dependent) | only pointer to the mobj at 1056 -3616 (verified) |
| 20B582 | 4 | health | 100 -> 94 when shot (verified) |
| 20B586 / 20B58A | 4 / 4 | armor points / type | blue armor 196/2 (verified); ARMS sets 143 (verified) |
| 20B58E | 6 x 4 | powers (invuln, berserk, invis, radsuit, map, liteamp) | layout (inferred) |
| 20B5A6 | 6 x 4 | cards | idkfa sets all six (verified) |
| 20B5D2 | 4 | readyweapon (0 fist .. 7 chainsaw) | 1 pistol (verified) |
| 20B5D6 | 4 | pendingweapon (9 = none: 8 weapons) | verified at start |
| 20B5DA | 8 x 4 | weaponowned | fist, pistol 1 (verified) |
| 20B5FA | 4 x 4 | ammo: bullets, shells, cells, rockets | verified (route, ARMS) |
| 20B60A | 4 x 4 | maxammo 200 50 300 50 | verified |
| 20B62A / 20B62E / 20B632 | 4 each | kills / items / secrets | kills 6, secrets 1 on E1M1 (verified) |
| 20BAD4 / 20BAC0 | 4 / 4 | gameepisode / gamemap (follow idclev and the exit) | verified (E1M2 after the tally) |
| 20B9EC / 20B9E0 | 4 / 4 | follow idclev, not the exit (start values) | verified |
| mobj +12/+16/+20, +32, +56/+60, +88, +92, +108 | | x, y, z, angle, floorz/ceilingz, type, info, health | verified (position, type 0, health 100) |
| mobjinfo | 88 bytes each | 1.1 types: 0 player, 1 imp, 2 zombieman, 3 shotgun guy, 4 demon, 5 spectre, 6 cacodemon, 7 lost soul, 8 baron, 9 spider, 10 cyberdemon (editor numbers in the table) | verified (table read) |
Converting a 1.9 address A in player_t (22B24C + o): 1.1 = 20B558 + o + 10 for o < 152, + 6 for o >= 156
(the ninth weapon slot is gone).

## Emulation notes
- **Model:** `svga-40000` (49 fps in the timedemo, above the 35 tic cap). 70 frames = 1 s = 35 tics.
- `-nosound` for determinism (as Quake/1.9); sound on not tried. `-nosfx`/`-nomusic` exist too.
- Determinism: same as 1.9 for frames and memory; cachecheck's "save" difference is the empty `C:\DOOMDATA`
  folder (Read first). `@checkpoint` routes are fine.
- Pickup messages last ~280 frames; `LEVEL` waits 280 after `idclev` so its "Changing level" message is gone.

## Checkpoints
See Read first; `s_*` = the `start` chain (honest), `m_*` = `LEVEL` starts for `main`.

## Sources
| Source | URL | Used for | Accessed |
|---|---|---|---|
| The game: DOOM.EXE strings, start-up text, menus, F1 pages | `rom/doom.zip` | parameters, version, keys, cheats | 2026-11-25 |
| DOOM.WAD map lumps, compared with Ultimate Doom 1.9's | `rom/doom.zip`, `rom/ultimate-doom.zip` | map differences, things | 2026-11-25 |
| ultimate-doom playbook and tools | `games/dos/ultimate-doom/` | macros, recipes, layout to start from | 2026-11-25 |
| id Software's released source (knowledge, not fetched) | - | player_t/mobj_t field order | 2026-11-25 |

## Open questions
- Skill menu: which entry the skull rests on after `up`/`down` in `menu_skill_*` lines (read on the sheet).
- E1M8 baron recipe on 1.1's E1M8 (map data differs); E3M3 weapon spot (things differ).
- End texts and end pictures of E1-E3 in 1.1 vs 1.9 (not reached yet).
- Sound on: drift after a state load? Not tried.
