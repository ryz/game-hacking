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
| FA | word-wrap point: measures the next word (incl. inserted strings) and emits FD if it does not fit, else a space ($20). In English `{FA}` replaces the space between words: never write a space next to it |
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

## Text banks and data records
- Typewriter text banks (`$C1C1`): only 45 (`$2D`, events/NPCs), 46 (`$2E`) and 49 (`$31`, system/dungeon).
  Message starts are set inline: `ld a,lo / ld [$C1BF],a / ld a,hi / ld [$C1C0],a` (~500 sites).
- Inserted strings (`$F3`) end with `$00` and their control codes act on the main pointer, so the patch adds
  its own `$F2 bank lo hi` jump instead.
- Items: bank 40 `$4000`, 224 records of 40 bytes, name = bytes 0-17 (`$00`-padded).
- Monsters: bank 57 `$4840`, 166 records of 64 bytes, name at `+$20`, 12 chars + `$00`; `$FD` = line break.
- Default characters: bank 46 `$4000`, `$80`-byte records, 8-byte name.
- Party records in WRAM `$C880 + $80*n`, name `$00`-terminated; copied by `ld a,[hli] / or a / jr z / ld [de],a / inc de / jr` loops.
- Bank 49 `$4000-$418F`: `$00`-separated name lists (gender, race, alignment, class, status, battle commands).
- Some rect blocks are also lookup tables: fixed-length unrolled copies (`(ld a,[hli] / ld [de],a / inc de)* / ld a,[hl] / ld [de],a`)
  read their rows directly (e.g. `38:71AC` alignments).
- Menus also write text from code: `ld a,X / ld [de],a / inc de` or `ld hl,dst / (ld a,X / ld [hli],a)* / ld a,X / ld [hl],a`.
- Font: bank 1 `$4400` (256 tiles), loaded by queue entries `$4400->VRAM0:$9000`, `$4800->$9400`, then
  `$4C00/$5000` -> VRAM1 `$9000` (split) or VRAM0 `$8800` (flat); `$4300` (16 tiles) -> `$8F00` for frames in flat screens.
- A second glyph builder at `0:19C9` composes tiles from the font into WRAM `$D200` (used by the museum/spell screens?).
