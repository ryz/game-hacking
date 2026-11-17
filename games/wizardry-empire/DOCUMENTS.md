# Documentation map and rules (Wizardry Empire)

Every document of this game belongs to one of these places (paths from `games/wizardry-empire/`). The same fact
may appear in a design doc and a tech doc; that overlap is intended (different readers), but the two must agree.

| Folder / file | Reader | What goes there |
|---|---|---|
| `design/` | game designers | How the game works: rules, formulas, data tables, quirks. No ROM addresses. |
| `tech/` | engineers (ROM work, modding, verifying the design docs) | How the game systems are implemented: record layouts, RAM, routines, data tables at their addresses, how each fact was established. |
| `shots/<set>/` | everyone | Reference screenshots (original and English side by side), made by `translation/tools/shoot.py`. |
| `saves/` | everyone | Test saves made by the tools; list in `saves/README.md`. |
| `translation/docs/re/` | engineers working on the translation patch | Reverse-engineering notes on text, display and the patch itself (text engines, small font, screen buffers, where each text lives). See `translation/docs/re/README.md`. |
| `translation/docs/status.md` | everyone | Current snapshot of the translation: what works, what is next, known issues. |
| `translation/docs/progress-log.md` | everyone | History, newest first, append-only; every test ROM sent with its commit. |

Who writes what: tracer agents write `tech/` and `translation/docs/re/` (skills/tracer), design-writer agents write `design/`
(skills/design-writer), the coordinator files and commits. The skills describe how to do the job; the rules below
describe the documents and apply to everyone, people included.

## Rules for all documents

- **ROM revision.** Facts refer to the Japanese **Rev 1** ROM unless marked "(v1.0)".
- **Names.** English names follow `translation/glossary.md`. Give the Japanese name next to the English one in data tables
  (a JP column) and on first mention in prose where it helps someone compare with the original.
- **Truth lives in `tech/`.** Every number in a design doc must also appear in a tech doc (or a generated table)
  with its source. When a fact changes, fix the tech doc first, then the design doc.
- **Generated tables are never edited by hand.** `design/items_table.md` and `design/monsters_table.md` come from
  `python3 tools/designtables` (run from `translation/`); change the generator instead.
- **Open questions.** Each system document ends with an "Open questions" section: what is not known yet and what
  was tried. Never fill a gap with a guess presented as fact.
- **Cross-links.** Each design section ends with a `Tech:` link to the matching tech section; each tech section
  starts with a `Design:` link where one exists. Relative Markdown links (`../tech/combat.md#...`). Check them with
  `python3 tools/doclinks.py` (run from `translation/`; checks the whole game folder, 0 broken).
- **Dates.** A dated note says `(YYYY-MM-DD)`; status and history live in `status.md` / `progress-log.md`, not in
  the system documents.

## Design documents (`design/`)

Notation, confidence tags, terms and structure for design documents are defined once in
[design/README.md](design/README.md) ("Notation and style"). In short: no addresses or hex, decimal numbers,
`NdS+B` dice, `Rnd(a, b)` in pseudocode, plain formulas, tags (verified) / (inferred) / (computed) / (game text)
with untagged meaning data, quirks in `design/findings.md`, each section ending with a `Tech:` link.

## Tech documents (`tech/`, `translation/docs/re/`)

- **Addresses** as `BB:AAAA`, bank and address in hex (`2D:63EB`; bank `00` is the fixed bank), RAM as `$C880`
  (WRAM bank as `bank 3 $D000` where it matters). Record fields as `+$0C`. Write a bank in prose as `$2D (45)`.
  `script/*.json` files store banks in decimal: convert when citing.
- **Source tag for each fact:** `(code BB:AAAA)`, `(data BB:AAAA)`, `(emulator)` with the state/route used,
  `(display)` (only seen in on-screen text such as the museum), `(inferred)`.
- **No addresses in headings.** Put a section's addresses on a `Code:` line under the heading, so links from the
  design docs get readable anchors.
- **Reproducible:** name the script, state or route that shows a fact when it took more than reading code.
- Translation-patch notes (`translation/docs/re/`) also say which patch code (`translation/asm/`, `translation/tools/`) depends on the fact.
