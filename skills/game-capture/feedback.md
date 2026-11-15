---
skill: game-capture
---

# Feedback - game-capture

Running log for this skill, newest first. Status: `open`, `logged`, `promoted YYYY-MM-DD`, `superseded`.
Never delete entries.

## Entries

### 2026-11-15 - Pokémon Blue main set (first capture)
- Task: capture the Pokémon Blue main set (early game, menus, battles, Elite Four, blackout), design docs,
  saves, milestone commits (rule arrived mid-run).
- Worked: deterministic replays (~75 battle turns land on the same frame); `do!` + sampled `wN` montage to pick
  animation frames; goto + do loops with RAM peeks to drive long battles; `shoot.py --list --only` to bring
  proven scout routes into main.
- Friction: snap right after goto saved a black frame, after undo a stale one (the one MISMATCH); new game.json
  macros needed a session restart; --verify/--publish 4-5 min with no output until the end; single-tile walking
  never triggers wild encounters; the scout's LATE recipe had wrong EXP (growth groups 3/5 swapped, fraction
  >100%).
- Proposed rule change: "after goto/undo, `do settle` before snap" (or render a frame on load); check RAM-recipe
  values on screen (summary/EXP pages) before snapping late-game menus; flush --verify output.
- Corrected: coordinator reran --verify; play.py now refuses snap until a frame ran after goto/undo/start at a
  checkpoint, reloads game.json on every do; shoot.py flushes each line; mkrecipe.py fixed (pret
  data/growth_rates.asm) and committed as games/pokemon-blue/tools/mkrecipe.py; MID regenerated (EXP only).
- Status: promoted 2026-11-15 (stale-frame guard in the tool, recipe check in skill.md)
