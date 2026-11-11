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
