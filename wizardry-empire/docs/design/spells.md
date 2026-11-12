# Spells: schools, the spell list, learning, slots, Summoner pacts

How magic works in Wizardry Empire: who casts which school, every spell, how spells are learned, how many casts a
character has, and how the Summoner gains summons. Character classes, leveling and statuses are in
[characters.md](characters.md); how a spell gets through a monster's resistance is in [combat.md](combat.md); items
that cast spells are in [items.md](items.md). Notation and confidence tags: [README.md](README.md).

## Overview

- **125 spells in 7 schools**, each with 7 spell levels: Mage 28 and Priest 28 (the classic schools), and one school
  per special class: Valiant Prayers 16, Avenger Arts 12, Musashi Arts 12, Kunoichi Arts 13, Summons 16.
- **Who casts:** Mage, Priest and Bishop from level 1; Samurai (Mage spells) and Lord (Priest spells) from level 4;
  the special classes from level 5 (Summoner from level 3). Fighter, Thief, Ninja and Archer cast nothing.
- **Learning:** each spell level opens at a fixed character level per class. On exactly that level the character
  learns **one guaranteed random spell** of the new spell level; no stat affects it. At every level-up it also gets
  a stat-based chance (IQ, PIE, VIT or LUK; 5% to 60%) at each missing spell of the spell levels it has started.
- **Summoners never learn at level-up:** they form **pacts** at 16 magic circles in the maze, each with a minimum
  level from 3 to 38.
- **Spell slots** (casts per spell level, refilled every inn night, the free Stables included):
  `min(9, max(spells known at that level, character level − opening level + 1))`. Spells kept from an earlier class
  give one cast per spell known.
- **Effects are not documented yet:** damage, durations and success chances of individual spells were not traced.
  The list gives where each spell works and, as a reading of the data, its target and element.

---

## 1. Schools and who casts them

Each school has 7 spell levels. A spell's level is fixed by its place in the school's list.

| School (JP) | Spells | Spells per level (1-7) | Cast by |
|---|---|---|---|
| Mage (まほうつかいの じゅもん) | 28 | 4-3-4-3-4-6-4 | Mage, Bishop, Samurai |
| Priest (そうりょの じゅもん) | 28 | 4-5-5-3-4-4-3 | Priest, Bishop, Lord |
| Valiant Prayers (ヴァリアントの じゅもん) | 16 | 2-2-2-2-2-2-4 | Valiant |
| Avenger Arts (アベンジャーの じゅもん) | 12 | 2-2-2-2-2-1-1 | Avenger |
| Musashi Arts (ムサシの じゅもん) | 12 | 2-2-2-2-1-2-1 | Musashi |
| Kunoichi Arts (くのいちの じゅもん) | 13 | 2-2-2-2-2-2-1 | Kunoichi |
| Summons (しょうかんしの じゅもん) | 16 | 2-2-2-2-2-2-4 | Summoner (pacts only) |

(Special-school counts per level: from the lists in section 3, computed.)

**Opening levels:** the character level at which each spell level (1 to 7) opens, and the stat behind the chance to
learn extra spells (section 4.2):

| Class | School | Spell level 1, 2, 3, 4, 5, 6, 7 opens at character level | Extra-spell stat |
|---|---|---|---|
| Mage | Mage | 1, 3, 5, 7, 9, 11, 13 | IQ |
| Priest | Priest | 1, 3, 5, 7, 9, 11, 13 | PIE |
| Bishop | Mage | 1, 5, 9, 13, 17, 21, 25 | IQ |
| Bishop | Priest | 4, 8, 12, 16, 20, 24, 28 | PIE |
| Samurai | Mage | 4, 7, 10, 13, 16, 19, 22 | IQ |
| Lord | Priest | 4, 6, 8, 10, 12, 14, 16 | PIE |
| Valiant | Valiant Prayers | 5, 10, 15, 20, 25, 30, 35 | PIE |
| Avenger | Avenger Arts | 5, 10, 15, 20, 25, 30, 35 | VIT |
| Musashi | Musashi Arts | 5, 10, 15, 20, 25, 30, 35 | VIT |
| Kunoichi | Kunoichi Arts | 5, 10, 15, 20, 25, 30, 35 | LUK |
| Summoner | Summons | 3, 6, 14, 16, 20, 27, 34 (slots only; spells come from pacts, section 6) | none |
| Fighter, Thief, Ninja, Archer | none | | |

**Notes:** a Mage reaches the top spell level at character level 13, a Bishop's Priest side only at 28 and the
special classes at 35.

Tech: [characters.md §5.3](../tech/characters.md#53-spell-schedule-per-class-learning-103),
[characters.md §10](../tech/characters.md#10-spells)

---

## 2. Casting

- **Cost:** a cast uses one slot of the spell's level (inferred). Slots are counted per school and per spell level
  (section 5).
- **Where:** each spell is marked for use in battle, in camp, both, or at a chest. The camp marks match the crosses
  the game shows on its camp spell screen (verified); the battle and chest marks are (inferred). The two chest spells
  are Inspect and Trap Breaker; that they check and disarm a chest's trap is inferred from their names.
- **Target:** one enemy, an enemy group, all enemies, the caster, one ally, the party, a chest, or none (inferred
  from the pattern of spell names). Seven spells have a target kind that is unexplained: five Musashi and Kunoichi
  sword arts (Counter Cut, Triple Slash, Four Lights Cut, Rainfall Slash, Mist Slash), Dispel Magic and Begone,
  Evil. Only Counter Cut and Mist Slash share one, marked (A) in the list.
- **Element:** the monster resistance the spell is checked against, named as in the museum: Earth, Water, Fire,
  Wind, Spirit, the 6th element (name not read), Holy, None (inferred from the pattern of spell names). Monsters have
  one resistance per element ([monsters_table.md](monsters_table.md)); how a spell's power is set against it is in
  [combat.md](combat.md).

**Notes:** spell items (potions, staves, rings that cast a spell) are in [items.md](items.md). The odds of a raising
spell (the patient's age and VIT, the caster's PIE) are in the raise table in [town.md](town.md), section "Temple".

Tech: [characters.md §10](../tech/characters.md#10-spells),
[monsters.md §5](../tech/monsters.md#5-party-attacks-and-spells-on-monsters)

---

## 3. The spell list

All 125 spells by school and level. **Where** is from the spell data. **Target** and **Element** are readings of the
data (inferred, section 2). The effects (damage, duration, success chance) were not traced; the name is the only
guide for now.

### 3.1 Mage spells (まほうつかいの じゅもん)

| Lv | Spell | JP | Where | Target (inferred) | Element (inferred) |
|---|---|---|---|---|---|
| 1 | Call Fear | コールフィアー | battle | enemy group | Spirit |
| 1 | Shield | シールド | battle | caster | 6th element |
| 1 | Flame Arrow | フレイムアロー | battle | one enemy | Fire |
| 1 | Compass | コンパス | camp | none | None |
| 2 | Sleep | スリープ | battle | enemy group | Spirit |
| 2 | Lightning Bolt | ライトニングボルト | battle | enemy group | Wind |
| 2 | Darkness | ダークネス | battle | enemy group | None |
| 3 | Fireball | ファイアボール | battle | enemy group | Fire |
| 3 | Missile Shield | ミサイルシールド | battle | party | Wind |
| 3 | Striking | ストライキング | battle | one ally | None |
| 3 | Hold Ray | ホールドレイ | battle | enemy group | Spirit |
| 4 | Ice Storm | アイスストーム | battle | enemy group | Water |
| 4 | Explosion | エクスプロージョン | battle | all enemies | Fire |
| 4 | Levitate | レビテート | camp | party | 6th element |
| 5 | Thunderbolt | サンダーボルト | battle | all enemies | Wind |
| 5 | Stone Ray | ストーンレイ | battle | enemy group | Earth |
| 5 | Dispel Magic | ディスペルマジック | battle+camp | unexplained | 6th element |
| 5 | Magic Screen | マジックスクリーン | battle | party | 6th element |
| 6 | Frost Blizzard | フロストブリザード | battle | enemy group | Water |
| 6 | Earthquake | アースクウェイク | battle | all enemies | Earth |
| 6 | Rainbow Ray | レインボーレイ | battle | enemy group | 6th element |
| 6 | Sun Ray | サンレイ | battle | enemy group | Holy |
| 6 | Astral Gate | アストラルゲート | battle | enemy group | Holy |
| 6 | Dissolve | ディゾルヴ | battle | one enemy | 6th element |
| 7 | Nuclear Blast | ニュークリアブラスト | battle | all enemies | Fire |
| 7 | Teleport | テレポート | battle+camp | party | 6th element |
| 7 | Anti-Magic Shell | アンチマジックシェル | battle | party | 6th element |
| 7 | Wish | ウィッシュ | battle | none | 6th element |

### 3.2 Priest spells (そうりょの じゅもん)

| Lv | Spell | JP | Where | Target (inferred) | Element (inferred) |
|---|---|---|---|---|---|
| 1 | Restore | レストア | battle+camp | one ally | Holy |
| 1 | Light | ライト | camp | none | None |
| 1 | Remove Fear | リムーブフィアー | battle+camp | one ally | Spirit |
| 1 | Iron Body | アイアンボディ | battle | one ally | 6th element |
| 2 | Healing | ヒーリング | battle+camp | one ally | Holy |
| 2 | Silence | サイレンス | battle | enemy group | Wind |
| 2 | Yell | エール | battle | party | Spirit |
| 2 | Wake Up | ウェイクアップ | battle | one ally | Spirit |
| 2 | Search Person | サーチパーソン | camp | none | None |
| 3 | Cure Paralysis | キュアパラライズ | battle+camp | one ally | Holy |
| 3 | Encyclopedia | エンサイクロペディア | battle+camp | party | None |
| 3 | Continual Light | コンティニュアルライト | camp | none | None |
| 3 | Inspect | インスペクト | chest | chest | None |
| 3 | Protection | プロテクション | battle | party | 6th element |
| 4 | Cure Poison | キュアポイズン | battle+camp | one ally | Water |
| 4 | Force Field | フォースフィールド | battle+camp | party | Holy |
| 4 | War Cry | ウォークライ | battle | party | Spirit |
| 5 | Recovery | リカバリー | battle+camp | one ally | Holy |
| 5 | Revive | リバイブ | battle+camp | one ally | Holy |
| 5 | Stone to Flesh | フレッシュストーン | battle+camp | one ally | Earth |
| 5 | Death Spell | デススペル | battle | one enemy | 6th element |
| 6 | Magic Armor | マジックアーマー | battle | party | 6th element |
| 6 | Cure All | キュアオール | battle+camp | one ally | Holy |
| 6 | Bless | ブレス | battle | party | None |
| 6 | Recall Word | リコールワード | camp | party | None |
| 7 | Elixir Light | エリクサーライト | battle+camp | party | Holy |
| 7 | Holy Word | ホーリーワード | battle | all enemies | Holy |
| 7 | Resurrection | リザレクション | battle+camp | one ally | Holy |

### 3.3 Valiant Prayers (ヴァリアントの じゅもん)

| Lv | Spell | JP | Where | Target (inferred) | Element (inferred) |
|---|---|---|---|---|---|
| 1 | Healing to Thee | なんじにいやしを | battle+camp | one ally | Holy |
| 1 | Be Thou Whole | なんじすこやかなれ | battle+camp | one ally | Holy |
| 2 | Be Thou Healed | なんじいやされよ | battle+camp | one ally | Holy |
| 2 | Vigor to Thee | なんじにかつりょくを | battle+camp | one ally | Holy |
| 3 | Grace to Thee | なんじにかごあれ | battle | one ally | 6th element |
| 3 | Be Thou Guarded | なんじまもりたもう | battle | one ally | 6th element |
| 4 | Be Ye All Whole | みなすこやかなれ | battle+camp | party | Holy |
| 4 | Might to Thee | なんじにちからを | battle | one ally | Holy |
| 5 | Be Ye All Healed | みないやされよ | battle+camp | party | Holy |
| 5 | Be Ye All Guarded | みなをまもりたもう | battle | party | 6th element |
| 6 | Might to Ye All | みなにちからを | battle | party | Holy |
| 6 | Grace to Ye All | みなにかごあれ | battle | party | 6th element |
| 7 | A Miracle for Thee | なんじきせきあれ | battle+camp | one ally | Holy |
| 7 | O God | かみよ | battle+camp | one ally | Holy |
| 7 | Heaven, Smite Them | てんばつくだされよ | battle | enemy group | Holy |
| 7 | Begone, Evil | あしきちからされ | camp | unexplained | Holy |

### 3.4 Avenger Arts (アベンジャーの じゅもん)

| Lv | Spell | JP | Where | Target (inferred) | Element (inferred) |
|---|---|---|---|---|---|
| 1 | Grudge Aura | うらみのオーラ | battle | caster | 6th element |
| 1 | Blade of Fear | きょうふのけん | battle | one enemy | Spirit |
| 2 | Nightmare Blade | あくむのけん | battle | one enemy | Spirit |
| 2 | Binding Blade | そくばくのけん | battle | one enemy | Spirit |
| 3 | Blade of Enmity | おんしゅうのけん | battle | one enemy | None |
| 3 | Blade of Madness | きょうきのけん | battle | enemy group | Spirit |
| 4 | Hatred Aura | にくしみのオーラ | battle | caster | 6th element |
| 4 | Cursed Blade | のろいのけん | battle | one enemy | Earth |
| 5 | Wrath Aura | いかりのオーラ | battle | caster | 6th element |
| 5 | Life Stealer | いのちうばいしもの | battle | one enemy | 6th element |
| 6 | Vengeance Blade | ふくしゅうのけん | battle | one enemy | None |
| 7 | Hellish Wail | あびきょうかん | battle | enemy group | None |

### 3.5 Musashi Arts (ムサシの じゅもん)

| Lv | Spell | JP | Where | Target (inferred) | Element (inferred) |
|---|---|---|---|---|---|
| 1 | Blunt Strike | みねうち | battle | one enemy | Spirit |
| 1 | Counter Cut | かえすがたな | battle | unexplained (A) | None |
| 2 | Meditation | めいそう | battle+camp | caster | Holy |
| 2 | Triple Slash | さんれんぎり | battle | unexplained | None |
| 3 | Fighting Spirit | きこん | battle | enemy group | Spirit |
| 3 | Four Lights Cut | よんこうざん | battle | unexplained | None |
| 4 | Blade Lock | つばぜりあい | battle | caster | 6th element |
| 4 | Rainfall Slash | さみだれぎり | battle | unexplained | None |
| 5 | Whirl Slash | たてまわり | battle | enemy group | None |
| 6 | Read the Blade | みきり | battle | caster | 6th element |
| 6 | Mind's Eye Blade | しんがんのけん | battle | one enemy | None |
| 7 | Wild Dance Blade | らんぶのけん | battle | all enemies | None |

### 3.6 Kunoichi Arts (くのいちの じゅもん)

| Lv | Spell | JP | Where | Target (inferred) | Element (inferred) |
|---|---|---|---|---|---|
| 1 | Trap Breaker | からくりやぶり | chest | chest | None |
| 1 | Illusion | げんかく | battle | one enemy | Spirit |
| 2 | Substitution | かわりみ | battle | one ally | 6th element |
| 2 | Hunger Pill | きかつがん | battle+camp | one ally | Holy |
| 3 | Smokescreen | えんまく | battle | all enemies | None |
| 3 | Sleep Powder | ねむりごな | battle | enemy group | Spirit |
| 4 | Fire Art | かとん | battle | enemy group | Fire |
| 4 | Shadow Dance | かげまい | battle | one enemy | None |
| 5 | Numbing Drug | しびれぐすり | battle | enemy group | Spirit |
| 5 | Shadow Double | かげぼうし | battle | one ally | 6th element |
| 6 | Mist Slash | かすみぎり | battle | unexplained (A) | None |
| 6 | Izuna Drop | いずなおとし | battle | one enemy | None |
| 7 | Thunder | いかづち | battle | all enemies | Wind |

### 3.7 Summons (しょうかんしの じゅもん)

| Lv | Spell | JP | Where | Target (inferred) | Element (inferred) |
|---|---|---|---|---|---|
| 1 | Zombie | ゾンビ | battle+camp | none | 6th element |
| 1 | Ghoul | グール | battle+camp | none | 6th element |
| 2 | Lion of Hell | ライオン オブ ヘル | battle+camp | none | 6th element |
| 2 | Minotaur | ミノタウロス | battle+camp | none | 6th element |
| 3 | Djinni | ジィニー | battle+camp | none | Wind |
| 3 | Ifrit | イフリート | battle+camp | none | Fire |
| 4 | Dao | ダオ | battle+camp | none | Earth |
| 4 | Marid | マリッド | battle+camp | none | Water |
| 5 | Titan | タイタン | battle+camp | none | None |
| 5 | Greater Demon | グレーターデーモン | battle+camp | none | 6th element |
| 6 | Vampire Lord | ヴァンパイアロード | battle+camp | none | 6th element |
| 6 | Shadow Dragon | シャドウドラゴン | battle+camp | none | Holy |
| 7 | Magic Gate | まどうゲート | battle+camp | none | None |
| 7 | Ancient One | いにしえからのもの | battle+camp | none | None |
| 7 | From Beyond | かなたよりのもの | battle+camp | none | None |
| 7 | Unspeakable | けいようしがたきもの | battle+camp | none | None |

**Notes:** the summons share their names with monsters (one name per creature, [glossary](../../glossary.md)).
"(A)" marks the one unexplained target kind that two spells share (Counter Cut, Mist Slash).

Tech: [characters.md §10.2](../tech/characters.md#102-spell-lists)

---

## 4. Learning spells

A caster learns spells in two ways at every level-up (and once at creation): a guaranteed spell when a new spell
level opens, and a chance at every spell still missing. Summoners use neither (section 6).

### 4.1 The guaranteed spell

When the character reaches **exactly** the opening level of a spell level (section 1), it learns **one spell of that
spell level, picked at random**. If the pick is a spell it already knows, it gains nothing. No stat affects this
spell, for any class. "Exactly" matters: the spell is given on that level-up only, not later.

Each spell level thus opens with one spell for certain, then grows through the extra chances. Special rule: if the
guaranteed Priest level-6 spell is **Recall Word**, the character also learns one of Magic Armor, Cure All or Bless
([findings.md](findings.md)).

Tech: [characters.md §10.3](../tech/characters.md#103-learning)

### 4.2 Extra spells

At each level-up, for every spell **not yet known** in every spell level where the character already knows at least
one spell, the game rolls a random number from 0 to 99; the spell is learned if it is below the chance. The chance
comes from a class stat:

| Stat value | 11 or less | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Mage school (IQ), Priest school (PIE) | 5% | 10% | 15% | 20% | 25% | 30% | 35% | 40% | 45% | 50% | 55% | 60% |
| Valiant (PIE) | 5% | 5% | 5% | 5% | 5% | 5% | 5% | 10% | 15% | 20% | 25% | 25% |
| Avenger (VIT) | 5% | 5% | 5% | 5% | 5% | 5% | 5% | 10% | 15% | 15% | 20% | 25% |
| Musashi (VIT) | 5% | 5% | 5% | 5% | 5% | 5% | 5% | 7% | 12% | 12% | 15% | 20% |
| Kunoichi (LUK) | 5% | 5% | 5% | 5% | 5% | 5% | 5% | 5% | 7% | 7% | 7% | 12% |

A Mage with IQ 18 thus has 40% per missing spell per level-up; a Kunoichi rarely gets more than the guaranteed
spells.

**Notes:**
- Mage spells use IQ and Priest spells use PIE for every class, Bishops included.
- A stat above 22 has no entry of its own; the game then uses the next class's row (IQ 23 would give the Valiant
  value, 5%). By the race limits ([characters.md](characters.md#1-races)) only a Hobbit can have a stat above 22
  (LUK 23-24), so only a Hobbit Kunoichi is affected (computed). See [findings.md](findings.md).
- By the same limits, the 20+ columns are reachable only by an Elf (IQ), an Elf, Dwarf or Gnome (PIE), a Dwarf
  (VIT; 21 for a female Dwarf) or a Hobbit (LUK) (computed from the race table).

Tech: [characters.md §10.3](../tech/characters.md#103-learning)

### 4.3 At creation

The learning step runs once for a new character as if it had just reached level 1: a Mage, Priest or Bishop gets one
guaranteed level-1 spell of its school (a Bishop: Mage) plus the extra-spell chance at every other level-1 spell.
Example: the ready-made Bishop starts with Call Fear and Flame Arrow ([characters.md](characters.md#26-ready-made-characters)).

Tech: [characters.md §3.5](../tech/characters.md#35-what-the-new-character-gets), [characters.md §3.6](../tech/characters.md#36-ready-made-characters)

### 4.4 After a class change

- **Mage and Priest spells are kept** through any class change and stay castable (section 5).
- **Special-school spells are lost** when the class changes, together with their slots.
- Change Class at the Training Grounds gives a new Mage, Priest or Bishop its guaranteed level-1 spell at once.
  A class change by item gives no spell; the special schools open at level 5 anyway.
- After that, the new class learns on its own schedule from level 1 ([characters.md](characters.md#34-change-class-training-grounds)).

Tech: [characters.md §10.3](../tech/characters.md#103-learning),
[characters.md §5.4](../tech/characters.md#54-change-class)

---

## 5. Spell slots

Slots are the number of casts per spell level and school, as in classic Wizardry. The camp and status screens show
the remaining casts as "n/n/n/n/n/n/n" (levels 1 to 7).

- **Refill:** every inn night refills all slots, in every room including the free Stables (verified: a stay in the
  Stables at full HP and a Cots stay from 1 HP both refilled them). The only night that does not is one on which the
  character is hurt and cannot pay ([town.md](town.md)).
- Slots are also recomputed at each level-up and class change.

For each school and spell level, with `known` the number of spells the character knows at that level, `L` the
character level and `open` the level at which the class opens that spell level:

```csharp
int Slots(bool classUsesSchool, int known, int L, int open)
{
    if (known == 0) return 0;                                      // nothing known: no casts
    if (classUsesSchool && L >= open)
        return Math.Min(9, Math.Max(known, L - open + 1));         // grows by 1 per level, cap 9
    return known;                                                  // e.g. spells kept from an old class
}
```

Examples:
- **Mage:** level-1 slots equal the character level from 1 to 8, then stay at 9. Level-7 slots appear at character
  level 13 with 1.
- **Samurai:** Mage level-1 slots appear at character level 4 (1 slot) and reach 9 at level 12.
- **A Mage who became a Fighter** keeps one cast per Mage spell known, at each level.

**Notes:** a Summoner's slots follow the same rule with its own opening levels; a pact also raises a spell level that
had 0 slots to 1 straight away (section 6).

Tech: [characters.md §10.4](../tech/characters.md#104-spell-slots),
[characters.md §8](../tech/characters.md#8-inn-rest)

---

## 6. Summoner pacts

The Summoner never learns at level-up. Its 16 summons come from **magic circles** in the maze, one per summon and at
most one per floor.

- Without a Summoner in the party the square only says "A strange pattern is drawn on the ground".
- With a Summoner who is OK, Afraid or Asleep, the game asks who will step inside the circle; only a Summoner can be
  picked. The summon then appears by name ("From the pattern's center Zombie appeared! Will you form a pact?"; seen
  with the Zombie circle, verified).
- If the Summoner's level is below the circle's minimum: "Your level is too low. The summoning failed."
- If the pact already exists: "A pact already exists."
- Otherwise the Summoner learns that summon ("The pact is sealed."; verified). If its spell level had 0 slots, it
  gets 1 now.

| Floor | Square (x, y) | Summon (JP) | Minimum Summoner level | Spell level |
|---|---|---|---|---|
| 1 | (15, 15) | Zombie (ゾンビ) | 3 | 1 |
| 3 | (4, 0) | Ghoul (グール) | 4 | 1 |
| 5 | (15, 9) | Lion of Hell (ライオン オブ ヘル) | 6 | 2 |
| 8 | (3, 8) | Minotaur (ミノタウロス) | 10 | 2 |
| 9 | (11, 5) | Djinni (ジィニー) | 14 | 3 |
| 12 | (8, 15) | Ifrit (イフリート) | 15 | 3 |
| 13 | (9, 3) | Dao (ダオ) | 16 | 4 |
| 14 | (12, 1) | Marid (マリッド) | 17 | 4 |
| 15 | (0, 2) | Titan (タイタン) | 20 | 5 |
| 18 | (15, 13) | Greater Demon (グレーターデーモン) | 23 | 5 |
| 21 | (0, 3) | Vampire Lord (ヴァンパイアロード) | 27 | 6 |
| 23 | (13, 3) | Shadow Dragon (シャドウドラゴン) | 31 | 6 |
| 24 | (7, 15) | Magic Gate (まどうゲート) | 34 | 7 |
| 26 | (12, 3) | Ancient One (いにしえからのもの) | 36 | 7 |
| 29 | (11, 1) | From Beyond (かなたよりのもの) | 37 | 7 |
| 30 | (7, 15) | Unspeakable (けいようしがたきもの) | 38 | 7 |

The minimum level of the first summon of each spell level (3, 6, 14, 16, 20, 27, 34) is also the level at which the
Summoner's slots for that spell level open (section 1). Floors 21-30 are a separate, harder area
([dungeon.md](dungeon.md)).

**Notes:** how a summon behaves in battle (the summoned creature, its strength, how long it stays) was not traced.

Tech: [characters.md §10.5](../tech/characters.md#105-summoner-pacts),
[monsters.md §8](../tech/monsters.md#8-summoner-pacts),
[dungeon.md §4](../tech/dungeon.md#4-floors)

---

## Open questions

- **Spell effects:** damage dice, durations and success rolls of every spell were not traced; neither was which
  spells cure which status or raise the dead ([characters.md](characters.md#6-status-ailments-and-cures)).
- **Target and element** are readings of the spell data from the pattern of names; six target kinds (used by Counter
  Cut, Mist Slash, Triple Slash, Four Lights Cut, Rainfall Slash, Dispel Magic and Begone, Evil) are unexplained.
- **Casting cost:** "one slot of the spell's level" is unconfirmed in play.
- **Kunoichi with LUK 23-24:** the extra-spell chance then comes from past the end of the table; those values were
  not read.
- **Extra spells after a class change:** whether a character of a non-casting class who still knows Mage or Priest
  spells keeps rolling extra-spell chances at level-up is unconfirmed.
- **Summons in battle:** the Summoner's battle command and what a summon does were not traced.
