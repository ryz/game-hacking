---
skill: triage
---

# Feedback - triage

Running log for this skill, newest first. Status: `open` (proposed change waiting), `logged` (nothing to
promote), `promoted YYYY-MM-DD`, `superseded`. Promote a lesson into `skill.md` when it shows up in two entries or
the owner states it as a rule; then bump `updated:` in skill.md and mark the entries. Never delete entries.

## Entries

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
