---
skill: game-scout
---

# Feedback - game-scout

Running log for this skill, newest first. Status: `open`, `logged`, `promoted YYYY-MM-DD`, `superseded`.
Never delete entries.

## Entries

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
