# Progress log - game database

Append-only, newest first.

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
