# Deep Dungeon III - towns and dungeon floors

## Overview
The world is a set of square grids walked in first person: one grid that holds the towns (32 squares wide, 48 long,
several towns packed side by side) and four dungeons, each a stack of 32 by 32 floors: the underground (2 floors),
the cave (4), the tower (6) and the castle (4) **(ROM, area names inferred from the text stored with each dungeon)**.
Every square is either solid wall or open; doors, stairs and events sit on squares, not on the edges between them
**(verified: walking and bumping into walls matches the grids)**. The maps in [maps/](maps/) are drawn from the
game's own data by `../tools/maps.py`: dark blue wall, white floor, blue door, red shut door, green U/D stairs
(up/down), yellow numbered event squares, pink other specials. `maps/grids.md` has the same grids as text.
Coordinates are (x, y) with (0,0) the north-west corner; x grows east, y grows south **(verified)**.

## 1. Square types
| Code | Look | What happens | How sure |
|---|---|---|---|
| wall | solid | walking into it: "いたい! かべに ぶつかってしまった。" ("Ouch! You bumped into a wall.") | verified |
| floor | open | - | verified |
| door | door in the wall | A opens it / enters the building behind it | verified (inn door) |
| shut door | door | unknown (locked house? 16 in the towns) | open question |
| stairs down (D) | ladder down | "くだるかいだんが ある。つかいますか?" (There are stairs going down. Use them?) | verified |
| stairs up (U) | ladder up | "のぼるかいだんが ある。つかいますか?" (stairs going up) | verified |
| numbered squares | - | towns: buildings (5 = the inn of Dirige); dungeons: events (chests, messages, people, masters) | inn verified, rest inferred |
In the tower the "up" stairs lead to the next floor (floor 1's U squares match floor 2's D squares) **(computed)**;
in the underground and cave the "down" stairs do **(computed)**. Stairs keep the position: a staircase is on the same
square on both floors **(computed)**.

## 2. Town stairs
Eight stair squares in the town grid lead to the first floor of the underground or the cave **(ROM)**:
| Town square | Leads to |
|---|---|
| (1,25) | underground floor 1 (1,1) (verified) |
| (16,46) | underground floor 1 (30,30) |
| (29,17) | cave floor 1 (3,27) |
| (30,1) | cave floor 1 (1,1) (verified) |
| (30,6) | cave floor 1 (1,6) |
| (6,23) | underground floor 1 (21,1) |
| (4,23) | underground floor 1 (13,1) |
| (8,18) | cave floor 1 (30,16) |
The tower and the castle have no stairs from a town; their entrances are reached another way (ROM text "とうの
いりぐち まちにでますか?", "Tower entrance: go out to the town?") **(ROM, open question how)**.

## 3. Stairs per floor (computed from the grids)
| Dungeon | Floor | Up | Down |
|---|---|---|---|
| underground | 1 | (1,1) (13,1) (21,1) (30,30) to town | (30,1) (1,30) (20,30) |
| underground | 2 | (30,1) (1,30) (20,30) | - |
| cave | 1 | (1,1) (1,6) (30,16) (3,27) to town | (30,1) (25,3) (6,17) |
| cave | 2 | (30,1) (25,3) (6,17) | (4,3) (29,3) |
| cave | 3 | (4,3) (29,3) | (30,4) (18,7) (18,24) (5,30) |
| cave | 4 | (1,2) (30,4) (9,5) (14,29) | - |
| tower | 1 | (27,8) (16,15) | - |
| tower | 2 | (15,14) (4,23) | (27,8) (16,15) |
| tower | 3 | (17,2) (2,14) (16,17) (29,17) (14,29) | (15,14) (4,23) |
| tower | 4 | (17,5) (5,14) (15,14) (26,17) (14,26) | (17,2) (2,14) (16,17) (29,17) (14,29) |
| tower | 5 | (16,2) (2,15) (21,16) (29,16) (15,29) | (17,5) (5,14) (15,14) (26,17) (14,26) |
| tower | 6 | - | (16,2) (2,15) (21,16) (29,16) (15,29) |
| castle | 1 | (4,3) (27,3) (27,16) (4,28) (27,28) | - |
| castle | 2 | (21,16) | (4,3) (27,3) (27,16) (4,28) (27,28) |
| castle | 3 | - | (21,16) |
| castle | 4 | - | - (reached by an event) |

## 4. Maps
| File | What |
|---|---|
| [maps/towns.png](maps/towns.png) | the town grid (Dirige is the south-west part; the inn at (13,39)) |
| [maps/area1_f1.png](maps/area1_f1.png), [f2](maps/area1_f2.png) | the underground |
| [maps/area2_f1.png](maps/area2_f1.png) .. [f4](maps/area2_f4.png) | the cave |
| [maps/area3_f1.png](maps/area3_f1.png) .. [f6](maps/area3_f6.png) | the tower |
| [maps/area4_f1.png](maps/area4_f1.png) .. [f4](maps/area4_f4.png) | the castle (floor 4: twelve rooms of statues) |

## 5. Data format (for tools; addresses are in ../playbook.md)
One byte per square, rows of 32, stored uncompressed. Wall = $80 (any value with the top bit set and the door
bit clear counts as solid), floor $00, door $C0, shut door $C8, stairs up $40, stairs down $41, events $01-$1B,
$81, $C1-$CF, town $C7 (one square). Dungeon floor F of dungeon A lives in the PRG bank listed by `tools/maps.py`
(underground 1, cave 2-3, tower 4-6, castle 7-8; odd floors at $9800, even at $9C00); the town grid in bank 9 at
$9700. The game copies the current grid to battery RAM.

## Open questions
- Which event number is what (chests, messages, companions, masters); the shut doors; the $C7 town square.
- How the tower and castle are entered; what the pink special squares do.
- Which part of the town grid is which town (Dirige, Ail, ...).
