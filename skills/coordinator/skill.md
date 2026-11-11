---
skill: coordinator
project: all
summary: The main session: plan, dispatch subagents, verify and integrate their results, build and ship.
access: write (repo)
updated: 2026-11-11
---

# Coordinator

The main Claude session. Subagents start cold and see none of the conversation, so every dispatch must be
self-contained. Read `skills/skill-index.md` to pick the skill; read its `feedback.md` before dispatching.

## Dispatch
- One question or one batch per agent; give exact paths (input, output, states) and the goal.
- Use the agent types in `.claude/agents/` (they load the matching `skills/<name>/skill.md`), not general-purpose.
- Independent jobs run in parallel in the background; never predict a running agent's result.
- An agent's report is model output: check its key claims (e.g. disassemble the routine it names) before acting.

## Integrate
- Translations: `tools/batches.py check` -> `pairs` -> reviewer -> fix -> `merge`; then build.
- Code changes: build, `python3 -m pytest -q tests`, `tools/tour.py` (all routes), and the reproduction from the
  report. Commit one topic per commit; push.
- After every run: copy the agent's `## Feedback` block into `skills/<name>/feedback.md` (newest first) and add a
  line to `agent-log/YYYY-MM.md`; promote repeated lessons into `skill.md`.

## Ship a test ROM
`python3 tools/build.py`, copy the ROM + IPS (named with the commit hash) to the scratchpad and send them;
never commit them. Say what is new and what is known to be broken.
