---
skill: translator
project: wizardry-empire
summary: Translate one batch (work/tl/<batch>.json) JP->EN.
access: write
updated: 2026-11-11
---

# Translator - Wizardry Empire (GBC, 1999)

> **Before you start:** paths below are relative to `wizardry-empire/`. Read the open entries in this skill's
> `feedback.md` (same folder) and apply their proposed rules. Binding terms: `wizardry-empire/glossary.md`.


You translate one batch of the Japanese script into English for a fan patch. Wizardry Empire is a first-person
dungeon crawler in the classic Wizardry mould: a town of shops and guilds, a party of six, a deep maze, demons
and an Emperor of the abyss. Do all translation yourself; do not dispatch subagents.

## Read first
1. `glossary.md` - binding names, terms and rulings.
2. `script/messages.json` and `script/rects.json` - the voice used so far (match it).

## Input / output: `work/tl/<batch>.json`
A JSON list; fill every entry's `"en"` and change nothing else. Write the file with your file-edit tool.
- `kind: "msg"` (typewriter message): `jp` and `en` are strings, `\n` = next row of the box. The box is
  18 cells = `maxpx` (144) pixels wide; the font is proportional (about 5 px per letter). Keep the original's
  line structure: most messages use a blank row between lines (`\n\n`); keep the same leading newlines.
  - Copy every insert code `{F8 ...}` (number/name) and `{F3 ...}` (string) exactly, once each.
  - Yes/No choices: the cursor is placed by the game at fixed columns. Write them as `{col:N}Yes` / `{col:N}No`,
    where N = number of spaces before はい/いいえ in the Japanese, keeping the newlines between them.
  - Indented lines: a leading space is fine; use `{col:N}` only to line up with the cursor.
- `kind: "rect"` (fixed box `w` cells x `h` rows): `en` is a list of at most `h` rows, each at most `w*8` px.
  Row prefixes: `^` center, `>` right-align, `@N:` start at cell column N (use for Yes/No under a cursor).
  `{x:N}` jumps to pixel N inside a row (columns, e.g. inn prices).
- Characters available: ASCII letters, digits, `. , ! ? ' " - : ; / ( ) + % & =`, `…`, `●`. Nothing else.

## Validate
`python3 tools/batches.py check <batch>` must print OK; fix every ERROR (width, rows, insert codes, Yes/No).
Measure a line: `python3 -c "import sys;sys.path.insert(0,'tools');import text;print(text.width('Your line'))"`.

## Style
- Faithful: same information and order of ideas; idiomatic English, no additions, no summaries.
- Archaic/samurai speech (せっしゃ, ござる, ぬし) -> formal, slightly old-fashioned English, not pastiche.
  Monster-speak in katakana (ワレラ, タスケテ) -> ALL CAPS broken English.
- Glossary names exactly. If a line cannot fit, rephrase; never abbreviate glossary names.
- Prompts end with "?"; messages are sentences with full stops.

## Report (your final message)
`OK <batch> <n> entries` plus a list of `key - note` for anything uncertain (unclear Japanese, missing context).


## Feedback (end of every run)
End your final report with this block; the coordinator files it in `skills/translator/feedback.md` and in
`agent-log/YYYY-MM.md` (you do not edit those files yourself):

```
## Feedback
- Task: <one line>
- Worked: <what went well, worth keeping>
- Friction: <what slowed you down or was unclear in this skill or the tools>
- Proposed rule change: <a concrete change to skill.md, or "none">
```
