# Ultima I: The First Age of Darkness (DOS) - content (variety lens)

What the game is filled with: its places, opponents, things and people, shown as a reasonable variety rather
than a full list. Read it to see the range of what a player meets. The rules behind the content are in
[systems.md](systems.md), the screens it appears on in [interface.md](interface.md); the same shots appear
there, overlap is intended. Notation: [README.md](README.md). Check: `python3 tools/lenses.py dos/ultima`.
Shot ids are the playbook's planned ids.

## 1. Kinds of content
| Kind | In the game (count if known) | Shown here | Full list |
|---|---|---|---|
| Environments | overworld (4 continents), towns (32), castles (8), landmarks (8), dungeons (36), space (49 sectors), Mondain's chamber **(verified data)** | 8 | `../tools/worldmap.py --list` |
| Opponents | 13 overworld kinds, 22 dungeon kinds, guards, space enemies, Mondain **(ROM text)** | 8 | playbook Game structure |
| Items | 4 gems, food **(verified)** | 4 | |
| Equipment | 16 weapons, 6 armours **(ROM text)** | 6 | playbook RAM map |
| Abilities / spells | 11 spells **(ROM text)** | 3 | playbook RAM map |
| Vehicles | horse, cart, raft, frigate, aircar, shuttle, time machine **(verified)** | 5 | |
| Characters and people | 8 kings, 8 princesses (Julia, Cassandra, Marsha, Donna, Kristen, Beth, Lori, Dianne), shopkeepers, guards, jesters, Iolo the Bard, Gwino the jester, wenches, Mondain **(ROM text)** | 5 | |

## 2. Environments
| Environment | Where | What sets it apart | Shots |
|---|---|---|---|
| Grassland and woods | all continents | the default overworld, dotted grass, round woods **(verified)** | `start_overworld` |
| Sea and mountains | coasts, mountain ranges | blue waves, grey peaks; mountains block **(verified)** | `gameplay_continents` |
| Town (Britian) | (27,27) | grey brick walls, six shops with signs, pond **(verified)** | `gameplay_britian` |
| Castle (Lord British) | (28,26) | white walls, pools, armour/food/weaponry halls, king's throne room, prison **(verified)** | `gameplay_castle` |
| Landmark (Grave of the Lost Soul) | (62,58), an island | inscription box **(verified)** | `system_landmark_grave` |
| Dungeon | 36 entrances | white wireframe corridors, doors, chests **(verified)** | `gameplay_dungeon` |
| Space | 49 sectors | planet, sun, starbases; starfield front view; hyperspace streaks **(verified)** | `gameplay_space_top`, `gameplay_space_front`, `system_hyperjump` |
| Mondain's chamber | after the time machine | red cracked stone walls on black **(verified)** | `boss_mondain` |
| Ending | | white text on black **(verified)** | `ending_text` |

## 3. Opponents
| Opponent | Where met | Family / picture | What it does | Shots |
|---|---|---|---|---|
| Skeleton | dungeon level 1 | wireframe undead | 2-damage hits **(verified)** | `battle_skeleton` |
| Thief | overworld | human | attacks (21 damage seen), steals **(verified / ROM text)** | `battle_overworld` |
| Orc | overworld | green humanoid | attacks (3 damage seen) **(verified)** | `battle_overworld` |
| Evil trent | overworld | walking tree | 9 damage seen **(verified)** | |
| Knight | overworld | armoured | 5 damage seen **(verified)** | |
| Gelatinous cube, Carrion creeper, Lich, Balron | deep dungeons | quest monsters of the four gem kings **(code)** | | `battle_dungeon_*` |
| Enemy vessels | space | fighters **(ROM text)** | shoot back ("Alien fires!") | `battle_space` |
| Mondain | his chamber | white-robed wizard with a staff; bat form **(verified)** | magic missile, mind blaster, psionic shock **(verified)** | `boss_mondain`, `boss_mondain_bat` |

## 4. Items and equipment
| Item | Type | Got from | What it does | Shots |
|---|---|---|---|---|
| Dagger, Mace, Rope & Spikes | weapon | start, weapon shop (8, 19 pence) **(verified)** | melee | `shop_weapons` |
| Pistol, Blaster | weapon | late shops **(ROM text)** | late weapons | `inventory_ztats_late` |
| Leather armor, Chain mail, Plate mail | armour | armour shop (45, 90, 135) **(verified)** | defence | `shop_armour` |
| Vacuum suit, Reflect suit | armour | after 3,000 moves **(code)** | space-age armour | `inventory_ztats_late` |
| Red, green, blue, white gems | quest items | the four gem kings **(code)** | open the time machine **(verified)** | `cutscene_time_machine` |
| Horse, cart, raft, frigate, aircar, shuttle | vehicles | transport shop (36 to 1,296) **(verified)** | travel, guns, space | `shop_transport`, `gameplay_vehicles` |
| Time machine | vehicle | the princess's reward **(verified)** | to Mondain | `gameplay_time_machine` |

## 5. Abilities
| Spell | Got from | What it does | Shots |
|---|---|---|---|
| Prayer | always | "POTENTIS-LAUDIS!" (no effect outdoors) **(verified)** | |
| Open, Magic Missile, Ladder Down | Mad Chad's Magic Shoppe (5, 15, 25) **(verified)** | dungeon spells **(source)** | `shop_magic`, `system_spell_cast` |
| Kill | magic shops **(ROM text)** | "INTERFICIO-NUNC!" kills a monster; makes Mondain stronger **(ROM text)** | |

## 6. People
| Person | Where | Role | Shots |
|---|---|---|---|
| Lord British | his castle | quest giver (landmark), sells hit points **(verified)** | `dialogue_king_quest` |
| Princess Julia | Lord British's prison | rescue reward, time machine **(verified)** | `system_princess_reward` |
| Shopkeepers | towns | e.g. Lord Eldric D'Charbonneux, Mad Chad, Li'l Karelia **(verified)** | `shop_*` |
| Jester | castles | carries the prison key **(code)** | `system_jester_key` |
| Tavern keeper | pubs | ale, tips **(verified)** | `shop_pub`, `system_pub_tip` |

## Open questions
- Which shops sell the later weapons and spells, and where each dungeon monster first appears.
