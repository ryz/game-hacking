# Wizardry II: The Knight of Diamonds (DOS) - content (variety lens)

What the game is filled with: its places, opponents, things and people, shown as a reasonable variety rather
than a full list. Read it to see the range of what a player meets. The rules behind the content are in
[systems.md](systems.md), the screens it appears on in [interface.md](interface.md); the same shots appear
there, overlap is intended. Notation: [README.md](README.md). Check: `python3 tools/lenses.py dos/wizardry-2`.

## 1. Kinds of content
| Kind | In the game (count if known) | Shown here | Full list |
|---|---|---|---|
| Environments | 6 floors of 20 x 20 plus the Castle menus (verified: disk data) | corridors, doors, darkness, rock floors, traps, message rooms, Gnilda's temple | [maps](maps/floors.txt) |
| Opponents | groups from a per-floor table, up to four kinds at once; 5 guardians (verified) | 30 kinds below | not decoded (names are packed on the disk) |
| Items | 129 (verified) | Boltac's 25, the regalia, the staff, chest finds | [items.md](items.md) |
| Abilities / spells | Wizardry I's 21 mage and 29 priest spells (verified: books) | Badios, Halito, Lahalito, Tiltowait, Dios, Dumapic, Malor; enemy Katino, Dilto, Mahalito, Lahalito | [Wizardry I](../../wizardry/design/content.md) |
| Characters and people | 6 stock veterans, the imported party, the sphinx, Gnilda's apparition, the sage, the shouting figure (verified) | below | - |
| Riddles and clues | 2 riddles, about 20 message squares (verified) | all that were reached | [maps](maps/floors.txt) |

## 2. Environments
Every floor is drawn in the same white wireframe: a corridor on floor 4 or 6 can be pixel for pixel the
entrance view of floor 1 (verified: the capture dropped two such views as duplicates); what tells the floors
apart is darkness, traps, messages and the monsters.

| Environment | Where | What sets it apart | Shots |
|---|---|---|---|
| The Castle "Llylgamyn" | town | menus only, the party list always shown | `menu_castle`, `menu_castle_geared` |
| Floor 1 | under the temple | the entrance under the stairs up, 98 dark squares, the Magic Armor before the stairs down, Gnilda's temple at (9,10) | `gameplay_maze_f1_start`, `gameplay_dark`, `gameplay_stairs_down`, `dialogue_gnilda` |
| Floor 2 | second | mostly dark (172 squares), teleports, the riddle before the Magic Shield, the sage's study | `gameplay_door`, `dialogue_f2_riddle`, `dialogue_f2_sage_study` |
| Floor 3 | third | rooms, a pit with a waiting group, the Magic Sword's corner | `battle_f3_orcs`, `boss_magic_sword` |
| Floor 4 | fourth | corridors cut through 177 squares of rock, ouch squares, the cavern and its fountain | `gameplay_ouch`, `dialogue_f4_cavern`, `dialogue_f4_fountain` |
| Floor 5 | fifth | dark maze, four chutes down to floor 6, the wishing well | `gameplay_chute`, `dialogue_f5_well` |
| Floor 6 | deepest | dark rooms, spinners, the sphinx's door, the king's clues, demons and dragons | `dialogue_sphinx`, `battle_f6_arch_demon` |
| Traps | all floors | pits, ouch squares, chutes | `gameplay_pit`, `gameplay_pit_damage`, `gameplay_ouch`, `gameplay_chute` |
| Gnilda's temple | floor 1 (9,10), reached from floor 6 by teleport | the apparition, the test | `gameplay_teleport_temple`, `dialogue_gnilda_test` |

## 3. Opponents
| Opponent | Where met | Family / picture | What it does | Shots |
|---|---|---|---|---|
| Large animals | floor 1 | beast | strike first, poison | `battle_f1_large_animals` |
| Dogs | floor 1 | beast | groups of 4 | `battle_f1_dogs` |
| Men in armor | floor 1 | human fighter | groups of 5 | `battle_f1_men_in_armor` |
| Fuzzballs | floors 1-2 | round furry creature | often friendly | `battle_f1_fuzzballs`, `battle_friendly` |
| Ogre lords | floors 2-3, 5 | giant | Halito, Katino, Dilto | `battle_f2_ogre_lords`, `battle_enemy_katino`, `battle_enemy_dilto` |
| Lvl 7 thieves | floor 2 | human | groups of 4 | `battle_f2_thieves` |
| Rhino beetles | floor 2 | insect | chew for 14-23, leave a chest | `battle_f2_rhino_beetles`, `battle_monster_hit` |
| Priests | floor 2 | robed human | groups of 4 | `battle_f2_priests` |
| Men in leather | floor 2 | human | groups of 3 | `battle_f2_men_in_leather` |
| Animals | floor 2 (alarm) | beast | answer a chest's alarm | `battle_surprised_monsters` |
| Orcs | floor 3 | humanoid | groups of 4 | `battle_f3_orcs` |
| Nightstalkers (gaunt figures) | floor 3 | undead | drain levels | `battle_level_drain`, `battle_f3_nightstalkers` |
| Cave dwellers | floor 4 | humanoid | groups of 8 | `battle_f4_cave_dwellers` |
| Corrosive slimes | floor 4 | slime | poison | `battle_f4_slimes` |
| Scrylls, frogs, nightstalkers, ogre lords | floor 5 | four groups at once | - | `battle_f5_four_groups` |
| Fire dragon, orc lord, lesser demons | floor 6 | dragon, demons | - | `battle_f6_fire_dragon` |
| Arch demon, demonic figures | floor 6 | demons | - | `battle_f6_arch_demon` |
| Men in robes, hatamoto | floor 6 | samurai, mages | slice at the front rank | `battle_f6_men_in_robes`, `battle_f6_hatamoto` |
| Dragon zombies, strange animal, master ninjas, mages | floor 6 | four groups | - | `battle_f6_four_groups` |
| Magic Armor (guardian) | floor 1 (15,2) | animated armour | 305 hit points, regenerates, resists spells (RAM) | `boss_magic_armor`, `boss_armor_killed` |
| Magic Shield (guardian) | floor 2 (2,6) | animated shield | claws for 64, nibbles EBO to death | `boss_magic_shield`, `boss_shield_ebo_killed` |
| Magic Sword (guardian) | floor 3 (14,13) | animated sword | decapitates | `boss_magic_sword`, `boss_sword_decapitated` |
| Magic Helm (guardian) | floor 4 (10,4) | animated helm | casts Lahalito | `boss_magic_helm`, `boss_helm_lahalito` |
| Magic Gauntlets (guardians) | floor 5 (10,9) | two animated gauntlets | cast Mahalito | `boss_magic_gauntlets`, `boss_gauntlet_mahalito` |

## 4. Items and equipment
| Item | Type | Got from | What it does | Shots |
|---|---|---|---|---|
| Long sword 25 ... dagger 5 | basic weapons | Boltac's | - | `shop_boltac_buy`, `shop_bought` |
| Shields, robes, leather, chain, breast plate, plate mail 750, helm 100 | basic armour | Boltac's | AC | `shop_boltac_armor`, `shop_boltac_potions` |
| Potions of Dios and Latumofis, scrolls of Katino, Badios, Halito | consumables | Boltac's | spells in a bottle | `shop_boltac_potions`, `shop_boltac_magic`, `camp_use_item`, `battle_use_item` |
| Leather+1 ... breast plate+1 1500, staff+2 2500, gloves of copper 6000 | magic gear | Boltac's | better AC | `shop_boltac_magic`, `shop_boltac_rare`, `camp_equip_gauntlets` |
| Robe of curses | cursed armour | (poked) | cannot be removed; Boltac uncurses | `shop_uncurse`, `shop_uncursed` |
| Staff, sword (unidentified) | chest finds | the rhino beetles' chest | - | `chest_found_item` |
| Hrathnir, KOD's helm, shield, gauntlets, armor | the regalia | the five guardians | worn together AC -18 and regeneration | `boss_found_armor`, `boss_found_shield`, `boss_found_sword`, `boss_found_helm`, `boss_found_gauntlets`, `inventory_kod_set`, `inventory_bishop_identify`, `shop_identified` |
| Staff of Gnilda | quest item | Gnilda, for the five | "* Powerless *"; ends the game | `dialogue_staff_gift`, `inventory_staff`, `inventory_staff_powerless` |
| Stones (Damien, youth, mind, piety, Blarney, granite, dreamer's) | specials | not met | probably invoked (disk text) | none: not found in the fights played |

## 5. Abilities and spells
| Ability | Who | Cost | What it does | Shots |
|---|---|---|---|---|
| Badios | EBO (priest) | 1 priest point, level 1 | damage to one monster | `battle_badios` |
| Halito | MNZ (bishop) | mage level 1 | small fire damage | `battle_halito` |
| Lahalito | DEDDO, MNZ | mage level 4 | fire on a group | `battle_lahalito`, `battle_lahalito_kill` |
| Tiltowait | DEDDO (mage) | mage level 7 | damage to all; killed the Shield, Sword and Helm | `boss_shield_tiltowait`, `boss_sword_killed`, `boss_helm_killed` |
| Dios, Dumapic, Malor | camp | - | heal, position, teleport | `camp_cast_whom`, `system_dumapic`, `camp_malor` |
| Dispell | EBO (priest) | - | against undead groups | `battle_dispell_which` |
| Enemy Katino, Dilto, Lahalito, Mahalito | monsters | - | sleep, darkness, fire | `battle_enemy_katino`, `battle_enemy_dilto`, `boss_helm_lahalito`, `boss_gauntlet_mahalito` |

## 6. Characters and people
| Who | Role | Where | Shots |
|---|---|---|---|
| RYZ CONDI EBO CUBI DEDDO MNZ | the party, moved from Wizardry I | roster C-F, K, L | `menu_castle`, `inventory_sheet_import`, `ending_final_party` |
| CALEB, BOREE, ODDLER, NAUTUS, ZIL, GUYDOMAN | ready veterans (levels 12-13) | roster | `menu_tavern_stock`, `inventory_stock_caleb`, `inventory_roster` |
| The Wizardry I roster (TARKIN ... MNZ) | the source disk | Move characters | `system_move_list` |
| The sphinx | riddle keeper | floor 6 (1,2) | `dialogue_sphinx` |
| Gnilda's apparition | quest giver | floor 1 (9,10) | `dialogue_gnilda`, `dialogue_staff_gift` |
| The wizened sage | sells knowledge for 100,000 | floor 2 (18,10) | `dialogue_f2_sage` |
| A familiar figure ("MAPIRO MAHAMA DIROMAT") | sends the party home | floor 3 (8,10) | `dialogue_f3_mapiro` |
| The Knights of the City | the bearer's companions | ending | `ending_make_knight`, `ending_sheet_condi` |

## 7. Riddles and message squares
| Square | Text (short) | Shots |
|---|---|---|
| Floor 1 (11,2) | "The armor you seek, to bring to the fray, lies four steps ahead, but three steps away" | `dialogue_f1_armor_clue` |
| Floor 2 (3,17) | "Three roads to follow, only one may you take ..." | `dialogue_f2_three_roads` |
| Floor 2 (3,6) | "I am a lonely being, scarred by swords ... Tell me, what am I?" - answer SHIELD (verified) | `dialogue_f2_riddle`, `dialogue_f2_riddle_2`, `dialogue_f2_riddle_answer` |
| Floor 2 (15,19), (18,14) | "A panel slams shut behind you!" | `dialogue_f2_panel` |
| Floor 2 (18,9) | the sage's study: the stars, "several spells are not what they seem" | `dialogue_f2_sage_study`, `dialogue_f2_sage_spells` |
| Floor 3 (4,10) | "Ever considered another line of work?" | `dialogue_f3_line_of_work` |
| Floor 4 (16,8), (16,9), (17,9) | "... down the hall ...", "... as the inside of a mountain ...", "A cavern's dark ..." | `dialogue_f4_hall`, `dialogue_f4_mountain`, `dialogue_f4_cavern_sign` |
| Floor 4 (7,13), (6,17) | the cavern, a cave-in | `dialogue_f4_cavern`, `dialogue_f4_cave_in` |
| Floor 6 (13,15), (16,13) | "That king ... will no more see his treasure room", "... finds doom!" | `dialogue_f6_king_treasure`, `dialogue_f6_king_doom` |
| Floor 6 (1,2) | the sphinx's riddle - answer THE KNIGHT OF DIAMONDS | `dialogue_sphinx`, `dialogue_sphinx_answer` |
| Floor 6 (1,3) | "One alone." | `dialogue_one_alone_real` |

## Open questions
- Monster names are packed on the disk; only those met are known. The stones and what they do.
- The floor 6 fixed fight (group 47) and floor 2 (16,3) were not reached.
