---
skill: game-capture
project: gamedb
summary: Play a scouted game from its playbook and capture the database screenshot set (gameplay, systems, screens).
access: write (gamedb/work/, gamedb/games/<slug>/ checkpoints.txt, shots.txt, playbook.md, game.json)
updated: 2026-11-15 (in-between commits)
---

# Game capture - play and photograph a game for the database

> **Before you start:** paths are relative to `gamedb/`. Read `docs/emulator.md`, `docs/capture-guide.md`, the
> game's `games/<slug>/playbook.md` (all of it: controls, strategy, shortcuts) and the open entries in this
> skill's `feedback.md`. The playbook exists so you do not rediscover the game: use its macros, checkpoints and
> RAM before experimenting.

Owner's rules (2026-11-15): cataloguing, not a fair playthrough. Skip, cheat, hack RAM, patch the ROM, load
downloaded saves whenever that is faster than playing (`docs/emulator.md`, "Cataloguing, not playing fair").
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
   (`docs/emulator.md`, "Saves for the owner").
   **In-between commit at every major milestone** (owner's rule 2026-11-15; e.g. starter chosen, each
   badge/world, late game reached, end): save in the game + `export`, `shoot.py SLUG SET --verify` (fix
   mismatches first), `shoot.py SLUG SET --publish`, then commit and push only the game folder:
   ```sh
   git add gamedb/games/SLUG
   git commit -m "gamedb: SLUG capture - <milestone> (<n> shots)"   # + the attribution lines from the dispatch
   git pull --rebase origin master && git push origin master        # retry up to 4 times on a network error
   ```
   Never `git add` anything outside `gamedb/games/SLUG/`, never force-push, never commit `work/` or `rom/`.
   A failing rebase (someone changed the same files): stop committing, report it.
   Before snapping screens that show RAM-recipe values (summary, EXP, trainer card, Pokédex counts), check them
   on screen against the game's own rules (EXP inside the level's range, stats plausible for the level) and fix
   the recipe first.
4. Stuck for more than ~10 steps: re-read the playbook strategy and shortcuts, `undo`/`goto`, look up the
   specific problem (a FAQ section, a code list), or poke/code past it. Never grind.
5. **Document the game as you play** in `games/SLUG/design/` (notation in its README): every rule, number and
   system you observe (prices, damage, timers, unlock conditions, enemy behaviour, menus and what they do),
   tagged (verified) with the shot id or checkpoint that shows it, or (RAM) when measured through memory;
   quirks and likely bugs in `design/findings.md`. Measure instead of guessing: e.g. note HP before and after a
   hit over several hits. Write as you go (the next agent starts from it), not at the end.
   Action sequences (`docs/capture-guide.md`, "Action sequences and clips"): a `seq-<action>` set per action, a
   snap per step and `play.py record` clips for the motion, published like any set.
6. Add opportunistic shots of anything distinctive the plan missed (category `extra` or the right one).
7. Finish: `python3 tools/shoot.py SLUG SET --verify` (every shot must reproduce; re-snap or fix the route of a
   MISMATCH), then look at `work/shots/SLUG/SET/sheet.png` as a whole: variety, duplicates, broken frames.
   Then `python3 tools/shoot.py SLUG SET --publish` -> `games/SLUG/shots/SET/`.
8. **Update the playbook** (the next agent's head start): verified controls, new macros/checkpoints and what
   they are, strategy that worked, RAM found, timing quirks, dead ends. Copy the finished shot lines into
   `games/SLUG/shots.txt` so the plan is replayable. Tick the Shot plan.

## Guardrails
- Write only `work/`, `rom/saves/SLUG/`, `rom/patches/SLUG/` and `games/SLUG/` (playbook.md, design/, saves/,
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
- Friction: <what slowed you down or was unclear in this skill, the tools or docs/emulator.md>
- Proposed rule change: <a concrete change to skill.md or docs/emulator.md, or "none">
```
