# Status - game database

Current snapshot; history in `progress-log.md`.

## Ready
- GB/GBC backend (gbemu-cli), ROM intake with header identification and a boot probe.
- NES/Famicom backend (2026-11-17): Mesen libretro core at a pinned commit, driven in-process by `tools/lrcore.py`;
  `.nes` cartridges, 256x240, models ntsc/pal/dendy, savestates, battery saves, full CPU-space peek/poke and PC
  (`tools/mesen-debug.patch`), RAM search, NES Game Genie. First game: Dragon Quest (Famicom, English patch), 2026-11-17: main set 67 shots, title to staff roll, 67/67
  verified from an empty cache. Open there: shop_keys, swamp, bridge, check_command, a rainbow-bridge clip set,
  the middle floors of the Dragon King's castle, a retake of commands_window (cursor blinked off). Not set up: Famicom Disk System, second controller, 6-letter Game Genie codes on
  bank-switched games.
- Owner-supplied patches (2026-11-17): `tools/patch.py` applies IPS, BPS and UPS (CRC checks, iNES/SNES copier
  header layout found from the CRC or given as `:headered`/`:unheadered`); `intake.py --patch` registers the
  patched ROM and records the source in game.json. Dragon Quest and SMT were patched before this by hand.
- Megami Tensei (Famicom, English BPS), 2026-11-18: main set 41 shots (intro, stats, battle, negotiation, Comp
  summon, fusion, sage password, shop, healer, status, Tyrant Minotaur encounter, game over), 41/41 verified.
  Open there: level-up (EXP poke did not trigger one), battle magic, a deeper floor, the Minotaur fight, a
  demon fighting, the ending (password format not decoded).
- Megami Tensei II (Famicom, English IPS), 2026-11-18: main set 36 shots (intro, naming, Devil Buster, battles,
  level-up, healer, Tokyo overworld, 3D cave, magic, computer room, save slots, shelter, game over), save
  01_computer_room. Open: Pazuzu, automap, a demon joining, summoning, fusion, shop, bosses; shots.txt not in game
  order; start_room retake. Some lines are untranslated by the patch (checked, not a layout error).
- `tools/dis6502.py` shared 6502 disassembler (2026-11-18).
- Dungeon Magic (NES), 2026-11-18: main set 41 shots, floor maps of all 39 floors + overworld, saves 01-02.
  Open: the King, camp, swords, bosses beaten, Darces, ending.
- Sets are ordered by `shots.txt` (game order), 2026-11-18.
- Wizardry I (NES), 2026-11-18: main set 71 shots through Werdna and the ending, 10 floor maps with all special
  squares decoded, saves 01-03. Open: Identify, spinner, teleport square; party_dead retake.
- `play.py dump/diff` (2026-11-18).
- Might and Magic (NES), 2026-11-18: main set 93 shots through the ending, 55 maps with terrain and exits, saves
  01-03. Open: services in the other towns, spells above level 1, Bribe/Giveup.
- Wizardry II (NES), 2026-11-18: main set 91 shots through the ending, 6 floor maps with special types checked
  in play, saves 01-04. Open: Sell/Identify, darkness, spinner, level drain, floor 4 room fight.
- Queue (registered 2026-11-18, not scouted): wizardry-2-nes, might-and-magic,
  deep-dungeon-3.
- Tokens incl. hold (`right:30`), mash, settle, macros, checkpoints as routes (cached per ROM).
- `play.py`: persistent session with undo, snap (capture + route), checkpoint/goto, RAM search, RAM watches.
- `shoot.py`: replay, `--verify` (pixel-exact reproduction), `--publish`; catalogue index.json/md + contact sheet.
- SNES/Super Famicom backend (2026-11-17): Mesen-S libretro core at a pinned commit, same driver as NES;
  `.sfc`/`.smc`, 256x224 (239-line and hi-res frames kept), models ntsc/pal, 12 buttons, 24-bit peek/poke and PC
  (`tools/mesen-s-debug.patch`), RAM search over work RAM, Pro Action Replay (`gs:`) and Game Genie. First game: Shin
  Megami Tensei (Super Famicom, English patches), 2026-11-17: main set 56 shots after two runs (boot to day 2:
  second dream, battles, level-up, game over, negotiation, automap; one hi-res frame), verified. Open there: no
  demon has joined (negotiation needs a Bead; item list not found in RAM), so no summoning, fusion or
  terminals; the second dream needs a flag poke (real trigger unknown). Special-chip games untested.
- Layout (2026-11-17): every game under `games/<slug>/`, shared tools/tests/docs at the repo root; emulator
  guide split into general rules and one file per platform.
- Skills game-scout and game-capture with agent wrappers; docs `emulator/` and `capture-guide.md`.
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
- First real game through the whole pipeline; promote its lessons into `docs/emulator/` and the skills.
- More platforms: a backend per system in tools/platforms.py (candidates: stable-retro / libretro cores for
  NES, SNES, GBA, Genesis; needs a pip install approved by the owner).
- Optional: a database export step once the target schema is known.
