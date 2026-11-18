# Deep Dungeon III: Yuushi e no Tabi (Famicom, Japan) - design reference

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
Deep Dungeon III is a first-person dungeon role-playing game: a swordsman hero and up to three companions (hunter,
priest or magician) walk square by square through towns and four dungeons, fighting random battles from a
menu **(verified: party creation, town, underground, battle)**. It is the first game of the series with several
towns and several dungeons - an underground, a cave, a tower and a castle, sixteen floors of 32 by 32 squares in all
**(ROM; names inferred from text)** - each dungeon with a master, and the monster in the castle is said to have
created this world **(ROM text)**. The game ends when the swordsman dies; players share out stat points on
level-up; random encounters stop once the party far outclasses an area; monsters drop gold **(source: Wikipedia)**.
Progress is saved at an inn into one of three party slots **(verified)**.

## Documents
| Document | Covers |
|---|---|
| [maps.md](maps.md) | towns and dungeon floors: square types, stairs, drawn maps in [maps/](maps/) |
| [towns-and-shops.md](towns-and-shops.md) | inn, shops and prices, temple, magic hall, information seller |
| [combat-and-characters.md](combat-and-characters.md) | battle flow, damage samples, stats, levels, companions, game over |
| [story.md](story.md) | story threads, masters, ending |
| [findings.md](findings.md) | quirks, exploits, likely bugs |
<!-- Add one document per system, e.g. controls-and-feel.md (movement, physics, input), progression.md (levels,
     unlocks, difficulty curve), combat.md, characters.md (stats, leveling), items.md (+ an items table),
     enemies.md (+ table), economy.md (money, shops, prices), world.md (areas, map, secrets), modes.md. -->

## Sources
| Source | URL | Used for |
|---|---|---|
| Wikipedia "Deep Dungeon" | https://en.wikipedia.org/wiki/Deep_Dungeon | game-over rule, level-up, encounters, gold |
| ROM text and data | `rom/deep-dungeon-3.nes` (see ../playbook.md) | place names, maps, stairs |
