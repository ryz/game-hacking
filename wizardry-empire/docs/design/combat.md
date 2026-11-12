# Combat: rounds, hitting, damage, special hits, spells, escape, rewards

How a battle is resolved: how the party hits and damages monsters, how monsters hit back, special hits and saves,
spells against resistances, hiding, running away, and what a victory pays. Who the monsters are, when a fight starts
and how a monster picks its action are in [monsters.md](monsters.md). Equipment rules (who may wield what, curses)
are in [items.md](items.md); the weapon numbers that matter in battle live here. Random numbers, dice and tags are
written as defined in [README.md](README.md#notation-and-style-binding-for-every-design-document).

---

## Overview

- **One to-hit rule for both sides.** Every attacker has a to-hit value (lower is better). The number to roll is
  `need = clamp(attacker's to-hit − target AC − weapon Hit+, 1, 19)`, and a swing hits if a random number from 0 to
  19 is at least `need`. So every swing hits at least 5% and at most 95% of the time. Monsters have no weapon, so
  their Hit+ is 0.
- **Swings.** A character swings `1 + class bonus by level + the weapon's Swings+` times per round (daggers add 1 to
  6, the Swift Sword 7). A monster swings a fixed number of times, 1 to 14.
- **Damage.** Weapon dice plus a random Strength bonus (none below STR 13, up to 0-10 at STR 22), then multipliers:
  ×2 against a sleeping target, ×2 with the Clockwork Doll, ×1.5 or ×2 with a slaying weapon against its monster
  family.
- **Twenty weapons always hit at 95%.** Their Hit+ is 47 to 50 instead of 0 to 8 (verified for the Battle Axe).
- **Special hits** (poison, fear, sleep, paralysis, stone, decapitation, level drain) each give the struck
  character a save based on LUK and the character's own level, at most 99% (95% against level drain).
- **Spells against monsters:** chance = spell power − the monster's resistance %, kept between 5% and 95%; 100%
  resistance means immune.
- **Escape:** 75% minus the highest escape block among the monster groups (2 to 18), plus party values whose
  meaning was not traced (0 in the party examined); at most 95%.
- **Rewards:** each kill adds its EXP and gold to a pool, split evenly among the members who are OK, Afraid or
  Asleep. Only guarded squares give a chest.
- **Not known yet:** who acts first in a round (initiative, surprise), breath damage, which class uses which swing
  and to-hit rule, and the party's critical-hit rule (see Open questions).

---

## 1. Round structure and ranks

The player sees a battle as rounds: the party and the monster groups act, then the next round begins. Each monster
picks its action once per round from the priority list in [monsters.md](monsters.md#6-monster-actions); an
attacking character or monster then makes all its swings.

**Not known:** the order in which characters and monsters act within a round, and whether a fight can open with a
surprise round. The start of a battle contains no random roll except the choice of formation and the group sizes,
so a surprise roll, if there is one, happens later; it was not traced.

**Ranks.** The first three party members are the **front row**. Monster groups 1-2 are the **front ranks**, groups
3-4 the **back ranks**. Ranks decide whom monsters can reach ([section 8](#8-monster-reach-and-targets)). Which
monster groups each party weapon range (S, M, L) can reach was not traced.

Tech: [monsters.md §2.4](../tech/monsters.md#24-surprise--initiative), [monsters.md §4.2](../tech/monsters.md#42-reach-and-targets)

---

## 2. Party attacks: swings per round

How many times a character attacks per round; it grows with level.

`swings = 1 + class bonus + the weapon's Swings+`, where `class bonus = min(cap, (level − 1) / k)` (rounded down;
k and the cap depend on the class).

| Example class rule | k | cap | Class bonus at level 1 / 11 / 46 (computed) |
|---|---|---|---|
| rule A | 5 | 9 | 0 / 2 / 9 |
| rule B | 10 | 3 | 0 / 1 / 3 |

Which class uses which rule was not traced. The weapon's extra swings are the **Swings+** column of
[items_table.md](items_table.md): 1 to 6 on daggers (most 2 to 6; the Thieves' Dagger and Butterfly Knife 1, the
Main Gauche 6), 3 on the Blade Cusinart, 7 on the Swift Sword, 1 on a few other weapons; most weapons add nothing.

**Notes:** only the main-hand weapon counts, for swings and for damage. What a Musashi's second weapon adds was not
traced.

Tech: [items.md §4.1](../tech/items.md#41-swings-per-round)

---

## 3. Party attacks: to-hit

Each swing rolls separately, with the to-hit rule of [README.md](README.md#notation-and-style-binding-for-every-design-document):
`need = clamp(attacker's to-hit − target AC − weapon Hit+, 1, 19)`; the swing hits if a random number from 0 to 19
is at least `need`, so the hit chance is `(20 − need) × 5%`.

- **The character's to-hit** is a class value that falls with level, plus a second value whose source was not
  traced. For one class the class value is `max(0, 33 − level) − 15`, that is `18 − level`, bottoming out at −15.
  The class value is at most about 20 (at level 1). Lower is better.
- **Hit+** is the weapon's **Hit+** column in [items_table.md](items_table.md): 0 to 8 on most weapons.
- **Target AC** is the monster's **AC** in [monsters_table.md](monsters_table.md) (10 down to −30), plus a second
  battle value whose source was not traced. Whether spells change a monster's AC during battle was not traced.
- **Two attacker conditions** change the number: one lowers `need` by 4 (easier to hit) and halves the damage;
  another raises `need` by 4 and multiplies the damage by 1.25. What puts a character in either condition (a
  status, a spell, a battle command) was not traced.
- A **long-range (L)** weapon against a monster with a certain property hits only on a roll of 0 (5%). What that
  monster property means was not traced.

Example (computed; the class above at level 1, so to-hit 17, with the second value taken as 0):

| Weapon (Hit+) | vs Goblin, AC 6 | vs Abyss Lurker, AC −30 |
|---|---|---|
| Long Sword (0) | need 11, 45% | need 47 → 19, 5% |
| Battle Axe (50) | need −39 → 1, 95% | need −3 → 1, 95% |

### 3.1 Weapons with Hit+ 47 to 50

Twenty weapons have a Hit+ of 47 to 50 instead of 0 to 8: Battle Axe, Great Axe, Chain Sickle, Quarterstaff, the
staves and rods, Shamshir, the whips, Nunchaku, Cursed Flail, Unholy Mace, Lance, Halberd, Sickle Spear, Windmill
Glaive and the Spiked Shield. The bonus is subtracted in full, so `need` is pinned at 1 and these weapons hit 95% of
the time: a Fighter with a Battle Axe needed 1 on every swing, and 9 with his sword against the same monster
(verified). With a to-hit of 18 or less, the need stays at 1 even against the lowest AC in the bestiary, −30
(computed). The values look like a data slip rather than a design choice; see
[findings.md](findings.md). The Spiked Shield is an off-hand item
and only the main-hand weapon is read, so whether its bonus is ever used is an open question.

| Weapon | Damage | Hit+ |
|---|---|---|
| Long Sword | 1-8 (1d8) | 0 |
| Battle Axe | 4-12 (2d5+2) | 50 |
| Halberd | 1-24 (1d24) | 47 |
| Quarterstaff | 1-4 (1d4) | 50 |

Rows from [items_table.md](items_table.md) (Hit+ blank there = 0).

Tech: [items.md §4.2](../tech/items.md#42-to-hit-per-swing), [items.md §11](../tech/items.md#11-open-questions--not-found-what-was-tried)

---

## 4. Party attacks: damage

Each hit rolls its damage separately, in this order:

1. **Weapon dice**: the **Damage** column of [items_table.md](items_table.md), e.g. Long Sword 1d8. A bow, crossbow
   or sling **without matching ammo** rolls each die from 1 to S/4 + 1 instead of 1 to S (S = the die size; computed
   from the rule), so it does very little.
2. **Strength bonus**: plus a random number from 0 to the value below.

   | STR | up to 12 | 13-15 | 16-17 | 18 | 19 | 20 | 21 | 22 or more |
   |---|---|---|---|---|---|---|---|---|
   | bonus up to | 0 | 1 | 2 | 3 | 4 | 6 | 8 | 10 |

3. **Unarmed** (no weapon): 1 + a random number from 0 to X instead of weapon dice, where X rises with STR from 0
   (1 from STR 7) to 12 at STR 22. A Ninja adds level / 4 to X. Whether the Strength bonus of step 2 is added on top
   was not traced.
4. **Attacker condition**: ÷2 (at least 1) in one condition, ×1.25 in the other ([section 3](#3-party-attacks-to-hit)).
5. **Sleeping target**: ×2. **Clockwork Doll** equipped (an accessory): ×2.
6. **Slaying**: ×1.5 or ×2 against the weapon's monster family ([section 5](#5-slaying-weapons-and-other-weapon-properties)).

Example (computed): a Long Sword with STR 18 does 1d8 plus 0-3, so 1 to 11 per hit; against a sleeping monster 2
to 22.

**Notes:** with a launcher and ammo, the slaying property comes from the ammo, not from the bow.

Tech: [items.md §4.3](../tech/items.md#43-damage-per-hit), [items.md §2](../tech/items.md#2-equipment-rules)

---

## 5. Slaying weapons and other weapon properties

Some weapons multiply their damage against a monster family. The family is the monster's **Type** in
[monsters_table.md](monsters_table.md).

| Property (museum text) | Works against | Damage | Items |
|---|---|---|---|
| vs Demons, Undead | demon or undead | ×1.5 | Sword of Flash |
| vs Demons, Spirits, Dragons | demon, spirit or dragon | ×1.5 | Odin Sword |
| vs Demons | demon | ×1.5 | Silver Quarrel, Kris, Holy Flail, Faust Halberd |
| vs Undead ("damage up 2") | undead | ×1.5 | none |
| vs Undead | undead | ×2 | Exorcist Arrow, Holy Cross Sword, Purified Mace |
| vs Dragons | dragon | ×1.5 | Dragonslayer |

**Other weapon and armor properties** that matter in battle are known only from their museum texts (game text):
critical hit chance +10% or +5%, "no critical bonus", magic evade 30% / 50% / 85%, level-drain evade 50% / 10%
(the drain part is confirmed by the game's rules, see [section 9](#9-special-hits-and-saves)), Hide +10%, fire or
water damage halved. The party's base critical-hit rule was not traced.

**Notes:** the two "vs Undead" texts are swapped against what the game does: the property whose text says "damage
up 2" gives ×1.5, and the one that says plain "damage up" gives ×2. No item uses the first one. See
[findings.md](findings.md).

Tech: [items.md §4.4](../tech/items.md#44-slaying)

---

## 6. Weapon status effects on monsters

Some party attacks can stone, frighten, put to sleep or paralyze a monster. The chance is the attacker's value minus
the monster's level, in percent: the effect lands if a random number from 0 to 99 is below it, and 0 to 4 always
land while 99 never does, so the chance is kept between 5% and 99%.

- **Stone** fails against a monster with 100% Earth resistance (9 of the 167 monsters, computed from
  [monsters_table.md](monsters_table.md)).
- **Sleep, paralysis and fear** fail against a monster with 100% Spirit resistance (63 of the 167, computed).

Which weapons or classes produce these effects, and what the attacker's value is, was not traced.

**Notes:** a frightened monster can only try to flee; a sleeping or paralyzed one does nothing, and a sleeping one
takes double damage ([monsters.md](monsters.md#6-monster-actions)).

Tech: [monsters.md §5](../tech/monsters.md#5-party-attacks-and-spells-on-monsters)

---

## 7. Monster attacks: to-hit and damage

When a monster attacks it makes all its swings (**Swings** in [monsters_table.md](monsters_table.md), 1 to 14,
with no cap) against one target. Each swing uses the same to-hit rule as the party, with no weapon:
`need = clamp(monster's to-hit − target AC, 1, 19)`; the swing hits if a random number from 0 to 19 is at least
`need`.

- **The monster's to-hit** is its **Hit** column (lower is more accurate: 1 for the top monsters, 19 for Goblins),
  plus a battle modifier that was 0 in every attack observed (verified); spells probably change it (inferred).
- **Target AC** is the character's AC from equipment plus two battle modifiers (not traced), and 2 better while a
  party-wide protection is active (inferred: a protective spell).
- **Damage per hit** is the **Dmg** dice in [monsters_table.md](monsters_table.md) (Goblin 1d7, Musashi 2d8+14),
  ×2 against a sleeping target.
- All hits of the round are added up and then subtracted from HP; at 0 HP or less the character is Dead.
- A **ranged** monster (Reach 2) against a party under a missile shield hits only on a roll of 0 (5%) (inferred: the
  effect is probably a spell). The game checks Reach 2 only; whether Reach 3 monsters are meant to be affected was
  not traced.

Example (verified): a Crawling Claw (Hit 19) against a character with AC 8: need 11, so each swing hits 45%. Computed
from the rule: the same Crawling Claw needs 19 (5%) against AC 0 or better.

**Notes:** because lower AC raises `need` one for one, every point of AC is worth 5% less chance to be hit, down to
the 5% floor. The damage of a single hit is kept as a number from 0 to 255; only From Beyond (32d10, up to 320) can
roll more, and such a hit would wrap around to a small number (inferred; it needs a roll far above average and was
never seen).

Tech: [monsters.md §4.1](../tech/monsters.md#41-hit-and-damage)

---

## 8. Monster reach and targets

A monster's **Reach** and its group's rank decide whom it can attack:

| Reach | From groups 1-2 (front ranks) | From groups 3-4 (back ranks) |
|---|---|---|
| 0 melee | front row (members 1-3) | cannot attack |
| 1 reach | anyone | front row |
| 2 or 3 ranged | anyone | anyone |

So a melee monster in a back group never attacks; back-row characters are safe only from melee monsters and from
reach monsters in the back groups. Reach 2 and 3 choose targets the same way; the only difference found is the
missile-shield check ([section 7](#7-monster-attacks-to-hit-and-damage)).

**Notes:** which character is chosen among those allowed was not traced.

Tech: [monsters.md §4.2](../tech/monsters.md#42-reach-and-targets), [monsters.md §1](../tech/monsters.md#1-the-monster-record)

---

## 9. Special hits and saves

After each successful hit, every special hit the monster has is tried once, and the struck character gets a save
S. The character resists if a random number from 0 to 99 is below S, so S is the chance to resist, in percent.
**Lvl is the struck character's level**, not the monster's (counted as 255 above 255).

| Special hit | Effect | Save S (at most 99) |
|---|---|---|
| Poison | Poisoned | LUK + VIT + Lvl |
| Fear | Afraid | LUK + IQ + Lvl |
| Sleep | Asleep | LUK + Lvl |
| Paralysis | Paralyzed | LUK + Lvl |
| Stone | Stoned | LUK + Lvl |
| Decapitation (the monster's critical hit) | Dead, HP 0 | LUK + Lvl |
| Level drain | loses as many levels as the monster's drain value | 2 × LUK + 60 + Lvl / 16, at most 95 |

Example (computed): a level-5 character with LUK 10 and VIT 12 resists poison 27%, sleep 15%, decapitation 15% and
level drain 80%.

- A status is applied only if it is worse than the character's current one (inferred): an Afraid character can be
  put to sleep, a Stoned one cannot be made Afraid.
- **Level drain protection:** an item with drain evade gives an extra 50% or 10% chance to avoid the drain.
- A character drained to level 0 dies (level set to 1, HP 0, Dead). After a drain the stats are lowered to the new
  level's maximums (inferred).

**Notes:** the save grows with the character's level, so the same monster's special hits matter less to a
high-level party. Level drain has a high base save (at least 60%) but its cap is 95%, so without drain protection
it lands at least 1 time in 20. Statuses and their cures are in
[characters.md](characters.md#6-status-ailments-and-cures).

Tech: [monsters.md §4.3](../tech/monsters.md#43-special-hit-effects-one-roll-per-special-after-a-hit)

---

## 10. Breath

A monster that can breathe uses it 1 turn in 8 when nothing above it in its priority list fired
([monsters.md](monsters.md#6-monster-actions)). Breath hits the party. The breath is fire, frost, poison, lightning,
acid or stone; the battle text names it ("breathed fire").

**Not known:** the breath damage and any save against it were not traced.

Tech: [monsters.md §4.4](../tech/monsters.md#44-breath)

---

## 11. Spells against monsters

Attack and status spells check the monster's resistance to the spell's element (one of the 8 in
[monsters.md](monsters.md#1-what-a-monster-is)): Earth, Water, Fire, Wind, Spirit, the 6th element, Holy, None.

```csharp
bool SpellAffects(int spellPower, int resistancePercent)
{
    if (resistancePercent >= 100) return false;               // immune
    int chance = Math.Max(0, spellPower - resistancePercent);
    int roll = Rnd(0, 99);
    if (roll <= 4) return true;                               // 0-4 always work: at least 5%
    if (roll >= 95) return false;                             // 95-99 always fail: at most 95%
    return roll < chance;
}
```

- **Spell power** is set by the spell for each cast; the values per spell were not traced
  ([spells.md](spells.md#2-casting)).
- Some spells add an extra roll first (it passes only below 15, 50 or 40, depending on the spell); which spells, and
  the range of that roll, were not traced.
- Which element each spell uses is a pattern reading (inferred); see [spells.md](spells.md#2-casting).

Example (computed, with a supposed power of 80): a spell of the Fire element against a Vampire (Fire 20%) has
chance 60%; against an Abyss Lurker (100% in every element) no spell that checks resistance works.

**Notes:** resistance values are shown in the museum and in the **Resistance %** column of
[monsters_table.md](monsters_table.md).

Tech: [monsters.md §5](../tech/monsters.md#5-party-attacks-and-spells-on-monsters), [characters.md §10.1](../tech/characters.md#101-the-spell-record)

---

## 12. Statuses in battle

Only the battle effects are listed here; the statuses themselves and their cures are in
[characters.md](characters.md#6-status-ailments-and-cures).

| Status | In battle |
|---|---|
| Afraid | a monster can only try to flee; a character still gets a share of the rewards |
| Asleep | takes ×2 damage (party and monsters); a monster does nothing; a character still gets a share of the rewards |
| Paralyzed, Stoned | a monster does nothing; a character gets no share of the rewards |
| Dead | gets no share of the rewards |

**Not known:** how Afraid, Asleep and Paralyzed wear off during a battle; what Poisoned and Silenced do in battle.

Tech: [characters.md §9](../tech/characters.md#9-status-ailments-and-recovery), [monsters.md §3](../tech/monsters.md#3-monster-turn)

---

## 13. Hide

A character can try to hide. This reading of the rule is inferred: the character hides if a random number from 0
to 99 is at least T, where

`T = clamp(V − the highest (level + living monsters) among the groups, 5, Vmax)`

and V and Vmax are two battle values whose meaning was not traced. Taken literally, stronger or larger groups lower
T and so make hiding easier, which suggests the reading is incomplete. Some items claim Hide +10% (game text).

Tech: [monsters.md §5](../tech/monsters.md#5-party-attacks-and-spells-on-monsters)

---

## 14. Escape

The party can try to run away. On success it returns to the maze with **no EXP, gold or chest**.

`chance % = 75 + A + B + 4 × (party size − N) − the highest escape block among the groups`

The escape succeeds if a random number from 0 to 99 is below both 95 and the chance, so it is at most 95%.

- **A and B** are averages of two character values over the members who are OK or Afraid; their meaning was not
  traced, and both were 0 in the party examined.
- **N** is a battle count that was not traced; the examples below take the whole `4 × (party size − N)` term as 0.
- **Escape block** is the **Esc** column of [monsters_table.md](monsters_table.md) (2 to 18).

| Against | Escape block | Chance (A, B and the size term 0) |
|---|---|---|
| Goblins | 10 | 65% |
| Bowmen | 12 | 63% |
| dragons | 4 | 71% |
| the "Ancient One" monsters | 17-18 | 57-58% |

**Notes:** the cap is 95%, so running can always fail.

Tech: [monsters.md §6](../tech/monsters.md#6-escape)

---

## 15. Rewards

What a won fight pays:

- **EXP and gold**: every monster **killed** adds its EXP and gold to two pools. Monsters that fled or are left alive
  give nothing. EXP per monster runs from 30 (Crawling Claw) to 150,000 (Abyss Lurker); gold from 20 G to 250 G.
- **Split**: each pool is divided evenly (rounded down) among the members who are **OK, Afraid or Asleep**. Dead,
  Paralyzed and Stoned members get nothing.
- **Chest**: only a guarded-square victory gives a chest; its gold goes into the same pool
  ([dungeon.md](dungeon.md#52-gold)).
- **Museum**: killing a monster whose group was **identified** marks it as seen in the museum. Killing an
  unidentified one does not ([findings.md](findings.md)).

Example (computed): six Goblins killed give 6 × 290 = 1740 EXP and 6 × 30 = 180 G. With six members able to share,
each gets 290 EXP and 30 G; with one member dead, each of the other five gets 348 EXP and 36 G.

**Notes:** because the split ignores who did the killing, keeping a weak character alive in the back row gives it a
full share. How the game decides at battle start whether a group is identified was not traced.

Tech: [monsters.md §7](../tech/monsters.md#7-rewards), [items.md §9](../tech/items.md#9-gold-sources)

---

## Open questions

- **Initiative and surprise:** the order of actions within a round and any surprise roll were not found.
- **Class rules:** which class uses which swings rule and which to-hit rule; the second part of a character's to-hit.
- **Weapon range S/M/L:** which monster groups each range can reach.
- **Musashi's second weapon:** only the main-hand weapon is read for swings and damage; what the off-hand weapon adds
  was not traced.
- **Attacker conditions** that give −4 / ÷2 and +4 / ×1.25: whether they are statuses, spell effects or commands.
- **Monster AC in battle:** what the second battle value added to a monster's AC is, and whether spells change it.
- **Long-range weapons:** the monster property that limits them to a roll of 0.
- **Missile shield:** which spell sets it, and whether Reach 3 monsters should be affected.
- **Party critical hits:** the base rule; the +10% / +5% / "no critical bonus" properties are museum texts only.
- **Weapon status effects:** which weapons or classes stone, frighten, put to sleep or paralyze, and the attacker's
  value.
- **Breath damage** and any save against it.
- **Spell power** per spell, the extra first roll, and the element of each spell (pattern reading only).
- **Hide:** the values V and Vmax, and whether the rule really makes hiding easier against stronger groups.
- **Escape:** the two party values A and B and the count N.
- **Statuses in battle:** how they wear off; what Poisoned and Silenced do.
- **Unarmed damage:** whether the Strength bonus is added to the unarmed roll.
- **Hit+ 47-50:** whether the values are intended, and whether the Spiked Shield's bonus (off hand) is read at all.
- **Identification** of monster groups at battle start.

Tech: [monsters.md §9](../tech/monsters.md#9-not-found--open), [items.md §11](../tech/items.md#11-open-questions--not-found-what-was-tried)
