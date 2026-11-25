# Doom (DOS, registered 1.1) - content (variety lens)

What the game is filled with: its places, opponents, things and people, shown as a reasonable variety rather
than a full list. The rules behind the content are in [systems.md](systems.md), the screens it appears on in
[interface.md](interface.md); the same shots appear there, overlap is intended. Notation: [README.md](README.md).
Check: `python3 tools/lenses.py dos/doom`. Shot ids are from the `main` set unless marked `start`.

## 1. Kinds of content
| Kind | In the game (count if known) | Shown here | Full list |
|---|---|---|---|
| Environments | 27 maps in 3 episodes: Phobos techbases, Deimos, Hell (verified, WAD) | 9 | `games/dos/doom/tools/wadmap.py list` |
| Opponents | 10 monster kinds (verified, mobjinfo table) | 10 | playbook RAM map |
| Items | health, armor, ammunition, power-ups, keys | 9 | |
| Equipment | 8 weapons | 8 | |
| Abilities / spells | none | | |
| Characters and people | the marine only | 1 | |

## 2. Environments
| Environment | Where | What sets it apart | Shots |
|---|---|---|---|
| Hangar techbase | E1M1 | grey tech walls, brown panels, nukage pool | `env_e1m1`, `view_reduced`, start `09_env_corridor` |
| Nukage outdoors | E1M1 | brown hills sky over the green nukage pool | `pickup_megaarmor`, start `16_blue_armor` |
| Computer and imp rooms | E1M1, E1M3 | dark rooms, red ceiling lights, computer walls | `mon_imp_fireball`, `face_100`, start `17_imp_fireball` |
| Phobos Anomaly | E1M8 | wood and stone hall before the barons' closets | `boss_barons`, `weapon_plasma` |
| Deimos base | E2M1, E2M2 | grey corridors, lit tech rooms | `env_e2m1`, `env_e2m2` |
| Tower of Babel | E2M8 | grey arena under a red sky | `boss_cyberdemon`, `boss_cyber_dies` |
| Hell Keep | E3M1 | flesh walls, red sky courtyards | `env_e3m1`, `weapon_rocket`, `weapon_bfg_blast` |
| Hell marble and lava | E3M3 | green marble corridors with skull lamps, a lava room | `weapon_chainsaw`, `weapon_pistol`, `mon_cacodemon` |
| Dis | E3M8 | green ground, red sky, the Spider's plain | `env_e3m8`, `boss_spider`, `boss_spider_dead` |

## 3. Opponents
| Opponent | Where met | Family / picture | What it does | Shots |
|---|---|---|---|---|
| Zombieman | E1M1 on | former human, rifle | hitscan shots | `mon_sguys`, start `11_zombie3`, `14_zigzag` |
| Shotgun guy | E1M3 on | former human, black armour | shotgun | `mon_sguys`, `weapon_shotgun`, `face_67`, `face_16` |
| Imp | E1M1 on | brown, spiked | throws fireballs | `mon_imp_fireball`, `weapon_rocket`, start `15_imp_ledge`, `18_imp_hit` |
| Demon | E1M2 on | pink, horned | charges and bites | `weapon_fist`, `weapon_chainsaw`, `weapon_pistol` |
| Spectre | E1M7 on | a demon drawn as a shimmer | same as the demon, hard to see | `mon_spectre` |
| Lost soul | E3M3 and others | flaming skull | flies at the marine | `mon_lostsoul`, `weapon_chaingun` |
| Cacodemon | E2 on | red floating ball, one eye | spits fireballs | `mon_cacodemon` |
| Baron of Hell (boss of E1) | E1M8 | horned, goat legs | green fireballs; 1000 health; two died to five BFG shots (RAM) | `boss_barons`, `boss_baron_fireball`, `weapon_plasma` |
| Cyberdemon (boss of E2) | E2M8 | huge, rocket arm | rockets; 4000 health (RAM); outlasted 296 cells, killed after an idkfa refill (RAM) | `boss_cyberdemon`, `boss_cyber_dies` |
| Spider Mastermind (boss of E3) | E3M8 | brain on mechanical legs | super chaingun; 3000 health (RAM) | `boss_spider`, `boss_spider_bfg`, `boss_spider_tracers`, `boss_spider_dead` |

## 4. Items and equipment
| Item | Type | Got from | What it does | Shots |
|---|---|---|---|---|
| Fist | weapon, slot 1 | start | melee; berserk boosts it | `weapon_fist`, `face_16` |
| Chainsaw | weapon, slot 1 | maps, idchoppers | continuous melee | `weapon_chainsaw` |
| Pistol | weapon, slot 2 | start | single bullets | `weapon_pistol`, start `11_zombie3` |
| Shotgun | weapon, slot 3 | E1M1 secret, maps | pellets | `weapon_shotgun`, `mon_lostsoul` |
| Chaingun | weapon, slot 4 | maps | rapid bullets | `weapon_chaingun` |
| Rocket launcher | weapon, slot 5 | maps | rockets with blast damage | `weapon_rocket`, `boss_cyberdemon` |
| Plasma rifle | weapon, slot 6 | maps | plasma bolts, 1 cell each | `weapon_plasma` |
| BFG9000 | weapon, slot 7 | E3M3 and later | green ball and tracers, 40 cells | `weapon_bfg_blast`, `boss_spider_bfg`, `boss_cyber_dies` |
| Green armor | armor | maps | 100% armor | `pickup_armor` |
| MegaArmor | armor | E1M1 nukage pool | 200% armor | `pickup_megaarmor`, start `16_blue_armor` |
| Invulnerability | power-up | maps | no damage, inverse grey | `power_invuln` |
| Berserk | power-up | maps | strong fist, red view | `power_berserk`, `weapon_fist` |
| Partial invisibility | power-up | maps | weapon drawn as fuzz | `power_invis` |
| Radiation suit | power-up | maps | no floor damage, green view | `power_radsuit` |
| Computer map | power-up | maps | whole map on the automap | `automap_full` |
| Light amplification | power-up | maps | full brightness | `power_liteamp` |
| Armor bonus | item | E1M1 exit room | +1% armor | start `19_exit_room` |

## 5. Abilities and spells
None: the game has weapons and power-ups only.

## 6. Characters and people
| Who | Role | Where | Shots |
|---|---|---|---|
| The marine | the player, seen as the face and on the title picture | everywhere | `title_screen`, `face_100` |

## 7. Story
| Text | When | Shots |
|---|---|---|
| E1: "Once you beat the big badasses and clean out the moon base ..." ending on "play The Shores of Hell and its amazing sequel, Inferno!" | after E1M8 | `ending_e1`, `ending_e1_order` |
| E2: "You've done it! The hideous cyber-demon lord that ruled the lost Deimos moon base has been slain ..." | after E2M8 | `ending_e2`, `ending_e2_deimos` |
| E3: "The loathsome spiderdemon that masterminded the invasion of the moon bases ..." | after E3M8 | `ending_e3`, `ending_e3_bunny`, `ending_e3_scroll` |

## Open questions
- Keycards and skull keys on the maps, the secret ninth maps: not captured.
