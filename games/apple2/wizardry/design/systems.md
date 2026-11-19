# Wizardry: Proving Grounds of the Mad Overlord - systems (game-design lens)

The index of everything the game lets the player do and every rule that shapes play: one row per feature,
system or mechanic, with the rule in one line, where the details live and which shots show it. Read it to see
what the game is made of; follow the links for numbers. The same shots also appear in
[interface.md](interface.md), which looks at the screens themselves, and in [content.md](content.md), which
shows the variety of what fills the game; overlap is intended.
Notation: [README.md](README.md). Check: `python3 tools/lenses.py apple2/wizardry`.

Status: `shown` (a shot shows it at work), `described` (known, no shot: say why), `open` (not understood).
Shots are ids of the set `../shots/main/` (file names in its `index.md`). Every rule in the table is
**(verified)** by the shots named in its row unless the cell carries another tag.

## 1. Core loop
Form a party in the Tavern, buy at the trading post and equip in the camp, enter the maze, fight groups of
monsters for experience and chests, come back up the stairs before the party is spent, rest at the Inn (which
heals and grants the levels earned), have the fallen raised at the Temple, and go deeper **(verified: each
step has its shot below; the order of the loop is the DOS port's, source)**. Between loops the characters gain
levels, spells and gear; the maze does not change.

## 2. Systems
| Group | System / mechanic | Rule in one line | Player's inputs | Numbers known | Details | Shots | Status |
|---|---|---|---|---|---|---|---|
| Player verbs | Castle menus | one letter per place: Inn, Tavern, Trading post, Temple, Edge of Town | `A G B C E` | 5 places | §5 | `menu_castle`, `menu_castle_empty`, `menu_castle_vets` | shown |
| Player verbs | Tavern: add, remove, see | members join by typed name and password; alignments must fit (an evil character may not join a good one); six at most | `A` + name, `R` + number, number | 6 members | §5 | `menu_tavern_empty`, `menu_tavern_add`, `tavern_password`, `tavern_who`, `tavern_wrong_password`, `tavern_bad_alignment`, `menu_tavern`, `tavern_remove`, `tavern_removed` | shown |
| Player verbs | Edge of Town | maze (only with a party), training grounds, castle, leave the game | `M T C L` | - | - | `menu_edge`, `menu_edge_empty` | shown |
| Player verbs | Walk and turn | forward, left, right; a wall stops the step with "OUCH!" | `F L R` (also `W A D`) | 1 square per step | [maps](maps/floors.txt) | `gameplay_maze_f1_start`, `gameplay_wall`, `gameplay_f3_crossing`, `gameplay_f6_doors`, `gameplay_f7_hall` | shown |
| Player verbs | Kick a door | F)orward does not pass a door; K)ick does (all doors, also secret ones) | `K` | - | [findings](findings.md) | `gameplay_door`, `boss_werdna` | shown |
| Player verbs | Camp | inspect a member, reorder the marching order, equip everyone, disband (leave the party in the maze), leave | `C`, then number, `R E D L` | - | - | `gameplay_camp`, `camp_reorder`, `camp_disband`, `inventory_camp_inspect` | shown |
| Player verbs | Equip | walks through every slot that has a candidate (weapon, armor, shield, helmet, gauntlets, misc) and asks which one | number, Return for none | - | - | `camp_equip`, `camp_equip_armor` | shown |
| Player verbs | Maze utilities | T)ime sets the message delay (1-5000); I)nspect searches the square for the bodies of other parties; S)tatus and Q)uick showed no change in a still picture | `T I S Q` | delay 1-5000 | - | `gameplay_time_delay`, `gameplay_inspect_none` | shown (T, I); open (S, Q) |
| Player verbs | Search at statues | some message squares ask "SEARCH (Y/N) ?"; searching gives the square's item | `Y N` | - | - | `system_search`, `system_search_found` | shown |
| Characters and progression | Creation | a new name, optional password (typed twice), race (5), alignment (3), bonus points onto six scores, a class the scores allow, keep or discard | typed name, letters, `+ -`, Return, Esc, `Y N` | elf base 7 10 10 6 9 6; bonus 8 here (7 in the scout's roll); new mage: 2 hit points, 170 gold | §4 | `create_new_name`, `create_password`, `create_password_again`, `create_race`, `create_align`, `create_bonus`, `create_bonus_minus`, `create_bonus_spent`, `create_class`, `create_keep`, `training_inspect_new` | shown |
| Characters and progression | Classes | fighter, mage, priest, thief, bishop, samurai, lord, ninja; the list beside the scores shows the ones open: STR 11 fighter, IQ 11 mage, AGI 11 thief (priest needs good or evil) | class letter | 8 classes | content §6 | `create_bonus_spent`, `inventory_sheet_ninja`, `inventory_sheet_samurai`, `inventory_sheet_lord` | shown |
| Characters and progression | Class change | Training Grounds C)hange class lists the other classes the scores allow; the change resets the scores to the race's base and adds years (19 to 25 here), level 1 | letter | +6 years, scores 11 11 10 7 11 6 back to 7 10 10 6 9 6 | [findings](findings.md) | `training_change_class`, `training_class_changed`, `training_class_changed_sheet` | shown |
| Characters and progression | Character records | typing a known name (and its password) opens inspect, delete, reroll (the creation form again under the same name), change class, set new password | name, `I D R C S` | 20 roster places | - | `training_name_password`, `training_char_menu`, `training_delete`, `training_reroll`, `training_password`, `training_no_room`, `menu_roster`, `menu_roster_inherited` | shown |
| Characters and progression | Levels | experience comes from fights; a level is made only by staying at the Inn: each score may rise or fall, casters learn spells | Inn stay | fighter: level 2 at 1000; level 14 needs 257,878 more at 431,906 | §5 | `inn_stables`, `inn_levelup`, `inn_levelup_mage`, `inn_stables_vet`, `ending_inn` | shown |
| Characters and progression | Age | shown in years on the sheet; Inn weeks and class changes add to it; "YOU HAVE DIED OF OLD AGE" exists **(program text)** | - | new characters 19 | - | `inventory_sheet_l1`, `inventory_sheet_mage` | shown (sheet); described (old age: not reached) |
| Characters and progression | The chevron | the mark `">"` after the name of a character who finished the quest | - | - | §7 | `ending_chevron`, `inventory_sheet_lord` | shown |
| Resources and economy | Gold | each member carries gold; from creation and chests, spent at the Inn, Temple and trading post; T)rade moves gold and items between members | `T`, amount, item number | chest shares 5 and 58 GP | - | `inventory_trade`, `inventory_trade_gold`, `inventory_trade_item`, `chest_gold`, `chest_gold_58` | shown |
| Resources and economy | Trading post | sells from a finite stock list at list price, buys at half, identifies and uncurses for half the item's price; warns before a class buys what it cannot use | `B S U I L`; `P F B S L` | Latumofis potion 300; Dios potion sells for 250; identify dragon slayer 5000; uncurse robe 4000 | content §4 | `shop_boltac_who`, `shop_boltac`, `shop_boltac_buy`, `shop_purchase`, `shop_bought`, `shop_unusable`, `shop_sell`, `shop_sold`, `shop_identify`, `shop_identified`, `shop_uncurse`, `shop_uncursed` | shown |
| Resources and economy | Inn | stables free (no healing), cots 10, economy 50, merchant 200, royal 500 gold per week; hit points return week by week while gold counts down; every stay ends with the level check | number, `A`-`E` | cots: 1 hit point a week; royal suite: 10 a week | §5 | `menu_inn_who`, `menu_inn`, `inn_healing`, `inn_royal` | shown |
| Resources and economy | Temple of Cant | helps only characters who are not in the party: a donation by level, paid by a party member; dead 250, ashes 500 gold per level | typed name, payer's number | 3250 and 6500 at level 13; the raised character has 1 hit point | §5 | `menu_temple`, `temple_not_here`, `temple_is_ok`, `temple_donation`, `temple_ritual`, `temple_healed`, `temple_healed_sheet`, `temple_ashes_donation`, `temple_cheap` | shown |
| Resources and economy | Spell points | per spell level 1-7, mage and priest lists apart, shown as 9/8/7/6/5/4/2; a cast takes one of its level, also when MALOR is cancelled | - | - | content §5 | `inventory_spellbooks`, `inventory_sheet_priest`, `inventory_sheet_bishop` | shown |
| Conflict | Rounds | every able member gets an order, Return starts the round (B goes back), then blows and spells play as timed messages | `F S P R U D`, Return, `B` | a message stays about 80-160 frames at the default delay | §6 | `battle_slimes`, `battle_orders`, `battle_kill`, `battle_multi_hit`, `battle_round2` | shown |
| Conflict | Front and back rank | members 1-3 may F)ight; 4-6 are offered spell, parry, run, use only | - | 3 in front | - | `battle_slimes`, `battle_spell_prompt`, `battle_three_dead` | shown |
| Conflict | Targets | with more than one group F)ight and group spells ask for the group number | `1`-`4` | up to 4 groups | - | `battle_group_select`, `battle_spell_group`, `battle_f8_demon` | shown |
| Conflict | Surprise | "YOU SURPRISED THE MONSTERS!" gives the party a free round without S)pell on floor 1; "THE MONSTERS SURPRISED YOU!" gives the monsters theirs | - | - | §6 | `battle_f1_skeletons`, `battle_surprised`, `battle_encounter`, `boss_werdna`, `boss_werdna_spell` | shown |
| Conflict | Friendly groups | a group may hail the party: F)ight or L)eave in peace; leaving costs nothing | `F L` | - | [findings](findings.md) | `battle_friendly`, `battle_friendly_thieves`, `battle_f7_friendly_daimyos`, `boss_werdna_friendly`, `boss_friendly_left` | shown |
| Conflict | Monster identification | groups appear under a generic name (Slimes, Small humanoids, Unseen entity) or their real one (Bubbly slimes, Vampire lord); the roll is per fight | - | - | content §3 | `battle_f1_small_humanoids`, `battle_f1_bubbly_slimes`, `battle_f1_kobolds`, `boss_werdna_geared` | shown |
| Conflict | Dispell | a priest dissolves undead; dissolved monsters give no experience | `D` | 0 experience points | - | `battle_f9_unseen_entity`, `battle_dispell`, `battle_dispell_ep` | shown |
| Conflict | Use item | U)se lists the member's items; a potion casts its spell (Dios: "FULLY HEALED") | `U`, item number, target | - | - | `battle_use_item`, `battle_potion`, `camp_use_item`, `camp_use_whom` | shown |
| Conflict | Run | R)un is tried at once for the whole party: success puts it back in the maze, failure gives the monsters a round | `R` | 2 of 7 timings fled from four Gaze-hound-like animals on floor 9 | - | `battle_run`, `battle_run_failed` | shown |
| Conflict | Parry | P)arry spends the member's turn defending | `P` | - | - | `battle_orders`, `battle_enemy_spell` | shown |
| Conflict | Status conditions | poison from a bite, sleep (KATINO), death in battle ("IS SLAIN!", "DIES!"), ashes, lost; dead members drop to the end of the party | - | - | §6 | `battle_poisoned`, `battle_katino`, `battle_not_slept`, `battle_slain`, `boss_member_dies`, `boss_four_dead` | shown |
| Conflict | Spell resistance | a spell can leave its target untouched: "IS UNAFFECTED!" | - | - | - | `battle_unaffected`, `battle_demon_unaffected`, `boss_spell_unaffected` | shown |
| Conflict | Level drain and paralysis | a vampire's touch paralyzes and drains levels in the same blow; the paralyzed member drops to the end of the party (`P-LYZE`) | - | 2 levels and 4 damage in one touch; 4 levels in the scout's run | §6 | `boss_paralyzed`, `boss_level_drain`, `boss_round2` | shown (stoning: scout only, no shot) |
| Opponents | Groups and pictures | up to four groups with counts and, in brackets, how many can act; one picture (the first group's) | - | 101 monsters, 20 pictures (disk data) | content §3 | `battle_f1_two_groups`, `battle_f9_three_groups`, `battle_f8_demon` | shown |
| Opponents | Monster spells and breath | casters "CAST A SPELL" for damage or sleep, named only in some result lines ("IS HIT BY MABADI!"); dragon flies breathe on every member | - | arch mage 3 and 7 damage; breath 4-7; Werdna 57-104 a member | content §3 | `battle_enemy_spell`, `battle_gas_spell`, `battle_breath`, `boss_werdna_spell`, `boss_vampire_spell`, `boss_mabadi` | shown |
| Opponents | Reinforcements and flight | a monster may call for help (heard or not: the group grows) or flee | - | 3 animals became 4 | - | `battle_call_for_help`, `battle_help_heard`, `battle_flees` | shown |
| Opponents | Fixed fights | squares and rooms that always start a fight: floor 3 (13,17), floor 4 guard rooms, the rooms behind some messages, Werdna | - | - | [maps](maps/floors.txt) | `battle_f3_dragon_flies`, `battle_f4_fixed`, `battle_f2_priests`, `battle_f1_kobolds`, `boss_werdna` | shown |
| Opponents | Random encounters | entering a room through its door, or turning inside one, can start a fight with a group from the floor's table | - | - | playbook | `battle_f1_skeletons`, `battle_f7_ninjas`, `battle_f8_trolls`, `battle_f9_gaze_hounds`, `battle_f10_giant`, `battle_f3_wolves`, `battle_f3_gargoyles`, `battle_f7_four_groups` | shown |
| Items and equipment | Equipment and marks | weapon, armor, shield, helmet, gauntlets, misc; `*` equipped, `-` cursed, `?` unknown, `#` unusable by the class; armour class falls from 10 | E)quip | AC -4 with plate mail + 2, shield + 2, helm + 1 | content §4 | `inventory_sheet_vet`, `inventory_cursed`, `inventory_sheet_jib`, `menu_castle_vets` | shown |
| Items and equipment | Drop | D)rop removes an item for good | `D`, number, 0 to leave | - | - | `inventory_drop`, `inventory_dropped` | shown |
| Items and equipment | Chests and traps | a won fight may leave a chest: inspect (thief) or Calfo (priest) names the trap, disarm needs the name typed, open sets a trap off; then items and gold | `O C L I D`, number, typed name | crossbow bolt; 58 GP a share | §6 | `battle_chest`, `chest_inspect_who`, `chest_inspected`, `chest_open_who`, `chest_disarm_prompt`, `chest_not_trapped`, `chest_calfo_who`, `chest_calfo`, `chest_crossbow_bolt`, `chest_item_found`, `chest_disarmed` | shown |
| Items and equipment | Identification and curses | found items are unknown (`?SWORD`); a bishop identifies for free in camp, the trading post for gold; a cursed item is removed by U)ncurse | `I`, `U` | - | - | `inventory_bishop_identify`, `inventory_identified`, `shop_identify`, `shop_identified`, `shop_uncurse`, `shop_uncursed` | shown |
| Abilities and magic | Spells | typed by name in battle and camp; 21 mage and 29 priest spells in 7 levels; battle messages say only "CASTS A SPELL" | `S`, name, Return, target | - | content §5 | `battle_spell_prompt`, `battle_cast`, `battle_mahalito`, `battle_malikto`, `battle_tiltowait`, `inventory_mage_book`, `inventory_priest_book`, `camp_cast_whom` | shown |
| Abilities and magic | DUMAPIC | reports facing, squares east and north of the castle stairs, and levels below | camp `S` | - | - | `system_dumapic`, `system_dumapic_f4` | shown |
| Abilities and magic | MALOR | teleports by a displacement set with N S E W U D; into rock the party bounces back; above the castle it falls to its death; Esc cancels but the spell point is spent | camp `S`, keys, Return, Esc | one level up from floor 1 is the Castle (safe); two up kills all six | [findings](findings.md) | `camp_malor`, `camp_malor_set`, `camp_malor_bounce`, `camp_malor_home`, `gameover_malor_midair` | shown |
| World and navigation | Maze | ten floors of 20 x 20 squares; stairs with a Y/N prompt; an elevator for floors 1-4 (buttons A-D) and one for 4-9 (A-F) | `Y N`, button letter, Return | 10 floors | [maps](maps/floors.txt) | `gameplay_stairs`, `gameplay_stairs_down`, `gameplay_elevator`, `gameplay_elevator_f2`, `gameplay_elevator_f4` | shown |
| World and navigation | Traps of the maze | pits, a chute (floor 9 to 10), darkness, anti-magic squares where spells fail, spinners and teleporters (silent) | - | positions in the maps | [maps](maps/floors.txt) | `gameplay_pit`, `gameplay_chute`, `gameplay_dark`, `system_fizzle` | shown (spinners and teleporters described: nothing is drawn or said) |
| World and navigation | Signs and scenes | message squares: signs, statues, placards, smoke and fog; long ones page with "[RET] FOR MORE" | Return | about 40 squares | content §2 | `dialogue_sign_f1`, `dialogue_f1_chicken`, `dialogue_f1_altar`, `dialogue_f2_placard`, `dialogue_f2_frog`, `dialogue_f2_bear`, `dialogue_f3_mosaic`, `dialogue_f4_control`, `dialogue_f4_treasure`, `dialogue_f4_allocation`, `dialogue_f4_desk`, `dialogue_f4_private`, `dialogue_f4_alarm`, `dialogue_f4_alarm_guardians`, `dialogue_f10_plaque`, `dialogue_f10_plaque_2`, `dialogue_f10_plaque_3`, `dialogue_f10_guardians`, `dialogue_werdna_sign` | shown |
| World and navigation | The way out by magic | the robed man of floor 1 (9,19) sends the party to the Castle | Return | - | - | `dialogue_f1_mapiro` | shown |
| Goals and gating | Main goal | Werdna's amulet on floor 10 (17,3), carried up to the Castle | - | reward 250,000 experience points each | §7 | `boss_amulet_found`, `inventory_amulet`, `gameplay_stairs_amulet`, `ending_congratulations` | shown |
| Goals and gating | Gates | rooms that need an item: bronze smoke, silver fog, a door nobody can break down, the private elevator that puts a party without the blue ribbon to sleep, the sliding wall with the bear | - | - | content §2 | `dialogue_f2_bronze_smoke`, `dialogue_f2_silver_fog`, `dialogue_f2_silver_fog_flee`, `dialogue_f2_door`, `dialogue_f4_asleep`, `dialogue_f4_asleep_outside`, `dialogue_f4_bear_wall` | shown |
| Goals and gating | The price of the ending | all equipment and all gold above the last four digits are taken; the chevron and the experience stay | - | 24,817 -> 4,817 gold; AC back to 10 | [findings](findings.md) | `ending_castle`, `ending_chevron` | shown |
| Chance | Random rolls | hit points and gold at creation, level-up changes, encounters, surprise, identification, hits, spell effects, fleeing; with a fixed route they repeat | - | - | playbook | `inn_levelup`, `battle_not_slept`, `battle_run_failed` | shown |
| Failure and recovery | Death and the cemetery | a party killed to the last member is shown as six tombstones; the dead stay on the roster marked DEAD until a temple visit | Return | - | §6 | `gameover_cemetery`, `gameover_roster_dead`, `battle_three_dead` | shown |
| Saving and sessions | The roster disk | characters are written when made, when the party changes and on L)eave the game; a disbanded party stays in the maze as OUT | Edge of Town `L` | 20 places | playbook Saves | `save_leave_game`, `camp_disband`, `boot_disk_master`, `boot_disk_duplicate` | shown |
| Saving and sessions | Utilities | on the boot menu: recover OUT characters, transfer between scenario disks, backup, make a scenario disk, update the disk, change names; each asks for disks | `U`, then `R T B M U C L` | - | - | `menu_utilities`, `util_change_names`, `util_change_names_disk`, `util_transfer`, `util_transfer_disk`, `util_backup`, `util_backup_dir`, `util_recover`, `util_recover_disk`, `util_update`, `util_update_step1`, `util_make_scenario` | shown (first screens; none was run to the end) |
| Pacing and difficulty | Ramp | floor 1 slimes fall to level 1 fighters in one round; a level 1 party on floor 8 loses its front rank in one; Werdna's first spell kills four level 13 members when he surprises them and he dies in one round when surprised | - | Werdna's spell 57-104 damage a member | §6 | `battle_kill`, `battle_l1_floor8`, `battle_slain`, `boss_four_dead`, `boss_werdna_killed` | shown |

## 3. How the systems feed each other
- Fights give experience and chests; chests give gold and unidentified items (`battle_victory`, `chest_item_found`).
- Gold buys gear (armour class), Inn weeks (healing, levels) and Temple cures (`shop_boltac_buy`, `menu_inn`, `temple_donation`).
- Experience becomes a level only at the Inn; levels change the scores, give hit points and spells
  (`inn_levelup`, `inn_levelup_mage`).
- The ending resets wealth (no items, little gold) but leaves levels and adds experience: the characters go
  on to the next scenario **(verified: `ending_chevron`; inferred: the purpose)**.

## 4. Character creation (verified, `create_*`)
1. A name that is not on the roster asks "DO YOU WANT TO CREATE IT (Y/N) ?"; with 20 characters on the disk
   it answers "THERE IS NO ROOM LEFT - TRY DELETING" (`training_no_room`).
2. Password, typed twice; Return for none.
3. Race: human, elf, dwarf, gnome, hobbit. The elf's base scores: STR 7, IQ 10, PIE 10, VIT 6, AGI 9, LUC 6.
4. Alignment: good, neutral, evil.
5. Bonus points (8 in the shots): `+` and `-` change the marked score, Return moves to the next one, Esc
   goes on only when no point is left. The classes the scores allow appear beside them as they change.
6. Class letter, then "KEEP THIS CHARACTER (Y/N)?". The new mage has 2 hit points, 170 gold, age 19 and two
   level 1 spell points (`training_inspect_new`).

## 5. Castle services (verified)
- **Tavern**: every added name is asked for its password, set or not. Errors: `** WHO? **`, `** THATS NOT IT
  **`, `** BAD ALIGNMENT **`.
- **Inn**: who stays, then a room. A paid room heals week by week and takes its price each week until the
  member is whole or broke; every room, the stables too, ends with "YOU NEED n MORE EXPERIENCE POINTS TO MAKE
  LEVEL" or "YOU MADE A LEVEL!" with one line per score gained or lost and "YOU LEARNED NEW SPELLS!!!!" for
  casters. The party table on that screen is not redrawn.
- **Temple**: the name of the character to help is typed. A party member "IS NOT HERE"; a healthy one "IS
  OK". For a dead or ashen character out of the party it names the donation and asks who tithes; a member
  without enough gold gets "** CHEAP APOSTATES! OUT! **". The ritual prints "MURMUR - CHANT - PRAY -
  INVOKE!" word by word. Both the dead and the ashen CONDI came back ("IS WELL") with 1 hit point; a failed
  ritual was not seen.
- **Trading post**: one member enters. The stock is a list of 31 kinds scrolled six at a time (F and B move
  five places, S returns to the start); bought items leave the stock when it runs out **(source: DOS
  documents)**. Sell, identify and uncurse list the pack with half the list price as the offer or the fee.

## 6. Combat (verified)
- Each blow is one message block: "CONDI THRUSTS AT A SLIME AND HITS 1 TIMES FOR 4 DAMAGE! CONDI KILLS
  ONE!"; level 13 fighters hit 2-3 times a round (`battle_multi_hit`, `battle_demon_stab`, `boss_werdna_chop`).
- Spells are announced as "NAME CASTS A SPELL" and then one line per target: damage and "DIES!", "IS
  SLEPT" / "IS NOT SLEPT", "IS UNAFFECTED!", "IS FULLY HEALED".
- After a fight: "FOR KILLING THE MONSTERS EACH SURVIVOR GETS n EXPERIENCE POINTS" (27 for three slimes, 0
  for a dissolved undead, 4421 for Werdna and two vampires), then a chest or nothing.
- Chest: the level 1 chest was trapless (inspect says so; disarm answers "THE CHEST WAS NOT TRAPPED"); the
  floor 9 chest held a crossbow bolt that Calfo and the thief both named; opened anyway it went off
  ("OOPPS! A CROSSBOW BOLT") and still gave a SWORD and 58 GP a share. The thief typing CROSSBOW BOLT disarmed it
  ("YOU DISARMED IT!"); the fighter typing the same name set it off (`chest_disarmed`).
- Werdna (`boss_*`): met with two "unseen entities" (a Vampire lord and a Vampire when named). When the
  party surprises them, MALIKTO, TILTOWAIT and LAHALITO plus two fighters end the fight in the free round:
  TILTOWAIT 75 and 70 on the vampires and 69 on Werdna, LAHALITO "IS UNAFFECTED", RYZ's three hits for 15
  kill him. When they surprise the party, Werdna's spell does 57-104 to every member and the vampires' spells
  finish the wounded: four dead before the first order.

## 7. The ending (verified, `ending_*`)
Climbing the floor 1 stairs with the amulet shows the Congratulations text: 250,000 experience points each,
the chevron, and the loss of all equipment and most gold. The Castle then shows the six at armour class 10;
at the Inn RYZ still needs 3457 points for level 14 (`ending_inn`): the boon is less than one level at that height. The game goes on as before.

## Open questions
- What S)tatus and Q)uick plot change in the maze (no change in a still frame).
- Stoning was seen by the scout only; no shot.
- A failed Temple ritual, old age, and the trap kinds other than the crossbow bolt were not seen.
- Level tables, hit and damage rules: the DOS documents' (`../../../dos/wizardry/design/systems.md`), not re-measured here.
