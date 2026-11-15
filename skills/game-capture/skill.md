---
skill: game-capture
project: gamedb
summary: Play a scouted game from its playbook and capture the database screenshot set (gameplay, systems, screens).
access: write (gamedb/work/, gamedb/games/<slug>/ checkpoints.txt, shots.txt, playbook.md, game.json)
updated: 2026-11-15
---

# Game capture - play and photograph a game for the database

> **Before you start:** paths are relative to `gamedb/`. Read `docs/emulator.md`, `docs/capture-guide.md`, the
> game's `games/<slug>/playbook.md` (all of it: controls, strategy, shortcuts) and the open entries in this
> skill's `feedback.md`. The playbook exists so you do not rediscover the game: use its macros, checkpoints and
> RAM before experimenting.

You play the game toward the playbook's shot plan and capture each target with `play.py snap`, so every shot
carries the route that reproduces it. You extend the playbook with everything you learn. You do not judge or
edit anything outside the game's folder.

## Inputs (from the dispatch)
- Game slug, set name (default `main`), the targets (default: the whole playbook Shot plan), a time budget.

## Steps
1. `python3 tools/play.py start SLUG --name SLUG` (start from the latest useful checkpoint: `--route @name`).
   Use `--name SLUG` on every command so parallel captures do not collide.
2. Work through the plan in game order. For each target: reach it (play, or the playbook's shortcut), make the
   screen good (`docs/capture-guide.md` quality rules), then
   `play.py --name SLUG snap ID CATEGORY "caption" --set SET`. Look at the native PNG it wrote.
3. `checkpoint` at every milestone (new area, before a boss, a menu reached), with a description.
4. Stuck for more than ~10 steps: re-read the playbook strategy and shortcuts, `undo`/`goto`, look up the
   specific problem (a FAQ section) if your tools allow, or poke past it (say so in the report). Do not grind.
5. Add opportunistic shots of anything distinctive the plan missed (category `extra` or the right one).
6. Finish: `python3 tools/shoot.py SLUG SET --verify` (every shot must reproduce; re-snap or fix the route of a
   MISMATCH), then look at `work/shots/SLUG/SET/sheet.png` as a whole: variety, duplicates, broken frames.
   Then `python3 tools/shoot.py SLUG SET --publish` -> `games/SLUG/shots/SET/`.
7. **Update the playbook** (the next agent's head start): verified controls, new macros/checkpoints and what
   they are, strategy that worked, RAM found, timing quirks, dead ends. Copy the finished shot lines into
   `games/SLUG/shots.txt` so the plan is replayable. Tick the Shot plan.

## Guardrails
- Write only `work/` and `games/SLUG/` (playbook.md, game.json macros/ram/press, checkpoints.txt, shots.txt,
  shots/SET/ via --publish). No commits; the coordinator reviews and commits.
- Never commit ROMs, states or saves (`work/` is ignored; `--publish` copies only PNGs and the catalogue).
- A shot whose route contains a poke that shows on screen gets a caption that says so; prefer pokes that do not
  show (stage number, position) over visible ones (lives 99).
- Stop at the time budget with what you have: a verified partial set beats an unverified full one.

## Report (your final message)
- Set path, shot count by category, `--verify` result (n/n reproduce), published path.
- Table: id | category | caption | notes (not settled, poke used, retake wanted).
- Plan targets not captured and why (unreachable in budget, needs a password, ...).
- Playbook changes (sections touched, new checkpoints/macros/RAM).

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
