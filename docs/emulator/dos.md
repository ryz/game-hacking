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

## Savestates
The core saves and loads a state only while a DOS program is running, not in its start menu or at the DOS
prompt. The backend covers both cases (`Dos.save_state` in `tools/platforms.py`):
- before a program runs, a "state" is the list of inputs since power-on; loading it powers on and replays them;
- a real state also stores the inputs that started the program and the files written so far; a machine where
  nothing runs yet (a new process loading a cached checkpoint), or whose written files differ, powers on with
  those files, replays the launch inputs, then loads the state.
So `undo`, `checkpoint`, `goto` and the cache work from power-on like on the consoles. Only this tool reads
these files.

With the patch the same route gives the same frames on every boot, and a run loaded from a state continues exactly
like the run that made it (tests `test_dos_same_route_same_frames`, `test_dos_pipeline`). A machine that was
just opened runs 4 frames before its first state load; with fewer than 2 the timing differs.

## A game is a ZIP
`python3 tools/intake.py GAME.zip [--slug S --title "T"]`: the ZIP of the game's folder is the dump (SHA-1 in
`game.json`, copied to `rom/<slug>.zip`, never committed); the game lands in `games/dos/<slug>/`. The ZIP is mounted as `C:`. Power-on shows DOSBox
Pure's start menu listing the programs in the ZIP; the boot route picks one (`w120,enter` for the first, `down`
to move). A ZIP with a single program starts it without the menu. The files may sit in a folder inside the ZIP
(a GOG install folder works as it is, without its DOSBOX subfolder). CD images and installers are not set up yet.

## Models
`game.json` "model" is `MACHINE[-CYCLES]`: machine `svga` (default), `vga`, `ega`, `cga`, `tandy`, `pcjr` or
`hercules`; cycles = emulated instructions per millisecond, fixed (default `7800`, about a 386DX-33; `315` =
4.77 MHz 8088, `1320` = 286-6, `2750` = 286-12). Auto cycles are not offered: they follow host speed. A game
from the early 1980s that runs too fast needs fewer cycles, not waits.

## Screenshots
The picture has the size the core outputs for the video mode: text mode 640x400, and a 320x200 game came out
as 960x600 (Might and Magic 1: each pixel 3x3); it can change during a route. No aspect correction (320x200 was shown 4:3 on a real monitor).
The text cursor blinks, so text screens rarely `settle`; capture anyway.

## Keys
Keyboard keys by name: `a`-`z`, `0`-`9`, `f1`-`f12`, `enter esc space tab backspace delete insert home end
pageup pagedown up down left right`, `shift ctrl alt` (left) and `rshift rctrl ralt`, `minus equals comma period
slash semicolon quote leftbracket rightbracket backslash backquote`, keypad `kp0`-`kp9 kpplus kpminus kpmultiply
kpdivide kpperiod kpenter`. Chords as on consoles: `shift+a`, `alt>f4`.
- `w30` is still "wait 30 frames"; the W key is `w`, held longer `w:30`.
- `type:Some Text` types a string (US layout, shift handled; no comma inside, `\n` = Enter).
- Mouse: `mouse1 mouse2 mouse3` are buttons (tokens like keys), `mouse:DX:DY` moves the pointer relatively.

## Memory
The physical address space, address = segment * 16 + offset: `00000-9FFFF` conventional memory (interrupt
vectors, BIOS data area at `00400`, DOS, then the game), extended memory from `100000`. Video memory
(`A0000-BFFFF`) and ROM are not readable through `peek`. `find` covers `00500-9FFFF`. `status` shows CS:IP.
A game's addresses depend on where DOS loads it, which is the same on every boot with the same ZIP and model.

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

## Not supported yet
CD-ROM images, installing a game inside the emulator, booting a real DOS or Windows, MIDI music devices, joystick.
