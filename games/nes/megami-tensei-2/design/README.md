# Digital Devil Monogatari: Megami Tensei II (Famicom, English translation patch) - design reference

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
Megami Tensei II is a role-playing game in which two teenagers, the hero and his girlfriend, are drawn out of a
computer game called Devil Buster into a Tokyo ruined by nuclear war and overrun by demons **(source)**. It begins
inside Devil Buster itself: an overhead maze with stairs between floors and random battles **(verified)**. Exploration
mixes an overhead map with a small first-person view of the corridor ahead **(verified)**. Battles are turn-based
from a first-person view: each round the player chooses FIGHT, FLEE, CHAT (talk to the demon) or AUTO, then a
command per hero **(verified)**. Demons are recruited by talking, summoned from a computer program and fused into
new demons **(source)**. The moon's phase changes as you walk and affects demons **(verified for the change,
source for the effect)**. Battles give experience, money (Makka) and magnetite (MAG) **(verified)**. Choices set an
alignment that decides the ending **(source)**. Progress is kept in battery-backed save slots **(source: ROM text)**.

Creating the party: the player names the hero, the girlfriend and a best friend, then spends 15 points per hero
over five stats (VIT, INT, STR, SPEED, LUK), each starting at 5 **(verified)**. The hero has no magic; the
girlfriend starts with MP 11 **(verified)**.

## Documents
| Document | Covers |
|---|---|
| [world.md](world.md) | Devil Buster floors, the computer room, the shelter, the overworld, saving |
| [combat.md](combat.md) | battle commands, magic, negotiation, rewards, level up, healing, game over |
| [findings.md](findings.md) | quirks, exploits, likely bugs |
<!-- Planned: controls-and-feel.md, characters.md (stats, levels), combat.md, demons.md (negotiation, fusion, moon), world.md (Devil Buster floors, Tokyo areas), economy.md -->
<!-- Add one document per system, e.g. controls-and-feel.md (movement, physics, input), progression.md (levels,
     unlocks, difficulty curve), combat.md, characters.md (stats, leveling), items.md (+ an items table),
     enemies.md (+ table), economy.md (money, shops, prices), world.md (areas, map, secrets), modes.md. -->

## Sources
| Source | URL | Used for |
|---|---|---|
| Wikipedia | https://en.wikipedia.org/wiki/Digital_Devil_Story:_Megami_Tensei_II | story outline, systems, release |
| Patched ROM text | `rom/megami-tensei-2.nes` (decoded) | save prompts, place names |
