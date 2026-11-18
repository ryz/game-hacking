---
skill: game-capture
---

# Feedback - game-capture

Running log for this skill, newest first. Status: `open`, `logged`, `promoted YYYY-MM-DD`, `superseded`.
Never delete entries.

## Entries

### 2026-11-18 - Deep Dungeon III (Famicom, Japanese) main set
- Task: main set (74/74; commits fb6c8ee c3b8e42 4294138), event squares and towns decoded, ending found, saves.
- Worked: in-process event scanner over all 16 floors in one parallel call (~3 min), tiled sheets readable enough to
  caption; `w.sh` (goto + warp tokens + snap) made each dungeon shot one call; poking status-page bytes in turn found
  level/EX in ~4 calls; warping to area 6 gave the ending.
- Friction: freeze cannot save a character whose death check falls inside one `w60`; leaving a shop overwrote
  position pokes in the same `do`; a town stairs prompt blocked input after arrival (~4 calls); typewriter text
  again needed `do!` sampling. ~205 calls (within budget).
- Proposed rule change: (1) emulator guide: new `do` after a building exit before poking position; (2) shared
  warp-shot helper with a per-game warp template in game.json.
- Corrected: (1) added to the emulator guide; (2) built as macros with arguments in `tools/emu.py` (`WARP:a:b:c`,
  fifth hand-built warp helper) with a test; 6/6 sample re-verified; set folder = index.
- Status: promoted 2026-11-18 ((1), (2)); open: typewriter-text sampling (`snapafter`), now reported four times

### 2026-11-18 - Might and Magic (NES) main set
- Task: main set (93/93; commits 63279a4 5d0785b 3a6af15), maps (legend, terrain, exits), boss and ending, saves.
- Worked: stepping into every event square from each open side (warp, face, Up) found shops, the Soul Maze answer
  and the ending; per-area script table in ~5 disassembly calls gave exits and the ending square; the item-name
  table made the boss a poke (Eye of Goros); reloading the save proved the story state persisted.
- Friction: event-script facing differs from $A2 (~6 calls); typewriter battle text needed `do!` sampling (third
  report); a late snap fixed by unsnap + replay; full verify ~25 min; publish-only left a stale PNG; ~376 calls
  (budget ~250).
- Proposed rule change: (1) shared `tools/eventscan.py` (third hand-written copy); (2) publish removes stale PNGs;
  (3) emulator guide: test all four facings before calling an event gated.
- Corrected: (2) done in `tools/shoot.py` (second report), (3) added to the emulator guide; set folder checked
  (93 = index); 6/6 re-verified. (1) not built yet: hooks differ per game (position, facing, pending map).
- Status: promoted 2026-11-18 ((2), (3)); open ((1) eventscan, `snapafter` for typewriter text: third report;
  budget overrun 376/250)

### 2026-11-18 - Wizardry II (NES) main set
- Task: main set (91/91 verified; commits 9bda454 a3cb2bd 498f4f3 20aa150), special types checked on all floors,
  maps.md, castle/combat/story docs, ending via RAM edits, saves 02-04.
- Worked: in-process scanner (warp next to every special record, step in, log new ASCII strings from 6000-7FFF)
  checked all types in three runs; reading text from cart RAM beat screenshots; `add.py` (shot = another shot's
  route + tokens) + `shoot.py --only` for long battle/ending chains; decoding the type 11/12/13 handlers (~6 calls).
- Friction: first presses after a menu change dropped (checkpoint ended right after a menu); a route recorded
  after `undo` replayed differently; `--publish-only` crashed on hand-deleted PNGs (a commit went through anyway
  because of a pipe to `tail`); poked records vanish from exports unless the game re-saves them; tiling helper
  sometimes dropped the last frame.
- Proposed rule change: (1) emulator guide: `w30` after the last menu action in checkpoints; remove shots only
  with `unsnap`; (2) `play.py` undo route warning/fix; (3) nes.md: veteran saves from a game-saved base; (4)
  shared `tools/textscan.py`.
- Corrected: (1) and (3) added to the docs; published folder checked (91 ids = 91 PNGs); 6/6 sample re-verified.
  (2): the undo code restores state and tokens together; the replay difference is not reproduced yet.
- Status: promoted 2026-11-18 ((1), (3)); open ((2) needs a repro, (4); auto-advancing text and "shot = route +
  N steps" now asked for twice (see Wizardry I): candidate for `play.py snapafter`)

### 2026-11-18 - Wizardry I (NES) main set
- Task: main set (71/71 verified; commits 69d7eaa 5805efa 41939b7), special squares decoded, maps.md, saves 02-03.
- Worked: special-square jump table (~6 disassembly calls) explained squares and floor-entry fixed fights; the
  roster-to-battle copy loop gave record offsets; monster HP poked to 1 for bosses/chests; auto-advancing battle
  text: `do "a,w40"` loops + tiled image, then routes from `play.py route` + N `,a,w40,settle`, `shoot.py --only`.
- Friction: `--name wiz` reused the scout's folder, stale numbered PNGs read for ~10 calls; remembered battle
  cursors shifted orders; poking monster status to dead does not end a fight; no snap for "route + N more steps";
  full verify of 70 needed a background run; ~300 tool calls (budget ~250).
- Proposed rule change: (1) clear stale PNGs on `play.py start`; (2) emulator guide: fixed encounters may be set
  up only on floor entry, warp onto stairs/elevator/chute; (3) `play.py snapafter ID N`.
- Corrected: (1) done in `tools/play.py`; coordinator re-verified 6/6 incl. Werdna and the ending.
- Status: promoted 2026-11-18 ((1)); open ((2) first occurrence, (3))

### 2026-11-18 - Dungeon Magic (NES) main set and floor maps
- Task: main set (41/41 verified; commits 91cae5d 242b035 1e9c2b0 9171d1e), floor maps of every town and dungeon,
  milestone saves.
- Worked: decoding the exit tables (~6 calls) gave exact warps to every floor and the map index; writing the game's
  own transition variables beat position pokes; in-process scripts (warp-scan of all floors, four-facing views,
  door survey, random walk with a "monster in view" detector); RAM diff of declined vs accepted apprenticeship.
- Friction: sheet/index.json in snap order, not shots.txt (reordered by hand; second occurrence); freeze inside
  one `wN` again; the scout's `maps.py` bank formula was wrong; auto-advancing text needed frame sweeps; casting
  controls by experiment.
- Proposed rule change: (1) publish in shots.txt order; (2) emulator guide: decode exit/warp tables early, warp via
  the game's transition variables; (3) `play.py snap` warns on `freeze:` before a long single `w`.
- Corrected: (1) done in `tools/shoot.py` (every snap, reindex, publish), (2) added to `docs/emulator/README.md`;
  6/6 sample re-verified; 228 calls; all four milestone commits made.
- Status: promoted 2026-11-18 ((1), (2)); open ((3); freeze-in-long-wait now reported by three runs: consider
  making freezes per-frame for new routes only)

### 2026-11-18 - Megami Tensei II (Famicom) main set
- Task: capture the main set (36 shots, 36/36 verified; commits fa9a47d e2d1b8b), save 01_computer_room, design.
- Worked: throwaway in-process scripts on `tools/emu.py` (breadth-first explorer over savestates, 16x16 event-scan
  sheet for first-person mazes, frame sweep for CHAT outcomes); cheat addresses from web-search summaries when
  TCRF would not load (no-encounter byte); losing on purpose inside the game-within-the-game moved the story on.
- Friction: ~60 calls of 6502 RE on the Devil Buster ending without result (no shared disassembler); HP freeze
  did not stop a wipe inside `w10*25`; savestates refuse `rom:` variants; a script wrote into the repo root once;
  published order is snap order, not game order.
- Proposed rule change: (1) emulator guide: on a story gate try losing/quitting, time-box ROM RE to ~20 calls;
  (2) shared `tools/explore.py` (BFS + event scan) and `tools/dis6502.py`; (3) publish in shots.txt order.
- Corrected: coordinator re-verified 6/6 from an empty cache and checked the "untranslated text" finding against
  the unheadered patch layout (layout right, patch gap). Milestones (a)(b) committed; (c) not reached. 231 calls.
- Status: open ((1)-(3): first occurrence each; the RAM-warp scan of Megami Tensei is the same idea as (2))

### 2026-11-18 - Megami Tensei (Famicom) main set
- Task: capture the `main` set: sage password, negotiation/summon/fusion, shop/healer/status, Minotaur (41/41
  verified; commits 23a7460 b29aa51 e88f35c).
- Worked: a scanner that warps the party in RAM to each square and steps in found every NPC/service on 8F in ~5
  min per facing (hand exploration failed for ~25 calls); poking value ranges at a negotiation prompt found the
  money bytes; `shoot.py --verify --only` made milestone checks cheap.
- Friction: `freeze:` only re-applied between tokens, a long `wN` let HP reach 0 (two game overs); `play.py do`
  ends with a `settle`, so RNG outcomes differed between session and `emu.py` replay; `undo` one level deep; a
  full verify of ~40 shots exceeds the 120 s Bash timeout; position bytes found only via view-relative copies.
- Proposed rule change: emulator guide: freeze timing and `w10*N`; "`do` ends with a settle; for timing-decided
  outcomes keep the sequence in one `do`"; first-person dungeons: find position, then RAM-warp scan.
- Corrected: freeze timing and the RAM-warp scan added to `docs/emulator/README.md` (code unchanged: per-frame
  freezes would change existing verified replays). Milestone commits made as asked (dispatch listed them
  explicitly). Budget 289 tool calls against ~250. 6/6 sample re-verified by the coordinator.
- Status: promoted 2026-11-18 (freeze note, RAM-warp scan); open (`do` settle note, deeper undo, long verify
  timeout)

### 2026-11-17 - Shin Megami Tensei main set, run 2
- Task: extend the Shin Megami Tensei main set past run 1's apartment blocker; battles, negotiation, game over,
  automap (56/56 verified, one commit bd1607c).
- Worked: listing RAM bytes that took a distinct value in each of three buildings found the map id; the door
  table in the ROM explained the entrance; decoding the event text in the ROM showed the sleep script has a
  condition; testing one bit at a time with emu.py found the flag in a few runs; a checkpoint before every
  negotiation choice made branch exploration cheap.
- Friction: watches print decimal while the playbook uses hex coordinates (the cause of run 1's wrong square); a
  brute-force script comparing whole screens gave false positives from animation timing; a full `--verify`
  takes about 10 minutes and blocks snapping; the end-of-task wait loop overflowed the output (own mistake);
  one commit only, despite the dispatch asking for milestone commits; about 325 tool calls against a budget of
  about 250.
- Proposed rule change: (1) `"fmt": "hex"` for RAM watches; (2) emulator guide: decode the script next to a
  stuck event and test nearby flag bits one at a time; (3) mention `shoot.py --verify --only ID,...` in the skill
  for shots added during a run.
- Corrected: (1) added to `tools/play.py`; (2) added to `docs/emulator/README.md`; `automap` (snapped during a
  verify) verified by the coordinator, 4/4 sample incl. it.
- Status: promoted 2026-11-17 ((1), (2)); open ((3) skill wording; milestone commits asked for twice and
  skipped twice: next time state the milestones explicitly in the dispatch)

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
