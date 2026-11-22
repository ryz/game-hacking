# WASTELAND - design reference

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
Wasteland is a post-apocalyptic party role-playing game: a squad of up to four created Desert Rangers (seven
with hired followers) explores a top-down world map of the American south-west in 2087 and enters towns and
buildings drawn as top-down maps **(source)**. Play is keyboard-driven: one key per step and one letter per
command (Use, Enc, Order, Disband, View, Save, Radio) **(verified, checkpoint `start`)**. Characters have seven
attributes (ST, IQ, LK, SP, AGL, DEX, CHR), CON as hit points, a rank and bought skills such as Clip pistol,
Rifle and Perception **(verified, `party`)**; skills are used on the world as well as in fights (source).
Combat is menu-driven in rounds: each member picks Run, Use, Hire, Evade, Attack, Weapon or Load/Unjam, then the
round is played out as text **(verified, `fight`)**. A game clock runs in the corner and advances with steps and
rests **(verified)**. The game saves to its play disks: by command, and when a location is entered or left
**(source)**; the C64 release needs play copies of its four disk sides, made by its own Utils menu
**(verified: the masters are refused as play disks)**. Length: a dozen major areas from Highpool to Base Cochise
**(source)**.

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
