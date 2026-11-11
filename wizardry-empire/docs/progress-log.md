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
