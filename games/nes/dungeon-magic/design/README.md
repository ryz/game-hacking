# Dungeon Magic: Sword of the Elements (NES, USA) - design reference

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
Dungeon Magic: Sword of the Elements is a single-character, real-time, first-person role-playing game: the hero
walks a grid one square at a time, turning in 90-degree steps, while people in towns and monsters in the field
move on their own **(verified)** (movement and wandering townsfolk seen at checkpoint `start`). Towns, the
castle and dungeons are 16 by 16 square maps with walls between squares; the outdoors is made of 16 by 16
field sections joined at their edges **(verified)** (Granville, its north field and Granville Castle). The quest
is to find five elemental swords (Earth, Water, Fire, Wind/Sky, Fairy) and join them to defeat the dark
overlord Darces **(source)** (Wikipedia; in-game text). Magic is built from runes learned by becoming the
apprentice of a wizard of each element; one to three runes make a spell and spells cost hit points, not magic
points **(source)** (Wikipedia). Levels are granted by wise men once enough experience is earned, food and
water run down at camp and inns, and a night at an inn is the only way to save **(source)** (Wikipedia; inn save
**(verified)**: the title offers "Continue your adventure" afterwards).

The screen is split into a first-person view (with HP) and a status panel: portrait, condition, experience,
level, gold, and five command icons - Fight (weapons and armour), Item, Spell (rune slots), Use (open doors, take
boxes) and Camp (weight, food, water) **(verified)** (`hud_pause`, `spell_panel`). Start pauses the game and is
the only way to change the active command **(verified)**.

## Documents
| Document | Covers |
|---|---|
| [findings.md](findings.md) | quirks, exploits, likely bugs |
| [maps.md](maps.md) | all 39 floors (towns, castle, forests, dungeons) and the overworld, drawn from the game data |
| [magic.md](magic.md) | wizards, apprenticeship, the Spell panel, casting controls, HP cost |
| [progression.md](progression.md) | levels from wizards, real-time combat, game over |
| economy.md (planned) | shops, inn (2 gold a night **(verified)**, `inn_morning`: 214 to 212), item shop jug 56 gold each **(verified)** (`shop_buying`), food and water |
<!-- Add one document per system, e.g. controls-and-feel.md (movement, physics, input), progression.md (levels,
     unlocks, difficulty curve), combat.md, characters.md (stats, leveling), items.md (+ an items table),
     enemies.md (+ table), economy.md (money, shops, prices), world.md (areas, map, secrets), modes.md. -->

## Sources
| Source | URL | Used for |
|---|---|---|
| Wikipedia | https://en.wikipedia.org/wiki/Dungeon_Magic:_Sword_of_the_Elements | release, story, magic system, saving |
| In-game text (ROM) | `../playbook.md` (ROM text) | place names, quest |
