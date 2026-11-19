# Ultima III: Exodus (DOS) - design reference

How the game works, for game designers: rules, formulas, progression, data tables, and quirks, built up while
the game is researched and played. No RAM/ROM addresses here (those live in `../playbook.md`). Screenshots are
the evidence: link them (`../shots/main/<file>.png`; the file name of a shot is in the set's `index.md`).

## Notation and style (binding for every document in this folder)
- **Confidence tags** after the claim they cover:
  **(verified)** seen in play here (name the shot id or the route/checkpoint);
  **(source)** from the manual/FAQ/wiki, link in Sources below;
  **(RAM)** read from or tested through memory while playing (e.g. the HP formula from before/after values);
  **(inferred)** reasoned from observations with a gap;
  **(computed)** worked out here from a stated rule or table;
  **(code)** read from the program (EXODUS.BIN) or its data files with a disassembler, not yet seen in play;
  **(ROM text)** a text or table read from the program or data files.
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
Ultima III: Exodus (Origin Systems, 1983; this is the IBM PC version with CGA graphics) is a party role-playing
game: the player creates up to twenty characters from five races and eleven classes, forms a party of four and
moves it as one icon over the 64x64 world of Sosaria, its townes and castles **(verified)**. Fights move to a
separate tactical screen where every character and monster acts in turn **(verified)**; dungeons are
first-person, eight levels deep and dark without torches **(verified)**. Progress is a chain of hidden
knowledge rather than levels alone: Lord British turns experience into hit points, four marks branded by red-hot
rods deep in the dungeons open the way (force fields, lava, the Silver Snake, levels past five), a whirlpool
leads to the lost land of Ambrosia whose four shrines raise statistics and hide four cards, the Time Lord,
reachable only through a moongate, tells their order, and the cards inserted into Exodus in the Castle of Fire
end the game **(verified with pokes, code)**. Two moons drive the moongates and the brief appearance of the city
of Dawn **(code, verified)**. Saving is Quit & Save on the map of Sosaria; entering any place also writes the
save **(verified)**. No music; PC speaker effects **(source: Wikipedia)**.

## Documents
| Document | Covers |
|---|---|
| [systems.md](systems.md) | game-design lens: index of every feature, system and mechanic, with rule, details and shots |
| [interface.md](interface.md) | UI/UX lens: conventions, inventory of every screen, menu, prompt and element, screen flow |
| [content.md](content.md) | content lens: a reasonable variety of environments, opponents, items, equipment, abilities, people |
| [rules.md](rules.md) | the numbers: combat, magic and classes, shops, chests and traps, dungeons, travel, the quest |
| [findings.md](findings.md) | quirks, exploits, likely bugs |
| [../playbook.md](../playbook.md) | not a design document: addresses, routes, the place and shop squares, the quest chain with code references |
<!-- Add one document per system, e.g. controls-and-feel.md (movement, physics, input), progression.md (levels,
     unlocks, difficulty curve), combat.md, characters.md (stats, leveling), items.md (+ an items table),
     enemies.md (+ table), economy.md (money, shops, prices), world.md (areas, map, secrets), modes.md. -->

## Sources
| Source | URL | Used for |
|---|---|---|
| The game's files (program text, code, map and dungeon files) | `rom/ultima-3.zip` (GOG release) | commands, messages, places, prices, quest rules, talk lines **(ROM text, code)** |
| Wikipedia, Ultima III: Exodus | https://en.wikipedia.org/wiki/Ultima_III:_Exodus | release history, PC version, story outline |
| Web search snippets of walkthroughs | https://wiki.ultimacodex.com/wiki/Ultima_III_walkthrough | card order and the Time Lord (confirmed in play) |
