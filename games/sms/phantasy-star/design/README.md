# Phantasy Star - design reference

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
Phantasy Star is a turn-based science-fiction RPG for the Sega Master System (Japan 1987, export 1988) **(source)**.
The player leads Alis, whose brother Nero is killed by the tyrant Lassic's robotcops in the opening
**(verified: intro, checkpoint `start`)**, across three planets of the Algol system (Palma, Motavia, Dezoris)
**(source)**. Towns and planet surfaces are seen from above and walked tile by tile **(verified)**; caves,
towers and dungeons switch to a first-person view with smoothly scrolled 3D corridors **(verified: checkpoint
`dungeon`)**; battles are first person against an animated monster, with ATTK, MAGC, ITEM, TALK and RUN for
each party member **(verified: `battle`)**. Beaten monsters give experience and sometimes a treasure chest with
meseta, or a trap **(verified for meseta; source for traps)**. The party grows to four fixed characters: Alis,
the talking cat Myau, the warrior Odin and the esper Noah **(source)**; nobody is named by the player
**(verified)**. Vehicles (Landrover, Hovercraft, Ice Digger) and a spaceport connect the world **(source; item
names verified)**. Dark caves cannot be entered without light (a Flash or the Magic Lamp) **(verified for Flash)**.
The game saves to one of five slots anywhere outside battle **(verified)**.

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
| US manual (OCR) | https://archive.org/stream/Phantasy_Star_1988_U/Phantasy_Star_1988_U_djvu.txt | controls, menus, commands, characters, planets, vehicles, spells |
| Wikipedia | https://en.wikipedia.org/wiki/Phantasy_Star_(video_game) | release, staff, outline of the story |
