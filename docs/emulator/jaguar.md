# Atari Jaguar

Platform notes for `jaguar` games (Atari Jaguar cartridges). The general rules (routes, tokens, the working loop)
are in [README.md](README.md). Added 2026-11-27 and checked with the test cartridge `tests/make_jaguar_rom.py`
(tests `test_jaguar_*`). First game: Alien vs Predator (2026-11-27): about 60 routes of 2,500 frames (menus,
all cutscenes, all 15 areas, save and restore) with no freeze, render fault or speed problem. The core's own
notes say some other cartridges freeze or run at the wrong speed
([compatibility page](https://jaguar.provenance-emu.com/compatibility.html)).

## Backend
Virtual Jaguar, the libretro continuation (`libretro/virtualjaguar-libretro`, v3.13.1), run inside the Python
process by `tools/lrcore.py`. Built by `sh tools/setup_emu.sh jaguar` (about 40 s) at a pinned commit into
`tools/virtualjaguar/`; the target also installs capstone for `tools/dis68k.py`.
`tools/virtualjaguar-debug.patch` adds `retro_gamedb_pad` (the 21 buttons set directly, so every keypad key is
reachable), `retro_gamedb_peek`/`poke` (the core's debugger path: no side effects, RAM-only writes) and
`retro_gamedb_pc`. Single-threaded, no host clock: the same route always gives the same frames, and a loaded
savestate continues exactly like the run that saved it (test `test_jaguar_backend`, with input).
Speed: about 2,600 frames per second on the test cartridge (a real game, with the GPU, DSP and blitter busy, is
far slower).

Fixed settings: the console as it was. No enhancements (true colour, 2x, widescreen, per-title defaults, texture
packs), no frame skipping, no link cable, the accurate blitter, the RISC clock at 1x. The core's other defaults
stay, including its GPU/DSP idle-loop skip (deterministic; the core's recommended setting).

## Boot and models
No BIOS file is needed: both console boot ROMs are built into the core.

| Model | Video | Boot |
|---|---|---|
| `ntsc` (default) | 60 Hz | the core's high-level boot: straight into the game at its entry point, no logo |
| `pal` | 50 Hz | the same |
| `ntsc-bios`, `pal-bios` | as above | the real Series K boot ROM first: the Jaguar logo, then the cartridge, if it is signed |

The high-level boot is the core's default and the more compatible path. Use a `-bios` model only to capture the
console's boot logo; an unsigned cartridge (homebrew, the test cartridge) stops on the red logo screen there, as
on the real console. Carts are region-free; the model only sets the video standard.

## Games
A game is one cartridge image, `.j64` or `.jag` (a raw dump, mapped at 800000). `.rom`, `.abs`, `.cof`, `.prg`
and `.bin` are not taken (`.bin` is the Mega Drive's, `.prg` the C64's). The cartridge has no title in its header:
`game.json` "header" holds the size, the CRC32 and the entry vector of the universal header (800404, usually
802000), so `--region` is always given at intake. Jaguar CD discs are not set up.

## Screenshots
The frame the core makes: 352x240 on NTSC for the common pixel width (the visible window with a black border at
the sides; other video modes give other widths), 345x240 seen on PAL. No aspect correction.
Enlarged copies only on demand (`tools/x3.py`). A screenshot never advances emulation.

## Buttons
`up down left right a b c option pause 0 1 2 3 4 5 6 7 8 9 star hash`: the whole controller in port 1 (the keypad
is `0`-`9`, `star`, `hash`). Example: `a`, `option:30`, `b+right:60`, `star+hash`. Port 2, the Pro Controller,
Team Tap, rotary, mouse and light gun are not set up.

## Memory
68000 addresses, six hex digits (`poke:1A2B3C=03E7`, `"addr": "01A2B3"` in `game.json`); values are big-endian
(`ENDIAN = "be"`).
- `000000-1FFFFF` DRAM (2 MiB): the game's RAM; `find` (RAM search) covers all of it (the first search takes
  about 2 s).
- `800000-` the cartridge (read only), `E00000-E1FFFF` the boot ROM.
- `F00000-` TOM and JERRY: `F03000-F03FFF` GPU RAM, `F1B000-F1CFFF` DSP RAM, CLUT and line buffer are RAM too
  (peek and poke); the chips' registers can be peeked (no side effects) but not poked.
- `regs` gives the 68000's program counter at the frame end (the GPU and DSP run their own code).
- Code: `python3 tools/dis68k.py SLUG 802000 40` disassembles the cartridge at CPU addresses;
  `--xref ADDR` finds the instructions that name a variable. Many cartridges are compressed and run their
  code from DRAM (Alien vs Predator: ROM strings unreadable): disassemble live memory with
  `dis68k.py SLUG --route @checkpoint ADDR [N]` (or `--route ROUTE --xref ADDR`), read text from DRAM.
- Pad: games read it active-low in the standard Atari layout (Alien vs Predator: A = bit 29, B = 25, C = 13,
  Pause = 28, Option = 9 of the long they build).

## Cheats
No Jaguar cheat format is set up: hold a value with `freeze:ADDR=HEX` or write it once with `poke:`.

## Saves
The battery save is the cartridge EEPROM: 128 bytes (64 big-endian words; the core gives every cartridge one).
`play.py export` writes it as `.sav` (rename it to the game's `.srm` for RetroArch's Virtual Jaguar core);
`sav:NAME` powers on with it. Without a save the EEPROM starts erased (all FF), as a new cartridge. (The core
itself would start it at zero: it unpacks its empty save buffer over the blank chip on the first frame; the
backend hands it an erased one.) `--state` adds a savestate that only this core build loads
(`GAMEDB-JAGUAR-STATE-1` header, the core's state zlib-compressed: 2.9 MB raw, about 20 KB stored).
