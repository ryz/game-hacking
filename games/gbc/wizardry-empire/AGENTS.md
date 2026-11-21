# Agent instructions - Wizardry Empire

Adds to the repository rules in the root `AGENTS.md` (read those first). Everything here is about
`games/gbc/wizardry-empire/`; the game is not registered with the shared tools at the repo root.

## Quick reference
Run from `games/gbc/wizardry-empire/translation/`:
- Setup emulator: `sh tools/setup_emu.sh` (calls the shared setup: gbemu-cli, a headless SameBoy with a JSON-lines
  API, built once into `tools/gbemu-cli` at the repo root; Python client in its `cli/py/gbemu.py`).
- ROM: copy your dump of the Japanese **Rev 1** to `rom/wizardry_empire_j.gbc` (`rom.sha1`; kept in the private vault:
  `python3 tools/vault.py pull gbc/wizardry-empire` from the repository root); v1.0 only as
  `rom/wizardry_empire_j_v10.gbc` for `tools/revmap.py` (old addresses -> Rev 1).
- Build: `python3 tools/build.py` -> `build/wizardry_empire_en.gbc` + `.ips`. The build fails loudly when a
  translated line is wider than its box.
- Tests: `python3 -m pytest -q tests`.
- **One-command check**: `python3 tools/check.py` (build + tests + parallel tour + pixel diff vs the accepted
  baseline; exit 3 = frames changed, see `work/qa/check/diff.png`; `--accept` after review). ~20 s.
- Play/screenshot: `python3 tools/emu.py --out work/qa/x --seq "boot,right*3,a" [--state S] [--save S]`
  (exit 2 = hang, with PC/backtrace in `log.txt`). Tokens also: `PARTY`, `poke:ADDR=HEX`, `KEY>KEY` (held
  modifier). Routes starting with `boot`/`boot,PARTY` load a cached state per ROM (`work/cache/`, `--no-cache`);
  in scripts: `g, toks, skip = emu.start(rom, seq); emu.play(g, toks[skip:])`.
- Batches: `python3 tools/batches.py split msg|rect NAME ... / check / pairs / merge` (`check` includes the lint).
- Lint: `python3 tools/lint.py` (glossary names, Yes/No kept, quotes, duplicates, spacing); the build refuses lint
  errors (`NO_LINT=1` to skip while debugging).
- **Interactive play**: `python3 tools/play.py start --seq "boot,PARTY"`, then `play.py do "up,a,w30"` / `status` /
  `save NAME` / `load NAME` / `peek` / `poke` / `stop` (one emulator kept running; ~1-2 s per command).
- Standard playtest party (ryz, condi, ebo, cubi, deddo, mnz) + checkpoint states for the current build:
  `python3 tools/party.py --out work/states/party` (renamed/party/camp/maze.state).
- Test save with a powerful party knowing every spell (level 60, special classes): `../saves/test-party-all-spells.sav`,
  rebuilt by `python3 tools/testsave.py --out ../saves/test-party-all-spells.sav` (see `../saves/README.md`).
- Screen tour: `python3 tools/tour.py [--jp] [route ...]` (routes in `tools/routes/tour.txt`) ->
  `work/qa/tour_en|tour_jp/<route>/sheet.png`; run it after every build and give the sheets to `visual-qa`.
- Reference screenshots: `python3 tools/shoot.py SET [--only ids]` (curated list `tools/routes/shots.txt`) ->
  `work/shots/SET/` native 160x144 + 3x + JP|EN compare PNGs and a catalogue (`--publish` copies to `../shots/SET/`).
  Files: `wizardry-empire_gbc_jp_<category>_<id>.<set>.<rom>.png`; categories are the database's
  (`docs/capture-guide.md`); set names are words joined by `-` (`rev1-tour`).
- Maze reach: `tools/maze_goto.py` (poke next to a square + check the event), `tools/maze_route.py` (walking
  tokens), `tools/maze_make_chest.py` (chest after a battle); random walk to a battle: `tools/explore.py ROM STATE
  OUTDIR [MAXSTEPS] [SEED]`. Recipes: `docs/re/reach.md`.
- Reference fan patch (never committed): `python3 tools/bps.py rom/reference_en.bps rom/wizardry_empire_j.gbc
  rom/wizardry_empire_ref.gbc`; `shoot.py --rom ref`. Port audit: `tools/revaudit.py` (after a build).
- Disassemble: `python3 tools/gbdis.py BANK ADDR [N]`. Assembler: `tools/asm.py` (rgbds-like syntax, see its docstring).
- Census tools (find text in the original ROM): `tools/census_rects.py`, `tools/chain_rects.py`,
  `tools/census_msgs.py`, `tools/census_inline.py`.
- Docs map and rules for all documents of the game: `../DOCUMENTS.md`. Game design for designers (rules, formulas,
  data, no addresses): `../design/`; the same systems with addresses and evidence: `../tech/`; reference
  screenshot sets: `../shots/`; patch/text reverse-engineering notes: `docs/re/`. Data tables and floor maps:
  `python3 tools/designtables` (writes into `../design/`).
- Read `docs/re/text.md` (text engines, control codes) and `docs/re/vwf.md` (VWF design) before touching `asm/`.

## Text formats (`games/gbc/wizardry-empire/translation/`)
| File | What | Notes |
|---|---|---|
| `script/rects.json` | fixed boxes `[w][h][tiles]` | `^` center, `>` right, `@N:` cell column N, `{x:N}` pixel x; `fixed: true` = 8 px ASCII in place |
| `script/messages.json` | typewriter messages | `\n` = row; `{col:N}` cursor column; `{F8 ..}`/`{F3 ..}` inserts copied from the Japanese |
| `script/inline.json` | text written by code | replaced by `rst $38` calls; `hl` moves the destination |
| `script/items.json`, `monsters.json`, `templates.json`, `npcs.json` | name fields in data records | in place: 16 / 12 / 7 / 7 chars max |
| `script/classprompts.json` | Training "Become a <class>?" records | RAM rect header (like titles) |

## Documents and skills
- Status and history of the translation: `translation/docs/status.md`, `translation/docs/progress-log.md`;
  reverse-engineering findings in `translation/docs/re/`; log every test ROM sent (commit hash).
- Binding terms: `translation/glossary.md`. Skills (translator, reviewer, editor, playtester, visual-qa,
  photographer, tracer, triage, design-writer): `skills/skill-index.md` at the repo root.
