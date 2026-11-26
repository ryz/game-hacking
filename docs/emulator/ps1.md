# PlayStation

Platform notes for `ps1` games (PlayStation, all regions). The general rules (routes, tokens, the working loop)
are in [README.md](README.md). Added 2026-11-26 and checked with the test disc `tests/make_ps1_disc.py` (tests
`test_ps1_*`) on the free OpenBIOS. Not tried with a real game or a Sony BIOS yet: multi-disc games, analog
controllers, CD audio tracks, games that need the second memory card.

## Backend
Beetle PSX (Mednafen's PlayStation) as a libretro core, run inside the Python process by `tools/lrcore.py`. Built
by `sh tools/setup_emu.sh ps1` (about 3 min) at a pinned commit into `tools/beetle-psx/`, software renderer only
(`HAVE_HW=0`): the native picture, no GPU needed. The CPU runs in the interpreter (no dynarec), the GPU on the
emulation thread, the CD at native 2x speed, `cd_access_method` sync: the same route always gives the same frames,
and a loaded savestate continues exactly like the run that saved it (test `test_ps1_backend`, with input).
`tools/beetle-psx-debug.patch` adds `retro_gamedb_pc` and silences the core's info-level log.
Speed: about 300 frames per second on the test disc (a real game will be slower).

The target also installs `chdman` (apt `mame-tools`) and a MIPS cross compiler (apt `gcc/g++-mipsel-linux-gnu`),
and builds OpenBIOS from PCSX-Redux's MIPS tree (`tools/nugget/`, pinned).

## BIOS
A real PlayStation boots a game through its BIOS (Sony logo, then the disc). The core needs the BIOS of the
model's region in `rom/bios/` (never committed; the vault keeps it under `_system/ps1/`, like Amiga Kickstarts):

| Model | File name (the core's) | SHA-1 of the one the core expects |
|---|---|---|
| `ntsc-u` | `scph5501.bin` (also `scph5503.bin`, `scph7003.bin`) | `0555c6fae8906f3f09baf5988f00e55f88e9f30b` |
| `ntsc-j` | `scph5500.bin` | `b05def971d8ec59f346f2d9ac21fb742e3eb6917` |
| `pal` | `scph5502.bin` (also `scph5552.bin`) | `f6bc2d1f5eb6593de7d089c425ac681d6fffd3f0` |

A file with that SHA-1 is found under any name. Another BIOS version of the same region also boots when saved
under the file name (the core warns). Without the BIOS the backend refuses to start and says which file is missing;
it never falls back silently. `REGION-openbios` (`ntsc-u-openbios`) boots the free OpenBIOS instead: no Sony
logo, its own boot animation, fewer games run. It is for the tests; shots of real games use the real BIOS.

## Games
A game is one CHD file (`rom/<slug>.chd`). `tools/intake.py GAME.cue` converts a Redump-style `.cue` with its
`.bin` tracks into a CHD (`chdman createcd`) and records the original files (names, sizes, SHA-1s, as Redump lists
them) in `game.json` "source" "dump"; a `.chd` is registered as it is. The header in `game.json` comes from the
disc's `SYSTEM.CNF`: boot file, serial (`SLUS-01234`), volume id; the serial's third letter gives the region and
the model (`U` = `ntsc-u`, `P` = `ntsc-j`, `E` = `pal`). `.bin` alone is not taken (it is the Mega Drive's
extension); `.pbp`, `.iso`, `.m3u` are not set up. `--patch` is refused for discs: apply a translation patch to
the tracks with its own tool (usually xdelta), register the patched `.cue`, and keep the patch for the vault.

**Vault: discs over 100 MB do not fit.** GitHub refuses files over 100 MB and `vault.py push` refuses them; a
CHD of a full CD is usually 200-600 MB. Until the vault can store a disc (split into parts, or another store:
the owner's decision), a PlayStation game stays in the session's `rom/` only.

## Models
`ntsc-u` (North America, default), `ntsc-j` (Japan), `pal` (Europe, 50 Hz); each with the BIOS of its region.
Add `-openbios` for the free BIOS (tests only).

## Screenshots
The native frame of the game's video mode, the overscan cropped the same way every frame (`crop_overscan`
static): 320x240 in the common mode, 256x240, 368x240, 512x240, 640x240; 640x480 in interlaced high resolution
(both fields woven); PAL games up to 288 lines. No aspect correction: the pixels as the console makes them.
Enlarged copies only on demand (`tools/x3.py`).

A screenshot never advances emulation; savestates carry the frame on screen.

## Buttons
`cross circle square triangle l1 r1 l2 r2 start select up down left right`: a digital pad (SCPH-1080) in port 1.
Example: `cross`, `start:30`, `cross+right:60`. Analog sticks, the DualShock's L3/R3 and port 2 are not set up.

## Memory
CPU addresses, eight hex digits: `poke:800A1B2C=03E7`, `"addr": "800A1B2C"` in `game.json`; values are little
endian.
- `80000000-801FFFFF` main RAM (2 MB); the same RAM answers at `00000000-` and `A0000000-` and mirrors up to
  8 MB: write `8xxxxxxx` like game code and cheat codes do.
- `1F800000-1F8003FF` scratchpad (1 KiB of fast RAM; some games keep player values there).
- `find` (RAM search) covers main RAM and the scratchpad (2 MB: the first search takes about 1.5 s).
- Video RAM, sound RAM and the CD-ROM buffers are not reachable.
- `regs` gives the program counter at the frame end.

## Cheats
GameShark constant writes are held with `gs:` (written every frame, like the device): `gs:800A1B2C 03E7` (16 bit)
and `gs:300A1B2C 0063` (8 bit). Conditional codes (`D0`, `E0`, ...) are refused: hold the value with
`freeze:ADDR=HEX`.

## Saves
The battery save is memory card 1 (port 1, 128 KiB raw image, the `.mcr` format); `play.py export` writes it as
`.sav`, `sav:NAME` powers on with it inserted. Memory card 2 is not connected. A fresh card is what the core makes
(formatted, empty). `--state` adds a savestate that only this core build loads (`GAMEDB-PS1-STATE-1` header, the
core's state zlib-compressed: 17 MB raw, about 150 KB stored).
