# SNES / Super Famicom

Platform notes for `snes` games (SNES and Super Famicom cartridges). The general rules (routes, tokens, the
working loop) are in [README.md](README.md).

## Backend
Mesen-S, built as a libretro core and run inside the Python process by `tools/lrcore.py`. Built by
`sh tools/setup_emu.sh snes` at a pinned commit into `tools/mesen-s/`; `tools/mesen-s-debug.patch` adds
side-effect-free memory access and the program counter. One process runs one game; parallel sessions use
`play.py --name`. ROMs: `.sfc`, and `.smc` with or without the 512-byte copier header. Special-chip cartridges
(SuperFX, SA-1, DSP, CX4, S-DD1, SPC7110) are emulated by the core. Deterministic: power-on RAM is all zeros
(set explicitly; the core's own default is random), so the same route always gives the same frames.

## Models
`game.json` "model" comes from the region byte of the cartridge header: `ntsc` (North America, Japan, South
Korea; 60 Hz) or `pal` (Europe, Australia; 50 Hz). Override with `--model`.

## Screenshots
256x224, the raw frame, no filter. Enlarged copies only on demand (`tools/x3.py`, nearest neighbour).
- The core always sends 239 lines; a normal picture is lines 7-230 with black above and below, and that black
  margin is cut off. A game that really uses the 239-line overscan mode has picture in the margin and keeps the
  full 256x239 frame, so a set can contain both sizes.
- Hi-res and interlaced screens come out as 512x448 (or 512x478). Do not scale them down.

A screenshot never advances emulation; savestates carry the frame on screen (same as NES).

## Buttons
`a b x y l r start select up down left right` (player 1).

## Memory
The 24-bit CPU address space, written as six hex digits `BBAAAA` (bank, address): `poke:7E0DBE=05`,
`"addr": "7E0019"` in `game.json`.
- `7E0000-7FFFFF` work RAM (128 KiB); its first 8 KiB also appear at `0000-1FFF` of banks `00-3F` and `80-BF`.
  Always write RAM addresses in the `7E`/`7F` form.
- Battery RAM where the cartridge maps it: LoROM `700000-`, HiROM `306000-307FFF` (and mirrors).
- ROM by its mapping: LoROM `808000-`, HiROM `C00000-`.
- `peek` has no side effects; `poke` writes work RAM, battery RAM and ROM, never the PPU/APU/CPU registers.
- `find` (RAM search) covers the 128 KiB of work RAM.
- `status` shows the PC as `BBAAAA`.
- The sound CPU's RAM and video RAM are not reachable.

## Cheats
- **Pro Action Replay** (`AAAAAAVV`): a RAM code is held with `gs:AAAAAAVV` (written every frame, like the
  device) or `freeze:AAAAAA=VV`.
- **Game Genie** (`XXXX-XXXX`): a ROM patch in a `rom:` variant (`game.json` `"rom_variants": {"gg": {"gg":
  ["XXXX-XXXX"]}}`). The code names a CPU address; it is patched at the file offset the cartridge's mapping
  gives. There is no compare byte on this console, so a code made for another revision silently patches the
  wrong byte: check the result.

## Saves
`play.py export` writes the battery RAM as a `.sav` (the cartridge's real size; the `.srm` format of other
emulators is the same bytes); `--state` adds a savestate that only this Mesen-S core build loads.

## Not supported
A second controller, multitap, mouse, Super Scope; Satellaview and Super Game Boy cartridges are untested.
MSU-1 audio packs are not set up.
