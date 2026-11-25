# Spear of Destiny (DOS) - design reference

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
A first-person shooter on the Wolfenstein 3D engine (id Software, 1992, published by FormGen): B.J. Blazkowicz
fights through one mission of 21 floors on a grid of walls and doors to recover the Spear of Destiny **(verified:
map data, `tools/sodmap.py list`)**. The core loop is walk, open doors, shoot guards, collect ammunition, food
and treasure, find pushwall secrets and reach the elevator switch; each floor ends on a tally of time, par and
kill/secret/treasure ratios with a bonus **(verified: tally after Tab+E on floor 1)**. Structure: Tunnels 1-4 and
Trans Grosse (floor 5), Dungeons 1-4 and Barnacle Wilhelm (10), Castle 1-5 and the Ubermutant (16), the Ramparts
(17), the Death Knight and the Spear (18), two secret floors (19, 20; secret exits on floors 4 and 12) and the
Angel of Death (21, shown as "18" on the status bar) **(verified: map names and boss objects; floor 21's
number seen in play)**. Four skills, save anywhere in ten named slots **(verified)**. No episode select (unlike
Wolfenstein 3D) **(verified)**.

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
