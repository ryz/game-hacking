# Might and Magic (NES) - maps

## Overview
Every area is a 16x16 grid of squares; the outdoors (VARN) is 20 such sectors in a 5x4 grid. Each square has
four sides (wall, door, opening or a terrain/ornament type) and a set of properties (blocked per side, an event,
darkness, anti-magic, no camping) **(ROM data; walls and doors checked against the view in Sorpigal, verified)**.
Renders of all 55 maps are in [maps/](maps/) (`NN_name.png`, NN = the game's area number in hex) with the
outdoor sectors joined in [maps/varn_atlas.png](maps/varn_atlas.png); the raw grids are in
[maps/maps.txt](maps/maps.txt). Regenerate: `python3 games/might-and-magic/tools/maps.py --text`.

## 1. How to read a render
- North is up; square (0,0) is the south-west corner, x grows east, y grows north **(verified: Up from (8,5)
  facing north goes to (8,6))**.
- Thick line: the side cannot be passed. Thin line with a small box: a door or opening that can be passed.
  Colour = side type: black wall, brown door, green type 3 (town ornament; outdoors trees/terrain, open
  question), purple = blocked with no wall graphic (invisible barrier) **(ROM data)**.
- Red square: an event square (sign, shop door, inn, stairs, trap, message, fight). Grey fill: darkness.
  Blue "a": anti-magic **(ROM data; flag names from Data Crystal)**.
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
Sector letters A-E run west to east, numbers 1-4 north to south (A1 north-west, E4 south-east) **(computed: the
shared edges of neighbouring sectors agree for 86-90% of squares this way, about 25% the other way; not yet
walked across)**.

## Open questions
- Terrain types outdoors (wall type 3 and the blocked flags there).
- Exits between areas are coded per event square (no table): which door/stairs leads where.
