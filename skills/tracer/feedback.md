---
skill: tracer
---

# Feedback - tracer

Running log for this skill, newest first. Status: `open` (proposed change waiting), `logged` (nothing to
promote), `promoted YYYY-MM-DD`, `superseded`. Promote a lesson into `skill.md` when it shows up in two entries or
the owner states it as a rule; then bump `updated:` in skill.md and mark the entries. Never delete entries.

## Entries

### 2026-11-12 - Rev 1 vs v1.0 differences
- Task: list Rev 1 changes relevant to the translation (text coverage, RAM layout, code summary).
- Worked: classifying changed regions by pointer shift, forward-mapping message sites, RAM operand counts.
- Friction: revmap has no inverse map or gap iterator; mapping a whole site fails when its own pointer bytes
  changed; census_msgs guesses text banks (noisy diffs); decode_msg fails on control codes.
- Proposed rule change: for revision diffs classify by pointer shift and compare per mapped site; tools:
  revmap.inv_addr()/gaps(), decode_msg with all control codes.
- Corrected: findings verified (31:4592 bytes, 32:5807 31 entries, 2B:788B) and applied in 8052a1f; notes in
  docs/re/rev1.md.
- Status: logged (tool requests in docs/status.md backlog)

### 2026-11-11 - numbers and 8 px glyphs inventory
- Task: list every 8 px number/word printer in the EN build, group by routine, propose VWF routes.
- Worked: count-only PC breakpoints on caller return addresses read per input token, plus a VRAM-glyph scanner
  on every tour screen; JP states were enough for unpatched sites.
- Friction: emulator limits (64 breakpoints, 32 in-memory snapshots), no EN battle states, census misses
  digit-only rects.
- Proposed rule change: count-only breakpoints on return addresses for "which routine prints X"; never a
  stopping breakpoint on a per-frame routine; file snapshots. Tools: EN battle states in party.py, census mode
  for digit/ASCII-only rects.
- Corrected: 0:108B hook implemented as proposed (Stub_Num); the 16-entry cache became the shared name/number
  cache; tabular '1' and the $7F figure space applied. Separators/labels/spell slots/symbol sheet not yet.
- Status: promoted 2026-11-11 (count-only breakpoint rule in skill.md); tools in the backlog

### 2026-11-11 - museum: text sources, printers, hooks
- Task: museum text (menu, item/monster lists, entry pages): sources, printers, hook proposals.
- Worked: comparing VRAM tiles against the `01:4400` font per bank and tile-data base found a third font layout
  and the extra glyph sheet; a `0:142A` breakpoint lists every graphics load with its caller; poking the seen
  bitfields reached the monster pages; hooks proven on a scratch ROM copy.
- Friction: `$D800` is also used as a scratch list (not only the window); one saved EN state had left the page;
  the skill assumes two font layouts; `emu.py press` cannot be interleaved with breakpoints; census misses
  attribute rects (~70 museum rects).
- Proposed rule change: (1) read LCDC bit 4 before decoding a buffer and map VRAM tiles to the font; (2) tools:
  a `0:142A` DMA logger and a pokes+sequence runner; (3) dispatch: "do not patch" allows scratch ROM copies
  under `work/re/<topic>/`.
- Corrected: notes copied to docs/re/museum.md. Item hooks A/B/C and the rects not applied yet (planned);
  monster room needs a third VWF layout.
- Status: promoted 2026-11-11 ((1) extends the window-decode rule from the spells entry; (3) in the dispatch
  template); (2) in the tool backlog

### 2026-11-11 - camp party list: status word garbage
- Task: find the printer of the status word in the Camp party list HP column, explain the garbage, propose a hook.
- Worked: dump the buffer row first (raw kana = unhooked copy), write watch from a state one input before the
  screen, scratch ROM with the hook bytes and re-keyed FixMap entries before any real change.
- Friction: the dispatch's repro value was wrong (status 3 = Paralyzed, not Dead; the coordinator took the table
  order as the encoding); skill says notes in `work/re/`, the dispatch said `work/trace/`.
- Proposed rule change: (1) read how the printer turns a RAM byte into a table index before trusting a repro
  value; (2) fix_sites() should also match copies ending in `2a 12` and look for duplicate tables in other banks.
- Corrected: coordinator verified the bytes (39:49FE copy, 39:4004 = 38:754D) and applied the hook as proposed
  with 32 px short forms (a98cef8); encoding noted in docs/re/text.md. Dispatch paths: use `work/re/` next time.
- Status: promoted 2026-11-11 ((1) skill.md + text.md; (2) tests/test_coverage.py checks both cases)

### 2026-11-11 - spells: where spell text lives and how it is printed
- Task: locate every spell text piece (headers, list, battle name, detail labels, element, descriptions) with hooks.
- Worked: dumping the window buffer ($D800/$DC00) first, then write watches; a scratch ROM with one record
  changed proved the data-only fix for list + battle; EN/JP bank diff found a stray Stub_Fix at 2A:4A31.
- Corrected: none yet (being implemented).
- Friction: window-buffer codes depend on attribute bit 3, so tbl.dec/census decode some rects wrongly; no JP
  battle state with a living caster.
- Proposed rule change: (1) window buffer decode rule; (2) diff EN vs JP at a site before proposing a hook.
  Tools: census_rects should apply attributes; a reproducible JP battle route in tools/routes.
- Status: promoted 2026-11-11 (owner approved; tools: census attributes and JP battle route still open)

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
- Status: promoted 2026-11-11 (input-list rule); census segment mode still open
