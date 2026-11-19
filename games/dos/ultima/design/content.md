# Ultima I: The First Age of Darkness (DOS) - content (variety lens)

What the game is filled with: its places, opponents, things and people, shown as a reasonable variety rather
than a full list. Read it to see the range of what a player meets. The rules behind the content are in
[systems.md](systems.md), the screens it appears on in [interface.md](interface.md); the same shots appear
there, overlap is intended. Notation: [README.md](README.md). Check: `python3 tools/lenses.py dos/ultima`.
Shot ids are those of set `main`.

## 1. Kinds of content
| Kind | In the game (count if known) | Shown here | Full list |
|---|---|---|---|
| Environments | overworld (4 continents, 4 terrains), towns (32 on 8 plans), castles (8 on 2 plans), landmarks (8), dungeons (36, 10 levels each), space (49 sectors), Mondain's chamber **(verified data)** | 4 continents, 8 town plans, 2 castle plans, 8 landmarks, dungeon levels 1-10, space top and front view, the chamber | `../tools/worldmap.py --list` |
| Opponents | 15 overworld kinds (4 at sea), 25 dungeon kinds, guards, enemy fighters, Mondain **(verified)** | 11 overworld, 24 dungeon, guards, fighters, Mondain | §3 |
| Items | 4 gems, food, coin **(verified)** | gems, food | |
| Equipment | 16 weapons, 6 armours **(verified)** | 12 weapons, 6 armours | playbook RAM map |
| Abilities / spells | 11 spells **(verified)** | 10 | §5 |
| Vehicles | horse, cart, raft, frigate, aircar, shuttle, time machine **(verified)** | all 7 | §4 |
| Characters and people | 8 kings, 8 princesses (Julia, Cassandra, Marsha, Donna, Kristen, Beth, Lori, Dianne), merchants, tavern keepers, guards, jesters, Iolo the Bard, wenches, Mondain **(ROM text / verified)** | 6 | §6 |

## 2. Environments
| Environment | Where | What sets it apart | Shots |
|---|---|---|---|
| Grassland | everywhere | dotted green, the default **(verified)** | `start_overworld`, `gameplay_horse` |
| Woods | all continents | round trees; aircars cannot enter **(verified)** | `gameplay_woods`, `system_aircar_woods` |
| Mountains and lakes | all continents | grey peaks, blue water; both block walkers **(verified)** | `gameplay_lands_lord_british`, `system_blocked_mountains`, `system_blocked_water` |
| The four lands | one per quarter | same terrain kinds, their own coasts, ridges and places **(verified)** | `gameplay_lands_lord_british`, `gameplay_lands_feudal_lords`, `gameplay_lands_dark_unknown`, `gameplay_lands_danger_despair` |
| Open sea | around the continents | ships, sea monsters **(verified)** | `gameplay_at_sea`, `gameplay_raft` |
| Town: Britian plan | Britian, Arnold, Nassau, Gorlab | all six shops, a pond **(verified)** | `gameplay_britian` |
| Town: Moon plan | Moon, Linda, Clear Lagoon, Dextron | central pond, grocery, inn **(verified)** | `gameplay_town_moon` |
| Town: Fawn plan | Fawn, Helen, Stout, Magic | a green park **(verified)** | `gameplay_town_fawn` |
| Town: Paws plan | Paws, Owen, Gauntlet, Wheeler | six shops side by side, two ponds **(verified)** | `gameplay_town_paws` |
| Town: Montor plan | Montor, John, Imagination, Bulldozer | round walls, only food and weapons **(verified)** | `gameplay_town_montor` |
| Town: Yew plan | Yew, Gerry, Ponder, The Brother | pub in the middle **(verified)** | `gameplay_town_yew` |
| Town: Tune plan | Tune, Wolf, Wealth, Turtle | a moat around the town **(verified)** | `gameplay_town_tune` |
| Town: Grey plan | Grey, The Snake, Poor, Lost Friends | shops along the north wall **(verified)** | `gameplay_town_grey` |
| Castle: Lord British plan | odd castles | pools, armour, food and weaponry rooms, throne, prison **(verified)** | `gameplay_castle` |
| Castle: Lost King plan | even castles | mess hall, stables, prison, F W A rooms **(verified)** | `gameplay_castle_lost_king` |
| Landmark | 8 on the map | a sign, a pillar, a tower or a grave on the map, an inscription box inside **(verified)** | `gameplay_landmark_tower`, `system_landmark_grave` |
| Dungeon | 36 entrances | white wireframe on black; doors, ladders, force fields; deeper is deadlier **(verified)** | `gameplay_dungeon`, `gameplay_dungeon_door`, `gameplay_dungeon_ladder`, `system_spell_create` |
| Space | 49 sectors | planet, sun, starbases; starfield front view; hyperspace streaks; the sun burns ships **(verified)** | `gameplay_space_top`, `gameplay_space_front`, `system_hyperjump`, `gameover_sun` |
| Mondain's chamber | after the time machine | red brick walls on black **(verified)** | `boss_mondain` |
| Ending | | white text on black **(verified)** | `ending_text` |

## 3. Opponents
Overworld (map pieces; each kind has two animation pictures) **(verified)**:
| Opponent | Where met | Picture | What it does | Shots |
|---|---|---|---|---|
| Orc | land | green humanoid | 2 damage | `battle_orc_hit`, `battle_orc_killed`, `system_aircar_lasers` |
| Thief | land | blue figure | 8 damage; steals (ROM text) | none: looks like the other land fights; the dungeon thief's theft is `battle_thief` |
| Evil trent | land | a walking tree, looks like woods | 14 damage | `battle_evil_trent` |
| Knight, Dark knight | land | armoured figures | 2 and 10 damage | `battle_knight`, `battle_dark_knight` |
| Necromancer, Wandering warlock | land | robed casters | 6 and 14 damage | `battle_necromancer`, `battle_wandering_warlock` |
| Bear | land | brown bear | 2 damage | `battle_bear` |
| Hood | land | red figure | 2 damage | `battle_hood` |
| Hidden archer | land | invisible on the map | 6 damage | `battle_hidden_archer` |
| Ness creature, Giant squid, Dragon turtle | sea | serpent, squid, turtle | 8, 8, 4 damage | `battle_ness_creature`, `battle_giant_squid`, `battle_dragon_turtle` |
| Pirate ship | sea | a ship | sunk by cannons | `system_frigate_fire` |
| Evil ranger | land | figure | (ROM text, spawned in tests) | none: same picture family as the knights |

Dungeon (25 kinds, white line drawings; stronger kinds deeper; the level shown is where they were met here)
**(verified)**:
| Opponent | Level | What it does | Shots |
|---|---|---|---|
| Ranger | 1 | | `battle_ranger`, `system_klimb_down` |
| Skeleton | 1 | 2 damage | `battle_skeleton` |
| Thief | 1 | steals an item | `battle_thief` |
| Giant rat, Bat | 2 | | `battle_giant_rat`, `battle_bat` |
| Spider, Viper | 3 | | `battle_spider_killed`, `battle_viper` |
| Orc, Cyclops | 4 | | `battle_magic_missile`, `battle_cyclops` |
| Gelatinous cube | 4 | invisible; destroys armour; Lost King's quest monster | `battle_gelatinous_cube`, `system_quest_kill` |
| Ettin | 5 | 105 damage | `battle_ettin` |
| Mimic | 5 | looks like a chest | `battle_mimic` |
| Lizard man, Minotaur | 6 | Minotaur 175 damage | `battle_lizard_man`, `battle_minotaur` |
| Carrion creeper | 7 | Rondorin's quest monster | `battle_carrion_creeper` |
| Tangler | 7 | | `battle_tangler` |
| Gremlin | 8 | steals food | `battle_gremlin` |
| Wandering eyes | 8 | | `battle_wandering_eyes` |
| Wraith | 9 | 255 damage | `battle_wraith` |
| Lich | 9 | Black Dragon's quest monster | `battle_lich`, `system_spell_kill` |
| Invisible seeker | 9 | not drawn | none: an empty corridor picture, like the cube |
| Mind whipper | 10 | mental attack, 197 damage | `battle_mind_whipper` |
| Zorn, Daemon | 10 | | `battle_zorn`, `battle_daemon` |
| Balron | 10 | Shamino's quest monster | `battle_balron` |

Others: castle guards (`battle_guard`), the jester (`system_jester_key`), enemy fighters in space
(`gameplay_space_enemy`, `battle_space_hit`, `battle_alien_fires`), Mondain and his bat form (`boss_mondain`,
`boss_hit_mondain`, `boss_mondain_bat`, `boss_or_is_he`) **(verified)**.

## 4. Items, equipment, vehicles
| Item | Type | Got from | What it does | Shots |
|---|---|---|---|---|
| Dagger, Axe, Sword, Bow & Arrows, Wand | weapon | even towns' weapon shops | melee / ranged | `shop_weapons_even`, `inventory_ready_weapon` |
| Mace, Rope & Spikes, Great Sword, Amulet, Staff | weapon | odd towns' weapon shops | | `shop_weapons`, `shop_weapons_late` |
| Light Sword, Blaster (and Pistol, Phazor, Triangle) | weapon | castle storerooms, by stealing | space-age weapons | `system_steal_storeroom`, `inventory_ztats_late` |
| Leather armor, Chain mail, Plate mail | armour | armour shops | defence | `shop_armour`, `inventory_ready_armour` |
| Vacuum suit, Reflect suit | armour | armour shops after 3,000 moves | needed to dock in space | `shop_armour_late`, `system_steal` |
| Food | supply | grocery | 10 per pack | `shop_food_bought` |
| Red, green, blue, white gems | quest items | the four gem kings | open the time machine | `dialogue_gem_red`, `cutscene_time_machine` |
| Horse, cart | vehicle | transport shop | faster on land | `gameplay_horse`, `gameplay_cart` |
| Raft, frigate | vehicle | transport shop | sea travel; the frigate has cannons | `gameplay_raft`, `gameplay_frigate`, `system_frigate_fire` |
| Aircar | vehicle | transport shop after 3,000 moves | lasers; no woods | `gameplay_aircar`, `system_aircar_lasers` |
| Shuttle | vehicle | transport shop after 3,000 moves | into space | `gameplay_shuttle`, `system_liftoff` |
| Time machine | vehicle | the princess's reward | to Mondain; needs all four gems | `gameplay_time_machine`, `system_time_machine_no_gems` |

## 5. Abilities
| Spell | Got from | What it does | Shots |
|---|---|---|---|
| Prayer | always | "POTENTIS-LAUDIS!"; no effect outdoors | `system_cast_prayer` |
| Open | odd magic shops (5) | opens a coffin | `system_spell_open` |
| Unlock | even magic shops (10) | opens a chest without its trap | `system_spell_unlock` |
| Magic Missile | odd magic shops (15) | damages the monster ahead | `battle_magic_missile` |
| Ladder Down / Ladder Up | odd (25) / even (30) magic shops | creates a ladder | `system_spell_ladder_down`, `system_spell_ladder_up` |
| Blink | not sold in towns | teleports | `system_spell_blink` |
| Create / Destroy | not sold in towns | force field ahead / removes it | `system_spell_create`, `system_spell_destroy` |
| Kill | not sold in towns | destroys the monster ahead | `system_spell_kill` |
| Steal | not sold in towns | (not tried) | none: not owned in any save made here |

## 6. People
| Person | Where | Role | Shots |
|---|---|---|---|
| Lord British | his castle | landmark quests, hit points for pence | `dialogue_king_offer`, `dialogue_king_quest`, `dialogue_quest_done` |
| The Lost King | his castle | monster quest, red gem | `dialogue_king_kill_quest`, `dialogue_gem_red` |
| Kings of Rondorin, the Black Dragon's Castle, Shamino | their castles | green, blue, white gems with hints | `dialogue_gem_green`, `dialogue_gem_blue`, `dialogue_gem_white` |
| King of Olympus | his castle | landmark quest (Pillar of Ozymandias) | `dialogue_king_olympus` |
| Princess Julia | Lord British's prison | rescue reward, the time machine | `system_cell_open_late`, `system_princess_reward` |
| Merchants | town shops | Lord Eldric D'Charbonneux, Mad Chad, Li'l Karelia, Max, Mystic Melinda ... | `shop_armour`, `shop_magic`, `shop_food`, `shop_armour_late`, `shop_magic_even` |
| Tavern keeper | pubs | ale, tips | `shop_pub`, `dialogue_pub_mondain` |
| Jester | castles | carries the prison key | `system_jester_key` |
| Guards | towns, castles | punish theft and violence | `battle_guard`, `system_steal_caught` |

## Open questions
- Where Blink, Create, Destroy, Kill and Steal are sold (no town sells them; maybe castles or none).
- The Evil ranger and Invisible seeker pictures were not captured on their own.
