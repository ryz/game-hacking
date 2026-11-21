# Progress log - game database

Append-only, newest first.

## 2026-11-21 - Aspect rule for flattened frames; Beyond Zork row-doubled, monochrome shot
- Owner: Beyond Zork's 640x200 frames looked 3.2:1. Rule (owner, 2026-11-21): decided per game in `game.json`
  "aspect" (`rowdouble` = each row twice, 640x400, lossless; `native` = as drawn). Tools: `platforms.Libretro.shaped()`
  applies it to every frame (play, preview, shoot, cachecheck); undecided flattened frames (width >= 3 x height)
  warn and `shoot.py --publish` refuses (exit 5); test added. No other published set has such frames.
- Beyond Zork: `aspect: rowdouble`; both sets republished at 640x400 and re-verified from an empty cache (start
  34/34, main 88/88). New shot `options_monochrome` (N at "Do you want color?"); palettes 1 and 2 checked: same
  as the default blue on this EGA.

## 2026-11-21 - Beyond Zork (DOS): first text adventure, scouted and captured
- Owner uploaded `beyond_zork.zip` (SHA-1 `498c08e5...`): story file Z-machine v5 release 57 / 871221 with
  Infocom's own `Bzork.exe` and DOS Frotz 2.32 (the bundle's `.bat`). Registered as `dos/beyond-zork`, region na.
- Scout: `Bzork.exe` chosen (original look, 640x200 16-colour graphics, so no `play.py text`); start deterministic
  from power-on, the moors randomised by the typed route; 11 honest checkpoints to the first save; Z-machine base
  0CDB0, attributes 1454A. Coordinator: 11/11 cold.
- Capture: `start` 34 (honest, power-on to SAVE) and `main` 87 (setup screens, options and palettes, village,
  cellar deaths, moors fights, Mizniaport shop, Frotz comparison); lenses; `ATTRS`/`MONEY` pokes in `main` only.
  Coordinator: 34/34 and 87/87 from an empty cache.
- Rules: game-capture leaves `gamestable.py` to the coordinator (promoted); dos.md: commas in `type:`, Z-machine
  memory layout. Backlog: text reading for graphics-mode text games, a settle that ignores a blinking cursor.
- Open: level 2, a magic item with a visible effect, the cellar solution, Skyway, Gurth City, Fields of Frotzen;
  walkthrough hosts are blocked by the network.

## 2026-11-21 - The Bard's Tale (Apple II) registered, scouted and captured
- Owner's upload (four disks, cracked release; the character disk holds a played roster). Scout: 16
  checkpoints, city warp, records, dungeon walls and flags. Capture: `start` 45 (honest), `main` 132 to Mangar
  and the ending (final fight by poke, captioned), lenses, a decoded map of all 16 dungeon levels in
  `design/maps/` (the game has no automap). Verified cold by the coordinator (45/45, 132/132).
- Tools: `dis6502.py --route` disassembles live memory at a checkpoint (asked twice); docs: archive.org
  downloads blocked, one-time square flags.
- Open: an honest won fight, bard song effects, riddle answers, what disk 4 holds; Apple II hi-res text reader
  (backlog, asked twice).

## 2026-11-20 - Might and Magic II (DOS): new rules applied, set `start`
- Owner re-uploaded the GOG ZIP (SHA-1 matches). `main` re-verified with the new tools from an empty cache:
  228/228, 213 s with 4 processes.
- New set `start` (game-capture, ccbd75e): 52 shots played honestly from power-on to the first inn sign-in, no
  pokes or warps. Found: the new party has 0 gold (shops browse only), the (8,1) cats fight is walled in, no
  encounters in Middlegate; the first one on foot (ten Orcs at C2 (2,5)) beats the level-1 party, so the set shows
  the defeat and the return to the inn. Wall map at 161D6 decoded (playbook). Coordinator re-verified from an
  empty cache: 52/52.
- Open: a won fight and a purchase in `start` (needs a stronger honest route, e.g. resting/training first or a
  different first fight), plus the older open items in `game.json`.

## 2026-11-20 - Wizardry II (Apple II) captured; Might and Magic II (Apple II) registered and scouted
- Owner re-uploaded the Wizardry I and II disks (same disk SHA-1s). `emu.py` check_rom accepts a re-packed ZIP
  of disk images when every disk matches `game.json` "header" "disks" by name and SHA-1 (16748be). Wizardry I
  02_ending, Wizardry II 00_transfer, 01_start and 02_ending rebuilt byte-identical from their routes.
- Wizardry II: `start` 35 and `main` 229 shots, lenses, verified cold by the coordinator (35/35, 229/229).
- Might and Magic II (Apple II, six nibble disks): registered (9759bd4), scouted: 16 checkpoints (16/16 cold),
  warp to all 60 areas, record layout, poked parties, save 01_start, 47 previewed shot lines.
- Might and Magic II (Apple II) captured: `start` 45 (honest), `main` 216 (to Sheltem, year 800 via the century
  byte `2F7C9`), lenses; verified cold by the coordinator (45/45, 216/216).
- Owner asked for a filled map or automap of Might and Magic II (Apple II): main 216 -> 220 (automap walked,
  three areas filled by poking the visited bits). Apple II find/dump/diff now cover aux RAM and the language card.
- Open: Wizardry II R)un/Q)uick/S)tatus, floor 6 fixed fights; Might and Magic II (Apple II) Sheltem fight not
  won (no ending), Earth/Water planes, Unlock/Use, hirelings.

## 2026-11-20 - Sword of Vermilion: town talk and encounters with the map
- Owner's examples: a talk shot with the hero and speaker side by side mid-screen (Stow during the monster raid,
  found via the line table; flag FFC75C) and overworld encounters with the area map in the panel. `main`
  113 -> 136: talk in 7 towns, 7 town views, the full Aries list, 4 encounters with the map. NPC table, collision
  grid and a per-game talk planner (`games/md/sword-of-vermilion/tools/npcs.py`). Re-verified: 136/136.
- Open: Malaga talk (people under the text box), Watling, Barrow, Tadcaster, Swaffham, Hastings.

## 2026-11-20 - Sword of Vermilion: bosses and ending
- Found through the code with `tools/dis68k.py`: main state word `FFC400` (0x12 = ending; set in play after the
  Sixteen Rings are used at the right place, `FFC77E`), bosses requested by `FFC8NN=FF` + `FFC817=FF` (14 bosses,
  setup 0x2A92, boss HP `FFD108`). `main` 96 -> 113 (7 bosses, the first one's intro, strike, defeat and reward,
  ending pages and staff roll), new sets `seq-boss` 14 and `seq-ending` 12. Re-verified from an empty cache.
- Tools: `dis68k.py --xref` takes `C400` as `FFC400`; scene-finding recipe in `docs/emulator/md.md`.
- Open: where each boss is met in play, the ring quest on foot, Watling, message speed.

## 2026-11-20 - 68000 disassembler
- Owner: install capstone. `tools/dis68k.py SLUG ADDR [N]` disassembles Mega Drive code; `--xref ADDR` lists
  every instruction naming a variable (absolute-short `$c818.w` included), with `game.json` watch names as
  comments. `setup_emu.sh md` installs capstone; test added. Unblocks Sword of Vermilion's boss and ending triggers.

## 2026-11-20 - Sword of Vermilion: area maps and presentations
- Owner's request: more presentations (travel and so on) and the full map in the overworld panel. The panel shows
  the whole 16x16 area map once the area's map is owned: flags `FFC820 + y*16 + x` (FF = owned), set by NPC map
  gifts (Wyclif's well man: five maps to Parma), by the Mirror of Atlas (all maps) or for the moment by
  Titania's Mirror. `main` 65 -> 96 shots (maps of four areas and two caves, mirrors, intro and prologue frames,
  Aries arrival, Griffin Wing, battle start, Ring of Wisdom keeper, six more enemy groups); new set `seq-aries`
  (7, cast to arrival in Wyclif). Re-verified from an empty cache: 96/96, 7/7.
- Tools: `preview.py --out PATH` and `--peek ADDR:0xNN` fixed. Backlog: a 68000 disassembler.
- Open: first boss and ending triggers (need the disassembler), the NPC with the cave map.

## 2026-11-20 - Sword of Vermilion: first Mega Drive game, scouted and captured
- Owner uploaded the North American Genesis dump (SHA-1 `c18fc75e...`, header GM 00005502-00); registered as
  `md/sword-of-vermilion`, region na, model ntsc. First real game on the md backend (Genesis Plus GX): no
  friction with buttons, battery RAM, `export`/`sav:`, peek/poke or timing; H32 (256-wide) name keyboard.
- Scout (2 rounds): 23 checkpoints to the first battle; the Wyclif gate opens only after Blade's speech.
  Capture: `main` 65 and `start` 35 shots, both re-verified from an empty cache by the coordinator; lenses;
  45 checkpoints to Parma and two caves.
- Tools: `play.py diff --range LO-HI --max N` (second ask). Checked: a state loaded mid-battle differs from a
  flat replay only in a dead stack word (`docs/emulator/md.md`). Promoted: routes copied from `play.py` need
  `settle` where calls were split (`docs/emulator/README.md`). Backlog: `cachecheck --show-diff`,
  `preview --repeat`.
- Open: first boss, rings, later towns, Area Map, message-speed option; research hosts mostly blocked
  (GameFAQs, tcrf, StrategyWiki 403; archive.org file hosts not allowed: manual scans unreachable).

## 2026-11-20 - Shin Megami Tensei (SNES) re-verified with the new tools
- The owner uploaded `smte1.ips` and `smte2.ips` (SHA-1s as in `game.json` "source"); `tools/mkrom.py` rebuilt
  the patched ROM with the expected SHA-1. `shoot.py snes/shin-megami-tensei main --verify --published` from an
  empty cache: 56/56 identical to the committed pictures. 428 s with 4 processes; 41 of 45 checkpoints built.
  The chain is one line 37 links deep, so one process builds it and the others wait: here the gain is from
  building each link once, not from parallel replays. No cold figure from the old tools exists for this set.
- Seen in the set (older than the tool changes, not changed): two captions over 80 characters,
  `police_roadblock` (87) and `automap` (90).
- Still to verify: `apple2/wizardry`, `amiga/dungeon-master`, `nes/megami-tensei-2`.

## 2026-11-20 - Wizardry III (DOS) re-verified with the new tools
- First published set checked after the process review: the owner uploaded the dump (SHA-1 as in `game.json`).
  `shoot.py dos/wizardry-3 main --verify --published` from an empty cache: 228/228 identical to the committed
  pictures, which the old tools made. 64 s with 4 processes, 201 s with one; the capture run of 2026-11-19
  reported about 15 minutes for a full verify. 41 of the 56 checkpoints were built (chain depth 34, 25 routes
  on `sav:00_transfer`), 92 MB of states.
- New: `shoot.py --verify --published` compares with the committed set instead of the working set (a new
  container has none) and writes nothing into it; test added.
- Seen: the DOS core writes about 16 log lines per shot to stderr (`docs/backlog.md`).
- Open: the other sets named in `docs/status.md`. Shin Megami Tensei: the base dump uploaded in this session
  matches `game.json` "source" (`f765341b...`), but the IPS that came with it (`Shin_Megami_Tensei_if_SNES_J.ips`,
  SHA-1 `3963452b...`) is neither `smte1.ips` nor `smte2.ips`, the two patches the set was made with; the set
  cannot be rebuilt or verified until those two are uploaded.

## 2026-11-20 - Process review: faster verify, shared previewer, native pictures, shorter reading, generated tables
Owner's request: analyse the repository and its feedback for what costs time and tokens, then implement it.
- **Findings** (from 31 capture and 22 scout feedback entries): interactive play with a 3x picture per
  step was the main cost (250-376 calls per run); a cold verify rebuilt every checkpoint from power-on in one
  process (15-35 minutes, run by the agent and again by the coordinator); `try.py` was copied into ten game
  folders, `cachecheck.py` into five, while the shared previewer stayed a wish through six runs; an agent read
  about 30,000 tokens before its first command (`AGENTS.md`, guides, a 48 KB feedback log); one run was filed
  in five or six files and the game table existed in three versions.
- **Tools** (`5f90131`): `emu.py` builds a checkpoint from the state of the one it starts from and caches every
  link, under a lock; `shoot.py --jobs N` (default 4) for shooting and `--verify`, index and sheets written
  once per batch, `pixel_sha1` per shot, identical pictures reported by `--only`, the set's own `shots.txt`
  gives the order, a set without a working list falls back to its published list; `play.py`: native pictures
  (`shot --scale N`, `game.json` "look_scale" on demand), `call=N` in the status line, `snap` names a shot
  with the same picture, `goto` picks up edited macros, `text` reads the Apple II text page; new
  `tools/preview.py` (plan files or routes in parallel on one sheet, played as `shoot.py` plays them; `?`
  marks, `--timeline`, `--text`, `--peek`, `--set`), `tools/cachecheck.py` (flat replay vs chained build vs
  cache hit vs the existing cache: frame, memory, save data; sheet of all checkpoints), `tools/x3.py`.
  Measured on a synthetic Apple II chain of 20 checkpoints with 40 shots, empty cache: 508 s with the tools of
  `26ad47e`, 61 s now; the deepest shot is byte-identical. 59 tests (was 54), the new ones on the Apple II
  test disk because its picture records the exact timing of a route.
- **Owner's decision: no 3x pictures by default** (`4f1018f`): 3,595 enlarged files (94 of 177 MB of shots)
  removed from the database sets, `index.json` without `file_3x`, `index.md` linking the native files, the
  sets' `3x/` folders ignored by git; enlarged copies on demand with `tools/x3.py`. Wizardry Empire's compare
  images (its own tools) are unchanged.
- **Helpers** (`ab83987`): ten `try.py`, five `cachecheck.py` and two `screen.py` removed from game folders; the
  eleven playbooks that name them say at their top what replaces them.
- **Skills and guides:** capture works in batches by default (plan file, `preview.py` sheet, `shoot.py --only`),
  `play.py` for exploring; budgets in tool calls; milestone commits stated as part of the task; the push recipe
  without `pull --rebase`; scouts check tables on the second and last record and run `cachecheck.py`;
  playbooks get a "Read first" block (template; existing playbooks at their next run).
- **Reading load:** `skills/<name>/feedback.md` is now the short list of open lessons, the full history moved to
  `feedback-log.md` (nothing deleted); tool wishes are one list, `docs/backlog.md`, with the rule that a second
  request is built or dropped; `AGENTS.md` lost the game table and the Wizardry Empire reference (now
  `games/gbc/wizardry-empire/AGENTS.md`, loaded through its own `CLAUDE.md`): 19.7 KB -> 11.6 KB. A capture
  agent's fixed reading went from about 120 KB to 71 KB (before the playbook).
- **Bookkeeping:** each game's `game.json` holds "edition", "work" and "open"; `tools/gamestable.py` writes the
  tables in `README.md` (it listed 3 of 27 games) and `docs/status.md` from them. `docs/status.md` is a snapshot
  again (platforms, tools, generated game table, next); its accumulated text is kept unchanged in
  `docs/archive/status-2026-11-20.md`.
- **Not done:** no published set was re-verified with the new tools (no dumps in this container): first session
  with a dump runs `shoot.py SLUG main --verify` from an empty cache. The per-game `maps.py` / `roster.py` /
  `transfer.py` were not merged into shared modules (untestable without the dumps; `docs/backlog.md`). Existing
  playbooks have no "Read first" block yet. Wizardry Empire's own tools still write their 3x compare images.
## 2026-11-20 - Mega Drive / Genesis backend
- New platform `md` on the Master System's core (Genesis Plus GX, same pinned commit and build;
  `setup_emu.sh md` is an alias of `sms`). `tools/gpgx-debug.patch` gains `retro_gamedb_peek68k`/`poke68k`/`pc68k`:
  side-effect-free reads of work RAM, ROM, Z80 RAM and mapped cartridge RAM (I/O, VDP and open bus are refused,
  since reading them changes the hardware), writes to RAM only.
- `platforms.MegaDrive` (subclass of `Sms`): header identification (titles, product code, I/O field and
  six-button pad, old/new region field, `RA` backup RAM, checksum), models ntsc/ntsc-j/pal, fixed core options
  (Mega Drive hardware whatever the extension, no TMSS, no add-on or lock-on), the 64 KiB cartridge RAM buffer
  appended to savestates and exported as `.sav`, Pro Action Replay and Game Genie as the core decodes them.
- 68000 values are big-endian: RAM watches and `set:` now default to the backend's byte order (`ENDIAN`,
  little-endian everywhere else, so other platforms are unchanged); `find --wide` compares big-endian words.
- Tests: `tests/make_md_rom.py` builds an original test ROM (hand-assembled 68000, V-blank loop, pad read,
  cartridge RAM); 3 tests (header and cheats, backend, intake-to-shoot pipeline). Docs: `docs/emulator/md.md`.

## 2026-11-20 - rule: `start` sets in play order
- Owner's rule: `start` set ids are numbered in play order (`01_<step>` ...) and listed in that order, so the
  set reads as one playthrough. In `docs/capture-guide.md` ("Sets") and the game-capture skill. Dungeon Master's
  set already follows it; Apple II Wizardry's (unnumbered, partly out of order) does not yet.
- Follow-up the same day: in `start` sets the step number goes before the category in the file name
  (`<game>_<platform>_<region>_<NN>_<area>_<step>.start.png`), so a folder listing is the play order.
  `tools/shoot.py`: `stem()` builds it and refuses unnumbered `start` ids; `list_order()` sorts a set by its own
  `shots.txt` (before: the game's main list, which put Apple II Wizardry's `start` index out of order). Both
  `start` sets renamed without replaying (no ROMs here): Dungeon Master (37), Apple II Wizardry (47, ids
  numbered `01_` to `47_` in the order of its shot list); index.md and contact sheets rebuilt.

## 2026-11-20 - Dungeon Master (Amiga) captured to the ending
- game-capture run: set `main` 111 shots (boot, Hall of Champions and five mirror panels, level 2 systems,
  inventories, statistics, spells and fireball, level-up, food and water, pit, fountain, champion death, 22
  creature kinds over 24 battle shots, red dragon, Lord Chaos, game over, the save flow, plain views of levels 3
  to 14, the ending with Lord Order, the fusion and the Grey Lord) and set `start` 37 shots played honestly from
  power-on to the first in-game save (first fight: the Mummy behind the east gate of level 2). Both verified from
  an empty cache by the agent; the coordinator re-verified the ending shot and the last `start` shot cold.
- Core: two leftover debug printfs in the PUAE core's VFS (a line on stdout per file open) removed.
- How: the whole dungeon is in slow RAM (map descriptors, squares, thing tables; `tools/dungeon.py` writes
  `design/maps.md`); level warp = poke onto a down staircase and turn (`DL3`..`DL14`, checkpoints `l3`..`l14`);
  the ending by `FUSE`: the club made the complete Firestaff, the party poked next to Lord Chaos and his open
  neighbouring squares turned to walls in the same frame as the click. Finding: poking the facing byte with
  champions in the party leaves their formation cells unrotated (fighters miss); move with position pokes and
  the game's own turns (`GO`).
- Open: a teleporter, pressure plate, chest, scroll, Swamp Slime, Giant Scorpion, Black Flame, Gando's mirror,
  KICK/WAR CRY/CALM/INVOKE/FLUXCAGE in use, the altar of rebirth.

## 2026-11-20 - Dungeon Master (Amiga) scouted; Amiga mouse moves fixed
- game-scout run: playbook, pointer macros `HOME`/`AT`/`CLICK` with `tools/at.py` (pointer pushed into a corner,
  then measured offsets; 2 counts = 1 pixel), Hall of Champions mapped by a walker on the position bytes (23 of
  24 mirrors), party ryz (Halk reincarnated), Tiggy, Wuuf, Stamm; the game formats a blank disk itself
  (`sav:blank`), save and RESUME verified, export `01_level2`; RAM: position `C167CF`-`C167D4`, champion records
  from `C18538` (0x140 apart); 57-line shot plan, lenses started. Checkpoints `sd_dungeon`, `party`, `level2`,
  `saved`, `resumed`; all 7 rebuilt cold match.
- Backend: one `mouse:` step above about 128 counts lost the rest (the machine takes about 120 a frame); long
  moves now go out at 120 counts a frame. Moves up to 120 are unchanged, so the scout's routes are too (checked
  by the cold rebuild). `docs/emulator/amiga.md` corrected, plus the corner recipe and the `sav:blank` base.
- Open: capture, level warp, Gando, the eye panel; the strategy sites (dmweb.free.fr, dungeon-master.com,
  tcrf.net, aminet) refuse automated access from here.

## 2026-11-20 - Amiga: Kickstarts, Dungeon Master registered and played into the dungeon
- Owner supplied Kickstart 1.3 (`kick34005.A500`) and 3.1 (`kick40068.A1200`); both match the SHA-1s in
  `Amiga.KICKSTARTS`, copied to `rom/kickstart/` (uncommitted). The test disk boots on A500, A500OG and A1200 with
  them; fire, keys and a disk write through trackdisk.device work on all three.
- Dungeon Master v3.60 (owner's ZIP, one cracked ADF) registered as `games/amiga/dungeon-master/` (region eu,
  model A500). Route: crack intro (left click), 80 s of loading on the logo, entrance doors, ENTER, 90 s of
  loading, dungeon view; keypad 8 steps forward. Checkpoints `entrance` and `dungeon`; a cold rebuild from
  power-on matches the checkpoint. The first attempt looked stuck on the logo: it was only loading at real floppy
  speed (noted in `docs/emulator/amiga.md`, "Loading takes real time").
- Core fix found on the way: the restore was deferred to the next frame, so right after a state load `peek`,
  `find` and `status` read the old machine. `retro_unserialize` now restores at once and returns before the CPU
  runs (`gamedb_restore_only` in `newcpu.c`); test `test_amiga_same_route_same_frames` checks memory and PC
  right after the load. Amiga tests: 6 passed.
- Open: a save disk (the game saves to a disk named `DungeonSave`; none in the owner's ZIP), scout and capture.

## 2026-11-20 - Amiga emulator set up (PUAE libretro core)
- Owner's request: an Amiga emulator. PUAE (libretro-uae) at commit d366f77, built by `sh tools/setup_emu.sh
  amiga` (90 s, no extra packages), backend `Amiga` in `tools/platforms.py`, platform folder `games/amiga/`.
- `tools/puae-debug.patch`, each change for something found while setting it up: the core crashed in
  `retro_init` without a frontend log interface (its fallback logger writes to `stderr`, which its VFS build
  defines as 0); a loaded state ran one frame ahead of the run that saved it (the core emulated frames inside
  `retro_unserialize` until the restore at the next vsync was done; now it restores at the start of the next
  frame); the battery clock read the host's time; a state names its disks by full path, and each machine has
  its own temporary folder (a restore now takes them from `retro_gamedb_disk_dir`). Added peek/poke/pc, disk
  insert/eject and a flush of buffered disk writes.
- Found by testing, not in the patch: the RetroPad has to be plugged into port 0 for the joystick to reach
  Amiga port 2; the core's default hotkeys (F12 status bar, right Ctrl mouse toggle, RetroPad X = space) are
  switched off; 24-bit colour, so the 12-bit palette comes out exact.
- Kickstart: real ROMs are looked up in `rom/kickstart/` by PUAE's names, Amiga Forever names or SHA-1; the
  core's built-in AROS Kickstart (`-aros`) boots bootblocks on the A1200 presets only, so the tests use
  `A1200-aros` and real A500 games need the owner's Kickstart 1.3.
- Test disk `tests/make_amiga_adf.py`: a hand-assembled bootblock that shows fire, mouse button, raw key code and
  a frame counter as the background colour, stores the counter and the mouse counters in chip RAM and can write
  a sector through trackdisk.device. Tests `test_amiga_*` (6): identify, Kickstart lookup, backend, same route
  same frames (fresh and busy loads, re-save without a frame), disks (swap, drives, writes in states, export,
  `sav:`), intake-play-shoot pipeline. Full suite: 29 passed, 25 skipped (other cores not built here).
- Not done: no real game registered; untested with a real game: everything, in particular the reset keys,
  NTSC games, AGA games, multi-disk swaps in a real game. Not supported: `.ipf`, hard disk/WHDLoad, CD32/CDTV,
  write-protected disks.

## 2026-11-19 - Capture guide: standard environment shots and the `start` set; Wizardry I (Apple II) has both
- Owner's request: a few regular dungeon screenshots for Wizardry I, and as general rules a few standard
  environment shots with nothing special happening, and a set `start` for the early game (ending after the
  save). Both rules are in `docs/capture-guide.md` (Must-have list, Sets) and step 6 of the capture skill.
- Wizardry I `main`: +13 plain maze views over floors 1-10 (`env_...`), picked from 60 sampled squares; 304
  shots. Four sampled views were pixel-identical to other shots (the wireframe repeats: same wall arrangement,
  same picture on any floor) and were replaced. Lens check clean.
- Wizardry I `start`: 47 shots in play order, power-on to L)eave the game, played with the level 1 party and no
  pokes: creation, tavern, Boltac's with the 101 starting gold (long sword, leather armor), camp and equip,
  the walk from the stairs to the first room, a real first fight (five Orcs surprise the party, three flee, 39
  experience each), the thief inspects and opens the chest (6 gold a share), the walk back, the inn (healing,
  1011 experience to the next level), save. New checkpoints `s_shopped` to `s_home`. Verified 49/49 from an
  empty cache before two duplicate pictures were dropped.
- Not done: the other games have neither the plain views nor a `start` set yet.

## 2026-11-19 - Wizardry I-V registered on the Apple II; I scouted and captured, II scouted; queue halted
- Owner uploaded the five games and asked for them in order, then halted the queue after the Wizardry I capture
  and the Wizardry II scout. Disk sets: I boot + scenario, II and III two disks, IV six, V nine sides (side E
  from the archive's "fixed" copy; the other E, the word list and the documentation disks are in
  `rom/docs/wizardry-5/`, uncommitted). All five boot to their titles.
- Backend, each change for something a game needed: extra disks through a `sav:` ZIP (Wizardry II takes its party
  from a Wizardry I disk; worked on first use); write protection (`wpN` in the model, core hook
  `retro_gamedb_protect`: Wizardry's boot disk writes to itself and hangs unless refused; the scout had poked
  around it); per-platform dump and save paths (the Apple II dump had overwritten `rom/wizardry.zip` of the DOS
  game); `play.py export` writes disk-image saves to `rom/saves/apple2/<slug>/`. Tests: write protect, extra
  disk. Apple Pascal needs model `iiplus` (80-column text on a //e).
- Wizardry I: scout (26 checkpoints to the ending, real Werdna win, RAM map, warp, tools) and capture (291 shots,
  cold verify 298/298 before seven identical pictures were dropped, coordinator re-verify of the 291, lenses
  clean). The boot change to real write protection shifted every fight: the scout re-timed the chain; the
  Werdna win holds at one input timing out of about 47.
- Wizardry II: scout (39 checkpoints to the ending, transfer through the game's utility, guardians, RAM map,
  transfer disks for III). Its disk 2 is a used disk whose four characters own four armor pieces; a guardian
  does not appear while any roster character owns its piece, so the routes delete them. Two guardians and the
  carrying of the five pieces are by poke.
- Agents ran in parallel in one working tree (capture I, scout II) with path-limited commits: no collision.
- Not done: Wizardry II capture; III-V scout and capture; the agents' tool requests (status.md).

## 2026-11-19 - Phantasy Star (Master System): corridor battles and looping movement clips
- Owner's requests: battles in front of long corridors, and dungeon movement that loops smoothly.
- battles set 16 (corridor_vampire/nessie/ghoul/skeleton): forced FIGHT always uses the field backdrop, so these
  are real encounters after a warp to the start of a 13-square corridor.
- New set `loops` (4 GIFs: walking in a blue and a red corridor, endless turning at a blue and a yellow
  crossroads), made by `games/sms/phantasy-star/tools/loop.py`, which keeps the first exactly repeating cycle;
  a re-run gives byte-identical files.

## 2026-11-19 - Phantasy Star (Master System) capture part 2 (main 109, battles 12, four sequences)
- game-capture (32802e3): rest of the game up to Lassic's castle, talk solved (step toward the person, push
  again), C202 state warps, FIGHT/PARTY/DUN macros, ROM tables decoded; ending not reached.
- Coordinator: all six sets 141/141 from an empty cache, lenses clean, sheets looked at; the battles set leans on
  forced encounters on one field background. Merged to `master`.

## 2026-11-19 - Phantasy Star (Master System) scouted, early game captured (53 shots)
- game-scout (a7271a5): playbook, 12 checkpoints, RAM map, item table, save 01_start; found that SMS savestates
  dropped cartridge RAM, fixed in the backend with a test (7bff75b).
- game-capture (75ae7b7): 53 shots from the title to the first cave and game over, three lenses (early game),
  floor map at CB00, 4 more checkpoints. Coordinator: cold `--verify` 53/53, sheet looked at. Merged to `master`.

## 2026-11-19 - Phantasy Star (Master System) registered
- `intake.py --slug phantasy-star --region na` (SHA-1 257ca76e..., 512 KiB, header Export, product 9500,
  version 2, checksum ok, model ntsc). Boot probe: title from frame ~120; `b1` on the title starts the intro.
  Next: game-scout.

## 2026-11-19 - Master System backend (Genesis Plus GX)
- New platform `sms`: `Sms` backend in `tools/platforms.py` on the Genesis Plus GX libretro core (pinned
  b9c2316, `tools/gpgx-debug.patch`: Z80-space peek/poke, PC, whole cartridge RAM, info log silenced), built by
  `sh tools/setup_emu.sh sms`. Chosen over SMS Plus GX / Gearsystem / PicoDrive for accuracy and because the same
  core covers Game Gear, SG-1000 and Mega Drive later.
- `Libretro._bind` split out of `_open` so a core with other debug symbol names reuses the shared driver; NES
  and SNES unchanged (their tests re-run).
- Tests: header/cheats, backend (picture, buttons, Pause NMI, RAM, state round trip, two cores at once, ntsc-j
  RAM, `.sav` load) and the intake/play/shoot pipeline on an original 64 KiB test ROM. Notes `docs/emulator/sms.md`.

## 2026-11-19 - Ultima III (DOS) scouted and captured to the ending (260 shots); DOS queue done
- game-scout (a454aa8, cbe4b62): party ryz/condi/ebo/cubi, model svga-300 (CGA palette survives loads on svga),
  23 checkpoints to the ending, RAM map from EXODUS.BIN's load address, warps, quest chain from the code.
- game-capture (c835148, 9a54149): 260 shots, rolls forced with a simulator of the random generator, all nine
  combat fields, design/rules.md; corrected the scout (a calm also blocks frigates; fountain kind by column).
- Coordinator: replayed four scout checkpoints; cold `shoot.py dos/ultima-3 main --verify` 260/260, lenses
  clean, sheets looked at. Random-state rule promoted into the emulator guide (third report). Merged to
  `master`. The owner's DOS queue of this session is done: Might and Magic II 228, Wizardry I 208, II 212,
  III 228, Ultima I 195, II 226, III 260 shots, each verified from an empty cache.

## 2026-11-19 - Ultima II (DOS) scouted and captured to the ending (226 shots)
- game-scout (3523e50): ryz created, 29 checkpoints to the ending, BCD player record mapped, period warp,
  quest chain decoded from the program; starts in 1423 B.C. (the coordinator's brief said 1990).
- Coordinator (7b8d63d): `play.py export` writes the route from power-on into save READMEs (third report of
  circular `@checkpoint` routes), check in test_dos_pipeline fails without the fix.
- game-capture (3288ec2): 226 shots, honest Minax fight, every shop kind, all planets, spawn/dungeon/chest/trap
  rules and the random state decoded; Lord British's limits corrected (5000/7500/9900).
- Coordinator: cold `shoot.py dos/ultima-2 main --verify` 226/226, lenses clean, sheets looked at. Merged to
  `master`. Ultima III registered (0f34e01); scout dispatched.

## 2026-11-19 - Ultima I (DOS) captured to the ending (195 shots)
- game-capture (1c37e9d, d19fdf1): set `main` 195 shots, three lenses, RNG state found (115CC) for chosen rolls,
  save 03_midgame, `tools/shops.py`; RAM map corrections (class index, dungeon level at 19CA0).
- Coordinator: cold `shoot.py dos/ultima main --verify` 195/195, lenses clean, sheets looked at. Capture skill
  step 1: delete the game's cache before the first command. Merged to `master`.
- Ultima II (DOS) registered; scout dispatched.

## 2026-11-19 - Wizardry III (DOS) captured to the ending (228 shots); play.py rollback; Ultima I scouted
- Wizardry III scout (5b30832): Wizardry II party moved and legated (only Save2.Dsk needed), alignment gates,
  crystals, orb, ending; 22 checkpoints, all 107 messages read in play, saves 00-02.
- Wizardry III capture (de02d74): 228 shots; the Neutral Crystal made in play (the lead from a walkthrough was
  right, but the power is behind E)quip, not U)se); floor-gate rule verified (both earlier claims were wrong).
- Coordinator cold verify: 199/228. Everything from checkpoint `gfloor6` on came from states one key press
  ahead of their routes: `play.py do "y,w300!"` had pressed `y` before failing on the bad token, without
  recording or rolling back. Backend shown deterministic (loaded states agree with the cold build). Agent fix
  ad4511a (route gets the second `y`), coordinator cold verify 228/228. Coordinator fix dec8536: `do`/`sample`
  roll back on any error, regression check in `test_dos_pipeline` (fails without the fix); capture skill step 7:
  final verify from an empty cache. Merged to `master`.
- Ultima I (DOS) registered (ef538e3) and scouted (ad34deb, 843126a, 790e379): five programs played through to
  the ending, 22 checkpoints (cold and cache hit identical across program switches), player record mapped, warp
  to 84 places, saves 01-02; coordinator replayed four checkpoints. Rule into the emulator guide: stale status
  displays after pokes. Capture dispatched.

## 2026-11-19 - Wizardry II (DOS) captured to the ending (212 shots); Wizardry III registered
- game-capture (af9641c): set `main` 213 shots, lenses, GEAR/EQUIP/KODGEAR, save 03_wizardry3_transfer; floor 2
  riddle answer "shield", all five drops confirmed in RAM, monster HP at 0D3BA, Gnilda takes the whole pack.
- Coordinator: sheets looked at, `shoot.py dos/wizardry-2 main --verify` from an empty cache 213/213, then
  `save_leave_game` dropped (DOSBox Pure's overlay after the program quits, not the game) and republished: 212
  shots, lenses clean (166 / 190 / 113). Rules into the emulator guide: compare wireframe floor views before
  snapping; do not snap the front end's screens. Merged to `master`.
- Wizardry III (DOS) registered (7f7048f); scout dispatched with the transfer from 03_wizardry3_transfer.

## 2026-11-19 - DOS backend: writes through open files reach states; Wizardry II scouted
- Wizardry II (DOS) scout (04bd3a9, 3a1201c): the Wizardry I party imported through the game's own Move
  characters (`tools/transfer.py` puts Wizardry I's SAVE1.DSK next to the loader); quest chain to the ending
  (five KOD pieces, sphinx riddle, one character alone receives the Staff of Gnilda, knights); 22 checkpoints,
  saves 00-02, six floors decoded, roster at SAVE2.DSK 1D200 for Wizardry III. Found the stale-disk effect:
  the game reads its roster back, and states lacked the writes made through the open SAVE2.DSK.
- Coordinator (5310311): core patch `GamedbMarkWritten` marks a file for the save ZIP on every write through
  an open handle; test `test_dos_state_carries_writes_to_open_file` (hand-assembled HOLD.COM; fails without
  the fix); shared tests 29 passed, 15 skipped (other cores not built). The scout's failing case
  (`@ending,KNIGHTS,...` from a cached checkpoint) now equals the one-segment route. All DOS caches deleted
  and the published sets re-verified with the new core: dos/wizardry 208/208, dos/might-and-magic-2 228/228.
  Merged to `master`. Wizardry II capture dispatched.

## 2026-11-19 - Wizardry I (DOS): registered, scouted, captured to the ending (208 shots)
- Intake d997343 (slug `wizardry`, platform dos; one program, starts without the menu).
- game-scout (88e5d0e, eec5340): WIZ1.COM runs the 1984 booter from WIZ1.DSK (game) and SAVE1.DSK (scenario
  disk, shipped ready to use). Model `ega-315` (8088 speed; `cga`/`tandy` lose the palette on a state load).
  Party macros, 16 checkpoints title to ending, roster at SAVE1.DSK 1D800, RAM map, WARP via the stairs record,
  ten floors decoded (maps.py), saves 01-02. Found the backend's open-file flush gap (dos.md, open).
- game-capture (23dc245, 89185fc): set `main` 208 shots; Werdna beaten on screen without pokes; items.md;
  save 03_werdna_beaten as the Wizardry II transfer source.
- Coordinator: replayed four scout checkpoints, looked at the sheets, `shoot.py dos/wizardry main --verify`
  from an empty cache 208/208. Merged to `master`.
- Wizardry II (DOS) registered (0cd7a41); scout dispatched with the transfer from 03_werdna_beaten.

## 2026-11-19 - Might and Magic II (DOS): registered, scouted, captured to the ending (228 shots)
- Owner uploaded the GOG ZIP. Intake 782d91b (slug `might-and-magic-2`, region na).
- game-scout (5a06d6c, b71fdc7): MM2.EXE quits from the start menu ("Not enough memory for 16 color version");
  GOG's autoexec runs `loadfix -4`, so `BOOT` goes through the command line. Model `svga-8000` (GOG's cycles).
  The game reads ROSTER.DAT in its folder (six premade characters); `cloud_saves/ROSTER.DAT` is a played copy,
  not used. Party macros, 8 checkpoints (empty-cache rebuilds identical, disk included), save 01_start, RAM
  map, WARP to all 60 areas via the game's own edge transition, scan.py and texts.py.
- game-capture (f5a948a): set `main` 228 shots to the Congratulations screen; ending decoded from code and
  memory (Kalohn's quest bit, the Square Lake gate bit no script sets, override code WAFE, cryptogram answer in
  memory); three lenses; macros VET/HERO/MARKS/BATTLES; events.py; saves 02-04.
- Coordinator: replayed four scout checkpoints from a fresh process, looked at the three contact sheets,
  `lenses.py` clean, `shoot.py dos/might-and-magic-2 main --verify` 228/228. Rules promoted: dos.md (read the
  game's own DOSBox config; disk check of checkpoints), emulator guide (`goto` after a macro edit). Merged to
  `master`.
- Wizardry I (DOS) registered (d997343); scout dispatched.

## 2026-11-18 - Might and Magic 1 (DOS): 249/249 after the fix-up round
- Coordinator: cache deleted, `shoot.py dos/might-and-magic main --verify` in one run: 249/249 reproduce, no
  `check:` line (no identical pictures, no caption over 80 characters). Shared tests 35 passed, 8 skipped
  (SNES and Apple II cores not built in this container). Merged to `master`.

## 2026-11-18 - Might and Magic 1 (DOS) fix-up round: 249 shots
- game-capture (commit 8aedd0a): the three groups of identical pictures resolved (`encounter_retreat` dropped:
  Retreat at the encounter prints nothing, documented; `temple_poisoned` retaken as the clerics' prompt with the
  star on the poisoned member, the temple menu being the same picture for poison and wounds; `trap_door_after`
  retaken lit, map checked as CAVE1); 38 captions shortened to 80 characters; macros `LOWHP2`, `WORTHY2` and
  checkpoint `astral2` with the right record spacing, checked on screen, and the death, game over, ending and
  Astral shots retaken with them. The old `WORTHY` had marked only the first member: the ending's performance
  total is now 399602 (was 70122). Old macros and checkpoint kept, marked superseded.
- Coordinator: audit of the republished index (no identical pictures, no caption over 80, no route with the
  old macros), six retaken shots looked at, `tools/lenses.py` clean (201 / 199 / 176 of 249, 217 in two or more),
  the full re-verification from an empty cache was still running when this was written: result in the entry above this one.
- Promoted into `docs/emulator/README.md` (RAM): check a record table's spacing on the second and last record
  and read a record macro back on screen; a checkpoint built on a superseded macro is superseded too.
- Lead, not tried: the Astral door's "Key Card rejected" was tested with the old WORTHY; it may open with WORTHY2.

## 2026-11-18 - environment: no setup script, emulators are built per session
- Correction to the entry below: the setup script was removed again. Owner's decision: one session per
  platform, so building all five emulators at every session start (203 s) wastes most of the time; a session
  runs `sh tools/setup_emu.sh PLATFORM` when it first needs its emulator. Clean build times measured one by
  one: gb 9 s, nes 57 s, snes 53 s, dos 32 s, apple2 78 s.

## 2026-11-18 - DOS follow-ups: shot checks, prune, paged sheets, change token, text screen, menu test, setup script
- Owner: do all the points of the DOS handoff list, and a setup script for the environment.
- `tools/shoot.py`: `--verify` lists still shots with identical pixels (not in seq-* sets, not clips) and
  captions over 80 characters; `--publish` refuses identical pictures (exit 4, `--allow-duplicates`); `--prune`
  drops shots the work shots.txt no longer lists; contact sheets hold 100 shots (sheet.png, sheet2.png ...);
  after publishing `main` the lens check is printed. `tools/play.py`: `unsnap`/`recaption --game GAME` without
  a session; `text` prints a text-mode screen.
- `tools/emu.py`: token `change[:N]` (run until the picture differs from the start of the token, then N frames;
  an error if nothing changes within 4x the settle limit).
- DOS backend: `Dos.text()` through `retro_gamedb_readb` (core patch); a machine that was only just opened plays
  a state's launch itself instead of powering on a second time. Measured on Might and Magic 1: a shot costs
  0.5-2 s, the launch replay about 0.3 s, so the planned start without the menu was not built.
- Tests: `make_dos_zip.build(menu=True)` (two programs, so the core shows its start menu),
  `test_dos_start_menu_states`, `test_dos_text_screen_and_change_token`, checks/prune/unsnap in
  `test_dos_pipeline`. 35 passed, 8 skipped here; ten Might and Magic shots re-verified after the load change.
- `tools/lrcore.py`: one test run crashed (fatal error in the interpreter, not reproduced in nine further runs;
  an emulator build was running at the same time). Suspected, not proven: the private core copy was unloaded
  while its emulation thread was still exiting. The unload now happens one close later; memory stays bounded
  (30 opens: 151 MB).
- Cloud environment `game-hacking`: setup script added (owner approved): `sh tools/setup_emu.sh` in the repo, a
  failed build does not stop the session. Checked in a clean clone: all five emulators in 203 s (gb 9, nes 57,
  snes 53, dos 32, the rest apple2), shared tests 41 passed with nothing skipped. Unproven until a fresh
  session starts on the environment.

## 2026-11-18 - Might and Magic 1 (Apple II) brought up to the breadth and three-lens rules: 308 shots
- Owner's request after the new capture rules. The DOS set already meets them and is the same game, so its 250
  routes were translated (record addresses, waits, macros with the DOS arguments: `WARPX`, `DSTRONG`, `DVET`,
  sixteen checkpoints of the same names) and replayed here. Every result was looked at on review sheets: about
  200 matched their DOS captions as they were, 36 got a caption for what this version showed (Orcs where DOS
  met Poltergeists, other numbers, traps going off), 31 were dropped (combat sequences that diverged) and the
  main combat orders were re-taken by hand (options, Fight, Exchange, Use, cast with target, Lightning Bolt,
  victory, the chest found by Search). 60 of the earlier Apple II shots that the port duplicates were removed.
- Mistake found and fixed on the way: the DOS records are 128 bytes apart, not 127 as its playbook's LOWHP and
  WORTHY macros suggest; the first translation garbled members two to six in 22 shots (rerun).
- 306/308 reproduced from an empty cache; the two others were frames taken straight on a checkpoint and were
  re-taken settled (2/2). Published.
- `design/systems.md`, `interface.md`, `content.md` built from the DOS lenses, keeping only shots that exist
  here, each with an "Apple II" section; `tools/lenses.py apple2/might-and-magic`: 308 shots, all used, 279
  in two or more documents. The detail documents stay the DOS version's and are linked.
- Corrected: the playbook's claim that only the Apple II asks a yes/no before a service (DOS does too).
- Not done: detail documents of its own for this version; the rows' "numbers known" are the DOS run's except
  where the Apple II section says otherwise; six DOS mechanics have no shot here (listed there).

## 2026-11-18 - Might and Magic 1 (DOS) round 2: 250 shots, first three-lens documents; lrcore leak fixed
- game-capture round 2 (commits 916bb5b 6afca22): 113 -> 250 shots. Mechanics at work (bash and its trap,
  unlock, trade of item/gold/food, share, gather, discard, use, remove, equip refused, casting outside combat,
  bribe/retreat outcomes, exchange, bless, sleep, turn undead, temple cure and raise price, tavern, selling,
  chest trap), 30 more monster groups incl. Demon Lord, Lich, Gray Minotaur, Evil Eyes, Scorpion, Dark Rider and
  monsters acting (dragon breath, stoning, drain, paralysis), 20 environments. `design/systems.md`,
  `interface.md`, `content.md` written (`tools/lenses.py`: 202 / 201 / 177 of 250 used, 219 in two or more,
  nothing unused, no empty row). `tools/survey.py` surveyed all 55 areas; saves 04 and 05.
- Correction to the scout's RAM map: party records are 0x80 apart, not 0x7F; round 1's LOWHP and WORTHY macros
  hit the neighbouring byte for members 2-6 and were left unchanged so round-1 routes reproduce (playbook).
- Tool fix (coordinator): a private copy of a libretro core stayed loaded after close, about 40 MB per DOS
  machine opened (30 opens: 1232 MB, after the fix 120 MB); the agent's full verify had been killed for lack of
  memory and was run in two halves. `tools/lrcore.py` now unloads the copy and deletes its file.
- Coordinator: cache deleted, `shoot.py dos/might-and-magic main --verify` in one run: 250/250; sixteen new
  shots and three captions looked at; no game data in the commits. Shared tests 33 passed, 8 skipped.
- Not captured (tried): surprise message, search finding something, rest interrupted, surrender accepted;
  no screen change: retreat and block in combat, bash on a wall; not attempted: impostor, Eye of Goros, Astral
  door; wall sets per area are by eye, WALLPIX.DTA not decoded.

## 2026-11-18 - third lens: content
- Owner: the third area is content: variety in environments, items, enemies, equipment and so on; not a full
  set but a reasonable variety; in general shots should cover these areas, depending on game, genre and
  structure. Added `design/content.md` (template: kinds of content with totals, then samples that span the
  range per kind; kinds are adapted per game), the guide section is now "Three lenses", skill step 6 and
  AGENTS.md follow, `tools/lenses.py` checks the three documents.

## 2026-11-18 - capture: breadth rule and two lenses (systems, interface)
- Owner after the Might and Magic 1 (DOS) set: more battles with interesting enemies, the minor commands (bash,
  trade ...) to document mechanics, several visual environments; "rather document a few more
  features/mechanics/systems and shots than less". Promoted into `skills/game-capture/skill.md` step 6 and the
  capture guide's must-have list.
- Owner: a structured approach for features/systems/mechanics (game design) and for screens, system menus and
  interface elements (UI/UX analysis); overlap is expected. Built as two index documents over the same shots:
  `design/systems.md` (fixed groups from player verbs to pacing; rule, inputs, numbers, details, shots, status)
  and `design/interface.md` (conventions, inventory of every screen/menu/prompt/element, screen flow, main
  screens element by element; judgements marked Observation). Templates in `games/_template/design/`,
  `docs/capture-guide.md` "Two lenses", `tools/lenses.py` (shots in neither document, rows without a shot or a
  reason) with a test.
- Not done: no shot tags in shots.txt or the index (the documents are the mapping); existing games have no
  systems.md/interface.md yet. Might and Magic 1 (DOS) round 2 is running and writes the first pair.

## 2026-11-18 - Might and Magic 1 (Apple II): full tour, 134 shots to the ending
- Owner's request: a full tour. Solved first: combat (the back rank must block, attack is only offered in
  melee), the character records (language card RAM), an area warp (Sorpigal's exit event at A719 carries the
  same map ids and sections as the DOS port's table) and the ending square on the Astral Plane.
- Emulator: memory range `20000-2FFFF` = the main 64K as stored, for RAM that is not mapped while the game
  waits (`retro_gamedb_poke_main` in `tools/applewin-debug.patch`, backend, test, `docs/emulator/apple2.md`).
- Set `main`: +76 shots = one view of each of the other 54 areas (best of four facings chosen by a script),
  services in use, level-up, leprechaun travel, a won fight, game over, the Inner Sanctum ending and what an
  unworthy party is told. 134/134 reproduce from an empty cache; published. Side 4 is confirmed (all
  section-3 areas load from it).
- Macros POWER, EQUIP, CAST, LIGHT, WARP, DISK, WORTHY, LOWHP; checkpoint `strong`.
- Not done: a scout pass (manual, FAQ), maps, treasure and spell screens in combat, the towns' own services,
  design reference; area shots are arrival views, not chosen landmarks.

## 2026-11-18 - Might and Magic 1 (Apple II): set `main` grown to 58 shots
- Owner's request: more shots. From `@party`, `@menu` and `@title` with the `AT` move macro and the DOS port's
  table of Sorpigal's event squares (it matched square for square): blacksmith with its three price lists,
  market, temple, training, tavern, leprechaun, statue and plaque, jail sign, stairs and the dark cavern,
  quick reference, order, protect, rest, search, sheets and the cast prompt, the fixed fight at (3,6) with the
  monster picture and the combat screen, character creation step by step, delete prompt, "INSERT DISK B",
  second title picture and five demo scenes, more wilderness. 58/58 reproduce from an empty cache; published.
- Differences from the DOS port noted in the playbook: a yes/no before every service menu.
- Open: combat does not advance past the fourth member's turn with the keys tried, so no fight was finished;
  side 4, other towns, level-up, game over and ending are not in the set.

## 2026-11-18 - Might and Magic 1 (Apple II): new party, first shot set
- Owner's request: wipe the party, make a new one, do the shot roundtrip. From `@menu`: the six inherited
  characters deleted (view all, A, Ctrl-D, Y, six times), six created with re-rolls until the wanted class was
  offered: RYZ knight, CONDI paladin, EBO archer, CUBI robber, DEDDO cleric, MNZ sorcerer. Checkpoints `roster`,
  `party`, `signed_in`; save `02_ryz_party` kept in `rom/saves/` (a whole disk side, not committed).
- Roundtrip: 9 shots snapped (title, options menu, roster, character sheet, Sorpigal, inn sign-in, inn list,
  "INSERT DISK C", wilderness), `shoot.py --verify` 9/9 from an empty cache (the route replays the wipe, the
  creation with its re-rolls and both disk changes) and 9/9 from the cache, published to
  `games/apple2/might-and-magic/shots/main/`.
- Corrected in the playbook: the title picture waits for a key; the "ESC to start" screen comes after Space.

## 2026-11-18 - Might and Magic 1 (Apple II) runs across its disk sides
- Owner uploaded five ZIPs: sides 1-4 as `.dsk` (TOSEC `[b]`) and a cracked side 1 as `.nib`. Registered as
  `games/apple2/might-and-magic/` with the `.nib` as disk 1 and the `.dsk` sides 2-4 (region na). The `[b]`
  side 1 hangs on the first title picture re-reading track $0E forever; reported in the playbook, not used.
- Played: crack screen -> title -> ESC -> "INSERT DISK B" -> `disk:2,enter` -> options menu -> Sorpigal with
  the six characters found on the disk -> passage outside -> "INSERT DISK C" -> `disk:3,enter` -> wilderness.
  Meal at the market, sign-in at the inn: the roster is written to side 2; `sav:` power-on shows gold 43,
  food 40. Position and facing found in zero page (0080-008C); macros TITLE, MENU, TOWN:n, AT, FN/FE/FS/FW,
  OUTSIDE; checkpoints title, menu, sorpigal, outdoors, after_save, all replayed from an empty cache.
- Bug found by this game and fixed in `tools/applewin-debug.patch`: frames drawn after loading a cached state
  differed from straight play in 621 pixels by 1 (the core's colour tables, rebuilt on load with leftover
  filter memory). New test `test_apple2_colour_after_state_load`; the earlier tests only had text screens.
- An exported save is a ZIP of the whole changed side 2: game data, so it stays in `rom/saves/` (not committed).
- Not done: side 4 (castles, deeper dungeons: seen only as text on the image), going back into a town from
  the wilderness, combat, character creation, scout and capture.

## 2026-11-18 - Might and Magic 1 (DOS) main set: 113 shots to the ending
- game-capture (commits a5a6a46 fd0cd53 8e2f286): the 32 scouted routes, then creation steps, all Sorpigal
  services, one fight from encounter to victory, game over, the cavern dark and lit, wilderness sectors, towns
  2-5, three castles, Quivering Forest, Astral Plane and the Inner Sanctum text. Found the map loader and its
  55-entry table in Sorpigal's overlay; macro `WARP:x:y:idlow:idhigh:section` pokes the operands of the town's
  own exit event, so the game loads any area (only from inside Sorpigal). 13 checkpoints, save
  03_portsmith_inn, design/combat.md, world.md, characters.md. Fixed in the game's tools/maps.py: event tables
  were read two bytes early (OVR header is 14 bytes), which had hidden two event squares per area.
- Reached by poke, stated in the captions: gold, experience, positions, 1 HP for the game over, quest marks and
  position for the ending (level-1 party; the Astral door rejected a poked Key Card, cause not found).
- Coordinator: cache deleted, `shoot.py dos/might-and-magic main --verify` 113/113; twelve shots across the set
  looked at; no game data in the commits; file names follow the new scheme
  (`might-and-magic_dos_na_<area>_<id>.png`). Shared tests 32 passed, 7 skipped (SNES and Apple II cores not
  built in this container).
- Tool notes from the run, not acted on: `play.py unsnap` needs a running session; `shoot.py --publish-only`
  orders the index by the game folder's shots.txt; `emu.py` and `shoot.py` differ by a few frames on an
  animated title; the container clock barely advanced during the run.

## 2026-11-18 - shot file names carry game, platform, region and area; Wizardry slugs renamed
- Owner's rule: a shot file must say what it shows outside its folder (the files are used in other contexts).
  Scheme: `<game>_<platform>_<region>_<area>_<id>[.<set>].<ext>` (`docs/capture-guide.md`, "File names").
  game/platform/region = `game.json` slug, platform and the new key `region` (`jp`, `na`, `eu`: the release of
  the dump, not the language; a translated Japanese ROM is `jp`; DOS Might and Magic is `na`), area = the shot's
  category, id unchanged (ids that start with their category repeat it, accepted). Sets other than `main` and
  `seq-*` add `.<set>`; contact sheet, strip and sequence GIFs use the area `set`.
- Slugs are the short game name without the platform: `games/nes/wizardry-nes` -> `games/nes/wizardry`,
  `games/nes/wizardry-2-nes` -> `games/nes/wizardry-2` (ROM paths `rom/wizardry.nes`, `rom/wizardry-2.nes`).
  Entries below keep the old paths.
- Tools: `shoot.py` builds the names (`stem`, `set_file`) and renames a working set on its next run when the
  scheme, a category, the region or the slug changed; `play.py` snap/record/unsnap use them (a re-snap with
  another category removes the old file; unsnap of a clip no longer fails); `intake.py --region` (read from the
  header only where it is certain: GB Japan, SNES country code, NES PAL), slug checked.
- Migration: 1604 published images of the 11 registered games and 690 of Wizardry Empire renamed with `git mv`
  (pixels untouched), index.json/index.md rewritten, links in design and tech documents followed; no broken
  image link in non-history documents. Nothing was replayed: no ROMs in this container, so `--verify` of the
  renamed sets is still to be run where the dumps are.
- Wizardry Empire: same scheme with the set always written and the ROM last
  (`wizardry-empire_gbc_jp_menu_camp.rev1-tour.en.png`); its place categories (town, tavern, maze...) became
  the database categories; sets `jp_tour`/`rev1_tour` are `jp-tour`/`rev1-tour`.
- Branch rule changed (owner): sessions work on their own branch and make sure the work is merged to `master`.
- Tests: 33 passed with all four emulators built (new: file-name unit test, category change renames files,
  old working set renamed on the next run).
## 2026-11-18 - Apple II backend (AppleWin)
- Owner asked for an Apple II emulator. Chosen: AppleWin in audetto's Linux port, which has a libretro core (fits
  `tools/lrcore.py`, no SDL, savestates, firmware ROMs in its source, DSK/DO/PO/NIB/WOZ/2MG/HDV). MAME would
  be a far bigger build; the other Apple II emulators have no libretro core. Pinned e9ebeb7.
- `tools/applewin-debug.patch`, each part for something measured: power-on RAM held bytes of the host time; the
  emulator's rand() (disk noise, copy-protection jitter) is not part of a state; a frame's length followed the
  host's sound buffer, so the same state loaded into machines of different age continued four different ways
  (now one video frame per call on the saved cycle counter: all equal); the keyboard was a type-ahead queue of
  which a state kept one key (now the real one-key latch). Added: disk insert/eject, flush, peek/poke, PC, a
  settable clock, a silent log. The build wants `xxd` (not installed here, no apt package reachable):
  `tools/xxd_i.py` stands in; a font resource from a git submodule (SDL frontend only) is dropped.
- `tools/platforms.py` `Apple2`: a game is one image or a ZIP of images (a ZIP of only disk images is Apple II,
  any other ZIP stays DOS); private copies of the disks, the dump is never written; states store the changed
  4 KiB blocks of the images and restore them on load; `play.py export` = ZIP of the changed images, `sav:`
  powers on with them. `tools/emu.py`: `disk:N`, `disk2:N`. `tools/lrcore.py`: start without content; a core
  dropped without close() is closed when collected (AppleWin's exit handlers otherwise used freed memory: a
  random abort at interpreter exit, about 1 run in 6 after a failed test; found with valgrind).
- Tests: `tests/make_apple2_disk.py` (boot sector that echoes keys with a cycle-exact timing letter) + 6 tests:
  identify, backend, same route same frames, disk swap, state carries disk writes (DOS 3.3 `SAVE` on the master
  disk from the AppleWin source), intake -> play -> snap -> `shoot.py --verify`.
- Seen working by hand: DOS 3.3 master, ProDOS 2.4.3 (`.po`), hi-res colour in four video modes, II Plus and
  unenhanced //e ROMs, states taken while the drive reads. `sh tools/setup_emu.sh apple2` built from an empty
  folder.
- Not done: no Apple II game registered or played; reset keys; write-protected disks; hard disk images with a
  real game; `dis6502.py` for Apple II memory.

## 2026-11-18 - Might and Magic 1 (DOS) scouted; launch log bug fixed
- game-scout (commit 4550427): playbook filled (about 30 controls verified, rest from the manual in the ZIP),
  macros for creating RYZ and renaming the stock party, checkpoints title/menu/start/created/blacksmith/
  equipped/combat, RAM (position 15E68.., party records 1682C + 7F*n, gold, experience), move-by-poke macro AT,
  tools/maps.py and scan.py, save 02_ryz_party, shot plan with 32 routed lines, design/sorpigal.md.
  Coordinator: title/menu/start/combat replayed from an empty cache; combat frame looked at.
- Bug found by the scout: a cached checkpoint whose route created a character showed the character twice after
  the next sign-in. Cause: the "launch" stored with a DOS state ran to the first save_state (the end of the
  checkpoint route), so loading replayed the creation on a disk that already had it. Fix: the launch ends at
  the first 10-frame step after which a program runs (`retro_gamedb_running` in the core patch); a load now
  fails loudly if the launch does not start a program or changes the disk. The scout's reproduction: same
  frames and roster A-G on cache miss and hit. Test extended. 30 passed, 2 skipped.
- dos.md corrected: 320x200 games are 320x200 in `emu.py`/`shoot.py` output (960x600 is play.py's 3x view).

## 2026-11-18 - DOS: in-game saves, states carry the disk
- Tested saving in Might and Magic 1: signing in at the inn writes ROSTER.DTA into DOSBox Pure's save ZIP. A
  cached checkpoint made after the save, loaded in a new process, showed the saved roster on screen (the game
  keeps it in memory) but the disk there was the original one: wrong as soon as the program restarts.
- Fix: DOS states store the written files (save ZIP) and loading restores them (power-on with those files,
  replay of the launch inputs, then the core state) whenever the machine's files differ. The core writes its
  save ZIP one emulated second after a change, so the patch gained `retro_gamedb_flush`.
- `play.py export` and `sav:NAME` work for DOS (the save is that ZIP); `games/dos/might-and-magic/saves/01_signed_in.sav`.
- Test program KEYS.COM creates S.DAT on `w`; new test `test_dos_state_carries_written_files`. 30 passed, 2 skipped.
  Might and Magic trial shots still 2/2 from an empty cache.

## 2026-11-18 - Wizardry II: maze SOLID vs LINE comparison set
- Owner's request: set `compare-maze`, 11 shots (options with LINE, floors 1/2/4/5/6 x SOLID/LINE), 11/11 verified
  from an empty cache; option byte $6DA3 (1 SOLID, 0 LINE) found with `play.py diff`; side by side in
  `games/nes/wizardry-2-nes/design/maze-solid-vs-line.png`. A first floor 2 view met a random fight in LINE only
  (drawing time shifts the RNG); replaced by the `f2` checkpoint view.

## 2026-11-18 - Might and Magic 1 (DOS) runs
- Owner uploaded the GOG folder as a ZIP (97 files, SHA-1 c1a9248d...). Registered as `games/dos/might-and-magic/`
  (same slug as the NES game, so commands need `dos/might-and-magic`), model `svga-1500` (GOG's own cycles).
- Played: start menu -> MM.EXE -> title -> ESC -> Enter -> options -> town 1 -> inn, six stock characters added
  with Ctrl+A..F -> Sorpigal, walking, character sheet. Macros BOOT, MENU, TOWN:n; checkpoint `sorpigal`.
  Trap: Space at the title starts a slideshow of scenes that look like gameplay; an early ESC lands in it.
- Found with the real game, fixed in `tools/platforms.py`: the core refuses to save a state in its start menu
  and refuses to load one unless a program is running (the test program had hidden this: a ZIP with one program
  starts it at once). States before a program runs are now input logs replayed from power-on; real states carry
  the inputs that launched the program. Check: 2 shots recorded live, `shoot.py --verify` 2/2 from an empty
  cache and 2/2 from the cache.
- `tools/play.py start` returned only after 10 minutes when its server died at once (here: ambiguous slug);
  it now stops waiting when the server process has exited.
- Not done: scout/capture, character creation, combat, in-game saving and what a savestate does to ROSTER.DTA.

## 2026-11-18 - Wizardry I: maze SOLID vs LINE comparison set
- Owner's request (asked for Might and Magic; the option is in Wizardry I/II, Might and Magic has none): set
  `compare-maze`, 9 shots (options with LINE, four views x SOLID/LINE), 9/9 verified from an empty cache; option
  byte $7ABC found with `play.py diff`; side-by-side `games/nes/wizardry-nes/design/maze-solid-vs-line.png`.

## 2026-11-18 - games grouped by platform
- Owner's decision: `games/<slug>/` -> `games/<platform>/<slug>/`, so a game can exist on several platforms (the
  DOS Might and Magic next to the NES one). The folder is the game.json "platform" value. Mapping:
  `nes/`: deep-dungeon-3, dragon-quest, dungeon-magic, megami-tensei, megami-tensei-2, might-and-magic,
  wizardry-2-nes, wizardry-nes; `gb/`: pokemon-blue; `gbc/`: wizardry-empire; `snes/`: shin-megami-tensei.
  `games/_template/` stays. Entries below this one and all feedback/agent logs keep the old paths.
- Tools: `emu.find_game` (GAME = `slug`, or `platform/slug` when the slug is not unique; an ambiguous slug is
  an error that names the platforms), `Game.id` = `platform/slug` for `work/shots|cache|roms|intake/`;
  `intake.py` creates `games/<platform>/<slug>/`; `dis6502.py` resolves through emu. `rom/<slug>.<ext>`,
  `rom/saves/<slug>/` and `rom/patches/<slug>/` are unchanged (uncommitted; they collide only if two platforms
  share a slug and a file extension).
- Path depth fixed in game tools that find the repo root from their own location (dungeon-magic atlas/maps,
  might-and-magic maps, wizardry-nes and wizardry-2-nes maps/roster, shin-megami-tensei mkrom, Wizardry Empire
  `translation/tools/emu.py` and `setup_emu.sh`). Paths in docs, skills, agent wrappers, playbooks, game.json
  and .gitignore rewritten; markdown link check before/after: no new broken links.
- Checked: shared tests 29 passed, 2 skipped (SNES core not built here); Wizardry Empire tests 10 passed, 4
  skipped (no ROM here). Not checked: anything that needs a ROM (no dumps in this container), so the map tools
  and the Wizardry Empire build were only compiled/started, not run against data.
- The slugs `wizardry-nes` and `wizardry-2-nes` still carry the platform in their name; not renamed.

## 2026-11-18 - DOS backend (DOSBox Pure)
- Owner asked for a DOS emulator, first game to be Might and Magic 1. Chosen: DOSBox Pure as a libretro core
  (no SDL, no display, fits `tools/lrcore.py`, has savestates); DOSBox-X and DOSBox Staging would need SDL2,
  Xvfb and a new driver, Staging has no savestates. Source from github.com/libretro/dosbox-pure (pinned
  e39497e); schellingb/dosbox-pure on GitHub is now only a pointer to Codeberg.
- `tools/lrcore.py`: keyboard callback and held-key polling (without the polling the core releases a key at
  once: letters still arrive, Shift/Ctrl/Alt never do), mouse buttons and relative motion, a virtual host clock
  (`frame_usec`), `epoch`, memory maps, private library copy per game (`private`; the core crashes when a second
  game is loaded into the same library), all open cores closed at interpreter exit (a core with its own thread
  otherwise blocks the exit of a failed script).
- `tools/dosbox-pure-debug.patch`: settable clock (time, gettimeofday, clock_gettime, localtime wrapped at link
  time), frame sync, CS:IP, and a savestate fix. What was wrong without each: the BIOS tick counter started from
  the host time (two boots differed); the emulation thread ran ahead of the frontend (keys landed at
  host-dependent moments, one RAM byte differed in 1 of 3 runs); a loaded state was one frame ahead of the run
  that made it (the render reset on load dropped the frame in progress).
- `tools/platforms.py` `Dos` backend, `tools/emu.py`: digits in key tokens (`1`, `f1`, `kp4`), `type:TEXT`,
  `mouse:DX:DY`. `tools/setup_emu.sh dos`. Tests: `tests/make_dos_zip.py` (33-byte KEYS.COM that prints a
  tick-derived letter before every key) + 4 tests incl. intake -> play -> snap -> `shoot.py --verify`.
- Measured: 6 boots identical; 200 random key steps identical between straight play and play with a state
  save+load every third step; a fresh machine needs 2+ frames before its first state load (backend runs 4).
- Not done: no real DOS game run yet (no game files in the container); save export, `sav:`, disk files in
  savestates, CD images.

## 2026-11-18 - Megami Tensei round 2: maps of all 35 floors, bosses, ending
- game-capture round 2: 41 -> 88 shots (commits 5702a0b 1030de2): level-up (the "next level" counter at $0576, not
  EXP), battle magic, a demon fighting, all six bosses beaten (each needs its item: Ratos Statue, Purski's Trumpet,
  White Dragon Orb ...), the ending and credits; all 35 floors decoded from ROM (one 128x64 grid + block table)
  into design/maps/ + maps.md; late password recorded; WARP macro. Coordinator: folder = index (88), game.json
  changes are additions only, 6/6 re-verified (3 old, 3 new incl. the ending).

## 2026-11-18 - Megami Tensei II round 2; play.py sample
- game-capture round 2: 67 shots (commits 9e8c146 6d009b8), set in game order, start_room retaken; Devil Buster
  finished as intended (Taurus -> S.ORB -> god statue -> Pazuzu), found by stepping onto every entry of the ROM's
  event-square table; demons in the COMP by poke (CHAT joins still never happen), summon, demons in battle, fusion;
  village shop, totem save (02_village_totem), registry; overhead maps (Devil Buster, overworld, towns) in
  design/maps/. Coordinator: folder = index (67), 6/6 re-verified; naming prompts checked on screen (hero,
  girlfriend CONDI, best friend EBO), so the captions follow the game's labels.
- `play.py sample "TOKS" N`: frames after each of N runs tiled, state and route unchanged (typewriter text; asked
  for by five runs). Emulator guide: story gates -> step on every event-table entry first.

## 2026-11-18 - Deep Dungeon III main set; macros with arguments; batch of five done
- game-capture: 74 shots (commits fb6c8ee c3b8e42 4294138): towns and shops of three towns, temple, magic hall,
  combat, level-up, companion joining/dying, events on all floors, masters Zosem and Barzas, the ending (area 6)
  and credits; maps: three towns identified, building kinds, event squares per floor, warp tokens; design docs;
  save 02_veterans. Coordinator: folder = index (74), 6/6 sample re-verified incl. the ending.
- `tools/emu.py`: macros take arguments (`NAME:a:b` fills `{0}` `{1}`), for one-token warps; test in
  `tests/test_small_tools.py` (renamed from test_dis6502.py). A warp/event helper had been hand-built in five runs.
- The owner's batch of 2026-11-18 (Dungeon Magic, Wizardry I and II, Might and Magic, Deep Dungeon III) has a full
  first pass: sets, floor maps, saves, design docs.

## 2026-11-18 - Deep Dungeon III scouted; NES docs: PRG ROM pokes have no effect
- Scout: Japanese only (no patch supplied); party りず/こんでい/えぼ/きゅび (hiragana-only keyboard, four members),
  save 01_start, warp via the cave's stairs reload, 16 floors + town grid decoded and drawn; 14 routed shots
  verified 14/14 by the coordinator.
- `docs/emulator/nes.md` and the Nes docstring said poke reaches mapped PRG; checked: it has no effect on PRG ROM.
- `play.py start` keeps RAM dumps (only old frames are cleared), so diffs work across session restarts.

## 2026-11-18 - Might and Magic (NES) main set: complete through the ending
- game-capture: 93 shots (commits 63279a4 5d0785b 3a6af15): town services, character sheets, camp, combat,
  chests, game over, all five towns, VARN sectors, caves, castles, the impostor King Alamar, the Soul Maze and
  the Inner Sanctum ending; maps with legend, terrain (checked by walking) and decoded exits, `towns.md`,
  `combat.md`, `story.md`; saves 02-03. Coordinator: folder = index (93), 6/6 sample re-verified.
- `shoot.py --publish`/`--publish-only` remove published images whose id left the index (second report, after
  Wizardry II); checked with a planted stale file. Emulator guide: event-script facing may differ from RAM facing.

## 2026-11-18 - Might and Magic (NES) scouted
- Scout: hero RYZ + five inn fellows renamed CONDI/EBO/CUBI/DEDDO/MNZ by poking the name table (the game names
  only the hero; record check byte fixed), save 01_party, warp via the pending-area byte $9D, all 55 areas decoded
  and drawn (`games/might-and-magic/design/maps/`); 16 routed shots verified 16/16 by the coordinator.
- game-scout skill step 3: test macros as one `do` from power-on (second report), rebuild checkpoints after a
  macro edit.

## 2026-11-18 - Wizardry II (NES) main set: complete through the ending
- game-capture: 91 shots (commits 9bda454 a3cb2bd 498f4f3 20aa150; 498f4f3's publish failed on a stale id, fixed
  by 20aa150): castle, combat, chests, story events on all six floors, "Rock!" (type 04 = party dies), the ending
  via the regalia (Staff of Gnilda, Knights of the City, credits); every special type checked in play except
  06/07; `design/story.md`, `castle.md`, `combat.md`, `maps.md`; saves 02-04. Coordinator: published folder
  matches the index (91/91), 6/6 sample re-verified incl. the ending.

## 2026-11-18 - Wizardry II (NES) scouted; NES cartridge RAM reachable while disabled
- `tools/platforms.py` Nes: peek/poke of 6000-7FFF use the core's battery-RAM buffer (8 KiB carts). Before, MMC3
  games with the RAM disabled read open bus and silently dropped pokes (Wizardry II scout, ~6 calls). Regression:
  Wizardry I roster-poke shots 5/5 and Dungeon Magic rune shots (poke $61CB) 2/2 reproduce. `docs/emulator/nes.md`.
- Wizardry II (NES): scout done (engine shared with Wizardry I; tools ported): party macro, save 01_party, roster
  CRC tool `tools/roster.py`, 6 floors decoded and drawn; 10 routed shots verified 10/10 by the coordinator.

## 2026-11-18 - Wizardry I (NES) main set: complete through the ending
- game-capture: 71 shots (commits 69d7eaa 5805efa 41939b7): creation, castle, shops, temple, spell books, combat
  and spells, chests and traps, Murphy's ghost, pit, chute, elevator, floors 4 and 10, Werdna, the ending and
  credits; all 19 special-square types decoded, `design/maps.md`, `castle.md`, `combat.md`; saves 02_veterans,
  03_werdna_defeated. Coordinator: 6/6 sample re-verified (incl. Werdna and the ending), sheet reviewed.
- `play.py start` clears the session folder's old frames and dumps (an agent read stale scout frames for ~10 calls).

## 2026-11-18 - Wizardry I (NES) scouted; play.py dump/diff
- `play.py dump NAME` / `diff A [B]`: RAM snapshot and byte diff (NES/SNES search ranges; GB work/save RAM);
  third scout in a row had copied an ad-hoc ramdiff.py. Emulator guide: play.py routes are the reproducible ones.
- Wizardry I (NES): scout done; party RYZ/CONDI/EBO/CUBI/DEDDO/MNZ by macro, save 01_party, all 10 floors decoded
  from ROM and drawn (`games/wizardry-nes/design/maps/`), warp by position pokes; 15 routed shots verified 15/15
  from an empty cache by the coordinator.

## 2026-11-18 - Dungeon Magic main set and floor maps; sets published in game order
- game-capture: 41 shots (commits 91cae5d 242b035 1e9c2b0 9171d1e), all 39 floors + overworld mapped into
  `games/dungeon-magic/design/maps/` (`maps.md` index, warp tokens per floor), design `magic.md`,
  `progression.md`, save `02_granville_fire_lv1`. Coordinator: 6/6 sample re-verified from an empty cache.
  Open: the King, camp, the swords, beaten bosses, Darces, the ending (floor-92 guardian ignores blows).
- `shoot.py`: index.json, index.md and the sheet follow the game's `shots.txt` order (on every snap, reindex and
  publish); second request (Megami Tensei II and Dungeon Magic captures). Checked on a shuffled copy of a set.

## 2026-11-18 - Dungeon Magic scouted; shared 6502 disassembler
- `tools/dis6502.py` (any registered NES game or ROM path, bank size option, truncated operands as .db; test
  `tests/test_dis6502.py`), promoted from the Dungeon Magic scout's game copy (second ad-hoc disassembler after the
  Megami Tensei II capture). Emulator guide: map block in RAM -> stored maps in ROM; joypad read before guessing.
- Dungeon Magic: scout done, 4 checkpoints, save 01_start, maps located (RAM $0600, ROM towns/dungeons), renderer
  `games/dungeon-magic/tools/maps.py`; 12 routed shots verified 12/12 from an empty cache by the coordinator.

## 2026-11-18 - Megami Tensei II main set; five more games registered
- Megami Tensei II (Famicom, English IPS, headered layout): scout (3cb9dea, 15 routed shots, 15/15 verified) and
  capture (fa9a47d, e2d1b8b): 36 shots, save `01_computer_room.sav`, design `world.md` and `combat.md`. Devil Buster
  not finished (last stairs inside a wall); the real world reached by losing inside it. Coordinator: 6/6 sample
  re-verified from an empty cache; the untranslated lines checked against the unheadered layout (garbles the
  first English page), so the layout is right and the lines are a gap in the patch.
- Registered (no patches): Dungeon Magic, Wizardry I and II (NES), Might and Magic (NES), Deep Dungeon III (b1cb5fc).

## 2026-11-18 - Megami Tensei main set
- game-capture: 41 shots, commits 23a7460 b29aa51 e88f35c (milestone commits made as asked). Sage password
  recorded (macro `PW_SAGE1`), position/money/Comp RAM, 8F event map from a RAM-warp scanner, design `demons.md`
  and `world.md`. Coordinator: 6-shot sample incl. fusion, password and Minotaur re-verified 6/6 from an empty
  cache; sheet reviewed.
- Emulator guide: `freeze:` is re-applied between tokens, not inside one `wN` (party died in long waits); RAM-warp
  floor scan for first-person dungeons.

## 2026-11-17 - Megami Tensei scouted; NES/SNES RAM search fixed
- `play.py find reset` on the libretro backends (NES, SNES) cleared the search without a snapshot, so the first
  `find` compared RAM with itself (`new == old + 1` always 0 candidates). Reset now snapshots; reported by the
  Megami Tensei scout, rechecked on the game (12 candidates after one step).
- Megami Tensei (Famicom, English BPS): scout done (commit 2ef4abc), 9 routed shots verified 9/9 from an empty
  cache by the coordinator. Capture run next.

## 2026-11-17 - owner-supplied patches are always applied
- Owner's rule: if an IPS/BPS/UPS patch comes with a ROM, use it. Written into `AGENTS.md` (rules + quick
  reference), the coordinator skill and `docs/emulator/README.md`.
- New `tools/patch.py` (IPS incl. RLE and truncation, BPS, UPS; CRC checks; header layout detected for BPS/UPS
  from the source CRC, given by hand for IPS) and `intake.py --patch` (repeatable): patched ROM in `rom/`, dump in
  `rom/src/`, patches in `rom/patches/<slug>/`, game.json "source" with names, SHA-1s, layouts and the rebuild
  command. Tests: `tests/test_patch.py`; end-to-end intake with a BPS on the synthetic NES ROM rebuilt the same
  SHA-1. Wizardry Empire's own `translation/tools/bps.py` left as is.
- `patch.py` layout `ines1` (tried automatically): the dump's header rewritten as plain iNES 1.0. Found with
  Megami Tensei (Famicom): the owner's dump has an NES 2.0 header, the BPS was made against the iNES 1.0 header
  of the same body (mapper 76); CRC matched after that, body untouched.

## 2026-11-17 - 3x copies in a subfolder
- Owner's request: originals in the set folder, 3x copies in a `3x/` subfolder with the same file names
  (`title_screen.png` and `3x/title_screen.png`; also clips, `steps.gif`, `full.gif`, Wizardry's compare images
  `3x/<id>.compare.png`). Tools: `emu.x3()`, shoot.py, play.py, Wizardry's `translation/tools/shoot.py`
  (publishes only the compare images into `3x/`). `index.json` `file_3x` is `3x/<name>`.
- Migration: 404 published files moved with `git mv` across all 8 sets, catalogues rewritten (links checked: 0
  broken), working sets in `work/` migrated the same way. Sample shots re-verified (Dragon Quest 2/2, SMT
  republished with no `@3x` left). 18 shared tests and 14 Wizardry tests pass.

## 2026-11-17 - Shin Megami Tensei main set, run 2
- game-capture: 22 new shots (56): second dream, heroine naming (cubi), first battle and commands, damage, enemy
  spell, result, level-up, failed escape, death, game over, full-moon refusal, negotiation steps, automap.
  Commit bd1607c. Run 1's blocker was a misread watch: the apartment door is square 32,88 (decimal 134/136 read
  as hex). The second dream needs story flag 7E07C1 bit 02; its real trigger is not found, so the route pokes it.
- Not reached: a demon joining (always asks for a Bead), summoning, fusion, terminals, healing, items list,
  bosses. Save 03_second_dream exported.
- Coordinator: `automap` (snapped while a verify was starting) and a sample verified 4/4; the agent's full
  verify covered the other 55. Tools: RAM watches take `"fmt": "hex"`; emulator guide notes on stuck events.

## 2026-11-17 - Shin Megami Tensei (Super Famicom, English patches): intake, scout, main set run 1
- Owner supplied the Japanese dump and two IPS patches (translation, then its bug-fix). The patches expect
  different layouts (smte1 with the 512-byte copier header, smte2 without): `games/shin-megami-tensei/tools/
  mkrom.py` rebuilds and checks SHA-1s. SNES header checksum now handles sizes that are not a power of two.
- game-scout: playbook, 6 checkpoints, RAM map (yen, magnetite, character records), save 01_start, shot plan.
  Names: ryz (hero), condi (Law hero), ebo (Chaos hero); the heroine is named later (cubi).
- game-capture run 1: 34 shots (boot, intro incl. one hi-res frame, dream, naming, stats, room, mail, save/load,
  3D corridor, command menus, town map, clinic, arcade shops, cafe, roadblock, full moon), commits a6c6883,
  9db24cd, be549c9. Found position, facing, moon/step counter and town-map tile; town-map warp at an exit
  prompt. Partial: could not find the way back into the apartment, so the story does not advance (no battles,
  negotiation, fusion, terminals, later districts).
- Coordinator: full verify rerun 34/34; contact sheet reviewed.
- Tool fixes from the two reports: `MACRO*N`; `prefix()` skips `pow` (sav: routes replay); `play.py export`
  refuses an empty battery; `play.py unsnap` / `recaption`; contact sheets scale bigger frames to the common
  cell (a 512x448 frame blew up every cell and detached the labels). 18 tests pass.

## 2026-11-17 - SNES / Super Famicom backend (Mesen-S); core options were not applied
- Owner's request: an emulator for SNES/SFC games. Mesen-S as a libretro core (libretro/Mesen-S at 9e4fdeb),
  chosen to match the NES setup: same driver, same kind of debug patch (`tools/mesen-s-debug.patch`: peek/poke
  over the 24-bit address space, PC with bank). `setup_emu.sh [gb|nes|snes]`.
- `platforms.py`: shared `Libretro` base class (states, screenshots, RAM search, battery) for `Nes` and the new
  `Snes` (header detection LoROM/HiROM/ExHiROM with copier header, region -> ntsc/pal, 12 buttons, PAR codes
  through `gs:`, Game Genie as a ROM patch through the mapping). Frames: the 239-line output is cropped to 224
  when the margins are black.
- Bug found and fixed: `lrcore.py` compared option keys as text against the core's bytes, so no core option was
  ever applied. NES ran on defaults that equal the intended values (only the region was auto-detected instead
  of forced; `--model pal` did nothing). On SNES the default power-on RAM is random, which the new test caught.
  Dragon Quest shots re-verified from an empty cache after the fix (5/5).
- Tests: generated SNES test ROM (`tests/make_snes_rom.py`), header/cheats, backend, full pipeline. 16 pass.
  ~330 fps. Docs: `docs/emulator/snes.md`.

## 2026-11-17 - repository restructured
- Owner's request: the repo had grown project by project (a translation, then a screenshot database next to it).
  Now the repo is the database: every game under `games/<slug>/`, shared tooling at the root, the Wizardry
  Empire translation a sub-part of its game. Path mapping (older entries and feedback logs keep the old paths):

  | Before | Now |
  |---|---|
  | `gamedb/games/`, `gamedb/tools/`, `gamedb/tests/`, `gamedb/rom/`, `gamedb/work/` | `games/`, `tools/`, `tests/`, `rom/`, `work/` |
  | `gamedb/README.md` | merged into `README.md`; `docs/README.md` is the index of the shared docs |
  | `gamedb/docs/emulator.md` | `docs/emulator/README.md` (general) + `docs/emulator/gb.md` + `docs/emulator/nes.md` |
  | `gamedb/docs/capture-guide.md`, `status.md`, `progress-log.md` | `docs/` |
  | `wizardry-empire/docs/design`, `docs/tech`, `docs/shots`, `saves` | `games/wizardry-empire/design`, `tech`, `shots`, `saves` |
  | `wizardry-empire/docs/README.md` (document rules) | `games/wizardry-empire/DOCUMENTS.md` |
  | `wizardry-empire/` everything else (script, asm, fonts, tbl, glossary, tools, tests, docs/re, status, log, rom.sha1) | `games/wizardry-empire/translation/` |
- One emulator build: the Wizardry tools use `tools/gbemu-cli` at the repo root (its own copy of the setup and
  the Linux patch are gone). Its design-table, map and publish tools write to the game-level folders.
- NES notes are their own document, not a list of differences from Game Boy.
- Wizardry Empire checked with the owner's ROM after the move: identical build (ROM and IPS) and identical tour
  frames (135) compared with the pre-move commit; generators reproduce the committed files.
- Not done: Wizardry Empire is not registered with the shared tools (no game.json/playbook/checkpoints); its
  play, tour and screenshot tools are still its own. Merging the two toolchains is a separate job.

## 2026-11-17 - Dragon Quest (Famicom, English patch): main set
- game-capture: 67 shots from the logo to the staff roll (towns, shops, inn, caves with torch/Remira, 7 battles,
  Golem, green dragon, both Dragon King forms, death, full ending, password screens, the kana password grid via
  `rom:jp`), 27 new checkpoints, design docs combat/world/items-and-shops, commits d253e69, c131c6c.
  Techniques: poke position or map number during a map transition for clean warps.
- Coordinator: full `--verify` from an empty cache, 67/67 reproduce (about 15 min; the first attempt hit a
  10-minute command limit). Sheet reviewed.
- Open tool requests from the capture feedback: `play.py recaption`, a session clock in `play.py status`.
- Not captured: shop_keys, swamp, bridge, check_command, seq-rainbow clips, castle middle floors.

## 2026-11-17 - Dragon Quest (Famicom, English patch): intake, scout, NES frame fix
- Owner supplied the Japanese dump and an English translation IPS; the patched ROM is registered as
  `dragon-quest` (SHA-1s of dump, patch and result in game.json "source"; a `rom:jp` variant restores the
  original). game-scout: playbook, 9 checkpoints (title, password_entry, start, late and five late_* places),
  password helper `games/dragon-quest/tools/pw.py`, RAM map, 54-line shot plan. No battery: passwords only.
- Bug found by the scout, fixed: `lrcore.Core.image()` emulated one frame when no frame had been drawn (after
  loading a state into a new core), so cached and freshly built checkpoints differed by a frame. Screenshots
  no longer emulate; savestates carry the frame in a trailer. Test added (13 pass). Checkpoints rebuilt.

## 2026-11-17 - NES / Famicom backend (Mesen)
- Owner's request: an emulator for NES/Famicom games like the GB one. Checked FCEUmm and Mesen as libretro cores
  (both build headless here, deterministic, savestates round-trip); owner chose Mesen.
- `tools/setup_emu.sh [gb|nes]` builds libretro/Mesen at 0102910 with `tools/mesen-debug.patch`
  (retro_mesen_peek/poke/pc). `tools/lrcore.py`: ctypes libretro frontend. `platforms.Nes`: iNES/NES 2.0
  identification, ntsc/pal/dendy, private empty save directory per run, RAM search in Python, Game Genie as a
  ROM patch (8-letter; 6-letter only without bank switching), `gs:` refused. play.py export names the emulator
  of the `.state`. `.gitignore`: `*.nes`, `*.fds`, `tools/mesen/`.
- Tests: generated NES test ROM (`tests/make_nes_rom.py`, hand-assembled, no game data); header/Game Genie,
  backend, and the intake -> play -> snap -> export -> shoot --verify pipeline. 12 pass. ~700 fps.
- Open: first commercial NES game (scout + capture) will show what the docs and skills still assume about GB.

## 2026-11-15 - sequence file names carry the set name
- Owner's request: files of `seq-*` sets are prefixed with the set name (seq-fishing_01_shore.png,
  seq-fishing_full.gif, ...); ids unchanged; shoot.py/play.py add the prefix (shoot.prefix()). Pokémon Blue
  seq-fishing and seq-fly reshot under the new names (15/15, 9/9). Test checks no unprefixed media remain.

## 2026-11-15 - stitched sequence GIFs
- Owner's request: a full GIF per sequence with all steps stitched. `seq-*` sets now get full.gif / full@3x.gif
  (stills held, clips at game speed), rebuilt on publish. Pokémon Blue: seq-fishing 34 s (144 KB / 626 KB @3x),
  seq-fly 19 s (49 KB / 207 KB @3x). Test checks the stitched timing.

## 2026-11-15 - Pokémon Blue sequences: fishing, Fly
- game-capture: seq-fishing (Vermilion harbour: menu path, cast clip, bite, battle-transition clip, hooked
  Shellder, plus the "Not even a nibble!" branch) and seq-fly (Vermilion -> Lavender: party, FLY, town map,
  take-off and landing clips), commit 12fdafe; world.md: fishing outcome rules and Fly.
- Tools from its feedback: clip poster choice (`rec:N:K:P`, `record --poster`, numbered frame sheet), category
  check up front, passing --verify rebuilds index.md/strip/steps. Coordinator re-picked 4 posters; 15/15, 9/9.

## 2026-11-15 - action sequences and clips
- Owner's request: capture actions as sequences (fishing, Fly). Tools: `rec:N[:K]` token, `play.py record`
  (GIF clips at game speed, @3x, poster PNG), `seq-<action>` sets get strip.png + steps.gif, --verify compares
  every clip frame, publish copies GIFs. Image labels fold accents. Test added (9 pass).

## 2026-11-15 - Pokémon Blue main set, run 2
- game-capture: 42 new shots (92 total): Brock gym and badge, learn move, evolution, Surf, fishing, bicycle, Cut,
  Fly map, forest, Mt. Moon, Safari Zone, Game Corner slots, S.S. Anne, Pokémon Tower ghost, Silph Co.,
  Champion, Hall of Fame, credits, PC. Saves 04_pewter_boulderbadge, 06_hall_of_fame. Commits 41d507a, 5a4d0ea.
  Design docs extended (~45 claims), 3 findings. Coordinator: full --verify, both saves booted.
- Tools: snap reports UNCHANGED re-snaps; shoot.py --publish-only; emulator.md: pick animation frames in play.py.

## 2026-11-15 - Pokémon Blue main set
- game-capture: 50 shots published (boot to Elite Four Lorelei, menus, battles, catch, blackout, Mart, Center),
  design docs, saves 03_starter_lab and 05_elite_four_lorelei; commit 4d04ea9. Coordinator --verify rerun 50/50.
- Fixes: mkrecipe.py growth groups (3 medium slow / 5 slow) and EXP fraction, committed in
  games/pokemon-blue/tools/; MID macro EXP regenerated (LATE kept, LATE_EXP corrects it). play.py: snap refuses
  stale frames after goto/undo, reloads game.json on every do; shoot.py flushes progress lines.

## 2026-11-15 - Pokémon Blue scouted
- game-scout: playbook (controls, RAM map, sources: pret/pokered), macros TITLE/NEWGAME/CONTINUE/LATE/MID,
  checkpoints title/start/late, door-warp recipe, ~50-id shot plan, design README started; saves 01_start and
  02_late_game_test exported. Verified by the coordinator (replay without cache, both saves boot).
- Tools: RAM watches take `"fmt": "bcd"`; emulator.md: mash and blank-frame rules, undo depth.

## 2026-11-15 - milestone saves committed
- Owner's rule: commit the saves agents make, so the owner can jump in. `play.py export NAME "desc" [--state]`
  writes `games/<slug>/saves/NAME.sav` (+ SameBoy `.state`) and its README row; `.gitignore` exception added;
  `sav:NAME` finds these first. Test added (8 pass).
- Pokémon Blue registered (intake); game-scout running.

## 2026-11-15 - shortcuts, naming, design reference
- Owner's rules: cataloguing over fair play (cheat/hack freely, realistic values), main character "ryz", use
  saves/codes from the web, document systems in a design reference while playing.
- Tools: set:/gs:/freeze: tokens, rom: variants (Game Genie decoding checked against SameBoy's cheats.c; GameShark
  types against EnHacklopedia), sav: prefix, IPS; tests for all (7 pass, run without pytest: not installed).
- Templates: design/README.md (notation, confidence tags) and findings.md; playbook Naming and Saves sections.

## 2026-11-15 - pipeline set up
- New project `gamedb/`: generalised the Wizardry Empire photographer/playtester tooling for any GB/GBC ROM.
- Tools: platforms.py (backend registry), emu.py, play.py, shoot.py, intake.py; tests in tests/.
- Docs: emulator.md (general emulator rules), capture-guide.md (database categories and quality rules).
- Skills: game-scout (research -> playbook), game-capture (play -> set).
- Verified on cgb-acid2 and the gbemu test ROM: intake, checkpoint, snap, undo, RAM search, --verify (2/2
  reproduce), --publish. No game captured yet.
