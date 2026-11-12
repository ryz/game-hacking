> Copied from work/re/sheet2c.md (tracer, 2026-11-12); scratch, states and screenshots stay in the untracked
> work/re/sheet2c/. Hidden developer UI: not restyled (decided 2026-11-12, low priority).

# Bank 2C "second character sheet" (numbers.md group G) - what it is, how to reach it, field map

Original ROM = Rev 1 (`rom/wizardry_empire_j.gbc`), EN = `build/wizardry_empire_en.gbc` (b9f4a72, built 05:20).
Scratch: `work/re/sheet2c/` (scripts, states, `shots/`).

## 1. Answer

Group G is not a player-facing character sheet. It is the developers' **debug mode**. 2C:4036 is a 4-page
**debug character editor** and 2C:4C24 is a **debug event tester** in the maze. Both start with
`ld a,[$C003] / cp $A5 / ret nz`. `$C003` is set to `$A5` only by a button code on the STAR*FISH logo
(01:686A clears it, 01:686E-6883 compares the inputs against the table at 01:688F `04 40 80 01 20 08 00`).
The code is **Select, Up, Down, A, Left, Start**. Once the code is entered, power-on shows a sound-test menu
("BGM / SE / MASK VERSION 1.1 / END", 01:689E) instead of the title. Normal play never reaches either
screen. In debug mode:
- 26:491E: Training Grounds > View character, roster list (26:48BF loop, cursor `$D001`). **Select** opens the editor
  for the highlighted character, then 0:2BFC writes the edited data back.
- 2A:52A4: maze Camp > Inspect > "Inspect whom?" list (cursor `$D005`). **Select** opens the same editor (+ 2A:6388, 0:2C33).
- 20:522B: maze Select menu (Search / Pick a lock / Find allies / [End the quest] / Settings, 20:49B2). Confirm
  any item except the first with **A while Select is held** to open the event tester (2D:7C63 notice "-- About
  debug mode --", then menu 2D:62BB: event number, param 1, param 2, flag clear). Confirming the first item
  ("Search") goes to 20:51FD instead (another debug path, not examined). With the flag on, pressing Select in
  the maze first forces a fixed battle (20:4834 sets `$C00B` bit 1, `$C48E` = the map square's monster). The
  route below therefore opens the menu first and then sets the flag.

Recommendation: the owner's consistency goal is for screens a player sees. This one is hidden debug UI with
untranslated debug help text, so a restyle is optional and low priority. One EN bug found here is general,
though: see "DE after an English rect" in section 4.

## 2. Routes (all reproduced; scripts in work/re/sheet2c/)

`reach.py ROM OUT [--state=S] TOKENS`: power-on; at frame 260 tap select, up, down, a, left, start (input_tap
2+8 frames, then 4 frames each); run 200 frames; then the tokens (emu.py-like; `tstart` = tap start + 60 frames;
`hold:k1+k2:N`; `save:NAME`). The script prints count-only hits of 2C:4036 / 2C:4C24 for each token.

| State (work/re/sheet2c/states/) | From | Tokens | Check |
|---|---|---|---|
| `jp_town_dbg.state` / `en_town_dbg.state` | power-on + code (JP / EN ROM) | `up a w400 tstart*4 b w60` (Up wraps to END on the sound menu; A leaves it) | `$C003=$A5`, town |
| `jp_roster.state` / `en_roster.state` | town_dbg | `right a w60 down a w60` (Training > View character) | 26:48DD loop running |
| `jp_sheet1..4.state`, `en_sheet1..4.state` | roster | `select w60` (page 1), then `start w60` for each later page (4 pages, cycles) | 2C:4036 hit = 1 |
| (EN, from camp) `en_camp_dbgpoke.state` | `party_en/camp.state` + poke `$C003=$A5` | `a w40 select w60` (Inspect, list, Select) | 2C:4036 hit = 1, shot `shots/p1_from_camp_inspect_en.png` |
| event tester EN | `party_en/camp.state` + `b w200 down*3 a w300` (= `en_maze_quiet.state`, no random battle with this timing; `en_maze_quiet_nodbg.state` = same with `$C003=0`) | `maze_prompt.py ROM en_maze_quiet_nodbg.state OUT select`: b w20, select w60 (menu), **poke `$C003=$A5`**, down w30, hold select 4 frames, then select+a 10 frames, w60 | 20:49C3, 20:522B, 2C:4C24 hits = 1 each |
| event tester JP | `jp_camp.state` = emu.py JP `boot,PARTY,left*3,a,w60,a,w150` (PARTY from tour.py) + `b w200 down*3 a w300` (= `jp_maze_quiet.state`) | same `maze_prompt.py`; then `a w60` for the menu (`jp_mp2/prompt2.state`) | same hits |

`party_en/` = `tools/party.py --out work/re/sheet2c/party_en` on this build (the Nov-11 work/states/party states
predate the current VWF signature). Pitfall: select and A pressed on the same frame register A only (`$FF8B` =
$01 at 20:49C3), so Select must be held first.

Screenshots (3x, `work/re/sheet2c/shots/`): `p1_identity`, `p2_items`, `p3_stats`, `p4_monsters`, `event_menu`
as `_jp.png`, `_en.png`, `_cmp.png` (JP | EN), `event_notice_jp.png`, `p1_from_camp_inspect_en.png`.

## 3. Field map (2C:4036 editor)

Window buffer `$D800` (WRAM3, stride 32; row 0 and col 0/19 = frame; cleared to `$FF` by 0:1A42). Cell = row/col
of `$D800+32*r+c`. Number calls go through 0:0FE9 (A = bytes, B = `$30` base, C = digits | bit 7 = pad, so the
field is right-aligned). "EN" = how the cell renders in the EN build, classified by comparing VRAM tiles with the
original font (`cells.py`): **8** = original 8 px glyph, **V** = VWF, **G** = garbage. Each field's EN cause is in brackets.
Record working copy at `$C497-$C4F4` (race `$C497`, class `$C498`, alignment `$C499`, gender `$C49A`, status
`$C49B`, level `$C49C`, days `$C49E`/`$C49F` bit 0, age `$C49F`>>1, items `$C4A0+2n`, stats `$C4E0-5`, gold
`$C4E8`, EXP `$C4EC`, max HP `$C4F1`, HP `$C4F3`). Cursor `$F0` at col 1, row `$FFE0`+1 (2C:4C07-4C19).

**Page 1, identity (draw 2C:404A, calls 4826/4915/4951/498C/49B8/4A70/4AB3/4AF3/48FD/4C07):**

| Row, cols | Field | Site | Format | EN |
|---|---|---|---|---|
| 1, c2-5 | race | 2C:4826: 0:0C97 copies 4 bytes from 26:71B0+4*`$C497` into a RAM rect at `$C54F` (`[4][1]`), blitted at 2C:485C (dst `$D822`) | text | G (raw kana from the JP table: the 0:0C97 copy is not hooked) |
| 1, c15 | sub-selector `$FFE1`+1 | 2C:408D (`$D82F`, C=$81: 1 digit) | number | V |
| 2, c2-7 | class | 2C:4915: 6 bytes from 26:7211+6*`$C498`, blit 2C:494D (`$D842`) | text | G (EN table entry 0 bytes `41 6f 41 ..` copied raw) |
| 3, c2-6 | alignment | 2C:4951: 5 bytes from 26:71D5+5*`$C499`, blit 2C:4988 (`$D862`) | text | G (same) |
| 4, c2-4 | gender | 2C:498C: rect 26:715C (male) / 26:7161 (female), blit 2C:49B4 (`$D882`) | text | V "Male" (rects.json) |
| 5, c2-4 | status byte (raw) | 2C:49C0 (C=$83, **DE from the 0:1789 return**, see section 4) | 3 cells, right | **missing in EN** |
| 5, c14-18 | status word | 2C:4A2B: 5 bytes from 26:7574+5*idx (`$C49B`&$3F, capped 7), blit 2C:4A6C (`$D8AE`); bit 7 / Silenced variants at 2C:49F4/4A28 | text | G |
| 6, c2 | 'L' | 2C:4A73 `ld a,$4C` / 4A75 `ld [de],a` | 1 cell ASCII | 8 |
| 6, c3-4 | level `$C49C` (2 bytes) | 2C:4A7F (C=0: no pad, left) | left | V |
| 6, c10 | `$C4E6` & $1F | 2C:4A94 (C=0) | left | V |
| 6, c11 | '-' | 2C:4A97 `ld a,$2D` / 4A99 | 1 cell ASCII | 8 |
| 6, c12 | (`$C4E6`>>5)+1 | 2C:4AAF (C=1) | 1 digit | V |
| 7, c2-4 + c5-6 | age + 'さい' | 2C:4AC8 (C=$83) + 2C:4ACB (EN inline 'yrs') | right + label | V / V |
| 8, c2-4 + c5-6 | days + 'にち' | 2C:4AE8 (2 bytes, C=$83) + 2C:4AEB (EN 'days') | right + label | V / V |
| 9, c2-5 / c9-18 | 'ゴールド' / gold `$C4E8` (4 bytes) | 2C:4AF6 (EN 'Gold') / 2C:4B11 (C=$8A) | label / right at c18 | V / V |
| 10, c2-6 / c9-18 | 'けいけんち' / EXP `$C4EC` | 2C:4B17 (EN 'EXP') / 2C:4B35 (C=$8A) | label / right at c18 | V / V |
| 11, c2-7 / c10-14 | 'HP-MAX' / max HP `$C4F1` | 2C:4B3B-4B52 (6 ASCII `ld a,X / ld [de],a`) / 2C:4B5D (C=$85) | label / right at c14 | 8 / V |
| 12, c2-3 / c10-14 | 'HP' / HP `$C4F3` | 2C:4B63-4B6A / 2C:4B79 (C=$85) | label / right at c14 | 8 / V |
| 13, c1-17 | 'ステータス:ABへんか/LRまほう' | rect 2C:48EA (17x1), blit 2C:40A4 (`$D9A1`) | text | G (not in rects.json) |
| 14-16, c1-18 | 'ーーーー DEBUGモード ーーーー' / 'スタートキーで きりかえ' / 'セレクトキーで しゅうりょう' | rect 2C:4860 (18x3), blit 2C:4911 (`$D9C1`), all pages | text | 8 ('DEBUG' and dashes) + G |

**Page 2, items (2C:41A9 → 4BC7):** rows 1-8 = item slots n=0-7 (`$C4A0+2n`):
c2-4 item id (2C:4BA3, C=$83, right); c5.. name, max 10 chars, copied raw by the loop 2C:4B84-4B8B (`ld a,[hli] /
or a / ret z / ld [de],a / inc de / dec c / ret z`) from `$C550` (item name), or from ROM 2C:4570 'アイテムなし'
when the id is 255; then the flags byte `$C4A1+2n` right after the name (2C:4BC3, C=3: left, so its column depends on the
name length). EN: id/flags V, names 8 px ASCII from items.json, cut at 10 ('Leather Ar'), 'アイテムなし' G.
Rows 9-13: rect 2C:4898 (16x5, blit 2C:41E1, `$D921`): 'じょうけん:うえにつめてあること' / 'アイテムじょうほう:B+スタート' /
'A:アイテムじょうほうのしょきか' / '1:ステータスなし' / '2:みしきベつ 3:のろい' (G in EN); row 11 c18 `$FFE1`+1
(2C:41F4, V).

**Page 3, stats (2C:430E → 433D, 4577):** rows 1-6 c4-9 stat labels = rect 26:735A (blit 2C:433D,
`$D822`; the main card's label rect, V 'Strength..Luck' in EN); c10-12 stats `$C4E0-$C4E5` (2C:4582/4590/459E/45AC/45BA/45C8,
`$D82A+32n`, C=$83 right, V). Row 8 c2-4 index `$FFE2` (2C:45DB, V). Row 10 c2-4 item id `$C5C7+$FFE2` (2C:45F7,
V) + name (0:24FF into `$C54F`, or 2C:4570 for 255) via 2C:4B84, max 10 (G for 'アイテムなし').

**Page 4, monster test (2C:440D):** row 1 c2-4 'ON '/'OFF' for `$C5DA` (2C:4433-443D / 4440-444A direct writes,
8 px ASCII in both). Rows 2-5 = 4 monster ids at WRAM4 `$D918-$D91B` (0-166; L/R adjust 2C:44FE/4529): c2-4 id
(2C:4624, C=$83, V) + monster name (0:2394 into `$C510`) via 2C:4B84, max 10 (8 px ASCII from monsters.json,
'Lion of He'; id 171 is out of range, so garbage in both builds).

**Event tester (2C:4C24):** typewriter messages 2D:624A (debug notice, 9 rows) and 2D:62BB (menu). Neither is
in messages.json, so the EN shows garbage ('-- o/d50" --'). Numbers 2C:4E04/4E1A/4E30: event number / param 1 / param 2
(`$FFB0-2`), C=$82 (2 digits right), at `$D98F/$D9AF/$D9CF` (rows 12-14, c15-16), V in EN. Menu value 1 =
chest debug (2C:4C7B-4CE2: `$FFC4-6`, pushes `$C00B`|4); 8/9 set `$C00B` bit 5 (ending); <$28 calls the
event dispatcher 2D:63EB.

## 4. Hook proposal (only if the owner wants the debug screens done)

Do this fix first, because it is general:
- **DE after an English rect.** 0:1789 returns DE = dest + h*32 (0:17AC-17B4 advance per row). The VWF path of
  `Stub_RectCommon` (asm/vwf.asm 1388-1393, tail call to VWF_Rect) does not. 2C:498C (gender rect) returns
  and 2C:49B8 prints the status number at that DE. In EN, DE = $60C0 at 2C:49C0, so the number is written outside the
  buffer and is missing on screen. Fix: VWF_Rect (or the stub) returns DE = `[hDstLo/Hi]` + h*32. A
  straight-line scan of all 309 `call $1789/$173C` sites (`de_after_rect.py`) found no other site that reads DE right
  after the call. Cases that cross a `ret`, like this one, are not covered by that scan.

Restyle items for the editor:
- Race/class/alignment/status copies are banked copies with `call $0C97` at 2C:4845/4936/4971/4A55 (+49DD/4A11
  variants). Same precedent as the shop alignment: replace each with `call Stub_Fix / db n|$80, $26` keyed on the bank-26
  table row. This also fixes the copies of class/alignment table entry 0, which the EN build overwrote.
- Labels 'L' 2C:4A73, '-' 2C:4A97, 'HP-MAX' 2C:4B3B (6 x `3e xx 12 13`, 24 bytes), 'HP' 2C:4B63, 'ON'/'OFF'
  2C:4433/4440: inline.json entries (`rst $38` + bank + ptr), like the four existing bank-44 entries.
- Rects 2C:4860 (18x3), 2C:4898 (16x5), 2C:48EA (17x1), string 2C:4570 (7 bytes incl. $00, read through `ld hl` +
  2C:4B84): rects.json / fixtables.
- Name loop 2C:4B84 (10-char cap) → Stub_PrintZ-like with a 10-cell limit, for 8 px names and VWF.
- Numbers are already VWF. For card-style right alignment, the level (C=0, 2C:4A7F), `$C4E6` pieces (C=0/1)
  and the item flags (C=3) are the only unpadded fields. All others already pad to their width.

## 5. Open / not confirmed

- Meaning of `$FFE1` (shown at r1 c15 and r11 c18 of page 2; 'LRまほう' suggests a spell-level selector), `$C4E6`
  (row 6 'x-y'), `$FFE2`/`$C5C7` (page 3 row 10, a storage list?), page-4 `$C5DA` ON/OFF and what consumes `$D918-$D91B`.
- 20:51FD (Select+A on 'Search' in debug mode) was not examined.
- Not tested whether the maze menu opens after the forced debug battle (20:4834) without the `$C003` poke. The event-tester
  route uses that one poke. It sets the same byte as the logo code.
- docs/re/reach.md says 2C:4C96 is "around the found-character sheet". It is the event tester's chest-debug branch.
