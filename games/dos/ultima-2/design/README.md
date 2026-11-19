# Ultima II: The Revenge of the Enchantress (DOS) - design reference

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
A single-character role-playing game seen from above on the surface and in towns, and in first-person
wireframe in dungeons and towers (verified). The hero walks Earth in five periods - the Time of Legends, Pangea
9,000,000 B.C., 1423 B.C., 1990 A.D. and the Aftermath of 2112 - joined by time doors that wander between four
fixed squares in each period, and flies a rocket to nine planets by typing three coordinates (verified). Time runs
on its own: if the player waits, the game passes a turn about once a second and monsters keep acting
(verified). The goal is to kill the enchantress Minax in her castle Shadow Guard in the Time of Legends: buy the
quicksword Enilno from a jailed swashbuckler, earn a priest's blessing on planet X, buy the ring that protects
from force fields, and fight her as she jumps between two chambers (verified with pokes, see the playbook
route). Progress is otherwise free: money from fights and thieves, hit points from Lord British, items from
slain thieves, fighters, wizards and guards (code). One character, saved on the surface of Earth with Q
(verified). The IBM release uses CGA four-colour graphics and 40-column text screens (verified).

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
| The game's own files | `rom/ultima-2.zip` (ULTIMAII.EXE strings and code, MAPX/MAPG maps, MONX objects, TLK talk lines) | rules, names, places, quest |
| Wikipedia | https://en.wikipedia.org/wiki/Ultima_II:_The_Revenge_of_the_Enchantress | release history, periods, outline of the ending |
