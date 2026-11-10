# Text engine notes

ROM: Wizardry Empire (J), CGB-only (header $143=$C0), MBC5+RAM+battery ($147=$1B), 1 MB (64 banks), 8 KB SRAM.
SHA-1 `041c125115c83c6fef1b888761ba0b2b1f9bd291`.

## Encoding / font
- One byte per character; the byte is also the BG tile index of the 8x8 font (`tbl/jp.tbl`).
- The font already has ASCII layout for `0-9` ($30), `A-Z` ($41) and `a-z` ($61); kana fill the gaps.
- In menus the font sits in VRAM bank 0, tiles $8800-$97FF (LCDC bit 4 = 0, signed addressing): code $00-$7F at $9000+, $80-$FF at $8800+.
- $20 = space (window colour), $00 = empty tile, $F0 = cursor arrow, $F1-$F3 = window frame pieces.

## Screen buffer
- WRAM bank 3: `$D000` = 32x18 tile-number buffer (stride 32), `$D400` = matching CGB attribute buffer.
- `26:40EF` packs $D000/$D400 into a transfer list at `$D800` (bank 3); the VBlank handler pushes it to VRAM.
- VBlank (`JP $C004` -> `$01E5`) also services a GDMA queue at bank 2 `$D404/$D405` (entries in `$D4xx`) - `0:14EC`.
- `0:153A` = synchronous HBlank-DMA copy (src `$FFB8/$FFB9`, bank `$FFBA`, dst `$FFBB/$FFBC`, VRAM bank `$FFBD`, B = blocks).

## Bank switching
- `rst $28` = switch ROM bank (A -> `$FF9E` and `$2000`).
- `$C1A0` (RAM trampoline) = far call: A = bank, HL = address (`rst $10` = `jp hl`).
- `$FF9D` mirrors SVBK (`$FF70`).

## Text path 1: rectangle blocks
Data: `[w][h]` then `w*h` tile bytes (some screens follow with `w*h` attribute bytes).
Padded with $20 to the box width. Blitted into $D000 by `0:1703`, `0:1723`, `0:1770`, `0:17A7`
(source `$FFB8-$FFBA` = ptr/bank, destination `$FFBB/$FFBC`).
Example: bank 43 (`$2B`) `5F14` is a pointer table for the town building info boxes; bank 38 (`$26`) holds many menu blocks.

## Text path 2: typewriter messages (`0:1B92`)
Called each frame; delay `$C1C7/$C1C8`; source pointer `$C1BF/$C1C0`, bank `$C1C1`;
cursor column `$C1C5`, row `$C1C6`, right margin `$C1C3`; destination buffer pointer `$C1D3/$C1D4` (WRAM bank 3).
Writes tile = code ($80+ -> code&$7F with attribute bit 3 = VRAM bank 1) and attribute `$C1C2`.
Control codes:

| code | meaning (provisional) |
|---|---|
| FF | end |
| FE | `1F62` |
| FD | newline |
| FC | `1E35` |
| FB | `1ED8` |
| FA | word-wrap lookahead: measures the next word (incl. inserted strings) and emits FD if it does not fit |
| F9 | `1E5F` |
| F8 b, bank, ptr16 | insert number (b = digits/format) |
| F7 | `1DE9` |
| F6 | `1E20` |
| F5 | `1DF1` |
| F4 x, y | set cursor (FF = keep) |
| F3 bank, ptr16 | insert string via pointer |

Strings of this kind live in banks 45 (`$2D`), 49 (`$31`) and others, FF-terminated.

## Free space
Most banks end in $00 padding (see `tools/` census). The patch expands the ROM to 2 MB (MBC5) and keeps new code/text in banks 64+.
