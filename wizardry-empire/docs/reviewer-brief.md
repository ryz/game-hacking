# Translation reviewer brief - Wizardry Empire (GBC)

You review one translated batch. Read-only: no edits, no git, no subagents. Mechanical validity (width, rows,
insert codes, Yes/No) is enforced by `tools/batches.py check`; judge translation quality.

## Inputs (paths in your dispatch)
- `work/tl/<batch>.pairs.txt`: `>> key [kind]` / `JP:` / `EN:` per entry, in ROM order (neighbours are context;
  ` / ` = row break, ` | ` = rect row break). Read all of it.
- `glossary.md`.

## Judge
- Accuracy: mistranslation, omission, addition, wrong speaker, reversed meaning. Quote the JP and say what it means.
  Kana-only Japanese is easy to misread: check homophones against context.
- Consistency with `glossary.md` (names, classes, statuses, places) and with neighbouring entries.
- Insert codes: the sentence must read right with a name or number inserted at `{F8 ..}` / `{F3 ..}`.
- Naturalness and register (archaic speakers, monster-speak in caps).

## Report (your final message)
### Critical (meaning reversed, broken insert grammar, wrong speaker)
### Important (clear mistranslation, glossary inconsistency)
### Minor (style)
Each: `key - JP gist - problem - suggested EN`.
### Assessment
Approved | Needs fixes - one sentence why.
