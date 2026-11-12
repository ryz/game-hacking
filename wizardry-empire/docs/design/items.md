# Items: equipment, curses, item use, identification

How items work for the player: what each item stat means, where items are equipped, curses and alignment locks,
using items in battle and in camp, and identification. Every item with its stats is in the generated table
[items_table.md](items_table.md). Prices, the shop and the temple are in [town.md](town.md); how weapon numbers
turn into hits and damage is in [combat.md](combat.md); which class may equip what is in
[characters.md](characters.md#32-equipment-groups). Notation: [README.md](README.md).

## Overview

- **224 fixed item types.** An item never varies: no random enchantments, no durability, no "+1" rolls. Two Long
  Swords are always identical.
- **Inventory:** each character carries **8 items**. Each carried item can be equipped (main or off hand), stuck,
  or unidentified.
- **Six equipment slots:** Weapon, Off-hand, Armor, Helm, Gloves, Other. Each item lists which of the 14 classes
  may equip it; two-handed weapons leave the off hand empty, launchers take matching ammo there, and only the
  **Musashi** can wield two weapons.
- **Curses and alignment:** equipping a cursed item, or an item your alignment is not allowed, makes it **stick**:
  it cannot be taken off. 36 items are cursed, and 17 of them also drain HP while worn (computed: counted in the item
  table). The **Avenger** class is immune to both locks and to the drain.
- **Using items:** potions, scrolls, staves, rods and some rings cast a spell, in battle, in camp or both, with a
  per-item **chance to break** after each use (Healing Potion 100%, Staff of Healing 25%). Anyone can use them,
  whatever the class. Some weapons and potions can be **thrown** and come back with a per-item chance.
- **Special powers:** a handful of items do something permanent when their power is used: LUK +1, age −1 year, or a
  change of class. The class-changing items are the only way into the five special classes
  ([characters.md](characters.md#33-special-classes-and-their-items)).
- **Identification:** items found in chests are unidentified and show a generic name ("Sword", "Ring"). The shop
  identifies for a fee and never fails; in camp the chance is (6 + identifier level − item level) / 20, and a
  failure can make the identifier Afraid.

---

## 1. What an item is

Every item has one fixed set of stats. The player sees them on the museum page and in the shop; the table below
explains each column of [items_table.md](items_table.md) in play terms.

| Column | What it means in play | Values |
|---|---|---|
| Slot | What kind of item it is, and so where it is equipped (section 2) | one-handed weapon, two-handed weapon, parry dagger, bow, crossbow, sling, arrows, quarrels, sling stones, body armor (robes too), shield, helm, gloves, other (accessories and consumables) |
| Unid. name | Name shown while the item is unidentified; also picks the attack verb in battle | a list of 25 generic names (section 5) |
| Damage | Damage per hit, rolled again on every swing, written `NdS+B` with its min-max | Hand Axe 2-7 (1d6+1), Crescent Axe 24-42 (2d10+22) |
| Swings+ | Extra swings per round on top of the class's own count; only the main-hand weapon counts | mostly +1; daggers up to +6, Swift Sword +7 |
| Hit+ | Lowers the number needed to hit by its value: each point is 5% more chance to hit (computed from the to-hit rule), inside the 5%-95% limits | mostly 0-8; 47-50 on 20 weapons, which therefore always hit at the 95% cap (verified for the Battle Axe; [combat.md](combat.md#31-weapons-with-hit-47-to-50), [findings.md](findings.md)) |
| AC | Added to the wearer's armor class, summed over everything equipped; negative is better | Demon Armor −12, Main Gauche −1 |
| Range | S, M or L on weapons; "-" on ammo, armor, shields and accessories (computed: counted in the table; the Spiked Shield has S) | which enemy groups each range reaches was not traced |
| Throw (keep %) | The item can be thrown with the Throw command; the number is the chance it comes back | Hand Axe 70, Shuriken 95, potions 0 |
| Classes | The classes allowed to equip it; "none" = nobody can equip it (consumables), though anyone can use it | see [characters.md](characters.md#32-equipment-groups) |
| Align | Alignments (Good, Neutral, Evil) that may equip it **without it sticking** | "any" on most items |
| Curse | Cursed items stick when equipped | 36 items |
| Price | Shop price; selling, identifying and uncursing cost half, rounded up ([town.md](town.md#1-shop)) | 10 G (Arrow, Short Sword) to 5,000,000 G (Ura Muramasa) |
| Use (break %) | Spell the item casts when used, [where it can be used, its target], and the chance it breaks after a use | section 4.1 |
| Special | A passive property while equipped, a throw effect, or a special power | sections 4.3 and 4.4 |
| HP/step | HP regained (or lost, if negative) for every step walked while equipped | Ring of Healing +5, Garb of Lords +3, Demon Gloves −5 |
| Lv | Item level, 1-15: how hard it is to identify | 1 for starter gear, 15 for the top items |

Example row (Hand Axe, quoted from [items_table.md](items_table.md)):

| # | English | Japanese | Slot | Damage | Range | Throw (keep %) | Classes | Price | Lv | Shop |
|---|---|---|---|---|---|---|---|---|---|---|
| 0 | Hand Axe | ハンドアックス | 1H weapon | 2-7 (1d6+1) | S | 70 | Fig Sam Lor Nin Val Mus Kun | 60 | 1 | unlimited |

Read: a one-handed axe for the fighting classes, 2-7 damage per hit, can be thrown and comes back 70% of the time,
60 G at the shop, always in stock.

**Notes:** damage, swings, Hit+ and AC are item stats here; how they combine with the character's class, level and
STR into a hit chance and damage is in [combat.md](combat.md#3-party-attacks-to-hit) and
[combat.md](combat.md#4-party-attacks-damage).

Tech: [items.md §1](../tech/items.md#1-the-item-record), [items.md, inventory slot](../tech/items.md#inventory-slot)

---

## 2. Equipping: slots, classes, launchers

The Equip screen walks through six slots in order. Each slot accepts only certain kinds of item, and each item
lists which of the 14 classes may equip it.

| Slot | Accepts | Extra rules |
|---|---|---|
| Weapon | one-handed and two-handed weapons, parry daggers, bows, crossbows, slings | the class must be allowed |
| Off-hand | shield, parry dagger (Main Gauche) | Two-handed weapon in the main hand: nothing. Bow: arrows only. Crossbow: quarrels only. Sling: sling stones only. **Musashi:** may also put a one-handed weapon here (two weapons). |
| Armor | body armor and robes | |
| Helm | helms | |
| Gloves | gloves | |
| Other | one accessory (rings, amulets, cloaks and other odd objects) | |

**Classes.** An item whose Classes column leaves out your class cannot be equipped. Which classes take which
weapons and armor, including the rings and accessories with class limits, is summarized in
[characters.md](characters.md#32-equipment-groups); the per-item lists are the Classes column of
[items_table.md](items_table.md). Potions, scrolls, charms and the other consumables show "none": nobody can equip
them, but anyone can use them (section 4.1).

**Launchers and ammo.** A bow, crossbow or sling needs its ammo in the off hand. Without it the launcher still
works, but every damage die shrinks to about a quarter of its size (exact rule in [combat.md](combat.md#4-party-attacks-damage)). With
ammo, the slaying property comes from the **ammo**, not the launcher: Exorcist Arrows slay undead from any bow.

**Notes:**
- Changing class takes off all equipment except items that are stuck; see
  [characters.md](characters.md#34-change-class-training-grounds).
- In the shop, items the selected character cannot equip are marked ([town.md](town.md#1-shop)).

Tech: [items.md §2](../tech/items.md#2-equipment-rules), [characters.md §5.2](../tech/characters.md#52-equipment-groups)

---

## 3. Curses and alignment locks

Some items stick to the character who equips them. A stuck item cannot be taken off, so the character carries its
penalties until the shop's Uncurse removes it.

An item sticks when it is equipped and either it is **cursed** (36 items), or the character's alignment is not among
the item's allowed alignments, unless the wearer is an Avenger, whose items never stick.

17 of the 36 cursed items also **drain HP every step** while equipped (computed: counted in the item table). Rows
quoted from [items_table.md](items_table.md):

| # | English | Japanese | Slot | AC | Curse | Price | HP/step | Lv |
|---|---|---|---|---|---|---|---|---|
| 3 | Blood Axe | ブラッドアックス | 2H weapon | | cursed | 25000 | -3 | 10 |
| 121 | Demon Armor | あくまのよろい | Body armor | -12 | cursed | 200000 | -4 | 13 |
| 170 | Demon Gloves | あくまのこて | Gloves | -7 | cursed | 400000 | -5 | 15 |

Several cursed items are strong (Demon Armor is AC −12); for those the curse is a trade: power for a permanent HP
drain and no way to take the item off.

**The Avenger** (a special class) ignores both locks: its items never stick, and negative HP/step values do nothing
to it. The Avenger Sword is itself cursed, but only the Avenger may equip it, so in practice it never sticks.

**Getting rid of a stuck item.** The shop refuses to buy a cursed item. The shop's Uncurse frees the character but
**destroys the item** and costs half its price ([town.md](town.md#1-shop)).

**Notes:**
- The game also re-checks the alignment of equipped items at some other moment and shows a message; what triggers
  that check was not traced.

Tech: [items.md §2](../tech/items.md#2-equipment-rules), [items.md §5](../tech/items.md#5-identification-and-curses)

---

## 4. Using items

### 4.1 Spell items
Potions, scrolls, staves, rods, stones and some rings and weapons cast a spell when used with the Use command. Each
such item has:

- **Effect:** the spell it casts (the Use column).
- **Where and on whom:** battle, camp or both; and its target (one ally, one enemy group, all enemies, the party, or
  no target). The target is read from which items carry which value (inferred).
- **Break chance:** after **every** use, the item is used up with this chance (100 = always consumed).

**Who can use them.** Using an item does not depend on the class: a Fighter can drink a Healing Potion or use a
Revival Charm (verified, in camp). Consumables cannot be equipped by anyone (Classes "none").

Rows quoted from [items_table.md](items_table.md):

| # | English | Japanese | Price | Use (break %) |
|---|---|---|---|---|
| 18 | Staff of Healing | いやしのつえ | 1000 | Healing [battle+camp, one ally] (breaks 25%) |
| 20 | Rod of Flame | ロッド オブ フレイム | 10000 | Fireball [battle, enemy group] (breaks 10%) |
| 172 | Revival Charm | ふっかつのごふ | 1000000 | Cures death, ashes and even Lost [battle+camp, one ally] (breaks 100%) |
| 193 | Map Record Sheet | マップきろくシート | 400 | Shows the map [camp, no target] (breaks 30%) |
| 194 | Healing Potion | ヒーリングポーション | 100 | Healing [battle+camp, one ally] (breaks 100%) |
| 202 | Ring of Warping | てんいのゆびわ | 25000 | Teleport [camp, party] (breaks 25%) |

- The **Healing Potion** works in battle and in camp (verified in camp: a Fighter at 1 of 10 HP was healed to full,
  and the potion was gone).
- The **Revival Charm** turns a Dead, Ashes or even **Lost** member back to OK at full HP, with no roll (verified in
  camp on a Lost member); on anyone else nothing happens. The temple does not cure Lost; the charm does
  ([town.md](town.md#32-raising-the-dead)).
- A Staff of Healing lasts 4 uses on average and a Rod of Flame about 10 (computed: 1 / break chance).

What each spell does (damage, healing amount) is in [spells.md](spells.md); how strong the item versions are was not
traced.

### 4.2 Throwing
The Throw command in battle throws an item at the enemy:
- Only items marked throwable, and only when they are **not equipped**: hand axes, daggers, flails, spears, the
  Gladius, maces, shuriken, Gungnir, Longinus, healing potions and stones, the Exorcism Charm and the Potion of
  Poison.
- After the throw the item comes back with its keep chance (Hand Axe 70%, Shuriken 95%); otherwise it is lost.
  Potions and charms have 0: they are always gone.
- Healing items hurt undead when thrown (game text): High Heal Potion 32-48, Healing Potion and Healing Stone 16-24.
  The Elixir "can destroy the undead", the Exorcism Charm has a Sun Ray effect, and the Potion of Poison poisons the
  foe (game text). The throw damage itself was not traced.

### 4.3 Equipped effects
Some items work simply by being worn. The Special column names the effect.

| Effect | Items (examples) | Confidence |
|---|---|---|
| HP per step (positive regenerates, negative drains) | Ring of Healing, Ring of Life +5; Garb of Lords +3; Ring of Death −5; cursed gear −3 to −5 | |
| Double damage on every hit | Clockwork Doll (Ninja, Kunoichi) | |
| Slaying: extra damage against undead, demons, dragons or spirits | Dragonslayer, Exorcist Arrow, Holy Cross Sword, Kris, Odin Sword ... | multipliers in [combat.md](combat.md#5-slaying-weapons-and-other-weapon-properties) |
| Critical +10% / +5% | Kunai, Ura Muramasa / Shuriken, Muramasa | (game text) |
| Magic evade 30% / 50% / 85% | Shell Amulet / +1 / +2 | (game text) |
| Drain evade 50% / 10% | Synthesis Stone / Holy Ring | (game text) |
| Water damage ½ | Winter Mittens, Ring of Fire | (game text) |
| Fire damage ½ | Ring of Ice | (game text) |
| "Hide" success +10% | Hider Cloak | (game text) |
| Healing and cure success +50% | Priest Ring | (game text) |
| Teleport | Helm of Warping | (game text) |
| Lets you ride the elevator / meet the twin fairies | Key Card / Fairy's Heart | (game text) |

The (game text) effects are the museum's own descriptions; how the game applies them was not traced. For HP per
step, the museum text says "+5 / −5 HP per step", but the real amount is each item's own HP/step value.

### 4.4 Special powers
A few items have a power used with "Use its special power?". Using it first **takes the item off**, then applies the
effect, then decides what happens to the item.

| # | Item | Japanese | Effect | Item afterwards |
|---|---|---|---|---|
| 184 | Rabbit's Foot | ウサギのあし | LUK +1 (up to the race maximum, race base + 10) | always used up |
| 183 | Youth Stone | わかがえりのいし | Age −1 year, not below 12 | always used up |

The other seven items with a power change the character's class (Thieves' Dagger and Butterfly Knife to Ninja, and
one item for each of the five special classes). Their conditions, what the change does to the character, and what
becomes of the item are in [characters.md](characters.md#33-special-classes-and-their-items).

Tech: [items.md §3.1](../tech/items.md#31-spell-items), [§3.2](../tech/items.md#32-throwing-command-throw),
[§3.3](../tech/items.md#33-special-powers), [§4.4](../tech/items.md#44-slaying),
[characters.md §5.2](../tech/characters.md#52-equipment-groups),
[characters.md §9](../tech/characters.md#9-status-ailments-and-recovery)

---

## 5. Identification

Items found in chests ([dungeon.md](dungeon.md#5-chests)) arrive **unidentified**. An unidentified item shows a generic name
instead of its own, and the battle text uses a verb that fits that name. The list has 25 entries (some repeat): Axe,
Arrow, Stone, Scythe, Odd object, Staff, Sword, Dagger, Hammer, Cord, Long staff (two entries), Staff, Spear, Bow,
Armor, Robe, Shield, Helm, Gloves, Odd object, Scroll, Potion, Cloth, Ring. Each item's generic name is the
"Unid. name" column of [items_table.md](items_table.md).

An unidentified item **cannot be sold**. There are two ways to identify it:

| Where | Chance | Cost | Risk |
|---|---|---|---|
| Lorelei's Shop, Identify | always succeeds | half the item's price ([town.md](town.md#1-shop)) | none |
| Camp, "Identify what?" | (6 + L − I) / 20 | free | a failure can make the identifier Afraid |

Which classes may identify in camp was not traced; it is probably the Bishop (inferred).

**Camp identification.** L is the identifier's level, I the item level (1-15). The identification succeeds if a
random number from 0 to 19 is below 6 + L − I, a chance of (6 + L − I) / 20; it always succeeds when L − I is 14 or
more, and never when the item is 6 or more levels above the identifier.

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
a level-20 identifier has 55% on a level-15 item, and only level 29 makes the top items certain (computed).

**Failure.** The game prints "Oops!" and the identifier may turn **Afraid**; the chance falls with LUK:

| LUK | under 7 | 7-8 | 9-10 | 11-13 | 14-17 | 18-20 | 21-22 | 23 | 24+ |
|---|---|---|---|---|---|---|---|---|---|
| Chance to become Afraid | 20% | 19% | 18% | 17% | 15% | 12% | 10% | 7% | 5% |

Tech: [items.md §5](../tech/items.md#5-identification-and-curses), [items.md §1](../tech/items.md#1-the-item-record)

---

## Open questions

1. **Range S/M/L:** which enemy groups each range reaches was not traced. Two further range markings have no known
   meaning: one is set on most two-handed and heavy weapons, the other on daggers and claws, and the Spiked Shield
   has both.
2. **Use targets** (one ally, enemy group, party ...) are read from which items carry which value; unconfirmed.
3. **Spell power of item effects** and **throw damage** were not traced; the throw numbers above are museum text.
4. **Passive specials** (criticals, magic evade, drain evade, elemental halving, Hide, healing bonus, Helm of
   Warping teleport): the effects are the museum's descriptions; how the game applies them was not traced.
5. **Alignment re-check** on equipped items: what triggers it was not traced.
6. **Camp Identify:** which classes may use it (probably the Bishop) was not traced.
7. **Equipping unidentified items:** whether an unidentified item can be equipped (and so get stuck unseen) was not
   traced.

Tech: [items.md §11](../tech/items.md#11-open-questions--not-found-what-was-tried)
