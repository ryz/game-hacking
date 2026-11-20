# Mega Drive / Genesis

Platform notes for `md` games (Sega Mega Drive and Genesis cartridges). The general rules (routes, tokens, the
working loop) are in [README.md](README.md).

## Backend
Genesis Plus GX, the same core and build as the Master System ([sms.md](sms.md)), run inside the Python process by
`tools/lrcore.py`. Built by `sh tools/setup_emu.sh md` (~15 s; `sms` builds the same thing) at a pinned commit into
`tools/gpgx/`; `tools/gpgx-debug.patch` adds side-effect-free access to the 68000 address space and its program
counter (`retro_gamedb_peek68k/poke68k/pc68k`) next to the Z80 functions the Master System uses. One process runs
one game; parallel sessions use `play.py --name`. ROMs: `.md`, `.gen`, `.bin` (plain, not interleaved; an `.smd`
copier dump is refused by `intake.py`: convert it first). The backend always starts the Mega Drive hardware,
whatever the extension. No TMSS boot ROM: the cartridge starts at power-on. Special cartridges the core knows
from its own database (bank-switched games over 4 MiB, EEPROM saves, Virtua Racing's SVP chip) work without
setup. Deterministic: the same route always gives the same frames (test `test_md_backend`).

## Models
- `ntsc`: Genesis (North America), 60 Hz.
- `ntsc-j`: Japanese Mega Drive, 60 Hz.
- `pal`: European Mega Drive, 50 Hz.

The model is the console region the game reads from the version register; region-locked games refuse the wrong
one with their own message. `game.json` "model" comes from the header's region field (`1F0`, old letters `JUE`
or a new-style hex digit): any North America gives `ntsc`, else Japan gives `ntsc-j`, else Europe gives `pal`.
The header region names more than one release for most games, so `intake.py` needs `--region jp|na|eu` (where
the dump was released) unless the header names one; set `--model` when the dump's release differs from the
default pick (a European dump of a `JUE` game: `--region eu --model pal`).

## Screenshots
320x224 for most games (H40 mode), 256x224 for games in the narrow H32 mode, the raw frame, no filter, no border.
Enlarged copies only on demand (`tools/x3.py`, nearest neighbour).
- A game can switch modes between screens (a 256-wide title, a 320-wide game), so a set can hold both widths
  (Sword of Vermilion: the name keyboard is 256 wide, the rest 320).
- PAL games in the 240-line mode give 320x240. Interlaced screens (two-player split screens) are one field:
  320x224, as the core renders them.

A screenshot never advances emulation; savestates carry the frame on screen.

## Buttons
`a b c start up down left right` (three-button pad, player 1), plus `x y z mode` for games whose header I/O
field (`190`) lists the six-button pad (`6`): the core gives those games a six-button pad and every other game a
three-button one, as the console would with a pad the game supports. `game.json` "header" "six_button" says
which. Example: `start`, `c:30`, `b+right:60`. The console's Reset button is not mapped.

## Memory
The 68000 address space, six hex digits: `poke:FF0123=09`, `"addr": "FF0123"` in `game.json`.
- `FF0000-FFFFFF` work RAM (64 KiB; the console mirrors it from `E00000`, write the `FFxxxx` form).
- `A00000-A03FFF` the Z80's 8 KiB RAM (mirrored at `A02000`): sound drivers, some games' variables.
- `000000-3FFFFF` ROM; cartridge RAM where the game maps it (usually `200000-20FFFF`, a byte at every odd
  address on most cartridges: `200001`, `200003`, ...).
- `peek` has no side effects and refuses I/O, VDP and open-bus addresses (reading those would change the
  hardware's state); `poke` writes work RAM, Z80 RAM and mapped cartridge RAM only (ROM is an error).
- `find` (RAM search) covers the 64 KiB of work RAM. `find --wide` compares 16-bit words, big-endian.
- **Byte order is big-endian (68000).** RAM watches (`"size": 2`, `"fmt": "hex"`) and `set:FF0040=300:2` use it by
  default; write `:le` / `"fmt": "le"` only for the rare little-endian value.
- Video RAM, colour RAM and the VDP registers are not reachable.

## Cheats
- **Pro Action Replay** (`AAAAAA:VVVV`): a RAM code is held with `gs:AAAAAA:VVVV` (written every frame, like the
  device). An even address takes the word `VVVV` (high byte included), an odd address the byte `VV`. Also
  `freeze:FF0123=09`.
- **Game Genie** (`ABCD-EFGH`): a word patch at an even ROM address, in a `rom:` variant (`game.json`
  `"rom_variants": {"gg": {"gg": ["ABCD-EFGH"]}}`). The ROM file offset is the address (no paging below 4 MiB).
  Decoding is the core's own (`test_md_header_and_cheats` checks two codes against it).

## Saves
`play.py export` writes the core's whole cartridge RAM buffer as a 64 KiB `.sav` (bytes the game never wrote are
`FF`; the export refuses when the game wrote nothing). It covers battery SRAM and serial EEPROM saves alike, at
the offsets the core uses: Genesis Plus GX loads it as its `.srm`; `sav:NAME` powers on with it. `--state` adds
a savestate that only this core build loads.
- Savestates carry the cartridge RAM (the core's own state leaves it out; the backend appends it, as on the Master
  System). A state of one platform is refused by the other.
- The header's `RA` field (`1B0`) says whether a cartridge declares backup RAM (`game.json` "header" "battery");
  many EEPROM games do not, the core finds them in its database.

## Not supported
Mega-CD / Sega CD, 32X, Sonic & Knuckles lock-on, Power Base Converter (Master System games run on the `sms`
platform), Pico, a second controller, Team Player / 4 Way Play, mouse, Menacer / Justifier light guns, the
Reset button, the TMSS boot screen, interleaved `.smd` dumps. Codes and debug menus that need the second pad
cannot be entered.

First game on this backend: Sword of Vermilion (scout 2026-11-20) found no friction with buttons, battery RAM,
`export`/`sav:`, peek/poke or timing. Most of work RAM changing on a step is tile maps: use
`play.py diff A --range FFC000-FFFFFF` (or wherever the game keeps its variables).
A state loaded mid-scene can differ from a flat replay in a dead stack word (Sword of Vermilion: `FFFD8C`, a
return address below the stack pointer, 600 frames into a battle; game variables and frames equal, gone after
more play): an interrupt landed one instruction apart. `cachecheck.py` reports such a checkpoint as "DIFFERS
(memory)"; end checkpoints outside real-time scenes, or check that the differing bytes are stack.
