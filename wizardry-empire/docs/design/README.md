# Game design reference (Wizardry Empire, GBC, 1999)

How the game works, recovered from the Japanese ROM (Rev 1): rules, formulas and data tables, written for game
designers. Translation and patch internals are in `docs/re/`. Every number names its source (ROM table or routine
`bank:addr`, or an emulator observation); guesses are marked as guesses.

| Document | Covers |
|---|---|
| [characters.md](characters.md) | races, classes and requirements, creation and bonus points, party record layout, leveling, aging, status ailments, spells and spell slots |
| [items.md](items.md) | item record layout, equipment rules, shops, inn, temple, identification and curses, chests and traps (full item table: items_table.md if split out) |
| [monsters.md](monsters.md) | monster record layout, bestiary, encounters, combat formulas, rewards, summoning / pacts |
| [dungeon.md](dungeon.md) | floors, map format, special squares, events per floor |

Related findings already in `docs/re/`: chest types by floor and the guarded-square rule (`reach.md`), the hidden
developer debug mode (`debug-mode.md`), game task scheduler (`tasks.md`).

Names follow `glossary.md` (the English the patch uses); Japanese names are given next to them.
