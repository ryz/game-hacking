# VWF design (asm/vwf.asm)

## Tile pool
- The original font is 256 8x8 tiles (ROM bank 1 `$4400`). Codes `$00-$7F` always live in VRAM0 `$9000`.
  Codes `$80-$FF` are loaded either to VRAM1 `$9000` ("split" layout: typewriter screens, dungeon) or
  VRAM0 `$8800` ("flat" layout: town/menu screens), always through the VBlank DMA queue (`0:142A`).
- English needs no kana, so the patch drops the loads of codes `$80-$EF` (`VWF_FontLoad`, called from the
  enqueue stub) and keeps `$F0-$FF` (cursor arrow, window frame). Those 112 VRAM slots are the VWF pool;
  nothing else writes them, so the VWF can upload at any time.
- The same hook records the layout (`wLayout`) and invalidates the WRAM shadow copies (`wValid`).

## Allocation
- `cellmap` (WRAM7 `$D000-$D7FF`): last slot used by each cell of the bank-3 buffers (`$D000`/`$D800`).
  `owner` (WRAM7 `$DF00`): the cell each slot belongs to. A cell reuses its slot when it still owns it:
  the game clears and re-blits boxes every few frames, so reuse keeps slot use stable.
- New slots come from a ring with an allocation bitmap (`wBits`). When it runs dry, `GC` rebuilds the bitmap
  from what the bank-3 buffers reference.

## Upload
- Each tile is built in `wUp` (`$CF80`, ink = colour 3, paper = colour 2 like the original font), compared
  with the shadow in WRAM7 (`$D000 + code*16`), and uploaded only when changed: a one-block HBlank DMA started
  on a visible line < 140 (interrupts masked while the registers are set), or a CPU copy when the LCD is off.
  (An earlier version used the VBlank queue; together with the game's full-map GDMA it overran VBlank and
  corrupted the tilemap.)

## Text paths
| Path | Hook | English data |
|---|---|---|
| Rect blocks (`[w][h][tiles]`) | `$1723`/`$1770` -> `Stub_Rect*`; `$17BD` masks the marker | first 5 bytes become `[w|$80][h][bank][ptr]`; rows split by `$FD`, `$FC n` = pixel x, `$FF` end |
| Typewriter messages | `$1C11` char output -> `TW_Char`; `$1B3F` init | original message start becomes `$F2 bank lo hi` (jump); `$F4 col $FF` places the cursor |

The typewriter reports to the game the number of cells used (`$C1C5`), so the game's own newline/cursor logic
keeps working; it resyncs whenever the game moves the cursor or the buffer base changes.

## RAM used
`$CF00-$CFFF` (WRAM0, above the stack, unused by the game); WRAM bank 7 (never touched by the game in any tested state).
