# Wizardry: Proving Grounds of the Mad Overlord (NES, USA) - design reference

How the game works, for game designers: rules, formulas, progression, data tables, and quirks, built up while
the game is researched and played. No RAM/ROM addresses here (those live in `../playbook.md`). Screenshots are
the evidence: link them (`../shots/main/<id>.png`).

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
A first-person party dungeon game: the player creates up to twenty adventurers in the Training Grounds (name,
race, alignment, bonus points, class) **(verified)**, forms a party of six in Gilgamesh's Tavern **(verified)**
and explores a maze of ten floors, each a grid of 20 by 20 squares that wraps at its edges **(verified, maze
data)**, fighting groups of monsters that are shown unidentified at first ("5 Small humanoids") **(verified)**.
Between trips the castle offers an inn, a shop (Boltac's Trading Post) and a temple **(verified menus)**. The
floors contain doors, darkness, stairs, teleporters, elevators, pits and spinners **(inferred from the maze data,
partly verified)**; the goal is Werdna on floor 10 **(source: series)**. The game saves to the cartridge: the
roster is kept in battery memory and Edge of Town > Leave Game is the save point **(verified)**. This US NES
release (Nexoft 1990, by Game Studio) renames the Priest "Cleric" and the Bishop "Wizard" **(verified on screen)**.

## Documents
| Document | Covers |
|---|---|
| [findings.md](findings.md) | quirks, exploits, likely bugs |
| [castle.md](castle.md) | character creation, inn and levels, Boltac's prices, temple, spell books, saving |
| [combat.md](combat.md) | encounters, orders, spells, chests, death |
| [maps.md](maps.md) | the maze floor by floor: walls, secret doors, every special square with its meaning, connections, the ending |
| [maps/](maps/) | all ten floors drawn from the game data (`floor_NN.png`, `atlas.png`, `floors.txt`) |
| characters.md (planned) | races, classes and their requirements, creation, bonus points, levels |
| combat.md (planned) | encounters, surprise, options, spells |
| world.md (planned) | castle services, floors, elevators, special squares |
<!-- Add one document per system, e.g. controls-and-feel.md (movement, physics, input), progression.md (levels,
     unlocks, difficulty curve), combat.md, characters.md (stats, leveling), items.md (+ an items table),
     enemies.md (+ table), economy.md (money, shops, prices), world.md (areas, map, secrets), modes.md. -->

## Sources
| Source | URL | Used for |
|---|---|---|
| Wikipedia | https://en.wikipedia.org/wiki/Wizardry:_Proving_Grounds_of_the_Mad_Overlord | release facts |
