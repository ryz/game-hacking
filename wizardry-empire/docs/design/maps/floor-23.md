# Floor 23: map, squares, monsters

The third floor of the second, harder area (floors 21-30), B23F. How to read the map, coordinates and what each kind
of square does: [maps/README.md](README.md).

![Floor 23 map](wizardry-empire-floor-23.png)

## 1. Overview

- No solid rock; 13 doors (computed from the map). The walls cut the floor into **six parts that do not connect on
  foot** (computed from the map, special walls counted as closed): a main part of 216 squares, two strips along the
  north edge, (0, 14)-(5, 15) and (9, 14)-(15, 15), and three closed rooms: (6, 10)-(7, 12), (6, 14)-(7, 15) and
  (7, 7)-(8, 8).
- **Entrance and exits:** no stairs up. How a party first reaches floor 23 was not traced
  ([findings.md](../findings.md), "Floors 21-30 are not reached by stairs"). **Five stairs down**, all to floor 24:
  (15, 0) in the main part; (0, 15) and (14, 15) in the two north strips; (7, 8) and (8, 7) in the closed room
  (7, 7)-(8, 8), which can only be entered by those stairs from floor 24 (computed from the map).
- **8 guarded squares**, **1 event** (the Shadow Dragon magic circle), **12 floor traps**, **2 pairs of hidden
  spots** and 4 markers.
- **Zones:** 49 squares marked as both zone kinds (no known effect): the west block (0, 6)-(5, 12) except (5, 7) and
  (5, 8), and the 3 × 3 room (12, 2)-(14, 4) around the magic circle.
- **Random fights:** area 25 on almost every square; area 27 (the monsters of floor 25) on (7, 7) and the stairs
  (7, 8), (8, 7); area 26 (the monsters of floor 24) only on the guarded square (5, 8).
- **Monsters:** levels 12-19, up to 4 groups of 1 to 4 (computed from the formations): fighters, ninja, priests,
  bishops and mages, golems, a Balrog. Guard chests here are Platinum at best ([dungeon.md](../dungeon.md), chest
  quality by floor).

## 2. Squares

| Square (x, y) | What | On this floor |
|---|---|---|
| (15, 0), (0, 15), (14, 15), (7, 8), (8, 7) | Stairs down | To floor 24, same square. No stairs up. |
| (13, 3) | Magic circle (event) | Shadow Dragon pact, from Summoner level 31 ([spells.md](../spells.md)). In the both-marks room (12, 2)-(14, 4), entered by the door south of (13, 2); three of the room's squares are pits. |
| (12, 2), (14, 2), (13, 4), (15, 6) | Pit, strength 25 | The first three ring the magic circle. |
| (11, 12), (11, 10) | Rockfall, strength 24 | |
| (1, 8), (11, 3) | Rockfall, strength 25 | (1, 8) is in the west zone block. |
| (13, 11) | Ceiling trap (TF), strength 24 | |
| (3, 2) | Ceiling trap (TF), strength 25 | |
| (15, 3) | Viper, strength 25 | Each member's save is level/2 + LUK − 25 ([dungeon.md](../dungeon.md)). |
| (2, 9) | Spinner | In the west zone block. |
| (0, 14) + (0, 13), (11, 14) + (11, 13) | Hidden spots, in pairs | Each pair faces the other across a special wall; these are the only links between the two north strips (with the stairs at (0, 15) and (14, 15)) and the main part: probably hidden doors (inferred). |
| (8, 15), (6, 13), (15, 13), (8, 11) | Marker | Nothing visible (auto-map memory, inferred). |
| (8, 10), (6, 7), (10, 7), (7, 5), (4, 4), (0, 1), (1, 0) | Guarded square | Fight from area 25, then a chest. |
| (5, 8) | Guarded square | Fight from area 26, then a chest. |
| West block, room (12, 2)-(14, 4) | Both zone marks | 49 squares, see the overview. |

How much damage pits, rockfalls and ceiling traps do, and what their strength changes, was not traced. A viper of
strength 25 poisons a member every time except on a roll of 99 (1%) unless level/2 + LUK is above 30 (computed from
the viper rule: rolls 0-4 always poison).

## 3. Monsters

| Area | Where | Formations (one is picked per fight) |
|---|---|---|
| 25 | everywhere, 7 guarded squares | Gladiator ×1-2 + Overlord ×1-3 + High Wizard ×0-2 + Master Ninja ×0-2, or High Bishop ×2 + Daimyo ×2 + High Priest ×2 + Gunner ×3, or Juggernaut ×3 + Iron Golem ×3 + High Wizard ×2 + Kali ×1-2, or Poison Giant ×2-3 + Balrog ×3 + Succubus ×4 |
| 26 | guarded square (5, 8) | High Bishop ×4 + Mstr. Priest ×2 + High Priest ×2 + Mstr. Bishop ×2, or Archmage ×4 + Juggernaut ×1 + High Wizard ×2 + Kali ×3, or Mstr. Priest ×4 + Mstr. Bishop ×1 + Necromancer ×3 + High Priest ×2, or Mstr. Bishop ×3 + Necromancer ×3 + Swordmaster ×2 + Sagittarius ×2 |
| 27 | (7, 7), (7, 8), (8, 7) | Floor 25's area: formations and stats in [floor-25.md](floor-25.md#3-monsters). |

| Monster | Lv | HP | AC | Swings | Damage | Spells | Special | EXP | Gold |
|---|---|---|---|---|---|---|---|---|---|
| Gladiator | 14 | 18d8 | -4 | 4 | 2d9+8 | - | - | 5980 | 140 |
| Overlord | 14 | 17d8 | -5 | 4 | 2d9+7 | Priest 6 | - | 6650 | 140 |
| High Wizard | 14 | 16d4 | 1 | 2 | 2d4+8 | Mage 6 | - | 6380 | 140 |
| Master Ninja | 14 | 18d6 | -6 | 4 | 2d9+7 | - | decapitation | 6110 | 140 |
| High Bishop | 15 | 18d6 | -2 | 3 | 1d7+8 | Mage 5, Priest 5 | calls 25% | 7050 | 150 |
| Daimyo | 15 | 20d8 | -4 | 4 | 3d9+7 | Mage 5 | - | 6780 | 150 |
| High Priest | 15 | 16d6 | -4 | 3 | 1d6+8 | Priest 6 | calls 25% | 6920 | 150 |
| Gunner | 16 | 18d6 | -1 | 4 | 3d9+7 | - | calls 25% | 7860 | 150 |
| Juggernaut | 17 | 40d8 | 0 | 1 | 11d11 | - | - | 9470 | 170 |
| Iron Golem | 15 | 20d8 | 3 | 1 | 5d11 | - | - | 7320 | 150 |
| Kali | 13 | 19d8 | -2 | 8 | 2d9 | - | - | 5570 | 130 |
| Poison Giant | 14 | 19d8 | 3 | 1 | 3d13+11 | - | poison, poison breath | 7600 | 140 |
| Balrog | 19 | 30d8 | -4 | 3 | 7d7 | Priest 5 | fire breath | 20000 | 170 |
| Succubus | 12 | 14d8 | -2 | 1 | 3d9 | Mage 5 | level drain 1 | 4000 | 120 |
| Mstr. Priest | 16 | 21d6 | -6 | 4 | 1d6+10 | Priest 7 | calls 25% | 8530 | 160 |
| Mstr. Bishop | 16 | 25d6 | -4 | 4 | 1d7+10 | Mage 6, Priest 6 | calls 25% | 8660 | 160 |
| Archmage | 18 | 30d4 | -3 | 4 | 2d5+12 | Mage 7 | - | 9870 | 170 |
| Necromancer | 16 | 26d4 | -1 | 3 | 2d5+10 | Mage 7 | - | 8120 | 160 |
| Swordmaster | 16 | 25d8 | -6 | 5 | 2d9+10 | - | - | 8260 | 160 |
| Sagittarius | 16 | 25d6 | -3 | 5 | 3d9+9 | - | - | 8390 | 160 |

Spells: the school and the highest spell level cast. Full stats and resistances:
[monsters_table.md](../monsters_table.md).

**Notes for play:** 11 of the 20 monsters cast spells, up to level 7 (Archmage, Necromancer, Master Priest), and
the guard at (5, 8) fights mostly casters. The Juggernaut has the most HP (40d8, up to 320) and the hardest single
hit (11d11, 11-121); the Kali swings 8 times. The Succubus is the only level drainer, the Master Ninja the only
decapitator (all computed from the table).

## 4. Open questions

- How the party reaches floor 23: no stairs lead up, and floor 22 has no stairs down.
- What the special walls between the hidden-spot pairs do (probably hidden doors, inferred), and how hard each spot
  is to notice.
- Five guarded squares ((8, 10), (5, 8), (6, 7), (10, 7), (7, 5)) share one "already fought" mark, and (0, 1) and
  (1, 0) share another; whether beating one guard of a set also clears the others for that visit was not traced.
- Damage of pits, rockfalls and ceiling traps.

Tech: [dungeon.md §4 Floors](../../tech/dungeon.md#4-floors), [§2 Square types](../../tech/dungeon.md#2-square-types),
[§1 Map storage](../../tech/dungeon.md#1-map-storage-and-cell-format); `python3 tools/designtables/floormap.py 23 --list`.
