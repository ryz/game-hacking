# Dragon Quest (Famicom, English translation patch) - design reference

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
Dragon Quest is a role-playing game for one player and one hero, seen from above on the overworld, in towns and
in caves, with battles against a single enemy shown from the hero's eyes. **(verified)** `@start`, `@late_battle`
The loop: fight random encounters near the castle for experience (E) and gold (G), buy better equipment, reach
the next town, and travel further as the enemies allow; enemies get stronger with distance from Tantegel
Castle. **(source)** The goal is to defeat the Dragon King, whose castle is visible across the water from the
first step outside. **(verified)** `@late_overworld`
What makes this first version distinctive: every action is a menu command, including taking stairs (Stairs),
opening doors (Door), opening chests (Take) and talking, which asks for a compass direction because the hero
never turns. **(verified)** `@start` Progress is kept as a 20-symbol password told by the king; the level and
all stats are rebuilt from experience when it is entered, and the hero's name keeps only part of each symbol.
**(verified)** `@late` The hero has ten spells, learned by level, and one weapon, one armour and one shield at a
time. **(verified)** `@late` Stats window. Length: one continuous world, about ten hours of play without
shortcuts. **(source)**

## Documents
| Document | Covers |
|---|---|
| [findings.md](findings.md) | quirks, exploits, likely bugs |
| [controls-and-commands.md](controls-and-commands.md) | the command windows, what each command does (started) |
| [combat.md](combat.md) | battle flow, enemies met, the Dragon King, death |
| [items-and-shops.md](items-and-shops.md) | the king's gifts, shop and inn prices, spells seen in use, levels |
| [world.md](world.md) | places and their overworld tiles, cave light, roofs, the rainbow bridge, the ending |
| progression.md (to write) | experience table, spells by level, the critical path |
| password.md (to write) | what the Return Spell stores and what it drops |

## Sources
| Source | URL | Used for |
|---|---|---|
| Wikipedia, Dragon Quest (video game) | https://en.wikipedia.org/wiki/Dragon_Quest_(video_game) | release, differences to Dragon Warrior |
| Data Crystal, Dragon Warrior RAM map | https://datacrystal.tcrf.net/wiki/Dragon_Warrior/RAM_map | item and spell lists |
