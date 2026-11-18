# Missing Japanese text: prologue, title/options, item effect descriptions (tracer, 2026-11-12)

> Status: all applied in de456d3. Credits are not ASCII: a credits charset at codes $80+, 2C:5C51-6223, 10
> rects, now VWF rects in rects.json.

Rev 1 addresses. Original ROM `rom/wizardry_empire_j.gbc`. English build copied from `build/wizardry_empire_en.gbc`
(built 2026-11-12 01:49, HEAD b57597a) to `work/re/missing-text/en_build.gbc`. Scratch scripts, shots and states
are in `work/re/missing-text/`. Nothing was patched.

## 1. Answer

**(1) Prologue: the game has none.** From power-on the game goes logo -> copyright -> title. The title waits
for A or Start with no timeout (2B:59E4 loop; idle for 30000 frames, nothing changes). Start opens Mode
Settings, which is shown only while SRAM flag `$C5C6` bit 6 is clear (01:6121-6134 -> 2B:454E). Then it goes
to the town (01:615D -> 2B:5A50). No other path prints story text. The story intro is the Notice Board scroll,
which is done. The story text that is really missing is the **ending (epilogue)**: 7 pages of attribute rects
at **2B:6435-6E62**, drawn by the ending tasks 2B:4935 (first clear) and 2B:4AEA (second clear plus credits).
None of these pages is in `rects.json`, and the English build shows garbage there (checked in the emulator).

**(2) Title / mode select / options: no Japanese left.** The title is a graphic logo ("Wizardry EMPIRE",
Latin letters). The publisher logo and copyright screens are English graphics. Mode Settings is fully English
in the EN build, with all values toggled (On/Off, Normal/Mania). Found on the way: the **"End the quest"
power-off screen, 2B:6E83**, a rect not in the script. It shows garbage in the English build.

**(3) Item effect descriptions: they are the museum "Special"/"Use" rects in bank 41, not bank 46.**
Bank 46 holds only typewriter text for the 110 spell descriptions (the only bank-46 text reader in the ROM is
`ld a,$2E / ld [$C1C1],a` at 2A:4ABE). Using an item prints the bank-38 rects 26:7796-77C5 (all translated).
**Two museum "Special" rects are still missing: 29:78D4 and 29:78FE**, entries 30 and 31 of the table at
41:63B6, used by the Ring of Healing, Ring of Life and Ring of Death.

Found on the way (not in the three areas, but untranslated and on a normal screen): **the Training "change
class" confirm prompt, 26:76C8** ("Become a <class>?"). It shows garbage in the English build (checked).

## 2. Findings

### F1 - Ending text (epilogue), bank 43
| Rect (Rev 1) | Size | Site (`ldh [$b8]` setup) | Content (first line) |
|---|---|---|---|
| 2B:6435 | 16x11 + attrs | 2B:49A8 | ちじょうにもどった きみたちを まっていたのは ときのこうていの しであった ... |
| 2B:6597 | 16x13 + attrs | 2B:4A2F | くしくも ときをおなじくした ふたりのこうていの し ... |
| 2B:6739 | 16x13 + attrs | 2B:4A8D | と そのとき まどうをちゅうしんにして まちぜんたいがゆれだした ... |
| 2B:68DB | 16x13 + attrs | 2B:4B7A | いじげんのものはさり デーモンたちも まかいへともどっていった ... |
| 2B:6A7D | 16x13 + attrs | 2B:4C01 | ちじょうに のこったものは がれきにうもれた まちなみと ... |
| 2B:6C1F | 16x9 + attrs | 2B:4C5F | かくちで ひのてがあがり ひとびとの ひめいがひびきわたる ... |
| 2B:6D41 | 16x9 + attrs | 2B:4CBD | そして はるかとおいみらい ひとりのきょうおうが 1つの しろを ... |
| 2B:6E63 | 15x1 + attrs | 2B:4D25 | `Wizardry EMPIRE` (ASCII, nothing to translate) |

- Format: `[w][h][w*h tiles][w*h attributes]` rects. Attribute bit 3 = the glyph is in VRAM1, i.e. code `|$80`.
  `tbl.dec` without attributes gives nonsense such as `ぅぉ ていこくうか`; `work/re/missing-text/rectattr.py`
  decodes them correctly. Text rows alternate with empty rows (double spacing).
- Printer: `0:173C` (rect with attributes), destination `$D062` (bank 3). This is the same path as Mode
  Settings (2B:462D), which works in the English build.
- Flow: the main dispatcher 01:618F reads `[$D000]` (WRAM1). Value 8 -> 01:61A0. If `$C5C6` bit 7 is clear,
  it runs task 2B:4935: pages 6435/6597/6739 ("the rift opens wider, evil is not gone"). Then 2B:4AD1 sets
  bit 7 and saves. Otherwise it runs task 2B:4AEA: pages 68DB/6A7D/6C1F/6D41, then "Wizardry EMPIRE", then
  the staff credits (credits are ASCII already).
- In script: no. There is no rects.json entry with bank 43 between 63DE and 6F0C. Searching by text finds
  nothing either.
- How to reach: in normal play, after clearing the game. I did not trace which code stores 8 into `[$D000]`
  (the town code only cycles it 0-7). To force it: from a town state, stop at 2B:5B70 (the town input handler,
  WRAM bank 1), write `$D000 = 8`, then press A. Script: `python3 work/re/missing-text/ending2.py ROM TOWNSTATE
  OUT first|repeat N` (`repeat` also sets `$C5C6` bit 7). Town states: `work/re/missing-text/town_jp.state`
  (JP, `boot`) and `town_en.state` (EN build, `boot`). Results: `end_jp/sheet.png` (both endings plus credits,
  hits 2B:4935=1, 2B:4AEA=2, 2B:49A8=1) and `end_en/sheet.png` (pages are garbage).
- Note: on the forced JP run the attribute-bit-3 cells show wrong glyphs, because coming from the town the
  VRAM1 font half is not loaded and the ending task loads only `01:4300` frames. In real play the screen
  before the ending probably loads it (not verified). The VWF draws its own tiles, so this does not matter for
  the English pages.
- Reference patch (`rom/wizardry_empire_ref.gbc`, bank 2B $6540-$6C00) has an English version of these pages
  ("When you arrive back in town, you find the Empire in ruins..."). It can serve as a style reference only.

### F2 - "End the quest" power-off screen, bank 43
| Location | Format | Printer | Content |
|---|---|---|---|
| 2B:6E83 (data to 6F0B) | rect 15x9, no attributes | `0:1789`, set up at 27:6EA4-6EB8, destination `$D083` | おつかれさまでした / このじょうたいで でんげんを / きることが できます / Aボタンを おせば ぼうけんを / さいかいできます |

- Reach: `boot,a,w60,down,down,a,w60` (Edge of Town -> Outskirts -> "End the quest"; no party needed). State
  one input before: `work/re/missing-text/edge_jp.state` (JP, `boot,a,w60`). The count breakpoint 27:6EB8 fired
  once and `0:1BAB` did not fire, so the screen is this rect and not a typewriter message. EN:
  `work/re/missing-text/quit_en/sheet.png` shows garbage.
- In script: not by address. The same text is in messages.json as 45:620A (a typewriter version printed from
  another site), so a text-only coverage check misses this rect. The English line exists there and can be
  reused.

### F3 - Item effect ("Special") descriptions, bank 41
| Rect | Size | Table entry | Items (record byte +38 = special index) | Content |
|---|---|---|---|---|
| 29:78D4 | 10x2 + attrs | 41:63F2 (index 30 of 41:63B6) | 207 Ring of Healing, 211 Ring of Life | そうびして あるくと / HPが5ずつかいふく |
| 29:78FE | 10x2 + attrs | 41:63F4 (index 31) | 210 Ring of Death | そうびして あるくと / HPが5ずつへる |

- Printer: `0:1723` at 41:667D, destination `$D967` (museum item page, "Special" row), as in docs/re/museum.md.
  That doc counts 30 special rects; the table actually has 32 (index 0 = なし 29:74AE through index 31 =
  29:78FE). The two last ones were missed.
- Byte diff between EN and JP: 29:78AA (index 29) carries redirect header bytes, while 29:78D4 and 29:78FE are
  identical to the Japanese. So those two still print raw kana.
- Reach: museum item page of one of those rings. Mark it seen by setting bit `id&7` of `$C592+(id>>3)` (207 ->
  `$C5AB` bit 7; 210 -> `$C5AC` bit 2; 211 -> `$C5AC` bit 3), then open Museum -> items -> the rings' category.
  Not done on screen; the record mapping was checked on known items instead: index 1 -> Helm of Warping
  (テレポート), 28 -> Key Card (elevator), 29 -> Fairy's Heart (fairies).
- Not present in this game: an item description in bank 46, or a separate item "info" text when you use an
  item. Item use prints the shared rects 26:7796 (HP restored), 77A2 (cast the spell), 77AF (healed), 77B9
  (nothing happened), 77C5 (summoned), all already in rects.json.

### F4 (aside) - Class-change confirm, bank 38
| Location | Format | Printer | Content |
|---|---|---|---|
| 26:76C8-7757 | 9 records x 16 bytes, no header (class order せんし, まほうつかい, そうりょ, とうぞく, ビショップ, サムライ, ロード, ニンジャ, ゆみつかい) | 26:5072: `hl = $76C8 + 16*class`, writes `[$10][$01]` to `$C632`, copies 16 bytes, then `0:1789` from `$C632` (`$FFBA=$26`) at 26:50A2 to `$D0C3` | `<class> になりますか?` |

- Reach: `boot,right,a,w60,down*4,a,w60,a,w60,a,w60` (Training -> Change class -> first character -> a class).
  The fresh SRAM has a default fighter, so it works from power-on. 26:5072 was hit once on both ROMs. EN
  screenshot: `work/re/missing-text/cls_en.png` (garbage line above Yes/No). JP: `cls_jp.png`.
- In script: no (nothing at 26:76C8; the census misses it because it has no `[w][h]` header in ROM).

### Not reported (already known or debug only)
- Debug-mode text: 2C:4860, 2C:4898, 2C:48EA (rects), 45:624A, 45:62BB (messages), and the bank-45 debug menu
  around 2D:6320 ("たからばこデバッグ", "エンディング:..."). Reachable only with `$C003=$A5`.
- 26:7006-70D7, the kana pages of the name entry chart (the patch uses Latin name entry).

## 3. Hook proposals

- **F1 ending, data only.** Add 7 `rects.json` entries (bank 43, addresses above, `w` 16, `h` 11/13/13/13/13/9/9,
  `"attrs": true`, same flags as the Mode Settings rects 2B:77BB/77CD). Keep the empty rows, or use them, since
  the VWF fits about 2x the characters per row. Per page that is at most 7 rows x 16 cells = 112 tiles,
  under the 157-tile pool. 2B:6E63 stays as it is. No code change: the `0:173C` sites already go through the rect
  hook (Mode Settings proves it on the same routine and bank).
- **F2 power-off, data only.** One `rects.json` entry (bank 43, 0x6E83, w 15, h 9, no attrs). The text can come
  from messages.json 45:620A.
- **F3 museum, data only.** Two `rects.json` entries (bank 41, 0x78D4 and 0x78FE, w 10, h 2, `"attrs": true`,
  `"nofix": true` like 29:7888/78AA). Suggested: "Walking while worn / restores 5 HP" and "... / drains 5 HP".
- **F4 class confirm, needs code. Use the same method as `insert_titles`.** Make each 16-byte record a
  redirect header `[$90][$01][bank][lo][hi]` plus padding. At 26:507F-5087 (`3e10 4f 12 13 3e01 12 13`, 9 bytes),
  keep `ld a,$10 / ld c,a` (C = copy count) and NOP the two header stores (`12 13`, `3e01 12 13`). The 16-byte
  copy then places the record itself at `$C632` as the rect header that `0:1789` reads. Preserve C and DE. Check first
  that the rect hook accepts a RAM source with `$FFBA=$26` (the title case uses `$1770`, not `$1789`). Script:
  9 lines like "Become a Fighter?", max 16 cells (128 px).

## 4. Open questions
- Which code stores 8 into `[$D000]` in real play (the final boss/event). Not found by a byte search
  (`ld [$d000],a` with a nearby `ld a,8`, or `ld [hl],8`). State 6 (01:6661, task 27:4BB1) dispatches on the
  value its task leaves in `[$D000]`, which is the most likely route.
- Whether the VRAM1 font half is loaded when the ending runs after a real victory (it matters only for the JP
  reference shots).
- The F3 rings were not seen on screen (museum navigation to the rings' category was not scripted).
- `census_msgs` output for banks 45/46/49 still has many unknown addresses. All the ones I read are
  mid-string offsets from sites whose text bank it guessed wrong, or debug text. I did not go through all 278
  lines (the filter script crashed on a null `jp` field partway).

## 5. Method / files (`work/re/missing-text/`)
- `scan.py`, `scan2.py`, `scan3.py`: kana runs in the ROM checked by text against every script jp field (scan3 =
  bigram-scored, `scan3.txt`). Result: no uncovered story-like typewriter text.
- `rectsites.py` -> `rectsites.txt`: every `ld a,lo/ldh [$b8] + ld a,hi/ldh [$b9] (+ ldh [$ba])` rect source,
  decoded with attributes and checked by address against rects.json (50 hits, mostly graphics/debug noise;
  F1, F2 come from here).
- `rectattr.py ROM BANK ADDR N`: decode a chain of attribute rects.
- `idle.py`, `idle/`, `idle2/`: power-on idle 6000 and 30000 frames (title static after frame 780).
- `flow.py`: count breakpoints on the title/mode-select/town branches. `pro.py`, `pro2/`: mode select taps.
- `mode_en/`, `men2/`, `mjp2/`: Mode Settings with every value toggled (EN all English).
- `quit.py`, `quit_jp/`, `quit_en/`: power-off screen. `ending.py` (first attempt, unused), `ending2.py`,
  `end_jp/`, `end_en/`: forced endings (states `end_*/end.state`). `cls.py`, `cls_jp.png`, `cls_en.png`.
- States: `title_jp.state` (JP power-on + 800 frames), `edge_jp.state` (JP `boot,a,w60`), `town_jp.state`
  (JP `boot`), `town_en.state` (EN `boot`), `pro_jp_start2.state` (JP `w750,start,w60,start,...`, mode select).
