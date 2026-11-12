# Game systems - technical reference

How Wizardry Empire's game systems are implemented in the Japanese Rev 1 ROM: record layouts, RAM, routines and
data tables at their addresses, with how each fact was established (code reading, data, emulator runs). This is
the source of truth for the numbers in `../design/` (the same systems explained for designers, without addresses).
Text and display internals of the translation patch are in `../re/`. Conventions: `../README.md`.

| File | Covers | Design counterpart |
|---|---|---|
| [characters.md](characters.md) | Races, creation, party record layout, classes, EXP and leveling, aging, statuses, spell records, learning, slots, pacts | `design/characters.md`, `design/spells.md` |
| [items.md](items.md) | Item record layout, equipment rules, item use, weapon combat code, identification, shop, inn, temple, gold, chests and traps | `design/items.md`, `design/town.md`, `design/combat.md` |
| [monsters.md](monsters.md) | Monster record layout, encounters, AI, monster attacks, escape, rewards, pacts, RNG | `design/monsters.md`, `design/combat.md` |
| [dungeon.md](dungeon.md) | Map storage and cell format, square types, event catalogue, floors | `design/dungeon.md` |

Data tables generated from the ROM: `python3 tools/designtables` (writes `design/items_table.md`,
`design/monsters_table.md`; generators in `tools/designtables/`).

These four documents were written as one "design reference" on 2026-11-12 and moved here when the design docs
were split off; some still use the older section wording.
