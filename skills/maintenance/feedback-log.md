---
skill: maintenance
---

# Feedback - maintenance

Running log for this skill, newest first. Status: `open`, `logged`, `promoted YYYY-MM-DD`, `superseded`.
Never delete entries.

## Entries

### 2026-11-12 - health check after the Rev 1 port and VWF day
- Task: docs vs code, stale v1.0 facts, status/log, skills and feedback bookkeeping, new tools and tests.
- Worked: revmap + gbdis on Rev 1 to tell converted from unconverted addresses; CheckInit bytes vs docs and
  `git log -G` for the signature; diffing equ lines since the last bump; work/* dirs newer than the session
  start to find unlogged agent runs; byte-identical rebuild check.
- Friction: `git log --since=DATE` empty (time zone; use '... 00:00 +0000'); revmap maps ambiguously both
  ways; RE notes have no status line; the skill has no tool-docstring check.
- Proposed rule change: Checks 1 + tool docstrings name the real path and options; check 7: RE notes carry a
  `> Status:` line when applied, and `$`-prefixed bank-0 addresses match the asm orgs; dispatch template
  note for git log --since.
- Corrected: applied nearly all proposed edits (vwf.md hooks/signature/pool/space, triage stub areas, text.md,
  numbers/battle-text v1.0 addresses, asm comments, reach.md paths, tool docstrings, visual-qa/playtester/
  editor/photographer skills, status Done/Next, progress-log, RE status lines, AGENTS.md, skill-index,
  promotions, tests/test_coverage.py fix-site test, .gitignore). Signature bumped to V^.
- Status: promoted 2026-11-12 (checks added to maintenance skill.md)

### 2026-11-11 - health check after the VWF session
- Task: docs vs code, WRAM7 map, skills, status/log after the redraw cache / GC / Notice Board / 39:49FE work.
- Worked: a script listing every `equ` with sizes and checking overlaps and pool shadows; `git show` of the
  session's asm commit to see whether the signature needed a bump; grep for dates against `git log`.
- Friction: `--help` runs build.py/tour.py and crashes gbdis/chain_rects; untracked `work/` paths in skills;
  placeholder paths make the reference check noisy.
- Proposed rule change: read docstrings instead of `--help`; flag `work/` paths in skills; check the wMagic bump.
- Corrected: all 23 findings checked; applied: vwf.md (owner bank, wUp, signature/tables, reservations, GC
  passes), main.asm path, signature VY, cache blocked while a font load is pending, wRC_valid cleared at init,
  explore.py moved to tools/, dates, status counts, triage report rule, placeholders, log header. Not applied:
  Stub_Hold removal (kept, commented), lint noise (backlog).
- Status: promoted 2026-11-11 (all three rules in skill.md)
