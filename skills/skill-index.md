---
updated: 2026-11-11
---

# Skill index

Routing map: which skill to load for a job. Each `<skill>/skill.md` is the source of truth; this file only points
to it. Every skill folder has a `feedback.md` - read its open entries before working.

## Quick start
1. Read `AGENTS.md` (repo rules) if you have not this session.
2. Pick the skill below; open its `skill.md` and the open entries in its `feedback.md`.
3. Subagents: the `.claude/agents/<skill>.md` wrapper loads the skill; the coordinator dispatches with exact paths.
4. End every run with a `## Feedback` block; the coordinator files it (feedback.md + `agent-log/`).

## Layers
- **Coordination:** coordinator (the main session).
- **Investigation:** tracer (where/how text is printed), triage (hangs/crashes).
- **Language:** translator -> reviewer -> (late) editor.
- **Verification:** playtester (plays toward a goal), visual-qa (judges screenshot sheets).
- **Documentation:** photographer (pixel-exact reference screenshots, English and original side by side).
- **Upkeep:** maintenance (repo health check: docs vs code, skills, feedback, status drift).

Typical chains: tracer -> (coordinator hooks it) -> translator -> reviewer -> build -> tour -> visual-qa;
user bug report -> triage -> coordinator fix -> playtester repro;
photographer set -> visual-qa (or reviewer with the compare images) for a screen-by-screen JP/EN check.

## Skills

### coordinator
- File: `skills/coordinator/skill.md`
- Use when: planning work, dispatching agents, integrating results, building and shipping test ROMs.
- Main output: commits, builds, test ROMs, filed feedback and agent-log lines.
- Also load: the skill of every agent it dispatches.
- Do not use for: delegating judgement it can verify cheaply itself.
- Guardrails: verify agent claims before acting; never commit game data; one topic per commit.

### translator
- File: `skills/translator/skill.md`
- Use when: a batch exists (`tools/batches.py split ...`) and needs English.
- Main output: the filled `wizardry-empire/work/tl/<batch>.json` (passes `batches.py check`).
- Also load: `wizardry-empire/glossary.md`.
- Do not use for: review, script-wide edits, hooking new text.
- Guardrails: edits only its batch file; glossary names exactly; no subagents.

### reviewer
- File: `skills/reviewer/skill.md`
- Use when: a translated batch passed `check` and `pairs` was generated.
- Main output: a ranked issue report (critical / important / minor) with suggested English.
- Also load: `wizardry-empire/glossary.md`.
- Do not use for: mechanical checks (lint/check do those), editing files.
- Guardrails: read-only.

### editor
- File: `skills/editor/skill.md`
- Use when: most of the script is translated; whole-script English pass.
- Main output: must-fix / should-fix / polish report.
- Also load: `wizardry-empire/glossary.md`, lint output.
- Do not use for: per-batch review, early in the project.
- Guardrails: read-only; width limits are hard.

### playtester
- File: `skills/playtester/skill.md`
- Use when: a build exists and a goal needs playing (e.g. "form a party, win a battle").
- Main output: report with route, states and issues (screenshot paths, repro inputs).
- Also load: `wizardry-empire/tools/routes/tour.txt` (known routes).
- Do not use for: diagnosing a hang (triage) or judging fixed sheets (visual-qa).
- Guardrails: writes only its session dir; never edits the repo.

### visual-qa
- File: `skills/visual-qa/skill.md`
- Use when: tour sheets or playtest sheets need a verdict.
- Main output: verdict file `path<TAB>ok|issue<TAB>note` + summary.
- Also load: `wizardry-empire/glossary.md`; the `tour_jp` sheets for comparison.
- Do not use for: playing the game.
- Guardrails: writes only its verdict file.

### tracer
- File: `skills/tracer/skill.md`
- Use when: we do not know where some text lives or which routine prints it.
- Main output: notes file with routines, data layout, evidence and a hook proposal.
- Also load: `wizardry-empire/docs/re/text.md`, `docs/re/vwf.md`, `docs/re/tasks.md`.
- Do not use for: patching; translation.
- Guardrails: traces the original ROM; writes only its notes/scratch dir.

### triage
- File: `skills/triage/skill.md`
- Use when: a hang or crash is reported (with state/inputs if possible).
- Main output: report with reproduction, stuck PC/loop, cause (patch or original) and suggested fix.
- Also load: `wizardry-empire/docs/re/vwf.md`, `docs/re/tasks.md`.
- Do not use for: fixing; general RE questions (tracer).
- Guardrails: diagnose only; writes only its case dir.

### photographer
- File: `skills/photographer/skill.md`
- Use when: we need exact reference images of screens/features/options/gameplay, JP vs EN (docs, review,
  regression comparison, the README).
- Main output: `wizardry-empire/work/shots/<set>/` (native + 3x + compare PNGs, `index.md`/`index.json`),
  published and committed to `wizardry-empire/docs/shots/<set>/`, and proposed `tools/routes/shots.txt` lines.
- Also load: `wizardry-empire/tools/routes/shots.txt`, `tools/routes/tour.txt`.
- Do not use for: judging the translation (visual-qa) or finding bugs on purpose (playtester).
- Guardrails: writes `work/shots/<set>/` and `docs/shots/<set>/`; commits only its shot set (no ROM/state files); never pushes.

### maintenance
- File: `skills/maintenance/skill.md`
- Use when: after a big change (asm refactor, new tool/skill) or every few sessions.
- Main output: Broken / Drift / Suggestions report with exact proposed fixes.
- Also load: `AGENTS.md`, `skills/skill-index.md`, the project's `docs/status.md` and `docs/progress-log.md`.
- Do not use for: fixing things itself; translation quality (reviewer/editor).
- Guardrails: read-only; every finding cites file:line and proposes exact text.

## Templates
`skills/_templates/`: `skill.md`, `feedback.md` (new skills), `dispatch.md` (every subagent dispatch),
`bug-report.md` (user and playtester bug reports).

## Adding a skill
Copy `skills/_templates/` to `skills/<name>/`, fill `skill.md`, add a block here with the six fields (File,
Use when, Main output, Also load, Do not use for, Guardrails) and a `.claude/agents/<name>.md` wrapper if it runs
as a subagent.
