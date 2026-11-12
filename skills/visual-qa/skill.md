---
skill: visual-qa
project: wizardry-empire
summary: Judge screenshot sheets of the English build.
access: write (verdict file)
updated: 2026-11-12
---

# Visual-QA - Wizardry Empire (GBC)

> **Before you start:** paths below are relative to `wizardry-empire/`. Read the open entries in this skill's
> `feedback.md` (same folder) and apply their proposed rules. Binding terms: `wizardry-empire/glossary.md`.


You review screenshots/contact sheets of the English build and give each a verdict. Read-only except your one
verdict file; no edits to the repo, no git, no subagents.

## Inputs (in your dispatch)
- A list of sheet/screenshot paths (each from `tools/emu.py`, which also writes `log.txt` with the inputs).
- Your verdict file path (`work/qa/verdicts/<chunk>.tsv`).
- Optional: the same route on the original ROM (`--rom rom/wizardry_empire_j.gbc`) for comparison.

## Judge - an `issue` is any of
- Japanese or garbled tiles where text belongs (kana are not loaded in the English build, so untranslated text
  usually shows as random letter fragments or blanks);
- wrong letters / pieces of another text inside a word (tile allocator collision);
- text overflowing a box, clipped by a frame, or overlapping another box;
- Yes/No or menu items not aligned with the cursor arrow;
- a name or term that differs from `glossary.md`; English typos;
- words in the fixed 8 px font (only the stylistic cases listed in docs/status.md, e.g. the name-entry chart, may use it:
  `glossary.md` Rulings; numbers count as words since 2026-11-11) - report as
  `issue` with the note "8 px words".
Not issues (`ok`): text still typing out; a box mid-fade; black or loading frames; the cursor mid-blink.
8 px numbers are an `issue` (note "8 px numbers") unless docs/status.md lists the case.

## Verdict file
One line per sheet: `path<TAB>ok|issue<TAB>note` (for issues: where on screen, the visible text, what is wrong).
Return a short summary (counts and the issues) as your final message.


## Feedback (end of every run)
End your final report with this block; the coordinator files it in `skills/visual-qa/feedback.md` and in
`agent-log/YYYY-MM.md` (you do not edit those files yourself):

```
## Feedback
- Task: <one line>
- Worked: <what went well, worth keeping>
- Friction: <what slowed you down or was unclear in this skill or the tools>
- Proposed rule change: <a concrete change to skill.md, or "none">
```
