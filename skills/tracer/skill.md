---
skill: tracer
project: wizardry-empire
summary: Answer one reverse-engineering question about where/how text is printed.
access: write (notes file)
updated: 2026-11-12
---

# Tracer - Wizardry Empire (GBC): reverse-engineering questions

> **Before you start:** paths below are relative to `wizardry-empire/`. Read the open entries in this skill's
> `feedback.md` (same folder) and apply their proposed rules. Binding terms: `wizardry-empire/glossary.md`.


You answer one reverse-engineering question from your dispatch, e.g. "where do the status values on the character
sheet come from and how are they printed?". You find and explain; you do not patch. Do not edit `asm/`, `script/`
or `tools/`; no git; no subagents. Write only your notes file (path in the dispatch, normally
`work/re/<topic>.md`) and scratch files under `work/re/<topic>/`.

## Read first
`docs/re/text.md` (encoding, buffers, text engines, banks, data records) and `docs/re/vwf.md` (what the patch hooks).
Do not re-derive what they already state.

## Tools
- Static: `python3 tools/gbdis.py BANK ADDR [N]` (bank-aware disassembly of the original ROM `rom/wizardry_empire_j.gbc`),
  `tools/tbl.py` (`tbl.dec(bytes)` decodes text), the census tools (`tools/census_*.py`, `tools/chain_rects.py`).
- Dynamic: the emulator client (`tools/gbemu-cli/cli/py/gbemu.py`, docs `tools/gbemu-cli/cli/PROTOCOL.md` and
  `cli/SKILL.md`) via `tools/emu.py` (`emu.open_emu(rom, state)`, `emu.boot(g)`, `emu.press(g, keys)`).
  Use the ORIGINAL ROM for tracing the game's own code (`--rom rom/wizardry_empire_j.gbc`), the English build only
  to check how a hook behaves.
- Useful recipes: watch reads of a data table (`watch_add(addr, end, access="r", bank=B)`, then `regs()` /
  `backtrace()`); watch writes of a known tile value into the screen buffer (WRAM bank 3 `$D000-$DBFF`);
  count-only breakpoints + `break.log` to list every PC that writes a range; `trace.start(with_mem=True)` around one frame.
- Reaching screens: from power-on `boot` puts you in the town. Party/maze routes: `tools/routes/tour.txt`.
  Savestates from the original ROM and the English build are not interchangeable.
- Every state you save goes into the notes with its exact input list (start state + tokens); a state from a
  random walk without its inputs cannot be reproduced.
- `gbdis.py BANK 0xADDR`: bank decimal, address with `0x` (a bare number is read as decimal).
- A value you write to RAM to reach a state (status, class, flags): read how the printer turns it into a table
  index first; table order is not the encoding.
- Window buffer (`$D800`, attributes `$DC00`): the tile bank depends on attribute bit 3, so decode cells with
  their attributes (tbl.dec/census without attributes read some rects wrongly).
- Before proposing a hook, diff the English build against the original at the site (bytes and the buffer it
  writes): an existing stub or a stray patch there changes the answer.
- Garbled field in the English build: dump the EN `$D000` buffer for it first. Header bytes (`[bank][lo][hi]`)
  mean a raw copy of a redirected rect; a repeated value like `$29` means A was clobbered by a stub.

## Answer (your notes file, also your final message)
1. Answer in one paragraph.
2. Evidence: routine addresses (`BB:AAAA`), what each does (registers in/out), data layout with an example decoded
   from the ROM, and how you confirmed it (which watch/breakpoint fired, from which screen).
3. Hook proposal: the smallest patch that would route this text through the VWF (which instructions to replace,
   how many bytes are available, registers that must be preserved), and what script format the text would need.
4. Open questions / what you could not confirm.


## Feedback (end of every run)
End your final report with this block; the coordinator files it in `skills/tracer/feedback.md` and in
`agent-log/YYYY-MM.md` (you do not edit those files yourself):

```
## Feedback
- Task: <one line>
- Worked: <what went well, worth keeping>
- Friction: <what slowed you down or was unclear in this skill or the tools>
- Proposed rule change: <a concrete change to skill.md, or "none">
```
