# Dungeon Master - design reference

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
Dungeon Master is a first-person dungeon crawler that runs in real time: monsters move and attack while the
player decides (source: manual "Game Hints"; verified: `esc` freezes the game, "GAME FROZEN"). The player is
Theron, apprentice of the Grey Lord, who frees up to four champions from mirrors in the Hall of Champions and
leads them down through the dungeon to recover the Firestaff and defeat Lord Chaos (source: Wikipedia, manual).
Everything is done with the mouse on one screen: party bars and hands at the top, the dungeon view at left, the
spell runes, the champions' action buttons and six movement arrows at right; movement also works from the
numeric keypad (verified). Champions are not created but chosen: resurrected as they were, or reincarnated with
a new name and their skills turned into higher statistics (source: manual; verified: both work). Skills (fighter,
ninja, priest, wizard) rise by use, spells are spoken as sequences of runes, light, food and water must be kept
up (source: manual). The dungeon has 14 levels (RAM: [maps.md](maps.md)); the first is the Hall of Champions
(verified: 23 mirrors mapped). The quest ends when Lord Chaos, trapped so that he cannot move, is fused with the
complete Firestaff; Chaos and Lord Order become the Grey Lord again and a final roll shows the champions with
their ranks (verified: the ending reached in the emulator, shots `ending_*`). The game saves to a separate disk that it formats itself; a saved game is
reloaded with RESUME at the entrance (verified). This is version 3.60 for the Amiga (Psygnosis, 1992), with
English, French and German texts on the disk (verified: ROM text).

## Documents
| Document | Covers |
|---|---|
| [systems.md](systems.md) | game-design lens: index of every feature, system and mechanic, with rule, details and shots |
| [interface.md](interface.md) | UI/UX lens: conventions, inventory of every screen, menu, prompt and element, screen flow |
| [content.md](content.md) | content lens: a reasonable variety of environments, opponents, items, equipment, abilities, people |
| [maps.md](maps.md) | all 14 levels from memory: squares, stairs, doors, pits, teleporters, creature groups |
| [findings.md](findings.md) | quirks, exploits, likely bugs |
<!-- Add one document per system, e.g. controls-and-feel.md (movement, physics, input), progression.md (levels,
     unlocks, difficulty curve), combat.md, characters.md (stats, leveling), items.md (+ an items table),
     enemies.md (+ table), economy.md (money, shops, prices), world.md (areas, map, secrets), modes.md. -->

## Sources
| Source | URL | Used for |
|---|---|---|
| Dungeon Master manual (archive.org text) | https://archive.org/stream/DungeonMasterManual/DungeonMasterManual_djvu.txt | controls, champions, magic, inventory, saving |
| Wikipedia | https://en.wikipedia.org/wiki/Dungeon_Master_(video_game) | release, story, endings |
| The game disk (ROM text) | `strings` on the dump | creature, item, action and skill names, dialog texts |
| Playbook | [../playbook.md](../playbook.md) | everything verified in the emulator, with routes |
