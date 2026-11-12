---
skill: triage
project: wizardry-empire
summary: Reproduce and diagnose one hang/crash report.
access: write (case dir)
updated: 2026-11-12
---

# Crash triage - Wizardry Empire (GBC)

> **Before you start:** paths below are relative to `wizardry-empire/`. Read the open entries in this skill's
> `feedback.md` (same folder) and apply their proposed rules. Binding terms: `wizardry-empire/glossary.md`.


You get one hang or crash report (a description, usually a savestate and inputs). Reproduce it, find where and why
the CPU gets stuck, and say whether the patch or the original game is at fault. You diagnose; you do not fix.
Do not edit `asm/`, `script/` or `tools/`; no git; no subagents. Write only `work/triage/<case>/` (notes + scratch).

## Read first
`docs/re/vwf.md` (every hook the patch installs, its RAM: WRAM banks 6/7 only - see `docs/re/tasks.md` for the
game's task stacks at `$CE00-$CFFF` - bank-0 stubs at
`$0038`, `$00B1-$00F0` (stub area 1), `$19B4-$1A3A` (stub area 2, the dead monster-panel routine),
`$3FF0-$3FFF` (Stub_Measure); hooks at `$1443`, `$10A4`, `$173C`, `$1789`, `$17D6`, `$1B58`, `$1C2A`, `$1CB3`,
`$1D1E`, `$24E8` (see `asm/vwf.asm`), code in ROM bank `$40`) and `docs/re/text.md`.

## Steps
1. Reproduce with `python3 tools/emu.py --state STATE --seq "..." --out work/triage/<case>/repro` (exit 2 = hung;
   `log.txt` has PC, bank and backtrace). No state? Get there with `tools/routes/tour.txt` routes.
2. Same inputs on the original ROM (`--rom rom/wizardry_empire_j.gbc`; build its own state, states are not
   interchangeable). Hangs there too = original-game behaviour.
3. Find the stuck loop: `regs()`, `backtrace()`, `disasm` around the PC; `trace.start(with_regs=True, with_mem=True)`
   for the frames before the hang. Run the sanitizer (`sanitize.start`, `sanitize.report`) on both ROMs and diff the
   sites: entries only on the English build point at the patch.
4. Map the PC/bank to the patch: assemble symbols with
   `python3 -c "import sys;sys.path.insert(0,'tools');import asm;a=asm.assemble('asm/main.asm');print(a.sym)"`.

## Report: your final message (write `work/triage/<case>/report.md` too only if your tools allow it)
- Reproduced? Exact inputs + state. Original ROM behaviour.
- Where it hangs: PC/bank, the loop, the condition it waits on, the call chain.
- Cause: which hook or data (with evidence), or "original game".
- Suggested fix (what to change and why), and how to verify it.


## Feedback (end of every run)
End your final report with this block; the coordinator files it in `skills/triage/feedback.md` and in
`agent-log/YYYY-MM.md` (you do not edit those files yourself):

```
## Feedback
- Task: <one line>
- Worked: <what went well, worth keeping>
- Friction: <what slowed you down or was unclear in this skill or the tools>
- Proposed rule change: <a concrete change to skill.md, or "none">
```

## Display corruption (no hang) (2026-11-12)
1. Reproduce from a state of the SAME build; build scratch copies from `git show <commit>:path`, never the
   working tree, and compare the ROM sha1 with the reported build.
2. Write-watch one bad cell (WRAM bank 3 buffer) and follow the code that writes the wrong code; then watch
   that slot's allocation bit (wBits $DF60 + code/8, bank 7), owner (bank 6 $D800 + code*2) and wVer.
3. Symbolise backtraces with build/wizardry_empire_en.sym.
4. Prove the cause by poking the suspected guard variable in a state just before the bad frame.

- Before chasing "two owners of one code": read the attribute's VRAM-bank bit (+$400) and the bank-6 cell map; in
  the split layout a cell with bit 3 set is code | $80, a different slot.
- A stale cell shows as NO write to the bad cell: write-watch the whole row/box and look for the gap.
- Scratch builds: `git archive HEAD wizardry-empire | tar -x -C <case>/scratch`, symlink `rom/` and
  `tools/gbemu-cli`, then build.py / tour.py / pytest run in place.

## Reproduce on HEAD first; slowdowns (2026-11-12)
- Step 1: reproduce on HEAD and note the ROM sha1. If HEAD does not reproduce, bisect between the reported commit
  and HEAD with git-archive scratch builds before diagnosing: a later commit may only hide the bug.
- Slowdown / performance (no hang): `emu.loops(g)` = main-loop passes per 120 frames (count-only breakpoint on
  0:07C5; 360 at town/camp idle); put count-only breakpoints after each cache-hit test (PLHit, RectCacheHit,
  NameCacheHit) to find the failing condition, then write-watch its guard variable.
- WRAM bank writes: `g.mem_write(0, data, region='wram', offset=bank*0x1000 + (addr - 0xD000))`.
- "Clean on build X" from one screenshot is unreliable for allocator bugs (ring position, input timing): run the
  inputs on the good build from its own state AND from the bad build's state, and check graphics integrity (VRAM
  against the DMA source), not only the screenshot.
- Check `wLayout` against the JP buffer's attribute bank bits early: a stale layout puts text into game graphics.
- gbdis: `gbdis.py 2D:63EB 20` (hex bank:addr) or `gbdis.py 45 0x63eb 20` (decimal bank).

