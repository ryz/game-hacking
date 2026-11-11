---
skill: coordinator
---

# Feedback - coordinator

Running log for this skill, newest first. Status: `open` (proposed change waiting), `logged` (nothing to
promote), `promoted YYYY-MM-DD`, `superseded`. Promote a lesson into `skill.md` when it shows up in two entries or
the owner states it as a rule; then bump `updated:` in skill.md and mark the entries. Never delete entries.

## Entries

### 2026-11-11 - battle hang fix
- Task: act on the triage and tracer reports; move VWF RAM; ship a fixed ROM.
- Worked: verified the triage claim in the game code (`0:06EF`) before refactoring; tour routes caught a
  regression (uninitialised WRAM bank 7) before shipping; a full battle replayed after the fix.
- Corrected: earlier claim that `$CF00-$CFFF` was unused came from zero-in-savestates, which is not evidence.
- Friction: no free WRAM0 block exists; free-RAM measurement must exclude the boot clear and must include battle.
- Proposed rule change: never treat RAM as free without write watches over all tour routes plus a battle;
  run the full tour after any asm change before shipping.
- Status: open
