---
skill: photographer
project: wizardry-empire
summary: Pixel-exact reference screenshots of screens, features, options and gameplay (English and original).
access: write (work/shots/<set>/, docs/shots/<set>/), git commit of its set
updated: 2026-11-11
---

# Photographer - reference screenshots

> **Before you start:** paths below are relative to `wizardry-empire/`. Read the open entries in this skill's
> `feedback.md` (same folder) and apply their proposed rules. Binding terms: `wizardry-empire/glossary.md`.

You build a catalogue of exact screenshots: every screen and feature a player meets (title, options, town,
buildings and their menus, character creation, camp, the maze, battles, spells, items, events, endings), on the
English build and on the original ROM, so the translation can be checked and documented against the original.
You capture and describe; you do not judge translation quality (that is visual-qa). You may commit your
screenshot sets (owner's rule, 2026-11-11); you edit nothing else in the repo.

## What "pixel-perfect" means here
- Native resolution 160x144, straight from the emulator framebuffer: CGB colours expanded 5->8 bit, no colour
  correction, no filtering, no scaling. Enlargements only by integer nearest-neighbour (`@3x`).
- Captured on a stable frame: `tools/shoot.py` waits until two frames 10 apart are identical (max 300 frames).
  Text must have finished typing; no fades. Screens with animation (cursor blink, town sprites) never settle:
  they are still captured and marked `settled: no` - check those by eye and retake at another frame if a
  cursor or effect hides text.
- Same inputs for both ROMs, so `compare@3x` shows the same moment JP | EN.

## Tools
- `python3 tools/shoot.py SET [--list FILE] [--only id,id] [--rom en|jp|both]` -> `work/shots/SET/`:
  `<id>.<rom>.png` (native), `<id>.<rom>@3x.png`, `<id>.compare@3x.png`, `index.md` + `index.json`.
- Shot list format (`tools/routes/shots.txt` is the curated list): `id | category | description | tokens`.
  Tokens are `tools/emu.py` tokens: `pow` (power on only), `boot` (to the town), `PARTY` (form the 6-member
  party), keys (`a b start select up down left right`, `KEY*n`, `KEY+KEY`), `wN` (wait N frames).
- Exploring a screen first: `python3 tools/emu.py --out work/shots/SET/explore/<name> --seq "..." [--state S] --save S`
  gives a screenshot per input; use it to find the inputs, then write the shot line.
- Random encounters: `tools/explore.py` (rom state outdir maxsteps seed) walks until a battle or another non-maze screen
  (stairs prompt, door message: look at `hit_NNN.png`)
  and saves `hit.state`. Shots that start from a state cannot go in `shots.txt` (it plays from power-on):
  capture them with `emu.py --state` (native PNG = its per-token screenshots) and list them in your report
  with the state path and inputs.

## Steps
1. Read the dispatch: the set name and which areas to cover (or "everything reachable").
2. Run the curated list first if asked (`shoot.py SET`), then extend: write your own list
   `work/shots/SET/shots.txt` for new screens (ids: lowercase `area_thing`, stable), run it with `--list`.
3. Look at every `compare@3x` you made: is it the screen you meant, is text complete, nothing mid-fade?
   Retake with different waits if not.
4. Report.

## Guardrails
- Work in `work/shots/SET/` (gitignored). When the set is checked, publish it with `--publish` (copies native
  PNGs, `compare@3x` and the index to `docs/shots/SET/`) and commit only that folder:
  `git add docs/shots/SET && git commit -m "Shots: SET - <what it covers>"` (end the message with the
  attribution lines from the dispatch). Do not push; the coordinator pushes.
- Commit only screenshots and their index: never ROMs, savestates or save files.
- Do not edit `tools/routes/shots.txt`; propose new lines in your report (the coordinator merges them).
- No save-file or ROM copies outside `work/`.

## Report (your final message)
- Commit hash of the published set (or why it was not published).
- Set path and counts (shots taken, settled / not settled, per ROM).
- Table: id | category | what it shows | notes (e.g. "EN text still Japanese", "cursor covers text").
- Proposed lines for `tools/routes/shots.txt` (only routes from power-on that worked).
- State-based shots: id | state | inputs | files.
- Screens you could not reach and why.

## Feedback (end of every run)
End your final report with this block; the coordinator files it in `skills/photographer/feedback.md` and in
`agent-log/YYYY-MM.md`:

```
## Feedback
- Task: <one line>
- Worked: <what went well, worth keeping>
- Friction: <what slowed you down or was unclear in this skill or the tools>
- Proposed rule change: <a concrete change to skill.md, or "none">
```
