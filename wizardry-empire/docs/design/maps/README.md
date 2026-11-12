# Maps: how to read the floor maps, and the floor index

One page per maze floor, each with a map drawn from the game's own floor data. This page holds what is the same
for every floor; the floor pages only list what is particular to their floor. What each kind of square does (stairs,
traps, hidden spots, guarded squares, events, chests) is explained once in [dungeon.md](../dungeon.md); monsters and
encounter rules in [monsters.md](../monsters.md). Notation: [README.md](../README.md#notation-and-style-binding-for-every-design-document).

## 1. The floors

- **30 floors** (B1F to B30F), each **16 × 16 squares**. A floor **wraps at its edges**: walking off the east edge
  brings the party onto the west edge, and the same north-south.
- **Coordinates** are (x, y): x counts east from 0 to 15, y counts north from 0 to 15, so (0, 0) is the bottom-left
  square of the map and (15, 15) the top-right. These are the numbers the Compass spell reports in play.
- **Floors connect** by stairs at the same (x, y) on the floor above or below, and by chutes and other means
  ([dungeon.md](../dungeon.md)).
- **Found secret doors and picked locks stay open** for good (inferred; [dungeon.md](../dungeon.md#36-secret-and-locked-doors)).
- **Guarded squares and one-shot events come back** every time the party changes floor
  ([findings.md](../findings.md#29-guards-and-one-shot-events-re-arm-on-every-floor-change)).

## 2. Reading a map

The legend is printed under every map; the full rules for how maps look are in the
[style guide](style-guide.md). In short:

| On the map | Meaning |
|---|---|
| black line | wall ("Ouch!" when walked into) |
| black line with a brown bar | door. Walking through a door raises the chance of a random fight until the next plain step ([monsters.md](../monsters.md)) |
| door with a black arrow | one-way door: passable only in the arrow's direction; from the other side it is a wall ("Ouch!") |
| dashed red line | secret door: a wall ("Ouch!") until found with **Search** from the hidden spot beside it ([dungeon.md](../dungeon.md#36-secret-and-locked-doors)) |
| red bar | locked door: "It is locked." until opened with **Pick a lock** (a Thief's job) |
| dark grey square | solid rock (deadly if a teleport lands the party there) |
| **UP** / **DN** | stairs up / down |
| **G** | guarded square: a fixed fight, then a chest |
| **H** | hidden spot: faces a secret door (members with a good eye may notice it; Search finds it anyway) |
| **E** / **E1** | event / one-shot event |
| **T** + letter | floor trap: TP pit, TC chute, TF falling ceiling, TR rockfall, TV viper, TS spinner |
| **B** | button panel; **C** corpse |
| small grey dot | marker square: remembers visited squares, probably for the auto-map (inferred); no effect on play |
| red hatch / blue dots / purple both | damage zone / anti-magic zone (inferred) / both marks (no known effect) |
| small grey number | the square's encounter area (only where it differs from the area named under the title) |
| light grey square | no random fights on that square |

Encounter areas are set **per square**, not per room: on floor 1 the three areas alternate square by square, so
every corridor mixes all three monster sets. A fight picks one of the area's four formations at random, and the
group sizes are rolled for each fight ([monsters.md](../monsters.md)).

## 3. What each floor page contains

1. **Overview:** size of the open area, entrance and exits, counts of guarded squares, events, traps and hidden
   spots, the monster level range.
2. **Squares:** every square that is not plain floor, with what it does on this floor.
3. **Monsters:** the floor's encounter areas with their formations, and the stats of every monster in them.
4. **Open questions** particular to the floor.

The maps are generated: `python3 tools/designtables/floormap.py N` writes `wizardry-empire-floor-NN.png` (add `--list` for every
special square). The walls of floor 1 were checked against the game at the entrance (verified).

## 4. Floor index

All 30 maps and floor pages are written. The one-table overview of all floors is in [dungeon.md](../dungeon.md)
(floor by floor).

| Floor | Map | Page |
|---|---|---|
| 1 | [map](wizardry-empire-floor-01.png) | [floor-01.md](floor-01.md) |
| 2 | [map](wizardry-empire-floor-02.png) | [floor-02.md](floor-02.md) |
| 3 | [map](wizardry-empire-floor-03.png) | [floor-03.md](floor-03.md) |
| 4 | [map](wizardry-empire-floor-04.png) | [floor-04.md](floor-04.md) |
| 5 | [map](wizardry-empire-floor-05.png) | [floor-05.md](floor-05.md) |
| 6 | [map](wizardry-empire-floor-06.png) | [floor-06.md](floor-06.md) |
| 7 | [map](wizardry-empire-floor-07.png) | [floor-07.md](floor-07.md) |
| 8 | [map](wizardry-empire-floor-08.png) | [floor-08.md](floor-08.md) |
| 9 | [map](wizardry-empire-floor-09.png) | [floor-09.md](floor-09.md) |
| 10 | [map](wizardry-empire-floor-10.png) | [floor-10.md](floor-10.md) |
| 11 | [map](wizardry-empire-floor-11.png) | [floor-11.md](floor-11.md) |
| 12 | [map](wizardry-empire-floor-12.png) | [floor-12.md](floor-12.md) |
| 13 | [map](wizardry-empire-floor-13.png) | [floor-13.md](floor-13.md) |
| 14 | [map](wizardry-empire-floor-14.png) | [floor-14.md](floor-14.md) |
| 15 | [map](wizardry-empire-floor-15.png) | [floor-15.md](floor-15.md) |
| 16 | [map](wizardry-empire-floor-16.png) | [floor-16.md](floor-16.md) |
| 17 | [map](wizardry-empire-floor-17.png) | [floor-17.md](floor-17.md) |
| 18 | [map](wizardry-empire-floor-18.png) | [floor-18.md](floor-18.md) |
| 19 | [map](wizardry-empire-floor-19.png) | [floor-19.md](floor-19.md) |
| 20 | [map](wizardry-empire-floor-20.png) | [floor-20.md](floor-20.md) |
| 21 | [map](wizardry-empire-floor-21.png) | [floor-21.md](floor-21.md) |
| 22 | [map](wizardry-empire-floor-22.png) | [floor-22.md](floor-22.md) |
| 23 | [map](wizardry-empire-floor-23.png) | [floor-23.md](floor-23.md) |
| 24 | [map](wizardry-empire-floor-24.png) | [floor-24.md](floor-24.md) |
| 25 | [map](wizardry-empire-floor-25.png) | [floor-25.md](floor-25.md) |
| 26 | [map](wizardry-empire-floor-26.png) | [floor-26.md](floor-26.md) |
| 27 | [map](wizardry-empire-floor-27.png) | [floor-27.md](floor-27.md) |
| 28 | [map](wizardry-empire-floor-28.png) | [floor-28.md](floor-28.md) |
| 29 | [map](wizardry-empire-floor-29.png) | [floor-29.md](floor-29.md) |
| 30 | [map](wizardry-empire-floor-30.png) | [floor-30.md](floor-30.md) |

Tech: [dungeon.md §1 Map storage](../../tech/dungeon.md#1-map-storage-and-cell-format), [§4 Floors](../../tech/dungeon.md#4-floors);
generator `tools/designtables/floormap.py`.
