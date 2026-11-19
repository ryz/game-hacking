# Wizardry: Proving Grounds of the Mad Overlord (DOS) - design reference

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
Wizardry I is a first-person party role-playing game: the player creates up to six adventurers in the Training
Grounds, forms a party in Gilgamesh's Tavern and leads it down a ten-floor maze of 20 x 20 squares under the
castle of the Mad Overlord Trebor, drawn as white wireframe corridors (verified: `gameplay_maze_f1_start`).
The loop is: descend, fight groups of monsters in turn-based rounds where every member gets an order (fight,
parry, spell, use item, run), open the chests they leave, climb back to rest at the Adventurer's Inn (where
levels are gained), buy equipment at Boltac's, revive the dead at the Temple of Cant (verified: `inn_levelup`,
`temple_healed`). The goal is Werdna's amulet on floor 10; carrying it back up to the castle gives
the ending, 50,000 gold and experience and the Chevron of Rank (verified: `ending_congratulations`).
Characters live on the scenario disk (SAVE1.DSK): the game saves the roster itself and keeps it when the
program is left with L)eave game (verified). This is the IBM PC version (1984 PC booter) as re-released in 1998
with a DOS loader that maps the floppy drives to two disk images (verified, playbook).

## Documents
| Document | Covers |
|---|---|
| [systems.md](systems.md) | game-design lens: index of every feature, system and mechanic, with rule, details and shots |
| [interface.md](interface.md) | UI/UX lens: conventions, inventory of every screen, menu, prompt and element, screen flow |
| [content.md](content.md) | content lens: a reasonable variety of environments, opponents, items, equipment, abilities, people |
| [items.md](items.md) | all 100 items by number with Boltac's prices (names read on screen) |
| [findings.md](findings.md) | quirks, exploits, likely bugs |
| [maps/floors.txt](maps/floors.txt) | all ten floors as text maps with every special square (stairs, teleports, pits, spinners, darkness, rock, anti-magic, messages, fixed fights, elevators), decoded from the game disk by `../tools/maps.py` |
<!-- Add one document per system, e.g. controls-and-feel.md (movement, physics, input), progression.md (levels,
     unlocks, difficulty curve), combat.md, characters.md (stats, leveling), items.md (+ an items table),
     enemies.md (+ table), economy.md (money, shops, prices), world.md (areas, map, secrets), modes.md. -->

## Sources
| Source | URL | Used for |
|---|---|---|
| Wikipedia | https://en.wikipedia.org/wiki/Wizardry:_Proving_Grounds_of_the_Mad_Overlord | release years, races and classes |
| MobyGames (search summary) | https://www.mobygames.com/game/1367 | the 1998 Ultimate Wizardry Archives ship the booter games as disk images with a loader |
| the game itself | `rom/wizardry.zip` | everything tagged (verified) or (RAM); floor data decoded from WIZ1.DSK |
