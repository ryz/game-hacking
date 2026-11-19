# Wizardry III: Legacy of Llylgamyn (DOS) - design reference

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
A first-person party RPG on the Wizardry I engine: a party of up to six walks a wireframe maze square by square,
fights groups of monsters in menu-driven rounds and returns to the Castle to rest, shop and heal (verified). Its own
idea is the **legacy**: there is no character creation; veterans of Wizardry I or II are moved onto this game's disk
and reborn as their descendants at level 1, keeping name, race, class and honors and choosing a new alignment
(verified, [systems.md](systems.md)). The maze is a volcano climbed upward over six floors that fork after floor 1:
floors 2 and 4 refuse parties with evil members and no good one, 3 and 5 any party with a good member, so the game is
played with two parties; each half ends in a guardian with a crystal, and floor 6, the summit, opens only to a party
carrying one (verified). One good or evil character holding both crystals invokes his own and makes the Neutral
Crystal, which a statue on floor 6 turns into the Orb of Earithin; bringing it to the Castle ends the game with the
Star of Llylgamyn for six characters (verified in play, set `main`, [findings.md](findings.md)). The roster is saved
on the scenario disk whenever the game writes it (verified).

## Documents
| Document | Covers |
|---|---|
| [systems.md](systems.md) | game-design lens: index of every feature, system and mechanic, with rule, details and shots |
| [interface.md](interface.md) | UI/UX lens: conventions, inventory of every screen, menu, prompt and element, screen flow |
| [content.md](content.md) | content lens: a reasonable variety of environments, opponents, items, equipment, abilities, people |
| [findings.md](findings.md) | quirks, exploits, likely bugs |
| [messages.md](messages.md) | every maze message, riddle and answer, with its square |
| [items.md](items.md) | the 103 items by number, quest items, special powers, curses, swaps |
| [maps/floors.txt](maps/floors.txt) | the six floors with walls, doors, fight zones and special squares (`tools/maps.py`) |
<!-- Add one document per system, e.g. controls-and-feel.md (movement, physics, input), progression.md (levels,
     unlocks, difficulty curve), combat.md, characters.md (stats, leveling), items.md (+ an items table),
     enemies.md (+ table), economy.md (money, shops, prices), world.md (areas, map, secrets), modes.md. -->

## Sources
| Source | URL | Used for |
|---|---|---|
| Wikipedia | https://en.wikipedia.org/wiki/Wizardry_III:_Legacy_of_Llylgamyn | year, six-level volcano, descendants at level 1 |
| Apple II manual text (archive.org) | https://archive.org/stream/sir-tech-wizardry-3-a2-v4-ph/components/wizardry%203%20manual_djvu.txt | the rite of passage, the orb and L'kbreth, Pool gold |
| playbook | `../playbook.md` | routes, checkpoints and addresses behind every (verified) claim |
