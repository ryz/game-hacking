---
skill: game-capture
---

# Feedback log - game-capture

History: every run\'s feedback in full. Agents read `feedback.md` (open lessons) instead; the coordinator files
new entries here at the top.

Running log for this skill, newest first. Status: `open`, `logged`, `promoted YYYY-MM-DD`, `superseded`.
Never delete entries.

## Entries

### 2026-11-22 - Ultima I (DOS) set start
- Task: Ultima I DOS, set `start`, the early game played honestly to the first save (52 shots).
- Worked: a walker planning a path around the people (read from RAM), a few steps per `play.py do`, crossed
  castle and town at about one call per destination; a path search on MAP.BIN did the same outdoors; a
  checkpoint before each fight plus `goto` and the exact number of blows kept routes free of extra turns;
  `ROUTE,a,!` caught "Killed!" before the monster's answer scrolled it away.
- Friction: the walker's `play.py peek` calls count toward `call=` (~5x the agent's own calls); extra blows
  after a kill needed a `goto` (undo is one level).
- Proposed rule change: skill.md line for top-down `start` sets: walk with a path-search helper instead of
  position pokes; checkpoint before each fight, replay the exact blows. Backlog: peek counts toward `call=`.
- Corrected: none; sheet checked by the coordinator. Wrote games/dos/ultima/tools/walk.py (per game: the shared
  walk tool is on the backlog, now asked four times).
- Status: promoted 2026-11-22 (walk-helper lesson, three start-set runs: skill.md); backlog (walk tool, peek count).

### 2026-11-22 - Ultima III (DOS) set start
- Task: capture the Ultima III DOS `start` set (60 shots, honest play to the first Quit & Save).
- Worked: a BFS path script over the town file (moves joined by `w20`) gave walking routes in one call; a
  headless script passing turns and reading the object table found an honest first fight (eight wait variants
  in parallel, no pokes); branch shots built by splitting checkpoint routes at `,settle,` reproduced first try.
- Friction: renumbering ids after dropping shots made `shoot.py --prune` delete every renamed shot, so the
  whole set was reshot (the capture guide says renumbered files are renamed on the next run; they were not);
  the shop exit key was missing from the playbook (~4 calls).
- Proposed rule change: `shoot.py SLUG start --renumber` (rewrite `NN_` ids in play order, rename files
  instead of pruning); in `docs/emulator/README.md`: scan turn variants headless for honest fights on maps
  with wandering monsters.
- Corrected: none; four shots checked against captions by the coordinator. 60/60 verified by the agent,
  cachecheck 44/44.
- Status: backlog (renumber; walk/path tool third ask); headless fight scan logged (open lesson).

### 2026-11-22 - Ultima II (DOS) set start
- Task: Ultima II DOS set `start`, honest play from creation to the first Q save (48 shots).
- Worked: a short breadth-first search over the map bytes told at once which places are reachable on foot and
  gave exact key lists; walking them produced a real first fight with no setup. Previewing shop/talk lines in
  batches and checking merchant squares with `u2objs.py` fixed every failed Transact in one round.
- Friction: preview and the play session disagreed about the fight until the agent saw that settles between
  calls had moved the RNG (fight shots built in preview from a clean route); wandering merchants made each
  Transact timing-dependent; one key dropped during an automatic PASS on a long walk.
- Proposed rule change: a shared `tools/path.py SLUG MAP FROM TO` (map bytes + walkable tiles from game.json)
  for reachability and key routes on top-down maps.
- Corrected: none; sheet checked by the coordinator (48 shots in play order). Lord British's healing not
  reachable on foot (castle on an island), recorded in game.json "open".
- Status: backlog (walk/path tool, second ask: `docs/backlog.md`); RNG-moved-by-settles lesson logged.

### 2026-11-22 - Dragonflight (Amiga) round 3
- Task: Dragonflight Amiga capture round 3 (dungeon, Great Map, magic/potions) appended to `main`.
- Worked: rendering the suspected land grid as an image showed the whole world and its place icons in one
  look; one preview batch of Search+Enter per icon found two temples, two towns and the dungeon; a short
  disassembly (`moveq #msg` of a message index, then branches) answered "how to drink a potion" in ~5 calls
  after ~10 calls of UI guessing.
- Friction: `dis68k.py` treats an Amiga dump as Mega Drive (`--xref` maps to FF....); `play.py dump` writes
  JSON, not binary; preview label bars misled y offsets once; a black dungeon view looked like a disk hang.
- Proposed rule change: emulator README: a first-person view that stays black: try a click or a light
  before suspecting a load hang. Backlog: `dis68k.py` for Amiga dumps; `play.py dump --bin`.
- Corrected: the report called the red symbol after "Potion" a stray glyph from a poked suffix 00; the item
  names in RAM are "Potion " + character 88-91 (the game's marks), the suffix changes nothing: shots kept,
  playbook corrected. Coordinator verify 93/93 and 24/24 from an empty cache; save 03_dungeon pushed.
- Status: darkness lesson -> open lesson in feedback.md; two tool wishes -> backlog.

### 2026-11-22 - Dragonflight (Amiga) round 2
- Task: Dragonflight Amiga round 2: combat, magic and other systems, appended to `main`.
- Worked: `preview.py` with `?` frames and sheets to compare restore points; a flat route against chained
  routes isolated the restore problem in about 6 calls; poking the opponent kind/count during the load gave
  every monster picture; `--only` batches.
- Friction: the checkpoint cache is keyed by the expanded flat route, so a checkpoint rewritten from
  `@world,...` to the same tokens from power-on silently reused the state built through restores (file deleted
  by hand); a restore before a disk load changed what the load did, unflagged; ~30 calls hunting opponent HP.
- Proposed rule change: amiga.md: a state restored before a disk load can make the load fail; build such a
  checkpoint flat from power-on and checkpoint only after the load. Tool wish: cache key includes the build
  path (chained or flat).
- Corrected: coordinator verified 58 shots from an empty cache (result in progress log); pushed save 02_armed.
- Status: amiga.md note added (platform fact); cache key wish built 2026-11-22 (parent in the key).

### 2026-11-22 - Dragonflight (Amiga)
- Task: capture the Dragonflight (Amiga) start and main sets with the three lenses; find fights, shops,
  dungeon and magic.
- Worked: a random-walk script comparing part of the screen with the normal panel found the first encounter
  in one run; RAM string dumps (items, monsters, spells, shops) gave the content lens and item indexes; preview
  batches covered 12 unknown commands in one look.
- Friction: restores not exact on this core, so pictures depended on the order the checkpoint cache was built:
  four-job verifies from an empty cache disagreed, only `--jobs 1` full runs were stable (~30 calls); combat
  frames (Disk A load) never reproduced; watches printed byte-swapped on the Amiga; `play.py checkpoint` writes
  checkpoints.txt lines silently.
- Proposed rule change: Amiga sets shot and verified as full `--jobs 1` runs from an empty cache; tool wish:
  build every checkpoint as a flat replay from power-on where restores are not exact.
- Corrected: cause found in `tools/emu.py` `at_checkpoint`: on a cache miss it returned the machine that had
  just built the checkpoint, on a hit a machine loaded from the file; on an inexact platform the two go on
  differently. Fixed 2026-11-22: a miss now saves, then continues from the loaded file, so build order and
  `--jobs` no longer matter (verify result in the progress log). Watches: `Amiga.ENDIAN = "be"` was missing,
  added. The proposed `--jobs 1` rule is not needed after the fix.
- Status: tool wishes built (at_checkpoint reload, Amiga byte order); `play.py checkpoint` silence -> logged.

### 2026-11-22 - Wasteland (C64)
- Task: publish the Wasteland C64 `start` and `main` sets with the three lens documents.
- Worked: zero-page map size ($55/$56 = 64x64) led to the world map byte grid at $3C00 in about 5 calls; a search
  over it found the route to Highpool the scout missed. `--timeline` batch found the honest first fight in one call.
- Friction: C64 `play.py export` writes to `rom/saves/` (whole images), unclear whether owner milestone saves are
  committed; a repeated combat macro goes out of step as rangers fall (game over needs a poke, not input); the
  scout's `shots.txt` at the game root duplicates `shots/main/shots.txt` and goes stale.
- Proposed rule change: docs/emulator/README.md RAM: look for a byte grid of a top-down map's size before walking.
- Corrected: coordinator verify from an empty cache 49/49 and 62/62, both sheets looked at. README rule added
  (RAM, item 3). Save 02_highpool pushed to the vault (C64 saves are game data: vault, README row in saves/ only,
  as c64.md says). shots.txt duplication -> backlog. No state divergence seen (the scout's claim stays unconfirmed).
- Status: logged (README rule; backlog row)
### 2026-11-21 - Phantasie (C64)
- Task: capture the Phantasie (C64) start and main sets, write the lenses, update the playbook.
- Worked: decoding the BASIC variable table (VARTAB at 2D/2E) found position, party and combat state at once after
  per-byte RAM searches found nothing; float pokes gave a clean warp; a background walk script stopping on a map
  change found encounters without looking at frames; `--timeline` previews picked combat message frames.
- Friction: routes need `settle` after every menu key (presses during busy BASIC are dropped; same keys as separate
  `play.py` calls worked), ~15 calls to diagnose; first press after a message only clears it; `find` cannot find
  BASIC floats.
- Proposed rule change: c64.md note on BASIC games (variable table, floats); backlog `tools/c64vars.py`.
- Corrected: coordinator cold verify 39/39 and 77/77, lenses clean, contact sheet checked.
- Status: logged (platform fact -> c64.md; tool wish -> backlog)

### 2026-11-21 - The Bard's Tale III (Apple II), sequences
- Task: seq-dungeon-walk (29) and seq-automap (18), honest walks on UnterBrae 1-2 (owner: dungeon walk, more
  automap).
- Worked: scan.py on both levels plus a tiled crop of the message windows gave every stairs, message and fight
  square in one look; BFS over the decoded map planned the routes (tools/mazeroute.py); a per-step fight-free
  wait search (tools/safewalk.py) replaced trial previews; both sets in ~60 calls.
- Friction: doors need `k` (playbook said buildings only); scan.py's "name plate" rows were the roster, so the
  fight check missed fights until moved to rows 98-110; lenses.py does not take a whole seq set named in a row;
  the Mage Flame ran out mid-sequence without warning.
- Proposed rule change: README "Two loops": per-step wait search for fight-free walks; backlog: shared safewalk,
  lenses.py accepting `seq-NAME`.
- Corrected: coordinator deleted the cache and reran --verify: 29/29, 18/18; automap strip checked (the map
  grows modestly: small window, walls and doors only). No clips (the game redraws each step at once).
- Status: fight-free walk lesson -> feedback.md (open); safewalk -> backlog row "Shared module" Asked 8;
  lenses seq row -> backlog; logged.

### 2026-11-21 - The Bard's Tale III (Apple II)
- Task: capture `main` (110) and `start` (54) sets, 58 level maps, three lenses.
- Worked: preview batches (25 lit dungeon lines on one sheet showed which levels arrive in a fight, dark or on a
  prompt); start-set lines built from prefixes of the checkpoint routes by a script; scan.py found Tarjan on his
  6x6 level in one run; hirestext.py: two `learn` calls read message windows with few `?` (party roster
  unreadable).
- Friction: `preview.py --text` printed the text page until font.json existed; no monster group counts found
  for a won fight or the ending (~25 calls on fights that did not end); tall contact sheets downscale in Read.
- Proposed rule change: README: find the monster group record before playing rounds for a won fight or ending
  (~10 calls); backlog: contact sheet with 6 columns of half-size tiles for sets over 60 shots.
- Corrected: coordinator deleted the cache and reran --verify: start 54/54, main 110/110; sheet 2 checked.
  Level maps: wall decoding checked only against the catacombs automap (doubtful on UnterBrae 4, Sceadu).
- Status: group-record lesson promoted 2026-11-21 into skill.md step 4 (second case: Might and Magic II Apple
  II, Sheltem); contact-sheet wish -> backlog; logged.

### 2026-11-21 - Beyond Zork (DOS, palette 6 retake and Frotz shots)
- Task: retake main (88) and start (34) in COLOR palette 6 (owner's choice) and add Frotz comparison shots.
- Worked: a memory diff over repeated `color` commands plus the published ZIL source found the colour globals in 3
  calls; two pokes in BOOT (`GREYPC` interpreter defaults, `GREY` game globals) give grey from the first prompt;
  recolouring the old PNGs and comparing proved 122/122 routes unchanged; one preview sheet for 12 Frotz candidates.
- Friction: scripts get the game from `emu.Game(name)`, not `find_game`; the set index has no notes field (note
  went to a `#` line in shots.txt); plain `sleep` blocked (until-loop on a done file worked).
- Proposed rule change: README "RAM": for a restyle that must not change routes, copy the published PNGs first and
  compare each retake through a colour map; backlog: `shoot.py --verify --published --map OLD=NEW`, a notes field
  in the set index.
- Corrected: none. Coordinator: cold verify start 34/34, main 100/100; lenses clean; sheet looked at (grey except
  the palette and Frotz shots); four moors/shop shots compared with d8587ce0 through a colour map: consistent.
  About 50 of 180 calls.
- Status: restyle check -> open lesson in `feedback.md`; both tool wishes -> `docs/backlog.md`.

### 2026-11-21 - Beyond Zork (DOS, first text adventure)
- Task: sets `main` (87) and `start` (34) with the three lenses, from the scout's chain.
- Worked: `preview.py` sheets of 9-12 exploration routes explored an unknown text adventure (one look per 12
  commands) far better than `play.py` steps; the scout's chain and plan lines used as they were; `find "new == 6"`
  after a sale found the money at once.
- Friction: `play.py` restarts `call=N` with every `start` (no budget count across sessions); `gamestable.py`
  writes outside the game folder; `unsnap` also removes the line from the working `shots.txt`; routes differing
  only in typed commands change random layouts and scroll words (captions from the frame); "NOT settled" on every
  line from the blinking cursor buries real warnings.
- Proposed rule change: skill step 8: leave `gamestable.py` to the coordinator; dos.md: Z-machine object data
  stays big-endian.
- Corrected: no separate first-half commit (main shot in one batch): accepted. Coordinator re-verified from an
  empty cache: start 34/34, main 87/87; lenses clean; main sheet looked at (variety, deaths, shop, options, Frotz
  comparison). About 95 of 280 calls used.
- Status: gamestable rule promoted into skill.md 2026-11-21 (second case: the scout skill already has it); dos.md
  note extended; the settle noise is now a second case -> backlog row; `call=N` across sessions and `unsnap`
  editing shots.txt logged.

### 2026-11-21 - The Bard's Tale (Apple II)
- Task: capture `main` and `start` sets, lenses and dungeon maps for Bard's Tale (Apple II), including the open
  level warp and Mangar's Tower.
- Worked: `dis6502.py --route` plus a byte-pattern search over live memory found the level-change code in ~6
  calls; the warp opened every level, the final boss and the ending. `preview.py --crop` over the message
  window (38 special squares on one sheet) found Kylearan, Mangar and the riddles in one call. Varying the wait
  before a forced fight gave a different monster group each time (cheap portrait gallery).
- Friction: `play.py text` useless on Apple II hi-res screens (every message read from a picture); forced-fight
  flags are cleared on use, so the first map dumps lost the arrival square's flag; one wrong LV argument.
- Proposed rule change: README RAM: one-time square flags are cleared as they fire; dump before stepping on
  the arrival square or patch out the write-back.
- Corrected: coordinator deleted the cache and reran --verify: start 45/45, main 132/132; sheet 2 and the
  Mangar level 5 map checked. No honest won fight in main (ending by group-count poke, captioned).
- Status: one-time flags -> docs/emulator/README.md; hi-res text reader -> backlog (asked twice, with the
  Might and Magic II scout's text-page friction); logged.

### 2026-11-20 - Might and Magic II (Apple II), automap
- Task: add the Cartographer automap to the main set: one map partly walked, filled maps (Middlegate, C2, cavern).
- Worked: snapshotting 10000-1FFFF and 20000-2FFFF with peek and diffing around one step found the visited bits
  in auxiliary RAM in ~3 calls; a 256-byte block with walls on every edge found the wall map at once; a walker on
  emu.start/emu.play checking each step against the position byte gave a reproducible honest walk in one call.
- Friction: play.py find/dump/diff did not cover aux RAM or the language card (own peek-dump diff); a poke into
  page 2 looked ineffective because `m` rebuilds it (3 calls); shoot.py reports "NOT settled" for every shot of
  this game (all screens animate).
- Proposed rule change: apple2.md Memory: diff 10000-1FFFF too; raise the find/diff backlog row.
- Corrected: coordinator reran --verify --only on the 4 new ids from an empty cache (4/4), looked at all four
  maps; ran gamestable.py (README/status were stale after the game.json change).
- Status: find/dump/diff range asked twice -> built 2026-11-20 (Apple II SEARCH = mapped 48K + aux + language
  card; apple2.md updated, backlog row moved to done); "NOT settled" noise logged.

### 2026-11-20 - Might and Magic II (Apple II)
- Task: capture `main` and `start` for Might and Magic II (Apple II), solve the year variable, try the Sheltem fight.
- Worked: converting the DOS set's routes with a script gave ~150 working Apple II routes in three preview
  sheets; DOS event squares and start-set walking keys transfer one to one; `?` frames and `--timeline` found
  combat and victory frames; diffing a counter the game advances (the day, by resting) led to the century byte.
- Friction: `play.py dump`/`diff` cover only 0000-BFFF on the Apple II while this game keeps its state in the
  language card (own 192K dump script); encounter pictures load ~600 frames after "Encounter!"; a `freeze`
  cannot undo a condition set before it started.
- Proposed rule change: apple2.md: search all of 0-2FFFF (state in the language card), tool wish for
  find/dump/diff there; skill step 2: convert a captured port's routes with a script and preview in bulk.
- Corrected: coordinator deleted the cache and reran --verify: start 45/45, main 216/216; one caption over 80
  characters (gameplay_luck_plaque) shortened with recaption and republished; sheet 3 checked (Year= shows 900
  on some year-800 shots: the display quirk is in findings.md).
- Status: port-route conversion promoted 2026-11-20 into skill.md step 2 (second case: Might and Magic I Apple
  II replayed the DOS routes); language card note -> apple2.md; find/dump/diff range -> backlog; encounter
  load time already in the game's playbook.

### 2026-11-20 - Might and Magic II (DOS, set `start`)
- Task: set `start` for an honest new party from power-on to the first inn sign-in.
- Worked: decoding the area's wall map early (one dump, 161D6) plus a small BFS gave every walking route and
  showed the dispatch's (8,1) fight is walled in; a scripted walker stopping on a monster-record change found the
  first encounter in a few calls; logging both sides' HP per round picked fight frames, `preview.py` fixed them.
- Friction: the dispatch assumed the (8,1) fight was walkable and a purchase possible (walled in; 0 gold for all
  six), ~15 calls; `rm -f $W/*.png` blocked (`shoot.py --prune` is the tool); ids repeating the category
  (`01_boot_nwc_logo`) cost a rename pass; `play.py peek` per record costs one call each.
- Proposed rule change: guide/`shoot.py` warn when a start id repeats the category; coordinator: check starting
  gold and reachability of the first fight before dispatching a start set; backlog `tools/walk.py SLUG FROM TO`
  building walking routes from a wall-map decoder in `game.json`.
- Corrected: one commit instead of the two asked for (whole route verified in one pass): accepted. Coordinator
  re-verified `start` from an empty cache: 52/52 (104 s); sheet and battle captions checked against the frames.
  The repeat-category warning not built: the guide already accepts such ids and 20 published start shots in four
  games use them, so it would be noise.
- Status: coordinator lesson in `skills/coordinator/feedback.md` (open); walk.py in `docs/backlog.md`; id
  repeat logged.

### 2026-11-20 - Wizardry II (Apple II)
- Task: capture `start` (35) and `main` (229) for apple2/wizardry-2, plus the three lens documents.
- Worked: preview.py batches without a play.py session; `--text` captions for town screens; cropped
  `--timeline` sheets with `--page 90` found every timed battle, chest and guardian message; a montage script
  checked 58 new shots at once (caught captions where monsters struck first); a door-kick route generator from
  the decoded map (tools/doors.py) gave 13 encounters in two previews.
- Friction: captions edited in the work shots.txt do not reach index.json; --verify/--publish-only keep the old
  caption (second pass with recaption, one commit with long captions); preview --set does not flag identical
  frames inside an unshot plan.
- Proposed rule change: backlog: shoot.py takes captions/categories from the work shots.txt or warns; apple2 /
  Wizardry playbooks: after a poke warp the wireframe view is stale until a turn (`l,w200,r,w200`).
- Corrected: coordinator deleted the cache and reran --verify: start 35/35, main 229/229; sheet 3 checked.
- Status: caption sync and identical-frame flag -> backlog; stale view -> already in the game's playbook (Read
  first, Shortcuts WARP row); logged.

### 2026-11-20 - Sword of Vermilion (Mega Drive, run 4: town talk, encounters with map)
- Task: outdoor talk shots with the hero and speaker side by side mid-screen (owner's Stow example) and overworld
  encounters with the full area map in the panel (owner's example).
- Worked: line text -> ROM pointer -> Stow's line selector named the raid flag (FFC75C); NPC table FFD0E0 + n*0x40
  and the collision grid FF2000 (found via dis68k from FFC606) gave a BFS planner (tools/npcs.py --plan); one
  preview of 23 routes gave 14 usable talks; panels chosen at an Aries arrival show map and stats without walking.
- Friction: a `cat >` without heredoc hung ~10 calls; the Aries list ignores 8-frame taps and lands a row lower
  from a checkpoint than in a flat route (fixed by checking FFC40C); EXP above the threshold opened a level-up
  window (poke the whole stat block); `set:...:bcd` defaults to little-endian.
- Proposed rule change: README RAM section: NPC table + collision grid early, per-game talk planner; check
  menu-driven warps by RAM index.
- Corrected: none; coordinator re-verified main from an empty cache: 136/136; talk and encounter shots checked on
  a sheet (talk_stow_old_man matches the owner's example).
- Status: both lessons open in feedback.md; `set:bcd` byte order on big-endian platforms: backlog.

### 2026-11-20 - Sword of Vermilion (Mega Drive, run 3: bosses and ending)
- Task: first boss and the ending found through the code with dis68k, captured in main plus seq-boss and seq-ending.
- Worked: dis68k --xref plus a ROM search for 4-byte pointers found both triggers in ~15 calls (ending text ->
  state dispatcher FFC400 = 0x12; battle flag -> field loop boss request FFC8NN/FFC817); one preview --timeline
  sheet each for ending and boss intro/defeat; all 14 boss indices on one preview sheet.
- Friction: `--xref C400` gave an unrelated hit (needed FFC400); the dispatch's text address was 4 bytes early
  (0x17722 vs 0x17726); `play.py find` twice without play in between gives 0 candidates without a hint;
  preview --timeline applies to every -r route.
- Proposed rule change: (1) dis68k: 4-digit addresses as FFxxxx, hint when an address points inside an
  instruction/string; (2) md.md: recipe for finding what starts a scene; (3) playbook facts (written).
- Corrected: none; coordinator re-verified from an empty cache: main 113/113, seq-boss 14/14, seq-ending 12/12;
  boss and ending frames checked on a sheet. Bosses and ending are poked; boss 0 is not confirmed as the first
  met in play.
- Status: (1) 4-digit form built 2026-11-20, inside-instruction hint not built (backlog); (2) logged in md.md;
  (3) logged. find/timeline friction: backlog.

### 2026-11-20 - Sword of Vermilion (Mega Drive, run 2: area maps, presentations)
- Task: extend main with presentations and area maps; republish, lenses, playbook.
- Worked: preview --timeline found intro, prologue, Aries and battle-start frames in a few looks; RAM diff around
  the mirror found the map flags in 2 calls; searching the ROM for 4-byte pointers to a dialogue line found the
  town's (line table, flag) list and the story flags without a disassembler; RAM compared across 3 battle
  checkpoints gave the encounter-type byte.
- Friction: no 68000 disassembler (boss and ending triggers unreached; capstone install refused); preview --out
  with a path doubled it; --peek wanted a decimal length; wandering NPCs cost ~15 calls.
- Proposed rule change: (1) backlog: tools/dis68k.py; (2) fix preview --out and hex --peek; (3) md.md: a
  mode-like byte can be an ignored status copy.
- Corrected: none; coordinator re-verified from an empty cache: main 96/96, seq-aries 7/7; map shots checked on a
  sheet. Note: seq-aries 04_warp_clip.png equals 05_arrival (the warp is only in the GIF).
- Status: (1) backlog; (2) fixed 2026-11-20; (3) logged in md.md.

### 2026-11-20 - Sword of Vermilion (Mega Drive)
- Task: capture and publish `main` and `start` of Sword of Vermilion (md) with the three lenses.
- Worked: preview.py with `?` markers gave whole dialogue/menu sequences on one sheet; the map as a 48x32 byte
  window in RAM and a BFS walker (battles fought with HP frozen) reached Parma and two caves without frames;
  item/spell lists found by diffing around one purchase.
- Friction: cursor moves after `c,w60` dropped in preview/shoot but not in play.py (settles between calls);
  the walker lost its place when the map window re-centred; town interiors have no readable map; enemies can
  push the prince off the edge (battle ends as an escape). Playbook "Read first" 61 lines (limit 60).
- Proposed rule change: (1) README "Two loops": routes copied from play.py need `settle` where calls were split;
  (2) md.md: maps as byte grids in work RAM.
- Corrected: none; coordinator re-verified from an empty cache: main 65/65, start 35/35; sheets checked.
- Status: (1) promoted 2026-11-20 into docs/emulator/README.md (second case: the scout's round-1 friction);
  (2) logged in md.md.

### 2026-11-20 - owner's rule: start sets in sequential order
- Task: owner's request, not an agent run.
- Worked: Dungeon Master's `start` set already used numbered ids (`01_crack_note` ...) in play order.
- Friction: Apple II Wizardry's `start` set has unnumbered ids, and its list and `index.md` are not in play
  order (Tavern A)dd after the roster, a chest before the first shop), so the set is hard to follow.
- Proposed rule change: `start` ids numbered `01_<step>` ... in play order, `shots.txt` in that order.
- Corrected: -
- Status: promoted 2026-11-20 (owner's rule; `docs/capture-guide.md` "Sets", skill step "Standard environment shots").
  Same day, owner's follow-up: in `start` sets the number goes before the category in the file name
  (`tools/shoot.py` `stem()`); both existing `start` sets renamed.

### 2026-11-20 - Dungeon Master (Amiga)
- Task: Dungeon Master (Amiga v3.60) sets `main` (to the ending) and `start`, three lenses, from the scout's playbook.
- Worked: reading the whole dungeon from RAM once (map descriptors, squares, thing tables) gave stairs, monsters and
  walls for every level; the level warp is "poke onto a down staircase and turn"; generated viewing positions gave
  22 creature kinds in one preview batch; a parallel previewer (4 routes, tiled at native size) and a timeline tool
  (route plus N times a step, tiled) found every frame (damage starbursts, ending messages); poking map squares
  into walls in the same frame as the click made the scripted ending (FUSE) possible.
- Friction: (1) the scout's same-level warp poked the facing byte, which with champions in the party leaves their
  formation cells unrotated and the fighters' blows never land (about 15 calls to diagnose); (2) previewing with
  `emu.play` needs `E.expand(g, E.split(...))` for macros; (3) the PUAE core printed `retro_vfs_file_open_impl`
  lines on every state load; (4) the cold verify of 148 shots took about 35 minutes.
- Proposed rule change: (a) docs/emulator/README.md, RAM: in party games never poke the facing byte, move by
  position pokes plus the game's own turns; (b) a shared `tools/preview.py` (parallel previews tiled at native
  size, timeline mode); (c) silence the core's VFS log.
- Corrected: coordinator checked the commits (game folder only), counts (main 111, start 37), lenses (clean), the
  contact sheets, and re-verified `ending_grey_lord` and `start/37_saved` from an empty cache (both reproduce).
  (c) fixed: two leftover debug printfs in the core's libretro-common VFS removed in `tools/puae-debug.patch`.
- Status: (a) open (first time seen; promote on a second case or the owner's word); (b) open (also asked for by
  earlier runs as cachecheck/screen tools); (c) done 2026-11-20.

### 2026-11-19 - Wizardry I (Apple II)
- Task: set `main` for Apple II Wizardry I from the title to the ending with three lenses: 291 shots, cold verify
  298/298 before seven duplicates were dropped, published, commit c846278 pushed.
- Worked: no interactive session at all. Plan files in shots.txt format, previewed four at a time by a small
  wrapper that plays each line exactly as `shoot.py` does and prints the 40x24 text screen, so about 120
  text-screen shots were captioned from text without opening a picture. Timelines (route + N x `w80`, tiled)
  found every battle, chest and temple message. Rebuilding all 25 checkpoints in parallel first took about 7
  minutes.
- Friction: (1) a checkpoint route is flattened and replayed from power-on, so each of 25 checkpoints costs a full
  boot and the serial cold verify took 30 minutes; (2) the `--frames K` count of `try.py` includes the trailing
  `!`, so every timeline was read one step early and 42 shots were reshot; (3) `w100*26` is one token, not 26;
  (4) duplicates surface only in the final verify, and after `unsnap` `--publish-only` ran on a set that differed
  from the verified one; (5) milestone commits were skipped to save time that was not short; (6) the skill's
  commit recipe says `git pull --rebase`, which the dispatch forbade and the permission system refused.
- Proposed rule change: skill step 3: replace `git pull --rebase` with a plain push and retry when the dispatch
  forbids rebasing. Emulator guide: "frame k of a timeline = `w(step*k)`; check one message shot before writing
  forty", and "Apple II Wizardry: doors need K, the temple needs the patient out of the party". Tool wishes: a
  duplicate check in `shoot.py --only`, and a shared previewer with a text-screen option for Apple II.
- Corrected: coordinator re-verified the 291 published shots, ran the lens check (clean) and read the one caption
  the agent flagged as unreadable (`gameplay_elevator_f2`: buttons A through D). One commit instead of
  milestone commits; no shared file changed for the proposals: the owner halted the queue after this run.
- Status: open

### 2026-11-19 - Phantasy Star (Master System, US/EU), part 2
- Task: rest of the game, a battles set, four dungeon sequences: main 109, battles 12, seq-dungeon-walk/turn/
  stairs/door 6/6/4/4, commit 32802e3; ending not reached (Dark Falz trigger not found).
- Worked: decoding the ROM's own tables (entrances, town buildings/people, dungeon events, monsters, text) made
  every place reachable from @start; writing the game state byte C202 gave clean warps and battles; a small
  preview harness (~0.1 s per route) before `shoot.py --only`.
- Friction: ending trigger and event-scene cursor timing (Odin's cure) cost many calls without result; a warped
  overworld still counts as a town for vehicles; no Z80 disassembler; full-page fetches of walkthrough hosts fail.
- Proposed rule change: (1) emulator README RAM section: find the game's main state byte and write its
  "enter map"/"start battle" values for clean warps; (2) tools: a Z80 disassembler like dis6502.py.
- Corrected: coordinator re-ran all six sets from an empty cache: 141/141; lenses clean; sheets looked at.
  The battles set is mostly forced encounters on one field background (Lassic and Dark Falz included, captioned
  honestly), weaker than the dispatch asked for real boss rooms; retakes listed by the agent.
- Status: (1) logged; (2) open tool wish.

### 2026-11-19 - Phantasy Star (Master System, US/EU), early game
- Task: early part of the main set: 53 shots (title, intro, Camineet, shops, church, menus, items, overworld,
  battles with EXP/level-up/chests, lit cave with clips and a chest, death and game over, continue), 53/53 from
  an empty cache, three lenses for the early game, commit 75ae7b7.
- Worked: shooting the scout's planned lines first, then fixing what the sheet showed; `play.py sample` for
  flash/typing frames; a RAM dump in first person showed the 16x16 floor map (CB00) in two calls.
- Friction: `record` refuses after `sample` (stale screen); ~12 calls lost on how to talk to townspeople (no
  source reachable); the playbook's town-poke note read as a warp, it is not.
- Proposed rule change: (1) emulator README: in first-person views dump RAM once and look for a 16x16 block
  with few distinct values (the floor map); (2) tools: `sample` should not mark the screen stale, or `record`
  should take leading tokens.
- Corrected: coordinator re-ran `shoot.py sms/phantasy-star main --verify` from an empty cache: 53/53; sheet
  looked at, all frames as captioned (intro_nero_dying is one page of a longer speech).
- Status: (1) logged (first report); (2) open tool wish.

### 2026-11-19 - Ultima III (DOS) set main
- Task: set `main` from power-on to the ending with three lenses: 260 shots, 260/260 from an empty cache,
  published and pushed (c835148, 9a54149).
- Worked: a simulator of the random generator (`u3rng.py`) found the state for every chest, trap and steal
  outcome in one try; a monster-placement macro (`MON`) gave all nine combat fields; `play.py sample
  "space,w90" N` with a crop of the message area found the rare combat lines; cold verify of 260 shots took a
  few minutes.
- Friction: a poke before a waiting prompt does not survive the idle loop, which rolls every frame (one shot
  lost); the scout's `SHIP` note was wrong (a calm blocks frigates too); `DNG` needs a two-digit facing;
  `recaption` updates the work `shots.txt` but not the game's copy; background waits hit the shell's sleep
  and timeout rules. Not captured: Ready refused in combat, Surmandum failing into ashes, lava damage without
  the Mark of Fire, the Shrine of Strength (same picture as Intelligence), the wandering jester, starvation
  and poison damage per turn.
- Proposed rule change: emulator guide: write a simulator of the generator and poke right before the deciding
  key, not before a waiting prompt; skill step 7: copy the work list to the game's `shots.txt` before the final
  verify.
- Corrected: coordinator cold `--verify` 260/260, lenses clean (189 / 100 / 115), sheets looked at.
- Status: random-state rule promoted 2026-11-19 into docs/emulator/README.md (third report: Ultima I, II, III);
  `recaption` and the game's shots.txt: open tool wish.

### 2026-11-19 - Ultima II (DOS) set main
- Task: set `main` from power-on to the ending with the three lenses: 226 shots, 226/226 from an empty cache,
  published, commit 3288ec2.
- Worked: a string-to-offset helper over the scout's disassembly answered the open questions in a few calls
  each (shops, spawning, dungeon format, chests, traps, steal, the clerk, death); random-state pokes forced
  every rare outcome; small route generators (merchant, monster, talk placement) + try.py sheets of 10-50
  candidates, then `shoot.py --only`, ~15 batches; Minax killed in an honest fight.
- Friction: captions had to be checked against the four-line command log (long answers scroll earlier lines
  away; two captions first named commands no longer on screen); `!,settle` inside recorded routes reads oddly;
  a cold verify of 226 DOS shots ~15-20 min, and one late HUD shot cost a second full verify; no way to wait
  for a background verify except a polling loop. Not captured: Up ladder and Blink spells (FAILED), fleeing,
  natural-kill loot, Uranus talk lines (no named people), dungeon pictures 2/4/6 on their own.
- Proposed rule change: skill step 6: check the must-have list (title, menu, first control, HUD, game over)
  before the first cold verify; emulator guide: in games with a short scrolling command log, write the caption
  from the frame, not from the keys sent.
- Corrected: coordinator cold `--verify` 226/226, lenses clean (164 / 72 / 152), sheets looked at; the scout's
  Lord British thresholds corrected by this run.
- Status: logged (first report of both).

### 2026-11-19 - Ultima I (DOS) set main
- Task: set `main` from power-on to the ending with the three lenses: 195 shots, 195/195 from an empty cache,
  published and pushed (1c37e9d, d19fdf1).
- Worked: string refs plus ndisasm gave steal, pub, king, landmark, chest/coffin and docking rules in a few calls;
  the random number state (115CC) poked right before the deciding key picks any roll reproducibly; dungeon
  monsters placed by poking the square in front (all 25 kinds in one sheet); a mid-game save through `sav:` gives
  correct panel values; batches of 10-30 lines previewed, shot with `--only`, new shots tiled.
- Friction: try.py and the shot of `system_steal` disagreed until the cache was deleted (stale scout states);
  try.py labels hide bottom-line messages; checkpoint-only lines give no try frame; ~25 calls on starbase docking
  without success; `w650!` fails (`w650,!` works). Not captured: starbase docking and ship choice, pub seduction,
  bard/jester songs, Steal spell (not sold), Evil ranger and Invisible seeker shots.
- Proposed rule change: emulator guide: find the game's random number state early and poke it right before the
  deciding key; capture skill: delete the game's cache at the start of a capture that follows a scout.
- Corrected: coordinator cold `--verify` 195/195, `lenses.py` clean, sheets looked at (overworld, all dungeon
  levels, space, Mondain, ending).
- Status: cache-at-start promoted 2026-11-19 into skill.md step 1 (second report of stale states, after
  Wizardry III); RNG rule logged (first report).

### 2026-11-19 - Wizardry III (DOS) fix-up: cold verify
- Task: 29 shots (everything from checkpoint `gfloor6` on) did not reproduce from an empty cache (coordinator
  verify 199/228); fixed the `gfloor6` route, cold verify 228/228 (commit ad4511a), no shot retaken.
- Worked: the coordinator's evidence (loaded states and cold build agree, the session's states do not) pinned it
  to one checkpoint; reading `emu.play()` gave the cause; a try.py pixel comparison against the published
  PNGs proved the fix before the 15-minute verify.
- Friction: `play.py do "y,w300!"` pressed `y`, then failed on the bad token: the press was in the machine but
  not in the route, nothing rolled back; the agent's own verify passed because the cache held the drifted
  states.
- Proposed rule change: play.py `do` validates or rolls back; skill step 7: final `--verify` after deleting
  the cache; emulator guide: `undo` after a failed `do`.
- Corrected: coordinator fixed `play.py` (`do` and `sample` restore the state on any error; regression check in
  `test_dos_pipeline` fails without the fix, 0/3 reproduce) and reran the cold verify (docs/progress-log.md).
- Status: tool fixed 2026-11-19 (the `undo` rule is not needed); step 7 promoted 2026-11-19 (empty-cache final
  verify: the coordinator's own practice since Wizardry I, now required of the agent).

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
