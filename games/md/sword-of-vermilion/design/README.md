# SWORD OF VERMILION - design reference

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
Action role-playing game (Sega AM2, 1989/1990) told from four views **(source: Wikipedia)**: top-down towns
with houses, shops, an inn, a tavern and a church entered by walking into their doors **(verified: Wyclif,
checkpoints `tavern`, `church`)**; a first-person overworld and caves split into 16x16 maps **(source:
TheStarbird walkthrough, via search snippet)** with random encounters that switch to side-view real-time
battles **(source: Wikipedia)**; side-view boss fights **(source)**. One hero, the prince (named by the player,
**ryz** here), raised by the knight Blade in Wyclif; he gathers the eight Rings of Good and the Sword of
Vermilion against King Tsarkon of Cartahena **(source: Wikipedia; ROM text: ring and sword names)**.
Fourteen towns and villages from Wyclif to Cartahena **(ROM text: town name table)**. Field commands on C:
Talk, Magic, Item, Equip, Str (status), Seek, Open, Take **(verified)**. Character values: Level, EXP, Next
level EXP, HP/MHP, MP/MMP, STR, AC, INT, DEX, LUK, KIM (money) **(verified: status screen)**. Saving at
churches into three slots ("Saved Game 1-3"); the church also removes curses and cures poison **(verified:
checkpoints `church_menu`, `saved`, `continue`)**. The opening is gated: houses and shops stay locked
("Sorry, you can't open that!") until the prince has heard Blade's last words **(verified)**.

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
| Wikipedia | https://en.wikipedia.org/wiki/Sword_of_Vermilion | release, developer, story frame, the four views |
| ROM text (this dump) | `strings` over `rom/sword-of-vermilion.md` | menu words, town, item, ring, sword, armour, magic names |
