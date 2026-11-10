# Crash triage brief - Wizardry Empire (GBC)

You get one hang or crash report (a description, usually a savestate and inputs). Reproduce it, find where and why
the CPU gets stuck, and say whether the patch or the original game is at fault. You diagnose; you do not fix.
Do not edit `asm/`, `script/` or `tools/`; no git; no subagents. Write only `work/triage/<case>/` (notes + scratch).

## Read first
`docs/re/vwf.md` (every hook the patch installs, its RAM: WRAM0 `$CF00-$CFFF`, WRAM banks 6/7, bank-0 stubs at
`$0038`, `$00B1-$00F0`, `$1C11-$1C78`, `$3F50-$3FD9`, code in ROM bank `$40`) and `docs/re/text.md`.

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

## Report: `work/triage/<case>/report.md`, also your final message
- Reproduced? Exact inputs + state. Original ROM behaviour.
- Where it hangs: PC/bank, the loop, the condition it waits on, the call chain.
- Cause: which hook or data (with evidence), or "original game".
- Suggested fix (what to change and why), and how to verify it.
