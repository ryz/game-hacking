# Typewriter message coverage ($C1BF/$C1C0, bank $C1C1) - JP Rev 1 census

> Status: the five missing messages were added in 5ab9d44; the appendix shows the state at 13636d2.

Base: original `rom/wizardry_empire_j.gbc` (SHA-1 f5f4e8be..., Rev 1). EN build 13636d2 copied to
`work/re/msgcov/wizardry_empire_en.gbc` (+ .sym) and used only to check that the missing texts are still raw
Japanese there. Scripts in `work/re/msgcov/` (sites.py, cover.py, full.py, fcchain.py, orphans.py, table.py,
test_msg_coverage_proposal.py). All static; no emulator run.

## 1. Answer
Every one of the 585 `ld [$c1bf],a` in the ROM is classified (566 immediate pairs, 14 pointer-table reads over
7 tables, 2 HRAM `$CE/$CF` reads, 3 typewriter-internal saves). There are no other writers: no `ld hl/de/bc,$c1bf`,
no block copy into $C1A0-$C1C1. $C1C1 gets only $2D (100 sites), $31 (13, among them the window-open
routines 0:278D and 01:6400) and $2E (once, 2A:4ABE before the 2A:76D0 table). Together with $FC continuations
these give **446 roots / 461 segments**. 432 are messages.json starts. **Five messages with Japanese are still
missing** (all bank 49, all still raw JP in the EN build 13636d2):

| bank:addr | JP | reached by | note |
|---|---|---|---|
| 49:43B9 | しきべつ | code 20:495B (maze status line, `$CB84` bit 6) | the "identify" indicator next to 49:43B5 あかり (Lit) and 49:43BE ほご (AC), which are in the script. 4 chars + FF: room for a $F2 redirect (exactly 4 bytes) |
| 49:4432 | {F3 31 C6E3}を えらんでください | code 22:5266 | "Choose {slot}": C6E3 = 49:5703[$C6E9] (equipment slot names, already in lists.json) |
| 49:451F | ␣␣どこへ テレポートしますか?//␣␣␣␣ちか {F8 20 31 C6E3}かいの/ ここから きたへ␣␣{F8 10 31 C6E5}/␣␣␣␣ひがしへ␣␣{F8 10 31 C6E7}//␣␣␣␣いどうした ちてん | code 23:4759 | teleport coordinate prompt (Malor), same screen family as 49:44CE (party location, now in the script) |
| 49:4583 | /もとのちてんに もどされた | code 20:43F6 (after `call $278D`; when `$CB84` bit 0 is set) | "you were sent back to where you started". Byte before is $00 (end of the direction list 49:4575-4582), which is why `$FF`-boundary searches skip it |
| 49:55A4 | モンスターは/␣␣とつぜん おそいかかってきた | code 22:4617 (battle start, `$C001` bit 2) and the `$FC` continuation of 49:5594 | 49:5594 (alignment change) is in the script but ends in $FC; the EN build `$F2`-jumps back to that $FC and the typewriter then prints 55A4 in Japanese. One entry at 49:55A4 fixes both paths |

Not missing (no Japanese in the segment, nothing to translate): 49:4191, 4197, 419D, 41B5, 41C9, 41DC, 41E9, 41EF,
41F4 (pure {F8}/{F3} inserts), 49:426B (`{F8 name}{F4 0A FF}L{F8 level}`, ASCII "L"; translate only if "L"
should become "Lv"), 49:430A ("."), 49:442C ({F8 00 31 C54F}), 49:4F98 (32:4219, only when `[$D000]`!=0:
number + $F0/$F1 glyphs, looks like a debug read-out). 49:45AA (22:4452, 22:4DD0, 25:49D6, 2C:4CCC) is a
typewriter **init default** (the routines set $C1BF/C1/C3/C4/C7 and never call the typewriter) - it points
19 bytes into 49:4597 at a bare $FC; harmless.

Debug / test texts (keep separate, intentionally untranslated):
- 45:624A (2D:7C75) and 45:62BB (2C:4C3E): debug-mode help (as known).
- 49:4A09 `/DEBUG:{F8 spell}{FC}` (24:7DBF, no caller of 24:7DB9 found = probably dead; ASCII only).
- 49:4C9C, 4CB3, 4CCA, 4CE3, 4CFC (`…のACが さがった!`, `T→D D→U`, `MAGIC OK!`, each with the same `$F0..$F1`
  tail): no pointer anywhere; only reachable if a caller of 49:4C87 let the typewriter run past its $FC, and every
  4C87 site (24:61AB...) waits (`call $24AD`) and sets the next pointer. Unreferenced test strings.
- 2C:4860.. from the dispatch is not a typewriter message (no $C1BF pointer goes to bank 44; $C1C1 is never 44).

Every other FF/FC segment with kana in 45/46/49 is a script start or reached (orphans.py found only code/graphics
noise in 45:64A9-786E and 46:4CED-4D00), so the list above is complete for pointers the static census can see.

## 2. Evidence

### 2.1 Writers of $C1BF/$C1C0 (585)
| class | sites | value origin |
|---|---|---|
| immediate pair `ld a,lo / ld [$c1bf],a / ld a,hi / ld [$c1c0],a` | 566 | in the code |
| typewriter internal | 0:1E4F ($FC pause), 0:1E87 ($FD newline), 0:1EFD ($FB wait) | save of the running pointer HL |
| table, word, `ld a,[hli] / ld [$c1bf],a / ld a,[hl] / ld [$c1c0],a` | 24:51A8, 51BE, 51D4 | 24:50DE[$FFDD/$DE/$DF] (7 words, random 0..6 by 0:0DC0), bank 49 |
| table, word | 2A:4AB2 | 2A:76D0[A] - 110 words 44DA..4CC8 (next word $010D), bank 46 (`ld a,$2e` at 2A:4ABE, the only $2E store) |
| table, 8-byte records of 4 words | 2D:6783, 679F, 67BB, 6858 | 2D:66C5 + [$FFB1]*8, 8 records 66C5-6704 (code follows), bank 45 |
| table, word | 2D:7724 | 2D:763B[A], 5 words 5EC0..5F06 (then $0101 / code), bank 45 |
| table, 3-byte records `[n][lo][hi]` | 2D:7A13 | 2D:79C8 + 3*(A-$0F [-$0C]), 12 records (then code 21 B0 FF), bank 45 |
| table, word | 32:43E6, 32:4872 / 32:4D89, 32:5265 | battle verb templates 32:58D6 / 32:59CE (4 words each; docs/re/verbs.md) |
| HRAM | 24:7908, 24:7986 (`ldh a,[$ce] / ld [$c1bf],a / ldh a,[$cf] / ld [$c1c0],a`) | 19 sites in bank 24 `ld a,lo / ldh [$ce],a / ld a,hi / ldh [$cf],a` (49:46D9, 46E9, 46F9, 4707, 4715, 4723, 4731, 4741). The other `ldh [$ce]` pairs (2A:402B-4195) are menu cursor data, unrelated |

`$C1C0` stores: exactly the 585 partners of the above. Data hits for `21 C0 C1` (0D:59EE, 1C:51B6), `31 C0 C1`
(0C:40C8), `01/11 C1 C1` (1F, 26, 2C) are graphics/data, not code.

### 2.2 Text bank ($C1C1)
`0:278D` (window open) sets $C1C1=$31 at 0:27D3; 01:6400.. sets $31 at 01:6427. Event code then stores $2D
(`ld a,$2d / ld hl,$c1c1 / ld [hl],a`, 100 sites, mostly right after `call $278D`). Some routines set it
after the pointer pair (22:445C) - census_msgs only looked 64 bytes back. Rule used: a $C1C1 store up to 16 bytes
after the pair, else the nearest $C1C1 store or `call $278D` up to $180 bytes back, else $31; cross-checked
with "byte before the pointer is $FF/$FC" in 45/46/49 (533 unique, 40 ambiguous 46/49 or 45/49 - all resolve
to a script entry in the static bank; no site's pointer is in the script only under a different bank).

### 2.3 $FC
$FC (0:1E4E) saves HL to $C1BF, wakes the waiting task (`0:0721` sets bit 6 of task [$C00F]), yields one
frame and goes on at 0:1BD4, reloading $C1BF. Battle code sets the next pointer during that frame
(`call $24AD` then the next pair), so its templates do not chain; a caller that only waits (32:4181:
`call $24B0`) lets the typewriter print the next segment. insert_msgs() ends English with `$F2` back to the
original $FC, so any continuation that is not its own entry prints Japanese. Of the script entries ending in $FC
only 49:5594 -> 55A4 is a real gap (others: 49:49FA -> 4A09 debug, 49:4C87 -> 4C9C test strings, 49:51EB -> 520E
and 49:54E9 -> 54FE `$00` lists covered by chests.json / lists.json).

## 3. Why tests/test_coverage.py did not catch them
1. It has no message test at all: its two tests cover unrolled text copies (`2a 12 13`) and duplicated
   fixtables. Nothing compares message pointers with messages.json.
2. The script itself was seeded from tools/census_msgs.py, which (a) only matches the immediate pair;
   (b) takes the bank from a $C1C1 store at most 64 bytes BEFORE the pair, else guesses the bank by kana
   plausibility over banks 1-63 - it does not know that `call $278D` sets bank 49, nor stores after the pair.
   Result: only 17 of its 278 (bank, addr) entries get bank 49 although ~440 of the 566 pair sites point into bank 49; 49:422B came out as bank 3, 49:4314 and 44CE as
   bank 1, 49:41FA as bank 19, 49:4432 as bank 4, 49:451F/55A4 as bank 45, 49:4583 as bank 46 - then dropped as
   junk; (c) ignores tables, the HRAM path and $FC continuations.

## 4. Proposed test (scratch copy: work/re/msgcov/test_msg_coverage_proposal.py, runs as is)
`test_every_message_pointer_is_in_script()`: collect roots (immediate pairs with the bank rule of 2.2, bank-24
HRAM pairs, the 7 tables with their walked counts), require every non-immediate `ld [$c1bf],a` to be in a
19-site allowlist (so a new indirect site fails), follow `$FC` from every root and from every script entry
ending in $FC, and fail on any reached segment that has Japanese (tbl.dec, no `$00` lists) and is not a
messages.json start, except DEBUG (45:624A, 45:62BB), NOT_PRINTED (49:45AA) and UNREFERENCED (49:4C9C..4CFC).
Validated: with messages.json from before 761efed it reports 49:422B, 4314, 44CE, 5594 (the four known) plus
the five above; with the current file it reports exactly the five above (and nothing else).
Also worth fixing: census_msgs.py bank rule (2.2) so a regenerated census is right.

## 5. Hook proposal
None needed: all five are ordinary bank-49 typewriter messages; adding them to script/messages.json (bank 49,
addr as above, {F3}/{F8} inserts copied from the JP) is enough. 49:43B9 is 4 chars + $FF, so insert_msgs takes
the $F2 path (t-o = 4); keep the English short anyway (status line, the neighbours "Lit"/"AC" are in place).
49:451F has three {F8} numbers and the direction words come from lists.json (きた/ひがし/みなみ/にし at
49:4575-4580), keep its {F4}/row layout.

## 6. Open / not confirmed
- All static. Not run in the emulator: the 55A4-after-5594 continuation (needs an alignment change in battle),
  the trigger of 49:4583 ($CB84 bit 0) and of 49:43B9 ($CB84 bit 6).
- Reach of 24:7DB9 (DEBUG:) - no direct call/jump found; may be in a jump table.
- 49:4F98 meaning (32:4219, `[$D000]`!=0) - no Japanese, not investigated further.
- Strings inserted with {F3} via 0:0EDF: all 6 tables (49:5661, 567D, 56AF, 5703, 570F, 572F) are inside the
  lists.json slot range 49:55D5-5735; not re-audited entry by entry.

## Appendix: every reached segment (generated by work/re/msgcov/table.py)
| bank:addr | JP (segment, `/` = newline) | reached by | in script |
|---|---|---|---|
| 45:4466 | /ボタンが ならんでいる//どのボタンを おしますか?///  A B C D E | code 2d:6432 | script |
| 45:4490 | /じめんに ふしぎなもようが//えがかれている | code 2d:6657 | script |
| 45:44A8 | /じめんに まほうじんが//えがかれている///だれが なかにはいりますか? | code 2d:652b | script |
| 45:44CF | /もようの ちゅうしんから//{F8 00 2D C577} があらわれた//けいやくを かわしますか?///     ... | code 2d:6591 | script |
| 45:4512 | /レベルが ひくいため//しょうかんに しっぱいしました | code 2d:663b | script |
| 45:452F | /けいやくが せいりつした | code 2d:65fd | script |
| 45:453D | /すでに けいやくずみです | code 2d:661c | script |
| 45:454B | /とびらのよこに なにかうすい//ものを さしこむようなあなが//あいている そのうえには//  『まどうエレベータ』/... | code 2d:6699 | script |
| 45:45A6 | /  パーティーが いっぱいです | code 2d:6807 | script |
| 45:45B7 | / わかわかしいおとこが たっている// 『ぼくは マーフィー//  じぶんの そんざいいぎを//  もとめて このまど... | table 2D:66C5 rec 0 ptr 0 (2D:6783/679F/67BB/6858) | script |
| 45:4626 | /『ぼくも なんども あぶないめに// あいましたが うんがいいのか// いままで いきてこれました// あなたたちと ... | table 2D:66C5 rec 0 ptr 1 (2D:6783/679F/67BB/6858) | script |
| 45:46A1 | /////     『マーフィー』を//  パーティーに くわえますか?///        はい//        い... | table 2D:66C5 rec 0 ptr 2 (2D:6783/679F/67BB/6858) | script |
| 45:46E0 | /// 『ぼくはなぜ そんざいしている//  のだろう? これがわかるまでは//  しぬわけにはいかない・・・』// お... | table 2D:66C5 rec 0 ptr 3 (2D:6783/679F/67BB/6858) | script |
| 45:4736 | ///  おとこが はなしかけてきた//  『せっしゃ ロイドともうす//   ゆみの うでまえにかけては//   てい... | table 2D:66C5 rec 1 ptr 0 (2D:6783/679F/67BB/6858) | script |
| 45:4788 | ////  『きでんらのはなしを//   さかばで よくみみにする//   せっしゃを パーティーに//   くわえても... | table 2D:66C5 rec 1 ptr 1 (2D:6783/679F/67BB/6858) | script |
| 45:47CB | /////      『ロイド』を//  パーティーに くわえますか?///        はい//        いい... | table 2D:66C5 rec 1 ptr 2 (2D:6783/679F/67BB/6858) | script |
| 45:4809 | //// 『ゆだんめされるな//  このまどうの あしきようきに//  のみこまれぬよう・・・・・・』// そういうと ... | table 2D:66C5 rec 1 ptr 3 (2D:6783/679F/67BB/6858) | script |
| 45:4850 | / ローブをきたおとこが// はなしかけてきた// 『おぬし しっておるか?//  このまどうの おそろしさを//  わ... | table 2D:66C5 rec 2 ptr 0 (2D:6783/679F/67BB/6858) | script |
| 45:48AF | / 『わしは ビショップのルーイ//  さまよいしものたちを//  とわのやすらぎに つかせる//  ことができる// ... | table 2D:66C5 rec 2 ptr 1 (2D:6783/679F/67BB/6858) | script |
| 45:4911 | /////      『ルーイ』を//  パーティーに くわえますか?///        はい//        いい... | table 2D:66C5 rec 2 ptr 2 (2D:6783/679F/67BB/6858) | script |
| 45:494F | ///『ふぉっふぉっふぉ// けっきさかんなのも ほどほどにのう// おぬしのよこにいた// たましいは じょうぶつさせ... | table 2D:66C5 rec 2 ptr 3 (2D:6783/679F/67BB/6858) | script |
| 45:49A9 | /// いさましいおとこが たっている// 『わがなは ジークフリート//  まどうにねむると つたわる//  でんせつ... | table 2D:66C5 rec 3 ptr 0 (2D:6783/679F/67BB/6858) | script |
| 45:49F7 | /// 『そのアイテムを つかうと//  あたらしい しょくぎょうに//  なることが できるらしい//  どうだ?//... | table 2D:66C5 rec 3 ptr 1 (2D:6783/679F/67BB/6858) | script |
| 45:4A45 | /////    『ジークフリート』を//  パーティーに くわえますか?///        はい//        ... | table 2D:66C5 rec 3 ptr 2 (2D:6783/679F/67BB/6858) | script |
| 45:4A85 | ////  『まぁいい きがかわったら//   さそいにきてくれ//   さかばで まっている』//  おとこは たちさ... | table 2D:66C5 rec 3 ptr 3 (2D:6783/679F/67BB/6858) | script |
| 45:4AC4 | / ふとったおとこが ひょっこりと// あらわれた// 『わたしは ライラ//  ぶっぽうのみちを あゆむもの//  し... | table 2D:66C5 rec 4 ptr 0 (2D:6783/679F/67BB/6858) | script |
| 45:4B27 | // 『みょうにち あらわれし//  うんめいの ぼうけんしゃと//  ともに みちをあゆめと//  いわれた//  ど... | table 2D:66C5 rec 4 ptr 1 (2D:6783/679F/67BB/6858) | script |
| 45:4B80 | /////      『ライラ』を//  パーティーに くわえますか?///        はい//        いい... | table 2D:66C5 rec 4 ptr 2 (2D:6783/679F/67BB/6858) | script |
| 45:4BBE | /// 『うんめいの ぼうけんしゃとは//  きみたちのことでは//  ないようだな』// おとこは あたまをかきながら... | table 2D:66C5 rec 4 ptr 3 (2D:6783/679F/67BB/6858) | script |
| 45:4C06 | ///  おとこが ちかづいてきた//  『せっしゃ こじろうともうす//   わがかたな ものほしざおを//   なに... | table 2D:66C5 rec 5 ptr 0 (2D:6783/679F/67BB/6858) | script |
| 45:4C5E | /// 『みどもを きでんらのなかまに//  くわえては もらえぬか?//  きでんらのちからが あれば//  さらにふ... | table 2D:66C5 rec 5 ptr 1 (2D:6783/679F/67BB/6858) | script |
| 45:4CB4 | /////      『こじろう』を//  パーティーに くわえますか?///        はい//        い... | table 2D:66C5 rec 5 ptr 2 (2D:6783/679F/67BB/6858) | script |
| 45:4CF3 | /// 『ううむ むねんなり//  しかたがない じつりょくのある//  ぼうけんしゃは ほかにもいよう//  さらばで... | table 2D:66C5 rec 5 ptr 3 (2D:6783/679F/67BB/6858) | script |
| 45:4D46 | //// おとこが どこからともなく// あらわれた// スキのないかまえだ// しかし さっきは かんじられない | table 2D:66C5 rec 6 ptr 0 (2D:6783/679F/67BB/6858) | script |
| 45:4D80 | //// 『わしは バディック//  わがちから きでんらのために//  つかいたく さんじょうした//  ヘんとうはい... | table 2D:66C5 rec 6 ptr 1 (2D:6783/679F/67BB/6858) | script |
| 45:4DC1 | /////     『バディック』を//  パーティーに くわえますか?///        はい//        い... | table 2D:66C5 rec 6 ptr 2 (2D:6783/679F/67BB/6858) | script |
| 45:4E00 | // 『ふむ さようか//  ひつようなときは いつでも//  こえを かけてくだされ//  では これにてごめん』//... | table 2D:66C5 rec 6 ptr 3 (2D:6783/679F/67BB/6858) | script |
| 45:4E5B | ///ローブをきたおとこが たたずんでいる//『わたしは ワーナード// わがれきしは このせかいと// ともにある//... | table 2D:66C5 rec 7 ptr 0 (2D:6783/679F/67BB/6858) | script |
| 45:4EA9 | ////  『わたしが きえるときは//   このせかいが しぬとき//   せかいとともに//   たびをするきはない... | table 2D:66C5 rec 7 ptr 1 (2D:6783/679F/67BB/6858) | script |
| 45:4EE9 | /////     『ワーナード』を//  パーティーに くわえますか?///        はい//        い... | table 2D:66C5 rec 7 ptr 2 (2D:6783/679F/67BB/6858) | script |
| 45:4F28 | /// 『ふっ それでは まだみぬ//  きょうおうの たんじょうを//  たのしみに ふたたび//  ねむりに つくこ... | table 2D:66C5 rec 7 ptr 3 (2D:6783/679F/67BB/6858) | script |
| 45:4F80 | /まもののしたいが よこたわっている//かすかに ふしゅうが ただよっている//     しらベてみますか?///   ... | code 2d:68fd | script |
| 45:4FD0 | /とくに なにもなかった | code 2d:695f | script |
| 45:4FDD | /まもののしたいが うごきだした//『わたしのねむりを// さまたげるのは だれだ!』 | code 2d:6934 | script |
| 45:5009 | / たくさんのきんかが おちている//      ひろいますか?///        はい/        いいえ | code 2d:698d | script |
| 45:5043 | /きんかを ひろおうとすると//とつぜんうごきだし おそってきた | code 2d:69c4 | script |
| 45:5064 | /{F8 10 2D FFB4}ゴールドひろった | code 2d:69fa | script |
| 45:5073 | /ローブをきた きかいなすがたの//モンスターが さけんだ//『なにものだ!// ここは たちいりきんしだぞ!』 | code 2d:6aad | script |
| 45:50AC | /モンスターは しんだ//たおれざまに なにかがローブから//とびだして おくにおちた | code 2d:6ad5 | script |
| 45:50D8 | /いおりの なかには//しずかに せいざしている//ひとりの おとこがいた | code 2d:6b09 | script |
| 45:50FE | /『ちじょうからの きゃくじんは// ひさしぶりだ しょうしょう// たいくつしていたところよ// ちょうどいいときに ... | code 2d:6b28 | script |
| 45:514F | /おとこをたおした!//しかし そこにのこされていた//ものは まるたであった//かわりみのじゅつだ!//『ふふふ・・・... | code 2d:6b50 | script |
| 45:51A9 | /ちゅうおうに いちする//ぎょくざには おそろしい//デーモンキングが すわっており//そのあしもとには さまざまな/... | code 2d:6b84 | script |
| 45:51F4 | /『ここまでこれたのは ほめてやる// だが それもここまでだ// こうていのもとには いかせぬわ』 | code 2d:6ba3 | script |
| 45:5227 | /『ぬう ここはひいてやろう』//デーモンキングのからだが//けむりとなって きえていった | code 2d:6bcb | script |
| 45:5255 | /ぜっせいの びじょが//イスに すわっている | code 2d:6bff | script |
| 45:526D | /しかし ざんねんそうな//ひょうじょうをうかベ//すがたを けしてしまった | code 2d:6c9f | script |
| 45:5294 | /びじょは うれしそうな//ほほえみをうかベ たちあがった//『ようこそ わたしのまちヘ// かんげいするわ// あなた... | code 2d:6c37 | script |
| 45:52F4 | /ここは//サキュバスのまち だったのだ//ほかの ぼうけんしゃは みな//とりこになって しまったのだろう | code 2d:6c5f | script |
| 45:532B | /とつぜん しんだはずの//サキュバスクィーンが たちあがり//あやしいえみを うかベた//『すごいのね ステキだったわ... | code 2d:6c7e | script |
| 45:5384 | /そこには//さまざまなデーモンがいた//いちばんおくの ぎょくざには//おそろしくも うつくしい//デーモンクィーンが... | code 2d:6cd3 | script |
| 45:53C8 | /『こうていが おまちしておるぞ// おまえたちのちからを// たかく ひょうかされておる// どれ わたしがためしてや... | code 2d:6cf2 | script |
| 45:5408 | /『ここまでとは・・・// そのちから わがしんえいたいに// ほしいくらいだ』//デーモンクィーンの からだが//ゆっ... | code 2d:6d1a | script |
| 45:544F | /とつぜん//めのまえの くうかんがさけた!//そこから なにかがでてこようと//している//『アディッシュ・・シンダ・... | code 2d:6d4e | script |
| 45:54A6 | /モンスターは くるったように//さけびながら くうかんのひずみに//にげこんでいった | code 2d:6d76 | script |
| 45:54D2 | /とつぜん きょだいな ゆみやが//あらわれた//やさきが つきつけられ//げんが ひきしぼられていく | code 2d:6da4 | script |
| 45:5506 | /いけのそこから なにかがうかんできた | code 2d:6ddb | script |
| 45:551A | /そこには まかいのしんぷが//しずかに たたずんでいた//『ちじょうのものたちよ// ししゃのねむりを みだしたつみ/... | code 2d:6e12 | script |
| 45:5579 | ///みたこともない おおきなものが//てんじょうと ゆかに//めりこんでいる//そのなかから ムシのような//いきもの... | code 2d:6e4f | script |
| 45:55C1 | /そのいきものが はなしかけてきた//『タスケテホシイ 500G// ワケテ クレナイカ?』///       はい/ ... | code 2d:6e77 | script |
| 45:5607 | /『アリガトウ ワレラノ チョウサニ// ヨルト チカフカクデ デーモンガ// イジゲンカラ マモノヲショウカン// シ... | code 2d:6ef1 | script |
| 45:5650 | /おおくのアンバーハルクが//あつまっていた//しせんはすベて こちらに//むけられている キケンだ! | code 2d:6f25 | script |
| 45:5684 | /ここは//アンバーハルクの まちなのだ//ここから さまざまなところヘ//かりに いくのだろう | code 2d:6f4d | script |
| 45:56B5 | /しっこくのふくをきた//うつくしいおとこが たっていた | code 2d:6f7b | script |
| 45:56D2 | /『アディッシュは しんだようだな// こんな かとうせいぶつに// たおされるようでは まかいの// ものも ちにおち... | code 2d:6f9a | script |
| 45:5714 | /『もっとも われらとて// やつらをりようしただけ// ちじょうを ものにしたあと// やつらをころす// てはずだっ... | code 2d:6fb9 | script |
| 45:5769 | /くうかんの ひずみから//きょうだいなものが//すがたを あらわそうとしている! | code 2d:6ff6 | script |
| 45:5793 | /『いにしえからのもの』は//いじげんヘ ひきあげていった | code 2d:701e | script |
| 45:57B1 | /きょだいな ぎょくざに//まかいのこうていが すわっている | code 2d:704f | script |
| 45:57D0 | /とつぜん いてつくようなしせんが//こちらに つきつけられた//『ようやくきたか ちじょうのものよ// だが おそすぎ... | code 2d:706e | script |
| 45:5836 | /『わしとともに ちじょうが// あんこくに そめあげられていく// さまを みとどけるかね?// それとも・・・・・・... | code 2d:708d | script |
| 45:5874 | /デーモンアディッシュは//だんまつまの こえをあげた | code 2d:70b5 | script |
| 45:5890 | /『グオォォォ......// なんということだ!// きさまらごときに// きさまらごときに やられるとは』 | code 2d:70d4 | script |
| 45:58C8 | /『しかし// これでおわったわけではない// わが しょうかんせし// いじげんのものたち// やつらが// やつらが... | code 2d:70f3 | script |
| 45:590F | /そこまでいうと//しずかに うごきをとめた//そのめはカッと//みひらかれたままであった | code 2d:7112 | script |
| 45:593D | /めのまえに なにかがいる!//いままでの ぼうけんしゃとしての//カンが にげることをおしえている | code 2d:714c | script |
| 45:5970 | /デーモンアディッシュが//いじげんから よびだした//さいきょう さいあく さいだいの//かいぶつが すぐそこにいるの... | code 2d:716b | script |
| 45:59AF | /いま さいごのけっせんが//はじまろうとしている | code 2d:718a | script |
| 45:59C9 | /かいぶつの からだからは//ねんちゃくしつの たいえきが//まきちらされ ひどいにおいを//はなちながら どすぐろいケ... | code 2d:71b2 | script |
| 45:5A18 | /そして おぞましきかいぶつの//さけびが くうかんをひずませ//いじげんへの とびらを//ひらいていく//かいぶつの ... | code 2d:71d1 | script |
| 45:5A74 | /やがて いじげんへの//とびらは きえ あたりには//せいじゃくだけがのこった・・・ | code 2d:71f0 | script |
| 45:5AA0 | /きょうだいなる まのふういんが//ほどこされている | code 2d:722e | script |
| 45:5ABB | / とびらには フダがはりつけてあり// なにか もじがかいてある// 『まものが しゅつぼつするため//  このいけを... | table 2D:79C8[0] (2D:7A13) | script |
| 45:5B08 | /      ごうもんしつ | table 2D:79C8[1] (2D:7A13) | script |
| 45:5B16 | /       ろうごく | table 2D:79C8[2] (2D:7A13) | script |
| 45:5B23 | / もんのわきに もじがかかれている// 『まどうぼち//  まかいのゆうしゃ ここにねむる』 | table 2D:79C8[3] (2D:7A13) | script |
| 45:5B53 | /      れいはいどう | table 2D:79C8[4] (2D:7A13) | script |
| 45:5B61 | / とびらには フダがはりつけてあり// なにか もじがかかれている// 『これよりさき ちていこ//  キケンにつき ... | table 2D:79C8[5] (2D:7A13) | script |
| 45:5BA6 | /   ゆるやかな くだりざかだ | table 2D:79C8[6] (2D:7A13) | script |
| 45:5BB7 | / このみちは まかいのちゅうしんヘ//    つづくように おもえた | table 2D:79C8[7] (2D:7A13) | script |
| 45:5BDB | /      このさきには// まかいのこうていの ヘやがある | table 2D:79C8[8] (2D:7A13) | script |
| 45:5BFB | /    『このさきキケン!』// なんびとも たちいることをきんず | table 2D:79C8[9] (2D:7A13) | script |
| 45:5C1E | /どこからか クスクスッという//わらいごえが きこえてくる//『おとこかしら おとこだわ//    おとこよ おとこね... | code 2d:7272 | script |
| 45:5C6D | /ようせいがいる//しかし こちらに きづいたとたん//にげるように さっていった | code 2d:7387; code 2d:749a | script |
| 45:5C97 | /なにかひかるものが//ひらひらと ちかづいてきた//それは ちいさなようせいであった | code 2d:72f5; code 2d:7409 | script |
| 45:5CC3 | /『こんにちは 1Gでわたしのふたごの// あね レイのところヘテレポートして// さしあげますけど いかがかしら?』/... | code 2d:7314 | script |
| 45:5D18 | /『それでは いきますよ// デーモンたちには ないしょにして// くださいね』 | code 2d:7343 | script |
| 45:5D41 | /『よう! 1Gでアタイの ふたごの// いもうと シアのところに// テレポートしてやるけど どう?』///     ... | code 2d:7428 | script |
| 45:5D8F | /『それじゃ いくぜ!// デーモンたちには ないしょにして// くれよな!』 | code 2d:7457 | script |
| 45:5DB7 | /そこには さまざまなガラクタが//やまのように つまれている//やくだつものが あるかもしれない//    しらベてみ... | code 2d:74bd | script |
| 45:5E0F | /やくにたちそうなものは//ありませんでした | code 2d:7534 | script |
| 45:5E26 | /{F8 00 2D C54F} が//みつかりました | code 2d:7513 | script |
| 45:5E38 | /もちものが いっぱいです | code 2d:7602 | script |
| 45:5E46 | /さきほどのモンスターが//おとしたものを みつけた//きんぞくせいのカードであった | code 2d:75df | script |
| 45:5E71 | /なにも みつからなかった | code 2d:7624 | script |
| 45:5E7F | /そこにはいどがあり みずがある//    のんでみますか?///       はい/       いいえ | code 2d:7651 | script |
| 45:5EB5 | だれが のみますか? | code 2d:7682 | script |
| 45:5EC0 | / たいりょくが すベてかいふくした | table 2D:763B[0] (2D:7724) | script |
| 45:5ED3 | /    どくのいずみだった | table 2D:763B[1] (2D:7724) | script |
| 45:5EE2 | / せいじょうな じょうたいになった | table 2D:763B[2] (2D:7724) | script |
| 45:5EF5 | /   おおきなダメージをうけた | table 2D:763B[3] (2D:7724) | script |
| 45:5F06 | /     からだがまひした | table 2D:763B[4] (2D:7724) | script |
| 45:5F15 | /そこには ひとりのまじゅつしがいた//『500Gで ふゆうのじゅもんを// かけて しんぜよう いかがかな?』/// ... | code 2d:77be | script |
| 45:5F67 | /まじゅつしは じゅもんをとなえた//『よし うかびあがったぞ// それでは たっしゃでな』 | code 2d:7806 | script |
| 45:5F96 | /かわいらしい かおだちをした//メイドすがたの むすめがいた//『よろしければ ちじょうヘ// おくりとどけて さしあ... | code 2d:7829 | script |
| 45:5FFE | /それでは いきますよ | code 2d:785d | script |
| 45:600A | /なにかが てんじょうに//はりついている//それは めだまにつばさがはえた//ちいさなモンスターであった//こちらをじ... | code 2d:7897 | script |
| 45:605A | /そこにはマントすがたの//うつくしい おとこがたっていた | code 2d:78e0 | script |
| 45:6078 | /『ここまでこれたものは// そうはいない たいしたものだ// まかいのものがちじょうを// しはいするのは われらもこ... | code 2d:7906 | script |
| 45:60E6 | /キラリとひかった そのくちもとに//かすかにキバらしきものがみえた//おとこは きえるようにさっていった | code 2d:7925 | script |
| 45:611C | /そこにはドレスすがたをした//けだかくもうつくしき//じょせいがたっていた | code 2d:796e | script |
| 45:6143 | /『わたしは やみのせかいのじょおう// あなたたちのことは きいています// とくベつなしょくぎょうになるには// こ... | code 2d:798d | script |
| 45:61B0 | / とつぜん けいほうがなりひびいた// しばらくすると なにかが// ちかづいてくるおとが きこえてきた | code 2d:79b0 | script |
| 45:61E6 | / まどうエレベータ かんりにんしつ | table 2D:79C8[10] (2D:7A13) | script |
| 45:61F9 | /   まりょく むこうくうかん | table 2D:79C8[11] (2D:7A13) | script |
| 45:620A | //おつかれさまでした//このじょうたいで でんげんを//きることができます//Aボタンをおせば//ぼうけんをさいかいで... | code 20:4a8c; code 2d:7c14 | script |
| 45:624A | ーー デバッグモードについて ーー//こちらでは じょうけんを//せっていしません//かくじ じょうけんを//さんしょう... | code 2d:7c75 | MISSING |
| 45:62BB | イベントナンバーのみ/    15~23/36~38/じょうけんがいろいろ/    11/25~35/パラメーター1でへ... | code 2c:4c3e | MISSING |
| 45:638F | /マップきろくシートを つかいますか?//        はい/        いいえ | code 2d:7c38 | script |
| 46:44DA | 『いにしえからのもの』を//しょうかんする | table 2A:76D0[0] (2A:4AB2) | script |
| 46:44F0 | 『イフリート』をしょうかんする | table 2A:76D0[1] (2A:4AB2) | script |
| 46:4500 | 『ヴァンパイアロード』を//しょうかんする | table 2A:76D0[2] (2A:4AB2) | script |
| 46:4516 | 『かなたよりのもの』を//しょうかんする | table 2A:76D0[3] (2A:4AB2) | script |
| 46:452B | 『グール』をしょうかんする | table 2A:76D0[4] (2A:4AB2) | script |
| 46:4539 | 『グレーターデーモン』を//しょうかんする | table 2A:76D0[5] (2A:4AB2) | script |
| 46:454F | 『けいようしがたきもの』を//しょうかんする | table 2A:76D0[6] (2A:4AB2) | script |
| 46:4566 | 『ジィニー』をしょうかんする | table 2A:76D0[7] (2A:4AB2) | script |
| 46:4575 | 『シャドウドラゴン』を//しょうかんする | table 2A:76D0[8] (2A:4AB2) | script |
| 46:458A | 『ゾンビ』をしょうかんする | table 2A:76D0[9] (2A:4AB2) | script |
| 46:4598 | 『タイタン』をしょうかんする | table 2A:76D0[10] (2A:4AB2) | script |
| 46:45A7 | 『ダオ』をしょうかんする | table 2A:76D0[11] (2A:4AB2) | script |
| 46:45B4 | 『マリッド』をしょうかんする | table 2A:76D0[12] (2A:4AB2) | script |
| 46:45C3 | 『ミノタウロス』を//しょうかんする | table 2A:76D0[13] (2A:4AB2) | script |
| 46:45D6 | 『ライオン オブ ヘル』を//しょうかんする | table 2A:76D0[14] (2A:4AB2) | script |
| 46:45ED | 『きょうふ』をかいふくする | table 2A:76D0[15] (2A:4AB2) | script |
| 46:45FB | 『すいみん』をかいふくする | table 2A:76D0[16] (2A:4AB2) | script |
| 46:4609 | 『いし』をちりょうする | table 2A:76D0[17] (2A:4AB2) | script |
| 46:4615 | 『どく』をちりょうする | table 2A:76D0[18] (2A:4AB2) | script |
| 46:4621 | 『まひ』をちりょうする | table 2A:76D0[19] (2A:4AB2) | script |
| 46:462D | 『しぼう』したキャラクタを//そせいさせる | table 2A:76D0[20] (2A:4AB2) | script |
| 46:4643 | 『しぼう・はい』じょうたいの//キャラクタを そせいさせる | table 2A:76D0[21] (2A:4AB2) | script |
| 46:4661 | 10~100の ダメージをあたえる//+クリティカルのかのうせいがたかい | table 2A:76D0[22] (2A:4AB2) | script |
| 46:4686 | 10~100の ダメージをあたえる | table 2A:76D0[23] (2A:4AB2) | script |
| 46:4698 | 12~144の ダメージをあたえる | table 2A:76D0[24] (2A:4AB2) | script |
| 46:46AA | 12~96の ダメージをあたえる | table 2A:76D0[25] (2A:4AB2) | script |
| 46:46BB | 2~16の ダメージをあたえる | table 2A:76D0[26] (2A:4AB2) | script |
| 46:46CB | 20~200の ダメージをあたえる | table 2A:76D0[27] (2A:4AB2) | script |
| 46:46DD | 24~32の ダメージをあたえる | table 2A:76D0[28] (2A:4AB2) | script |
| 46:46EE | 3~24の ダメージをあたえる | table 2A:76D0[29] (2A:4AB2) | script |
| 46:46FE | 4~32の ダメージをあたえる | table 2A:76D0[30] (2A:4AB2) | script |
| 46:470E | 7~56の ダメージをあたえる | table 2A:76D0[31] (2A:4AB2) | script |
| 46:471E | 6~48の ダメージをあたえる | table 2A:76D0[32] (2A:4AB2) | script |
| 46:472E | 60~170の ダメージをあたえる | table 2A:76D0[33] (2A:4AB2) | script |
| 46:4740 | 8~64の ダメージをあたえる | table 2A:76D0[34] (2A:4AB2) | script |
| 46:4750 | 9~72の ダメージをあたえる | table 2A:76D0[35] (2A:4AB2) | script |
| 46:4760 | 75%のかくりつで//まほうをかいひする | table 2A:76D0[36] (2A:4AB2) | script |
| 46:4775 | 60%のかくりつで//まほうをかいひする | table 2A:76D0[37] (2A:4AB2) | script |
| 46:478A | 90%のかくりつで//まほうをむこうにする | table 2A:76D0[38] (2A:4AB2) | script |
| 46:47A0 | 95%のかくりつで//まほうをむこうにする | table 2A:76D0[39] (2A:4AB2) | script |
| 46:47B6 | 95%のかくりつで//たからばこのワナを みやぶる | table 2A:76D0[40] (2A:4AB2) | script |
| 46:47D0 | しゃていLの こうげきを//95%のかくりつで むこうにする | table 2A:76D0[41] (2A:4AB2) | script |
| 46:47EF | たからばこのワナを//95%のかくりつで みやぶる | table 2A:76D0[42] (2A:4AB2) | script |
| 46:4809 | ACをー2する | table 2A:76D0[43] (2A:4AB2) | script |
| 46:4811 | ACをー4する | table 2A:76D0[44] (2A:4AB2) | script |
| 46:4819 | ACをー5する | table 2A:76D0[45] (2A:4AB2) | script |
| 46:4821 | ACをー7する | table 2A:76D0[46] (2A:4AB2) | script |
| 46:4829 | ACをー8する | table 2A:76D0[47] (2A:4AB2) | script |
| 46:4831 | ACをー9する | table 2A:76D0[48] (2A:4AB2) | script |
| 46:4839 | HPを14~42かいふくする | table 2A:76D0[49] (2A:4AB2) | script |
| 46:4848 | HPを16~24かいふくする | table 2A:76D0[50] (2A:4AB2) | script |
| 46:4857 | HPを24~32かいふくする | table 2A:76D0[51] (2A:4AB2) | script |
| 46:4866 | HPを32~48かいふくする | table 2A:76D0[52] (2A:4AB2) | script |
| 46:4875 | HPを25~39かいふくする | table 2A:76D0[53] (2A:4AB2) | script |
| 46:4884 | HPを4~8かいふくする | table 2A:76D0[54] (2A:4AB2) | script |
| 46:4891 | HPを7~21かいふくする | table 2A:76D0[55] (2A:4AB2) | script |
| 46:489F | あくまを たいきょさせる | table 2A:76D0[56] (2A:4AB2) | script |
| 46:48AC | アンデッドモンスターを はかいする | table 2A:76D0[57] (2A:4AB2) | script |
| 46:48BE | いきていれば HPも じょうたいも//すベてかいふくする | table 2A:76D0[58] (2A:4AB2) | script |
| 46:48DB | いきていれば//HPをすベてかいふくする | table 2A:76D0[59] (2A:4AB2) | script |
| 46:48F0 | いきていれば//じょうたいを『せいじょう』にする | table 2A:76D0[60] (2A:4AB2) | script |
| 46:4909 | いきていれば//ステータス・HPをすベてかいふくする | table 2A:76D0[61] (2A:4AB2) | script |
| 46:4924 | 『しぼう』や『はい』であっても//HPやじょうたいが ぜんかいふく | table 2A:76D0[62] (2A:4AB2) | script |
| 46:4946 | あいてを きょうふさせる | table 2A:76D0[63] (2A:4AB2) | script |
| 46:4953 | あいてを しぼうさせる | table 2A:76D0[64] (2A:4AB2) | script |
| 46:495F | あいてを しょうめつさせる | table 2A:76D0[65] (2A:4AB2) | script |
| 46:496D | あいてを ねむらせる | table 2A:76D0[66] (2A:4AB2) | script |
| 46:4978 | あいてを いしにする | table 2A:76D0[67] (2A:4AB2) | script |
| 46:4983 | あいてを ちんもくさせる | table 2A:76D0[68] (2A:4AB2) | script |
| 46:4990 | あいてを まひさせる | table 2A:76D0[69] (2A:4AB2) | script |
| 46:499B | めいきゅうのしかいをひろげる | table 2A:76D0[70] (2A:4AB2) | script |
| 46:49AA | ちょうじかん//めいきゅうのしかいをひろげる | table 2A:76D0[71] (2A:4AB2) | script |
| 46:49C1 | つうじょうこうげき | table 2A:76D0[72] (2A:4AB2) | script |
| 46:49CB | つうじょうこうげき//+きょうふ | table 2A:76D0[73] (2A:4AB2) | script |
| 46:49DC | つうじょうこうげき+クリティカルの//かのうせいがとてもたかい | table 2A:76D0[74] (2A:4AB2) | script |
| 46:49FC | つうじょうこうげき+クリティカルの//かのうせいがたかい | table 2A:76D0[75] (2A:4AB2) | script |
| 46:4A19 | つうじょうこうげき//+すいみん | table 2A:76D0[76] (2A:4AB2) | script |
| 46:4A2A | つうじょうこうげき//+いし | table 2A:76D0[77] (2A:4AB2) | script |
| 46:4A39 | つうじょうこうげき//+ダメージぶん HPかいふく | table 2A:76D0[78] (2A:4AB2) | script |
| 46:4A53 | つうじょうこうげき//+まひ | table 2A:76D0[79] (2A:4AB2) | script |
| 46:4A62 | すでに つうかしたばしょに//いどうする | table 2A:76D0[80] (2A:4AB2) | script |
| 46:4A77 | のろわれたアイテムを//1つ じょきょする | table 2A:76D0[81] (2A:4AB2) | script |
| 46:4A8D | ピット・シュートをかいひする//すいめんを あるくことができる | table 2A:76D0[82] (2A:4AB2) | script |
| 46:4AAD | まちにテレポートする//1どとなえると わすれる | table 2A:76D0[83] (2A:4AB2) | script |
| 46:4AC6 | みかたの『つうじょうこうげき』に//1~8の ついかダメージをくわえる | table 2A:76D0[84] (2A:4AB2) | script |
| 46:4AEA | モンスターを ランダムで//しょうかんする | table 2A:76D0[85] (2A:4AB2) | script |
| 46:4B00 | モンスターを しきベつする | table 2A:76D0[86] (2A:4AB2) | script |
| 46:4B0E | めいちゅうりつと ついかダメージに//4をくわえる | table 2A:76D0[87] (2A:4AB2) | script |
| 46:4B28 | めいちゅうりつと ついかダメージに//6をくわえる | table 2A:76D0[88] (2A:4AB2) | script |
| 46:4B42 | めいちゅうりつと ついかダメージに//1をくわえる | table 2A:76D0[89] (2A:4AB2) | script |
| 46:4B5C | めいちゅうりつと ついかダメージに//3をくわえる | table 2A:76D0[90] (2A:4AB2) | script |
| 46:4B76 | めいちゅうりつと ついかダメージに//5をくわえる | table 2A:76D0[91] (2A:4AB2) | script |
| 46:4B90 | めいちゅうりつを 4さげる//ACを 4あげる | table 2A:76D0[92] (2A:4AB2) | script |
| 46:4BA8 | うんを 1あげる | table 2A:76D0[93] (2A:4AB2) | script |
| 46:4BB1 | めいきゅうにいる ほかの//パーティーのざひょうを しらベる | table 2A:76D0[94] (2A:4AB2) | script |
| 46:4BD0 | カギをあける | table 2A:76D0[95] (2A:4AB2) | script |
| 46:4BD7 | かならず せんとうから//にげることができる | table 2A:76D0[96] (2A:4AB2) | script |
| 46:4BEE | 『きしゅう』じょうたいで//こうげきする | table 2A:76D0[97] (2A:4AB2) | script |
| 46:4C03 | げんざい こうかをおよぼしている//まほうをむこうにする | table 2A:76D0[98] (2A:4AB2) | script |
| 46:4C20 | なにか いいことがおこるが//レベルが1さがる | table 2A:76D0[99] (2A:4AB2) | script |
| 46:4C38 | パーティーのいちを ひょうじする | table 2A:76D0[100] (2A:4AB2) | script |
| 46:4C49 | HPを28~55かいふくする | table 2A:76D0[101] (2A:4AB2) | script |
| 46:4C58 | よそくできないダメージをあたえる | table 2A:76D0[102] (2A:4AB2) | script |
| 46:4C69 | HPを33~54かいふくする | table 2A:76D0[103] (2A:4AB2) | script |
| 46:4C78 | 50%のかくりつで//まほうをかいひする | table 2A:76D0[104] (2A:4AB2) | script |
| 46:4C8D | 85%のかくりつで//まほうをかいひする | table 2A:76D0[105] (2A:4AB2) | script |
| 46:4CA2 | HPを45~85かいふくする | table 2A:76D0[106] (2A:4AB2) | script |
| 46:4CB1 | HPを24~52かいふくする | table 2A:76D0[107] (2A:4AB2) | script |
| 46:4CC0 | ACをー6する | table 2A:76D0[108] (2A:4AB2) | script |
| 46:4CC8 | HPを20~32かいふく+いきて//いれば じょうたいを『せいじょう』に | table 2A:76D0[109] (2A:4AB2) | script |
| 49:4191 | {F8 40 31 C1DA} | code 22:5ac0 | MISSING |
| 49:4197 | {F8 00 31 C48F} | code 22:5961 | MISSING |
| 49:419D | {F8 24 31 C4F3}/{F8 24 31 C4F1} | code 22:5a38 | MISSING |
| 49:41B5 | {F8 00 31 C48F}{F4 08 FF}{F8 A4 31 C4F3}/{F8 A4 31 C4F1} | code 20:61b2; code 32:4295 | MISSING |
| 49:41C9 | {F8 00 31 C48F}{F4 08 FF}{F8 A4 31 C4F3}/{F3 31 C6E3} | code 20:61a6; code 32:4289 | MISSING |
| 49:41DC | {F8 00 31 C48F}{F4 08 FF}{F3 31 C6E3} | code 32:42c7 | MISSING |
| 49:41E9 | {F8 00 31 C50F} | code 20:615e | MISSING |
| 49:41EF | {F3 31 C6E3} | code 00:248f; code 22:5414; code 22:599b (+3 more) | MISSING |
| 49:41F4 | {F8 00 31 4106} | code 22:5a75 | MISSING |
| 49:41FA | うえに のぼる かいだんが ある/    のぼりますか?/      はい/      いいえ/ | code 20:5b7a | script |
| 49:422B | したに おりる かいだんが ある/    おりますか?/      はい/      いいえ/ | code 20:5bbf | script |
| 49:425B | パーティーは ぜんめつしました | code 01:64ef | script |
| 49:426B | {F8 00 31 C48F}{F4 0A FF}L{F8 A3 31 C49C} | code 01:653d | MISSING |
| 49:427A | さがす/かぎをこじあける/なかまをさがす/ぼうけんをやめる/せってい | code 20:491a | script |
| 49:429D | さがす/かぎをこじあける/なかまをさがす/せってい | code 20:4903 | script |
| 49:42B7 |  でんげんを きれるようにする/ ベつの パーティーをくむ | code 20:4a21 | script |
| 49:42D5 | /    ドアが あります | code 20:51c2 | script |
| 49:42E3 | /シークレットドアを みつけた | code 20:51b3 | script |
| 49:42F3 | /   なにもみつかりません | code 20:51d1 | script |
| 49:4302 | さがしています | code 20:4aed | script |
| 49:430A | . | code 20:6339 | MISSING |
| 49:430C | みつかりました | code 20:4d19; code 20:4e85 | script |
| 49:4314 | だれを パーティーに くわえますか?/                 {F4 06 03}あと {F8 10 31 C... | code 20:4d55 | script |
| 49:4346 | だれも いません | code 20:4ee0 | script |
| 49:434F | パーティーは いっぱいです | code 20:4ea2 | script |
| 49:435D | だれが かぎを あけますか | code 20:4f76 | script |
| 49:436B | かぎを あけています | code 20:4fd8 | script |
| 49:4376 | しっぱいしました | code 20:50ea | script |
| 49:437F | かぎが あきました | code 20:50c4 | script |
| 49:4389 | かぎは かかっていません | code 20:5104 | script |
| 49:4396 | ドアが ありません | code 20:511e | script |
| 49:43A0 | かぎが かかっています | code 20:4683 | script |
| 49:43AC | まっくらやみだ! | code 20:5316 | script |
| 49:43B5 | あかり | code 20:493d | script |
| 49:43B9 | しきベつ | code 20:495b | MISSING |
| 49:43BE | ほご | code 20:4979 | script |
| 49:43C1 | ふゆう | code 20:4997 | script |
| 49:442C | {F8 00 31 C54F} | code 22:53f1 | MISSING |
| 49:4432 | {F3 31 C6E3}を えらんでください | code 22:5266 | MISSING |
| 49:446B | そうびしない | code 22:52d7 | script |
| 49:4472 | のろわれているので はずせません | code 22:53a7 | script |
| 49:4483 | いしのなか | code 20:5b50; code 23:49de | script |
| 49:4489 | どくへび | code 20:5d9b | script |
| 49:448E | らくばん | code 20:5daf | script |
| 49:4493 | つりてんじょう | code 20:5dc4 | script |
| 49:449B |      ピット | code 20:5dd9 | script |
| 49:44A4 |      シュート | code 20:5edb | script |
| 49:44AE | しかし ちゅうにういている | code 20:5e05; code 20:5f06 | script |
| 49:44BC | /{F8 00 31 C48F}は なにかに きづいた | code 20:5cc7 | script |
| 49:44CE |   パーティーの げんざいいちは//      ちか {F8 20 31 C6E3}かい//      きた {F8 1... | code 23:46d6 | script |
| 49:451F |   どこへ テレポートしますか?//       ちか {F8 20 31 C6E3}かいの/ ここから きたへ  {F... | code 23:4759 | MISSING |
| 49:4583 | /もとのちてんに もどされた | code 20:43f6 | MISSING |
| 49:4592 | /いてっ | code 20:46d3 | script |
| 49:4597 | /{F8 00 31 C50F}は{FA}{F8 00 31 C48F}に{FA}{F3 31 C6E3}{FC} | table 32:59CE[0] (32:4D89/5265) | script |
| 49:45AA | {FC} | code 22:4452; code 22:4dd0; code 25:49d6 (+1 more) | inside 49:4597 |
| 49:45AB | /{F8 00 31 C50F}は{FA}{F8 00 31 C48F}を{FA}{F3 31 C6E3}{FC} | table 32:59CE[1] (32:4D89/5265); table 32:59CE[2] (32:4D89/5265); table 32:59CE[3] (32:4D89/5265) (+1 more) | script |
| 49:45BF | /{F8 00 31 C50F}は{FA}{F8 00 31 C48F}の{FA}{F3 31 C6E3}{FC} | $FC continuation of 49:4597 | script |
| 49:45D3 | /{F8 00 31 C50F}は{FA}{F3 31 C6E3}{FC} | code 22:712f; $FC continuation of 49:4597 | script |
| 49:45E0 | /{F8 00 31 C48F}は{FA}{F8 00 31 C50F}に{FA}{F3 31 C6E3}{FC} | table 32:58D6[0] (32:43E6/4872); $FC continuation of 49:4597 | script |
| 49:45F4 | /{F8 00 31 C48F}は{FA}{F8 00 31 C50F}を{FA}{F3 31 C6E3}{FC} | table 32:58D6[1] (32:43E6/4872); table 32:58D6[2] (32:43E6/4872); table 32:58D6[3] (32:43E6/4872) (+1 more) | script |
| 49:4608 | /{F8 00 31 C48F}は{FA}{F8 00 31 C50F}の{FA}{F3 31 C6E3}{FC} | $FC continuation of 49:4597 | script |
| 49:461C | /{F8 00 31 C48F}は{FA}{F3 31 C6E3}{FC} | $FC continuation of 49:4597 | script |
| 49:4629 | /{F8 00 31 C48F}は{FA}さらにこうげきした{FC} | code 32:47ec; $FC continuation of 49:4597 | script |
| 49:463B | /そして{F8 20 04 D963}ダメージを{FA}あたえた{FC} | code 32:45df; code 32:49fb; code 32:4b69 (+3 more) | script |
| 49:464F | /そして{F8 10 04 D962}かい{FA}あたり{FA}{F8 20 04 D963}ダメージを{FA}あたえた... | code 32:45c3; code 32:49df; code 32:4e33 (+2 more) | script |
| 49:466F | /{F8 00 31 C50F}は{FA}{F8 20 04 D963}ダメージを{FA}うけた{FC} | $FC continuation of 49:4597 | script |
| 49:4686 | /{F8 00 31 C48F}は{FA}{F8 20 04 D963}ダメージを{FA}うけた{FC} | code 22:71a7; code 22:7728; code 32:4a0b (+1 more) | script |
| 49:469D | /しかし ダメージをあたえられなかった{FC} | code 32:4628; code 32:4a44; code 32:4b75 (+3 more) | script |
| 49:46B1 | /{F8 00 31 C50F}は{FA}{F8 00 31 C577}を{FA}となえた{FC} | $FC continuation of 49:4597 | script |
| 49:46C5 | /{F8 00 31 C48F}は{FA}{F8 00 31 C577}を{FA}となえた{FC} | code 00:2f2a; code 00:2fab; code 00:302f (+44 more) | script |
| 49:46D9 | /{F8 00 31 C50F}は{FA}きょうふした!{FC} | code 24:4cee; code 32:4755; code 24:4247 (hram $CE/$CF) (+2 more) | script |
| 49:46E9 | /{F8 00 31 C48F}は{FA}きょうふした!{FC} | code 32:4f90; code 32:502a; code 32:5474 (+4 more) | script |
| 49:46F9 | /{F8 00 31 C50F}は{FA}ねむった!{FC} | code 24:4d07; code 24:63d4; code 32:4744 (+5 more) | script |
| 49:4707 | /{F8 00 31 C48F}は{FA}ねむった!{FC} | code 24:643a; code 32:4f81; code 32:5065 (+5 more) | script |
| 49:4715 | /{F8 00 31 C50F}は{FA}まひした!{FC} | code 24:4d20; code 32:4733; code 24:478f (hram $CE/$CF) (+4 more) | script |
| 49:4723 | /{F8 00 31 C48F}は{FA}まひした!{FC} | code 25:4f86; code 25:4fe5; code 32:4f72 (+6 more) | script |
| 49:4731 | /{F8 00 31 C50F}は{FA}いしになった!{FC} | code 24:4caf; code 32:4722; code 24:4953 (hram $CE/$CF) (+2 more) | script |
| 49:4741 | /{F8 00 31 C48F}は{FA}いしになった!{FC} | code 22:721b; code 22:7786; code 25:5045 (+6 more) | script |
| 49:4751 | /{F8 00 31 C50F}の{FA}くびをはねた!{FC} | code 32:47ae; $FC continuation of 49:4597 | script |
| 49:4761 | /{F8 00 31 C48F}は{FA}くびをはねられた!{FC} | code 32:4ef6; code 32:5119; code 32:53d0 (+2 more) | script |
| 49:4773 | /{F8 00 31 C50F}は{FA}しんだ!{FC} | code 22:65f1; code 24:4c6e; code 24:4da8 (+9 more) | script |
| 49:4780 | /{F8 00 31 C48F}は{FA}しんだ!{FC} | code 22:7233; code 22:7799; code 24:58f4 (+7 more) | script |
| 49:478D | /{F8 00 31 C50F}は{FA}くらやみに{FA}つつまれた!{FC} | code 24:45b6; $FC continuation of 49:4597 | script |
| 49:47A2 | /{F8 00 31 C48F}は{FA}くらやみに{FA}つつまれた!{FC} | code 24:4631; $FC continuation of 49:4597 | script |
| 49:47B7 | /{F8 00 31 C50F}は{FA}じめんに{FA}のみこまれた!{FC} | code 24:4bbc; $FC continuation of 49:4597 | script |
| 49:47CC | /{F8 00 31 C50F}は{FA}くずれさった!{FC} | $FC continuation of 49:4597 | script |
| 49:47DC | /{F8 00 31 C50F}は{FA}きえさった!{FC} | code 24:4e20; $FC continuation of 49:4597 | script |
| 49:47EB | /{F8 00 31 C50F}は{FA}どくをうけた!{FC} | code 24:4cc3; $FC continuation of 49:4597 | script |
| 49:47FB | /{F8 00 31 C48F}は{FA}どくをうけた!{FC} | code 22:71fc; code 22:776d; code 25:4ef0 (+3 more) | script |
| 49:480B | /{F8 00 31 C50F}は{FA}ちんもくした!{FC} | code 24:4cd6; code 24:54c7; $FC continuation of 49:4597 | script |
| 49:481B | /{F8 00 31 C48F}は{FA}ちんもくした!{FC} | code 24:5546; $FC continuation of 49:4597 | script |
| 49:482B | /{F8 00 31 C48F}は{FA}{F8 10 04 C537}レベル{FA}すいとられた!{FC} | code 32:5178; $FC continuation of 49:4597 | script |
| 49:4844 | /{F8 00 31 C48F}は{FA}{F8 00 31 C50F}の{FA}HPをすいとった!{FC} | code 32:4675; code 32:4713; $FC continuation of 49:4597 | script |
| 49:485D | /{F8 00 31 C50F}は{FA}{F8 00 31 C48F}の{FA}HPをすいとった!{FC} | code 32:4f54; code 32:5432; $FC continuation of 49:4597 | script |
| 49:4876 | /{F8 00 31 C50F}は{FA}にげた!{FC} | code 22:72b4; $FC continuation of 49:4597 | script |
| 49:4883 | /{F8 00 31 C50F}は{FA}たすけをよんだ...{FC} | code 22:72c4; $FC continuation of 49:4597 | script |
| 49:4896 | /いっぴきのモンスターがあらわれた{FC} | code 22:7323; $FC continuation of 49:4597 | script |
| 49:48A8 | /しかし たすけはこなかった{FC} | code 22:7333; $FC continuation of 49:4597 | script |
| 49:48B7 | /えんぐんがとうちゃくした{FC} | code 22:602b; $FC continuation of 49:4597 | script |
| 49:48C5 | /{F8 00 31 C50F}が{FA}ぜんしんした{FC} | code 22:6a81; $FC continuation of 49:4597 | script |
| 49:48D4 | /{F8 00 31 C50F}には{FA}きかなかった!{FC} | code 24:45c2; code 24:4bcb; code 24:4d38 (+11 more) | script |
| 49:48E5 | /{F8 00 31 C48F}には{FA}きかなかった!{FC} | code 00:32e1; code 24:799c; $FC continuation of 49:4597 | script |
| 49:48F6 | /{F8 00 31 C50F}には{FA}こうかがなかった!{FC} | code 24:4d2c; code 24:54d3; code 24:7912 (+1 more) | script |
| 49:4909 | /{F8 00 31 C48F}には{FA}こうかがなかった!{FC} | code 00:2f6a; code 00:3063; code 24:4758 (+15 more) | script |
| 49:491C | /しかし ブレスはかききえた!{FC} | code 22:7295; code 22:77b1; $FC continuation of 49:4597 | script |
| 49:492C | /{F8 00 31 C50F}に{FA}{F8 10 04 D962}かい{FA}あたり{FA}{F8 20 04 D... | code 32:45d3; code 32:49ef; $FC continuation of 49:4597 | script |
| 49:4950 | /{F8 00 31 C48F}に{FA}{F8 10 04 D962}かい{FA}あたり{FA}{F8 20 04 D... | code 32:4e4b; code 32:531a; $FC continuation of 49:4597 | script |
| 49:4974 | /{F8 00 31 C50F}に{FA}{F8 20 04 D963}ダメージを{FA}あたえた{FC} | code 32:45ef; $FC continuation of 49:4597 | script |
| 49:498C | /{F8 00 31 C48F}に{FA}{F8 20 04 D963}ダメージを{FA}あたえた{FC} | code 32:4e6f; code 32:533e; $FC continuation of 49:4597 | script |
| 49:49A4 | /{F8 00 31 C50F}には{FA}ダメージをあたえられなかった{FC} | code 32:4638; code 32:4a54; $FC continuation of 49:4597 | script |
| 49:49BC | /{F8 00 31 C48F}には{FA}ダメージをあたえられなかった{FC} | code 32:5215; code 32:563b; $FC continuation of 49:4597 | script |
| 49:49D4 | /{F8 00 31 C50F}に{FA}さらにこうげきした{FC} | code 32:47fc; $FC continuation of 49:4597 | script |
| 49:49E6 | /{F8 00 04 DD36}は{FA}どくのダメージをうけた{FC} | code 22:65e4; code 22:6605; $FC continuation of 49:4597 | script |
| 49:49FA | /さらに こうかをはっきした{FC} | code 32:4d25; $FC continuation of 49:4597 | script |
| 49:4A09 | /DEBUG:{F8 00 31 C577}{FC} | code 24:7dbf; $FC continuation of 49:4597 | MISSING |
| 49:4A16 | /{F8 00 31 C50F}に{FA}{F8 20 04 D963}ダメージを{FA}あたえた{FC} | code 24:4c4c; code 24:6903; code 24:7523 (+3 more) | script |
| 49:4A2E | /{F8 00 31 C50F}は{FA}{F8 00 31 C577}を{FA}となえた{FC} | code 24:4252; code 24:4263; code 24:4294 (+55 more) | script |
| 49:4A42 | /{F8 00 31 C48F}に{FA}{F8 20 04 D963}ダメージを{FA}あたえた{FC} | code 24:69ad; code 24:75b3; code 24:76c2 (+1 more) | script |
| 49:4A5A | /{F8 00 31 C48F}は{FA}{F8 00 31 C54F}を{FA}つかった!{FC} | code 2e:4f6c; code 2e:5158; code 2e:5210 (+1 more) | script |
| 49:4A6F | /{F8 00 31 C48F}は{FA}すベてかいふくした{FC} | code 00:3906; $FC continuation of 49:4597 | script |
| 49:4A81 | /{F8 00 31 C48F}のHPが{FA}{F8 20 04 D963}かいふくした{FC} | code 00:3912; $FC continuation of 49:4597 | script |
| 49:4A98 | /{F8 00 31 C48F}は{FA}いやされた{FC} | code 00:38ea; $FC continuation of 49:4597 | script |
| 49:4AA6 | /{F8 00 31 C48F}は{FA}しにました | code 00:367b; code 20:44cb; $FC continuation of 49:4597 | script |
| 49:4AB4 | /{F8 00 31 C48F}は{FA}しにました{FC} | code 00:3666 | script |
| 49:4AC2 | /{F8 00 31 C48F}は{FA}はいになった!{FC} | code 00:38d2; $FC continuation of 49:4AB4 | script |
| 49:4AD2 | /{F8 00 31 C48F}を{FA}ロストした!{FC} | code 00:38de; $FC continuation of 49:4AB4 | script |
| 49:4AE1 | /{F8 00 31 C48F}は{FA}そせいした!{FC} | code 00:38c6; $FC continuation of 49:4AB4 | script |
| 49:4AF0 | /{F8 00 31 C48F}は{FA}{F8 00 31 C577}{FA}とねがった!{FC} | code 24:5b81; code 24:5b9d; code 24:5c1b (+12 more) | script |
| 49:4B05 | /{F8 00 31 C48F}は{FA}{F8 00 31 C577}で{FA}きりかかった!{FC} | code 24:6218; code 24:6309; code 24:65fc (+2 more) | script |
| 49:4B1C | /{F8 00 31 C48F}は{FA}{F8 00 31 C577}を{FA}した!{FC} | code 24:638e; code 24:646d; code 24:6561 (+1 more) | script |
| 49:4B2F | /{F8 00 31 C48F}は{FA}こうげきをみきった!{FC} | code 24:65c1; $FC continuation of 49:4AB4 | script |
| 49:4B42 | /{F8 00 31 C48F}は{FA}{F8 00 31 C577}で{FA}かくらんさせた!{FC} | code 24:668f; $FC continuation of 49:4AB4 | script |
| 49:4B5A | /{F8 00 31 C48F}は{FA}{F8 00 31 C577}を{FA}つかった!{FC} | code 24:66f4; $FC continuation of 49:4AB4 | script |
| 49:4B6F | /{F8 00 31 C48F}は{FA}{F8 00 31 C577}を{FA}はった!{FC} | code 24:6725; $FC continuation of 49:4AB4 | script |
| 49:4B83 | /{F8 00 31 C48F}は{FA}{F8 00 31 C577}を{FA}まいた!{FC} | code 24:675e; code 24:67de; $FC continuation of 49:4AB4 | script |
| 49:4B97 | /{F8 00 31 C48F}は{FA}{F8 00 31 C577}を{FA}しかけた!{FC} | code 24:68ae; $FC continuation of 49:4AB4 | script |
| 49:4BAC | /{F8 00 31 C50F}は{FA}いきたえた!{FC} | code 24:694d; $FC continuation of 49:4AB4 | script |
| 49:4BBB | /{F8 00 31 C48F}は{FA}{F8 00 31 C577}を{FA}はなった!{FC} | code 24:61bb; code 24:629b; code 24:62c6 (+3 more) | script |
| 49:4BD0 | /{F8 00 31 C50F}は{FA}{F8 00 31 C577}{FA}とねがった!{FC} | code 24:5d0b; code 24:5d2b; code 24:5dcf (+7 more) | script |
| 49:4BE5 | /{F8 00 31 C50F}は{FA}{F8 00 31 C577}で{FA}きりかかった!{FC} | code 24:622d; code 24:6246; code 24:631e (+6 more) | script |
| 49:4BFC | /{F8 00 31 C50F}は{FA}{F8 00 31 C577}を{FA}した!{FC} | code 24:6379; code 24:6408; code 24:6551 (+1 more) | script |
| 49:4C0F | /{F8 00 31 C50F}は{FA}こうげきをみきった!{FC} | code 24:65b1; code 24:65d1; $FC continuation of 49:4AB4 | script |
| 49:4C22 | /{F8 00 31 C50F}は{FA}{F8 00 31 C577}で{FA}かくらんさせた!{FC} | code 24:66a4; code 24:66bd; $FC continuation of 49:4AB4 | script |
| 49:4C3A | /{F8 00 31 C50F}は{FA}{F8 00 31 C577}を{FA}つかった!{FC} | code 24:66e4; code 24:6704; $FC continuation of 49:4AB4 | script |
| 49:4C4F | /{F8 00 31 C50F}は{FA}{F8 00 31 C577}を{FA}しかけた!{FC} | code 24:677e; code 24:679f; code 24:67fe (+4 more) | script |
| 49:4C64 | /{F8 00 31 C50F}は{FA}{F8 00 31 C577}を{FA}まいた!{FC} | $FC continuation of 49:4AB4 | script |
| 49:4C78 | /{F8 00 31 C48F}は{FA}いきたえた!{FC} | code 24:69f6; $FC continuation of 49:4AB4 | script |
| 49:4C87 | /{F8 00 31 C50F}は{FA}{F8 00 31 C577}を{FA}はなった!{FC} | code 24:61ab; code 24:61cb; code 24:628b (+6 more) | script |
| 49:4C9C | /{F8 00 31 C48F}のACが{FA}さがった!→デバッグ┌{FC} | $FC continuation of 49:4AB4 | MISSING |
| 49:4CB3 | /{F8 00 31 C50F}のACが{FA}さがった!→デバッグ┌{FC} | $FC continuation of 49:4AB4 | MISSING |
| 49:4CCA | /{F8 00 31 C48F}の{FA}T→D┌{FA}D→U┌!→デバッグ┌{FC} | $FC continuation of 49:4AB4 | MISSING |
| 49:4CE3 | /{F8 00 31 C50F}の{FA}T→D┌{FA}D→U┌!→デバッグ┌{FC} | $FC continuation of 49:4AB4 | MISSING |
| 49:4CFC | /MAGIC OK!→デバッグ┌{FC} | $FC continuation of 49:4AB4 | MISSING |
| 49:4D0D | {F5}{F4 00 00}/なにを ねがいますか?/{FC} | code 24:518f; $FC continuation of 49:4AB4 | script |
| 49:4D1F | /かみがみはねがいを ききいれなかった{FC} | code 24:5364; $FC continuation of 49:4AB4 | script |
| 49:4D33 | {F5}{F4 00 00}/ねがいは かなえられた{FC} | code 24:5375; code 24:5383; $FC continuation of 49:4AB4 | script |
| 49:4D44 | /   まほうからのほご{FC} | table 24:50DE[0] (24:51A8/51BE/51D4); $FC continuation of 49:4AB4 | script |
| 49:4D51 | /   まりょくのかいふく{FC} | table 24:50DE[1] (24:51A8/51BE/51D4); $FC continuation of 49:4AB4 | script |
| 49:4D5F | /   ふっかつとちりょう{FC} | table 24:50DE[2] (24:51A8/51BE/51D4); $FC continuation of 49:4AB4 | script |
| 49:4D6D | /   うしなったレベルのかいふく{FC} | table 24:50DE[3] (24:51A8/51BE/51D4); $FC continuation of 49:4AB4 | script |
| 49:4D7F | /   まものをけしさる{FC} | table 24:50DE[4] (24:51A8/51BE/51D4); $FC continuation of 49:4AB4 | script |
| 49:4D8C | /   ぼうぎょりょくをたかめる{FC} | table 24:50DE[5] (24:51A8/51BE/51D4); $FC continuation of 49:4AB4 | script |
| 49:4D9D | /   まもののちからをふうじる{FC} | table 24:50DE[6] (24:51A8/51BE/51D4); $FC continuation of 49:4AB4 | script |
| 49:4DAE | /   まちヘテレポートする{FC} | $FC continuation of 49:4AB4 | script |
| 49:4DBD | /{F8 00 31 C48F}は{FA}まほうをはじいた!{FC} | code 00:32ee; $FC continuation of 49:4AB4 | script |
| 49:4DCF | /{F8 00 31 C50F}は{FA}まほうをはじいた!{FC} | code 24:6c22; $FC continuation of 49:4AB4 | script |
| 49:4DE1 | /{F8 00 31 C48F}の{FA}{F8 00 31 C577}は{FA}こうかを{FA}はっきできなかった{F... | code 24:410e; code 2e:4dce; code 2e:4fa6 (+1 more) | script |
| 49:4DFF | /{F8 00 31 C50F}の{FA}{F8 00 31 C577}は{FA}こうかを{FA}はっきできなかった{F... | code 24:40f8; code 2e:4db8; $FC continuation of 49:4AB4 | script |
| 49:4E1D | /{F8 00 31 C48F}は{FA}{F8 10 04 D060}たいの{FA}{F8 00 31 C50F}を{... | code 24:6b23; $FC continuation of 49:4AB4 | script |
| 49:4E3D | /{F8 00 31 C48F}は{FA}しょうかんにしっぱいした{FC} | code 24:6b7c; $FC continuation of 49:4AB4 | script |
| 49:4E52 | /{F8 00 31 C48F}は{FA}{F8 00 31 C50F}を{FA}もとのせかいにかえした{FC} | code 22:6eab; $FC continuation of 49:4AB4 | script |
| 49:4E6D | /{F8 00 31 C48F}は{FA}{F8 10 04 D962}たいの{FA}のろいをといた{FC} | code 22:6f47; $FC continuation of 49:4AB4 | script |
| 49:4E86 | /{F8 00 31 C48F}は{FA}{F8 00 31 C50F}の{FA}のろいをとこうとしたがしっぱいした{F... | code 22:6f57; $FC continuation of 49:4AB4 | script |
| 49:4EA7 | /{F8 00 31 C48F}は{FA}{F8 00 31 C54F}を{FA}なげた!{FC} | code 22:703a; $FC continuation of 49:4AB4 | script |
| 49:4EBB | /{F8 00 31 C48F}は{FA}そうびをかえた!{FC} | code 22:6fa3; $FC continuation of 49:4AB4 | script |
| 49:4ECC | /{F8 00 31 C48F}は{FA}のろわれた!{FC} | code 22:700b; $FC continuation of 49:4AB4 | script |
| 49:4EDB | たたかう/まえにもどる | code 22:5ee8; $FC continuation of 49:4AB4 | script |
| 49:4EE7 | どのモンスターと たたかいますか? | code 22:4d4a | script |
| 49:4EF9 | どのモンスターに となえますか? | code 22:4e3a; code 22:4e9c | script |
| 49:4F0A | だれに じゅもんをとなえますか? | code 22:5e5b | script |
| 49:4F1B | どのアイテムを なげますか? | code 22:4ff8 | script |
| 49:4F2A | どのモンスターに なげますか? | code 22:508e | script |
| 49:4F3A | どのアイテムを つかいますか? | code 22:50d6 | script |
| 49:4F4A | どのモンスターに つかいますか? | code 22:519b | script |
| 49:4F6C | じぶんのばんが まわってきたときに/していしたそうびに へんこうします | code 22:5213 | script |
| 49:4F90 | にげられない! | code 22:488c | script |
| 49:4F98 | {F8 00 04 D000}{F4 0C FF}→{F8 91 04 D061}┌{F8 91 04 D060} | code 32:4219 | MISSING |
| 49:51C9 | /いきのこったメンバーは それぞれ/{F8 30 31 C65D}の けいけんちをえた{FC} | code 25:4777 | script |
| 49:51EB | /いきのこったメンバーは それぞれ/{F8 30 31 C65D}ゴールドを てにいれた{FC} | code 25:527d; $FC continuation of 49:51C9 | script |
| 49:520E | かわの ふくろだ!□せいどうの たからばこだ!□どうの たからばこだ!□ぎんの たからばこだ!□きんの たからばこだ!□... | $FC continuation of 49:51C9 | MISSING |
| 49:5289 |   {F3 31 C6E5}/  どうしますか?/    しらベる/    じゅもんをとなえる/    わなをはずす/ ... | code 25:47e1 | script |
| 49:52D1 | だれが しらベますか? | code 25:481c | script |
| 49:52DD | だれが じゅもんを となえますか? | code 25:4967 | script |
| 49:52EF | だれが わなを はずしますか? | code 25:4a8a | script |
| 49:52FF | だれが あけますか? | code 25:4c77 | script |
| 49:537A |   わなは?//     ファイアーボルト/     ばくだん/     マジックドレイン/     エナジードレイン/... | code 25:4ad7 | script |
| 49:542C | /わなを はずした{FC} | code 25:4c67 | script |
| 49:5436 | /わなを はずせなかった{FC} | code 25:4c43; $FC continuation of 49:542C | script |
| 49:5443 | /おおっと! {F3 31 C6E3}{FC} | code 25:4ce6; $FC continuation of 49:542C | script |
| 49:544F | /わなは かかっていなかった{FC} | code 25:4cb3; $FC continuation of 49:542C | script |
| 49:545E | /わなは さどうしなかった{FC} | code 25:4d09; $FC continuation of 49:542C | script |
| 49:546C | /{F8 00 31 C48F}は{FA}{F3 31 C6E3}を{FA}ひろった{FC} | code 25:520b; $FC continuation of 49:542C | script |
| 49:547F | //したいのなかに なにかがみえる/{F8 00 31 C48F}は{FA}{F3 31 C6E3}を{FA}ひろった{... | code 25:52e1; $FC continuation of 49:542C | script |
| 49:54A3 | /{F8 00 31 C48F}は{FA}{F8 20 04 D963}ダメージを{FA}うけた{FC} | code 25:4d4e; code 25:4dd1; $FC continuation of 49:542C | script |
| 49:54BA | /{F8 00 31 C48F}は{FA}じゅもんのちからを{FA}すいとられた{FC} | code 25:4e19; $FC continuation of 49:542C | script |
| 49:54D3 | /{F8 00 31 C48F}は{FA}けいけんちを{FA}すいとられた{FC} | code 25:4e5a; $FC continuation of 49:542C | script |
| 49:54E9 | /{F8 00 31 C48F}は{FA}{F8 00 31 C54F}を{FA}うしなった{FC} | code 25:4f3c; $FC continuation of 49:542C | script |
| 49:54FE | あくま□ガイコツ□ガスじょうのもの□きみょうなもの□きょだいなもの□ケモノ□ちいさなすがた□ちをはうもの□つち□つばさを... | $FC continuation of 49:542C | MISSING |
| 49:556D |    ゆうこうてきな//{F8 00 04 DD36}//     たたかう/     たちさる | code 32:406a | script |
| 49:5594 | {F8 00 31 C48F}のせいかくがかわった{FC} | code 32:4181; code 32:41d1 | script |
| 49:55A4 | モンスターは/  とつぜん おそいかかってきた | code 22:4617; $FC continuation of 49:5594 | MISSING |
| 49:55BC | モンスターは/  まだ こちらに きづいていない | code 22:4625 | script |
