# Game Boy / Game Boy Color

Platform notes for `gb` and `gbc` games. The general rules (routes, tokens, the working loop) are in
[README.md](README.md).

## Backend
gbemu-cli, a headless SameBoy with a JSON-lines API, one process per game (`tools/gbemu-cli/`, built by
`sh tools/setup_emu.sh gb` at a pinned commit; `tools/gbemu-linux.patch` fixes the Linux link). ROMs: `.gb`,
`.gbc`, `.sgb`. Deterministic: fixed seed, fixed boot ROM, turbo mode.

## Models
- `game.json` "model" comes from the header: CGB games -> `cgb`, everything else -> `dmg` (the original grey).
- Dual-mode games (CGB-enhanced) are shot in `cgb`; a `--model dmg` set may be added. Super Game Boy games:
  `--model sgb` captures 256x224 with the border and SGB colours (a separate set, e.g. `sgb`).
- Known problem: `--model sgb` hangs on the SGB transfer screen in some games (Pokémon Blue); capture in `dmg`.

## Screenshots
160x144, the raw framebuffer (CGB colours 5->8 bit, no colour correction, no filter). Enlarged copies only on demand
(`tools/x3.py`, nearest neighbour). Never resample by non-integer factors.

## Buttons
`a b start select up down left right`.

## Memory
The CPU address space: `0000-7FFF` ROM (bank 0 and the mapped bank), `A000-BFFF` cartridge RAM, `C000-DFFF`
work RAM (CGB: `D000-DFFF` banked), `FF80-FFFE` high RAM. `status` shows the PC and the mapped ROM bank.
`find` (RAM search) is the emulator's own search.

## Cheats
- **GameShark** (`gs:TTVVAAAA`): written every frame like the device. `01VVAAAA` writes value VV to address AAAA
  (low byte first: `01 09 A2 C0` -> `poke:C0A2=09`); types `8n`/`9n` address RAM bank n (cartridge RAM, CGB
  work RAM).
- **Game Genie** (`ABC-DEF` or `ABC-DEF-GHI`): a ROM patch in a `rom:` variant (`game.json` `"rom_variants":
  {"gg": {"gg": ["ABC-DEF-GHI"]}}`), applied where the compare byte matches.

## Saves
`play.py export` writes the cartridge RAM as a `.sav` (loads in any Game Boy emulator next to the ROM); `--state`
adds a SameBoy savestate.
