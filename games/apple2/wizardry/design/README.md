# Wizardry: Proving Grounds of the Mad Overlord - design reference

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
Wizardry: Proving Grounds of the Mad Overlord, the 1981 Apple II original (version 2.1 of 22 January 1982), is
a first-person party role-playing game. The player keeps a roster of up to 20 characters, forms a party of six
in a castle made of text menus (tavern, inn, temple, trading post, training grounds) and takes it down a maze
of ten floors of 20 by 20 squares drawn as a small wireframe view beside the command list and the party table
**(verified)** `start`, `maze1`. Fights are turn-based against up to four groups of monsters, with orders given
to all six members before a round runs **(verified)** `battle`, `werdna`. The goal is the amulet held by the
wizard Werdna on floor 10; bringing it back to the castle ends the quest with 250,000 experience points and
the chevron of rank for each member, at the price of all equipment and most gold **(verified)** `ending`. The
roster on the scenario disk is the only save; the game writes it as it goes **(verified)** saves 01, 02.
This folder starts the three lens documents for the Apple II version. The scenario data (floors, items,
monsters, spells) is the DOS port's **(verified by decoding both disks: the ten floors differ in one square)**;
the DOS design documents (`../../../dos/wizardry/design/`) hold the detailed rules and tables and are linked
from the rows here, each row saying what was re-checked on the Apple II.

## Documents
| Document | Covers |
|---|---|
| [systems.md](systems.md) | game-design lens: index of every feature, system and mechanic, with rule, details and shots |
| [interface.md](interface.md) | UI/UX lens: conventions, inventory of every screen, menu, prompt and element, screen flow |
| [content.md](content.md) | content lens: a reasonable variety of environments, opponents, items, equipment, abilities, people |
| [findings.md](findings.md) | quirks, exploits, likely bugs |
| [maps/floors.txt](maps/floors.txt) | the ten floors as text maps with their special squares, decoded from the scenario disk (`../tools/maps.py`) |
| DOS: [systems](../../../dos/wizardry/design/systems.md), [interface](../../../dos/wizardry/design/interface.md), [content](../../../dos/wizardry/design/content.md), [items](../../../dos/wizardry/design/items.md), [findings](../../../dos/wizardry/design/findings.md) | the detail documents of the DOS port (same scenario data, other screens and keys) |
<!-- Add one document per system, e.g. controls-and-feel.md (movement, physics, input), progression.md (levels,
     unlocks, difficulty curve), combat.md, characters.md (stats, leveling), items.md (+ an items table),
     enemies.md (+ table), economy.md (money, shops, prices), world.md (areas, map, secrets), modes.md. -->

## Sources
| Source | URL | Used for |
|---|---|---|
| the game disks | `rom/wizardry.zip` (not committed) | every prompt and message (program text), maps, item and monster tables, roster |
| DOS port documents | `games/dos/wizardry/design/` | rules and tables, re-checked where a row says so |
| scout's playbook | `../playbook.md` | routes, checkpoints, what was verified on 2026-11-19 |
