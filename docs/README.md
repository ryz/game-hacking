# Documentation (shared tooling)

How the database tooling is used. Documents about one game live in that game's folder (`games/<platform>/<slug>/`).

| File | What |
|---|---|
| [emulator/README.md](emulator/README.md) | **How to drive a game** (read first): routes and checkpoints, tokens, the play loop, shortcuts, saves, RAM. |
| `emulator/<platform>.md` | One file per platform ([gb](emulator/gb.md), [nes](emulator/nes.md), [snes](emulator/snes.md), [sms](emulator/sms.md), [dos](emulator/dos.md), [apple2](emulator/apple2.md), [amiga](emulator/amiga.md)): backend, models, screenshots, memory, cheat formats, limits. |
| [capture-guide.md](capture-guide.md) | What a screenshot set must contain: categories, quality rules, sequences, sets. |
| [status.md](status.md) | Current snapshot: platforms, tools, the generated game table (sets, lenses, open items), next steps. |
| [backlog.md](backlog.md) | Tool work wished for or planned, one list; what was built. |
| [progress-log.md](progress-log.md) | History, newest first, append-only. |
| `archive/` | Superseded documents kept unchanged. |

Tools (`tools/`, run from the repo root):

| Tool | What |
|---|---|
| `setup_emu.sh` | builds the emulators, one per platform |
| `intake.py`, `patch.py` | registers a ROM as a game; applies owner-supplied patches |
| `platforms.py`, `lrcore.py` | platform backends and ROM identification; headless libretro frontend |
| `emu.py` | games, tokens, macros, checkpoints (chained, cached), settling, one-shot runs |
| `play.py` | persistent session for exploring: do / undo / snap / checkpoint / goto / find / text |
| `preview.py` | many candidate routes or a plan file at once, on one sheet or as text |
| `shoot.py` | replays a shot list in parallel, verifies it, publishes a set |
| `cachecheck.py` | proves that cached checkpoints equal a replay from power-on |
| `lenses.py` | coverage of the three lens documents |
| `x3.py` | enlarged copies of shots, on demand |
| `gamestable.py` | writes the game tables in `README.md` and `status.md` |
| `dis6502.py` | 6502 disassembler |
