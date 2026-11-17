# Digital Devil Monogatari: Megami Tensei (Famicom, English translation patch) - design reference

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
A first-person dungeon role-playing game: two fixed heroes, Nakajima and Yumiko, explore a labyrinth floor by
floor in turn-based steps and fight random encounters in turn-based battles **(verified)**. Demons can be
persuaded to join, kept in a computer ("Comp": Call / Bind / Order) and summoned to fight; demons do not gain
levels but are fused into new ones at the Heretic **(source; menu verified)**. The moon phase, shown on screen
at all times ("FULL MOON"), changes how demons behave **(source; display verified)**. Before play each hero
gets 15 points to spread over five stats (STR, WIS, ATT, AGI, LUK), all starting at 5 **(verified)**. The
labyrinth is Daedalus; the start floor (8F) is the town of Micom, and play goes downwards (stairs to 7F,
verified); six bosses: Tyrant Minotaur, Medusa, Loki, Hecate, Set, and the Dark Lord Lucifer **(source: game
text)**. Progress is kept by passwords, given by the sage in Micom **(source: game text)**.

## Documents
| Document | Covers |
|---|---|
| [findings.md](findings.md) | quirks, exploits, likely bugs |
| characters.md (to write) | the two heroes, stat allocation (15 points over STR/WIS/ATT/AGI/LUK, base 5), levels, Yumiko's spells (Mappa 2 MP at level 1, verified) |
| combat.md (to write) | Fight / Run / Order / Auto, per-hero actions (Fight/Comp/Guard, Fight/Magic/Guard), damage |
| demons.md (to write) | negotiation, Comp (Call / Bind / Order), fusion at the Heretic, moon phases |
| world.md (to write) | Daedalus floors, Micom (8F), Bien (the moving town), shops, healing |
| passwords.md (to write) | the sage, the 40-character password, what it keeps (dead demons are lost: source) |
<!-- Add one document per system, e.g. controls-and-feel.md (movement, physics, input), progression.md (levels,
     unlocks, difficulty curve), combat.md, characters.md (stats, leveling), items.md (+ an items table),
     enemies.md (+ table), economy.md (money, shops, prices), world.md (areas, map, secrets), modes.md. -->

## Sources
| Source | URL | Used for |
|---|---|---|
| Wikipedia | https://en.wikipedia.org/wiki/Digital_Devil_Story:_Megami_Tensei | demons, fusion, moon, passwords |
| Game text (English patch) | decoded from the ROM, see ../playbook.md | place and boss names, the sage |
