# Doom (DOS, registered 1.1) - design reference

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
First-person shooter in real time: the marine walks through 2.5D maps (rooms at different heights, lifts,
doors, nukage and lava floors), shoots demons with up to eight weapons and finds the exit switch of each map
**(verified, E1M1 played to its exit)**. Version 1.1 (December 1993) has three episodes of eight maps plus a
secret ninth (27 maps: Knee-Deep in the Dead, The Shores of Hell, Inferno) **(verified: WAD, episode menu)**
and four skills: I'm too young to die, Hey, not too rough, Hurt me plenty, Ultra-Violence; Nightmare! came
later **(verified, skill menu)**. Saves anywhere into six named slots **(verified)**. Between maps a tally
(kills, items, secrets, time, par) and the episode map ("Entering ...") **(verified)**. The same game as The
Ultimate Doom 1.9 (`games/dos/ultimate-doom/design/`) in its first three episodes, with small map edits
(E1M1, E1M4, E1M5, E1M8, E2M2 and others differ in their map data) **(verified, WAD comparison)**; the
capture run fills the lenses by comparison.

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
