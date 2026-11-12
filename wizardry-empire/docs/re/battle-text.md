# Battle text: where it lives and how it is printed (original ROM)

> Addresses refer to the Japanese **Rev 1** (the base since 2026-11-12). Written for v1.0 and converted with
> `tools/revmap.py`; a few marked "(v1.0)" did not map. `docs/re/rev1.md` lists what Rev 1 changed.

_From the tracer agent (2026-11-11). Scratch scripts/logs referenced below were in `work/re/battle-text/` (not committed). The "$F2 bank" bug described here is fixed: redirected English now jumps back to the original terminator._

## 1. Answer
All battle text goes through the normal typewriter (`0:1BAB`). The text bank is **49 ($31)**. Battle init sets
`$C1C1` once (`22:445C`, also `22:4DAD/4DD9`). After that the battle code in banks **$22 (34)**, $24 and
**$32 (50)** sets only `$C1BF/$C1C0`. The census missed these messages for two reasons. Battle lines are not
`$FF`-terminated messages: they are **`$FD ... $FC` segments** in one stream at `49:4585-4EC8` (plus
`49:51B7-51FB`, `49:541A-54EB`). They start with a newline. `$FC` saves the pointer and puts the typewriter
task to sleep. So no segment has `$FF` before it, and `census_msgs.guess_bank` picks the wrong banks.

Each line is built from fragments:
- `{F8 00 31 C48F}` = actor name and `{F8 00 31 C50F}` = target name. These are `$00`-terminated WRAM
  buffers. Note: the 2nd byte of `F8`/`F3` is an **SVBK value**, not a ROM bank.
- `{F8 00 31 C577}` = spell/action name and `{F8 00 31 C54F}` = item name.
- `{F3 31 C6E3}` = a string whose pointer is in `$C6E3` (monster attack verb, command word, etc.). It is read
  from ROM bank 49.
- Numbers: `{F8 10 04 D962}` (hits, WRAM4) and `{F8 20 04 D963}` (damage).

The command menu and the side panels use the same typewriter. The command menu is `22:76C4`, which calls
`0:2482` with each command ID and table `49:5607`. That table points into the `$00`-separated lists at
`49:40A1-40FD` (confirmed). The monster-group panel (top right) is different: it is **bitmap tiles**. `22:565C`
puts up to 4 group names into `$C50F`. Then `0:19B4` copies 8x8 font glyphs from ROM 1:`$4400` into WRAM1
`$D200` and DMAs them to VRAM1 `$8C00` (tiles `$C0-$E7`). After that, RAM rect blocks are blitted with `0:173C`.

**Bug in the current EN build (confirmed):** the `$F2` jump writes `$C1C1` and nothing in battle sets it back.
Any bank-49 battle prompt that is redirected to bank 65 makes every later line read bank-49 offsets from
bank 65. This was seen with `4F5A` (equip screen, below).

## 2. Evidence

### Getting there
- I used triage's original-ROM states: `work/triage/battle1/s/ejp.state` (command menu) and
  `work/triage/battle1/battle_start_jp.state`. I copied the second one to `work/re/battle-text/battle_start_jp.state`.
- Their inputs: triage `explore.py` with seed 7 from triage `maze_jp.state`. When I re-ran it, it did **not**
  reproduce the encounter (no battle in 80 steps), so I don't have an input list.
- My own maze state: `work/re/battle-text/maze_jp.state`. Route: boot, PARTY, `left*3,a,w60,a,w150,b,w60`.
- Gotcha: in the maze the message box is in the bank-3 `$D800` buffer, and codes `>= $80` are stored as
  `code & $7F`. Search the buffer with masked bytes.

### Tracing method
- Script: `work/re/battle-text/tw.py`. It sets watchpoints on writes to `$C1BF-$C1C1` and `$C1D3/4`, and logs
  backtraces while replaying presses.
- Run on `ejp.state` with `a,w30,a,w30,a,w60,...`. Log: `work/re/battle-text/t1/log.txt`.
- Rule: a message start is a write to `$C1BF/$C1C0` from bank $22/$32 code. Writes from `1E71/1E39` are the
  typewriter's own `$FD`/`$FC` handlers.

| Pointer | Written at | Text |
|---|---|---|
| `49:45E2` | `32:43E9` (via `22:70AF (v1.0)`) | `\n{actor}は{FA}{target}を{FA}{F3 C6E3}{FC}` (attack verb) |
| `49:468B` | `32:462D` | `\nしかし ダメージをあたえられなかった{FC}` |
| `49:4871` | `22:72C9` | `\n{target}は{FA}たすけをよんだ...{FC}` |
| `49:4884` | — | Reached by fall-through after that line's `$FC` |
| `49:4896` | `22:7328` | `\nしかし たすけはこなかった{FC}` |
| `49:4EC9` | `22:5EED` | `たたかう\nまえにもどる{FF}` (sub-menu) |
| `49:4ED5` | `22:4D4F` | `どのモンスターと たたかいますか?{FF}` |
| `49:41B5`/`41C9` | `32:429A`/`32:428E` | Party panel rows (`$C1D3=$D822`, set at `32:41F5`) |
| `49:4197`, `419D`, `41E7`, `4191` | `22:5966`, `22:5A3D`, `22:5A7A`, `22:5AC5` | Active-character panel |

- `$C1C1` stayed `$31` throughout. `$C1C1` is **0** in maze/town states, so battle init sets it. Battle init
  is `22:4434-446E`:
  - It sets typewriter parameters and `$C1C1=$31`.
  - Then `ld a,2 / ld b,$22 / ld de,$20DA / call $06EF` creates **task 2**. Task 2 runs the typewriter at
    `0:20F3`, which loops on `1B92`.
- Breakpoints on `22:4434`/`22:4D9E` never fired during a full round (`pcs.py`). So nothing re-sets the bank
  between messages.
- Full segment decode: `work/re/battle-text/bank49_4400.txt` (made by `dec49.py`).

### Routines
| Routine | In | What it does |
|---|---|---|
| `0:2494 (v1.0)` | `$C1BF/C0` = segment | Calls `0:36BA`: removes `$FD` from the target name at `$C50F`. If `$C54D` bit 7 is set (unidentified), it substitutes the name from `49:56FD[$C51C]`. Then `0:24B0`: `ld a,2 / call 072B` wakes task 2. It waits until task 2 sleeps (`$C01A` bit 6, set by `$FC` → `1E35` → `0721`), then waits for a key (`$FF8B`). |
| `0:24A2` | `$FFD6` | Chooses `36A1` (actor `$C48F`, same normalisation) or `365A` |
| `0:2484 (v1.0)` | — | `36E8`: if unidentified, item name from `49:566B[$C560]` → `$C54F` |
| `0:2482` | A = index, HL = table (bank 49) | `0:0EDF` (b=$31) reads the pointer and stores it in `$C6E3/4`. Sets `$C1BF/C0=$41E2` (`{F3 31 C6E3}{FF}`). Calls `1B92` once, which prints the whole string at the current `$C1C5/$C1C6`. |
| `0:236A`/`0:237E` | — | Combatant `$80`-byte records at WRAM `$D080+$80n` ↔ `$C48F` |
| `0:2394` | A = monster ID | Copies 64 bytes from 57:`$4820+$40*id` to `$C50F` (name first, 12 chars + `$00`) |

### Command menu: `22:76C4`
- `B = [$C587]` = command count; IDs are at `$C588...`.
- For each ID: `hl=$5607`, call `2469`, restore the column, then `$C1C6++`.
- Table `49:5607`:
  - IDs 0-17 → `40A1 たたかう`, `40A6 かくれる`, `40AB きしゅう`, `40B0 みをまもる`, `40B6 まほう`,
    `40BA けんじゅつ`, `40C0 にんじゅつ`, `40C6 しょうかん`, `40CC たいきょ`, `40D1 のろいをとく`,
    `40D8 アイテム`, `40DD にげる`, `40E1 ノーマル`, `40E6 ヒットねらい`, `40ED ダメージねらい`,
    `40F5 つかう`, `40F9 そうび`, `40FD なげる`.
  - IDs 18-35 → 4-char abbreviations at `49:4F9B-4FF0` (5-byte entries).
- In the trace, `2469` was called with HL `5620/5622/5624` (`76E6`) and the menu showed
  たたかう/かくれる/みをまもる/アイテム/にげる.

### Other shared pointer tables (strings `$00`-terminated in bank 49)
One table area runs from about `49:55BF` to `5725`:

| Table | Contents | Used by |
|---|---|---|
| `55D1` / `55D7` | Alignment / class | `22:5A65` / `22:5A52` via 2469 |
| `564F` | Trap names | `25:4951` |
| `566B` | Unidentified item types | `0:3757` |
| `56AF` | 42 attack verbs at `49:503D-51C2` (Rev 1; v1.0 `569D`/`502B`) | `32:43C4`, `32:4850` (party, templates `32:58D6`), `32:4D64`, `32:5240` (monster, `32:59CE`), `22:7119` (breath, fixed `45D3`); store to `$C6E3` → `{F3 31 C6E3}`. Target/no-target per verb and dead entries: `docs/re/verbs.md` |
| `56F1` | Equip slots | — |
| `56FD` | Unidentified monster names (`54EC あくま`...) | — |

Also: tables in bank 50 (`32:57DB (v1.0)`, `32:57FF (v1.0)`) point at bank-49 status words (`49:4FFA...`) for the party panel.

### Monster-group panel
- `22:565C` loops over the `$D928` groups. Group records are at `$D4B8 + $40n`:
  - name: 13 bytes
  - unidentified flag: `+$3E` bit 7
  - class: `+$0D` (for `22:5706 (v1.0)` → `49:56FD`)
- Names are copied as 13-byte entries into `$C50F`. Then `call $199B` at `22:5688`.
- `0:19B4`:
  - Sets SVBK=1, maps ROM 1, and fills `$D200` with the blank glyph (`1:$43F0/1`).
  - For each name, it copies a 16-byte font tile from `1:$4400+code*16`. `$FD` moves to row 2 (`+$A0` = 10 tiles).
  - Queues `$D200` → VRAM1 `$8C00` (`$40` blocks) through `0:1443`.
- Panel rects are 10x2 tiles + attributes, built in RAM at `$C632/$C65C/$C686/$C6B0`. The tiles are
  `$C0+`, `$CF`=(, `$D0`=), and digits `$F4+n`. They are blitted by `22:57A3`/`22:58B8` (`0:173C`) to bank-3
  `$D02A/$D06A/$D0AA/$D0EA`.
- Confirmed by a write watch on bank-3 `$D021-$D034` (`wbuf.py`, `ejp.state`): writes from `0:000A`
  (`rst $08`) under `1746 ← 58B2/579D`.
- In the EN build this panel still shows kana (`きみょうなもの`) because it copies from the ROM font, not VRAM.

### EN-build confirmation of the `$C1C1` bug
- Run: `tw.py` on `build/wizardry_empire_en.gbc` from `work/re/battle-text/t_en/00.state` (command menu),
  inputs `down*4,a,...`. Log and sheet: `work/re/battle-text/t_en2/`.
- What happens:
  1. `49:4F5A` (equip help) is now `F2 41 A4 7F`.
  2. At `1C2C`, `$C1C1` becomes `$41`.
  3. Then `22:526B` sets `4425` and `22:53F6` sets `441F`, and so on. These are read from **bank 65**, so the
     screen shows fragments of unrelated English ("party.", "form a party", "points remain").
- The same will happen after `4ED5`/`4EE7`/... ("Fight which monster?", multi-group battles) and `4F7E`
  ("Can't escape!"). Every later attack line will then be garbage.
- In the EN build, bank 49 is unchanged except for 186 bytes at the redirect sites. The free space
  `49:5726-7FFF` (about **10.4 KB**, `$00`-filled) is unused.

## 3. Hook proposal
**A. Battle lines and prompts (typewriter): no new code, data only.**
- Char output already goes through `TW_Char` (`$1C11`).
- Rule: every bank-49 message is redirected with `$F2` to **bank 49 itself** (`F2 31 lo hi`) and placed in
  `49:5726-7FFF`. Then `$C1C1` stays `$31`.
- This also fixes the confirmed bug: move the 47 bank-49 entries now in bank 65 to bank 49 too, at least the
  battle/equip prompts `4ED5-4F7E`.
- Each segment is at least 13 bytes, so the 4-byte `F2` always fits. Overwrite the leading `$FD`. The English
  text must start with `\n` itself.
- End each English segment with `{FC}{F2 31 <next original segment>}` (4 extra bytes). This keeps the
  fall-through cases working (e.g. `4871` → `4884`).
- `{F3 ..}` and `{F8 ..}` inserts can be reordered freely in English, e.g.
  `{F8 00 31 C48F} {F3 31 C6E3} {F8 00 31 C50F}!`.
- Script format: `messages.json` entries with `"end": "FC"` (kind `segment`). `census_msgs.py` needs a
  segment mode: start = byte after `$FC`/`$FF`, end = `$FC`, `$FD` as the first byte, and `F8`'s 2nd byte
  treated as SVBK.
- Size: Japanese is about 3.5 KB (`4585-4EC8`, `51B7-51FB`, `541A-54EB`). The English plus lists may come close
  to the 10.4 KB, so measure it.
- Fallback if bank 49 fills up: patch `0:24B0` (`3E 02 CD 2B 07`, 5 bytes) to a stub that does
  `ld a,$31 / ld [$C1C1],a` first, then runs the original two instructions. This alone is not enough: these
  sites set a pointer and then call `1B92` directly, and all of them would need the same fix:
  - `0:2482`
  - `32:4223`
  - `22:5EF2`
  - `22:4D4F`
  - `22:526B`
  - `22:53F6`
  - `22:52DC`
  - more

**B. List strings (commands, verbs, classes, unidentified names): repoint, don't hook.**
- They are read with ROM bank 49 mapped (the table read hard-codes `$31` in `0:0EDF`, `0:2482`, `0:36D9`;
  the `F3` string is read under `$C1C1`). So the English must stay in bank 49.
- Rewrite the 2-byte entries of `49:55BF-5725` (and `32:57DB (v1.0)/57FF`) to point at English `$00`-terminated
  strings in bank-49 free space.
- Format: one record per entry, e.g. `{"table": "49:5607", "index": n, "jp", "en", "max_px"}`.
- Width limits:
  - command box: 7 cells = 56 px, as `TW` reports
  - attack verbs: mid-sentence, with word-wrap `{FA}` around them
- `0:36BA`/`0:3701` remove `$FD` from names, so English names can keep breaks.

**C. Monster-group panel (bitmap tiles).**
- Replace the 3-byte `call $199B` at `22:5688` with a far call to a VWF routine.
- In: HL=`$C50F`, 4 × 13-byte names (`$FD` = row 2). The count is not needed: empty names are `$00`.
- The routine renders each name proportionally into the 10+10-tile layout in WRAM1 `$D200`, using the same
  ink/paper as the font. It then does the same `0:1443` queue: src `$D200` bank 1 → VRAM1 `$8C00`, `$40`
  blocks, the same as `1A02-1A1D`.
- It must restore SVBK/ROM bank like `0:19B4` (pushes `$FF9D`/`$FF9E`). It is free to use A/BC/DE/HL; the
  caller does `call 07C5` right after.
- Tiles `$C0-$E7` in VRAM1 `$8800` space are outside the VWF pool, so there is no allocation conflict.
- Names come from the bank-57 records (`items/monsters` 12-char fields), so no new script is needed. Up to
  about 80 px fits on row 1, and longer names can use row 2.

## 4. Open questions
- Exact entry IDs for battle init (`22:4434` vs `22:4D9E`): which one runs for which encounter type.
  Neither fired during a round.
- Who uses the abbreviated command IDs 18-35 (`49:4F9B`)? Probably the party-panel "planned action". Not traced.
- Group records at `$D4B8`: which WRAM bank, and the copy from bank 57. Not traced; only seen in disassembly.
- Fall-through segments other than `4871`→`4884`: I saw only one implicit continuation.
- Not checked: whether `$FC` segments are printed in other screens (chests `5277`, traps `541A`, camp).
  They use the same bank 49 and the same rule should apply.
- I could not reproduce triage's encounter route, so there is no input list for `battle_start_jp.state`.
