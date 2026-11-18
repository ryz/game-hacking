# Might and Magic Book One: The Secret of the Inner Sanctum (Apple II) - design reference

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
The Apple II original (1986) of the game whose DOS port is documented in
[`../../../dos/might-and-magic/design/`](../../../dos/might-and-magic/design/README.md). Rules, classes, spells,
towns and maps are the same game **(inferred: every DOS route that was replayed here led to the same screens,
events and monsters' names; 231 of the DOS set's 250 shots were re-taken on this version)**. This folder holds
the three lenses over the Apple II shots; the detail documents are the DOS version's and are linked from them.
What differs on this version (four disk sides and their prompts, the picture and colours, no "are you ready"
prompt, numbers that came out differently on the same routes) is in the section "Apple II" at the end of each
lens and in `../playbook.md`.

## Documents
| Document | Covers |
|---|---|
| [systems.md](systems.md) | game-design lens: every feature, system and mechanic in one table, with shots |
| [interface.md](interface.md) | UI/UX lens: conventions, every screen, menu, prompt and message, the screen flow |
| [content.md](content.md) | variety lens: environments, opponents, items, spells, people, and the tour of all 55 areas |
| [findings.md](findings.md) | quirks seen on this version |
| DOS detail documents | [characters](../../../dos/might-and-magic/design/characters.md), [combat](../../../dos/might-and-magic/design/combat.md), [world](../../../dos/might-and-magic/design/world.md), [Sorpigal](../../../dos/might-and-magic/design/sorpigal.md), [findings](../../../dos/might-and-magic/design/findings.md) |

Check: `python3 tools/lenses.py apple2/might-and-magic`.

## Sources
| Source | URL | Used for |
|---|---|---|
| Play in the emulator, 2026-11-18 | `../playbook.md` routes and checkpoints | everything tagged verified |
| The DOS version's design reference | `../../../dos/might-and-magic/design/` | rules and numbers not re-measured here |
