# The Bard's Tale: Tales of the Unknown - content (variety lens)

What the game is filled with, as a reasonable variety. The rules are in [systems.md](systems.md), the screens
in [interface.md](interface.md); overlap is intended. Notation: [README.md](README.md). Check:
`python3 tools/lenses.py apple2/bards-tale`. Shot ids are from the `main` set.

## 1. Kinds of content
| Kind | In the game (count if known) | Shown here | Full list |
|---|---|---|---|
| Environments | the city and 16 dungeon levels in 6 dungeons, 5 wall looks | all 16 levels | [maps/README.md](maps/README.md) |
| Opponents | many monster kinds with portraits (not counted) | 25 groups | - |
| Items | Garth's 9 basics and more pages, found items, quest objects | about 15 | - |
| Spells and songs | four-letter spells of four mage classes, six bard tunes | 9 spells, 1 song prompt | - |
| People | shopkeepers, priests, barkeeps, Roscoe, Kylearan, Mangar | 8 | - |
| Riddles and inscriptions | per dungeon | 11 | [maps/README.md](maps/README.md) (`!` squares) |

## 2. Environments
| Environment | Where | What sets it apart | Shots |
|---|---|---|---|
| Skara Brae streets | the city | painted house fronts, red street, blue sky; snow-closed gate | `hud_city`, `env_city_street`, `env_city_houses`, `gameplay_gate` |
| City buildings | taverns, temples, shops | a keeper's picture in place of the view | `shop_garth`, `system_temple`, `dialogue_tavern`, `system_roscoe` |
| Grey-blue brick | Wine cellar, Harkyn's Castle 1-3, Kylearan's Amber Tower | light blue bricks, green doors | `env_cellar_corridor`, `env_cellar_door`, `env_castle1_corridor`, `env_castle1_door`, `env_castle2_corridor`, `env_castle3_corridor`, `env_kylearan_corridor`, `env_kylearan_door` |
| Sewers | Sewers 1-3 | brown-orange stone with green slime, water | `env_sewers`, `env_sewers2_corridor`, `env_sewers3_corridor` |
| Catacombs | Catacombs 1-3 | purple walls with skulls and bones | `env_catacombs1_corridor`, `env_catacombs1_door`, `env_catacombs2_corridor`, `env_catacombs3_corridor` |
| Mangar's Tower | levels 1-5 | green and orange diagonal stone, blue doors; many dark squares | `env_mangar1_corridor`, `env_mangar2_corridor`, `env_mangar3_corridor`, `env_mangar3_door`, `env_mangar5_corridor` |
| Darkness | squares in the Sewers and Mangar's Tower | the view goes black, light is put out | `gameplay_darkness` |

## 3. Opponents
| Opponent | Where met | Family / picture | What it does | Shots |
|---|---|---|---|---|
| Skeletons and a Kobold | Skara Brae streets | undead | claws for 7-12, kill a level-1 party | `battle_encounter`, `battle_target`, `battle_round` |
| Stone Golem | city guardian statue | statue | comes to life when attacked | `battle_golem` |
| Spinners | Sewers | giant spider | fixed group | `battle_spinners` |
| Bladesman, Wizards, Magicians, Assassin | Sewers | human party | casters with fighters | `battle_humans` |
| Ogre magi | Catacombs 2 | ogre | groups of 7 | `battle_ogre_magi` |
| Wight, Magicians, Sorcerer | Catacombs 2 | undead and mages | mixed groups | `battle_magicians` |
| Blue dragons | Harkyn's Castle | dragon | - | `battle_blue_dragons` |
| Stone giants, Jackalweres, Black widows, Goblin lords | Harkyn's Castle | four groups | the most groups at once | `battle_stone_giants` |
| Green dragons | Kylearan's Tower | dragon | a forced fight square | `battle_green_dragons` |
| Crystal statue | Kylearan's Tower | statue | Fight it or Exit the room | `gameplay_ky_statue` |
| Lurkers, Magicians, Xorns | Mangar's Tower 1 | Xorn portrait | - | `battle_xorns` |
| Fred | Mangar's Tower 1 | a single odd foe | "You face 1 Fred" | `battle_fred` |
| Shadows and Phantoms | Mangar's Tower 1 | spirits (blue cloud portrait) | - | `battle_phantoms` |
| Fire giant, Magicians, Wizard | Mangar's Tower 1 | giant | - | `battle_fire_giant` |
| Ivory monks | Mangar's Tower 1 | monk | - | `battle_ivory_monks` |
| Storm giants | Mangar's Tower 5 | giant | - | `battle_storm_giants` |
| Ancient enemies | Mangar's Tower 5 | spirits | - | `battle_ancient_enemies` |
| Balrogs | Mangar's Tower 5 | demon (old man portrait) | - | `battle_balrogs` |
| Spectres | Mangar's Tower 5 | ghost | - | `battle_spectres` |
| Archmage | Mangar's Tower 5 | mage | - | `battle_archmage` |
| Mangar the Dark (boss) | antechamber, Mangar's Tower 5 | archmage with 2 Greater demons and 3 Vampire lords | summons friends; casts at the whole party (16-24 points each); a Vampire lord claws for 69 | `boss_mangar`, `boss_mangar_friends`, `boss_mangar_group`, `boss_mangar_spell` |

## 4. Items and equipment
| Item | Type | Got from | What it does | Shots |
|---|---|---|---|---|
| Torch, Lamp | light | Garth's (5, 15) | light in dungeons | `shop_buy` |
| Broadsword, Short Sword, Dagger, War Axe, Halbard, Mace, Staff | weapons | Garth's (20-200) | melee | `shop_buy` |
| Buckler and further goods | shields, armour | Garth's next pages | defence | `shop_buy2` |
| Leather Gloves, Mithril Dagger, Mandolin | armour, weapon, instrument | found (ALFAR's list) | the Mandolin lets a Bard play | `inventory_items`, `shop_sell`, `inventory_bard_items` |
| Misc. Item | found | Mangar's treasure | unknown until identified | `ending_treasure` |
| Silver triangle | quest object | Kylearan's Tower | one of the three shapes of Mangar's tower | `gameplay_silver_triangle`, `gameplay_m5_shapes` |
| Wine, Ale, Beer, Mead, Foul spirits, Ginger Ale | drinks | taverns | Wine at the Scarlet Bard leads to the cellar | `dialogue_drinks` |

## 5. Spells and songs
| Spell | Class | What it does | Shots |
|---|---|---|---|
| MAFL (Mage Flame) | Conjurer 1 | light, torch icon | `system_mafl` |
| ARFI (Arc Fire) | Conjurer 1 | fire at one foe (0 damage seen once) | none: in the `start` set (`25_cast`, `29_arfi_miss`) |
| MACO (Magic Compass) | Conjurer | compass icon | `spell_maco` |
| LERE (Lesser Revelation) | Conjurer | brighter light, blue icon | `spell_lere` |
| LEVI (Levitation) | Conjurer | levitation icon | `spell_levi` |
| WOHL (Word of Healing) | Conjurer | heals a member | `spell_wohl` |
| SCSI (Scry Site) | Magician | position from the entry stairs | `spell_scsi` |
| AREN | Magician | eye icon (detection) | `spell_aren` |
| Bard tunes 1-6 | Bard | lasting effects (not measured) | `song_prompt`, `song_no_instrument` |

## 6. People
| Person | Where | Role | Shots |
|---|---|---|---|
| Garth | Equipment Shoppe | trader | `shop_garth`, `shop_menu` |
| Roscoe | Energy Emporium | spell points | `system_roscoe` |
| Priests | temples | healing | `system_temple` |
| Priest of the Mad God | his temple | asks the Mad One's name (TARJAN) | `dialogue_madgod` |
| Barkeeps | taverns | drinks, rumours for tips | `dialogue_barkeep`, `dialogue_rumour` |
| Guild leaders | Review Board | levels and spells | `system_review` |
| Michael Cranford | the building in front of the Guild | the author's portrait | `extra_credits` |
| Kylearan | his tower; the ending | the good archmage | `dialogue_kylearan`, `ending_kylearan` |

## 7. Riddles, inscriptions and other specials
| Text | Where | Shots |
|---|---|---|
| "Seek the Snare from behind the scenes" / "The hand of time writes and cannot erase" | Sewers | `gameplay_sewers_inscription`, `gameplay_sewers_inscription2` |
| Tripwire trap, stone block falls | Sewers, Castle 2 | `gameplay_sewers_trap`, `gameplay_trap` |
| "Name the endless byway ..." / "Name the one of cold, foretold twofold" | Kylearan's Tower | `gameplay_ky_riddle`, `gameplay_ky_riddle2` |
| "Beware the sting at the tail (south) of the serpent-way" | Kylearan's Tower | `gameplay_ky_voice` |
| "As a guardian he must walk ..." / "Made of earth, yet without soul ..." | Kylearan's Tower | `gameplay_ky_inscription`, `gameplay_ky_inscription2` |
| "Death to those who would attack the mighty one!" | Mangar's Tower 5 | `gameplay_m5_mouth` |
| Smoke in your eyes; a pool of boiling liquid | Mangar's Tower 5 | `gameplay_smoke`, `gameplay_m5_pool` |
| Mangar's treasure trove with two hungry dragons | Mangar's Tower 5 | `gameplay_m5_treasure` |
| "What can bind the mightiest foes?" (a tavern rumour names the Spectre Snare) | Mangar's Tower 5 | `gameplay_m5_bind`, `dialogue_rumour` |
| "You are in the sewers under Skara Brae ..." | Sewers 1 | `gameplay_sewers_arrival` |

## Open questions
- The answers to the Kylearan riddles were not tried.
- Item list beyond Garth's first two pages; what the found Misc. Item is.
