# Might and Magic II: Gates to Another World (DOS) - content (variety lens)

What the game is filled with: its places, opponents, things and people, shown as a reasonable variety rather
than a full list. Read it to see the range of what a player meets. The rules behind the content are in
[systems.md](systems.md), the screens it appears on in [interface.md](interface.md); the same shots appear
there, overlap is intended. Notation: [README.md](README.md). Check: `python3 tools/lenses.py dos/might-and-magic-2`.

## 1. Kinds of content
| Kind | In the game (count if known) | Shown here | Full list |
|---|---|---|---|
| Environments | 60 areas: 5 towns, 20 outdoor areas, 16 caverns, 5 castles, 8 dungeon levels, 2 towers, 4 elemental planes **(verified)**; wall sets town, cavern, castle; outdoor sets tundra, forest, mountains, desert, lava, ocean, swamp, sky **(verified: graphics files and views)** | section 2 | [world.md](world.md) |
| Opponents | about 250 monster kinds in MONSTERS.DAT (compressed) **(source: file size, manual)** | section 3 | - |
| Items | 256 item records: weapons, missile weapons, shields, armour, helms, miscellaneous, quest items **(RAM: ITEMS.DAT, 20 bytes each)** | section 4 | ITEMS.DAT |
| Abilities | 96 spells (48 cleric, 48 sorcerer, 9 levels) **(source)**, about 15 secondary skills **(verified: those on sale)** | section 5 | manual Appendix B |
| People | 6 premade characters, hirelings, quest givers, shopkeepers, trainers **(verified)** | section 6 | - |
| Puzzles and oddities | statues, levers, fountains, pools, joke signs, access codes, the final cryptogram **(verified)** | section 7 | - |

## 2. Environments
| Environment | Where | What sets it apart | Shots |
|---|---|---|---|
| Middlegate | area 00 | blue-green stone, wooden doors under signboards, torches; inn, fountains, arena, city gates, stairs down **(verified)** | `gameplay_inn_start`, `gameplay_middlegate_sign`, `gameplay_arena_entrance`, `gameplay_city_gates`, `gameplay_stairs_cavern`, `gameplay_fountain_clairvoyance`, `gameplay_feldecarb` |
| Atlantium | area 01 | the same stone under an open sky, chequered floor; Colosseum, city jail **(verified)** | `gameplay_atlantium`, `gameplay_atlantium_jail` |
| Tundara | area 02 | icy town with a Frozen Monster behind a door **(verified)** | `gameplay_tundara_frozen` |
| Vulcania | area 03 | volcanic town with a wild section **(verified)** | `gameplay_vulcania_wild`, `gameplay_lava_grenade` |
| Sandsobar | area 04 | desert town with the Monster Bowl and slums **(verified)** | `gameplay_monster_bowl`, `gameplay_sandsobar_sewage` |
| Tundra and snow | A1, B2 | white snowfields, snowy forest **(verified)** | `env_tundra_a1`, `env_snowforest_b2` |
| Forest | B1, D1, C3, D4 | broadleaf forest, signposts **(verified)** | `env_signpost_b1`, `env_forest_d1`, `env_lake_c3`, `env_signpost_d4` |
| Mountains | C1 | grey rock range **(verified)** | `env_mountains_c1` |
| Grassland and lava | D3, E1 | plain with trees, lava field **(verified)** | `env_lava_d3`, `env_lava_e1` |
| Desert | E2 | red and yellow sand, oasis **(verified)** | `env_desert_e2` |
| Meadow | C4 | flowering meadow of the Quagmire of Doom **(verified)** | `env_meadow_c4` |
| Sea and rivers | A3, C2 | open water, whirlpools, ferries **(verified)** | `env_sea_a3`, `gameplay_outdoors_c2`, `system_ferry` |
| Caverns | 11-20 | green stone, dark without light **(verified)** | `gameplay_cavern_lit`, `cave_atlantian_deity`, `cave_scholar_statue`, `cave_frozen_cadavers`, `gameplay_sarakin_mine`, `gameplay_murray_door`, `gameplay_druid_sign`, `gameplay_dawn_throne` |
| Castles | 37-3B | grey brick, banners, blue floor, iron doors named above **(verified)** | `env_castle_hillstone`, `gameplay_slayer_palace`, `gameplay_hoardall_palace`, `gameplay_unmarked_deadly`, `env_castle_xabran` |
| Dungeons and towers | 2D-36 | castle walls below ground, towers with stasis chambers **(verified)** | `gameplay_bottomless_pit`, `gameplay_giant_lever`, `gameplay_syrup_walls`, `gameplay_magical_well`, `gameplay_fear_no_evil`, `gameplay_access_code` |
| Elemental planes | 29-2C | outdoor sets in one element each: snow (Air), fire, grass (Earth), water **(verified)** | `env_plane_air`, `env_plane_fire`, `env_plane_earth`, `env_plane_water` |
| Places seen from outside | outdoors | castle and cave pictures in the view: Mandagual's Keep, Castle Xabran, Corak's Cave **(verified)** | `gameplay_mandagual_keep`, `gameplay_xabran_800`, `gameplay_corak_cave_entrance` |

## 3. Opponents
| Opponent | Where | Notes | Shots |
|---|---|---|---|
| Witch's Cats, Rabid Rodents | Middlegate (8,1) | first fixed fight **(verified)** | `battle_encounter` |
| Skeletons | Middlegate Skeleton Closet | 13, "+5 more" **(verified)** | `battle_skeletons` |
| Brain Eaters and a Merchant | Middlegate (13,12) | **(verified)** | `battle_brain_eaters` |
| Blood Suckers and Muggers | Middlegate (12,14) | **(verified)** | `battle_blood_suckers` |
| Mixed horde | cavern under Vulcania | Rabid Rodents, Royal Horsemen, Frost Dragons, Werewolves, nine Barbarians **(verified)** | `battle_vulcania_cavern` |
| Skeletons and Zombies | Corak's Cave | **(verified)** | `battle_corak_cave` |
| Valiant Knights, Guardian Hounds | Ice Cavern | **(verified)** | `battle_ice_cavern` |
| Killer Bees, Death's Agents, Magic Serpent | Pinehurst Dungeon | **(verified)** | `battle_killer_bees` |
| Square Lake's guardians | cavern under Square Lake | Phantasms, Gargoyles, Guardians, Warbots, Alien Probes with Devil's Envoys, Killer Cobras, Hunchbacks **(verified)** | `battle_sl_phantasms`, `battle_sl_gargoyles`, `battle_sl_guardians`, `battle_sl_warbots`, `battle_sl_alien_probes` |
| 66 Devil Kings | Square Lake (11,14) | attack unless the party is the Chosen One **(verified)** | `battle_square_lake_devils`, `dialogue_devil_kings_bow` |
| The Jouster | Jouster's Way, B3 | fights knights only **(verified: area text)** | `boss_jouster` |
| Queen Beetle | E2 (11,6), "the Crawling Envoy of Evil" | **(verified)** | `boss_queen_beetle` |
| Lich Lord and Monster Masher | D3, holding a scientist | **(verified)** | `dialogue_lich_lord`, `boss_lich_lord` |
| Mega Dragon | C4, year 800 | kills King Kalohn without the Orb and Talons **(verified)** | `boss_mega_dragon` |
| Sheltem and four Elementals | Square Lake gate | the final fight: 500 and 250 hit points **(RAM)** | `boss_sheltem_appears`, `boss_sheltem_fight`, `boss_sheltem_slashes` |

## 4. Items and equipment
| Item | Kind | Notes | Shots |
|---|---|---|---|
| Dagger ... Nunchakas, Staff, Sling, Crossbow | weapons | Middlegate's stock, "+1" specials **(verified)** | `shop_blacksmith_weapons`, `shop_blacksmith_specials` |
| Small Shield ... Ring Mail, Helm | armour | **(verified)** | `shop_blacksmith_armor` |
| Torch, Lantern, Magic Herbs, Thief's Pick, Rope'n'Hooks, Green Ticket | misc | the ticket opens an arena **(verified: list; source: use)** | `shop_blacksmith_misc` |
| Magic Sword, S Plate Mail, Gold Shield, Death Bow, Defense Ring | late gear | ryz's end-game equipment **(verified: profile)** | `system_use_prompt` |
| Lava Grenade | found item | **(verified)** | `gameplay_lava_grenade` |
| Flaming Sword | found item | stuck in volcanic rock **(verified)** | `gameplay_flaming_sword` |
| Admit 8 Pass | quest item | given by a zombie, opens Corak's Cave **(verified)** | `dialogue_zombie_pass` |
| Gold Goblet | quest item | Nordon's goblet in the cavern under Middlegate **(verified: area text)** | `dialogue_nordon_quest` |
| Discs, Talons, Element Orb | quest items | Discs in Castle Xabran (year 800), Talons from the planes' shrines, the Orb in Dawn's Mist **(verified: Disc and Orb prompts)** | `dialogue_xabran_disc`, `dialogue_element_orb` |

## 5. Abilities and spells
| Ability | Kind | Notes | Shots |
|---|---|---|---|
| Light, Bless, Flame Arrow, Protection from Elements | spells levels 1-2 | **(verified: cast)** | `system_cast_spellbook`, `battle_cast_prompt`, `battle_spell_hit`, `system_protect_elements` |
| Enchant Item | sorcerer level 9 | sold by the gemmaker in the volcano **(verified: offer)** | `system_gemmaker` |
| Cartographer, Athlete, Hero, Crusader, Merchant, Pathfinder, Mountaineer | skills | **(verified: offers)** | `system_otto_mapper`, `system_athlete`, `system_hero_skill`, `system_crusader`, `system_merchant` |
| Thievery | robbers | **(verified)** | `system_thief_trainer` |
| Walking on water | travel skill | taught by a river walker for 50 gold **(verified: offer)** | `system_river_walker` |

## 6. Characters and people
| Person | Where | Notes | Shots |
|---|---|---|---|
| The party | everywhere | ryz, condi, ebo, cubi, deddo, mnz **(verified)** | `inventory_profile_vet`, `inventory_remove_prompt` |
| Spirit of Corak | Middlegate | greets the party **(verified)** | `dialogue_spirit_corak` |
| Svendegard the blacksmith, the waitress, the cleric | Middlegate | **(verified)** | `shop_blacksmith_door`, `dialogue_waitress`, `system_temple` |
| Nordon and Nordonna | Middlegate | wizard siblings: a goblet quest and a rebuff **(verified)** | `dialogue_nordon`, `dialogue_nordonna` |
| Guardian Pegasus | C2 | helps once a year if you know its name **(verified)** | `gameplay_pegasus` |
| Townsfolk | Sandsobar | drunk sorcerer, wino with a rumor **(verified)** | `dialogue_drunk_sorcerer`, `dialogue_wino` |
| A prisoner of Lord Slayer | Hillstone Dungeon | offers a way to Woodhaven Dungeon **(verified)** | `dialogue_orc_joker` |
| Ybmug and Yekop | Dark Keep, Tower of Mercy | the evil and the good wizard in stasis fields **(verified)** | `dialogue_ybmug`, `dialogue_yekop` |
| King Kalohn | C4, year 800 | **(verified)** | `dialogue_kalohn_asks`, `dialogue_kalohn_wins` |

## 7. Puzzles and oddities
| Thing | Where | Shots |
|---|---|---|
| Fountains, pools, wells | towns, caverns, dungeons | `gameplay_swirling_pool`, `gameplay_magical_well` |
| Murray's Goofy Juice, cans of spinach, a giant treadmill | caverns | `gameplay_goofy_juice`, `gameplay_spinach`, `gameplay_treadmill` |
| Joke signs before the end | Square Lake, y=15 | `extra_just_kidding` |
| The final cryptogram | Square Lake control room | `ending_cryptogram` |

## Open questions
- Monster statistics: MONSTERS.DAT is compressed; the fight record in memory gives names and hit points.
