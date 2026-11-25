# Spear of Destiny (DOS) - playbook

Everything an agent needs to play this game efficiently: read it before playing, add to it after every run.
Status of each fact: **verified** (seen in the emulator, with the route) or **source** (manual/FAQ/wiki, not yet
checked). Never delete a fact that turned out wrong: strike it and say what is true.

## Read first
- **Start:** `rom/spear-of-destiny.zip` (vault; the same ZIP as `dos/wolfenstein-3d`, Spear is in `m1/`), model
  `svga-15000` (the bundle's `start.bat` runs `spear.exe` at `cycles fixed 15000`). Boot = DOSBox Pure "Go to
  Command Line" (6th entry), `cd m1`, `spear` (macro `BOOT`; `SOD:ARGS` passes parameters). Frames 320x200.
  Sound devices left on. **No copy-protection quiz** in this build (its strings are in the program, it never
  appeared on the verified path).
- **Same engine as Wolfenstein 3D**, read `games/dos/wolfenstein-3d/playbook.md` "Read first" for movement:
  **W/A/S/D** (CONFIG.SOD is byte-identical to CONFIG.WL6), `w:N` walks 0.084 tile per frame, `shift+w:N` twice
  as far, `a:51`/`d:51` turn about 89 degrees, `alt+d:N` strafes right, `ctrl:6` fires once, `space` opens doors,
  pushwalls and the elevator switch, `1`-`4` weapons, `esc` Options. `w30` = wait, `w:30` = W key.
- **Differences from Wolfenstein:** debug parameter is **`debugmode`** (not `goobers`); `tedlevel N` takes
  the map index N = floor - 1 (0-20, no episodes); no episode menu (`NEWGAME` = MENU, Enter, Enter on "Bring
  'em on!"); sign-on needs no key (title at BOOT+850, id credits at BOOT+2050); the warp prompt asks "(1-21)";
  floor 21 shows **"18"** on the status bar; RAM is 0xB40 higher (gamestate at 45452, player at 475B2).
- **Macros:** `TITLE`, `MENU`, `NEWGAME`; honest floor 1 route `F1AMMO,F1DOOR,F1GUARD1,F1GUARD2,F1GUARD3,F1TDOOR,
  F1TREASURE`, `SAVE1:NAME`. For `main`: `LEVEL:N` (tedlevel N, normal, debug keys on, straight into floor N+1),
  `DNEW` (new game through the menu with debug keys on: Tab+E there gives a real tally and goes on), `GOD`
  (Tab+G), `MLI` (cheat: health 100, ammo 99, both keys, chain gun), `TP:X:Y:A` (teleport; hex from
  `python3 games/dos/spear-of-destiny/tools/sodmap.py --tp 31.5 36.5 90`, last line).
- **Checkpoints** (all flat): `title`, `menu`, `s_f1`, `s_ammo`, `s_door`, `s_guard1`, `s_guard2`, `s_guard3`,
  `s_treasure_door`, `s_treasure`, `s_saved` (save `01_start`).
- **Determinism:** as Wolfenstein's (coordinator's note there): flat replay from power-on reproduces the
  session exactly (score/health at every checkpoint matched); `cachecheck` says "cold/hit DIFFERS from flat
  (memory)" for the in-game checkpoints (frames equal), but a cache miss and two hits of
  `@s_guard2,w:40,ctrl:6,w60,d:30,w60` gave identical frame, memory (45000-4AFFF) and score/health
  (checked 2026-11-25). Shot routes may start from `@s_...`; checkpoint routes stay flat.
- **Maps:** `python3 games/dos/spear-of-destiny/tools/sodmap.py list` (21 floors, bosses, Spear, secret exits),
  `sodmap.py 18 --skill 2` (ASCII map + objects; legend in wlmap.py plus `*` secret-elevator tile).
- **Bosses (verified in view, `shots.txt` main):** Trans Grosse floor 5 (6,31); Barnacle Wilhelm floor 10
  (19,44); Ubermutant floor 16 (24,32); Death Knight floor 18 (31,31); the Spear floor 18 (31,22) behind the gold
  door; Angel of Death floor 21 (38,14). Bosses ignore you until shot (`ctrl:12` wakes them).
- **Taking the Spear** (walk onto (31,22) on floor 18) moves straight to floor 21 at the same spot, facing a
  screaming-face wall (verified, under `tedlevel`).
- **Traps:** doors close again after a few seconds and `play.py`'s settle can let them shut; Space on an open
  door closes it; doorways need the player centred (x or y = n.5) or walking slides along the frame; a `do`
  that settles in a fight gives the enemy free shots (use `do!`).
- **Open:** killing the Angel of Death (120 short presses of `ctrl:10` with ammo frozen did not), the ending
  text, death/game over and high-score entry, the secret floors' entrances by play, LevelRatios over 20 floors
  and the victory totals screen. Nothing shot yet.

## Identity
| Field | Value |
|---|---|
| Title (EN / original) | Spear of Destiny |
| Platform / model used | MS-DOS, `svga-15000` (see `game.json`) |
| Release (region, year) | North America; 1992 (FormGen), this copy from the Activision Wolfenstein 3D bundle (`m1/Spear.exe`, 113418 bytes, compressed) |
| Developer / publisher | id Software / FormGen (title picture: "Copyright 1992 id Software, Inc.") |
| Genre | first-person shooter, real-time, grid-based floors |
| Players / save system | 1 player; save anywhere, 10 named slots (`M1/SAVEGAM0.SOD` ... ), verified |

Version evidence (verified 2026-11-25, strings read from memory after load): Gravis GamePad option (the 1.4
generation of the engine, as in the bundle's Wolfenstein 1.4), `debugmode`, `TEDLEVEL`, `NOWAIT`, the MLI
message ("Cheatmeister"), "Warp to which level(1-21):", and the copy-protection quiz texts ("You must like
these quizzes", "Nice try, but no Spear") although no quiz is shown: this is the later Spear build (1.4 by the
engine features); the sign-on shows no version number. Exact build not matched to a list (Open questions).

## Boot sequence
- `BOOT` = `w120,down*5,enter,w120,type:cd m1\n,w30,type:spear\n`: sign-on (Spear of Destiny banner, memory
  bars, mouse/joystick/AdLib/Sound Blaster/Sound Source) at +200, PC-13 screen at +400 without a key, title
  picture at +600 (`TITLE` = `BOOT,w900`), id credits at about +1800-2400 (BOOT+2050).
- `MENU` = `TITLE,space,w120`: Options (New Game, Sound, Control, Load Game, Change View, View Scores, Back to
  Demo, Quit). No Read This.
- `NEWGAME` = `MENU,settle,enter,w120,enter,w400,settle`: skill menu ("How tough are you?", cursor on "Bring
  'em on!"), Get Psyched!, floor 1 at (32.5,59.5) facing north.

## Controls
| Context | Key | Action | Status |
|---|---|---|---|
| Sign-on | none | runs on by itself to PC-13 and the title | verified |
| Title, attract | any key | Options menu | verified (space) |
| Menus | up/down, enter, esc | move, select, back | verified |
| Play | W / S | forward / back, 0.084 tile per frame | verified (w:20 = 1.68 tiles) |
| | A / D | turn left / right (~1.75 degrees per frame) | verified |
| | Shift + W | run (twice the speed) | verified (20 frames = 3.37 tiles) |
| | Alt + A / D | strafe | verified (alt+d:20 = 1.12 tiles right, angle kept) |
| | Ctrl | fire | verified |
| | Space | open/close door, pushwall | verified (doors, pushwall at (30,56)) |
| | 1 2 3 4 | knife, pistol, machine gun, chain gun | verified (after MLI) |
| | Esc | Options in play (Save Game, End Game, Back to Game) | verified |
| | M+L+I held | cheat: health 100, ammo 99, both keys, chain gun | verified |
| Debug (`spear debugmode`) | LShift+Alt+Backspace | "Debugging keys are now available!" | verified |
| | Tab+G / Tab+W / Tab+E | god mode / warp (1-21) / end floor (tally) | verified |
| | Tab+I / Tab+F | free items / coordinates | source (Wolfenstein engine, same code) |

Input timing: default press works in menus; in play everything is a hold `KEY:N`.

## Game structure
One mission, 21 floors (verified, `sodmap.py list`, map names): Tunnels 1-4, Tunnel Boss (5, Trans Grosse),
Dungeons 1-4, Dungeon Boss (10, Barnacle Wilhelm), Castle 1-5, Castle Boss (16, Ubermutant), Ramparts (17),
Death Knight (18, the Spear), Secret 1 (19), Secret 2 (20), Angel of Death (21). Secret elevator tiles on
floors 4 and 12 (`*` in sodmap: Use on the switch while standing on it). Floor 21 has the Angel and many
spectre (ghost) objects (map data; ghosts not seen yet). Regular enemies are Wolfenstein's: guard, SS,
officer, dog, mutant (codes identical). Spear-only items: 25-clip box, marble pillar, truck, the Spear.
Tally after each floor (verified): bonus, time, par, kill/secret/treasure ratios; extra life at 40000.

## Shot plan
`shots.txt` holds both plans with previewed routes. `start` (22 lines, honest, previewed together:
`work/preview/dos/spear-of-destiny/start.png`): sign-on, PC-13, title, menu, skill, Get Psyched, floor 1
start, pushwall secret, ammo room, three guard fights with the face going from 100% to 16%, treasure room,
in-game menu, save. Tune: `08_pushwall` (pick a mid-slide frame with `--timeline`), `18_treasure_taken` (faces
a wall: add a turn). `main` first part (27 lines, previewed): boot, title, credits, menus, floor 1, HUD,
env views (floors 4, 8, 11, 19, 20), four weapons firing on floor 6, all five bosses and the Spear, the Angel's
fireball, a tally, debug messages.
Still to plan for `main`: Spear-specific objects (25-clip box, truck, marble pillar), dogs/SS/officer/mutant
close-ups (sodmap `--objects` for spots), silver/gold key doors, elevator switch, secret elevator, death and
game over (`poke:45462=0000` lives 0, `poke:45464=0100` health 1, as in Wolfenstein), high-score name ryz, the
Angel killed, the ending text and victory totals, env views of floors 1-3, 6, 9, 13-17, 21.

## Strategy and walkthrough notes
- Floor 1 honest route (macros F1...): north 3 tiles, west, Space on the wall at (30,56): pushwall, 6 clips
  (ammo 56, secret 1); north door (32,52): guard 1 in the doorway (7 shots); vine hall: guard 2 comes close (health
  falls to 25); west door (24,47): guard 3 (health 16), his clip; south through the room to the door (19,53):
  treasure room, 8 crosses and chalices (score 2700). The guard in the room east of (21,51) kills you from 16%:
  the honest run saves in the treasure room instead.
- Bosses: GOD first; under god a hit still flashes the screen red.

## Naming
Save slot names are typed (`SAVE1:Floor 1 treasure`). High-score entry: type `ryz` (not tried).

## Shortcuts
| What | How | Status |
|---|---|---|
| Start any floor | `spear debugmode tedlevel N normal nowait` (macro `LEVEL:N`, N = floor - 1) | verified (0-20) |
| Debug keys | `debugmode` + LShift+Alt+Backspace | verified |
| God / warp / end floor | Tab+G / Tab+W / Tab+E | verified |
| Cheat | M+L+I | verified |
| Teleport | `TP:` from `sodmap.py --tp` | verified (all five bosses, the Spear) |
| Save | `games/dos/spear-of-destiny/saves/01_start.sav` (`sav:01_start`, Load Game slot 1) | verified (score 2700, health 16 restored) |

### Saves (rom/saves/spear-of-destiny/, never committed)
None downloaded (no web source used).

## RAM map (for `game.json` "ram" watches and pokes)
Gamestate is Wolfenstein's + 0xB40 (verified by the starting values and the watches in play).
| Address | Size | What | Status |
|---|---|---|---|
| 45452 | 2 | difficulty (0-3) | verified (2) |
| 45454 | 2 | map on = floor - 1 (0x14 on the Angel's floor) | verified |
| 4545A | 4 | score | verified |
| 4545E | 4 | next extra life (40000) | verified |
| 45462 | 2 | lives | verified |
| 45464 | 2 | health | verified |
| 45466 | 2 | ammo | verified |
| 45468 | 2 | keys (bit 0 gold, bit 1 silver) | verified (MLI sets 3) |
| 4546A / 4546C / 4546E | 2 each | best / current / chosen weapon | inferred (Wolfenstein layout) |
| 4547A / 4547C / 4547E | 2 each | secrets / treasures / kills found | verified (secret 1, treasure 8) |
| 45480 / 45482 / 45484 | 2 each | totals (floor 1 skill 2: 5 / 45 / 18) | verified |
| 45486 | 4 | play time in tics | inferred |
| 45796 | 20 x 10 | per-floor tally records (kill %, secret %, treasure %, time in s) | verified for floor 1 (time 4 after Tab+E); 20 records per the engine source for Spear, not checked |
| 475B2 / 475B6 | 4 each | player x / y, 16.16 fixed tiles | verified |
| 475BA / 475BC | 2 each | player tile x / y | verified (teleports) |
| 475CC | 2 | player angle, degrees, 0 east, 90 north | verified |

## Emulation notes
- Model `svga-15000` as in the bundle; sound on.
- Flat routes reproduce; cached states reproduce themselves (see Read first).
- Doors close after about 5 s; pushwalls slide for about 256 frames.
- Do not snap the DOS command line (front end).

## Checkpoints
`checkpoints.txt`: `title`, `menu` "same" in cachecheck; the nine `s_*` reach the same frames as the flat replay
and differ only in memory (see Determinism). `s_saved` writes `M1/SAVEGAM0.SOD`.

## Sources
| Source | What | Date |
|---|---|---|
| The program itself (strings in memory, CONFIG.SOD, GAMEMAPS.SOD, start.bat) | version evidence, parameters, debug strings, menus, key bindings, maps | 2026-11-25 |
| `games/dos/wolfenstein-3d/playbook.md` and tools | engine behaviour, macros, map reader | 2026-11-25 |
| id Software's released Wolfenstein 3D / Spear source (knowledge, not fetched) | Spear's `debugmode`, static object list, boss spawn codes, tedlevel = map index, floor 21 shown as 18, LevelRatios of 20 | 2026-11-25 |
No web research this run (budget spent on verification; the engine facts were checked in play instead).

## Open questions
- Exact build (Spear 1.4 by engine features; FormGen/Activision re-release not matched by EXE size).
- Why the quiz code is present but silent (a later build that skips it, or a condition not met?).
- Killing the Angel of Death: health and the fight pattern; what comes after (ending text, victory totals).
- Where the secret floors 19/20 return to after their exit; ghosts (spectres) on floor 21 not seen yet.
- LevelRatios: 20 records assumed from the source, only record 1 seen.
