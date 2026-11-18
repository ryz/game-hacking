---
skill: game-capture
project: all games (shared tools at the repo root)
summary: Play a scouted game from its playbook and capture the database screenshot set (gameplay, systems, screens).
access: write (work/, games/<platform>/<slug>/ checkpoints.txt, shots.txt, playbook.md, game.json)
updated: 2026-11-18 (breadth rule; two lenses: systems.md and interface.md)
---

# Game capture - play and photograph a game for the database

> **Before you start:** paths are relative to the repo root. Read `docs/emulator/README.md` and the file for the game's platform (`docs/emulator/gb.md`, `nes.md`, `snes.md`, `dos.md` or `apple2.md`), `docs/capture-guide.md`, the
> game's `games/<platform>/<slug>/playbook.md` (all of it: controls, strategy, shortcuts) and the open entries in this
> skill's `feedback.md`. The playbook exists so you do not rediscover the game: use its macros, checkpoints and
> RAM before experimenting.

Owner's rules (2026-11-15): cataloguing, not a fair playthrough. Skip, cheat, hack RAM, patch the ROM, load
downloaded saves whenever that is faster than playing (`docs/emulator/README.md`, "Cataloguing, not playing fair").
Anything set by cheating looks realistic (8973 gold, not 9999; varied, consistent with progress). Main character
name: **ryz** (further party members: condi, ebo, cubi, deddo, mnz).

You play the game toward the playbook's shot plan and capture each target with `play.py snap`, so every shot
carries the route that reproduces it. You extend the playbook with everything you learn. You do not judge or
edit anything outside the game's folder.

## Inputs (from the dispatch)
- Game slug, set name (default `main`), the targets (default: the whole playbook Shot plan), a time budget.

## Steps
1. `python3 tools/play.py start SLUG --name SLUG` (start from the latest useful checkpoint: `--route @name`).
   Use `--name SLUG` on every command so parallel captures do not collide.
2. Work through the plan in game order. For each target: reach it by the fastest route the playbook offers
   (save, code, poke, debug menu; playing last), make the
   screen good (`docs/capture-guide.md` quality rules), then
   `play.py --name SLUG snap ID CATEGORY "caption" --set SET`. Look at the native PNG it wrote.
3. `checkpoint` at every milestone (new area, before a boss, a menu reached), with a description. At the bigger
   milestones also leave a save for the owner: save in the game, then `play.py export NN_place "contents"`
   (`docs/emulator/README.md`, "Saves for the owner").
   **In-between commit at every major milestone** (owner's rule 2026-11-15; e.g. starter chosen, each
   badge/world, late game reached, end): save in the game + `export`, `shoot.py SLUG SET --verify` (fix
   mismatches first), `shoot.py SLUG SET --publish`, then commit and push only the game folder:
   ```sh
   git add games/PLATFORM/SLUG
   git commit -m "SLUG: capture - <milestone> (<n> shots)"   # + the attribution lines from the dispatch
   git pull --rebase origin BRANCH && git push origin BRANCH        # BRANCH = the branch named in the dispatch;
                                                                    # retry up to 4 times on a network error
   ```
   The coordinator merges the branch into `master` (AGENTS.md, Branch). Never `git add` anything outside `games/PLATFORM/SLUG/`, never force-push, never commit `work/` or `rom/`.
   A failing rebase (someone changed the same files): stop committing, report it.
   Before snapping screens that show RAM-recipe values (summary, EXP, trainer card, Pokédex counts), check them
   on screen against the game's own rules (EXP inside the level's range, stats plausible for the level) and fix
   the recipe first.
4. Stuck for more than ~10 steps: re-read the playbook strategy and shortcuts, `undo`/`goto`, look up the
   specific problem (a FAQ section, a code list), or poke/code past it. Never grind.
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
   Add opportunistic shots of anything else distinctive (category `extra` or the right one).
   **Two lenses** (owner's request 2026-11-18, `docs/capture-guide.md` "Two lenses"): keep
   `design/systems.md` (game design: one row per feature, system, mechanic) and `design/interface.md` (UI/UX:
   one row per screen, menu, prompt, element; conventions; screen flow) up to date while capturing; copy the
   templates from `games/_template/design/` if the game has none. Every shot belongs in at least one of them,
   most in both. Before finishing run `python3 tools/lenses.py SLUG SET` and clear its list (add the row, or
   say in the row why there is no shot).
7. Finish: `python3 tools/shoot.py SLUG SET --verify` (every shot must reproduce; re-snap or fix the route of a
   MISMATCH), then look at the contact sheet `work/shots/PLATFORM/SLUG/SET/<game>_<platform>_<region>_set_sheet.png` as a whole: variety, duplicates, broken frames.
   Then `python3 tools/shoot.py SLUG SET --publish` -> `games/PLATFORM/SLUG/shots/SET/`. The tools name the files
   (`<game>_<platform>_<region>_<category>_<id>.png`, `docs/capture-guide.md` "File names"): pick the category
   with care, it is part of the name; link shots from `design/` by the file name in the set's `index.md`.
8. **Update the playbook** (the next agent's head start): verified controls, new macros/checkpoints and what
   they are, strategy that worked, RAM found, timing quirks, dead ends. Copy the finished shot lines into
   `games/PLATFORM/SLUG/shots.txt` so the plan is replayable. Tick the Shot plan.

## Guardrails
- Write only `work/`, `rom/saves/SLUG/`, `rom/patches/SLUG/` and `games/PLATFORM/SLUG/` (playbook.md, design/, saves/,
  game.json macros/ram/press/rom_variants, checkpoints.txt, shots.txt, shots/SET/ via --publish). Commits:
  only the in-between commits above (game folder only, to master); the coordinator reviews and makes the final
  commit.
- Never commit ROMs, states or saves (`work/` is ignored; `--publish` copies only PNGs and the catalogue).
- Cheated values that show on screen are realistic (below the cap, not round, varied); captions describe the
  screen, they need not mention the cheat.
- Stop at the time budget with what you have: a verified partial set beats an unverified full one.

## Report (your final message)
- Set path, shot count by category, `--verify` result (n/n reproduce), published path.
- In-between commits (hash: milestone).
- Table: id | category | caption | notes (not settled, poke used, retake wanted).
- Plan targets not captured and why (unreachable in budget, needs a password, ...).
- Playbook changes (sections touched, new checkpoints/macros/RAM, saves/codes used).
- Saves exported (name: contents).
- Design reference: documents written or extended, number of claims by tag, findings added.

## Feedback (end of every run)
End your final report with this block; the coordinator files it in `skills/game-capture/feedback.md` and in
`agent-log/YYYY-MM.md`:

```
## Feedback
- Task: <one line>
- Worked: <what went well, worth keeping>
- Friction: <what slowed you down or was unclear in this skill, the tools or docs/emulator/>
- Proposed rule change: <a concrete change to skill.md or docs/emulator/, or "none">
```
