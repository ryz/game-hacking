---
skill: game-scout
---

# Feedback log - game-scout

History: every run\'s feedback in full. Agents read `feedback.md` (open lessons) instead; the coordinator files
new entries here at the top.

Running log for this skill, newest first. Status: `open`, `logged`, `promoted YYYY-MM-DD`, `superseded`.
Never delete entries.

## Entries

### 2026-11-25 - Wolfenstein 3D (DOS, Activision 1.4)
- Task: boot, model, controls, determinism, checkpoints to the first save, RAM, `start` and `main` plans with
  action shots.
- Worked: dumping conventional memory after the EXE unpacked gave every parameter, debug message and menu string
  in one call (`goobers`, `tedlevel`, `nowait`, no "Read This!"); CONFIG.WL6 explained the dead arrow keys (WASD);
  long preview routes with `?` frames and `--peek` found each E1M1 leg in one call; `tools/wlmap.py` map reader.
- Friction: `cachecheck` said "DIFFERS (memory)" with hashes only (scratch script needed); even flat checkpoints
  differ after a load; `w30` (wait) vs `w:30` (W key) easy to confuse in WASD games; `preview --peek` reads only
  after the last token.
- Proposed rule change: dos.md note for Wolfenstein; backlog: `cachecheck --diff`, `preview --peek` at every `?`.
- Corrected: the flat-only rule for shot routes was too strict: coordinator checked miss vs hits on
  `@s_guard2,...` (identical frame and actor memory three times), so `@s_...` shot routes reproduce; playbook
  corrected. Stop condition "checkpoints reproduce" is met in the sense that matters (cold == hit; only flat
  differs, in memory).
- Status: `cachecheck --show-diff N` built 2026-11-25 (second ask after Sword of Vermilion; test added); dos.md
  note added; `preview --peek` at `?` frames -> `docs/backlog.md`; WASD wait/key confusion logged.

### 2026-11-23 - Quake (DOS shareware 1.06)
- Task: scout Quake for a `start` set: boot, model, controls, determinism, checkpoints to the first in-game save,
  previewed plan.
- Worked: the map entity lump from PAK0.PAK gave exact positions (skill triggers, gates, monsters with skill flags,
  secrets): cheap routing in 3D; a game-specific chain helper (`tools/qstate.py`) replaced dozens of play.py
  calls; finding the player entity by a field pattern (hull mins/maxs, view height) beat a float diff search.
- Friction: DOS savestates are not exact for a real-time game (state + key diverges from flat; with sound even
  without keys), ~15 calls to isolate; a cache miss gave other pictures than a hit (`at_checkpoint` continued
  live); no float RAM watch; nothing warns that undo/goto make the next snapped route unrepeatable here.
- Proposed rule change: dos.md real-time note; backlog: core patch serialising input timing, `at_checkpoint`
  reloading what it saved, `"fmt": "f32"` watch.
- Corrected: coordinator fixed `at_checkpoint` (a miss reloads the state it saved; checked miss == hit on
  `@s_e1m1,up:40,...`), so `qstate.py --warm` is no longer needed (playbook struck). Cold `cachecheck` 10/10;
  sheet matches.
- Status: dos.md note added (platform fact); at_checkpoint built 2026-11-23; core input timing and f32 watch in
  `docs/backlog.md`.
### 2026-11-22 - Dragonflight (Amiga)
- Task: scout Dragonflight (Amiga, Thalion 1990): boot, controls, RAM, save/load, shot plan.
- Worked: placing the mouse by poking the game's own pointer variable (found with `find` after two relative
  moves) instead of HOME-plus-offset moves; `preview.py --timeline` mapped the long loads; plain-ASCII game text
  in a RAM dump replaced the missing manual (commands, messages, opponents).
- Friction: (1) every cachecheck line DIFFERS: a loaded state gives the same frame but 30-45 bytes of game RAM
  differ 60 frames later, already in the Kickstart boot on A500; (2) large `mouse:` moves wrap in this game
  (it reads the counters every few frames); (3) web research empty (Thalion Webshrine host not allowed, GameFAQs
  403); (4) `play.py dump` without a name crashes.
- Proposed rule change: amiga.md Keys: look for the game's pointer variable first; amiga.md Backend: restores
  are not exact in every game; backlog: exact restore, research hosts, `play.py dump` default.
- Corrected: coordinator reproduced the drift (w100 on A500: slow RAM differs after 60 frames). Causes found:
  the core restores at beam line 0 while states are saved about 3 lines after the vsync, and `cia_reset`
  zeroes the keyboard handshake counter after a restore. Neither fix removed the drift in the crack intro
  (same bytes with and without them); core left unchanged, findings in `docs/backlog.md`.
- Status: pointer lesson -> `docs/emulator/amiga.md` (platform fact); restore -> amiga.md + backlog; research
  hosts and `play.py dump` -> backlog.

### 2026-11-21 - Wasteland (C64)
- Task: scout Wasteland (C64, 9 D64 images, EA/Interplay 1988): boot and disk swaps, controls, RAM map,
  checkpoints up to the world map and a first fight.
- Worked: byte comparison of the D64 images settled masters (disk:1-4) vs play copies (disk:5-8) in one call;
  preview.py batches of 4-12 key variants found movement keys, Esc, field commands and combat; dump/diff over
  three steps found the party block (F400) and character records (F500 + 0x100 each).
- Friction: play continued from a loaded state seemed to roll differently from a power-on replay (encounters,
  creation rolls), about 15 calls; `play.py goto` piped to /dev/null once seemed not to take effect; about 20
  calls walking around Highpool's mountain ring; mocagh.org unreachable.
- Proposed rule change: c64.md: savestates not exact for every game, write chance-dependent checkpoints from
  power-on; backlog: find the C64 random source missing from the state; c64.md: Esc is usually `leftarrow`.
- Corrected: coordinator could not reproduce the state divergence: `@start,w1000` and `@party,LEAVE,ORDER4,
  settle,w1000` match the power-on replay (same "3 Animals" frame) in two cachecheck runs; suspect is the
  interactive `play.py` session (goto/do between calls), not the savestate. Not written into c64.md. Cachecheck
  6/6 verified; save 01_start pushed to the vault.
- Status: open (state divergence in play.py sessions: waiting for a second case with a reproduction); Esc ->
  game playbook (C64 games differ)
### 2026-11-21 - Phantasie (C64)
- Task: scout Phantasie (C64, first real game on the VICE backend): boot, party creation, first save, RAM map,
  shot plan.
- Worked: `preview.py --text` with `?` markers to compare stat rolls and bank withdrawals in one call;
  `--timeline` with long steps (300-600 frames) for load times on a slow drive; archive.org `/stream/.../_djvu.txt`
  for manual text when the PDF host is blocked; "Continue saved game" on the dump found a ready-made second party.
- Friction: slow disk loads make `settle` useless (static frames for thousands of frames), every load needed a
  timeline; macro arguments plus `*N` failed silently; outdoor moves lose presses unless the wait is long (three
  previews); about 25 calls on encounter hunting found nothing.
- Proposed rule change: c64.md note on load times and fixed waits, and on previous owners' saves on used disks;
  emu.py: reject or support `MACRO:args*N`.
- Corrected: coordinator verified cachecheck 10/10. `MACRO:args*N` now repeats the filled-in macro (emu.py, test
  `test_macro_with_arguments_repeats`). c64.md got the load-time note.
- Status: logged (platform fact -> c64.md; tool wish built 2026-11-21; `?` inside a token -> backlog)
### 2026-11-21 - The Bard's Tale III (Apple II)
- Task: scout The Bard's Tale III (Apple II): dump check of disk 3, boot, party, RAM, warps, automap,
  checkpoints and a shot plan.
- Worked: loading every level through the game's own stairs code made a complete dump check possible in one
  background run (tools/levels.py: 34 + 27 levels, 10 city maps); the BT1 approach (cityscan -> scan.py, warps
  through the stairs code) carried over almost unchanged; preview `-r` variants in parallel kept looks low.
- Friction: random encounters spoil scans and routes; position scans depend on the facing at arrival;
  `play.py checkpoint ... >/dev/null` hid a lost checkpoint and the session crashed once without a reason; city
  maps live on the character disk (found only through the prompt). Coordinator swapped disk 3 mid-run (second
  upload); the agent redid the check on the new image.
- Proposed rule change: skill step 3: load every level through the game's level code before writing warps (dump
  check too); backlog: shared position-scan tool with a fight filter.
- Corrected: coordinator reran cachecheck: 25/25, sheet checked.
- Status: level-load lesson -> feedback.md (open); scan tool -> backlog row "Shared module ..." Asked 6 -> 7;
  logged.

### 2026-11-21 - Beyond Zork (DOS)
- Task: scout Beyond Zork (DOS): interpreter, boot macros, controls, first save and RESTORE, checkpoints to the
  first save, shot plan.
- Worked: `preview.py -r` batches of 8 routes found the start-menu order, the interpreter choice, all ten function
  keys and the opening map in 4 sheets; the Z-machine base found by searching DOS memory for the story header,
  then attributes by value (3 calls, any Z-machine game).
- Friction: `type:` cannot hold a comma (the `comma` token workaround was not documented); "NOT settled" on every
  frame of a blinking-cursor graphics game hides real settle problems; no approved walkthrough host, so the plan
  stops at the opening; Infocom's DOS interpreter stores words little-endian (easy to misread).
- Proposed rule change: dos.md comma note and Z-machine note; backlog: `--text` for graphics-mode text games
  (OCR of the 8x8 font or Z-machine output).
- Corrected: none. Coordinator: `cachecheck.py dos/beyond-zork` from an empty cache 11/11, sheet matches the
  descriptions; `gamestable.py` run (the scout left the table test failing, by design).
- Status: both notes in `docs/emulator/dos.md` (platform facts); text-reading wish in `docs/backlog.md`; the
  settle noise logged (second case would make it a backlog row).
### 2026-11-21 - The Bard's Tale (Apple II)
- Task: scout The Bard's Tale (Apple II, 4 disks): boot, party, city, dungeons, RAM, warp, automap answer, shot plan.
- Worked: poking the position onto every square and grouping the message-window bytes (cityscan.py) mapped all
  of Skara Brae's buildings and a dungeon level's events in one unattended run and gave the GO warp table;
  three-way dumps (city / cellar / sewers) narrowed the level candidates to five bytes.
- Friction: manual and FAQ hosts blocked (403; archive.org downloads redirect to dn*.archive.org, not allowed),
  spell codes found by trying; no 6502 disassembler for Apple II memory (dis6502.dis over a dump by hand);
  status lines not redrawn after a poke (fixed with New order); scan output lost once by piping to tail.
- Proposed rule change: README Web research: archive.org downloads need other hosts; backlog: dis6502 on an
  Apple II dump or checkpoint; apple2.md: the poke-every-square scan for buildings and events.
- Corrected: coordinator reran cachecheck: 16/16, sheet checked (dungeon views dark without light).
- Status: dis6502 asked twice -> built 2026-11-21 (`--route`); archive.org note -> docs/emulator/README.md;
  square scan -> apple2.md; logged.

### 2026-11-20 - Might and Magic II (Apple II)
- Task: scout Apple II Might and Magic II (boot, party, warp, RAM, checkpoints, shot plan).
- Worked: matching the DOS port's area-neighbour bytes (07 22 0E 0A) found the area header in language-card RAM
  in one search, and from it the key table, forward handler and loader; previewing the warp to all 60 ids
  cropped to the prompt mapped every area to its disk in one look; previewing the whole plan caught 3 bad routes.
- Friction: `play.py dump` JSON keys are unpadded hex (read as decimal, calls lost); no 6502 disassembler for
  Apple II memory (installed py65, scratch script); `settle` on animated encounter screens changed a fight's
  outcome while cachecheck still reported it reproducing; `play.py text` useless when text page 1 holds data.
- Proposed rule change: apple2.md / backlog: dis6502.py on a dump or main/aux memory; dump keys are hex;
  README: end checkpoints on animated encounter screens with a fixed wait or `!`, never `settle`.
- Corrected: commits checked (d2b87ee, 39d28ea, 10f369d, only its folder); cachecheck rerun by the coordinator.
- Status: dis6502 and dump keys -> backlog; settle rule -> docs/emulator/README.md (platform-independent tool
  fact, added to the `!` row); logged.

### 2026-11-20 - Sword of Vermilion (Mega Drive, round 2)
- Task: reach the overworld and the first battle as checkpoints; verify the buttons there.
- Worked: a search snippet led to retrying the gate after Blade's speech; preview batches with --peek found
  gate, encounter step and battle buttons; mashing each button in parallel with EXP/kims/HP peeked found the
  attack button; diff --range found the overworld position at once.
- Friction: cachecheck says "DIFFERS (memory)" without addresses (a dropped `revived` checkpoint); preview
  --timeline only adds waits; speedrun.com, rpgclassics not allowed, GameFAQs 403.
- Proposed rule change: (1) lesson: retry an exit after the story event; (2) backlog: cachecheck --show-diff;
  (3) backlog: preview --repeat; (4) md.md: mid-battle state drift, to confirm.
- Corrected: (4) checked by the coordinator: the only difference is a dead stack word (FFFD8C), gone after more
  play; game state and frames equal. 23/23 checkpoints reproduce (cachecheck, sheet checked).
- Status: (1) open (merged with the door lesson); (2), (3) backlog; (4) logged in md.md with the explanation.

### 2026-11-20 - Sword of Vermilion (Mega Drive, round 1)
- Task: scout Sword of Vermilion, the first Mega Drive game: boot, controls, checkpoints, save, shot plan.
- Worked: md backend deterministic; big-endian set:/poke: and BCD watches; odd-byte cartridge RAM via peek
  200001; export/sav:/Continue round-trip; H32 256-wide name keyboard; preview batches of 3-6 variants found the
  door, stair and church-counter rules; the ROM's ASCII strings replaced blocked wikis for names.
- Friction: research hosts blocked (GameFAQs, tcrf, StrategyWiki 403; archive.org file hosts not allowed);
  `play.py diff` capped at 80 rows, all tile maps; dump/diff take no range; preview vs play.py differ after
  settles; gamestable.py writes files outside a scout's scope; the fresh-press door rule cost ~40 calls. Town
  exit of Wyclif not found within budget: no overworld or battle yet.
- Proposed rule change: (1) md.md: no backend friction; H32 switch real; pad-2 codes unusable; (2) backlog:
  diff --range, no cap; (3) lesson: fresh press on door tiles; (4) skill step 7: gamestable.py is run by the
  coordinator; (5) owner: allow ia*.us.archive.org for manual scans.
- Corrected: none; 14/14 checkpoints reproduce (coordinator cachecheck, sheet checked).
- Status: (1) logged in md.md; (2) built 2026-11-20 (second ask); (3) open; (4) logged in skill.md;
  (5) reported to the owner.

### 2026-11-20 - Dungeon Master (Amiga)
- Task: scout Dungeon Master v3.60 (Amiga, first game on the new backend): pointer positioning, controls, Hall of
  Champions map, party of four on level 2, in-game save and RESUME, RAM map, shot plan, lenses started.
- Worked: putting the pointer into a corner and moving by measured offsets (`HOME`/`AT`/`CLICK` macros plus a
  pixel-to-token helper); finding the position bytes with a pattern script over RAM snapshots after `find`
  stalled on noisy buffers; a depth-first explorer driven by the position bytes, which mapped 133 squares and all
  mirrors without hand-walking; reading the save disk's AmigaDOS directory to confirm a save before exporting;
  about 8 route variants in parallel tiled into one sheet.
- Friction: `docs/emulator/amiga.md` was wrong about large mouse moves (cut at about 120 counts per token), which
  cost a calibration round; `sav:` must start a checkpoint's own route, so the chain was rebuilt on a new
  `sd_dungeon` base; most strategy sites refused automated access (dmweb.free.fr, dungeon-master.com, tcrf.net,
  gamefaqs, aminet), so strategy rests on the manual; helper scripts calling `E.play` need `E.expand`; output
  piped through `grep` to a file is block-buffered.
- Proposed rule change: (1) amiga.md, Keys: per-token mouse limit and the corner-plus-offsets recipe; (2)
  amiga.md, Saves: start the chain on a `sav:blank` base for games that save to their own disk; (3) skill step
  3: for first-person games with position bytes, map a level with a depth-first walker before exploring by hand.
- Corrected: coordinator measured the mouse limit on the test disk (up to about 128 counts arrive, the rest of a
  larger step is lost) and changed the backend instead of only the doc: a long move now goes out at 120 counts a
  frame (test in `test_amiga_backend`); the scout's macros use at most 120 per token, so its routes are
  unchanged: a cold rebuild of all 7 checkpoints with the new backend matched its cached frames and position
  bytes; the `resumed` frame shows the four champions on level 2.
- Status: (1) and (2) promoted 2026-11-20 into `docs/emulator/amiga.md` (owner-facing platform doc, not the
  skill); (3) open.

### 2026-11-19 - Wizardry II (Apple II)
- Task: scout Wizardry II (Apple II): boot, Wizardry I transfer through the game's utility, 39 checkpoints to the
  ending, RAM map, warp, saves, shot plan, lenses started, Wizardry III transfer disks.
- Worked: reading the disk's Pascal directory and roster before playing (it showed the used scenario disk); the DOS
  routes as hypotheses run eight at a time in `try.py`; text page reads instead of screenshots; 1x frames for
  hi-res text; `cachecheck.py` extended with a party line and per-checkpoint frames, which exposed a "won"
  checkpoint with four dead that the hashes passed.
- Friction: guardians silently replaced by random groups cost about ten calls before the roster hypothesis (a
  guardian does not appear while any roster character owns its piece; the used disk held four such characters);
  keys lost during the variable camp load (`m,w900`); `play.py` screenshots are 3x and costly to read;
  `cachecheck.py` with names still wipes the whole cache; a second agent's edits in the same tree trigger "file
  modified" notes; full cold checks take about 12 minutes.
- Proposed rule change: (1) skill step 1: for disk games, list the save roster or inventory on the dump before
  playing, since a used disk can change quest behaviour; (2) `docs/emulator/apple2.md`: Apple Pascal Wizardry
  loads vary by 600 frames with earlier disk activity, use `w1500` or `change` after `m`; (3) shared tool:
  `play.py text` and a 1x `look` frame (third request for `screen.py` as a shared tool); (4) cachecheck as a
  shared tool that builds a chain once and writes a contact sheet, with the rule "look at every fight
  checkpoint's party table, not only hashes".
- Corrected: coordinator replayed `@ending` (Gaudeamous screen seen). The extra-disk `sav:` transfer worked as
  designed on first use. Nothing changed in shared files yet: the session was halted by the owner after this
  scout and the Wizardry I capture.
- Status: open ((1)-(4); (1) and (3) now appear in two entries: promote next session)

### 2026-11-19 - Wizardry I (Apple II)
- Task: scout Wizardry I (Apple II): boot, party, 26 checkpoints to the ending, RAM map, warp, veteran party, saves,
  Wizardry II transfer disk, shot plan, lenses started.
- Worked: reading the p-code loop out of memory (interpreter pointer at `0058`) found the write-protect hang in a
  few calls; printing text page 1 as text (`screen.py`, `try.py --text`) replaced most screenshots; the DOS macros
  carried over by address offset alone; the scenario file's own table of contents gave every table offset; twelve
  parallel timing variants found a one-round Werdna win; Malor as the honest way home.
- Friction: no write protection in the backend (the game is unreachable without a poke); the default `iie` model
  shows Pascal text in 80-column mode; `rom/wizardry.zip` is shared by the dos and apple2 slugs and was
  overwritten; the second maze entry loads longer and silently drops keys; `play.py diff` prints only the first 80
  bytes, which are all screen memory on this platform; dump keys are hex strings; `play.py` screenshots are 3x and
  costly to read; background-wait commands are blocked, so long checks need `run_in_background`.
- Proposed rule change: (1) apple2.md: Apple Pascal games need `iiplus`; (2) backend: per-disk write protection,
  then drop the `845A` poke; (3) intake: a dump path per platform when the slug exists on another; (4) apple2.md:
  text page 1 can be read as text, offer `screen.py` as a shared `play.py text`; (5) `play.py diff`: skip
  `0400-07FF` and `2000-3FFF` on the Apple II.
- Corrected: (1), (2), (3) done by the coordinator the same day: model `wpN` (core hook `retro_gamedb_protect`),
  `MENU` without the poke and all checkpoints rebuilt, dumps in `rom/apple2/`, saves in `rom/saves/apple2/`,
  `play.py export` keeps disk-image saves out of the repo. The scout used the poke although the dispatch said to
  stop on a backend gap; it said so plainly, which is what made the fix possible.
- Status: open ((4) and (5) not done)

### 2026-11-19 - Phantasy Star (Master System, US/EU)
- Task: scout Phantasy Star (SMS, first game on the new Master System backend): boot macros, 12 checkpoints, RAM
  map (characters C400, inventory C4C0, meseta C4E0, town position C301/C305, dungeon C30A/C30C), item table,
  save 01_start, shot plan with 28 replayable early shots.
- Worked: parallel route variants tiled into one sheet (try.py); poking eight item ids at a time named all 64
  items in one run; a RAM dump diff around one step found position bytes where `find` did not.
- Friction: (1) SMS savestates dropped cartridge RAM, so an in-game save after `goto` was broken (found only
  when CONTINUE started a new game); (2) most walkthrough/wiki hosts 403 or unresolved, critical path unverified;
  (3) `*N` repeats a single token only.
- Proposed rule change: (a) backend: carry cartridge RAM in states; (b) skill step 3: after `export`, reload the
  save with `sav:NAME` through the game's Continue before reporting it; (c) README tokens: `*N` is one token.
- Corrected: coordinator replayed start, shop, dungeon, battle, continue from an empty cache: as described.
- Status: (a) fixed in the backend + test, note in sms.md; (b) logged (note in sms.md); (c) fixed in the
  emulator guide.

### 2026-11-19 - Ultima III (DOS, GOG)
- Task: scout Ultima III (DOS, GOG): boot, party of four led by ryz, controls, 23 checkpoints to the ending, RAM
  map, warps, saves 01_start/02_endgame, shot plan, three design lenses.
- Worked: load address from a RAM match against EXODUS.BIN (COM image: physical = 0x1A80 + file offset), so
  disassembly offsets equal data offsets; the Other-command, Enter, moongate, shrine, card, rod and Insert code
  gave the quest chain in about an hour; ~40 variants verified in parallel try.py sheets; poking a whirlpool or
  moongate tile under the party fires the game's own transition (clean warps); cachecheck.py carried over.
- Friction: a frigate checkpoint chain failed once on the random wind (seen only on the sheet after later
  checkpoints were built on it); editing `HERO` meant rebuilding everything; `undo` is one level deep; no
  little-endian BCD watch format (`set:...:bcd` writes it); two walkthrough hosts do not resolve.
- Proposed rule change: (1) emulator guide: in checkpoint chains that depend on a random world state (wind,
  moons, a moving whirlpool), poke it to a fixed value in the macro and look at each checkpoint's frame before
  building on it; (2) tools: `"fmt": "bcd-le"` watch.
- Corrected: coordinator replayed `start`, `fight`, `timelord`, `ending` (start beside Lord British's castle,
  orc fight, the Time Lord's card order, Congratulations): all as described.
- Status: (1) logged; (2) open tool wish.

### 2026-11-19 - Ultima II (DOS, GOG)
- Task: scout Ultima II (DOS, GOG): boot, ryz, controls, 29 checkpoints to the ending, RAM map, period warp,
  quest chain, saves 01_start and 02_endgame, shot plan, design lenses.
- Worked: reading the program first (strings, ndisasm of the FCB file calls, offer/transact/loot/door/space code,
  MAPX/MONX/TLK decoded) gave every place, person, quest condition and coordinate without the web; a "patch the
  door's destination for one step, then restore" macro warps to any period; parallel try.py sheets settled the
  variants (commands, shops, Minax with/without the quicksword, field with/without the ring); Ultima I's
  cachecheck carried over.
- Friction: the dispatch said the game starts in 1990 (it starts in 1423 B.C.) and that MAPG were working copies
  (they are planet maps; MAPX/MONX are rewritten); town objects taken for vehicles; attacks never find object 0;
  real-time turns never settle; `play.py export` wrote `@checkpoint` routes (third report); walkthrough hosts
  unreachable.
- Proposed rule change: (1) skill step 1: verify the dispatch's "start" facts on screen before naming
  checkpoints; (2) `play.py export`: write the expanded power-on route; (3) emulator guide: poke monsters into
  an object slot the game's lookups reach (index 0 can be skipped), check with one attack.
- Corrected: coordinator replayed `start`, `lordbritish`, `space`, `minax_dead` (as described); the dispatch's
  1990 start and MAPG guess were the coordinator's errors. (2) fixed by the coordinator (`power_on_route`, check
  in test_dos_pipeline that fails without it).
- Status: (2) fixed 2026-11-19; (1) logged (a dispatch quality issue: the coordinator states guessed facts as
  "to be checked", already in the coordinator skill); (3) logged.

### 2026-11-19 - Ultima I (DOS, GOG, five programs)
- Task: scout Ultima I (DOS, GOG): boot through ULTIMA/GEN/OUT/SPACE/MONDAIN, ryz creation, 22 checkpoints to
  the ending, RAM map, warp, quest structure, saves 01_start and 02_endgame, design lenses, shot plan.
- Worked: the game's strings named every command, place and quest message; ndisasm from string references found
  the quest table, gem and continent rules, princess conditions, shop gating and Mondain's HP; parallel try.py
  sheets for all command letters, monster types and shop counters; the empty-cache vs cache-hit script covers
  frames and written files across program switches (rerun after the play.py rollback fix).
- Friction: the status panel redraws only on in-game changes (poked values invisible until a Q save and `sav:`);
  a poke-spawned shuttle with no fuel/shield killed the player at lift-off (found by diffing INUSE.U1); an
  exported save's README recorded a circular route once its checkpoint was rebuilt from the save; `type:` too
  fast at 500 cycles.
- Proposed rule change: emulator guide: games that draw status values only when they change in play: after
  pokes check the HUD in a frame; if stale, save in the game and start from the save, or poke before a program
  switch. `play.py export`: record the route from power-on, not the checkpoint name.
- Corrected: coordinator replayed `start`, `dungeon`, `space`, `ending` (overworld, Mines of Mt. Drash level 1,
  shuttle lift-off in SPACE.EXE, Mondain's ending text): all as described.
- Status: HUD rule promoted 2026-11-19 into docs/emulator/README.md (second report: Wizardry II capture, HP and
  status pokes shown only after a menu change); export route: open tool wish.

### 2026-11-19 - Wizardry III (DOS, legacy from Wizardry II)
- Task: scout Wizardry III (DOS): Wizardry II transfer and legacy, macros, 22 checkpoints to the ending, RAM
  map and warp, maps, all messages, quest and alignment rules, saves 00-02, shot plan, design start.
- Worked: loader diff against WIZ2.COM with ndisasm (only Save2.Dsk needed); Wizardry II tools reused,
  addresses at Wizardry II + 0xA6; quest conditions tested in parallel try.py runs (alignment x floor x item);
  all 107 compressed messages read by pointing a riddle square at each message number (~1 min); cold vs
  cache-hit compare.
- Friction: item names misread by one (a nameless item is not listed); slow floor loads (1,000+ frames at 315
  cycles) ate keys, so warp routes failed silently; one-way doors missed by the survey's wall rule; walkthrough
  hosts unreachable; the Neutral Crystal step not found (the ending route pokes it).
- Proposed rule change: (1) emulator guide, record tables: count names shown against items poked (nameless
  entries are skipped); (2) skill step 3: for compressed text, point an existing message square at each message
  number before decoding the format; (3) dos.md: loads can exceed 1,000 frames at 315 cycles and drop keys.
- Corrected: coordinator replayed `start`, `guard_good`, `floor6`, `ending` (as described). Lead for the
  Neutral Crystal from a web search (Wizardry Archives PC walkthrough): one non-neutral character holding both
  crystals equips and invokes the crystal of their own alignment; the wrong one turns them to ash; neutral or
  one crystal only: the crystals vanish. The scout's tries did not include that combination: handed to the
  capture. The same walkthrough states the stair rule as party majority; the scout's emulator finding (any
  member of the other alignment is refused) stands until tested.
- Status: (3) promoted 2026-11-19 into dos.md (a fact about the platform at low cycles); (1), (2) logged.

### 2026-11-19 - Wizardry II (DOS, imported party)
- Task: scout Wizardry II (DOS): boot, the Wizardry I import through the game's own Move characters, macros,
  22 checkpoints to the ending, RAM map, floor warp, floor maps, saves 00_transfer/01_start/02_ending, shot
  plan, lenses started.
- Worked: reading the loader with ndisasm first (the import needs only one extra file, Save1.Dsk in the game's
  folder: `tools/transfer.py`); copying the Wizardry I tools and finding addresses at Wizardry I + 0xA6;
  warping by re-pointing the entry staircase at the "Stairs up" prompt; naming all items by poking 8 at a time;
  testing ending variants in parallel (solo/six, equipped/carried, event/poked staff) found the "one alone" rule
  in two runs; cold vs cache-hit comparison exposed the stale disk.
- Friction: the open-handle flush gap broke real routes (roster read back after Tavern changes); one stray key
  made a scratch checkpoint look like a game rule; `play.py checkpoint` writes scratch checkpoints into
  checkpoints.txt; walkthrough hosts outside the network.
- Proposed rule change: (1) dos.md: make the open bug concrete and raise the backend fix; (2) play.py: scratch
  checkpoints kept out of checkpoints.txt; (3) skill step 3: test quest-end variants in parallel before
  decoding code.
- Corrected: coordinator replayed `start`, `guard1`, `sphinx`, `knights` (as described) and fixed the backend
  the same day (5310311, `GamedbMarkWritten` + test that fails without it); `@ending,KNIGHTS,...` from a cached
  `ending` now gives the same frame as the one-segment `knights` route. The game says five KOD pieces, not six:
  the coordinator's dispatch (from Wikipedia) was wrong.
- Status: (1) fixed in the backend instead (dos.md Saves); (2) open tool wish, second occurrence with the MM2
  scout's "checkpoint moves a replaced line" (both: checkpoints.txt handling); (3) promoted 2026-11-19 into
  skill.md step 3 (parallel variants, the same idea as "try every button in parallel").

### 2026-11-19 - Wizardry I (DOS, 1998 loader with disk images)
- Task: scout Wizardry I (DOS): boot, party macros, 16 checkpoints to the ending, RAM map, floor warp, saves
  01_start and 02_ending, floor maps, shot plan, lenses started.
- Worked: ndisasm on the loader (drives, auto-typed disk prompts, save path); matching RAM against the disk image
  for the floor buffer and Pascal records; all ten floors decoded from the disk; warp via the game's own stairs
  record; a cache-hit vs cold compare script (frames + party memory + written disk) for every checkpoint in ~90 s;
  counting the game's disk writes by patching the loader in memory.
- Friction: `cga` loses its palette on a state load (found after building checkpoints; all rebuilt on `ega`);
  DOSBox Pure keeps writes to an open file out of the save ZIP until close (source reading needed); editing
  `WARP`'s wait changed the RNG and broke the Werdna route (recovered with the AMULET poke); keys swallowed by a
  battle starting during a turn; `play.py`'s 2-byte watch showed gold as the low word only.
- Proposed rule change: (1) dos.md Models: cga/tandy palette after a state load, use ega, compare a frame across
  a load; (2) backend: flush files written through open handles, with a test; (3) skill step 3: reusable
  cache-hit/cold compare for DOS (offer `work/scout/wizardry/cmp.py` as `tools/cpcheck.py`).
- Corrected: coordinator replayed `start`, `maze1`, `battle`, `ending` from a fresh process: all as described
  (Castle, wireframe floor 1, 4 Slimes with ryz's options, Congratulations). The loader-holds-SAVE1.DSK-open
  claim not re-derived by the coordinator; written into dos.md as an open bug with the agent's evidence.
- Status: (1) promoted 2026-11-19 into dos.md (a tool fact); (2) open, recorded in dos.md Saves; (3) open (MM2
  and this scout both wrote their own compare: second occurrence of the need, tool not built yet).

### 2026-11-19 - Might and Magic II (DOS, GOG)
- Task: scout Might and Magic II (DOS, GOG): `loadfix` boot, party macros, 8 checkpoints, `01_start`, RAM map,
  area warp, event scan, area-text dump, shot plan, design start.
- Worked: finding the data segment from instruction patterns for the known x/y/facing addresses, then ndisasm for
  the map-change, edge-transition and event-lookup code; the game's own edge transition as a clean warp to all 60
  areas; dumping each area's event buffer after a warp (place names, quest chain, prices without the web); MM1's
  scan approach (Middlegate, Square Lake ~20 s each); the empty-cache vs cache-hit check extended to the disk.
- Friction: the start-menu launch fails without `loadfix` ("Not enough memory for 16 color version") and the
  intake probe cannot show it; the scanner's default landing square was a fixed fight in area 17; one try.py
  result (combat turn order) not reproducible; `play.py checkpoint` moves a replaced line to the end of
  checkpoints.txt; GameFAQs, TCRF, StrategyWiki 403, archive.org download hosts refused (pages work).
- Proposed rule change: (1) dos.md: read the game's own DOSBox autoexec (`loadfix`, `mount`, overlay) and copy
  what matters into `BOOT` via the command line; (2) intake.py: record the `dosbox*.conf` autoexec lines and
  cycles in `game.json` "header" for DOS ZIPs; (3) `play.py checkpoint`: replace a line in place.
- Corrected: coordinator replayed `title`, `start`, `outdoors` and `combat` from a fresh process: all four frames
  as described (title picture, inn door, area C2 outdoors, Witch's Cats encounter options). Disk check (3) of
  the 2026-11-18 entry done by this scout.
- Status: (1) promoted 2026-11-19 into dos.md; (2), (3) open tool wishes. The 2026-11-18 entry's (3) disk check:
  second occurrence, promoted 2026-11-19 (done here, written into dos.md Saves).

### 2026-11-18 - Might and Magic Book One (DOS, first DOS game)
- Task: scout Might and Magic Book One (DOS): playbook, party macros, title/menu/start and four more checkpoints,
  RAM map, move-by-poke, event scan, save export, shot plan, design start.
- Worked: the manual in the ZIP as primary source; RAM dump/diff over a step and a turn gave position and facing
  in one call; searching the dump for a character name gave the party records; reading the event-table addresses
  out of each `.OVR`, then a parallel `emu.py` scan of every event square, mapped all of Sorpigal's services in
  about 20 s; the single-run macro test from power-on; the empty-cache versus cache-hit comparison extended to
  the disk (sign in and look at the roster), which exposed a backend bug.
- Friction: cached checkpoints replaying character creation (about 10 calls to isolate; `start` moved to a `sav:`
  route); TCRF and StrategyWiki 403; no way for the scout to run `shoot.py`; `emu.py` and `play.py` frame sizes
  differ.
- Proposed rule change: (1) backend: replay only up to program launch on a cache hit, with a test; (2) dos.md:
  until fixed, routes that append to a save file must not be the base of checkpoints; (3) skill step 3: for
  games that save to disk, extend the empty-cache check to the disk by saving after a cache hit and comparing;
  (4) dos.md: note the 320x200 `emu.py` frames.
- Corrected: the cause was confirmed in `tools/platforms.py` (the launch log ran to the first save_state, i.e.
  the whole checkpoint route) and fixed the same day; the scout's reproduction now gives the same roster on a
  cache miss and a cache hit. (2) is therefore not needed. The agent wrote "about 25 rolls" for class
  requirements as an inference: marked as such in the playbook, not checked by the coordinator.
- Status: (1) done, (4) done in dos.md; (3) open (first entry asking for a disk check).

### 2026-11-18 - Deep Dungeon III (Famicom, Japanese)
- Task: scout Deep Dungeon III: playbook, naming macros, six checkpoints, RAM, 01_start, 16 floors + town grid
  decoded and drawn, warp, shot plan.
- Worked: RAM diff over turns/steps -> x/y -> map-address routine -> battery-RAM map -> ROM floor data in ~4 calls;
  bank-select jump table on 7003 mapped areas to banks; the cave's stairs handler does a full reload (clean warp);
  parallel emu.py runs tiled to test buttons and all routed shots; Data Crystal text table + small encoder.
- Friction: Start (not A) confirms title menus (~3 calls); keyboard skips blank squares (one name mistyped); dumps
  gone after stop/start (cross-session diff failed); poking PRG had no effect though nes.md said it would; the first
  warp idea failed (area-1 stairs reload only their bank).
- Proposed rule change: nes.md: PRG pokes have no effect; skill: test all buttons in parallel on new screens;
  emulator guide: keyboards may skip blank squares.
- Corrected: PRG claim checked and fixed in nes.md and the Nes docstring; dumps now survive `play.py start`
  (my earlier cleanup removed them); button and keyboard notes added to skill.md step 3. 14/14 verified.
- Status: promoted 2026-11-18

### 2026-11-18 - Might and Magic (NES)
- Task: scout Might and Magic: playbook, macros incl. party, title/start/party/cavern checkpoints, RAM, inn save and
  01_party, 55 maps decoded and drawn, shot plan.
- Worked: Data Crystal RAM map (position, area, map RAM); matching map RAM against the ROM fixed the map order
  (Data Crystal's list is 8 slots off from Castle Doom on); following the pending-area byte through the main loop
  gave a clean warp in ~6 calls; record check byte confirmed on all 16 records before poking; one batch of emu.py
  runs tiled into one image to check all routed shots.
- Friction: lost presses while signs/prompts/keyboard draw (~15 calls), hidden by play.py settles; dump keys are
  hex without prefix (parser written); editing a macro silently changes checkpoints built from it.
- Proposed rule change: emulator guide/skill: test macros as one `do`, pad keyboards; skill: rebuild checkpoints
  after a macro edit; document dump key format.
- Corrected: 16/16 verified by the coordinator; single-`do` macro test promoted into skill.md step 3 (second
  occurrence, see Wizardry II) with the padding and rebuild notes; dump key format in play.py help.
- Status: promoted 2026-11-18

### 2026-11-18 - Wizardry II (NES)
- Task: scout Wizardry: Knight of Diamonds (NES): playbook, party macros, title/castle/start/f2 checkpoints, RAM,
  save handling with a check-value tool, 6 floor maps from ROM, shot plan.
- Worked: porting the sister game's tools with changed addresses; Data Crystal position bytes -> cell fetch ->
  floor table in ~5 calls; searching the ROM for the battery copy of a table found the originals; porting the
  record CRC to Python and checking it on every record before editing a save.
- Friction: peek/poke/dump of MMC3 battery RAM returned open bus and dropped writes (~6 calls); macro waits behave
  differently split across `do` calls (twice landed with the pre-made party); a checkpoint on a stairs square sits
  on the prompt; steps.py copies need a session name per game.
- Proposed rule change: NES peek/poke of 6000-7FFF via the core's save RAM (+ test); nes.md note on disabled RAM
  and record checks; skill step 3: run a ported macro once as a single `do` from power-on.
- Corrected: shared fix in `tools/platforms.py` (direct save-RAM access), regression-checked on Wizardry I and
  Dungeon Magic poke routes; nes.md section added; 10/10 routed shots verified by the coordinator.
- Status: promoted 2026-11-18 (save-RAM access, nes.md); open (single-`do` macro check: first occurrence)

### 2026-11-18 - Wizardry I (NES)
- Task: scout Wizardry (NES): playbook, macros, title/castle/start/battle checkpoints, RAM, maze data, party macro,
  01_party export, shot plan.
- Worked: code early (position bytes -> cell fetch -> ROM maze tables in ~5 calls; joypad dispatch); creation
  macros generated by a script (`tools/party.py --write`); stat-1 poke + Right per row to force a redraw;
  step-and-tile helper in its own `--name` session.
- Friction: `play.py do "@title"` rejected; keyboard shift state persists across names (found after six
  characters); play.py vs emu.py encounters differ (settle steps); no shared RAM dump/diff (third copy);
  almarsguides outside the network.
- Proposed rule change: emulator guide: play.py routes are the reproducible ones; shared `play.py dump/diff`;
  skill step 3: check whether a name keyboard's shift/case persists between names.
- Corrected: coordinator verified 15/15 (the report said 17; shots.txt has 15); `play.py dump/diff` added (third
  occurrence); routes/RNG note in `docs/emulator/README.md`. Keyboard note: first occurrence, logged.
- Status: promoted 2026-11-18 (dump/diff, routes note); logged (keyboard shift)

### 2026-11-18 - Dungeon Magic (NES)
- Task: scout Dungeon Magic: playbook, macros, title/start/field/castle checkpoints, RAM and map-data location,
  inn save export, shot plan.
- Worked: disassembling the joypad handler found the pause-then-icon command scheme in 3 calls after ~8 blind
  tries; RAM dump before/after a step found position and the map at $0600, matched against the ROM to locate the
  stored maps; wall-consistency scan + PNG renderer for an atlas; parallel poke-warps next to doors found the inn
  and shops in one call; the step-and-tile helper.
- Friction: no shared 6502 disassembler or RAM dump/diff; web sources mostly blocked (search snippets and ROM text
  instead); ~10 calls on the pause scheme before going to the code; scout cannot run `shoot.py --verify`.
- Proposed rule change: skill step 3: joypad read before guessing controls; shared `tools/dis6502.py` and `play.py
  dump/diff`; emulator guide: dump the RAM floor block and search the ROM for stored maps.
- Corrected: coordinator verified 12/12 from an empty cache; `tools/dis6502.py` made shared (second occurrence)
  with a test, game copy removed and playbook updated; joypad and map-block hints in `docs/emulator/README.md`.
- Status: promoted 2026-11-18 (disassembler, hints); open (`play.py dump/diff`, scout running shoot.py)

### 2026-11-18 - Megami Tensei II (Famicom, English IPS)
- Task: scout Megami Tensei II: playbook, macros, title/start and later checkpoints, RAM, save handling, shot plan.
- Worked: step-and-tile helper (`work/scout/megami-tensei-2/steps.py`); `emu.py` sheets to time typing text;
  ROM script decoding by relative search (two encodings): save prompts, places, an original story-point list;
  RAM block dumps for HP/MP/stats; `find "new == 20"` after a victory found money; empty-cache vs cache-hit check.
- Friction: `settle` stopped on a typewriter pause, a checkpoint was a page behind (~8 calls); `peek` length is
  decimal; TCRF and the manual host outside the network; `01_start` export impossible before Devil Buster ends.
- Proposed rule change: typewriter note on checking before checkpoint; hex `peek` length or document it; shared
  `play.py steps`; skill step 4: export at the first save point when none exists at start.
- Corrected: coordinator verified 15/15 routed shots from an empty cache. Typewriter/checkpoint and peek notes in
  `docs/emulator/README.md`; step-and-tile helper (second occurrence, see Shin Megami Tensei) and ROM-script
  decoding (second occurrence, see Megami Tensei) promoted into skill.md step 3; export exception in step 4.
  Shared `play.py steps` not built. Network hosts are the owner's environment decision.
- Status: promoted 2026-11-18 (helper, ROM script, export exception); open (`play.py steps`)

### 2026-11-17 - Megami Tensei (Famicom, English BPS patch)
- Task: scout Digital Devil Story: Megami Tensei (Famicom, English patch): playbook, macros, title/start and
  later checkpoints, RAM, password handling, shot plan.
- Worked: one-shot `emu.py` runs with a contact sheet per token to learn menus; decoding the patched ROM's script
  by relative search ("password") replaced the blocked web sources (sage in Micom gives passwords, floor/town/boss
  names); dump-and-diff RAM over four turns found the facing byte; empty-cache rebuild vs cache hit for every
  checkpoint.
- Friction: `play.py find` gave 0 candidates right after `find reset` although `055C` counts steps; `play.py
  checkpoint` writes straight into checkpoints.txt (a scratch checkpoint removed by hand); GameFAQs,
  StrategyWiki, TCRF, gamehacking.org 403, archive.org download host refused; the status window does not redraw
  after a poke, so HP pokes looked as if they failed.
- Proposed rule change: skill.md step 2: when web sources are blocked and the game is a translation, decode the
  ROM script (relative search for a known word) and tag those facts "ROM text"; tools: check `play.py find` on
  NES; `play.py checkpoint --scratch`; proxy: allow archive.org download hosts.
- Corrected: coordinator re-took the 9 routed shots and verified 9/9 from an empty cache. Proxy hosts are the
  owner's environment decision (not changed).
- Status: open (ROM-script decoding: first occurrence; `--scratch` not done). `find` on NES fixed 2026-11-17
  (reset took no snapshot).

### 2026-11-17 - Shin Megami Tensei (Super Famicom, English patches; first SNES game)
- Task: scout Shin Megami Tensei (Super Famicom, English patch), the first SNES game: playbook, macros,
  title/start checkpoints, RAM map, save, shot plan.
- Worked: a small step-and-tile helper (several token groups, one tiled image) cut the look-at-every-frame cost;
  fixed `a,w150` per text page made the naming route replayable; `find "new == 10000"` right after the allowance
  found the money address in one call; rebuilding every checkpoint with an empty cache and comparing with a
  cache hit.
- Friction: about 30 minutes on the opening (presses during typing text counted unreliably, two macro attempts
  typed wrong names); macros could not be repeated with `*N`; 8-frame Up/Down skips rows in this game; SNES
  emulation about half the NES speed and the opening is 20,000 frames; TCRF, GameFAQs and StrategyWiki 403 and
  the only code list is on a host that is not allowed (no walkthrough, debug or save source); the write list
  excludes `work/shots/`, so planned routes could not go through `shoot.py`.
- Proposed rule change: emulator guide: typewriter text needs one press per page with a fixed wait; support
  `MACRO*N` or document that it is not supported; skill.md step 3: test Up/Down with a 4-frame hold if a default
  press skips a row; let the scout run `shoot.py` into `work/scout/<slug>/`.
- Corrected: `MACRO*N` added to `tools/emu.py` (test); typewriter-text and short-hold notes added to
  `docs/emulator/README.md`. No late-game checkpoint: flags and position not found (left to the capture run).
- Status: promoted 2026-11-17 (empty-cache check and `games/<slug>/tools/` in the write list: second
  occurrence, see the Dragon Quest entry); open (scout running `shoot.py`)

### 2026-11-17 - Dragon Quest (Famicom, English patch; first NES game)
- Task: scout Dragon Quest (Famicom, English patch), the first NES game: playbook, macros, title/start/late
  checkpoints, password handling, RAM map, shot plan.
- Worked: making a late-game "save" by poking the state and asking the king for a password; an inverse IPS as a
  `rom:jp` variant to compare the kana and translated password grids; position poke plus one step as a warp;
  rebuilding every checkpoint with an empty cache and comparing against cache hits, which exposed a frame bug.
- Friction: cache hit versus build differed by one frame on NES (`lrcore.Core.image()` ran a frame when none was
  drawn); `status` PC is useless for this game (always the frame-wait loop); TCRF and StrategyWiki 403; the
  skill's write list has no `tools/` folder although pokemon-blue has one; reading a password off a screenshot
  is error-prone (icons are symbols).
- Proposed rule change: fix `lrcore.Core.image()` so a screenshot never advances emulation, with a test; in
  skill.md step 3 add "rebuild the checkpoints once with an empty cache and compare with a cache hit"; allow
  `games/<slug>/tools/` in the guardrails; for password games "make passwords by poking the state and asking
  the game for one".
- Corrected: backend fixed the same day (screenshots never emulate; savestates carry the frame; test
  `test_nes_state_keeps_frame_and_timing`); all nine checkpoints rebuilt and checked by the coordinator.
  Password-by-poke and the PC note went into `gamedb/docs/emulator.md`.
- Status: open (skill.md changes: empty-cache check, `tools/` in the write list; first occurrence)

### 2026-11-15 - Pokémon Blue (first game through the pipeline)
- Task: scout Pokémon Blue: playbook, macros, title/start/late checkpoints, RAM recipes (late game, warp),
  saves for the owner.
- Worked: pret/pokered disassembly via curl to raw.githubusercontent.com + base stats read from the ROM ->
  generator script for realistic party pokes, right first time; warping by rewriting a door's warp entry;
  in-game save + `play.py export --state`, checked with `sav:` + CONTINUE.
- Friction: `undo` one level only (an over-long mash typed into the naming keyboard); settle accepts all-white
  fade frames; RAM watches could not show BCD money; `--model sgb` hangs on SGB transfer garbage; snap routes
  using a macro break silently when the macro changes later; WebFetch fails, TCRF/GameFAQs 403.
- Proposed rule change: docs/emulator.md: never mash into a name prompt; settle should refuse/warn on blank
  frames; a bcd type for RAM watches.
- Corrected: coordinator replayed @late without cache, the party screen, both exported saves via
  `sav:NAME,TITLE,CONTINUE` (trainer card ryz / 48215 / 27:47 / 8 badges; bedroom for 01): all as reported.
  Added `"fmt": "bcd"` watches (money watch for pokemon-blue) and the mash and blank-frame rules to
  docs/emulator.md. Settle itself left unchanged (recorded routes depend on it). SGB hang and macro-change
  breakage go to docs/status.md Next.
- Status: promoted 2026-11-15 (mash rule, blank-frame note, bcd watch); sgb and macro versioning open
