# Combat

How a battle is resolved: how rolls work, how the party hits and damages monsters, how monsters hit back, special
hits and saves, spells against resistances, running away, and what a victory pays. Who the monsters are, when a
fight starts and how a monster picks its action are in [monsters.md](monsters.md). Equipment rules (who may wield
what, curses) are in [items.md](items.md); the weapon numbers in combat live here.

Notation: see [README.md](README.md). Untagged numbers are **(data)**, read from the game's own tables or code.
"(game text)" means the number only appears in the museum's description and its code was not traced. Numbers marked
"computed" were worked out here from the stated rule.

---

## Overview

- **Rolls.** Most rolls are either a d20 (a random number from 0 to 19) or a percentile roll (0 to 99).
- **To-hit is THAC0-like for both sides.** Each attacker has a to-hit value where lower is better. The number to
  roll is `to-hit − target AC` (the party also subtracts the weapon's hit bonus), clamped to 1..19, and a d20 roll
  at or above it hits. So every swing hits at least 5 % and at most 95 % of the time.
- **Swings.** A character swings `1 + class bonus by level + weapon bonus` times per round (daggers add 2 to 6, the
  Swift Sword 7). Monsters swing a fixed number of times.
- **Damage.** Weapon dice plus a random Strength bonus (none below STR 13, up to 0-10 at STR 22), then
  multipliers: ×2 against a sleeping target, ×2 with the Clockwork Doll, ×1.5 or ×2 with a slaying weapon against its
  monster family.
- **Special hits** (poison, fear, sleep, paralysis, stone, decapitation, level drain) each get a percentile save based
  on the target's Luck and level, capped at 99 % (95 % against level drain).
- **Spells against monsters**: chance = spell power − the monster's resistance %, kept between 5 % and 95 %; 100 %
  resistance means immune.
- **Escape**: for a standard party, 75 % minus the highest escape block among the monster groups (2 to 18), at most
  95 %.
- **Rewards**: each kill adds its EXP and gold to a pool, split evenly among the members who are OK, Afraid or
  Asleep. Only guarded squares give a chest.
- **Not known yet:** who acts first in a round (initiative, surprise), breath damage, the class-by-class swing and
  to-hit tables, and the critical-hit rule for the party (see Open questions).

---

## How rolls work

Rolls start from a random byte (0-255); a roll over a range scales it:
`result = floor(byte × (n + 1) / 256)` gives a random number from 0 to n. The byte comes from a simple 16-bit
generator (`x = 5x + 16675`, high byte used) **(verified)**; the game keeps two such streams.

Because 256 is not a multiple of 20 or 100, the results are very slightly uneven (computed from the formula):

- a d20 result (0-19) comes up 13 or 12 times in 256, so "a roll of 0" is 13/256 = 5.1 % instead of 5 %;
- a percentile result (0-99) comes up 2 or 3 times in 256, so a "95 %" cap is really 244/256 = 95.3 %.

This document writes chances as the intended round numbers (5 %, 95 %); the real values differ by less than half a
percentage point.

Tech: [characters.md §1 header](../tech/characters.md#characters-races-classes-creation-leveling-aging-statuses-spells), [monsters.md §2.1](../tech/monsters.md#21-when-a-fight-starts-code-204422-4460-emu)

---

## Round structure and initiative

The player sees a battle as rounds: the party and the monster groups act, then the next round begins. Each monster
decides its action once per round with the priority list in [monsters.md](monsters.md#monster-ai-how-a-monster-picks-its-action);
an attacking character or monster then makes all its swings.

**What is not known:** the order in which characters and monsters act within a round, and whether a fight can open
with a surprise round. The battle start was read and contains no random roll except the formation and the group
sizes, so a surprise roll, if it exists, is elsewhere. This is an open question.

**Ranks.** The first three party members are the **front row**. Monster groups 1-2 are the **front ranks**, groups 3-4
the **back ranks**. Ranks decide who monsters can reach ([below](#monster-reach-and-targets)); which monster groups each
party weapon range (S, M, L) can reach was not traced.

Tech: [monsters.md §2.4](../tech/monsters.md#24-surprise--initiative), [monsters.md §4.2](../tech/monsters.md#42-reach-and-targets-code-2262b5-62e0)

---

## Party attacks: swings per round

How many times a character attacks per round; it grows with level.

```
swings = 1 + classBonus + weaponExtraSwings
classBonus = min(cap, (level − 1) / k)        // integer division; k and cap depend on the class
```

| Example class rule (data) | k | cap | Class bonus at level 1 / 11 / 46 (computed) |
|---|---|---|---|
| rule A | 5 | 9 | 0 / 2 / 9 |
| rule B | 10 | 3 | 0 / 1 / 3 |

Which class uses which rule was not traced. Weapon extra swings (the **Swings+** column of
[items_table.md](items_table.md)) are 2 to 6 on daggers and 7 on the Swift Sword; most weapons add 0.

**Notes:** only the main-hand weapon counts for swings (and for damage, below). What a Musashi's second weapon
contributes was not traced.

Tech: [items.md §4.1](../tech/items.md#41-swings-per-round)

---

## Party attacks: to-hit

Each swing rolls separately.

```
miss = clamp(attackerToHit − weaponHitBonus − targetAC, 1, 19)
hit if d20 (0..19) ≥ miss          → hit chance = (20 − miss) / 20, from 5 % to 95 %
```

- **attackerToHit** is a class value that falls with level, plus a second modifier whose source was not traced. For
  one class the class value is `max(0, 33 − level) − 15`, that is `18 − level`, bottoming out at −15. Lower is better.
- **weaponHitBonus** is the weapon's **Hit+** column in [items_table.md](items_table.md): usually 0 to 8.
- **targetAC** is the monster's AC as held in battle (lower is better; 10 to −30 in the bestiary).
- Two attacker states change the number: one lowers `miss` by 4 (easier to hit) and halves damage; another raises it
  by 4 and multiplies damage by 1.25. What these states are was not traced.
- A **long-range (L)** weapon against a monster carrying a certain battle flag hits only on a roll of 0 (5 %); what
  the flag means was not traced.

Example (computed; the class above at level 1, second modifier taken as 0): attackerToHit = 17.

| Weapon (Hit+) | vs Goblin, AC 6 | vs Abyss Lurker, AC −30 |
|---|---|---|
| Long Sword (0) | miss 11 → 45 % | miss 47 → 19 → 5 % |
| Battle Axe (50) | miss −39 → 1 → 95 % | miss −3 → 1 → 95 % |

**Notes:** 20 weapons have a hit bonus of 47 to 50 instead of 0-8 (Battle Axe, Great Axe, Chain Sickle, Quarterstaff,
the staves and rods, Shamshir, the whips, Nunchaku, Cursed Flail, Unholy Mace, Lance, Halberd, Sickle Spear,
Windmill Glaive, Spiked Shield). As the game does it, these always hit at the 95 % cap against any monster. This is a
code reading, not checked in the emulator; it may be intended ("easy to hit") or a data slip. See
[findings.md](findings.md). The Spiked Shield is an off-hand item, and the swing rule reads only the main-hand
weapon, so whether its bonus is ever used is an open question. Rows from [items_table.md](items_table.md):

| # | English | Japanese | Slot | Unid. name | Damage | Swings+ | Hit+ | AC | Range | Throw (keep %) | Classes | Align | Curse | Price | Sell | Use (break %) | Special | HP/step | Lv | Shop |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Battle Axe | バトルアックス | 2H weapon | Axe | 4-12 (2d5+2) |  | 50 |  | S |  | Fig Sam Lor Nin Val Kun | any |  | 180 | 90 |  |  |  | 2 | unlimited |
| 32 | Long Sword | ロングソード | 1H weapon | Sword | 1-8 (1d8) |  |  |  | S |  | Fig Sam Lor Nin Val Mus Kun | any |  | 100 | 50 |  |  |  | 2 | unlimited |

Tech: [items.md §4.2](../tech/items.md#42-to-hit-per-swing), [items.md §11](../tech/items.md#11-open-questions--not-found-what-was-tried)

---

## Party attacks: damage

Each hit rolls its damage separately, in this order:

1. **Weapon dice**: the **Damage** column of [items_table.md](items_table.md), e.g. Long Sword 1-8. A bow, crossbow or
   sling **without matching ammo** rolls each die from 0 to S/4 instead of 0 to S−1, so it does very little.
2. **Strength bonus**: plus a random number from 0 to the value below.

   | STR | up to 12 | 13-15 | 16-17 | 18 | 19 | 20 | 21 | 22 or more |
   |---|---|---|---|---|---|---|---|---|
   | bonus range 0.. | 0 | 1 | 2 | 3 | 4 | 6 | 8 | 10 |

3. **Unarmed** (no weapon): `1 + a random number from 0 to X` instead of weapon dice, where X rises with STR from 0
   (1 from STR 7) to 12 at STR 22. A Ninja adds level/4 to X. Whether the Strength bonus of step 2 is added on top
   is not stated in the tech notes.
4. **Attacker state**: ÷2 (at least 1) in one state, ×1.25 in another (see to-hit above).
5. **Sleeping target**: ×2. **Clockwork Doll** equipped (an accessory): ×2.
6. **Slaying**: ×1.5 or ×2 against the weapon's monster family (next section).

Example (computed): a Long Sword with STR 18 does 1-8 plus 0-3, so 1 to 11 per hit; against a sleeping monster 2 to
22.

**Notes:** with a launcher and ammo, the slaying property comes from the ammo, not from the bow.

Tech: [items.md §4.3](../tech/items.md#43-damage-per-hit-324474-4537), [items.md §2](../tech/items.md#2-equipment-rules)

---

## Slaying weapons

Some weapons multiply their damage against a monster family. The family is the monster's **Type** in
[monsters_table.md](monsters_table.md).

| Property (museum text) | Works against | Damage | Items |
|---|---|---|---|
| vs Demons, Undead | demon or undead | ×1.5 | Sword of Flash |
| vs Demons, Spirits, Dragons | demon, spirit or dragon | ×1.5 | Odin Sword |
| vs Demons | demon | ×1.5 | Silver Quarrel, Kris, Holy Flail, Faust Halberd |
| vs Undead ("damage up 2") | undead | ×1.5 | none |
| vs Undead | undead | **×2** | Exorcist Arrow, Holy Cross Sword, Purified Mace |
| vs Dragons | dragon | ×1.5 | Dragonslayer |

**Other weapon and armour properties** that matter in battle are known only from their museum texts **(game text)**:
critical hit chance +10 % or +5 %, "no critical bonus", magic evade 30 / 50 / 85 %, level-drain evade 50 % / 10 %
(the drain part is confirmed in code, see [Special hits](#special-hits-and-saving-throws)), Hide +10 %, fire or water
damage halved. The base critical-hit rule for the party was not traced.

**Notes:** the two "vs Undead" texts are swapped against the code: the property whose text says "damage up 2" gives
×1.5, and the one that says plain "damage up" gives ×2. No item uses the first one. See [findings.md](findings.md).

Tech: [items.md §4.4](../tech/items.md#44-slaying-byte-38-target-type-bits--monster-record-byte-0e-c51d-code-32454e)

---

## Weapon status effects on monsters

Some party attacks can stone, frighten, put to sleep or paralyze a monster. The chance is

```
chance % = attackerValue − monster level      (roll 0..99; 0-4 always succeeds, 99 always fails)
```

- **Stone** fails against a monster with 100 % Earth resistance.
- **Sleep, paralysis and fear** fail against a monster with 100 % Spirit resistance.

Which weapons or classes produce these effects, and what the attacker value is, was not traced.

**Notes:** a frightened monster can only try to flee; a sleeping or paralyzed one does nothing and takes double
damage while asleep ([monsters.md](monsters.md#monster-ai-how-a-monster-picks-its-action)).

Tech: [monsters.md §5](../tech/monsters.md#5-party-attacks-and-spells-on-monsters)

---

## Monster attacks: to-hit and damage

When a monster attacks it makes all its swings (**Att** in [monsters_table.md](monsters_table.md)) against one target.

```
T = clamp(monsterHitBase + modifier − targetAC, 1, 19)
hit if d20 (0..19) ≥ T              → hit chance = (20 − T) / 20, from 5 % to 95 %
damage per hit = minimum + N rolls of 0..(S−1)     (the Dmg range in monsters_table.md)
```

- **monsterHitBase** is the **Hit** column: lower is more accurate (1 for the top monsters, 19 for Goblins).
- **modifier** was 0 in every attack logged in the emulator **(verified)**; spells presumably change it
  **(inferred)**.
- **targetAC** is the character's AC from equipment plus two battle modifiers, and 2 better while a party-wide
  protection is active **(inferred: a protective spell)**.
- A **sleeping** target takes ×2 damage.
- All hits of the round are added up and then subtracted from HP; at 0 HP or less the character is Dead.
- A **ranged** monster against a party under a missile-shield effect hits only on a roll of 0 (5 %) **(inferred)**.

Example (verified): Crawling Claw, hit base 19, against a character with AC 8: T = 11, so each swing hits 45 %.
Computed from the formula: the same Crawling Claw needs T = 19 (5 %) against AC 0 or better.

**Notes:** because lower AC raises T one-for-one, every point of AC is worth 5 % less chance to be hit, until the 5 %
floor.

Tech: [monsters.md §4.1](../tech/monsters.md#41-hit-and-damage)

---

## Monster reach and targets

A monster's **Reach** and its group's rank decide whom it can attack:

| Reach | From groups 1-2 (front ranks) | From groups 3-4 (back ranks) |
|---|---|---|
| 0 melee | front row (members 1-3) | cannot attack |
| 1 reach | anyone | front row |
| 2-3 ranged | anyone | anyone |

So a melee monster in a back group never attacks; back-row characters are only safe from melee monsters and from
reach monsters in the back groups.

**Notes:** which character is chosen among those allowed was not traced.

Tech: [monsters.md §4.2](../tech/monsters.md#42-reach-and-targets-code-2262b5-62e0)

---

## Special hits and saving throws

After each successful hit, every special hit the monster has is tried once, and the target gets a save:

```
save S = (formula below), at most 99
roll 0..99: the target resists if roll < S
```

Lvl is the target's level (counted as 255 above 255).

| Special | Effect | Save S |
|---|---|---|
| Poison | Poisoned | LUK + VIT + Lvl |
| Fear | Afraid | LUK + IQ + Lvl |
| Sleep | Asleep | LUK + Lvl |
| Paralysis | Paralyzed | LUK + Lvl |
| Stone | Stoned | LUK + Lvl |
| Decapitation (the monster's critical hit) | Dead, HP 0 | LUK + Lvl |
| Level drain | loses as many levels as the monster's drain value | 2 × LUK + 60 + Lvl / 16, at most 95 |

Example (computed): a level-5 character with LUK 10 and VIT 12 resists poison 27 %, sleep 15 %, decapitation 15 %,
and level drain 80 %.

- A status is applied only if it is worse than the target's current one **(inferred)**: an Afraid character can be
  put to sleep, a Stoned one cannot be made Afraid.
- **Level drain protection**: an item with drain evade gives an extra 50 % or 10 % chance to avoid the drain.
- A character drained to level 0 dies (level set to 1, HP 0, Dead). After a drain the stats are lowered to the new
  level's maximums **(inferred)**.

**Notes:** the save grows with level, so the same monster's specials matter less to a high-level party. Level drain
has a high base save (at least 60 %) but its cap is 95 %, so without drain protection it lands at least 1 time in
20. Statuses and their
cures are in [characters.md](characters.md#6-status-ailments-and-cures).

Tech: [monsters.md §4.3](../tech/monsters.md#43-special-hit-effects-code-324fbf-51cd-one-roll-per-special-after-a-hit)

---

## Breath

A monster that can breathe uses it 1/8 of its turns when nothing above it in its priority list fired
([monsters.md](monsters.md#monster-ai-how-a-monster-picks-its-action)). Breath hits the party. The element is fire,
frost, poison, lightning, acid or stone; the battle text names it ("breathed fire").

**Not known:** the breath damage formula and any save against it were not traced.

Tech: [monsters.md §4.4](../tech/monsters.md#44-breath-227121-32-side-not-traced)

---

## Spells against monsters

Attack and status spells check the monster's resistance to the spell's element (one of the 8 in
[monsters.md](monsters.md#what-a-monster-is)).

```csharp
bool SpellAffects(int spellPower, int resistancePercent)
{
    if (resistancePercent >= 100) return false;          // immune
    int chance = Math.Max(0, spellPower - resistancePercent);
    int roll = Random(0, 99);
    if (roll <= 4) return true;                          // always 5 %
    if (roll >= 95) return false;                        // never above 95 %
    return roll < chance;
}
```

- **Spell power** is set by the spell for each cast; the values per spell were not traced
  ([spells.md](spells.md#2-casting)).
- Some spells add an extra roll first (pass thresholds 15, 50 or 40 depending on the spell); which spells, and the
  range of that roll, were not stated in the tech notes.
- Which element each spell uses is a pattern reading **(inferred)**; how spell elements line up with the 8
  resistances is in [spells.md](spells.md#2-casting).

Example (computed, with a hypothetical power of 80): a spell against a Vampire (Fire 20 %) has chance 60 %; against an Abyss Lurker
(100 % everywhere) it never works.

**Notes:** resistance values are shown in the museum and in [monsters_table.md](monsters_table.md) (Resist %).

Tech: [monsters.md §5](../tech/monsters.md#5-party-attacks-and-spells-on-monsters), [characters.md §10.1](../tech/characters.md#101-the-spell-record-246c95-16-bytes--125-id-order)

---

## Statuses in battle

Only the battle effects are listed here; the statuses themselves, cures and the temple are in
[characters.md](characters.md#6-status-ailments-and-cures).

| Status | In battle |
|---|---|
| Afraid | a monster can only try to flee; still shares the rewards |
| Asleep | takes ×2 damage (party and monsters); a monster does nothing; still shares the rewards |
| Paralyzed, Stoned | a monster does nothing; gets no share of the rewards |
| Dead | gets no share of the rewards |

**Not known:** how Afraid, Asleep and Paralyzed wear off during a battle; the effect of Poisoned and Silenced in
battle.

Tech: [characters.md §9](../tech/characters.md#9-status-ailments-and-recovery), [monsters.md §3](../tech/monsters.md#3-monster-turn-ai-code-2261b2-6315)

---

## Hide

A character can try to hide. The reading of the rule is **(inferred)**:

```
threshold = clamp(V − highest (level + living monsters) among the groups, 5, Vmax)
hidden if a roll 0..99 ≥ threshold
```

V and Vmax are battle values whose meaning was not traced. Taken literally, stronger or larger groups lower the
threshold and so make hiding easier, which suggests the reading is incomplete. Some items claim Hide +10 %
**(game text)**.

Tech: [monsters.md §5](../tech/monsters.md#5-party-attacks-and-spells-on-monsters)

---

## Escape

The party can try to run away. On success it returns to the maze with **no EXP, gold or chest**.

```
chance % = 75 + partyBonusA + partyBonusB + 4 × (party size − a count, not traced) − highest escape block among the groups
success if a roll 0..99 is below both 95 and chance
```

The two party bonuses are averages of two character values over the members who are OK or Afraid (meaning not
traced); both are 0 for a standard party.
The escape block is the **Esc** column of [monsters_table.md](monsters_table.md) (2 to 18).

| Against | Escape block | Chance (party bonuses 0) |
|---|---|---|
| Goblins | 10 | 65 % |
| Bowmen | 12 | 63 % |
| dragons | 4 | 71 % |
| the "Ancient One" monsters | 17-18 | 57-58 % |

**Notes:** the cap is 95 %, so running can always fail.

Tech: [monsters.md §6](../tech/monsters.md#6-escape-code-2247c1-4858)

---

## Rewards

What a won fight pays:

- **EXP and gold**: every monster **killed** adds its EXP and gold to two pools. Monsters that fled or are left alive
  give nothing. EXP per monster runs from 30 (Crawling Claw) to 150,000 (Abyss Lurker); gold from 20 to 250.
- **Split**: each pool is divided evenly (integer division, fractions dropped) among the members who are **OK,
  Afraid or Asleep**. Dead, Paralyzed and Stoned members get nothing.
- **Chest**: only a guarded-square victory gives a chest; its gold goes into the same pool ([dungeon.md](dungeon.md#chests),
  [town.md](town.md#gold-where-it-comes-from)).
- **Museum**: killing a monster whose group was **identified** marks it as seen in the museum. Killing an
  unidentified one does not.

Example (computed): six Goblins killed give 6 × 290 = 1740 EXP and 6 × 30 = 180 gold. With six members able to share,
each gets 290 EXP and 30 gold; with one member dead, each of the other five gets 348 EXP and 36 gold.

**Notes:** because the split ignores who did the killing, keeping a weak character alive in the back row gives it a
full share. How the game decides at battle start whether a group is identified was not traced.

Tech: [monsters.md §7](../tech/monsters.md#7-rewards-code-02eee-2f22-split-itemsmd-9), [items.md §9](../tech/items.md#9-gold-sources)

---

## Open questions

- **Initiative and surprise**: the order of actions within a round and any surprise roll were not found.
- **Class tables**: which class uses which swings rule and which to-hit rule; the second to-hit modifier.
- **Weapon range S/M/L**: which monster groups each range can reach.
- **Musashi's second weapon**: only the main-hand weapon is read for swings and damage; what the off-hand weapon adds
  was not traced.
- **Attacker states** that give −4 / ÷2 and +4 / ×1.25, and the monster battle flag that limits long-range weapons.
- **Party critical hits**: the base rule; the +10 % / +5 % / "no critical bonus" properties are museum texts only.
- **Weapon status effects**: which weapons or classes stone, frighten, put to sleep or paralyze, and the attacker
  value.
- **Breath damage** and any save against it.
- **Spell power** per spell, the extra pre-roll, and the element of each spell (pattern reading only).
- **Hide**: the values V and Vmax, and whether the formula really makes hiding easier against stronger groups.
- **Escape**: the two party bonuses and the count in the party-size term.
- **Statuses in battle**: how they wear off; Poisoned and Silenced effects.
- **Unarmed damage**: whether the Strength bonus is added to the unarmed roll.
- **Hit bonus 47-50**: confirm in the emulator that these weapons really always hit at 95 %, and whether the Spiked
  Shield's bonus (off hand) is read at all.
- **Identification** of monster groups at battle start.

Tech: [monsters.md §9](../tech/monsters.md#9-not-found--open), [items.md §11](../tech/items.md#11-open-questions--not-found-what-was-tried)
