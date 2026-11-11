# Progress log - Wizardry Empire

Append-only, newest first. One entry per session and per test ROM sent. `docs/status.md` is the current
snapshot; this file is the history (what changed since the ROM you tested). Format:

```
## YYYY-MM-DD - <headline>
- ROM: <commit> sent? (yes/no)
- Changed: ...
- Found / fixed: ...
- Open: ...
```

## 2026-11-11 - town speed, numbers in the small font
- ROM: `2edfeec` sent.
- Changed: numbers through the VWF (0:0FD0, 84 sites), tabular digits, typewriter figure space; party-list
  skip/restore, name/number cache, rect sums, Dedupe hash index; font rule widened (numbers too).
- Measured: town with a party = Japanese (360 loops/120f, reaction frame 2; was 174); without a party
  reaction 7-13 frames (JP 2).
- Checked: tests, tour 8/8, shop header/prices, inn, Camp, a full battle with chest menu.
- Open: flicker on screen switches (analysis in status Next 7), 8 px separators/labels, a box render still
  costs 1.5 frames, one unreproduced wrong-digit frame (chest list).

## 2026-11-11 - shop lists, coverage tests, maintenance, museum trace
- ROM: `615e150` sent.
- Changed: shop Buy/Sell, "Sold out" rows and character item lists in the VWF; init signature VY; redraw
  cache blocked during a pending font load; tests/test_coverage.py; tools/explore.py; skills: tracer,
  coordinator, triage, maintenance rules promoted; doc drift fixed (maintenance report).
- Found: museum text map (docs/re/museum.md); monster room needs a third font layout.
- Checked: tests (3), tour 8/8, town speed 360/120f, shop buy/sell/pool gold, Camp items.
- Open: museum hooks, name-entry field in 8 px, long playtest for the slowdown report.

## 2026-11-11 - town speed, maze walls, party-list status
- ROM: `a98cef8` sent.
- Changed: rect redraw cache (town idle 360 loops/120f, JP 360, was 72); graphics reservations pruned by GC;
  dry GC pass keeps game graphics; party-list status words (39:49FE).
- Checked: tests, tour (8/8), town cursor moves, 20x "It is locked." at a door (walls clean), one full battle
  round, Camp with every status value.
- Open: the progressive slowdown the owner saw was not reproduced; needs a long playtest.
- Closed: Dedupe speed (town input lag) - superseded by the redraw cache.

## 2026-11-11 - Notice Board
- ROM: `9a5f3a8` sent.
- Changed: Notice Board scroll in English (VWF_Notice, script/notice.json); see docs/re/vwf.md.
- Checked: notice screen EN vs JP, back to town; tests; tour (all routes OK). Battle not re-run (change is
  limited to the notice screen).
- Open: museum (separate glyph set), shop lists in 8 px, Dedupe speed, friendly-encounter prompt unseen.

## 2026-11-11 - playtest pt2 fixes
- ROM: `635baf0` sent (game code; docs commit on top).
- Changed: see docs/status.md "Done (fourth session)"; screen-hold experiment switched off (made switches
  worse); photographer jp_tour set committed; emulator survey (Gearboy, PyBoy recommended as additions).
- Found / fixed: pt2 issues #1, #2, #4, #5 (untested on screen), #9, #11, #12 (data path), #15, #16; owner's
  findings: disarm menu, empty selection menus, temple wording, spell menu artifacts.
- Open: Notice Board, museum (separate glyph set), shop lists in 8 px, Dedupe speed.

## 2026-11-11 - titles, monster panel, temple, name entry, spells
- ROM: `3f26beb` sent.
- Changed: titles (2B:5F4F records as VWF headers); VWF_Panel replaces 0:199B; Stub_Enqueue reports non-font
  DMAs (VWF_DmaCheck reserves overwritten slots); $A0/$CF/$D0 out of the pool; spells (records, SpellNames
  + wSpell via 0:24CF, list trampoline 2A:7F00, rects, element FixMap, bank-46 descriptions); GC marks both
  layouts; FixMap 600; {FA} spacing; font rule; photographer may commit shot sets (docs/shots/).
- Found / fixed: chest/bag picture painted with text; "(1)" garbage in the monster panel; temple
  "No one is here." raw kana; name entry typed kana; shop header dots; spell names missing in battle.
- Open: see docs/status.md Next.

## 2026-11-11 - battle text, gold bug, character card, chest
- ROM: `c5c6b84` sent (see below).
- Changed: battle command lists and 129 battle segments translated; bank-49 English kept in bank 49; VWF GC
  limited to visible rows/window; typewriter no slot reuse; private VWF stack; Stub_Fix far-bank variant and
  destination blanking; fixtables/chests scripts; build writes a `.sym` file.
- Found / fixed: user findings (mode select, character card, combat menu); battle menu "Item" overwritten (GC
  over garbage rows); scroll corruption in the battle log; attack verbs printed shop text (`{F3}` bank);
  playtester: buying added gold / inn free / EXP garbage (RAM copies stubbed as text); shop crash (task
  stack overflow); chest menu blank; sold-out rows.
- Open: card title, monster panel, spells, the rest of the playtester list (`docs/status.md` Next).

## 2026-11-11 - battle hang fixed, agents and skills
- ROM: `9395438` and `84c5fb5` sent (same game code; `84c5fb5` adds only docs).
- Changed: VWF state moved from WRAM0 to WRAM bank 7; redirected messages jump back to their original terminator;
  agent setup restructured into `skills/` with feedback logs and an agent log; maintenance skill, progress log,
  bug-report and dispatch templates.
- Found / fixed: battle lock-up on the first attack (VWF variables in the game's task stacks, found by the triage
  agent); `$F2` left the text bank on the English bank (found by the tracer agent); bank 7 not initialised
  (caught by the tour before shipping); lower font half could overwrite VWF slots.
- Open: battle text (located: bank 49 `$FC` segments), monster-group panel, character-sheet values, spells,
  name entry, title screen.

## 2026-11-10 - first playable English build
- ROM: `a3a4660` sent. User report: battle froze on the first attack (fixed 2026-11-11).
- Changed: toolchain (disassembler, assembler, build, IPS); VWF engine with hooks for rect boxes, typewriter
  messages, name copies, inline code text and fixed-length table copies; 2 MB expansion.
- Translated: 206 menu/info boxes, 185 messages (bank 45 events, bank 49 system), 224 items, 166 monsters,
  default characters, character-sheet labels, tavern menu.
- Agents: translator, reviewer, playtester, visual-qa, tracer, triage, editor; lint and screen tour.
