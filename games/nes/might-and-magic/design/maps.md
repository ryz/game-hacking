# Might and Magic (NES) - maps

## Overview
Every area is a 16x16 grid of squares; the outdoors (VARN) is 20 such sectors in a 5x4 grid. Each square has
four sides (wall, door, opening or a terrain/ornament type) and a set of properties (blocked per side, an event,
darkness, anti-magic, no camping) **(ROM data; walls and doors checked against the view in Sorpigal, verified)**.
Renders of all 55 maps are in [maps/](maps/) (`NN_name.png`, NN = the game's area number in hex, e.g.
`0A_dusk_cavern.png`; before 2026-11-18 the file numbers were decimal) with the
outdoor sectors joined in [maps/varn_atlas.png](maps/varn_atlas.png); the raw grids are in
[maps/maps.txt](maps/maps.txt). Regenerate: `python3 games/nes/might-and-magic/tools/maps.py --text`.

## 1. How to read a render
Every render carries its legend under the grid.
- North is up; square (0,0) is the south-west corner, x grows east, y grows north **(verified: Up from (8,5)
  facing north goes to (8,6))**.
- Thick line: the side cannot be passed. Thin line with a small box: a door or opening that can be passed.
  Colour = side type: black wall, brown door, green type 3 (ornament in towns, castles and caves), purple =
  blocked with no wall graphic (invisible barrier) **(ROM data)**.
- Outdoors (VARN sectors) the side types are terrain, drawn in terrain colours: green forest, brown mountains,
  blue water (sand in the desert sectors D1, D2, E1, E2); a square enclosed by one terrain on all four sides is
  filled with it (see section 4) **(verified by walking, ROM data)**.
- Red square: an event square (sign, shop door, inn, stairs, trap, message, fight). Grey fill: darkness.
  Blue "a": anti-magic **(ROM data; flag names from Data Crystal)**.
- Blue ring with a number NN: the square where a party arrives when an exit coded in area NN leads here; the
  exit itself is next to it (section 5) **(ROM code)**.
- Sorpigal: the party starts at (8,5) facing north; the Inn of Sorpigal is entered by walking south through
  the door to (8,4) and on to the counter square (8,3) **(verified)**.

## 2. The 55 areas (number = in-game area id)
| Id | Area | Id | Area | Id | Area |
|---|---|---|---|---|---|
| 01 | Sorpigal | 0F-22 | VARN outdoor sectors A1..E4 (label "Barn : A1") | 2C-2D | Enchanted Forest 1-2 ("ENCHANT B1/B2") |
| 02 | Portsmith | 23 | Castle Doom ("DOOM") | 2E-2F | Wizard's lair ("QUIV B1/B2") |
| 03 | Algary | 24 | Castle White Wolf | 30-31 | Raven's Wood 1-2 |
| 04 | Dusk | 25 | Castle Alamar | 32-35 | City of Gold ("P-PEEK1..4") |
| 05 | Erliquin | 26 | Castle Blackridge North | 36 | Astral Plane |
| 06 | Sorpigal Cavern ("C-SORPIGAL") | 27 | Castle Blackridge South | 37 | Soul Maze |
| 07 | "N-BARIER" cave (Data Crystal: C2 cave) | 28 | Castle Dragadune | | |
| 08 | Portsmith Cavern | 29-2B | Dragadune dungeon B1-B3 | | |
| 09 | Erliquin Cavern | 0B | Korin Bluffs | | |
| 0A | Dusk Cavern ("CAVE DUSK") | 0C | Volcano | | |
| 0D | "HAWKSEYE" (Data Crystal: square puzzle cave) | 0E | White Wolf cave | | |
Labels in quotes are the names the game shows in the area box **(ROM data; 01, 06, 0B, 0F, 23, 30 verified by
warping)**. The outdoor label really reads "Barn" in this release **(verified, map 0F)**.

## 3. VARN layout
Sector letters A-E run west to east, numbers 1-4 north to south (A1 north-west, E4 south-east) **(verified by
walking across edges: B2 south edge -> B3 (2,15), B3 east edge -> C3 (0,9), C3 east edge -> D3 (0,1); the north
edge of A1 answers "Solid wall!")**. Walking off a sector edge moves the party to the facing square of the
neighbouring sector; there is no edge exit at the outer border **(verified)**.

## 4. Outdoor terrain
Outdoors the four side values of a square name the terrain beyond that side, and the "blocked" properties
decide whether the party may step there **(verified by stepping into each type in B3, D1 and A2 from
`@vets`; the messages are the game's)**:

| Side value | Terrain | Blocked side: message | Unblocked side |
|---|---|---|---|
| 0 | open ground (road, grass) | - | walk on |
| 1 | forest | "Too dense!" | walk through (A2, verified) |
| 2 | mountains | "Impassable!" | (not seen unblocked) |
| 3 | water, or desert in D1, D2, E1, E2 | water: "Cannot swim!" | desert: walk in, "It's hot... You're lost!!!" or "Too windy!" (D1, verified) |

The graphics of each terrain depend on the sector (A1 blue night forest, A2 red mountains, C4 yellow forest,
D1 grey mountains in orange desert) **(verified, tour screenshots `varn_*`)**. Large water bodies are event
squares (red) in the data **(ROM data; what the event does there is not checked)**.

## 5. Exits between areas
Each area has its own event script (entry E of PRG bank B, the pairs are a table indexed by area); a script
checks the square and facing, prints its message ("Stairs going down! Take them?") and on Yes writes the target
area and square, which the main loop loads **(ROM code, decoded 2026-11-18; Sorpigal stairs verified as an event
prompt, `@town` route)**. The warps written as plain values are listed below with the arrival square (the exit
is the event square next to the arrival square in the source area); the warp tokens put the party on the arrival
square. Exits computed at run time (Sorpigal's stairs, the leprechaun's town choice, most town gates) do not
appear here **(ROM code)**.

| From (id) | Leads to (id, arrival square x,y) | Warp tokens for the arrival (from any checkpoint) |
|---|---|---|
| Dusk (04) | Varn E1 (1F, 9,11); Dusk Cavern (0A, 14,0) | `poke:009D=1F,poke:009F=09,poke:00A0=0B,WARP_GO`<br>`poke:009D=0A,poke:009F=0E,poke:00A0=00,WARP_GO` |
| Erliquin (05) | Varn B1 (13, 13,1); Erliquin Cavern (09, 0,7) | `poke:009D=13,poke:009F=0D,poke:00A0=01,WARP_GO`<br>`poke:009D=09,poke:009F=00,poke:00A0=07,WARP_GO` |
| Sorpigal Cavern (06) | C2 Cave (07, 8,0) | `poke:009D=07,poke:009F=08,poke:00A0=00,WARP_GO` |
| C2 Cave (07) | Varn C2 (18, 15,11); Portsmith Cavern (08, 7,0) | `poke:009D=18,poke:009F=0F,poke:00A0=0B,WARP_GO`<br>`poke:009D=08,poke:009F=07,poke:00A0=00,WARP_GO` |
| Portsmith Cavern (08) | Portsmith (02, 0,15); Erliquin Cavern (09, 2,7) | `poke:009D=02,poke:009F=00,poke:00A0=0F,WARP_GO`<br>`poke:009D=09,poke:009F=02,poke:00A0=07,WARP_GO` |
| Erliquin Cavern (09) | Erliquin (05, 15,7); Varn B1 (13, 14,1) | `poke:009D=05,poke:009F=0F,poke:00A0=07,WARP_GO`<br>`poke:009D=13,poke:009F=0E,poke:00A0=01,WARP_GO` |
| Dusk Cavern (0A) | City of Gold F4 (35, 5,13) | `poke:009D=35,poke:009F=05,poke:00A0=0D,WARP_GO` |
| Korin Bluffs (0B) | Varn B3 (15, 0,7) | `poke:009D=15,poke:009F=00,poke:00A0=07,WARP_GO` |
| Volcano (0C) | Varn C4 (1A, 7,2); Sorpigal (01, 8,5) | `poke:009D=1A,poke:009F=07,poke:00A0=02,WARP_GO`<br>`poke:009D=01,poke:009F=08,poke:00A0=05,WARP_GO` |
| Square Puzzle Cave (0D) | Varn D3 (1D, 7,13) | `poke:009D=1D,poke:009F=07,poke:00A0=0D,WARP_GO` |
| White Wolf Cave (0E) | Varn B2 (14, 8,4) | `poke:009D=14,poke:009F=08,poke:00A0=04,WARP_GO` |
| Varn B1 (13) | Erliquin (05, 0,7); Castle Blackridge South (27, 0,7); Castle Blackridge North (26, 7,15); Wizard's Lair F1 (2E, 2,2); Erliquin Cavern (09, 15,7) | `poke:009D=05,poke:009F=00,poke:00A0=07,WARP_GO`<br>`poke:009D=27,poke:009F=00,poke:00A0=07,WARP_GO`<br>`poke:009D=26,poke:009F=07,poke:00A0=0F,WARP_GO`<br>`poke:009D=2E,poke:009F=02,poke:00A0=02,WARP_GO`<br>`poke:009D=09,poke:009F=0F,poke:00A0=07,WARP_GO` |
| Varn B2 (14) | White Wolf Cave (0E, 8,0); Raven's Wood F1 (30, 7,1) | `poke:009D=0E,poke:009F=08,poke:00A0=00,WARP_GO`<br>`poke:009D=30,poke:009F=07,poke:00A0=01,WARP_GO` |
| Varn B3 (15) | Portsmith (02, 1,15); Korin Bluffs (0B, 15,0); Castle White Wolf (24, 15,8); Sorpigal (01, 8,5); Enchanted Forest F1 (2C, 8,8) | `poke:009D=02,poke:009F=01,poke:00A0=0F,WARP_GO`<br>`poke:009D=0B,poke:009F=0F,poke:00A0=00,WARP_GO`<br>`poke:009D=24,poke:009F=0F,poke:00A0=08,WARP_GO`<br>`poke:009D=01,poke:009F=08,poke:00A0=05,WARP_GO`<br>`poke:009D=2C,poke:009F=08,poke:00A0=08,WARP_GO` |
| Varn C4 (1A) | City of Gold F4 (35, 12,4); Volcano (0C, 7,5) | `poke:009D=35,poke:009F=0C,poke:00A0=04,WARP_GO`<br>`poke:009D=0C,poke:009F=07,poke:00A0=05,WARP_GO` |
| Castle Alamar (25) | Varn E3 (21, 14,7); Varn E3 (21, 15,7); Soul Maze (37, 6,0); Varn E3 (21, 4,7) | `poke:009D=21,poke:009F=0E,poke:00A0=07,WARP_GO`<br>`poke:009D=21,poke:009F=0F,poke:00A0=07,WARP_GO`<br>`poke:009D=37,poke:009F=06,poke:00A0=00,WARP_GO`<br>`poke:009D=21,poke:009F=04,poke:00A0=07,WARP_GO` |
| Castle Blackridge North (26) | Varn B1 (13, 14,10); Varn B1 (13, 14,9) | `poke:009D=13,poke:009F=0E,poke:00A0=0A,WARP_GO`<br>`poke:009D=13,poke:009F=0E,poke:00A0=09,WARP_GO` |
| Castle Blackridge South (27) | Varn B1 (13, 11,2); Varn B1 (13, 12,2); Dragadune Dungeon 3 (2B, 7,4) | `poke:009D=13,poke:009F=0B,poke:00A0=02,WARP_GO`<br>`poke:009D=13,poke:009F=0C,poke:00A0=02,WARP_GO`<br>`poke:009D=2B,poke:009F=07,poke:00A0=04,WARP_GO` |
| Castle Dragadune (28) | Varn E1 (1F, 12,12) | `poke:009D=1F,poke:009F=0C,poke:00A0=0C,WARP_GO` |
| Dragadune Dungeon 1 (29) | Dusk Cavern (0A, 15,12) | `poke:009D=0A,poke:009F=0F,poke:00A0=0C,WARP_GO` |
| Soul Maze (37) | Sorpigal (01, 8,5) | `poke:009D=01,poke:009F=08,poke:00A0=05,WARP_GO` |

Korin Bluffs portal list: Castle Doom (23, 7,3), Castle Dragadune (28, 7,14), Castle Alamar (25, 3,7), Castle Blackridge South (27, 3,7), Castle Blackridge North (26, 7,12), Castle White Wolf (24, 13,8), Sorpigal Cavern (06, 1,13), C2 Cave (07, 7,3), Portsmith Cavern (08, 9,0), Erliquin Cavern (09, 13,7), Sorpigal (01, 12,2), Portsmith (02, 1,14), Algary (03, 8,13), Dusk (04, 12,7), Erliquin (05, 4,7)


Shops and services use the same mechanism with codes from $80 up instead of an area: 80 inn, 81 blacksmith,
82 market (food), 83 tavern, 84 temple ("House"), 85 training, 8C guild **(RAM, verified in Sorpigal)**.

### Sorpigal (verified by stepping into every event square from each open side)
| Square (x,y), facing | What |
|---|---|
| (8,3) S from (8,4) | Inn of Sorpigal: "Would you like to sign in?" |
| (6,5) W from (7,5) | B and B Blacksmiths: "A man speaks: Can I help you?" |
| (A,5) E from (9,5) | Eulard's Fine Foods (market): "Would you like to buy some Food?" |
| (4,1) N from (4,0) | Temple: "Do you seek our help?" |
| (D,B) N from (D,A) | sign "OTTO'S TRAINING"; pressing Up once more there: "Do you require training?" |
| (2,D) E from (1,D) | Guild master: "Need help?" (Change class, Rename) |
| (B,E) E from (A,E) | Tavern: "Step up to the counter?" (Drink, Tip, Rumors) |
| (B,3) W from (C,3) | Leprechaun: "Only 1 Gem you lose... I'll send you to the town you choose." |
| (E,0) W from (F,0) | "Stairs going down! Take them?" (to the cavern) |
| (C,0) S from (C,1) | Gate keeper: "You are too weak to use City gate!" |
| (0,2) (2,2) (0,4) (2,4) (0,6) (3,6) | stone reliefs: "On this stone relief, a plaque reads:" |
| (2,0) (3,9) | sign "Sorpigal Gallery" |
| (5,8) | "Pit!!" |
| most other red squares | a fight (the same group whenever the square is entered at the same moment) |

### Story squares (verified by warping onto or stepping into them; facing as $A2: 0 N, 1 E, 2 S, 3 W)
| Area | Square, facing | What |
|---|---|---|
| 25 Castle Alamar | warp to (C,7) facing south, press Up | throne: "The omnipotent King Alamar speaks"; with the Eye of Goros: into the Soul Maze |
| 25 Castle Alamar | several squares (event scan) | "Boom! A fiery explosion." and "Singe! Acid trap." traps, "A loud scream from behind the door!", King's guards ("No King's Pass, no admittance!"), "THRONE ROOM" sign, "A passage leads outside", many fights |
| 37 Soul Maze | (0,0) | sign "Soul Maze 0:0"; (6,0): the alien and the "Answer!" keyboard (SHELTEM) |
| 36 Astral Plane | (4,6) (4,A) (7,E) (A,A) (A,6) | the five gates: "You've opened the First (Second, Third, Fourth, Fifth) gate!" |
| 36 Astral Plane | (7,8) facing 2 | "You are not yet worthy for transfer" / after the Soul Maze "My dream leads me, your dream leads you." |
| 36 Astral Plane | (7,A) | "There's a small slot in the door." |
| 36 Astral Plane | (6,7) facing 3 | the Inner Sanctum ending |

## Open questions
- Exits computed at run time (stairs, gates, the leprechaun) and the source square of each coded exit are not
  tabled; the arrival squares are.
- What the outdoor water event squares do.
- Map header fields after the label (encounters, music, palettes).
