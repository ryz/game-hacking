# Beyond Zork: The Coconut of Quendor (DOS) - design reference

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
Beyond Zork is a parser text adventure (Infocom, 1987, Brian Moriarty) with role-playing rules on top: the
player types commands at a `>` prompt, and a character with six attributes (Endurance, Strength, Dexterity,
Intelligence, Compassion, Luck) and an Armor Class fights monsters, gains experience and rises in level
(Level 0 Male Peasant at the start, Level 1 after the first won fight) **(verified, checkpoints `start`,
`vapor_won`)**. The character is chosen in a Character Setup menu before play: a preset, one of six named
presets (Lucky, Tank, Muscles, Nimble, Genius, Saint), a random roll (SPACE rolls again) or points spread by
hand from a 60% potential **(verified, checkpoint `setup`)**. The "enhanced" screen keeps the current room's
description in a framed window under a title bar, draws an auto-map of nearby rooms at the right and shows an
Endurance bar while fighting; MODE switches to a standard screen with a one-line status of all attributes and
exits **(verified)**. Ten function keys are command macros that the player can redefine (DEFINE); SETTINGS,
COLOR (six palettes), ZOOM, PRIORITY, NOTIFY and MONITOR change the display **(verified)**; DEFINE, UNDO and
SAVE/RESTORE to a named file **(verified)**. Parts of the world are generated per game: the moors south of the
village change their room names and layout with the route taken **(verified: Mud Flats/Eyes in one run,
Deep Mist/Odors/Noises in another)**; the goal is to recover the Coconut of Quendor from the Ur-Grues
**(source: Wikipedia, manual)**. Past the moors lies the seaport Mizniaport with a boutique that buys found
items and sells armour (cloak 30 zorkmids) **(verified, `shop_buy`)**, and Gurth City beyond it; a character
dies when Endurance reaches 0 or in the dark (a grue), with RESTORE, RESTART or QUIT offered **(verified,
`gameover_ratant`, `gameover_grue`)**. Details: [systems.md](systems.md), [findings.md](findings.md).

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
| Source | URL | Used for |
|---|---|---|
| Wikipedia | https://en.wikipedia.org/wiki/Beyond_Zork | releases (47, 49, 51, 57 of 1987-12-21), author, features |
| Manual (archive.org full text) | https://archive.org/stream/vgmuseum_infocom_beyondzork-manual/beyondzork-manual_djvu.txt | special commands, function keys, combat, SAVE/UNDO rules |
