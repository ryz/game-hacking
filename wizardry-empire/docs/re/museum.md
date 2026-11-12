# Museum (はくぶつかん): where its text lives and how it is printed

> Addresses refer to the Japanese **Rev 1** (the base since 2026-11-12). Written for v1.0 and converted with
> `tools/revmap.py`; a few marked "(v1.0)" did not map. `docs/re/rev1.md` lists what Rev 1 changed.

Tracer notes, 2026-11-11 (copied from work/re/museum.md). Original ROM traced, English build a98cef8 used for comparison. Scratch files (states, scripts, scratch ROM) are in the untracked `work/re/museum/`.

## 1. Answer

The museum code is all in bank 41 (`$29`, `41:5B00-6B20`). It uses the ordinary text paths and the ordinary font,
plus one small extra glyph sheet:

- **Rects.** Headers, labels and the item "use" and "special" descriptions are `[w][h]` rects in bank 41
  `$6F3D-$78D7`. They are blitted by `0:1789` (tiles only) or `0:173C` (tiles plus attributes). Most of the
  attribute rects are missing from `script/rects.json`. The census decodes them without attributes and missed them.
- **Names.** Item and monster names come from the same bank-40 and bank-57 records that `items.json` and
  `monsters.json` already translate, copied to `$C54F` (`0:24FF`) and `$C50F` (`0:2394`). The museum keeps no copy
  of its own. Bank 41 does have its own copies of the unidentified-name lists: `41:5706` for items, `41:6730` for
  monsters.
- **Code writes.** Numbers, class letters, monster abilities and element labels are written tile by tile by code.
- **The extra glyphs.** The earlier note about "a separate glyph set" is partly right. On entry pages the game DMAs
  33 tiles from `01:4100` to VRAM0 `$8D00` (codes `$D0-$F0`, attribute bit 3 clear). They hold
  `) ちゅうりつ EXP 相手 石化 眠 仲間 呼 恐怖 呪文 抵抗 地水火風 精… 聖 無 法 神 ↑ →`. See
  `work/re/museum/glyphs_01_4100.png`.

The item side can be fixed with three small hooks and data entries:
- `41:66C2` becomes `jp Stub_PrintZ`.
- The `41:62C7` list copy calls `Stub_PrintZ`.
- The `41:5706` unidentified-name table is repointed.

I tested the first two on a scratch copy of a98cef8; both work. **The monster room is blocked.** It uses a third
font layout the VWF does not know: LCDC bit 4 = 1 (unsigned tile data), the whole font in VRAM1 `$8000-$8FFF`
loaded by `41:5FE8-608F`, and every text cell with attribute bit 3. In the English build `VWF_FontLoad` drops or
misplaces those loads, so all monster-room text (list, page, digits, even ASCII) shows as garbage. The VWF needs
layout support before any monster hook makes sense.

## 2. Evidence

### Reaching the screens (all states in `work/re/museum/`)
| state | ROM | from | inputs |
|---|---|---|---|
| `jp_menu.state` | original | power-on | `boot,right,right,a,w60` (museum menu, cursor on アイテムの間) |
| `jp_cat.state` | original | `jp_menu` | `a,w60` (item categories; found 65 / unfound 159 in a fresh game) |
| `jp_list.state` | original | power-on | `boot,right,right,a,w60,a,w60,a,w60` (weapon list) |
| `jp_entry.state` | original | `jp_list` | `a,w60` (Hand Axe page) |
| `jp_monmenu.state` | original | `jp_menu` | poke `$C5AE-$C5C2` = `$FF` x21, then `down` |
| `jp_monlist.state` | original | `jp_menu` | same poke, `down,a,w120` |
| `jp_monpage.state` | original | `jp_monlist` | `a,w60` (monster 1 page; `down` on a page goes to the next entry, `a` back to the list) |
| `en_menu.state` | EN a98cef8 | power-on | `boot,right,right,a,w60` |
| `en_after.state` | EN a98cef8 | `en_menu` | poke `$C5AE`=FF x21 and `$C592`=FF x28, `down,a,w120,a,w60,down,w30,b,w60,up,a,w60,a,w60,down*3,a,w60` |
| `en_entry.state` | EN a98cef8 | power-on | `boot,right,right,a,w60,a,w60,a,w60,a,w60,down,w30,a,w60,b,w60,down,a,w60` (ends on the **armor list**, not a page) |

Pokes go through `work/re/museum/py/run.py ROM STATE OUT "ADDR=hex;..." "seq" [save]`.

**Seen flags.** These are WRAM bitfields: bit `i&7` of byte `i>>3` means entry `i` was seen.
- Items: `$C592-$C5AD` (224 bits). Scanned by `41:5D26` per category; categories are in `41:5CBA`, 4 bytes each:
  start, count, start2, count2.
- Monsters: `$C5AE-$C5C2` (167 bits). Scanned by `41:621D`.

The museum writes the list of found ids (`index+1`, 0 = not found, `$FF` = end) to WRAM3 `$D800`. That is the
window buffer, so it gets overwritten when a page opens. A fresh game already has 65 items flagged, and no
monsters; with no monsters the monster room does not open.

### Screens and printers
| piece | source | printer | destination |
|---|---|---|---|
| museum title / menu | rects `29:6F3D`, `6F45`, `6F4D` | `1770` | done in EN |
| item categories, found/unfound | rects `29:6F56`, `6F6A`; numbers by `0:0FE9` | `1770` | done in EN |
| item list row | number `0:0FE9` (`bc=$3083`), name `41:62C7-62D4`: up to 12 bytes from `$C54F` (`ld a,[hli]/or a/jr z/ld [de],a/inc de/dec c/jr nz`) | `41:6282` | `$D082 + $20*row` from col 6, flat layout, attributes untouched (0) |
| page header (item name) | `$C54F` (bank-40 record via `0:24FF`) | `41:66C2` (copies a `$00`-terminated string, then writes attribute `$08` for bytes >= `$80` at +`$400`) | `$D822` (row 1, cols 2-17 = 128 px) |
| unidentified item name | `41:5706[$C560]` -> pointer, +2, `$00`-terminated | `41:66C2` (called at `41:64E3`) | `$D86A` (row 3, cols 10-18 = 72 px) |
| labels | rects `29:6F7E` ●ふかくていめい: (w9), `6F92` ●こうげきりょく: (w9), `6FA6` ●AC:__ ●こうげきはんい: (w17), `6FCA` ●しよう: (w5), `6FD6` ●とくしゅ: (w6), `6FE4` ●ねだん: (w5), `6FF0` ●そうび: (w5) | `1723` (tiles plus attributes) from `41:6416-64B4` | `$D861`, `$D8A1`, `$D8E1`, `$D921`, `$D961`, `$D9A1`, `$D9E1` |
| damage `a~b` | record `$C568-$C56A`, `0:0FE9`; tilde = `ld a,$3B` at `41:650B` | code | `$D8AA` |
| AC, range | `$C56B` (`$2D` minus at `41:6535`), range char from `41:6374` = `S M L ー` | code | `$D8E5`, `$D8F2` |
| use (しよう) value | `41:6378[$C572 or ($C570&$3F)+10]`: 31 rects w2-12, h1-2, with attributes | `1723` at `41:665B` | `$D926` (row 9, col 6; h2 uses row 10) |
| special (とくしゅ) value | `41:63B6[$C575]`: 30 rects w2-12, h1-2 | `1723` at `41:667D` | `$D967` (row 11, col 7; h2 uses row 12) |
| price | `$C562-$C564`, `0:0FE9` | code | `$D9A6` |
| equip class letters | `41:7020` (14 tiles: せまそとビサロニ + ゆヴアムくし) / `41:702E` (14 attributes); bits `$C565` (8 classes), `$C566` (6 extra classes, gated by `$C5C6` bits) | loops `41:659E-662A` | row 15 cols 6,8..18, row 16 col 6; extras row 16 cols 8..18 |
| alignment `(ぜん)` etc. | rects `29:6FFC`, `7008` (uses glyphs `$D1-$D3` ちゅうりつ), `7014`; picked by `$C567&7` | `1723` at `41:66B6` | `$DA01` (5 cells) |

Monster room (font layout described in section 1):

| piece | source | printer | destination |
|---|---|---|---|
| monster list row | number `0:0FE9`, name `41:633E-634F`: up to 12 bytes from `$C50F` (bank-57 record via `0:2394`), skips `$FD` | `41:62F9` | `$D082 + $20*row` col 6, attribute `$08` |
| page name / unidentified name | `$C50F`; `41:6730[$C51C]` (16 pointers to `$00`/`$FD` strings, untranslated in EN) | `41:66E5`: 2 rows of 8 cells, break at `$FD` or 8 chars, attribute `$08` | `$D82B`, `$D8AB` (cols 11-18 = 64 px per row) |
| labels | rects `29:6F7E` (shared with item page), `706C` AC:, `703C` ゴールド: (EN "Gold:"), `7048` HP:, `7050` とくしゅ (w6), `705E` 呪文抵抗 (4 special glyphs) | `1770` / `1723` from `41:67AA-6831` | `$D88A`, `$D8EA`, `$D92A`, `$D947`, `$D967`, `$D9E7` |
| EXP label | glyphs `$D4 $D5` + `:` (`41:68A9`) | code | `$D90A` |
| AC / EXP / Gold / HP | `0:0FE9`; HP tilde `ld a,$3B` at `41:6917` | code | `$D8ED`, `$D90D`, `$D92F`, `$D94A` |
| abilities | `41:6989-6AE7` (called once, at `41:6926`): `$C536` bits 0-6 = どく, 恐怖, 眠り, まひ, 石化, クリティカル, ブレス; `$C537` = ドレイン; `$C538` high nibble = 仲間を呼ぶ, low nibble = にげる; `$C52F-31` != 0 = 2 glyphs `$E9 $EC` (reading unsure). Hard-coded tile and attribute pairs; attribute `$80` = special glyph (VRAM0), `$88` = font (VRAM1) | code | rows 12-14 at fixed cells |
| resistances | element labels: glyphs `$E4-$E7` / `$E8-$EB` (地水火風 / 精…聖無…) written at `41:6844-685C`; values `41:6AB2` -> `6AE8` (`$EE` glyph for 100) | code | rows 16-17 |

How each was confirmed:
- Write watches on WRAM3 `$D861-$D872` from `jp_list.state` + `a`: the hits were `0:1A6E` (clear), the
  `0:175F` blit called from `41:642A` with source `29:6F7E`, and `41:66CB` (unidentified-name copy, HL = `6EA7`).
- Write watch on `$D086-$D08C` from `jp_monmenu.state` + `a`: `41:634C`.
- Breakpoint on `0:1443` (DMA queue) while entering the monster room and its page: `41:6002/6023/6044/6065/6086`
  load `01:4400/4800/5000/4C00/4300` into VRAM1 `$8000/$8400/$8C00/$8800/$8F00`. `21:4241/4268` load the
  picture `05:4000` into VRAM0 `$8000`. `41:60FB` loads `01:4140` into VRAM0 `$8D40`.
- The item-page DMA (`01:4100` -> VRAM0 `$8D00`, `$21` blocks) is at `41:5DA0`.
- VRAM tile comparison against `01:4400` (`py/font.py`):
  - JP item page: split layout.
  - JP item list: flat layout.
  - JP monster screens: font in VRAM1 `$8000-$8FFF`, LCDC `$F7`.
  - EN monster screens: VRAM1 `$8000-$87FF` all blank.
- There is no other `$4400 -> VRAM1 $8000` load in the ROM (pattern search), so this layout is museum-only.

### English build today (a98cef8)
These screens print correctly: menu, categories, Found/Unfound, list numbers, the "●True name:" and "●Special:"
labels, and "Gold:".
- **Item list:** names are printed raw in 8 px and cut at 12 characters ("Staff of Hea", "Leather Armo").
- **Page header:** raw 8 px.
- **Other labels:** the remaining five labels, the use/special values, the class letters and the alignment
  rects are kana and show as garbage, because the kana codes are VWF slots now.
- **Damage range:** `~` (`$3B`) shows as `;`.
- **Unidentified names:** these are broken. 17 of the 25 `41:5706` targets became redirected rects
  (`[w|$80][1][bank][ptr]`). `41:66C2` reads from +2, so it prints the header bytes ("A", `$97`, "J"…) and then the
  leftover Japanese. Only `29:6EA4` "Ax" (in place) is clean.
- **Monster room:** completely garbled (layout problem).

Scratch check: `work/re/museum/scratch_hooks.gbc` is a copy of a98cef8 with `41:66C2 = c3 7d 3f` and
`41:62C7 = 21 4f c5 cd 7d 3f 18 06 00 00 00 00 00 00`. In `work/re/museum/scr/sheet.png` the list shows the full
proportional names ("Staff of Healing", "Studded Leather") and the page header is proportional. `Stub_PrintZ` is
`0:19E1` in a98cef8; `build/wizardry_empire_en.sym` says the same.

## 3. Hook proposals (item side first; monster side after the layout work)

Bank 41 has `$7928-$7FFF` free (1752 bytes) in both ROMs, which is enough for trampolines and tables. The working
tree already adds shop hooks in this bank (`41:4A52`, `41:49EB`, `41:5674`, uncommitted). The museum sites below do
not overlap them.

### A. `41:66C2` (page header and unidentified item name)
- Patch: `jp Stub_PrintZ`, 3 bytes over `e5 d5 2a`.
- Registers: there are only 2 callers (`41:64CB`, `41:64E3`) and both reload HL/DE afterwards. Stub_PrintZ keeps
  BC and returns A=0, as the original did after its loop.
- Data: the bank-40 records (items.json, `$00`-padded) are read unchanged.
- Width limit: 128 px for the header, 72 px for the unidentified name.

### B. `41:62C7-62D4` (item list name, 14 bytes)
- Patch: `ld hl,$C54F / call Stub_PrintZ / jr $62D5` + 6 × `nop`, i.e.
  `21 4F C5 CD <Stub_PrintZ> 18 06 00×6`.
- Registers: `62D5` pops BC/DE/HL, so nothing has to survive.
- Width limit: 104 px (cols 6-18). Items.json names should be linted against 104 px.

### C. Unidentified item names `41:5706` (25 pointers): data only
- Format: write 25 records `[len][$01][ASCII][$00]` in bank 41 free space and point `41:5706+2i` at each record
  start.
- Why the header bytes matter: the shop's counted copy at `41:5738-575A` uses `len` (≤ 16, it pads to 16), and the
  museum and shop `$C54F` copy (`41:56EA`) skip 2 bytes.
- English: reuse the bank-49 strings in lists.json (`49:566B` table, same 25 names: Axe, Arrow, Stone…).
- rects.json: drop entries `29:6ea4`…`29:6f37`. They are not rects: nothing blits them (no immediate references in
  bank 41). Their redirect headers break both readers.
- Width limit: 72 px on the page, 16 bytes for the shop.

### D. Item page labels and values: rects.json entries (mode 1723, existing Stub_Rect1 path)
- **Labels to add:**
  - `29:6F92` w9 (72 px, "●Damage:").
  - `29:6FA6` w17: write `●AC:` in cells 0-3 (32 px) and `@8:●Range:` in cells 8-16. Cells 4-6 (AC value) and
    cell 17 (range letter, written after the blit) must stay free.
  - `29:6FCA` w5 (●Use:).
  - `29:6FE4` w5 (●Price:).
  - `29:6FF0` w5 (●Equip:).
- **Fix:** `29:6F7E` ("●True name:" is wrong). ふかくていめい = the name shown while unidentified, e.g.
  "●Unid. name:" in at most 72 px. The monster page shares this rect.
- **Values:** the 31 use rects (`41:6378` table, includes a second なし at `29:7322`) and the 30 special rects
  (`41:63B6`, なし at `29:74AE`). Use: 1-2 rows of up to 12 cells (96 px; cols 6-17). Special: up to 12 cells
  (cols 7-18). Lines that wrap use the spare row below.
- **Alignment:** `29:6FFC` / `7008` / `7014`: 5 cells, e.g. `(Good)`, `(Neut.)`, `(Evil)`.
- **Census:** the census needs the attribute-aware decode to find rects like these. That is the open
  `census_rects` attribute item.

### E. Small in-place bytes
- `41:650C` `$3B` -> `$2D` (damage "2-7"). The same fix for monster HP at `41:6918`.
- `41:7020` (14 bytes) -> ASCII class initials, and `41:702E` (14 bytes) -> `$80` (VRAM0).
  - The 8 classes have single letters `F M P T B S L N`.
  - The extras collide: ゆ = ?, V(aliant), A(venger), M(usashi) vs Mage, K(unoichi), S(ummoner) vs Samurai.
  - Each letter has a free cell to its right. Two-letter abbreviations need a helper in `$7928+` called in place
    of `ld a,[hl] / ld [de],a` (`41:65AE`, `41:65F5`, `41:6624`, 2 bytes each). That needs a `call` (3 bytes), so
    it means a slightly larger rewrite of the two loops.

### F. Monster room (blocked: VWF layout 3)
- **Layout support needed in `asm/vwf.asm`, in this order:**
  - `VWF_FontLoad`: a load with `hDstVBank=1` and `hDstHi=$80` (`$4400`) sets a new layout. Every font block
    goes to VRAM1 `$8000 + code*16`, keeping `PoolFlags` (drop `$80-$EF`).
  - `SlotTile` / `CellSlot` / Upload: in layout 3, tile = code (no `&$7F`), attribute bit 3 always set, address
    VRAM1 `$8000 + code*16`.
  - GC: mark this layout.
  - Without this, every hook below prints into tiles that are never shown.
- **After that:**
  - List name `41:633E-634F` (18 bytes): `ld hl,$C50F / call <PrintZ that treats $FD as a space> / jr $6350`.
    Width limit: 104 px.
  - `41:66E5` (2 callers `41:686C`, `41:6885`): `jp` to a new 2-line VWF printer. It prints up to `$FD` at DE and
    the rest at DE+$20, 64 px per line, attribute `$08` in layout 3.
  - Monster unidentified names `41:6730` (16 pointers): repoint to `$00`/`$FD` English in bank 41 (English as for
    `49:56FD` in lists.json).
  - Rects `29:7050` / `29:705E`: add to rects.json.
  - Abilities: replace `call $6989` at `41:6926` (3 bytes) with a far call to a new VWF routine. Inputs:
    `$C536`, `$C537`, `$C538`, `$C52F-31`. It must preserve BC (`41:6929` pops it) and the SVBK=3 that the caller
    set; any other registers are free. Script format: one English word per flag at fixed rows and columns, like
    the original cells.
  - EXP / element labels: smallest is a graphics edit of the special glyph tiles `01:4100-4310` (33 tiles; DMAs
    from `41:5DA0` and `41:60FB`). The 8 element labels are one tile each (`$E4-$EB`), so they become 1-2 letter
    tiles. ちゅうりつ (3 tiles) could become "Neutral" as a 24 px bitmap.

## 4. Open questions
- Readings of a few special glyphs are unsure: `$E8-$EB`, `$E9 $EC`, and ゆ in the class list (ゆうしゃ?). The
  glossary has no English for ゆ.
- I did not reach an item with an alignment restriction or with non-zero use/special values on screen. The rect
  tables are decoded from the ROM only.
- `41:5738` (counted copy of the unidentified name for the shop, 8 px raw): which shop list calls it was not
  traced. It prints raw ASCII even after fix C.
- Width of the longest items.json and monsters.json names in VWF pixels was not measured: 104 px for the lists,
  128 px / 2×64 px for the headers.

## Implemented 2026-11-12 (item side)
A (41:66C2 jp Stub_PrintZ), B (41:62C7), C (insert_unid, records in bank 41 $7928+), D (labels + 60 value rects
read from the Japanese tiles with attribute-aware rendering, `nofix`), E ('~' bytes; classes as packed VWF
abbreviations by MusClasses at 41:7B00 instead of single letters). The value rects' Japanese is in
rects.json. Item names: field is 16 chars + $00, byte 17 = unidentified class (the old 17-char limit zeroed it).

## Implemented 2026-11-12 (monster page, Rev 1)
- Headers: rects `29:7050` (とくしゅ -> "Special") and `29:705E` (呪文抵抗, 4 special glyphs -> "Resistance"), w6
  with attributes, centered. Labels `29:706C` "AC:" and `29:7048` "HP:" as VWF rects (were 8 px ASCII).
- "EXP:" (41:68A6-68B9 wrote glyphs `$D4 $D5` + ':'): `Stub_PrintZ` at `$D90A`.
- Element labels (41:6844-685D wrote one glyph `$E4-$EB` per element at `$DA03+4i` / `$DA23+4i`): `MusElem`
  (41:7D40) prints 3-letter words with a 2 px lead ($7C, thin space) in the 2 cells left of each value
  (`$DA02+4i`, cols 2-3, 6-7, 10-11, 14-15): Ear Wat Fir Air / Min Aur Hol Non (地水火風 / 精神 気 神聖 無, the
  spell-element table 2A:49BF). Must keep BC (41:685E uses B).
- Resistance 100 (41:6B10: '10' then glyph `$EE` over the second cell): VWF "100" over both cells.
- Pool pressure: the page (~96 slots) is built in the hidden window while the list (~84) is on the BG; the pool has
  157. `AllocScan` in layout 2 orders the dry GC passes by destination (see vwf.md). Opening a page: 37 frames
  (previous build 22, Japanese 9); each GC costs ~5-6 frames. Closing a page shows a few frames of garbage in
  the page before the list appears (the list redraw under the shown page takes the page's slots; the old build
  showed garbage in the list instead).
- Open: the minus signs ('-' before AC, HP range) are still the 8 px glyph.
