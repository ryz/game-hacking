# Status - game database

Current snapshot; history in `progress-log.md`.

## Ready
- GB/GBC backend (gbemu-cli), ROM intake with header identification and a boot probe.
- NES/Famicom backend (2026-11-17): Mesen libretro core at a pinned commit, driven in-process by `tools/lrcore.py`;
  `.nes` cartridges, 256x240, models ntsc/pal/dendy, savestates, battery saves, full CPU-space peek/poke and PC
  (`tools/mesen-debug.patch`), RAM search, NES Game Genie. First game: Dragon Quest (Famicom, English patch), 2026-11-17: main set 67 shots, title to staff roll, 67/67
  verified from an empty cache. Open there: shop_keys, swamp, bridge, check_command, a rainbow-bridge clip set,
  the middle floors of the Dragon King's castle, a retake of commands_window (cursor blinked off). Not set up: Famicom Disk System, second controller, 6-letter Game Genie codes on
  bank-switched games.
- Owner-supplied patches (2026-11-17): `tools/patch.py` applies IPS, BPS and UPS (CRC checks, iNES/SNES copier
  header layout found from the CRC or given as `:headered`/`:unheadered`); `intake.py --patch` registers the
  patched ROM and records the source in game.json. Dragon Quest and SMT were patched before this by hand.
- Megami Tensei (Famicom, English BPS), 2026-11-18: main set 41 shots (intro, stats, battle, negotiation, Comp
  summon, fusion, sage password, shop, healer, status, Tyrant Minotaur encounter, game over), 41/41 verified.
  Open there: level-up (EXP poke did not trigger one), battle magic, a deeper floor, the Minotaur fight, a
  demon fighting, the ending (password format not decoded).
- Megami Tensei round 2 (2026-11-18): 88 shots through the ending, 35 floor maps, late password. Open: other
  sections' wall graphics after a warp, stairs prompt shot.
- Megami Tensei II round 2 (2026-11-18): 67 shots in game order, Pazuzu, fusion, shop, totem save, overhead maps.
  Still open: a CHAT join, automap, Nebro and later bosses, first-person maze maps.
- (round 1) Megami Tensei II (Famicom, English IPS), 2026-11-18: main set 36 shots (intro, naming, Devil Buster, battles,
  level-up, healer, Tokyo overworld, 3D cave, magic, computer room, save slots, shelter, game over), save
  01_computer_room. Open: Pazuzu, automap, a demon joining, summoning, fusion, shop, bosses; shots.txt not in game
  order; start_room retake. Some lines are untranslated by the patch (checked, not a layout error).
- `tools/dis6502.py` shared 6502 disassembler (2026-11-18).
- Dungeon Magic (NES), 2026-11-18: main set 41 shots, floor maps of all 39 floors + overworld, saves 01-02.
  Open: the King, camp, swords, bosses beaten, Darces, ending.
- Sets are ordered by `shots.txt` (game order), 2026-11-18.
- Wizardry I (NES), 2026-11-18: main set 71 shots through Werdna and the ending, 10 floor maps with all special
  squares decoded, saves 01-03. Open: Identify, spinner, teleport square; party_dead retake.
- `play.py dump/diff` (2026-11-18).
- Deep Dungeon III (Famicom, Japanese), 2026-11-18: main set 74 shots through the ending, 16 floors + 3 towns mapped
  with event squares, saves 01-02. Open: castle master, other towns' item shops/temples, lit cave.
- Macros with arguments (`WARP:a:b:c`), 2026-11-18.
- Might and Magic (NES), 2026-11-18: main set 93 shots through the ending, 55 maps with terrain and exits, saves
  01-03. Open: services in the other towns, spells above level 1, Bribe/Giveup.
- Wizardry II (NES), 2026-11-18: main set 91 shots through the ending, 6 floor maps with special types checked
  in play, saves 01-04. Open: Sell/Identify, darkness, spinner, level drain, floor 4 room fight.
- Queue: none. Every registered game has a set and maps; open items per game are in its status line above.
- Tokens incl. hold (`right:30`), mash, settle, macros, checkpoints as routes (cached per ROM).
- `play.py`: persistent session with undo, snap (capture + route), checkpoint/goto, RAM search, RAM watches.
- `shoot.py`: replay, `--verify` (pixel-exact reproduction), `--publish`; catalogue index.json/md + contact sheet.
- SNES/Super Famicom backend (2026-11-17): Mesen-S libretro core at a pinned commit, same driver as NES;
  `.sfc`/`.smc`, 256x224 (239-line and hi-res frames kept), models ntsc/pal, 12 buttons, 24-bit peek/poke and PC
  (`tools/mesen-s-debug.patch`), RAM search over work RAM, Pro Action Replay (`gs:`) and Game Genie. First game: Shin
  Megami Tensei (Super Famicom, English patches), 2026-11-17: main set 56 shots after two runs (boot to day 2:
  second dream, battles, level-up, game over, negotiation, automap; one hi-res frame), verified. Open there: no
  demon has joined (negotiation needs a Bead; item list not found in RAM), so no summoning, fusion or
  terminals; the second dream needs a flag poke (real trigger unknown). Special-chip games untested.
- Layout (2026-11-17): every game under `games/<platform>/<slug>/`, shared tools/tests/docs at the repo root; emulator
  guide split into general rules and one file per platform.
- Skills game-scout and game-capture with agent wrappers; docs `emulator/` and `capture-guide.md`.
- Shortcuts: `set:` (decimal/BCD values), `gs:` GameShark codes held like the device, `freeze:`, ROM variants
  (`rom:` with Game Genie / IPS / bytes, built in work/roms/), downloaded saves (`sav:` from rom/saves/).
- Action sequences (`seq-<action>` sets: strip.png, steps.gif) and GIF clips (`rec:N:K:P`, `play.py record`
  with poster choice).
- Per-game design reference (`games/<platform>/<slug>/design/`, written by scout and capture agents).
- Network: research hosts allowed in the environment (GameFAQs, TCRF, Data Crystal, StrategyWiki, Wikipedia,
  gamehacking.org, Kodewerx, archive.org). curl reached them from this session; WebFetch did not yet (may need a
  new session). GameFAQs/TCRF answer curl with 403 (bot protection): agents skip refusing sites.
- Tested end to end on SameBoy's cgb-acid2 and gbemu's generated test ROM (not committed).

- DOS backend (2026-11-18): DOSBox Pure libretro core at a pinned commit (`sh tools/setup_emu.sh dos`), driven
  by `tools/lrcore.py`; a game is a ZIP of its files (`intake.py GAME.zip`), keyboard and mouse tokens, `type:`,
  fixed cycles and a fixed emulated clock (same route = same frames), exact savestates, physical-memory
  peek/poke/find, CS:IP. First game: Might and Magic 1 (`games/dos/might-and-magic/`, GOG files), played from the title
  into Sorpigal with the stock party; 2 trial shots reproduce from an empty cache and from the cached checkpoint.
  In-game saving checked: written files travel with savestates, `play.py export` and `sav:` work (5 DOS tests).
  Scouted and captured 2026-11-18: main set 113 shots from the title to the Inner Sanctum ending text, 113/113
  verified from an empty cache by the coordinator; WARP macro (area change through Sorpigal's exit handler) and
  the table of all 55 areas; saves 01-03; design combat/world/characters/sorpigal. Open there: 39 areas not
  surveyed, the Astral door with a Key Card, the impostor fight, bash/trade/temple cure, statues 2-8; the ending
  was reached by position poke with a level-1 party. Open in the tools: CD images; `unsnap` needs a session;
  `--publish-only` orders by the game folder's shots.txt. Notes: `docs/emulator/dos.md`.

- Master System backend (2026-11-19): Genesis Plus GX libretro core at a pinned commit (`sh tools/setup_emu.sh
  sms`, ~11 s), driven by `tools/lrcore.py`; `.sms` cartridges (`games/sms/<slug>/`), 256x192, models
  ntsc/ntsc-j/pal (from the `TMR SEGA` header; headerless Japanese carts need `--region jp --model ntsc-j`), keys
  `b1 b2 pause`, savestates, 32 KiB cartridge-RAM `.sav` export and `sav:`, Z80-space peek/poke and PC
  (`tools/gpgx-debug.patch`), RAM search on work RAM, Pro Action Replay (`gs:`), Game Genie (`rom:` variant);
  3 tests on an original test ROM (`tests/make_sms_rom.py`). First game: Phantasy Star (US/EU, `games/sms/phantasy-star/`):
  main set 109 shots (three planets, Myau joining, bosses), battles 16 (4 in front of long corridors),
  looping movement GIFs (set `loops`, tools/loop.py), seq-dungeon-walk/turn/stairs/door,
  all verified cold; warp/dungeon/fight/party macros from decoded ROM tables. Open: the ending (Dark Falz
  trigger, likely floor 3B/3C squares coded 7), Noah joining, Odin's cure, vehicles in use, RUN/DRP, spells
  cast, a trap, milestone saves, battle retakes in the real boss rooms. Not set up: Game Gear,
  SG-1000, light gun/paddle, Reset button, Sega Card. Notes: `docs/emulator/sms.md`.

- Apple II backend (2026-11-18): AppleWin libretro core (audetto's Linux port) at a pinned commit
  (`sh tools/setup_emu.sh apple2`, needs cmake), driven by `tools/lrcore.py`; a game is a disk image or a ZIP of
  disk images (`intake.py`; `games/apple2/<slug>/`), `disk:N` / `disk2:N` change disks, keyboard tokens and
  `type:`, models `MACHINE[-VIDEO][-joy]` (default enhanced //e, colour TV), 560x384 pictures, peek/poke/find
  on the 64K the program sees, exact savestates that carry what the game wrote to its disks, `play.py export`
  and `sav:` (7 tests). First game: Might and Magic Book One (`games/apple2/might-and-magic/`, four sides in one
  ZIP): title, options menu (side 2), Sorpigal, wilderness (side 3), inn save; macros, 5 checkpoints, position RAM;
  inherited roster wiped and the standard party created (RYZ, CONDI, EBO, CUBI, DEDDO, MNZ; checkpoints `roster`,
  `party`, `signed_in`); set `main` of 308 shots: the DOS set's routes replayed here (231 of its 250 shots: every command, about 45
  monster groups, the other towns, quests, chests) plus this version's own (disk prompts, one view of each of the
  55 areas, ending); verified from an empty cache, published; three lens documents, `tools/lenses.py` clean. Area warp, strong-party and ending shortcuts
  in the playbook. Not scouted,
  side 4 not reached. Open: reset keys, write-protected disks, hard disk images with a real game, held keys/auto-repeat.
  Notes: `docs/emulator/apple2.md`.
- Amiga backend (2026-11-20): PUAE (libretro-uae) core at a pinned commit (`sh tools/setup_emu.sh amiga`, 90 s),
  driven by `tools/lrcore.py`; a game is an `.adf`/`.adz`/`.dms` or a ZIP of them (`intake.py`;
  `games/amiga/<slug>/`), `disk:N` / `disk2:N` change disks, models `MACHINE[-ntsc][-aros][-dfN]` (default A500,
  PAL), joystick (port 2), mouse (port 1) and keyboard tokens, `type:`, picture follows the screen mode (lores
  360x287 PAL), peek/poke/find on the 24-bit address space, exact savestates that carry what the game wrote to
  its disks, `play.py export` and `sav:` (6 tests, on the core's built-in AROS Kickstart with an A1200).
  `tools/puae-debug.patch` makes a loaded state continue on the exact frame (the core ran a frame inside its
  state load) and fixes a crash of the core without a frontend log interface. No game registered yet; real
  games need the owner's Kickstart ROMs in `rom/kickstart/` (1.3 for the A500). Not supported: `.ipf`, hard
  disk/WHDLoad, CD32/CDTV, write-protected disks. Notes: `docs/emulator/amiga.md`.

- Wizardry I-V on the Apple II (2026-11-19, queue halted by the owner after two games' worth of work):
  **I** scouted and captured (`games/apple2/wizardry/`: `main` 304 shots to the ending incl. 13 plain maze views,
  lenses clean; `start` 47 shots, the early game to the first save). **II** scouted, not
  captured (`games/apple2/wizardry-2/`: transfer from I works, 39 checkpoints to the ending; next step: dispatch
  game-capture; its disk 2 carries four characters of an earlier player that the routes delete). **III, IV, V**
  registered only (next step for III: game-scout with `rom/saves/apple2/wizardry-3/00_transfer.sav`). Dumps and
  transfer disks are in this container only (`rom/apple2/`, `rom/saves/apple2/`): a new container needs the
  owner's five ZIPs again, and the transfer disks rebuilt from the `final` checkpoints (`tools/transfer.py` in
  each game folder).
- Apple II backend additions (2026-11-19): write-protected disks (model suffix `wpN`), extra disks through a
  `sav:` ZIP (character transfer), dumps in `rom/<platform>/` and uncommitted saves in
  `rom/saves/<platform>/<slug>/` when a slug exists on several platforms, `play.py export` keeps disk-image
  saves out of the repo. Open requests from the agents: `play.py text` for the Apple II text screen, a shared
  checkpoint cold-check with a contact sheet, a duplicate check in `shoot.py --only`.

- Games grouped by platform (2026-11-18): `games/<platform>/<slug>/`, folder = game.json "platform"; tools take
  `slug` or `platform/slug`; work directories are `work/<kind>/<platform>/<slug>/`. The same slug may exist on two
  platforms (`nes/might-and-magic`, later `dos/might-and-magic`).

## File names and slugs (2026-11-18)
- Shot files: `<game>_<platform>_<region>_<area>_<id>[.<set>].<ext>`, built by the tools (`docs/capture-guide.md`,
  "File names"). Every `game.json` has `region` (`jp`/`na`/`eu`). All published sets are renamed.
- Slugs carry no platform: `wizardry`, `wizardry-2` (were `wizardry-nes`, `wizardry-2-nes`). Local `rom/` and
  `work/` copies under the old names must be renamed by hand (`rom/wizardry.nes`, `rom/wizardry-2.nes`,
  `rom/saves/<slug>/`, `work/*/nes/<slug>/`).
- Open: `shoot.py SLUG SET --verify` of the renamed sets has not been run (no dumps in the session that renamed
  them); working sets in `work/shots/` are renamed by the next `shoot.py` run.

- Three lenses (2026-11-18): templates `design/systems.md` (game design), `design/interface.md` (UI/UX) and
  `design/content.md` (variety of content), `tools/lenses.py` coverage check, capture skill step 6. First game
  with the three documents: Might and Magic 1 (DOS), 2026-11-18 (250 shots: 202 / 201 / 177 used, 219 in two or
  more). The other games have none yet. Earlier note: Might and Magic 1
  (DOS) is the first, written in capture round 2. Breadth rule in the capture skill (same day).

- Might and Magic II (DOS, GOG), 2026-11-19: main set 228 shots from power-on to the Congratulations ending,
  228/228 verified by the coordinator, three lenses 147 / 109 / 121 (133 in two or more), saves 01-04. Boots via
  the command line with `loadfix -4` (GOG's autoexec), model `svga-8000`. Open: hireling hire, Cartographer
  automap, elemental shrines and lords, bashing a locked door, time travel by the game's own means (YEAR poke
  used), temple cure and spell purchase transactions. Tool wishes: `goto` rebuild after a macro edit,
  `play.py checkpoint` replacing a line in place, intake recording a DOS ZIP's dosbox.conf autoexec and cycles.
- Wizardry I (DOS), 2026-11-19: main set 208 shots from power-on to the ending (Werdna beaten on screen without
  pokes), 208/208 verified by the coordinator from an empty cache, three lenses 117 / 141 / 135, ten floors
  decoded from the disk, items.md, saves 01-03 (03_werdna_beaten = Wizardry II transfer source). Model
  `ega-315`. Open: Murphy's ghost and the keys (floor 1 statues never offer a search), spinner, criticals,
  stoning, body recovery. Backend gap found here (writes through a file the game keeps open missing from states)
  fixed 2026-11-19 (5310311); both DOS sets re-verified with the new core.
- Wizardry II (DOS), 2026-11-19: main set 212 shots from power-on to the knights (the Wizardry I party
  imported through Move characters, five guardians with their drops, sphinx, Gnilda's test, Staff,
  Congratulations), 213/213 verified by the coordinator from an empty cache before dropping `save_leave_game`
  (emulator overlay), three lenses 166 / 190 / 113, saves 00-03 (03 = Wizardry III transfer source). Open: floor
  2 (16,3) room (doors open outward only), floor 6 fixed fight, spinners, stones.
- Tool to build (third request, MM2 / Wizardry I / Wizardry II captures): a shared shot previewer (try.py-style
  parallel runs with shoot.py's final settle, plan-file input, `--frames` counted from a marker token, paged
  timelines) and a duplicate check in `shoot.py --only`.
- Wizardry III (DOS), 2026-11-19: main set 228 shots from power-on to the stars (the Wizardry II party legated,
  both halves and guardians, the Neutral Crystal made in play through E)quip's invoke, orb, Congratulations,
  Queen Beyki), 228/228 verified by the coordinator from an empty cache after a route fix, three lenses
  192 / 193 / 118, saves 00-03. Floor gates verified: any good member admits to 2/4, any good member is refused
  on 3/5, all-neutral enters all. Open: Abdul's sale and coffer (floor 5), floor 6 dragon room fight.
- Tool fixed 2026-11-19: `play.py do`/`sample` roll back when a token fails (a failed `do` had left its earlier
  presses in the machine but not in the route). Capture skill: final verify from an empty cache.
- Ultima I (DOS, GOG), 2026-11-19: main set 195 shots from power-on to the ending text, 195/195 verified by the
  coordinator from an empty cache, three lenses 157 / 104 / 127, saves 01-03. Model `svga-500`. Open: starbase
  docking and ship choice, pub seduction, bard/jester songs, Steal spell.
- Ultima II (DOS, GOG), 2026-11-19: main set 226 shots from power-on to the ending text (Minax killed without
  pokes), 226/226 verified by the coordinator from an empty cache, three lenses 164 / 72 / 152, saves 01-03.
  Model `svga-500`. Open: Up ladder and Blink spells, fleeing, natural-kill loot.
- Ultima III (DOS, GOG), 2026-11-19: main set 260 shots from power-on to the ending text, 260/260 verified by
  the coordinator from an empty cache, three lenses 189 / 100 / 115 plus design/rules.md, saves 01-03. Model
  `svga-300`. Open: Surmandum failing into ashes, lava damage without the Mark of Fire, starvation and poison
  per turn.
- DOS queue (owner, 2026-11-19): done (Might and Magic II, Wizardry I-III, Ultima I-III). Tool wishes still
  open: shared shot previewer with duplicate check per batch; `goto` rebuilding a checkpoint whose route
  changed; `recaption` updating the game's shots.txt; little-endian BCD watch; intake recording a DOS ZIP's
  dosbox.conf autoexec and cycles. (import characters from
  the previous game's SAVEn.DSK), then Ultima I, II, III (GOG; cycles 500/500/300 in GOG's configs).
- Might and Magic 1 (DOS), state after the fix-up round (2026-11-18): 249 shots, 249/249 verified in one run
  from an empty cache by the coordinator, no identical pictures, no caption over 80 characters. Round 2 before
  it: 250 shots (after the memory leak fix in `tools/lrcore.py`). Open there: surprise message, search find,
  rest interrupted, surrender accepted, impostor, Eye of Goros, Astral door, wall sets decoded from WALLPIX.DTA,
  Fire Ball hitting the party (unexplained). Tool wishes open: `unsnap` without a session, old file dropped when
  a shot's id or category changes, contact sheet in pages above about 100 shots.

## Games
| Slug | Title | Playbook | Sets |
|---|---|---|---|
| pokemon-blue | Pokémon Blue Version (USA, Europe) | scouted + first capture 2026-11-15; design docs battle, pokemon, progression, world, economy, findings | main: 92 shots (verified 92/92); sequences seq-fishing (15), seq-fly (9) with GIF clips; saves 01-06 (start, late test, starter lab, Boulder Badge, Lorelei, Hall of Fame) |

## Next
- **DOS handoff (2026-11-18, from the session that built the backend; nothing below is started):**
  1. DONE 2026-11-18 (fix-up round, 249 shots). Was: three pixel-identical pairs (`sorpigal_inn_sign`/`encounter_retreat`,
     `temple_price`/`temple_poisoned`, `trap_door_after`/`dungeon_darkness`: retake the second of the first two,
     drop the third); 33 captions over 80 characters; macros `LOWHP` and `WORTHY` use the wrong record spacing
     (0x7F, real 0x80): correct them as new macro names and retake `death_party_down`, `gameover`, `ending_*`.
  2. DONE 2026-11-18: `shoot.py` lists identical pictures and long captions at `--verify`, refuses identical
     pictures at `--publish` (`--allow-duplicates`), `--prune`, sheets of 100, lens report at publish;
     `play.py unsnap --game` without a session.
  3. DONE (measured instead of rebuilt) 2026-11-18: a shot costs about a second, the launch replay 0.3 s of it;
     removed the second power-on per shot. Starting without the menu was not worth building.
  4. DONE 2026-11-18: `make_dos_zip.build(menu=True)`, `test_dos_start_menu_states`.
  5. DONE 2026-11-18: token `change[:N]` (emulator guide). Not yet used in any published route.
  6. DONE 2026-11-18: `play.py text` / `emu.text()` for text modes. Not tried on a real text-mode game.
  7. Untested on DOS: mouse tokens, a game with CD image or installer, machines other than `svga`, cycles other
     than 1500, a game that needs a sound card choice. Expect work with the first game that needs each.
  8. Scout rules worth promoting once seen a second time (open in `skills/game-scout/feedback.md`): check a
     record table's spacing on the second and the last entry, not only the first; extend the empty-cache
     check to the disk for games that save to files.
  9. DECIDED 2026-11-18: no setup script. The owner keeps one session per platform, so each session builds its
     one emulator on demand: `sh tools/setup_emu.sh gb|nes|snes|sms|dos|apple2|amiga` (clean builds: 9, 57, 53, 11, 32, 78, 90 s;
     all five 203 s). A script building all five was saved and removed again the same day.
  10. Content: the other ten games have no systems/interface/content documents; Might and Magic 1 now exists
      on NES, DOS and Apple II, a comparison of the three versions is possible from the existing sets.
- Pokémon Blue leftovers (optional): trainer "!" spotting, a PC box with Pokémon, Safari BAIT, stone evolution,
  Rocket Hideout; the MID recipe has never been shown on screen.
- `--model sgb` hangs on the SGB transfer screen (Pokémon Blue, pc=20b4): gbemu-cli SGB handshake; until fixed,
  capture in dmg.
- Routes using a macro change silently when the macro is edited: freeze macros once used in published shots
  (copy as a new macro name instead of editing), or store expanded routes in index.json.
- First real game through the whole pipeline; promote its lessons into `docs/emulator/` and the skills.
- More platforms: a backend per system in tools/platforms.py (candidates: stable-retro / libretro cores for
  NES, SNES, GBA, Genesis; needs a pip install approved by the owner).
- Optional: a database export step once the target schema is known.
