# Master System / Mark III

Platform notes for `sms` games (Sega Master System and Mark III cartridges). The general rules (routes, tokens, the
working loop) are in [README.md](README.md).

## Backend
Genesis Plus GX, built as a libretro core and run inside the Python process by `tools/lrcore.py`. Built by
`sh tools/setup_emu.sh sms` (~11 s) at a pinned commit into `tools/gpgx/`; `tools/gpgx-debug.patch` adds
side-effect-free access to the Z80 address space, the program counter and the whole cartridge RAM, and silences
the core's info-level log. One process runs one game; parallel sessions use `play.py --name`. ROMs: `.sms`.
No BIOS: the cartridge starts at power-on (the core picks the console variant and mapper from its own game
database, with the Sega mapper for every ROM over 48 KiB). Deterministic: power-on RAM is fixed by the model
(zeros, or `$F0` on a Japanese console), so the same route always gives the same frames (test `test_sms_backend`).

## Models
- `ntsc`: Master System sold outside Japan, 60 Hz.
- `ntsc-j`: Japanese Master System / Mark III, 60 Hz: the FM sound unit is on, RAM starts as `$F0`, and games that
  check the console's region see Japan.
- `pal`: 50 Hz.

`game.json` "model" comes from the `TMR SEGA` header: Japan gives `ntsc-j`, Export gives `ntsc`. Most Japanese
cartridges have no header: register them with `--region jp --model ntsc-j`. A cartridge whose header says Game
Gear is refused (not set up).

## Screenshots
256x192, the raw frame, no filter, no border. The 3x copy is nearest neighbour.
- Games that hide the leftmost 8 pixels (VDP register 0 bit 5; most scrolling games) show an 8-pixel strip of
  the backdrop colour there, as on the console. It is part of the picture, do not crop it.
- Games that switch to the 224- or 240-line mode give 256x224 / 256x240 frames.

A screenshot never advances emulation; savestates carry the frame on screen.

## Buttons
`b1 b2 pause up down left right`: button 1 (usually start and the main action), button 2, and the console's Pause
button (an NMI; many games pause, some open a menu). Example: `b1`, `b2:30`, `b1+right:60`. There is no Start
button on this console: title screens usually take `b1`. The console's Reset button is not mapped.

## Memory
The Z80 address space, four hex digits: `poke:C0A2=09`, `"addr": "C0A2"` in `game.json`.
- `C000-DFFF` work RAM (8 KiB), mirrored at `E000-FFFF`. `FFFC-FFFF` are the Sega mapper's registers (writes
  there also land in RAM). Write RAM addresses in the `Cxxx`/`Dxxx` form.
- `0000-BFFF` the ROM pages mapped right now; `8000-BFFF` is cartridge RAM while the game maps it there.
- `peek` has no side effects; `poke` writes work RAM and mapped cartridge RAM only (a ROM address is an error).
- `find` (RAM search) covers the 8 KiB of work RAM.
- Video RAM and the colour RAM are not reachable.

## Cheats
- **Pro Action Replay** (`00AA-AAVV`): a RAM code is held with `gs:00AA-AAVV` (written every frame, like the
  device) or `freeze:AAAA=VV`.
- **Game Genie** (`XXX-XXX[-XXX]`, the Game Gear device's format): a ROM patch in a `rom:` variant (`game.json`
  `"rom_variants": {"gg": {"gg": ["XXX-XXX-XXX"]}}`). With the compare byte every 16 KiB page that holds it is
  patched; a 6-digit code is only accepted for games without paging (<= 48 KiB).

## Saves
The header does not say whether a cartridge has a battery. `play.py export` writes the cartridge RAM as a 32 KiB
`.sav` (both Sega mapper pages; the export refuses when the game never wrote it). Genesis Plus GX loads it as its
`.srm`; `sav:NAME` powers on with it. `--state` adds a savestate that only this core build loads.
- Savestates carry the cartridge RAM (the core's own state leaves it out; the backend appends it, since
  2026-11-19, found by the Phantasy Star scout). Older cached states are refused; delete them and the route
  rebuilds them. After `export`, check the save by loading it with `sav:NAME` through the game's Continue.

## Not supported
Game Gear and SG-1000 cartridges (the core runs them; the backend is not set up for them), a second controller,
Light Phaser, Paddle, Sports Pad, 3-D Glasses, the console's Reset button, the BIOS intro, Sega Card games.
