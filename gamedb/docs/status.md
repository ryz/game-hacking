# Status - game database

Current snapshot; history in `progress-log.md`.

## Ready
- GB/GBC backend (gbemu-cli), ROM intake with header identification and a boot probe.
- Tokens incl. hold (`right:30`), mash, settle, macros, checkpoints as routes (cached per ROM).
- `play.py`: persistent session with undo, snap (capture + route), checkpoint/goto, RAM search, RAM watches.
- `shoot.py`: replay, `--verify` (pixel-exact reproduction), `--publish`; catalogue index.json/md + contact sheet.
- Skills game-scout and game-capture with agent wrappers; docs emulator.md and capture-guide.md.
- Shortcuts: `set:` (decimal/BCD values), `gs:` GameShark codes held like the device, `freeze:`, ROM variants
  (`rom:` with Game Genie / IPS / bytes, built in work/roms/), downloaded saves (`sav:` from rom/saves/).
- Per-game design reference (`games/<slug>/design/`, written by scout and capture agents).
- Network: research hosts allowed in the environment (GameFAQs, TCRF, Data Crystal, StrategyWiki, Wikipedia,
  gamehacking.org, Kodewerx, archive.org). curl reached them from this session; WebFetch did not yet (may need a
  new session). GameFAQs/TCRF answer curl with 403 (bot protection): agents skip refusing sites.
- Tested end to end on SameBoy's cgb-acid2 and gbemu's generated test ROM (not committed).

## Games
| Slug | Title | Playbook | Sets |
|---|---|---|---|
| pokemon-blue | Pokémon Blue Version (USA, Europe) | scouted + first capture 2026-11-15; design docs battle, pokemon, progression, world, economy, findings | main: 50 shots (verified 50/50); saves 01_start, 02_late_game_test, 03_starter_lab, 05_elite_four_lorelei |

## Next
- Pokémon Blue, second capture run for what is missing: learning a move, evolution, a gym leader, cave/forest,
  Surf, fishing, bicycle, Cut, Fly map, Safari Zone, Game Corner, S.S. Anne, Pokémon Tower, Silph Co.,
  Champion, Hall of Fame, credits, PC; retake pokecenter_heal (machine frame).
- `--model sgb` hangs on the SGB transfer screen (Pokémon Blue, pc=20b4): gbemu-cli SGB handshake; until fixed,
  capture in dmg.
- Routes using a macro change silently when the macro is edited: freeze macros once used in published shots
  (copy as a new macro name instead of editing), or store expanded routes in index.json.
- First real game through the whole pipeline; promote its lessons into docs/emulator.md and the skills.
- More platforms: a backend per system in tools/platforms.py (candidates: stable-retro / libretro cores for
  NES, SNES, GBA, Genesis; needs a pip install approved by the owner).
- Optional: a database export step once the target schema is known.
