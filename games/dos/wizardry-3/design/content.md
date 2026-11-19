# Wizardry III: Legacy of Llylgamyn (DOS) - content (variety lens)

What the game is filled with: its places, opponents, things and people, shown as a reasonable variety rather
than a full list. Read it to see the range of what a player meets. The rules behind the content are in
[systems.md](systems.md), the screens it appears on in [interface.md](interface.md); the same shots appear
there, overlap is intended. Notation: [README.md](README.md). Check: `python3 tools/lenses.py dos/wizardry-3`.

## 1. Kinds of content
| Kind | In the game (count if known) | Shown here | Full list |
|---|---|---|---|
| Environments | 6 floors of 20 x 20 + the Castle (disk data) | one view per floor, dark squares, the lake, the Grand Wizard's house, graveyard, Fung's temple, the summit | [maps/floors.txt](maps/floors.txt) |
| Opponents | 78 monster records (disk data) | 2 guardians, 12 other groups | - |
| Items | 103 (verified) | quest items, swap items, loot, cursed items | [items.md](items.md) |
| Equipment | weapons and armour in -1/+0/+1/+2 tiers and named blades (verified names) | Boltac's stock, the party's outfit | [items.md](items.md) |
| Abilities / spells | Wizardry I's 21 mage and 29 priest spells (verified on the books) | about a dozen cast | [spell books](#5-abilities-and-spells) |
| Characters and people | 6 stock legacies + imports; NPCs by message | the party, the stock six, eight people of the volcano | [messages.md](messages.md) |
| Riddles and passwords | 5 riddles, 1 password (verified) | all six | [messages.md](messages.md) |

## 2. Environments
| Environment | Where | What sets it apart | Shots |
|---|---|---|---|
| Castle Llylgamyn | menus | five places, no picture | `menu_castle_start`, `menu_castle_geared` |
| Floor 1, entrance and corridors | floor 1 | the stairs down to the Castle at (0,0) | `gameplay_maze_f1_start`, `gameplay_door`, `gameplay_stairs_castle` |
| Floor 1 lake and beach | floor 1 (1-7, 0-7) | water's edge drowning warning, a beach with a picture, rock squares | `dialogue_f1_beach`, `dialogue_f1_water` |
| Fortress and moat | floor 1 (1,17), (8-13, 8-19) | moat monsters, barracks, Garian guards | `dialogue_f1_fortress`, `dialogue_f1_barracks`, `battle_f1_moat_monsters` |
| The Grand Wizard's house | floor 2 | office of S.E.G. Po'le, dining room, wine cellar, desk with the Staff of Earth | `gameplay_f2`, `dialogue_f2_pole`, `dialogue_f2_dining`, `dialogue_f2_wine_cellar`, `dialogue_f2_desk` |
| Graveyard, monk and pool | floor 3 | the warnings, an aged monk, a murky pool | `gameplay_f3`, `dialogue_f3_graveyard`, `dialogue_f3_crock`, `dialogue_f3_further`, `dialogue_f3_monk`, `dialogue_f3_pool` |
| Dark caverns of floor 4 | floor 4 | oily pool, "Look out!" traps, chutes, the guardian | `gameplay_f4`, `dialogue_f4_oily`, `dialogue_f4_look_out`, `gameplay_chute` |
| Dark floor 5 | floor 5 | grey hatched dark squares, pits, Fung's temple | `gameplay_f5`, `gameplay_f5_dark`, `gameplay_pit`, `dialogue_f5_fung` |
| The summit | floor 6 | statues, L'kbreth's lair, riddles, the teleport home | `gameplay_f6`, `gameplay_f6_arrival`, `dialogue_radiant_statue`, `dialogue_lkbreth_farewell`, `gameplay_teleport_home` |
| Loading and the stairs | between floors | "One moment" | `gameplay_one_moment`, `gameplay_stairs_up` |

## 3. Opponents
| Opponent | Where met | Family / picture | What it does | Shots |
|---|---|---|---|---|
| Giant Serpents | floor 1 | snake | attack a level-1 party first (verified) | `battle_f1_serpents` |
| Garian Guards, Corsairs | floor 1 (0,9) fixed fight | bearded men in hoods | ambush, then mostly run away from veterans (verified) | `battle_f1_ambush`, `battle_f1_runs_away`, `battle_lahalito`, `battle_katino`, `battle_kill` |
| Moat Monsters | floor 1 (8,12) | sea creature | caught by surprise (verified) | `battle_f1_moat_monsters` |
| Corsair, Garian Captains | floor 1 (16,13) | men | (verified) | `battle_f1_corsairs` |
| Shadowy Figures, Unseen Entity | floor 2 (3,1) | ghosts | (verified) | `battle_f2_shadowy` |
| Skeletal Figure, Po'le | floor 2 (11,19) | skeletons | the Grand Wizard's household (verified) | `battle_f2_pole` |
| Leprechauns | floor 3 | imp with a bow | random fight while turning (verified) | `battle_f3_leprechauns` |
| Were Rats, Vultures | floor 3 | rat, man | random fight (verified) | `battle_f3_were_rats` |
| Delf's Minions, Gaunt Figures | floor 4 (12,17) | skeletons | next to the guardian (verified) | `battle_f4_minions` |
| Banshees | floor 5 (0,9) | skulls | (verified) | `battle_f5_banshees` |
| Unseen Entity, Ghosts, Ghast | floor 6 | ghosts | resist a dispel; guard a teleporter chest (verified) | `battle_f6_ghosts`, `battle_f6_ghost_killed`, `battle_dispell_fails` |
| Xeno | floor 6 (4,4) statue search | monster | the guard of the third statue (verified) | `battle_f6_xeno` |
| Living Legend (Delf), Gaunt Figures - **guardian** | floor 4 (7,17) | bearded sage, skeletons | gaunt figures stone; Delf dies to TILTOWAIT; drops the Crystal of Evil (verified) | `boss_guardian_good`, `boss_delf_named`, `boss_tiltowait`, `boss_resists`, `boss_stoned`, `boss_found_evil` |
| Soul Trappers, Crusader Lords, Fighters, Crusaders - **guardian** | floor 5 (12,10) | spider, knights | paralyze, silence (MONTINO), BADIAL; drop the Crystal of Good (verified) | `boss_guardian_evil`, `boss_montino`, `boss_badial`, `boss_paralyzed`, `boss_cannot_speak`, `boss_found_good` |

## 4. Items and equipment
| Item | Type | Got from | What it does | Shots |
|---|---|---|---|---|
| Crystal of Evil | quest | the floor 4 guardian | opens floor 6; invoked by an evil bearer with the Crystal of Good -> Neutral Crystal (verified) | `boss_found_evil`, `inventory_crystals` |
| Crystal of Good | quest | the floor 5 guardian | the same for a good bearer (verified) | `boss_found_good`, `inventory_crystals` |
| Neutral Crystal | quest | the two crystals invoked | becomes the orb at the statue (verified) | `inventory_neutral_crystal` |
| Orb of Earithin | quest | statue (17,17) | the ending (verified) | `inventory_crystal_sphere`, `inventory_orb` |
| Orb of Mhuuzfes ("?SPHERE") | cursed decoy | statue (13,2) | AC -10, cursed (disk data) | `inventory_decoy_sphere` |
| Staff of Earth | quest | floor 2 desk | not known | `dialogue_f2_desk_found` |
| Gold Medallion, Holy Water | swap items | the monk and the pool on floor 3 | not known | `dialogue_f3_monk_traded`, `inventory_holy_water` |
| Broadsword+1, plate armor, heater shield, sallet, gloves of iron | equipment | Boltac's (RYZ's outfit) | AC 1 (verified) | `inventory_sheet_geared`, `camp_equip` |
| Short sword ... battle axe, shields, robes, armours, potions, +1 tiers | shop stock | Boltac's | prices 10-10000 (verified) | `shop_boltac_buy`, `shop_boltac_shields`, `shop_boltac_armor`, `shop_purchase`, `shop_boltac_magic` |
| Gem of Exorcism ("?JEWELRY") | cursed armour | MNZ's pack | identify 6000 (verified) | `shop_identify_fee`, `shop_identified`, `camp_equip_armor` |
| Sallet-1 | cursed helm | (poked) | uncurse 1000 (verified) | `shop_uncurse`, `shop_uncursed` |
| Jewelry, rod, weapon | loot | the floor 6 chest | unidentified (verified) | `chest_found_jewelry`, `chest_found_rod` |

## 5. Abilities and spells
| Ability | Who | Cost | What it does | Shots |
|---|---|---|---|---|
| HALITO ... TILTOWAIT, KALKI ... KADORTO | mage, priest, bishop | spell points per level | the books | `inventory_mage_book`, `inventory_priest_book`, `inventory_read` |
| LAHALITO | DEDDO | mage 4 | fire on a group, kills a Garian guard (verified) | `battle_lahalito` |
| KATINO | MNZ | mage 1 | sleep, a corsair slept (verified) | `battle_katino` |
| BADIOS | EBO | priest 1 | damage; wasted when no target is left (verified) | `battle_badios_wasted` |
| TILTOWAIT | DEDDO | mage 7 | kills Delf, some gaunt figures resist (verified) | `boss_tiltowait`, `boss_resists` |
| MADALTO | ZETT | mage 5 | kills the Crusader Lords (verified); silenced in another run | `battle_orders`, `boss_cannot_speak` |
| MONTINO, BADIAL (enemy) | guardian's men | - | silence; damage (verified) | `boss_montino`, `boss_badial` |
| DUMAPIC, MALOR | DEDDO in camp | mage 1, 7 | position; party teleport (verified) | `system_dumapic`, `camp_malor` |
| DIOS | EBO in camp | priest 1 | heal one (prompt verified) | `camp_cast_whom` |
| Dispell | EBO | - | undead; failed (verified) | `battle_dispell_which`, `battle_dispell_fails` |

## 6. Characters and people
| Who | Role | Where | Shots |
|---|---|---|---|
| RYZ CONDI EBO CUBI DEDDO MNZ | the descendants of the Wizardry II heroes | Castle | `menu_castle_start`, `inventory_descendant_sheet` |
| KLINDT LEIF ZETT VERPA SENA GITTER | stock legacies; four join the neutral party; six get the stars | roster | `menu_tavern_stock`, `inventory_stock_klindt`, `inventory_star_sheet` |
| L'kbreth | the dragon who took the orb | floor 1 warning, floor 6 farewell | `dialogue_f1_lkbreth`, `dialogue_lkbreth_farewell` |
| S.E.G. Po'le | the Grand Wizard, "out" | floor 2 | `dialogue_f2_pole`, `battle_f2_pole` |
| The woman with a whip | asks the password | floor 2 (7,11) | `dialogue_f2_whip`, `dialogue_f2_password` |
| Abdul | merchant: password hint, taxi, crystal | floors 3, 4, 5 | `dialogue_f4_abdul`, `dialogue_f3_taxi`, `dialogue_f5_taxi` |
| The aged monk, the apparition | swap items | floor 3 | `dialogue_f3_monk`, `dialogue_f3_pool` |
| Fung | irascible, behind a door | floor 5 (19,9) | `dialogue_f5_fung` |
| Queen Beyki | gives the stars | ending | `ending_gods_praised` |

## 7. Riddles and passwords
| Riddle | Where | Answer | Shots |
|---|---|---|---|
| "I am around you always..." | floor 2 (4,19) | AIR | `dialogue_f2_riddle_air`, `dialogue_f2_answer_air`, `gameplay_riddle_wrong` |
| "What's the password?" | floor 2 (7,11) | ABDUL SENT YOU | `dialogue_f2_password` |
| "Ours is an uneasy friendship..." | floor 4 (18,11) | FIRE | `dialogue_f4_riddle_fire`, `dialogue_f4_answer_fire` |
| "I am one of the deck of seventy-eight..." | floor 5 (5,13) | CHARIOT | `dialogue_f5_riddle_chariot`, `dialogue_f5_answer_chariot` |
| "Black figure on a black horse..." | floor 6 (19,17) | DEATH | `dialogue_riddle_death`, `dialogue_answer_death` |
| "On my roll, you move forward..." | floor 6 (11,4) | WHEEL | `dialogue_riddle_wheel`, `dialogue_answer_wheel` |

## Open questions
- Abdul's crystal sale and coffer on floor 5 (4,7)/(4,8): no open neighbour, probably reached by his taxi (not tried).
- The floor 6 dragon room (group 77) gave no fight (once tried).
