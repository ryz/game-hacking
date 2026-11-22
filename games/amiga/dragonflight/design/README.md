# Dragonflight - design reference

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
Dragonflight is a party role-playing game for four fixed heroes (Bladus, Rinakles, Dobranur, Andariel)
**(verified)**: towns and the land are shown from above, a square at a time, and dungeons in first person
("Forward", "Turn left", "Upstairs", "Downstairs" messages in the game text) **(RAM, inferred for dungeons)**.
Fights are turn-based on a grid with a side view of the combatants **(source: Wikipedia)**. The game is played
with the mouse: four portraits (status), a message scroll and an icon grid of commands that changes with the
place (town: magic, speak, use/open, look; land: magic, a second sword command, ship, enter, camp, search,
disk) **(verified)**; the right button swaps the icon grid for eight direction arrows and a rest icon
**(verified)**, the numeric keypad moves too **(verified)**. Time passes while the player waits ("Pass")
**(verified)**. The quest: an old sage gives the party a Ring of Stasis (it revives its bearer) and one part of
the Great Map; the other eleven parts must be found, and magic and the dragons, which have left the world,
brought back **(verified intro text; source: Wikipedia for the dragons)**. Saving: the disk icon on the land
writes one saved game to Disk B; "Old game" on the Main Menu loads it **(verified)**.

Systems named in the game text **(RAM)**: spells learned from scrolls and prepared before use, potions that can
be mixed ("Own potion mixed!"), the Staff of Stone loaded with gems, the ELTAM, doors to listen at, trapped
chests (poisoned needle, bolt of lightning), fleeing monsters (killing one costs character points), gold and
experience after a fight, ships, camps, food. Opponents named: Orc, Skeleton, Ghost, Bear, Snake, Beast,
Gnoll, Troll, Ghoul, Energyball, Balron, Statue, Guardian, Unicorn, Shadow **(RAM)**.

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
| Source | Used for |
|---|---|
| [Wikipedia: Dragonflight (video game)](https://en.wikipedia.org/wiki/Dragonflight_(video_game)) | credits, platforms, view types, combat style, premise |
| Game text read from memory in the emulator (scout 2026-11-22) | command names, messages, opponent names |

