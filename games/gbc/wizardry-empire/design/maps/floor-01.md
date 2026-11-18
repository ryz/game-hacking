# Floor 1: map, squares, monsters

The first floor of the maze (B1F), the one every new party starts on. How to read the map, coordinates and what
each kind of square does: [maps/README.md](README.md). The walls of this map were checked against the game at the
entrance (verified).

![Floor 1 map](wizardry-empire-floor-01.png)

## 1. Overview

- 37 squares are solid rock; the rest is corridors and rooms, joined by 18 doors and 3 one-way doors, plus 3 secret
  doors and 1 locked door (computed from the map).
- **Entrance and exit:** the stairs up at (0, 15) lead back to town; the party arrives there facing south (verified).
  The stairs down to floor 2 are in the opposite corner at (15, 0).
- **Route** (computed from the map): the stairs down lie behind the locked door (4, 7) ↔ (4, 8) and, beyond it, the
  secret door (4, 9) ↔ (4, 10). With every secret and locked door shut the party reaches 170 of the 219 open squares
  from the up stairs; with all of them open, every square. The fairy and the magic circle are each behind a secret
  door of their own.
- **8 guarded squares**, **3 events** (gold coins, a fairy, a magic circle), **2 pits** and **3 pairs of hidden
  spots**.
- **Random fights** come from three encounter areas (1, 2, 3) that alternate square by square; one square, the pit
  at (9, 13), has none.
- **Monsters:** levels 1-2, 1 to 7 per group: Kobolds, Goblins, Skeletons, Zombies, Orcs, a Banshee.

## 2. Squares

| Square (x, y) | What | On this floor |
|---|---|---|
| (0, 15) | Stairs up | To town. Start of every trip. |
| (15, 0) | Stairs down | To floor 2. Behind the locked door at (4, 7) ↔ (4, 8) and the secret door at (4, 9) ↔ (4, 10). |
| (5, 4) | Gold coins (one-shot event) | "Gold coins lie scattered. Pick them up?" They are either gold or they come alive (a fight). |
| (2, 12) | Fairy (event) | Flees, unless the party carries the Fairy's Heart; then she offers a trip to her twin on floor 11 for 1 G. Behind the secret door at (1, 9) ↔ (0, 9). |
| (15, 15) | Magic circle (event) | "A strange pattern..." With a Summoner in the party, a pact for the Zombie summon, from Summoner level 3 ([spells.md](../spells.md)). Behind the secret door at (11, 15). |
| (0, 2), (9, 13) | Pit | |
| (12, 15) → (13, 15), (14, 12) → (14, 11), (12, 15) → (11, 15) | One-way doors | Passable only in the direction given; the first two were tested in the game (verified). The third is the secret door at (11, 15) seen from inside: from (12, 15) it is always open. |
| (4, 7) ↔ (4, 8) | Locked door | "It is locked." (verified). Difficulty 5: a Thief has a real chance from level 2 (computed). Pick it from (4, 7) facing north. Behind it: a 6-square room, (3, 8) to (5, 9), with the hidden spot (4, 9); from there the secret door (4, 9) ↔ (4, 10) is the only way on to the stairs down (computed from the map). |
| (1, 9) + (0, 9) | Hidden spots, a pair | Each faces the secret door between them; Search here, facing the other spot, finds it (verified from (0, 9) facing east). Noticing difficulty 40. Behind it, seen from the up stairs: the fairy's corner, 6 squares from (0, 9) to (2, 12) (computed from the map). |
| (4, 9) + (4, 10) | Hidden spots, a pair | Each faces the secret door between them; Search here finds it (from (4, 9) facing north). Noticing difficulty 5. North of it: the stairs-down part, 28 squares (computed from the map). |
| (11, 15) | Hidden spot | Faces the secret door to (12, 15); Search here, facing east, finds it. Noticing difficulty 10. Behind it: the magic circle's corner, 9 squares from (12, 15) to (15, 15) and down to (14, 12) (computed from the map). |
| (12, 15) | Hidden spot | Inside the circle's corner. It belongs to the same door as (11, 15), but none of its own sides is a secret door: its west side is the one-way door back out (from the map). |
| (6, 15), (7, 1), (0, 5), (9, 9) | Guarded square | Fight from area 1, then a chest. |
| (5, 0), (13, 2), (11, 12) | Guarded square | Fight from area 2, then a chest. |
| (7, 1) + (5, 0) | Guarded squares sharing one mark | Both use the same once-per-visit mark: after one is fought, the other probably stays quiet until the next floor change (inferred). |
| (9, 4) | Guarded square | Fight from area 3, then a chest. |

**Secret and locked doors** (rules: [dungeon.md](../dungeon.md) §3.6): Search finds a secret door every time;
noticing a hidden spot first is only a hint, and the noticing difficulty is what a member's noticing skill must beat
for it (§3.3). A lock of difficulty D gives a Thief a real chance from level D/5 + 1: there 10% + AGI, then 10% more
per level, at most 95%; at level D/5 only about 1%. A Ninja needs 5 levels more, a Kunoichi 10 (computed from the
rule). Found and picked doors stay open for good (inferred).

## 3. Monsters

| Area | Where | Formations (one of 4 slots picked per fight) |
|---|---|---|
| 1 | 74 squares, mixed square by square with areas 2 and 3; 4 guarded squares | CrawlingClaw ×1-4, or Eye Wing ×1-4, or Gas Cloud ×1-4, or Banshee ×1 |
| 2 | 73 squares; 3 guarded squares | CreepingCoin ×1-2, or Skeleton ×1-4, or Orc ×1-2, or Zombie ×1-2 |
| 3 | 71 squares; 1 guarded square | Kobold King ×1-2, or Dryad ×1-2, or Kobold ×1-7, or Goblin ×1-4 |

| Monster | Lv | HP | AC | Swings | Damage | Special | Spells | EXP | Gold |
|---|---|---|---|---|---|---|---|---|---|
| CrawlingClaw | 1 | 1d6 | 8 | 1 | 1d4 | - | - | 30 | 20 |
| Eye Wing | 1 | 1d4 | 7 | 1 | 1d4 | flees 10% | - | 50 | 20 |
| Gas Cloud | 1 | 1d7 | 8 | 1 | 1d6 | - | - | 120 | 20 |
| Banshee | 1 | 3d3 | 8 | 1 | 1d4 | fear | - | 270 | 30 |
| CreepingCoin | 1 | 1 | 7 | 1 | 1d2 | lightning breath, calls 65% | - | 260 | 20 |
| Skeleton | 1 | 1d5 | 9 | 1 | 1d7 | - | - | 270 | 20 |
| Orc | 1 | 1d7 | 8 | 1 | 2d3 | calls 25%, flees 10% | - | 210 | 20 |
| Zombie | 1 | 2d5 | 8 | 1 | 1d8 | calls 25% | - | 230 | 30 |
| Kobold King | 2 | 4d8 | 6 | 1 | 3d3 | calls 25%, flees 10% | - | 240 | 30 |
| Dryad | 2 | 2d8 | 5 | 1 | 1d4 | flees 50% | Mage 4 | 250 | 30 |
| Kobold | 1 | 1d4 | 7 | 1 | 2d2 | calls 25%, flees 20% | - | 230 | 20 |
| Goblin | 2 | 1d7 | 6 | 1 | 1d7 | calls 25%, flees 10% | - | 290 | 30 |

Full stats: [monsters_table.md](../monsters_table.md).

**Notes for play:** the Creeping Coin's lightning breath and the Banshee's fear are the only special attacks on
the floor; the Dryad casts Mage spells up to level 4. The Kobold King and Dryad (level 2, up to 32 and 16 HP) are the
toughest regular monsters. The guarded squares re-arm on every floor change, so the down-and-up trip at (15, 0) is a
way to repeat their fights and chests. A new party needs a Thief to go deeper: the lock at (4, 7) ↔ (4, 8) gives a
level 1 Thief about 1% per try and a level 2 Thief 10% + AGI, while the other classes need level 32 (all computed
from the rule above).

## 4. Open questions

- How much gold the coins give, and the odds that they come alive instead.

Tech: [dungeon.md §4 Floors](../../tech/dungeon.md#4-floors), [§3 Event catalogue](../../tech/dungeon.md#3-event-catalogue),
[§2.1 Secret and locked doors](../../tech/dungeon.md#21-secret-and-locked-doors-wall-value-3);
`python3 tools/designtables/floormap.py 1 --list`.
