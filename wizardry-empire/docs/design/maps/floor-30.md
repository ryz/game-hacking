# Floor 30: map, squares, monsters

The last floor of the maze (B30F), the bottom of the second, harder area (floors 21-30) and the floor of the true
final battle. How to read the map, coordinates and what each kind of square does: [maps/README.md](README.md).

![Floor 30 map](wizardry-empire-floor-30.png)

## 1. Overview

- 7 squares are solid rock: (0, 9), (0, 10), (2, 9), (2, 10), (0, 14), (2, 14), (4, 12). 37 doors (computed from the
  map). The walls cut the floor into **four parts that do not connect on foot** (computed from the map, one-way doors
  counted as passable, special walls as closed): a main part of 124 squares around the west, north and east, with
  every event; a middle block of 77 squares, (3, 6)-(11, 15), with the guarded square (4, 11) and two hidden spots; a
  south-east block of 44 squares, (8, 0)-(15, 5), with two guarded squares and most of the spinners; and a closed
  strip (12, 0)-(15, 0).
- **Entrance and exits:** **no stairs**, no chute. How the party reaches floor 30 was not traced
  ([findings.md](../findings.md), "Floors 21-30 are not reached by stairs").
- **4 guarded squares**, **8 events** (5 of them one-shot, among them the true final battle), **18 floor traps** (12
  spinners, 2 each of rockfalls, vipers and ceiling traps), **3 hidden spots**, 33 markers and **20 one-way doors**.
- **Zones:** a **damage zone** of 16 squares, the room (12, 9)-(15, 12) in the east, with the maid and the well
  inside; its own encounter area (105) lists only empty formations.
- **Random fights:** areas 32 and 33 alternate square by square almost everywhere outside the damage zone, as on
  floor 1; area 105 in the zone.
- **Monsters:** levels 8-29, groups of 1 to 8 (computed from the formations), with the Star Seizer, From Beyond and
  the Unspeakable among them. Guard chests can reach Bewitching, the best tier ([dungeon.md](../dungeon.md), chest
  quality by floor).

## 2. Squares

| Square (x, y) | What | On this floor |
|---|---|---|
| (15, 14) | The last, strongest monster (one-shot event) | The true final battle. |
| (1, 11) | A man in jet black (one-shot event) | "So Adish is dead". |
| (1, 8) | Space tears open (one-shot event) | A rift monster appears. |
| (12, 7) | The Ancient One from the rift (one-shot event) | Something gigantic comes through a rift. |
| (6, 5) | A giant bow (one-shot event) | A giant bow appears, its arrow aimed at the party. |
| (7, 15) | Magic circle (event) | Unspeakable pact, from Summoner level 38 ([spells.md](../spells.md)). The square has walls on three sides, and its north side, across the map edge to (7, 0), lets the party out but not in, so it cannot be walked into (computed from the map). |
| (15, 11) | Maid (event) | "If you...": a service, not traced. In the damage zone. |
| (12, 10) | Well (event) | "Drink from it?": one random outcome (HP restored, poison, cure, heavy damage or paralysis). In the damage zone. |
| (12, 15), (5, 10), (9, 10) | Hidden spot | Each alone, just outside a closed one-square room (the markers (11, 15), (4, 10), (10, 10)) whose door opens only outward; from the hidden spot the wall back is a special wall, probably a hidden door (inferred). |
| (4, 11), (4, 5) | Guarded square | Fight from area 32, then a chest. (4, 11) is in the middle block. |
| (8, 4), (10, 2) | Guarded square | Fight from area 33, then a chest. South-east block. |
| (11, 5), (13, 5), (9, 3), (11, 3), (13, 3), (15, 3), (9, 1), (11, 1), (13, 1) | Spinner | A grid of spinners on every other square of the south-east block. |
| (3, 3), (5, 1), (1, 0) | Spinner | South-west. |
| (2, 6), (14, 2) | Viper, strength 31 | Each member's save is level/2 + LUK − 31 ([dungeon.md](../dungeon.md)). |
| (3, 1), (10, 0) | Rockfall, strength 31 | |
| (12, 13), (10, 4) | Ceiling trap (TF), strength 31 | |
| (0, 15), (3, 15), (11, 15), (5, 14), (9, 14), (4, 13), (6, 13), (7, 13), (8, 13), (10, 13), (10, 11), (4, 10), (10, 10), (4, 9), (6, 9), (8, 9), (10, 9), (5, 8), (9, 8), (4, 6), (5, 6), (0, 5), (1, 5), (3, 4), (12, 4), (4, 2), (6, 2), (12, 2), (0, 1), (7, 0), (8, 0), (12, 0), (15, 0) | Marker | Nothing visible (auto-map memory, inferred). 33 squares, 20 of them within (3, 6)-(11, 15). |
| (1, 2) → (1, 3), (1, 3) → (2, 3), (1, 5) → (1, 4), (2, 2) → (1, 2), (2, 3) → (2, 2), (4, 10) → (5, 10), (5, 9) → (4, 9), (5, 13) → (4, 13), (6, 10) → (5, 10), (6, 12) → (5, 12), (7, 11) → (8, 11), (7, 11) → (6, 11), (7, 15) → (7, 0), (8, 5) → (9, 5), (8, 10) → (9, 10), (8, 12) → (9, 12), (9, 9) → (10, 9), (9, 13) → (10, 13), (10, 10) → (9, 10), (11, 15) → (12, 15) | One-way doors | Passable only in the direction given. Four of them form a one-way loop in the south-west, (1, 2)-(2, 3); 12 others are in the middle block, around its one-square rooms. |
| (12, 9)-(15, 12) | Damage zone | Each member loses maxHP/4 + 1 HP after every action ([dungeon.md](../dungeon.md)). Doors at (12, 12) and (14, 12) on the north side and (14, 9) on the south side. |

How much damage rockfalls and ceiling traps do, and what their strength changes, was not traced. A viper of strength
31 poisons a member every time except on a roll of 99 (1%) unless level/2 + LUK is above 36 (computed from the viper
rule: rolls 0-4 always poison).

## 3. Monsters

| Area | Where | Formations (one is picked per fight) |
|---|---|---|
| 32 | every other square, guarded squares (4, 11), (4, 5) | Fire Giant ×4 + Titan ×4 + Iron Golem ×4 + Star Seizer ×1, or Lich ×2 + Vampire Qn. ×2 + Vampire Lord ×3 + DragonZombie ×3, or Demon Lord ×2 + Succubus Qn. ×3 + Arch Demon ×2 + Hell Master ×3, or Yasha ×4 + Musashi ×2 + Kunoichi ×2 + Valiant ×3 |
| 33 | every other square, guarded squares (8, 4), (10, 2) | Avenger ×3 + Valiant ×4 + Kunoichi ×3 + Musashi ×1, or Treant ×8 + Rakshasa ×6 + Phoenix ×4 + From Beyond ×1, or Demon Lord ×2 + Succubus Qn. ×3 + Arch Demon ×2 + Hell Master ×3, or Beholder ×4 + Nightcrawler ×4 + Night Rider ×4 + Unspeakable ×1 |
| 105 | damage zone | Empty formations only. What a fight does when it picks one was not traced ([findings.md](../findings.md), "Two damage-zone areas have empty formations"). |

The monsters of the one-shot events (the rift, the giant bow, the Ancient One, the final battle) are not part of
these areas; which fight each event starts was not traced.

| Monster | Lv | HP | AC | Swings | Damage | Spells | Special | EXP | Gold |
|---|---|---|---|---|---|---|---|---|---|
| Fire Giant | 13 | 17d8+5 | -1 | 1 | 3d11+10 | - | - | 5440 | 130 |
| Titan | 17 | 30d8 | 0 | 1 | 7d7+14 | - | - | 9330 | 160 |
| Iron Golem | 15 | 20d8 | 3 | 1 | 5d11 | - | - | 7320 | 150 |
| Star Seizer | 28 | 220d8 | -20 | 1 | 26d8 | Mage 5, Priest 5 | - | 130000 | 240 |
| Lich | 21 | 36d8 | 0 | 1 | 1d11 | Mage 7 | paralysis | 50240 | 180 |
| Vampire Qn. | 22 | 45d8 | -12 | 1 | 2d11 | Mage 7 | level drain 3 | 50000 | 180 |
| Vampire Lord | 23 | 40d8 | -8 | 1 | 2d9 | Mage 6 | level drain 4, calls 25% | 40000 | 180 |
| DragonZombie | 18 | 25d8 | -2 | 3 | 4d9 | Mage 5 | poison, poison breath | 12000 | 170 |
| Demon Lord | 23 | 45d8 | -10 | 1 | 11d11+10 | Mage 7, Priest 3 | level drain 3 | 65000 | 190 |
| Succubus Qn. | 21 | 50d8 | -10 | 4 | 4d11 | Mage 7 | level drain 3 | 57000 | 190 |
| Arch Demon | 22 | 40d8 | -7 | 1 | 13d10 | Mage 4, Priest 6 | level drain 1, calls 25% | 62000 | 190 |
| Hell Master | 22 | 35d8 | -6 | 1 | 11d11 | Mage 6 | level drain 1 | 24000 | 170 |
| Yasha | 20 | 30d8 | -9 | 6 | 2d9+11 | Mage 7 | - | 28580 | 180 |
| Musashi | 20 | 36d8 | -10 | 14 | 2d8+14 | Musashi* 7 | - | 44050 | 180 |
| Kunoichi | 20 | 31d6 | -9 | 7 | 2d9+13 | Kunoichi* 7 | decapitation | 40960 | 180 |
| Valiant | 20 | 35d8 | -10 | 7 | 2d9+13 | Valiant* 7 | - | 37860 | 180 |
| Avenger | 20 | 35d8 | -10 | 7 | 2d9+13 | Avenger* 7 | - | 31670 | 180 |
| Treant | 8 | 10d8 | 2 | 2 | 3d7 | - | - | 710 | 80 |
| Rakshasa | 10 | 12d8 | -5 | 3 | 2d7 | Mage 5, Priest 3 | flees 10% | 2080 | 100 |
| Phoenix | 15 | 21d8 | -2 | 3 | 3d9 | Mage 7 | fire breath | 8000 | 150 |
| From Beyond | 27 | 175d8 | -18 | 1 | 32d10 | Mage 4, Priest 4 | - | 120000 | 240 |
| Beholder | 11 | 13d8 | 0 | 1 | 3d9 | Mage 6 | sleep | 3150 | 110 |
| Nightcrawler | 17 | 36d8 | -4 | 2 | 3d9 | - | poison, level drain 1 | 13000 | 160 |
| Night Rider | 15 | 22d8 | -5 | 3 | 4d9 | - | paralysis | 7180 | 150 |
| Unspeakable | 29 | 200d8+55 | -22 | 1 | 27d8 | Mage 6, Priest 6 | fear | 140000 | 240 |

Spells: the school and the highest spell level cast; * = the school is inferred from the order of the spell schools
([monsters_table.md](../monsters_table.md), which also has the full stats and resistances).

**Notes for play:** the two areas have seven different formations (one is shared), and three of them end in an ancient
monster behind three large groups: the Star
Seizer (220d8 HP, up to 1760; AC -20), From Beyond (32d10 per hit, 32-320, the only hit that can pass 255,
[findings.md](../findings.md), "From Beyond's damage could wrap past 255") and the Unspeakable (AC -22). Three of
the seven have level drainers. The maid and the well sit in the damage zone, so every visit costs each member
maxHP/4 + 1 HP for every action in the zone (all computed from the tables and the map).

## 4. Open questions

- How the party reaches floor 30, and how it leaves after the final battle.
- Which monsters the one-shot events fight (the rift, the giant bow, the Ancient One from the rift, the true final
  battle), and whether they stay done for good apart from the per-visit reset.
- What the maid offers, the odds of the well, and what a fight in the damage zone does with its empty formations.
- How the party gets onto the magic circle (7, 15), which cannot be walked into, and into the middle and south-east
  blocks and the strip (12, 0)-(15, 0); the special walls next to the hidden spots are probably hidden doors
  (inferred).
- Damage of rockfalls and ceiling traps.

Tech: [dungeon.md §4 Floors](../../tech/dungeon.md#4-floors), [§3 Event catalogue](../../tech/dungeon.md#3-event-catalogue),
[§1 Map storage](../../tech/dungeon.md#1-map-storage-and-cell-format); `python3 tools/designtables/floormap.py 30 --list`.
