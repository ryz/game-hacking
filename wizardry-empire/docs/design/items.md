# Items (Wizardry Empire, GBC, 1999)

How items work for the player: what each item stat means, where items are equipped and by whom, curses and
alignment locks, using items in battle and in camp, special powers, and identification. Every item with its stats is
in the generated table [items_table.md](items_table.md). Prices and the shop, inn and temple are in
[town.md](town.md); the combat formulas behind weapon numbers are in [combat.md](combat.md). Notation and confidence
tags: [README.md](README.md). Untagged numbers are (data).

## Overview

- **224 fixed item types** (data). An item never varies: no random enchantments, no durability, no "+1" rolls. Two
  Long Swords are always identical.
- **Inventory:** each character carries **8 items** (data). Besides the item itself, a slot only remembers four
  things: equipped, stuck (cursed), unidentified, and worn in the off hand (data).
- **Six equipment slots:** Weapon, Off-hand, Armor, Helm, Gloves, Other (data). Each item lists the classes allowed
  to equip it; two-handed weapons leave the off hand empty, launchers take matching ammo there, and only the
  **Musashi** can dual-wield (data).
- **Curses and alignment:** equipping a cursed item, or an item your alignment is not allowed, makes it **stick**:
  it cannot be taken off (data). 36 items are cursed, and 17 of them also drain HP while worn (counted from the item
  table). The **Avenger** class is immune to both locks and to the drain (data).
- **Using items:** potions, scrolls, staves, rods and some rings cast a spell, in battle, in camp or both, with a
  per-item **chance to break** after each use (Healing Potion 100%, Staff of Healing 25%) (data). Some weapons and
  potions can be **thrown** and come back with a per-item chance (data).
- **Special powers:** a handful of items do something permanent when their power is used: Luck +1, age −1 year, or
  a change of class. Five legendary items are the **only way** to reach the five special classes (data).
- **Identification:** items found in chests are unidentified and show a generic name ("Sword", "Ring") (data). The
  shop identifies for a fee and never fails (data); in camp the chance is `(6 + identifier level − item level) / 20`,
  and a failure can make the identifier Afraid (data).

---

## What an item is

Every item is one fixed record. The player sees its stats on the museum page and in the shop; the table below
explains each column of [items_table.md](items_table.md) in play terms.

| Column | What it means in play | Values |
|---|---|---|
| Slot | Where it is equipped (see [Equipment slots](#equipment-slots-and-class-restrictions)) | one-handed weapon, two-handed weapon, parry dagger, bow, crossbow, sling, arrows, quarrels, sling stones, body armour (robes too), shield, helm, gloves, other (accessories and consumables) |
| Unid. name | Name shown while the item is unidentified; also picks the attack verb in battle | a list of 25 generic names (see [Identification](#identification)) |
| Damage | Damage per hit, rolled again on every swing, written `NdS+B` with its min-max | Hand Axe 2-7 (1d6+1), Crescent Axe 24-42 (2d10+22) |
| Swings+ | Extra attacks per round on top of the class's own count; only the main-hand weapon counts | daggers +2 to +6, Swift Sword +7 |
| Hit+ | Makes hitting easier: each point is one step on the 20-sided hit roll, i.e. 5% more chance to hit (computed from the d20 roll), inside the game's 5%-95% limits | mostly 0-8; 47-50 on 20 weapons (see Notes) |
| AC | Added to the wearer's armour class, summed over everything equipped; negative is better | Demon Armor −12, Main Gauche −1 |
| Range | S, M, L or "-" | which enemy groups each range reaches is an open question |
| Throw (keep %) | The item can be thrown with the Throw command; the number is the chance it comes back | Hand Axe 70, Shuriken 95, potions 0 |
| Classes | The classes allowed to equip it | see [Equipment slots](#equipment-slots-and-class-restrictions) |
| Align | Alignments (Good, Neutral, Evil) that may equip it **without it sticking** | "any" on most items |
| Curse | Cursed items stick when equipped | 36 items |
| Price | Shop price; selling, identifying and uncursing cost half (see [town.md](town.md#shop)) | 10 (Arrow, Short Sword) to 5,000,000 (Ura Muramasa) |
| Use (break %) | Spell the item casts when used, where it can be used, and the chance it breaks after a use | see [Spell items](#spell-items) |
| Special | A passive property while equipped, a throw effect, or a special power | see [Equipped effects](#equipped-effects) and [Special powers](#special-powers) |
| HP/step | HP regained (or lost, if negative) for every step walked while equipped | Ring of Healing +5, Garb of Lords +3, Demon Gloves −5 |
| Lv | Item level, 1-15: how hard it is to identify | 1 for starter gear, 15 for the top items |

Example row (Hand Axe, quoted from [items_table.md](items_table.md)):

| # | English | Japanese | Slot | Damage | Range | Throw (keep %) | Classes | Price | Lv | Shop |
|---|---|---|---|---|---|---|---|---|---|---|
| 0 | Hand Axe | ハンドアックス | 1H weapon | 2-7 (1d6+1) | S | 70 | Fig Sam Lor Nin Val Mus Kun | 60 | 1 | unlimited |

Read: a one-handed axe for the fighting classes, 2-7 damage per hit, can be thrown and comes back 70% of the time,
60 G at the shop, always in stock.

**Notes:**
- Damage, swings, hit and AC are explained here as item stats; how they combine with the character's class, level
  and Strength into a hit chance and damage is in [combat.md](combat.md).
- The weapon's swing bonus is read from the **main-hand weapon only** (data); see
  [combat.md](combat.md#party-attacks-swings-per-round).
- 20 weapons (Battle Axe, Great Axe, Chain Sickle, the staves and rods, Shamshir, the whips, Nunchaku, Lance,
  Halberd and others) carry a Hit+ of 47 to 50 instead of 0-8, which puts them at the 95% maximum hit chance (data);
  see [combat.md](combat.md#party-attacks-to-hit) for the rule and whether it is intended.

Tech: [items.md §1](../tech/items.md#1-the-item-record),
[items.md, inventory slot](../tech/items.md#inventory-slot)

---

## Equipment slots and class restrictions

The Equip screen walks through six slots in order. Each slot accepts only certain item types, and every item lists
the classes that may equip it.

| Slot | Accepts | Extra rules |
|---|---|---|
| Weapon | one-handed and two-handed weapons, parry daggers, bows, crossbows, slings | the class must be allowed |
| Off-hand | shield, parry dagger (Main Gauche) | Two-handed weapon in the main hand: nothing. Bow: arrows only. Crossbow: quarrels only. Sling: sling stones only. **Musashi:** may also put a one-handed weapon here (dual wield). |
| Armor | body armour and robes | |
| Helm | helms | |
| Gloves | gloves | |
| Other | one accessory (rings, amulets, cloaks and other odd objects) | |

All rules in this table: (data).

**Class restrictions.** Each item has an allowed/not-allowed mark for each of the 14 classes; an item whose mark is
off for your class cannot be equipped (data). The pattern across the item list (data, counted from the item table):

- Fighter, Lord, Valiant, Ninja and Kunoichi can use nearly every weapon.
- Samurai and Musashi own the katanas but take no shields.
- Priests wear heavy armour and shields but use no edged weapons.
- Mage, Archer and Summoner are limited to robes and light armour.
- The Avenger has a short, special list.
- Rings and odd objects are open to every class.

The per-item lists are the "Classes" column of [items_table.md](items_table.md); the per-class counts are in
[characters.md](characters.md#32-equipment-groups).

**Launchers and ammo.** A bow, crossbow or sling needs its ammo in the off hand. Without it the launcher still
works but every damage die is cut to about a quarter of its size (data; exact rule in
[combat.md](combat.md#party-attacks-damage)). With
ammo, the weapon's slaying property comes from the **ammo**, not the launcher (data): Exorcist Arrows slay undead
from any bow.

**Notes:**
- Changing class takes off all equipment except items that are stuck (data); see
  [characters.md](characters.md#34-change-class-training-grounds).
- In the shop, items the selected character cannot equip are marked (data); see [town.md](town.md#shop).

Tech: [items.md §2](../tech/items.md#2-equipment-rules), [characters.md §5.2](../tech/characters.md#52-equipment-groups)

---

## Curses and alignment locks

Some items stick to the character who equips them. A stuck item cannot be unequipped, so the character carries its
penalties until the shop's Uncurse removes it.

An item sticks when it is equipped and either (data):
- the item is **cursed** (36 items), or
- the character's alignment is not among the item's allowed alignments.

```csharp
bool sticks = item.Cursed || !item.AllowedAlignments.Contains(character.Alignment);
if (character.Class == Class.Avenger) sticks = false;   // the Avenger never gets stuck
```

17 of the 36 cursed items also **drain HP every step** while equipped (counted from the item table). Rows quoted
from [items_table.md](items_table.md):

| # | English | Japanese | Slot | AC | Curse | Price | HP/step | Lv |
|---|---|---|---|---|---|---|---|---|
| 3 | Blood Axe | ブラッドアックス | 2H weapon | | cursed | 25000 | -3 | 10 |
| 121 | Demon Armor | あくまのよろい | Body armor | -12 | cursed | 200000 | -4 | 13 |
| 170 | Demon Gloves | あくまのこて | Gloves | -7 | cursed | 400000 | -5 | 15 |

Several cursed items are strong (Demon Armor is AC −12); for those the curse is a trade: power for a permanent HP
drain and no way to take the item off.

**The Avenger** (a special class) ignores both locks: its items never stick, and negative HP-per-step values do
nothing to it (data). The Avenger Sword is itself cursed but only the Avenger may equip it, so it never sticks in
practice (follows from the two rules above).

**Getting rid of a stuck item.** The shop refuses to buy a cursed item (data). The shop's Uncurse service frees the
character, but **destroys the item** and costs half its price (data); see [town.md](town.md#shop) and
[findings.md](findings.md).

**Notes:**
- The game re-checks alignment on equipped items at some other point and shows a message, but what triggers that
  check is not known (open question).

Tech: [items.md §2](../tech/items.md#2-equipment-rules), [items.md §5](../tech/items.md#5-identification-and-curses)

---

## Using items

### Spell items
Potions, scrolls, staves, rods, stones and some rings and weapons cast a spell when used with the Use command. Each
such item has three properties (data):

- **Effect:** the spell it casts (the "Use" column).
- **Where:** usable in battle, in camp, or both.
- **Break chance:** after **every** use, the item is used up with this chance (100 = always consumed).

Rows quoted from [items_table.md](items_table.md):

| # | English | Japanese | Price | Use (break %) |
|---|---|---|---|---|
| 18 | Staff of Healing | いやしのつえ | 1000 | Healing [battle+camp, mode 9] (breaks 25%) |
| 20 | Rod of Flame | ロッド オブ フレイム | 10000 | Fireball [battle, mode 6] (breaks 10%) |
| 172 | Revival Charm | ふっかつのごふ | 1000000 | Cures death, ashes and even Lost [battle+camp, mode 9] (breaks 100%) |
| 193 | Map Record Sheet | マップきろくシート | 400 | Shows the map [camp, mode 0] (breaks 30%) |
| 194 | Healing Potion | ヒーリングポーション | 100 | Healing [battle+camp, mode 9] (breaks 100%) |
| 202 | Ring of Warping | てんいのゆびわ | 25000 | Teleport [camp, mode 10] (breaks 25%) |

So a Staff of Healing is a reusable healer that lasts 4 uses on average (computed: 1 / 25%), and a Rod of Flame
about 10 (1 / 10%).

**Use mode (inferred).** Each usable item also has a target mode: none, one enemy group, all enemies, one ally,
or the party / the user. This reading comes from which items carry which value and is not confirmed in code. The
table's Use column shows it as "mode N" (0 none, 6 enemy group, 7 all enemies, 9 one ally, 10 party or self).

What each spell effect does (damage, healing amount) is in [spells.md](spells.md); the item side uses the effect
by name only and its power was not traced (open question).

### Throwing
The Throw command in battle throws an item at the enemy (data):
- Only items marked throwable, and only when they are **not equipped**: hand axes, daggers, flails, spears, the
  Gladius, maces, shuriken, Gungnir, Longinus, healing potions and stones, the Exorcism Charm and the Potion of
  Poison.
- After the throw the item comes back with its keep chance (Hand Axe 70%, Shuriken 95%); otherwise it is lost.
  Potions and charms have 0: they are always gone.
- Healing items do damage when thrown at undead (game text): High Heal Potion 32-48, Healing Potion and Healing
  Stone 16-24. The Elixir "can destroy the undead", the Exorcism Charm has a Sun Ray effect, and the Potion of Poison
  poisons the foe (game text). The throw damage code was not traced, so these are the museum's numbers.

### Equipped effects
Some items work simply by being worn. The "Special" column names the effect.

| Effect | Items (examples) | Confidence |
|---|---|---|
| HP per step (positive regenerates, negative drains) | Ring of Healing, Ring of Life +5; Garb of Lords +3; Ring of Death −5; cursed gear −3 to −5 | (data) |
| Double damage on every hit | Clockwork Doll (Ninja, Kunoichi) | (data) |
| Slaying: extra damage against undead, demons, dragons or spirits | Dragonslayer, Exorcist Arrow, Holy Cross Sword, Kris, Odin Sword ... | (data); multipliers in [combat.md](combat.md#slaying-weapons) |
| Critical +10% / +5% | Kunai, Ura Muramasa / Shuriken, Muramasa | (game text) |
| Magic evade 30% / 50% / 85% | Shell Amulet / +1 / +2 | (game text) |
| Drain evade 50% / 10% | Synthesis Stone / Holy Ring | (game text) |
| Water damage ½ | Winter Mittens, Ring of Fire | (game text) |
| Fire damage ½ | Ring of Ice | (game text) |
| "Hide" success +10% | Hider Cloak | (game text) |
| Healing and cure success +50% | Priest Ring | (game text) |
| Teleport | Helm of Warping | (game text) |
| Lets you ride the elevator / meet the twin fairies | Key Card / Fairy's Heart | (game text) |

The (game text) effects are the museum's own descriptions; the code that applies them was not traced (open
question). For HP per step, the museum text says "+5 / −5 HP per step" but the real amount is each item's own
HP/step value (data).

### Special powers
A few items have a power used with "Use its special power?". Using it first **unequips** the item, then applies the
effect, then decides the item's fate (data).

| Item | Japanese | Effect | Item afterwards |
|---|---|---|---|
| Rabbit's Foot | ウサギのあし | Luck +1 (up to the race maximum, base + 10) | always used up |
| Youth Stone | わかがえりのいし | Age −1 year, not below 12 | always used up |
| Thieves' Dagger | シーブズダガー | a **Thief** becomes a **Ninja** (male only) | always used up |
| Butterfly Knife | バタフライナイフ | becomes a **Ninja** (male only) | always used up |
| Guardian Shield | かごのたて | becomes a **Valiant** | 30% vanishes, else becomes the Valiant Shield |
| The Avenger | ジ・アベンジャー | becomes an **Avenger** | 30% vanishes, else becomes the Avenger Sword |
| Warrior's Helm | もののふのかぶと | becomes a **Musashi** | 30% vanishes, else becomes Musashi's Helm |
| Charming Gloves | みわくのこて | becomes a **Kunoichi** (female only) | 30% vanishes, else becomes the Kunoichi Gloves |
| Magic Robe | まどうのローブ | becomes a **Summoner** | 30% vanishes, else becomes the Summoner's Robe |

All values in this table: (data).

- **The five class items** are the only route to the special classes; the Training Grounds never offer them (data).
  The changed item (Valiant Shield, Avenger Sword ...) is the new class's own gear, usable only by that class (data,
  "Classes" column of [items_table.md](items_table.md)). A successful change also unlocks the class's letter in the
  museum (data).
- **What a class change does to the character** (summary; the rules live in
  [characters.md](characters.md#33-special-classes-and-their-items)): level
  1, EXP 0, 1-3 years older, stats reset to the race base raised to the new class's minimums (data).
- **Requirements.** The power checks only gender (Ninja male, Kunoichi female) and, for the Thieves' Dagger, that
  the user is a Thief (data). No stat or alignment check was found; the item's own class and alignment marks may be
  the real gate (inferred, open question).
- **Thieves' Dagger in other hands.** By the order of the code, a non-Thief who uses the power loses the dagger with
  no effect (inferred); see [findings.md](findings.md).

Tech: [items.md §3.1](../tech/items.md#31-spell-items), [§3.2](../tech/items.md#32-throwing-command-throw),
[§3.3](../tech/items.md#33-special-powers),
[characters.md §5.5](../tech/characters.md#55-special-classes-legendary-items)

---

## Identification

Items found in chests ([dungeon.md](dungeon.md)) arrive **unidentified** (data). An unidentified item shows a
generic name instead of its own, and the battle text uses a verb that fits that generic name (data). The list has 25
entries (some repeat): Axe, Arrow, Stone, Scythe, Odd object, Staff, Sword, Dagger, Hammer, Cord, Long staff (two
entries), Staff, Spear, Bow, Armor, Robe, Shield, Helm, Gloves, Odd object, Scroll, Potion, Cloth, Ring (data). Each item's generic name is the "Unid. name"
column of [items_table.md](items_table.md).

An unidentified item **cannot be sold** (data). There are two ways to identify it:

| Where | Chance | Cost | Risk |
|---|---|---|---|
| Lorelei's Shop, Identify | always succeeds | half the item's price ([town.md](town.md#shop)) | none |
| Camp, "Identify what?" | `(6 + L − I) / 20`, see below | free | a failure can make the identifier Afraid |

Which classes may identify in camp was not traced; it is probably the Bishop (inferred).

**Camp identification.** L is the identifier's level (counted as 255 above level 255), I the item level (1-15)
(data).

```csharp
int L = Math.Min(identifier.Level, 255);
int I = item.Level;                              // 1..15
bool success = (L - I >= 14)                     // always succeeds
            || RandomFrom0To(19) < 6 + L - I;    // chance (6 + L - I) / 20, zero once I >= L + 6
```

What that means in play (computed from the formula):

| Identifier level − item level | Chance |
|---|---|
| −6 or less | 0% |
| −5 | 5% |
| 0 | 30% |
| +5 | 55% |
| +10 | 80% |
| +14 or more | 100% |

So a level-1 identifier gets level-1 starter gear 30% of the time and can never identify an item of level 7 or more;
a level-20 identifier has 55% on a level-15 item, and only level 29 makes the top items certain (computed from the
formula).

**Failure.** The game prints "Oops!" and the identifier may turn **Afraid**; the chance falls with Luck (data):

| LUK | <7 | 7-8 | 9-10 | 11-13 | 14-17 | 18-20 | 21-22 | 23 | 24+ |
|---|---|---|---|---|---|---|---|---|---|
| Chance to become Afraid | 20% | 19% | 18% | 17% | 15% | 12% | 10% | 7% | 5% |

Tech: [items.md §5](../tech/items.md#5-identification-and-curses), [items.md §1](../tech/items.md#1-the-item-record)

---

## Open questions

Carried over from the tech reference; nothing here should be read as a rule yet.

1. **Hit+ of 47-50** on 20 weapons: intended or a data slip is not known, and the 95% result is not yet checked in
   the emulator; tracked in [combat.md](combat.md#open-questions).
2. **Range S/M/L:** which enemy groups each range reaches was not traced. Two further range bits (set on most
   two-handed and heavy weapons, daggers and claws, and the Spiked Shield) have no known meaning.
3. **Use mode** of usable items is a reading of the data, not confirmed in code.
4. **Spell power of item effects** and the **throw damage** were not traced; the numbers above are museum text.
5. **Passive specials** (criticals, magic evade, drain evade, elemental halving, Hide, healing bonus, Helm of
   Warping teleport): effects are the museum's descriptions; the code that applies them was not traced.
6. **Class-item requirements:** only gender (and Thief for the Thieves' Dagger) is checked; whether the item's own
   class or alignment marks are the real gate was not tested.
7. **Alignment re-check** on equipped items: what triggers it was not traced.
8. **Camp Identify class gate:** probably the Bishop, not traced.
9. **Equipping unidentified items:** whether an unidentified item can be equipped (and so get stuck unseen) is not
   stated in the tech reference.
10. **Healing Potion in camp:** the tech reference's example lists it as usable in battle only, while the generated
    table shows battle+camp. One of the two needs checking.
11. **Revival Charm and Lost:** the museum text says it cures Lost, but a Lost character is removed from the party
    and roster (see [town.md](town.md#temple)); how the charm reaches one was not traced.

Tech: [items.md §11](../tech/items.md#11-open-questions--not-found-what-was-tried)
