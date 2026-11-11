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
- The typewriter never reuses a cell's previous slot: the game scrolls message boxes by copying rows, so
  the slot a cell owned may now be shown by the row above.
- New slots come from a ring with an allocation bitmap (`wBits`). When it runs dry, `GC` rebuilds the bitmap
  from what the bank-3 buffers reference: only the 18 rows the game's GDMA copies (`0:1674`, `$23` blocks), and
  the window buffer `$D800` only while the window is on screen (LCDC bit 5, WX < 167, WY < 144). Battle hides
  the party list with WX=167 and re-sends it before showing it. Scanning all 32 rows marked garbage as used,
  the pool ran dry and the fallback overwrote live tiles (battle menu "Item" -> "r em").
- Known conflict: after a battle the game loads the chest picture into VRAM0 `$8800+` while the last battle
  line is still visible, so it flickers for a few frames.

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
- WRAM bank 7: shadows `$D000 + code*16` (`$D000-$DEFF`), variables `$DF00-$DFFF` (cleared once on first use,
  signature `VW` at `$DFFE`). Bank 7 is the engine's home bank: every entry point saves the caller's SVBK,
  switches to 7 and restores it. Buffers (bank 3) and the cell map (bank 6) are reached only through
  `Read3/Write3/Read6/Write6`; source strings through `FetchSrc` (caller's WRAM bank).
- WRAM bank 6: cell map `$D000-$D7FF`, slot owners `$D800 + code*2`.
- No WRAM0: the first version used `$CF00-$CFFF`, which are the game's task stacks (`docs/re/tasks.md`); that
  caused the battle hang. Bank-0 stubs pass everything in registers or on the stack: the VWF reads caller
  HL/BC/argument pointer from fixed stack offsets (see the comment above `Stub_Inline`).

## Game graphics in pool tiles
`Stub_Enqueue` passes every non-font VBlank DMA to `VWF_DmaCheck`: pool slots inside the destination lose their
owner and shadow and are reserved (`wGame`, bank 7 `$D200`) until the next GC, which keeps them only if cells
still reference them. Codes `$A0` (VRAM1 tile `$20` in the split layout, kept blank), `$CF`/`$D0` (the monster
panel's parentheses) are not in the pool. GC marks cells under both layouts (VWF-range tiles only).

## Battle monster panel
`22:5682` -> trampoline `22:7F00` -> `VWF_Panel`: the 4 group names ($C50F, 13 bytes each) are drawn
proportionally into WRAM1 `$D200+$100*g` (tiles 0-9 row 1, 10-15 row 2; word break past 80 px) with
`wPanel` set, which makes `CommitIfInk` write tiles there; then the original DMA to VRAM1 `$8C00`.

## Spells
`0:24CF` (record copy to `$C577`) first calls `Stub_SpellPre` -> `VWF_SpellName`: full English name from
`SpellNames` (bank, ptr per id) into `wSpell` (bank 7 `$D280`). Messages print it with `{F8 00 07 D280}` (the
2nd F8 byte is written to SVBK). The spell list blanks the rect's name cells (`2A:4D42` reads zeros) and
`2A:4D8E` -> `2A:7F00` -> `VWF_SpellList` prints `wSpell` one cell after the blit destination.

## Tile sharing and reuse rules (2026-11-11)
- Dedupe: when a cell with a newly allocated slot is finished, a slot in use with the same content (1-byte
  hash per slot in `wHash`, then a 16-byte shadow compare, VRAM-valid) is shared and the own slot freed if
  still owned. Never the typewriter's current slot; not while a font load is pending.
- In-place reuse (CellSlot) takes a fresh slot when the content changes and the tile may be shown elsewhere:
  shared (`wShared`) or the same tile 1-2 rows above/below (rows copied by scrolling). Screens restored from a
  saved copy need stable slot numbers, so reuse otherwise stays.
- GC first pass counts both buffers fully plus graphics reservations (`wGame`, until the next font load).
  Only when the pool is still dry, a second pass ignores a hidden window, BG rows under a full-width window
  and the reservations (disarm trap list, battle party list).
- The typewriter blanks every cell it leaves without ink (the original wrote a space tile per cell).

## Stack
Task stacks are 64 bytes (`$CE00+$40n`). Called from a task (shop card, battle typewriter), the VWF chain
(stub, far call, Fix/Inline/Rect, Commit, GC) overflowed into the next task's frames and crashed (shop hang).
Every entry runs its body through `PrivCall`: when SP >= `$CE00` it switches to a private stack at `$CD80`
(WRAM0 `$CCE0-$CDD5` is zero in every savestate checked; the main stack's lowest residue is about `$CDD6`),
otherwise it stays on the caller's stack.

## Fixed-length copies (`Stub_Fix`)
`call Stub_Fix / db n` replaces unrolled `ld a,[hli] / ld [de],a / inc de` copies whose source is a ROM table.
The FixMap key is the source (bank, address); rect rows and `script/fixtables.json` provide the English. On a
miss the raw bytes are printed. `db n|$80, bank` reads the source from another ROM bank (shop alignment,
29:421A, replaced a `call $0C97` banked copy). The destination cells are blanked first. Copies whose source is
set by `ld hl,$8000+` are data (gold, EXP, HP) and must not be stubbed: doing so made buying add gold.

## Message redirect
Original message start -> `$F2 bank lo hi` (English). The English ends with `$F2 <original bank> <terminator>`
pointing back at the original `$FF`/`$FC`, so the game ends or pauses the message in the original text bank.
Without this, `$C1C1` stayed on the English bank and `$FC`-chained battle segments read the wrong bank.
Bank-49 messages keep their English inside bank 49 (free `$5726-$7FFF`, shared with `lists.json` and
`chests.json`): `{F3 ..}` inserts read their string pointer from the current text bank, so English in bank
`$42` printed shop text instead of attack verbs.

## Notice Board (2B:57C0)
The scroll is one picture (rect `2C:5978` blitted to `$D000` by `$1723`); the Japanese text is part of the
bitmap (rows 2-15, cols 2-17, palette 6, VRAM1). `2B:57E0` (far call to the fade-in `38:4054`) now calls the
trampoline `2B:7F00`: far call `VWF_Notice`, then the fade-in. It has to run before the fade-in: the buffer is
not copied to VRAM again afterwards. `VWF_Notice` fills the area with tile `$20` (VRAM0, paper colour 2),
sets the attributes to palette 5 without flips (palette 6 colour 3 = 18,15,11 is nearly the paper 19,17,12;
the picture flips some tiles in row 10) and prints `NoticeText` lines at `NoticeRows`, column 2. Lines: 8 x 28
bytes, filled by `insert.py` from `script/notice.json`, max 128 px. `VWF_PrintBuf` clobbers `wDed*`; loop
counters belong on the stack.
