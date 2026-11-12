# Rev 1 vs v1.0: what changed that matters for the translation (tracer, 2026-11-12)

ROMs: `rom/wizardry_empire_j.gbc` = Rev 1 (SHA-1 f5f4e8be...), `rom/wizardry_empire_j_v10.gbc` = v1.0 (041c1251...).
Scratch scripts and outputs: `work/re/rev1/` (gaps.py, census_cmp.py, sites.py, sitefwd.py, refsets.py, ramcount.py,
both.sh; outputs gaps_all.txt, census_cmp.txt, sites.txt, ramdiff.json).

## 1. Answer

Rev 1 is a bug-fix release. Almost every changed byte is a relocated pointer: code grew or shrank in banks 0, 20,
22, 24, 26, 27, 2A, 2B, 2D, 2E, 31 and 32, and everything after it moved. Not counting pointer shifts, the text
changes are:

- the three bank-45 messages already handled by hand;
- one new message, **31:4592 `\nいてっ` ("Ouch!")**, printed when you walk into a wall. **Not in script.**
- two new messages made only of control codes, 31:41DC and 31:41E4 (no Japanese text);
- one new 3-entry pointer table, **32:583F-5844 -> 31:401F/4022/4028 (ぜん/ちゅうりつ/あく)**, used by a new
  alignment column in the friendly-encounter party panel. `tools/insert.py` repoints only 28 entries of the
  32:5807 table, so these 3 are missed and will show kana.

All other script entries are byte-identical at their Rev 1 addresses.

The WRAM/HRAM layout the patch uses has not changed. Every listed variable keeps its address and meaning. A few
gained new readers or writers in new code (bug fixes, details in section 3). Bank 0 code from $0DE3 up moved by
+$19, and by more past $26FD: 0FD0->0FE9, 1B92->1BAB, 1703->171C and so on.

## 2. Text: every changed region in the text banks, classified

Method: for each bank, the unmatched regions between revmap blocks (MIN 8) were checked byte by byte. A region
counts as "ptr" when every changed byte lies in a 16-bit word, or a split `ld a,lo ... ld a,hi` pair (gap 4 or 5),
whose v1.0 value moves by the shift of the matching block where it points, or when it is a `jr` operand
(`work/re/rev1/gaps.py`). Results (`gaps_all.txt`): 2D 319 ptr / 5 len / 1 other, 2E 162/7/1, 31 1/3/0,
32 219/6/4, 2B 285/9/1, 26 299/13/4, 27 368/13/10, 2A 371/4/3, 2C 83/3/6. I read every non-ptr region by hand
(disassembly from both ROMs, `both.sh`).

### Text banks 45/46/49 (typewriter)
| Rev 1 region | v1.0 | Content | Class |
|---|---|---|---|
| 2D:4400-4464 | 2D:4400 | event message pointer table (all -$0A) | ptr, not text |
| 2D:4490 (len 24) / 2D:44A8 (len 39) | 2D:4490 (31) + 2D:44AF (41) | v1.0 "しらべてみたが とくにかわった ことは みつからなかった" is gone. 4490 = `\nじめんに ふしぎなもようが\n\nえがかれている` (the site 2D:6657 that used to print "searched, nothing"), 44A8 = "magic circle ... だれが なかにはいりますか?" (site 2D:652B) | text covered (both entries in messages.json; the jp fields match the Rev 1 bytes) |
| 2D:4D27 (1 byte deleted) | 2D:4D30 `』` | message 2D:4CF3: stray `』` after "ほかにもいよう" removed | text covered (jp matches) |
| 2D:783E, 7FFB | | code (`ld a,1 / ld [$C1BD],a`), end padding | not text |
| 2E:4D13-4E34 | | bank-46 code + jump table | ptr, not text |
| 2E:4F03, 509F, 53C3, 5435, 5480-54B5, 54FE | | code: SRAM signature check/write (see 3) | not text |
| 31:41DC-41E8 (13 bytes inserted) | | two new control-only messages: 41DC `{F8 00 31 C48F}{F4 08 FF}` (name, then column 8) and 41E4 `{F3 31 C6E3}` (string through the pointer at $C6E3). Copies of the existing 41C9/41D1 pair | text, no Japanese: nothing to translate; handled by the existing $F3/$F8 engine paths |
| **31:4591-4595 (5 bytes inserted)** | (none) | **new message 31:4592 = `FD 0C 1D 0A FF` = `\nいてっ`** | **text NOT covered** |
| 31:563D-57xx | 31:562B | message pointer table (+$12) | ptr, not text |
| 31:7FEE end padding | | bank-49 free space now starts at $5737 (insert.py already uses $5737) | not text |

Suggested script entry (messages.json, next to the other bank-49 system messages):
```
{"bank": 49, "addr": "0x4592", "jp": "\nいてっ", "en": "\nOuch!"}
```
Context: 20:46BC (maze move, wall bump: 20:45EA `and 3 / jp z,$470C` = open, else `jp z,$46BC`) now runs
`call 0:3C78` (SE 5, skipped when $CB99 bit 6 is set), then `ld bc,$0307 / call $278D`, prints 31:4592 with
`call $1BAB`, and waits for A/B/Start/Select (`$FF8D and $F3`). In v1.0 a wall bump only played the sound.

### Bank 50 (32) and bank 43 (2B) rect/list text
| Region | Content | Class |
|---|---|---|
| **32:5807 table, now 31 entries (v1.0 32:57DB, 28)** | entries 0-27 unchanged, all +$12; **new entries 28-30 at 32:583F/5841/5843 -> 31:401F ぜん, 31:4022 ちゅうりつ, 31:4028 あく** | **text NOT covered**: the strings are in lists.json (Good/Neutral/Evil), but `insert_lists()` only repoints `range(28)` of 32:5807. These 3 pointers stay on the Japanese strings. Fix: `range(31)` (or repoint 583F-5844 on their own) |
| 32:4075, 4244, 42B1 (new code) | friendly encounter (31:556D "ゆうこうてきな ... たたかう/たちさる"): `ld a,$FF / ld [$D92D],a`. The party panel loop at 32:4237 then takes 32:42B3: `[$C6E3/4] = word at 32:583F + 2*[$C499]` (alignment), prints 31:41DC (name, column 8) and continues with 31:41E4 = the alignment word | new feature; check on screen that "Neutral" fits from column 8 (right margin $C1C3 = $0C) |
| 32:46DA, 47DB, 4A5F, 5220 | code, call/jump retargets | ptr |
| 2B:55D5-563D | transfer screen: rect sites moved/added for 2B:7708 てんそうが しゅうりょうしました, 2B:7663 そのなまえは すでにつかわれています, 2B:76F7 キャラクタが かえってきました | text covered (all 3 in rects.json) |
| 2B:4026, 40B8, 422C, 4251, 5341 | code (roster limit 20, SRAM signature) | not text |
| 2B other | rect pointers (+$1C/+$1F) | ptr |

### Other banks with text (26, 27, 2A, 2C, 22, 24, 20, 25)
Every non-ptr region is code (disassembled). The only ones that touch text are the message selection changes
below, and every message they now select is already in messages.json:
- 24:61C0/62B1/65A6 (battle): "X slashed with Y" now uses 31:4B05 (`{F8 .. C48F}は ... できりかかった!`) instead
  of 31:4BD3 (`C50F` variant); 24:65C1 uses 31:4B2F instead of 4BFD. Both variants exist in v1.0 and both are
  in the script.
- 0:2F6A, 0:3063, 24:4758 ... 24:6063, 2E:51AD/524C: `call 0:236A` (load the target name) now runs before
  31:4909 "`{C48F}には こうかがなかった!`" (covered). In v1.0 the name was not loaded first (wrong name).
- 20:46D3: the new "Ouch" message above.

A site-by-site comparison (`sitefwd.py`: every v1.0 `ld [$C1BF]/[$C1C0]` site, forward-mapped) found no other
message reference that now points somewhere else. The reference-set diff (`refsets.py`) shows only two Rev 1
message addresses that no v1.0 reference maps to: 2D:44A8 (handled) and 31:4592 (new).

### Non-text-bank changes worth knowing
- 01:6CD4 (9x8 rect, debug sound-test menu, ASCII): rows "NONE" x5 -> "--------- / MASK / VERSION / 1.1 /
  ---------". Debug only, ASCII; nothing to translate.
- 28:5FB1: item 202 (てんいのゆびわ / Ring of Warping), record byte +33 $C9 -> $49 (flag bit 7 cleared). Name
  unchanged.
- 37:41E0-4508: map/attribute data (rows of $01 added). Not text.
- Header: $014C version $00 -> $01. v1.0 code read the header checksum byte `[$014D]` (= 5) as a game constant
  (0:3C8F/3D0B/3DE5); Rev 1 uses `ld a,5`. So the patch can rewrite the header checksum without side effects.

### Aside (not Rev 1-specific)
2B:788B (Rev 1; v1.0 2B:786C), a 4x1 rect with attributes, `にいます` (the "... is on floor N" location
column of the find-character list, drawn by 2E:57E3 after a number). It is not in rects.json, and HEAD did not
have it either. Check whether a hook covers it.

## 3. RAM (WRAM/HRAM) used by the patch and tools

Two independent checks:
1. Gap analysis: a changed RAM operand in code of the same length cannot be explained as a ROM pointer
   ($C000+ is excluded), so it would show up as "other". The few "other" regions contain no RAM-operand change
   except inside new code.
2. Operand census (`ramcount.py`): counts of `fa/ea/21/11/01/31/08 nn` and `e0/f0 n` operands per address in both
   ROMs, and for every listed address that differs, the Rev 1 sites with no v1.0 image (and the reverse).

| Address(es) | Status |
|---|---|
| $C00A frame counter | same (no difference) |
| $C1BF-$C1DE typewriter | same layout; the typewriter 0:1B92 -> 0:1BAB is byte-identical up to pointer shifts (+$19). The 2 extra $C1BF/$C1C0 refs = new message sites (20:46D5 Ouch, 32:42C9 alignment) |
| $C49B-$C4F3 | same layout. New uses: $C49C/$C49D (24:52A2: after a battle, if the level changed, recompute the exp for the next level via 27:5BEA into $C4EC-$C4EF); $C4A4-$C4AF (26:6200: record load now sets the 6 pairs to $FF/$00); $C4A0 loop 2A:59DC now 8 pairs instead of 16 (v1.0 over-read up to $C4BF); $C4E2 (24:6129 `+$50 -> $DD57`). Bug fixes; no address moved |
| $C50F, $C51C, $C527-$C538 | same |
| $C54F-$C575 | same |
| $C592-$C5C6 museum flags | same |
| $C632 | same; it is still read by 0:2626 (record decode, Rev 1 0:263F). New in Rev 1: 0:2716 strips $FD from the name at $C800 and clears bit 7 of $C83E after the decode |
| $C6E3/$C6E4 | same meaning (pointer for `{F3 31 C6E3}`); 2 new writers (32:42C0/42C4 alignment, see above) |
| $C6E5 | same |
| $C880+ roster records ($80 each) | same; new count checks `cp $14`/`cp $15` (20 characters) in 26:6443, 26:6B42, 26:49E2, 2B:40B8, 2B:422C |
| $CB85 party count | same (one new reader 26:6464/2B:425B in the roster-limit code) |
| $CBF5 | same |
| $CD80 private stack ($CD70-$CD80) | no new game use (the differing raw counts at $CD4x-$CD7x are `call $xxCD` operand bytes, checked) |
| HRAM $FF8D-$FFC1 | same layout. The number printer 0:0FD0 -> 0:0FE9 is identical (value $FFA8-$FFAB, C -> $FFAC, B -> $FFAD, DE -> $FFAE/F, digits $FFB8-$FFC1). New: 0:0DFA (24x16 multiply, called only from 27:5C1E exp table) uses $FFAC-$FFAF as scratch, and 27:5C21 writes $FFB0-$FFB3; the 16x16 multiply 0:0DE2 no longer uses $FFA8-$FFAA. None of these run inside a number print. $FF8D: one new reader (20:46E8 key wait) |

Bank 0 shifts for the port: $0000-$0DE2 same; $0E30... +$1B; $0FD0-$26FC +$19; $26FD-$27E2 +$2E;
$27E6.. +$36, then more (see revmap). Bank 0 free space: v1.0 had zeros at $3F69-$3FD9 and $3FF0-$3FFF. Rev 1 has
code up to $3FEF, so only **$3FF0-$3FFF (16 bytes)** is free (asm uses $3FF0 for Stub_Measure, still fits).
Bank end-of-data (free from): 20:7305, 22:7831, 24:7E53, 26:77D1, 27:7930, 2A:7838, 2B:7895, 2C:6A63, 2D:7C89,
2E:63B7, 31:5737, 32:5C63. The asm `org NN,$7F00` areas in 22/2A/2B are still free.

## 4. Summary of the changed code (cheap view)
- **Maze (20)**: wall bump prints "いてっ" and waits for a key (new). Status masks fixed: `and $C0` -> `and $3F`
  at 20:5D85/5E6F (severity is the low 6 bits). 20:443B `and $41` -> `and $01`. 20:4793 grew (+44 bytes,
  position/map lookup via $CB80-$CB82, $DD28).
- **Battle (24, 0, 2E)**: load the right character before status checks and messages (`call 0:3A67` / `0:236A`
  moved ahead of the status read at 0:2FB6, 24:4723, 24:5279, 24:5F8C ...); attacker/target name variables
  corrected in hit messages; level change after battle recomputes the next-level exp (24:5279 -> 27:5BEA).
- **Exp table (27:5BEA)**: levels above 17 use the new 24-bit multiply 0:0DFA (overflow fix).
- **Roster (26, 2B)**: cap at 20 characters in create/transfer/list code.
- **Char record load (26:6200)**: initialises $C4A4-$C4AF. **2A:59DC**: scans 8 pairs at $C4A0, not 16.
- **Item flags (26:5163)**: loop over 8 bytes uses `cp $FF` and also clears bit 4.
- **Save (2B:4026, 2E:5456/5480)**: SRAM gets a signature "Wizardry"/"EMPIRE1" at $AFF8/$BFF8 (2E:53E6/53EE),
  written on SRAM init and checked by 2E:5480. A `.sav` from v1.0 has no signature; what Rev 1 does on a
  mismatch was not traced.
- **Record decode (0:2716)**: strips $FD from the decoded name at $C800.
- **Friendly encounter (32)**: party panel shows each member's alignment (new).
- **Event text (2D)**: one event no longer says "searched, nothing" but shows the strange-pattern text; magic
  circle wording; stray quote.
- **Data**: item 202 flag byte, bank-55 map data, header version 1.

## 5. Open questions
- What 2B:4026/2E:5480 do on a signature mismatch (wipe SRAM?). This matters for any v1.0 `.sav` used with Rev 1.
  The tool states are savestates, not affected.
- The alignment column and "Ouch!" were found statically; I did not see them on screen. To reproduce: walk into
  a wall in the maze; a friendly encounter shows the alignment panel.
- 2B:788B `にいます` coverage (aside above).
