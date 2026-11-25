# Spear of Destiny (DOS) - content (variety lens)

A sample that spans what fills the game. Shots are ids of the set `main` unless numbered (set `start`).
Totals from the maps (`tools/sodmap.py list`, skill 2 where it matters). Notation: [README.md](README.md).

## Environments (21 floors; one shot per look)
| Floor | Name | Look | Shots |
|---|---|---|---|
| 1 | Tunnels 1 | yellow-veined stone with vines | `floor1_start`, `07_floor1_start` |
| 2 | Tunnels 2 | yellow-veined stone corridor, steel door | `env_f2` |
| 3 | Tunnels 3 | grey stone | `env_f3` |
| 4 | Tunnels 4 | orange rock, steel door | `env_f4` |
| 5 | Tunnel Boss | grey and brown rock (Trans Grosse) | `trans_grosse` |
| 7 | Dungeons 2 | blue stone, green lamps | `env_f7` |
| 8 | Dungeons 3 | blue stone hall | `env_f8` |
| 6 | Dungeons 1 | blue stone, cell doors, dark red ceiling | `enemy_officer`, `weapon_knife` |
| 10 | Dungeon Boss | blue stone (Barnacle Wilhelm) | `barnacle_wilhelm` |
| 11 | Castle 1 | white brick; the garage with the truck | `env_f11`, `truck` |
| 13 | Castle 3 | brown rock with columns, red banners | `env_f13`, `enemy_mutant` |
| 15 | Castle 5 | grey steel panels | `env_f15` |
| 16 | Castle Boss | teal steel (Ubermutant) | `ubermutant` |
| 17 | Ramparts | white stone open to the sky | `env_f17` |
| 18 | Death Knight | brown brick hall; blue skull walls around the Spear | `death_knight`, `spear_of_destiny` |
| 19 | Secret 1 | teal metal doors, red sky | `env_f19` |
| 20 | Secret 2 | grey cave rock | `env_f20` |
| 21 | Angel of Death | red rock; blue skull walls at the start | `env_f21`, `angel_of_death` |
Not shot: floors 9, 12, 14 (looks shared with their neighbours).

## Opponents
| Kind | Where first | Shots |
|---|---|---|
| Guard (brown) | floor 1 | `11_door_guard`, `14_guard_close`, `weapon_chain_gun` |
| Officer (white) | floor 6 | `enemy_officer`, `enemy_officer_hit`, `enemy_officer_dies`, `enemy_officer_dead` |
| Mutant (green) | floor 13 | `enemy_mutant`, `enemy_mutant_hit`, `enemy_mutant_dies`, `enemy_mutant_falls` |
| SS, dog | floors 1-6 | not shot close: seen only far away in previews (open) |
| Spectre (ghost) | floor 21 | `spectre` |
| Trans Grosse | floor 5 | `trans_grosse`, `trans_grosse_fight`, `trans_grosse_hit`, `trans_grosse_dies`, `trans_grosse_dead`, `face_8` |
| Barnacle Wilhelm | floor 10 | `barnacle_wilhelm`, `barnacle_fight` |
| Ubermutant | floor 16 | `ubermutant`, `ubermutant_fight`, `ubermutant_hit` |
| Death Knight | floor 18 | `death_knight`, `death_knight_fight`, `death_knight_rockets` |
| Angel of Death | floor 21 | `angel_of_death`, `angel_fireball`, `angel_fight`, `angel_hit`, `angel_dissolves`, `angel_remains` |

## Items and equipment
| Kind | Examples | Shots |
|---|---|---|
| Weapons | knife, pistol, machine gun, chain gun | `weapon_knife`, `weapon_pistol`, `weapon_machine_gun`, `weapon_chain_gun` |
| Ammunition | clips (secret room on floor 1) | `09_ammo_room`, `10_ammo_taken` |
| Treasure | crosses and chalices | `18_treasure_door`, `19_treasure_room` |
| Keys | gold and silver (status bar) | `hud` |
| The Spear | floor 18 | `spear_of_destiny`, `spear_taken` |
| Scenery | vines, barrels, truck, lamps, banners, columns | `truck`, `env_f13` |

## People and story
B.J. Blazkowicz (portraits on the tally, You Win! and the victory animation: `tally_floor1`, `bj_spear`,
`victory_win`); the end pages with an officer and the President (`end_debt`, `end_allies`), B.J. breaking a
wall (`end_another_story`) and the credits (`end_title`, `credits_id_game`, `credits_formgen`,
`credits_beta`, `end_thanks`, `end_the_end`); the end text (`end_text`).
