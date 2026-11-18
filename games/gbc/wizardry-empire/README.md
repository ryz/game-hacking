# Wizardry Empire (Game Boy Color, Starfish, 1999)

Everything this repository holds about the game. Japanese **Rev 1** is the reference ROM (1048576 bytes, SHA-1
`f5f4e8bead0fe45075141133a530a0eb116ea78c`, CRC32 `FA82620F`). No game data is included.

| Part | What it is |
|---|---|
| [`design/`](design/README.md) | Design reference for designers: rules, formulas, item and monster tables, [all 30 floor maps](design/maps/README.md), [quirks and likely bugs](design/findings.md). No addresses. |
| [`tech/`](tech/README.md) | The same systems for engineers: record layouts, RAM, routines, addresses, evidence. |
| [`shots/`](shots/) | Reference screenshot sets: the original and the translation side by side ([rev1_tour](shots/rev1_tour/index.md), `jp_tour`), and a comparison with another fan patch ([compare3](shots/compare3/README.md)). |
| [`saves/`](saves/README.md) | Test saves made by the tools (a powerful party knowing every spell). |
| [`translation/`](translation/README.md) | The unofficial English translation: script, variable-width font engine, patch build chain, tests, reverse-engineering notes, status and history. |
| [`DOCUMENTS.md`](DOCUMENTS.md) | Which document goes where, and the rules all of them follow. |

The game's tools (build, emulator driver, screen tour, reference screenshots, design-table and floor-map
generators) live in `translation/tools/` and run from `translation/`; the translation came first and the rest
grew out of its tooling. The game is not registered with the shared database tools yet (no `game.json`,
playbook or checkpoints): its screenshot sets are made by `translation/tools/shoot.py`.
