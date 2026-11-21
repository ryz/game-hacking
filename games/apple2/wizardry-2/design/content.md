# Wizardry II: The Knight of Diamonds - content (variety lens)

What the game is filled with: its places, opponents, things and people, shown as a reasonable variety rather
than a full list. Read it to see the range of what a player meets. The rules behind the content are in
[systems.md](systems.md), the screens it appears on in [interface.md](interface.md); the same shots appear
there, overlap is intended. Notation: [README.md](README.md). Check: `python3 tools/lenses.py apple2/wizardry-2 main`.
Shots are ids of the set `main`.

## 1. Kinds of content
| Kind | In the game (count if known) | Shown here | Full list |
|---|---|---|---|
| Environments | 6 maze floors and the castle **(disk data, verified)** | all six floors, the castle's six places | [maps](maps/floors.txt) |
| Message squares | 20 on six floors **(disk data)** | 18 with their pages | [maps](maps/floors.txt) |
| Opponents | 78 kinds, pictures numbered 0-29 **(disk data)** | 5 guardians, 14 random encounters, 13 pictures | `../tools/data.py monsters` |
| Items and equipment | 130 **(disk data)** | Boltac's stock (6 pages), the party's gear, 6 quest items, unknown and cursed items | `../tools/data.py items`, [DOS items](../../../dos/wizardry-2/design/items.md) |
| Abilities / spells | 21 mage and 29 priest spells **(verified: the books)** | both books, 7 cast | [Wizardry I](../../wizardry/design/content.md) |
| Characters and people | the party, four characters found on the disk, Gnilda, the sphinx, the sage, a familiar figure, Queen Margda | all below | - |

## 2. Environments
| Environment | Where | What sets it apart | Shots |
|---|---|---|---|
| Castle of Llylgamyn (written LLYLGAMN) | town menus | text screens with the place name in the header **(verified)** | `menu_castle`, `menu_tavern`, `menu_inn`, `shop_boltac`, `menu_temple`, `menu_edge` |
| Wireframe corridors | all floors | purple walls, doors as inner frames, white frame **(verified)** | `gameplay_maze_f1_start`, `env_f1_corridor`, `env_f2_doors`, `env_f3_junction`, `env_f4_hall` |
| The cavern | floor 4 (7,13) | open area with stalactites in the text, side walls missing in the view **(verified)** | `env_f4_cavern`, `dialogue_f4_cavern`, `dialogue_f4_stalactites` |
| Dark squares | floors 1, 2, 5, 6 **(disk data)** | nothing drawn **(verified on floor 1)** | `gameplay_dark` |
| Pits, chutes, OUCH squares, teleports, spinners | floors 1-6 **(disk data)** | one-line messages, hit points lost, the party moved **(verified)** | `gameplay_pit`, `gameplay_chute`, `gameplay_ouch`, `gameplay_teleport_temple`, `env_f6_spinner` |
| Gnilda's temple | floor 1 (9,10) | the speech for six, the test for one alone **(verified)** | `dialogue_gnilda`, `dialogue_gnilda_2`, `dialogue_gnilda_3`, `dialogue_gnilda_4`, `dialogue_gnilda_test` |
| The sage's study | floor 2 (18,9)-(18,10) | a fee of 100,000 and hints about changed spells **(verified)** | `dialogue_f2_sage`, `dialogue_f2_sage_study`, `dialogue_f2_sage_stars`, `dialogue_f2_sage_spells`, `dialogue_f2_sage_latumapic` |
| A Burma-Shave rhyme | floor 4 (17,9) to (16,7) | four signs in a row: "A CAVERN'S DARK...", "AS THE INSIDE OF A MOUNTAIN...", "DOWN THE HALL...", "... A CLEAR BLUE FOUNTAIN." BURMA SHAVE (TM), then a fountain to wade in **(verified)** | `dialogue_f4_cavern_sign`, `dialogue_f4_mountain`, `dialogue_f4_hall`, `dialogue_f4_fountain` |
| The well | floor 5 (11,8) | "WISHES: 5000 GP WIZICORP." **(verified)** | `dialogue_f5_well` |
| The kings' tomb clues | floor 6 | three "THAT KING ..." signs: gold, power, doom **(verified)** | `dialogue_f6_king_treasure`, `dialogue_f6_king_power`, `dialogue_f6_king_doom` |
| The sphinx's door | floor 6 (1,2) | five pages of riddle, "ONE ALONE." beyond **(verified)** | `dialogue_sphinx_2`, `dialogue_sphinx_4`, `dialogue_one_alone` |
| Other signs | floors 2, 3, 4 | panel, three roads, riddle, "MAPIRO MAHAMA DIROMAT", "ANOTHER LINE OF WORK?", a cave-in **(verified)** | `dialogue_f2_panel`, `dialogue_f2_three_roads`, `dialogue_f2_riddle`, `dialogue_f3_mapiro`, `dialogue_f3_mapiro_shout`, `dialogue_f3_line_of_work`, `dialogue_f4_cave_in` |
| The cemetery | after a total defeat | six tombstones **(verified)** | `gameover_cemetery` |

## 3. Opponents
A spread over pictures, floors and group sizes; bosses marked.

| Opponent | Where met | Picture | What it did | Shots |
|---|---|---|---|---|
| Magic Armor (boss) | floor 1 (15,2) | animated armor | 305 hit points, AC -10; three spells did nothing **(verified)** | `boss_magic_armor`, `boss_armor_ep` |
| Magic Shield (boss) | floor 2 (2,6) | a shield, shown as "ANIMATED OBJECT" **(verified)** | AC -10 **(disk data)** | `boss_magic_shield` |
| Magic Sword (boss) | floor 3 (14,13) | a sword | died in one round to Lahalito and Malikto **(verified)** | `boss_magic_sword`, `boss_sword_dies`, `boss_sword_ep` |
| Magic Helmet (boss) | floor 4 (10,4) | a helmet in green flames | one spell: 72-98 damage to each of four members, all dead **(verified)** | `boss_magic_helmet`, `boss_helmet_spell`, `boss_helmet_costly` |
| Magic Gauntlets (boss, two) | floor 5 (10,9) | a gauntlet | casts too **(verified)** | `boss_magic_gauntlets`, `boss_gauntlet_spell` |
| Men in armor, lvl 8 mages | floor 1 | fighter with sword and shield | - | `battle_f1_men_in_armor` |
| Swarm | floors 1, 5 | insects | up to four groups of nine; giant wasps bite **(verified)** | `battle_f1_swarm`, `battle_f5_swarms` |
| Demonic figures and a lvl 8 ninja | floor 1 | a demon face | - | `battle_encounter` |
| Men in armor with a lvl 7 priest | floor 2 | archer | struck first **(verified)** | `battle_f2_men_in_armor` |
| Men in armor and priests | floor 2 | priest with a mace | - | `battle_f2_priests` |
| Weretigers | floor 2 | a big cat | - | `battle_f2_weretigers` |
| Fluffy things | floor 2 | a green fuzzball | - | `battle_f2_fluffy_things` |
| Manticores | floor 3 | a big cat | tear and gnaw, 12-26 damage **(verified)** | `battle_f3_manticores`, `battle_monster_hit` |
| Four groups of men and casters | floor 3 | priest | a mage thrust and missed **(verified)** | `battle_f3_four_groups` |
| Greater demons, ninjas, demonic figures | floor 6 | demon face | three groups **(verified)** | `battle_f6_greater_demons` |
| Evil eyes and skulls | floor 6 | a skull | - | `battle_f6_evil_eyes` |
| Men in black, a dragon, strange animals | floor 6 | a green dragon's head | - | `battle_f6_dragon` |
| Ninjas, a succubus, demonic figures, priests | floor 6 | demon face | four groups, struck first **(verified)** | `battle_f6_succubus` |

## 4. Items and equipment
| Item | Type | Got from | What it does | Shots |
|---|---|---|---|---|
| Long sword 25 ... dagger 5 | weapons | Boltac's page 1 **(verified)** | - | `shop_buy_weapons` |
| Shields, robes, leather 50, chain mail 90 | armor | Boltac's page 2 **(verified)** | - | `shop_buy_armor` |
| Breast plate 200, plate mail 750, helm 100, potions | armor, potions | Boltac's page 3 **(verified)** | - | `shop_buy_plate` |
| Long sword+1 10,000, staff of Mogref, scroll of Katino | magic | Boltac's page 4 **(verified)** | - | `shop_buy_magic` |
| Leather+1 to breast plate+1, 1,500 each | magic armor | Boltac's page 5 **(verified)** | - | `shop_buy_plus` |
| Staff+2 2,500, dragon slayer 10,000, shield-1 | rare | Boltac's page 6 **(verified)** | - | `shop_buy_rare` |
| The party's gear | weapons and armor | Boltac-priced (poked) | AC 0 to 9 **(verified)** | `camp_menu`, `inventory_sheet_ebo`, `inventory_sheet_cubi`, `inventory_sheet_deddo`, `inventory_sheet_mnz` |
| Potion of Sopic | potion, unknown at first ("POTION") | poked into a pack | identified by MNZ and by Boltac **(verified)** | `camp_identified`, `shop_identified` |
| Cursed robe | cursed armor | poked into a pack | uncursed at Boltac's for 4,000 **(verified)** | `shop_uncurse` |
| KOD's armor, shield, helmet, gauntlets, Hrathnir | quest armor and sword | the five guardians, unidentified ("PLATE ARMOR", "BROAD SWORD", "HELMET", "GAUNTLETS") **(verified)** | worn together: AC -18, regeneration **(verified)** | `boss_found_armor`, `boss_found_sword`, `boss_found_helmet`, `boss_found_gauntlets`, `inventory_kod_set` |
| Staff of Gnilda | quest item | Gnilda **(verified)** | ends the quest at the castle | `dialogue_staff_gift_3`, `inventory_staff` |
| Items of the earlier player | KOD pieces, blade Cusinart', mind stone, neutral plate mail+2, copper gloves | on the delivered disk **(verified)** | - | `inventory_stock_kelrach`, `inventory_stock_fury` |

## 5. Abilities and spells
| Ability | Who | Cost | What it does | Shots |
|---|---|---|---|---|
| The mage book: Halito to Tiltowait | mage, bishop | a point of the spell's level | 21 spells **(verified list)** | `inventory_mage_book` |
| The priest book: Kalki to Kadorto | priest, bishop | the same | 29 spells **(verified list)** | `inventory_priest_book` |
| Lahalito, Halito, Badios | mage, bishop, priest | 1 point | damage to monsters: 2-22 seen **(verified)** | `battle_spell_damage`, `boss_sword_lahalito` |
| Malikto | priest | a level 7 point | 40 damage to the Magic Sword **(verified)** | `boss_sword_dies` |
| Dumapic | mage | 1 point | position and facing **(verified)** | `camp_dumapic` |
| Malor | mage | a level 7 point | teleport by a typed displacement **(verified prompt)** | `camp_malor` |
| Dios | priest, potion | 1 point or the potion | heals one member **(verified prompt)** | `camp_cast_whom`, `battle_use_item` |

## 6. Characters and people
| Who | Role | Where | Shots |
|---|---|---|---|
| RYZ, CONDI, EBO, CUBI, DEDDO, MNZ | the party: two fighters, priest, thief, mage, bishop, level 13 | from Wizardry I **(verified)** | `inventory_sheet_import`, `inventory_sheet_geared`, `system_transfer_list` |
| THUG, HALIG, KELRACH, FURY | characters of an earlier player on this copy's disk, levels 28-38, holding four of the pieces **(verified)** | Training Grounds | `inventory_roster_original`, `inventory_stock_thug` |
| Gnilda's apparition, the fiery face | quest giver | floor 1 (9,10) **(verified)** | `dialogue_gnilda_fades`, `dialogue_staff_gift`, `dialogue_staff_gift_2` |
| The sphinx | riddle | floor 6 (1,2) **(verified)** | `dialogue_sphinx`, `dialogue_sphinx_3`, `dialogue_sphinx_5` |
| A wizened sage | hints for gold | floor 2 **(verified)** | `dialogue_f2_sage` |
| A familiar figure | shouts "MAPIRO MAHAMA DIROMAT" and the party is back in the Castle **(verified)** | floor 3 (8,10) | `dialogue_f3_mapiro_shout` |
| Queen Margda | ruler, speaks the ending **(verified)** | ending | `ending_gaudeamous` |

## Open questions
- Floor 4 has no room doors: its random groups were not met. Floor 5 and 6 fixed fights (High Priest) not visited.
