# Text engine notes

> Addresses refer to the Japanese **Rev 1** (the base since 2026-11-12). Written for v1.0 and converted with
> `tools/revmap.py`; a few marked "(v1.0)" did not map. `docs/re/rev1.md` lists what Rev 1 changed.

ROM: Wizardry Empire (J), CGB-only (header $143=$C0), MBC5+RAM+battery ($147=$1B), 1 MB (64 banks), 8 KB SRAM.
SHA-1 `f5f4e8bead0fe45075141133a530a0eb116ea78c` (Rev 1; these notes were made on v1.0, SHA-1
`041c125115c83c6fef1b888761ba0b2b1f9bd291`).

## Encoding / font
- One byte per character; the byte is also the BG tile index of the 8x8 font (`tbl/jp.tbl`).
- The font already has ASCII layout for `0-9` ($30), `A-Z` ($41) and `a-z` ($61); kana fill the gaps.
- In menus the font sits in VRAM bank 0, tiles $8800-$97FF (LCDC bit 4 = 0, signed addressing): code $00-$7F at $9000+, $80-$FF at $8800+.
- $20 = space (window colour), $00 = empty tile, $F0 = cursor arrow, $F1-$F3 = window frame pieces.

## Screen buffer
- WRAM bank 3: `$D000` = 32x18 tile-number buffer (stride 32), `$D400` = matching CGB attribute buffer.
- `26:40EF` packs $D000/$D400 into a transfer list at `$D800` (bank 3); the VBlank handler pushes it to VRAM.
- VBlank (`JP $C004` -> `$01E5`) also services a GDMA queue at bank 2 `$D404/$D405` (entries in `$D4xx`) - `0:1505`.
- `0:1553` = synchronous HBlank-DMA copy (src `$FFB8/$FFB9`, bank `$FFBA`, dst `$FFBB/$FFBC`, VRAM bank `$FFBD`, B = blocks).

## Bank switching
- `rst $28` = switch ROM bank (A -> `$FF9E` and `$2000`).
- `$C1A0` (RAM trampoline) = far call: A = bank, HL = address (`rst $10` = `jp hl`).
- `$FF9D` mirrors SVBK (`$FF70`).

## Text path 1: rectangle blocks
Data: `[w][h]` then `w*h` tile bytes (some screens follow with `w*h` attribute bytes).
Padded with $20 to the box width. Blitted into $D000 by `0:171C`, `0:173C`, `0:1789`, `0:17C0`
(source `$FFB8-$FFBA` = ptr/bank, destination `$FFBB/$FFBC`).
Example: bank 43 (`$2B`) `5F14` is a pointer table for the town building info boxes; bank 38 (`$26`) holds many menu blocks.

## Text path 2: typewriter messages (`0:1BAB`)
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
- 0:278D and 01:6400 (window open) set the text bank `$C1C1` = $31 (bank 49); a message set after them
  without its own `$C1C1` store is in bank 49. `$FC` pauses and hands control back to the waiting task, which
  may continue with the next bytes (a `$FC` continuation is its own segment: it needs its own script entry,
  e.g. 49:5594 -> 49:55A4) or set a new pointer. Full census of message pointers: docs/re/msgcov.md;
  tests/test_msg_coverage.py checks every reachable segment by address.

## Free space
Most banks end in $00 padding (see `tools/` census). The patch expands the ROM to 2 MB (MBC5) and keeps new code/text in banks 64+.

## Text banks and data records
- Typewriter text banks (`$C1C1`): only 45 (`$2D`, events/NPCs), 46 (`$2E`) and 49 (`$31`, system/dungeon).
  Message starts are set inline: `ld a,lo / ld [$C1BF],a / ld a,hi / ld [$C1C0],a` (~500 sites).
- Inserted strings (`$F3`) end with `$00` and their control codes act on the main pointer, so the patch adds
  its own `$F2 bank lo hi` jump instead.
- Items: bank 40 `$4000`, 224 records of 40 bytes, name = bytes 0-16 (16 chars + `$00`); byte 17 = unidentified class (`$C560` after the record copy;
  docs/re/overflow.md).
- Monsters: bank 57 (`$39`) `$4820 + 64 x id`, 167 records of 64 bytes, name at `+0`, 12 chars + `$00`; `$FD` = line
  break (the old note '$4840, name at +$20' framed the same data 32 bytes off). `script/monsters.json` index = id - 1.
  Field map: docs/design/monsters.md.
- Default characters: bank 46 `$4000`, `$80`-byte records, 8-byte name.
- Party records in WRAM `$C880 + $80*n`, name `$00`-terminated; copied by `ld a,[hli] / or a / jr z / ld [de],a / inc de / jr` loops.
- Bank 49 `$4000-$418F`: `$00`-separated name lists (gender, race, alignment, class, status, battle commands).
- Some rect blocks are also lookup tables: fixed-length unrolled copies (`(ld a,[hli] / ld [de],a / inc de)* / ld a,[hl] / ld [de],a`)
  read their rows directly (e.g. `38:71AC` alignments).
- Menus also write text from code: `ld a,X / ld [de],a / inc de` or `ld hl,dst / (ld a,X / ld [hli],a)* / ld a,X / ld [hl],a`.
- Font: bank 1 `$4400` (256 tiles), loaded by queue entries `$4400->VRAM0:$9000`, `$4800->$9400`, then
  `$4C00/$5000` -> VRAM1 `$9000` (split) or VRAM0 `$8800` (flat); `$4300` (16 tiles) -> `$8F00` for frames in flat screens.
- `0:19B4-1A3A`: the original monster-panel glyph builder (group names into WRAM1 `$D200+$100*g`). Its only
  caller, 22:5688, now goes to `VWF_Panel`; the routine is dead and holds bank-0 stub area 2.

## Party list status word (39:4991)
The shared party-list printer (`39:4931` -> `39:4991`, far-called from Camp `2A:4E12 (v1.0)` and 14 other places) prints
max HP, '/', then current HP or, when the status byte (record +$0C, records $80 bytes from `$C880`) is non-zero,
a 4-cell word from `39:4004` (a byte copy of `38:754D`). Status encoding: low 6 bits = severity (1 Afraid,
2 Asleep, 3 Paralyzed, 4 Stoned, 5 Dead, 6 Ashes, 7+ Lost); 0 with bit 6 = Silenced, bit 7 = Poisoned (also a
'-' instead of '/'). Table order is not the encoding. The copy at `39:49FE` ends in `2a 12`, which the
fix_sites() pattern misses: it is an EXTRA_FIX_SITES entry. The bank-45 twin (event party list, magic circle
2D:7B4B..7BCA) reads its own table 2D:7ADF and copies with the name loop 2D:7BE5: `EvStatus` routes it through
`Stub_Fix` (4 cells; fixtables.json bank 45). Do not print fixed-width table words with Stub_PrintZ: it blanks
one cell per character.
