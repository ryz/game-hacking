# Agent instructions

This repository (`game-hacking`, formerly `game-translations`) is a game database built by taking games apart:
per game, reproducible screenshot sets, a design reference, a playbook for automated play and, where there is
one, a fan translation with its patch tools and reverse-engineering notes. Overview for people: `README.md`.

## Layout
| Path | What |
|---|---|
| `games/<slug>/` | everything about one game: `game.json`, `playbook.md`, `checkpoints.txt`, `shots.txt`, `shots/<set>/`, `design/`, `saves/`, `tools/` (game-specific helpers); optional `translation/` and `tech/` |
| `games/_template/` | starting files for a new game (used by `tools/intake.py`) |
| `tools/`, `tests/` | shared tooling for all games (emulators, play, capture) and its tests |
| `docs/` | shared tooling docs: `emulator/` (general rules + one file per platform), `capture-guide.md`, `status.md`, `progress-log.md` |
| `skills/`, `.claude/agents/`, `agent-log/` | agent procedures, their wrappers, the run log |
| `rom/`, `work/` (also inside `games/wizardry-empire/translation/`) | ROMs, downloads, states, caches, scratch: ignored by git |

| Game | Platform | Work |
|---|---|---|
| `games/wizardry-empire/` | Game Boy Color | English translation (`translation/`: script, VWF engine, build chain, RE notes), design docs, tech docs, floor maps, reference screenshots |
| `games/pokemon-blue/` | Game Boy | screenshot sets and sequences, design reference, saves |
| `games/dragon-quest/` | Famicom (English translation patch) | screenshot set, design reference, password tools |

## Rules (all work)
- Never commit game data: ROMs, savestates, save files, patched builds (`.gitignore` covers `*.gb[c]`, `*.nes`, `*.sfc`, `*.smc`,
  `*.sav`, `*.state`, `rom/`, `build/`, `work/`). Original dumps are verified by SHA-1 (`game.json`, or
  `rom.sha1` for the Wizardry Empire translation). Exceptions (owner's decisions 2026-11-12 and 2026-11-15):
  saves made by a game's own tools or by the capture agents while playing, in `games/<slug>/saves/`, each
  documented in its `README.md`. Downloaded saves are never committed.
- Patches supplied by the owner (IPS, BPS, UPS: translations, bug fixes, restorations) are always used (owner's
  rule 2026-11-17): register the ROM with them applied, in the order given (`tools/intake.py ROM --patch P ...`),
  so screenshots, playbook and design reference describe the patched game. A patch that does not apply (CRC
  mismatch: wrong revision or header layout) is reported to the owner, never skipped silently. Patches and dumps
  stay uncommitted; `game.json` "source" records their names, SHA-1s and layouts.
- Screenshots may be committed: sets go to `games/<slug>/shots/<set>/` (`shoot.py ... --publish`).
- Document as you go. Shared tooling: `docs/status.md` (current snapshot) and `docs/progress-log.md` (history,
  append-only, newest first). Wizardry Empire translation: `games/wizardry-empire/translation/docs/status.md`
  and `progress-log.md`, reverse-engineering findings in its `docs/re/`; log every test ROM sent (commit hash).
  Update both files of the area you worked in at the end of every session.
- History is not rewritten: progress logs, feedback logs and `agent-log/` keep the paths that were true when
  they were written. Before 2026-11-17 the layout was `wizardry-empire/` and `gamedb/` at the root (mapping in
  `docs/progress-log.md`, entry "repository restructured").
- Agent work follows the skills in `skills/` (index: `skills/skill-index.md`) and its feedback loop (below).
- Translations live in script files (Japanese kept next to the English for review). Edit those, not the ROM.
- Commit messages: what changed and why; one topic per commit.
- Branch: work and push on `master` (owner's rule 2026-11-15); merge any session branch into it.

## Shared tooling quick reference
Run from the repo root (how to drive any game: `docs/emulator/README.md`, then the platform file
`docs/emulator/gb.md`, `nes.md` or `snes.md`; what to capture: `docs/capture-guide.md`):
- Setup: `sh tools/setup_emu.sh [gb|nes|snes]` (gbemu-cli for GB/GBC, Mesen libretro core for NES/Famicom
  `.nes`, Mesen-S libretro core for SNES/Super Famicom `.sfc`/`.smc`).
- Register a ROM: `python3 tools/intake.py ROM [--patch PATCH[:headered|unheadered] ...]` -> `games/<slug>/` +
  `rom/<slug>.*`; apply/rebuild patches by hand: `python3 tools/patch.py SRC OUT PATCH[:layout] ...`.
- Play: `python3 tools/play.py start SLUG`, `do "tokens"`, `undo`, `snap ID CATEGORY "caption"`,
  `checkpoint NAME "desc"`, `goto NAME`, `find "new == old - 1"`, `stop`.
- Sets: `python3 tools/shoot.py SLUG SET [--verify|--publish]`. Tests: `python3 -m pytest -q tests`.
- Per game: `games/<slug>/playbook.md` is read before playing and updated after; checkpoints are routes (cache
  states are not committed). Milestone saves for the owner: save in the game, then `play.py export NAME "desc"`
  -> `games/<slug>/saves/` (committed); password games record passwords in the playbook instead. Capture agents
  commit + push their game folder at every major milestone.
- Wizardry Empire is not registered with these tools yet; it uses its own in `translation/tools/` (below).

## Wizardry Empire quick reference
Run from `games/wizardry-empire/translation/`:
- Setup emulator: `sh tools/setup_emu.sh` (calls the shared setup: gbemu-cli, a headless SameBoy with a JSON-lines
  API, built once into `tools/gbemu-cli` at the repo root; Python client in its `cli/py/gbemu.py`).
- ROM: copy your dump of the Japanese **Rev 1** to `rom/wizardry_empire_j.gbc` (`rom.sha1`); v1.0 only as
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

## Text formats (Wizardry Empire translation, `games/wizardry-empire/translation/`)
| File | What | Notes |
|---|---|---|
| `script/rects.json` | fixed boxes `[w][h][tiles]` | `^` center, `>` right, `@N:` cell column N, `{x:N}` pixel x; `fixed: true` = 8 px ASCII in place |
| `script/messages.json` | typewriter messages | `\n` = row; `{col:N}` cursor column; `{F8 ..}`/`{F3 ..}` inserts copied from the Japanese |
| `script/inline.json` | text written by code | replaced by `rst $38` calls; `hl` moves the destination |
| `script/items.json`, `monsters.json`, `templates.json`, `npcs.json` | name fields in data records | in place: 16 / 12 / 7 / 7 chars max |
| `script/classprompts.json` | Training "Become a <class>?" records | RAM rect header (like titles) |

## Skills and subagents
- `skills/skill-index.md` routes every job to a skill; each `skills/<name>/` has `skill.md` (source of truth) and
  `feedback.md` (running log). Templates: `skills/_templates/`.
- Subagents are thin wrappers in `.claude/agents/<name>.md` that load `skills/<name>/skill.md`. Dispatch these
  types (translator, reviewer, editor, playtester, visual-qa, photographer, tracer, triage, maintenance, design-writer, game-scout, game-capture), not general-purpose
  agents, with exact paths filled in from `skills/_templates/dispatch.md`. Bug reports: `skills/_templates/bug-report.md`. The main session follows `skills/coordinator/skill.md`.
- Binding terms: `games/wizardry-empire/translation/glossary.md`.

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
5. the area's `status.md` and `progress-log.md` updated (shared tooling: `docs/`; Wizardry Empire translation:
   `games/wizardry-empire/translation/docs/`); the user told plainly what changed and what remains open.
