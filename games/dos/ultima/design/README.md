# Ultima I: The First Age of Darkness (DOS) - design reference

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
Ultima I is a single-character role-playing game (1986 remake of the 1981 original; MS-DOS EGA version 1987)
**(source)**. The player creates one hero (30 points over six statistics, four races, four classes)
**(verified)** and walks a top-down overworld of four continents, buying food, arms, armour, spells and vehicles
in towns, taking quests from the eight kings in the castles and fighting in first-person wireframe dungeons
**(verified)**. Two kinds of quest alternate: find a landmark (rewarded with strength) or kill a named dungeon
monster (rewarded with one of four gems) **(verified for the first, code for the second)**. The game then turns
into science fiction: a shuttle into space, twenty enemy ships shot down to become a Space Ace, a rescued
princess who reveals a time machine, and a journey back in time to destroy Mondain's gem and Mondain himself
**(verified from the time machine to the ending text)**. Saving is by Q on the overworld, four character slots
**(verified)**. Modes are separate programs: character generation, overworld/towns/dungeons, space, the final
confrontation **(verified)**.

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
| The game's own programs (text and code, read 2026-11-19) | `rom/ultima.zip` | names, prices, quest rules, messages |
| Wikipedia | https://en.wikipedia.org/wiki/Ultima_I:_The_First_Age_of_Darkness | release history, remake changes |
| Manual scans (OCR text) | https://archive.org/details/Ultima_I-Manual | monster and spell names, space flight |
