# game-hacking

Game-hacking projects, one directory per game: fan translations, reverse engineering, ROM patches and the tools
that build them, and game-design documentation worked out from the code. No game data is included: every project
builds from your own dump of the original, verified by checksum.

## Projects

| Project | Platform | What it is | Status |
|---|---|---|---|
| [Wizardry Empire](wizardry-empire/README.md) | Game Boy Color (Starfish, 1999) | Unofficial English translation of the Japanese Rev 1, with a variable-width font engine, reverse-engineering notes, a design reference for the game's rules and all 30 dungeon floors mapped | Playable in English throughout; polish and speed work ongoing ([status](wizardry-empire/docs/status.md)) |

### Wizardry Empire at a glance
- **Patch:** `wizardry-empire/tools/build.py` turns the Japanese ROM into an English build and an IPS patch; the
  English text lives in `script/*.json` next to the Japanese.
- **Engine:** a variable-width font (mixed case, proportional) drawn into a tile pool at run time
  ([VWF notes](wizardry-empire/docs/re/vwf.md)).
- **Docs:** [design reference](wizardry-empire/docs/design/README.md) (rules, formulas, item and monster tables,
  [floor maps](wizardry-empire/docs/design/maps/README.md), [quirks and likely bugs](wizardry-empire/docs/design/findings.md)),
  [technical reference](wizardry-empire/docs/tech/README.md) (the same systems with ROM addresses and evidence),
  [reverse-engineering notes](wizardry-empire/docs/re/README.md).
- **Screenshots:** reference sets with the original next to the translation, e.g.
  [rev1_tour](wizardry-empire/docs/shots/rev1_tour/index.md) and a three-way comparison with another fan patch,
  [compare3](wizardry-empire/docs/shots/compare3/README.md).

## Layout

| Path | What |
|---|---|
| `<project>/` | Everything for one game: `tools/`, `docs/`, `tests/`, `asm/`, `script/` (as the project needs); its own README |
| `skills/` | Working procedures for the AI agents that do much of the work (translator, tracer, playtester, ...), each with a feedback log; index in `skills/skill-index.md` |
| `agent-log/` | One line per agent run: who, what, which files, outcome |
| `AGENTS.md` | Rules for all projects and agents (also read by `CLAUDE.md`) |

## Rules in short
- Never commit game data: ROMs, savestates, saves or patched builds (`.gitignore` covers them).
- Translations are edited in each project's script files, never in a ROM.
- Every project keeps a current snapshot (`docs/status.md`) and an append-only history (`docs/progress-log.md`).

## Getting started (Wizardry Empire)

```sh
cd wizardry-empire
cp /path/to/your/dump.gbc rom/wizardry_empire_j.gbc    # Japanese Rev 1, SHA-1 in rom.sha1
python3 tools/build.py                                   # -> build/wizardry_empire_en.gbc + .ips
python3 -m pytest -q tests
```

Optional: `sh tools/setup_emu.sh` builds a headless emulator for the automated checks
(`python3 tools/check.py`: build, tests, screen tour and pixel diff).

## Licence

Tools, patches and documentation: MIT. Original game text appears only where a project needs it to check its work
against the source. Do not share patched ROMs.
