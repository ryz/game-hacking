# Town (Wizardry Empire, GBC, 1999)

The three town services that cost gold, and where the gold comes from: **Lorelei's Shop** (しょうてん ローレライ)
buys, sells, identifies and uncurses; the **Aries Inn** (アリエスの やど) heals, restores spells, ages the party and
is where level-ups happen; the **Samsara Temple** (サンサーラじいん) cures statuses and raises the dead. Item stats
are in [items.md](items.md) and [items_table.md](items_table.md). Notation and confidence tags:
[README.md](README.md). Untagged numbers are (data).

## Overview

- **Gold is per character** and comes mainly from battles: each monster is worth a fixed amount (20 to 250 G),
  the total is split evenly among the members who are OK, Afraid or Asleep, and guarded-square victories add a
  chest bonus (data). Selling returns half an item's price (data). A new character starts with 100 G (data).
- **Shop:** buy at full price, sell / identify / uncurse at **half** the price (rounded up) (data). Uncursing
  **destroys** the item (data). A new game starts with 65 items in stock, 39 of them never running out (data).
  Items you sell go into the stock, so the shop is also the long-term store for spare finds (data).
- **Inn:** a stay is 7 nights (Stables: 1). Each night heals a dice amount that grows with the room: Cots 3d6+2,
  Economy 10d6, Suite 8d10+20, Royal Suite 10d20+20 (data). The room price is charged **per night spent healing**,
  so the menu's "per week" is really a per-night price: a Royal Suite stay costs 0 to 3,500 G (data). Every night
  outside the Stables ages the character by a day (data; one observation questions this, see the inn section), a
  year is 360 days, and as written any inn birthday that reaches **age 57 kills** the character (verified).
- **Temple:** fee = rate × level, the rate being 10 for minor statuses, 30 Paralyzed, 50 Stoned, 100 Dead, 300
  Ashes (data). Raising the Dead or Ashes succeeds 1% to 96% of the time depending on age and Vitality (computed from
  the tables below); a failure turns Dead into Ashes and Ashes into **Lost** (data). A success costs Vitality about
  60% of the time and ages the character 1-3 years 89% of the time (data).

---

## Shop

**Lorelei's Shop** is the only place to buy items, and the only place that sells for gold, identifies for certain
and removes curses.

| Action | Price | Rules |
|---|---|---|
| Buy | full price | stock goes down by 1, unless the item is unlimited |
| Sell | half price, rounded up | refused for unidentified and cursed items; selling an equipped item asks first; the item joins the stock (+1, up to 254) |
| Identify | half price, rounded up | always succeeds ([items.md](items.md#identification) for the camp alternative) |
| Uncurse | half price, rounded up | frees the character, but **the item is destroyed** |
| Pool gold | - | gathers the party's gold on one member |

All rules in this table: (data). Half price is the "Sell" column of [items_table.md](items_table.md), which is also
the Identify and Uncurse fee. Examples quoted from the table:

| # | English | Japanese | Curse | Price | Sell |
|---|---|---|---|---|---|
| 0 | Hand Axe | ハンドアックス | | 60 | 30 |
| 3 | Blood Axe | ブラッドアックス | cursed | 25000 | 12500 |
| 170 | Demon Gloves | あくまのこて | cursed | 400000 | 200000 |

So freeing a character from Demon Gloves costs 200,000 G and leaves nothing to sell.

**Uncurse destroys the item.** The shop frees a stuck item only by destroying it, so the character pays the fee and
loses the item (data). Selling, identifying and uncursing all use the same half-price fee (data). See
[findings.md](findings.md).

**Buying and class marks.** When a character browses the stock, items that character's class cannot equip are
marked; items usable from the camp menu are never marked (data).

### Stock
- Each item type has its own stock count. A count of 255 means **unlimited**; buying lowers any other count by 1,
  selling raises it by 1 up to 254 (data).
- **Opening stock:** a new game starts with 65 item types in stock (data); the same step marks them as seen in the
  museum, which is why a fresh museum shows 65 items (data).
  - 39 are unlimited: the basic weapons, armour and consumables (Hand Axe, Long Sword, Leather Armor, Healing
    Potion ...), plus the **Revival Charm at 1,000,000 G** (data).
  - 26 are limited: Great Axe 1, Claws 2, Staff of Healing 1, Gladius 1, Falchion 1, Katana 1, Silver Dagger 3,
    Kris 3, Main Gauche 1, Morning Star 5, Nunchaku 5, Vermilion Spear 1, Lance 1, Long Bow 2, Scale Mail 5, Chain
    Mail 5, Kite Shield 5, Spiked Shield 1, Plate Helm 4, Chain Gloves 3, Shell Amulet 1, Dreaming Stone 1, Scroll
    of Sleep 5, High Heal Potion 15, Elixir 3, Cloak 5 (data).
  - Every item's opening stock is the "Shop" column of [items_table.md](items_table.md).
- **Selling stocks the shop.** An item you sell can be bought back later at full price (data). Combined with the
  8-item inventory limit ([items.md](items.md)), the shop acts as the party's storage, at the cost of half the price
  each round trip (computed: sell for half, buy for full).

**Notes:** the game supports a "cannot be sold" mark, but no item has it (data). There is also a check whether an
item already exists in the shop, the party or the roster, probably to stop chests handing out a second copy of
some items (inferred); who calls it is an open question.

Tech: [items.md §6](../tech/items.md#6-shop-bank-41-lorelei), [items.md §5](../tech/items.md#5-identification-and-curses)

---

## Inn

The **Aries Inn** is where characters heal, get their spells back and **level up**. Each character checks in
separately and picks a room.

### Rooms and healing

| Room | Price per night charged | Nights | HP healed per night | Average per night | Gold per HP (average) | Ages? |
|---|---|---|---|---|---|---|
| Stables | free | 1 | none | - | - | no |
| Cots | 10 | 7 | 3d6+2 | 12.5 | 0.8 | yes |
| Economy | 50 | 7 | 10d6 | 35 | 1.4 | yes |
| Suite | 200 | 7 | 8d10+20 | 64 | 3.1 | yes |
| Royal Suite | 500 | 7 | 10d20+20 | 125 | 4.0 | yes |

Prices, nights, dice and aging: (data). Averages and gold per HP are computed from the dice (average of NdS+B is
N × (S + 1) / 2 + B) and the price. Healing never goes above max HP (data).

So the cheap rooms are the most efficient per gold, and the expensive rooms buy **speed**: a Royal Suite heals in one
night about what Cots heal in ten (computed from the averages). A full week heals on average 87.5 (Cots), 245
(Economy), 448 (Suite) or 875 HP (Royal Suite) (computed: 7 × the average).

### Paying
The menu shows a "per week" price, but the game charges it **once for each night the character is still hurt**
(data):

```csharp
// one character checks in
if (character.Gold < room.Price) { Say("Not enough gold."); return; }   // must afford one night
for (int night = 1; night <= room.Nights; night++)                       // Stables 1, other rooms 7
{
    if (character.HP < character.MaxHP)
    {
        character.Gold -= room.Price;
        character.HP = Math.Min(character.MaxHP, character.HP + Roll(room.HealDice));
    }
    // a night at full HP is free
}
```

- A character at full HP stays for free (data).
- A Royal Suite stay from 1 HP can cost up to 7 × 500 = 3,500 G (data).
- Observed: a character at 1/200 HP paid 70 G for 7 nights at Cots and healed 104 HP; a character at 1/10 HP paid
  10 G (verified).

### Spells and level-ups
- **Spells:** every stay, Stables included, refills spell slots (inferred: the tech reference places the refill in
  the stay routine but did not trace it). Slot counts are in [spells.md](spells.md).
- **Level-ups happen only here.** Choosing a room first checks the character's EXP; with enough, that stay grants
  **one** level, otherwise the inn says how much EXP is still missing (data; "1200 more EXP" for a new Fighter is
  verified). What a level-up gives (HP, stat changes, spells) is in [characters.md](characters.md#42-when-a-level-is-gained).

### Aging, birthdays and old-age death
The inn is the game's clock. Each night outside the Stables adds one day to the character's age; after **360 days**
the age goes up by one year (up to 99), a "birthday" (data). A full 7-night stay is 7 days (verified: the day counter
rose by 7 after a Cots stay). So a year passes in about 51 seven-night stays (computed: 360 / 7).

At each birthday:

```csharp
age = Math.Min(99, age + 1);
if (age < 57)
    Say("Happy birthday!");
else
{
    // the game rolls RandomFrom0To(99 + VIT/2 + LUK/2) and compares it with age - 56,
    // but never uses the result: every birthday at 57 or older is fatal
    Say("... died of old age.");
    character.Status = Dead; character.HP = 0;   // and the character leaves the party
}
```

- **Death at 57** (verified): a Fighter (VIT 14, LUK 8) set to age 56, day 359, died of old age after one Cots
  stay; the same happened on the Japanese ROM (2026-11-12). A character going from 55 to 56 got "Happy birthday!"
  and survived (verified).
- **The ignored roll** is a reading of the code (data): the survival roll is made and then discarded. The emulator
  test confirms the death, not that the roll is ignored; see the open questions. The intended rule was probably
  "dies if the roll is below age − 56" (inferred); see [findings.md](findings.md).
- **Practical lifespan:** a character created at 16 has about 41 game years, about 14,800 inn nights (data), i.e.
  roughly 2,100 seven-night stays (computed: 14,800 / 7).
- Other things that age a character (temple raise, class change, the Youth Stone) are listed in
  [characters.md](characters.md#5-aging); the temple's share is in [Temple](#temple) below.

**Notes:**
- **Does a full-HP stay age the character?** The code reading says every night outside the Stables counts. One
  control stay contradicts it: a character at age 50, day 359, at full HP, stayed at Cots and had **no** birthday,
  and the day counter was unchanged afterwards (verified, one sample). Until this is checked again, treat "every
  night ages" as the code reading and the full-HP case as open.
- The Stables cost nothing, heal nothing and do not age (data), so a healthy party can refill spells (inferred,
  see above) and collect a level-up there without spending days (follows from the rules above).

Tech: [items.md §7](../tech/items.md#7-inn-bank-39-aries-inn),
[characters.md §8](../tech/characters.md#8-inn-rest-aries-inn-275046-5b53),
[characters.md §7](../tech/characters.md#7-aging),
[characters.md §6.2](../tech/characters.md#62-when-the-level-up-happens)

---

## Temple

The **Samsara Temple** cures everything except Lost, for a fee that scales with the patient's level. Any party
member can pay.

### Fees

| Status | Japanese | Rate (G per level) | Outcome |
|---|---|---|---|
| Afraid, Asleep, Poisoned, Silenced | きょうふ, すいみん, どく, まふうじ | 10 | always cured |
| Paralyzed | まひ | 30 | always cured |
| Stoned | いし | 50 | always cured |
| Dead | しぼう | 100 | resurrection roll |
| Ashes | はい | 300 | resurrection roll |
| Lost | ロスト | - | not offered |

All values: (data). Fee = rate × the patient's level, paid by a party member you choose; "Not enough gold." if that
member is short (data). Examples (computed): curing a level-10 Paralyzed character costs 300 G, raising a level-10
Dead character 1,000 G, a level-10 Ashes character 3,000 G.

### Resurrection
Dead and Ashes need a roll. The chance depends on the patient's age and Vitality (data):

```csharp
bool raised = RandomFrom0To(100) < AgeBase(age) + VitBonus(vit) + 1;   // chance (base + bonus + 1) / 101
```

| Age | Base | | VIT | Bonus |
|---|---|---|---|---|
| under 20 | 90 | | under 7 | 0 |
| 20-29 | 80 | | 7 | 1 |
| 30-39 | 65 | | 8-9 | 2 |
| 40-49 | 40 | | 10-14 | 3 |
| 50-69 | 10 | | 15-19 | 4 |
| 70+ | 0 | | 20-21 | 5 |
| | | | 22+ | 6 |

What that means in play:
- A 25-year-old with VIT 12: 84 / 101 = 83% (data).
- Best case, under 20 with VIT 22+: 97 / 101, about 96%; a 45-year-old with VIT 12: 44 / 101, about 44%; a
  55-year-old with VIT 12: 14 / 101, about 14%; worst case, 70+ with VIT under 7: 1 / 101, about 1% (computed from
  the tables).
- The big drop is at **40** and again at **50**: past 50 a raise is a long shot.

**Failure:** Dead becomes **Ashes**, Ashes becomes **Lost** (data). A Lost character is removed from the party and
deleted from the roster (data). So a failed raise of Ashes is permanent.

**Success:** the status is cleared and HP set to 1 if it was 0 (data). Then two separate rolls (data):
- **Vitality −1** if a random number from 0 to 100 is below 61 (about 60%). VIT never drops below the race minimum:
  Human 8, Elf 6, Dwarf 10, Gnome 8, Hobbit 6, plus 1 for female characters.
- **Age +1 to +3 years** (up to 99) if a random number from 0 to 99 is below 89 (89%).

Cures of the other statuses have no side effects (data).

**Notes:**
- Each raise makes the next one harder: it ages the character (lower base) and may cost Vitality (lower bonus).
  Near 56 it can also bring the old-age death at the inn closer ([Inn](#aging-birthdays-and-old-age-death))
  (follows from the rules above).
- There is also a raise spell, with its own odds and +1 year on success; see [spells.md](spells.md).

Tech: [items.md §8](../tech/items.md#8-temple-bank-39-samsara-temple),
[characters.md §9](../tech/characters.md#9-status-ailments-and-recovery)

---

## Gold: where it comes from

Each character carries their own gold (data). The party earns it in the maze and spends it in town.

### Sources

| Source | Amount | Notes |
|---|---|---|
| Monsters | a fixed amount per monster killed: 20 G (Crawling Claw) to 250 G (Abyss Lurker) | monsters that flee or are left alive give nothing; per-monster values in [monsters_table.md](monsters_table.md) |
| Chest bonus | `10 × (a random number from 0 to V, + 4)` G, V = the chest's value | only fights on guarded squares give a chest; random encounters give gold only |
| Selling | half the item's price, rounded up | see [Shop](#shop) |
| New character | 100 G | see [characters.md](characters.md#25-what-a-new-character-starts-with) |
| Maze events | e.g. the "gold coins" square on floor 1 | amount not traced |

All values: (data). Chest value V is drawn from a table row set by the monsters in the fight; a small bag of value
3 gives 40-70 G (data), and any leather bag (V 0 to 6) gives 40-100 G (computed from the formula). How V and the chest tiers work is
in [dungeon.md](dungeon.md).

### The split
After a victory, the monsters' gold plus any chest bonus is pooled and shared evenly among the members who are OK,
Afraid or Asleep (data); the full rule and a worked example are in [combat.md](combat.md#rewards). **Pool gold**
(shop) and **Divide gold** then move gold between members (data).

### The economy at a glance
Comparisons computed from the numbers above:
- A Cots week from low HP costs at most 70 G, about the gold of four of the weakest monsters (20 G each); a Royal
  Suite week costs up to 3,500 G, the gold of 14 Abyss Lurkers.
- Raising a level-10 character costs 1,000 G (Dead) or 3,000 G (Ashes); temple fees grow with level while monster
  gold per kill stays between 20 and 250 G, so high-level deaths are expensive.
- Top items cost far more than battles pay: the Revival Charm is 1,000,000 G, the gold of 4,000 Abyss Lurkers.
  Selling chest finds at half price is the other large income.

Tech: [items.md §9](../tech/items.md#9-gold-sources),
[monsters.md §7](../tech/monsters.md#7-rewards-code-02eee-2f22-split-itemsmd-9),
[characters.md §3.5](../tech/characters.md#35-what-the-new-character-gets-2647da-4852)

---

## Open questions

Carried over from the tech reference; nothing here should be read as a rule yet.

1. **Inn aging on a full-HP stay:** one control stay at full HP showed no change to the day counter, against the
   code reading that every night outside the Stables counts. Needs a second test (hurt vs full-HP character, same
   room).
2. **Old-age death roll:** that the survival roll is ignored is a code reading. The emulator confirmed the death at
   57 for one Fighter (VIT 14, LUK 8); the items reference counts this as one sample, the characters reference
   reports three seeds. Several samples, or a breakpoint on the roll, would settle it.
3. **Spell refill at the inn:** placed in the stay routine but not traced.
4. **Running out of gold mid-stay:** only the first night is checked at check-in; what happens when a character
   cannot pay a later night is not stated.
5. **Inn alternate mode:** under a condition that was not traced, the inn uses another path that charges 10 × level
   for one full-heal night. Separately, a room with no menu entry sets HP straight to max; its caller was not
   traced.
6. **Unique-item check:** the shop/party/roster check for an existing copy of an item; its callers and the item list
   were not traced.
7. **Maze event gold:** the amount of the floor-1 "gold coins" square was not traced.
8. **Raising someone who died of old age:** the character is left Dead at 57+; whether the temple treats them like
   any other Dead character was not tested.

Tech: [items.md §11](../tech/items.md#11-open-questions--not-found-what-was-tried),
[characters.md §11](../tech/characters.md#11-open-questions--not-found)
