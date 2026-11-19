# Wizardry II: The Knight of Diamonds - design reference

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
Wizardry II: The Knight of Diamonds, the 1982 Apple II original (version PV3S2V1 of 10 March 1982), is the
second scenario of the first-person party role-playing game Wizardry. It has no character creation: a party of
six must be moved over from a Wizardry I scenario disk with the boot menu's transfer utility, one character at a
time **(verified)** checkpoint `start`. From the castle of Llylgamyn (menus of text: tavern, inn, temple, trading
post, training grounds) the party goes down six floors of 20 by 20 squares drawn as a small wireframe view
**(verified)** `maze1`. Each of the first five floors keeps its stairs down behind an animated piece of the
Knight of Diamonds' armor, which must be beaten and then worn **(verified)** `guard1` to `guard5`. One character
alone, wearing all five, answers the riddle of the sphinx at Gnilda's temple and is given the Staff of Gnilda;
carrying it up to the castle ends the quest with the rank of Keeper of the Holy Staff and five knighthoods to
hand out **(verified)** `gnilda_test`, `staff`, `ending`, `knights`. The roster on the scenario disk is the only
save **(verified)** saves 01, 02.
This folder starts the three lens documents for the Apple II version. The six floors are the DOS port's
**(verified by decoding both: one number differs)**; the DOS design documents (`../../../dos/wizardry-2/design/`)
hold the detailed rules and tables and are linked from the rows here. Names in the Shots columns are checkpoint
names of the scout (`../checkpoints.txt`) until the capture run replaces them with shot ids.

## Documents
| Document | Covers |
|---|---|
| [systems.md](systems.md) | game-design lens: index of every feature, system and mechanic, with rule, details and shots |
| [interface.md](interface.md) | UI/UX lens: conventions, inventory of every screen, menu, prompt and element, screen flow |
| [content.md](content.md) | content lens: a reasonable variety of environments, opponents, items, equipment, abilities, people |
| [findings.md](findings.md) | quirks, exploits, likely bugs |
| [maps/floors.txt](maps/floors.txt) | the six floors as text maps with their special squares, decoded from the scenario disk (`../tools/maps.py`) |
| DOS: [systems](../../../dos/wizardry-2/design/systems.md), [interface](../../../dos/wizardry-2/design/interface.md), [content](../../../dos/wizardry-2/design/content.md), [items](../../../dos/wizardry-2/design/items.md), [findings](../../../dos/wizardry-2/design/findings.md) | the detail documents of the DOS port (same floors and quest, other screens, keys and wording) |
| Apple II Wizardry I: [systems](../../wizardry/design/systems.md), [interface](../../wizardry/design/interface.md) | the same program family: castle, camp, maze and battle screens described there apply here |
<!-- Add one document per system, e.g. controls-and-feel.md (movement, physics, input), progression.md (levels,
     unlocks, difficulty curve), combat.md, characters.md (stats, leveling), items.md (+ an items table),
     enemies.md (+ table), economy.md (money, shops, prices), world.md (areas, map, secrets), modes.md. -->

## Sources
| Source | URL | Used for |
|---|---|---|
| the game disks | `rom/apple2/wizardry-2.zip` (not committed) | utility prompts (program text), maps, item and monster tables, roster |
| DOS port documents | `games/dos/wizardry-2/design/` | rules and tables, re-checked where a row says so |
| scout's playbook | `../playbook.md` | routes, checkpoints, what was verified on 2026-11-19 |
