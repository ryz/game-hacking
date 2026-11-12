# Town: shop, inn, temple, gold

The three town services that cost gold, and where the gold comes from: **Lorelei's Shop** (しょうてん ローレライ)
buys, sells, identifies and uncurses; the **Aries Inn** (アリエスの やど) heals, restores spells, ages the party and
is where level-ups happen; the **Samsara Temple** (サンサーラじいん) cures statuses and raises the dead. Item stats
are in [items.md](items.md) and [items_table.md](items_table.md). Notation: [README.md](README.md).

## Overview

- **Shop:** buy at full price; sell, identify and uncurse at **half** the price, rounded up. Uncursing **destroys**
  the item. A new game starts with 65 items in stock, 39 of them never running out. Items you sell go into the
  stock, so the shop is also the long-term store for spare finds.
- **Inn:** a stay is 7 nights (Stables: 1). Each night heals a dice amount that grows with the room: Cots 3d6+2,
  Economy 10d6, Suite 8d10+20, Royal Suite 10d20+20. The room price is charged **per night spent healing**, so the
  menu's "per week" is really a per-night price: a Royal Suite stay costs 0 to 3,500 G. Every night refills the
  spells, except a hurt night the character cannot pay for (verified). Every night outside the Stables ages the character by a day, at any HP (verified); a year is
  360 days, and any inn birthday that reaches **age 57 kills** the character (verified).
- **Temple:** fee = rate × level, the rate being 10 for minor statuses, 30 Paralyzed, 50 Stoned, 100 Dead, 300
  Ashes. Raising the Dead or Ashes succeeds 1.2% to 95.3% of the time depending on age and VIT; a failure turns Dead
  into Ashes and Ashes into **Lost**. A success costs a point of VIT about 60% of the time and ages the character 1-3
  years 89% of the time. A raising spell uses a similar roll with the caster's PIE added.
- **Gold is per character** and comes mainly from battles: each monster is worth a fixed amount (20 to 250 G), the
  total is split evenly among the members who are OK, Afraid or Asleep, and guarded-square victories add a chest.
  Selling returns half an item's price. A new character starts with 100 G.

---

## 1. Shop

**Lorelei's Shop** is the only place to buy items, and the only place that buys them for gold, identifies for certain
and removes curses.

### 1.1 Services

| Action | Price | Rules |
|---|---|---|
| Buy | full price | the stock goes down by 1, unless the item is unlimited |
| Sell | half price, rounded up | refused for unidentified and cursed items; selling an equipped item asks first; the item joins the stock |
| Identify | half price, rounded up | always succeeds ([items.md](items.md#5-identification) for identifying in camp) |
| Uncurse | half price, rounded up | frees the character, but **the item is destroyed** |
| Pool gold | - | gathers the party's gold on one member |

Half price is the Sell column of [items_table.md](items_table.md), which is also the Identify and Uncurse fee.
Examples quoted from the table:

| # | English | Japanese | Curse | Price | Sell |
|---|---|---|---|---|---|
| 0 | Hand Axe | ハンドアックス | | 60 | 30 |
| 3 | Blood Axe | ブラッドアックス | cursed | 25000 | 12500 |
| 170 | Demon Gloves | あくまのこて | cursed | 400000 | 200000 |

So freeing a character from Demon Gloves costs 200,000 G and leaves nothing to sell.

**Uncurse destroys the item.** The shop frees a stuck item only by destroying it, so the character pays the fee and
loses the item.

**Class marks.** When a character browses the stock, items that character's class cannot equip are marked; items
usable from the camp menu are never marked.

Tech: [items.md §6](../tech/items.md#6-shop-lorelei), [items.md §5](../tech/items.md#5-identification-and-curses),
[items.md §2](../tech/items.md#2-equipment-rules)

### 1.2 Stock
- Each item has its own stock count. Some items are unlimited. For the others, buying lowers the stock by 1 and
  selling raises it by 1, up to 254.
- **Opening stock:** a new game starts with 65 items in stock; the same step marks them as seen in the museum, which
  is why a fresh museum shows 65 items.
  - 39 are unlimited: the basic weapons, armor and consumables (Hand Axe, Long Sword, Leather Armor, Healing
    Potion ...), plus the **Revival Charm at 1,000,000 G**.
  - 26 are limited: Great Axe 1, Claws 2, Staff of Healing 1, Gladius 1, Falchion 1, Katana 1, Silver Dagger 3,
    Kris 3, Main Gauche 1, Morning Star 5, Nunchaku 5, Vermilion Spear 1, Lance 1, Long Bow 2, Scale Mail 5, Chain
    Mail 5, Kite Shield 5, Spiked Shield 1, Plate Helm 4, Chain Gloves 3, Shell Amulet 1, Dreaming Stone 1, Scroll
    of Sleep 5, High Heal Potion 15, Elixir 3, Cloak 5.
  - Every item's opening stock is the Shop column of [items_table.md](items_table.md).
- **Selling stocks the shop.** An item you sell can be bought back later at full price. With only 8 items per
  character ([items.md](items.md)), the shop acts as the party's storage, at the cost of half the price per round
  trip (computed: sell for half, buy for full).

**Notes:**
- No item is marked unsellable ([findings.md](findings.md)).
- The game can check whether a copy of an item already exists anywhere (shop, party or roster); where this is used
  (probably chests) is open.

Tech: [items.md §6](../tech/items.md#6-shop-lorelei)

---

## 2. Inn

The **Aries Inn** is where characters heal, get their spells back and **level up**. Each character checks in
separately and picks a room.

### 2.1 Rooms and healing

| Room | Price per night | Nights | HP healed per night | Average per night | Gold per HP (average) | Ages? |
|---|---|---|---|---|---|---|
| Stables | free | 1 | none | - | - | no |
| Cots | 10 | 7 | 3d6+2 | 12.5 | 0.8 | yes |
| Economy | 50 | 7 | 10d6 | 35 | 1.4 | yes |
| Suite | 200 | 7 | 8d10+20 | 64 | 3.1 | yes |
| Royal Suite | 500 | 7 | 10d20+20 | 125 | 4.0 | yes |

Averages and gold per HP are computed from the dice (the average of NdS+B is N × (S + 1) / 2 + B) and the price.
Healing never goes above max HP.

So the cheap rooms are the most efficient per gold, and the expensive rooms buy **speed**: a Royal Suite heals in one
night about what Cots heal in ten (computed from the averages). A full week heals on average 87.5 (Cots), 245
(Economy), 448 (Suite) or 875 HP (Royal Suite) (computed: 7 × the average).

Tech: [items.md §7](../tech/items.md#7-inn-aries-inn), [characters.md §8](../tech/characters.md#8-inn-rest)

### 2.2 Paying
The menu shows a "per week" price, but the game charges it **once for each night the character is still hurt**:

1. At check-in the character must have the price of one night; otherwise the inn says "Not enough gold."
2. Each night, a character below max HP pays the room price and heals the room's dice, up to max HP.
3. A night at full HP is free.
4. A hurt night the character cannot pay for gives no healing and no spell refill.

- A Royal Suite stay from 1 HP can cost up to 7 × 500 = 3,500 G.
- Observed: a character at 1/200 HP paid 70 G for 7 nights at Cots and healed 104 HP; a character at 1/10 HP paid
  10 G (verified).
- The per-night pricing is listed in [findings.md](findings.md).

Tech: [items.md §7](../tech/items.md#7-inn-aries-inn), [characters.md §8](../tech/characters.md#8-inn-rest)

### 2.3 Spells and level-ups
- **Spells:** every night refills the spell slots, in every room including the Stables and on free nights at full
  HP (verified: a Stables night at full HP and a Cots stay from 1 HP both refilled them). The only exception is a
  hurt night the character cannot pay for. Slot counts are in [spells.md](spells.md#5-spell-slots).
- **Level-ups happen only here.** Choosing a room first checks the character's EXP; with enough, that stay grants
  **one** level, otherwise the inn says how much EXP is still missing ("1200 more EXP" for a new Fighter, verified).
  What a level-up gives (HP, stat changes, spells) is in
  [characters.md](characters.md#42-when-a-level-is-gained).

Tech: [characters.md §8](../tech/characters.md#8-inn-rest),
[characters.md §6.2](../tech/characters.md#62-when-the-level-up-happens)

### 2.4 Aging
The inn is the game's clock. Every night in Cots, Economy, Suite or Royal Suite adds one day to the character's age,
whatever the character's HP; the Stables never do (verified: the day counter rose by 7 after a Cots stay, both from
1 HP and at full HP, and did not move after the Stables). After **360 days** the age goes up by one year (up to 99),
a "birthday". A year is about 51 full stays (computed: 360 / 7).

A birthday at the inn that brings a character to **57 or older kills them** (verified); the rule, its ignored
survival roll and the practical lifespan are in [characters.md](characters.md#5-aging).

**Notes:** the Stables cost nothing, heal nothing and do not age, but they refill spells and grant a level-up, so a
healthy party can do both there without spending days.

Tech: [characters.md §7](../tech/characters.md#7-aging), [items.md §7](../tech/items.md#7-inn-aries-inn)

---

## 3. Temple

The **Samsara Temple** cures every status except Lost, for a fee that scales with the patient's level. Any party
member can pay.

### 3.1 Fees

| Status | Japanese | Rate (G per level) | Outcome |
|---|---|---|---|
| Afraid, Asleep, Poisoned, Silenced | きょうふ, すいみん, どく, まふうじ | 10 | always cured |
| Paralyzed | まひ | 30 | always cured |
| Stoned | いし | 50 | always cured |
| Dead | しぼう | 100 | raise roll (section 3.2) |
| Ashes | はい | 300 | raise roll (section 3.2) |
| Lost | ロスト | - | not offered |

Fee = rate × the patient's level, paid by a party member you choose; "Not enough gold." if that member is short.
Examples (computed): curing a level-10 Paralyzed character costs 300 G, raising a level-10 Dead character 1,000 G,
a level-10 Ashes character 3,000 G. Cures of the other statuses have no side effects.

Tech: [items.md §8](../tech/items.md#8-temple-samsara-temple),
[characters.md §9](../tech/characters.md#9-status-ailments-and-recovery)

### 3.2 Raising the dead
Dead and Ashes characters can be raised at the temple or by a raising spell (which spell uses this roll is unknown).
Both use the patient's age and VIT; the spell adds the caster's PIE and treats old age more kindly.

| Rule | Temple | Spell |
|---|---|---|
| Cost | 100 × level (Dead), 300 × level (Ashes) | one cast |
| Succeeds if | a random number from 0 to 100 is below base + VIT bonus + 1 | a random number from 0 to 99 is below base + VIT bonus + PIE bonus |
| Chance | (base + VIT bonus + 1) out of 101 | (base + VIT bonus + PIE bonus) out of 100 |
| Base, age under 20 | 90 | 90 |
| Base, age 20-29 | 80 | 80 |
| Base, age 30-39 | 65 | 65 |
| Base, age 40-49 | 40 | 40 |
| Base, age 50-69 | 10 | 10 |
| Base, age 70+ | 0 | 10 |
| VIT bonus (patient) | under 7: 0; 7: 1; 8-9: 2; 10-14: 3; 15-19: 4; 20-21: 5; 22+: 6 | same |
| PIE bonus (caster) | - | under 7: 0; 7-10: 1; 11-14: 2; 15-17: 3; 18-19: 4; 20+: 5 |
| Chance in play | 1.2% (age 70+, VIT under 7) to 95.3% (under 20, VIT 20-21) | 10% to 100% (computed) |
| On success | status OK; HP 1 if it was 0 | status OK |
| Aging on success | +1 to 3 years (up to 99), 89% of the time | +1 year |
| VIT loss on success | −1 about 60% of the time (a random number from 0 to 100 below 61), never below the race's base VIT: Human 8, Elf 6, Dwarf 10, Gnome 8, Hobbit 6, +1 for female characters | none |
| On failure | Dead becomes Ashes; Ashes becomes **Lost**, and the Lost character is deleted at once | Dead becomes Ashes; Ashes becomes **Lost** |

The temple's 1.2% and 95.3% are the game's exact odds: the roll is very slightly uneven, which lifts 1 out of 101
to 1.2%. The VIT 22+ row can never apply: no race can raise VIT above 21 (race base + 10, female Dwarf).
The spell's range is computed from the tables: base 10 with no bonuses, up to 90 + 5 + 5.

What that means in play (temple):
- A 25-year-old with VIT 12: 84 out of 101 = 83%.
- A 45-year-old with VIT 12: 44 out of 101, about 44%; a 55-year-old with VIT 12: 14 out of 101, about 14%
  (computed from the table).
- The big drops are at **40** and again at **50**: past 50 a temple raise is a long shot, and past 70 almost
  hopeless.
- By spell, the same 25-year-old with a PIE 15 caster: 80 + 3 + 3 = 86% (computed). Past 70 the spell keeps a base
  of 10 where the temple has 0 ([findings.md](findings.md)).

**Lost.** The temple does not treat Lost. A Lost character from a failed temple raise is deleted at once; after a
failed spell raise on Ashes the Lost character stays in the party (how this plays out was not traced in full). The
**Revival Charm** (1,000,000 G at the shop) turns a Dead, Ashes or Lost member back to OK at full HP, with no roll
(verified on a Lost member; [items.md](items.md#41-spell-items)).

**Notes:**
- Each temple raise makes the next one harder: it ages the character (lower base) and may cost VIT (lower bonus).
  Near 56 it can also bring the old-age death at the inn closer ([characters.md](characters.md#5-aging)).
- The temple roll has 101 outcomes rather than 100 ([findings.md](findings.md)).

Tech: [items.md §8](../tech/items.md#8-temple-samsara-temple),
[characters.md §9](../tech/characters.md#9-status-ailments-and-recovery)

---

## 4. Gold

Each character carries their own gold. The party earns it in the maze and spends it in town.

### 4.1 Sources

| Source | Amount | Notes |
|---|---|---|
| Monsters | a fixed amount per monster killed: 20 G (Crawling Claw) to 250 G (Abyss Lurker) | monsters that flee or are left alive give nothing; per-monster values in [monsters_table.md](monsters_table.md) |
| Chests | an amount set by the chest's value; formula in [dungeon.md](dungeon.md#52-gold) | only fights on guarded squares give a chest; random encounters give gold only |
| Selling | half the item's price, rounded up | section 1.1 |
| New character | 100 G | [characters.md](characters.md#25-what-a-new-character-starts-with) |
| Maze events | e.g. the "gold coins" square on floor 1 | amount not traced |

Tech: [items.md §9](../tech/items.md#9-gold-sources), [monsters.md §7](../tech/monsters.md#7-rewards),
[characters.md §3.5](../tech/characters.md#35-what-the-new-character-gets)

### 4.2 The split
After a victory, the monsters' gold plus any chest gold is pooled and shared evenly among the members who are OK,
Afraid or Asleep; the full rule and a worked example are in [combat.md](combat.md#15-rewards). **Pool gold** (shop)
and **Divide gold** then move gold between members.

Tech: [items.md §9](../tech/items.md#9-gold-sources)

### 4.3 The economy at a glance
Comparisons computed from the numbers above:
- A Cots week from low HP costs at most 70 G, about the gold of four of the weakest monsters (20 G each); a Royal
  Suite week costs up to 3,500 G, the gold of 14 Abyss Lurkers.
- Raising a level-10 character costs 1,000 G (Dead) or 3,000 G (Ashes); temple fees grow with level while monster
  gold per kill stays between 20 and 250 G, so high-level deaths are expensive.
- Top items cost far more than battles pay: the Revival Charm is 1,000,000 G, the gold of 4,000 Abyss Lurkers.
  Selling chest finds at half price is the other large income.

Tech: [items.md §9](../tech/items.md#9-gold-sources)

---

## Open questions

1. **Running out of gold mid-stay:** a hurt night that cannot be paid gives no healing and no spell refill; what the
   player sees when that happens was not checked in play.
2. **Unused inn options:** the inn has two options the menu never offers: a full-heal night for 10 × level, and a
   room that heals fully at once. What would enable them was not traced ([findings.md](findings.md)).
3. **Unique items:** the shop/party/roster check for an existing copy of an item; which items it covers and where it
   is used were not traced.
4. **Maze event gold:** the amount of the floor-1 "gold coins" square was not traced.
5. **Raising someone who died of old age:** the character is left Dead at 57+; whether the temple treats them like
   any other Dead character was not tested.
6. **Lost after a spell raise:** how a Lost character who stays in the party plays out (before the Revival Charm)
   was not traced in full.

Tech: [items.md §11](../tech/items.md#11-open-questions--not-found-what-was-tried),
[characters.md §11](../tech/characters.md#11-open-questions--not-found)
