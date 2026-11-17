# Documentation (shared tooling)

How the database tooling is used. Documents about one game live in that game's folder (`games/<slug>/`).

| File | What |
|---|---|
| [emulator/README.md](emulator/README.md) | **How to drive a game** (read first): routes and checkpoints, tokens, the play loop, shortcuts, saves, RAM. |
| [emulator/gb.md](emulator/gb.md) | Game Boy / Game Boy Color: backend, models, screenshots, memory, cheat formats. |
| [emulator/nes.md](emulator/nes.md) | NES / Famicom: backend, models, screenshots, memory, cheat formats, limits. |
| [capture-guide.md](capture-guide.md) | What a screenshot set must contain: categories, quality rules, sequences, sets. |
| [status.md](status.md) | Current snapshot of the tooling: what works, known issues, next steps. |
| [progress-log.md](progress-log.md) | History, newest first, append-only. |

Tools (`tools/`, run from the repo root):

| Tool | What |
|---|---|
| `setup_emu.sh` | builds the emulators (gbemu-cli for Game Boy, Mesen core for NES) |
| `intake.py` | registers a ROM as a game |
| `platforms.py` | platform backends and ROM header identification |
| `lrcore.py` | minimal headless libretro frontend used by the NES backend |
| `emu.py` | games, tokens, macros, checkpoints, settling, one-shot runs |
| `play.py` | persistent play session: do / undo / snap / checkpoint / goto / find (RAM search) |
| `shoot.py` | replays a shot list, verifies it, publishes a set |
