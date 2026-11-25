# Wolfenstein 3D (DOS) - content (variety lens)

What the game is filled with: its places, opponents, things and people, shown as a reasonable variety rather
than a full list. Read it to see the range of what a player meets. The rules behind the content are in
[systems.md](systems.md), the screens it appears on in [interface.md](interface.md); the same shots appear
there, overlap is intended. Notation: [README.md](README.md). Check: `python3 tools/lenses.py PLATFORM/SLUG`.

Which kinds exist depends on the game, its genre and structure: keep the kinds this game has, drop the rest,
add its own (vehicles, tracks, puzzles, levels, minigames ...). For each kind say how many there are in total
if known, then show a sample that spans the range: early and late, common and rare, plain and strange, one of
each visual family. A complete table belongs in its own document (items.md, enemies.md) and is linked here.

## 1. Kinds of content

| Kind | In the game (count if known) | Shown here | Full list |
|---|---|---|---|
| Environments | 60 floors in 6 episodes, a dozen wall families (verified: map data) | 10 looks from all six episodes | `wlmap.py list` |
| Opponents | 5 regular kinds, 6 bosses, Hitler's fake ghosts (verified: map data) | all 5 kinds, all 6 bosses | section 3 |
| Items | food, first aid, clips, keys (2), treasure (4 kinds), extra life (source) | clip, key, treasure, first aid | section 4 |
| Equipment | 4 weapons (verified) | all 4 | section 4 |
| Abilities / spells | none | | none: the game has no abilities |
| Characters and people | B.J. Blazkowicz, the bosses | B.J. on title, tally and end screens | section 5 |

## 2. Environments

| Environment | Where | What sets it apart | Shots |
|---|---|---|---|
| Blue stone cells | E1M1, E1M5 | dark blue stone, steel doors | `env_e1m5`, `12_corridor` |
| Grey stone halls | E1M1, E1M3 | grey stone, banners and pictures | `env_e1m3`, `13_hall_guard` |
| Wood panelling | E1M1, E6M6 | brown wood, eagle pictures, gold crosses | `16_wood_corridor`, `env_e6m6`, `treasure_room` |
| Yellow-veined stone | E2M1, demo floor | yellow and grey stone | `env_e2m1`, `demo` |
| Teal steel | E2M9, E1M9 | riveted teal walls of the boss floors | `boss_schabbs`, `enemy_mutant_fire` |
| Eagle banner halls | E3M1 | grey stone with eagle-and-swastika banners, plants | `env_e3m1` |
| Large grey blocks | E3M5, E1M2 | big rough blocks | `env_e3m5`, `door_gold` |
| Pillared brick | E4M1 | grey brick with white pillars | `env_e4m1` |
| Dark blue stone | E4M6 | dim blue rock | `env_e4m6` |
| Skull walls | E5M1 | blue stone with skulls | `env_e5m1`, `weapon_chain_gun` |
| Brown cave rock | E5M6, E6M9 | brown rock, bloodstains | `env_e5m6`, `boss_fett` |
| Elevator | every floor | grey steel room, switch panel | `elevator` |
| Outside | E1M9 exit | sky and grass beyond the gold door | `e1m9_exit` |

## 3. Opponents

| Opponent | Where met | Family / picture | What it does | Shots |
|---|---|---|---|---|
| Guard | E1M1 on | brown uniform, pistol | patrols, shoots, drops a clip; 100 points | `13_hall_guard`, `enemy_guard_fires`, `17_guard2_hit` |
| Dog | E1M1 on | German shepherd | runs at the player and bites | `enemy_dogs` |
| SS | E1M2 on | blue uniform, machine gun | bursts of fire | `enemy_ss`, `weapon_machine_gun` |
| Officer | E5M1 and others | white uniform | fast, quick to shoot; 400 points | `weapon_chain_gun`, `enemy_officer_dies` |
| Mutant | Episode 2 | green, a gun in the chest | silent, fires from the chest; 700 points | `enemy_mutant_fire`, `enemy_mutant_dies`, `weapon_knife` |
| Hans Grosse (boss) | E1M9 | blue giant with two chain guns | guards the gold key; 5000 points | `boss_hans`, `boss_hans_hit` |
| Dr. Schabbs (boss) | E2M9 | blood-spattered white coat | throws syringes, among mutants | `boss_schabbs`, `boss_schabbs_walks` |
| Hitler (boss) | E3M9 | mech suit with four chain guns | fires from the suit (fake ghosts not shown) | `boss_hitler` |
| Otto Giftmacher (boss) | E4M9 | white coat, rocket launcher | fires rockets | `boss_otto` |
| Gretel Grosse (boss) | E5M9 | red giant with two chain guns | Hans's sister | `boss_gretel` |
| General Fettgesicht (boss) | E6M9 | uniform, chain gun and rockets | with officers around him | `boss_fett` |

## 4. Items and equipment

| Item | Type | Got from | What it does | Shots |
|---|---|---|---|---|
| Knife | weapon | start | close stab, no ammunition | `weapon_knife` |
| Pistol | weapon | start | single shots | `weapon_pistol`, `14_guard_fire` |
| Machine gun | weapon | floors, SS | held fire | `23_machine_gun`, `weapon_machine_gun` |
| Chain gun | weapon | floors (MLI here) | fast held fire | `weapon_chain_gun`, `hud` |
| Ammo clip | ammunition | floors, dead guards | +4 when dropped by a guard (verified) | `20_clip` |
| First aid | health | floors | restores health, left at 100% | `22_secret_room` |
| Gold key | key | floors, bosses | opens gold doors | `key_gold`, `key_gold_taken` |
| Treasure (cross, chalice) | treasure | floors | points, treasure ratio | `treasure_room`, `treasure_pickup` |

## 5. Abilities and spells
None: the game has no abilities.

## 6. Characters and people

| Who | Role | Where | Shots |
|---|---|---|---|
| B.J. Blazkowicz | the player | title, status bar face, tally, end | `title_screen`, `tally_floor1`, `victory_run`, `episode_end_text` |
| id Software staff | credits and default high scores | attract loop | `credits_id`, `high_scores` |

## Open questions
- Silver key, chalice/chest/crown pickups, food, the extra-life sphere and Hitler's ghosts not shot.
- Secret floors (EnM10) not visited.
