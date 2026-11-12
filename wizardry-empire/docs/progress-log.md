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

## 2026-11-12 - remaining 8 px text, tooling, design docs
- ROM: `6389ee3` sent.
- Small font: event party list (magic circle; status words were blank), item info range word and negative AC,
  camp heal box, character creation '?' fields, Search Person (dots, 'B1 X0, Y0', stray particle removed), item
  list marks '?'/'-' (4 sites). Text: inn old-age death line ('...died of old age.').
- Tooling: route-state cache, parallel tour, tools/check.py (build+tests+tour+pixel diff), tools/play.py
  (persistent session), gbdis --en/--xref/BB:AAAA, emu tokens poke:/KEY>KEY, asm overlap check.
- Docs: docs/design/ (characters, items + table, monsters + table, dungeon); docs/re/glyphs8.md, debug-mode.md.

## 2026-11-12 - small-font numbers: AC sign, HP slash, party list, spell grid, monster panel
- ROM: `d0727be` sent.
- Card/shop: negative AC as one right-aligned '-N'; 'Lo'/'Hi' in the VWF; card HP '/' + max as one string.
- Town party list: '/', '+', poison '-' in the VWF. Spell slot grid: '1 / 0 / 0 ...' as one VWF string on
  the level cursor's grid. Monster panel '(1) 1' and automap digits: symbol tiles from the VWF glyphs.
- Rect blits return DE past the box like the original (tracer finding; tour A/B 230 shots identical).
- Bank-2C 'second sheet' is the hidden debug mode (docs/re/debug-mode.md), left as is.

## 2026-11-12 - card 'Status: OK' as one right-aligned unit; maze strip fix
- ROM: `b9f4a72` sent.
- 'Status:' label now sits one space before the status word; both end at col 18 (all 10 status words checked).
- Maze view strip under the dungeon SELECT menu: no more mirrored menu glyphs (immediate HBlank DMA 0:1553
  now reported to VWF_DmaCheck; triage report work/triage/maze_strip/). Tour 8/8, 11 tests.

## 2026-11-12 - character sheet: status right-aligned (owner's request)
- ROM: `35003bf` sent.
- The status word ('OK', 'Paralyzed', ...) ends at col 18 like Lvl/Age/AC; 'Status:' label stays at col 8.
  CardStatus (26:7800) + build-generated table (tools/build.py card_status()); checked with all status kinds
  poked (work/qa/status/sheet.png), Tavern/Camp cards and the tour.

## 2026-11-12 - character sheet: Age, small HP/AC, right-aligned numbers (owner's request)
- ROM: `43afb2b` sent.
- Changed: card 'Lvl'/'Age'/'AC' labels in one VWF column, values (and Title/EXP/Gold) end at col 18; age in
  the VWF ('Age 16' instead of '16yrs'); HP/AC labels in the small font; AC right-aligned with a small '-';
  shop header 'AC' and gold aligned the same way; titles are 14-cell rects.
- Open: the bank-44 window sheet (2C:4ACB, 'yrs') not seen on screen; maze strip text glitch (triage running).

## 2026-11-12 - playtest fixes, maintenance, owner-delegated rulings
- ROM: `b70ce52` sent.
- Changed: teleport prompt columns, Add-whom row, Find allies list and battle Equip prompt; temple result line
  and Camp Equip alignment; docs/skills maintenance (signature V^); rulings: one name per creature (Lion of Hell,
  Ancient One, From Beyond, Unspeakable), Dragonslayer, Magic Robe, ADISH in caps, level(s)/curse(s), 'quest',
  editor Polish list; Sigfrid kept (owner).
- Open: status.md Next (museum page speed, flicker, 8 px leftovers, tool backlog).

## 2026-11-12 - chests/events playtest, temple fee, missing messages, NPC names
- ROM: `5ab9d44` sent (includes the message census: five more bank-49 messages, tests/test_msg_coverage.py).
- Changed: NPC recruit names in English (Sigfrid in the 7-letter field); down-stairs prompt and three more
  bank-49 messages added; {FA} word wrap measures 3/4 cell per character; magic-circle party list in the
  small font; number stub leaves B = 0 (was making the event list show everyone as poisoned).
- Found / fixed: temple fee copy treated as text (payer's gold corrupted) - fix_sites() takes the nearest
  ld hl; limit tests for copied strings. Chests come only from guarded squares (docs/re/reach.md); chest,
  trap, event, recruit and temple screens checked by the playtester.
- Open: status.md Next.

## 2026-11-12 - crash fix (unidentified group names), name entry, Camp reorder
- ROM: `e45012c` sent.
- Changed: name-entry field and cursor in the VWF; Camp reorder digits/names in the VWF; 'Power hit' (was
  'Aim for damage', ran over its box); monster panel keeps names that fit on line 1; museum minus/range.
- Found / fixed: CRASH - unidentified group names of 13+ characters (Haggard figure, Armored figure, Gaseous
  thing) overflowed $C50F into the type index; the kill message then ran code bytes (playtester). Renamed;
  tests/test_limits.py. Tavern list after the sheet submenus (cache epoch wrap).
- Tried and reverted: faster museum page (list garbage), copy-tied slot quarantine for flicker (stalls).
- Open: chests and maze events not yet reached in the EN build (tracer making states); buffer-size audit of
  all copied strings running.

## 2026-11-12 - ending and credits, playtest fixes (battle panel, tavern list, level-up)
- ROM: `6500974` sent.
- Changed: last untranslated screens (ending 7 pages + credits, power-off screen, Ring of Healing/Death lines,
  "Become a <class>?"), reviewer fixes (reigning Emperor vs Emperor of the Abyss, Mad Overlord foreshadowing),
  museum minus/range in the small font, spaced unidentified group names in battle ('Robed figure').
- Found / fixed: battle panel garble ('cono', HP as 'Run'; GC read SCX mid-frame under the battle's raster
  split), tavern list after the sheet submenus (one-byte cache epoch wrapped), inn level-up line printed off
  screen (Stub_PrintZ DE), credits charset overwritten by VWF slots; explore.py works on Rev 1; the
  assembler now refuses code past the end of a bank.
- Open: ending only seen via a forced route; museum page speed; status.md Next.

## 2026-11-12 - Rev 1 port, museum monster page, editor pass, faster GC
- ROM: `7bbf900` sent (first build on the Japanese Rev 1; v1.0 saves may be wiped, old savestates do not load).
- Changed: base ROM = Japanese Rev 1 (revmap/revport/revaudit tools; script, asm, insert constants, docs
  converted); Rev 1 additions translated ("Ouch!" wall bump, magic-circle messages, 31 status words); museum
  monster page labels/headers/elements in the VWF; GC: pass order for the museum page/list buffers, faster scan
  (~45% less per GC); editor fixes (names, battle past tense, maze wording) and breath verbs; emulator turbo
  default; shot lists (museum, maze_dmenu, stairs_up_prompt).
- Checked: build, lint, tests, tour 8/8, town speed = JP (360 loops/120f), regression shots vs the previous
  build (only intended diffs), a full battle from a maze walk, museum page open/close/paging.
- Open: museum page opens in ~31 frames (JP 9) and shows a few frames of garbage while closing; AC/HP minus
  signs 8 px; status.md Next.

## 2026-11-12 - museum items, unidentified names, Lvl, GC visible columns
- ROM: `3869893` sent.
- Changed/fixed: see docs/status.md "tenth session".
- Open: museum monster room (layout 3), reference translation patch needs the matching Japanese dump,
  photographer round trip on the reference (blocked by that).

## 2026-11-11 - render speed, shop 'AC' fix
- ROM: `00a8b90` sent.
- Changed: shift-table Glyph, unrolled hot loops, one bank switch per cell write; card age stays 8 px.
- Measured: cursor move without a party 55k instructions (was 74k), reaction frame 6-12 (JP 2).
- Fixed: garbled 'AC' in the shop header (shipped in 2edfeec).
- Open: per-tile bookkeeping is now the cost; flicker; 8 px separators/labels.

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
