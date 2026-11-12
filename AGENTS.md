# Agent instructions

This repository holds fan-translation projects, one directory per game. Each project is self-contained
(its own `tools/`, `docs/`, `script/`, `tests/`). Current projects:

| Directory | Game | Platform |
|---|---|---|
| `wizardry-empire/` | Wizardry Empire (J) -> English | Game Boy Color |

## Rules (all projects)
- Never commit game data: ROMs, savestates, save files, patched builds (`.gitignore` covers `*.gb[c]`, `*.sav`,
  `*.state`, `rom/`, `build/`, `work/`). The original dump is verified by SHA-1 (`rom.sha1`).
- Screenshots may be committed: reference sets go to `<project>/docs/shots/<set>/` (photographer,
  `tools/shoot.py SET --publish`).
- Document as you go: reverse-engineering findings in `docs/re/`, the current snapshot in `docs/status.md`, the
  history in `docs/progress-log.md` (append-only, newest first). Update both at the end of every session and log
  every test ROM sent (commit hash).
- Agent work follows the skills in `skills/` (index: `skills/skill-index.md`) and its feedback loop (below).
- Translations live in `script/*.json` (Japanese kept next to the English for review). Edit those, not the ROM.
- Commit messages: what changed and why; one topic per commit.

## Wizardry Empire quick reference
Run from `wizardry-empire/`:
- Setup emulator: `sh tools/setup_emu.sh` (builds gbemu-cli, a headless SameBoy with a JSON-lines API, into
  `tools/gbemu-cli`; Python client in `tools/gbemu-cli/cli/py/gbemu.py`).
- ROM: copy your dump of the Japanese **Rev 1** to `rom/wizardry_empire_j.gbc` (`rom.sha1`); v1.0 only as
  `rom/wizardry_empire_j_v10.gbc` for `tools/revmap.py` (old addresses -> Rev 1).
- Build: `python3 tools/build.py` -> `build/wizardry_empire_en.gbc` + `.ips`. The build fails loudly when a
  translated line is wider than its box.
- Tests: `python3 -m pytest -q tests`.
- Play/screenshot: `python3 tools/emu.py --out work/qa/x --seq "boot,right*3,a" [--state S] [--save S]`
  (exit 2 = hang, with PC/backtrace in `log.txt`).
- Batches: `python3 tools/batches.py split msg|rect NAME ... / check / pairs / merge` (`check` includes the lint).
- Lint: `python3 tools/lint.py` (glossary names, Yes/No kept, quotes, duplicates, spacing); the build refuses lint
  errors (`NO_LINT=1` to skip while debugging).
- Standard playtest party (ryz, condi, ebo, cubi, deddo, mnz) + checkpoint states for the current build:
  `python3 tools/party.py --out work/states/party` (renamed/party/camp/maze.state).
- Screen tour: `python3 tools/tour.py [--jp] [route ...]` (routes in `tools/routes/tour.txt`) ->
  `work/qa/tour_en|tour_jp/<route>/sheet.png`; run it after every build and give the sheets to `visual-qa`.
- Reference screenshots: `python3 tools/shoot.py SET [--only ids]` (curated list `tools/routes/shots.txt`) ->
  `work/shots/SET/` native 160x144 + 3x + JP|EN compare PNGs and a catalogue.
- Disassemble: `python3 tools/gbdis.py BANK ADDR [N]`. Assembler: `tools/asm.py` (rgbds-like syntax, see its docstring).
- Census tools (find text in the original ROM): `tools/census_rects.py`, `tools/chain_rects.py`,
  `tools/census_msgs.py`, `tools/census_inline.py`.
- Read `docs/re/text.md` (text engines, control codes) and `docs/re/vwf.md` (VWF design) before touching `asm/`.

## Skills and subagents
- `skills/skill-index.md` routes every job to a skill; each `skills/<name>/` has `skill.md` (source of truth) and
  `feedback.md` (running log). Templates: `skills/_templates/`.
- Subagents are thin wrappers in `.claude/agents/<name>.md` that load `skills/<name>/skill.md`. Dispatch these
  types (translator, reviewer, editor, playtester, visual-qa, photographer, tracer, triage, maintenance), not general-purpose
  agents, with exact paths filled in from `skills/_templates/dispatch.md`. Bug reports: `skills/_templates/bug-report.md`. The main session follows `skills/coordinator/skill.md`.
- Binding terms: `wizardry-empire/glossary.md`.

### Feedback loop
- Every agent ends its report with a `## Feedback` block (Task, Worked, Friction, Proposed rule change).
- The coordinator files it at the top of `skills/<name>/feedback.md` (plus `Corrected` and `Status`) and adds a
  line to `agent-log/YYYY-MM.md`: `- YYYY-MM-DD · <agent> · <task> · <paths touched> · <outcome>`.
- Status: `open` (proposed change waiting), `logged`, `promoted YYYY-MM-DD`, `superseded`. Promote a lesson into
  `skill.md` when it shows up in two entries or the user states it as a rule; bump `updated:`. Never delete entries.

### End-of-run checklist (coordinator)
1. Agent output checked (key claims verified) and saved where the skill says, findings in `docs/re/` if RE.
2. Feedback filed for every skill used; repeated lessons promoted.
   (Maintenance skill after big changes.)
3. Agent-log line written.
4. Build + tests + tour pass for code changes; commits pushed.
5. `docs/status.md` and `docs/progress-log.md` updated; the user told plainly what changed and what remains open.

## Text formats (Wizardry Empire)
| File | What | Notes |
|---|---|---|
| `script/rects.json` | fixed boxes `[w][h][tiles]` | `^` center, `>` right, `@N:` cell column N, `{x:N}` pixel x; `fixed: true` = 8 px ASCII in place |
| `script/messages.json` | typewriter messages | `\n` = row; `{col:N}` cursor column; `{F8 ..}`/`{F3 ..}` inserts copied from the Japanese |
| `script/inline.json` | text written by code | replaced by `rst $38` calls; `hl` moves the destination |
| `script/items.json`, `monsters.json`, `templates.json` | name fields in data records | in place: 16 / 12 / 7 chars max |
