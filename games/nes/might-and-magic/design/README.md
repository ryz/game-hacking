# Might and Magic: Secret of the Inner Sanctum (NES, USA) - design reference

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
A first-person party RPG on 16x16-square maps: one named hero (a Knight) and up to five fellows hired from the
roster at the town inns explore the five towns of VARN, their caverns, the outdoor sectors, castles and
dungeons, fighting random encounters in menu-driven battles **(verified: Sorpigal, inn, Rabid Jackal fight)**.
The NES version (G-Amusements 1991) replaces the original's six-character creation with a single named hero
plus fifteen pre-made fellows, each living in one of the towns **(verified: inn Member > Add list, RAM)**.
The quest leads to the Inner Sanctum and the impostor king **(ROM text)**. Saving: sign in at an inn
("Push A button and save your adventure.") **(verified)**; one battery save, Continue on the title screen.
Areas: 5 towns, 9 caves, 20 outdoor sectors (A1-E4), 5 castles, 3 castle dungeon levels, 2+2+2 forest/lair/wood
levels, 4 City of Gold (P-Peek) levels, the Astral Plane and the Soul Maze: 55 maps **(ROM data)**.

## Documents
| Document | Covers |
|---|---|
| [maps.md](maps.md) | the 55 maps: list, ids, how walls/doors/specials are stored, how to read the renders in `maps/` |
| [towns.md](towns.md) | inn, blacksmith, market, temple, training, guild, tavern, leprechaun, camp/equipment, character sheet |
| [combat.md](combat.md) | orders, spells, messages, victory, treasure chests and traps, death and game over |
| [story.md](story.md) | the impostor king, the Soul Maze riddle, the Astral Plane, the Inner Sanctum ending |
| [findings.md](findings.md) | quirks and likely bugs |

Still planned: party and classes (six classes, stats, the fifteen fellows), the full spell lists, items.

## Open questions
- Outdoor terrain: decoded ([maps.md](maps.md) section 4). Event squares: decoded for Sorpigal, the Astral Plane,
  Castle Alamar and the Soul Maze by stepping in; the other areas only through their coded exits.

## Sources
See `../playbook.md` Sources.
