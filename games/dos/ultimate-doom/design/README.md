# The Ultimate Doom (DOS) - design reference

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
The Ultimate Doom is a real-time first-person shooter: the marine walks through rooms of varying floor and
ceiling heights, opens doors and presses switches, picks up weapons, ammunition, health, armor and power-ups,
and shoots demons until he reaches the exit of each map **(verified, E1M1 played to the exit)**. Four episodes of
eight maps plus one secret map each (36 maps) **(verified, map list read from the game data)**: Knee-Deep in the
Dead, The Shores of Hell, Inferno and Thy Flesh Consumed **(verified, episode menu)**; the first three end with
boss maps (two Barons of Hell, the Cyberdemon, the Spider Mastermind) **(verified, game data; Cyberdemon and
Spider Mastermind seen in play)**. Five skill levels change which monsters and items are placed
**(verified, skill menu and game data)**. Each map ends with a tally of kills, items, secrets and time against
a par time, then the episode map shows the next level **(verified, E1M1 tally)**. The game can be saved anywhere
in six named slots **(verified, slot 1)**. The fourth episode is what Ultimate Doom added to the 1993 game
**(source: Wikipedia)**.

## Documents
| Document | Covers |
|---|---|
| [systems.md](systems.md) | game-design lens: index of every feature, system and mechanic, with rule, details and shots |
| [interface.md](interface.md) | UI/UX lens: conventions, inventory of every screen, menu, prompt and element, screen flow |
| [content.md](content.md) | content lens: a reasonable variety of environments, opponents, items, equipment, abilities, people |
| [findings.md](findings.md) | quirks, exploits, likely bugs |
<!-- Planned for the capture run: combat.md (weapons, damage, monster behaviour), world.md (maps, secrets,
     doors and keys, hazards), items.md (pickups, power-ups and their durations). -->
<!-- Add one document per system, e.g. controls-and-feel.md (movement, physics, input), progression.md (levels,
     unlocks, difficulty curve), combat.md, characters.md (stats, leveling), items.md (+ an items table),
     enemies.md (+ table), economy.md (money, shops, prices), world.md (areas, map, secrets), modes.md. -->

## Sources
| Source | URL | Used for |
|---|---|---|
| Wikipedia, Doom (1993 video game) | https://en.wikipedia.org/wiki/Doom_(1993_video_game) | release, episode names |
| The game and DOOM.WAD (via `../tools/wadmap.py`) | - | maps, things, skills, specials |
