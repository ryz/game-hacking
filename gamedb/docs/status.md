# Status - game database

Current snapshot; history in `progress-log.md`.

## Ready
- GB/GBC backend (gbemu-cli), ROM intake with header identification and a boot probe.
- NES/Famicom backend (2026-11-17): Mesen libretro core at a pinned commit, driven in-process by `tools/lrcore.py`;
  `.nes` cartridges, 256x240, models ntsc/pal/dendy, savestates, battery saves, full CPU-space peek/poke and PC
  (`tools/mesen-debug.patch`), RAM search, NES Game Genie. First game: Dragon Quest (Famicom, English patch), scouted 2026-11-17. Not set up: Famicom Disk System, second controller, 6-letter Game Genie codes on
  bank-switched games.
- Tokens incl. hold (`right:30`), mash, settle, macros, checkpoints as routes (cached per ROM).
- `play.py`: persistent session with undo, snap (capture + route), checkpoint/goto, RAM search, RAM watches.
- `shoot.py`: replay, `--verify` (pixel-exact reproduction), `--publish`; catalogue index.json/md + contact sheet.
- Skills game-scout and game-capture with agent wrappers; docs emulator.md and capture-guide.md.
- Shortcuts: `set:` (decimal/BCD values), `gs:` GameShark codes held like the device, `freeze:`, ROM variants
  (`rom:` with Game Genie / IPS / bytes, built in work/roms/), downloaded saves (`sav:` from rom/saves/).
- Action sequences (`seq-<action>` sets: strip.png, steps.gif) and GIF clips (`rec:N:K:P`, `play.py record`
  with poster choice).
- Per-game design reference (`games/<slug>/design/`, written by scout and capture agents).
- Network: research hosts allowed in the environment (GameFAQs, TCRF, Data Crystal, StrategyWiki, Wikipedia,
  gamehacking.org, Kodewerx, archive.org). curl reached them from this session; WebFetch did not yet (may need a
  new session). GameFAQs/TCRF answer curl with 403 (bot protection): agents skip refusing sites.
- Tested end to end on SameBoy's cgb-acid2 and gbemu's generated test ROM (not committed).

## Games
| Slug | Title | Playbook | Sets |
|---|---|---|---|
| pokemon-blue | Pokémon Blue Version (USA, Europe) | scouted + first capture 2026-11-15; design docs battle, pokemon, progression, world, economy, findings | main: 92 shots (verified 92/92); sequences seq-fishing (15), seq-fly (9) with GIF clips; saves 01-06 (start, late test, starter lab, Boulder Badge, Lorelei, Hall of Fame) |

## Next
- Pokémon Blue leftovers (optional): trainer "!" spotting, a PC box with Pokémon, Safari BAIT, stone evolution,
  Rocket Hideout; the MID recipe has never been shown on screen.
- `--model sgb` hangs on the SGB transfer screen (Pokémon Blue, pc=20b4): gbemu-cli SGB handshake; until fixed,
  capture in dmg.
- Routes using a macro change silently when the macro is edited: freeze macros once used in published shots
  (copy as a new macro name instead of editing), or store expanded routes in index.json.
- First real game through the whole pipeline; promote its lessons into docs/emulator.md and the skills.
- More platforms: a backend per system in tools/platforms.py (candidates: stable-retro / libretro cores for
  NES, SNES, GBA, Genesis; needs a pip install approved by the owner).
- Optional: a database export step once the target schema is known.
