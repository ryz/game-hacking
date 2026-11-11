---
skill: playtester
---

# Feedback - playtester

Running log for this skill, newest first. Status: `open` (proposed change waiting), `logged` (nothing to
promote), `promoted YYYY-MM-DD`, `superseded`. Promote a lesson into `skill.md` when it shows up in two entries or
the owner states it as a rule; then bump `updated:` in skill.md and mark the entries. Never delete entries.

## Entries

### 2026-11-11 - pt2: full session on 3f26beb (report only, owner compares with own playtest)
- Task: full first-session playtest of the owner's ROM, report only.
- Worked: building the target commit from git archive into the session dir; frame-by-frame capture to tell
  transient from persistent glitches; RAM pokes (Fighter record $C8D1, gold $C8D9, EXP $C8DD, HP $C8E4) to
  reach a level-up, same poke on JP for comparison.
- Corrected: none yet (owner comparing).
- Friction: build/ was rebuilt mid-session by the coordinator (states broke, ~15 min); explore walker stops on
  any bank change and cannot aim for the stairs; fast inputs are swallowed outside battle too; dead status in
  RAM unknown.
- Proposed rule change: build the dispatched commit into SESSION/src and always pass --rom; document the
  Fighter record addresses for level-up tests.
- Status: promoted 2026-11-11 (build-your-own-ROM rule + record addresses; coordinator caused the friction)

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

