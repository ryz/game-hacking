---
skill: game-capture
project: all games (shared tools at the repo root)
summary: Play a scouted game from its playbook and capture the database screenshot set (gameplay, systems, screens).
access: write (work/, games/<platform>/<slug>/ checkpoints.txt, shots.txt, playbook.md, game.json)
updated: 2026-11-21 (gamestable left to the coordinator; 2026-11-20: routes converted from a captured port; batches with preview.py as the default loop; native pictures; budget in calls; shared cachecheck; start set ids numbered in play order)
---

# Game capture - play and photograph a game for the database

> **Before you start:** paths are relative to the repo root. Read `docs/emulator/README.md` and the file for the game's platform (`docs/emulator/<platform>.md`), `docs/capture-guide.md`, the
> game's `games/<platform>/<slug>/playbook.md` (its "Read first" block, then the sections your targets need; all
> of it when it has no such block) and this skill's `feedback.md` (short: lessons not yet in this file). The
> playbook exists so you do not rediscover the game: use its macros, checkpoints and RAM before experimenting.

Owner's rules (2026-11-15): cataloguing, not a fair playthrough. Skip, cheat, hack RAM, patch the ROM, load
downloaded saves whenever that is faster than playing (`docs/emulator/README.md`, "Cataloguing, not playing fair").
Anything set by cheating looks realistic (8973 gold, not 9999; varied, consistent with progress). Main character
name: **ryz** (further party members: condi, ebo, cubi, deddo, mnz).

You work toward the playbook's shot plan and capture each target with its route (a line in the set's
`shots.txt`, shot by `shoot.py`; or `play.py snap` while exploring), so every shot can be reproduced. You extend the playbook with everything you learn. You do not judge or
edit anything outside the game's folder.

## Inputs (from the dispatch)
- Game slug, set name (default `main`), the targets (default: the whole playbook Shot plan), a budget in tool
  calls (the container has no usable clock; `play.py` prints `call=N`), the branch and the attribution lines
  for commits.

## Steps
1. Delete `work/cache/<platform>/<slug>` before the first command: states left by the scout may not match their
   routes (Ultima I DOS: a preview and a shot disagreed until the cache was cleared, 2026-11-19). Then
   `python3 tools/cachecheck.py SLUG --flat leaves` (background for a long chain): it rebuilds every checkpoint,
   proves the chain reproduces and writes one sheet of all checkpoint frames: look at it instead of visiting
   each checkpoint.
2. Work through the plan in game order, **in batches** (`docs/emulator/README.md`, "Two loops"). Looking at
   pictures is what a capture costs, so one look should cover many routes:
   - Write 10-30 targets as lines `id | category | caption | route` in a plan file under `work/plan/SLUG/`,
     each reached by the fastest route the playbook offers (save, code, poke, debug menu, warp macro; playing last).
   - `python3 tools/preview.py SLUG FILE --set SET`: one sheet at native size (`--text` for text screens,
     `--timeline N:STEP` for message and battle frames, `--crop` for a message line). Fix the lines the sheet
     shows wrong; make the screen good (`docs/capture-guide.md` quality rules).
   - Append the good lines to `work/shots/<platform>/<slug>/SET/shots.txt` in game order and run
     `python3 tools/shoot.py SLUG SET --only id,id,...`. It lists any new shot whose picture the set already has.
   - Explore with `python3 tools/play.py start SLUG --name SLUG [--route @name]` only where the route is not
     known yet (`--name SLUG` on every command so parallel captures do not collide); `snap ID CATEGORY "caption"
     --set SET` there is fine. Turn what you learn into a macro, a checkpoint or plan lines and return to batches.
   Small generators help: a script that writes plan lines for every shop, floor or monster from a decoded table.
   **A port of the game is already captured** (another platform's set): convert its routes with a script
   (position format, warp macro, waits) and preview them in bulk before exploring (Might and Magic I and II
   Apple II, 2026-11-20).
3. `checkpoint` at every milestone (new area, before a boss, a menu reached), with a description. At the bigger
   milestones also leave a save for the owner: save in the game, then `play.py export NN_place "contents"`
   (`docs/emulator/README.md`, "Saves for the owner").
   **In-between commit at every major milestone** (owner's rule 2026-11-15; e.g. starter chosen, each
   badge/world, late game reached, end): save in the game + `export`, `shoot.py SLUG SET --verify` (fix
   mismatches first), `shoot.py SLUG SET --publish-only` (copies what the passing verify just compared;
   `--publish` replays everything again without comparing), then commit and push only the game folder:
   ```sh
   git add games/PLATFORM/SLUG
   git commit -m "SLUG: capture - <milestone> (<n> shots)"   # + the attribution lines from the dispatch
   git push origin BRANCH        # BRANCH = the branch named in the dispatch; retry up to 4 times on a network error
   ```
   A rejected push (the branch has commits you lack): `git fetch origin BRANCH && git merge --no-edit FETCH_HEAD`,
   push again; never rebase, never force-push. A merge conflict: stop committing, report it.
   The coordinator merges the branch into `master` (AGENTS.md, Branch). Never `git add` anything outside
   `games/PLATFORM/SLUG/`, never commit `work/` or `rom/`. The milestones are part of the task, not optional:
   three runs skipped them and committed only at the end.
   Before snapping screens that show RAM-recipe values (summary, EXP, trainer card, Pokédex counts), check them
   on screen against the game's own rules (EXP inside the level's range, stats plausible for the level) and fix
   the recipe first.
4. Stuck for more than ~10 calls: re-read the playbook strategy and shortcuts, `undo`/`goto`, look up the
   specific problem (a FAQ section, a code list), or poke/code past it. Never grind. Code reading is boxed to
   about 20 calls per question; a target not reached by then goes into the report as open.
5. **Document the game as you play** in `games/PLATFORM/SLUG/design/` (notation in its README): every rule, number and
   system you observe (prices, damage, timers, unlock conditions, enemy behaviour, menus and what they do),
   tagged (verified) with the shot id or checkpoint that shows it, or (RAM) when measured through memory;
   quirks and likely bugs in `design/findings.md`. Measure instead of guessing: e.g. note HP before and after a
   hit over several hits. Write as you go (the next agent starts from it), not at the end.
   Action sequences (`docs/capture-guide.md`, "Action sequences and clips"): a `seq-<action>` set per action, a
   snap per step and `play.py record` clips for the motion, published like any set.
6. **Breadth: more rather than fewer** (owner's rule 2026-11-18). The set documents how the game works, so when
   in doubt take the shot and write the mechanic down. Beyond the plan, cover:
   - **Every command and mechanic the game offers**, one shot each showing it at work (its prompt and its
     result): each entry of every command list, menu and prompt the playbook or the manual names, also the
     minor ones (in a party RPG: bash, trade, share, gather, discard, use, rest, protect, bribe, retreat,
     surrender, exchange, block, shoot, cure at a temple, rumours ...). A command not tried is listed in the
     report with the reason.
   - **Battles with interesting enemies**: not only the first group met. Several fights that differ in enemy
     picture, group size or behaviour (special attacks, status effects, spells cast at the party), and the
     strongest or strangest ones reachable.
   - **Different visual environments**: at least one shot of each distinct look the game has (each wall or tile
     set, town, cave, dungeon, outdoors by terrain, castle, special places), not several of the same look.
   - Each of these goes into `design/` too (what the command does, what the enemy did), per step 5.
   - **Standard environment shots** (owner's rule 2026-11-19, `docs/capture-guide.md`): a few plain views per
     kind of place with nothing happening (`env_...`), and the set `start`: the early game in play order to
     the first save, played honestly (capture guide, "Sets"). Its ids are numbered in play order
     (`01_power_on`, `02_title`, ...) and its `shots.txt` lists them in that order; the tools put the number
     in front of the category in the file names (owner's rule 2026-11-20).
   Add opportunistic shots of anything else distinctive (category `extra` or the right one).
   **Three lenses** (owner's request 2026-11-18, `docs/capture-guide.md` "Three lenses"): keep
   `design/systems.md` (game design: one row per feature, system, mechanic), `design/interface.md` (UI/UX:
   one row per screen, menu, prompt, element; conventions; screen flow) and `design/content.md` (a reasonable
   variety of environments, opponents, items, equipment, abilities, people: a sample that spans the range,
   not a full set; the kinds depend on the game) up to date while capturing; copy the templates from
   `games/_template/design/` if the game has none. Every shot belongs in at least one of them, most in two. Before finishing run `python3 tools/lenses.py SLUG SET` and clear its list (add the row, or
   say in the row why there is no shot).
7. Finish: delete `work/cache/<platform>/<slug>`, then `python3 tools/shoot.py SLUG SET --verify` (in the
   background for a big set; a warm cache holds the states your session made, and a state that its route no
   longer produces passes there: Wizardry III DOS, 2026-11-19, 29 shots). Every shot must reproduce: re-snap or
   fix the route of a MISMATCH. It also lists `check:` lines: shots with identical pictures, which `--publish`
   refuses, and captions over 80 characters: retake, drop or shorten. Removing or renaming a shot: `play.py
   unsnap ID --game SLUG` (no session needed), or edit the work `shots.txt` and run `shoot.py SLUG SET --prune`.
   The order of the set is the order of the work `shots.txt`: put the lines in game order.
   Then look at the contact sheet(s) `work/shots/PLATFORM/SLUG/SET/<game>_<platform>_<region>_set_sheet.png`
   as a whole: variety, duplicates, broken frames.
   Then `python3 tools/shoot.py SLUG SET --publish-only` -> `games/PLATFORM/SLUG/shots/SET/` (index, list and
   native pictures; no enlarged copies). The tools name the files
   (`<game>_<platform>_<region>_<category>_<id>.png`, `docs/capture-guide.md` "File names"): pick the category
   with care, it is part of the name; link shots from `design/` by the file name in the set's `index.md`.
8. **Update the playbook** (the next agent's head start): verified controls, new macros/checkpoints and what
   they are, strategy that worked, RAM found, timing quirks, dead ends. Keep its **Read first** block current
   (at most 60 lines at the top: how to start, the macros and checkpoints that matter, the traps that cost
   calls, what is still open); write it if the playbook has none. Tick the Shot plan. Set `game.json` "work"
   (one line: what exists, as the README table shows it) and "open" (what is still missing). Do not run `tools/gamestable.py`: the coordinator does (it writes
   `README.md` and `docs/status.md`).

## Guardrails
- Write only `work/`, `rom/saves/SLUG/`, `rom/patches/SLUG/` and `games/PLATFORM/SLUG/` (playbook.md, design/, saves/,
  game.json macros/ram/press/rom_variants/work/open, checkpoints.txt, shots.txt, shots/SET/ via --publish). Commits:
  only the in-between commits above (game folder only, to the branch named in the dispatch); the coordinator
  reviews and makes the final commit.
- Never commit ROMs, states or saves (`work/` is ignored; `--publish` copies only PNGs and the catalogue).
- Cheated values that show on screen are realistic (below the cap, not round, varied); captions describe the
  screen, they need not mention the cheat.
- Stop at the call budget with what you have: a verified partial set beats an unverified full one. At 80% of
  the budget stop adding targets: verify, publish, commit, write the playbook.
- Pictures are native size; enlarge only when small text cannot be read (`--scale 2`, `--crop`). Do not print
  long tool output into your context: redirect it to a file under `work/` and read the part you need.

## Report (your final message)
- Set path, shot count by category, `--verify` result (n/n reproduce), published path.
- In-between commits (hash: milestone).
- Table: id | category | caption | notes (not settled, poke used, retake wanted).
- Plan targets not captured and why (unreachable in budget, needs a password, ...).
- Playbook changes (sections touched, new checkpoints/macros/RAM, saves/codes used).
- Saves exported (name: contents).
- Design reference: documents written or extended, number of claims by tag, findings added.

## Feedback (end of every run)
End your final report with this block; the coordinator files it in `skills/game-capture/feedback-log.md`
(lessons still open also in `feedback.md`, tool wishes in `docs/backlog.md`) and in `agent-log/YYYY-MM.md`:

```
## Feedback
- Task: <one line>
- Worked: <what went well, worth keeping>
- Friction: <what slowed you down or was unclear in this skill, the tools or docs/emulator/>
- Proposed rule change: <a concrete change to skill.md or docs/emulator/, or "none">
```
