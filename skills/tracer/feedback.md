---
skill: tracer
---

# Feedback - tracer

Running log for this skill, newest first. Status: `open` (proposed change waiting), `logged` (nothing to
promote), `promoted YYYY-MM-DD`, `superseded`. Promote a lesson into `skill.md` when it shows up in two entries or
the owner states it as a rule; then bump `updated:` in skill.md and mark the entries. Never delete entries.

## Entries

### 2026-11-11 - battle-text: where battle text lives
- Task: locate battle messages, command menu and monster-group panel text and propose hooks.
- Worked: reused triage's original-ROM battle states instead of walking; watchpoints on `$C1BF-$C1C1`;
  found a real bug in the patch (`$F2` left `$C1C1` on the English bank), now fixed.
- Corrected: none.
- Friction: run cut off by a usage limit (resumed with SendMessage); `census_msgs` misses `$FC`-chained
  segments; triage's seeded walk did not reproduce the encounter.
- Proposed rule change: when a state is reached by a random walk, save the state AND the exact input list;
  census tools need a segment mode (`$FC` boundaries) - tool change, open.
- Status: open
