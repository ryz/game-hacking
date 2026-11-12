# Floor 9: map, squares, monsters

The ninth floor of the maze (B9F); how to read the map, coordinates and what each kind of square does:
[maps/README.md](README.md).

![Floor 9 map](wizardry-empire-floor-09.png)

## 1. Overview

- 89 squares are solid rock; the rest is corridors and rooms with 10 doors and 10 one-way doors, plus 2 secret
  doors and 10 locked doors; the one-way doors are the ten cell doors, which are locked doors seen from the room
  (computed from the map).
- **Entrance and exits:** two stairs up to floor 8, at (13, 13) and (4, 14); the stairs down to floor 10 at (0, 15).
  The stair at (4, 14) lands in a two-square room closed by a secret door (below).
- **8 guarded squares**, **6 events** (a magic circle, two recruitable adventurers, two signs, a key-hole), **a button
  panel**, **4 pits** and **2 pairs of hidden spots**.
- **Ten one-square cells** in the south-west, in two rows at (1-5, 0) and (1-5, 3), hold two adventurers and four
  guarded squares. Each cell opens outward only, by a one-way door; from the room between the rows the same side is a
  locked door, so each cell is entered by picking its lock (computed from the map).
- **Route** (computed from the map): from the stairs down or the up stairs at (13, 13) the party reaches 152 of the
  167 open squares with every secret and locked door shut, and all of them with the doors open. Behind the doors are
  the ten cells, the stair room at (4, 14) and the circle room; nothing on the floor stays closed.
- **Random fights** all come from area 11 (163 squares). Area 12, the monster set of floor 10, appears only on the
  four guarded squares in the cells.
- **Monsters:** levels 1-10, 1 to 7 per group: elementals, Medusas, undead (Wights, Mummies), Nagpas and Mind Flayers
  with Mage spells up to level 5.
- **Chests:** the guard fights rate 10-12, so the best chest is Bronze (computed from the monsters' chest ratings in
  [monsters_table.md](../monsters_table.md); tiers in [dungeon.md](../dungeon.md)).

## 2. Squares

| Square (x, y) | What | On this floor |
|---|---|---|
| (13, 13), (4, 14) | Stairs up | To floor 8 (its two stairs down). The room at (4, 14)-(5, 14) has no way out but the secret door east of (5, 14) (computed from the map); on floor 8 the same stair ends in the closed room of the hermit ([floor-08.md](floor-08.md)), so the hermit is reached only from this floor, through that secret door. |
| (0, 15) | Stairs down | To floor 10. |
| (11, 5) | Magic circle (event) | Djinni pact, from Summoner level 14 ([spells.md](../spells.md)). Its room, (11, 5) to (13, 5), is closed by the secret door east of (13, 5) (computed from the map). |
| (1, 0) | Adventurer (event) | Laila offers to join ([dungeon.md](../dungeon.md)). In a cell, behind a lock of difficulty 55. |
| (3, 3) | Adventurer (event) | Kojiro offers to join. In a cell, behind a lock of difficulty 55. |
| (9, 3), (8, 1) | Sign (event) | Text not traced. |
| (13, 15) | Button panel | Buttons A-E: the elevator (inferred); destinations not traced. Its only door opens onto the key-hole square (14, 15). |
| (14, 15) | Key-hole (event) | "Beside the door is a hole for slipping something in": the door to the button panel. Which item it takes: not traced. |
| (9, 13), (4, 10), (12, 6), (6, 4) | Pit | |
| (6, 14) + (5, 14), (14, 5) + (13, 5) | Hidden spots, in pairs | Each pair faces the secret door between them; Search here, facing the other spot, finds it (from outside: (6, 14) and (14, 5), facing west). Noticing difficulty 55 for both. These two doors are the only ways into the stair room at (4, 14) and the circle room (computed from the map). |
| (1, 0) → (1, 1) to (5, 0) → (5, 1); (1, 3) → (1, 2) to (5, 3) → (5, 2) | One-way doors | The ten cell doors, passable only out of the cell (northward from the lower row, southward from the upper row), so the way out is always open. Each is a locked door seen from the room (next row). |
| (1, 1) ↔ (1, 0) to (5, 1) ↔ (5, 0); (1, 2) ↔ (1, 3) to (5, 2) ↔ (5, 3) | Locked doors, 10 | One per cell, picked from the room facing the cell (south for the lower row, north for the upper). Difficulty 45, a Thief has a real chance from level 10; Laila's cell (1, 0) and Kojiro's cell (3, 3) have difficulty 55, from level 12 (computed). |
| (1, 10), (1, 5), (9, 2), (13, 2) | Guarded square | Fight from area 11, then a chest. |
| (1, 3), (5, 3), (2, 0), (4, 0) | Guarded square | Fight from area 12 (floor 10's monsters), then a chest. In cells. |

The cells at (3, 0), (5, 0), (2, 3) and (4, 3) are empty.

**Secret and locked doors** (rules: [dungeon.md](../dungeon.md) §3.6): Search finds a secret door every time;
noticing a hidden spot first is only a hint, and the noticing difficulty is what a member's noticing skill must beat
for it (§3.3). A lock of difficulty D gives a Thief a real chance from level D/5 + 1: there 10% + AGI, then 10% more
per level, at most 95%; at level D/5 only about 1%. A Ninja needs 5 levels more, a Kunoichi 10 (computed from the
rule). Found and picked doors stay open for good (inferred).

## 3. Monsters

| Area | Where | Formations (one of 4 slots picked per fight) |
|---|---|---|
| 11 | every square except the 4 guarded cells (163 squares); 4 guarded squares | Earth Elem. ×2 + Water Elem. ×0-1 + Air Elem. ×2 + Water Elem. ×1, or Lion of Hell ×3 + Medusa ×1 + Gr. Medusa ×2-3 + Cerberus ×0-2, or Wight ×3 + Mummy ×3-4 + Wight ×0-2, or Kobold ×2 + Dark Elf ×2-3 + Nagpa ×2-4 + Mind Flayer ×1 |
| 12 | guarded squares only: the 4 guards in the cells | Lizard Man ×2 + Yuan-ti ×2 + Water Elem. ×2-3 + Lizard King ×1-2, or Goblin King ×3-4 + Dark Elf ×3-5 + Nagpa ×2 + Mind Flayer ×0-1, or Orc ×4 + Troll ×2 + Nagpa ×2 + Mind Flayer ×0-2, or Nightmare ×3-7 + Mummy ×2 + Vampire ×1 |

| Monster | Lv | HP | AC | Swings | Damage | Special | Spells | EXP | Gold |
|---|---|---|---|---|---|---|---|---|---|
| Earth Elem. | 8 | 10d8 | 2 | 1 | 5d9 | - | - | 850 | 80 |
| Water Elem. | 8 | 10d8 | 2 | 1 | 6d7 | - | - | 840 | 80 |
| Air Elem. | 8 | 10d8 | 2 | 1 | 3d11 | - | - | 760 | 80 |
| Lion of Hell | 5 | 7d8 | 4 | 1 | 1d12+3 | - | - | 500 | 50 |
| Medusa | 6 | 8d8 | 5 | 1 | 1d5 | poison, stone, calls 25% | - | 570 | 60 |
| Gr. Medusa | 7 | 9d8 | 3 | 1 | 3d6 | poison, stone | - | 700 | 70 |
| Cerberus | 7 | 10d8 | -2 | 3 | 3d9 | - | - | 730 | 70 |
| Wight | 6 | 4d8+5 | 8 | 1 | 1d5 | level drain 1 | - | 220 | 20 |
| Mummy | 7 | 6d8+5 | 3 | 1 | 1d13 | fear, paralysis | - | 650 | 70 |
| Kobold | 1 | 1d4 | 7 | 1 | 2d2 | calls 25%, flees 20% | - | 230 | 20 |
| Dark Elf | 4 | 5d8 | 4 | 1 | 1d9 | calls 25%, flees 10% | Mage 3 | 410 | 40 |
| Nagpa | 9 | 9d8 | 3 | 1 | 1d9 | - | Mage 5 | 950 | 90 |
| Mind Flayer | 9 | 10d8+5 | 5 | 4 | 1d5 | paralysis | Mage 5 | 960 | 90 |
| Lizard Man | 3 | 3d8+5 | 5 | 3 | 1d5 | flees 5% | - | 350 | 40 |
| Yuan-ti | 6 | 10d8 | 0 | 2 | 2d8+1 | - | - | 600 | 60 |
| Lizard King | 8 | 8d8+7 | 3 | 1 | 3d6+5 | - | - | 790 | 80 |
| Goblin King | 3 | 5d8 | 4 | 2 | 2d7 | calls 25%, flees 10% | - | 330 | 40 |
| Orc | 1 | 1d7 | 8 | 1 | 2d3 | calls 25%, flees 10% | - | 210 | 20 |
| Troll | 7 | 8d8+6 | 4 | 2 | 2d5+4 | - | - | 720 | 70 |
| Nightmare | 6 | 10d8 | -4 | 3 | 3d7 | paralysis | - | 630 | 60 |
| Vampire | 10 | 10d8+5 | 1 | 1 | 2d7+4 | paralysis, level drain 1 | - | 1000 | 80 |

Full stats: [monsters_table.md](../monsters_table.md).

**Notes for play:** Medusas and Greater Medusas can turn a member to stone; Mummies, Mind Flayers and Nightmares
paralyze; Wights and the Vampire drain levels. The Mind Flayer swings four times a round. The cell guards use floor
10's set, whose Vampire (level 10) is the strongest monster on the floor. Greater Medusas and Dark Elves are ranged,
and the elementals and Lizard Kings have reach, so all of them can attack the back row
([combat.md](../combat.md#8-monster-reach-and-targets)).

## 4. Open questions

- The text of the two signs.
- Which item the key-hole at (14, 15) takes, and where the button panel leads.
- What Laila and Kojiro need, besides room in the roster, to join.

Tech: [dungeon.md §4 Floors](../../tech/dungeon.md#4-floors), [§3 Event catalogue](../../tech/dungeon.md#3-event-catalogue),
[§2 Square types](../../tech/dungeon.md#2-square-types), [§2.1 Secret and locked doors](../../tech/dungeon.md#21-secret-and-locked-doors-wall-value-3);
`python3 tools/designtables/floormap.py 9 --list`.
