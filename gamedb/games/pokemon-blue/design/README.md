# Pokémon Blue Version - design reference

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
Pokémon Blue Version is a top-down, turn-based role-playing game about catching, raising and battling creatures
called Pokémon **(source)**. The player (named by the player; here ryz) leaves his house in Pallet Town, receives
a first Pokémon from Professor Oak, and travels through the Kanto region to win the badges of eight Gym Leaders,
then defeats the Elite Four and the Champion, his rival **(source)**. The core loop is exploring routes, towns
and dungeons, meeting wild Pokémon in tall grass, caves and water, catching them with Poké Balls, and battling
trainers one Pokémon at a time with up to four moves each **(source)**; parties hold six Pokémon, the rest are
stored in a PC **(source)**. A second goal is the Pokédex: 151 species, some only obtainable by trading with
Pokémon Red **(source)**. Progress is saved to one battery-backed file from the menu at any point in the field
**(verified: save_prompt)**. Version facts: Blue offers BLUE/GARY/JOHN as player names and RED/ASH/JACK for the
rival **(verified: oak_name_menu, NEWGAME route)**.

## What research and verification established so far
- The new-game flow: title, NEW GAME / OPTION, Professor Oak's speech, naming the player and the rival, then
  control in the player's bedroom with no Pokémon and 3000 money **(verified: checkpoint `start`)**.
- Options: text speed FAST/MEDIUM/SLOW (default MEDIUM), battle animation ON/OFF, battle style SHIFT/SET
  **(verified: options)**.
- A Pokémon's stats follow ((base + individual value) x 2 + a training bonus) x level / 100 + 5, HP + level + 10;
  the game stores the results and shows them on the summary screen **(source)**; a check against a real level-up
  is still open.
- Pokémon Centers heal the whole party for free **(verified: pokecenter_heal)**; every Center's second desk is the
  Cable Club for link trades and battles **(verified: cable_club)**.
- The trainer card shows name, money, play time and the eight badge slots **(verified, `late` checkpoint)**.

## Documents
| Document | Covers |
|---|---|
| [findings.md](findings.md) | quirks, exploits, likely bugs |
| battle.md (to write) | turn order, damage, types, status, catching odds |
| pokemon.md (to write) | species, stats, growth rates, evolution, learnsets |
| progression.md (to write) | badges, HMs and what they unlock, story order |
| world.md (to write) | towns, routes, dungeons, encounter areas |
| economy.md (to write) | money, prize money, marts and prices |
<!-- Add one document per system, e.g. controls-and-feel.md (movement, physics, input), progression.md (levels,
     unlocks, difficulty curve), combat.md, characters.md (stats, leveling), items.md (+ an items table),
     enemies.md (+ table), economy.md (money, shops, prices), world.md (areas, map, secrets), modes.md. -->

## Sources
| Source | URL | Used for |
|---|---|---|
| pret/pokered disassembly | https://github.com/pret/pokered | ids, data tables, game structure |
| Wikipedia | https://en.wikipedia.org/wiki/Pok%C3%A9mon_Red_and_Blue | release, overview |
