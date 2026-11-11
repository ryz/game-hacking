---
skill: tracer
---

# Feedback - tracer

Running log for this skill, newest first. Status: `open` (proposed change waiting), `logged` (nothing to
promote), `promoted YYYY-MM-DD`, `superseded`. Promote a lesson into `skill.md` when it shows up in two entries or
the owner states it as a rule; then bump `updated:` in skill.md and mark the entries. Never delete entries.

## Entries

### 2026-11-11 - char-card: printers of the garbled character-card fields
- Task: find the routines that print the garbled card fields (gender, status, location, title, shop alignment,
  gold) and propose VWF hooks.
- Worked: write-watch on bank-3 cells from a state one input before the card; dumping the EN buffer showed why
  each field is garbled (header bytes, A clobbered). Every state saved with its input list.
- Corrected: none; proposals A/B/C/D implemented (c5c6b84). The gender site crashed the shop at first, not
  because of the site but because the VWF overflowed the 64-byte task stack (fixed with a private stack).
- Friction: `gbdis.py` address parsing (decimal unless `0x`); `mem_read` returns bytes; emu.py hang check
  false positives on slow VWF screens; 4 KB output budget.
- Proposed rule change: gbdis usage note and "dump the EN buffer first" -> promoted 2026-11-11. emu.py hang
  check: only report a hang when the PC stays in a tight range (tool change, open).
- Status: promoted 2026-11-11 (input-list rule, second entry; gbdis note; EN buffer dump)

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
