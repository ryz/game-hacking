# Agent instructions

This repository (`game-hacking`, formerly `game-translations`) is a game database built by taking games apart:
per game, reproducible screenshot sets, a design reference, a playbook for automated play and, where there is
one, a fan translation with its patch tools and reverse-engineering notes. Overview for people: `README.md`.

## Layout
| Path | What |
|---|---|
| `games/<platform>/<slug>/` | everything about one game: `game.json`, `playbook.md`, `checkpoints.txt`, `shots.txt`, `shots/<set>/`, `design/`, `saves/`, `tools/` (game-specific helpers); optional `translation/` and `tech/` |
| `games/<platform>/` | one folder per platform, named like `game.json` "platform": `gb`, `gbc`, `nes` (NES and Famicom), `snes` (SNES and Super Famicom), `sms` (Master System and Mark III), `md` (Mega Drive and Genesis), `dos`, `apple2`, `amiga`, `c64` (Commodore 64) |
| `games/_template/` | starting files for a new game (used by `tools/intake.py`) |
| `tools/`, `tests/` | shared tooling for all games (emulators, play, capture) and its tests |
| `docs/` | shared tooling docs: `emulator/` (general rules + one file per platform), `capture-guide.md`, `status.md` (snapshot), `backlog.md` (tool wishes), `progress-log.md` (history) |
| `skills/`, `.claude/agents/`, `agent-log/` | agent procedures, their wrappers, the run log |
| `rom/`, `work/` (also inside `games/gbc/wizardry-empire/translation/`) | ROMs, downloads, states, caches, scratch: ignored by git |

Games: the table in `README.md` (what is here) and the one in `docs/status.md` (sets with shot counts, lens
documents, open items). Both are written by `python3 tools/gamestable.py` from each game's `game.json` fields
"edition", "work" and "open": change those, never the tables. 32 games on 9 platforms as of 2026-11-21.

## Rules (all work)
- Never commit game data: ROMs, savestates, save files, patched builds (`.gitignore` covers `*.gb[c]`, `*.nes`, `*.sfc`, `*.smc`,
  Apple II and Amiga disk images, `*.sav`, `*.state`, `rom/`, `build/`, `work/`). Original dumps are verified by SHA-1 (`game.json`, or
  `rom.sha1` for the Wizardry Empire translation). Exceptions (owner's decisions 2026-11-12 and 2026-11-15):
  saves made by a game's own tools or by the capture agents while playing, in `games/<platform>/<slug>/saves/`, each
  documented in its `README.md`. Downloaded saves are never committed.
- Game data lives in the private vault `ryz/game-hacking-r` (owner's rule 2026-11-21): whenever the owner drops a
  ROM, disk image, patch, save or Kickstart, register it (`tools/intake.py`) and then `python3 tools/vault.py push
  GAME [PATH ...]` in the same session, without being asked; exported saves (`rom/saves/`) are pushed too. A fresh
  session restores a game's files with `python3 tools/vault.py pull GAME` (or `--all`). Cloud sessions attach the
  vault first (`add_repo` ryz/game-hacking-r); `vault.py` commits to the vault's `main` directly. Layout: its `README.md`.
- Patches supplied by the owner (IPS, BPS, UPS: translations, bug fixes, restorations) are always used (owner's
  rule 2026-11-17): register the ROM with them applied, in the order given (`tools/intake.py ROM --patch P ...`),
  so screenshots, playbook and design reference describe the patched game. Header-only differences are handled
  by `tools/patch.py` (layouts, iNES 1.0 vs NES 2.0); a patch that still does not apply (wrong revision) is
  reported to the owner, never skipped silently. Patches and dumps
  stay uncommitted; `game.json` "source" records their names, SHA-1s and layouts.
- Screenshots may be committed: sets go to `games/<platform>/<slug>/shots/<set>/` (`shoot.py ... --publish`).
  Native pictures only (owner's rule 2026-11-20): no 3x copies by default, in sets or while playing; enlarged
  copies on demand (`tools/x3.py`, `play.py shot --scale N`), not committed.
- Document as you go. Shared tooling: `docs/status.md` (current snapshot, short; the game table in it is
  generated) and `docs/progress-log.md` (history, append-only, newest first); tool wishes in `docs/backlog.md`.
  What a game has and lacks is written once, in its `game.json` ("work", "open"). Wizardry Empire translation: `games/gbc/wizardry-empire/translation/docs/status.md`
  and `progress-log.md`, reverse-engineering findings in its `docs/re/`; log every test ROM sent (commit hash).
  Update both files of the area you worked in at the end of every session.
- History is not rewritten: progress logs, feedback logs and `agent-log/` keep the paths that were true when
  they were written. Before 2026-11-17 the layout was `wizardry-empire/` and `gamedb/` at the root (mapping in
  `docs/progress-log.md`, entry "repository restructured"); from 2026-11-17 to 2026-11-18 games were
  `games/<slug>/` without the platform folder (entry "games grouped by platform").
- Agent work follows the skills in `skills/` (index: `skills/skill-index.md`) and its feedback loop (below).
- Translations live in script files (Japanese kept next to the English for review). Edit those, not the ROM.
- Commit messages: what changed and why; one topic per commit.
- Branch: work on the branch the session was given (owner's rule 2026-11-18; before that, only `master`). Before a
  session ends, make sure its work is merged into `master` and pushed, and say so in the report; if the merge or
  push is not possible, tell the owner what is left on which branch.

## Shared tooling quick reference
Run from the repo root (how to drive any game: `docs/emulator/README.md`, then the platform file
`docs/emulator/<platform>.md`; what to capture: `docs/capture-guide.md`):
- Setup: `sh tools/setup_emu.sh [gb|nes|snes|sms|md|dos|apple2|amiga|c64]` builds one emulator (9-90 s; backends, what a
  game file is and what is not supported per platform: `docs/status.md`, "Platforms"). Amiga Kickstart ROMs go
  into `rom/kickstart/` (never committed).
- Vault (private game data): `python3 tools/vault.py push GAME [PATH ...]`, `pull GAME|--all`, `list`.
- Register a ROM: `python3 tools/intake.py ROM [--slug NAME] [--region jp|na|eu] [--patch PATCH[:headered|unheadered] ...]` -> `games/<platform>/<slug>/` +
  `rom/<slug>.*`; apply/rebuild patches by hand: `python3 tools/patch.py SRC OUT PATCH[:layout] ...`; 6502 code:
  `python3 tools/dis6502.py SLUG BANK ADDR [N] [--bank-kib 8]` (NES) or `SLUG --route @cp ADDR [N]` (live memory, Apple II); 68000 code: `python3 tools/dis68k.py SLUG ADDR [N]`,
  `--xref ADDR` (who reads a variable).
- SLUG is the game's folder name; write `PLATFORM/SLUG` (`dos/might-and-magic`) when two platforms have the
  same slug. Work files follow the same shape: `work/shots/<platform>/<slug>/`, `work/cache/...`, `work/intake/...`.
- Explore: `python3 tools/play.py start SLUG`, `do "tokens"`, `undo`, `snap ID CATEGORY "caption"`,
  `checkpoint NAME "desc"`, `goto NAME`, `find "new == old - 1"`, `dump A` / `diff A [B]`, `sample "TOKS" N`,
  `text` (Apple II hi-res games: a font taught with `tools/hirestext.py`), `stop`. Pictures are native size; every status line carries `call=N` (budgets are counted in calls).
- Capture in batches (the default once a route is known, `docs/emulator/README.md` "Two loops"):
  `python3 tools/preview.py SLUG PLANFILE [--set SET] [--timeline N:STEP] [--text]` shows many candidate routes
  on one sheet exactly as they will be shot; then the lines go into the set's `shots.txt` and
  `python3 tools/shoot.py SLUG SET --only id,id`.
- Sets: `python3 tools/shoot.py SLUG SET [--verify|--publish|--publish-only] [--jobs N]` (four processes by
  default; a set's order is its own `shots.txt`; `--verify --published` checks the committed set itself). Checkpoints: `python3 tools/cachecheck.py SLUG` (cache equals
  replay from power-on; sheet of all checkpoints). Tests: `python3 -m pytest -q tests`.
- Shot file names (owner's rule 2026-11-18, `docs/capture-guide.md` "File names"):
  `<game>_<platform>_<region>_<area>_<id>[.<set>].png` = `game.json` slug, platform, region (`jp`/`na`/`eu`: the
  release of the dump, a translated Japanese ROM is `jp`), the shot's category, its id; `.<set>` for sets other
  than `main` and `seq-*`. The slug is the short game name without the platform (`wizardry`, not `wizardry-nes`).
  The tools build the names; link a shot by the file name in the set's `index.md`.
- Standard sets and shots (owner's rules 2026-11-19, `docs/capture-guide.md`): every `main` set has a few plain
  environment views with nothing happening (`env_...`); a set `start` shows the early game in play order to the
  first save, played honestly.
- Three lenses per game (owner's request 2026-11-18, `docs/capture-guide.md` "Three lenses"): `design/systems.md`
  (game design: every feature, system, mechanic), `design/interface.md` (UI/UX: every screen, menu, prompt,
  element, conventions, screen flow) and `design/content.md` (a reasonable variety of environments, opponents,
  items, equipment, abilities, people) index the same shots; `python3 tools/lenses.py SLUG [SET]` lists shots
  used by none and rows without a shot.
- Per game: `games/<platform>/<slug>/playbook.md` is read before playing and updated after; checkpoints are routes (cache
  states are not committed). Milestone saves for the owner: save in the game, then `play.py export NAME "desc"`
  -> `games/<platform>/<slug>/saves/` (committed); password games record passwords in the playbook instead. Capture agents
  commit + push their game folder at every major milestone.

## Wizardry Empire
Its quick reference (build, check, play, tour, shots, maze tools, disassembler, census) and its text formats are
in `games/gbc/wizardry-empire/AGENTS.md`: read that file before any work in `games/gbc/wizardry-empire/`
(Claude Code loads it through `games/gbc/wizardry-empire/CLAUDE.md` when it works in that folder; subagents
are told to read it by their wrapper). It uses its own tools in `translation/tools/`, with the same file-name scheme.

## Skills and subagents
- `skills/skill-index.md` routes every job to a skill; each `skills/<name>/` has `skill.md` (source of truth),
  `feedback.md` (open lessons, short: what agents read) and `feedback-log.md` (every run's feedback in full).
  Templates: `skills/_templates/`.
- Subagents are thin wrappers in `.claude/agents/<name>.md` that load `skills/<name>/skill.md`. Dispatch these
  types (translator, reviewer, editor, playtester, visual-qa, photographer, tracer, triage, maintenance, design-writer, game-scout, game-capture), not general-purpose
  agents, with exact paths filled in from `skills/_templates/dispatch.md`. Bug reports: `skills/_templates/bug-report.md`. The main session follows `skills/coordinator/skill.md`.
- Binding terms: `games/gbc/wizardry-empire/translation/glossary.md`.

### Feedback loop
- Every agent ends its report with a `## Feedback` block (Task, Worked, Friction, Proposed rule change).
- The coordinator files it at the top of `skills/<name>/feedback-log.md` (plus `Corrected` and `Status`) and adds a
  line to `agent-log/YYYY-MM.md`: `- YYYY-MM-DD · <agent> · <task> · <paths touched> · <outcome>`.
- Each proposal in it goes to exactly one place: a lesson for agents -> a line in `skills/<name>/feedback.md`
  (open lessons); a tool wish -> a row in `docs/backlog.md` (or its "Asked" count raised); a fact about one
  game -> that game's playbook; a fact about a platform -> `docs/emulator/<platform>.md`.
- Status in the log: `open` (lesson waiting for a second case), `backlog` (tool wish), `logged`, `promoted
  YYYY-MM-DD`, `superseded`. Second occurrence, or the user states it as a rule: a lesson is promoted into
  `skill.md` (bump `updated:`) and its line leaves `feedback.md`; a tool wish is built before the next dispatch
  of that skill or dropped with the reason. Prefer a tool that enforces a rule to a sentence that states it:
  every sentence is read by every agent on every run. Never delete log entries.

### End-of-run checklist (coordinator)
1. Agent output checked (key claims verified) and saved where the skill says, findings in `docs/re/` if RE.
2. Feedback filed for every skill used (log, open lessons, backlog); repeated lessons promoted, repeated tool
   wishes built. (Maintenance skill after big changes.)
3. Agent-log line written.
4. Build + tests + tour pass for code changes; commits pushed.
5. The area's `status.md` and `progress-log.md` updated (shared tooling: `docs/`; Wizardry Empire translation:
   `games/gbc/wizardry-empire/translation/docs/`); for a database game its `game.json` "work"/"open" and
   `python3 tools/gamestable.py`; the user told plainly what changed and what remains open.
