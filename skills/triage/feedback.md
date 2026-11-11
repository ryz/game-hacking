---
skill: triage
---

# Feedback - triage

Running log for this skill, newest first. Status: `open` (proposed change waiting), `logged` (nothing to
promote), `promoted YYYY-MM-DD`, `superseded`. Promote a lesson into `skill.md` when it shows up in two entries or
the owner states it as a rule; then bump `updated:` in skill.md and mark the entries. Never delete entries.

## Entries

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
- Status: open
