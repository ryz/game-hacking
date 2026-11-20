---
skill: editor
---

# Feedback - editor

Running log for this skill, newest first. Status: `open` (proposed change waiting), `logged` (nothing to
promote), `promoted YYYY-MM-DD`, `superseded`. Promote a lesson into `skill.md` when it shows up in two entries or
the owner states it as a rule; then bump `updated:` in skill.md and mark the entries. Never delete entries.

## Entries

### 2026-11-12 - readability review of docs/design/ (document review, not script)
- Task: review the 9 design documents + table headers for a game-designer reader; proposals only.
- Worked: full read, then greps across files for engineering words (flag, record, field, routine, caller, code N,
  mode N, school N), random-helper variants, % style and armour/armor - objective lists; a script for one Tech:
  line per section.
- Friction: the skill covers script proofreading only (widths, lint, Must/Should/Polish), so the report format was
  adapted; design rules were split between docs/README.md and docs/design/README.md and disagreed on "(data)".
- Proposed rule change: a "Document review" mode in skill.md (inputs: docs/README.md + docs/design/README.md;
  checks: notation, engineering-word grep, duplicated rules -> links, glossary names, American spelling; report per
  file verdict + numbered quote -> proposal, then cross-file); one owner for notation.
- Corrected: notation now has one owner (docs/design/README.md "Notation and style", tags defined incl. computed,
  game text, v1.0); table generators fixed; per-file items go to a design-writer revision round
  (work/design/review-1.md).
- Status: open (Document review mode for skill.md: promote on a second document review)

### 2026-11-12 - full proofread after the Rev 1 move
- Task: proofread all 13 script files for consistency, voice, typos, glossary; report only.
- Worked: one flat JP/EN dump in the scratchpad; lint first; battle-text.md for verb inserts.
- Friction: skill inputs listed only 5 files; no way to see which battle template a verb uses; no width
  helper for suggested rect lines; lint misses Ifrit/Efreet.
- Proposed rule change: inputs = all script/*.json; look for duplicate names and battle tense; a width helper.
- Corrected: Must fixes applied (Exorcist Arrow, Guardian Shield, Ifrit, Cutthroat, Thief line, battle past
  tense) plus most Should/Polish; checked はまや/かごのたて readings. Not applied: attack-verb templates (need a
  battle sheet), 29:6e95 and 26:6fde (need a screen check), Maze Robe/Magic Gate (open ruling), ADISH caps,
  plural counts. Build/lint/tour pass.
- Status: promoted 2026-11-12 (inputs, duplicate names, battle tense - fixes to the skill's own scope); width
  helper -> tool backlog

