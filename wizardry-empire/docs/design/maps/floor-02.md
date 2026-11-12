# Floor 2: map, squares, monsters

The second floor of the maze (B2F), a narrow cave cut mostly out of solid rock; how to read the map, coordinates and
what each kind of square does: [maps/README.md](README.md).

![Floor 2 map](wizardry-empire-floor-02.png)

## 1. Overview

- 142 squares are solid rock; the other 114 are winding corridors and a few small rooms, joined by only 4 doors
  (computed from the map).
- **Stairs:** up at (15, 0), back to floor 1's down stairs; down at (0, 15), in the opposite corner, to floor 3.
- **Route:** the stairs down can only be reached through the special wall between (2, 10) and (2, 11), and Murphy
  only through the one between the hidden spots (6, 8) and (6, 9) (computed from the map, not tested). So special
  walls are probably passable (inferred).
- **3 guarded squares**, **1 event** (Murphy, a recruitable adventurer), **7 traps** (4 rockfall, 3 pits) and **one
  pair of hidden spots**.
- **Random fights** come from encounter area 4 on every open square except (2, 6), which has none.
- **Monsters:** levels 1-6, 1 to 3 groups of up to 6: Kobolds with Kobold Kings, Orcs with an Orc Lord, Goblins with
  a Goblin King, or a lone Minotaur.

## 2. Squares

| Square (x, y) | What | On this floor |
|---|---|---|
| (15, 0) | Stairs up | To floor 1 (its down stairs, same square). |
| (0, 15) | Stairs down | To floor 3. |
| (9, 10) | Murphy (event) | A recruitable adventurer: he offers to join ("Add Murphy?") if the roster has fewer than 20 characters and a condition of his own (not traced) is met ([dungeon.md](../dungeon.md#7-events)). |
| (7, 14), (0, 11), (8, 7), (14, 4) | Rockfall | Damage; amount not traced. |
| (12, 13), (3, 8), (2, 2) | Pit | |
| (6, 9) + (6, 8) | Hidden spots, a pair | They face each other across a special wall: probably a hidden door (inferred). |
| (5, 12), (10, 8), (6, 2) | Guarded square | Fight from area 4, then a chest. |

A second special wall, between (2, 10) and (2, 11), has no hidden spot next to it (from the map); the way to the
stairs down passes through it.

## 3. Monsters

| Area | Formations (one is picked per fight) |
|---|---|
| 4 | Minotaur ×1, or Kobold ×2-6 + Kobold King ×2 + Kobold ×1-6, or Orc ×2-5 + Orc Lord ×1-2, or Goblin ×2-5 + Goblin King ×1-2 |

| Monster | Lv | HP | AC | Swings | Damage | Special | EXP | Gold |
|---|---|---|---|---|---|---|---|---|
| Minotaur | 6 | 10d8 | 6 | 1 | 2d10+1 | reach | 680 | 70 |
| Kobold | 1 | 1d4 | 7 | 1 | 2d2 | calls 25%, flees 20% | 230 | 20 |
| Kobold King | 2 | 4d8 | 6 | 1 | 3d3 | calls 25%, flees 10% | 240 | 30 |
| Orc | 1 | 1d7 | 8 | 1 | 2d3 | calls 25%, flees 10% | 210 | 20 |
| Orc Lord | 3 | 3d4+14 | 4 | 3 | 2d8+2 | flees 10% | 320 | 30 |
| Goblin | 2 | 1d7 | 6 | 1 | 1d7 | calls 25%, flees 10% | 290 | 30 |
| Goblin King | 3 | 5d8 | 4 | 2 | 2d7 | calls 25%, flees 10% | 330 | 40 |

"Reach": attacks the back row from the front groups ([combat.md](../combat.md#8-monster-reach-and-targets)). Full
stats: [monsters_table.md](../monsters_table.md).

**Notes for play:** the Minotaur comes alone but is the big step up from floor 1: level 6, up to 80 HP, 2d10+1 per
hit. The Orc Lord swings three times a round. The Kobold formation brings up to 14 monsters in three groups
(computed: 6 + 2 + 6). The guards here still give Leather bags only
([dungeon.md](../dungeon.md#54-chest-quality-by-floor)). Seven trap squares sit on a floor of narrow corridors.

## 4. Open questions

- The damage of the rockfall and pit squares (each carries a trap strength of 2; what strength does for these traps
  was not traced).
- What a special wall does when the party walks into it (both the stairs down and Murphy lie behind one), how hard
  the hidden pair at (6, 9)/(6, 8) is to notice, and what noticing it opens.
- Murphy's own join condition.

Tech: [dungeon.md §4 Floors](../../tech/dungeon.md#4-floors), [§3 Event catalogue](../../tech/dungeon.md#3-event-catalogue);
`python3 tools/designtables/floormap.py 2 --list`.
