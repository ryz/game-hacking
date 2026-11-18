# Progress log - game database

Append-only, newest first.

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
