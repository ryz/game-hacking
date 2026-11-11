---
skill: maintenance
---

# Feedback - maintenance

Running log for this skill, newest first. Status: `open`, `logged`, `promoted YYYY-MM-DD`, `superseded`.
Never delete entries.

## Entries

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
