# RAM buffer overflow audit: script text copied into fixed-size RAM (tracer, 2026-11-12)

> Status: fixes applied in d7d7e93 (temple fee) and 85d10bc (NPC names, script/npcs.json); limit tests in
> tests/test_limits.py, the fix-site test in tests/test_coverage.py.

Base: Japanese Rev 1 `rom/wizardry_empire_j.gbc`; English build e45012c (copied to `work/re/overflow/`).
Scratch: `work/re/overflow/` (`scan.py`/`scan26.py` loop finder + `loops*.txt`, `diff.py` JP/EN byte diff,
`pay.py` dynamic check, `tw_1bab.txt` typewriter disassembly).

## 1. Answer
Only five places copy translated text into a fixed RAM buffer by a terminator-driven loop. All five fit today:
`$C50F`/`$C48F` (unidentified monster names, already fixed), `$C54F` (unidentified item types), `$DD36`
(monster names) and the VWF's own `wNameBuf` (`$DFC0`, 32 bytes). `wNameBuf` is full to the last byte by
one 31-character rect row. Everything else is not copied. Inserts (`{F3 ..}` verbs/traps/directions/equip
slots/chest names/statuses, `{F8 ..}` names) are streamed by the typewriter straight from the source; the
typewriter has no string buffer, and `$C1DE` is numbers only. In-place records (items, monsters, templates,
spells, titles, class prompts) are copied with fixed lengths. The remaining terminator copies are hooked by
`Stub_PrintZ`/`VWF_Print2`.

Two other findings came out of the search:
- **Real bug (confirmed dynamically).** `Stub_Fix` was applied to a data copy at `27:662C`, the temple
  resurrection "Who will pay?" gold check. The game copies the payer's 4-byte gold into `$FFB0`, subtracts
  the fee and writes the result back as that character's gold. The English build writes VWF tile codes into
  `$FFB0` instead. The fee check and the payer's new gold are computed from garbage.
- **Untranslated names (coverage gap).** The 8 recruitable NPC records in bank 45 `$4000` are still
  Japanese in the English build. They are in no script file. The name is copied into HRAM `$FFC4` and its
  limit is 7 characters. "Siegfried" (9) does not fit.

## 2. Table

| Source (script) | Copy routine | Destination / size | Right after the buffer | JP max | EN max | Verdict |
|---|---|---|---|---|---|---|
| lists.json `0x570F-0x572D` (unidentified monster names) | `0:36EF` (target), `0:3736` (actor); `ld a,[hli] / cp $FD / jr z / ld [de],a / inc de / or a / jr nz` | `$C50F` / `$C48F`, 13 bytes incl. `$00` (`$FD` skipped) | `$C51C` / `$C49C` = unidentified type index | 12 | 12 ("Gaseous form", "Small figure", "Winged thing", "Gaunt figure"; "Robed\nfigure" = 11 bytes after `$FD` is dropped) | **fixed** (test_limits covers both, same table) |
| same table, battle group panel | `22:570C` + `0:0C97`, fixed 13 bytes | `$C50F + 13*g` (4 slots, `$C50F-$C542`) | next group's slot | 12 | 12 | fits. A 13+ name loses its `$00`; `VWF_Panel` caps at 13 |
| lists.json `0x567D-0x56AD` (unidentified item types) | `0:376D` (`$C5DB` bit 6), `ld a,[hli] / ld [de],a / inc de / or a / jr nz` | `$C54F`, 17 bytes (item record name bytes 0-16) | `$C560` = unidentified class (index into this table and 41:5706) | 7 | 10 ("Odd object", "Long staff") | fits (limit 16) |
| bank-41 unidentified item records (made from the same lists by `insert_unid`) | `29:56FF` (record +2, `$00`-terminated) | `$C54F`, 17 bytes | `$C560` | 7 | 10 | fits (limit 16; `insert_unid` asserts <= 16) |
| same records, shop counted copy `29:5738` | JP: copies `len` bytes and pads to 16 with `c = 16 - len` (`len` = 16 gives `c` = 0, which writes 256 spaces) | screen row | - | - | - | not copied in EN: replaced by blank-16 + `Stub_PrintZ` (bytes `e5 0e 10 3e 20 22 0d 20 fc e1 13 13 d5 54 5d e1 cd e1 19`) |
| monsters.json (bank 57 +`$20`, in place) | `0:2394` fixed 64 bytes to `$C50F`; group records `$D4B8+$40n` fixed 13; `32:4020` FD-strip copy `$D4B8` -> `$DD36` | `$DD36`, 13 bytes | `$DD43` (`$80` flag written at `0:3AA3`), `$DD45/46` pointer | 12 | 12 | fits (insert asserts <= 12) |
| items.json (bank 40, 16 + `$00` in place) | `0:24FF` fixed 40 bytes (`0:0C97`) | `$C54F` record copy | `$C560` = byte 17 of the record | 16 | 16 | fits (fixed copy; field limit 16) |
| templates.json (bank 46, 8-byte field) | fixed `$80`-byte record copies | party/roster records, name field 8 | record byte 8 (data) | 6 | 7 | fits (insert asserts <= 7) |
| spells.json | `0:24E8` fixed 16-byte record -> `$C577` (short name <= 11); `VWF_SpellName` -> `wSpell` | `wSpell` `$D280`, 32 bytes, copy capped at 31 + `$00` | `$D2A0` `wGameNew` | 11 | 18 ("A Miracle for Thee") | fits. Longer names are truncated silently, never overflow |
| titles.json / classprompts.json | `2B:5FB8` fixed 12 / `26:5072` fixed 16 -> RAM rect `$C632` | record = rect header -> VWF | - | - | - | fixed copy, no overflow (width checked by layout_rows: 96 / 128 px) |
| rect rows + fixtables.json via FixMap; inline.json; notice.json; `Stub_PrintZ` sources (names, item names, unid records); `VWF_Print2` | `InlineBody`, `VWF_PrintZ`, `VWF_Print2`, Fix raw path: `ld [hl],a / inc c` into `wNameBuf`, **no cap** (index wraps at 64) | `wNameBuf` `$DFC0`, 32 bytes | `$DFE0` `wInL`, `wInH`, `wInBank`, `wInLo/Hi`, `wInE/D`, `wFixN` ... (the engine's own state) | - | **31** (rect `2b:6d41` "And in the far, distant future,"; also `2b:6435`, `2b:63de`, `27:78f8` at 30); fixtables 9, inline 11, notice 28 (asserted) | fits, 0 bytes to spare. A 32-char row reached by a Fix/Inline/PrintZ path would overwrite `wInL` |
| lists.json verbs `0x56AF-0x5701`, traps `0x5661-0x567B`, equip slots `0x5703-0x570D`, directions `0x572F-0x5735`, commands/abbr `0x5619-0x565F`, gender/race/align/class/status; lists50.json; chests.json | pointer stored in `$C6E3`/`$C6E5`/`$C6E9` (`22:5258`, `22:5406`, `22:7121`, `23:46CB`, `25:4CD6`, `25:51FB`, `25:52D1`, `32:4281`, `32:42BF`, bank-37 chests) or `0:2482`/`2469` | none: `{F3 bank ptr}` is read char by char by the typewriter (`0:1D33` -> `0:1DCE`) | - | - | 27 (verbs) | not copied (width only, `{FA}` wraps) |
| `{F8 00 31 C48F/C50F/C54F}`, `{F8 00 07 D280}` | typewriter `0:1D55` (b = 0: string streamed in place; b != 0: number -> `$C1DE`, 10 bytes, digits only) | - | - | - | - | not copied |
| messages.json | `$F2` redirect, streamed | - | - | - | - | not copied |
| **bank-45 recruitable NPC records** (`2D:4000`, `$80` each, 8 records, *no script file*) | `2D:68C9`: `ld a,[hli] / ld [de],a / inc de / or a / jr nz` into HRAM (then `0:2CA7` compares with the SRAM roster); `2D:68B9` fixed `$80` record copy -> `$C48F` | `$FFC4`, 8 bytes (name field 8) | `$FFCC` (5 writes / 10 reads in the ROM) | 7 (ジークフリート) | untranslated | **coverage gap**. When translated: limit 7. Murphy, Lloyd, Louie, Laila, Kojiro, Badick, Warnard fit; **Siegfried (9) does not** |

The JP->EN records in bank 45 (decoded): 0 マーフィー, 1 ロイド, 2 ルーイ, 3 ジークフリート (7 bytes), 4 ライラ, 5 こじろう,
6 バディック, 7 ワーナード. The EN bytes are identical to the JP ones, so recruiting prints kana codes through the
English font.

## 3. Evidence

### Finding every copy
- Every immediate pointing into the bank-49 table area `55C0-5737` (`21/11/01 lo hi`, all banks; 131 hits,
  most of them noise). The real readers are `0:36D9`, `0:3720`, `0:3757`, `22:5258`, `22:5406`, `22:570F`,
  `22:5A52`, `22:5A65`, `22:7121`, `22:76D2`, `23:46C6`, `25:4951`, `25:4A6E`, `25:4CD6`, `25:51FB`,
  `25:52D1` and `32:43F0/487C/4D93/526F`. Only `0:36D9`, `0:3720` and `0:3757` copy; the rest store a pointer
  for `{F3}`. Bank-50 table `32:5807` readers (`32:424C`, `4268`, `42B3`) also store into `$C6E3`. Bank-41
  table `29:5706` readers: `29:56EE`, `29:573F` and `29:64D3`.
- Loop scan (`scan.py`/`scan26.py`): every backward branch with a body of 14 or 26 bytes or less that loads
  (`2a/1a/0a/7e/3a`), tests (`b7/a7/fe`) and stores (`12/22/77/02/32`). This gave 72 + 23 loops in banks
  0-3F, each classified. The rest are player data (name entry `$D060`, SRAM roster `$A001`, party records
  `$C800`), list/sound data (`0:3ABE`, `20:4E26`, `2B:4364`, `2E:53B8`), screen writes (rect blitters,
  `2A:4F34` -> `$D142`) or hooked. All 24 loops whose EN bytes differ are `call $19E1` (`Stub_PrintZ`) or
  `jp $19E1` or a trampoline (list in `diff.py` output). `0:0FCE`/`0:0FE2` (banked `$00` copies) have no
  callers.
- Typewriter `0:1BAB` (`tw_1bab.txt`): `$F3` (`0:1D33`) and `$F8` with b = 0 (`0:1D55`) only set
  `$C1D0-$C1D2` and then read the insert byte by byte (`0:1DCE`). `$F8` numbers go through `$C1DE` (10 bytes).
- EN/JP diff (`diff.py`): `0:36BA-3747` (`$C50F`/`$C48F` copies), `0:3748` (`$C54F`), `29:56EA` and
  `22:5700` are unchanged in EN, so the game's own copies run. `22:5688` calls `7F00` (`VWF_Panel`).

### `$C54F` (unidentified item type)
`0:3748`: if `$C5DB` bit 6, the index is `[$C560]`, so `49:567D[i]` is copied to `$C54F` including the
`$00`. `$C54F` is the 40-byte item record copied by `0:24FF`. Name bytes 0-16 come first, then `$C560` =
byte 17 = unidentified class (insert.py: "writing over it made every item look like an Axe"). Limit 16
characters. The same limit applies to `29:56FF` (bank-41 record +2).

### Temple pay check `27:662C` (bug)
- JP `27:661B`: `hl = $D028 + 4*[$D006]` (payer's gold, `$D006` = selected member) and `de = $FFB0`, then 4
  unrolled `ld a,[hli]/ld [de],a`. Next, `call 0:0E62` (32-bit `$FFB0 -= $FFB4`; the fee was copied to
  `$FFB4` at `27:660A` from `$D024`). On borrow it prints rect `26:7673` "Not enough gold." Otherwise
  `27:69DA` writes `$FFB0-$FFB3` to `$C8D9 + $80*member` (party record +`$59`, gold). Screen rects:
  `26:765B` "Who will pay?", `26:7668` "Fee:", next to `26:7647` "Leave them at Samsara Temple.".
- EN: `cd 51 1c 04` + 7 zero bytes (`Stub_Fix`, n = 4). `fix_sites()` only skips copies with an `ld hl,$8000+`
  in the 8 bytes before the copy; `ld hl,$D028` is 13 bytes before it. `FixFind` misses (source page
  `$D0`), so the raw path prints the 4 RAM bytes as text at DE = `$FFB0`.
- Dynamic check (`work/re/overflow/pay.py`). Both ROMs: power-on, `emu.boot`, stopping breakpoint at
  `0:07C5`, then `$2000`=`$FF9E`=`$27`, `$D006`=0, `$D028`=`10 27 00 00` (10000), `$D024`=`E8 03 00 00`,
  `$FFB0`=`AA BB CC DD`, PC=`661B`, SP=`$CDC0`, `run_until 6637`:
  - JP: 20 instructions. `$FFB0..B3` = `10 27 00 00`.
  - EN: 1418 instructions. `$FFB0..B3` = `C3 BB CC DD`. The first byte is a VWF tile code and the gold
    never arrives.
  - So in the English build, paying a resurrection fee sets the payer's gold to `garbage - fee`, or refuses
    with "Not enough gold." This is the same class of bug as the earlier "buying adds gold".
- It is the only false positive. The other 10 `Stub_Fix` sites (`26:5671/56B3/56E8/5741/579E/58D7/6102`,
  `27:49FD`, `29:421D`, `2A:4A3F`) all read ROM tables (`hl` = `$402C-$759C`).

### NPC recruits `2D:68C9`
Called at `2D:6733` with the record index in `$FFB1`. `hl = $4000 + $80*a` reads bank 45 itself, and the
name is copied with its `$00` to `$FFC4`. `0:2CA7` compares it against the SRAM roster (`$A000`, 20 × `$80`).
`2D:68B9` copies the whole `$80` record to `$C48F`. The field is 8 bytes (record byte 8 is data, e.g. `06`).

## 4. Fix proposal (not applied)
- **Temple:** add `(39, 0x662C)` to `SKIP_FIX_SITES` (rom offset `39*0x4000 + 0x662C - 0x4000`), or better,
  have `fix_sites()` look back to the last `ld hl,nn` in the basic block instead of a fixed 8 bytes. Then
  rebuild and check that the EN bytes at `27:662C` equal the JP ones (`2a 12 13 2a 12 13 2a 12 13 7e 12`).
- **NPC names:** a `script/npcs.json` (bank 45, `$4000 + $80*i`, 8-byte field, in place like templates,
  assert <= 7) with a short form for Siegfried (e.g. "Siegfrd", or a glossary decision). The recruit
  messages already say "Siegfried", which is fine because messages are streamed.

### Proposed tests/test_limits.py checks
1. `test_unid_item_types_fit_c54f`: lists.json `0x567D <= table <= 0x56AD` -> `len(en) <= 16` (`$C560`
   follows; the bank-41 copy at `29:56FF` writes the same strings).
2. `test_monster_names_fit`: monsters.json `len(text.encode(en)) <= 12` (`$C50F`/`$D4B8`/`$DD36`; insert
   already asserts this, the test makes it visible).
3. `test_wnamebuf_31`: every rect row in the FixMap (same filter as `fixmap_entries`), fixtables, inline,
   notice lines, spells `en` and items `en` -> encoded length <= 31 (`wNameBuf` 32 bytes, uncapped copies;
   currently 31 is used by `2b:6d41`).
4. `test_spell_names_31`: spells.json `len(en) <= 31` (`wSpell` cap; truncation, not overflow).
5. `test_fix_sites_read_rom` (in test_coverage.py): for every `insert.fix_sites()` site, the nearest
   `ld hl,nn` (`21 lo hi`) within 16 bytes before the copy has `hi < $80`, or the site is in
   SKIP/EXTRA. This catches `27:662C`.
6. When NPC names are added: `len <= 7` (`$FFC4`, 8 bytes, `$FFCC` follows; record name field 8).

## 5. Open questions
- The temple bug was confirmed by running the copy directly, not by playing a resurrection: no state with a
  dead character. A playtest should check a payer's gold before and after paying.
- I did not check whether `$FFCC` is live at the time of the `$FFC4` copy (only that the game uses it). The
  7-character limit comes from the record field anyway.
- Visual (not RAM) overflows were out of scope: `29:62CC`/`29:6343` used to copy only 12 characters of an
  item/target name. In EN they are `Stub_PrintZ` without a cell cap, so a 16-character item name draws
  past a 12-cell field.
