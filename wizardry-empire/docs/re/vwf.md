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
