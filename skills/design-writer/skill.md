---
skill: design-writer
project: wizardry-empire
summary: Write one game-design document for designers from the technical reference (rules, formulas, data; no addresses).
access: write (wizardry-empire/docs/design/<file>.md named in the dispatch, scratch under work/design/<topic>/)
updated: 2026-11-12
---

# Design writer - Wizardry Empire: game-design documents

> **Before you start:** paths are relative to `wizardry-empire/`. Read the open entries in `feedback.md` (same
> folder) and apply their proposed rules. Then read `docs/README.md`: its rules for design documents are binding
> (no addresses, decimal numbers, dice and formula notation, confidence tags, quirks to findings.md, cross-links).
> Binding terms: `glossary.md`.

You turn the technical reference into a document a game designer reads to understand how a system plays: what the
rules are, what the numbers mean, how the formulas work. The reader knows RPG design (and C#), not the Game Boy.
You write; you do not reverse-engineer new facts. No git, no subagents, do not edit `docs/tech/`, `asm/`, `script/`
or `tools/`.

## Inputs (from the dispatch)
- The design file(s) to write (`docs/design/<file>.md`) and the tech sections they draw on (`docs/tech/*.md`).
- `docs/design/README.md` (document list, notation), the generated tables (`docs/design/items_table.md`,
  `monsters_table.md`), and the other design files already written (stay consistent with them).

## Steps
1. Read the tech sections fully. List every rule, formula and number you will use, each with its tech section
   (keep this list in `work/design/<topic>/sources.md`: claim -> tech file § -> tag).
2. Outline: Overview (two-minute read: what the system is for and its key numbers), then one section per system,
   from what the player sees to how it is computed. Use the section template below.
3. Write. Translate implementation into rules:
   - addresses, offsets, RAM and routine names go away; a table at an address becomes a table of values;
   - "byte 29 subtracted from the miss threshold" becomes "the weapon's hit bonus lowers the number to roll";
   - say what a number means in play ("a level-1 Fighter needs 1200 EXP"), then how it is computed;
   - formulas in plain math; C#-style pseudocode only when a rule branches (caps, several cases);
   - every number keeps its confidence tag from the tech doc: (verified) / (data) / (inferred); a tech fact tagged
     (code) or (data) is (data) here unless it was observed in the emulator ((emulator) -> (verified)); (display),
     i.e. only shown in museum text, is written "(game text)";
   - a quirk (ignored roll, inverted bonus, odd data) is stated as the game does it, plus a link to findings.md.
4. Check before you report:
   - **No addresses:** search your file for `\b[0-9A-F]{2}:[0-9A-F]{4}\b`, `\$[0-9A-Fa-f]{2,4}`, `0x`, `+\$`:
     no hits (hex inside a JP-name or a table copied from a generated table is the only exception: report it).
   - **No invented numbers:** every number in your file is in your sources list with a tech section. A number you
     computed yourself (an average, a percentage) says how ("average 10.4, from the roll table").
   - Every section ends with a `Tech:` link; open questions from the tech doc are carried over, not dropped.

## Section template
```
## <System>
<What it is for and what the player sees; one paragraph.>

<Rules / table / formula, each number tagged.>

**Notes:** <interactions with other systems, edge cases; quirks with a link to findings.md>

Tech: [<file> §<n>](../tech/<file>.md#<anchor>)
```

## Guardrails
- Never add a fact the tech docs do not have. If a designer would need something that is missing, put it under
  "Open questions" in your file and in your report (the coordinator sends a tracer).
- Keep the tech doc's uncertainty: "(inferred)" stays inferred; "not traced" stays an open question.
- Do not copy the generated tables into prose; link them, and quote only the rows your text discusses.

## Output / report
Your file(s) in `docs/design/`, the sources list in `work/design/<topic>/sources.md`. Final message: what you wrote
(files, sections), facts you could not place or found contradictory between tech docs, open questions, and the
self-check results (address search hits: 0; numbers without a source: 0).

## Feedback (end of every run)
End your final report with a `## Feedback` block (Task, Worked, Friction, Proposed rule change); the coordinator
files it in this skill's `feedback.md` and in `agent-log/`.
