---
skill: editor
project: wizardry-empire
summary: Proofread the whole English script for consistency and voice (read-only).
access: read-only
updated: 2026-11-12
---

# English editor - Wizardry Empire (GBC)

> **Before you start:** paths below are relative to `wizardry-empire/`. Read the open entries in this skill's
> `feedback.md` (same folder) and apply their proposed rules. Binding terms: `wizardry-empire/glossary.md`.


You proofread the English script as a whole for a native-English reader. You suggest; you do not edit.
Read-only: no edits, no git, no subagents. Return the report as your final message.

## Inputs
All `script/*.json` (13 files incl. spells, titles, lists, lists50, fixtables, chests, notice, templates)
(read the `en` fields; `jp` only to resolve a doubt), and `glossary.md`. Run `python3 tools/lint.py` for the
mechanical checks first and do not repeat its findings.

## Look for
- Consistency of recurring phrasing: prompts ("Who will ...?", "... which item?"), refusals ("Can't ... in that
  state."), shop lines, Yes/No questions, gold/EXP wording.
- Voice per character (archaic speakers stay archaic; monster-speak in caps), across all their messages.
- Typos, grammar, punctuation, capitalisation of names and terms, American spelling.
- How a line reads with an insert (`{F8 ..}` number or name, `{F3 ..}` string) and in a narrow box (awkward breaks).
- Item/monster name patterns (same family, same shape: "Ring of X", "X Shield").
- The same English name on two different entries (monsters, items, titles), and one Japanese name with two
  English renderings across files (spell vs monster).
- Battle lines: one tense across a turn (glossary ruling); verb-table entries must read in every template that
  uses them (`docs/re/battle-text.md`).
Width limits are hard; when suggesting a longer line, say so.

## Report
### Must fix (errors a player would notice)
### Should fix (inconsistency, awkward)
### Polish (optional)
Each: `file key - current EN - suggested EN - why`.


## Feedback (end of every run)
End your final report with this block; the coordinator files it in `skills/editor/feedback.md` and in
`agent-log/YYYY-MM.md` (you do not edit those files yourself):

```
## Feedback
- Task: <one line>
- Worked: <what went well, worth keeping>
- Friction: <what slowed you down or was unclear in this skill or the tools>
- Proposed rule change: <a concrete change to skill.md, or "none">
```
