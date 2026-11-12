# Designer's notes: quirks, likely bugs and oddities

Behavior in Wizardry Empire (Rev 1) that looks unintended, contradicts its own text, or is simply odd. Each entry
says what the game does (**Behavior**), what was probably meant (**Intended**, a reading, never a fact), how sure
the facts are (**Confidence**, tags as in [README.md](README.md#notation-and-style-binding-for-every-design-document))
and what it means for play (**Impact**).

## Index

Grouped by system, in the order of the [document list](README.md#documents).

| System | Quirk | Confidence | Impact |
|---|---|---|---|
| Characters | [1. Old-age death at 57 ignores its survival roll](#1-old-age-death-at-57-ignores-its-survival-roll) | verified | high |
| Characters | [2. Level-up HP favors low VIT and LUK](#2-level-up-hp-favors-low-vit-and-luk) | data | high |
| Characters | [3. Level-up HP has a 1% one-point case and an unused age step](#3-level-up-hp-has-a-1-one-point-case-and-an-unused-age-step) | data | low |
| Characters | [4. Level 2 costs two steps of the EXP table](#4-level-2-costs-two-steps-of-the-exp-table) | verified | medium |
| Characters | [5. Special-class requirements are never checked](#5-special-class-requirements-are-never-checked) | data | medium |
| Characters | [6. Each race has an unused sixth value](#6-each-race-has-an-unused-sixth-value) | data | none |
| Characters | [7. Room for eight unused extra items per character](#7-room-for-eight-unused-extra-items-per-character) | data | none |
| Spells | [8. Spell-learning chance reads past its table above 22](#8-spell-learning-chance-reads-past-its-table-above-22) | data | low |
| Spells | [9. Class change keeps Mage and Priest spells](#9-class-change-keeps-mage-and-priest-spells) | data | medium (probably intended) |
| Spells | [10. Extra spells keep coming after a class change](#10-extra-spells-keep-coming-after-a-class-change) | inferred | medium |
| Spells | [11. Recall Word comes with a bonus spell](#11-recall-word-comes-with-a-bonus-spell) | data | low (probably intended) |
| Combat, items | [12. Twenty weapons always hit at the 95% cap](#12-twenty-weapons-always-hit-at-the-95-cap) | verified (Battle Axe), data (the others) | high |
| Combat, items | [13. Slaying texts for undead are swapped](#13-slaying-texts-for-undead-are-swapped) | data | low |
| Combat, items | [14. The Thieves' Dagger is used up by a non-Thief](#14-the-thieves-dagger-is-used-up-by-a-non-thief) | inferred | low |
| Combat, items | [15. No item is marked unsellable](#15-no-item-is-marked-unsellable) | data | none |
| Town | [16. Inn rooms charge per night of healing, not per week](#16-inn-rooms-charge-per-night-of-healing-not-per-week) | verified | medium |
| Town | [17. The temple raise roll has 101 outcomes](#17-the-temple-raise-roll-has-101-outcomes) | data | negligible |
| Town | [18. Raising by spell ignores the temple's 70-plus penalty](#18-raising-by-spell-ignores-the-temples-70-plus-penalty) | data | low |
| Town | [19. Two inn options the menu never offers](#19-two-inn-options-the-menu-never-offers) | data | unknown |
| Monsters | [20. Random encounters almost only happen after doors](#20-random-encounters-almost-only-happen-after-doors) | verified (base rate), data (door rate) | high |
| Monsters | [21. Encounter areas 54-100 are unused](#21-encounter-areas-54-100-are-unused) | data | none |
| Monsters | [22. Two damage-zone areas have empty formations](#22-two-damage-zone-areas-have-empty-formations) | data | unknown |
| Monsters | [23. A monster with minimum HP 0 would hang the game](#23-a-monster-with-minimum-hp-0-would-hang-the-game) | data | none (modding) |
| Monsters | [24. From Beyond's damage could wrap past 255](#24-from-beyonds-damage-could-wrap-past-255) | inferred | none in practice |
| Monsters | [25. Monsters that pick a non-battle spell lose their turn](#25-monsters-that-pick-a-non-battle-spell-lose-their-turn) | data | low |
| Monsters | [26. Kills of unidentified monsters are not entered in the museum](#26-kills-of-unidentified-monsters-are-not-entered-in-the-museum) | data | low |
| Monsters | [27. Unused monster data](#27-unused-monster-data) | data | none |
| Dungeon | [28. Floors 21-30 are not reached by stairs](#28-floors-21-30-are-not-reached-by-stairs) | data | high, unresolved |
| Dungeon | [29. Guards and one-shot events re-arm on every floor change](#29-guards-and-one-shot-events-re-arm-on-every-floor-change) | data | high |
| Dungeon | [30. Noticing a hidden spot jumps from 16% to 80%](#30-noticing-a-hidden-spot-jumps-from-16-to-80) | data | low |
| Dungeon | [31. Single squares carry another floor's encounter area](#31-single-squares-carry-another-floors-encounter-area) | data (squares), inferred (fights) | low |
| Dungeon | [32. Stoned members still take damage-zone damage](#32-stoned-members-still-take-damage-zone-damage) | inferred | low |
| Dungeon | [33. Map values with no known effect](#33-map-values-with-no-known-effect) | data | unknown |
| Dungeon | [34. Chest ratings above 47 are never used](#34-chest-ratings-above-47-are-never-used) | data | none |
| Curiosities | [35. The hidden debug mode](#35-the-hidden-debug-mode) | verified | none |

---

## 1. Old-age death at 57 ignores its survival roll

**Behavior:** Age goes up at a "birthday" during an inn stay. If the new age is 57 or more, the character dies of
old age ("... died of old age."): status Dead, HP 0, and the character leaves the party. The game does roll a random
number from 0 to `99 + VIT/2 + LUK/2` and compares it with `age − 56`, but the result of the comparison is never
used, so **every inn birthday at 57 or older is fatal**. The same is true of v1.0. A birthday from 55 to 56 is
survived ("Happy birthday!"). Rules: [characters.md, Aging](characters.md#5-aging).

**Intended:** "Dies if the roll is below `age − 56`": a small, growing risk each year after 56, lower with high VIT
and LUK. For the tested characters (VIT 18, LUK 18) the roll runs from 0 to 117, so the intended rule would kill at
57 only on a roll of 0, 1 chance in 118 (computed).

**Confidence:** Verified. Six characters at age 56 on the last day of the year, each with a different random seed,
stayed at the Cots; the survival roll was read at the moment of the comparison: 89, 89, 59, 50, 8 and 11,
against `age − 56` = 1. Under the intended rule all six would have lived; all six died. A 55-year-old turning 56
survived.

**Impact:** A hard lifespan: from the usual starting age of 16, about 41 game years, roughly 14,800 inn nights.
Every inn night outside the Stables ages the character at any HP (verified); the Stables never age, but they heal
nothing. Anything that adds years (class change, resurrection) brings death closer. A designer reproducing the
game should decide which rule to keep.

Design: [characters.md](characters.md#5-aging), [town.md](town.md#24-aging) ·
Tech: [characters.md §7](../tech/characters.md#7-aging), [items.md §7](../tech/items.md#7-inn-aries-inn)

---

## 2. Level-up HP favors low VIT and LUK

**Behavior:** At each level-up the HP gain is 1 plus a class die, and up to two extra dice are added when a random
number from 0 to 99 is **at least** VIT + LUK. So the lower VIT + LUK, the more extra dice; with VIT + LUK of 100 or
more there is never an extra die. The full rule: [characters.md §4.3](characters.md#43-hp-gained-per-level).

**Intended:** The comparison reversed (extra dice when the roll is **below** VIT + LUK), so that tough, lucky
characters gain more HP (inferred).

**Confidence:** Read from the game's code; not measured in play.

**Impact:** Raising VIT or LUK lowers HP growth, the opposite of what players expect. From VIT + LUK 12 (the lowest
race bases, Elf) to 40 (a maxed Hobbit), the first extra die's chance falls from 88% to 60% (computed).

Design: [characters.md](characters.md#43-hp-gained-per-level) ·
Tech: [characters.md §6.3](../tech/characters.md#63-hp-gained-per-level)

---

## 3. Level-up HP has a 1% one-point case and an unused age step

**Behavior:** Before the normal HP roll, the game checks whether a random number from 0 to 99 equals
`LUK + a random number from 0 to LUK` (about 1%); if so the level gives **only 1 HP**. Just before that it works
out an age bracket and then overwrites it, so age has no effect on HP gain.

**Intended:** The age bracket was probably meant to scale HP gain with age (as it does for stat changes). The 1-HP
case may be a deliberate "bad level" roll (inferred).

**Confidence:** Read from the game's code.

**Impact:** Rare 1-HP levels; age does not slow HP growth.

Design: [characters.md](characters.md#43-hp-gained-per-level) ·
Tech: [characters.md §6.3](../tech/characters.md#63-hp-gained-per-level)

---

## 4. Level 2 costs two steps of the EXP table

**Behavior:** Each class has a table of 16 EXP steps. The total EXP needed to reach level L is the sum of the first
L steps, so level 2 already needs the first **two** steps. A level-1 Fighter needs 1,200 EXP for level 2 and 2,200
for level 3: the second level-up (1,000) is cheaper than the first. Mage 1,520 then 1,300; Thief 1,080 then 840
(differences computed from the EXP table).

**Intended:** Possibly level 2 after the first step only, which would make every level cost more than the one
before. The original v1.0 ROM showed **500** EXP for the same Fighter at the inn (v1.0), so the curve was changed
between revisions; the Rev 1 numbers may be a deliberate retune rather than an off-by-one. Unclear.

**Confidence:** Verified: the inn tells a level-1 Fighter with 0 EXP "1200 more EXP" (Rev 1), "500" on v1.0, and a
level-9 Thief with 29,820 EXP "15500 more", the level-10 total minus his EXP.

**Impact:** The first level takes longer than the second for every class.

Design: [characters.md](characters.md#41-exp-needed) · Tech: [characters.md §6.1](../tech/characters.md#61-exp-needed)

---

## 5. Special-class requirements are never checked

**Behavior:** The class table holds stat, alignment and gender requirements for the five special classes
(Valiant, Avenger, Musashi, Kunoichi, Summoner; e.g. Musashi STR 18, IQ 13, PIE 13, VIT 18, AGI 17, LUK 13, Good or
Neutral). But creation and Change Class only ever offer the nine basic classes, and the legendary item that changes
the class checks only gender (Ninja male, Kunoichi female) and, for the Thieves' Dagger, that the user is a Thief.
The requirements are used only afterwards: the new class resets the stats to race base raised to these minimums
(a new Musashi starts with STR 18, VIT 18, AGI 17).

**Intended:** The requirements were meant to gate the item change; or the item's own class and alignment equip
rules are the real gate (inferred).

**Confidence:** Read from the game's code; no stat or alignment check was found in the special-power rule.

**Impact:** Anyone who can use the item becomes the special class, and weak stats are lifted to the class minimums
for free (while stats above them are lost).

Design: [characters.md](characters.md#33-special-classes-and-their-items) ·
Tech: [characters.md §3.4](../tech/characters.md#34-class-eligibility), [§5.5](../tech/characters.md#55-special-classes-legendary-items)

---

## 6. Each race has an unused sixth value

**Behavior:** The race table has one more value per race after the six stats (Human 6, Elf 6, Dwarf 7, Gnome 6,
Hobbit 5). The game loads it at creation and throws it away.

**Intended:** A leftover racial value, perhaps a base AC or a size (inferred).

**Confidence:** Read from the game's data and code.

**Impact:** None. Races differ only in base stats and bonus points.

Design: [characters.md](characters.md#1-races) · Tech: [characters.md §2](../tech/characters.md#2-races)

---

## 7. Room for eight unused extra items per character

**Behavior:** Each character's saved data has room for eight more items right after the eight real inventory
places. Rev 1 fills it with "empty" and never reads it; v1.0 read it as eight more inventory places (v1.0).

**Intended:** A larger inventory (or a storage) was reduced between revisions (inferred).

**Confidence:** Read from the game's data and code.

**Impact:** None in Rev 1: eight items per character.

Design: [characters.md](characters.md), [items.md](items.md) ·
Tech: [characters.md §4](../tech/characters.md#4-party-record)

---

## 8. Spell-learning chance reads past its table above 22

**Behavior:** At each level-up a caster may learn missing spells with a chance read from a 12-entry table by stat
(11 or less up to 22). A stat above 22 reads past the end into the next class's table: IQ 23 would read the Valiant
table's first entry (5%). Race limits keep IQ and PIE at 20 or below, so in practice only a Hobbit Kunoichi with
LUK 23-24 reads past the last table (values there unknown, probably low).

**Intended:** The table should have been capped at 22 (inferred).

**Confidence:** Read from the game's code.

**Impact:** Tiny: a very lucky Hobbit Kunoichi may learn spells at an unexpected rate.

Design: [spells.md](spells.md#42-extra-spells) · Tech: [characters.md §10.3](../tech/characters.md#103-learning)

---

## 9. Class change keeps Mage and Priest spells

**Behavior:** Changing class resets level and stats, but the Mage and Priest spells the character knows stay
known and castable, with one cast per known spell at each spell level. Special-school spells are lost.

**Intended:** Yes: this is the series' way of building multi-school characters.

**Confidence:** Read from the game's code.

**Impact:** A former Mage or Priest keeps a spell kit in any class. See also entry 10.

Design: [characters.md](characters.md#34-change-class-training-grounds), [spells.md](spells.md#44-after-a-class-change) ·
Tech: [characters.md §5.4](../tech/characters.md#54-change-class), [§10.4](../tech/characters.md#104-spell-slots)

---

## 10. Extra spells keep coming after a class change

**Behavior:** The extra-spell rolls for Mage spells (with IQ) and Priest spells (with PIE) do not check the class.
A character who knows at least one Mage or Priest spell of a spell level, for example a former Mage after a class
change, seems to keep rolling for the missing spells of that level at every level-up, in any class.

**Intended:** Probably only for classes that cast that school (inferred); it may also be accepted as part of the
multi-school design (entry 9).

**Confidence:** Inferred from the game's code; not checked in play (a Fighter with a known Mage spell, leveled up at
the inn, would settle it).

**Impact:** A former caster in a fighting class keeps filling in spell levels he already has, without ever opening
new ones.

Design: [spells.md](spells.md#42-extra-spells) · Tech: [characters.md §10.3](../tech/characters.md#103-learning)

---

## 11. Recall Word comes with a bonus spell

**Behavior:** When a Priest-school caster opens spell level 6, one random spell of that level is learned. If it is
Recall Word, the character also learns one of Magic Armor, Cure All or Bless.

**Intended:** Yes: an explicit special case, presumably so that the camp-only Recall Word does not use up the
level's guaranteed spell.

**Confidence:** Read from the game's code.

**Impact:** Priests are never left with only Recall Word at level 6.

Design: [spells.md](spells.md#41-the-guaranteed-spell) · Tech: [characters.md §10.3](../tech/characters.md#103-learning)

---

## 12. Twenty weapons always hit at the 95% cap

**Behavior:** The number to roll is the attacker's to-hit minus the target's AC minus the weapon's Hit+, kept
between 1 and 19; the attack hits if a random number from 0 to 19 is at least that number, so the hit chance is
always between 5% and 95%. Most weapons have a Hit+ of 0-8. Twenty items have **47-50**: Battle Axe, Great Axe,
Chain Sickle, Quarterstaff, the staves and rods, Shamshir, the whips, Nunchaku, Cursed Flail, Unholy Mace, Lance,
Halberd, Sickle Spear, Windmill Glaive and the Spiked Shield. A bonus that large pins the number at 1, so these
weapons hit 95% of the time against every monster.

**Intended:** Small bonuses. The stored values are the codes of the text characters "/", "0", "1", "2", which
suggests text leaked into the data. "Easy to hit" by design is possible but unlikely at this size (inferred).

**Confidence:** Verified for the Battle Axe: a Fighter's number to roll was 1 on every swing with it (Hit+ 50), and 9
with his sword. The other nineteen items: read from the game's data, same rule.

**Impact:** Cheap or heavy weapons are the most accurate in the game. The Quarterstaff is the starting weapon of
Priests and Bishops, so they hit at 95% from level 1. The Spiked Shield is an off-hand item, and only the main-hand
weapon counts for to-hit, so its bonus probably does nothing (inferred).

Design: [combat.md](combat.md#3-party-attacks-to-hit), [items.md](items.md) ·
Tech: [items.md §4.2](../tech/items.md#42-to-hit-per-swing), [§11](../tech/items.md#11-open-questions--not-found-what-was-tried)

---

## 13. Slaying texts for undead are swapped

**Behavior:** Two "slaying" properties work against undead. The one that does ×1.5 damage says "damage up 2" in
the museum, and the one that does ×2 says only "damage up". The ×1.5 one is on no item; the ×2 one is on the
Exorcist Arrow, the Holy Cross Sword and the Purified Mace.

**Intended:** The texts the other way round (inferred).

**Confidence:** Read from the game's data and code.

**Impact:** The museum understates the three anti-undead weapons.

Design: [combat.md](combat.md#5-slaying-weapons-and-other-weapon-properties), [items.md](items.md) · Tech: [items.md §4.4](../tech/items.md#44-slaying)

---

## 14. The Thieves' Dagger is used up by a non-Thief

**Behavior:** The Thieves' Dagger's special power turns a Thief into a Ninja and is used up. As the game is
written, it is also used up when a character who is not a Thief uses the power, with no class change.

**Intended:** A refusal message with the item kept (inferred).

**Confidence:** Inferred from the order of the steps in the game's code; not observed.

**Impact:** A player who tries it on the wrong character loses the dagger.

Design: [items.md](items.md) · Tech: [items.md §3.3](../tech/items.md#33-special-powers)

---

## 15. No item is marked unsellable

**Behavior:** Items can be marked "cannot be sold", and the shop has the matching refusal ("That item can't be
sold."), but no item is marked.

**Intended:** A cut or unused feature (quest items would be the natural candidates).

**Confidence:** Read from the game's data.

**Impact:** None; every identified, uncursed item can be sold.

Design: [items.md](items.md), [town.md](town.md#11-services) · Tech: [items.md §1](../tech/items.md#1-the-item-record)

---

## 16. Inn rooms charge per night of healing, not per week

**Behavior:** The room menu lists prices "per week" (Cots 10, Economy 50, Suite 200, Royal Suite 500). A stay lasts
7 nights, and the room price is charged for **each night on which the character is still below max HP**; nights at
full HP are free (they still age the character). A character at 1 of 200 HP paid 70 G at the Cots for 7 nights and
healed 104 HP; one at 1 of 10 HP paid 10 G; one at full HP paid nothing. A Royal Suite stay from 1 HP can cost up to
3,500 G.

**Intended:** Either the menu text is loose, or the per-night charge is deliberate ("pay only for the healing").
Unclear.

**Confidence:** Verified (the payments were observed).

**Impact:** Badly hurt characters pay up to 7 times the listed price; healthy characters rest for free.

Design: [town.md](town.md#22-paying) ·
Tech: [characters.md §8](../tech/characters.md#8-inn-rest), [items.md §7](../tech/items.md#7-inn-aries-inn)

---

## 17. The temple raise roll has 101 outcomes

**Behavior:** A temple resurrection succeeds if a random number from 0 to 100 (101 outcomes) is below
c = `base(age) + bonus(VIT) + 1`, which is about c in 101. The game makes that number from one random value of 256
steps, so the exact chance is `ceil(256c / 101) / 256`. The age and VIT tables allow c from 1 to 97, but no race
reaches VIT 22, so the bonus is at most 5 and the real range is **1.2% (age 70 or more, VIT under 7) to 95.3% (under
20, VIT 20-21)**. Example: a 25-year-old with VIT 12 has c = 84, 83%. Full table:
[town.md](town.md#32-raising-the-dead).

**Intended:** A plain percent roll (0 to 99), giving exactly c% (inferred).

**Confidence:** Read from the game's code.

**Impact:** Negligible (about one percentage point).

Design: [town.md](town.md#32-raising-the-dead) · Tech: [items.md §8](../tech/items.md#8-temple-samsara-temple),
[characters.md §9](../tech/characters.md#9-status-ailments-and-recovery)

---

## 18. Raising by spell ignores the temple's 70-plus penalty

**Behavior:** The temple's age base drops to 0 at age 70 and over. The spell version of raising uses the same table
but keeps 10 for every age from 50 up, adds the caster's PIE bonus, and on success ages the target by 1 year only
(the temple: 1-3 years at 89%, and a 61% chance to lose 1 VIT).

**Intended:** Unclear; a cheaper, kinder spell raise may be deliberate.

**Confidence:** Read from the game's code.

**Impact:** Very old characters can only realistically come back through a spell.

Design: [characters.md](characters.md#6-status-ailments-and-cures), [town.md](town.md#32-raising-the-dead) ·
Tech: [characters.md §9](../tech/characters.md#9-status-ailments-and-recovery)

---

## 19. Two inn options the menu never offers

**Behavior:** The inn has two options the menu never offers:
- one that charges `10 × level` for one night that heals fully;
- a room that sets HP to max at once.

What enables them was not traced.

**Intended:** Unknown; perhaps an early inn design or a special case.

**Confidence:** Read from the game's code.

**Impact:** None known.

Design: [town.md](town.md#2-inn) ·
Tech: [characters.md §11](../tech/characters.md#11-open-questions--not-found), [items.md §7](../tech/items.md#7-inn-aries-inn)

---

## 20. Random encounters almost only happen after doors

**Behavior:** After every action in the maze (step, turn, turn-around) the game checks for a random fight:

- **Normally the chance is 1 in 512 (0.2%)**: a 1-in-256 roll followed by a second, even-or-odd roll.
- **Right after walking through a door it is 13 in 256 (5.1%)** (a "1 in 20" roll that comes out slightly
  higher), and it stays there until the next plain step forward or a turn-around. Turning left or right keeps it.
- There is no step counter and no deeper-is-busier rule.

**Intended:** The door rule looks deliberate (monsters wait behind doors). The base rate is so low that it may not
be: the second, even-or-odd roll halves an already rare chance, and nothing explains it. Unclear.

**Confidence:** The base rate is verified: 357 random actions in play gave 803 roll checks, 5 successful first rolls
and 1 fight, which fits 1 in 512. The after-door rate is read from the game's code, not measured.

**Impact:** Corridors are almost safe; fights come from doors. A party that steps through a door and then turns on
the spot keeps the 5.1% chance on every turn, an easy way to farm fights.

Design: [monsters.md](monsters.md#3-when-a-fight-starts), [dungeon.md](dungeon.md#4-fights-in-the-maze) ·
Tech: [monsters.md §2.1](../tech/monsters.md#21-when-a-fight-starts)

---

## 21. Encounter areas 54-100 are unused

**Behavior:** The encounter table has entries 54-100, but no map square and no event uses them. Each is a sliding
window over the formation list (area 54 takes formations 15, 17, 19 and 21; area 55 the next ones, and so on).

**Intended:** A cut "random depth" table, perhaps for a mode that picks fights by depth instead of by square
(inferred).

**Confidence:** Read from the game's data; nothing in the game uses them.

**Impact:** None. A ready-made set of mixed encounter tables for anyone extending the game.

Design: [monsters.md](monsters.md#5-encounter-areas-and-group-formation) ·
Tech: [monsters.md §2.3](../tech/monsters.md#23-group-formation), [dungeon.md §5](../tech/dungeon.md#5-not-found--open)

---

## 22. Two damage-zone areas have empty formations

**Behavior:** Area 104 (the damage zone on floor 27) lists one real formation and two empty ones; area 105 (the
damage zone on floor 30) lists only empty ones.

**Intended:** Unclear: either "no random monsters in these zones" or unfinished data. What the game does when it
picks an empty formation was not traced.

**Confidence:** Read from the game's data (the generated encounter table); the effect in play is unknown.

**Impact:** Unknown: possibly fewer or no random fights in those zones.

Design: [monsters.md](monsters.md#5-encounter-areas-and-group-formation), [dungeon.md](dungeon.md#34-damage-zones-and-anti-magic-zones) ·
Tech: [monsters_table.md](monsters_table.md) (encounter tables)

---

## 23. A monster with minimum HP 0 would hang the game

**Behavior:** A monster's HP is rolled at the start of a fight as a minimum plus dice. If the minimum were 0, the
game would freeze. No monster has it.

**Intended:** A guard against zero HP, written so that it loops forever (inferred).

**Confidence:** Read from the game's code.

**Impact:** None; only relevant when adding monsters.

Design: [monsters.md](monsters.md#1-what-a-monster-is) · Tech: [monsters.md §1](../tech/monsters.md#1-the-monster-record)

---

## 24. From Beyond's damage could wrap past 255

**Behavior:** The damage of one monster hit is added up in a counter that holds only 0 to 255. Only From Beyond can
roll more (32d10, 32-320); a hit of 256 or more would wrap around to a small number (260 would become 4, computed).

**Intended:** The full damage (inferred).

**Confidence:** Inferred from the game's code; never seen. A hit above 255 needs a roll about 5 standard deviations
above the average.

**Impact:** None in practice; relevant only when adding stronger monsters.

Design: [combat.md](combat.md#7-monster-attacks-to-hit-and-damage), [monsters.md](monsters.md) · Tech: [monsters.md §4.1](../tech/monsters.md#41-hit-and-damage)

---

## 25. Monsters that pick a non-battle spell lose their turn

**Behavior:** A spellcasting monster casts with a 25% chance per round. It picks a school it knows and then any
spell up to its top level in that school. If the pick is a spell that cannot be cast in battle, the monster does
nothing that turn.

**Intended:** Picking only battle spells (inferred).

**Confidence:** Read from the game's code.

**Impact:** Casters whose schools include camp-only spells are a little weaker than their spell level suggests.

Design: [monsters.md](monsters.md#6-monster-actions) · Tech: [monsters.md §3](../tech/monsters.md#3-monster-turn)

---

## 26. Kills of unidentified monsters are not entered in the museum

**Behavior:** A monster killed while its group is still unidentified gives EXP and gold as usual but is not entered
as "seen" in the museum.

**Intended:** Probably deliberate: you must know what you killed (inferred).

**Confidence:** Read from the game's code.

**Impact:** Completing the museum needs identified kills.

Design: [combat.md](combat.md#15-rewards), [monsters.md](monsters.md) · Tech: [monsters.md §7](../tech/monsters.md#7-rewards)

---

## 27. Unused monster data

**Behavior:** Each monster has several values that are always 0 or never used: one that is 0 in all 167 monsters,
ten more that are 0 everywhere, a value from 0 to 14 that nothing reads, and a probable picture number that nothing
reads directly. Two type marks have no known meaning: a "golem mark" on the four golems, the Gargoyle, the
Juggernaut and the Kugutsu, and a "ghost mark" on 13 monsters, the ghosts among them (counts from
[monsters_table.md](monsters_table.md), computed).

**Intended:** Room for features that were cut or never added (inferred).

**Confidence:** Read from the game's data.

**Impact:** None known; the two type marks may matter to spells that were not traced.

Design: [monsters.md](monsters.md#1-what-a-monster-is) · Tech: [monsters.md §1](../tech/monsters.md#1-the-monster-record)

---

## 28. Floors 21-30 are not reached by stairs

**Behavior:** Floor 20 has no stairs, and floor 21 has no up stairs. The second area is itself split: floors 21-22
are linked by stairs, floor 22 has no down stairs, floor 23 has no up stairs, floors 23-25 are linked by stairs,
floor 25 has no down stairs, and floors 26-30 have no stairs at all. Chutes exist on floors 24 and 29.

**Intended:** Another way in: the elevator button panels, or an event after the ending (the game notes a second
clear) (inferred). The gaps of the main dungeon (6 → 7, 19 → 20) are inferred to be chutes.

**Confidence:** Read from the maps; how the area is entered was not traced.

**Impact:** The late-game route (floors 21-30, monsters of level 20-30, the true final battle) cannot be described
yet.

Design: [dungeon.md](dungeon.md#2-how-floors-connect) ·
Tech: [dungeon.md §4](../tech/dungeon.md#4-floors), [§5](../tech/dungeon.md#5-not-found--open)

---

## 29. Guards and one-shot events re-arm on every floor change

**Behavior:** Guarded squares fight once and one-shot events run once, but only **per floor visit**: every floor
change resets them. Going down a stair and coming back brings every guard (and its chest) back, and the one-shot
events too (for example the gold coins on floor 1).

**Intended:** Likely deliberate for the guards (a renewable source of chests). Whether the story events (the Demon
King, the final battles) also stay done for good was not traced.

**Confidence:** Read from the game's code. Not yet checked in play whether the reset happens per floor change or per
trip to town.

**Impact:** Guards next to stairs can be farmed for chests and gold by stair-hopping. The floor-13 Umber Hulk guards
stand out: their chests can reach Paulownia, far above anything else on floors 1-20.

Design: [dungeon.md](dungeon.md#4-fights-in-the-maze) ·
Tech: [dungeon.md §2](../tech/dungeon.md#2-square-types), [monsters.md §2.2](../tech/monsters.md#22-fixed-fights)

---

## 30. Noticing a hidden spot jumps from 16% to 80%

**Behavior:** The chance to notice a hidden spot depends on the margin m between the member's skill and the spot's
difficulty: never below 0, about 1% at 0, then 4% per point (4%, 8%, 12%, 16% for m = 1 to 4), and then straight
to **80%** from m = 5.

**Intended:** Probably a steadier climb, for example 4% per point up to the 80% cap (inferred).

**Confidence:** Read from the game's code.

**Impact:** Low: one more point of skill (one level for a Thief adds 5) can multiply the chance by five; past the
jump, more skill adds nothing.

Design: [dungeon.md](dungeon.md#33-hidden-spots) · Tech: [dungeon.md §2](../tech/dungeon.md#2-square-types)

---

## 31. Single squares carry another floor's encounter area

**Behavior:** On floors 22, 23, 24, 27 and 28 a few single squares (some of them stairs, a marker and a trap) carry
the encounter area of another floor: for example area 25 at (14,2) on floor 22, or area 32 on the trap (8,8) of
floor 28. The fight check does not look at the square's type, so a random fight on such a square would use that
area. List of squares: [dungeon.md §8](dungeon.md#8-floor-by-floor).

**Intended:** Probably leftovers from editing the maps (inferred).

**Confidence:** The squares are read from the maps; that a fight there uses the other area is inferred, not seen.

**Impact:** Low: a rare chance of another floor's monsters on those squares. It is also why the encounter tables
list these areas on more floors.

Design: [dungeon.md](dungeon.md#8-floor-by-floor), [monsters.md](monsters.md#5-encounter-areas-and-group-formation) · Tech: [dungeon.md §4](../tech/dungeon.md#4-floors)

---

## 32. Stoned members still take damage-zone damage

**Behavior:** In a damage zone, every member who is not Dead, Ashes or Lost, which includes Stoned members, loses
a quarter of max HP plus 1 per action, so Stoned members are hit too and can die there.

**Intended:** A "still alive" check that forgot Stoned; or deliberate (inferred).

**Confidence:** Inferred: the zone rule and the order of the statuses are both read from the game, but nobody has
walked a Stoned member through a zone.

**Impact:** Carrying a Stoned member through a damage zone turns a cheap cure into a resurrection.

Design: [dungeon.md](dungeon.md#34-damage-zones-and-anti-magic-zones) ·
Tech: [dungeon.md §1](../tech/dungeon.md#1-map-storage-and-cell-format), [characters.md §9](../tech/characters.md#9-status-ailments-and-recovery)

---

## 33. Map values with no known effect

**Behavior:** Two map values do nothing that has been found:
- a fourth kind of wall side besides open, wall and door, whose behavior depends on something not traced;
- squares marked as both zone kinds, on 60 squares of floor 5, 19 of floor 12 and 126 of floor 28. One of the two
  marks also switches the wall pictures, so these squares at least look different.

**Intended:** A decorative marker (different wall pictures) and perhaps a special wall type such as a one-way or
secret wall (inferred).

**Confidence:** The values are read from the maps; their effect is open.

**Impact:** Unknown.

Design: [dungeon.md](dungeon.md#34-damage-zones-and-anti-magic-zones) ·
Tech: [dungeon.md §1](../tech/dungeon.md#1-map-storage-and-cell-format), [§5](../tech/dungeon.md#5-not-found--open)

---

## 34. Chest ratings above 47 are never used

**Behavior:** A chest's value comes from a table row picked by the highest chest rating among the monsters in the
fight. The table has rows up to 63, and rows 49-63 have a flat spread (14-16% Leather bag up to 19% Bewitching). But
no monster has a chest rating above 47 (the highest is the Unspeakable), so those rows never come up. The item roll
uses a list number from 0 to value − 1, and a value of 48 or more would pick a list past the last item list; since
the value never exceeds 47, that never happens.

**Intended:** Spare rows, possibly for a cut monster tier (inferred).

**Confidence:** Read from the game's data (the table and the bestiary's chest ratings).

**Impact:** None. A latent bug for anyone adding stronger monsters.

Design: [dungeon.md](dungeon.md#51-chest-rating-chest-value-tier) ·
Tech: [items.md §10.1](../tech/items.md#101-chest-value-and-type), [§10.2](../tech/items.md#102-chest-contents)

---

## 35. The hidden debug mode

**Behavior:** The developers' debug mode is still in the game. While the STAR*FISH logo is on screen at power-on,
press **Select, Up, Down, A, Left, Start**. From then on, power-on shows a sound-test menu ("BGM / SE / MASK VERSION
1.1 / END") instead of the title, and:
- **Character editor:** at the Training Grounds (View character) or in camp (Inspect), Select on a character opens a
  four-page editor: identity, items, stats, and a monster test page listing four monster numbers (what uses them was
  not traced).
- **Event tester:** in the maze, open the menu and confirm any entry except the first with A while holding Select.
  After a debug notice, a menu lets you pick an event number and its parameters and reset the events; it can run any
  maze event, force a chest of a chosen tier, or trigger the ending.
- Pressing Select in the maze while the mode is on first starts a fixed fight with the current square's monsters.

**Intended:** A development tool left in the retail ROM. Normal play never reaches it.

**Confidence:** Verified (every route reproduced in play, Japanese and English builds).

**Impact:** None for normal play. Useful for testing: any event, any chest tier. Its help texts are untranslated in
the English patch.

Design: none · Tech: [../re/debug-mode.md](../re/debug-mode.md), [../re/reach.md](../re/reach.md)
