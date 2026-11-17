# Progress log - game database

Append-only, newest first.

## 2026-11-17 - Megami Tensei scouted; NES/SNES RAM search fixed
- `play.py find reset` on the libretro backends (NES, SNES) cleared the search without a snapshot, so the first
  `find` compared RAM with itself (`new == old + 1` always 0 candidates). Reset now snapshots; reported by the
  Megami Tensei scout, rechecked on the game (12 candidates after one step).
- Megami Tensei (Famicom, English BPS): scout done (commit 2ef4abc), 9 routed shots verified 9/9 from an empty
  cache by the coordinator. Capture run next.

## 2026-11-17 - owner-supplied patches are always applied
- Owner's rule: if an IPS/BPS/UPS patch comes with a ROM, use it. Written into `AGENTS.md` (rules + quick
  reference), the coordinator skill and `docs/emulator/README.md`.
- New `tools/patch.py` (IPS incl. RLE and truncation, BPS, UPS; CRC checks; header layout detected for BPS/UPS
  from the source CRC, given by hand for IPS) and `intake.py --patch` (repeatable): patched ROM in `rom/`, dump in
  `rom/src/`, patches in `rom/patches/<slug>/`, game.json "source" with names, SHA-1s, layouts and the rebuild
  command. Tests: `tests/test_patch.py`; end-to-end intake with a BPS on the synthetic NES ROM rebuilt the same
  SHA-1. Wizardry Empire's own `translation/tools/bps.py` left as is.
- `patch.py` layout `ines1` (tried automatically): the dump's header rewritten as plain iNES 1.0. Found with
  Megami Tensei (Famicom): the owner's dump has an NES 2.0 header, the BPS was made against the iNES 1.0 header
  of the same body (mapper 76); CRC matched after that, body untouched.

## 2026-11-17 - 3x copies in a subfolder
- Owner's request: originals in the set folder, 3x copies in a `3x/` subfolder with the same file names
  (`title_screen.png` and `3x/title_screen.png`; also clips, `steps.gif`, `full.gif`, Wizardry's compare images
  `3x/<id>.compare.png`). Tools: `emu.x3()`, shoot.py, play.py, Wizardry's `translation/tools/shoot.py`
  (publishes only the compare images into `3x/`). `index.json` `file_3x` is `3x/<name>`.
- Migration: 404 published files moved with `git mv` across all 8 sets, catalogues rewritten (links checked: 0
  broken), working sets in `work/` migrated the same way. Sample shots re-verified (Dragon Quest 2/2, SMT
  republished with no `@3x` left). 18 shared tests and 14 Wizardry tests pass.

## 2026-11-17 - Shin Megami Tensei main set, run 2
- game-capture: 22 new shots (56): second dream, heroine naming (cubi), first battle and commands, damage, enemy
  spell, result, level-up, failed escape, death, game over, full-moon refusal, negotiation steps, automap.
  Commit bd1607c. Run 1's blocker was a misread watch: the apartment door is square 32,88 (decimal 134/136 read
  as hex). The second dream needs story flag 7E07C1 bit 02; its real trigger is not found, so the route pokes it.
- Not reached: a demon joining (always asks for a Bead), summoning, fusion, terminals, healing, items list,
  bosses. Save 03_second_dream exported.
- Coordinator: `automap` (snapped while a verify was starting) and a sample verified 4/4; the agent's full
  verify covered the other 55. Tools: RAM watches take `"fmt": "hex"`; emulator guide notes on stuck events.

## 2026-11-17 - Shin Megami Tensei (Super Famicom, English patches): intake, scout, main set run 1
- Owner supplied the Japanese dump and two IPS patches (translation, then its bug-fix). The patches expect
  different layouts (smte1 with the 512-byte copier header, smte2 without): `games/shin-megami-tensei/tools/
  mkrom.py` rebuilds and checks SHA-1s. SNES header checksum now handles sizes that are not a power of two.
- game-scout: playbook, 6 checkpoints, RAM map (yen, magnetite, character records), save 01_start, shot plan.
  Names: ryz (hero), condi (Law hero), ebo (Chaos hero); the heroine is named later (cubi).
- game-capture run 1: 34 shots (boot, intro incl. one hi-res frame, dream, naming, stats, room, mail, save/load,
  3D corridor, command menus, town map, clinic, arcade shops, cafe, roadblock, full moon), commits a6c6883,
  9db24cd, be549c9. Found position, facing, moon/step counter and town-map tile; town-map warp at an exit
  prompt. Partial: could not find the way back into the apartment, so the story does not advance (no battles,
  negotiation, fusion, terminals, later districts).
- Coordinator: full verify rerun 34/34; contact sheet reviewed.
- Tool fixes from the two reports: `MACRO*N`; `prefix()` skips `pow` (sav: routes replay); `play.py export`
  refuses an empty battery; `play.py unsnap` / `recaption`; contact sheets scale bigger frames to the common
  cell (a 512x448 frame blew up every cell and detached the labels). 18 tests pass.

## 2026-11-17 - SNES / Super Famicom backend (Mesen-S); core options were not applied
- Owner's request: an emulator for SNES/SFC games. Mesen-S as a libretro core (libretro/Mesen-S at 9e4fdeb),
  chosen to match the NES setup: same driver, same kind of debug patch (`tools/mesen-s-debug.patch`: peek/poke
  over the 24-bit address space, PC with bank). `setup_emu.sh [gb|nes|snes]`.
- `platforms.py`: shared `Libretro` base class (states, screenshots, RAM search, battery) for `Nes` and the new
  `Snes` (header detection LoROM/HiROM/ExHiROM with copier header, region -> ntsc/pal, 12 buttons, PAR codes
  through `gs:`, Game Genie as a ROM patch through the mapping). Frames: the 239-line output is cropped to 224
  when the margins are black.
- Bug found and fixed: `lrcore.py` compared option keys as text against the core's bytes, so no core option was
  ever applied. NES ran on defaults that equal the intended values (only the region was auto-detected instead
  of forced; `--model pal` did nothing). On SNES the default power-on RAM is random, which the new test caught.
  Dragon Quest shots re-verified from an empty cache after the fix (5/5).
- Tests: generated SNES test ROM (`tests/make_snes_rom.py`), header/cheats, backend, full pipeline. 16 pass.
  ~330 fps. Docs: `docs/emulator/snes.md`.

## 2026-11-17 - repository restructured
- Owner's request: the repo had grown project by project (a translation, then a screenshot database next to it).
  Now the repo is the database: every game under `games/<slug>/`, shared tooling at the root, the Wizardry
  Empire translation a sub-part of its game. Path mapping (older entries and feedback logs keep the old paths):

  | Before | Now |
  |---|---|
  | `gamedb/games/`, `gamedb/tools/`, `gamedb/tests/`, `gamedb/rom/`, `gamedb/work/` | `games/`, `tools/`, `tests/`, `rom/`, `work/` |
  | `gamedb/README.md` | merged into `README.md`; `docs/README.md` is the index of the shared docs |
  | `gamedb/docs/emulator.md` | `docs/emulator/README.md` (general) + `docs/emulator/gb.md` + `docs/emulator/nes.md` |
  | `gamedb/docs/capture-guide.md`, `status.md`, `progress-log.md` | `docs/` |
  | `wizardry-empire/docs/design`, `docs/tech`, `docs/shots`, `saves` | `games/wizardry-empire/design`, `tech`, `shots`, `saves` |
  | `wizardry-empire/docs/README.md` (document rules) | `games/wizardry-empire/DOCUMENTS.md` |
  | `wizardry-empire/` everything else (script, asm, fonts, tbl, glossary, tools, tests, docs/re, status, log, rom.sha1) | `games/wizardry-empire/translation/` |
- One emulator build: the Wizardry tools use `tools/gbemu-cli` at the repo root (its own copy of the setup and
  the Linux patch are gone). Its design-table, map and publish tools write to the game-level folders.
- NES notes are their own document, not a list of differences from Game Boy.
- Wizardry Empire checked with the owner's ROM after the move: identical build (ROM and IPS) and identical tour
  frames (135) compared with the pre-move commit; generators reproduce the committed files.
- Not done: Wizardry Empire is not registered with the shared tools (no game.json/playbook/checkpoints); its
  play, tour and screenshot tools are still its own. Merging the two toolchains is a separate job.

## 2026-11-17 - Dragon Quest (Famicom, English patch): main set
- game-capture: 67 shots from the logo to the staff roll (towns, shops, inn, caves with torch/Remira, 7 battles,
  Golem, green dragon, both Dragon King forms, death, full ending, password screens, the kana password grid via
  `rom:jp`), 27 new checkpoints, design docs combat/world/items-and-shops, commits d253e69, c131c6c.
  Techniques: poke position or map number during a map transition for clean warps.
- Coordinator: full `--verify` from an empty cache, 67/67 reproduce (about 15 min; the first attempt hit a
  10-minute command limit). Sheet reviewed.
- Open tool requests from the capture feedback: `play.py recaption`, a session clock in `play.py status`.
- Not captured: shop_keys, swamp, bridge, check_command, seq-rainbow clips, castle middle floors.

## 2026-11-17 - Dragon Quest (Famicom, English patch): intake, scout, NES frame fix
- Owner supplied the Japanese dump and an English translation IPS; the patched ROM is registered as
  `dragon-quest` (SHA-1s of dump, patch and result in game.json "source"; a `rom:jp` variant restores the
  original). game-scout: playbook, 9 checkpoints (title, password_entry, start, late and five late_* places),
  password helper `games/dragon-quest/tools/pw.py`, RAM map, 54-line shot plan. No battery: passwords only.
- Bug found by the scout, fixed: `lrcore.Core.image()` emulated one frame when no frame had been drawn (after
  loading a state into a new core), so cached and freshly built checkpoints differed by a frame. Screenshots
  no longer emulate; savestates carry the frame in a trailer. Test added (13 pass). Checkpoints rebuilt.

## 2026-11-17 - NES / Famicom backend (Mesen)
- Owner's request: an emulator for NES/Famicom games like the GB one. Checked FCEUmm and Mesen as libretro cores
  (both build headless here, deterministic, savestates round-trip); owner chose Mesen.
- `tools/setup_emu.sh [gb|nes]` builds libretro/Mesen at 0102910 with `tools/mesen-debug.patch`
  (retro_mesen_peek/poke/pc). `tools/lrcore.py`: ctypes libretro frontend. `platforms.Nes`: iNES/NES 2.0
  identification, ntsc/pal/dendy, private empty save directory per run, RAM search in Python, Game Genie as a
  ROM patch (8-letter; 6-letter only without bank switching), `gs:` refused. play.py export names the emulator
  of the `.state`. `.gitignore`: `*.nes`, `*.fds`, `tools/mesen/`.
- Tests: generated NES test ROM (`tests/make_nes_rom.py`, hand-assembled, no game data); header/Game Genie,
  backend, and the intake -> play -> snap -> export -> shoot --verify pipeline. 12 pass. ~700 fps.
- Open: first commercial NES game (scout + capture) will show what the docs and skills still assume about GB.

## 2026-11-15 - sequence file names carry the set name
- Owner's request: files of `seq-*` sets are prefixed with the set name (seq-fishing_01_shore.png,
  seq-fishing_full.gif, ...); ids unchanged; shoot.py/play.py add the prefix (shoot.prefix()). Pokémon Blue
  seq-fishing and seq-fly reshot under the new names (15/15, 9/9). Test checks no unprefixed media remain.

## 2026-11-15 - stitched sequence GIFs
- Owner's request: a full GIF per sequence with all steps stitched. `seq-*` sets now get full.gif / full@3x.gif
  (stills held, clips at game speed), rebuilt on publish. Pokémon Blue: seq-fishing 34 s (144 KB / 626 KB @3x),
  seq-fly 19 s (49 KB / 207 KB @3x). Test checks the stitched timing.

## 2026-11-15 - Pokémon Blue sequences: fishing, Fly
- game-capture: seq-fishing (Vermilion harbour: menu path, cast clip, bite, battle-transition clip, hooked
  Shellder, plus the "Not even a nibble!" branch) and seq-fly (Vermilion -> Lavender: party, FLY, town map,
  take-off and landing clips), commit 12fdafe; world.md: fishing outcome rules and Fly.
- Tools from its feedback: clip poster choice (`rec:N:K:P`, `record --poster`, numbered frame sheet), category
  check up front, passing --verify rebuilds index.md/strip/steps. Coordinator re-picked 4 posters; 15/15, 9/9.

## 2026-11-15 - action sequences and clips
- Owner's request: capture actions as sequences (fishing, Fly). Tools: `rec:N[:K]` token, `play.py record`
  (GIF clips at game speed, @3x, poster PNG), `seq-<action>` sets get strip.png + steps.gif, --verify compares
  every clip frame, publish copies GIFs. Image labels fold accents. Test added (9 pass).

## 2026-11-15 - Pokémon Blue main set, run 2
- game-capture: 42 new shots (92 total): Brock gym and badge, learn move, evolution, Surf, fishing, bicycle, Cut,
  Fly map, forest, Mt. Moon, Safari Zone, Game Corner slots, S.S. Anne, Pokémon Tower ghost, Silph Co.,
  Champion, Hall of Fame, credits, PC. Saves 04_pewter_boulderbadge, 06_hall_of_fame. Commits 41d507a, 5a4d0ea.
  Design docs extended (~45 claims), 3 findings. Coordinator: full --verify, both saves booted.
- Tools: snap reports UNCHANGED re-snaps; shoot.py --publish-only; emulator.md: pick animation frames in play.py.

## 2026-11-15 - Pokémon Blue main set
- game-capture: 50 shots published (boot to Elite Four Lorelei, menus, battles, catch, blackout, Mart, Center),
  design docs, saves 03_starter_lab and 05_elite_four_lorelei; commit 4d04ea9. Coordinator --verify rerun 50/50.
- Fixes: mkrecipe.py growth groups (3 medium slow / 5 slow) and EXP fraction, committed in
  games/pokemon-blue/tools/; MID macro EXP regenerated (LATE kept, LATE_EXP corrects it). play.py: snap refuses
  stale frames after goto/undo, reloads game.json on every do; shoot.py flushes progress lines.

## 2026-11-15 - Pokémon Blue scouted
- game-scout: playbook (controls, RAM map, sources: pret/pokered), macros TITLE/NEWGAME/CONTINUE/LATE/MID,
  checkpoints title/start/late, door-warp recipe, ~50-id shot plan, design README started; saves 01_start and
  02_late_game_test exported. Verified by the coordinator (replay without cache, both saves boot).
- Tools: RAM watches take `"fmt": "bcd"`; emulator.md: mash and blank-frame rules, undo depth.

## 2026-11-15 - milestone saves committed
- Owner's rule: commit the saves agents make, so the owner can jump in. `play.py export NAME "desc" [--state]`
  writes `games/<slug>/saves/NAME.sav` (+ SameBoy `.state`) and its README row; `.gitignore` exception added;
  `sav:NAME` finds these first. Test added (8 pass).
- Pokémon Blue registered (intake); game-scout running.

## 2026-11-15 - shortcuts, naming, design reference
- Owner's rules: cataloguing over fair play (cheat/hack freely, realistic values), main character "ryz", use
  saves/codes from the web, document systems in a design reference while playing.
- Tools: set:/gs:/freeze: tokens, rom: variants (Game Genie decoding checked against SameBoy's cheats.c; GameShark
  types against EnHacklopedia), sav: prefix, IPS; tests for all (7 pass, run without pytest: not installed).
- Templates: design/README.md (notation, confidence tags) and findings.md; playbook Naming and Saves sections.

## 2026-11-15 - pipeline set up
- New project `gamedb/`: generalised the Wizardry Empire photographer/playtester tooling for any GB/GBC ROM.
- Tools: platforms.py (backend registry), emu.py, play.py, shoot.py, intake.py; tests in tests/.
- Docs: emulator.md (general emulator rules), capture-guide.md (database categories and quality rules).
- Skills: game-scout (research -> playbook), game-capture (play -> set).
- Verified on cgb-acid2 and the gbemu test ROM: intake, checkpoint, snap, undo, RAM search, --verify (2/2
  reproduce), --publish. No game captured yet.
