# Documentation map and rules (Wizardry Empire)

Every document in `docs/` belongs to one of these places. The same fact may appear in a design doc and a tech doc;
that overlap is intended (different readers), but the two must agree.

| Folder / file | Reader | What goes there |
|---|---|---|
| `design/` | game designers | How the game works: rules, formulas, data tables, quirks. No ROM addresses. |
| `tech/` | engineers (ROM work, modding, verifying the design docs) | How the game systems are implemented: record layouts, RAM, routines, data tables at their addresses, how each fact was established. |
| `re/` | engineers working on the translation patch | Reverse-engineering notes on text, display and the patch itself (text engines, small font, screen buffers, where each text lives). See `re/README.md`. |
| `shots/<set>/` | everyone | Reference screenshots (original and English side by side), made by `tools/shoot.py`. Current set: `rev1_tour/`. |
| `status.md` | everyone | Current snapshot: what works, what is next, known issues. |
| `progress-log.md` | everyone | History, newest first, append-only; every test ROM sent with its commit. |

Who writes what: tracer agents write `tech/` and `re/` (skills/tracer), design-writer agents write `design/`
(skills/design-writer), the coordinator files and commits. The skills describe how to do the job; the rules below
describe the documents and apply to everyone, people included.

## Rules for all documents

- **ROM revision.** Facts refer to the Japanese **Rev 1** ROM unless marked "(v1.0)".
- **Names.** English names follow `glossary.md`. Give the Japanese name next to the English one in data tables
  (a JP column) and on first mention in prose where it helps someone compare with the original.
- **Truth lives in `tech/`.** Every number in a design doc must also appear in a tech doc (or a generated table)
  with its source. When a fact changes, fix the tech doc first, then the design doc.
- **Generated tables are never edited by hand.** `design/items_table.md` and `design/monsters_table.md` come from
  `python3 tools/designtables`; change the generator instead.
- **Open questions.** Each system document ends with an "Open questions" section: what is not known yet and what
  was tried. Never fill a gap with a guess presented as fact.
- **Cross-links.** Each design section ends with a `Tech:` link to the matching tech section; each tech section
  starts with a `Design:` link where one exists. Relative Markdown links (`../tech/combat.md#...`).
- **Dates.** A dated note says `(YYYY-MM-DD)`; status and history live in `status.md` / `progress-log.md`, not in
  the system documents.

## Design documents (`design/`)

- **No addresses, no hex.** No `BB:AAAA`, no RAM, no record offsets, no routine names. Numbers in decimal.
- **Plain formulas.** Dice as `NdS+B` (sum of N rolls of 1..S, plus B). A range roll as "a random number from 0 to
  19". Short formulas in plain math, e.g. `hit if roll ≥ 11 + target AC − weapon bonus`. Use C#-style pseudocode
  only where a rule branches (several cases, caps, special rules):

  ```csharp
  int slots = Math.Min(9, Math.Max(spellsKnown, level - openingLevel + 1));
  ```
- **Confidence tag per number or rule:** **(verified)** seen in the running game, **(data)** read from the game's
  own tables, **(inferred)** reasoned from code or data but not observed. Untagged means data.
- **Structure:** an Overview a designer can read in two minutes, then one section per system with tables. Explain
  what a value means for play ("a Fighter needs 1200 EXP for level 2") before how it is computed.
- **Quirks:** behaviour that looks unintended (an ignored roll, an inverted bonus) is stated as the game does it,
  with a link to `design/findings.md`, where each quirk gets what the game does, what was probably intended and how
  sure we are.

## Tech documents (`tech/`, `re/`)

- **Addresses** as `BB:AAAA`, bank and address in hex (`2D:63EB`; bank `00` is the fixed bank), RAM as `$C880`
  (WRAM bank as `bank 3 $D000` where it matters). Record fields as `+$0C`. Write a bank in prose as `$2D (45)`.
  `script/*.json` files store banks in decimal: convert when citing.
- **Source tag for each fact:** `(code BB:AAAA)`, `(data BB:AAAA)`, `(emulator)` with the state/route used,
  `(display)` (only seen in on-screen text such as the museum), `(inferred)`.
- **Reproducible:** name the script, state or route that shows a fact when it took more than reading code.
- Translation-patch notes (`re/`) also say which patch code (`asm/`, `tools/`) depends on the fact.
