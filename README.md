# game-hacking

A game database built by taking games apart: for each game, reproducible screenshot sets, a design reference of
how it works, a playbook for automated play and, where there is one, a fan translation with its patch tools and
reverse-engineering notes. No game data is included: everything runs from your own dump, verified by checksum.

## Games

| Game | Platform | What is here |
|---|---|---|
| [Wizardry Empire](games/gbc/wizardry-empire/README.md) | Game Boy Color (Starfish, 1999) | English translation (playable throughout, [status](games/gbc/wizardry-empire/translation/docs/status.md)) with a variable-width font engine; design and technical reference; all 30 dungeon floors mapped; reference screenshots, original next to translation |
| [Pokémon Blue](games/gb/pokemon-blue/playbook.md) | Game Boy | Screenshot sets ([main](games/gb/pokemon-blue/shots/main/index.md), action sequences), design reference, milestone saves |
| [Dragon Quest](games/nes/dragon-quest/playbook.md) | Famicom, with an English translation patch | Screenshot set from the logo to the staff roll ([main](games/nes/dragon-quest/shots/main/index.md)), design reference, password tools |

Platforms: Game Boy / Game Boy Color, NES / Famicom and SNES / Super Famicom cartridges. Another system is one backend class in
`tools/platforms.py`. Current state of the tooling: [docs/status.md](docs/status.md).

## Layout

| Path | What |
|---|---|
| `games/<platform>/<slug>/` | Everything about one game: `game.json` (identity), `playbook.md` (controls, strategy, shortcuts, RAM), `checkpoints.txt`, `shots.txt` and `shots/<set>/` (screenshots), `design/` (design reference), `saves/`, `tools/` (game-specific helpers). A game with a translation or deeper reverse engineering adds `translation/` and `tech/`. |
| `games/_template/` | Starting files for a new game. |
| `tools/` | Shared tooling for every game: register a ROM, drive the emulators, play, capture and verify screenshot sets. |
| `tests/` | Tests for the shared tooling. |
| `docs/` | How the tooling is used: [emulator guide](docs/emulator/README.md) (general rules, plus one file per platform: Game Boy, NES, SNES), [capture guide](docs/capture-guide.md), status and history. |
| `skills/` | Working procedures for the AI agents that do much of the work, each with a feedback log ([index](skills/skill-index.md)). |
| `agent-log/` | One line per agent run: who, what, which files, outcome. |
| `AGENTS.md` | Rules for all work in this repository (also read through `CLAUDE.md`). |
| `rom/`, `work/` | Your ROMs, downloaded saves and patches; states, caches and scratch. Ignored by git. |

## How a game gets into the database

```
ROM --tools/intake.py--> games/<platform>/<slug>/ --scout--> playbook + checkpoints --capture--> shots/<set>/ --> commit
```
1. **Intake:** `python3 tools/intake.py /path/game.gbc` identifies the ROM (header, SHA-1, CRC32), copies it to
   `rom/` (never committed), creates `games/<platform>/<slug>/` and films the first seconds after power-on.
2. **Scout** (`skills/game-scout/`): researches the game, verifies boot route, controls, RAM and shortcuts in
   the emulator, writes the playbook and the shot plan.
3. **Capture** (`skills/game-capture/`): plays toward the shot plan, snaps each target, verifies that every shot
   replays from power-on, publishes the set, extends the design reference.
4. **Review:** the coordinator reruns the verification, looks at the contact sheet and commits.

A set is one PNG per shot (native resolution, raw framebuffer), the same image enlarged 3x in `3x/` (nearest
neighbour, same name), `index.json` (identity and per shot: category, caption, route, model, ROM SHA-1, date),
`index.md`, a contact sheet and the routes in `shots.txt`. File names carry their context
(`docs/capture-guide.md`, "File names"): `<game>_<platform>_<region>_<category>_<id>.png`, e.g.
`dragon-quest_nes_jp_battle_battle_slime.png`.

## Quick start

```sh
sh tools/setup_emu.sh                                   # builds the emulators into tools/ (once)
python3 tools/intake.py ~/roms/mygame.nes --region na  # region of the dump: jp, na or eu
python3 tools/play.py start mygame
python3 tools/play.py do "w300,start"
python3 tools/play.py snap title_screen title "Title screen"
python3 tools/shoot.py mygame main --verify
python3 -m pytest -q tests
```

Building the Wizardry Empire translation: [games/gbc/wizardry-empire/translation/README.md](games/gbc/wizardry-empire/translation/README.md).

## Rules in short
- Never commit game data: ROMs, savestates, downloaded saves or patched builds (`.gitignore` covers them).
- Screenshots are catalogue pieces, not a fair playthrough: saves, codes and RAM pokes are used whenever faster,
  with realistic values on screen. Every shot keeps the route that reproduces it.
- Translations are edited in script files, never in a ROM.
- Every area keeps a current snapshot (`status.md`) and an append-only history (`progress-log.md`).

## Licence

Tools, patches and documentation: MIT. Original game text appears only where a translation needs it to check
its work against the source. Do not share patched ROMs.
