# World - Pokémon Blue Version

## Overview
A top-down tile world of towns, routes and buildings in the Kanto region **(verified: town_map)**. Movement is
one tile per step **(verified)**; tall grass on routes hides the lower half of the player's sprite and holds
wild Pokémon **(verified: route1_grass)**.

## 1. Areas seen
| Area | What is there | Shot |
|---|---|---|
| Red's house 2F | bedroom, SNES/TV, PC | start_room (verified) |
| Pallet Town | two houses, Oak's lab, signs, fence; Route 1 north, sea south | pallet_town (verified) |
| Oak's lab | three Poké Balls on a table, bookshelves, Oak | oak_lab_choose (verified) |
| Route 1 | tall grass strips, ledges, Pidgey | route1_grass, battle_wild (verified) |
| Indigo Plateau lobby | Pokémon Center nurse, Cable Club desk, Poké Mart clerk, door to the Elite Four | pokecenter_nurse, mart_buy, cable_club (verified) |
| Lorelei's room | ice floor, Lorelei by the next door | elite_four_room (verified) |

## 2. Encounters
- Wild battles happen while walking through grass; on Route 1 the per-step chance is 25/256 **(RAM)**.
  Single-tile taps did not trigger encounters in 18 steps while continuous walking did **(verified; see
  findings.md)**.

## 3. Maps
- TOWN MAP item and the Pokédex AREA page share the same Kanto map **(verified: town_map, pokedex_area)**.

## Open questions
- Caves, water routes (Surf, fishing) and the Safari Zone not visited this run.
