# Might and Magic II: Gates to Another World (DOS) - design reference

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
A first-person party role-playing game: a party of up to six created characters plus hirelings (eight at most)
walks square by square through 60 areas of 16x16 squares of the world of Cron: five towns, a 5x4 grid of
outdoor areas that wraps around at its edges, caverns, castles with two-level dungeons, two wizards' towers and
four elemental planes **(verified)** (areas reached by memory warp; see the playbook). Fights are turn-based text
menus over a full picture of the strongest monster; experience is paid for at training grounds; the world
changes with the century, and the quest needs travel to the past **(source: manual; verified for the year
change)**. Characters gain up to two secondary skills bought from trainers (Cartographer gives the auto-map,
Mountaineer and Pathfinder open mountains and forests) **(source: manual; trainers verified in Middlegate)**.
Saving is signing in at an inn; the whole roster is one file **(verified)**. The main quest: class quests for the
Jurors of Mount Farview, the Queen's Triple Crown in three arenas, four Discs and four elemental Talons, King
Kalohn's Element Orb returned to him in the 9th century so that he defeats the Mega Dragon, and the final
dungeon under Square Lake, where Sheltem, an override code and a cryptogram end the game **(source: area texts,
cluebook; the end verified: [systems.md](systems.md) section 3)**.

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
| Game manual (`Manual.pdf` in the GOG folder) | - | commands, classes, races, skills, spells, saving |
| Area texts read from memory after a warp (`tools/texts.py`) | - | places, quests, services, prices |
| Corak's Travelogue (cluebook), archive.org | https://archive.org/details/Might_and_Magic_II_Gates_to_Another_World_Cluebook | towns, caverns, castles, quest outline, hirelings |
| Wikipedia | https://en.wikipedia.org/wiki/Might_and_Magic_II:_Gates_to_Another_World | release, plot outline |
