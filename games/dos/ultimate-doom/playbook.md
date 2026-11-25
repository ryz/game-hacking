# The Ultimate Doom (DOS) - playbook

Everything an agent needs to play this game efficiently: read it before playing, add to it after every run.
Status of each fact: **verified** (seen in the emulator, with the route) or **source** (manual/FAQ/wiki, not yet
checked). Never delete a fact that turned out wrong: strike it and say what is true.

## Read first
- **Start:** `rom/ultimate-doom.zip` (vault; the bundle also holds Doom II, TNT, Plutonia and the Master Levels:
  not this game), model `svga-40000`. Boot = DOSBox Pure "Go to Command Line" (10th entry: `down*9`), then
  `doom -nosound` (macro `BOOT`). Only DOOM.EXE + DOOM.WAD (1.9, "The Ultimate DOOM Startup v1.9") are used.
  Frames 320x200 (the start-up text before the title is text mode). No aspect decision needed.
- **Macros:** `TITLE` (title picture, BOOT+90), `MENU` (main menu over the title), `NEWGAME` (Episode 1, Hurt me
  plenty, E1M1 first control), `LEVEL:E:M` (= `WARP`: `doom -nosound -skill 3 -warp E M`, straight into any map
  E1M1-E4M9 at Hurt me plenty), `ARMS` (iddqd + idkfa, then realistic armor 143 and ammo 137/38/212/27, wait
  300 so the pickup message is gone), `GOD`, `IDKFA`, `SAVE1:NAME` (Esc, Save Game, slot 1, type NAME, Enter),
  `TP:...` (teleport: get the call from `dstate.py --tp`). Honest E1M1 route: `E1DOOR, E1FIGHT1, E1ZOMBIE,
  E1ZIGZAG, E1ARMOR, E1EXIT, E1TALLY` (real key holds made by `tools/dnav.py`).
- **Checkpoints (17, all flat, `cachecheck` 17/17 "same" incl. memory):** `title`, `menu`, `s_e1m1`,
  `s_e1m1_door`, `s_e1m1_fight1`, `s_e1m1_zigzag`, `s_e1m1_armor`, `s_e1m1_exit` (tally), `s_e1m2`, `s_saved`
  (save `saves/01_start.sav`), `m_e1m1`, `m_e1m8`, `m_e2m1`, `m_e2m8`, `m_e3m1`, `m_e3m8`, `m_e4m1`.
- **Determinism:** better than Quake/Wolfenstein: a flat route gives identical frames and memory, and
  `@checkpoint,keys` gives exactly the same state as the flat route with the same keys (checked on
  `@s_e1m1_fight1,right:30,up:60,ctrl:20,w40` and `@s_e1m1_zigzag,left:40,up:80,w60`). Shot routes may start
  from any checkpoint. Doom's own random table restarts with every level, so fights repeat exactly.
- **Plans:** `shots.txt` holds `main` (19 active lines, previewed) and `start` (33 `#start ` lines, previewed
  in full: power-on to "game saved." at E1M2). Not shot yet. In-game lines end in `!` (nothing settles; a
  settle also wipes pickup messages and finishes the tally count).
- **Tools** (`games/dos/ultimate-doom/tools/`):
  `wadmap.py list | E1M1 [--grep RE] | --png OUT | --at X Y | --tp X Y A` (THINGS by skill, exits, doors and
  keys, secret sectors, plan picture, sector at a point); `dstate.py ROUTE ...` (map, position, angle, health,
  armor, ammo, weapon, kills/items/secrets, powers, keys; `--chain`; `--tp ROUTE X Y ANGLE` prints the `TP:`
  call for that exact route); `dnav.py ROUTE "path X Y; fight N; use; ..." --out FILE` (plays goals with RAM
  feedback and writes the real key tokens: grid path planner over the WAD, auto-use on doors, aim at the
  nearest monster from memory).
- **Keys:** arrows move/turn, `ctrl` fire, `space` use (doors, switches; within 64 units), `alt+left/right`
  strafe, `rshift` run (key_speed is RIGHT shift), `comma`/`period` strafe, `1`-`7` weapons, `tab` automap,
  `esc` menu, F1 help, F2 save, F3 load. `w30` is a wait, `w:30` the W key (unused here).
- **Traps:** the menu must open on the title picture (`TITLE` = BOOT,w90): presses later than ~BOOT+280 land in
  the title-to-demo wipe and the "new game" turns into the attract demo. The player mobj address changes per
  route: never reuse a `TP:` call on another route (regenerate). Walking without fighting gets you shot to
  pieces (hp 76 -> 11 on one stretch): `dnav.py fight N` at each room. `use` needs to stand within 64 units
  of the line. Solid decorations (lamps, columns, barrels) block walking.
- **Open:** barons on E1M8 (sealed closets behind walk triggers at 416 2496 and 304 2752; the TP into the
  pit faced a wall), episode end texts (kill a boss: E2M8/E3M8 end on the boss's death), a real death, face
  stages by real damage (`s_e1m1_exit` route shows 19% with the bloodied face), most `main` action shots.

## Identity
| Field | Value |
|---|---|
| Title (EN / original) | The Ultimate Doom (in-game: "The Ultimate DOOM", version 1.9) |
| Platform / model used | MS-DOS, `svga-40000` (see `game.json`) |
| Release (region, year) | North America; Doom 10 December 1993 (shareware), The Ultimate Doom 1995 (source: Wikipedia) |
| Developer / publisher | id Software / id Software (1993), GT Interactive (Ultimate Doom, 1995) (source: Wikipedia) |
| Genre | first-person shooter, real-time 2.5D |
| Players / save system | 1 player here (network/serial deathmatch not used); save anywhere, 6 named slots `DOOMSAV0.DSG`-`DOOMSAV5.DSG` (verified slot 0) |

Dump: the Steam DOS bundle (`game.json` "source"), DOOM.WAD md5 c4fe9fd9... = Ultimate Doom 1.9. Start-up
text (verified): "The Ultimate DOOM Startup v1.9", "This version is NOT SHAREWARE", "adding doom.wad",
"registered version", DPMI memory 0xd70000, 8 MB for the zone.

## Boot sequence
- Intake/vault probe: `w120,enter` (DOOM.EXE from the start menu) shows the title, then the attract demo.
- `BOOT` = `w120,down*9,enter,w120,type:doom -nosound\n` (verified). Frame +0: start-up text (text mode, R_Init
  progress); +60 to ~+280: title picture; then the melt wipe into attract demo 1.
- `TITLE` = `BOOT,w90` (verified); `MENU` = `TITLE,esc,w20`; `NEWGAME` = `MENU,enter,w20,enter,w20,enter,w120`
  (New Game, first episode, default skill Hurt me plenty; verified position 1056 -3616 facing north).
- `WARP:E:M` / `LEVEL:E:M` = `w120,down*9,enter,w120,type:doom -nosound -skill 3 -warp E M\n,w300` (verified for
  E1M1, E1M8, E2M1, E2M3, E2M8, E3M1, E3M5, E3M8, E4M1, E4M7).
- The bundle's `start.bat` (menu for the five games) is not used. DEFAULT.CFG has the Sound Blaster on
  (devices 3); `-nosound` keeps the determinism rule of `docs/emulator/dos.md` (not tested with sound).

## Controls
From DEFAULT.CFG (scan codes) and the F1 help screen (verified on screen).
| Context | Key | Action | Status |
|---|---|---|---|
| Play | up / down | forward / back | verified (`up:40` ~100-150 units from rest, ~3.7 units/frame at speed) |
| | left / right | turn | verified (1.76 degrees per tic for the first 6 tics, then 3.52; one tic = 2 frames) |
| | rshift + arrow | run | verified (`rshift+up:40` ~220 units); key_speed 54 = right Shift, left Shift does not run |
| | alt + left/right | strafe | verified |
| | comma / period | strafe left / right | source (DEFAULT.CFG key_strafeleft 51, key_straferight 52) |
| | ctrl | fire | verified (pistol, rocket, plasma, BFG) |
| | space | use: doors, switches | verified (door at 1536 -2496 from 16 units; failed from 76 units) |
| | 1-7 | fist/chainsaw, pistol, shotgun, chaingun, rocket launcher, plasma rifle, BFG 9000 | verified 5, 6, 7 |
| | tab | automap (F follow, M mark, C clear, +/- zoom, 0 full) | tab verified; others source (help screen) |
| | esc | main menu (pauses) | verified |
| | F1 help, F2 save, F3 load, F4 sound volume, F5 detail, F6 quicksave, F7 end game, F8 messages, F9 quickload, F10 quit, F11 gamma, -/= screen size | | F1 verified; others source (help screen) |
| Menus | up / down, enter, esc | move, choose, back | verified |
| Save name | letters, enter | type the slot name | verified (`type:ryz`) |
| Intermission | space (any key) | skip the count / continue | verified |

Input timing: the default press (hold 8, wait 40) works in menus; `w20` between menu presses is enough. In play
holds are movement for N frames; nothing is lost.

## Game structure
- Four episodes of 8 maps plus a secret map 9 each (36 maps, `wadmap.py list`): Knee-Deep in the Dead (E1:
  Hangar, Nuclear Plant, ... Phobos Anomaly with two Barons of Hell), The Shores of Hell (E2, ends with the
  Cyberdemon in E2M8 Tower of Babel), Inferno (E3, Spider Mastermind in E3M8 Dis), Thy Flesh Consumed (E4).
  Map names seen: E1M1 Hangar, E1M2 Nuclear Plant (verified on the tally and automap).
- Skills: I'm too young to die, Hey, not too rough, Hurt me plenty (default), Ultra-Violence, Nightmare!
  (verified on screen). THINGS carry skill bits: 1 = skills 1-2, 2 = skill 3, 4 = skills 4-5, 16 = multiplayer
  only (`wadmap.py --skill`).
- Main menu: New Game, Options, Load Game, Save Game, Read This!, Quit Game. Options: End Game, Messages, Graphic
  Detail, Screen Size, Mouse Sensitivity, Sound Volume (Sfx/Music). Save Game outside a game: "You can't save if
  you aren't playing! press a key." (all verified).
- Level end: exit switch or line -> tally (Kills, Items, Secret, Time, Par) -> "Entering <next map>" on the
  episode map -> next map. Health, armor, weapons and ammo carry over (verified E1M1 -> E1M2).

### Maps (read from DOOM.WAD)
`wadmap.py` reads THINGS/LINEDEFS/SIDEDEFS/VERTEXES/SECTORS/SEGS/SSECTORS/NODES: things by skill (monsters,
weapons, ammo, health, armor, power-ups, keys), exits (line specials 11/52/197 normal, 51/124/198 secret), doors
and key doors, other specials, secret sectors (special 9), the sector at a point (BSP walk: floor, ceiling,
light, special). E1M1 on Hurt me plenty (verified against play): 6 monsters (zombiemen at 2272 -2432, 2272 -2352,
2912 -2816, 3056 -3584; imps at 3440 -3472 on the ledge and 3008 -4416), MegaArmor 1824 -3280 in the nukage pool,
shotgun 3264 -3936 in a secret, green armor -224 -3232 (west secret), exit switch at 2912 -4768, 3 secrets.
Where things are in other maps (for `main`): Cyberdemon E2M8 -1472 576; Spider Mastermind E3M8 1600 -768;
Barons E1M8 304/528 2864; chainsaw E1M2 -2080 912 and E2M2 928 32; plasma E2M2 1056 528; BFG E3M3 -224 176;
invulnerability, berserk, computer map, soulsphere, spectre, lost soul, cacodemon, shotgun guy in E3M3;
invisibility E1M3 256 -2752; radiation suit E1M4 128 176 (skills 1-2 only there; E2M2 -48 16 HMP).

## Shot plan
`shots.txt`: set `start` (33 lines, honest play, previewed 2026-11-25) and the first 19 `main` lines.
- `start` (33): boot 1 (start-up text), title 1, menu 4 (main, episode, skill, help), gameplay 13 (melt wipe,
  first control, corridor, door, zigzag room, secret closet, yard, MegaArmor, medikit, exit room, tally
  counting and done, E1M2), battle 6 (zombieman fires, hit flash, dead, third zombieman, imp fireball, fireball
  hit), map 2 (automap, Entering Nuclear Plant), options 2, save 3 (menu, typing ryz, "game saved.").
- `main` planned and previewed (19): title, menus 3, help, automap with computer map and with iddt, power-ups
  active 5 (invulnerability, berserk, invisibility, radiation suit, light amplification), Cyberdemon 2 (in
  view, rocket fired), Spider Mastermind 2 (in view, BFG fired), env starts of E2M1, E3M1, E4M1.
- `main` still to plan (capture): every weapon firing at a monster (fist, chainsaw, pistol, shotgun, chaingun,
  plasma at monsters; rocket and BFG done), armors (green, MegaArmor pickup message), soulsphere, computer map
  pickup, monsters in action (zombieman, shotgun guy, imp, demon, spectre, lost soul, cacodemon, baron),
  face damage stages and a real death (no god, TP near a Cyberdemon, wait), tallies, episode end texts (E2M8:
  kill the Cyberdemon with BFG; E3M8: the Spider Mastermind), plain views of each episode (env_*), keys and key
  doors, a teleporter, the secret level tally, Read This! pages, quit prompt.

## Strategy and walkthrough notes
- **Build action shots with `TP`:** `python3 games/dos/ultimate-doom/tools/dstate.py --tp "LEVEL:2:8,ARMS,5"
  -1000 100 135` prints `TP:...` for that route; append it, then weapon key, `ctrl:N`, a wait, `!`. Spots:
  check the sector with `wadmap.py MAP --at X Y` (floor/ceiling) and pick an open area 400-700 units from the
  monster with nothing between. Keep 128 units between the spot and any monster (see RAM, teleport caveat).
- **Fights:** with `dnav.py`: `fight N [R]` aims at the nearest living monster within R units and holds fire
  20 frames, N rounds. Monster positions are read from memory (`mons`).
- **E1M1 route** (honest): start -> north-east corridor (1280 -2860, 1285 -2560) -> door at 1536 -2496 ->
  computer room (two zombiemen come through the door) -> east (2536 -2664) -> sector by the third zombieman
  (2808 -2808) -> zigzag room (zombieman, imp on the ledge) -> south corridor, through the secret closet (west
  door at 2944 -3840) and the lower rooms -> MegaArmor in the nukage pool (costs ~15% health) -> medikit (2304
  -4032) -> south door (y -4016) -> imp room -> exit room door (y -4648) -> switch on the west wall (2912 -4768).
  Health falls to 19%: the zigzag imp and the imp room imp do most of it.
- **Monster scan:** stale mobjs from earlier levels stay in memory (dnav `mons` showed doubles after a level
  restart): trust only the current level's list (first entries after a fresh load).

## Naming
The only name the game asks for is the save slot name: `ryz` (typed with `type:ryz` after Enter on the slot).

## Shortcuts
| What | How (tokens / prefix / code) | Source | Status |
|---|---|---|---|
| Level select | `LEVEL:E:M` (command line `-warp E M -skill 3`) | id's command-line parameters | verified |
| iddqd | god mode, "Degreelessness Mode On" | cheat | verified |
| idkfa | all weapons, full ammo, 200% blue armor, all six keys, "Very Happy Ammo Added" | cheat | verified (ARMS then lowers to realistic values) |
| idclevEM | change level, e.g. `type:idclev23` -> E2M3 (inventory reset to pistol) | cheat | verified |
| idbehold | prompt "inVuln, Str, Inviso, Rad, Allmap, or Lite-amp"; `idbeholdv/s/i/r/a/l` toggle each ("Power-up Toggled") | cheat | verified all six |
| iddt | automap: once full map, twice also things | cheat | verified (twice) |
| idchoppers | chainsaw, "... doesn't suck - GM" | cheat | verified |
| idmypos | coordinates line | cheat | verified |
| idspispopd | no clipping, "No Clipping Mode ON" | cheat | verified (idclip is Doom II) |
| Teleport | `TP:` from `dstate.py --tp ROUTE X Y A` | RAM | verified (E2M8, E3M8; E1M8 moved but faced a wall) |
| Saves | `sav:01_start` + Load Game slot 1: `TITLE,esc,w20,down*2,w10,enter,w30,enter,w100` | made here | verified (E1M2, health 19, armor 163) |
| Timedemo | `doom -nosound -timedemo demo1` prints "timed 1710 gametics in N realtics" | id | verified |

### Saves (rom/saves/ultimate-doom/, never committed)
None downloaded (a save is easier made here; cheats cover the rest).

## RAM map (for `game.json` "ram" watches and pokes)
Physical addresses with model `svga-40000` and `BOOT` (linear = physical under DOS/4GW here). Layout = id's
released source (player_t, mobj_t), checked against values in play.
| Address | Size | Meaning | How found |
|---|---|---|---|
| 22B24C | 4 | players[0].mo: pointer to the player's mobj (zone memory; address changes per route) | maxammo pattern 200 50 300 50 at +172 |
| 22B26C | 4 | health (status bar) | 100 -> 88 -> 76 when shot (verified) |
| 22B270 / 22B274 | 4 / 4 | armor points / armor type (1 green, 2 blue) | MegaArmor -> 194/2 (verified); poke 143 shows 143% (verified) |
| 22B278 | 6 x 4 | powers: invulnerability, berserk, invisibility, radiation suit, computer map, light amp (tics) | layout |
| 22B290 | 6 x 4 | cards: blue, yellow, red keycard, blue, yellow, red skull | idkfa sets all 1 (verified) |
| 22B2BC | 4 | readyweapon 0 fist 1 pistol 2 shotgun 3 chaingun 4 rocket 5 plasma 6 BFG 7 chainsaw | verified (pistol 1, plasma 5) |
| 22B2C4 | 9 x 4 | weaponowned | layout |
| 22B2E8 | 4 x 4 | ammo: bullets, shells, cells, rockets | verified (pokes show on the status bar) |
| 22B318 / 22B31C / 22B320 | 4 each | kills, items, secrets of this level | verified (tally 6 kills = 100%) |
| 22B7CC / 22B7BC | 4 / 4 | gameepisode / gamemap (follow -warp and idclev) | compared four boots (verified) |
| 22A778 / 22A770 | 4 / 4 | start episode / start map (do not follow idclev) | same |
| mobj +12/+16/+20 | 4 each | x, y, z (16.16 fixed) | verified (1056 -3616 0 at E1M1 start) |
| mobj +32 | 4 | angle (BAM, 0x40000000 = north) | verified |
| mobj +56/+60 | 4 each | floorz / ceilingz | poked by `TP` (verified needed: without it z stays at the old floor) |
| mobj +88 / +92 / +108 | 4 each | type / &mobjinfo[type] (92 bytes each) / health | used by dnav `mons` (verified) |
Teleport caveat (inferred from the released source): a poked position skips the game's blockmap unlinking;
on the next move the game re-links the player but drops the destination block's other things from the
collision lists. Monsters within ~128 units of the spot may then not block or be hit; keep spots clear.

## Emulation notes
- **Model:** `svga-40000`. `-timedemo demo1`: 7800 cycles 7.7 fps (1710 gametics in 7816 realtics), 20000 19.3
  fps, 40000 37.1 fps (above the 35 tics per second cap: full speed). Cost about 0.18 s per 100 frames at 40000.
  70 frames = 1 second = 35 game tics.
- `-nosound`: chosen for determinism (Quake rule); the sound-on case was not tested.
- Flat routes, `@checkpoint` routes and cache hits all agree exactly (cachecheck "same" for every checkpoint,
  frames and memory); nothing like the Quake/Wolfenstein state-load drift was seen.
- The start-up text screen is text mode (640x400 picture), then 320x200.
- Pickup messages stay about 4 s (280 frames) at the top of the screen; `ARMS` ends with `w300` for that.

## Checkpoints
See Read first; `s_*` are the `start` chain (honest), `m_*` are `-warp` starts for `main`.

## Sources
| Source | URL | Used for | Accessed |
|---|---|---|---|
| The game itself: start-up text, menus, F1 help screen, DEFAULT.CFG, start.bat | `rom/ultimate-doom.zip` | version, keys, menus, cheat messages | 2026-11-25 |
| DOOM.WAD map lumps | `rom/ultimate-doom.zip` | things, specials, secrets, sectors (wadmap.py) | 2026-11-25 |
| id Software's released Doom source (linuxdoom 1.10, knowledge, not fetched) | - | player_t/mobj_t layout, turn speeds, cheats, command-line switches | 2026-11-25 |
| Wikipedia, Doom (1993 video game) | https://en.wikipedia.org/wiki/Doom_(1993_video_game) | release dates, publisher, episode names | 2026-11-25 |

## Open questions
- Barons of Hell in action (E1M8 closets behind W1 door triggers, or another map), episode end texts, a real
  death, face stages by damage: routes not made yet.
- Sound on: does a loaded state drift as in Quake? Not tested (`-nosound` used throughout).
- Teleport side effect on monsters near the spot (blockmap) not observed in play yet.
- comma/period strafe, F2-F11 keys not tried.
