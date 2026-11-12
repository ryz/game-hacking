# Numbers and other 8 px glyphs in the English build (tracer, 2026-11-11)

> Addresses refer to the Japanese **Rev 1** (the base since 2026-11-12). Written for v1.0 and converted with
> `tools/revmap.py`; a few marked "(v1.0)" did not map. `docs/re/rev1.md` lists what Rev 1 changed.

(Copied from work/re/numbers.md; scratch files, states and screenshots stay in the untracked work/re/numbers/.)

EN ROM: commit 615e150 (`.../scratchpad/wizardry_empire_en_615e150.gbc`), original `rom/wizardry_empire_j.gbc`.
Scratch: `work/re/numbers/` (harness, census JSON, screenshots, states).

## 1. Answer

Almost every 8 px number in the English build comes from one routine, **0:0FE9** (binary to decimal, 84 call
sites in banks 0/21/26/27/29/2A/2C/2D/2E; no call site is patched yet). One hook inside it (0:10A4, the digit
store loop) can route all of them through the VWF. The only exceptions are the typewriter `$F8` path (0:1DAC, already VWF), the
two symbol-sheet digit sets (monster panel "(n) m" 22:5713 (v1.0)/5835, automap coordinates 21:40C4, tiles
`$F4+n` from 1:$4000) and one raw digit rect (Camp reorder 2A:7302). The other 8 px glyphs are short labels
and separators written by code (`ld a,'X' / ld [de],a`): "L", "HP", "AC", "HP-MAX", "Lo"/"Hi", "ON"/"OFF",
'/', '-', '~', ':', '*', '?', 'x', '"'. There are also two unlisted rects ('/' row 2A:7227, reorder 2A:7302), the
name-entry chart, and the 2-cell in-place rects "Ax" (29:6EA4) and "--" (29:71EC). No rect has `fixed: true`.
The VWF digits are 5 px except '1' (4 px), so columns need a tabular '1' (or per-digit 5 px cells). The
typewriter `$F8` padding (`$20`, 3 px) needs a 5 px figure space: the battle and maze party lists are VWF
already but misaligned by 2 px ("7/" vs "10/"). Performance: the party list (27:4990) calls 0FD0 4 times per
frame on every town/tavern/temple/inn/shop/camp/outskirts screen with a party (120 calls in 30 frames), so
the hook needs a redraw cache like the rect/name caches.

## 2. Evidence

### 2.1 The printer 0:0FE9
Inputs: **A** = value size in bytes (1-4, little endian) at **HL**; **B** = code of digit 0 (`$30` = font
digits; `$F4` = symbol sheet, 21:40xx only); **C** = width/flags: bit 7 = right-align (pads by *skipping*
`width - ndigits` cells, it never writes them), low 7 bits = width; bit 7 clear and width != 0 = keep only the
low `width` digits, left-aligned; C = 0 = natural width. **DE** = destination (bank-3 buffer `$D000-$DBFF`,
or `$C1DE` for the typewriter). HRAM: value -> `$FFA8-$FFAB`, C -> `$FFAC` (later ndigits), B -> `$FFAD`, DE ->
`$FFAE/$FFAF`, digits -> `$FFB8-$FFC1` (powers of ten at 0:10E3, subtract loop 0:10B7), terminator `$FFC2`.
Store loop 0:10A4-0:10B6 (19 bytes): `ldh a,[$ac] / and $7f / ld b,a / .l: ld a,[hli] / or a / jr z,+1 /
ld [de],a / inc de / ld a,l / cp $c2 / ret z / dec b / jr nz,.l / ret`.
Output: DE past the field. All 84 return sites use only DE afterwards (each next instruction reloads A/B/C/HL
or pops). Checked with `work/re/numbers/ctx.py` -> `callers.txt`.
Two other digit writers exist but are not used: 0:11A3 (byte -> decimal, no callers) and 0:3252 (hex).
No ad-hoc `add $30` digit writers in game banks.

How confirmed: count-only PC breakpoints on 0FD0 and on one return address per routine group (48 groups,
`groups.txt`), run over all 118 non-boot routes of `docs/shots/jp_tour/index.json` on the EN build
(`census.py` -> `census_tour.json`, screenshots `work/re/numbers/shots/<id>.png`), and over the 32 JP
battle/chest states (`census_jpbattle.json`). On every screen a scanner compared each visible BG/window cell's
VRAM tile with the 8 px font glyphs (01:4400, non-pool codes) (`harness.py scan()`).

### 2.2 Groups (by routine), screens, current state
Site = call address. "Tour" = seen on the tour; otherwise found statically.

| # | Sites | Prints | Screens (tour id) | Per-frame? |
|---|---|---|---|---|
| A | 27:49C0 (A=2,C=$84 -> col 10), '/' 27:49C3, 27:4A3C (C=$84 -> col 15), '-' 27:4A29 (poison) | party list "10/ 10" (record +$64, +$62) | party_town, tavern_*, temple_*, inn_who, shop_who, outskirts_*, camp, camp_reorder, stairs_up_climb | **yes**: 2 rows/frame, 120 calls / 30 frames |
| A2 | 2D:7B4B, '/' 2D:7B4E, 2D:7BCA, '-' 2D:7BB7 | twin copy of A (same offsets) | not on tour (bank 2D, reached from maze bank 20 / 2C:4C2A) | ? |
| B | 26:5699 (A=2,C=$83) after "L" 26:5684 | level | every card: tavern_add, training_*, camp_inspect, character_sheet, inn_*, shop_menu | inn sleep: ~0.5/frame (HP regen) |
| B | 26:5718 (C=$82) | age ("16yrs") | same | |
| B | 26:57D2 (C=$84) + '/' 26:57D5 + 26:57F2 (C=4); "HP" 26:57C1 | HP cur/max | card row 4 | |
| B | 26:5860 + "AC" 26:5807, "Lo"/"Hi" 26:5875 (AC out of range) | AC | card row 4 | |
| B | 26:595F, 26:598C (A=4, C=$8A) | EXP, Gold (10 cells) | character_sheet, *_pool | |
| B | 26:59D0..5A34 (6x, C=$82) | Strength..Luck | sheets | |
| B | 26:6055..60CA (7x, C=$82) | bonus screen stats + Bonus | training_create_bonus/class | |
| B | 0:381F/37CE + "HP" 0:380E, '/' 0:3822 | card HP refresh (same cells as 26:57D2) | not on tour | |
| B | '?' 26:56C6/5704/572C/5760 | unset fields during creation ("??????") | training_create_* | |
| C | 29:4260 + "AC" 29:4230, "Lo"/"Hi" 29:4275 | shop header AC | shop_* | |
| C | 29:42B5 (A=4, C=$8A) | shop header gold | shop_* | |
| C | 29:4AAA (A=3, C=$87, attrs set to palette 6 first = red) | buy prices | shop_buy_* | |
| C | 29:56D3 (A=3, C=$87) | sell prices | shop_sell | |
| C | 'x' 29:4A36 / 29:564C; '*' markers | stock / equipped marks | shop lists | |
| D | 29:6508/6517 + '~' 29:650B, 653B, 656E, 68A3 (sign '-' 29:689D), 68D1, 68E8, 6914/6923 + '~' 29:6917, 6B07; ':' 29:68AE, '"' 29:6A39; rects "Ax" 29:6EA4, "--" 29:71EC | item info page | museum_item_info (see docs/re/museum.md), also shop/camp item info | |
| D | 29:5CA3/5CB1, 29:62C3, 29:633A | museum counts / list numbers | museum_* (skip: museum.md) | |
| E | 2A:4B7B loop -> 2A:4B8E (7x A=1,C=1, one blank cell between); '/' from raw rect **2A:7227** (w 11, " / / / / / /"-style, not in rects.json) | spell slots "1/0/0/0/0/0/0" | camp_spells_*, tavern_sheet_spells, training_view_spells, battle_spell_list, chest_cast_list | |
| F | 27:5435 (A=4, C=0) | inn "Next level in 500" (row 13 col 1) | inn_stable, inn_cot | |
| F | 27:594C (A=1,C=3), 27:6AA0 (A=3,C=7 -> $D06B), 27:6B06 (A=4,C=$0A) | gold/count fields in bank 27 | not on tour | |
| G | 2C:408D/41F4, 2C:4582..45C8 (6 stats, window $D82A+), 45DB/45F7/4624/49C0, 4A7F ("L" 2C:4A73), 4A94/4AAF ('-' 2C:4A97), 4AC8/4AE8, 4B11/4B35 (gold/EXP C=$8A), 4B5D ("HP-MAX" 2C:4B3B)/4B79 ("HP" 2C:4B63), 4BA3/4BC3, 4E04/4E1A/4E30; "ON"/"OFF" 2C:4433/4440 | a character sheet in the window buffer (bank 2C entries 4036 from 26:491E/2A:52A4, 4C24 from maze 20:522B) | not on tour (maze: found/rescued character?) | ? |
| H | 2D:64A9/64C9 (window $D970/$D990, attr $80 written to $DD70/$DD90 first) | two values in a maze window (2D:63EB, called from 7 sites in bank 20) | not on tour | ? |
| I | 2E:5796 ("B"+floor+"の"), 2E:57B4 ("X"), 2E:57D9 ("Y") | maze location "B1F X.. Y.." | not on tour | |
| J | 0:1DAC (typewriter `$F8`, digits into `$C1DE`, padded with `$20` from 0:1D7F) | all message numbers; battle party list (32:429F), maze menu list, chest/battle messages | battle_*, chest_*, maze_dmenu | already VWF |
| K | 21:40CD/40E2/4100 (B=`$F4`, `$FF` blank, `$FE` sign) | automap floor/coordinates, symbol tiles | not on tour | graphic |
| L | 22:5713 (v1.0), 22:583B (`add $F4`, rows `$C644+$2A*g`: `$CF`,n,`$D0`,m, then `rst $08` into row 2) | monster panel "(2) 2" | every battle (EN: `walk2_7/end.png`) | graphic |
| M | rect 2A:7302 (1x6 "123456", 0:1789 from 2A:4FA0) | Camp reorder order numbers | camp_reorder(_pick) | VWF rect (2026-11-12); names 2A:7082 -> Stub_PrintZ |
| N | name-entry chart rects + "END", typed name (8 px, known) | name entry | training_create_name_*, training_rename_entry | |

Party list A: confirmed with a stopping breakpoint on 0FD0 from `work/states/p2/party.state` (A=2, B=$30,
C=$84, DE=$D16A..$D20A and $D16F..; 13 calls per row per 30 frames). Battle party list = typewriter: break on
0FD0 in the EN battle, return 0:1DAF, caller 32:429F (DE=$C1DE).
Monster panel: tile `$F6` at BG row 2 col 17/19 (attr $80, VRAM0) is a copy of the 8 px '2'; the only DMA into
`$8C00-$8FFF` is 1:$4000 (64 tiles) from 22:441F -> 0:19B0 (`panel3.py`). The reorder digits are written by
`rst $08` from 0:17AA (blit 0:1789), source `$FFB8-$FFBA` = 2A:7302 (`reorder2.py`).

States (EN, reproducible):
- `work/re/numbers/walk2_7/end.state`: battle start (Kobold King). Start `work/states/p2/maze.state`, tokens
  in `walk2_7/inputs.txt` (walk2.py seed 7, 213 tokens).
- `work/re/numbers/walk2_7/pre.state`: same walk minus the last 4 tokens (`walk2_7/pre_inputs.txt`); the
  encounter follows with `up,left,up,w30`.

## 3. Hook proposals

### 3.1 Global number hook (covers groups A-I, about 80 sites)
Patch 0:10A4-0:10B6 (19 bytes) to (15 bytes, 4 spare):
```
108B  call Stub_Num      ; carry = printed by the VWF, DE = field end
108E  ret c
108F  ld a,[hli]         ; original loop without "or a / jr z,+1": B is never 0 ($30/$F4)
      ld [de],a
      inc de
      ld a,l
      cp $c2
      ret z
      dec b
      jr nz,$108F
      ret
```
Stub_Num (bank 0, about 30 bytes; free: `$1C4F-$1C78` after Stub_TWInit, 42 bytes; check with the assembler):
```
Stub_Num:
    ldh a,[$ad]          ; digit base
    cp $30
    jr nz,.orig          ; symbol digits ($F4): unchanged
    ld a,d
    sub $d0
    cp $0c
    jr nc,.orig          ; only $D000-$DBFF; $C1DE (typewriter) stays as it is
    ld c,l               ; first digit = $FF00+C
    ld a,VWF_BANK
    ld hl,VWF_Num
    call FarCall
    scf
    ret
.orig:
    ldh a,[$ac]
    and $7f              ; clears carry
    ld b,a
    ret
```
VWF_Num (bank $40): n = min($C2 - C, [$FFAC]&$7F); start = [$FFAF]:[$FFAE]; pad = DE - start; cells =
pad + n; right-aligned if [$FFAC] bit 7 or pad > 0. Copy the n digit codes to wNameBuf, blank the `cells` cells
(as VWF_Fix does), Begin at start with the start cell's attribute (keeps the red shop prices), x = cells*8 - 5n
if right-aligned else 0, Glyph each digit, CommitIfInk, return DE = start + cells. Preserve: DE (output) only;
SVBK (saved by the VWF entry). Script format: none (no text data).
**Cache required:** key (start, cells, digit string) -> cell codes + tile versions, like `NameCacheHit/Save`
(NCWalk). The party list alone needs 12 entries per pass (plus 6 names already in wNC, NC_N = 6), so give
numbers their own table of >= 16 entries. Space: the free shadow fragments in bank 7 are too small. WRAM bank 6
`$DA00-$DFFF` received no writes on the town/camp/maze routes (`bank6.py`; battle not checked).
Pool: town party list = 12 fields x about 2 cells + '/' -> about 30 slots of 157; dedupe shares identical tiles.

### 3.2 Tabular digits
fonts/vwf.txt: '0' and '2'-'9' advance 5, '1' advance 4. Either `== 1  advance=5` with the art moved one
column right (simplest; also aligns typewriter numbers; prose '1' becomes 1 px wider), or VWF_Num adds 1 px
before '1'. That second way does not fix the typewriter path.

### 3.3 Typewriter `$F8` padding (group J)
0:1D7F `ld a,$20` (byte at 0:1D80) fills `$C1DE` before right-aligned numbers. Change it to a figure-space code
(a free text code whose VWF glyph is blank with advance 5, e.g. `== 7F  advance=5`). Fixes the 2 px misalignment
in the battle and maze party lists (`work/re/numbers/battle_en_zoom.png`) and in right-aligned message
numbers. 1 byte + 1 font entry.

### 3.4 Separators and labels written by code
- Per site with rst $38 inline (4 bytes: `rst $38 / db bank / dw text`). Each `ld a,X / ld [de],a / inc de`
  is 4 bytes, so every 1-char site fits exactly: '/' 27:49C3, 2D:7B4E, 26:57D5, 0:3822; "HP" 26:57C1 (9 bytes
  incl. the gap), "AC" 26:5807, 29:4230, "L" 26:5684, 2C:4A73, "HP-MAX" 2C:4B3B, "Lo/Hi", "ON/OFF". Verify
  that DE after VWF_Inline equals the original DE (start + chars); add padding `inc de` where the VWF text
  is shorter. New `script/inline.json` entries (en = "HP", ...).
- Cheaper alternative for one-glyph separators/markers ('/', '-', '~', ':', '*', '?', 'x', '"'): redraw those
  8 px font tiles in the small-font style, centred in the cell (build.py `patch_fixed_font`, add codes to
  ASCII_FIX). No code, no slots. They then match the VWF digits; the name-entry chart uses '?', '-', '/' too.
- Spell slots (E): one hook at 2A:4B7B (34 bytes up to 2A:4B9C) that builds "d/d/d/d/d/d/d" and prints it
  with Stub_PrintZ over the 13 cells, plus a blank English for rect 2A:7227 (or leave the rect and use the
  restyled '/').
- Reorder numbers (M): add rect `2a:7302` (w 1, h 6, en "1".."6") to script/rects.json (6 bytes >= 5-byte
  header). Data only.
- "Ax" 29:6EA4 / "--" 29:71EC: 2 cells, too small for a redirect. They need a Stub_Fix-style site hook at
  their copy, or they stay 8 px.

### 3.5 Symbol-sheet digits (K, L)
These are graphics (1:$4000 sheet, codes `$F4-$FD` plus the `$CF/$D0` parentheses), not the text font. Cheap
route: redraw the digit tiles 1:$4340-$43DF in the small-font style (build-time graphics patch, also changes
the automap). Full VWF: have VWF_Panel draw the counts with the names (22:5713 (v1.0)/5835 write rows
`$C644+$2A*g`).

## 4. Stylistic candidates (owner decides)
- Card/sheet big labels "L", "HP", "AC" and their values (JP uses the same 8 px ASCII):
  `docs/shots/jp_tour/character_sheet.jp.png` vs `work/re/numbers/shots/character_sheet.png`,
  `work/re/numbers/sheet_training.png`.
- Name-entry chart grid and "END": `work/re/numbers/shots/training_create_name_abc.png`.
- Monster panel "(2) 2" and automap coordinates (symbol sheet): `work/re/numbers/walk2_7/end.png`.
- Spell-slot grid "1/0/0/0/0/0/0": `work/re/numbers/shots/camp_spells_mage.png`.

## 5. Open questions
- Screens not reached: groups A2, F (27:594C/6A56/6ABC), G (bank 2C window sheet), H (2D:63EB), I (2E
  location), K (automap), 0:381F. They go through the same 0FD0 hook, but their layouts are unverified.
- WRAM bank 6 `$DA00-$DFFF` is unused only on the town/camp/maze routes checked; battle not checked.
- Per-call VWF cost is not measured; the town at 4 calls/frame is the case to test with the cache.
- Seen by the way (not numbers): `outskirts_quit` (end-session message) is garbled in EN while JP is settled:
  `work/re/numbers/quit_cmp.png` (EN left). For triage.
- The scanner reads the BG and window maps without the window overlap, so BG cells under the window can show
  up (e.g. maze_dmenu rows 7-8 are the typewriter list, VWF on screen).
