# Visual-QA brief - Wizardry Empire (GBC)

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
- a name or term that differs from `glossary.md`; English typos.
Not issues (`ok`): text still typing out; a box mid-fade; black or loading frames; the cursor mid-blink;
fixed-width 8 px letters in a few places (fallback font).

## Verdict file
One line per sheet: `path<TAB>ok|issue<TAB>note` (for issues: where on screen, the visible text, what is wrong).
Return a short summary (counts and the issues) as your final message.
