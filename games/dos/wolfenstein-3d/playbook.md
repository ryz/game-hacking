# Wolfenstein 3D (DOS) - playbook

Everything an agent needs to play this game efficiently: read it before playing, add to it after every run.
Status of each fact: **verified** (seen in the emulator, with the route) or **source** (manual/FAQ/wiki, not yet
checked). Never delete a fact that turned out wrong: strike it and say what is true.

## Read first
- **Start:** `rom/wolfenstein-3d.zip` (vault), model `svga-15000` (the bundle's `start.bat` runs it at
  `cycles fixed 15000`). Boot = DOSBox Pure "Go to Command Line" (6th entry), then `wolf3d` (macro `BOOT`;
  `WOLF:ARGS` passes parameters). Frames are 320x200, no aspect decision. Sound devices are left on (AdLib,
  Sound Blaster, Sound Source detected; `BOOTQ` = `noal nosb noss nopro`, not needed).
- **Movement keys are W/A/S/D, not the arrows** (the bundled CONFIG.WL6 binds them): `w:N` walks forward N
  frames (0.08 tile per frame), `s:N` back, `a:N` / `d:N` turn left / right (1.75 degrees per frame: `a:51` =
  89 degrees, `a:52` = 91; exactly 90 is not reachable, long corridors drift: correct with `a:1`/`d:1`).
  `ctrl:6` fires once, `space` opens doors and pushwalls (from within about 1.4 tiles), `1`-`4` = knife, pistol,
  machine gun, chain gun, `alt` strafe, `shift` run, `esc` Options menu. Note `w30` is a wait, `w:30` the W key.
- **Macros:** `TITLE`, `MENU`, `NEWGAME` (Episode 1, "Bring 'em on!", E1M1 first control), the E1M1 route
  `E1HALL,E1GUARD,E1NORTH,E1GUARD2,E1GUARD3,E1PUSH,E1SECRET`, `SAVE1:NAME` (save to slot 1, back to the game).
  For `main`: `LEVEL:N` (map index N = (episode-1)*10 + floor-1, skill 2, debug keys on, straight into the
  level), `GOD` (Tab+G), `MLI` (cheat: health 100, ammo 99, both keys, chain gun), `TP:X:Y:A` (teleport; get the
  hex from `python3 games/dos/wolfenstein-3d/tools/wlmap.py --tp 51.5 44.5 0`), `DNEW:TOKS` (new game through
  the menus with debug keys on; TOKS = episode cursor, `w1` for Episode 1, `down*2` for Episode 3).
- **Checkpoints** (all flat, `checkpoints.txt`): `title`, `menu`, `s_e1m1`, `s_hall`, `s_guard1`,
  `s_corridor`, `s_guard2`, `s_guard3`, `s_pushwall`, `s_mg`, `s_saved` (save 01_start).
- **Determinism (trap):** a flat route from power-on is reproducible (same frames twice; with and without sound).
  A loaded state (cached checkpoint) continues with the same frame and player position, but the guards' memory
  differs from the flat run within 60 frames (`cachecheck`: "cold/hit DIFFERS from flat (memory)" for every
  in-game checkpoint after `s_e1m1`). So: **`start` shot routes are flat macro chains (no `@`)**, as in
  `shots.txt`; `main` lines also start from macros (`LEVEL:`, `NEWGAME`), never from `@s_...`.
- **Maps:** `python3 games/dos/wolfenstein-3d/tools/wlmap.py list` (all 60 floors), `wlmap.py E1M1 --skill 2`
  (ASCII map + objects: enemies by skill, keys, treasure, weapons, pushwalls, start). Coordinates = tiles,
  same as the RAM position (x east, y south).
- **Shortcuts verified:** `wolf3d tedlevel N` (start map N directly; skill 1 unless `baby|easy|normal|hard`;
  ending the level quits to DOS), `nowait` (skips sign-on and title: Options menu at once), `goobers` +
  Left Shift+Alt+Backspace in play = "Debugging keys are now available!", then Tab+G god, Tab+W warp (type the
  floor number, Enter), Tab+I free items (score 100000, lives 5: unrealistic, prefer pokes), Tab+F coordinates,
  Tab+E end the floor (tally; under `tedlevel` it quits to DOS). MLI (hold M+L+I) needs no debug mode.
- **Plans:** `shots.txt` holds the `main` plan (active lines) and the `start` plan (`#start ` lines, 28 shots,
  all previewed). Open: other enemy close-ups (mutant), bosses 2-6, keys/locked doors, elevator, treasure,
  death and game over, env views per episode.
- **No "Read This!"** in this build (GT/Activision 1.4): the help screens are not reachable from the menu.

## Identity
| Field | Value |
|---|---|
| Title (EN / original) | Wolfenstein 3D |
| Platform / model used | MS-DOS, `svga-15000` (see `game.json`) |
| Release (region, year) | North America; original 1992 (Apogee); this is the 1.4 build re-released by Activision (sign-on shows the Activision logo, verified) |
| Developer / publisher | id Software / Apogee (1992), later GT Interactive and Activision (source: sign-on, Wikipedia knowledge) |
| Genre | first-person shooter, real-time, grid-based levels |
| Players / save system | 1 player; save anywhere, 10 slots (`SAVEGAM0.WL6` ... `SAVEGAM9.WL6`), named by the player (verified) |

Version evidence (verified 2026-11-25): Activision logo on the sign-on; the program's strings (read from memory
after load, the EXE is compressed) have the `goobers` debug parameter, the Gravis GamePad option of 1.4 and no
"Read This!" menu entry (the GT/Activision builds dropped it); `*.WL6` data with six episodes. Bundle extras:
`launcher/` (a graphical launcher, not used), `m1/` Spear of Destiny (registered separately as
`dos/spear-of-destiny`).

## Boot sequence
- `BOOT` = `w120,down*5,enter,w120,type:wolf3d\n`: sign-on (id logo, Activision, memory bars, detected
  devices, "Press a key") at +200 frames. Any key: PC-13 rating screen, then the title picture (~600 frames).
- Attract loop from `TITLE` (= `BOOT,w200,space,w700`): title until about +1000, id credits at +1100,
  High Scores at +1300+600 (`TITLE,w1300,w150*4,!`), then the demo (floor 38 shown on the status bar) at
  about +2600. Any key in the loop opens the Options menu (`MENU` = `TITLE,space,w120`).
- `NEWGAME` = `MENU,enter,w120,enter,w120,enter,w400`: New Game, Episode 1, "Bring 'em on!" (the default
  cursor), Get Psyched, E1M1 at (29.5,57.5) facing east.

## Controls
| Context | Key | Action | Status |
|---|---|---|---|
| Sign-on, title, attract | any key | sign-on: continue; attract: Options menu | verified |
| Menus | up/down, enter, esc | move, select, back (esc in the in-game Options menu asks "Dost thou wish to leave..." = quit) | verified |
| Play | W / S | forward / back (W/A/S/D from the bundled CONFIG.WL6; arrows do nothing) | verified |
| | A / D | turn left / right | verified |
| | Ctrl | fire | verified |
| | Space | open door, push a pushwall, flip the elevator switch | verified (door, pushwall) |
| | 1 2 3 4 | knife, pistol, machine gun, chain gun | verified (1, 3, 4; 2 = pistol) |
| | Alt + A/D | strafe | source (CONFIG binds Alt as strafe) |
| | Shift | run | source (CONFIG binds Left Shift); `shift+w:24` was blocked by a door in the test |
| | Esc | Options menu (Save Game, End Game, Back to Game) | verified |
| | M+L+I held | cheat: 100% health, 99 ammo, both keys, all weapons, score 0 | verified |
| Debug (needs `goobers`) | LShift+Alt+Backspace | enable debug keys | verified |
| | Tab+G / W / I / F / E | god / warp / free items / coordinates / end floor | verified |

Input timing: default press (hold 8, wait 40) works in menus. In play everything is a hold (`KEY:N`).
The game polls held keys at 70 Hz; a hold of N frames moves N tics.

## Game structure
Six episodes of nine floors plus a secret floor each (`wlmap.py list`): floor 9 is the boss floor
(E1 Hans Grosse, E2 Dr. Schabbs, E3 Hitler, E4 Otto Giftmacher, E5 Gretel Grosse, E6 General Fettgesicht;
verified from the map data). Each floor ends at an elevator switch (wall tile 21), then a tally (bonus, time,
par, kill/secret/treasure ratios, verified). Score extra life every 40000 (gamestate nextextra = 40000,
verified in RAM).

## Shot plan
See `shots.txt` (two plans). `start`: 28 lines, previewed. `main`: 20 previewed lines (boot, title, menus,
four weapons, dogs, SS, officer, Hans Grosse, tally, cheats, debug screens) plus a todo list.
Reach: `LEVEL:N` + `TP:` for any enemy or room; bosses from `LEVEL:8/18/28/38/48/58` (map index).

## Strategy and walkthrough notes
- E1M1 honest route (macros): door east, north corridor, two doors into the grey hall (first guard, 4 pistol
  shots), north door into the wood corridor (second guard, 3 shots), west at y=22.5: third guard (1 shot,
  ammo runs out, his clip is taken), Space on the eagle picture at (30,22): pushwall slides 2 tiles (wait 260
  frames before walking), room with 2 clips, 2 first aid kits (not taken at 100%) and the machine gun.
- Guards' damage is random: the route stays at health 100 in the flat replay (it read 59 after an extra 60
  frames at `s_guard2`: the third guard shoots if you wait).
- Bosses: `GOD` first; under god a hit still flashes the screen red (pick frames between hits).

## Naming
Save slots take a typed name: `SAVE1:E1M1 machine gun`. High-score name entry: type `ryz`.

## Shortcuts
| What | How | Status |
|---|---|---|
| Start any floor | `wolf3d tedlevel N [normal] [nowait]` (macro `LEVEL:N`) | verified (N=0, 1, 8, 10, 12, 40) |
| Skip intro | `nowait` | verified |
| Debug keys | `goobers` + LShift+Alt+Backspace | verified |
| God / warp / items / coords / end floor | Tab+G / Tab+W / Tab+I / Tab+F / Tab+E | verified |
| Cheat | M+L+I | verified |
| Teleport | `TP:` from `wlmap.py --tp` | verified (E1M1 dogs, E1M2 SS, E5M1 officer) |
| Save | `games/dos/wolfenstein-3d/saves/01_start.sav` (`sav:01_start`, Load Game slot 1) | verified |

## RAM map (for `game.json` "ram" watches and pokes)
Same addresses every boot with `BOOT` (DOS loads the game at the same place); with `BOOTQ` not checked.
| Address | Size | What | Status |
|---|---|---|---|
| 44912 | 2 | difficulty (0-3) | verified |
| 44914 | 2 | map on (floor - 1) | verified |
| 4491A | 4 | score | verified |
| 4491E | 4 | next extra life score (40000) | verified |
| 44922 | 2 | lives | verified |
| 44924 | 2 | health (poke shows on the HUD only when it changes) | verified |
| 44926 | 2 | ammo | verified |
| 44928 | 2 | keys (bits) | source (gamestate layout) |
| 4492A / 4492C / 4492E | 2 each | best weapon / weapon / chosen weapon (0 knife .. 3 chain gun) | verified (1 -> 2 at the machine gun) |
| 44938 | 2 | episode (0-5) | inferred |
| 4493A / 4493C / 4493E | 2 each | secrets / treasures / kills found | verified (secret 1, kills 3) |
| 44940 / 44942 / 44944 | 2 each | totals (E1M1 skill 2: 5 / 23 / 20) | verified |
| 44946 | 4 | play time in tics (70 per second) | verified |
| 4687C / 46880 | 4 each | player x / y, 16.16 fixed tiles | verified |
| 46884 / 46886 | 2 each | player tile x / y | verified |
| 46896 | 2 | player angle, degrees, 0 east, 90 north | verified |
| 48xxx | | other actors (guards); they differ after a state load | verified |

## Emulation notes
- Model `svga-15000` as in the bundle. Sound devices on; determinism was the same without them.
- A flat route is reproducible; a cached state + keys reproduces itself (preview twice the same) but not the
  flat run's actor memory: see Read first.
- Pushwalls take about 256 frames to slide; doors about 60 frames to open and close again after ~5 s.
- Do not snap the DOS command line or DOSBox banner (front end).

## Checkpoints
`checkpoints.txt`: `title`, `menu`, `s_e1m1` reproduce exactly (`cachecheck` "same"); the eight later `s_*`
reach the same frame and position but differ in actor memory from the flat replay (see Determinism).

## Sources
| Source | What | Date |
|---|---|---|
| The program itself (strings in memory, CONFIG.WL6, GAMEMAPS.WL6) | parameters, debug strings, menus, key bindings, maps | 2026-11-25 |
| id Software's released Wolfenstein 3D source (knowledge, not fetched) | gamestate/object layout, map format, cheat and debug key handling | 2026-11-25 |
| tcrf.net/Wolfenstein_3D_(DOS) | unavailable (HTTP 403 to automated access) | 2026-11-25 |

## Open questions
- Exact retail identity of the EXE (Activision 1.4 by the sign-on; the EXE size 108779 not matched to a list).
- Shift (run) and Alt (strafe) not tested in a free corridor.
- Mutant close-up position (E2M1), bosses 2-6, elevator, locked doors, treasure pickup, death/game over,
  high-score entry, episode end text: not routed yet.
- Why a state load changes the actors' memory (timer phase?): a backend question for `docs/backlog.md`.
