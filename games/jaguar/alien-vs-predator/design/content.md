# Alien vs Predator - content (variety lens)

What the game is filled with: places, opponents, things, shown as a reasonable variety. Rules in
[systems.md](systems.md), screens in [interface.md](interface.md). Notation: [README.md](README.md).
Check: `python3 tools/lenses.py jaguar/alien-vs-predator`. Shot ids in backticks are in `../shots/main/`
unless marked `start:`.

## 1. Kinds of content
| Kind | In the game (count if known) | Shown here | Full list |
|---|---|---|---|
| Playable species | 3 **(verified)** | 3 | section 2 |
| Environments | 15 areas: sublevels 1-5, 8 air ducts, Alien ship, Predator ship **(verified by warp)** | 9 looks | section 3 |
| Opponents | Aliens, facehuggers, Marines, Predator, Alien Queen **(source)** | Aliens | section 4 |
| Weapons | Marine 4, Predator 4 **(source; verified on screen)** | 8 | section 5 |
| Items | weapons, rounds, cards, motion tracker, medkits, food **(source)** | 3 | section 5 |
| Fixtures | doors, airlocks, lifts, vents, terminals, signs, cells, crates, barrels **(verified)** | 9 | section 3 |
| Texts | briefings, intro, terminal logs **(verified)** | 9 | section 6 |

## 2. Species
| Species | Start | Shots |
|---|---|---|
| Colonial Marine, Pvt. Lance J. Lewis | brig cell on sublevel 3, no weapon **(verified)** | `select_marine`, `brief_marine`, `marine_brig` |
| Alien | inside the Alien ship **(verified)** | `select_alien`, `brief_alien`, `alien_start`, `alien_sublevel1`, `alien_sublevel2`, `alien_predator_ship` |
| Predator | inside the Predator ship, wrist blade only **(verified)** | `select_predator`, `brief_predator`, `predator_start`, `predator_sublevel1`, `predator_alien_ship` |

## 3. Environments and fixtures
| Place / thing | Look | Shots |
|---|---|---|
| Sublevel 1 | dark storage hall full of barrels **(verified)** | `env_sublevel1` |
| Sublevel 2 | bright office corridors with doors, barrels, crates **(verified)** | `env_sublevel2` |
| Sublevel 3 | grey ribbed corridors of the brig block, cells with bars, a brig office with terminals **(verified)** | `env_sublevel3`, `env_sublevel3_office`, `start:10_long_corridor` |
| Sublevel 4 | rust-brown corridors with pipes **(verified)** | `env_sublevel4` |
| Sublevel 5 | halls with walls covered in dark Alien resin, crates **(verified)** | `entering_sublevel`, `marine_alien_sublevel5` |
| Air ducts | narrow square brown shafts **(verified)** | `vent_entered`, `airduct_alien` |
| Alien ship | dark ribbed organic walls, glowing slits by the door **(verified)** | `env_alien_ship`, `predator_alien_ship` |
| Predator ship | orange patterned walls and floor, plants **(verified)** | `env_predator_ship`, `alien_predator_ship` |
| Doors, airlocks | octagonal hatch door; double airlock doors with chevrons **(verified)** | `door_closed`, `airlock_door` |
| Lift | heavy hatch; cabin with red arrow panel **(verified)** | `lift_hatch`, `lift_inside`, `lift_arrived` |
| Vent | grille low in a wall **(verified)** | `vent` |
| Terminal | wall console with two green screens **(verified)** | `terminal` |
| Signs | BRIG, SUB LEVEL 3 (also CANTEEN, ELEVATOR, BARRACKS, PETTY OFFICERS AREA, AIRLOCK seen in previews) **(verified)** | `sign_brig`, `sign_sublevel` |

## 4. Opponents
| Opponent | Seen where | Behaviour | Shots |
|---|---|---|---|
| Alien (warrior) | sublevels 3, 4, 5, air ducts, outside a lift, Predator ship | runs in from a side, closes and strikes; dies in a yellow acid splash **(verified)** | `start:12_alien_enters`, `marine_alien_sublevel4`, `marine_alien_sublevel5`, `marine_alien_office`, `airduct_alien`, `lift_arrived`, `predator_combistick` |
| Dead Marines | brig corridor, brig office | lie on the floor, carry items **(verified)** | `marine_cell_open`, `marine_alien_office` |
| Facehuggers, Marines (as enemies), Predator (as enemy), Alien Queen | - | **(source)** | none: not met within budget |

## 5. Weapons and items
| Thing | Who | Shots |
|---|---|---|
| Shotgun | Marine, first weapon, from the body outside the cell **(verified)** | `pickup_shotgun`, `marine_shotgun` |
| Pulse rifle | Marine **(verified)** | `marine_pulse_rifle_hit`, `marine_pulse_rifle_kill`, `marine_alien_dead` |
| Flamethrower | Marine **(verified)** | `marine_flamethrower` |
| Smart gun | Marine **(verified)** | `marine_smartgun`, `marine_hurt` |
| Shotgun rounds | wall locker **(verified)** | `pickup_rounds` |
| Motion tracker | Marine **(verified)** | `marine_tracker` |
| Combistick | Predator **(verified)** | `predator_combistick` |
| Shoulder cannon | Predator **(verified)** | `predator_attained`, `predator_cannon`, `predator_cannon_kill` |
| Smart disc | Predator (icon) **(verified)** | `predator_smartdisc`, `predator_hurt` |
| Cloak and vision filters | Predator **(verified)** | `predator_cloak`, `predator_filter` |

## 6. Texts
| Text | Shots |
|---|---|
| Briefings of the three species | `brief_alien`, `brief_predator`, `brief_marine` |
| Attract intro: signal, docking, proximity alert | `intro_signal`, `intro_docked`, `intro_proximity` |
| General Log of a sublevel 3 terminal (3 pages: airducts, distress signals, armouries on levels 2 and 4) | `log_page1`, `log_page2`, `log_page3` |
| Credits: James Purple Hampton, Mike Beaton, Andrew Whittaker, Mike Pooler | `credits` |
| High score names (ANDY, PURPLE, JAMES among them) and the new RYZ | `highscores`, `highscore_ryz` |

## Open questions
- The other enemy kinds, the Queen and the ending screens were not reached.
