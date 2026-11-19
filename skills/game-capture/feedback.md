---
skill: game-capture
---

# Feedback - game-capture

Running log for this skill, newest first. Status: `open`, `logged`, `promoted YYYY-MM-DD`, `superseded`.
Never delete entries.

## Entries

### 2026-11-19 - Wizardry III (DOS) set main
- Task: set `main` to the ending, Neutral Crystal made in play, three lenses (228 shots, commit de02d74).
- Worked: testing the dispatch's lead with try.py variants on poked crystals first (minutes), then the whole
  quest as one play.py checkpoint chain; timelines (`w40`/`w20` x N, `--frames N --crop`); survey.py lines
  rebased onto geared checkpoints (~40 message squares in one sheet); reading the item records' special-power
  field pointed at the mechanism (the crystals' power is behind E)quip, not U)se).
- Friction: (1) try.py shows nothing for a route that is only `@checkpoint`; (2) full `--verify` and
  `--publish` ~15 min each, `--publish` replays without comparing; (3) the same guardian orders gave a different
  battle with `w40` steps than with one long wait: frames must come from the exact route; (4) macro waits hide
  prompts (`WARP` contains `y,w600`); (5) message boxes eat the next key. Not captured: Abdul's sale and coffer
  on floor 5, floor 6 dragon room fight, M)ake scenario disk after Y, Divvy/Run messages, level drain,
  friendly group.
- Proposed rule change: emulator guide (first-person RPGs): item powers can hide behind Equip as well as Use;
  read the item records before calling a quest item inert. Tool wishes: try.py tiles checkpoint-only lines;
  the skill should steer to `--publish-only` right after a passing `--verify`.
- Corrected: coordinator looked at the sheets; floor-gate rule now verified in play (any good member admits to
  2/4, any good member refused on 3/5), correcting both the scout and the walkthrough; cold `--verify` by the
  coordinator (docs/progress-log.md 2026-11-19).
- Status: logged; `--publish-only` after `--verify` promoted 2026-11-19 into skill.md step 3 (the skill text
  named only `--publish`; MM2 and this run both paid a second full replay); previewer wishes added to the tool
  item in docs/status.md (fourth request).

### 2026-11-19 - Wizardry II (DOS) set main
- Task: set `main` to the ending with the three lenses and the Wizardry III transfer save (213 shots, commit
  af9641c).
- Worked: plan files per area previewed with try.py, then `shoot.py --only` in the background while planning
  the next batch; `w40`/`w20` timelines for message frames; a survey script choosing the approach side from the
  decoded walls of both squares (doors can be one-way); interactive `play.py` with a checkpoint per round for
  multi-round guardian fights; the backend open-file fix let the ending chain run from cached checkpoints.
- Friction: (1) try.py `--frames K` counts from the end of all tokens, so short routes mix in early frames;
  (2) forcing random fights on floors 3-6 (arrival/turn on a fight-zone square rarely worked; a real step into a
  room with wait variants did); (3) HP/status pokes show only after a menu change, battle HP written back at
  round end; (4) identical wireframe floor views found only by the final verify (4 shots dropped, another full
  replay); (5) `checkpoint` refuses the session's start checkpoint name after an `undo`. Not captured: floor 2
  (16,3) room (doors open outward only), floor 6 fixed fight, spinners, stones, M)ake scenario disk after Y.
- Proposed rule change: emulator guide, first-person RPGs: compare new "floor view" shots with the existing ones
  before snapping (wireframe floors can be pixel-identical); tool wishes: a shared previewer (shoot.py's settle,
  plan-file input, `--frames` from a marker token) and a duplicate check in `shoot.py --only`.
- Corrected: coordinator looked at the sheets and dropped `save_leave_game` (mostly DOSBox Pure's own
  "press any key to return to start menu" overlay: emulator UI, which the Wizardry I capture had left out for
  that reason); lens rows updated; cold `--verify` by the coordinator (docs/progress-log.md 2026-11-19).
- Status: floor-view rule promoted 2026-11-19 into docs/emulator/README.md; previewer wish: third occurrence
  (MM2, Wizardry I, this run), moved to docs/status.md Next as a tool to build.

### 2026-11-19 - Wizardry I (DOS) set main
- Task: set `main` from power-on to the ending with Werdna beaten on screen, three lenses, transfer save for
  Wizardry II (208 shots, commits 23dc245 and 89185fc).
- Worked: shot lines written straight into plan files and previewed with the game's `try.py` (dozens of routes
  in parallel, one sheet) before `shoot.py --only`; timelines of 40-80 `w40` frames to pick battle message
  frames; a scripted "approach a square from every open side" survey from the decoded floor walls (~40 message
  squares in two runs); all 100 item names read by poking 8 items at a time into a pack; the real Werdna fight
  won with wait variants, no pokes.
- Friction: (1) try.py routes lack shoot.py's final settle, so previews can differ slightly; (2) long timeline
  sheets had to be cropped and split by hand; (3) reordering shots needs an edit script plus a full verify
  before `--publish-only`; (4) "NOT settled" noise for message frames ending in `!`. Not captured: Murphy's
  ghost and the keys (floor 1 statues never offer a search), spinner (no visible effect), Leave game screen
  (loader prints in DOS text mode), criticals, stoning, body recovery, Divvy message, M)ove characters past its
  first prompt.
- Proposed rule change: emulator guide, Cataloguing: party RPG battles: pick message frames from a timeline
  (`enter` then N x `w40`, tiled) instead of guessing waits; special squares: one route per open side from the
  decoded walls. Tool wishes: a shared try.py-style previewer with shoot.py's settle and paged timelines;
  `shoot.py --reorder FILE`.
- Corrected: coordinator looked at the contact sheets (game order, no broken frames) and reran `--verify` from
  an empty cache (result in docs/progress-log.md 2026-11-19).
- Status: logged (first report of the timeline technique; MM2's capture used try.py previews the same way:
  the previewer wish is the second occurrence, still a tool wish, not built).

### 2026-11-19 - Might and Magic II (DOS) set main
- Task: set `main` from power-on to the ending with the three lenses, saves 02-04 and the playbook (228 shots,
  commit f5a948a).
- Worked: decoding the end from memory and code instead of playing it (record diff around Kalohn -> quest-mark
  byte; test pokes -> the gate's bit; text-pointer tables -> ending code in 2SMITH.OVL -> fixed override code
  WAFE and the cipher answer's address); `try.py` previews of 20-55 candidate routes per run chose almost the
  whole set; party macros generated by a script and checked by tiling all twelve profiles in one run.
- Friction: (1) `play.py goto CHECKPOINT` loads the state saved when the checkpoint was made, not one rebuilt
  from the current macros, so after a macro edit the session silently differed from `shoot.py` replays;
  (2) full rebuild and full `--verify` of 228 DOS shots ~35 min each; (3) `unsnap` piped into `tail -0` raised
  BrokenPipe tracebacks; (4) turning to set the facing fires events on the landing square (captions adjusted).
  Not captured: hireling hire, Cartographer automap, elemental shrines/lords, bashing a locked door, time travel
  by the game's own means (YEAR poke used), temple cure and spell purchase transactions.
- Proposed rule change: emulator guide: after editing a macro a checkpoint uses, run `play.py checkpoint NAME`
  again or restart with `start --route`; tool wish: `goto` rebuilds when the expanded route's cache key changed.
- Corrected: coordinator looked at all three contact sheets (title to Congratulations, no broken frames),
  `lenses.py` 147 / 109 / 121 of 228, 133 in two or more; full `--verify` rerun by the coordinator (result in
  docs/progress-log.md 2026-11-19).
- Status: rule promoted 2026-11-19 into `docs/emulator/README.md` (third report of macro edits and checkpoints
  drifting apart: Might and Magic NES scout, MM1 DOS fix-up, this run); `goto` rebuild open tool wish.

### 2026-11-18 - Might and Magic Book One (DOS) fix-up round
- Task: fix-up of the published `main` set (3 duplicate groups, long captions, corrected LOWHP/WORTHY macros):
  249 shots verified and published.
- Worked: the game's `tools/try.py` with `--frames K --peek` answered all five questions (retreat frames,
  temple, trap-door map number, macro values, death timing) in one parallel run; a script looping
  `play.py recaption` with a length assert; `shoot.py --only` plus a comparison sheet of old and new frames; one
  background full verify.
- Friction: the agent's edit script stopped on an assert after the recaptions and the following `shoot.py
  --only` silently reshot the old routes (caught by looking at the pictures); the coordinator's count of long
  captions (33, from the published index) differed from the work list (38); a checkpoint that contains a
  superseded macro (`astral` with `WORTHY`) needs the same "new name" treatment as the macro; `lenses.py`
  checks the published set, not the work set.
- Proposed rule change: (1) a checkpoint whose route uses a superseded macro is superseded too: add a new
  checkpoint and move the shots; (2) `lenses.py SLUG SET --work`; (3) emulator guide, RAM section: after
  writing record pokes for a party, read all members on screen before using the macro in a shot.
- Corrected: nothing wrong found. Coordinator audited the republished index (no identical pictures, no caption
  over 80, no route with the old macros), looked at the six retaken shots, and re-verified the set (count in
  the progress log). The old macros were worse than the audit said: `WORTHY` marked only the first member, so
  the ending's performance total changed from 70122 to 399602 with the corrected macro.
- Status: (3) promoted 2026-11-18 into `docs/emulator/README.md` (second report of the same error: the scout's
  spacing and this round); (1) promoted into the same guide next to the macro rule; (2) open tool wish.

### 2026-11-18 - Might and Magic Book One (DOS) round 2
- Task: round 2 of set `main`: 137 shots added (mechanics, battles, environments, level-7 spells), the first
  three lens documents (systems, interface, content), 250/250 verified in two halves.
- Worked: an in-process survey of all 55 areas that reads the encounter list from memory (text instead of 55
  sheets to read); a parallel tester that tiles the last K frames of many candidate routes, with a crop for the
  combat message lines; generating the shot list from a script with anchors so new shots land in game order;
  setting the level and asking the trainer to confirm the experience value.
- Friction: a full `--verify` of 250 DOS shots was killed for lack of memory; `unsnap` needs a session; an
  off-by-one in the agent's own frame tester cost a reshoot of ten fights; the first survey read half of the
  monster number; a 400-line debug print wasted context; the contact sheet at 250 shots cannot be read as one
  image.
- Proposed rule change: (1) `shoot.py --verify` should free the emulator per shot or chunk itself; (2)
  `shoot.py` should drop the old file when a shot's id or category changes; (3) contact sheets over ~100 shots
  in pages; (4) promote a per-game survey (event squares + memory read of the encounter) into the skill for
  first-person RPGs.
- Corrected: (1) was a leak in `tools/lrcore.py`, not in shoot.py: a private copy of the core stayed loaded
  after close, about 40 MB per machine opened (measured 1232 MB after 30 opens, 120 MB after the fix). Fixed
  by the coordinator; the full verify in one run is in the progress log. The agent found that the scout's party
  record spacing was wrong (0x80, not 0x7F), so round 1's LOWHP and WORTHY macros hit a neighbouring byte for
  members 2-6; the macros were left as they are so round-1 routes reproduce, and the playbook says so.
  Coordinator looked at sixteen new shots and the captions of three that looked odd; nothing wrong found.
- Status: (1) done; (2), (3) open tool wishes (second request for unsnap/cleanup: see the entry below);
  (4) open, first request.

### 2026-11-18 - owner's rule: breadth
- Task: after the Might and Magic 1 (DOS) main set (113 shots) the owner asked for more battles with interesting
  enemies, the minor commands (bash, trade ...) to document mechanics, and several visual environments, and
  said to make this part of the skill: rather more features/mechanics/systems and shots than fewer.
- Status: promoted 2026-11-18 (skill.md step 6, `docs/capture-guide.md` must-have list).

### 2026-11-18 - Might and Magic Book One (DOS, first DOS game)
- Task: main set for Might and Magic 1 (DOS): 113/113 verified and published, three commits, area warp found,
  design reference and playbook extended.
- Worked: reading the Sorpigal overlay's exit handler gave the map loader and its id table in about six calls,
  and poking that handler's operands made every area one macro (WARP). Writing shot lines straight into the work
  `shots.txt` and running `shoot.py --only` (about 15 s per 20 shots) was faster than `play.py snap`. Parallel
  `emu.py --out` runs with one frame per token found every combat and ending frame. `scan.py` per area gave
  ready-made shot candidates.
- Friction: the scout's `maps.py` read event tables two bytes early (14-byte OVR header, not 12), which hid two
  event squares per area including the ending square, until the overlay was disassembled. `--publish-only`
  orders the index by the game folder's `shots.txt`, not the work set's. `unsnap` needs a running session.
  `emu.py` and `shoot.py` frames differ by a few frames on the animated title. The container clock barely
  advanced, so the time budget could not be measured. The contact sheet at 113 shots is too tall for one view.
- Proposed rule change: (1) skill.md: allow "write lines into the work `shots.txt` + `shoot.py --only`" as an
  alternative to `snap` for known routes, and copy the list to the game folder before `--publish-only`;
  (2) dos.md: an area overlay's exit handler holds the loader call, poke its operands for a warp; the 14-byte
  OVR header; (3) `play.py unsnap` without a session; (4) dispatches state the budget in tool calls too.
- Corrected: nothing found wrong. Coordinator re-verified the set from an empty cache (see the progress log for
  the count) and looked at twelve shots across the set (title, creation, shop, spell hit, victory, game over,
  lit cavern, forest, Okrim, Ironfist, both ending shots). The ending was reached by position poke with quest
  marks set on a level-1 party, as the agent states; captions say so.
- Status: open ((1) and (4) first asked here; (2) is game-specific and stays in the playbook; (3) tool wish).

### 2026-11-18 - Megami Tensei round 2
- Task: ROM maps of all 35 floors, level-up, battle magic, demon in battle, six bosses, ending, late password (41 ->
  88 shots; commits 5702a0b 1030de2).
- Worked: following the map-read routine from the position bytes decoded the format in ~20 calls; `play.py sample`
  picked every battle and typing frame; searching boss code by enemy id found each boss's required item; reading
  the level-up code showed the "next level" counter matters, not EXP.
- Friction: a warp does not reload a section's wall graphics; status window not redrawn after HP pokes; snap right
  after goto failed as stale (shot lost until a retake); battle cursors need longer waits; shared boss battle
  flags forced all boss routes from one checkpoint. ~260 calls (budget ~250).
- Proposed rule change: emulator guide: decode floor ownership before trusting a position scan; skill: `do settle`
  after `goto` before `snap`.
- Corrected: floor-ownership note added to the emulator guide; set and game.json checked, 6/6 re-verified.
- Status: promoted 2026-11-18 (floor ownership); logged (settle after goto: play.py already refuses a stale snap)

### 2026-11-18 - Megami Tensei II round 2
- Task: game order, start_room retake, Pazuzu, demons and fusion, shop and save point, maps (67/67; commits 9e8c146
  6d009b8).
- Worked: stepping onto every square of the ROM's overhead event table cracked the Devil Buster ending after 60+
  calls of code tracing; reading the code next to a system message gave the COMP layout in ~4 calls; a variant
  runner (`var.py`) and sampling typing text every 30 frames; map stitching from warped, sprite-hidden centre crops.
- Friction: `--publish` without `--only` re-shoots everything (past the 120 s limit); uncached `goto` timed out
  once; fusion menu needed held presses; events stepped on in the wrong area context show ERROR; third hand-made
  scanner, first map stitcher.
- Proposed rule change: (1) emulator guide: story gate -> step on every event-table entry first; (2) shared
  `tools/mapgrab.py`; (3) shared variant/sampling runner; (4) skill: run a full `--publish` in the background.
- Corrected: (1) added; (3) built as `play.py sample` (fifth request); 6/6 re-verified; naming roles checked on
  screen. (2) logged (first stitcher); (4) logged.
- Status: promoted 2026-11-18 ((1), (3)); open ((2), (4))

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
