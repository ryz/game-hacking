# Dungeon Master - playbook

Everything an agent needs to play this game efficiently: read it before playing, add to it after every run.
Status of each fact: **verified** (seen in the emulator, with the route) or **source** (manual/FAQ/wiki, not yet
checked). Never delete a fact that turned out wrong: strike it and say what is true.

## Identity
| Field | Value |
|---|---|
| Title (EN / original) | Dungeon Master, version 3.60 (multi-language English/French/German) |
| Platform / model used | Amiga, `A500` (Kickstart 1.3, 512K chip + 512K slow RAM): **verified** to the dungeon |
| Release (region, year) | Europe (Psygnosis release, title text "COPYRIGHT 1992"); the game is from 1987 (Atari ST), first Amiga release 1988 |
| Developer / publisher | FTL Games / Psygnosis (this version) |
| Genre | real-time first-person dungeon crawler |
| Players / save system | 1 player; saves to a separate disk named `DungeonSave` (strings on the game disk; **source**, not tried) |
| Dump | `Dungeon Master v3.60 (FTL + Psygnosis).adf` from the owner's ZIP (SHA-1 in `game.json`); a cracked release (crack intro by The Driver/Dytec, SCSI, Mr.Rox & AmoK/Ministry): no copy protection left, **verified** to the dungeon |

## Boot sequence
Power-on to the title and to first control. Put the result in `game.json` "macros" (e.g. `TITLE`, `NEWGAME`)
and make `title` / `start` checkpoints from them.
- Intake probe: `work/intake/amiga/dungeon-master/sheet.png` (frame every 60 frames, no input).
- **verified** 2026-11-20 (checkpoints `entrance`, `dungeon`; a cold rebuild of `dungeon` from power-on matched
  the checkpoint pixel for pixel):
  - Kickstart 1.3 boot, then the disk's Startup-sequence types the crack note (`dungeonrel.txt`) in a hires
    AmigaDOS window and waits for the left mouse button: `w700,mouse1:10`. A click before about frame 600 is
    lost (the window is not up yet).
  - `BJELoad_R` loads the game: the Dungeon Master logo stays for about 4000 frames (80 s of game time) at the
    real floppy speed; clicks do nothing while it loads. Then the entrance doors with ENTER / RESUME / QUIT,
    the pointer already on ENTER: checkpoint `entrance` = `w700,mouse1:10,w4000`.
  - `mouse1:10` on ENTER opens the doors, then about 4500 frames of loading (the doors stay open on the corridor)
    until the dungeon view with the movement arrows: checkpoint `dungeon` (no champions yet).
  - On an `A1200` model the same loads take a fraction of the time (seen once with `emu.py --model A1200`); the
    A500 is kept as the machine the game was made for.

## Controls
| Context | Button | Action | Status |
|---|---|---|---|
| Crack intro | `mouse1` (left button) | continue to the game | verified |
| Entrance | `mouse1` on ENTER (pointer starts there) | enter the dungeon | verified |
| Dungeon | `kp8` | step forward | verified |
| Dungeon | `kp4` `kp6` `kp5` `kp7` `kp9` | strafe left, strafe right, step back, turn left, turn right | source (standard DM keypad layout) |
| Dungeon | `mouse:DX:DY` + `mouse1` / `mouse2` | everything else is done with the mouse: champions, inventory, spells, attacks | source |

Input timing: (does the game drop presses shorter than N frames? need `wN` between menu presses? hold-to-run?)

## Game structure
Modes, menu tree, areas/levels/worlds in order, what unlocks what. Enough to plan a capture route.

## Shot plan
What this game needs in the database (see `docs/capture-guide.md`): the systems and screens that make it
distinctive. One line per planned shot id; the routes go into `shots.txt`.
- [ ] `title_screen` - title
- [ ] ...

## Strategy and walkthrough notes
How to progress quickly and safely: the critical path, dangerous spots, boss patterns, grinding needs, what to
buy. Keep it to what an agent needs to reach the shot targets.

## Naming
Main character: **ryz** (owner's rule); further party members condi, ebo, cubi, deddo, mnz. Name-entry controls
and the token route that types the name: ...

## Shortcuts
Cataloguing beats fair play: completed saves, passwords, GameShark (`gs:`) and Game Genie (`rom:` variant)
codes, debug menus, level select, sound test, RAM pokes. Values that show on screen stay realistic.
| What | How (tokens / prefix / code) | Source | Status |
|---|---|---|---|

### Saves (rom/saves/dungeon-master/, never committed)
| Name | Contents (progress, party, items) | URL | SHA-1 | Status |
|---|---|---|---|---|

## RAM map (for `game.json` "ram" watches and pokes)
| Address | Size | Meaning | How found |
|---|---|---|---|

## Emulation notes
Model choice (GB: DMG/CGB/SGB; NES and SNES: ntsc/pal) and why, RNG behaviour, lag, screens that never settle (animations), anything that
broke a route.

## Checkpoints
Named states are in `checkpoints.txt` (built from routes, never committed as files). Describe the important ones
here if their purpose is not obvious from the name.

## Sources
| Source | URL | Used for | Accessed |
|---|---|---|---|

## Open questions
