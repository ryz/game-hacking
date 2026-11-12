# Floor 26: map, squares, monsters

The sixth floor of the second, harder area (floors 21-30), B26F, the first of the five floors without any stairs. How
to read the map, coordinates and what each kind of square does: [maps/README.md](README.md).

![Floor 26 map](wizardry-empire-floor-26.png)

## 1. Overview

- The auto-map calls this floor **B358** ([findings.md](../findings.md), "Floors 21-30 are numbered B30 to B666 on the
  map").
- No solid rock; 6 doors, 2 one-way doors, no secret doors and no locked doors (computed from the map). The floor is
  built around **four square rings** (5 × 5 squares each, dark zone) set in the four quarters, each around a 3 × 3
  room.
- **Parts** (computed from the map, warps followed; with no secret or locked doors, nothing opens later). The walls
  alone cut the floor into **six pieces that do not connect on foot**:
  - the north-east and south-west quarters, joined across the centre (97 squares, with the arrival square (7, 8));
  - the north-west quarter (51 squares, with the guarded square (3, 13) and the warp (3, 12) to floor 27) and the
    east-west corridor along rows 7-8 (24 squares, x 0-5 and 10-15, across the map edge), which the one-way door
    (6, 8) → (5, 8) leads into from the quarter;
  - the south-east quarter (51 squares, with the magic-circle room and its four guards) and the north-south corridor
    along columns 7-8 (24 squares, y 0-5 and 10-15, across the map edge), joined the same way by the one-way door
    (8, 6) → (8, 5);
  - the north-east room (11, 11)-(13, 13), closed on all sides.
  The **14 warps** that stay on this floor join all six pieces: from the arrival square (7, 8) the party reaches
  every square of the floor, and every square can be reached from every other except the warp (3, 12), which leads
  off the floor.
- **Entrance and exits:** **no stairs**, no chute. A party comes down from floor 25 by the warp there, which lands on
  **(7, 8)** ([floor-25.md](floor-25.md)). The way on is the **warp (3, 12)** in the north-west room, just past the
  guarded square (3, 13), to (7, 10) on floor 27 ([floor-27.md](floor-27.md)). One way there from the arrival square
  (computed from the map): the warp (15, 15) to (15, 6) in the south-east quarter, then its warp (9, 7) to (6, 8) in
  the north-west quarter.
- **5 guarded squares**, **1 event** (the Ancient One magic circle), **11 floor traps** (5 vipers, 4 pits, 2
  rockfalls) and **15 warps** (one to floor 27).
- **Zones:** 73 squares of **dark zone** (entering puts out the light: no 3D view, "Pitch darkness!"): the four rings
  and the whole magic-circle room in the south-east.
- **Random fights:** area 28 on the corridors and inner rooms; area 29 (floor 27's monsters) on the 69 dark-zone squares
  other than the guards and on (11, 13) inside the closed north-east room; area 30 on 4 guarded squares.
- **Monsters:** levels 4-23, groups of 1 to 7 (computed from the formations): demons, ninja, Musashi, Kunoichi,
  Avengers, vampires and Leviathans. Guard chests are Lacquered at best ([dungeon.md](../dungeon.md), chest quality
  by floor).

## 2. Squares

| Square (x, y) | What | On this floor |
|---|---|---|
| (12, 3) | Magic circle (event) | Ancient One pact, from Summoner level 36 ([spells.md](../spells.md)). Centre of the south-east room (11, 2)-(13, 4): each of the room's four doors opens onto a guarded square, the circle is entered from the west or east guard, and the four corners are pits. |
| (12, 4) + (11, 3) + (13, 3) | Guarded squares, three of the circle room's four | Fight from area 30, then a chest. They share one once-per-visit mark: after one is fought, the other two probably stay quiet until the next floor change (inferred). |
| (12, 2) | Guarded square | Fight from area 30, then a chest. The fourth guard of the magic-circle room, with its own mark. |
| (3, 13) | Guarded square | Fight from area 28, then a chest. In the north-west room, just inside its door. |
| (11, 4), (13, 4), (11, 2), (13, 2) | Pit, strength 27 | The corners of the magic-circle room. |
| (10, 14), (14, 5), (5, 4) | Viper, strength 27 | On the rings. Each member's save is level/2 + LUK − 27 ([dungeon.md](../dungeon.md)). |
| (8, 13), (2, 8) | Viper, strength 27 | In the corridors. |
| (1, 2) | Rockfall, strength 27 | On the south-west ring. |
| (13, 7) | Rockfall, strength 27 | In a corridor. |
| (3, 12) | Warp | To floor 27 (7, 10). In the north-west room, past the guarded square (3, 13): the only way on from this floor. |
| (15, 15) → (15, 6), (11, 11) → (0, 0), (13, 11) → (8, 5), (7, 10) → (2, 3), (7, 9) → (8, 6), (5, 7) → (13, 13), (9, 7) → (6, 8), (10, 7) → (8, 10), (7, 5) → (2, 2), (2, 4) → (5, 8), (4, 4) → (11, 13), (10, 3) → (5, 3), (14, 3) → (10, 12), (4, 2) → (10, 8) | Warps (14) | To the second square, on this floor. They join the six pieces the walls make (overview). (5, 7) and (4, 4) are the only ways into the closed north-east room, (11, 11) and (13, 11) the ways out; (10, 3) and (14, 3) are in the dark zone. |
| (6, 8) → (5, 8), (8, 6) → (8, 5) | One-way doors | Passable only in the direction given: from the north-west quarter into the east-west corridor, and from the south-east quarter into the north-south corridor, with no way back on foot; the corridors are left by their warps (computed from the map). |
| (1, 10)-(5, 14), (10, 10)-(14, 14), (1, 1)-(5, 5), (10, 1)-(14, 5) | Dark zone | The four rings (their 3 × 3 centres excluded, except in the south-east). |

How much damage pits and rockfalls do, and what their strength changes, was not traced. A viper of strength 27
poisons a member every time except on a roll of 99 (1%) unless level/2 + LUK is above 32 (computed from the viper
rule: rolls 0-4 always poison).

## 3. Monsters

| Area | Where | Formations (one of 4 slots picked per fight) |
|---|---|---|
| 28 | the corridors and inner rooms; guarded square (3, 13) | Balrog ×2 + Gr. Demon ×3 + Poison Giant ×3-4 + Hell Fiend ×3, or Musashi ×2 + Cutthroat ×7 + Master Ninja ×5, or Kunoichi ×4 + Master Ninja ×4 + High Ninja ×4 + High Ninja ×1, or Avenger ×3 + Dark Rider ×2 + Lucky Star ×3 + Sagittarius ×2 |
| 29 | the rings (the dark-zone squares other than the guards) and (11, 13) in the closed north-east room | Vampire Lord ×2 + DragonZombie ×3 + Nightcrawler ×3 + U. Beholder ×2, or Valkyrie ×3 + Dark Rider ×3 + Sword Dancer ×1 + Shogun ×4, or Leviathan ×6 + Umber Hulk ×5 + Carrion Worm ×6, or Leviathan ×5 + Troll ×6 + Lion of Hell ×5 + Carrion Worm ×6 |
| 30 | guarded squares only: the four guards of the magic-circle room | Leviathan ×5 + Troll ×6 + Lion of Hell ×5 + Carrion Worm ×6, or Leviathan ×6 + Umber Hulk ×5 + Carrion Worm ×6, or Hell Master ×2-3 + Hell Fiend ×0-4 + Succubus ×3-4 + Succubus Qn. ×1, or Yasha ×3 + Musashi ×2 + Daimyo ×7 |

| Monster | Lv | HP | AC | Swings | Damage | Special | Spells | EXP | Gold |
|---|---|---|---|---|---|---|---|---|---|
| Balrog | 19 | 30d8 | -4 | 3 | 7d7 | fire breath | Priest 5 | 20000 | 170 |
| Gr. Demon | 18 | 25d8 | -3 | 2 | 5d11 | fear, calls 25% | Mage 4 | 9600 | 170 |
| Poison Giant | 14 | 19d8 | 3 | 1 | 3d13+11 | poison, poison breath | - | 7600 | 140 |
| Hell Fiend | 14 | 20d8 | -1 | 2 | 4d11 | fire breath | Priest 3 | 6700 | 140 |
| Musashi | 20 | 36d8 | -10 | 14 | 2d8+14 | - | Musashi* 7 | 44050 | 180 |
| Cutthroat | 11 | 12d8 | 0 | 3 | 2d9+5 | calls 25% | Mage 4 | 2620 | 110 |
| Master Ninja | 14 | 18d6 | -6 | 4 | 2d9+7 | decapitation | - | 6110 | 140 |
| Kunoichi | 20 | 31d6 | -9 | 7 | 2d9+13 | decapitation | Kunoichi* 7 | 40960 | 180 |
| High Ninja | 10 | 12d6 | -2 | 3 | 2d7+5 | decapitation | - | 1950 | 100 |
| Avenger | 20 | 35d8 | -10 | 7 | 2d9+13 | - | Avenger* 7 | 31670 | 180 |
| Dark Rider | 18 | 24d8 | -7 | 5 | 2d9+9 | - | Priest 6 | 10000 | 170 |
| Lucky Star | 16 | 25d4 | -3 | 4 | 3d5+9 | - | - | 7990 | 150 |
| Sagittarius | 16 | 25d6 | -3 | 5 | 3d9+9 | - | - | 8390 | 160 |
| Vampire Lord | 23 | 40d8 | -8 | 1 | 2d9 | level drain 4, calls 25% | Mage 6 | 40000 | 180 |
| DragonZombie | 18 | 25d8 | -2 | 3 | 4d9 | poison, poison breath | Mage 5 | 12000 | 170 |
| Nightcrawler | 17 | 36d8 | -4 | 2 | 3d9 | poison, level drain 1 | - | 13000 | 160 |
| U. Beholder | 17 | 24d8 | -4 | 1 | 3d11 | level drain 1 | Mage 6 | 9200 | 160 |
| Valkyrie | 19 | 25d8 | -5 | 3 | 4d9+17 | - | Priest 7 | 25480 | 170 |
| Sword Dancer | 18 | 30d8 | -9 | 6 | 2d9+12 | - | - | 16200 | 170 |
| Shogun | 18 | 25d8 | -6 | 5 | 3d9+9 | - | Mage 6 | 13100 | 170 |
| Leviathan | 21 | 65d8 | 2 | 1 | 4d12+1 | - | - | 65720 | 190 |
| Umber Hulk | 9 | 8d8+10 | 2 | 3 | 3d4+1 | fear | - | 890 | 90 |
| Carrion Worm | 4 | 5d8+3 | 7 | 8 | 2d3 | paralysis, flees 10% | - | 450 | 50 |
| Troll | 7 | 8d8+6 | 4 | 2 | 2d5+4 | - | - | 720 | 70 |
| Lion of Hell | 5 | 7d8 | 4 | 1 | 1d12+3 | - | - | 500 | 50 |
| Hell Master | 22 | 35d8 | -6 | 1 | 11d11 | level drain 1 | Mage 6 | 24000 | 170 |
| Succubus | 12 | 14d8 | -2 | 1 | 3d9 | level drain 1 | Mage 5 | 4000 | 120 |
| Succubus Qn. | 21 | 50d8 | -10 | 4 | 4d11 | level drain 3 | Mage 7 | 57000 | 190 |
| Yasha | 20 | 30d8 | -9 | 6 | 2d9+11 | - | Mage 7 | 28580 | 180 |
| Daimyo | 15 | 20d8 | -4 | 4 | 3d9+7 | - | Mage 5 | 6780 | 150 |

Full stats: [monsters_table.md](../monsters_table.md); * = spell school inferred.

**Notes for play:** the Musashi swings 14 times a round for 2d8+14 each (16-30), the most of any monster here.
Two of the four formations on the rings and in the circle room are swarms of 17 or 22 monsters led by 5 or 6
Leviathans (65d8 HP each, up to 520), with 6 Carrion Worms (8 swings, paralysis) in the back. The
Vampire Lord drains 4 levels per hit and the Succubus Queen 3 (all computed from the tables).

## 4. Open questions

- Damage of pits and rockfalls.

Tech: [dungeon.md §4 Floors](../../tech/dungeon.md#4-floors), [§2 Square types](../../tech/dungeon.md#2-square-types),
[§1 Map storage](../../tech/dungeon.md#1-map-storage-and-cell-format),
[§6 Auto-map](../../tech/dungeon.md#6-auto-map) (warps, floor numbers); `python3 tools/designtables/floormap.py 26 --list`.
