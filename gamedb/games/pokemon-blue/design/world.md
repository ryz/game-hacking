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

| Pewter Gym | boulders, one trainer, Brock at the top | pewter_gym (verified) |
| Viridian Forest | tall grass mazes between trees, bug catchers | viridian_forest (verified) |
| Mt. Moon 1F | dark cave floor, rock ledges, signs, trainers | mt_moon (verified) |
| Vermilion City | Pokémon Center by the harbour water, gym behind a small tree | surfing, fishing, bicycle, cut_tree (verified) |
| Indigo Plateau (outside) | League building flanked by statues | indigo_plateau (verified) |
| Safari Zone | gate (fee desk), center area with grass and a rest house | safari_gate, safari_zone (verified) |
| Celadon Game Corner | rows of slot machines with stools, gamblers | game_corner (verified) |
| S.S. Anne 1F | gangway, deck corridor with portholes, sailors | ss_anne (verified) |
| Pokémon Tower 3F | gravestones, CHANNELER trainers | pokemon_tower (verified) |
| Silph Co. 3F | office floor, warp tiles, machines | silph_co (verified) |
| Champion's room / Hall of Fame | statues, the rival; record machine room | champion_room, hall_of_fame_room (verified) |

## 2. Encounters
- Wild battles happen while walking through grass; on Route 1 the per-step chance is 25/256 **(RAM)**.
  Single-tile taps did not trigger encounters in 18 steps while continuous walking did **(verified; see
  findings.md)**.

- Fishing: facing water, ITEM > SUPER ROD; either "Oh! It's a bite!" (battle) or "Not even a nibble!";
  which one depends on the frame the rod is used (4 of 6 timings bit at Vermilion) **(verified: fishing)**.
  Vermilion with the Super Rod gave a Krabby L15 **(verified)**.
- Safari Zone center: wild Nidorina L31 in its grass **(verified)**. Entry costs 500, gives 30 Safari Balls
  **(verified: money 48215 -> 47715, BALL x30)**; the game lasts 500 steps **(source)**.
- Bicycle: twice walking speed (a tile in 8 frames instead of 16) **(RAM/verified: bicycle route)**.
- Pokémon Tower 3F: wild encounters are unidentifiable GHOSTs without the SILPH SCOPE **(verified: tower_ghost)**.

## 3. Maps
- TOWN MAP item and the Pokédex AREA page share the same Kanto map **(verified: town_map, pokedex_area)**.

## Open questions
- ~~Caves, Surf, fishing, Safari~~ visited 2026-11-15. Safari step counter and Bait odds not measured.
