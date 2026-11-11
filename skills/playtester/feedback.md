---
skill: playtester
---

# Feedback - playtester

Running log for this skill, newest first. Status: `open` (proposed change waiting), `logged` (nothing to
promote), `promoted YYYY-MM-DD`, `superseded`. Promote a lesson into `skill.md` when it shows up in two entries or
the owner states it as a rule; then bump `updated:` in skill.md and mark the entries. Never delete entries.

## Entries

### 2026-11-11 - pt1: first session (town, shop, inn, temple, training, maze, 3 battles, stairs)
- Task: first full playtest from power-on.
- Worked: same route on the Japanese ROM separated bugs from original behaviour; RAM search turned "gold looks
  wrong" into a confirmed bug (buying added gold: RAM data copies were stubbed as text, fixed 8fe8999).
- Corrected: "Status lists spell names as untranslated" is right; battle message order issue not reproduced
  after the bank-49 fix (verbs now read from bank 49).
- Friction: skill said A opens the dungeon menu (it is SELECT); stairs route missing; explore.py stops at
  message boxes; battle inputs need ~30 frames; skill asked for report.md though the harness forbids it.
- Proposed rule change: correct maze controls, compare with JP before reporting, check RAM for wrong values.
- Status: promoted 2026-11-11 (factual control fix + both rules; explore.py change open)

_No runs yet._
