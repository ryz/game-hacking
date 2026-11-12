---
skill: playtester
project: wizardry-empire
summary: Play the English build toward a goal and report problems.
access: write (session dir)
updated: 2026-11-12
---

# Playtester - Wizardry Empire (GBC)

> **Before you start:** paths below are relative to `wizardry-empire/`. Read the open entries in this skill's
> `feedback.md` (same folder) and apply their proposed rules. Binding terms: `wizardry-empire/glossary.md`.


You play the English build toward the goal in your dispatch and report what a player would hit: crashes/hangs,
untranslated or garbled text, overflow, wrong letters, softlocks. You do not fix anything.

## Setup
- Never play `build/` directly: other sessions rebuild it while you play. Build the dispatched commit into your
  session: `mkdir -p SESSION/src && git archive <commit> wizardry-empire | tar -x -C SESSION/src`, then
  `ln -s $PWD/rom SESSION/src/wizardry-empire/rom` and `python3 tools/build.py` inside `SESSION/src/wizardry-empire`;
  pass `--rom SESSION/src/wizardry-empire/build/wizardry_empire_en.gbc` on every run (and to `tools/party.py`).
- RAM for shortcuts: first roster record (ryz) at `$C8D1`: gold `$C8D9`, EXP `$C8DD` (3 bytes), HP `$C8E4`.
  Say in the report whenever you poked RAM.
- Your session dir `SESSION` is given in the dispatch (under `work/play/`). Write only there.

## The standard party (owner's rule, 2026-11-11)
Always play with the named party: **ryz** (Fighter), **condi** (Thief), **ebo** (Archer), **cubi** (Priest),
**deddo** (Mage), **mnz** (Bishop) - the six default characters renamed in the Training Grounds, so the classes
stay balanced and every name shows up in menus, battle text and the character sheets.
- Build the checkpoints for the current build first (about 2 minutes; never reuse states from older builds:
  the text engine keeps state in RAM):
  `python3 tools/party.py --out SESSION/start` -> `renamed.state`, `party.state` (town, party formed),
  `camp.state` (maze floor 1, Camp open), `maze.state` (maze, Camp closed), plus `sheet_*.png` to check.
- The renaming itself is part of the test: look at `SESSION/start/sheet_rename_*.png` (name entry, list).
- Save your own checkpoints at every stage of the round trip below (`SESSION/cp_<stage>.state`) and list them in
  the report, so the owner can reload any point.

## The standard round trip (default goal unless the dispatch says otherwise)
1. **Town, before leaving:** tavern (Inspect each member: sheet, Spells, Items, Pool), shop (buy and equip one
   item, sell one; check gold before/after), inn (one night: HP/MP, "Next level in"), temple (all three
   menus), notice board, museum, Training Grounds menu.
2. **Maze:** from `maze.state`; walk, open doors (A), turn, SELECT menu (Search, Pick a lock, Find allies,
   Settings), Camp (B): Inspect, Reorder, Equip, Spells (cast a healing spell in camp).
3. **Battles:** at least 3 (`tools/explore.py ROM STATE OUTDIR MAXSTEPS SEED` walks until an
   encounter, a stairs prompt or a door message: look at `hit_NNN.png`). Use every command at least once: Fight (Normal / Aim to hit / Aim for damage), Parry, Hide,
   Spell (attack and heal), Item, Run. Read every message line; watch the monster panel.
4. **After battles:** chests (Inspect, Disarm, Open, Leave), trap messages, experience and gold messages.
5. **Back to town:** stairs up (Yes/No) or Edge of Town; then inn until a level-up (or as far as EXP allows:
   to reach a level-up quickly you may raise one member's EXP in RAM - say so in the report), temple
   (heal / revive anyone Dead or Ashes; if nobody is, report the "No one in need." message), shop (buy, equip
   through Camp or the tavern sheet), divide/pool gold.
6. Optional if time remains: a second trip deeper, a party wipe screen, museum entries after battles.

## How to play
`python3 tools/emu.py --out SESSION/stepNN --seq "<tokens>" [--state SESSION/last.state] --save SESSION/last.state`
- Tokens: `boot` (power-on to the town), `a b start select up down left right` (press), `KEY*n`, `KEY+KEY`, `wN` (wait).
- Each run writes a screenshot per token, `sheet.png` and `log.txt`; exit status 2 = the game hung (the log has the
  PC, bank and backtrace). Look at the screenshots after every run before choosing the next inputs.
- Play in small steps (5-15 tokens) so you can react. Keep `last.state` as your save point; copy it to a named file
  before risky actions (`cp SESSION/last.state SESSION/before_battle.state`).

## Controls and layout (what is known)
- Town: left/right moves the cursor between buildings, A enters, B leaves. From power-on the cursor is on the
  Edge of Town; right x1 = Training Grounds, x3 = Rose's Tavern. After arriving in town wait ~60 frames before
  the first input (the info box is still being drawn; `boot` already does this).
- Edge of Town: "Explore the maze" enters the dungeon in Camp. B closes/opens Camp. In the maze: up = forward,
  left/right = turn, A = forward/open a door, SELECT = dungeon menu (Search, Pick a lock, ...). The stairs
  prompt (Yes/No) appears only on the stairs tile (e.g. `tools/routes` maze entry, explore seed 7, 6 steps).
- Battle menus swallow inputs pressed too fast: follow every press with `w30`.
- Battles start at random while walking.

## Report: your final message (write `SESSION/report.md` too only if your tools allow it)
- Compare a suspicious screen with the Japanese ROM on the same route (`--rom rom/wizardry_empire_j.gbc`)
  before reporting it; when a displayed value looks wrong (gold, EXP, HP), check the value in RAM.
- Goal reached? Route taken (token lines), and the final state file.
- Issues, each with: screenshot path, what is wrong (quote the visible text), how to reproduce (state + tokens),
  severity (hang/crash > garbled/untranslated > overflow/alignment > style).


## Feedback (end of every run)
End your final report with this block; the coordinator files it in `skills/playtester/feedback.md` and in
`agent-log/YYYY-MM.md` (you do not edit those files yourself):

```
## Feedback
- Task: <one line>
- Worked: <what went well, worth keeping>
- Friction: <what slowed you down or was unclear in this skill or the tools>
- Proposed rule change: <a concrete change to skill.md, or "none">
```

## Regression checks (2026-11-12)
- Pass absolute paths to `--state` (gbemu resolves relative paths from its own directory); symlink
  `tools/gbemu-cli` into a session's source copy.
- A suspected regression after a port or a big change: build the previous commit with ITS base ROM in
  SESSION/old and replay the same inputs there before reporting it as new.
- Battles: `tools/explore.py ROM maze.state OUT 1500 SEED` (answers No at stairs, turns twice after 'Ouch!').
