# Designer's notes: quirks, likely bugs and oddities

Behavior in Wizardry Empire (Rev 1) that looks unintended, contradicts its own text, or is simply odd. Each entry
has four parts: **Behavior** (what the game does), **Intended** (our reading of what was probably meant, never a
fact), **Confidence** (verified / data / inferred, as defined in [README.md](README.md#notation-and-style-binding-for-every-design-document))
and **Impact** (what it means for play).

## Index

| Quirk | System | Confidence | Impact |
|---|---|---|---|
| [Old-age death at 57 ignores its survival roll](#old-age-death-at-57-ignores-its-survival-roll) | inn, aging | verified (death), data (roll) | high |
| [Inn aging does not match the per-night rule](#inn-aging-does-not-match-the-per-night-rule) | inn, aging | verified (both observations) | high, unresolved |
| [Inn rooms charge per night of healing, not per week](#inn-rooms-charge-per-night-of-healing-not-per-week) | inn | verified | medium |
| [Level-up HP favours low VIT and LUK](#level-up-hp-favours-low-vit-and-luk) | leveling | data | high |
| [Level-up HP has a 1 percent one-point case and an unused age step](#level-up-hp-has-a-1-percent-one-point-case-and-an-unused-age-step) | leveling | data | low |
| [Level 2 costs two steps of the EXP table](#level-2-costs-two-steps-of-the-exp-table) | leveling | verified | medium |
| [Spell-learning chance reads past its table above 22](#spell-learning-chance-reads-past-its-table-above-22) | spells | data | low |
| [Special-class requirements are never checked](#special-class-requirements-are-never-checked) | classes | data | medium |
| [Each race has an unused sixth value](#each-race-has-an-unused-sixth-value) | races | data | none |
| [Twenty weapons always hit at the 95 percent cap](#twenty-weapons-always-hit-at-the-95-percent-cap) | combat, items | data | high |
| [Slaying texts for undead are swapped](#slaying-texts-for-undead-are-swapped) | items | data | low |
| [The Thieves' Dagger is used up by a non-Thief](#the-thieves-dagger-is-used-up-by-a-non-thief) | items | inferred | low |
| [No item uses the cannot-be-sold flag](#no-item-uses-the-cannot-be-sold-flag) | shop | data | none |
| [Chest rows above 47 are never used](#chest-rows-above-47-are-never-used) | chests | data | none |
| [Random encounters almost only happen after doors](#random-encounters-almost-only-happen-after-doors) | encounters | verified (base rate), data (door rate) | high |
| [Encounter areas 54-100 are unused](#encounter-areas-54-100-are-unused) | encounters | data | none |
| [Two damage-zone areas have empty formations](#two-damage-zone-areas-have-empty-formations) | encounters | data | unknown |
| [A monster with minimum HP 0 would hang the game](#a-monster-with-minimum-hp-0-would-hang-the-game) | monsters | data | none (modding) |
| [Monsters that pick a non-battle spell lose their turn](#monsters-that-pick-a-non-battle-spell-lose-their-turn) | monster AI | data | low |
| [Kills of unidentified monsters are not entered in the museum](#kills-of-unidentified-monsters-are-not-entered-in-the-museum) | museum | data | low |
| [Floors 21-30 are not reached by stairs](#floors-21-30-are-not-reached-by-stairs) | dungeon | data | high, unresolved |
| [Guards and one-shot events re-arm on every floor change](#guards-and-one-shot-events-re-arm-on-every-floor-change) | dungeon, chests | data | high |
| [Stoned members still take damage-zone damage](#stoned-members-still-take-damage-zone-damage) | dungeon | inferred | low |
| [Map values with no known effect](#map-values-with-no-known-effect) | dungeon | data | unknown |
| [The temple raise roll has 101 outcomes](#the-temple-raise-roll-has-101-outcomes) | temple | data | negligible |
| [Raising by spell ignores the temple's 70-plus penalty](#raising-by-spell-ignores-the-temples-70-plus-penalty) | resurrection | data | low |
| [Class change keeps Mage and Priest spells](#class-change-keeps-mage-and-priest-spells) | classes, spells | data | medium (probably intended) |
| [Recall Word comes with a bonus spell](#recall-word-comes-with-a-bonus-spell) | spells | data | low (probably intended) |
| [An unused second inventory block](#an-unused-second-inventory-block) | characters | data | none |
| [Hidden inn modes](#hidden-inn-modes) | inn | data | unknown |
| [Unused fields in the monster records](#unused-fields-in-the-monster-records) | monsters | data | none |
| [The hidden debug mode](#the-hidden-debug-mode) | curiosity | verified | none |

---

## Old-age death at 57 ignores its survival roll

**Behavior:** Age goes up at a "birthday" during an inn stay. If the new age is 57 or more, the
character dies of old age ("... died of old age."): status Dead, HP 0, and the character leaves the party. The game
does roll a random number from 0 to `99 + VIT/2 + LUK/2` and compares it with `age − 56`, but the result of the
comparison is never used, so **every inn birthday at 57 or older is fatal**. The same code is in v1.0. A birthday
from 55 to 56 is survived ("Happy birthday!").

**Intended:** "Dies if the roll is below `age − 56`": a small, growing risk each year after 56, lower
with high VIT and LUK. For the tested Fighter (VIT 14, LUK 8) the roll runs from 0 to 110, so the intended rule
would kill at 57 only on a roll of 0, 1 chance in 111 (computed).

**Confidence:** The death at 57 is **verified** in the emulator (age 56, last day of the year, one Cots stay; the
same on the Japanese ROM). The two tech notes disagree on how many runs were made: one sample in the items notes,
three seeds in the character notes. If three is right, three deaths in a row under the intended rule would have
odds of about 1 in 1.4 million (111 cubed, computed), so the ignored roll is all but confirmed. That the result is
unused is **data** (code reading).

**Impact:** A hard lifespan: from the usual starting age of 16, about 41 game years, roughly 14,800 inn
nights. Anything that adds years (class change, resurrection) brings death closer. A designer reproducing the game
should decide which rule to keep.

Design: [characters.md](characters.md), [town.md](town.md) ·
Tech: [characters.md §7](../tech/characters.md#7-aging), [items.md §7](../tech/items.md#7-inn-aries-inn)

---

## Inn aging does not match the per-night rule

**Behavior:** The tech notes describe aging as one day per inn night outside the Stables, 7 nights per
stay, with a birthday every 360 days, and they report a test where the day counter rose by 7 after a Cots stay.
A second emulator test contradicts this: a character aged 50 on the last day of the year, at full HP, stayed at
the Cots; there was **no birthday and the day counter did not change at all**.

**Intended:** Not known. One reading fits both tests: nights count only while the character is still
hurt (the same condition under which the inn charges for the night). This is **untested**.

**Confidence:** Both observations are **verified**, but they were made in different runs and the conditions
(hurt or not) were not compared. Open.

**Impact:** Large if the reading above is right: a character who rests only at full HP would never age at
the inn, which would make the [old-age death](#old-age-death-at-57-ignores-its-survival-roll) avoidable.

Design: [characters.md](characters.md), [town.md](town.md) ·
Tech: [items.md §7](../tech/items.md#7-inn-aries-inn), [characters.md §8](../tech/characters.md#8-inn-rest)

---

## Inn rooms charge per night of healing, not per week

**Behavior:** The room menu lists prices "per week" (Cots 10, Economy 50, Suite 200, Royal Suite 500).
A stay lasts 7 nights, and the room price is charged for **each night on which the character is still below max
HP**; nights at full HP are free. A character at 1 of 200 HP paid 70 G at the Cots for 7 nights and healed 104 HP;
one at 1 of 10 HP paid 10 G. A Royal Suite stay from 1 HP can cost up to 3,500 G.

**Intended:** Either the menu text is loose, or the per-night charge is deliberate ("pay only for the
healing"). Unclear.

**Confidence:** **Verified** (both payments observed).

**Impact:** Badly hurt characters pay up to 7 times the listed price; healthy characters rest almost free.

Design: [town.md](town.md) ·
Tech: [characters.md §8](../tech/characters.md#8-inn-rest), [items.md §7](../tech/items.md#7-inn-aries-inn)

---

## Level-up HP favours low VIT and LUK

**Behavior:** At each level-up the HP gain is one class die plus up to two extra dice, and the extra
dice are rolled when a random number from 0 to 99 is **at least** VIT + LUK. So the lower VIT + LUK, the more extra
dice; with VIT + LUK of 100 or more there is never an extra die. (`Random(n)` = a random number from 0 to n; D = the
class's HP die, 9 for a Fighter.)

```csharp
int gain = 1 + Random(D);
int first = Random(99);
if (first >= VIT + LUK)
{
    gain += Random(D - 1);
    if (Random(99) >= first - (VIT + LUK))
        gain += Random(D - 2);
}
```

Example, Fighter with VIT + LUK = 30: base 1-10 (average 5.5), a 70 % chance of +0-8, then usually another +0-7.

**Intended:** The comparison reversed (extra dice when the roll is **below** VIT + LUK), so that tough,
lucky characters gain more HP. **(inferred)**

**Confidence:** **Data** (code reading); not measured in the emulator.

**Impact:** Raising VIT or LUK lowers HP growth, the opposite of what players expect. From VIT + LUK 12
(the lowest race bases, Elf) to about 40 (a maxed Hobbit), the extra-die chance falls from about 88 % to about 60 %
(computed, ignoring rounding).

Design: [characters.md](characters.md) · Tech: [characters.md §6.3](../tech/characters.md#63-hp-gained-per-level)

---

## Level-up HP has a 1 percent one-point case and an unused age step

**Behavior:** Before the normal HP roll, the game checks whether a random number from 0 to 99 equals
`LUK + a random number from 0 to LUK` (about 1 %); if so the level gives **only 1 HP**. Just before that it works
out an age bracket and then overwrites it, so age has no effect on HP gain.

**Intended:** The age bracket was probably meant to scale HP gain with age (as it does for stat changes).
The 1-HP case may be a deliberate "bad level" roll. **(inferred)**

**Confidence:** **Data** (code reading).

**Impact:** Rare 1-HP levels; age does not slow HP growth.

Design: [characters.md](characters.md) · Tech: [characters.md §6.3](../tech/characters.md#63-hp-gained-per-level)

---

## Level 2 costs two steps of the EXP table

**Behavior:** Each class has a table of 16 EXP steps. The EXP needed for a level is the sum of the first
L steps, so level 2 already needs the first **two** steps. A level-1 Fighter needs 1,200 EXP for level 2 and 2,200
for level 3: the second level-up (1,000) is cheaper than the first. Mage 1,520 then 1,300; Thief 1,080 then 840
(differences computed from the EXP table).

**Intended:** Possibly level 2 after the first step only, which would make every level cost more than the
one before. The original v1.0 ROM showed **500** EXP for the same Fighter at the inn **(v1.0)**, so the curve was
changed between revisions; the Rev 1 numbers may be a deliberate retune rather than an off-by-one. Unclear.

**Confidence:** **Verified**: the inn tells a level-1 Fighter with 0 EXP "1200 more EXP" (Rev 1), "500" on v1.0.

**Impact:** The first level takes longer than the second for every class.

Design: [characters.md](characters.md) · Tech: [characters.md §6.1](../tech/characters.md#61-exp-needed)

---

## Spell-learning chance reads past its table above 22

**Behavior:** At each level-up a caster may learn missing spells with a chance read from a 12-entry table
by stat (11 or less up to 22). A stat above 22 reads past the end into the next class's table: IQ 23 would read the
Valiant table's first entry (5 %). Race limits keep IQ and PIE at 20 or below, so in practice only a Hobbit
Kunoichi with LUK 23-24 reads past the last table (values there unknown, probably low).

**Intended:** The table should have been capped at 22. **(inferred)**

**Confidence:** **Data** (code reading).

**Impact:** Tiny: a very lucky Hobbit Kunoichi may learn spells at an unexpected rate.

Design: [spells.md](spells.md) · Tech: [characters.md §10.3](../tech/characters.md#103-learning)

---

## Special-class requirements are never checked

**Behavior:** The class table holds stat, alignment and gender requirements for the five special classes
(Valiant, Avenger, Musashi, Kunoichi, Summoner; e.g. Musashi STR 18, IQ 13, PIE 13, VIT 18, AGI 17, LUK 13, Good or
Neutral). But creation and Change Class only ever offer the nine basic classes, and the legendary item that changes
the class checks only gender (Ninja male, Kunoichi female) and, for the Thieves' Dagger, that the user is a Thief.
The requirements are used only afterwards: the new class resets the stats to race base raised to these minimums
(a new Musashi starts with STR 18, VIT 18, AGI 17).

**Intended:** The requirements were meant to gate the item change; or the item's own class and alignment
equip rules are the real gate. **(inferred)**

**Confidence:** **Data** (code reading); no stat or alignment check was found in the item handler.

**Impact:** Anyone who can use the item becomes the special class, and weak stats are lifted to the class
minimums for free (while stats above them are lost).

Design: [characters.md](characters.md) · Tech: [characters.md §3.4](../tech/characters.md#34-class-eligibility), [§5.5](../tech/characters.md#55-special-classes-legendary-items)

---

## Each race has an unused sixth value

**Behavior:** The race table has one more value per race after the six stats (Human 6, Elf 6, Dwarf 7,
Gnome 6, Hobbit 5). The game loads it at creation and throws it away.

**Intended:** A leftover racial value, perhaps a base AC or a size. **(inferred)**

**Confidence:** **Data**.

**Impact:** None. Races differ only in base stats and bonus points.

Design: [characters.md](characters.md) · Tech: [characters.md §2](../tech/characters.md#2-races)

---

## Twenty weapons always hit at the 95 percent cap

**Behavior:** To hit, the attacker rolls a random number from 0 to 19 and must reach a number that
starts from the attacker's to-hit value, goes up with the target's AC and goes down by the weapon's hit bonus;
the number is kept between 1 and 19, so the hit chance is always between 5 % and 95 %. Most weapons have a hit
bonus of 0-8. Twenty items have **47-50**: Battle Axe, Great Axe, Chain Sickle, Quarterstaff, the staves and rods,
Shamshir, the whips, Nunchaku, Cursed Flail, Unholy Mace, Lance, Halberd, Sickle Spear, Windmill Glaive and the
Spiked Shield. A bonus that large pins the number at 1, so these weapons hit 95 % of the time against practically
any target.

**Intended:** Small bonuses. The stored values are the codes of the text characters "/", "0", "1", "2",
which suggests text leaked into the data. "Easy to hit" by design is possible but unlikely at this size.
**(inferred)**

**Confidence:** **Data** (the values and the formula); not yet checked in the emulator.

**Impact:** Cheap or heavy weapons are the most accurate in the game. The Quarterstaff is the starting
weapon of Priests and Bishops, so they hit at 95 % from level 1. The Spiked Shield is an off-hand item, and only the
main-hand weapon counts for to-hit, so its bonus probably does nothing. **(inferred)**

Design: [combat.md](combat.md), [items.md](items.md) ·
Tech: [items.md §4.2](../tech/items.md#42-to-hit-per-swing), [§11](../tech/items.md#11-open-questions--not-found-what-was-tried)

---

## Slaying texts for undead are swapped

**Behavior:** Two "slaying" properties work against undead. The one that does ×1.5 damage says "damage
up 2" in the museum, and the one that does ×2 says only "damage up". The ×1.5 one is on no item; the ×2 one is on
the Exorcist Arrow, the Holy Cross Sword and the Purified Mace.

**Intended:** The texts the other way round. **(inferred)**

**Confidence:** **Data**.

**Impact:** The museum understates the three anti-undead weapons.

Design: [items.md](items.md) · Tech: [items.md §4.4](../tech/items.md#44-slaying)

---

## The Thieves' Dagger is used up by a non-Thief

**Behavior:** The Thieves' Dagger's special power turns a Thief into a Ninja and is used up. From the
order of the code, it is also used up when a character who is not a Thief uses the power, with no class change.

**Intended:** A refusal message with the item kept. **(inferred)**

**Confidence:** **Inferred** from the code order; not observed.

**Impact:** A player who tries it on the wrong character loses the dagger.

Design: [items.md](items.md) · Tech: [items.md §3.3](../tech/items.md#33-special-powers)

---

## No item uses the cannot-be-sold flag

**Behavior:** Items have a "cannot be sold" flag, and the shop has the matching refusal ("That item can't
be sold."), but no item has the flag set.

**Intended:** A cut or unused feature (quest items would be the natural users).

**Confidence:** **Data**.

**Impact:** None; every identified, uncursed item can be sold.

Design: [items.md](items.md), [town.md](town.md) · Tech: [items.md §1](../tech/items.md#1-the-item-record)

---

## Chest rows above 47 are never used

**Behavior:** A chest's value comes from a table row picked by the strongest monster in the fight. The
table has rows up to 63, and rows 49-63 have a flat spread (14-16 % Leather bag up to 19 % Bewitching). But no
monster has a chest row above 47 (the highest is the Unspeakable), so those rows never come up. The item roll uses
a list number from 0 to value − 1, and a value of 48 or more would read past the last item list; since the value
never exceeds 47, that never happens.

**Intended:** Spare rows, possibly for a cut monster tier. **(inferred)**

**Confidence:** **Data** (the table and the bestiary's chest rows).

**Impact:** None. The over-read is a latent bug for anyone adding stronger monsters.

Design: [dungeon.md](dungeon.md#chests) ·
Tech: [items.md §10.1](../tech/items.md#101-chest-value-and-type), [§10.2](../tech/items.md#102-chest-contents)

---

## Random encounters almost only happen after doors

**Behavior:** After every action in the maze (step, turn, turn-around) the game checks for a random fight:

- **Normally the chance is 1 in 512 (0.2 %)**: a 1-in-256 roll followed by a second, even-or-odd roll.
- **Right after walking through a door it is 13 in 256 (5.1 %)** (a "1 in 20" roll that comes out slightly
  higher), and it stays there until the next plain step forward or a turn-around. Turning left or right keeps it.
- There is no step counter and no deeper-is-busier rule.

**Intended:** The door rule looks deliberate (monsters wait behind doors). The base rate is so low that
it may not be: the second, even-or-odd roll halves an already rare chance, and nothing explains it. Unclear.

**Confidence:** The base rate is **verified**: 357 random actions in the emulator gave 803 roll checks, 5 successful
first rolls and 1 fight, which fits 1 in 512. The after-door rate is **data** (code reading), not measured.

**Impact:** Corridors are almost safe; fights come from doors. A party that steps through a door and
then turns on the spot keeps the 5.1 % chance on every turn, an easy way to farm fights.

Design: [dungeon.md](dungeon.md#random-encounters), [monsters.md](monsters.md) ·
Tech: [monsters.md §2.1](../tech/monsters.md#21-when-a-fight-starts)

---

## Encounter areas 54-100 are unused

**Behavior:** The encounter table has entries 54-100, but no map square and no event uses them. Each is a
sliding window over the formation list (area 54 takes formations 15, 17, 19 and 21; area 55 the next ones, and so
on).

**Intended:** A cut "random depth" table, perhaps for a mode that picks fights by depth instead of by
square. **(inferred)**

**Confidence:** **Data** (no user found apart from the formation code).

**Impact:** None. A ready-made set of mixed encounter tables for anyone extending the game.

Design: [monsters.md](monsters.md) ·
Tech: [monsters.md §2.3](../tech/monsters.md#23-group-formation), [dungeon.md §5](../tech/dungeon.md#5-not-found--open)

---

## Two damage-zone areas have empty formations

**Behavior:** Area 104 (the damage zone on floor 27) lists one real formation and two empty ones; area
105 (the damage zone on floor 30) lists only empty ones.

**Intended:** Unclear: either "no random monsters in these zones" or unfinished data. What the game does
when it picks an empty formation was not traced.

**Confidence:** **Data** (the generated encounter table); the effect in play is unknown.

**Impact:** Unknown: possibly fewer or no random fights in those zones.

Design: [monsters.md](monsters.md), [dungeon.md](dungeon.md#damage-zones-and-anti-magic-zones) ·
Tech: [monsters_table.md](monsters_table.md) (encounter tables)

---

## A monster with minimum HP 0 would hang the game

**Behavior:** A monster's HP is rolled at the start of a fight as a minimum plus dice. If the minimum were
0, the game would freeze. No monster has it.

**Intended:** A guard against zero HP, written so that it loops forever. **(inferred)**

**Confidence:** **Data** (code reading).

**Impact:** None; only relevant when adding monsters.

Design: [monsters.md](monsters.md) · Tech: [monsters.md §1](../tech/monsters.md#1-the-monster-record)

---

## Monsters that pick a non-battle spell lose their turn

**Behavior:** A spellcasting monster casts with a 25 % chance per round. It picks a school it knows and
then any spell up to its top level in that school. If the pick is a spell that cannot be cast in battle, the
monster does nothing that turn.

**Intended:** Picking only battle spells. **(inferred)**

**Confidence:** **Data** (code reading).

**Impact:** Casters whose schools include camp-only spells are a little weaker than their spell level
suggests.

Design: [monsters.md](monsters.md) · Tech: [monsters.md §3](../tech/monsters.md#3-monster-turn)

---

## Kills of unidentified monsters are not entered in the museum

**Behavior:** A monster killed while its group is still unidentified gives EXP and gold as usual but is
not recorded as "seen" in the museum.

**Intended:** Probably deliberate: you must know what you killed. **(inferred)**

**Confidence:** **Data**.

**Impact:** Completing the museum needs identified kills.

Design: [monsters.md](monsters.md), [town.md](town.md) · Tech: [monsters.md §7](../tech/monsters.md#7-rewards)

---

## Floors 21-30 are not reached by stairs

**Behavior:** Floor 20 has no stairs, and floor 21 has no up stairs. The second area is itself split:
floors 21-22 are linked by stairs, floor 22 has no down stairs, floor 23 has no up stairs, floors 23-25 are linked
by stairs, floor 25 has no down stairs, and floors 26-30 have no stairs at all. Chutes exist on floors 24 and 29.

**Intended:** Another way in: the elevator button panels, or an event after the ending (the game has a
"second clear" flag). **(inferred)** The first ten floors' gaps (6 → 7, 19 → 20) are inferred to be chutes.

**Confidence:** **Data** (the maps); how the area is entered is **not traced**.

**Impact:** The late-game route (floors 21-30, monsters of level 20-30, the true final battle) cannot be
documented yet.

Design: [dungeon.md](dungeon.md#how-floors-connect) · Tech: [dungeon.md §4](../tech/dungeon.md#4-floors), [§5](../tech/dungeon.md#5-not-found--open)

---

## Guards and one-shot events re-arm on every floor change

**Behavior:** Guarded squares fight once and one-shot events run once, but only **per floor visit**:
every floor change clears all of those flags. Going down a stair and coming back brings every guard (and its chest)
back, and the one-shot events too (for example the gold coins on floor 1).

**Intended:** Likely deliberate for the guards (a renewable source of chests). Whether the story events
(the Demon King, the final battles) also have a permanent flag of their own was not traced.

**Confidence:** **Data** (code reading); a reachability note left "per floor or per trip to town" unchecked in the
emulator.

**Impact:** Guards next to stairs can be farmed for chests and gold by stair-hopping. The floor-13 Umber
Hulk guards stand out: their chests can reach Paulownia, far above anything else on floors 1-20.

Design: [dungeon.md](dungeon.md#guarded-squares-and-one-shot-events) ·
Tech: [dungeon.md §2](../tech/dungeon.md#2-square-types), [monsters.md §2.2](../tech/monsters.md#22-fixed-fights)

---

## Stoned members still take damage-zone damage

**Behavior:** In a damage zone, every member whose status is below Dead loses a quarter of max HP plus 1
per action. Stoned comes just below Dead in the status order, so Stoned members are hit too and can die there.

**Intended:** A "still alive" check that forgot Stoned; or deliberate. **(inferred)**

**Confidence:** **Inferred**: the zone rule and the status order are both data, but nobody has walked a Stoned member
through a zone.

**Impact:** Carrying a Stoned member through a damage zone turns a cheap cure into a resurrection.

Design: [dungeon.md](dungeon.md#damage-zones-and-anti-magic-zones) ·
Tech: [dungeon.md §1](../tech/dungeon.md#1-map-storage-and-cell-format), [characters.md §9](../tech/characters.md#9-status-ailments-and-recovery)

---

## Map values with no known effect

**Behavior:** Two map values do nothing that has been found:
- a fourth wall value besides open, wall and door, whose behaviour depends on a flag that was not traced;
- a fourth zone value (both zone marks at once), on 60 squares of floor 5, 19 of floor 12 and 126 of floor 28. One of
  its two marks also switches the wall graphics, so these squares at least look different.

**Intended:** A decorative marker (different wall graphics) and perhaps a special wall type such as a
one-way or secret wall. **(inferred)**

**Confidence:** **Data** for the values; their effect is open.

**Impact:** Unknown.

Design: [dungeon.md](dungeon.md#damage-zones-and-anti-magic-zones) ·
Tech: [dungeon.md §1](../tech/dungeon.md#1-map-storage-and-cell-format), [§5](../tech/dungeon.md#5-not-found--open)

---

## The temple raise roll has 101 outcomes

**Behavior:** A temple resurrection succeeds if a random number from 0 to 100 (101 outcomes) is below
`base(age) + bonus(VIT) + 1`. A 25-year-old with VIT 12 has 84 in 101, 83 %.

**Intended:** A plain percent roll (0 to 99). **(inferred)**

**Confidence:** **Data**.

**Impact:** Negligible (about one percentage point).

Design: [town.md](town.md) · Tech: [items.md §8](../tech/items.md#8-temple-samsara-temple)

---

## Raising by spell ignores the temple's 70-plus penalty

**Behavior:** The temple's age base drops to 0 at age 70 and over. The spell version of raising uses the
same table but keeps 10 for every age from 50 up, adds the caster's PIE bonus, and on success ages the target by
1 year only (the temple: 1-3 years at 89 %, and a 61 % chance to lose 1 VIT).

**Intended:** Unclear; a cheaper, kinder spell raise may be deliberate.

**Confidence:** **Data**.

**Impact:** Very old characters can only realistically come back through a spell.

Design: [characters.md](characters.md), [town.md](town.md) · Tech: [characters.md §9](../tech/characters.md#9-status-ailments-and-recovery)

---

## Class change keeps Mage and Priest spells

**Behavior:** Changing class resets level and stats, but the Mage and Priest spells the character knows
stay known and castable, with one cast per known spell at each spell level. Special-school spells are lost.

**Intended:** Yes: this is the series' way of building multi-school characters.

**Confidence:** **Data**.

**Impact:** A former Mage or Priest keeps a spell kit in any class.

Design: [characters.md](characters.md), [spells.md](spells.md) ·
Tech: [characters.md §5.4](../tech/characters.md#54-change-class), [§10.4](../tech/characters.md#104-spell-slots)

---

## Recall Word comes with a bonus spell

**Behavior:** When a Priest-school caster opens spell level 6, one random spell of that level is learned.
If it is Recall Word, the character also learns one of Magic Armor, Cure All or Bless.

**Intended:** Yes: an explicit special case, presumably so that the camp-only Recall Word does not use up
the level's guaranteed spell.

**Confidence:** **Data**.

**Impact:** Priests are never left with only Recall Word at level 6.

Design: [spells.md](spells.md) · Tech: [characters.md §10.3](../tech/characters.md#103-learning)

---

## An unused second inventory block

**Behavior:** The character record has room for eight more item slots right after the eight real ones.
Rev 1 fills it with "empty" and never reads it; the v1.0 code read it as eight more inventory slots **(v1.0)**.

**Intended:** A larger inventory (or a storage) was reduced between revisions. **(inferred)**

**Confidence:** **Data**.

**Impact:** None in Rev 1: eight slots per character.

Design: [characters.md](characters.md), [items.md](items.md) ·
Tech: [characters.md §4](../tech/characters.md#4-party-record)

---

## Hidden inn modes

**Behavior:** The inn has two paths that the normal menu never uses:
- an alternate mode, switched on by a flag, that charges `10 × level` for one night that heals fully;
- a room with no menu entry that sets HP to max outright.

What turns on the flag, and who calls the hidden room, was not traced.

**Intended:** Unknown; perhaps an early inn design or a special-case path.

**Confidence:** **Data** (code reading).

**Impact:** None known.

Design: [town.md](town.md) ·
Tech: [characters.md §11](../tech/characters.md#11-open-questions--not-found), [items.md §7](../tech/items.md#7-inn-aries-inn)

---

## Unused fields in the monster records

**Behavior:** Each monster record has spare space: one field that is 0 in all 167 monsters, ten more
bytes that are 0 everywhere, a value from 0 to 14 that nothing reads, a probable picture number that nothing reads
directly, and two type marks (one on golems and Wraith-like monsters, one on ghosts) whose meaning is unknown.

**Intended:** Room for features that were cut or never added. **(inferred)**

**Confidence:** **Data**.

**Impact:** None known; the two type marks may matter to spells that were not traced.

Design: [monsters.md](monsters.md) · Tech: [monsters.md §1](../tech/monsters.md#1-the-monster-record)

---

## The hidden debug mode

**Behavior:** The developers' debug mode is still in the game. While the STAR*FISH logo is on screen at
power-on, press **Select, Up, Down, A, Left, Start**. From then on, power-on shows a sound-test menu ("BGM / SE /
MASK VERSION 1.1 / END") instead of the title, and:
- **Character editor:** at the Training Grounds (View character) or in camp (Inspect), Select on a character opens a
  four-page editor: identity, items, stats, and a monster test page listing four monster ids (what uses them was
  not traced).
- **Event tester:** in the maze, open the menu and confirm any entry except the first with A while holding Select.
  After a debug notice, a menu lets you pick an event number and its parameters and clear the event flags; it can
  run any maze event, force a chest of a chosen type, or trigger the ending.
- Pressing Select in the maze while the mode is on first starts a fixed fight with the current square's monsters.

**Intended:** A development tool left in the retail ROM. Normal play never reaches it.

**Confidence:** **Verified** (every route reproduced in the emulator, Japanese and English builds).

**Impact:** None for normal play. Useful for testing: any event, any chest tier. Its help texts are
untranslated in the English patch.

Design: none · Tech: [../re/debug-mode.md](../re/debug-mode.md), [../re/reach.md](../re/reach.md)
