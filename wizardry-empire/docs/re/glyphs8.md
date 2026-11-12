> **Status 2026-11-12:** groups 1-5 converted (item marks '?'/'-' at all four sites, creation '?' fields, Search
> Person dots/location/particle, heal box, item info negative AC); the bullet '●' stays an icon; group 6 (automap
> graphics) waits for the owner.
> Copied from work/re/glyphs8.md (tracer, 2026-11-12, build e9125dd); scratch, states and crops stay in the
> untracked work/re/glyphs8/.

# 8 px font glyphs left in the English build (tracer, 2026-11-12)

EN ROM: `build/wizardry_empire_en.gbc` at e9125dd (rebuilt into `work/re/glyphs8/en.gbc`, byte-identical).
Original: `rom/wizardry_empire_j.gbc` (Rev 1). Scratch: `work/re/glyphs8/` (scripts, per-route JSON + PNG,
crops in `crops/`, states). Do not trust `work/re/sheet2c/party_en/*.state`: they were saved at 05:44, before
fd0ee0b (06:10), and their buffers still hold the old 8 px '/' in the party list until a full redraw. I
regenerated them with `tools/party.py --out work/re/glyphs8/party`.

## 1. Answer

Every route in `docs/shots/jp_tour/index.json` (121) is clean except the out-of-scope name-entry chart.
Every prefix of the `tools/routes/tour.txt` routes (230 screens) is clean too, and so are one full battle
(command menus for all six classes, fight modes, Equip, the spell list and spell info, the round confirm,
messages, Run, victory EXP) with its chest (menu, inspect, cast list, trap list, disarm, open, paralysis
trap, gold), the five maze events in reach.md, and the camp party list with a status word. The only
**text** glyphs (letters, digits, punctuation) still drawn in 8 px come from **seven groups of code
sites**. Five of them are not on the tour. To reach them I had to force a value: an item flag, a spell
effect id, or a negative stat.

1. Item list marks '?' (unidentified) and '-' (cursed), plus the '●' (font `*`) equipped/in-party mark: 6 sites.
2. "??????" unset fields on the character card during creation (26:56C6/56F5/571D/5751). This one is on the tour.
3. The Search Person spell result: five animated '.' cells and "B X , Y" around VWF digits (bank 2E).
4. The heal result box "HP 10/10": 'H', 'P', '/' at 0:380E/3812/3822.
5. The item info AC sign '-' (29:6535). It only shows when the item's AC byte is negative.
6. (Decided 2026-11-12: digits stay 8 px; the labels 地下 -> 'B', the warp panel ワープ先/東/北 -> Warp/E/N and the 16
   cursor labels are translated, see asm/main.asm 'Automap' and build.py patch_automap_labels.) The automap axis labels 0-15 and the floor digit under 地下 (Compass/Teleport map). These are graphic tiles
   from 18:4000, not font text. This is probably the "automap graphics" the dispatch put out of scope; listed so
   the owner can decide.
7. Out of scope as dispatched: the name-entry chart (all 71 glyphs, `training_create_name_*`,
   `training_rename_entry`) and the debug screens (2C:4433-4B67: ON/OFF, L, HP-MAX, HP, '-').

Everything else the scanner flags is an icon, not text: the → cursor (font `$FC`), the ↑ level cursor (`$F9`)
and the × "cannot use" mark (`$F8`). Section 4 lists them so they can be ignored or redrawn on purpose.
Side finding (not 8 px): Search Person writes the raw code `$5E` (JP 'は') after the name at 2E:5819. `$5E`
is a VWF pool slot now, so a random glyph appears there ("ryz1", "ryz|").

## 2. Table: remaining 8 px text cells

Crops: `work/re/glyphs8/crops/<name>.png` (3x, red boxes = 8 px cells). "Forced" = the input list includes a poke.

| # | Screen (route / how reached) | Glyphs | Buffer cells | Writing site (EN = JP bytes) | Confirmed by | Hook suggestion |
|---|---|---|---|---|---|---|
| 1a | Item list on the sheet (tavern_sheet_items, camp_items, tavern_item_*, camp_item_use): `crops/item_marks_sheet.png` | '?' '-' ('●' when equipped) | `$D122+$20*n` (col 2) | 2A:6EC3-6EDE: flags `[hl]` bit 7 -> `$2A` (2A:6ECC), bit 7+5 -> '-' (6EDC), bit 6 -> '?' (6ED4); store `ld [de],a` 2A:6EDE | write watch `$D122`=`$2A` -> pc 2A:6EDF (bt 2A:58A6 <- 2A:53E4); forced flags `$C4A1=$40,$C4A3=$A0` | one-char VWF stub at the join: replace `ld [de],a / inc de` (6EDE-6EDF, 2 bytes, both jr targets) with `jp` into a block stub, or rewrite 6EC3-6EDF (29 bytes) as `call MarkStub` (flag byte in A -> 1-char string -> Stub_PrintZ, DE+1) |
| 1b | Camp Equip lists (camp_equip_2/3): `crops/item_marks_equip.png` | '?' '-' '●' | `$D102+$20*n` | 2A:620B-6226 (same logic: 6214 '●', 621C '?', 6224 '-'), store 2A:6226 | watch `$D102` -> pc 2A:6227 (bt 2A:5B75 <- 2A:5169) | same MarkStub |
| 1c | Shop Sell list (shop_sell, shop_sell_confirm; same list for identify/uncurse when items qualify): `crops/item_marks_shop.png` | '?' '-' '●' | `$D022+$20*n` | 29:560A-5628 (561E '●', 5622 '?', 5626 '-', else `$20`), store `ld [hli],a` 29:5628 | watch `$D022` -> pc 29:5629 (bt 29:4B49 <- 29:439F); forced `$C4A1=$40,$C4A3=$A0` | MarkStub variant for HL (`[hli]`) |
| 1d | Battle Item > Equip, weapon/armor choice (battle2 step 5): `crops/battle_equip.png` | '●' ('?' '-' possible) | window `$D842+$20*[$C1C6]` (`$D902` seen) | 22:5425-5448: B = '?' / `$2A` / '-', store `ld [hl],b` 22:5448 | watch `$D902`=`$2A` -> pc 22:5449 (bt 22:52C3 <- 22:48B4) | MarkStub variant (char in B, dest HL) |
| 1e | Tavern Add roster, members already in the party (tt_tavern_13..16): `crops/tavern_add_marks.png` | '●' | `$D0E2+$20*n` | C = `$2A` at 27:43FF, store `ld [hl],a` 27:485F (routine 27:483D) | watch `$D0E2` -> pc 27:4860 (bt 27:440C) | '●' is an icon: keep, or MarkStub |
| 1f | Training > Change order, picked member (training_order_pick): `crops/order_mark.png` | '●' | `$D0E2` | 26:5437 `ld a,$2a / ld [hl],a` | watch -> pc 26:543A (bt 26:53C2) | icon: keep |
| 2 | Character creation, unset fields (training_create_gender ... _class): `crops/create_unset.png` | '?' x (6+4+2+5) | `$D041-$D046`, `$D049-$D04C`, `$D051-$D052`, `$D061-$D065` | 26:56C6 (6 cells, `ld a,$3f` + 6x `ld [de],a/inc de`), 26:56F5 (4), 26:571D (2, age = `$7F`), 26:5751 (5); each is the else-branch of a `call $1C51` (Stub_Fix) field | watch `$D041/$D049/$D051/$D061`=`$3F` -> pc 26:56C9/56F8/5720/5754 (bt 26:5590 <- 26:470D) | CardAge-style: `ld hl,QText / jp Stub_PrintZ` over the fill (13 / 9 / 5 / 11 bytes available), "??????" etc. as strings |
| 3 | Search Person (priest spell 36) result, target elsewhere: `crops/search_person.png` (forced) | '.' x5, 'B', 'X', ',', 'Y' (digits are VWF) | '.' `$D0E5-$D0E9`; 'B' `$D122`, 'X' `$D126`, ',' `$D128`, 'Y' `$D129` (attr `$80`) | dots: 2E:5640/5652/5664/5676/5688 (`ld a,$2e / ld [de],a / inc de`, 10-frame delay between); 'B' 2E:5774 (`ld a,$42 / ld de,$d122 / ld [de],a`), 'X' 2E:57A2, ',' 2E:57B8 (EN patch: kana `$75` -> 8 px ','), 'Y' 2E:57C5; separator 2E:579A (EN: `$20`), `$FF` 2E:579E | scanner on forced state (`sp36b/v03_03.json`); asm/main.asm:74 documents the EN patch; static bytes | dots: `call DotStub` in place of the 4-byte `ld a,$2e/ld [de],a/inc de`; location: one stub that formats "B1 X0, Y0" into a RAM string and prints it with Stub_PrintZ at `$D122` (CardNeg-style, replaces 2E:5774-57DC). The spacing is bad now ("B1    X0 ,Y0") |
| 4 | Heal spell result box (camp: Restore/Healing/Recovery/Cure All = ids 28/32/45/50): `crops/heal_box.png` | 'H' 'P' '/' | `$D0E4`, `$D0E5`, `$D0EB` | 0:380E `ld a,$48`, 0:3812 `ld a,$50`, 0:3822 `ld a,$2f` (each `ld [de],a / inc de`); digits 0:381F/0:382E via 0FE9 (VWF) | watch -> pc 0:3811/3815/3825 (bt 0:077B task); spell sweep `spsweep/id28_00.json` | same as the card: `call CardHP`-like (HP string via Stub_PrintZ, DE fixed) and `call CardSlash`; bank 0 space: 0:380B-3815 (11 bytes) and 0:3822-3825 (4 bytes) |
| 5 | Item info page, AC field when the item's AC byte (`$C56B`) is negative: `crops/iteminfo_neg.png` (forced) | '-' (8 px dash, 1 cell before the digits) | `$D8E5` (2 digits) / `$D8E6` (1 digit) | 29:6523-6538: negate, `ld a,$2d / ld [de],a` 29:6535 | `neg.py`: bp 29:6528, A=`$FE` -> scan hit `$D8E6`. Not checked whether any real item has a negative AC byte | CardNeg/ShopNeg pattern (right-aligned '-<digits>' VWF string) |
| 6 | Automap (Compass id 3, Teleport id 25; also the map item): `crops/automap.png` | axis labels 0-9 and the 10-15 two-digit tiles; floor digit under 地下 | `$D0E0-$D200` col 0, `$D221-$D22A` row 17, `$D052` | tiles `$80-$8F` = 16 tiles DMA'd from ROM 18:4000 (bytes = 8 px font digits; tiles 10-15 are condensed pairs); rows placed by rect blit 23:4149 -> 0:175F; floor tile `$80+floor` by 23:41AF | watch `$D0E0`=`$89` -> rst 08 from 0:175F (bt 23:4149 <- 23:4A3E); `$D052` -> pc 23:41AF; VRAM `$8800-$88FF` == ROM `$60000-$600FF` | data only: redraw 18:4000 tiles 0-15 in build.py like `patch_symbol_digits` (VWF digits centred; 10-15 need two narrow digits in 8 px, which the 5 px VWF digits cannot do). Owner decision (automap graphics) |
| 7 | Name entry (training_create_name_*, training_rename_entry); debug 2C | all | - | known | tour | out of scope |

Statically confirmed dead (patched around, do not report): card Lo/Hi 26:5875-5882 (26:5870 -> `call CardLoHi / jr`),
shop Lo/Hi 29:4275-4282 (29:4270 hook), card '-' 26:584C (26:5843 `jp CardNeg`).

## 3. Method and evidence

### Scanner (`work/re/glyphs8/scan.py`)
It adapts numbers.md `harness.scan()`. Glyph set: 16-byte tiles of the **running** ROM's font at 01:4400, codes
`$21-$FF`, with blank or near-blank tiles skipped. It includes pool codes, because the EN font changed
`" ' ( ) , ;` and VWF pool tiles are matched by content anyway. A cell is reported only when (a) its VRAM tile
equals a glyph and (b) the 8x8 block of the actual screenshot has the same colour partition as that tile. Check
(b) removes stale map cells, cells under the window and the wrong half of raster splits. BG interpretations
tried: LCDC addressing as at VBlank and the other mode (maze strip, lines 56-71 = `$8000`), SCX/SCY as at
VBlank and 0/0 (battle party panel). Window at (WX-7, WY). Sprites from OAM. Each hit records the map, the
row/col, the bank-3 buffer address (`$D000`/`$D800` + row*32 + col), the code, the attribute and the VRAM
address.
Writers: `wtrace.py STATE TOKENS ADDR VALUE` sets a stopping write watch on bank 3 with a value filter and
logs PC, ROM bank and backtrace for each distinct write. Static census: `literal.py` lists every `ld a,n`
(n = printable non-pool ASCII) directly followed by a store, unpatched (EN bytes == JP) ->
`literal_en.txt`. A second pass allowed an `ld de/hl,nn` in between. After removing task-pointer setups
(`ld a,lo / ld [hli],a / ld a,hi / ld [hld],a`), WRAM variables, `$C1C1` bank stores, debug bank 2C and the
icons, the only remaining sites are the ones in the table. Item marks that use B/C or `jr` joins were found by
searching for the flag-test shape (`bit 7 / ... ld a,$2a ... ld a,$3f ... ld a,$2d`): 22:5425, 29:561E,
2A:6214, 2A:6ECC.

### Coverage (all on the EN build e9125dd)
| Set | Inputs | Result files |
|---|---|---|
| jp_tour, 121 routes (from power-on, as listed) | `tour.py work/re/glyphs8/tour` | `tour/<id>.json/.png`, `tour.log` |
| tour.txt, every token prefix of the 8 routes (PARTY expanded), 230 screens | `routes_tourtxt.json` | `tourtxt/`, `tourtxt.log` |
| Party states | `python3 tools/party.py --out work/re/glyphs8/party` | `party/*.state` |
| Battle start (Zombie) | `tools/explore.py build/wizardry_empire_en.gbc work/re/glyphs8/party/maze.state work/re/glyphs8/walk3 400 3` (hit at step 121) | `walk3/hit.state` |
| Battle -> victory -> chest menu | `seqscan.py walk3/hit.state battle1 "w60,a*50" C00B=\|04`; `battle1/s017.state` = chest menu | `battle1/` |
| Item > Equip, other classes' menus | `battle1/s001.state` + `down,down,a,w30,down,a,b,b,b,up,up,a,w30,up,a,b,b,b,a,a,a,a,a,down,a,w30,b,down,a,w30,a,w30,b,b,b,b,a,a,a,a,a` | `battle2/` |
| Spell list, spell info | `battle3/s001.state` (= battle2/s024 + `up,w10`) + `w60,down,w30,down,w30,up,w30,a,w60,down,w30,a,w60,...`; `battle5/s010.state` + `a,w40,a,w40,...` | `battle5/`, `bspell/` |
| Run | `battle1/s001.state` + `w30,down,w20,down,w20,down,w20,a,w60,...` | `brun/` |
| Chest: cast list / open (paralysis trap, gold) / disarm (trap list) / inspect | `battle1/s017.state` + tokens in `chest1..5/steps.txt` | `chest1-5/` |
| Back in the maze, camp with "Paral." | `chest2/s022.state` + `w30,a,w150,...` | `postb/` |
| Events 5009, 5C6D, 4490, 44A8 (`C889=0D`), 5C97 (`C896=00,C897=AD`) | `tools/maze_goto.py build/... work/re/glyphs8/party/maze.state X Y work/re/glyphs8/ev/event_N.state`, then `up,w90,(a,w60)x9` | `ev/run_*` |
| Camp spell effects 0-55 | `sp36.py`: `party/camp.state` + `a,w40,down,down,down,a,w60,a,w60` + `a` until bp 24:40DF (cubi's Restore, A=`$1C` = `[$FFB0]`) -> `sp36/at40df.state`; `spsweep.py 0 55` sets A = id there, scans every 30 frames, `a` every 3rd | `spsweep/` |
| Search Person, other location | `sp36b.py 03`: at40df (A=`$24`), bp 2E:5697, `$C511`=03 (00 = "In town", 16 = "At temple") | `sp36b/` |
| Item marks '?'/'-' | jp_tour camp_items / camp_equip_2 / shop_sell, poke `$C4A1=$40, $C4A3=$A0` before the last 2 tokens (item flag bytes, 2 per slot) | `marks2_*.json/png` |
| Item info negative AC | museum_item_info, bp 29:6528 on the last `a`, A = `[$FFB0]` = `$FE` | `neg.py`, `neg_info.*` |

Not covered: Find allies with a lost character in the maze (bank 1F lists them; no 8 px literal stores in 1F,
`literal_en.txt`); the Training transfer outcome; the ending. Effect ids 56-124 (class skills, battle only)
were not swept.

### Notes per group
- Item marks: the flag byte is the item slot's 2nd byte (`$C4A1 + 2n` for the first character). Bit 7 =
  equipped ('●'), bit 6 = unidentified ('?'), bit 5 = cursed ('-'; with bit 7 it still shows '-' on the sheet,
  2A:6EC8). The 8 px '-' is a full-cell dash and looks like a long rule before the name (`crops/item_marks_*.png`).
- Search Person: the location byte is record `+$57` -> `$C511` (2E:581E). `&$1F`: 0 = "In town", 1-20 =
  B<floor> X<x>, Y<y> via 2E:5727 (SRAM `$AEE2 + 12*(n-1)`), otherwise a rect ("At temple" ...). When it equals
  the caster's own `$C8D7&$1F` the result is "Here" (rect via 0:173C). The `$FF` at 2E:579E is a blank cell. The
  text line is 'B', floor (0FE9 -> VWF), `$20`, `$FF`, 'X', x (0FE9), ',', 'Y', y.
- Heal box: 0:37BC `cp $00 / jr z,$37FC`. It is the A=0 branch of the camp result dispatcher at 0:37B9 (other
  values jump to 0:383D-3865, rects only).

## 4. Icons the scanner also flags (not text; listed so nobody chases them)
| Icon | Font code | Where / writer |
|---|---|---|
| → menu cursor | `$FC` (VRAM1 `$7C` attr `$88`, or VRAM0 `$F0`) | window menus: mode_select, maze_dmenu, maze_settings, battle command/sub-menus, chest menu, spell lists |
| ↑ spell level cursor | `$F9` (VRAM0 `$EF`) | spell sheets 2A (camp_spells_*, battle spell list) |
| × cannot cast / cannot equip | `$F8` (VRAM1 `$78` attr `$88`) | spell list marker (2A:4CBB rect), shop buy 29:4A36 / 29:564C, 2A:6F0D |
| ▼ typewriter prompt | VRAM1 `$79` | 0:1F2D |
| ● equipped / in party | `$2A` | group 1 |

## 5. Hook notes (shared)
- Single-character sites mostly have the shape `ld a,n / ld [de],a / inc de` (4 bytes). A `call Stub_Char /
  db n` (4 bytes: the char comes from the return address, printed as a one-character VWF string, DE+1) would
  fit those sites exactly, with no relocation: 2E dots, 0:3822 '/', 29:6535 (here followed by `inc de`, inside
  a branch). Adjacent letters should be one string ("HP", "B1 X0, Y0"), as in CardHP, so they kern.
- `[hl]` / `[hli]` / `ld [hl],b` variants (29:5628, 22:5448, 27:485F, 26:5439) need their own entry, or a
  block rewrite with `jp`.
- Before patching, diff each site against the EN build (all bytes above are EN == JP unless marked).

## 6. Open questions
- Does any real item have a negative AC byte (group 5)? I did not walk the item records.
- Find allies with a lost character (bank 1F list) was not reached. The static census shows no 8 px literals
  there.
- Whether the owner counts group 6 (automap axis tiles) as "automap graphics" (out of scope) or as digits to
  convert.
- Effect ids 56-124 (class skills) and battle-only effects were not swept.
