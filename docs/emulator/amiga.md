# Amiga

Platform notes for `amiga` games (Amiga 500 to 4000, floppy games). The general rules (routes, tokens, the
working loop) are in [README.md](README.md). Added 2026-11-20. No real game registered yet: everything below
was checked with the test disk `tests/make_amiga_adf.py` (tests `test_amiga_*`), not with a commercial game.

## Backend
PUAE (libretro-uae), built as a libretro core and run inside the Python process by `tools/lrcore.py`. Built by
`sh tools/setup_emu.sh amiga` (about 90 s) at a pinned commit into `tools/puae/`. `tools/puae-debug.patch`:
- A loaded savestate continues exactly like the run that saved it. The core used to finish a restore by
  emulating inside `retro_unserialize` (the old machine up to its next vsync, then a frame of the loaded one), so
  a loaded state ran one frame ahead. Now the restore happens at the start of the next frame, before the CPU runs.
- The battery-backed clock reads an emulated clock (1990-01-01 00:00:00 at power-on, following the frames), not
  the host's. The emulator's random seed is fixed (1) by the core already.
- A restore takes its disk images from this machine's own folder (`retro_gamedb_disk_dir`): a state names the
  images by full path, and every machine works on private copies in its own temporary folder.
- `retro_gamedb_peek/poke/pc`, `retro_gamedb_insert` (disk into a drive or out), `retro_gamedb_flush` (write
  buffered disk writes to the image files), `retro_gamedb_set_time`.
- The core's fallback logger crashed (it wrote to `stderr`, which the core's VFS build defines as 0) whenever the
  frontend offers no log interface; it is silent now unless `GAMEDB_CORE_LOG` is set.

Checked (tests `test_amiga_*`): two power-ons give the same frames and chip RAM; a run continued after a
savestate equals one loaded from it, into a machine that has not run yet and into a busy one; a state saved
again before any frame has run is the same file. Speed: about 330 frames per second on the A1200 test machine
(6-7 times real time); the cycle-exact A500 is slower.

## Kickstart
A real Amiga needs its Kickstart ROM, which is copyrighted and never committed. Put your dumps into
`rom/kickstart/` (ignored by git), under PUAE's names or the Amiga Forever names; files with other names are
found by SHA-1:

| Machines | Kickstart | File name | Amiga Forever name |
|---|---|---|---|
| A500, A500OG, A500ECS, A2000OG | 1.3 (34.5) | `kick34005.A500` | `amiga-os-130.rom` |
| A500PLUS | 2.04 (37.175) | `kick37175.A500` | `amiga-os-204.rom` |
| A600, A600OG, A2000 | 3.1 (40.63) | `kick40063.A600` | `amiga-os-310-a600.rom` |
| A1200, A1200OG | 3.1 (40.68) | `kick40068.A1200` | `amiga-os-310-a1200.rom` |
| A4030, A4040 | 3.1 (40.68) | `kick40068.A4000` | `amiga-os-310-a4000.rom` |

The SHA-1s are in `Amiga.KICKSTARTS` (`tools/platforms.py`). Encrypted Amiga Forever ROMs (with `rom.key`) are
not supported: decrypt them first. Without a Kickstart, `-aros` in the model uses the free AROS replacement
built into the core: it boots bootblock disks on the A1200 (the tests use `A1200-aros`), not on the A500
presets, and many games will not run on it. Use a real Kickstart for anything you capture.

## A game is a floppy image or a ZIP of them
`python3 tools/intake.py GAME.adf --region eu [--slug S --title "T"]` (the region of the release: a disk image
does not say it), or `intake.py GAME.zip` for a game on several disks. Formats: `.adf` (plain), `.adz` (gzipped
ADF, unpacked when the game starts), `.dms` (packed; the core unpacks it in memory, so what the game writes to
it is lost: convert it to `.adf` if the game saves to that disk). A ZIP that holds only such files is an Amiga
game; its images are the disks in name order (`Disk 1.adf`, `Disk 2.adf`), listed in `game.json` "header" with
their SHA-1s, boot block type and volume name. The volume name of disk 1 becomes the title when `--title` is
not given. The game lands in `games/amiga/<slug>/`, the dump in `rom/<slug>.<ext>` (never committed).
- Disk 1 is in DF0: at power-on. `disk:N` puts disk N into DF0:, `disk2:N` into DF1: (`disk3`, `disk4` do not
  exist as tokens; `emu.disk(n, drive)` takes drives 1-4), `disk:0` empties the drive. A disk is in one drive at
  a time.
- The drive reports a swap after the usual delay, like a person changing disks: give the game a second or two
  (`w100`) before pressing on.
- Only DF0: exists unless the model says `-dfN` (below). Many games use DF1: when it is there.
- The emulator works on private copies: the game can write to every disk, the registered dump never changes.
- Not supported: `.ipf` (needs the SPS capsimg library), hard disk images and WHDLoad packages (`.hdf`, `.lha`),
  CD32 and CDTV discs.

## Models
`game.json` "model" is `MACHINE[-ntsc][-aros][-dfN]`, default `A500`:
- machine: PUAE's presets (Kickstart and memory as the core labels them): `A500OG` (1.3, 0.5M chip), `A500`
  (1.3, 0.5M chip + 0.5M slow: most games), `A500ECS` (1.3, 1M chip), `A500PLUS` (2.04, 1M chip), `A600OG`
  (3.1, 2M chip), `A600` (3.1, 2M chip + 8M fast), `A1200OG` (3.1, AGA, 2M chip), `A1200` (3.1, AGA, 2M chip +
  8M fast), `A2000OG` (1.3, 0.5M chip + 0.5M slow), `A2000` (3.1, 1M chip), `A4030`, `A4040`. Try `A500OG`
  when an old game fails with the slow RAM, an `A1200` preset for AGA games.
- `ntsc`: a 60 Hz NTSC machine (shorter picture). Default PAL, 50 Hz: most Amiga games are European.
- `aros`: the built-in AROS Kickstart instead of a real one (see Kickstart).
- `dfN` (N = 1-3): drives DF0: to DFN:. Default DF0: only, like a stock A500/A1200. A savestate holds the
  machine with its drives: it loads only into a machine with the same number.

## Screenshots
The picture follows the screen mode: a lores game is 360x287 (PAL) with the overscan border, one pixel per
Amiga pixel; a hires screen (Workbench, some menus) is 720 wide; interlaced screens have twice the lines. NTSC
machines have fewer lines. 24-bit colour, so the Amiga's 12-bit colours are exact (channel x 17). The status
bar, floppy sounds and the core's hotkeys are switched off.

## Keys
- Keyboard: `a`-`z`, `0`-`9`, `f1`-`f10`, `enter esc space tab backspace delete help`, cursor keys
  `up down left right`, `minus equals comma period slash semicolon quote leftbracket rightbracket backslash
  backquote`, modifiers `shift rshift ctrl alt ralt lamiga ramiga capslock`, keypad `kp0`-`kp9 kpperiod kpenter
  kpplus kpminus kpmultiply kpdivide kplparen kprparen`. `type:Some text` types a string with shift where needed
  (US layout).
- Joystick in port 2: `joyup joydown joyleft joyright fire fire2` (`fire+joyright:30` = run right while firing).
  The cursor keys are the keyboard's, not the joystick's.
- Mouse in port 1: `mouse1` (left button), `mouse2` (right button), `mouse:DX:DY` moves it. One unit is one
  count of the Amiga's mouse counter (one lores pixel in most games); large moves arrive over a few frames, so
  wait a few frames before clicking.
- Ctrl + both Amiga keys (`ctrl+lamiga+ramiga`) should be the keyboard reset, as on the real machine (the core
  implements it; not tried yet).
- `w30` is "wait 30 frames" (`w` is the W key on its own).

## Memory
`peek`, `poke`, `find` and `dump` use the 68000 address space (24 bit): chip RAM from `000000` (512K on the
A500, 2 MB on the A1200), slow RAM at `C00000` (A500: 512K), fast RAM at `200000` when the model has it, the
Kickstart ROM at `F80000`. Custom chips (`DFF000`) and CIAs (`BFE001`, `BFD000`) are not memory: they read as 0
and cannot be poked (no side effects). `poke` writes RAM only. `find` covers chip, slow and fast RAM. `status`
shows the program counter. Game data on an Amiga often moves (the game allocates memory from the system): find
a value again after a reload instead of trusting a fixed address from another run.

## Saves
Amiga games save to a floppy (often a save disk the game formats, or the game disk itself). A savestate holds
the machine, the disk images are files, so the backend stores the changed parts of the images with every state
and puts them back on load: a state made after an in-game save still has the save on disk, in the same process
and in a new one (`test_amiga_disks`).
- `play.py export NAME "desc"` writes a ZIP of the whole images the game has written to, under their names from
  the game's ZIP (`disk.adf` for a single-image game). Like the Apple II, it is game data (whole disks):
  `play.py export` writes it to `rom/saves/amiga/<slug>/` (uncommitted) and only its line in
  `games/amiga/<slug>/saves/README.md` is committed; `sav:NAME` powers on with it.
- An image in the `sav:` ZIP whose name is not one of the game's disks becomes an extra disk after the game's
  own (a save disk: `disk2:3`). A game that wants a blank disk to format: put an empty 880 KiB `.adf` into the
  `sav:` ZIP under a new name.
- Only this tool reads the `.state` files.

## Not supported yet
Write-protected disks, `.ipf`/hard disk/WHDLoad/CD games, a joystick in port 1 or a second player, CD32 pads,
analogue controllers, the Action Replay cartridge. Untested with a real game: everything (first game wanted).
