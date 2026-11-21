# Phantasie - design reference

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
Phantasie is a party role-playing game: the player creates up to six adventurers in a town Guild (five races
plus "random creature", six classes, rolled attributes) **(verified: route of `guild_created`)**, equips them in
town (Armory, Bank, Inn, Mystic) **(verified)** and leads them square by square across the top-down wilderness
of the Isle of Gelnor **(verified)** and through dungeons **(source)**. Fights are menu-driven: the party first
chooses an approach (beg mercy, threaten, greet, fight, flee), then each member an attack style or a spell
**(source)**. Experience becomes levels only by paid training at a Guild **(source)**. The goal is to defeat
the Black Knights and their master Nikademus; 20 scrolls tell the story **(source)**. Saving happens only in
towns and divides the carried gold back into the members' bank accounts **(verified: `saved_start`)**. Several
parties can exist side by side in different towns **(source; verified: the disk holds a second party in
Pineville)**.

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
| Commodore 64 manual with supplement | https://archive.org/details/Phantasie_I_1986_SSI | races, classes, towns, combat options, saving (scout 2026-11-21) |
