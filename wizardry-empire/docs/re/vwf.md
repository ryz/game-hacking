# VWF design (asm/vwf.asm)

> Addresses refer to the Japanese **Rev 1** (the base since 2026-11-12). Written for v1.0 and converted with
> `tools/revmap.py`; a few marked "(v1.0)" did not map. `docs/re/rev1.md` lists what Rev 1 changed.

## Tile pool
- The original font is 256 8x8 tiles (ROM bank 1 `$4400`). Codes `$00-$7F` always live in VRAM0 `$9000`.
  Codes `$80-$FF` are loaded either to VRAM1 `$9000` ("split" layout: typewriter screens, dungeon) or
  VRAM0 `$8800` ("flat" layout: town/menu screens), always through the VBlank DMA queue (`0:1443`).
- English needs no kana, so the patch drops the loads of codes `$80-$EF` (`VWF_FontLoad`, called from the
  enqueue stub) and keeps `$F0-$FF` (cursor arrow, window frame). Those 112 VRAM slots are the VWF pool;
  nothing else writes them, so the VWF can upload at any time.
- The same hook records the layout (`wLayout`) and invalidates the WRAM shadow copies (`wValid`).

## Allocation
- `cellmap` (WRAM6 `$D000-$D7FF`): last slot used by each cell of the bank-3 buffers (`$D000`/`$D800`).
  `owner` (WRAM6 `$D800 + code*2`, cleared at init; 0 = no text cell): the cell each slot belongs to. A cell reuses its slot when it still owns it:
  the game clears and re-blits boxes every few frames, so reuse keeps slot use stable.
- The typewriter never reuses a cell's previous slot: the game scrolls message boxes by copying rows, so
  the slot a cell owned may now be shown by the row above.
- New slots come from a ring with an allocation bitmap (`wBits`). When it runs dry, `GC` rebuilds the bitmap
  from what the bank-3 buffers reference: only the 18 rows the game's GDMA copies (`0:168D`, `$23` blocks), and
  the window buffer `$D800` only while the window is on screen (LCDC bit 5, WX < 167, WY < 144). Battle hides
  the party list with WX=167 and re-sends it before showing it. Scanning all 32 rows marked garbage as used,
  the pool ran dry and the fallback overwrote live tiles (battle menu "Item" -> "r em").
- Known conflict: after a battle the game loads the chest picture into VRAM0 `$8800+` while the last battle
  line is still visible, so it flickers for a few frames.

## Upload
- Each tile is built in `wUp` (bank 7 `$DF80`, ink = colour 3, paper = colour 2 like the original font), compared
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
  signature `VY` at `$DFFE`; bump it when the variable layout or the init changes, so old savestates re-init),
  plus tables in the shadows of non-pool codes: `wGame` `$D200` ($20/21), `wRC_*`/`wEpoch` `$D220-$D22C` ($22),
  `wSpell` `$D280` ($28/29), `wGameNew` `$D2A0` ($2A/2B), `wHash` `$D2C0` ($2C-$3B), `wShared` `$D410`
  ($41/42), `wRC_cells`/`wRC_attrs` `$D440-$D53F` ($44-$53). CheckInit clears only `$DF00-$DFFD` and
  `wRC_valid`; wGame and wGameNew are cleared at the first Alloc (AllocReset). Bank 7 is the engine's home bank: every entry point saves the caller's SVBK,
  switches to 7 and restores it. Buffers (bank 3) and the cell map (bank 6) are reached only through
  `Read3/Write3/Read6/Write6`; source strings through `FetchSrc` (caller's WRAM bank).
- WRAM bank 6: cell map `$D000-$D7FF`, slot owners `$D800 + code*2`.
- No WRAM0: the first version used `$CF00-$CFFF`, which are the game's task stacks (`docs/re/tasks.md`); that
  caused the battle hang. Bank-0 stubs pass everything in registers or on the stack: the VWF reads caller
  HL/BC/argument pointer from fixed stack offsets (see the comment above `Stub_Inline`).

## Game graphics in pool tiles
`Stub_Enqueue` passes every non-font VBlank DMA to `VWF_DmaCheck`: pool slots inside the destination lose their
owner and shadow and are reserved in `wGameNew` (bank 7 `$D2A0`); the next full GC moves them to `wGame`
(`$D200`), which keeps a slot only while a buffer still references it. A font load clears both. Codes `$A0` (VRAM1 tile `$20` in the split layout, kept blank), `$CF`/`$D0` (the monster
panel's parentheses) are not in the pool. GC marks cells under both layouts (VWF-range tiles only).

## Battle monster panel
`22:5688` -> trampoline `22:7F00` -> `VWF_Panel`: the 4 group names ($C50F, 13 bytes each) are drawn
proportionally into WRAM1 `$D200+$100*g` (tiles 0-9 row 1, 10-15 row 2; word break past 80 px) with
`wPanel` set, which makes `CommitIfInk` write tiles there; then the original DMA to VRAM1 `$8C00`.

## Spells
`0:24E8` (record copy to `$C577`) first calls `Stub_SpellPre` -> `VWF_SpellName`: full English name from
`SpellNames` (bank, ptr per id) into `wSpell` (bank 7 `$D280`). Messages print it with `{F8 00 07 D280}` (the
2nd F8 byte is written to SVBK). The spell list blanks the rect's name cells (`2A:4D58` reads zeros) and
`2A:4DA4` -> `2A:7F00` -> `VWF_SpellList` prints `wSpell` one cell after the blit destination.

## Tile sharing and reuse rules (2026-11-11)
- Dedupe: when a cell with a newly allocated slot is finished, a slot in use with the same content (1-byte
  hash per slot in `wHash`, then a 16-byte shadow compare, VRAM-valid) is shared and the own slot freed if
  still owned. Never the typewriter's current slot; not while a font load is pending.
- In-place reuse (CellSlot) takes a fresh slot when the content changes and the tile may be shown elsewhere:
  shared (`wShared`) or the same tile 1-2 rows above/below (rows copied by scrolling). Screens restored from a
  saved copy need stable slot numbers, so reuse otherwise stays.
- GC first pass counts both buffers fully plus `wGame | wGameNew` (see "Graphics reservations" below). Only
  when the pool is still dry, a second pass scans a hidden window and BG rows under a full-width window in
  ownerless mode (frees their text slots, keeps game graphics; disarm trap list, battle party list);
  reservations still count.
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

## Notice Board (2B:57DF)
The scroll is one picture (rect `2C:597F` blitted to `$D000` by `$1723`); the Japanese text is part of the
bitmap (rows 2-15, cols 2-17, palette 6, VRAM1). `2B:57FF` (far call to the fade-in `38:4054`) now calls the
trampoline `2B:7F00`: far call `VWF_Notice`, then the fade-in. It has to run before the fade-in: the buffer is
not copied to VRAM again afterwards. `VWF_Notice` fills the area with tile `$20` (VRAM0, paper colour 2),
sets the attributes to palette 5 without flips (palette 6 colour 3 = 18,15,11 is nearly the paper 19,17,12;
the picture flips some tiles in row 10) and prints `NoticeText` lines at `NoticeRows`, column 2. Lines: 8 x 28
bytes, filled by `insert.py` from `script/notice.json`, max 128 px. `VWF_PrintBuf` clobbers `wDed*`; loop
counters belong on the stack.

## Rect redraw cache (2026-11-11)
The town clears the selected building's info box to `$20` and redraws it on every main-loop pass. `VWF_Rect`
keeps the last box (source, destination, mode, size, cell codes and attributes, max 128 cells, `wRC_*` in the
shadow area of non-pool codes `$22` and `$44-$53`) and the tile epoch `wEpoch` (+1 per Upload, font load and
game DMA over a slot); it is not used while a font load is pending (`wReset`). When the same box is asked for again, the epoch is unchanged and every cell holds its
saved code or `$20` with unchanged attributes, the saved codes are written back instead of rendering.

## Graphics reservations and the dry GC pass (2026-11-11)
- `wGameNew`: slots a game DMA overwrote since the last GC. The full first GC pass sets
  `wGame = (wGame & referenced) | wGameNew`, so a reservation lasts while a buffer still shows the slot (it used
  to last until the next font load and filled the pool in the maze: slowdowns and text in the walls).
  Both passes count `wGame | wGameNew`.
- The dry second pass scans BG rows under a full-width window and a hidden window in "ownerless" mode: it keeps
  slots no text cell owns (game graphics such as the maze walls in `$BC-$D1`) and frees only text slots.
  Owners (bank 6, `$D800 + code*2`) are cleared at init; DMAs disown slots.
- Museum monster room (layout 2, 2026-11-12): pages are built in the hidden window while the list is on the BG,
  and page + list need more than the 157 slots. `wGCSkipWin` modes after the normal pass: 1 = hidden window's
  text reclaimable (stamp-protected); 2 = BG text reclaimable, window counts (a print into the window buffer,
  `S_cellHi` $D8-$DB: 2 then 1); 4 = only BG text drawn in the last STAMP_KEEP frames counts, the page counts (a
  BG print under the shown page: the list rows the game redraws while paging); 3 = the window's older text
  reclaimable even when shown, the BG counts (a BG print while the page closes, flag `wMusClose` set by the
  41:612E hook, or under a hidden window). Mode 4 judges by stamp only: the list's cache-restored cells have no
  owner entry, so an ownerless scan kept them all.

## Speed: caches and indexes (2026-11-11, later the same day)
Measured with a count-only breakpoint on the frame wait `0:07C5` (main-loop passes per 120 idle frames; JP 360)
and the frames from a key press to the first screen change (JP 2).
- Name print cache (`VWF_PrintZ`) and number cache (`VWF_Num`) share `wNC` (24 entries, bank 7 `$D610`):
  destination cell, cell count, hash of the string (+ start pixel), the first cell's attribute, an epoch and
  per cell the slot code and its tile version. Slot codes are derived from the tile number and the VRAM bank bit
  (`CellCode`: split layout + bank bit = code | $80). Tile versions `wVer` (bank 6 `$DA00`, +1 per upload or
  game DMA over a slot); a hit needs every version unchanged (or the entry's epoch = `wEpoch`: nothing was
  uploaded at all) and every cell holding its code or $20. Restored cells get their codes, bank bits and wBits.
- Party list (`39:4931`, every pass on town-type screens): skipped entirely when the party data (names, status,
  HP), the tiles (`wEpoch`) and the rows `$D160-$D21F` (Fletcher sums of codes and attributes) are as after the
  last real draw or exactly as the game left them before it; the snapshot (bank 6 `$DD00`/`$DD80`) is restored.
  Hooks: `39:4931` -> `Party_Entry` (39:7F00; keeps the caller's B), `39:498A` -> `Party_End` (snapshot).
- Rect cache (`VWF_Rect`): check by Fletcher sums of the box's codes/attributes (bank 3 switched in once);
  a box cleared to $20 is restored through the WRAM0 scratch `RC_SCR` ($CCE0, the idle private stack).
- `Dedupe`: hash index `wHIdx`/`wHIdx2` (bank 6 `$DB00`/`$DC00`, last two slots per tile hash) instead of a
  scan of the pool.
- Results: town with a party 360 passes/120 frames, reaction at frame 2 (= JP; was 174 and a half-speed
  cursor). Town without a party (info box): reaction at frame 7-13 (was 14-18; JP 2): a box render costs
  ~22k instructions (1.5 frames).
- Savestates from older builds are unsafe after code changes (the saved call stack returns into moved code;
  the town froze). Signature now `'V','\\'` .. bumped on every layout change.

## Numbers (0:0FE9 -> Stub_Num -> VWF_Num)
`0:10A4` (digit store of the number printer, 84 call sites) calls `Stub_Num`: base `$30` into the bank-3
buffers goes to the VWF, everything else (symbol-sheet digits `$F4`, the typewriter buffer `$C1DE`) keeps the
original loop. The field is right-aligned when the game padded it or gave a fixed width ($FFAC bit 7), else
left-aligned; the field's cells are blanked and the digits drawn from the computed pixel. In the split layout
numbers prefer low pool codes (VRAM0 in both layouts), because the game sometimes writes 8 px text over a
number field afterwards (shop header: age, then 'AC') and would inherit the VRAM1 bit. Digits are 4 px wide
(tabular, advance 5); `$7F` is a blank 5 px figure space used by the typewriter's number padding (`0:1D7F`).

## Render speed (2026-11-11, later)
- `Glyph`: shift tables `ShiftTab` (bank $40 `$7000-$7FFF`, 16 pages from tools/build.py: page 2p = b >> p,
  2p+1 = b << (8-p)), 8 rows unrolled, empty rows skipped (19.6k -> 7.9k instructions per cursor move).
- `BitAddr` mask table `BitMask` ($6FF8); `NextCell` and the tile build in `Commit` unrolled; `Commit` writes
  the cell and attribute with one WRAM bank switch.
- Space: font tables cut to codes $00-$7F (FontAdv/FontRows; every lookup masks with $7F), FixMap capacity 440.
  Code and data must end below $6FF8 (assert).
- Not done: batching tile uploads into VBlank. Measured waits are ~0.2 frame per box; the rest is per-tile
  bookkeeping (~1000 instructions per tile: slot search, ownership, hash, duplicate check, shadow compare).
- Note: render frames execute ~13.5k instructions vs ~29k in idle busy-wait frames (heavier instructions), so
  instruction counts underestimate render time ~2x. A cursor move with the info box: ~55k instructions =
  ~4 frames; reaction at frame 6-12 (JP 2).
- Numbers that the game overwrites with 8 px text keep 8 px digits: `NumExcl` (bank, return address of the
  0:0FE9 call) - currently the card's age (26:571B), which the shop header overwrites with 'AC'. The excluded
  field's cells get attribute bit 3 cleared. `VWF_Num` reads the caller from the stack ([sp+9] after its push).

## Cache epochs and the GC's visible columns (2026-11-12)
- The rect, party-list and name caches validate with the one-byte `wEpoch`; after 256 bumps an old epoch matched
  again (tavern list garbled after exactly 512). `EpochBump` drops every epoch cache when the counter wraps to 0.
  Per-slot `wVer` is also one byte (a slot with exactly 256 uploads could still false-hit the name cache's slow
  path; not seen).
- Battle raster split: the monster area scrolls (SCX=$50) above the unscrolled party panel. With SCX != 0 the GC
  counts columns 0-20 as well as SCX/8..+20 (it read SCX mid-frame and freed the panel's slots).
- `Stub_PrintZ` returns DE past the text (game copy loops leave DE there; the inn prints next to the name).
