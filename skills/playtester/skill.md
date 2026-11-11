---
skill: playtester
project: wizardry-empire
summary: Play the English build toward a goal and report problems.
access: write (session dir)
updated: 2026-11-11
---

# Playtester - Wizardry Empire (GBC)

> **Before you start:** paths below are relative to `wizardry-empire/`. Read the open entries in this skill's
> `feedback.md` (same folder) and apply their proposed rules. Binding terms: `wizardry-empire/glossary.md`.


You play the English build toward the goal in your dispatch and report what a player would hit: crashes/hangs,
untranslated or garbled text, overflow, wrong letters, softlocks. You do not fix anything.

## Setup
- Build exists at `build/wizardry_empire_en.gbc` (the dispatcher builds it; do not edit the repo).
- Your session dir `SESSION` is given in the dispatch (under `work/play/`). Write only there.

## How to play
`python3 tools/emu.py --out SESSION/stepNN --seq "<tokens>" [--state SESSION/last.state] --save SESSION/last.state`
- Tokens: `boot` (power-on to the town), `a b start select up down left right` (press), `KEY*n`, `KEY+KEY`, `wN` (wait).
- Each run writes a screenshot per token, `sheet.png` and `log.txt`; exit status 2 = the game hung (the log has the
  PC, bank and backtrace). Look at the screenshots after every run before choosing the next inputs.
- Play in small steps (5-15 tokens) so you can react. Keep `last.state` as your save point; copy it to a named file
  before risky actions (`cp SESSION/last.state SESSION/before_battle.state`).

## Controls and layout (what is known)
- Town: left/right moves the cursor between buildings, A enters, B leaves. From power-on the cursor is on the
  Edge of Town; right x3 = Rose's Tavern (Add member to build a party from the 6 default characters).
- Edge of Town: "Explore the maze" enters the dungeon in Camp. B closes/opens Camp. In the maze: up = forward,
  left/right = turn, A = dungeon menu (Search, Pick a lock, ...). Stairs ask Yes/No (up/down + A, or B).
- Battles start at random while walking.

## Report: `SESSION/report.md`, also returned as your final message
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
