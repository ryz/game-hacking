---
skill: triage
---

# Feedback - triage

Running log for this skill, newest first. Status: `open` (proposed change waiting), `logged` (nothing to
promote), `promoted YYYY-MM-DD`, `superseded`. Promote a lesson into `skill.md` when it shows up in two entries or
the owner states it as a rule; then bump `updated:` in skill.md and mark the entries. Never delete entries.

## Entries

### 2026-11-12 - 'Choose a classsir' on the creation class screen
- Task: explain the VWF corruption at the end of rect 26:729B and propose a fix.
- Worked: checking the attribute bank bit and the bank-6 cell map disproved the brief's two-owner theory in
  minutes; a write watch on the whole box row showed the one cell nobody wrote; breakpoints on RectRows/Commit
  with S_px/S_slot gave the decision; scratch tree from git archive with symlinked rom/ and gbemu-cli.
- Friction: the coordinator's brief ignored attribute bit 3 ($40 in VRAM1 = $C0); run_until needs addr/expr;
  VWF variables are EQUs (not in .sym); no character-creation route in the tour.
- Proposed rule change: attribute-bit / cell-map check first; watch the whole row for stale cells; scratch-build
  recipe. Tool: a creation route in tour.txt.
- Corrected: fix applied as proposed (RectRows .eol/.setx blank a cell that got no ink), class prompt clean, tour
  unchanged; 'create' route added to tour.txt (baseline accepted). Three PrintZ-style paths with the same ending
  (vwf.asm ~5551/6010/6675) left for a later check.
- Status: promoted 2026-11-12 (Display corruption: bank bit, whole-row watch, scratch recipe)

### 2026-11-12 - maze strip: mirrored 'Pick a lock' in the view strip under the dungeon SELECT menu
- Task: explain the mirrored menu glyphs in the maze strip and propose a vwf.asm fix.
- Worked: per-frame VRAM poll-diff found the writer when VRAM write watches did not fire; watching the HDMA
  registers $FF51-$FF55 exposed the unhooked immediate DMA 0:1553; clean base tree + full-tour pixel diff proved
  no side effects.
- Friction: VRAM watchpoints miss GDMA/HDMA writes; LCDC from a savestate hid the STAT raster split;
  tools/gbdis.py reads the JP ROM only (cannot check patched bytes).
- Proposed rule change: Display corruption: (a) watch $FF40-$FF4B writes over one frame (raster splits show
  other maps on some lines); (b) VRAM watches do not see DMA: poll-diff VRAM or watch $FF51-$FF55; two DMA
  paths (0:1443 queue, 0:1553 immediate).
- Corrected: fix applied as proposed (MazeHdma, 20:7F00); claims checked (four identical sites, free space,
  strip clean in maze_dmenu, 11 tests, tour 8/8). docs/re/vwf.md updated.
- Status: open (rules (a)/(b) for skill.md; gbdis --rom option for the tool backlog)

### 2026-11-12 - tavern 'Inspect whom?' list garbled after the sheet submenus
- Task: diagnose display corruption (not a hang) on the tavern list after Spells/Items/Pool.
- Worked: write watch on one bad cell (bank 3) -> PLRestore; per-step wEpoch readout showed a 512-bump wrap;
  a one-value poke of wEpoch proved the cause; fixed ROM tested from the same state.
- Friction: skill written for hangs; working tree had uncommitted asm (scratch copy did not match the
  build); old-build savestates only safe when the PC is in the frame wait; brief asked for report.md but the
  agent may not write report files.
- Proposed rule change: a "display corruption" branch (watch the cell, then its slot's wBits/owner/wVer,
  symbolise with .sym, poke the guard variable); build scratch copies from `git show <commit>:`.
- Corrected: fix applied as proposed (EpochBump drops all epoch caches on the wrap; Upload and DmaCheck
  bump through it), list clean, build/tests/tour/town speed OK. Coordinator slip: appended EpochBump past
  ShiftTab (40:8000); tools/asm.py now refuses code that runs past its bank.
- Status: promoted 2026-11-12 (display-corruption branch; scratch from git show) - skill.md; dispatch template
  no longer asks for report.md from triage

### 2026-11-11 - battle1: lock-up on the first attack
- Task: reproduce and diagnose the user's battle freeze in the English build.
- Worked: original-vs-English comparison, sanitizer diff between ROMs, write watches on the stack area, decoding
  the task scheduler (found the VWF variables inside task stacks `$CF00-$CFFF`). Diagnosis confirmed and fixed.
- Corrected: none.
- Friction: (1) writing `work/triage/battle1/report.md` was blocked, so the report existed only as the final
  message; (2) `tools/emu.py` hang detection (VBlank counter) misses soft locks where VBlank keeps running;
  (3) random encounters are hard to reach - seed-based walks did not reproduce later.
- Proposed rule change: (1) the final message is the report of record (the coordinator saves it); (2) extend
  `emu.py` with a soft-lock check (screen and task table unchanged for N frames) - tool change, open;
  (3) always save the encounter state and keep it with the case.
- Status: promoted 2026-11-11 ((1) report rule, second entry with playtester pt1; (2) soft-lock check: tool
  change, in docs/status.md Next; (3) tools/explore.py saves hit.state/prev.state)
