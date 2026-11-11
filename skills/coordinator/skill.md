---
skill: coordinator
project: all
summary: The main session: plan, dispatch subagents, verify and integrate their results, build and ship.
access: write (repo)
updated: 2026-11-12
---

# Coordinator

The main Claude session. Subagents start cold and see none of the conversation, so every dispatch must be
self-contained. Read `skills/skill-index.md` to pick the skill; read its `feedback.md` before dispatching.

## Dispatch
- Fill `skills/_templates/dispatch.md` for every dispatch (goal, inputs, output, context, known issues, stop).
- One question or one batch per agent; give exact paths (input, output, states) and the goal.
- Use the agent types in `.claude/agents/` (they load the matching `skills/<name>/skill.md`), not general-purpose.
- Independent jobs run in parallel in the background; never predict a running agent's result.
- An agent's report is model output: check its key claims (e.g. disassemble the routine it names) before acting.
- Repro values in a dispatch come from the code that reads them, not from a table's order (status 3 is
  Paralyzed, not Dead: `docs/re/text.md`). If unsure, say so and let the agent derive it.

## Integrate
- Translations: `tools/batches.py check` -> `pairs` -> reviewer -> fix -> `merge`; then build.
- Code changes: build, `python3 -m pytest -q tests`, `tools/tour.py` (all routes), and the reproduction from the
  report. Commit one topic per commit; push.
- After every run: copy the agent's `## Feedback` block into `skills/<name>/feedback.md` (newest first) and add a
  line to `agent-log/YYYY-MM.md`; promote repeated lessons into `skill.md`.

- RAM: never treat a range as free without write watches over all tour routes plus a battle (zeros in a
  savestate are not evidence). New VWF variables go in the shadow areas of non-pool codes (`docs/re/vwf.md`).
- Speed: compare the main-loop rate with the Japanese ROM (count-only breakpoint on the frame wait `0:07C5`,
  loops per 120 idle frames; the instruction counter is saturated because the game busy-waits) on town, maze,
  Camp and battle after VWF changes. A screen the game redraws every pass must not re-render.
- Fonts: words go through the VWF (small font); the 8 px font only for numbers and grid layouts
  (`glossary.md` Rulings, owner's rule 2026-11-11). Prefer hooking a printer over abbreviating to a fixed field.

## Upkeep
- Append to `<project>/docs/progress-log.md` at the end of every session and whenever a test ROM is sent
  (commit hash, changed, found/fixed, open); keep `docs/status.md` as the current snapshot.
- Run the maintenance skill after big changes or every few sessions; apply approved fixes.
- User bug reports: ask for the fields in `skills/_templates/bug-report.md` that are missing.

## Ship a test ROM
`python3 tools/build.py`, copy the ROM + IPS (named with the commit hash) to the scratchpad and send them;
never commit them. Say what is new and what is known to be broken.
