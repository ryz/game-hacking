# Might and Magic Book One: The Secret of the Inner Sanctum (DOS) - playbook

Everything an agent needs to play this game efficiently: read it before playing, add to it after every run.
Status of each fact: **verified** (seen in the emulator, with the route) or **source** (manual/FAQ/wiki, not yet
checked). Never delete a fact that turned out wrong: strike it and say what is true.

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
- Intake probe: `work/intake/dos/might-and-magic/sheet.png` (frame every 60 frames, no input).
- **verified 2026-11-18** DOSBox Pure's start menu lists GRAPHSET.EXE, MM.EXE, unins000.exe: `BOOT` =
  `w120,down,enter,w300` runs MM.EXE and ends on the animated title (320x200, 4 colours).
- **verified** The title needs about 10 s before it shows "'ESC' TO START GAME / 'SPACE' FOR SCENES". Space (or
  any other key) steps through a slideshow of demo scenes that look like gameplay (party list, COMMANDS panel)
  but are pictures. ESC -> "ARE YOU READY? THEN PRESS ENTER!" -> Enter -> options menu (`C` create characters,
  `V` view all characters, `#` go to town 1-5). `MENU` = `BOOT,w900,esc,w90,enter,w200`.
- **verified** Keys typed too early stay in the keyboard buffer and are used by the next screen: wait for a
  screen before typing for it.
- **verified** Town number -> the inn's character list (the roster ships with six characters: Crag the Hack,
  Sir Galand, Zenon III, Swifty Sarg, Serena, Wizz Bane). Ctrl+A..F adds or removes a character, X leaves the
  inn into the town. `TOWN:1` = menu, town 1 (Sorpigal), all six added, exit: first control, facing a corridor.
- **verified** In town: arrow keys move and turn, `1`-`6` open a character sheet, ESC goes back. The other
  commands are listed on screen (O order, P protect, R rest, S search, B bash, U unlock, Q quick reference).
- Model `svga-1500`: 1500 cycles is the value in GOG's own DOSBox configuration for this game.
- Not checked yet: creating characters, combat, saving (the game writes ROSTER.DTA when the party checks into an
  inn; see "Saves" in `docs/emulator/dos.md` for what that means for savestates).

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

### Saves (rom/saves/might-and-magic/, never committed)
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
