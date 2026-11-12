# Floor 16: map, squares, monsters

The sixteenth floor of the maze (B16F), home of the Queen of Darkness, whose stairs down sit behind two locked doors;
how to read the map, coordinates and what each kind of square does: [maps/README.md](README.md).

![Floor 16 map](wizardry-empire-floor-16.png)

## 1. Overview

- No solid rock: corridors and rooms joined by 16 doors, with no one-way doors, no secret doors and 8 locked doors
  (red bars), all of difficulty 85 (computed from the map). This floor has no hidden spots.
- **Stairs:** up at (15, 15), back to floor 15; down at (14, 1), to floor 17. The stairs down sit in a small room,
  (13, 1)-(14, 2), behind **two locked doors in a row**: from the stairs up the way passes the guarded square (7, 4),
  goes through the lock between (7, 2) and (7, 1) into the south corridor (7, 1)-(12, 1), then through the lock
  between (12, 1) and (13, 1) (computed from the map). A party coming up from floor 17 starts behind the same two
  locks.
- **Locks:** a Thief needs level 18 (a Ninja 23, a Kunoichi 28) for any real chance at a difficulty-85 lock: 10% + AGI
  at that level, 10% more per further Thief level (computed from [dungeon.md](../dungeon.md), secret and locked doors).
  From the stairs up, 214 squares can be reached with the locks shut and all 256 with them open (the key-hole room
  through a warp, below); from the stairs down, 4 with them shut (computed from the map).
- **7 guarded squares**, **2 events** (the Queen of Darkness, a key-hole door), **a button panel** and 2 warps (both to
  squares on this floor); no traps.
- **The key-hole room** (13, 9)-(14, 11), with the button panel, the key-hole and a warp, cannot be walked into, even
  with every lock open. The way in is the **warp at (14, 7)**, which lands on (13, 9); that warp stands in the room
  (13, 6)-(14, 7), behind the locked doors (7, 6) ↔ (7, 7) and (12, 7) ↔ (13, 7). The warp at (14, 11) in the
  key-hole room leads back to (14, 6), in the same room as (14, 7) (computed from the map). Once stepped on, the
  auto-map shows where each warp leads ([dungeon.md](../dungeon.md) §9).
- **Random fights** come from encounter area 18 on every square.
- **Monsters:** levels 3-18, up to 4 groups of 1 to 6 (computed from the formations): nagas and scorpions, undead
  with level drain, spellcasting beasts, the Juggernaut. Guard chests here are Silver at best
  ([dungeon.md](../dungeon.md), chest quality by floor).

## 2. Squares

| Square (x, y) | What | On this floor |
|---|---|---|
| (15, 15) | Stairs up | To floor 15. |
| (14, 1) | Stairs down | To floor 17. In the room (13, 1)-(14, 2), behind two locked doors (see the overview). |
| (14, 4) | Queen of Darkness (event) | An encounter with the Queen of Darkness; what follows was not traced ([dungeon.md](../dungeon.md)). |
| (14, 9) | Button panel | Buttons A-E: the Maze Elevator (inferred); where they lead was not traced. Inside the key-hole room, reached by the warp at (14, 7). |
| (14, 10) | Key-hole (event) | "Beside the door is a hole for slipping something in": a door that is inferred to need an item (not traced which). Inside the key-hole room. |
| (14, 7) | Warp | To (13, 9) on this floor: into the key-hole room, its only way in. In the room (13, 6)-(14, 7), behind two locked doors. |
| (14, 11) | Warp | To (14, 6) on this floor: the way out of the key-hole room, back into the room (13, 6)-(14, 7). |
| (7, 2) ↔ (7, 1) | Locked door | Difficulty 85. From the corridor of the guard (7, 4) into the south corridor (7, 1)-(12, 1): the first lock on the way down. |
| (12, 1) ↔ (13, 1) | Locked door | Difficulty 85. From the south corridor into the stairs-down room (13, 1)-(14, 2): the second lock on the way down. |
| (9, 1) ↔ (9, 2) | Locked door | Difficulty 85. From the south corridor into the room (9, 2)-(10, 3), which holds nothing marked on the map. |
| (11, 1) ↔ (11, 2) | Locked door | Difficulty 85. From the south corridor into the room (11, 2)-(12, 3), which holds nothing marked on the map. |
| (7, 6) ↔ (7, 7) | Locked door | Difficulty 85. From the corridor of the guard (7, 4) into the north corridor (7, 7)-(12, 7). |
| (12, 7) ↔ (13, 7) | Locked door | Difficulty 85. From the north corridor into the room (13, 6)-(14, 7), whose warp (14, 7) leads into the key-hole room. |
| (9, 7) ↔ (9, 6) | Locked door | Difficulty 85. From the north corridor into the room (9, 5)-(10, 6), which holds nothing marked on the map. |
| (11, 7) ↔ (11, 6) | Locked door | Difficulty 85. From the north corridor into the room (11, 5)-(12, 6), which holds nothing marked on the map. |
| (3, 14), (11, 11), (2, 8), (7, 4), (1, 3) | Guarded square | Fight from area 18, then a chest. Every way from the stairs up to the stairs down passes (7, 4) (computed from the map). |
| (12, 14) + (13, 13) | Guarded squares, a pair | Fight from area 18, then a chest. The two share one once-per-visit mark: after one has fought, the other probably stays quiet until the next floor change (inferred). |

## 3. Monsters

| Area | Where | Formations (one of 4 slots picked per fight) |
|---|---|---|
| 18 | Everywhere (256 squares) and the 7 guarded squares | Dark Naga ×4 + Man Scorpion ×1-2 + Lizard King ×0-1 + Spider Queen ×3, or Wight ×2 + Ghoul ×0-3 + Specter ×5-6 + DragonZombie ×2, or Couatl ×3 + Sleipnir ×3-4 + Kirin ×1 + Snow Lady ×1, or Juggernaut ×1 + Skel.Warrior ×2-3 + Dullahan ×2 + Night Rider ×2 |

| Monster | Lv | HP | AC | Swings | Damage | Special | Spells | EXP | Gold |
|---|---|---|---|---|---|---|---|---|---|
| Dark Naga | 8 | 9d8 | 4 | 1 | 4d9 | fear | - | 730 | 80 |
| Man Scorpion | 8 | 9d8 | 1 | 2 | 4d5+2 | poison | - | 870 | 90 |
| Lizard King | 8 | 8d8+7 | 3 | 1 | 3d6+5 | - | - | 790 | 80 |
| Spider Queen | 15 | 20d8 | -2 | 3 | 2d9 | poison, poison breath, calls 25% | Mage 5 | 8300 | 150 |
| Wight | 6 | 4d8+5 | 8 | 1 | 1d5 | level drain 1 | - | 220 | 20 |
| Ghoul | 3 | 2d8 | 6 | 3 | 1d4 | paralysis, flees 5% | - | 360 | 40 |
| Specter | 6 | 7d8+7 | 3 | 1 | 1d9 | level drain 1, calls 25% | - | 800 | 60 |
| DragonZombie | 18 | 25d8 | -2 | 3 | 4d9 | poison, poison breath | Mage 5 | 12000 | 170 |
| Couatl | 9 | 11d8 | 5 | 2 | 2d5 | poison | Mage 3, Priest 5 | 990 | 90 |
| Sleipnir | 9 | 10d8 | -5 | 5 | 3d7 | - | Priest 7 | 970 | 90 |
| Kirin | 12 | 15d8 | -5 | 3 | 3d7 | decapitation | Mage 7 | 4630 | 130 |
| Snow Lady | 13 | 16d8 | -3 | 2 | 3d5 | frost breath, flees 10% | Mage 6 | 5800 | 130 |
| Juggernaut | 17 | 40d8 | 0 | 1 | 11d11 | - | - | 9470 | 170 |
| Skel.Warrior | 4 | 7d8 | 4 | 2 | 2d9 | - | - | 370 | 40 |
| Dullahan | 11 | 14d8 | 0 | 2 | 4d9 | - | - | 3290 | 110 |
| Night Rider | 15 | 22d8 | -5 | 3 | 4d9 | paralysis | - | 7180 | 150 |

Full stats: [monsters_table.md](../monsters_table.md).

**Notes for play:** the Juggernaut has the most HP (40d8, up to 320) and the hardest hit (11d11, 11-121); the Dragon
Zombie is the highest level (18) and breathes poison. The undead formation brings two level drainers (Wight,
Specter); the beast formation casts high spells (Sleipnir Priest 7, Kirin Mage 7) and the Sleipnir swings 5 times
(all computed from the table).

## 4. Open questions

- Which item the key-hole at (14, 10) asks for, and where the buttons lead.
- What the Queen of Darkness event does (a fight, a talk, an item).
- The guarded squares (12, 14) and (13, 13) share one "already fought" mark; whether beating one also clears the
  other for that visit was not traced.
- The walls of this map were not checked in the game.

Tech: [dungeon.md §4 Floors](../../tech/dungeon.md#4-floors), [§3 Event catalogue](../../tech/dungeon.md#3-event-catalogue),
[§2 Square types](../../tech/dungeon.md#2-square-types), [§2.1 Secret and locked doors](../../tech/dungeon.md#21-secret-and-locked-doors-wall-value-3);
`python3 tools/designtables/floormap.py 16 --list`.
