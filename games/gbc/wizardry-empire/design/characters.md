# Characters: races, creation, classes, leveling, aging, statuses

How a Wizardry Empire character is made and how it grows, ages and recovers. Spells (schools, the spell list,
learning, slots, Summoner pacts) are in [spells.md](spells.md); equipment rules and item use in
[items.md](items.md); the inn, temple and shop (prices, healing, raise odds) in [town.md](town.md); hitting and
damage in [combat.md](combat.md). Notation and confidence tags: [README.md](README.md).

## Overview

- **Five races, fourteen classes.** A race only sets the six starting stats and the lifetime stat limits (race value
  + 10); Humans get +1 and Hobbits +2 extra bonus points. Nine classes can be created (Fighter, Mage, Priest, Thief,
  Bishop, Samurai, Lord, Ninja, Archer). Five **special classes** (Valiant, Avenger, Musashi, Kunoichi, Summoner) are
  reached only by using one legendary item each, never at the Training Grounds.
- **Creation:** race, gender, alignment, then a **bonus-point roll** (usually 4-13, average 10.4, a 5.6% chance of 20
  or more, cap 60). Points go onto the six stats, **at most +10 on one stat**, and all must be spent. The classes
  whose stat minimums, alignment and gender are met are offered. A new character is 14-16 years old.
- **Class change:** at the Training Grounds a character can switch to any creatable class its current stats allow.
  It drops to level 1 with 0 EXP, ages 1-3 years and has its stats reset, but keeps its HP, gold and Mage and Priest
  spells.
- **Leveling** happens only at the **Inn**, one level per stay. Each level adds 1 HP plus one class die and up to
  two extra dice; as the game is written, **low VIT+LUK gives more HP** ([findings.md](findings.md)). Every stat is
  rolled: young characters gain STR, VIT and AGI, old ones lose them and gain PIE.
- **EXP curve:** 16 hand-tuned steps per class, then every further level costs the 16th step again. A Fighter needs
  1,200 EXP for level 2 (verified). Thief is the cheapest class; Valiant, Ninja and Kunoichi are the most expensive.
- **Aging is real.** Each inn night outside the Stables is one day of a 360-day year, whatever the character's HP.
  Class change and a temple raise add 1-3 years. The inn birthday that reaches age **57 always kills** the character:
  the survival roll is ignored (verified; [findings.md](findings.md)).
- **Statuses:** one main state (OK, Afraid, Asleep, Paralyzed, Stoned, Dead, Ashes, Lost) plus two conditions that
  can come on top of any state (Poisoned, Silenced). The temple cures everything but Lost; a failed raise turns Dead
  into Ashes and Ashes into Lost. The Revival Charm cures Dead, Ashes and even Lost (verified).

---

## 1. Races

The race fixes the starting value of each stat, the lifetime limits of each stat, and a few extra bonus points at
creation. Nothing else: no race is barred from any class, and no racial resistance or other trait was found.

| Race (JP) | STR | IQ | PIE | VIT | AGI | LUK | Sum | Extra bonus points |
|---|---|---|---|---|---|---|---|---|
| Human (にんげん) | 8 | 8 | 6 | 8 | 8 | 9 | 47 | +1 |
| Elf (エルフ) | 7 | 10 | 10 | 6 | 10 | 6 | 49 | 0 |
| Dwarf (ドワーフ) | 12 | 6 | 10 | 10 | 5 | 6 | 49 | 0 |
| Gnome (ノーム) | 7 | 7 | 10 | 8 | 10 | 7 | 49 | 0 |
| Hobbit (ホビット) | 6 | 7 | 7 | 6 | 10 | 14 | 50 | +2 |

- **Gender:** a female character has **STR −1 and VIT +1** on top of the race values. The same adjustment applies to
  her limits and to the stat reset on a class change.
- **Lifetime limits:** a stat can never rise above **race value + 10** (gender-adjusted) and never fall below the race
  value. It also cannot fall below the current class's minimum for that stat (section 2.4). A blocked rise or fall
  simply does not happen.

Maximum stats per race (computed: race value + 10; female: STR −1, VIT +1):

| Race | STR | IQ | PIE | VIT | AGI | LUK |
|---|---|---|---|---|---|---|
| Human | 18 | 18 | 16 | 18 | 18 | 19 |
| Elf | 17 | 20 | 20 | 16 | 20 | 16 |
| Dwarf | 22 | 16 | 20 | 20 | 15 | 16 |
| Gnome | 17 | 17 | 20 | 18 | 20 | 17 |
| Hobbit | 16 | 17 | 17 | 16 | 20 | 24 |

**Notes:** the race also sets the floor for the VIT that a temple raise can take away ([town.md](town.md), section
"Temple"). Each race has one more value (6/6/7/6/5) that the game loads and never uses (see Open questions and
[findings.md](findings.md)).

Tech: [characters.md §2](../tech/characters.md#2-races)

---

## 2. Character creation

The player creates characters at the Training Grounds in this order: name, race, gender, alignment, bonus points,
class, confirm. Six ready-made characters also exist (section 2.6).

Tech: [characters.md §3](../tech/characters.md#3-character-creation-training-grounds)

### 2.1 Starting age

A new character is **16 (about 66%), 15 (about 33%) or 14 (about 1%)** years old.

Its position within the year starts at a random day from 0 to 255 of the 360-day year, so the first birthday comes
after 105 to 360 inn nights.

Tech: [characters.md §3.1](../tech/characters.md#31-starting-age)

### 2.2 Bonus points

The bonus pool is what makes a character special. It is usually 4 to 13 points, with a small chance of a much
larger "jackpot" pool.

```csharp
int r = Rnd(0, 20);
int points = r < 5  ? 8 + Rnd(0, 2)     // 5 in 21:  8-10
           : r < 10 ? 4 + Rnd(0, 3)     // 5 in 21:  4-7
           :          10 + Rnd(0, 3);   // 11 in 21: 10-13
for (int i = 0; i < 4; i++)             // four separate jackpot rolls
    if (Rnd(0, 99) < 2) points += 10;   // about 2.3% each
points = Math.Min(60, points + raceExtra);   // Human +1, Hobbit +2
```

A jackpot comes up about 2.3% of the time rather than 2%, because the game's rolls are slightly uneven at this
scale; the table below includes that.

Distribution before the race extra:

| Points | 4-7 | 8 | 9 | 10 | 11-13 | 14-19 | 20-23 | 24+ |
|---|---|---|---|---|---|---|---|---|
| Chance | 5.4% each | 7.3% | 7.2% | **19.1%** | 11.9% each | 3.5% in total | 5.3% in total | 0.3% in total |

Average **10.4**; 20 or more: **5.6%**.

**Notes:** whether the player can re-roll by backing out of the screen was not tested; the roll is made each time
the screen is entered, so backing out to the alignment step and returning probably re-rolls it (inferred).

Tech: [characters.md §3.2](../tech/characters.md#32-bonus-points)

### 2.3 Spending the points

- The player moves points onto the six stats one at a time and can take them back, never below the race value.
- **A stat takes at most +10 points.** With that cap a character starts at most at its lifetime limit (section 1).
- **All points must be spent** before a class can be chosen ("Bonus points remain."). If no class qualifies, the
  game says "No class is available."
- The list of qualifying classes updates live as points move.

Tech: [characters.md §3.3](../tech/characters.md#33-spending-points)

### 2.4 Class requirements

A class is offered when every stat is at least its minimum (blank = no minimum), the gender fits and the alignment
is allowed. The special classes have requirements in the same table, but creation and the Change Class menu only
offer the first nine classes; for the special classes the minimums are used only when an item changes the class
(section 3.3).

| Class (JP) | STR | IQ | PIE | VIT | AGI | LUK | Gender | Alignment |
|---|---|---|---|---|---|---|---|---|
| Fighter (せんし) | 11 | | | | | | any | any |
| Mage (まほうつかい) | | 11 | | | | | any | any |
| Priest (そうりょ) | | | 11 | | | | any | Good, Evil |
| Thief (とうぞく) | | | | | 11 | | any | Neutral, Evil |
| Bishop (ビショップ) | | 12 | 12 | | | | any | Good, Evil |
| Samurai (サムライ) | 15 | 11 | 10 | 14 | 10 | | any | Good, Neutral |
| Lord (ロード) | 15 | 12 | 12 | 15 | 14 | 15 | any | Good |
| Ninja (ニンジャ) | 16 | 16 | 16 | 16 | 15 | 16 | **male** | Evil |
| Archer (ゆみつかい) | 10 | 10 | | | 12 | | any | any |
| Valiant (ヴァリアント) | 15 | 16 | 17 | 15 | 16 | 15 | any | Good |
| Avenger (アベンジャー) | 16 | 16 | 14 | 12 | | | any | Evil |
| Musashi (ムサシ) | 18 | 13 | 13 | 18 | 17 | 13 | any | Good, Neutral |
| Kunoichi (くのいち) | 17 | 16 | 16 | 17 | 18 | 17 | **female** | Evil |
| Summoner (しょうかんし) | | 18 | 18 | | | 16 | any | Neutral |

**Notes:** a Ninja at creation needs a jackpot roll: a Human needs 8+8+10+8+7+7 = 48 points to reach the minimums,
far above the usual 4-13.

Tech: [characters.md §3.4](../tech/characters.md#34-class-eligibility)

### 2.5 What a new character starts with

- **Stats:** race values (gender-adjusted) plus the points spent.
- **Gold:** 100 G.
- **HP** = a class roll + a VIT bonus. Only the nine creatable classes have a starting roll.

  | Class | Starting HP before the VIT bonus |
  |---|---|
  | Fighter | 1d3+5 (6-8) |
  | Mage | 1d2+3 (4-5) |
  | Priest | 1d2+5 (6-7) |
  | Thief | 1d2+4 (5-6) |
  | Bishop | 1d2+4 (5-6) |
  | Samurai | 1d3+6 (7-9) |
  | Lord | 1d5+7 (8-12) |
  | Ninja | 1d5+5 (6-10) |
  | Archer | 1d3+4 (5-7) |

  | VIT | 6-7 | 8-10 | 11-14 | 15-18 | 19-20 | 21 |
  |---|---|---|---|---|---|---|
  | HP bonus | 0 | +1 | +2 | +3 | +4 | +5 |

- **Kit and AC:** two items, both equipped.

  | Class | Items | AC |
  |---|---|---|
  | Fighter, Samurai, Lord | Sword + Leather Armor | 8 |
  | Thief | Short Sword + Leather Armor | 8 |
  | Archer | Dagger + Leather Armor | 8 |
  | Mage | Dagger + Robe | 9 |
  | Priest, Bishop | Quarterstaff + Robe | 9 |
  | Ninja | Short Sword + Robe | 9 |

- **Spells:** the level-up spell step is applied once at creation, so a Mage, Priest or Bishop starts with one
  guaranteed random level-1 spell and a stat-based chance at each other level-1 spell
  ([spells.md](spells.md#4-learning-spells)).

Tech: [characters.md §3.5](../tech/characters.md#35-what-the-new-character-gets)

### 2.6 Ready-made characters

Six characters come with the game, all level 1, age 16, 100 G, 0 EXP:

| Name (JP) | Race | Class | Alignment | Gender | STR | IQ | PIE | VIT | AGI | LUK | HP | AC | Spells |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Fighter (せんし) | Dwarf | Fighter | Good | M | 15 | 8 | 11 | 14 | 7 | 8 | 10 | 8 | |
| Thief (とうぞく) | Human | Thief | Evil | M | 8 | 9 | 7 | 9 | 13 | 13 | 7 | 8 | |
| Archer (ゆみつかい) | Hobbit | Archer | Neutral | M | 14 | 6 | 7 | 6 | 15 | 17 | 7 | 8 | |
| Priest (そうりょ) | Gnome | Priest | Good | M | 9 | 10 | 14 | 9 | 12 | 9 | 8 | 9 | Restore |
| Mage (まほうつかい) | Elf | Mage | Evil | F | 8 | 15 | 12 | 8 | 12 | 8 | 5 | 9 | Call Fear |
| Bishop (ビショップ) | Elf | Bishop | Good | M | 8 | 13 | 13 | 8 | 12 | 8 | 7 | 9 | Call Fear, Flame Arrow |

Tech: [characters.md §3.6](../tech/characters.md#36-ready-made-characters)

---

## 3. Classes

The class decides the weapons and armor a character can use, its spell schools, its HP growth and its EXP curve.

### 3.1 Summary

"HP die D" is the class value in the level-up HP formula (section 4.3); the base gain per level is 1d(D+1). EXP
values are totals from the table in section 4.1.

| Class | How obtained | Spell schools ([spells.md](spells.md#1-schools-and-who-casts-them)) | HP die D | Base HP per level | EXP to reach level 2 | EXP to reach level 10 |
|---|---|---|---|---|---|---|
| Fighter | created | none | 9 | 1d10 | 1,200 | 56,800 |
| Mage | created | Mage | 4 | 1d5 | 1,520 | 73,720 |
| Priest | created | Priest | 8 | 1d9 | 1,400 | 69,100 |
| Thief | created | none | 5 | 1d6 | 1,080 | 45,320 |
| Bishop | created | Mage, Priest | 6 | 1d7 | 1,650 | 97,550 |
| Samurai | created | Mage (from level 4) | 8 | 1d9 | 1,800 | 106,070 |
| Lord | created | Priest (from level 4) | 8 | 1d9 | 1,920 | 111,320 |
| Ninja | created (male) or item | none | 7 | 1d8 | 2,150 | 116,550 |
| Archer | created | none | 6 | 1d7 | 1,520 | 71,370 |
| Valiant | item only | Valiant Prayers (from level 5) | 8 | 1d9 | 2,100 | 121,400 |
| Avenger | item only | Avenger Arts (from level 5) | 8 | 1d9 | 1,360 | 62,910 |
| Musashi | item only | Musashi Arts (from level 5) | 8 | 1d9 | 1,980 | 116,150 |
| Kunoichi | item only (female) | Kunoichi Arts (from level 5) | 6 | 1d7 | 2,150 | 116,550 |
| Summoner | item only | Summons (pacts, from level 3) | 5 | 1d6 | 1,420 | 77,170 |

**Notes:** class rules that belong to equipment and combat are in their own documents: swings per round and to-hit
([combat.md](combat.md)), Musashi dual wielding and the Avenger's immunity to cursed and alignment-locked gear
([items.md](items.md)).

Tech: [characters.md §5.1](../tech/characters.md#51-summary)

### 3.2 Equipment groups

Each item lists the classes that may equip it. Counting the items per class and category gives each class's
equipment group. The column header gives the number of items in that category; "Staff/mace" also holds flails and
maces.

| Class | Sword (35) | Axe (6) | Spear (9) | Dagger (9) | Staff/mace (22) | Hammer (2) | Scythe (2) | Bow (7) | Arrow (4) | Armor (26) | Robe (6) | Shield (17) | Helm (16) | Gloves (14) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Fighter | 26 | 6 | 9 | 7 | 21 | 2 | 2 | 3 | 4 | 20 | 3 | 16 | 13 | 13 |
| Mage | 0 | 0 | 0 | 6 | 8 | 0 | 0 | 0 | 0 | 0 | 4 | 0 | 2 | 0 |
| Priest | 0 | 0 | 0 | 0 | 17 | 2 | 0 | 0 | 0 | 17 | 5 | 13 | 12 | 12 |
| Thief | 5 | 0 | 0 | 8 | 0 | 0 | 1 | 2 | 4 | 4 | 4 | 3 | 2 | 1 |
| Bishop | 0 | 0 | 0 | 0 | 17 | 2 | 0 | 0 | 0 | 6 | 5 | 3 | 5 | 2 |
| Samurai | 32 | 6 | 9 | 7 | 21 | 2 | 2 | 3 | 4 | 21 | 4 | 0 | 12 | 12 |
| Lord | 26 | 6 | 9 | 7 | 21 | 2 | 2 | 3 | 4 | 18 | 4 | 16 | 13 | 13 |
| Ninja | 27 | 6 | 9 | 9 | 22 | 2 | 2 | 3 | 4 | 20 | 4 | 3 | 11 | 12 |
| Archer | 0 | 0 | 0 | 6 | 0 | 0 | 0 | 7 | 4 | 3 | 4 | 0 | 2 | 1 |
| Valiant | 26 | 6 | 9 | 7 | 21 | 2 | 2 | 3 | 4 | 18 | 4 | 17 | 14 | 13 |
| Avenger | 6 | 2 | 2 | 1 | 4 | 0 | 1 | 0 | 0 | 7 | 4 | 6 | 4 | 4 |
| Musashi | 28 | 1 | 6 | 7 | 8 | 2 | 1 | 0 | 0 | 21 | 4 | 0 | 13 | 12 |
| Kunoichi | 27 | 6 | 9 | 9 | 22 | 2 | 2 | 3 | 4 | 20 | 4 | 11 | 11 | 13 |
| Summoner | 0 | 0 | 0 | 6 | 16 | 2 | 0 | 1 | 2 | 3 | 6 | 2 | 3 | 1 |

**In short:** Fighter, Lord, Valiant, Ninja and Kunoichi take nearly every weapon. Samurai and Musashi own the
katanas (32 and 28 swords) but use no shields. Priests wear heavy armor and shields but no edged weapons. Mage,
Archer and Summoner are limited to robes and light armor. The Avenger has a short, special list.

**Accessories and consumables:**
- **Rings:** 9 of the 10 rings can be equipped by every class; the Priest Ring only by Priest, Bishop, Lord and
  Valiant.
- **Other accessories** differ: Cloak, Shell Amulets, Rabbit's Foot, Synthesis and Youth Stone: every class; Hider
  Cloak: Thief; Clockwork Doll: Ninja and Kunoichi; Laila's Beads: Priest, Bishop and Valiant; Jewel of Magic: Mage,
  Priest, Bishop and Summoner; Fairy's Heart: every class except Ninja, Avenger and Kunoichi.
- **Consumables** (all potions and scrolls, the Dreaming, Healing and Exorcist Stones, the Exorcism and Revival
  Charms) and the Key Card **cannot be equipped by anyone; anyone can use them** (verified: a
  Fighter used a Healing Potion and a Revival Charm in camp). They show "none" in the Classes column of
  [items_table.md](items_table.md).

**Notes:** the exact list for every item is the Classes column of [items_table.md](items_table.md); how equipping
works (main and off hand, curses, alignment locks) is in [items.md](items.md).

Tech: [characters.md §5.2](../tech/characters.md#52-equipment-groups)

### 3.3 Special classes and their items

The five special classes, and the Ninja for characters who did not qualify at creation, come from using an item's
special power ("Use its special power?"). The change works like Change Class (section 3.4): **level 1, 0 EXP, +1 to
3 years of age, stats reset to the race values and then raised to the new class's minimums.** The item route does
not roll a starting spell; the special schools open at level 5 anyway.

| Item (JP) | Becomes | Condition checked | What happens to the item | Who can equip the item |
|---|---|---|---|---|
| Thieves' Dagger (シーブズダガー) | Ninja | a male **Thief** uses it | used up | Thi Nin Kun |
| Butterfly Knife (バタフライナイフ) | Ninja | male | used up | Fig Mag Thi Sam Lor Nin Arc Val Mus Kun Sum |
| Guardian Shield (かごのたて) | Valiant | none | 30%: vanishes; otherwise becomes the Valiant Shield (ヴァリアントシールド) | Fig Pri Thi Bis Lor Nin Val Kun |
| The Avenger (ジ・アベンジャー) | Avenger | none | 30%: vanishes; otherwise becomes the Avenger Sword (アベンジャーソード) | Fig Thi Sam Lor Nin Ave Mus Kun |
| Warrior's Helm (もののふのかぶと) | Musashi | none | 30%: vanishes; otherwise becomes Musashi's Helm (ムサシのかぶと) | Fig Sam Lor Val Mus |
| Charming Gloves (みわくのこて) | Kunoichi | female | 30%: vanishes; otherwise becomes the Kunoichi Gloves (くのいちのこて) | Fig Pri Sam Lor Nin Val Mus Kun |
| Magic Robe (まどうのローブ) | Summoner | none | 30%: vanishes; otherwise becomes the Summoner's Robe (しょうかんしのローブ) | all |

Two more items of the same kind change the character without changing the class: the **Rabbit's Foot**
(ウサギのあし, LUK +1, up to the lifetime limit; used up) and the **Youth Stone** (わかがえりのいし, age −1 year,
not below 12; used up).

The "who can equip" column is quoted from [items_table.md](items_table.md); none of the seven class items has an
alignment restriction there.

**Notes:**
- **No stat or alignment requirement is checked** when the item changes the class; only the gender (Ninja male,
  Kunoichi female) and, for the Thieves' Dagger, the Thief class. Because the stats are then raised to the class
  minimums, a character who becomes a Musashi starts with at least STR 18, VIT 18 and AGI 17 whatever they were
  before. Whether the character must be able to equip the item to use its power was not traced; the item's own
  class list may be the only gate (inferred). See [findings.md](findings.md).
- As the game is written, a non-Thief who uses the Thieves' Dagger loses the dagger without becoming a Ninja
  (inferred). See [findings.md](findings.md).
- A successful change also unlocks the class in the museum (it then shows the hidden class letters).
- The item is taken off before its power works; the item side of the change is in [items.md](items.md).

Tech: [characters.md §5.5](../tech/characters.md#55-special-classes-legendary-items),
[items.md §3.3](../tech/items.md#33-special-powers)

### 3.4 Change Class (Training Grounds)

A character can change to any of the nine creatable classes (not its current one) whose requirements its **current**
stats, alignment and gender meet (section 2.4). The price is steep:

- **Level 1 and 0 EXP**; age **+1 to 3 years** (capped at 99).
- **Stats reset:** each stat drops to the race value (gender-adjusted), then is raised to the new class's minimum
  where the class has one. Everything earned above that is lost.
- **Kept:** max and current HP, gold, and all Mage and Priest spells already known. Those old spells stay castable
  ([spells.md](spells.md#5-spell-slots)).
- **Lost:** spells of a special school, and their slots.
- **Equipment:** everything equipped is taken off, except cursed items, which stay stuck.
- If the new class is a Mage, Priest or Bishop, it learns one guaranteed random level-1 spell at once, and spell
  slots are recomputed ([spells.md](spells.md#4-learning-spells)).

**Notes:** because HP is kept and the new class starts at level 1, Change Class is how a character carries a large
HP pool into a new class. Keeping the old spells is listed in [findings.md](findings.md).

Tech: [characters.md §5.4](../tech/characters.md#54-change-class)

---

## 4. Experience and leveling

### 4.1 EXP needed

A level-1 Fighter needs **1,200 EXP** for level 2 (verified). Each class has its own curve of 16 steps; from level 17
on, every level costs the last (16th) step again, so the curve becomes linear. Monsters give EXP when killed, split
among the party ([combat.md](combat.md)).

Each row is the **total EXP needed to reach that level**. A character levels up at the Inn once its EXP is at least
the row of the next level. Example (verified): a level-9 Thief with 29,820 EXP (row 9) is told it needs 15,500 more,
which is row 10 (45,320) minus 29,820.

| Level | Fig | Mag | Pri | Thi | Bis | Sam | Lor | Nin | Arc | Val | Ave | Mus | Kun | Sum |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2 | 1,200 | 1,520 | 1,400 | 1,080 | 1,650 | 1,800 | 1,920 | 2,150 | 1,520 | 2,100 | 1,360 | 1,980 | 2,150 | 1,420 |
| 3 | 2,200 | 2,820 | 2,600 | 1,920 | 3,150 | 3,550 | 3,820 | 4,150 | 2,770 | 4,200 | 2,460 | 3,930 | 4,150 | 2,670 |
| 4 | 3,700 | 4,820 | 4,400 | 3,220 | 5,450 | 6,250 | 6,820 | 7,450 | 4,670 | 7,600 | 4,110 | 7,030 | 7,450 | 4,570 |
| 5 | 6,000 | 8,020 | 7,200 | 5,270 | 9,150 | 10,450 | 11,420 | 12,350 | 7,670 | 12,800 | 6,610 | 11,830 | 12,350 | 7,570 |
| 6 | 9,500 | 13,020 | 11,800 | 8,370 | 15,250 | 16,870 | 18,320 | 19,650 | 12,470 | 20,600 | 10,610 | 19,150 | 19,650 | 12,370 |
| 7 | 14,800 | 20,620 | 19,100 | 13,020 | 25,050 | 26,870 | 28,820 | 30,850 | 19,870 | 32,600 | 16,910 | 30,650 | 30,850 | 19,920 |
| 8 | 22,800 | 31,920 | 30,100 | 19,820 | 40,450 | 42,870 | 45,320 | 48,350 | 30,970 | 50,800 | 26,410 | 48,350 | 48,350 | 31,620 |
| 9 | 35,800 | 48,720 | 46,100 | 29,820 | 63,450 | 67,870 | 71,320 | 75,450 | 47,370 | 78,800 | 40,910 | 75,350 | 75,450 | 49,620 |
| 10 | 56,800 | 73,720 | 69,100 | 45,320 | 97,550 | 106,070 | 111,320 | 116,550 | 71,370 | 121,400 | 62,910 | 116,150 | 116,550 | 77,170 |
| 11 | 90,300 | 110,720 | 104,100 | 70,820 | 147,750 | 164,070 | 171,320 | 178,350 | 107,370 | 184,400 | 97,110 | 177,150 | 178,350 | 118,970 |
| 12 | 144,600 | 165,720 | 158,100 | 111,820 | 220,750 | 249,070 | 259,320 | 268,350 | 161,870 | 276,400 | 151,210 | 266,150 | 268,350 | 182,470 |
| 13 | 229,700 | 251,720 | 239,500 | 176,820 | 326,150 | 370,270 | 384,320 | 398,350 | 245,570 | 408,400 | 234,410 | 394,350 | 398,350 | 277,470 |
| 14 | 355,700 | 378,720 | 366,000 | 276,820 | 476,150 | 541,070 | 558,320 | 582,350 | 372,270 | 594,400 | 360,410 | 577,150 | 582,350 | 415,470 |
| 15 | 533,700 | 564,720 | 546,000 | 426,820 | 693,150 | 779,070 | 799,320 | 838,350 | 555,270 | 854,400 | 539,410 | 834,150 | 838,350 | 612,470 |
| 16 | 763,700 | 814,720 | 786,000 | 644,820 | 1,003,150 | 1,105,070 | 1,129,320 | 1,188,350 | 800,270 | 1,204,400 | 774,410 | 1,180,150 | 1,188,350 | 882,470 |
| 17 | 993,700 | 1,064,720 | 1,026,000 | 862,820 | 1,313,150 | 1,431,070 | 1,459,320 | 1,538,350 | 1,045,270 | 1,554,400 | 1,009,410 | 1,526,150 | 1,538,350 | 1,152,470 |
| each further level | +230,000 | +250,000 | +240,000 | +218,000 | +310,000 | +326,000 | +330,000 | +350,000 | +245,000 | +350,000 | +235,000 | +346,000 | +350,000 | +270,000 |

How the table is built: the EXP for level L is the sum of the class's first L steps; from level 17 on, add step 16
once more per level.

Cost ranking at level 10, cheapest first: Thief, Fighter, Avenger, Priest, Archer, Mage, Summoner, Bishop, Samurai,
Lord, Musashi, Ninja = Kunoichi, Valiant. Ninja and Kunoichi share the same curve.

**Notes:**
- **Level 2 costs the first two steps together**, so the steps are counted up to the level being reached, not from
  level 1. The original release told a new Fighter it needed 500 EXP at the same point (v1.0, verified), so the
  start of the curve changed between revisions. See [findings.md](findings.md).
- The level cap is 9999.

Tech: [characters.md §6.1](../tech/characters.md#61-exp-needed)

### 4.2 When a level is gained

Levels are gained **only at the Inn**, and **one per stay**. When a room is chosen for a character, the game checks
its EXP: if it is enough, that stay grants one level; otherwise the Inn says how many more EXP the next level needs
("Next level in N more EXP"). A character with EXP for several levels needs several stays.

A level-up does, in this order: level +1; a roll for each of the six stats (section 4.4); the HP gain (section 4.3);
spell learning ([spells.md](spells.md#4-learning-spells)).

**Notes:** room prices and healing are in [town.md](town.md). Every night outside the Stables also ages the
character (section 5).

Tech: [characters.md §6.2](../tech/characters.md#62-when-the-level-up-happens)

### 4.3 HP gained per level

Each level adds 1 HP plus one class die, and up to two extra dice. With D the class's HP die (section 3.1), the base
gain is 1d(D+1), the first extra die 1dD−1 (0 to D−1) and the second 1d(D−1)−1 (0 to D−2):

```csharp
int HpGain(int D, int vit, int luk)
{
    if (Rnd(0, 99) == luk + Rnd(0, luk)) return 1;   // about 1%: just 1 HP
    int gain = 1 + Rnd(0, D);                        // 1 .. D+1
    int r1 = Rnd(0, 99);
    if (r1 >= vit + luk)                             // LOW VIT+LUK passes more often
    {
        gain += Rnd(0, D - 1);                       // first extra die: 0 .. D-1
        int r2 = Rnd(0, 99);
        if (r2 >= r1 - (vit + luk))
            gain += Rnd(0, D - 2);                   // second extra die: 0 .. D-2
    }
    return gain;                                     // added to max and current HP (cap 65535)
}
```

Example, a Fighter (D = 9) with VIT+LUK = 30: a base of 1d10 (average 5.5); a 70% chance of a further 1d9−1 (0-8);
then usually another 1d8−1 (0-7).

**Notes:**
- **As the game is written, low VIT+LUK gives more HP.** The extra dice are rolled when a random number from 0 to 99
  is *at or above* VIT+LUK, so a character with VIT+LUK of 100 or more never gets them. This looks inverted against
  the usual intent (high VIT = more HP). See [findings.md](findings.md).
- The game works out the character's age bracket just before this step and then discards it: age has no effect on
  HP gain. See [findings.md](findings.md).
- That the second extra die can only follow the first, as in the code above, is (inferred).

Tech: [characters.md §6.3](../tech/characters.md#63-hp-gained-per-level)

### 4.4 Stat changes by age

At each level-up, each of the six stats is rolled separately and can rise by 1, stay, or fall by 1. The odds depend
on the character's age: young characters grow strong and agile, old ones decline physically but gain PIE.

Each stat rises by 1 with the first chance in the table, falls by 1 with the second, and otherwise stays. A change
beyond the stat's limits (race value + 10, race value, class minimum) does not happen. The game reports each change
("STR rose." / "STR fell.").

Chance to rise / chance to fall:

| Age | STR | IQ | PIE | VIT | AGI | LUK |
|---|---|---|---|---|---|---|
| under 20 | 75% / 11% | 50% / 6% | 40% / 21% | 89% / 6% | 79% / 6% | 46% / 16% |
| 20-24 | 70% / 11% | 55% / 6% | 45% / 16% | 84% / 6% | 79% / 6% | 46% / 17% |
| 25-29 | 60% / 21% | 55% / 11% | 50% / 16% | 75% / 11% | 75% / 11% | 41% / 21% |
| 30-39 | 45% / 30% | 60% / 11% | 55% / 16% | 64% / 21% | 70% / 11% | 38% / 25% |
| 40-49 | 30% / 40% | 60% / 21% | 60% / 11% | 50% / 30% | 55% / 30% | 25% / 25% |
| 50-59 | 20% / 50% | 55% / 25% | 64% / 11% | 40% / 40% | 30% / 60% | 20% / 25% |
| 60-69 | 10% / 65% | 45% / 40% | 70% / 11% | 30% / 55% | 20% / 75% | 20% / 25% |
| 70-79 | 5% / 75% | 30% / 55% | 79% / 11% | 15% / 70% | 5% / 90% | 19% / 25% |
| 80-89 | 0% / 90% | 20% / 70% | 89% / 6% | 10% / 80% | 5% / 90% | 19% / 30% |
| 90+ | 0% / 95% | 5% / 85% | 89% / 6% | 5% / 90% | 5% / 90% | 19% / 30% |

**Notes:** the brackets from 60 up matter little in practice, because the inn birthday that reaches 57 kills
(section 5).

Tech: [characters.md §6.4](../tech/characters.md#64-stat-changes-per-level)

---

## 5. Aging

Characters age in game days, and age matters: it drives the stat rolls at level-up (section 4.4), the odds of a
raise from the dead ([town.md](town.md), section "Temple"), and death by old age. This section is the one place for
the aging rules; the inn and temple link here.

- **Clock:** a year has 360 days; on day 360 the counter wraps and the character has a birthday (age cap 99).
- **What adds time:**

  | Event | Effect on age |
  |---|---|
  | An inn night in Cots, Economy, Suite or Royal Suite | +1 day, at any HP; a full stay is 7 nights, so +7 days (verified, from 1 HP and at full HP) |
  | A night in the Stables | nothing (verified) |
  | Change Class, or a class change by item | +1 to 3 years |
  | Raise at the temple, if it succeeds | +1 to 3 years, 89% of the time |
  | Raise by spell, if it succeeds | +1 year |
  | Youth Stone | −1 year, not below 12 |

  No aging in the maze was found.
- **Death by old age:** a birthday at the inn that brings the character to **57 or older kills them** ("died of
  old age."): status Dead, HP 0, and the character leaves the party. A 55-year-old turning 56 survives ("Happy
  birthday!").
- **Practical lifespan:** from 16, about 41 game years, about 14,800 inn nights (computed: 41 × 360).

**Notes:**
- The game makes a survival roll at the birthday, a random number from 0 to (99 + VIT/2 + LUK/2) compared with
  age − 56, but never uses the result, so every such birthday is fatal (verified: six characters aged 56 on the
  last day of the year, VIT and LUK 18, rolled 89, 89, 59, 50, 8 and 11 against 1, and all six died). The intended
  rule was probably "dies if the roll is below age − 56" (inferred), under which all six would have lived. See
  [findings.md](findings.md).
- Because the age bracket also sets the raise odds, every raise brings the next one and the fatal birthday closer.
- Inn rooms, prices and healing: [town.md](town.md).

Tech: [characters.md §7](../tech/characters.md#7-aging), [characters.md §8](../tech/characters.md#8-inn-rest),
[items.md §7](../tech/items.md#7-inn-aries-inn)

---

## 6. Status ailments and cures

A character has one main state and two conditions that can come on top of any state.

| Status (JP) | Kind | Cures |
|---|---|---|
| OK (せいじょう) | main state | |
| Afraid (きょうふ) | main state | temple; Remove Fear (by its name) |
| Asleep (すいみん) | main state | temple; Wake Up (by its name) |
| Paralyzed (まひ) | main state | temple; Cure Paralysis (by its name) |
| Stoned (いし) | main state | temple; Stone to Flesh (by its name) |
| Dead (しぼう) | main state | temple raise (roll); raising spell (roll); Revival Charm |
| Ashes (はい) | main state | temple raise (roll); raising spell (roll); Revival Charm |
| Lost (ロスト) | main state | Revival Charm (verified); the temple does not offer it |
| Poisoned (どく) | added condition | temple; Cure Poison (by its name) |
| Silenced (まふうじ) | added condition | temple |

"By its name" means only the spell's name says it cures the status; spell effects were not traced
([spells.md](spells.md#3-the-spell-list)).

- **Temple:** cures every status except Lost. The fee is a rate per status times the patient's level; Dead and
  Ashes need a roll on the patient's age and VIT. Fees, odds (from 1.2% to 95.3%) and side effects:
  [town.md](town.md), section "Temple". **A failed raise makes things worse: Dead becomes Ashes, Ashes becomes
  Lost**, and a character who becomes Lost at the temple is deleted from the roster at once.
- **Raising spell:** the game also has a raise roll for spells, on the patient's age and VIT plus the caster's PIE;
  its odds are in the same table in [town.md](town.md), section "Temple". Success: status OK, age +1 year. Failure:
  the status gets one step worse (Dead to Ashes, Ashes to Lost). This is the only way a Lost character stays in the
  party. Which spell uses this roll is not traced.
- **Revival Charm** (ふっかつのごふ, usable in battle and camp by any class, used up): on a Dead, Ashes or Lost
  member it sets status OK and HP to the maximum; on anyone else nothing happens (verified in camp on a Lost
  character).

**Notes:**
- How Afraid, Asleep and Paralyzed wear off in battle, how much poison hurts per step and how long Silence lasts
  were not traced.
- How monsters inflict statuses (special hits and their saving rolls), and the double damage a sleeping target
  takes: [combat.md](combat.md).
- A failed identification in camp can make the identifier Afraid ([items.md](items.md)).
- Death by old age: section 5.

Tech: [characters.md §9](../tech/characters.md#9-status-ailments-and-recovery),
[items.md §8](../tech/items.md#8-temple-samsara-temple)

---

## Open questions

- **Bonus re-roll:** whether backing out of the bonus screen re-rolls the points (likely) was not tested.
- **Unused race value:** each race has one more value (Human 6, Elf 6, Dwarf 7, Gnome 6, Hobbit 5) that the game
  loads and discards; perhaps a leftover base AC or size (inferred).
- **Item class change:** only gender (and the Thief class for the Thieves' Dagger) is checked. Whether the character
  must be able to equip the item, or match its alignment, was not traced.
- **Old-age death:** whether a character who died of old age can be raised, and what happens at the next birthday,
  was not traced.
- **Lost in the party:** a Lost member should only remain after a raising spell fails on Ashes; this was not seen
  in play.
- **Status wear-off in battle**, poison damage per step and Silence duration: not traced.
- **Which spells cure which status, and which spells raise the dead:** spell effects were not traced
  ([spells.md](spells.md#open-questions)).
- **Swings per round and to-hit per class:** the class tables exist but which belongs to which class was not traced
  ([combat.md](combat.md)).
