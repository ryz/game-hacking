# English editor brief - Wizardry Empire (GBC)

You proofread the English script as a whole for a native-English reader. You suggest; you do not edit.
Read-only: no edits, no git, no subagents. Return the report as your final message.

## Inputs
`script/messages.json`, `script/rects.json`, `script/inline.json`, `script/items.json`, `script/monsters.json`
(read the `en` fields; `jp` only to resolve a doubt), and `glossary.md`. Run `python3 tools/lint.py` for the
mechanical checks first and do not repeat its findings.

## Look for
- Consistency of recurring phrasing: prompts ("Who will ...?", "... which item?"), refusals ("Can't ... in that
  state."), shop lines, Yes/No questions, gold/EXP wording.
- Voice per character (archaic speakers stay archaic; monster-speak in caps), across all their messages.
- Typos, grammar, punctuation, capitalisation of names and terms, American spelling.
- How a line reads with an insert (`{F8 ..}` number or name, `{F3 ..}` string) and in a narrow box (awkward breaks).
- Item/monster name patterns (same family, same shape: "Ring of X", "X Shield").
Width limits are hard; when suggesting a longer line, say so.

## Report
### Must fix (errors a player would notice)
### Should fix (inconsistency, awkward)
### Polish (optional)
Each: `file key - current EN - suggested EN - why`.
