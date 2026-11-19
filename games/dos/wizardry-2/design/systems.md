# Wizardry II: The Knight of Diamonds (DOS) - systems (game-design lens)

The index of everything the game lets the player do and every rule that shapes play: one row per feature,
system or mechanic, with the rule in one line, where the details live and which shots show it. Read it to see
what the game is made of; follow the links for numbers. The same shots also appear in
[interface.md](interface.md), which looks at the screens themselves, and in [content.md](content.md), which
shows the variety of what fills the game; overlap is intended.
Notation: [README.md](README.md). Check: `python3 tools/lenses.py dos/wizardry-2`.

Status: `shown` (a shot shows it at work), `described` (known, no shot: say why), `open` (not understood).
Shot ids are those of set `main` (`../shots/main/index.md` gives the file names).

## 1. Core loop
As in Wizardry I: form a party in the Castle, descend, fight, map the floors, come back to rest and shop
(verified: same menus). Wizardry II starts where Wizardry I ended: the party arrives as veterans of levels 11-13
without equipment (the move keeps everything but the items), so the first trip is to Boltac's with the gold
carried over (verified: `shop_boltac`, `camp_menu`, `menu_castle_geared`). Each of floors 1-5 ends at a guardian
before the stairs down that drops one piece of the Knight of Diamonds' regalia (verified: all five fought,
`boss_found_*`); one character alone, wearing the five, answers the sphinx's riddle in Gnilda's temple, receives
the Staff of Gnilda and carries it to the Castle alone (verified: `dialogue_staff_gift`, `ending_congratulations`).

## 2. Systems
Rules shared with Wizardry I are listed once with a link; the Wizardry I reference has their formulas.

| Group | System / mechanic | Rule in one line | Player's inputs | Numbers known | Details | Shots | Status |
|---|---|---|---|---|---|---|---|
| Player verbs | Walk, turn, kick, bump | W steps, A/D turn, K goes through a door; a wall stops the party with a message (verified) | W A D K | 1 square per step | [Wizardry I systems](../../wizardry/design/systems.md) | `gameplay_maze_f1_start`, `gameplay_wall`, `gameplay_door` | shown |
| Player verbs | Views | S)tatus hides the party window, O)ff hides command line and party (verified) | S, O | - | Wizardry I | `gameplay_status_off`, `gameplay_full_view` | shown |
| Player verbs | Search for bodies | I)nspect searches the square: "Searching......." then "Found: * no one *" (verified) | I | about 300 frames | - | `gameplay_inspect_none` | shown |
| Player verbs | Answer a riddle | some squares ask for a typed answer; a wrong one puts the party back one square, the right one lets it stay (verified: floor 2 "shield", the sphinx "the knight of diamonds") | text + Enter | 2 riddles | [findings](findings.md) | `dialogue_f2_riddle`, `dialogue_f2_riddle_answer`, `dialogue_sphinx_answer` | shown |
| Player verbs | Pay for a service | some squares ask a fee: "The fee is N. Will you pay (Y/N)?"; Y takes the gold from the party and answers "Thank you!" (sage, 100000) or sends the party home (well, 5000) (verified) | Y, N | 100000, 5000 | content.md, Environments | `dialogue_f2_sage_fee`, `dialogue_f2_sage_paid`, `dialogue_f5_well_fee` | shown |
| Player verbs | Wade | the floor 4 fountain asks "Who (#) will wade?"; the wader came out poisoned (verified, one try) | digit | - | - | `dialogue_f4_wade`, `gameplay_poisoned` | shown |
| Characters and progression | Import (Move characters) | Utilities M)ove reads a Wizardry I scenario disk; letters mark characters ("+"), Enter removes them from the source roster and moves them one by one; they keep level, HP, E.P., gold, age, statistics, spells and the chevron and lose every item (verified) | letters, Enter, Esc | up to the free roster slots | playbook, Game structure | `system_move_list`, `system_move_marked`, `system_move_removing`, `system_move_insert`, `system_move_moving`, `system_move_moved`, `menu_tavern_imported`, `inventory_sheet_import` | shown |
| Characters and progression | No creation | the Training Grounds only inspect and list characters; six ready veterans of levels 12-13 come on the disk (verified) | I, R | 6 stock characters | - | `menu_training`, `training_pick`, `inventory_roster`, `menu_tavern_stock`, `inventory_stock_caleb` | shown |
| Characters and progression | Party forming | the Tavern adds characters by roster letter (the list closes at six) and removes by party number (verified) | A + letter, R + digit | 6 | Wizardry I | `menu_tavern`, `tavern_adding`, `tavern_remove`, `menu_castle_solo` | shown |
| Characters and progression | Levels | a stay at the Inn checks the E.P.: short of the next level it says how many are missing, otherwise "You made the next level!" with statistic changes and a hit point gain (verified: fighter level 12 at 232,044 E.P.) | Inn | RYZ needed 47,457 more at 184,587 | Wizardry I | `inn_stables`, `ending_inn_levelup` | shown |
| Characters and progression | Level drain | some undead touch drains a level ("CONDI is drained one level!"); after the fight "CONDI was drained!" (verified) | - | 1 level | - | `battle_level_drain`, `battle_run` | shown |
| Characters and progression | Awards | marks after the name: ">" Wizardry I's chevron kept, "G" Mark of Gnilda for the staff's bearer, "K" Knight of the City for chosen characters (verified) | Y/N per character | bearer +300,000 E.P., knights none | playbook | `ending_sheet_ryz`, `ending_sheet_condi`, `ending_make_knight` | shown |
| Resources and economy | Gold carried over | imported characters bring their Wizardry I gold (55,077-74,817 here); it buys the first gear (verified) | - | - | - | `inventory_sheet_import`, `shop_boltac` | shown |
| Resources and economy | Boltac's | the same 25-item stock as Wizardry I's start, five pages that wrap round; buy, sell, uncurse, identify, pool gold; unusable items are marked and asked about (verified) | B S U I P, digits | prices in [items.md](items.md) | items.md | `shop_boltac_who`, `shop_boltac`, `shop_boltac_buy`, `shop_boltac_armor`, `shop_boltac_potions`, `shop_boltac_magic`, `shop_boltac_rare`, `shop_purchase`, `shop_bought`, `shop_unusable`, `shop_sell`, `shop_sold`, `shop_pool`, `shop_identify`, `shop_identified`, `shop_uncurse`, `shop_uncursed`, `ending_rebuy` | shown |
| Resources and economy | Identify price | Boltac asks 150,000 to identify a regalia piece (more than one character carries: pool first) (verified) | I | 150000 | items.md | `shop_identify`, `shop_identified` | shown |
| Resources and economy | Inn | stables free (no healing), cot 10, economy 50, merchant 200, royal suite 500 gold per week; hit points recover week by week (verified) | digit, A-E | as listed | Wizardry I | `menu_inn_who`, `menu_inn`, `inn_recuperating` | shown |
| Resources and economy | Temple | cures the dead, paralysed and ashes for a donation per level (dead: 250 x level, verified 2750 for level 11) | letter, payer | 250 per level for death | Wizardry I | `menu_temple_empty`, `temple_dead`, `temple_donation`, `temple_healed` | shown |
| Conflict | Combat orders | each member gets an order in turn; members 4-6 cannot fight hand to hand; Enter starts the round, T takes orders back (verified) | F P S D U R T, digits | - | Wizardry I | `battle_orders`, `battle_group_select`, `battle_round2` | shown |
| Conflict | Surprise | either side may surprise the other: a surprise round offers no S)pell (verified: both ways) | - | - | - | `battle_surprised_monsters`, `battle_f2_ogre_lords`, `boss_magic_armor` | shown |
| Conflict | Hits and damage | a blow can hit several times; damage lines name the target; "is killed!" ends a monster (verified) | F | - | - | `battle_multi_hit`, `battle_kill`, `battle_monster_hit`, `boss_armor_killed` | shown |
| Conflict | Spells in battle | spells are typed by name; group spells ask for a group; monsters may resist (verified: guardians resist Lahalito and Tiltowait) | S + name | - | Wizardry I | `battle_spell_prompt`, `battle_badios`, `battle_halito`, `battle_lahalito`, `battle_lahalito_kill`, `boss_shield_tiltowait`, `boss_sword_killed` | shown |
| Conflict | Dispell, use, run | priests dispell undead groups; items can be used; R)un leaves the fight (verified) | D, U, R | - | Wizardry I | `battle_dispell_which`, `battle_use_item`, `battle_run` | shown |
| Conflict | Enemy magic and status | monsters cast Katino (sleep), Dilto (darkness: AC 2 worse), Halito, Mahalito, Lahalito; sleep, poison, death, decapitation shown in the party window (verified) | - | - | - | `battle_enemy_katino`, `battle_enemy_dilto`, `battle_party_asleep`, `battle_f1_large_animals`, `battle_f4_slimes`, `boss_helm_lahalito`, `boss_gauntlet_mahalito`, `boss_shield_ebo_killed`, `boss_sword_decapitated` | shown |
| Conflict | Rewards | E.P. per survivor after a won fight, then items and gold (verified) | - | guardians: 5555 (armor), 8888 (shield), 13333 (sword) E.P. | - | `battle_victory`, `boss_armor_ep`, `chest_gold` | shown |
| Opponents | Guardians | a fixed group on the square before each stairs down, floors 1-5: Magic Armor (305 hit points, regenerates), Magic Shield (79), Magic Sword (72), Magic Helm (156), two Magic Gauntlets (50 each); shown as "animated object" until identified; they fight on every visit (verified, RAM) | - | hit points (RAM) | playbook | `boss_magic_armor`, `boss_magic_shield`, `boss_magic_sword`, `boss_magic_helm`, `boss_magic_gauntlets` | shown |
| Opponents | Random groups | per-floor groups of up to four kinds; friendly groups offer F)ight or L)eave; rooms (fight zones) roll for a group when entered (verified) | F, L | - | [maps](maps/floors.txt) | `battle_friendly`, `battle_f5_four_groups`, `battle_f6_four_groups` | shown |
| Items and equipment | Equipping | camp E)quip goes member by member, slot by slot (weapon, armor, shield, helm, gauntlets); items a class cannot use are marked "#" and skipped (verified) | digit, Enter | 5 slots | Wizardry I | `camp_equip`, `camp_equip_gauntlets`, `camp_equipped`, `inventory_sheet_geared` | shown |
| Items and equipment | Identify, trade, drop | bishops identify (may fail: "You don't have a clue!"), any member trades gold and items or drops them (verified) | I, T, D | - | Wizardry I | `inventory_bishop_noclue`, `inventory_bishop_identify`, `inventory_identified`, `inventory_trade`, `inventory_trade_gold`, `inventory_drop` | shown |
| Items and equipment | The regalia | Hrathnir and KOD's helm, shield, gauntlets, armor: each guardian drops its piece unidentified ("ARMOR", "SWORD"); worn together AC -18 and hit point regeneration ("+") (verified, RAM item numbers 125-129) | E)quip, T)rade | AC -18 for a level 11 fighter | items.md | `boss_found_armor`, `boss_found_shield`, `boss_found_sword`, `boss_found_helm`, `boss_found_gauntlets`, `inventory_kod_set` | shown |
| Items and equipment | Chests | a won fight may leave a chest: inspect, Calfo, disarm (the trap's name is typed), open; a trap goes off when opened untouched (Alarm: a new group) (verified) | O C L I D | - | Wizardry I | `battle_chest`, `chest_inspect_who`, `chest_inspected`, `chest_calfo_who`, `chest_disarm_prompt`, `chest_disarmed`, `chest_found_item`, `chest_alarm`, `chest_alarm_encounter` | shown |
| Abilities and magic | Spells | Wizardry I's 21 mage and 29 priest spells; imported casters keep spells and points (verified: books) | camp S, battle S | - | Wizardry I | `inventory_spellbooks`, `inventory_mage_book`, `inventory_priest_book` | shown |
| Abilities and magic | Camp magic and items | Dios heals ("Cast on whom?"), Dumapic tells the position, Malor teleports the party, potions are used from the sheet (verified) | S, U | - | Wizardry I | `camp_cast_whom`, `system_dumapic`, `camp_malor`, `camp_use_item` | shown |
| World and navigation | Six floors | 20 x 20 each, one staircase down per floor behind its guardian; dark areas, pits, ouch squares, chutes, teleports, spinners, rock (verified: disk data and play) | - | 6 floors | [maps](maps/floors.txt) | `gameplay_stairs_down`, `gameplay_stairs_up` | shown |
| World and navigation | Traps on squares | pits ("A pit!", damage to several members), ouch squares ("Ouch!!"), chutes to floor 6 ("One moment"), darkness (grey view) (verified) | - | - | maps | `gameplay_pit`, `gameplay_pit_damage`, `gameplay_ouch`, `gameplay_chute`, `gameplay_dark` | shown |
| World and navigation | Teleports | floor 6 (1,4) sends the party to floor 1 (9,9) before Gnilda's temple; the "Mapiro Mahama Diromat" figure on floor 3 and the floor 5 well send it to the Castle (verified) | - | - | maps | `gameplay_teleport_temple`, `dialogue_f3_mapiro` | shown |
| World and navigation | Spinners | floor 6 squares turn the party (disk data); no visible effect to photograph | - | 5 squares | maps | none: nothing shows on screen | described |
| Goals and gating | The chain | guardians -> five pieces -> one bearer wears all five -> the sphinx's riddle (floor 6) -> Gnilda's test (alone) -> the staff -> the Castle alone -> the ending (verified, played through) | - | - | playbook | `dialogue_sphinx`, `dialogue_gnilda_test`, `dialogue_staff_gift`, `ending_congratulations` | shown |
| Goals and gating | Clues | message squares point the way: the armor "four steps ahead, but three steps away", the sphinx's "king within his tomb", the king lines on floor 6 (verified) | - | - | content.md | `dialogue_f1_armor_clue`, `dialogue_sphinx_2`, `dialogue_sphinx_3`, `dialogue_sphinx_4`, `dialogue_f6_king_treasure`, `dialogue_f6_king_doom` | shown |
| Goals and gating | "One alone" | Gnilda's test and the ending answer only a party of one; a party of six hears the speech and the apparition fades; Gnilda takes the whole pack and gives the staff (verified) | Tavern remove | 1 | [findings](findings.md) | `dialogue_one_alone_real`, `dialogue_gnilda_fades`, `menu_castle_solo`, `inventory_staff` | shown |
| Goals and gating | The staff | U)se says "* Powerless *"; carried into the Castle alone it ends the game (verified) | U | - | - | `inventory_staff_powerless`, `ending_congratulations` | shown |
| Chance | Encounters and rolls | random groups, hits, sleep and surprise follow the frame timing (verified: wait variants give other groups) | - | - | playbook | `battle_f1_dogs`, `battle_f1_large_animals` | shown |
| Failure and recovery | Death, burial, cemetery | a killed member shows DEAD and moves back; the Temple raises for gold; a party all dead ends in the cemetery (verified; the party wipe set by poke) | Temple, Enter | - | Wizardry I | `gameplay_member_dead`, `gameover_slaughtered`, `gameover_cemetery`, `temple_healed` | shown |
| Failure and recovery | Restart an "out" party | Utilities R)estart finds characters left in the maze ("No characters are in the maze" here) (verified) | R | - | - | `util_restart_none` | shown |
| Saving and sessions | The scenario disk | the roster on the disk is the save, written as the game goes; L)eave game ends the program ("Thanks for playing Wizardry!") (verified) | Edge of Town L | 20 slots | playbook, Saves | `menu_edge`, `save_leave_game` | shown |
| Saving and sessions | Making a scenario disk | the title's M)ake scenario disk warns that the disk's data will be erased (verified; Y not pressed) | M, Y/N | - | - | `menu_make_scenario` | shown |
| Pacing and difficulty | Veterans only | the game assumes a high-level party: on floor 1 Kobold kings, Men in armor; guardians that kill members (EBO and CONDI died on floors 2 and 3) (verified) | - | - | - | `battle_f1_men_in_armor`, `boss_shield_ebo_killed`, `boss_sword_decapitated` | shown |

## 3. How the systems feed each other
- Wizardry I's end state (levels, gold, spells, chevron) is Wizardry II's start; the items stay behind, so the
  carried gold buys the first gear at Boltac's (verified).
- Guardians gate the stairs and drop the pieces; identification is expensive at Boltac's (150,000) and a
  bishop may fail, so a bishop in the party matters (verified).
- The pieces gate the staff; the staff gates the ending; the ending's marks and E.P. carry on into Wizardry III
  (owner's queue; save `03_wizardry3_transfer`).

## Open questions
- What the floor 2 sage's 100,000 gold buys beyond "Thank you!" (the study at (18,9) speaks without payment).
- The well's 5,000 gold "wish": only the trip home was seen; other wishes not tried.
- Floor 2 (16,3) (message kind 9) cannot be entered from any side (one-way doors lead out): not reached.
- Floor 6 fixed fights (group 47) at (5,15)-(5,16) and (18,18)-(19,19): not fought (the (5,14) approach met a
  four-group fight; whether it was group 47 is not known).
