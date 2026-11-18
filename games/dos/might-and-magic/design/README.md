# Might and Magic Book One: The Secret of the Inner Sanctum (DOS) - design reference

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
A first-person party role-playing game in which up to six characters, picked from a roster of up to eighteen,
explore towns, caverns, wilderness and castles built from maps of 16 by 16 squares, and fight groups of monsters
in turn-based text combat **(verified: Sorpigal, routes in `../playbook.md`)**. Characters are made by rolling
seven statistics from 3 to 18 until the wanted class becomes eligible, then choosing race, alignment, sex and
name **(verified)**; six classes (Knight, Paladin, Archer, Cleric, Sorcerer, Robber) and five races **(verified
on the creation screens)**. Everything is done with letter keys printed on the screen; there is no automap
**(source: manual, "Tips on Mapping")**. Progress is kept only by signing in at the inn of one of the five towns
**(verified)**. Experience comes from fights and quests, but a level is gained only by paying for training in a
town **(verified: level 2 at 1500 experience for a Knight, 25 gold)**. Magic: 47 Cleric and 47 Sorcerer spells
in seven levels, paid with spell points and, for stronger spells, gems **(source: manual)**. The goal is to find
the Inner Sanctum **(source: Wikipedia)**.

## Documents
| Document | Covers |
|---|---|
| [sorpigal.md](sorpigal.md) | the first town: services, prices, what a new party owns |
| [characters.md](characters.md) | creation, the profile, party commands, levels, magic seen |
| [combat.md](combat.md) | encounter options, the combat screen, numbers measured, going down, treasure |
| [world.md](world.md) | the 55 areas, the five towns, cavern, wilderness, castles, the Astral Plane and the ending |
| [findings.md](findings.md) | quirks, exploits, likely bugs |
| [systems.md](systems.md) | game-design lens: every feature, system and mechanic in one table, with shots |
| [interface.md](interface.md) | UI/UX lens: conventions, every screen, menu, prompt and message, the screen flow |
| [content.md](content.md) | variety lens: environments, opponents, items, spells, people, as samples with totals |

Still planned: the 94 spells with what was seen of each, items and prices beyond Sorpigal, how the areas connect.

## Sources
| Source | URL | Used for |
|---|---|---|
| Game manual, second edition (c)1987, in the owner's game folder | - | commands, classes, races, spells, save rule |
| Wikipedia | https://en.wikipedia.org/wiki/Might_and_Magic_Book_One:_The_Secret_of_the_Inner_Sanctum | release, plot outline |
| Play in the emulator, 2026-11-18 | `../playbook.md` routes and checkpoints | everything tagged verified |
