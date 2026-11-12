# Spells: schools, the spell list, learning, slots, Summoner pacts

How magic works in Wizardry Empire: who casts which school, every spell, how spells are learned, how many casts a
character has, and how the Summoner gains summons. Character classes, leveling and statuses are in
[characters.md](characters.md); how a spell gets through a monster's resistance is in [combat.md](combat.md); items
that cast spells are in [items.md](items.md). Notation (dice, stats, confidence tags): [README.md](README.md).

`Rnd(a, b)` below is a random whole number from a to b, both included.

## Overview

- **125 spells in 7 schools**, each with 7 spell levels: Mage 28 and Priest 28 (the classic schools), and one school
  per special class: Valiant Prayers 16, Avenger Arts 12, Musashi Arts 12, Kunoichi Arts 13, Summons 16.
- **Who casts:** Mage, Priest and Bishop from level 1; Samurai (Mage spells) and Lord (Priest spells) from level 4;
  the special classes from level 5 (Summoner from level 3). Fighter, Thief, Ninja and Archer cast nothing.
- **Learning:** each spell level opens at a fixed character level per class. On exactly that level the character
  learns **one guaranteed random spell** of the new spell level. At every level-up it also gets a stat-based chance
  (IQ, PIE, VIT or LUK; 5% to 60%) at each missing spell of the spell levels it has started.
- **Summoners never learn at level-up:** they form **pacts** at 16 magic circles in the maze, each with a minimum
  level from 3 to 38.
- **Spell slots** (casts per spell level, refilled by any inn stay):
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

The counts for the five special schools are counted from the spell lists in section 3.

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
[characters.md §10.1](../tech/characters.md#101-the-spell-record)

---

## 2. Casting

- **Cost:** a cast uses one slot of the spell's level (inferred: the exact place where the game takes the slot was
  not pinned down). Slots are counted per school and per spell level (section 5).
- **Where:** each spell is marked for use in battle, in camp, both, or at a chest (for chest spells: checking or
  disarming a trap, by name). The camp marks match the crosses the game shows on its camp spell screen; the battle
  and chest marks are read from the same data (inferred).
- **Target** (one enemy, an enemy group, all enemies, the caster, one ally, the party, a chest, or none) and
  **element** are read from the spell data; both meanings are guesses from the pattern of names (inferred). Some
  target codes are unexplained: four used by Musashi and Kunoichi sword arts, plus those of Dispel Magic and
  Begone, Evil.
- **Element and resistance:** the element is the kind of resistance a monster uses against the spell. Monsters have 8
  resistances; how the spell's power is set against them is in [combat.md](combat.md). The two documents name the
  elements differently; matched by position (element n = the n-th resistance, inferred):

  | Element here | Monster resistance column ([monsters_table.md](monsters_table.md)) |
  |---|---|
  | earth | Earth |
  | water/cold | Water |
  | fire | Fire |
  | air/lightning | Wind |
  | mind | Spirit |
  | arcane | (6th, unnamed) |
  | holy/life | Holy |
  | none | None |

**Notes:** spell items (potions, staves, rings that cast a spell) are in [items.md](items.md). The success roll of
a raising spell (age, the patient's VIT, the caster's PIE) is with the other cures in
[characters.md](characters.md#6-status-ailments-and-cures).

Tech: [characters.md §10.1](../tech/characters.md#101-the-spell-record),
[monsters.md §5](../tech/monsters.md#5-party-attacks-and-spells-on-monsters)

---

## 3. The spell list

All 125 spells by school and level. **Where** is from the spell data. **Target** and **Element** are readings of the
data (inferred, section 2). The effects (damage, duration, success chance) were not traced; the name is the only
guide for now.

### 3.1 Mage spells (まほうつかいの じゅもん)

| Lv | Spell | JP | Where | Target (inferred) | Element (inferred) |
|---|---|---|---|---|---|
| 1 | Call Fear | コールフィアー | battle | enemy group | mind |
| 1 | Shield | シールド | battle | caster | arcane |
| 1 | Flame Arrow | フレイムアロー | battle | one enemy | fire |
| 1 | Compass | コンパス | camp | none / field | none |
| 2 | Sleep | スリープ | battle | enemy group | mind |
| 2 | Lightning Bolt | ライトニングボルト | battle | enemy group | air/lightning |
| 2 | Darkness | ダークネス | battle | enemy group | none |
| 3 | Fireball | ファイアボール | battle | enemy group | fire |
| 3 | Missile Shield | ミサイルシールド | battle | party | air/lightning |
| 3 | Striking | ストライキング | battle | one ally | none |
| 3 | Hold Ray | ホールドレイ | battle | enemy group | mind |
| 4 | Ice Storm | アイスストーム | battle | enemy group | water/cold |
| 4 | Explosion | エクスプロージョン | battle | all enemies | fire |
| 4 | Levitate | レビテート | camp | party | arcane |
| 5 | Thunderbolt | サンダーボルト | battle | all enemies | air/lightning |
| 5 | Stone Ray | ストーンレイ | battle | enemy group | earth |
| 5 | Dispel Magic | ディスペルマジック | battle+camp | unknown (code 11) | arcane |
| 5 | Magic Screen | マジックスクリーン | battle | party | arcane |
| 6 | Frost Blizzard | フロストブリザード | battle | enemy group | water/cold |
| 6 | Earthquake | アースクウェイク | battle | all enemies | earth |
| 6 | Rainbow Ray | レインボーレイ | battle | enemy group | arcane |
| 6 | Sun Ray | サンレイ | battle | enemy group | holy/life |
| 6 | Astral Gate | アストラルゲート | battle | enemy group | holy/life |
| 6 | Dissolve | ディゾルヴ | battle | one enemy | arcane |
| 7 | Nuclear Blast | ニュークリアブラスト | battle | all enemies | fire |
| 7 | Teleport | テレポート | battle+camp | party | arcane |
| 7 | Anti-Magic Shell | アンチマジックシェル | battle | party | arcane |
| 7 | Wish | ウィッシュ | battle | none / field | arcane |

### 3.2 Priest spells (そうりょの じゅもん)

| Lv | Spell | JP | Where | Target (inferred) | Element (inferred) |
|---|---|---|---|---|---|
| 1 | Restore | レストア | battle+camp | one ally | holy/life |
| 1 | Light | ライト | camp | none / field | none |
| 1 | Remove Fear | リムーブフィアー | battle+camp | one ally | mind |
| 1 | Iron Body | アイアンボディ | battle | one ally | arcane |
| 2 | Healing | ヒーリング | battle+camp | one ally | holy/life |
| 2 | Silence | サイレンス | battle | enemy group | air/lightning |
| 2 | Yell | エール | battle | party | mind |
| 2 | Wake Up | ウェイクアップ | battle | one ally | mind |
| 2 | Search Person | サーチパーソン | camp | none / field | none |
| 3 | Cure Paralysis | キュアパラライズ | battle+camp | one ally | holy/life |
| 3 | Encyclopedia | エンサイクロペディア | battle+camp | party | none |
| 3 | Continual Light | コンティニュアルライト | camp | none / field | none |
| 3 | Inspect | インスペクト | chest | chest | none |
| 3 | Protection | プロテクション | battle | party | arcane |
| 4 | Cure Poison | キュアポイズン | battle+camp | one ally | water/cold |
| 4 | Force Field | フォースフィールド | battle+camp | party | holy/life |
| 4 | War Cry | ウォークライ | battle | party | mind |
| 5 | Recovery | リカバリー | battle+camp | one ally | holy/life |
| 5 | Revive | リバイブ | battle+camp | one ally | holy/life |
| 5 | Stone to Flesh | フレッシュストーン | battle+camp | one ally | earth |
| 5 | Death Spell | デススペル | battle | one enemy | arcane |
| 6 | Magic Armor | マジックアーマー | battle | party | arcane |
| 6 | Cure All | キュアオール | battle+camp | one ally | holy/life |
| 6 | Bless | ブレス | battle | party | none |
| 6 | Recall Word | リコールワード | camp | party | none |
| 7 | Elixir Light | エリクサーライト | battle+camp | party | holy/life |
| 7 | Holy Word | ホーリーワード | battle | all enemies | holy/life |
| 7 | Resurrection | リザレクション | battle+camp | one ally | holy/life |

### 3.3 Valiant Prayers (ヴァリアントの じゅもん)

| Lv | Spell | JP | Where | Target (inferred) | Element (inferred) |
|---|---|---|---|---|---|
| 1 | Healing to Thee | なんじにいやしを | battle+camp | one ally | holy/life |
| 1 | Be Thou Whole | なんじすこやかなれ | battle+camp | one ally | holy/life |
| 2 | Be Thou Healed | なんじいやされよ | battle+camp | one ally | holy/life |
| 2 | Vigor to Thee | なんじにかつりょくを | battle+camp | one ally | holy/life |
| 3 | Grace to Thee | なんじにかごあれ | battle | one ally | arcane |
| 3 | Be Thou Guarded | なんじまもりたもう | battle | one ally | arcane |
| 4 | Be Ye All Whole | みなすこやかなれ | battle+camp | party | holy/life |
| 4 | Might to Thee | なんじにちからを | battle | one ally | holy/life |
| 5 | Be Ye All Healed | みないやされよ | battle+camp | party | holy/life |
| 5 | Be Ye All Guarded | みなをまもりたもう | battle | party | arcane |
| 6 | Might to Ye All | みなにちからを | battle | party | holy/life |
| 6 | Grace to Ye All | みなにかごあれ | battle | party | arcane |
| 7 | A Miracle for Thee | なんじきせきあれ | battle+camp | one ally | holy/life |
| 7 | O God | かみよ | battle+camp | one ally | holy/life |
| 7 | Heaven, Smite Them | てんばつくだされよ | battle | enemy group | holy/life |
| 7 | Begone, Evil | あしきちからされ | camp | unknown (code 13) | holy/life |

### 3.4 Avenger Arts (アベンジャーの じゅもん)

| Lv | Spell | JP | Where | Target (inferred) | Element (inferred) |
|---|---|---|---|---|---|
| 1 | Grudge Aura | うらみのオーラ | battle | caster | arcane |
| 1 | Blade of Fear | きょうふのけん | battle | one enemy | mind |
| 2 | Nightmare Blade | あくむのけん | battle | one enemy | mind |
| 2 | Binding Blade | そくばくのけん | battle | one enemy | mind |
| 3 | Blade of Enmity | おんしゅうのけん | battle | one enemy | none |
| 3 | Blade of Madness | きょうきのけん | battle | enemy group | mind |
| 4 | Hatred Aura | にくしみのオーラ | battle | caster | arcane |
| 4 | Cursed Blade | のろいのけん | battle | one enemy | earth |
| 5 | Wrath Aura | いかりのオーラ | battle | caster | arcane |
| 5 | Life Stealer | いのちうばいしもの | battle | one enemy | arcane |
| 6 | Vengeance Blade | ふくしゅうのけん | battle | one enemy | none |
| 7 | Hellish Wail | あびきょうかん | battle | enemy group | none |

### 3.5 Musashi Arts (ムサシの じゅもん)

| Lv | Spell | JP | Where | Target (inferred) | Element (inferred) |
|---|---|---|---|---|---|
| 1 | Blunt Strike | みねうち | battle | one enemy | mind |
| 1 | Counter Cut | かえすがたな | battle | unknown (code 2) | none |
| 2 | Meditation | めいそう | battle+camp | caster | holy/life |
| 2 | Triple Slash | さんれんぎり | battle | unknown (code 3) | none |
| 3 | Fighting Spirit | きこん | battle | enemy group | mind |
| 3 | Four Lights Cut | よんこうざん | battle | unknown (code 4) | none |
| 4 | Blade Lock | つばぜりあい | battle | caster | arcane |
| 4 | Rainfall Slash | さみだれぎり | battle | unknown (code 5) | none |
| 5 | Whirl Slash | たてまわり | battle | enemy group | none |
| 6 | Read the Blade | みきり | battle | caster | arcane |
| 6 | Mind's Eye Blade | しんがんのけん | battle | one enemy | none |
| 7 | Wild Dance Blade | らんぶのけん | battle | all enemies | none |

### 3.6 Kunoichi Arts (くのいちの じゅもん)

| Lv | Spell | JP | Where | Target (inferred) | Element (inferred) |
|---|---|---|---|---|---|
| 1 | Trap Breaker | からくりやぶり | chest | chest | none |
| 1 | Illusion | げんかく | battle | one enemy | mind |
| 2 | Substitution | かわりみ | battle | one ally | arcane |
| 2 | Hunger Pill | きかつがん | battle+camp | one ally | holy/life |
| 3 | Smokescreen | えんまく | battle | all enemies | none |
| 3 | Sleep Powder | ねむりごな | battle | enemy group | mind |
| 4 | Fire Art | かとん | battle | enemy group | fire |
| 4 | Shadow Dance | かげまい | battle | one enemy | none |
| 5 | Numbing Drug | しびれぐすり | battle | enemy group | mind |
| 5 | Shadow Double | かげぼうし | battle | one ally | arcane |
| 6 | Mist Slash | かすみぎり | battle | unknown (code 2) | none |
| 6 | Izuna Drop | いずなおとし | battle | one enemy | none |
| 7 | Thunder | いかづち | battle | all enemies | air/lightning |

### 3.7 Summons (しょうかんしの じゅもん)

| Lv | Spell | JP | Where | Target (inferred) | Element (inferred) |
|---|---|---|---|---|---|
| 1 | Zombie | ゾンビ | battle+camp | none / field | arcane |
| 1 | Ghoul | グール | battle+camp | none / field | arcane |
| 2 | Lion of Hell | ライオン オブ ヘル | battle+camp | none / field | arcane |
| 2 | Minotaur | ミノタウロス | battle+camp | none / field | arcane |
| 3 | Djinni | ジィニー | battle+camp | none / field | air/lightning |
| 3 | Ifrit | イフリート | battle+camp | none / field | fire |
| 4 | Dao | ダオ | battle+camp | none / field | earth |
| 4 | Marid | マリッド | battle+camp | none / field | water/cold |
| 5 | Titan | タイタン | battle+camp | none / field | none |
| 5 | Greater Demon | グレーターデーモン | battle+camp | none / field | arcane |
| 6 | Vampire Lord | ヴァンパイアロード | battle+camp | none / field | arcane |
| 6 | Shadow Dragon | シャドウドラゴン | battle+camp | none / field | holy/life |
| 7 | Magic Gate | まどうゲート | battle+camp | none / field | none |
| 7 | Ancient One | いにしえからのもの | battle+camp | none / field | none |
| 7 | From Beyond | かなたよりのもの | battle+camp | none / field | none |
| 7 | Unspeakable | けいようしがたきもの | battle+camp | none / field | none |

**Notes:** the summons share their names with monsters (one name per creature, [glossary](../../glossary.md)).

Tech: [characters.md §10.2](../tech/characters.md#102-spell-lists)

---

## 4. Learning spells

A caster learns spells in two ways at every level-up (and once at creation): a guaranteed spell when a new spell
level opens, and a chance at every spell still missing. Summoners use neither (section 6).

### 4.1 The guaranteed spell

When the character reaches **exactly** the opening level of a spell level (section 1), it learns **one random spell
of that spell level**. "Exactly" matters: the spell is given on that level-up only, not later.

```csharp
if (newLevel == openingLevel[spellLevel])
    Learn(spellsOf(school, spellLevel)[Rnd(0, count - 1)]);   // a spell already known: nothing gained
```

Each spell level opens with one spell for certain, then grows through the extra chances. Special rule: if the
guaranteed Priest level-6 spell is **Recall Word**, the character also learns one of Magic Armor, Cure All or Bless.

Tech: [characters.md §10.3](../tech/characters.md#103-learning)

### 4.2 Extra spells

At each level-up, for every spell **not yet known** in every spell level where the character already knows at least
one spell, the game rolls `Rnd(0, 99) < chance`. The chance comes from a class stat:

| Stat value | 11 or less | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Mage school (IQ), Priest school (PIE) | 5 | 10 | 15 | 20 | 25 | 30 | 35 | 40 | 45 | 50 | 55 | 60 |
| Valiant (PIE) | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 10 | 15 | 20 | 25 | 25 |
| Avenger (VIT) | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 10 | 15 | 15 | 20 | 25 |
| Musashi (VIT) | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 7 | 12 | 12 | 15 | 20 |
| Kunoichi (LUK) | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 7 | 7 | 7 | 12 |

Values in percent. A Mage with IQ 18 thus has 40% per missing spell per level-up; a Kunoichi rarely gets more than
the guaranteed spells.

**Notes:**
- Bishops use IQ for Mage spells and PIE for Priest spells.
- Stats above 22 read past the end of the table into the next row (e.g. IQ 23 would read the Valiant row: 5%). By
  the race limits ([characters.md](characters.md#1-races)) no character has IQ or PIE above 20, so only a Hobbit
  Kunoichi with LUK 23-24 runs past the last row, into unknown values. See [findings.md](findings.md).
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
the remaining casts as "n/n/n/n/n/n/n" (levels 1 to 7). All slots refill at any inn stay, the free Stables included
([town.md](town.md)); they are also recomputed at each level-up and class change.

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

Tech: [characters.md §10.4](../tech/characters.md#104-spell-slots)

---

## 6. Summoner pacts

The Summoner never learns at level-up. Its 16 summons come from **magic circles** in the maze, one per summon and at
most one per floor. A Summoner (who can still act) steps inside the circle; the game shows a monster in the circle
("From the pattern's center ... appeared! Will you form a pact?").

- If the Summoner's level is below the circle's minimum: "Your level is too low. The summoning failed."
- If the pact already exists: "A pact already exists."
- Otherwise the Summoner learns that summon ("The pact is sealed."). If its spell level had 0 slots, it gets 1 now.
- Without a Summoner in the party the square only says "A strange pattern is drawn on the ground".

| Floor | Summon (JP) | Minimum Summoner level | Spell level |
|---|---|---|---|
| 1 | Zombie (ゾンビ) | 3 | 1 |
| 3 | Ghoul (グール) | 4 | 1 |
| 5 | Lion of Hell (ライオン オブ ヘル) | 6 | 2 |
| 8 | Minotaur (ミノタウロス) | 10 | 2 |
| 9 | Djinni (ジィニー) | 14 | 3 |
| 12 | Ifrit (イフリート) | 15 | 3 |
| 13 | Dao (ダオ) | 16 | 4 |
| 14 | Marid (マリッド) | 17 | 4 |
| 15 | Titan (タイタン) | 20 | 5 |
| 18 | Greater Demon (グレーターデーモン) | 23 | 5 |
| 21 | Vampire Lord (ヴァンパイアロード) | 27 | 6 |
| 23 | Shadow Dragon (シャドウドラゴン) | 31 | 6 |
| 24 | Magic Gate (まどうゲート) | 34 | 7 |
| 26 | Ancient One (いにしえからのもの) | 36 | 7 |
| 29 | From Beyond (かなたよりのもの) | 37 | 7 |
| 30 | Unspeakable (けいようしがたきもの) | 38 | 7 |

The minimum level of the first summon of each spell level (3, 6, 14, 16, 20, 27, 34) is also the level at which the
Summoner's slots for that spell level open (section 1). The exact square of each circle is in
[dungeon.md](dungeon.md); floors 21-30 are a separate, harder area.

**Notes:**
- Which monster is *shown* in the circle is not settled: the tech notes name the pact by its summon spell in one place
  and by a bestiary monster with the same number in another (see Open questions). The summon learned is the spell in
  the table above.
- How a summon behaves in battle (the summoned creature, its strength, how long it stays) was not traced.

Tech: [characters.md §10.5](../tech/characters.md#105-summoner-pacts),
[monsters.md §8](../tech/monsters.md#8-summoner-pacts),
[dungeon.md §4](../tech/dungeon.md#4-floors)

---

## Open questions

- **Spell effects:** damage dice, durations and success rolls of every spell were not traced; neither was which
  spells cure which status or raise the dead ([characters.md](characters.md#6-status-ailments-and-cures)).
- **Target and element** are readings of the spell data from the pattern of names; target codes 2, 3, 4, 5, 11 and
  13 are unexplained.
- **Casting cost:** "one slot of the spell's level" is the reading of the code, but the exact place was not
  confirmed.
- **Bishop guaranteed spell:** the tech notes say a Bishop's guaranteed roll for both schools is made "with IQ";
  since that spell is guaranteed, what IQ changes there is unclear.
- **Kunoichi with LUK 23-24:** the extra-spell chance reads past the end of the table; the values found there were
  not listed.
- **Pact monster:** characters notes give the pact as the summon spell (Zombie ... Unspeakable); the monsters notes
  name the same numbers from the bestiary (Undead Beholder ... Damned). The learned spell is not in doubt; what the
  circle shows, and whether the bestiary names are a mix-up, needs a check in the game.
- **Summons in battle:** the Summoner's battle command and what a summon does were not traced.
