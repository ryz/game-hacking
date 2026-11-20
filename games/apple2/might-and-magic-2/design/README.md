# Might and Magic II: Gates to Another World - design reference

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
A first-person party role-playing game: a party of up to six characters (plus hirelings) walks square by square
through 16x16-square areas of the world of Cron - five towns, a 5x4 grid of outdoor areas, caverns, castles,
dungeons and four elemental planes, 60 areas in all **(verified: area warp)** - fighting menu-driven battles
against groups shown as a framed monster portrait and a name list **(verified: `combat`, `sheltem_options`)**,
buying services in towns and following quests; the party can travel through nine centuries, which the final
quest needs **(source: Wikipedia)**. This is the original 1988 Apple II release on six disk sides; the game asks
for each side when an area or picture is on another one **(verified)**. Saving is signing the registry at an
inn **(verified: `signed_in`)**. The rules, quests and content are those of the DOS port documented in
`games/dos/might-and-magic-2/design/` **(inferred: every area id, event square, item id and service checked here
matched; see the playbook)**: the documents below will link there and record the Apple II differences (the
Square Lake gate let an unmarked party meet Sheltem **(verified)**, hi-res pictures, disk prompts).

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
| Wikipedia | https://en.wikipedia.org/wiki/Might_and_Magic_II:_Gates_to_Another_World | release order, time travel, ending outline |
| DOS port's design reference | `games/dos/might-and-magic-2/design/` | rules and content of the same game |
