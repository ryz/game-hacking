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
| (none yet) | | | |

## Next
- First real game through the whole pipeline; promote its lessons into docs/emulator.md and the skills.
- More platforms: a backend per system in tools/platforms.py (candidates: stable-retro / libretro cores for
  NES, SNES, GBA, Genesis; needs a pip install approved by the owner).
- Optional: a database export step once the target schema is known.
