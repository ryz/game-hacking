---
skill: game-capture
---

# Feedback - game-capture

Running log for this skill, newest first. Status: `open`, `logged`, `promoted YYYY-MM-DD`, `superseded`.
Never delete entries.

## Entries

### 2026-11-17 - Shin Megami Tensei (Super Famicom, English patches; first SNES game) main set, run 1
- Task: capture, verify, publish and commit the early-game main set of Shin Megami Tensei (first SNES game);
  34 shots, priorities 1-4 plus the full moon, story blocked at re-entering the apartment.
- Worked: RAM dumps before and after single steps (`work/capture/ramdiff.py`) found position where `play.py
  find` did not; poking the map tile at an exit prompt gives a correctly drawn warp; watches for x/y/facing made
  lost inputs visible at once; a depth-first explorer found every shop and NPC of the arcade in one call;
  committing at three milestones.
- Friction: `find` narrowed to nothing when one of the test steps silently hit a wall; lost inputs after doors
  and scenes broke two "clean" routes and produced wrongly captioned snaps caught only by looking; no command to
  delete or recaption a shot; the `pow,sav:` route problem; the empty `.sav` export; contact-sheet labels are
  hard to match to images when a 512x448 frame is in the row.
- Proposed rule change: (1) record or accept `sav:`/`rom:` after `pow`. (2) `play.py export` refuses an empty
  battery. (3) `play.py unsnap ID` and `recaption`. (4) emulator guide RAM section: if `find` runs dry, dump RAM
  before and after one confirmed step and diff. (5) skill.md: look at the snapped PNG, not the last play frame.
- Corrected: (1) `emu.prefix()` skips `pow`; (2) export refuses all-00/FF battery RAM; (3) `play.py unsnap` and
  `recaption` added (recaption was also asked for in the Dragon Quest entry); (4) added to
  `docs/emulator/README.md`. All with tests. Coordinator reran the full verify.
- Status: promoted 2026-11-17 (tools); open ((5) skill wording, contact-sheet labels with mixed frame sizes,
  session clock from the Dragon Quest entry)

### 2026-11-17 - Dragon Quest (Famicom, English patch; first NES game) main set
- Task: capture, verify, publish and commit the Dragon Quest (Famicom) main set, first NES game, title to credits.
- Worked: checkpoint at every menu or battle the moment it appeared (cheap retakes); a shell loop on the `ehp`
  watch to find random battles; poking position or map number during a map transition (correctly drawn warps,
  skipped the seven-floor castle); reading the ROM bytes around `LDA #enemy` to find the fixed-fight triggers;
  full `--verify` in the background while exploring.
- Friction: the position warp leaves a stale background (three retakes before the transition trick); `do!` can
  capture mid-scroll; `ls 0*.png` stopped matching once play screenshots passed 099; snapping while a
  `--verify` or `--publish` is running is unsafe; caption edits need a re-shoot to reach `index.md`; no usable
  wall clock in the container (budget could not be measured); only one in-between commit, at the end.
- Proposed rule change: (1) emulator.md RAM section: a position poke does not redraw the map; poke during a map
  transition or use stairs. (2) `play.py recaption ID "caption"`. (3) `play.py status` prints elapsed session
  time so agents can keep a time budget.
- Corrected: (1) added to `gamedb/docs/emulator.md`. Coordinator reran the full verify from an empty cache.
- Status: open ((3) session clock); (2) recaption command added 2026-11-17

### 2026-11-15 - Pokémon Blue sequences: seq-fishing, seq-fly
- Task: publish seq-fishing (15 steps, 3 clips, incl. the no-bite branch) and seq-fly (9 steps, 2 clips),
  design notes, commit 12fdafe.
- Worked: record fits the do/snap loop, undo after record works; checkpoints just before each deciding input
  made retakes cheap; an emu.py w0..w3 loop found the bite frame; --verify handles clips; --publish-only.
- Friction: poster = first frame (transitions start white; 3-4 re-records for usable posters); clip length is
  hard to judge (GIF merges duplicate frames); no `clip` category, unknown categories only warned after the
  fact; hand edits of index.json did not refresh index.md/strip; re-recording a later clip from a checkpoint
  needed a hand-made `wN` for the earlier `rec:` (undocumented).
- Proposed rule change: record --poster N (or first non-blank frame) + a frame strip; reject unknown categories
  up front, clips take the category of what they show; --verify regenerates index.md/strip/steps; capture-guide
  line on posters.
- Corrected: coordinator reran --verify (15/15, 9/9), looked at both strips. Implemented: `rec:N:K:P` poster
  index, `record --poster P` + numbered kept-frame sheet, category check in snap/record, a full passing --verify
  rebuilds index.md/sheet/strip/steps; capture-guide poster and category notes. Re-picked the posters of
  07_cast_clip (102), 09_battle_clip (72), 07_takeoff_clip (42), 08_landing_clip (24), republished.
- Status: promoted 2026-11-15 (all four)

### 2026-11-15 - Pokémon Blue main set, run 2 (50 -> 92 shots)
- Task: extend the main set (gym, learn move/evolution, field moves, locations, endgame, PC), design docs,
  saves, milestone commits.
- Worked: one recipe tuned to a single fight (BROCK) gave five shots (learn move, level-up, badge, evolution,
  gym); lobby-exit warps + a map-script poke (D64C) reached Champion, Hall of Fame and credits in ~10 min;
  background `--verify --only` between milestones; goto + do loops with montages to pick frames.
- Friction: animation frames found with emu.py montages did not appear at the same wN in play.py (Safari rock,
  6 tries); start/party cursors remembered inside checkpoints broke `down*N`; a re-snap identical to the old
  PNG gave no sign (pokecenter_heal retake changed nothing); --publish replays the whole set.
- Proposed rule change: pick `!` frames in play.py, not emu.py; snap reports an unchanged re-snap;
  --publish copies without replay after a passing --verify.
- Corrected: coordinator checked both commits (game folder only), the contact sheet, booted saves 04 and 06
  (values as reported), reran full --verify. Added: snap prints UNCHANGED, `shoot.py --publish-only`,
  emulator.md note on picking animation frames in play.py. Cursor memory stays a playbook note.
- Status: promoted 2026-11-15 (all three, in tools/docs)

### 2026-11-15 - Pokémon Blue main set (first capture)
- Task: capture the Pokémon Blue main set (early game, menus, battles, Elite Four, blackout), design docs,
  saves, milestone commits (rule arrived mid-run).
- Worked: deterministic replays (~75 battle turns land on the same frame); `do!` + sampled `wN` montage to pick
  animation frames; goto + do loops with RAM peeks to drive long battles; `shoot.py --list --only` to bring
  proven scout routes into main.
- Friction: snap right after goto saved a black frame, after undo a stale one (the one MISMATCH); new game.json
  macros needed a session restart; --verify/--publish 4-5 min with no output until the end; single-tile walking
  never triggers wild encounters; the scout's LATE recipe had wrong EXP (growth groups 3/5 swapped, fraction
  >100%).
- Proposed rule change: "after goto/undo, `do settle` before snap" (or render a frame on load); check RAM-recipe
  values on screen (summary/EXP pages) before snapping late-game menus; flush --verify output.
- Corrected: coordinator reran --verify; play.py now refuses snap until a frame ran after goto/undo/start at a
  checkpoint, reloads game.json on every do; shoot.py flushes each line; mkrecipe.py fixed (pret
  data/growth_rates.asm) and committed as games/pokemon-blue/tools/mkrecipe.py; MID regenerated (EXP only).
- Status: promoted 2026-11-15 (stale-frame guard in the tool, recipe check in skill.md)
