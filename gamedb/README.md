# Game database captures

Agents play games you provide as ROMs and capture screenshots of their screens, gameplay and systems for a video
game database. Each game gets a **playbook** (controls, structure, strategy, shortcuts, RAM, sources) so no agent
has to work out the same game twice, and a **screenshot set** whose every image can be reproduced from
power-on by its recorded route.

Platforms: Game Boy and Game Boy Color (gbemu-cli, a headless SameBoy). Other systems plug in as a backend in
`tools/platforms.py`; nothing above it is GB-specific.

## Pipeline
```
ROM --intake.py--> games/<slug>/ --game-scout--> playbook + checkpoints --game-capture--> shots/<set>/ --> commit
```
1. **Intake** (coordinator): `python3 tools/intake.py /path/game.gbc` identifies the ROM (header, SHA-1, CRC32),
   copies it to `rom/<slug>.gbc` (never committed), creates `games/<slug>/` from `games/_template/` and films the
   first 30 s (`work/intake/<slug>/sheet.png`).
2. **Scout** (`skills/game-scout/`): researches the manual, FAQs, TCRF, Data Crystal; verifies boot route,
   controls, RAM and shortcuts in the emulator; writes the playbook and the shot plan.
3. **Capture** (`skills/game-capture/`): plays toward the shot plan with `tools/play.py`, snapping each target,
   verifies that every shot replays (`shoot.py --verify`), publishes the set and updates the playbook.
4. **Review and commit** (coordinator): verify, look at the contact sheet, commit `games/<slug>/`.

## Layout
| Path | What |
|---|---|
| `tools/platforms.py` | platform backends (GB/GBC now) and ROM header identification |
| `tools/emu.py` | games, tokens, macros, checkpoints, settling, one-shot runs |
| `tools/play.py` | persistent play session: do / undo / snap / checkpoint / goto / find (RAM search) |
| `tools/shoot.py` | replay a shot list, verify, publish a set |
| `tools/intake.py` | register a ROM |
| `docs/emulator.md` | **how to drive the emulator** (read first) |
| `docs/capture-guide.md` | what a set must contain, categories, quality rules |
| `games/_template/` | playbook, checkpoints and shot-list templates |
| `games/<slug>/` | `game.json`, `playbook.md`, `checkpoints.txt`, `shots.txt`, `shots/<set>/` |
| `rom/`, `work/` | ROMs, states, caches, scratch (gitignored) |

## A set (`games/<slug>/shots/<set>/`)
`<id>.png` (native resolution, raw framebuffer), `<id>@3x.png` (nearest neighbour), `index.json` (game identity
and per shot: id, category, caption, route, settled, model, ROM SHA-1, date), `index.md`, `sheet.png` (contact
sheet), `shots.txt` (the routes).

## Quick start
```sh
cd gamedb
sh tools/setup_emu.sh
python3 tools/intake.py ~/roms/mygame.gb
python3 tools/play.py start mygame
python3 tools/play.py do "w300,start"
python3 tools/play.py snap title_screen title "Title screen"
python3 tools/shoot.py mygame main --verify
python3 -m pytest -q tests
```
