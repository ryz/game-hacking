---
skill: coordinator
---

# Feedback - coordinator

Running log for this skill, newest first. Status: `open` (proposed change waiting), `logged` (nothing to
promote), `promoted YYYY-MM-DD`, `superseded`. Promote a lesson into `skill.md` when it shows up in two entries or
the owner states it as a rule; then bump `updated:` in skill.md and mark the entries. Never delete entries.

## Entries

### 2026-11-12 - Rev 1 port and a long autonomous day
- Task: port to Rev 1, keep agents busy while the owner was away, integrate ~15 agent reports.
- Worked: background shoots/tours as regression nets; worktree builds of the previous commit for A/B; every
  agent fix verified in the emulator before committing.
- Friction: rebuilt build/ while an agent or a shoot used it (mixed results); uncommitted asm while triage
  copied the tree; a tour 'OK' hid a boot stuck on Mode Settings (tour only checks hangs); appended code past
  the VWF bank (now an asm error).
- Proposed rule change: dispatch only committed work (promoted: Dispatch); look at at least one tour sheet
  after GC/boot-path changes, not only the OK count.
- Corrected: -
- Status: promoted 2026-11-12 (dispatch rule; maintenance found it in three entries)

### 2026-11-11 - town slowdown, maze walls, Camp status
- Task: owner's report (town slowdown, text in maze walls, Camp garbage); ship a ROM.
- Worked: measuring the main-loop rate against the Japanese ROM pinned the slowdown in minutes; count-only
  breakpoints on every VWF symbol showed the per-pass rect redraw; the tracer found the Camp printer.
- Corrected: the tracer dispatch carried a wrong repro value (status 3 taken as Dead from table order).
- Friction: the progressive slowdown was not reproducible with random walks (they drift back to town/shop).
- Proposed rule change: repro values from code; speed comparison with the JP ROM after VWF changes.
- Status: promoted 2026-11-11 (owner approved)

### 2026-11-11 - battle hang fix
- Task: act on the triage and tracer reports; move VWF RAM; ship a fixed ROM.
- Worked: verified the triage claim in the game code (`0:06EF`) before refactoring; tour routes caught a
  regression (uninitialised WRAM bank 7) before shipping; a full battle replayed after the fix.
- Corrected: earlier claim that `$CF00-$CFFF` was unused came from zero-in-savestates, which is not evidence.
- Friction: no free WRAM0 block exists; free-RAM measurement must exclude the boot clear and must include battle.
- Proposed rule change: never treat RAM as free without write watches over all tour routes plus a battle;
  run the full tour after any asm change before shipping.
- Status: promoted 2026-11-11 (owner approved; the tour rule was already in Integrate)
