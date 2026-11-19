# Might and Magic II: Gates to Another World (DOS) - world

## Overview
Cron is 60 areas of 16 by 16 squares **(verified)**. The outdoors is a grid of five columns (A-E, west to east)
and four rows (1-4, north to south) that wraps around: walking off the east edge of E1 leads into A1, off the
south edge of A4 into A1 **(verified: each area's neighbours)**. The five towns, the caverns, castles and
dungeons are entered from squares of the outdoor areas or of each other; the four elemental planes lie beyond
the four corners **(source: area texts)**. Coordinates in this game count x from the west and y from the south,
(0,0) in the south-west corner **(verified)**. The world also changes with time: the game starts in year 900,
and some places exist only in earlier centuries **(verified: Castle Xabran in C2 stands in year 800, ruins in
900)**.

## 1. The outdoor grid
| | A | B | C | D | E |
|---|---|---|---|---|---|
| 1 | Tundara (tundra) | Ice Cavern (source) | Woodhaven area (source) | Dead Zone, Dragon's Dominion (source) | Vulcania, Gemmaker Volcano |
| 2 | Pinehurst, Sarakin's Mine (source) | Falcon Forest (area text) | **Middlegate**, Corak's Cave, Square Lake | Luxus Palace Royale, Mount Farview (source) | desert oasis |
| 3 | sirens' coast (area text) | Dark Keep, Jouster's Way (area text, source) | Druid's Point, Forbidden Forest (source) | - | Nomadic Rift (source) |
| 4 | Atlantium | Tower of Mercy, Murray's Cavern (source) | Quagmire of Doom: King Kalohn and the Mega Dragon in the 9th century (area text) | Castle Hillstone, Dawn's Mist (source) | Sandsobar |
Tundara, Vulcania, Atlantium and Sandsobar are the four corners; the elemental planes of Air, Fire, Water and
Earth border them (area texts mention the planes in A1, E1, A4 and E4) **(source: area texts; cluebook)**.

## 2. Area kinds
| Kind | Count | Notes |
|---|---|---|
| Towns | 5 | Middlegate, Atlantium, Tundara, Vulcania, Sandsobar; each has an inn (saving), shops and services; three have arenas (Arena, Monster Bowl, Colosseum) **(verified for Middlegate; source for the rest)** |
| Outdoor areas | 20 | terrain by region: tundra, forest, mountains, desert, water; signposts, fountains, ferries **(verified in C2, A1, E1, E2)** |
| Caverns | 16 | dark: light needed **(verified for the cavern under Middlegate)**; one under each town, eleven more (Corak's Cave, Square Lake, Ice Cavern, Sarakin's Mine, Murray's Cavern, Druid's Point, Forbidden Forest, Dragon's Dominion, Dawn's Mist, Gemmaker Volcano, Nomadic Rift) **(source)** |
| Castles | 5 | Hillstone (Lord Slayer), Woodhaven (Lord Hoardall), Pinehurst (Lord Peabody), Luxus Palace Royale (Queen Lamanda), Castle Xabran (9th century) **(source; texts)** |
| Dungeons and towers | 10 | two levels under each of the four lords' castles, Dark Keep (Ybmug), Tower of Mercy (Yekop) **(source)** |
| Elemental planes | 4 | Air (Lord Shalwend), Fire (Lord Pyrannaste), Earth (Lord Gralkor), Water (Lord Acwalandar), each with a shrine that a Disc opens **(source: area texts)** |

## 3. Middlegate
The starting town: inn (7,3), blacksmith (4,4), tavern (4,6), temple (7,7), training (10,7), mage guild (1,12)
and spell sages (7,14), locksmith (1,8), portal to Sandsobar (0,5), travel agent (14,8), skill trainers
(Cartographer (0,15), Pathfinder (1,9), Mountaineering (3,12)), skill removal (12,10), arena (13,6), fountains,
four fixed fights, stairs down (8,0) and the city gates (5,15) to C2 **(verified: every square visited)**.

## 4. Caverns by id (verified 2026-11-19 by their exits and texts)
11 under Middlegate, 12 under Atlantium, 13 under Tundara, 14 under Vulcania, 15 under Sandsobar, 16 Corak's Cave,
17 under Square Lake (the final gate), 18 Ice Cavern, 19 Sarakin's Mine, 1A Murray's Cavern, 1B the Druids'
cavern, 1C the class-quest cavern (Paladins Only), 1D Dragon's Dominion, 1E Dawn's Mist, 1F Gemmaker Volcano,
20 Nomadic Rift **(verified)**. Shots: [content.md](content.md) section 2.

## Open questions
- The cells marked (source) in the grid are from the cluebook and area texts, not visited.
