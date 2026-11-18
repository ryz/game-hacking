# Deep Dungeon III - combat and characters

## Overview
Battles are random (and fixed on some squares, [maps.md](maps.md) section 7). The party first chooses to fight or
run, then gives each member an order; the round then plays out as scrolling text **(verified: shots
`battle_skeletons`, `battle_commands`, `battle_round`)**. Winning gives gold and the same EX to every member; a
level-up hands out bonus points to spend on stats **(verified)**. When the swordsman dies the game is over, even if
the others live **(verified: shot `gameover_swordsman`)**.

## 1. Battle flow
1. "X appeared!" with the monster group and count; first menu たたかう (fight) / にげる (run) **(verified)**.
2. Per member: たたかう fight, じゅもん spell, みをまもる defend, どうぐ item, にげる run; fight and spells pick a target
   among the monster pictures (highlighted) **(verified: shots `battle_target`, `battle_spell_select`)**.
3. The round: attacks, misses ("dodged nimbly"), spells ("cast the Spear spell"), kills ("defeated") **(verified)**.
4. Victory: "N gold obtained", "each got N EX" **(verified: shot `battle_victory`: three skeletons gave 42 gold and 6 EX
   each)**.
5. Level-up messages after the fight, then a status page per character with bonus points (section 3).

## 2. Damage seen
| Situation | Result | Source |
|---|---|---|
| skeleton (がいこつ) hits the level-5 swordsman, no armour | 28 HP | verified (shot `battle_round`) |
| skeleton hits the level-1 swordsman (15 HP) | dead in the first round | verified (shot `gameover_swordsman`) |
| Spear cast by a level-5 magician on a skeleton | kills it; costs 2 MP | verified (MP 25 -> 23) |
| pit trap on underground floor 2 | 22 HP to the priest | verified (shot `ev_pit_trap`) |

## 3. Characters and levels
| Stat | Meaning (in-game abbreviation) | How sure |
|---|---|---|
| LEVEL, EX | level and experience; the status page shows EX still needed | verified (shot `status_ryz`) |
| MAX-HP, MAX-MP | hit points, magic points | verified |
| AC | armour class | verified |
| AP | attack power (equal to ST without a weapon) | verified (ST 8 / AP 8) |
| ST, AG, LK | strength, agility, luck | verified |
Experience needed: 10 EX for level 2; 500 EX for level 6 **(verified on the status page)**.
Level-up: "LEVEL went up", then the status page: "you have N bonus points; press Start when done"; A adds a point to
the stat under the cursor (ST, AG, LK) **(verified: shots `level_up`, `level_up_points`)**. One example, the
swordsman from level 5 to 6: MAX-HP 58 -> 73, MAX-MP 8 -> 11, AC 3 -> 5, ST 14 -> 22, AG 10 -> 16, LK 5 -> 7, plus
2 bonus points **(RAM: level-5 values were set by hand, so the jump may include a recalculation)**.
Starting characters (level 1): swordsman HP 15 MP 3 (AC 2 AP 8 ST 8 AG 6 LK 2), hunter HP 12 MP 4, priest HP 9 MP 6,
magician HP 6 MP 8 **(verified)**.

## 4. Companions
Pre-made characters wait in the dungeons ("someone is here! What will you do?"); talking (はなす) to them makes them
ask to join. With a full party: "the party is full - part with someone in town and come back" **(verified)**. The
priest Birman (ビルマン) on cave floor 2 joins at level 15 with 135 HP and 90 MP **(verified: shot
`companion_joins`, party of three made by hand)**.

## 5. Game over
"The swordsman ran out of strength. The party lost its purpose" -> a menu: きろくしたところからはじめる (restart from the
last record) / ぼうけんをやめる (quit) **(verified: shots `gameover_swordsman`, `gameover_menu`)**.

## Open questions
- Spell lists and costs per class; what みをまもる (defend) changes (the swordsman took no damage the round he
  defended, one sample).
- Monster stats, gold and EX tables (in the ROM, not decoded).
