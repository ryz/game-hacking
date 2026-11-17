---
skill: game-scout
---

# Feedback - game-scout

Running log for this skill, newest first. Status: `open`, `logged`, `promoted YYYY-MM-DD`, `superseded`.
Never delete entries.

## Entries

### 2026-11-17 - Dragon Quest (Famicom, English patch; first NES game)
- Task: scout Dragon Quest (Famicom, English patch), the first NES game: playbook, macros, title/start/late
  checkpoints, password handling, RAM map, shot plan.
- Worked: making a late-game "save" by poking the state and asking the king for a password; an inverse IPS as a
  `rom:jp` variant to compare the kana and translated password grids; position poke plus one step as a warp;
  rebuilding every checkpoint with an empty cache and comparing against cache hits, which exposed a frame bug.
- Friction: cache hit versus build differed by one frame on NES (`lrcore.Core.image()` ran a frame when none was
  drawn); `status` PC is useless for this game (always the frame-wait loop); TCRF and StrategyWiki 403; the
  skill's write list has no `tools/` folder although pokemon-blue has one; reading a password off a screenshot
  is error-prone (icons are symbols).
- Proposed rule change: fix `lrcore.Core.image()` so a screenshot never advances emulation, with a test; in
  skill.md step 3 add "rebuild the checkpoints once with an empty cache and compare with a cache hit"; allow
  `games/<slug>/tools/` in the guardrails; for password games "make passwords by poking the state and asking
  the game for one".
- Corrected: backend fixed the same day (screenshots never emulate; savestates carry the frame; test
  `test_nes_state_keeps_frame_and_timing`); all nine checkpoints rebuilt and checked by the coordinator.
  Password-by-poke and the PC note went into `gamedb/docs/emulator.md`.
- Status: open (skill.md changes: empty-cache check, `tools/` in the write list; first occurrence)

### 2026-11-15 - Pokémon Blue (first game through the pipeline)
- Task: scout Pokémon Blue: playbook, macros, title/start/late checkpoints, RAM recipes (late game, warp),
  saves for the owner.
- Worked: pret/pokered disassembly via curl to raw.githubusercontent.com + base stats read from the ROM ->
  generator script for realistic party pokes, right first time; warping by rewriting a door's warp entry;
  in-game save + `play.py export --state`, checked with `sav:` + CONTINUE.
- Friction: `undo` one level only (an over-long mash typed into the naming keyboard); settle accepts all-white
  fade frames; RAM watches could not show BCD money; `--model sgb` hangs on SGB transfer garbage; snap routes
  using a macro break silently when the macro changes later; WebFetch fails, TCRF/GameFAQs 403.
- Proposed rule change: docs/emulator.md: never mash into a name prompt; settle should refuse/warn on blank
  frames; a bcd type for RAM watches.
- Corrected: coordinator replayed @late without cache, the party screen, both exported saves via
  `sav:NAME,TITLE,CONTINUE` (trainer card ryz / 48215 / 27:47 / 8 badges; bedroom for 01): all as reported.
  Added `"fmt": "bcd"` watches (money watch for pokemon-blue) and the mash and blank-frame rules to
  docs/emulator.md. Settle itself left unchanged (recorded routes depend on it). SGB hang and macro-change
  breakage go to docs/status.md Next.
- Status: promoted 2026-11-15 (mash rule, blank-frame note, bcd watch); sgb and macro versioning open
