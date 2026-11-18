# Wizardry II: Knight of Diamonds - The Second Scenario (NES, USA) - design reference

How the game works, for game designers: rules, formulas, progression, data tables, and quirks, built up while
the game is researched and played. No RAM/ROM addresses here (those live in `../playbook.md`). Screenshots are
the evidence: link them (`../shots/main/<id>.png`).

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
Wizardry: Knight of Diamonds is a first-person party dungeon RPG: six adventurers made in the Training Grounds
of the castle of Llylgamyn descend into the Ruins under the Temple of Gnilda, six floors of 20 by 20 squares,
to recover the five pieces of the legendary Knight of Diamonds' regalia and pass seven barriers, which earns the
staff of Gnilda **(source: ROM text)**. The castle is a set of menus (Gilgamesh's Tavern, Adventurer's Inn,
Boltac's Trading Post, Temple of Cant, Edge of Town) **(verified)**; the maze is drawn in first person, wall by
wall, with doors, secret doors, darkness and special squares (stairs, chutes, teleports, pits, spinners,
messages, fixed fights) **(verified for stairs and doors; the rest from the game data)**. The NES version
creates its own characters (no import from Wizardry I) and ships six ready-made level 1 characters **(verified)**.
The roster is kept in battery-backed memory; leaving the game from the Edge of Town saves it **(verified)**.
It runs on the same engine as the NES Wizardry I (`../../wizardry-nes/design/`), so most rules there are likely
to hold here too **(inferred)**.

## Documents
| Document | Covers |
|---|---|
| [maps.md](maps.md) | the six floors drawn from the game data, special squares, connections between floors |
| [findings.md](findings.md) | quirks, exploits, likely bugs |
<!-- To add while playing: castle.md (tavern, inn, shops, temple, training), combat.md, characters.md (races,
     classes, stats), items.md (the Knight's regalia), enemies.md. -->

## Sources
| Source | URL | Used for |
|---|---|---|
| ROM text and data (scout) | `../playbook.md` | story texts, floor data |
| Data Crystal | https://datacrystal.tcrf.net/wiki/Wizardry_II:_Knight_of_Diamonds_(NES) | release facts |
