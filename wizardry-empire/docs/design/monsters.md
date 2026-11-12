# Monsters: the bestiary, encounters, group formation, monster actions

What a monster is, which monsters exist, when and how a fight starts, and how a monster chooses what to do each
round. The full stat list of all 167 monsters and every encounter table is in
**[monsters_table.md](monsters_table.md)** (generated from the game data). How hits, damage, saves, spells, escape
and rewards are resolved is in [combat.md](combat.md). Notation and tags: [README.md](README.md#notation-and-style-binding-for-every-design-document).

---

## Overview

- **167 monsters**, each with fixed stats. Nothing about a monster is random except its HP, which is rolled per
  monster when the battle starts. There are no elite or scaled variants: a Goblin is always level 2 with AC 6.
- **Levels 1 to 30.** About half the bestiary is level 1-10, and only 5 monsters are above level 25 (computed from
  monsters_table.md).
- **A monster is a short list of numbers:** level, HP dice, AC, a to-hit value, swings per round and damage dice per
  swing, a reach (melee, reach or ranged), 8 elemental resistances, a type (undead, demon, dragon, spirit), up to six
  spell schools, special hits (poison, fear, sleep, paralysis, stone, decapitation, level drain), breath, how likely
  it is to call for help or flee, its EXP and gold, and a chest rating.
- **Random fights are rare in corridors and common at doors.** After every action in the maze (a step or a turn) the
  game rolls for a fight. The normal chance is **1 in 512 per action** (verified). Right after the party walks
  through a door it is **13 in 256, about 5.1%, per action**, until the next plain step or turn-around. The rates are
  the same on every floor.
- **Guarded squares** are fixed fights: 244 in the maze, from none (floor 20) to 21 (floor 4) per floor. Each fights
  once per floor visit and comes back when the party changes floors. They are the only fights that give a chest.
- **A fight** is one of 4 formations listed for the square's encounter area, picked at random. A formation has up
  to 4 groups of 1 to 9 monsters each.
- **Monster actions** follow a fixed priority list: a spellcaster casts 25% of the time; otherwise the monster may
  call for help, flee or breathe, and attacks if none of these fires.

---

## 1. What a monster is

Every monster has the stats below. The column names are those of [monsters_table.md](monsters_table.md).

| Stat (table column) | What it means in play |
|---|---|
| **Level** (Lv) | 1 to 30. Used against the party's weapon status effects, against Hide, and in some spell checks ([combat.md](combat.md#6-weapon-status-effects-on-monsters)). It does **not** enter the save against the monster's own special hits: that save uses the struck character's level ([combat.md](combat.md#9-special-hits-and-saves)). |
| **HP** | Dice rolled for each monster when the battle starts, written `NdS+B` (Goblin 1d7, 1 to 7). Every monster has at least 1 HP; see [findings.md](findings.md#a-monster-with-minimum-hp-0-would-hang-the-game). |
| **AC** | Armor class, lower is better: from 10 (Mudman) down to −30 (Abyss Lurker) (computed from monsters_table.md). The party's to-hit roll is made against it ([combat.md](combat.md#3-party-attacks-to-hit)). |
| **To-hit** (Hit) | How hard it is for this monster to hit; **lower is more accurate**. From 1 (Ancient One and the other top monsters) to 19 (Goblin, Orc). Same rule as the party's: [combat.md](combat.md#7-monster-attacks-to-hit-and-damage). |
| **Swings** | How many swings the monster makes when it attacks: 1 to 14, with no cap. 77 monsters swing once; the most are Musashi 14, Kamui 10, Kali, Scylla and Carrion Worm 8. |
| **Damage per swing** (Dmg) | Dice in the same `NdS+B` form, rolled per hit (Goblin 1d7, Musashi 2d8+14). |
| **Reach** | 0 melee, 1 reach, 2 or 3 ranged: decides which party members it can attack and from which rank ([combat.md](combat.md#8-monster-reach-and-targets)). Reach 2 and 3 pick targets alike. |
| **Resistances** (Resistance %) | 8 values, one per element: Earth, Water, Fire, Wind, Spirit, the 6th element, Holy, None (the museum's order). 0 = no resistance, 100 = immune. A spell loses this much of its chance ([combat.md](combat.md#11-spells-against-monsters)); Earth and Spirit at 100% also block the party's weapon status effects. |
| **Type** | Undead, demon, dragon, spirit: what slaying weapons check ([combat.md](combat.md#5-slaying-weapons-and-other-weapon-properties)). Two more marks exist, the **golem mark** and the **ghost mark**; their effect was not traced. The game also reads the type in its spell rules; what for was not traced. |
| **Spell schools** (Spells) | Up to 6 schools, each with the highest spell level (1 to 7) the monster can cast: Mage, Priest, and four more that are probably Valiant, Avenger, Musashi and Kunoichi (inferred; marked * in the table). A spellcaster gets 9 casts at each spell level for the battle. |
| **Special hits** | Poison, fear, sleep, paralysis, stone, decapitation, each tried after a successful hit; level drain (how many levels per hit). The struck character gets a save ([combat.md](combat.md#9-special-hits-and-saves)). |
| **Breath** | Whether it can breathe, and what: fire, frost, poison, lightning, acid or stone ([combat.md](combat.md#10-breath)). |
| **Call for help** | Whether it can call for help, and how strongly: 25% or 65% per turn ([section 6](#6-monster-actions)). |
| **Flee value** F | 0 = never flees. Otherwise the monster flees with F × 5% per turn (10% for F = 2, the value of 19 of the 26 monsters that flee; computed from monsters_table.md). |
| **Escape block** (Esc) | Subtracted from the party's chance to run away; the highest value among the groups counts. 2 to 18 (computed from monsters_table.md). See [combat.md](combat.md#14-escape). |
| **EXP, Gold** | Paid per monster killed: EXP 30 (Crawling Claw) to 150,000 (Abyss Lurker), gold 20 G to 250 G. |
| **Chest rating** (Chest) | The highest chest rating among the groups decides how good a guarded square's chest can be: the chest value is rolled from it, and the value gives the chest's tier ([dungeon.md](dungeon.md)). 1 to 47 in the bestiary. |
| **Unidentified name** | While a group is unidentified the battle shows one of 16 generic names instead of the real one. |
| **Attack words** | Which set of attack words the battle text uses. |

Example: the Goblin row of [monsters_table.md](monsters_table.md).

| # | English | Japanese | Lv | HP | AC | Hit | Swings | Dmg | Reach | Esc | Type | Spells | Special hits | Resistance % | EXP | Gold | Chest | Floors | G | Enc |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 52 | Goblin | ゴブリン | 2 | 1-7 (1d7) | 6 | 19 | 1 | 1-7 (1d7) | 0 | 10 | - | - | call 25%, flee 10% | - | 290 | 30 | 1 | 1-2,5 | 1-2,5 | 3-4,7,54,56 |

Read: a level-2 melee monster with 1d7 HP and AC 6 and the least accurate to-hit (19), one swing of 1d7 damage,
calls for help 25% of its turns and flees 10%, worth 290 EXP and 30 G, found on floors 1-2 and 5.

**Notes:** something in battle (not traced) can switch off a monster's special hits. Several stats are 0 in every
monster or never used; see [findings.md](findings.md#unused-fields-in-the-monster-records).

Tech: [monsters.md §1](../tech/monsters.md#1-the-monster-record)

---

## 2. The bestiary

The 167 monsters span levels 1 to 30. Counts below are computed from [monsters_table.md](monsters_table.md).

| Levels | 1-5 | 6-10 | 11-15 | 16-20 | 21-25 | 26-30 |
|---|---|---|---|---|---|---|
| Monsters | 34 | 43 | 41 | 26 | 18 | 5 |

**Families by type** (computed):

| Type | Count | Members |
|---|---|---|
| Undead | 26 | Skeleton, Skeleton Warrior, Zombie, Zombie Lord, Giant Zombie, Ghoul, Ghast, Wight, Mummy, Vampire, Vampire Lord, Vampire Queen, Lich, Death Knight, Dullahan, Nightmare, Night Rider, Nightcrawler, Damned, Dragon Zombie, Undead Beholder, Creeping Coin, Banshee, Ghost, Gas Cloud, Specter |
| Demon | 10 | Lesser Demon, Hell Fiend, Greater Demon, Balrog, Hell Master, Arch Demon, Demon Lord, Demon King, Demon Queen, and the final boss Demon Adish |
| Dragon | 3 | Shadow Dragon, Deep Dragon, Mist Dragon (level 21-22, floors 18-19) |
| Spirit | 11 | Dryad, Treant, the Air, Earth, Water and Fire Elementals, Djinni, Dao, Marid, Ifrit, Rakshasa |
| golem mark (effect not traced) | 7 | Stone Golem, Iron Golem, Doll Golem, Glass Golem, Juggernaut, Kugutsu, Gargoyle |
| ghost mark (effect not traced) | 13 | Banshee, Ghost, Gas Cloud, Specter, Undead Beholder, Air and Fire Elementals, Djinni, Phoenix, Beholder, Couatl, Eye Wing, Gargoyle |
| No type | 106 | humans and humanoids, beasts, giants, the "ancient" monsters |

A monster can carry more than one type (a Ghost is undead and has the ghost mark).

**What monsters do besides hitting** (computed): 68 cast spells (51 Mage, 34 Priest, and one each of the four
special schools), 20 breathe, 31 call for help (only the Creeping Coin at 65%), 26 can flee. Special hits: level
drain 15, paralysis 14, poison 11, fear 11, decapitation 9, stone 8, sleep 3. Reach: 102 melee, 45 reach, 20 ranged
(6 with Reach 2, 14 with Reach 3).

**Notable monsters** (selected columns of [monsters_table.md](monsters_table.md)):

| # | English | Japanese | Lv | HP | AC | Hit | Swings | Dmg | Reach | Spells | Special hits | Resistance % | EXP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 130 | CrawlingClaw | クラウリングクロウ | 1 | 1-6 (1d6) | 8 | 19 | 1 | 1-4 (1d4) | 0 | - | - | 0/0/0/0/100/0/0/0 | 30 |
| 115 | CreepingCoin | クリーピングコイン | 1 | 1 | 7 | 19 | 1 | 1-2 (1d2) | 0 | - | breath(lightning), call 65% | 95/100/95/95/100/95/80/95 | 260 |
| 42 | Wight | ワイト | 6 | 9-37 (4d8+5) | 8 | 15 | 1 | 1-5 (1d5) | 0 | - | drain 1 | 0/100/0/0/100/0/0/0 | 220 |
| 8 | Bowman | ボウマン | 5 | 5-30 (5d6) | 7 | 15 | 2 | 3-27 (3d9) | 2 | - | call 25%, flee 10% | - | 550 |
| 24 | Vampire | ヴァンパイア | 10 | 15-85 (10d8+5) | 1 | 12 | 1 | 6-18 (2d7+4) | 0 | - | paralyze, drain 1 | 20/60/20/60/100/50/5/20 | 1000 |
| 152 | Musashi | ムサシ | 20 | 36-288 (36d8) | -10 | 2 | 14 | 16-30 (2d8+14) | 0 | Musashi* 7 | - | - | 44050 |
| 7 | Abyss Lurker | しんえんよりのもの | 30 | 255-2295 (255d9) | -30 | 1 | 2 | 34-226 (24d9+10) | 3 | Mage 7 Priest 7 | fear, sleep, paralyze | 100/100/100/100/100/100/100/100 | 150000 |

- **Crawling Claw** is the weakest monster (30 EXP). **Creeping Coin** has a single HP but breathes lightning,
  calls for help 65% of its turns, resists most elements, and has its own event fight (area 34).
- **Level drain comes early:** the Wight drains 1 level from floor 5 on, the Specter from floor 8, the Vampire on
  floors 9-10 (also 27 and 29).
- **Bowman, Shooter, Gunner, Sagittarius** are the archer line: ranged, so they hit any party member from any
  rank.
- **Musashi, Kamui, Kali, Scylla, Carrion Worm** have the most swings (8 to 14 per attack).
- **Abyss Lurker** is the strongest: level 30, up to 2295 HP, AC −30, Mage 7 and Priest 7, 100% resistance in
  every element, so no spell that checks resistance affects it ([combat.md](combat.md#11-spells-against-monsters)).
- **Event-only monsters** (no floor in the table; they appear only in event fights): Ancient One, Fair Fiend,
  Godslayer, Rift Walker, Abyss Lurker, Demon King, Demon Queen, Demon Adish, Kamui, Alien.
- **Floors 21-30** are where most level 20-30 monsters live: the "ancient" ones (From Beyond, Unspeakable, Star
  Seizer), the high demons and vampires, and the special-class fighters (Valiant, Avenger, Musashi, Kunoichi).

**Notes:** several monsters share their name with a Summoner spell (Ifrit, Lion of Hell, Ancient One...). A pact at
a magic circle teaches the spell of that name; it does not involve the monster of the bestiary
([spells.md](spells.md#6-summoner-pacts)).

Tech: [monsters.md overview](../tech/monsters.md#overview-two-minute-read), [monsters.md §1](../tech/monsters.md#1-the-monster-record), [monsters.md §8](../tech/monsters.md#8-summoner-pacts)

---

## 3. When a fight starts

The player sees fights mostly on stepping through a door; a long corridor walk rarely triggers one.

After **every action** in the maze (a step, a left or right turn, a turn-around) the game rolls for a random fight:

| Situation | Chance per action | Average actions until a fight (computed: 1 / chance) |
|---|---|---|
| Normal | 1 in 512, about 0.2% (verified) | 512 |
| Right after walking through a door | 13 in 256, about 5.1% | about 20 |

- The "after a door" state starts with the door step and lasts until the next **plain step** or **turn-around**.
  Left and right turns do not end it, so turning in place after a door keeps rolling at 5.1%.
- There is no step counter and no depth modifier: the rate is the same on floor 1 and floor 30.
- A fight only happens on a square that has an **encounter area**. Squares with no area (rock, and some corridors on
  floors 2, 9, 13, 17, 19, 21, 22 and 25) never have random fights.

The 1-in-512 rate was checked in play: a walk of 357 actions gave one fight, which fits (a small sample). The door
rate was not measured.

**Notes:** the corridor rate is very low and doors raise it 26-fold (computed: 13/256 against 1/512); whether that
is intended is discussed in [findings.md](findings.md#random-encounters-almost-only-happen-after-doors). Doors,
squares and damage zones are described in [dungeon.md](dungeon.md).

Tech: [monsters.md §2.1](../tech/monsters.md#21-when-a-fight-starts)

---

## 4. Fixed fights: guarded squares and events

Besides random fights there are two kinds of fixed fight.

- **Guarded squares**: 244 fixed spots, from none (floor 20) and 2 (floor 10) up to 21 (floor 4) per floor.
  Stepping on one always starts a fight from that square's encounter area. Each guard fights **once per floor
  visit**: all guards come back whenever the party changes floors
  ([findings.md](findings.md#guards-and-one-shot-events-re-arm-on-every-floor-change)). A guarded-square victory is
  **the only way to get a chest**; random fights give gold only.
- **Event fights**: story events (bosses, named monsters) start a fight from areas 34-53, each with one fixed
  formation. Areas 48 and 49 play the boss music.

Example from [monsters_table.md](monsters_table.md): event area 49, the Abyss Lurker fight.

| area | random on floors | guarded squares on floors | formation (one of 4 picked at random; monster ×size) |
|---|---|---|---|
| 49 |  |  | F133: Mist Dragon ×2 + ShadowDragon ×1-2 + Deep Dragon ×0-2 + Abyss Lurker ×1 |

**Notes:** on most floors guards use the same areas as random fights, so a guarded square is a guaranteed,
re-arming fight with the floor's normal monsters plus a chest. The chest itself (value, tier, items, traps) is in
[dungeon.md](dungeon.md).

Tech: [monsters.md §2.2](../tech/monsters.md#22-fixed-fights), [dungeon.md §4](../tech/dungeon.md#4-floors)

---

## 5. Encounter areas and group formation

Every map square carries an **encounter area** number, and each area lists **4 formations**. The fight uses one of
the 4, each with chance 1 in 4; an area that lists the same formation twice makes it twice as likely.

| Area numbers | Used for |
|---|---|
| 1-33 | random fights and guarded squares of floors 1-30 (floor 1 has three zones, areas 1, 2 and 3; floor 2 is area 4; floor 3 is area 5, with area 6 on two guarded squares; ... floor 30 uses 32 and 33) |
| 34-53 | event fights, one fixed formation each; the guarded squares of floor 13 use area 50, and some of floor 18 use area 51 |
| 101-105 | the damage-zone squares of floors 8, 11, 25, 27 and 30, which have their own monster mix |
| 54-100 | on no map and used by no event ([findings.md](findings.md#encounter-areas-54-100-are-unused)) |

**Formation.** A formation has up to 4 **groups**, each a monster and a size rule: base size + a random number from
0 to (extra − 1), exactly the base size when extra is 0, at most 9. Group 1 always has at least one monster; groups
2-4 that come out at 0 are dropped. So a fight has 1 to 4 groups of 1 to 9 monsters. There are 150 formations.
Groups 1-2 fight from the front ranks and groups 3-4 from the back ([combat.md](combat.md#8-monster-reach-and-targets)).

Examples from [monsters_table.md](monsters_table.md):

| area | random on floors | guarded squares on floors | formation (one of 4 picked at random; monster ×size) |
|---|---|---|---|
| 1 | 1 | 1 | F0: CrawlingClaw ×1-4 / F1: Eye Wing ×1-4 / F2: Gas Cloud ×1-4 / F3: Banshee ×1 |
| 7 | 5 | 5 | F24: Dryad ×3-4 + Treant ×2-4 / F25: Ogre ×3-4 + Ogre Lord ×2-4 / F26: Skeleton ×4 + Wight ×3 + Zombie ×1-4 + Ghoul ×0-3 / F27: Goblin ×5-7 + Goblin King ×0-4 + Dark Elf ×3-4 |
| 33 | 29-30 | 29-30 | F128: Avenger ×3 + Valiant ×4 + Kunoichi ×3 + Musashi ×1 / F129: Treant ×8 + Rakshasa ×6 + Phoenix ×4 + From Beyond ×1 / F130: Demon Lord ×2 + Succubus Qn. ×3 + Arch Demon ×2 + Hell Master ×3 / F131: Beholder ×4 + Nightcrawler ×4 + Night Rider ×4 + Unspeakable ×1 |

Floor 1 starts with single groups of 1-4 weak monsters; by floor 5 fights have 2-4 groups; two of the four
formations of the last floors put a level 27-29 "ancient" monster behind three large groups.

**Notes:** areas 54-100 are overlapping slices of the formation list that no map or event uses; they may be a cut
"random depth" table (inferred). Areas 104 and 105 list formations 150 and 151, past the end of the list, shown as
"(none)" in the table ([findings.md](findings.md#two-damage-zone-areas-have-empty-formations)).

Tech: [monsters.md §2.3](../tech/monsters.md#23-group-formation)

---

## 6. Monster actions

Each round every monster picks one action by going down a fixed priority list; the first check that succeeds
decides. The checks use only the monster's own stats and status. F is the monster's flee value.

| Step | Condition | Action |
|---|---|---|
| Before anything else | the monster is Afraid | flees with chance (F + 5) × 5% if F is not 0; otherwise does nothing |
| Before anything else | the monster is Asleep or worse (Paralyzed, Stoned) | does nothing |
| 1 | it has spells: 25% | casts a spell |
| 2 | it can call for help: 25% (strong callers 65%) | calls for help |
| 3 | F is not 0: F × 5% (only on the monsters' side of the battle) | flees |
| 4 | it can breathe: 1 in 8 | breathes on the party |
| 5 | otherwise | attacks (all its swings against a target its reach allows) |

**The percentages are per step, not overall:** each check only runs if the ones above it failed. For a Goblin
(calls 25%, flee value 2): calls for help 25%, flees 75% × 10% = 7.5%, attacks the remaining 67.5% (computed).

**Spell choice.** The monster picks one of its schools at random, then one spell at random from **all** spells of
that school up to its top level, each equally likely, so a top-level-7 Mage monster casts a level-1 spell as often
as any other single spell. If the picked spell cannot be cast in battle, the monster does nothing that turn
([findings.md](findings.md#monsters-that-pick-a-non-battle-spell-lose-their-turn)).

**Fleeing** removes the monster from the fight; fled monsters give no EXP or gold ([combat.md](combat.md#15-rewards)).
An Afraid monster is more likely to flee than a calm one ((F + 5) × 5% against F × 5%), and an Afraid monster with
flee value 0 just stands there.

**Notes:** what calling for help does (how many monsters arrive, into which group) was not traced. Breath damage
was not traced either ([combat.md](combat.md#10-breath)).

Tech: [monsters.md §3](../tech/monsters.md#3-monster-turn)

---

## Open questions

- **Golem and ghost marks:** what the two type marks do; one more stat (0 to 14) is never read. The 6th element's
  name was not read.
- **Type in spells:** the spell rules read a monster's type; what for was not traced.
- **Spell schools 2-5:** probably Valiant, Avenger, Musashi and Kunoichi (each of those four monsters has the
  matching one), not confirmed.
- **Call for help:** what it adds to the battle.
- **Target choice:** which party member a monster attacks among those its reach allows.
- **Special hits switched off:** what in battle turns them off.
- **Areas 104 and 105** (damage zones of floors 27 and 30): what a fight there produces when an empty formation is
  picked was not checked.
- **Identification:** how the game decides at battle start whether a group shows its real name.
- **Surprise and initiative:** see [combat.md](combat.md#1-round-structure-and-ranks).
- **Encounter areas 54-100:** nothing in the game uses them.

Tech: [monsters.md §9](../tech/monsters.md#9-not-found--open)
