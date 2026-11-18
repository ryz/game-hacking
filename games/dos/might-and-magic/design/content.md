# Might and Magic Book One: The Secret of the Inner Sanctum (DOS) - content (variety lens)

What the game is filled with: its places, opponents, things and people, shown as a reasonable variety rather
than a full list. Read it to see the range of what a player meets. The rules behind the content are in
[systems.md](systems.md), the screens it appears on in [interface.md](interface.md); the same shots appear
there, overlap is intended. Notation: [README.md](README.md). Check: `python3 tools/lenses.py dos/might-and-magic`.

Totals come from the game's own tables **(RAM: read from the program and its data files, not all seen in
play)**; everything with a shot is **(verified)**.

## 1. Kinds of content
| Kind | In the game (count if known) | Shown here | Full list |
|---|---|---|---|
| Environments | 55 areas of 16 x 16 squares: 5 towns, 9 caverns, 20 wilderness sectors, 21 castle and dungeon levels; about ten distinct looks | every look, 25 areas | [world.md](world.md) 1, 7 |
| Opponents | 195 named monsters using 76 pictures | about 70 kinds in 45 groups, about 35 pictures | none yet (the table is in the program; `tools/survey.py` prints the groups per area) |
| Items and equipment | 255: 60 hand weapons, 25 missile weapons, 35 two-handed weapons, 35 armors, 15 shields, 85 other items | 30 by name, in shop lists, profiles and finds | none yet; Sorpigal's prices in [sorpigal.md](sorpigal.md) 2 |
| Spells | 94: 47 Cleric and 47 Sorcerer, 7 levels | 11 cast by the party, 4 cast by monsters | the manual, Appendix B |
| Characters and people | 6 classes, 5 races, 3 alignments; shopkeepers, trainers and innkeepers in 5 towns; lords, wizards and oddities on event squares | all classes and races; about 25 people | [characters.md](characters.md), [world.md](world.md) 2, 5 |
| Statues, plaques and messages | 8 statues in Sorpigal alone; wall messages in caverns and castles | all 8 statues, 3 messages | [sorpigal.md](sorpigal.md) 7 |

## 2. Environments
One row per distinct look or place type, not per map.

| Environment | Where | What sets it apart | Shots |
|---|---|---|---|
| Town corridors | the five towns | large white bricks, wooden doors between torches, signs over service doors | `start_inn_door`, `sorpigal_inn_sign`, `door_locked`, `portsmith_inn_sign`, `leprechaun_algary` |
| Service rooms | every town | the view stays a wall; the room is its menu and the name on the lower edge | `shop_blacksmith_menu`, `temple_services`, `tavern_menu`, `train_level2` |
| Cavern, lit | caverns 1-9 | grey-green rock walls, white portcullises | `dungeon_lit`, `env_cave6`, `cave_wall_message` |
| Darkness | any cavern or dungeon without light | only the word "DARKNESS" | `dungeon_darkness`, `trap_door_after` |
| Castle, plain | Castle Doom, the demon's stronghold, below Dragadune | smaller white bricks, long empty corridors | `env_doom`, `env_demon`, `env_udrag1`, `doom_golden_door` |
| Castle with banner doors | Blackridge South, White Wolf | cyan doors under red banners | `env_blackridge_s`, `env_whitewolf`, `whitewolf_button` |
| Castle with carved doors | Alamar | brown wooden doors with faces | `env_alamar`, `alamar_guards` |
| Dungeon with portcullis | Quivering Forest level 2 | blue portcullis in the brick wall | `env_qvl2`, `qvl_floor_spins` |
| Astral Plane | the last area | bare brick, projector squares, a slotted door | `astral_room`, `astral_door`, `astral_projector` |
| Forest | sectors C-1, C-2, D-1, E-3 and others | green firs along a sand path | `outdoors_first`, `env_forest_c1`, `env_road_d1`, `outdoors_forest`, `outdoors_fountain` |
| Mountains | C-2, C-3, D-2, D-3 | brown peaks with snow caps over green slopes | `env_mountains_d3`, `outdoors_cave`, `outdoors_statues` |
| Rock walls | A-1, A-4, B-2 | striped orange and green cliffs forming a canyon | `env_cliffs_a1`, `a1_ice`, `a1_castle_doom` |
| Ice | A-2, B-1 | cyan ice mountains, white frozen ground | `env_ice_a2`, `env_glacier_b1` |
| Sea and beach | A-3, A-4, B-4, C-4 | blue water, yellow sand | `env_sea_a3`, `env_beach_a4`, `env_coast_c4` |
| Swamp | D-4, E-4 | reeds with purple heads in green water | `env_swamp_d4` |
| Volcano and lava | E-1, E-2 | a red cone in a red field; lava across the road | `env_volcano_e1`, `env_lava_e2`, `e1_volcano`, `e1_dragadune` |
| Special places | on event squares | text only, the view does not change | `cave_arena`, `cave_portal`, `algary_portal`, `outdoors_gypsy`, `portsmith_secret` |

## 3. Opponents
A spread over families, strengths and behaviours; bosses and named ones marked. "Strength" is the experience the
game's table gives for one **(RAM)**.

| Opponent | Where met | Family / picture | What it does | Shots |
|---|---|---|---|---|
| Poltergeist (150) | Sorpigal (3,6) | spirit | two weak attacks a turn; Sleep does not affect it | `encounter_poltergeists`, `combat_round`, `combat_sleep_immune` |
| Goblin, Guardsman, Gnome (50-125) | Sorpigal (3,6) | humanoids | Guardsmen with Gnomes can be bribed with food | `encounter_goblins`, `encounter_guardsmen`, `encounter_bribe_demand` |
| Rabid Jackal, Vampire Bat (50-125) | Sorpigal (3,6) | beasts | first fights | `bash_after` |
| Skeleton, Fire Ant, Snake (50-125) | cavern below Sorpigal | undead, insect, reptile | Skeletons fall to Turn Undead | `cave_skeletons`, `cave_fire_ants`, `cave_snakes`, `combat_turn_undead` |
| Strangling Vine (100) | sector C-2 | plant | groups of nine | `outdoors_vines` |
| Unicorn (500) | the Arena | horse | two at once, no options | `cave_arena_fight` |
| Caryatid Guard, Cyclops (400) | cavern 2 | statue, giant | four of a kind | `battle_caryatids`, `battle_cyclops` |
| Alien (1000) | cavern 6 | oddity | four of a kind | `battle_alien` |
| Medusa (1000) | cavern 9 | gaze | turns a character to stone | `battle_medusas`, `combat_stoned` |
| Mummy, Vampire, Banshee (2000-5000) | Dusk's north wall | undead | groups of six to eleven inside a town | `battle_mummies`, `dusk_vampires`, `dusk_banshees` |
| Centaur, Satyr, Celestial Stag (200-700) | Quivering Forest | woodland | large mixed group | `battle_centaurs` |
| Dinobeetle (6000) | Quivering Forest | giant insect | eight at once | `battle_dinobeetles` |
| Hydras: Pyro, 8 and 12 Headed (2000-12000) | Quivering Forest | hydra | mixed with Man Eating Mares | `qvl_hydras` |
| Hippogriff, Harpy (200) | Quivering Forest 2 | winged | twelve in a group | `battle_hippogriffs` |
| Giants: Cave, Frost, Stone, Storm (2000-10000) | Raven's Wood 2 | giant | four kinds in one group | `battle_giants` |
| Cockatrice, Pegasus (250-500) | Enchanted Forest | winged beasts | with Strangling Vines | `battle_cockatrices` |
| Werewolf, Werebear (400-800) | Enchanted Forest 2 | were-creatures | ten in a group | `battle_werewolves` |
| Rabid Leper, Rotting Corpse, Zombie, Cleric (100-300) | below Dragadune | undead and their priest | thirteen in a group | `battle_lepers` |
| Earth and Air Elemental (4000) | below Dragadune 3 | elemental | - | `battle_elementals` |
| White Dragon with Warriors and a Wizard (10000) | below Dragadune 3 | dragon | mixed with humans | `battle_white_dragons` |
| Giant Scorpion (600) | PP level 1 | scorpion | twelve at once | `battle_scorpions` |
| Magician (600) | PP level 1 | spell caster | thirteen casting Lightning Bolt, 10-41 points | `battle_magicians`, `combat_magicians` |
| Red Dragon (15000) | sector A-2 | dragon | breath: 83 points to each character, half to some | `battle_red_dragons`, `combat_dragon_breath`, `combat_dies` |
| Assassins with a Black Knight (2000, 10000) | sector B-2 | humans, **named leader** | - | `battle_assassins` |
| **Okrim** (20000) with Wizards and a Brontasaurus | Quivering Forest (12,12) | wizard, boss | - | `qvl_okrim` |
| **Lich** (20000) with five Mummies | sector B-2 (2,1) | undead, boss | Disintegration eradicates a character before the party moves | `boss_lich`, `boss_lich_eradicates` |
| **Demon Lord** (60000) with Greater, Lesser and Minor Demons | cavern 3 (8,7) | demon, boss | eradicates with a blow; Greater Demons drain abilities | `boss_demon_lord`, `boss_demon_drain`, `boss_demon_drains` |
| **Gray Minotaur** (15000) with twelve Minotaurs | Enchanted Forest 2 (8,14) | minotaur, boss (the statue in Sorpigal speaks of it) | - | `boss_gray_minotaur`, `statue_minotaur` |
| Evil Eye, Lava Beast, Naga (4000-5000) | below Dragadune 3 | eye, blob, serpent | the Naga's Paralyze stops four characters | `boss_evil_eyes`, `combat_paralyzed`, `combat_lava_beast`, `combat_conditions` |
| **Scorpion** (12000) with Giant Scorpions | sector D-1 (10,5) | scorpion, boss | attacks without options | `boss_scorpion` |
| **Dark Rider** (12000) with eleven Warriors | sector A-1 (5,2) | knight, boss | a duel the party may refuse | `a1_dark_rider`, `boss_dark_rider` |

## 4. Items and equipment
A spread over types and tiers; the special ones marked.

| Item | Type | Got from | What it does | Shots |
|---|---|---|---|---|
| Club | weapon, the starting one | every new character | sells for 0 | `profile_menu`, `shop_sell` |
| Dagger, Hand Axe, Short Sword, Sling, Crossbow, Staff | weapons, 5-50 gold | Sorpigal blacksmith | class limits marked "-" | `shop_weapons`, `shop_cant_use` |
| Spear, Mace, Scimitar, Short Bow, Glaive, Bardiche | weapons, 15-80 gold | Portsmith blacksmith | a second tier | `portsmith_weapons` |
| Small Shield to Chain Mail | armor, 10-200 gold | Sorpigal blacksmith | Short Sword and Leather Armor: armor class 1 to 3 | `shop_armor`, `profile_ryz`, `remove_done` |
| Large Shield, Ring Mail | armor | Portsmith blacksmith | - | `portsmith_armor` |
| Chain Mail on a Sorcerer | armor | - | refused: wrong class | `equip_wrong_class` |
| Torch, Rope & Hooks, Garlic | tools, 2-10 gold | Sorpigal blacksmith | - | `shop_misc` |
| Magic Herbs | charged item, 50 gold, 3 charges | Sorpigal blacksmith | heals 8 hit points | `use_herbs_target`, `use_herbs_done`, `detect_magic` |
| Might Potion | charged item, 200 gold, 3 charges | Sorpigal blacksmith | Might +5 | `use_might_potion`, `detect_magic` |
| 10 Foot Pole, Smelling Salt, Curing Potion, Antidote Brew | tools and cures, 10-500 gold | Portsmith blacksmith | - | `portsmith_misc` |
| Undead Amulet | **magic item** | gold chest in Dusk | not tried | `chest_opened` |
| Gems | currency for travel and spells | chests | 200 in one chest | `chest_opened`, `leprechaun_algary` |
| Key Card, Eye of Goros | **quest items** | not found | the Astral door asks for the card; the true king names the eye | `astral_door`, `doom_true_king` |

## 5. Abilities and spells
| Ability | Who | Cost | What it does | Shots |
|---|---|---|---|---|
| Flame Arrow (Sorcerer 1-4) | MNZ | 1 point | 5 points to one monster | `combat_cast`, `combat_spell_hit` |
| Leather Skin (1-5), Light (1-6) | MNZ | 1 point each | party spells listed under Protect; Light shows dark areas | `cast_prompt`, `protect_active`, `protect_three`, `dungeon_lit` |
| Location (1-7) | MNZ | 1 point | sector and coordinates | `location_spell` |
| Detect Magic (1-2) | MNZ | 1 point | magic and charges of carried items | `detect_magic` |
| Sleep (1-8) | MNZ | 1 point | no effect on a Poltergeist | `combat_sleep_immune` |
| First Aid (Cleric 1-4) | DEDDO | 1 point | +8 hit points | `cast_on_whom`, `cast_done`, `cast_healed` |
| Bless (1-2) | DEDDO | 1 point | "DONE" (effect not measured) | `combat_bless` |
| Protection from Fear (1-7) | DEDDO | 1 point | "+ 21%" under Protect | `protect_three` |
| Turn Undead (1-8) | DEDDO | 1 point | destroyed two of four Skeletons | `combat_turn_undead` |
| Unlock (Robber skill) | CUBI | - | opens a lock without the trap | `unlock_success` |
| Monster spells: Lightning Bolt, Paralyze, Disintegration; breath and gaze | Magician, Naga, Lich, Red Dragon, Medusa | - | damage, paralysis, eradication, fire, stone | `combat_magicians`, `combat_paralyzed`, `boss_lich_eradicates`, `combat_dragon_breath`, `combat_stoned` |

## 6. Characters and people
| Who | Role | Where | Shots |
|---|---|---|---|
| Knight, Paladin, Archer, Robber, Cleric, Sorcerer | the six classes (RYZ, CONDI, EBO, CUBI, DEDDO, MNZ) | the party | `roster_view_all`, `profile_ryz`, `quickref`, `gather_done`, `trade_food_done`, `equip_wrong_class`, `cast_done` |
| Human, Elf, Dwarf, Gnome, Half-Orc | the five races | creation | `create_race` |
| Innkeepers | save points with a face each: Lara, a half-orc, a ghost, a gnome | the five inns | `save_inn_prompt`, `portsmith_inn`, `algary_inn`, `dusk_inn`, `erliquin_inn` |
| Blacksmiths | shops | Sorpigal, Portsmith | `shop_blacksmith_prompt`, `portsmith_blacksmith` |
| Trainers | level-ups: Worg, empty suits of armor, three knights | Sorpigal, Dusk, Erliquin | `train_level2`, `dusk_training`, `erliquin_training` |
| Leprechaun | travel for a gem | Sorpigal | `leprechaun` |
| Old courier master, Zam | the courier errand | cavern 1, Portsmith | `cave_courier`, `portsmith_zam` |
| Morango the Mystic, the gypsy seer, Agar | fortune tellers and a wizard | Algary, sector C-2, Erliquin | `algary_mystic`, `outdoors_gypsy`, `erliquin_agar` |
| Lord Ironfist | quest giver | Castle White Wolf | `whitewolf_ironfist`, `whitewolf_quest` |
| King Alamar, his guards and prisoner | the throne room | Castle Alamar | `alamar_king`, `alamar_guards`, `alamar_prisoner` |
| The true King Alamar | prisoner who reveals the plot | Castle Doom | `doom_true_king` |
| The Dark Rider | challenger | sector A-1 | `a1_dark_rider` |
| The Data Keeper | the ending | Inner Sanctum | `ending_panel`, `ending_sanctum` |
| People remembered on statues: Corak, Gala, the wizard Ranalou, the seer Og | lore | Sorpigal | `statue_archer`, `statue_cleric`, `statue_wizard`, `statue_paladin`, `statue_knight`, `statue_robber`, `statue_lore`, `statue_prompt` |

## Open questions
- Sea monsters (Shark, Sea Serpent, Great Sea Beast and others are in the table) were not met: no fixed fight
  on a water square was found by the survey; they may need a boat or random encounters at sea.
- Named monsters in the table not located: Volcano God, Demon King, Succubus Queen, Paul Pead, Lord Archer,
  Pirate Captain, Winged Beast, Tyrannosaurus.
- Magic weapons and armor (the table goes up to items such as Ultimate Sword and Holy Plate) were not seen in
  play; no chest besides the one in Dusk was opened.
- Spells above level 1 need a higher-level party.
