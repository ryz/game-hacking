# Phantasie - playbook

Everything an agent needs to play this game efficiently: read it before playing, add to it after every run.
Status of each fact: **verified** (seen in the emulator, with the route) or **source** (manual/FAQ/wiki, not yet
checked). Never delete a fact that turned out wrong: strike it and say what is true.

## Read first
At most 60 lines, kept current by every run: an agent reads this block, then only the sections its targets need.
- **Start:** (the checkpoint or macro to begin from; model; what must be in `rom/`)
- **Macros and checkpoints that matter:** (warp, party, fight setup; the chain to the late game)
- **Traps that cost calls:** (lost keys, stale HUD, pokes that break something, slow loads)
- **State:** (what is captured, what is open)

## Identity
| Field | Value |
|---|---|
| Title (EN / original) | |
| Platform / model used | see `game.json` |
| Release (region, year) | |
| Developer / publisher | |
| Genre | |
| Players / save system | (battery save, password, none) |

## Boot sequence
Power-on to the title and to first control. Put the result in `game.json` "macros" (e.g. `TITLE`, `NEWGAME`)
and make `title` / `start` checkpoints from them.
- Intake probe: `work/intake/c64/phantasie/sheet.png` (frame every 60 frames, no input).
- Route to the title: `TITLE` = ...
- Route to first gameplay: `NEWGAME` = ...

## Controls
| Context | Button | Action | Status |
|---|---|---|---|
| Title | Start | | |
| Field / gameplay | D-pad | | |
| | A | | |
| | B | | |
| | Start | | |
| | Select | | |
| Menus | A / B | confirm / back | |

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

### Saves (rom/saves/phantasie/, never committed)
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
