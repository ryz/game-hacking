# Progress log - game database

Append-only, newest first.

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
