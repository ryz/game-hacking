# Quake (DOS, shareware 1.06) - design reference

How the game works, for game designers: rules, formulas, progression, data tables, and quirks, built up while
the game is researched and played. No RAM/ROM addresses here (those live in `../playbook.md`). Screenshots are
the evidence: link them (`../shots/main/<file>.png`; the file name of a shot is in the set's `index.md`).

## Notation and style (binding for every document in this folder)
- **Confidence tags** after the claim they cover:
  **(verified)** seen in play here (name the shot id or the route/checkpoint);
  **(source)** from the manual/FAQ/wiki, link in Sources below;
  **(RAM)** read from or tested through memory while playing (e.g. the HP formula from before/after values);
  **(inferred)** reasoned from observations with a gap;
  **(computed)** worked out here from a stated rule or table.
  A claim with no tag is not allowed.
- **Numbers:** decimal; random ranges in prose "a random number from 1 to 8"; dice `NdS+B`; percentages `5%`.
- **Names:** the game's own on-screen names (English release; give the original name in tables if the game is
  Japanese-only). Prose uses full names.
- **No engineering words** in prose (byte, flag, routine): say what it means in play.
- **Structure:** each document starts with an Overview a designer reads in two minutes, then numbered sections
  (`## 1. ...`); one home per rule (other documents link to it); each document ends with **Open questions**
  (what is not known, what was tried). Never fill a gap with a guess presented as fact.
- **Quirks and likely bugs** go in [findings.md](findings.md): a `##` heading, then `**Behavior:**`,
  `**Intended:**`, `**Confidence:**`, `**Impact:**`.

## Overview
Quake is a real-time first-person shooter in a fully 3D world: the player runs, jumps, swims and turns
freely, shoots monsters with a growing arsenal, presses buttons and rides lifts, and looks for secrets on
the way to each level's exit (verified for movement, shooting, a door, a button and a lift in E1M1 on
Normal). A new game starts in a playable start map where the difficulty is chosen by walking into one of
three halls (Easy, Normal, Hard; a hidden fourth for Nightmare) that end in slipgates (teleporters) to a hub
with one slipgate per episode (verified for Normal; map data for the others). The shareware version holds
Episode 1, Dimension of the Doomed, eight levels from The Slipgate Complex to the boss level and a secret
level; the other episode gates show a "please register" message (verified on screen). The game can be saved
anywhere in twelve slots and quicksaved (verified: slot 1); dying restarts the level (source). Health,
armor and the current ammunition are always on the status bar; the score overlay (TAB) gives monsters
killed, secrets found and time (verified).

## Documents
| Document | Covers |
|---|---|
| [systems.md](systems.md) | game-design lens: index of every feature, system and mechanic, with rule, details and shots |
| [interface.md](interface.md) | UI/UX lens: conventions, inventory of every screen, menu, prompt and element, screen flow |
| [content.md](content.md) | content lens: a reasonable variety of environments, opponents, items, equipment, abilities, people |
| [findings.md](findings.md) | quirks, exploits, likely bugs |
<!-- Add one document per system, e.g. controls-and-feel.md (movement, physics, input), progression.md (levels,
     unlocks, difficulty curve), combat.md, characters.md (stats, leveling), items.md (+ an items table),
     enemies.md (+ table), economy.md (money, shops, prices), world.md (areas, map, secrets), modes.md. -->

## Sources
| Source | URL | Used for |
|---|---|---|
| id Software README.TXT, HELP.TXT, CONFIG.CFG | in the shareware ZIP | controls, switches, version notes |
| Map entities in ID1/PAK0.PAK (start.bsp, e1m1.bsp) | in the shareware ZIP | skill halls, episode gates, E1M1 monsters and items per skill |
| Wikipedia, Quake (video game) | https://en.wikipedia.org/wiki/Quake_(video_game) | release, publisher, episode name, save system |

