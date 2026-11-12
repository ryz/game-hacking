# Attack verbs (49:56AF, `{F3 31 C6E3}`): which battle template prints each one

Original ROM, Japanese Rev 1. The tracer wrote this on 2026-11-12 and did not patch anything.
Scratch files are in `work/re/verbs/`: `classify.py` (static classification), `classify.txt`, `monsters.txt`, and `dyn.py` (dynamic check).

## 1. Answer
The template is chosen by the **verb index**, not by the caller. Every site that reads a verb uses the same
index `A` for two things: `0:0EDF` with `HL=$56AF` (verb pointer -> `$C6E3`) and a 42-entry template table in bank 50.
- Party member attacks (`{A}`=`$C48F` is the subject): `32:58D6`, which holds 45E0 (に) / 45F4 (を) / 4608 (の) / 461C (no target).
- Monster attacks (`{B}`=`$C50F` is the subject): `32:59CE`, which holds the mirror templates 4597 (に) / 45AB (を) / 45BF (の) / 45D3 (no target).

The two tables agree entry by entry. So each verb is either always "target" or always "no target", whoever attacks.
The breath path `22:7121` is the only exception to the table lookup. It always uses 45D3, with index `[$C542]+15`
(the monster's breath type), which gives verbs 15-20.
The dispatch listed only the party-side target templates (45E0/45F4/4608). The monster-side ones are 4597/45AB/45BF.
In the current EN script all six target templates read `{subj} {verb} {obj}!` and both no-target templates read `{subj} {verb}!`.

**No-target verbs: 13, 14, 15-20 (breaths), 33 (called for help), 34 (spat fluid), 36 (fled), 37 (panicked).** All the others take a target.
The editor was right about 0x5187, 0x51A0 and 0x51A4, which are no-target. The editor was wrong about 0x518F
"spat fluid", which is no-target too and so is correct as it is.
The breath verbs ("breathed fire at" and the others) are a **live bug**: they print as "X breathed fire at!".
Eight verbs (13, 14, 29, 30, 31, 33, 36, 37) cannot be reached by any code path in Rev 1, so they are dead strings.

## 2. Table
"Template" means party-side/monster-side. Reach shows which code can pick the verb: P = party lists `32:5845`,
M = monster lists `32:5958` restricted to `$C539` values real monsters have, and B = breath `22:7121`.

| # | ptr | JP | current EN | template | reach | EN verdict |
|---|---|---|---|---|---|---|
| 0 | 503d | なぐりかかった | swung at | 45E0/4597 target | P,M | ok |
| 1 | 5045 | たたきつけようとした | tried to bash | 45F4/45AB target | P,M | ok |
| 2 | 5050 | ふみつけようとした | tried to trample | 45F4/45AB target | M | ok |
| 3 | 505a | しめあげようとした | tried to crush | 45F4/45AB target | P,M | ok |
| 4 | 5064 | なげつけようとした | tried to throw | 45F4/45AB target | M | ok |
| 5 | 506e | わしづかみにしようとした | tried to grab | 45F4/45AB target | P,M | ok |
| 6 | 507b | あばれかかった | lashed out at | 45E0/4597 target | P,M | ok |
| 7 | 5083 | たいあたりしようとした | tried to ram | 45E0/4597 target | P,M | ok |
| 8 | 508f | まきつこうとした | tried to coil around | 45E0/4597 target | M | ok |
| 9 | 5098 | かみつこうとした | tried to bite | 45E0/4597 target | M | ok |
| 10 | 50a1 | とびかかった | leapt at | 45E0/4597 target | P,M | ok |
| 11 | 50a8 | ちをすおうとした | tried to drink the blood of | 4608/45BF target (の) | M (vampires) | ok |
| 12 | 50b1 | からみつこうとした | tried to entangle | 45E0/4597 target | M | ok |
| 13 | 50bb | おそろしいこえでさけんだ | let out a terrible cry at | 461C/45D3 **no target** | none (dead) | drop "at" |
| 14 | 50c8 | うつくしいこえをかなでた | sang beautifully to | 461C/45D3 **no target** | none (dead) | drop "to" |
| 15 | 50d5 | ほのおのブレスをはいた | breathed fire at | 461C/45D3 **no target** | B (45D3 fixed) | **bug**: drop "at" |
| 16 | 50e1 | れいきのブレスをはいた | breathed frost at | same | B | **bug** |
| 17 | 50ed | どくのブレスをはいた | breathed poison at | same | B | **bug** |
| 18 | 50f8 | でんげきのブレスをはいた | breathed lightning at | same | B | **bug** |
| 19 | 5105 | さんのブレスをはいた | breathed acid at | same | B | **bug** |
| 20 | 5110 | せきかブレスをはいた | breathed stone breath at | same | B | **bug** (e.g. "breathed petrifying breath") |
| 21 | 511b | ふりおろした | struck down at | 45E0/4597 target | P,M | ok |
| 22 | 5122 | きりさこうとした | tried to slash | 45F4/45AB target | P,M | ok |
| 23 | 512b | つきさそうとした | tried to stab | 45F4/45AB target | P,M | ok |
| 24 | 5134 | なぎはらおうとした | tried to mow down | 45F4/45AB target | P,M | ok |
| 25 | 513e | きりきざもうとした | tried to cut up | 45F4/45AB target | P,M | ok |
| 26 | 5148 | やつざきにしようとした | tried to tear apart | 45F4/45AB target | P,M | ok |
| 27 | 5154 | やをはなった | shot an arrow at | 45E0/4597 target | P,M | ok |
| 28 | 515b | とりつこうとした | tried to possess | 45E0/4597 target | M | ok |
| 29 | 5164 | ムチをふるった | lashed a whip at | 45E0/4597 target | none (dead) | ok |
| 30 | 516c | ハリをとばした | shot needles at | 45E0/4597 target | none (dead) | ok |
| 31 | 5174 | トゲをとばした | shot spines at | 45E0/4597 target | none (dead) | ok |
| 32 | 517c | しょくしゅをふるった | lashed tentacles at | 45E0/4597 target | M | ok |
| 33 | 5187 | なかまをよんだ | called for help against | 461C/45D3 **no target** | none (dead) | "called for help" |
| 34 | 518f | たいえきをとばした | spat fluid | 461C/45D3 **no target** | M (Ghoul, Mummy, Zombie, Spider Queen...) | ok as is |
| 35 | 5199 | ゆうわくした | tried to seduce | 45F4/45AB target | M | ok |
| 36 | 51a0 | にげた | fled from | 461C/45D3 **no target** | none (dead) | "fled" |
| 37 | 51a4 | あわてた | panicked before | 461C/45D3 **no target** | none (dead) | "panicked" |
| 38 | 51a9 | いしをなげつけた | threw a stone at | 45E0/4597 target | P (list 12) | ok |
| 39 | 51b2 | うちぬこうとした | tried to shoot | 45F4/45AB target | P,M | ok |
| 40 | 51bb | きりかかった | slashed at | 45E0/4597 target | P,M | ok |
| 41 | 51c2 | つきかかった | thrust at | 45E0/4597 target | P,M | ok |

## 3. Evidence
- All five readers of the verb table (`21 AF 56` with `CD DF 0E`, then a store to `$C6E3`) were found by a full-ROM search.
  The other 18 writers of `$C6E3` use other tables (`49:5703`, `567D`, `5661`, `409C`...).
  - `32:43C4` (party; A=0..14 from 43AF..43AB) and `32:4850` (party; A=0..15 from the item type `$C561/$C560`):
    `HL=32:5845[A]` -> list `[count][idx...]`. `0:0DC0` picks a random 0..count-1, which gives the verb index.
    That index is `push af`ed, used to index `32:58D6`, and the result is written to `$C1BF/C0`.
    Then `pop af`, `ld b,$31 / ld hl,$56AF / call 0EDF`, which stores the verb pointer in `$C6E3`.
  - `32:4D55` (via `32:4D64`) and `32:5223` (via `32:5240`) (monster; A=`$C539` = monster record +$2A, 0..58):
    the same pattern with lists `32:5958` and templates `32:59CE`.
    These are entered from `22:737D`/`22:73BE`/`22:73F4` and `24:785E`/`24:78AC`.
  - `22:7119`: reached when the monster action byte is >=5 and <$80. It loads A=`[$C542]`+$0F (monster record +$33,
    which is 0..5 in the data) and sets `$C1BF/C0=$45D3` directly.
- The list contents are in `work/re/verbs/classify.txt`. Some counts read one byte past the list
  (`5A22` count 10 reads the next count byte 8, and `5A3C`, `5AA0`, `5B20` do the same). I used the indices as the code reads them.
- No JP/JR/CALL enters these paths between the list pick and `ld hl,$56AF` (scan of abs and rel jumps). So no
  other index can reach the verb table, and 13, 14, 29-31, 33, 36 and 37 are unreachable.
  The real "called for help" line is the separate segment `49:4871`.
- The EN build (0935c1d) has the same bytes as JP in `32:4380-4410`, `4800-4890`, `4D55-4DB0`, `5223-5290`, `5845-5B85` and
  `22:70FE-7140`. Only the verb pointers (`49:56AF`) and the template texts were repointed, so the logic is unchanged.
- Dynamic check (JP ROM): `work/re/verbs/dyn.py rom/wizardry_empire_j.gbc work/re/battle-text/battle_start_jp.state 150`.
  The inputs are 150 x (A held 8 frames, then 40 frames released), with breakpoints on the 5 sites. The hits were:
  - `32:43F0`: A=1 -> 45F4, A=21 -> 45E0, A=0 -> 45E0, A=22 -> 45F4, A=24 -> 45F4
  - `32:4D93`: A=12 -> 4597, A=34 -> **45D3**, A=10 -> 4597, A=28 -> 4597

  Every hit matched the tables. Spat fluid was seen to use the no-target template.
  `22:7121` did not fire (no breath in that fight).

## 4. Hook proposal
No code is needed. Fix the strings in `script/lists.json` only: indices 15-20 (live) and 13, 14, 33, 36, 37 (dead, for consistency).
If the templates must not change, every verb has to keep the grammar of its template class.

## 5. Open
- I did not confirm the breath path dynamically. It is static only, but the template is a constant `$45D3` at `22:712F`.
- I did not trace which monsters actually take the breath action (action byte >=5). Fire (index 15) needs breath type 0.
- I did not check whether `$C539` could hold values from outside the monster records (summons, for example).
