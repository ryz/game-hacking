# Agent instructions

This repository holds fan-translation projects, one directory per game. Each project is self-contained
(its own `tools/`, `docs/`, `script/`, `tests/`). Current projects:

| Directory | Game | Platform |
|---|---|---|
| `wizardry-empire/` | Wizardry Empire (J) -> English | Game Boy Color |

## Rules (all projects)
- Never commit game data: ROMs, savestates, save files, patched builds (`.gitignore` covers `*.gb[c]`, `*.sav`,
  `*.state`, `rom/`, `build/`, `work/`). The original dump is verified by SHA-1 (`rom.sha1`).
- Document as you go: reverse-engineering findings in `docs/re/`, progress and open issues in `docs/status.md`.
  Update `docs/status.md` at the end of every session.
- Translations live in `script/*.json` (Japanese kept next to the English for review). Edit those, not the ROM.
- Commit messages: what changed and why; one topic per commit.

## Wizardry Empire quick reference
Run from `wizardry-empire/`:
- Setup emulator: `sh tools/setup_emu.sh` (builds gbemu-cli, a headless SameBoy with a JSON-lines API, into
  `tools/gbemu-cli`; Python client in `tools/gbemu-cli/cli/py/gbemu.py`).
- ROM: copy your dump to `rom/wizardry_empire_j.gbc`.
- Build: `python3 tools/build.py` -> `build/wizardry_empire_en.gbc` + `.ips`. The build fails loudly when a
  translated line is wider than its box.
- Tests: `python3 -m pytest -q tests`.
- Play/screenshot: `python3 tools/emu.py --out work/qa/x --seq "boot,right*3,a" [--state S] [--save S]`
  (exit 2 = hang, with PC/backtrace in `log.txt`).
- Batches: `python3 tools/batches.py split msg|rect NAME ... / check / pairs / merge` (`check` includes the lint).
- Lint: `python3 tools/lint.py` (glossary names, Yes/No kept, quotes, duplicates, spacing); the build refuses lint
  errors (`NO_LINT=1` to skip while debugging).
- Screen tour: `python3 tools/tour.py [--jp] [route ...]` (routes in `tools/routes/tour.txt`) ->
  `work/qa/tour_en|tour_jp/<route>/sheet.png`; run it after every build and give the sheets to `visual-qa`.
- Disassemble: `python3 tools/gbdis.py BANK ADDR [N]`. Assembler: `tools/asm.py` (rgbds-like syntax, see its docstring).
- Census tools (find text in the original ROM): `tools/census_rects.py`, `tools/chain_rects.py`,
  `tools/census_msgs.py`, `tools/census_inline.py`.
- Read `docs/re/text.md` (text engines, control codes) and `docs/re/vwf.md` (VWF design) before touching `asm/`.

## Subagents
Defined in `.claude/agents/`; each is a thin wrapper around a brief in the project's `docs/`. Dispatch these types,
not general-purpose agents, and give each one exact paths.
| Agent | Brief | Writes | Typical dispatch |
|---|---|---|---|
| `translator` | `wizardry-empire/docs/translator-brief.md` | `work/tl/<batch>.json` only | after `tools/batches.py split ...`; then `merge` |
| `reviewer` | `wizardry-empire/docs/reviewer-brief.md` | nothing (report) | after `tools/batches.py pairs <batch>` |
| `playtester` | `wizardry-empire/docs/playtester-brief.md` | `work/play/<session>/` | a goal ("form a party, win a battle"), after a build |
| `visual-qa` | `wizardry-empire/docs/visual-qa-brief.md` | its verdict file | a list of `tools/emu.py` sheets (e.g. the tour) |
| `tracer` | `wizardry-empire/docs/tracer-brief.md` | `work/re/<topic>.md` | one RE question ("which routine prints the status values?") |
| `triage` | `wizardry-empire/docs/triage-brief.md` | `work/triage/<case>/` | one hang/crash report with state + inputs |
| `editor` | `wizardry-empire/docs/editor-brief.md` | nothing (report) | whole-script English pass, late in the project |
Binding terms: `wizardry-empire/glossary.md`.

## Text formats (Wizardry Empire)
| File | What | Notes |
|---|---|---|
| `script/rects.json` | fixed boxes `[w][h][tiles]` | `^` center, `>` right, `@N:` cell column N, `{x:N}` pixel x; `fixed: true` = 8 px ASCII in place |
| `script/messages.json` | typewriter messages | `\n` = row; `{col:N}` cursor column; `{F8 ..}`/`{F3 ..}` inserts copied from the Japanese |
| `script/inline.json` | text written by code | replaced by `rst $38` calls; `hl` moves the destination |
| `script/items.json`, `monsters.json`, `templates.json` | name fields in data records | in place: 17 / 12 / 7 chars max |
