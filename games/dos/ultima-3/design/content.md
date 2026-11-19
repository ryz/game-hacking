# Ultima III: Exodus (DOS) - content (variety lens)

What the game is filled with: its places, opponents, things and people, shown as a reasonable variety rather
than a full list. Read it to see the range of what a player meets. The rules behind the content are in
[systems.md](systems.md) and [rules.md](rules.md), the screens it appears on in [interface.md](interface.md);
the same shots appear there, overlap is intended. Notation: [README.md](README.md). Check:
`python3 tools/lenses.py dos/ultima-3`.

## 1. Kinds of content
| Kind | In the game (count if known) | Shown here | Full list |
|---|---|---|---|
| Environments | Sosaria (64x64), 10 townes, 2 castles, 7 dungeons of 8 levels, Ambrosia, 9 combat fields **(code)** | every place | ../playbook.md Game structure |
| Opponents | 13 kinds roam Sosaria (land and sea), guards, Lord British, Floors, Exodus; 16 alternate names **(code, ROM text)** | 19 fights | section 3 |
| Items | gold, food, gems, keys, powders, torches, 4 cards, 4 marks **(ROM text)** | all | section 4 |
| Equipment | 15 weapons + Exotic, 7 armours + Exotic **(ROM text)** | all, with prices | section 4 |
| Abilities / spells | 16 cleric and 16 wizard spells (one unnamed) **(ROM text, code)** | 15 cast | rules.md 2 |
| Characters and people | 5 races, 11 classes; Lord British, the Time Lord, Radrion, named townsfolk **(ROM text)** | all | section 6 |
| Vehicles | horse, frigate **(code)** | both | section 5 |
| Talk lines | about 70 lines in 12 places **(ROM text)** | 27 | section 7 |

## 2. Environments
| Environment | Where | What sets it apart | Shots |
|---|---|---|---|
| Sosaria: grass, brush, forest, mountains, sea | the world map **(verified)** | the party icon, castles and townes as pictures, monsters and ships walking | `gameplay_start`, `gameplay_horse`, `gameplay_monster_map` |
| The Dark Forest | (25,36) **(verified)** | trees close the view | `gameplay_dark_forest` |
| LCB | (2E,13) **(verified)** | the pond with its LCB sign, guards, jesters, the Pub | `gameplay_towne_lcb`, `dialogue_lcb_13` |
| Lord British's castle | (2D,12) **(verified)** | moat of trees, the BRITISH sign over the throne, the healer and the oracle | `gameplay_castle`, `dialogue_lb_experience` |
| Moon | (06,0D) **(verified)** | the Blue Boar tavern | `gameplay_moon`, `dialogue_moon_4` |
| Yew | (22,10) **(verified)** | the clerics' Rogation and Worships, the Circle of Light | `gameplay_yew`, `gameplay_yew_circle`, `system_pray` |
| Montor East / West | (31,3A) / (2F,3A) **(verified)** | Acme Weaponry; the Prison | `gameplay_montor_east`, `gameplay_montor_west` |
| Grey | (07,2C) **(verified)** | the thieves' towne: Taphouse, the Guild, the only chest behind a counter | `gameplay_grey`, `system_steal` |
| Devil Guard | (12,1F) **(verified)** | The Stables with horses | `gameplay_devil_guard`, `shop_horses` |
| Fawn | (1E,02) **(verified)** | City of the sea, Tools of Trade | `gameplay_fawn` |
| Death Gulch | (38,1F) **(verified)** | gates held by guards, the Draught or Spot tavern | `gameplay_death_gulch`, `system_unlock` |
| Dawn | (25,35), only at new moons **(verified)** | the magic arms, every kind of shop | `system_dawn_appears`, `gameplay_dawn` |
| Dungeons | 7, 8 levels each **(verified)** | wireframe corridors, fountains, rods | `gameplay_dungeon_l2`, `gameplay_dungeon_l8`, `system_fountain` |
| The Time dungeon | (3A,1E), walled in **(verified)** | reached only by moongate; the Time Lord | `system_moongate_through`, `cutscene_timelord` |
| Ambrosia | through the whirlpool **(verified)** | the AMBROSIA sign, four shrines, guardians | `gameplay_ambrosia_sign`, `gameplay_ambrosia_guardian`, `system_shrine` |
| The Silver Snake and the Isle of Fire | (0A,39), (0A,35) **(verified)** | a serpent filling the strait, the castle in its moat | `gameplay_silver_snake`, `gameplay_isle_of_fire` |
| Castle Exodus | (0A,35) **(verified)** | lava, force fields, the DEATH signs, the slots | `gameplay_exodus_gate`, `gameplay_exodus_hall`, `gameplay_exodus_death`, `boss_exodus` |
| Combat fields | 9 **(code, verified)** | grass, brush, forest, stone, shore, decks | rules.md 1.1 |

## 3. Opponents
| Opponent | Where met | Family / picture | What it does | Shots |
|---|---|---|---|---|
| Orcs (Goblins below ground) | grass, dungeons **(verified)** | humanoid | bands of up to 8; 3 experience each | `battle_start`, `battle_dungeon_goblins` |
| Thieves (Cutpurses) | brush **(verified)** | people | pilfer an item on a hit | `battle_cutpurses`, `battle_thieves_pilfer` |
| Skeletons (Zombies) | forest **(verified)** | undead | the cleric spell Pontori destroys them (half the time, once a fight) | `battle_zombies` |
| Giants | grass **(verified)** | large humanoid | hard hitters | `battle_giants` |
| Daemons | brush **(verified)** | winged | - | `battle_daemons`, `dialogue_exodus_0` |
| Balrons (Devils) | brush, Castle Exodus **(verified)** | winged, larger | poison | `battle_devils`, `gameplay_exodus_hall` |
| Pinchers (Snatches) | grass **(verified)** | crab-like | poison on a hit; 10 experience | `battle_snatches_poison`, `battle_member_killed` |
| Wizards | brush **(verified)** | robed people | - | `battle_wizards` |
| Dragons (Wyverns) | land beside the sea **(verified)** | winged reptiles | attack a frigate from the shore | `gameplay_monster_map`, `battle_wyverns_ship` |
| Sea serpents | the sea **(verified)** | serpent | attack the frigate | `gameplay_serpent_sea`, `battle_serpents` |
| Man-o-wars | the sea by the shore **(verified)** | jellyfish | poison | `battle_manowars` |
| Pirates | the sea **(verified)** | ships | cannons; boarded, their ship becomes the party's | `battle_pirates_fire`, `battle_pirates_board`, `battle_pirates_victory`, `battle_pirates_shore` |
| Guards | townes **(verified)** | armoured people | fight when attacked, bribed with 100 gold | `battle_guards`, `system_bribe` |
| Lord British | his throne room **(verified)** | the king | fights when attacked | `battle_lord_british` |
| The Silver Snake | the strait at (0A,39) **(verified)** | fixed serpent | blocks the way until EVOCARE | `gameplay_silver_snake` |
| Floors | before Exodus **(verified)** | invisible on the field | attack near the slots | `boss_floors` |
| Exodus | Castle Exodus **(verified)** | a machine of four slots | ended by the four cards | `boss_exodus` |

## 4. Items and equipment
| Item | Type | Got from | What it does | Shots |
|---|---|---|---|---|
| Dagger 5, Mace 30, Sling 60, Axe 125, Bow 350, Sword 200, 2H Sword 250 | weapons | weapon shops **(verified)** | ready with R | `shop_weapons`, `shop_weapons_buy` |
| +2 Axe 400, +2 Bow 1050, +2 Sword 800, Gloves 1200, +4 Axe 2700, +4 Bow 6550, +4 Sword 4550 | magic weapons | Dawn **(verified)** | - | `shop_weapons_dawn` |
| Exotic weapon and armour | the best | DIG on two islets **(verified)** | "Exotic clues found at Dawn!" (Grey) | `system_dig_weapon`, `system_dig_armour`, `dialogue_grey_24` |
| Cloth 75, Leather 195, Chain 575, Plate 2500, +2 Chain 6130, +2 Plate 8250 | armour | armour shops **(verified)** | wear with W | `shop_armour`, `shop_armour_buy`, `shop_armour_dawn` |
| Torches 6, keys 50, powders 90, gems 75 | tools | the Guild **(verified)** | light, unlock, negate time, peer | `shop_guild`, `shop_guild_buy` |
| Food | rations | grocers, 1 gold each **(verified)** | eaten as the party moves | `shop_grocer`, `shop_grocer_poor` |
| Cards of Love, Sol, Moons, Death | quest items | SEARCH on Ambrosia's shrines **(verified)** | inserted into Exodus | `system_card_sol`, `system_card_death`, `inventory_ztats_marks` |
| Marks of Force, Fire, Snake, Kings | brands | rods in dungeons **(verified)** | fields, lava, EVOCARE, levels past five | `system_rod_mark`, `inventory_ztats_marks` |
| Chest loot | gold, arms, armour | chests **(verified)** | - | `system_chest_weapon`, `system_chest_armour` |

## 5. Vehicles
| Vehicle | Got from | Shots |
|---|---|---|
| Horses | the stables of Devil Guard and Dawn, 800 gold for four **(verified)** | `shop_horses_buy`, `shop_horses_no`, `gameplay_horse` |
| Frigate | taken from pirates **(verified)** | `system_frigate_taken`, `gameplay_frigate` |

## 6. Characters and people
| Who | Role | Where | Shots |
|---|---|---|---|
| Races Human, Elf, Dwarf, Bobbit, Fuzzy; classes Fighter, Cleric, Wizard, Thief, Paladin, Lark, Barbarian, Druid, Illusionist, Alchemist, Ranger **(verified in the form)** | playable | creation | `menu_create_done`, `menu_create_fuzzy` |
| ryz (Human Paladin), condi (Elf Wizard), ebo (Dwarf Fighter), cubi (Bobbit Cleric) | the party here | - | `menu_register`, `menu_look` |
| Lord British | king, raises maximum hit points | his throne (20,0E) **(verified)** | `dialogue_lb_greater` |
| The Time Lord | gives the card order | Time dungeon level 8 **(verified)** | `cutscene_timelord` |
| Radrion, Prophet of Life | oracle, a rhyme for gold | oracle counters **(verified)** | `shop_oracle`, `shop_oracle_2` |
| Named townsfolk: Dupre, Gwino, Iolo, Cookie, Chuckles, the Wise Cleric, the Phantom Fighter, Baby Bob, Jolly Joe, Sentri, Shamino **(ROM text)** | color and hints | LCB, the castle, Montor East and West | `dialogue_lcb_13`, `dialogue_british_23`, `dialogue_british_20`, `dialogue_montor_e_28` |

## 7. Talk lines (the 27 shot, by place)
| Place | Lines shown | Shots |
|---|---|---|
| LCB | "Quest ye unto Lost Ambrosia!", "Exodus lies beyond the Silver Snake!", "`Dawn' comes each new pair!", "Dupre laughs: Drink up!" | `dialogue_lcb_9`, `dialogue_lcb_11`, `dialogue_lcb_12`, `dialogue_lcb_13` |
| Lord British's castle | "The Wise Cleric: 4 cards, 4 slots", "Phantom Fighter: The food stinks!", "Gwino sings: Muh eh oye oh!" | `dialogue_british_19`, `dialogue_british_20`, `dialogue_british_23` |
| Moon | "Seek ye the Shrines of Truth", "<Bribe> guards! They will leave!", "I've been beyond the whirlpool!", "Dawn rises in the Dark Forest." | `dialogue_moon_1`, `dialogue_moon_4`, `dialogue_moon_14`, `dialogue_moon_19` |
| Yew | "Search and ye shall find!" | `dialogue_yew_0` |
| Montor East / West | "<Insert> cards into pannels!", "Baby Bob: Bring me bucks!"; "None shall pass!" | `dialogue_montor_e_25`, `dialogue_montor_e_28`, `dialogue_montor_w_31` |
| Grey | "Exotic clues found at Dawn!", "Don't you wish you were a Jester!" | `dialogue_grey_24`, `dialogue_grey_26` |
| Devil Guard | "Hot metal leaves a `Mark'!", "A `Mark' helps invoke the Snake", "4 `Marks', 4 uses!" | `dialogue_devil_1`, `dialogue_devil_3`, `dialogue_devil_4` |
| Fawn | "<Pray> in the Circle of Light!", "`Invoke' the Silver Snake!", "To pass you need a Mark!" | `dialogue_fawn_1`, `dialogue_fawn_2`, `dialogue_fawn_3` |
| Death Gulch | "<Bribe> me to enter" | `dialogue_death_1` |
| Dawn | "<Dig> up Exotics", "Ambrosia awaits!" | `dialogue_dawn_19`, `dialogue_dawn_30` |
| Castle Exodus | "All may enter, None shall leave" | `dialogue_exodus_0` |
Every line of every place is listed by `tools/u3town.py FILE.ULT` **(ROM text)**.

## Open questions
- Which monster appears on which dungeon level; the alternate-name rule.
