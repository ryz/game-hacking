# NES / Famicom

Platform notes for `nes` games (NES and Famicom cartridges). The general rules (routes, tokens, the working
loop) are in [README.md](README.md).

## Backend
Mesen, built as a libretro core and run inside the Python process by `tools/lrcore.py` (a minimal headless
libretro frontend). Built by `sh tools/setup_emu.sh nes` at a pinned commit into `tools/mesen/`;
`tools/mesen-debug.patch` adds side-effect-free memory access and the program counter. One process runs one
game; parallel sessions use `play.py --name`. ROMs: `.nes` with an iNES or NES 2.0 header (Famicom cartridges
included). Deterministic: power-on RAM is all zeros, so the same route always gives the same frames. A few
games seed their RNG from uninitialised RAM and therefore behave the same on every boot; that is intended.

Core options (region, power-on RAM, no overscan crop) are passed explicitly. Until 2026-11-17 a bug in
`tools/lrcore.py` dropped them and the core ran on its defaults, which gave the same result except that the
region was detected by the core instead of forced; `--model pal` had no effect before that date.

## Models
`game.json` "model" comes from the header: `ntsc` (NES and Famicom, 60 Hz; default), `pal` (50 Hz) or `dendy`.
iNES headers often lack the region: a European ROM that runs too fast or glitches needs `--model pal`.

## Screenshots
256x240, the full frame without overscan crop, in Mesen's default palette. The console has no RGB output, so
every palette is a choice; this one is fixed for all sets. Many games leave garbage in the top and bottom 8
lines and the left column: that is what the console outputs, do not crop. The 3x copy (in the set's `3x/` folder) is
nearest neighbour.

A screenshot never advances emulation. Savestates are the core's own state followed by a trailer holding the
frame on screen, so a cached checkpoint and a freshly built one give the same picture and the same timing.

## Buttons
`a b start select up down left right` (player 1).

## Memory
The CPU address space: `0000-07FF` RAM (mirrored up to `1FFF`), `6000-7FFF` cartridge RAM (battery save or work
RAM, when the cartridge has it), `8000-FFFF` the PRG banks mapped at that moment.
- `peek` has no side effects; `poke` reaches RAM and mapped PRG, not the PPU, APU or mapper registers.
- `find` (RAM search) covers `0000-07FF` and `6000-7FFF`.
- `status` shows the PC without a bank number (banking depends on the mapper). Many games sit in one
  frame-wait loop, so the PC is the same all the time; that is not a hang.
- A position poke does not redraw the map; see "RAM" in [README.md](README.md).

## Cheats
- **Held RAM values:** `freeze:ADDR=HEX`. Pro Action Replay style RAM codes (`AAAA:VV`) are exactly that. There
  is no GameShark for this console, so `gs:` is refused.
- **Game Genie:** a ROM patch in a `rom:` variant. 8-letter codes always work (patched in every 8 KiB PRG bank
  where the compare byte matches). 6-letter codes have no compare byte, so they work only for games without
  bank switching (PRG up to 32 KiB); otherwise find the 8-letter form or patch the file offset with `"bytes"`.

## Saves
- Battery cartridges: `play.py export` writes the raw battery RAM as a `.sav` (8 KiB on most cartridges, the
  format every NES emulator uses); `--state` adds a savestate that only this Mesen core build loads.
- Password games have no `.sav`: record passwords in the playbook Shortcuts (see "Hangs and dead ends" in
  [README.md](README.md) for making one).

## Not supported
Famicom Disk System images (they need the disk BIOS), a second controller, the Famicom microphone, the Zapper.

## Cartridge RAM (6000-7FFF)
`peek`, `poke`, `dump`, `find` and `freeze:` on 6000-7FFF go straight to the core's battery RAM (8 KiB carts), so
they work while the game keeps the cartridge RAM disabled (MMC3 games often do: on the bus it reads open bus and
drops writes). Games may keep a check value per record (Wizardry II: CRC at +$5E, records failing it are wiped at
power-on): a poked record works until the next power-on unless the game itself saves it again. For a saved veteran party, start from a game-saved base
(`sav:NAME`), let the game save (e.g. Leave Game), export, and check the whole roster reloads. (2026-11-18)
