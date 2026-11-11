---
skill: maintenance
project: all
summary: Read-only repo health check; drafts fixes for doc/skill drift, stale feedback and broken references.
access: read-only
updated: 2026-11-11
---

# Maintenance - repo health check

> **Before you start:** read the open entries in `feedback.md` (same folder) and apply their proposed rules.

You check that the repo's instructions still match reality. Read-only: no edits, no git, no subagents. You
draft every fix as a concrete diff-like suggestion; the coordinator applies what the user approves.
Run it after a big change (asm refactor, new tool, new skill) or every few sessions.

## Checks (per project, currently `wizardry-empire/`)
1. **References:** every path, tool, script, symbol and command named in `AGENTS.md`, `skills/**/skill.md`,
   `skills/skill-index.md`, `wizardry-empire/README.md` and `wizardry-empire/docs/**` exists
   (`ls`, `grep`, `python3 tools/<x>.py --help`). Asm symbols: assemble once with
   `python3 -c "import sys;sys.path.insert(0,'wizardry-empire/tools');import asm;print(sorted(asm.assemble('wizardry-empire/asm/main.asm').sym))"`.
2. **Docs vs code:** claims in `docs/re/vwf.md`, `docs/re/text.md`, `docs/re/tasks.md` and the skills about
   RAM, banks, hook addresses and data layouts still match `asm/vwf.asm` and `tools/insert.py`
   (e.g. RAM ranges, stub areas, control codes). Flag any contradiction with both quotes.
3. **Skills:** every `skills/<name>/` has `skill.md` + `feedback.md` with frontmatter, an index block with all six
   fields, and (if it runs as a subagent) a `.claude/agents/<name>.md` wrapper pointing at it. Feedback
   entries `open` for more than two sessions, and lessons repeated in two or more entries but not promoted.
4. **Status and log:** `docs/status.md` "Done/Next/Known issues" vs `docs/progress-log.md` and the git log
   (`git log --oneline -30`): done items still listed as next, fixed bugs still listed as known.
5. **Script hygiene:** `python3 tools/lint.py` and `python3 tools/build.py` (from `wizardry-empire/`) pass;
   note warnings that keep recurring.
6. **Rules:** no game data tracked (`git ls-files | grep -iE '\.(gbc?|sav|state)$'` must be empty).

## Report (your final message)
### Broken (wrong or missing references, contradictions)
### Drift (stale status/feedback, unpromoted lessons)
### Suggestions
Each: `file:line - finding - proposed fix (exact text)`. End with the `## Feedback` block.

## Feedback (end of every run)
End your final report with this block; the coordinator files it in `skills/maintenance/feedback.md` and in
`agent-log/YYYY-MM.md`:

```
## Feedback
- Task: <one line>
- Worked: <what went well, worth keeping>
- Friction: <what slowed you down or was unclear in this skill or the tools>
- Proposed rule change: <a concrete change to skill.md, or "none">
```
