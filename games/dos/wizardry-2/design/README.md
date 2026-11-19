# Wizardry II: The Knight of Diamonds (DOS) - design reference

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
Wizardry II: The Knight of Diamonds is the second scenario of Wizardry: a first-person party RPG in which six
adventurers explore a wireframe maze from a castle of menus **(verified)**. It is not a new game but a new
scenario for Wizardry I's engine: the Castle (Tavern, Inn, Temple, Boltac's, Edge of Town), the commands, the
combat and the spell lists are Wizardry I's **(verified: same screens and keys)**. What is new: the party must
come from Wizardry I (the Training Grounds cannot create characters; six ready veterans of levels 12-13 come on
the disk) **(verified)**, the maze has six floors of 20 x 20 under the Temple of Gnilda **(verified: disk
data)**, and the goal is a chain: each of floors 1-5 has a guardian before its stairs down (Magic Armor,
Shield, Sword, Helm, Gauntlets) that carries one piece of the Knight of Diamonds' regalia; one character
wearing all five, alone, answers the sphinx's riddle in Gnilda's temple and receives the Staff of Gnilda;
bringing it to the Castle alone ends the game with the Mark of Gnilda for the bearer and the order of Knight of
the City for chosen companions **(verified: play, with shortcuts for the fights)**. Saving is continuous: the
roster on the scenario disk is the save. A run with an imported level 11-13 party is a few hours (inferred).

## Documents
| Document | Covers |
|---|---|
| [systems.md](systems.md) | game-design lens: index of every feature, system and mechanic, with rule, details and shots |
| [interface.md](interface.md) | UI/UX lens: conventions, inventory of every screen, menu, prompt and element, screen flow |
| [content.md](content.md) | content lens: a reasonable variety of environments, opponents, items, equipment, abilities, people |
| [findings.md](findings.md) | quirks, exploits, likely bugs |
| [items.md](items.md) | all 129 items by number, names as shown on the character sheet |
| [maps/floors.txt](maps/floors.txt) | the six floors decoded from the disk: walls, doors, fight zones, special squares |
<!-- Add one document per system, e.g. controls-and-feel.md (movement, physics, input), progression.md (levels,
     unlocks, difficulty curve), combat.md, characters.md (stats, leveling), items.md (+ an items table),
     enemies.md (+ table), economy.md (money, shops, prices), world.md (areas, map, secrets), modes.md. -->

## Sources
| Source | URL | Used for |
|---|---|---|
| Wikipedia | https://en.wikipedia.org/wiki/Wizardry_II:_The_Knight_of_Diamonds | year, designers, six levels, import requirement |
| Data Crystal (NES port) | https://datacrystal.tcrf.net/wiki/Wizardry:_Knight_of_Diamonds_(NES)/Notes | comparison only (the NES port moves the pieces) |
| Wizardry I DOS design reference | ../../wizardry/design/ | the shared engine's rules (character creation, spells, combat, Castle services) |
