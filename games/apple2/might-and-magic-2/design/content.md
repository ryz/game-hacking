# Might and Magic II: Gates to Another World (Apple II) - content (variety lens)

What fills the game, as a reasonable variety: environments, opponents, items, abilities, people and places,
early and late, common and rare. Not a full list: complete tables are in the DOS documents
(`games/dos/might-and-magic-2/design/`), which describe the same world. The same shots also appear in
[systems.md](systems.md) and [interface.md](interface.md); overlap is intended.
Notation: [README.md](README.md). Check: `python3 tools/lenses.py apple2/might-and-magic-2`.

## 1. Kinds of content
| Kind | Total | Sample shown here |
|---|---|---|
| Areas | 60 (5 towns, 20 outdoor, 16 caverns, 10 dungeons and towers, 5 castles, 4 planes) **(verified: area warp)** | 45 places below |
| Opponents | many groups; fixed groups per square **(verified)** | 20 groups and bosses |
| Items | weapons, armor, misc, quest items **(verified: shop lists)** | shop lists and quest items |
| Services and skills | blacksmiths, taverns, temples, guilds, trainers, transport **(verified)** | about 30 offers |
| People | wizards, innkeepers, sages, prisoners, ghosts, a king **(verified)** | 20 people |
| Centuries | the world in year 900 and in the past **(verified: 800)** | Castle Xabran and King Kalohn |

## 2. Environments
| Place | Look | Shots |
|---|---|---|
| Middlegate (town 1) | blue stone walls, chequered green-grey street, sky | `env_middlegate_street`, `gameplay_middlegate_sign`, `gameplay_inn_start`, `gameplay_arena_entrance`, `gameplay_fountain_clairvoyance`, `gameplay_feldecarb` |
| Atlantium (town 2) | the same town walls; the Colosseum | `gameplay_atlantium`, `gameplay_atlantium_jail` |
| Tundara, Vulcania, Sandsobar (towns 3-5) | town walls; signs on doors | `gameplay_tundara_frozen`, `gameplay_vulcania_wild`, `gameplay_monster_bowl`, `gameplay_sandsobar_sewage`, `gameplay_lava_grenade` |
| Outdoors: coast and river | forest, sea, river (C2) | `gameplay_outdoors_c2`, `system_ferry`, `system_river_walker`, `start 34_c2_outside` |
| Outdoors: mountains | grey peaks, snow at the foot (A1, B1, C1) | `env_mountain_a1`, `env_mountains_b1`, `env_mountains_c1`, `gameplay_chosen_only` |
| Outdoors: forest | pine and leaf forests (D1, B2, A3, C3, D4) | `env_forest_d1`, `env_forest_b2`, `env_forest_a3`, `env_lake_c3`, `env_forest_d4`, `gameplay_corak_cave_entrance` |
| Outdoors: lava and desert | orange plains (E1, D3), desert oasis (E2) | `env_lava_e1`, `env_d3`, `env_desert_e2` |
| Outdoors: meadow | flowers and grass (C4) | `env_c4`, `dialogue_kalohn_asks` |
| Caverns | mossy green walls, black ceiling | `gameplay_cavern_lit`, `cave_x_marks`, `cave_torture_chamber`, `cave_frozen_cadavers`, `cave_atlantian_deity`, `cave_scholar_statue`, `gameplay_males_only`, `gameplay_murray_door`, `gameplay_dawn_throne` |
| Darkness | an unlit cavern: only "Darkness" | `battle_square_lake_devils` |
| Dungeons and towers | grey brick walls with red banners, blue chequered floor | `dialogue_orc_joker`, `gameplay_bottomless_pit`, `gameplay_giant_lever`, `gameplay_syrup_walls`, `gameplay_magical_well`, `gameplay_fear_no_evil`, `dialogue_ybmug`, `dialogue_yekop`, `gameplay_access_code` |
| Castles | grey halls, iron doors with signs | `env_castle_hillstone`, `gameplay_slayer_palace`, `gameplay_hoardall_palace`, `gameplay_unmarked_deadly`, `env_castle_xabran`, `env_castle_xabran_hall` |
| Elemental planes | Air: grey plain; Fire: orange plain under a sky (Earth and Water looked the same as Fire from their landing squares) | `env_plane_air`, `env_plane_fire` |
| Keeps and castles outdoors | white castle against a mountain | `gameplay_mandagual_keep`, `gameplay_xabran_800`, `gameplay_ruins_900` |
| Square Lake | the last cavern | `battle_sl_wizards`, `extra_just_kidding`, `boss_sheltem` |

## 3. Opponents (sample)
| Group | Where | Shots |
|---|---|---|
| Orcs (10) | C2 road, the first fight of set start | `start 36_orcs` |
| Witch's Cats and Rabid Rodents | Middlegate (8,1) | `battle_encounter`, `battle_screen`, `battle_victory` |
| Skeletons (8 + 5 more) | Middlegate | `battle_skeletons` |
| Blood Suckers and Muggers | Middlegate | `battle_blood_suckers` |
| Brain Eaters and a Merchant | Middlegate | `battle_brain_eaters` |
| Mutant, Iron Wizards, Foot Soldiers, Gnome Elders | cavern under Vulcania | `battle_vulcania_cavern` |
| Inept Wizards, Magic Serpent, Ghost, Priests, Pyro Hydras | Square Lake | `battle_sl_wizards` |
| Coffin Creeps (mummies) | Square Lake | `battle_sl_coffin_creeps` |
| Slashers | Square Lake | `battle_sl_slashers` |
| Enchantresses | Square Lake | `battle_sl_enchantress` |
| Death's Agents | Square Lake | `battle_sl_deaths_agents` |
| 66 Devil Kings | Square Lake | `battle_square_lake_devils` |
| Jouster (boss) | Jouster's Way | `boss_jouster` |
| Queen Beetle (boss) | E2 | `boss_queen_beetle` |
| Mega Dragon (boss) | C4, year 800 | `boss_mega_dragon` |
| Sheltem and four Elementals (final) | Square Lake gate | `boss_sheltem_options`, `boss_sheltem_fight`, `boss_sheltem_breath`, `gameover_sheltem` |

## 4. Items and equipment (sample)
| Item | Kind | Shots |
|---|---|---|
| Dagger, Hand Axe, Cudgel, Long Dagger, Short Sword, Nunchakas | weapons (Middlegate) | `shop_blacksmith_weapons` |
| +1 Staff, Sickle, Scythe, Blowpipe, Sling, Crossbow | specials | `shop_blacksmith_specials` |
| Small Shield ... Ring Mail, Helm | armor | `shop_blacksmith_armor` |
| Torch, Lantern, Magic Herbs, Thief's Pick, Rope'n'Hooks, Green Ticket | misc | `shop_blacksmith_misc` |
| Long Sword, Chain Mail, Large Shield, Helm, Crossbow | a knight's kit | `inventory_equipped` |
| Large Club | starting weapon of the premades | `shop_blacksmith_identify`, `menu_rename` |
| Element Orb, discs, Lava Grenade, Admit 8 Pass, Flaming Sword | quest items | `dialogue_element_orb`, `dialogue_xabran_disc`, `gameplay_lava_grenade`, `dialogue_zombie_pass`, `gameplay_flaming_sword` |
| Drinks and specialties | tavern fare | `shop_tavern_drinks`, `shop_tavern_specialties` |

## 5. Services, trainers and transport (sample)
`system_temple`, `system_training`, `system_mage_guild`, `system_locksmith`, `system_poorman_portal`,
`system_travel_agent`, `system_otto_mapper`, `system_pathfinder`, `system_mountaineer`, `system_detox`,
`system_athlete`, `system_hero_skill`, `system_polar_bear`, `system_crusader`, `system_merchant`,
`system_vulcania_export`, `system_illusionist`, `system_thief_trainer`, `system_gemmaker`, `system_ferry`,
`system_river_walker`, `gameplay_goofy_juice`, `gameplay_spinach`, `gameplay_swirling_pool`,
`gameplay_dragon_dung`, `gameplay_treadmill`, `gameplay_luck_plaque` **(verified: their texts)**.

## 6. People (sample)
| Person | Where | Shots |
|---|---|---|
| Spirit of Corak | Middlegate inn door | `cutscene_corak` |
| Innkeepers, waitress Amber, sages, a cleric | Middlegate, Atlantium | `save_innkeeper`, `dialogue_atlantium_inn`, `dialogue_waitress`, `dialogue_sages`, `system_temple` |
| Nordon and Nordonna | Middlegate | `dialogue_nordon`, `dialogue_nordon_quest`, `dialogue_nordonna` |
| Drunk sorcerer, old wino | Sandsobar | `dialogue_drunk_sorcerer`, `dialogue_wino` |
| Guardian Pegasus | C2 | `start 35_pegasus` |
| Zombie with a pass, Lloyd, Sarakin's ghost | caverns | `dialogue_zombie_pass`, `dialogue_lloyd_beacon`, `dialogue_sarakin` |
| Orc joker, Ybmug, Yekop | dungeons | `dialogue_orc_joker`, `dialogue_ybmug`, `dialogue_yekop` |
| A Lich Lord and his captive | D3 | `dialogue_lich_lord` |
| King Kalohn the Conjurer | C4, year 800 | `dialogue_kalohn_asks`, `dialogue_kalohn_wins` |
| Sheltem | Square Lake | `boss_sheltem`, `boss_sheltem_face` |

## Open questions
- Elemental planes of Earth and Water: their own look was not found (the landing squares showed the Fire
  plane's picture); the ending scenes are not shown (Sheltem not beaten).
