# Wizardry: Proving Grounds of the Mad Overlord - content (variety lens)

What the game is filled with: its places, opponents, things and people, shown as a reasonable variety rather
than a full list. Read it to see the range of what a player meets. The rules behind the content are in
[systems.md](systems.md), the screens it appears on in [interface.md](interface.md); the same shots appear
there, overlap is intended. Notation: [README.md](README.md). Check: `python3 tools/lenses.py apple2/wizardry`.
Rows are **(verified)** by the shots they name unless a cell carries another tag.

## 1. Kinds of content
| Kind | In the game (count if known) | Shown here | Full list |
|---|---|---|---|
| Environments | the castle (text), ten maze floors of 20 x 20 **(disk data)** | the castle places, views of floors 1, 3, 6, 7 and 10, every kind of special square that shows something | [maps/floors.txt](maps/floors.txt) |
| Opponents | 101 monster records, 20 pictures **(disk data)** | about 40 groups on floors 1-4 and 7-10, 15 of the 20 pictures | `python3 ../tools/data.py monsters`; DOS [content](../../../dos/wizardry/design/content.md) |
| Items and equipment | 101 item records **(disk data)**; the DOS port's numbers with other spellings (LONG SWORD + 2, BLADE CUSINART', MURASAMA BLADE) | the whole trading post stock, the veterans' gear, the inherited characters' rare items | `python3 ../tools/data.py items`; DOS [items](../../../dos/wizardry/design/items.md) |
| Abilities / spells | 21 mage and 29 priest spells in 7 levels | both books; eleven spells cast | DOS content |
| Characters and people | 5 races, 3 alignments, 8 classes; Trebor, Werdna, Boltac, Gilgamesh, the Temple of Cant | all eight classes on sheets | - |
| Messages of the maze | about 40 message squares **(disk data)** | 27 pages from floors 1, 2, 3, 4 and 10 | [maps/floors.txt](maps/floors.txt) |

## 2. Environments
| Environment | Where | What sets it apart | Shots |
|---|---|---|---|
| Opening | power-on | the only full-colour drawing outside the monster pictures | `boot_prepare`, `title_cauldron`, `title_smoke`, `title_logo` |
| Castle | all menus | framed text header naming the place | `menu_castle`, `menu_tavern`, `menu_inn`, `menu_temple`, `shop_boltac`, `menu_edge`, `menu_training` |
| Corridor wireframe | every floor | purple outlines, side openings | `gameplay_maze_f1_start`, `gameplay_f3_crossing`, `gameplay_f7_hall`, `gameplay_after_werdna` |
| Doors | every floor | an inner frame in a wall; passed only by K)ick | `gameplay_door`, `gameplay_f6_doors` |
| Darkness | floor 1 column x 9-10 and others | the view stays empty | `gameplay_dark` |
| Stairs | every floor to 8 | a Y/N prompt on the square | `gameplay_stairs`, `gameplay_stairs_down`, `gameplay_stairs_amulet` |
| Elevators | floors 1-4 at (10,8), floor 2 at (10,9); floors 4-9 at (10,0) | button prompt A-D or A-F | `gameplay_elevator`, `gameplay_elevator_f2`, `gameplay_elevator_f4`, `system_dumapic_f4` |
| Pits and the chute | floor 3 and others; floor 9 (8,2) | a one-line message, then damage or the next floor | `gameplay_pit`, `gameplay_chute` |
| Anti-magic squares | floor 5 and 7 | spells fail | `system_fizzle` |
| Statues and scenes of floors 1-2 | floor 1 (13,3), (13,5), (9,19); floor 2 (9,18), (12,4), (8,7), (8,12), (14,11), (4,11) | paged descriptions; two guard a key item, two throw the party out | `dialogue_f1_chicken`, `dialogue_f1_altar`, `dialogue_f1_mapiro`, `dialogue_f2_bear`, `system_search`, `system_search_found`, `dialogue_f2_frog`, `dialogue_f2_bronze_smoke`, `dialogue_f2_silver_fog`, `dialogue_f2_silver_fog_flee`, `dialogue_f2_placard`, `dialogue_f2_door`, `dialogue_sign_f1` |
| Floor 3's mosaics | floor 3 crossings | "TURN LEFT." hints among pits and spinners | `dialogue_f3_mosaic` |
| The Testing Grounds Control Center | floor 4 (8-12, 10-15) | door signs, an alarm, guard rooms, the desk room, the private elevator | `dialogue_f4_control`, `dialogue_f4_alarm`, `dialogue_f4_alarm_guardians`, `dialogue_f4_treasure`, `dialogue_f4_allocation`, `dialogue_f4_desk`, `dialogue_f4_private`, `dialogue_f4_asleep`, `dialogue_f4_asleep_outside`, `dialogue_f4_bear_wall`, `battle_f4_fixed` |
| Werdna's floor | floor 10 | a chain of rooms joined by teleporters, taunting messages, the lair | `dialogue_f10_plaque`, `dialogue_f10_plaque_2`, `dialogue_f10_plaque_3`, `dialogue_f10_guardians`, `dialogue_werdna_sign`, `boss_werdna` |
| Cemetery | after a wiped party | tombstones in place of the maze screen | `gameover_cemetery` |

## 3. Opponents
The name in quotes is what the group is called before it is identified. Pictures are shared by families.

| Opponent | Where met | Family / picture | What it does | Shots |
|---|---|---|---|---|
| Bubbly slime ("SLIMES") | floor 1 | green blob | 27 experience points for three; dies to one hit | `battle_slimes`, `battle_f1_bubbly_slimes`, `battle_kill` |
| Kobold, Orc ("SMALL HUMANOIDS") | floor 1 | humanoid with a shield | come in fives, also beside slimes | `battle_f1_small_humanoids`, `battle_f1_kobolds`, `battle_f1_two_groups`, `battle_group_select` |
| Undead kobold ("SKELETONS") | floor 1 | skeleton | - | `battle_f1_skeletons`, `battle_f1_undead_kobolds` |
| Rogue ("SCRUFFY MEN") | floor 1 | running man in a blue cap | - | `battle_f1_scruffy_men` |
| Gas cloud | floor 2 (8,7) | orange cloud with eyes | surprises, casts weak damage and sleep, may flee | `battle_surprised`, `battle_flees`, `battle_gas_spell`, `battle_not_slept`, `battle_encounter` |
| Lvl 1 priest ("PRIESTS") | floor 2 (8,12) | blue-robed priest with a mace | - | `battle_f2_priests` |
| Spirit | floor 3 | pale humanoid, arms spread | alone, in fours, or friendly | `battle_f3_spirit`, `battle_friendly` |
| Killer wolves with a Dragon puppy | floor 3 | spotted four-legged animal | - | `battle_f3_wolves` |
| Priests with Lvl 4 thieves | floor 3 | running man in a blue cap | hostile or friendly | `battle_f3_priests_thieves`, `battle_friendly_thieves` |
| Gargoyles with Unseen entities | floor 3 | pale humanoid | - | `battle_f3_gargoyles` |
| Dragon fly | floor 3 (13,17) | winged insect | breathes on the whole party for 4-7 each; one of four slept by KATINO | `battle_f3_dragon_flies`, `battle_breath`, `battle_katino`, `battle_mahalito`, `battle_unaffected`, `battle_multi_hit`, `battle_round2` |
| Animals and Men in armor | floor 4 guard room | armoured man with sword and shield | two groups, five and three | `battle_f4_fixed` |
| Lvl 6 ninja with Priests | floor 7 | priest picture | - | `battle_f7_ninjas` |
| Medusalizard, Weretiger | floor 7 | spotted four-legged animal | - | `battle_f7_medusalizards`, `battle_f7_weretigers` |
| Champ samurai, Major daimyo, High priests | floor 7 | swordsman with a curved blade; priest; wizard | up to four groups; the daimyos were friendly | `battle_f7_champ_samurai`, `battle_f7_four_groups`, `battle_f7_friendly_daimyos` |
| Lesser demon, Ogre lords, Lvl 8 ninja, Unseen entities | floor 8 | horned demon face | four groups at once; the demon shrugged off TILTOWAIT | `battle_f8_demon`, `battle_spell_group`, `battle_demon_stab`, `battle_malikto`, `battle_malikto_ninja`, `battle_tiltowait`, `battle_demon_unaffected`, `battle_demon_alone` |
| Men in armor (two pictures) | floor 8 | sword-and-shield man; swordsman with a curved blade | - | `battle_f8_men_in_armor`, `battle_f8_samurai` |
| Priest with a Strange animal | floor 8 | priest | - | `battle_f8_priest_animal` |
| Master thief | floor 8 | running man in a blue cap | - | `battle_f8_master_thieves` |
| Arch mage | floor 8 | green-robed wizard, arms raised | casts for 3-7 damage a member | `battle_f8_arch_mages`, `battle_enemy_spell` |
| Troll | floor 8 | red-shirted giant | - | `battle_f8_trolls` |
| "Strange animal" with the giant's picture | floor 9 | red-shirted giant | - | `battle_f9_strange_animal` |
| Gaze hound and other "Strange animals" | floor 9 | spotted four-legged animal | bites poison; outruns a fleeing party most of the time | `battle_f9_gaze_hounds`, `battle_f9_strange_animals`, `battle_poisoned`, `battle_run_failed`, `battle_run`, `battle_use_item`, `battle_potion` |
| Wyverns, Men in robes, Unseen entities | floor 9 | green-robed wizard | three groups | `battle_f9_three_groups` |
| Lifestealer-type undead ("UNSEEN ENTITY") | floor 9 | pale humanoid | casts for 6; dissolved by a priest | `battle_f9_unseen_entity`, `battle_dispell`, `battle_dispell_ep` |
| Lvl 10 mages with a Man in robes | floor 10 | green-robed wizard | - | `battle_f10_mages` |
| Poison giant with Will o' wisps | floor 10 | red-shirted giant | - | `battle_f10_giant` |
| Master ninja with Strange animals | floor 8, level 1 party | green crouching animal | kill a level 1 fighter in one blow; the animals call for help | `battle_l1_floor8`, `battle_slain`, `battle_call_for_help`, `battle_help_heard`, `battle_three_dead` |
| Vampire, Vampire lord ("UNSEEN ENTITY") | Werdna's room | no picture of their own (Werdna's shows) | spells that finish wounded members; a touch that paralyzes and drains 2 levels | `boss_werdna_geared`, `boss_vampire_spell`, `boss_tiltowait`, `boss_paralyzed`, `boss_level_drain`, `boss_round2` |
| W E R D N A | floor 10 (17,3) | green-robed wizard | a spell of 57-104 damage on every member; takes 69 from TILTOWAIT, ignores LAHALITO; can be friendly | `boss_werdna`, `boss_werdna_orders`, `boss_werdna_hurt`, `boss_spell_unaffected`, `boss_werdna_killed`, `boss_werdna_spell`, `boss_member_dies`, `boss_four_dead`, `boss_werdna_friendly`, `boss_friendly_left`, `boss_werdna_ep`, `boss_werdna_chop`, `boss_mabadi` |
| Bear, amphibian, insect, dragon and coin pictures | floors 3-7 **(disk data)** | - | - | none: five of the 20 pictures were not met in the rooms tried |

## 4. Items and equipment
| Item | Type | Got from | What it does | Shots |
|---|---|---|---|---|
| Long sword 25, short sword 15, anointed mace 30, anointed flail 150, staff 10, dagger 5 | weapons | trading post | - | `shop_boltac_buy`, `shop_purchase`, `shop_unusable` |
| Small shield 20, large shield 40, robes 15, leather armor 50, chain mail 90, breast plate 200, plate mail 750, helm 100 | armour | trading post | - | `shop_boltac_armor`, `shop_boltac_potions` |
| Dios potion 500, Latumofis potion 300, Sopic potion 1500, scrolls of Katino, Badios, Halito 500 | one-use magic | trading post | the Dios potion heals fully in battle | `shop_boltac_potions`, `shop_bought`, `shop_sold`, `battle_potion`, `camp_use_item`, `camp_use_whom` |
| Short sword+1 15000, mace+1 12500, staff of Mogref 3000, leather + 1 to breast plate +1 1500 | magic gear | trading post | - | `shop_boltac_magic`, `shop_boltac_plus1` |
| Staff +2 2500, jeweled amulet 5000, copper gloves 6000, evil chain + 2 8000 | rare stock | trading post, last page | alignment-bound armour is sold too | `shop_boltac_rare` |
| Long sword + 2, plate mail + 2, shield + 2, helm + 1 and the other veterans' gear | fighter, priest, thief, mage gear | poked for the veterans | armour class 10 to -4 | `inventory_sheet_vet`, `inventory_sheet_condi`, `inventory_sheet_priest`, `inventory_sheet_thief`, `inventory_sheet_mage`, `inventory_sheet_bishop`, `shop_sell`, `camp_equip`, `camp_equip_armor` |
| Dragon slayer | sword | unidentified in a pack; on JIB | shows as SWORD until identified (fee 5000) | `shop_identify`, `shop_identified`, `inventory_sheet_jib` |
| Cursed robe | cursed armour | poked | marked `-`; uncursing (4000) removes it | `inventory_cursed`, `shop_uncurse`, `shop_uncursed` |
| Ring of Porfic | misc | poked, unidentified | identified by the bishop | `inventory_bishop_identify`, `inventory_identified` |
| Murasama blade, evil plate + 3, silver gloves, ring of healing, shield + 3 | end-game gear | the inherited characters | the blade is unusable (#) for the ninja, equipped by the samurai | `inventory_sheet_ninja`, `inventory_sheet_samurai` |
| Blue ribbon, bear statuette | quest items | floor 4 fight (inherited characters carry it); floor 2 statue | the ribbon opens the private elevator | `inventory_sheet_jib`, `system_search_found`, `dialogue_f4_asleep` |
| Werdna's amulet | quest item | Werdna's fight | "?AMULET" in the finder's pack; ends the game at the castle | `boss_amulet_found`, `inventory_amulet`, `ending_congratulations` |
| Chest loot | gold and unknown items | chests | 5 and 58 GP a share; a ?SWORD | `chest_gold`, `chest_gold_58`, `chest_item_found`, `chest_crossbow_bolt` |
| Traded and dropped items | - | sheet | - | `inventory_trade`, `inventory_trade_gold`, `inventory_trade_item`, `inventory_drop`, `inventory_dropped` |

## 5. Abilities and spells
| Ability | Who | Cost | What it does | Shots |
|---|---|---|---|---|
| The mage book | mage level 13 | - | 21 names in seven levels | `inventory_mage_book`, `inventory_spellbooks` |
| The priest book | priest level 13 | - | 29 names in seven levels | `inventory_priest_book` |
| HALITO | mage 1 | one level 1 point | one target | `battle_spell_prompt`, `battle_cast` |
| KATINO | mage 1 | - | sleep on a group: one of four slept | `battle_katino` |
| MAHALITO | mage 3 | - | 13-16 damage to each of a group | `battle_mahalito` |
| LAHALITO | mage 4 | - | 24 on an unseen entity; nothing on Werdna | `battle_spell_group`, `boss_spell_unaffected` |
| TILTOWAIT | mage 7 | - | 63-86 to every monster | `battle_tiltowait`, `boss_tiltowait`, `boss_werdna_hurt`, `battle_demon_unaffected` |
| BADIOS | priest 1 | - | one target; shrugged off by a dragon fly | `battle_unaffected` |
| DIOS | priest 1 | - | heals one member, in camp too | `camp_cast_whom` |
| CALFO | priest 2 | - | names a chest's trap | `chest_calfo_who`, `chest_calfo` |
| MALIKTO | priest 7 | - | 38-52 to every monster | `battle_malikto`, `battle_malikto_ninja` |
| DUMAPIC | mage 1, camp | - | position report | `system_dumapic`, `system_dumapic_f4`, `system_fizzle` |
| MALOR | mage 7, camp | - | teleport | `camp_malor`, `camp_malor_set`, `camp_malor_home`, `camp_malor_bounce`, `gameover_malor_midair` |
| Dispell | priest, bishop, lord | none | dissolves undead | `battle_dispell` |
| Thief's inspect and disarm | thief | none | names and removes chest traps | `chest_inspect_who`, `chest_inspected`, `chest_disarm_prompt`, `chest_not_trapped`, `chest_open_who`, `chest_disarmed` |

## 6. Characters and people
| Who | Role | Where | Shots |
|---|---|---|---|
| RYZ, CONDI, EBO, CUBI, DEDDO, MNZ at level 1 | the party: two fighters, priest, thief, mage, bishop | castle, floor 1 | `menu_castle`, `menu_roster`, `inventory_sheet_l1`, `gameplay_camp` |
| The same six as veterans | level 13 with gear | everywhere | `menu_castle_vets`, `inventory_sheet_vet`, `inventory_sheet_condi`, `inventory_sheet_priest`, `inventory_sheet_thief`, `inventory_sheet_mage`, `inventory_sheet_bishop`, `inventory_camp_inspect` |
| ZED | a new neutral elf mage, then fighter | Training Grounds | `create_keep`, `training_inspect_new`, `training_class_changed_sheet` |
| The inherited roster | 20 characters of an earlier player, levels 9-50, with samurai, lord and ninja, two with the chevron | the scenario disk as dumped | `menu_roster_inherited`, `inventory_sheet_ninja`, `inventory_sheet_samurai`, `inventory_sheet_lord`, `inventory_sheet_jib`, `tavern_password`, `tavern_bad_alignment` |
| Boltac, Gilgamesh, the priests of Cant | shopkeeper, tavern, temple: names on headers and greetings only | castle | `shop_boltac_who`, `menu_tavern_empty`, `menu_temple`, `temple_ritual`, `temple_healed`, `temple_cheap` |
| The robed man of floor 1 | shouts and sends the party home | floor 1 (9,19) | `dialogue_f1_mapiro` |
| Trebor | "your benificent ruler" | ending text | `ending_congratulations` |
| Werdna | the evil wizard | floor 10 | `dialogue_werdna_sign`, `boss_werdna`, `dialogue_f10_plaque_2` |
| The heroes afterwards | chevron, no gear | castle | `ending_castle`, `ending_chevron`, `ending_inn` |

## Standard views of the maze (2026-11-19)
Plain views with nothing happening, one or two per floor: what the player looks at most of the time. The maze
has one look on all ten floors (white and violet wireframe; doors are frames in a wall) **(verified: the shots)**. The same wall arrangement gives the same picture on any floor: three sampled views
were pixel-identical to others and were replaced.

| Floor | What is in view | Shots |
|---|---|---|
| 1 | an open passage with turnings; a corridor ending at a door | `env_f1_passages`, `env_f1_corridor` |
| 2 | a door close up; a crossing | `env_f2_door`, `env_f2_crossing` |
| 3-4 | a passage to the left; a door at the end of a short corridor | `env_f3_side_passage`, `env_f4_door` |
| 5-6 | a long view; corridors with doors along one wall | `env_f5_long_view`, `env_f5_corridor`, `env_f6_corridor` |
| 7-8 | a door ahead; a corner | `env_f7_door`, `env_f8_corner` |
| 9-10 | a long corridor with doors; a corridor ending at a door | `env_f9_corridor`, `env_f10_corridor` |

## Open questions
- Monsters of floors 5 and 6 and the five pictures not met (bear, amphibian, insect, dragon, creeping coin):
  kick into rooms of those floors with wait variants (playbook, "Encounters").
- The monster table's fields beyond the names are a reading of the record that was not checked in play.
- Trap kinds other than the crossbow bolt.
