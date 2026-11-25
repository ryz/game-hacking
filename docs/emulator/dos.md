# DOS

Platform notes for `dos` games (IBM PC, MS-DOS). The general rules (routes, tokens, the working loop) are in
[README.md](README.md). Added 2026-11-18. First game: Might and Magic Book One (`games/dos/might-and-magic/`), played from the title
into the first town; saving in the game has not been tried yet.

## Backend
DOSBox Pure, built as a libretro core and run inside the Python process by `tools/lrcore.py`. Built by
`sh tools/setup_emu.sh dos` at a pinned commit into `tools/dosbox-pure/` (from the libretro mirror on GitHub;
the author's own GitHub repository only points to Codeberg). `tools/dosbox-pure-debug.patch` adds:
- `retro_gamedb_set_time`: the emulated PC's date, BIOS tick counter and real-time clock follow a clock the
  driver sets (power-on is always 1990-01-01 00:00:00 and time advances with the emulated frames), not the host.
- `retro_gamedb_sync`: the core runs emulation on its own thread and lets it run ahead; the driver parks it at
  the end of every frame, so key presses and memory reads land at the same emulated moment on every run.
- `retro_gamedb_pc`: CS:IP for `status`.
- a fix in the savestate loader (the frame in progress was dropped, so a loaded run was one frame ahead).
- `retro_gamedb_flush`: write the save ZIP now (see Saves).
- `GamedbMarkWritten` in `src/dos/drive_union.cpp`: a write through a file that stays open marks it for the save
  ZIP at once (see Saves).
- `retro_gamedb_running`: whether a program runs (the launch log ends there); `retro_gamedb_readb`: one byte
  through the page handlers, for the text screen.

## Savestates
The core saves and loads a state only while a DOS program is running, not in its start menu or at the DOS
prompt. The backend covers both cases (`Dos.save_state` in `tools/platforms.py`):
- before a program runs, a "state" is the list of inputs since power-on; loading it powers on and replays them;
- a real state also stores the launch (the inputs from power-on to the first 10-frame step that ends with a
  program running, `retro_gamedb_running`; nothing later, or a load would repeat what the route wrote to disk:
  found by the Might and Magic scout as a duplicated character) and the files written so far; a machine where
  nothing runs yet (a new process loading a cached checkpoint), or whose written files differ, powers on with
  those files, replays the launch inputs, then loads the state.
So `undo`, `checkpoint`, `goto` and the cache work from power-on like on the consoles. A shot costs about a
second (measured on Might and Magic 1: 0.5-2 s; the launch replay is about 0.3 s of it; a machine that was
just opened plays the launch itself instead of powering on a second time). Only this tool reads
these files.

With the patch the same route gives the same frames on every boot, and a run loaded from a state continues exactly
like the run that made it (tests `test_dos_same_route_same_frames`, `test_dos_pipeline`). A machine that was
just opened runs 4 frames before its first state load; with fewer than 2 the timing differs.

## A game is a ZIP
`python3 tools/intake.py GAME.zip --region na [--slug S --title "T"]` (the region of the release; a ZIP has no header that says it): the ZIP of the game's folder is the dump (SHA-1 in
`game.json`, copied to `rom/<slug>.zip`, never committed); the game lands in `games/dos/<slug>/`. The ZIP is mounted as `C:`. Power-on shows DOSBox
Pure's start menu listing the programs in the ZIP; the boot route picks one (`w120,enter` for the first, `down`
to move). A ZIP with a single program starts it without the menu. The vault's boot check presses no key either: a game that
waits at this menu or at a still title needs `vault.py push ... --route BOOT` (its boot macro, or a key that starts
a demo). The files may sit in a folder inside the ZIP
(a GOG install folder works as it is, without its DOSBOX subfolder). CD images and installers are not set up yet.

**Read the game's own DOSBox config first** (GOG: `dosbox*.conf` / `*_single.conf` in the ZIP): its `cycles`
is the model's cycle count, and its `[autoexec]` may do more than start the program. Might and Magic II needs
`loadfix -4 mm2.exe` (started from the menu it prints "Not enough memory for 16 color version" and quits), so its
`BOOT` goes through "Go to Command Line": `w120,down,down,enter,w120,type:cd MIGHIC-2\n,w30,type:loadfix -4 mm2.exe\n`
(the folder has its DOS short name). The intake probe presses no key and cannot show such failures. GOG's
`mount ... -t overlay` of `cloud_saves` is not reproduced: the game reads the files in its own folder.

## Models
`game.json` "model" is `MACHINE[-CYCLES]`: machine `svga` (default), `vga`, `ega`, `cga`, `tandy`, `pcjr` or
`hercules`; cycles = emulated instructions per millisecond, fixed (default `7800`, about a 386DX-33; `315` =
4.77 MHz 8088, `1320` = 286-6, `2750` = 286-12). Auto cycles are not offered: they follow host speed. A game
from the early 1980s that runs too fast needs fewer cycles, not waits.

`cga` and `tandy` do not restore the CGA palette or mode registers on a state load (every screen turns cyan
after `goto` or a cached checkpoint); `ega`, `vga` and `svga` reload exactly. Use `ega` for CGA games until
this is fixed, and compare a frame before and after a state load when choosing the machine (Wizardry I,
2026-11-19: `ega-315`).

At low cycle counts disk loads are slow: Wizardry III's floor loads take 1,000-1,800 frames at 315 cycles, and
keys pressed meanwhile are lost (warp routes then fail silently). Use `change` or a long wait after a level
change.

## Screenshots
The picture has the size of the video mode: text mode 640x400, a 320x200 game 320x200 (that is what `emu.py`,
`shoot.py` and `play.py` write); it can change during a route. No aspect correction for 320x200 (shown 4:3 on a real monitor, close enough).
640x200 graphics (Infocom interpreters, CGA high resolution) is flattened 3.2:1: decided per game in `game.json`
"aspect" (owner's rule 2026-11-21): `rowdouble` writes 640x400 (each row twice, lossless), `native` keeps it. Without
a decision the tools warn and `shoot.py --publish` refuses: ask the owner. Beyond Zork: `rowdouble`.

Real-time games (Quake, 2026-11-23): start with no sound device (`-nosound`; with the Sound Blaster a loaded
state drifts on the next frame). Even then a loaded state followed by a key continues differently from the flat
replay (input timing not in the core's savestate): make checkpoint routes flat (no `@parent`) and check
`cachecheck` on a two-link chain before building more. Placing the player in a 3D level: build a spot finder from
the level data (fits, stands on the floor, line of sight) first; a teleport into a spot that does not fit is undone
by the game (Quake `tools/qpos.py`).
Wolfenstein 3D (2026-11-25): even flat checkpoint routes differ from the flat replay in actor memory after a
load (`cachecheck --show-diff N` shows where); shots built on such a checkpoint still reproduce (a miss reloads
its own state), so judge a real-time game's set by `shoot.py --verify`, not by cachecheck "memory" (cachecheck adds "cold == hit" where
that holds). Explore with `play.py do!` (no settle) once in play: a settle lets doors close and enemies fire
(Spear of Destiny, 2026-11-25).
The text cursor blinks, so text screens rarely `settle`; capture anyway.

## Keys
Keyboard keys by name: `a`-`z`, `0`-`9`, `f1`-`f12`, `enter esc space tab backspace delete insert home end
pageup pagedown up down left right`, `shift ctrl alt` (left) and `rshift rctrl ralt`, `minus equals comma period
slash semicolon quote leftbracket rightbracket backslash backquote`, keypad `kp0`-`kp9 kpplus kpminus kpmultiply
kpdivide kpperiod kpenter`. Chords as on consoles: `shift+a`, `alt>f4`.
- `w30` is still "wait 30 frames"; the W key is `w`, held longer `w:30`.
- `type:Some Text` types a string (US layout, shift handled; `\n` = Enter). A comma ends the token: `type:sailor,comma,type: hello\n`.
- Mouse: `mouse1 mouse2 mouse3` are buttons (tokens like keys), `mouse:DX:DY` moves the pointer relatively.

## Reading the screen as text
In a text mode `python3 tools/play.py text` prints the screen as text (in scripts: `emu.text()`, a list of
lines; None in a graphics mode). Use it instead of looking at a screenshot for DOS prompts, installers,
text-mode games. It reads video memory through the core (`retro_gamedb_readb`); `peek` still does not reach
`A0000-BFFFF`. Graphics-mode games draw their own letters (Might and Magic 1): no text to read there.

## Waiting
Cursor and animated screens never `settle`, and games buffer keys typed too early. Use `change` (emulator
guide, Tokens): `1,change:20` waits until the game has answered the key, however long that takes.

## Memory
The physical address space, address = segment * 16 + offset: `00000-9FFFF` conventional memory (interrupt
vectors, BIOS data area at `00400`, DOS, then the game), extended memory from `100000`. Video memory
(`A0000-BFFFF`) and ROM are not readable through `peek`. `find` covers `00500-9FFFF`. `status` shows CS:IP.
A game's addresses depend on where DOS loads it, which is the same on every boot with the same ZIP and model.
Z-machine games (Infocom): search for the story file's first header bytes to find the base of the game's
memory; Infocom's DOS interpreter keeps its own 2-byte word tables little-endian there, while object data (properties,
money) stays big-endian as in the story file (Beyond Zork, 2026-11-21).

## Saves
DOS games save to files on `C:`. DOSBox Pure keeps the changed files in a save ZIP; the backend gives every
power-on a private one, empty unless the route starts with `sav:NAME`, so each route starts from the pristine
game. Checked 2026-11-18 with Might and Magic 1 (signing in at an inn writes ROSTER.DTA) and with the test
program:
- A savestate holds the machine, not the disk, so the backend stores the written files with every state and
  puts them back on load (a state made before a save has no files, one made after it has them; `undo`,
  `goto` and cached checkpoints in a new process all see the right disk). `retro_gamedb_flush` in the core
  patch writes the save ZIP at once; the core alone writes it one emulated second after a change.
- `play.py export NAME "desc"` writes that ZIP as `games/dos/<slug>/saves/NAME.sav`. For the owner: unzip it
  and copy the files over the ones in the game folder (folders inside have DOS short names such as
  `MIGHIC-1/`). `sav:NAME` powers on with it.
- Might and Magic 1 keeps the roster in memory and reads ROSTER.DTA only when the program starts.
- Files a game keeps open (the Wizardry I-III loaders hold SAVEn.DSK all session): DOSBox Pure alone marks a
  file for the save ZIP only when it is closed, so such writes were missing from states until Leave game, and
  Wizardry II, which reads its roster back, showed old rosters after a cached checkpoint. Fixed 2026-11-19 in
  the core patch (`GamedbMarkWritten`: every write marks the file; test
  `test_dos_state_carries_writes_to_open_file`). States made with an older core keep the old behaviour: delete
  `work/cache/dos/<slug>` after rebuilding the core.
- Scouts check checkpoints on the disk too: save in the game after a cache hit and after an empty-cache
  rebuild and compare the written files (done for Might and Magic II, 2026-11-19).

## Not supported yet
CD-ROM images, installing a game inside the emulator, booting a real DOS or Windows, MIDI music devices, joystick.
