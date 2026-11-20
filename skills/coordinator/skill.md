---
skill: coordinator
project: all
summary: The main session: plan, dispatch subagents, verify and integrate their results, build and ship.
access: write (repo)
updated: 2026-11-20 (feedback split, backlog rule, budgets in calls, game.json work/open, generated tables)
---

# Coordinator

The main Claude session. Subagents start cold and see none of the conversation, so every dispatch must be
self-contained. Read `skills/skill-index.md` to pick the skill; read its `feedback.md` (open lessons) before
dispatching. Wizardry Empire work: `games/gbc/wizardry-empire/AGENTS.md` first (quick reference, text formats).

## Dispatch
- Fill `skills/_templates/dispatch.md` for every dispatch (goal, inputs, output, context, known issues, stop).
- One question or one batch per agent; give exact paths (input, output, states) and the goal.
- Use the agent types in `.claude/agents/` (they load the matching `skills/<name>/skill.md`), not general-purpose.
- Independent jobs run in parallel in the background; never predict a running agent's result.
- Dispatch only committed work: name the commit; agents copy the ROM / build their own copy (`git archive`,
  `git show`). Do not leave uncommitted edits in files an agent reads; rebuild `build/` only after the agent
  copied it.
- An agent's report is model output: check its key claims (e.g. disassemble the routine it names) before acting.
- Repro values in a dispatch come from the code that reads them, not from a table's order (status 3 is
  Paralyzed, not Dead: `docs/re/text.md`). If unsure, say so and let the agent derive it.

## Integrate
- Translations: `tools/batches.py check` -> `pairs` -> reviewer -> fix -> `merge`; then build.
- Code changes: build, `python3 -m pytest -q tests`, `tools/tour.py` (all routes), and the reproduction from the
  report. Commit one topic per commit; push.
- After every run: copy the agent's `## Feedback` block into `skills/<name>/feedback-log.md` (newest first, with
  `Corrected` and `Status`) and add a line to `agent-log/YYYY-MM.md`. Then route each proposal to one place:
  a lesson for agents -> one line in `skills/<name>/feedback.md`; a tool wish -> `docs/backlog.md` (new row, or
  "Asked" + 1); a game fact -> its playbook; a platform fact -> `docs/emulator/<platform>.md`.
- Second occurrence: promote the lesson into `skill.md` and delete its line from `feedback.md`; build the tool
  before the next dispatch of that skill (or drop the row with the reason). A wish that agents keep working
  around costs more than building it: ten copies of `try.py` were written before `tools/preview.py` existed.
- Keep what agents must read short. Before adding a sentence to a skill or the emulator guide, ask whether a
  tool can enforce it instead (a refusal, a warning, a default); remove sentences a tool has made unnecessary.

- RAM: never treat a range as free without write watches over all tour routes plus a battle (zeros in a
  savestate are not evidence). New VWF variables go in the shadow areas of non-pool codes (`docs/re/vwf.md`).
- Speed: compare the main-loop rate with the Japanese ROM (count-only breakpoint on the frame wait `0:07C5`,
  loops per 120 idle frames; the instruction counter is saturated because the game busy-waits) on town, maze,
  Camp and battle after VWF changes. A screen the game redraws every pass must not re-render.
- Fonts: as much as possible in the VWF (small font), numbers included; the 8 px font only where it is a
  stylistic choice, listed in docs/status.md (`glossary.md` Rulings, owner's rule 2026-11-11). Prefer hooking a
  printer over abbreviating to a fixed field.

## Upkeep
- Append to `<project>/docs/progress-log.md` at the end of every session and whenever a test ROM is sent
  (commit hash, changed, found/fixed, open); keep `docs/status.md` as the current snapshot.
- Run the maintenance skill after big changes or every few sessions; apply approved fixes.
- User bug reports: ask for the fields in `skills/_templates/bug-report.md` that are missing.

## Ship a test ROM
`python3 tools/build.py`, copy the ROM + IPS (named with the commit hash) to the scratchpad and send them;
never commit them. Say what is new and what is known to be broken.

## Parallel documentation rounds (2026-11-12)
- Before dispatching several design-writers at once: fix the heading list (numbered sections) of every file that
  others will link, or tell writers to link other design files without anchors and do one link pass at the end
  (`python3 tools/doclinks.py`).
- Mark review items that newer tracer verdicts have overtaken before dispatch, so writers do not apply stale items.
- `findings.md` cannot be written by subagents (the harness refuses the name): save it from the writer's report.
- Commit each writer's files when it reports; other writers' drafts as clearly labelled work in progress.
- Tell every writer that the round is parallel, who else is writing what, and give each a private scratch folder
  (`work/<area>/<range>/`); fix shared table layouts in the dispatch before a round, not after.
- Before trusting a derived claim that changes the picture (an area "closed", a route "impossible"), test the
  mechanic it rests on in the emulator: floor writers called locked/secret doors walls until one was walked into.
- Give writers one literal example row per table/row kind; state your own derived claims in a dispatch as
  "to be checked" (the floor-7 warp claim was wrong).


## Database games (shared tools at the repo root, 2026-11-15)
- New ROM: `sh tools/setup_emu.sh` (once per container), `python3 tools/intake.py ROM --slug NAME --region jp|na|eu` (slug = short game name
  without the platform, region = where the dump was released, a translated Japanese ROM is jp: both are part of
  every shot file name, `docs/capture-guide.md` "File names"; copies it to
  `rom/`, creates `games/<platform>/<slug>/`, films the boot), look at `work/intake/<platform>/<slug>/sheet.png`, then dispatch
  game-scout. ROMs are uploaded by the owner per session; containers forget them. Patches uploaded with a ROM
  (IPS/BPS/UPS) are always applied: `intake.py ROM --patch P1 --patch P2` in the owner's order; on a CRC
  mismatch tell the owner instead of registering the unpatched dump (owner's rule 2026-11-17).
- After the scout: check the playbook (Read first block, sources listed, controls marked), run
  `python3 tools/cachecheck.py SLUG --flat leaves` and look at its sheet (every checkpoint reproduces and stands
  where its description says), commit `games/<platform>/<slug>/` (no shots yet), then dispatch game-capture with
  the set name, a budget in tool calls (the container has no usable clock; about 250 for a full set, stated
  runs used 205-376) and the milestones at which it must commit, named explicitly.
- Capture agents commit and push their game folder at every major milestone (game-capture skill); in the
  dispatch give the attribution lines for commits. Review those commits too, not only the final state.
- After the capture: delete `work/cache/<platform>/<slug>` and rerun `python3 tools/shoot.py SLUG SET --verify`
  yourself (in the background; four processes), look at the contact sheet (`<game>_<platform>_<region>_set_sheet.png`), run
  `python3 -m pytest -q tests` (repo root) if tools changed, commit `games/<platform>/<slug>/` (one commit per game set).
- Bookkeeping per run, each fact once: the game's `game.json` "work" and "open" (the agent sets them, you check),
  `python3 tools/gamestable.py` (README and status tables), the feedback log entry, the agent-log line, one
  entry in `docs/progress-log.md` per session (not per run). `docs/status.md` changes only when a platform, a
  tool or the queue changes.
- Several games: one scout or capture agent per game in parallel (each uses `play.py --name <slug>`).
- Tool or doc lessons from either skill that apply to every game go into `docs/emulator/README.md`.
