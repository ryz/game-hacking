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
| dashed red line | special wall: its effect was not traced. Hidden spots tend to sit on both sides of one, so it is probably a hidden door (inferred) |
| dark grey square | solid rock (deadly if a teleport lands the party there) |
| **UP** / **DN** | stairs up / down |
| **G** | guarded square: a fixed fight, then a chest |
| **H** | hidden spot (members with a good eye may notice something; Thieves are best at it) |
| **E** / **E1** | event / one-shot event |
| **T** + letter | floor trap: TP pit, TC chute, TF falling ceiling, TR rockfall, TV viper, TS spinner |
| **B** | button panel; **C** corpse |
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

The maps are generated: `python3 tools/designtables/floormap.py N` writes `floor-NN.png` (add `--list` for every
special square). The walls of floor 1 were checked against the game at the entrance (verified).

## 4. Floor index

| Floor | Page | Notes |
|---|---|---|
| 1 | [floor-01.md](floor-01.md) | entrance floor, levels 1-2 |
| 2-30 | not mapped yet | overview of every floor: [dungeon.md](../dungeon.md) (floor by floor) |

Tech: [dungeon.md §1 Map storage](../../tech/dungeon.md#1-map-storage-and-cell-format), [§4 Floors](../../tech/dungeon.md#4-floors);
generator `tools/designtables/floormap.py`.
