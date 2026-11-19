# Wizardry II: The Knight of Diamonds (DOS) - interface (UI/UX lens)

Every screen, menu, prompt and on-screen element of the game, described as an interface: what it is for, what
it shows, what it accepts, how it answers. Read it to study how the game talks to the player. The same shots
also appear in [systems.md](systems.md), which looks at the rules, and in [content.md](content.md), which shows
the variety of what fills the game; overlap is intended.
Notation: [README.md](README.md). Check: `python3 tools/lenses.py dos/wizardry-2`.

Facts carry a confidence tag as everywhere in this folder. A judgement (clear, slow, easy to miss) is written
as **Observation:** with the reason, never as a fact.

## 1. Conventions
The interface is Wizardry I's (verified: identical layouts, fonts and keys; details in
[Wizardry I interface](../../wizardry/design/interface.md)). Short form and what differs:
- **Input:** keyboard only; one letter per menu entry (the letter before ")"), digits for party members,
  letters for roster characters, Enter (a bent arrow on screen) leaves or confirms, typed text for spells,
  trap names and riddle answers (verified: `battle_spell_prompt`, `chest_disarm_prompt`, `dialogue_f2_riddle_answer`).
- **Layout:** 320 x 200, CGA mode 5 shown with the cyan/magenta/white palette (white text, coloured monster
  pictures and the magenta title logo): a title box at the top ("LLYLGAMYN", "CAMP", "TRAINING GROUNDS",
  "MOVE CHARACTERS:"), the menu box in the middle, the party list at the bottom (# CHARACTER NAME CLASS AC HITS
  STATUS) (verified: `menu_castle`).
- **Text:** capitals only; long story texts fill the upper box and end with "PRESS ↵" (verified:
  `dialogue_f2_riddle`, `dialogue_sphinx`).
- **Feedback:** short messages in a box in the middle of the view ("YOU CAN'T WALK THROUGH WALLS!", "A PIT!",
  "OUCH!!", "* POWERLESS *"); in battle one line or two per action, each shown about 160 frames (verified).
- **State visibility:** the party list is always on screen: AC, hits (a "+" marks regeneration), status (OK
  as the maximum hits, POISON, DEAD, ASLEEP; in battle the order given: FIGHT, PARRY, the spell name; "??????"
  while orders are open) (verified: `battle_orders`, `gameplay_poisoned`, `battle_party_asleep`).
- **Help:** none on screen beyond the menus; the import is explained only by the 2019 `run.bat` text.

## 2. Screen inventory
| Screen / element | Type | Reached from -> leads to | Purpose | Shows | Accepts | Feedback and errors | Shots | Observation |
|---|---|---|---|---|---|---|---|---|
| Title and parade | screen | power-on -> scenario disk / Castle | start | logo, "Scenario #2 - The Knight of Diamonds", a monster picture that changes, S)tart / M)ake scenario disk | S, M | - | `title_screen`, `title_parade_four`, `title_parade_dwarves`, `title_parade_frog` | - |
| Make scenario disk | prompt | Title M | prepare a disk | "The disk you inserted has data on it ... Use it (Y/N)?" | Y, N | - | `menu_make_scenario` | - |
| Disk prompt and loading | transition | Title S -> Castle | load the program | "Place duplicate scenario diskette in drive 1, then press ↵" (answered by the 1998 loader), "Now loading the program into memory ..." | - | - | `boot_disk_prompt`, `boot_loading` | **Observation:** the prompt flashes by: the loader presses the key |
| Castle menu | menu | everywhere -> services | hub | Tavern, Inn, Temple, Boltac's, Edge of Town; the party list | G A T B E | - | `menu_castle_empty`, `menu_castle`, `menu_castle_geared`, `menu_castle_solo` | **Observation:** the imported party shows Wizardry I's AC until the first camp |
| Tavern | menu | Castle G | form the party | A)dd R)emove #)Inspect D)ivvy gold; the add list by roster letter | letters, digits | the list closes at six | `menu_tavern`, `menu_tavern_stock`, `menu_tavern_imported`, `tavern_adding`, `tavern_remove` | - |
| Character sheet | screen | Tavern #, camp #, Training I | look at a character | name, level, class, race, awards, statistics, gold, E.P., age, H.P., A.C., status, spell points, pack (* = equipped, # = unusable, ? = unidentified) | R T P S E D I U, Enter | - | `inventory_sheet_import`, `inventory_stock_caleb`, `inventory_sheet_geared`, `inventory_spellbooks`, `ending_sheet_ryz`, `ending_sheet_condi` | - |
| Spell books | screen | sheet R | read spells | the mage or priest list by level | M, P, Enter | - | `inventory_mage_book`, `inventory_priest_book` | - |
| Sheet prompts | prompt | sheet T, D, I, U, S | act on items | "Trade with whom (#)?", "Trade gold (amt)?", "Drop item (#)?", "You identified it!", "You don't have a clue!", "Cast on whom (#)?", "Use item (#)?" | digits, numbers | - | `inventory_trade`, `inventory_trade_gold`, `inventory_drop`, `inventory_bishop_noclue`, `inventory_bishop_identify`, `inventory_identified`, `camp_cast_whom`, `camp_use_item`, `inventory_staff_powerless` | - |
| Inn | menu | Castle A | rest, level up | "Who will stay?", the rooms and prices, recuperating counter, level message | digit, A-E, P | "You need N more E.P. to make the next level" | `menu_inn_who`, `menu_inn`, `inn_stables`, `inn_recuperating`, `ending_inn_levelup` | - |
| Temple | menu | Castle T | cure | "Who (letter) shall we help?", "The donation will be N. Who will tithe?", "Murmur - chant - pray - invoke!" | letter, digit | "* CONDI has been healed *" | `menu_temple_empty`, `temple_dead`, `temple_donation`, `temple_healed` | - |
| Boltac's | shop | Castle B | buy, sell, uncurse, identify, pool | "Who will enter?", the gold, the stock six items a page, the pack with prices | digits, B S U I P, P B F S | "* Just what you needed *", "Unusable item - buy it (Y/N)?", "* Anything else, noble sir? *" | `shop_boltac_who`, `shop_boltac`, `shop_boltac_buy`, `shop_boltac_armor`, `shop_boltac_potions`, `shop_boltac_magic`, `shop_boltac_rare`, `shop_purchase`, `shop_bought`, `shop_unusable`, `shop_sell`, `shop_sold`, `shop_pool`, `shop_identify`, `shop_identified`, `shop_uncurse`, `shop_uncursed`, `ending_rebuy` | **Observation:** USELESS marks in the stock tell a class what it cannot use before buying |
| Edge of Town | menu | Castle E | leave town | T)raining M)aze C)astle U)tilities L)eave game | T M C U L | - | `menu_edge` | - |
| Training Grounds | menu | Edge T | look at characters | I)nspect a character, R)oster of characters, Leave (no create) | I, R, Enter | - | `menu_training`, `training_pick`, `inventory_roster` | **Observation:** the menu shrinks to two entries, the only sign that this scenario cannot create characters |
| Wizardry Utilities | menu | Edge U | disk housekeeping | C)hange name, M)ove characters, R)estart an "out" party | C, M, R, Enter | "No characters are in the maze" | `menu_utilities`, `util_change_name`, `util_restart_none` | - |
| Move characters | list + messages | Utilities M -> Utilities | import | "Select chars by (letter), ↵ to move them, or (Esc) to exit without moving", the source roster in two columns; then "Removing ...", "Insert the destination scenario disk", "Moving ...", "RYZ has been moved" | letters (toggle "+"), Enter, Esc | a "+" replaces ")" after the letter | `system_move_list`, `system_move_marked`, `system_move_removing`, `system_move_insert`, `system_move_moving`, `system_move_moved` | **Observation:** the disk swap of the original is answered by the loader, so the player sees no wait |
| Camp | menu | maze C, entering the maze | prepare | #)Inspect R)eorder E)quip Leave; "Descending into the ruins under the Temple of Gnilda" on the way down | digits, R E, Enter | - | `gameplay_descending`, `camp_menu`, `camp_equipped`, `camp_reorder`, `inventory_kod_set`, `inventory_staff` | - |
| Equip | prompt | camp E | wear items | "Select weapon / armor / shield / helm / gauntlets - 1) ... Equip which (#)? ↵ for none" | digit, Enter | - | `camp_equip`, `camp_equip_gauntlets` | - |
| Camp spells | prompt | sheet S | cast | "Party teleport: east north up", "Party position: facing north, 0 east 0 north 1 down" | letters, Enter | - | `camp_malor`, `system_dumapic` | - |
| Maze view | screen | camp Leave | explore | wireframe corridor, doors as frames in walls, dark squares grey; command line "C)AMP S)TATUS I)NSPECT O)FF A-W-D K" | W A D K C S I O | message boxes | `gameplay_maze_f1_start`, `gameplay_door`, `gameplay_dark`, `gameplay_status_off`, `gameplay_full_view`, `gameplay_teleport_temple` | - |
| Maze messages | message | moves | report | "You can't walk through walls!", "A pit!", "Ouch!!", "One moment", "An encounter", "Searching....... Found: * no one *" | - | - | `gameplay_wall`, `gameplay_pit`, `gameplay_pit_damage`, `gameplay_ouch`, `gameplay_chute`, `gameplay_inspect_none`, `chest_alarm_encounter` | - |
| Stairs prompt | prompt | stairs squares | change floor | "Stairs up / Stairs down, take them (Y/N)?" | Y, N | - | `gameplay_stairs_up`, `gameplay_stairs_down` | - |
| Story pages | message | message squares | tell | up to 12 lines, "PRESS ↵" | Enter | - | `dialogue_f1_armor_clue`, `dialogue_f2_panel`, `dialogue_f2_three_roads`, `dialogue_f2_sage`, `dialogue_f2_sage_study`, `dialogue_f2_sage_spells`, `dialogue_f3_mapiro`, `dialogue_f3_line_of_work`, `dialogue_f4_fountain`, `dialogue_f4_cavern_sign`, `dialogue_f4_mountain`, `dialogue_f4_hall`, `dialogue_f4_cavern`, `dialogue_f4_cave_in`, `dialogue_f5_well`, `dialogue_f6_king_treasure`, `dialogue_f6_king_doom`, `dialogue_one_alone_real`, `dialogue_sphinx`, `dialogue_sphinx_2`, `dialogue_sphinx_3`, `dialogue_sphinx_4`, `dialogue_gnilda`, `dialogue_gnilda_2`, `dialogue_gnilda_fades`, `dialogue_staff_gift` | **Observation:** riddles and clues are plain text; the answer has to be remembered or written down |
| Riddle prompt | prompt | riddle squares | test | "What is your answer ?" (riddles) or "Your answer ? >" (Gnilda) with a cursor | text, Enter | none on a wrong answer: the party is one square back | `dialogue_f2_riddle_2`, `dialogue_f2_riddle_answer`, `dialogue_sphinx_answer`, `dialogue_gnilda_test`, `dialogue_gnilda_answer` | - |
| Fee and choice prompts | prompt | sage, well, fountain | pay, choose | "The fee is N. Will you pay (Y/N)?", "Thank you!", "Who (#) will wade?" | Y, N, digit | - | `dialogue_f2_sage_fee`, `dialogue_f2_sage_paid`, `dialogue_f5_well_fee`, `dialogue_f4_wade`, `gameplay_poisoned` | - |
| Battle screen | screen | encounters | fight | groups and counts at the top ("1) 3 RHINO BEETLES (3)"), the acting member's options, the monster picture, the party list with orders | F P S D U R T, digits, typed spells | one or two message lines per action | `battle_f2_rhino_beetles`, `battle_spell_prompt`, `battle_orders`, `battle_group_select`, `battle_dispell_which`, `battle_use_item`, `battle_round2`, `battle_f3_nightstalkers` | **Observation:** unidentified monsters keep a generic name ("animated object") until a later round |
| Battle messages | message | rounds | report | "CONDI charges at ... and hits 3 times for 18 damage", "... is killed!", "EBO casts a BADIOS", "An ogre lord casts a KATINO - CONDI is slept", "is drained one level!", "is decapitated!", "** You surprised the monsters! **" | - | - | `battle_multi_hit`, `battle_badios`, `battle_monster_hit`, `battle_halito`, `battle_lahalito`, `battle_lahalito_kill`, `battle_kill`, `battle_enemy_katino`, `battle_enemy_dilto`, `battle_party_asleep`, `battle_level_drain`, `battle_surprised_monsters`, `battle_run`, `boss_armor_killed`, `boss_shield_ebo_killed`, `boss_shield_tiltowait`, `boss_sword_decapitated`, `boss_sword_killed`, `boss_helm_lahalito`, `boss_helm_killed`, `boss_gauntlet_mahalito`, `boss_gauntlets_killed` | - |
| Friendly group | prompt | encounters | avoid a fight | "A friendly group of ... F)ight or L)eave" | F, L | - | `battle_friendly` | - |
| Rewards | message | battle end | report | "Each survivor gets N E.P.", "MNZ found : ARMOR", "Each survivor gets N G.P." | - | - | `battle_victory`, `boss_armor_ep`, `boss_found_armor`, `boss_found_shield`, `boss_found_sword`, `boss_found_helm`, `boss_found_gauntlets`, `chest_found_item`, `chest_gold` | - |
| Chest | menu | battle end | open treasure | "A chest! You may: O)pen C)alfo L)eave alone I)nspect D)isarm", "Who (#) will ...?", "Trap (↵ exits) ? >", the trap's name, "You disarmed the trap!", "Oops! Alarm" | O C L I D, digits, text | - | `battle_chest`, `chest_inspect_who`, `chest_inspected`, `chest_calfo_who`, `chest_disarm_prompt`, `chest_disarmed`, `chest_alarm` | - |
| Cemetery | screen | party wiped out | game over | tombstones, "Your entire party has been slaughtered. Press ↵ to leave the cemetery!" | Enter | - | `gameover_slaughtered`, `gameover_cemetery`, `gameplay_member_dead` | - |
| Congratulations | screen | Castle with the staff, alone | the ending | the text and "Press ↵ to select your knights!" | Enter | - | `ending_congratulations` | - |
| Make a knight | prompt | Congratulations -> each roster character -> Castle | choose companions | "Make CONDI a knight (Y/N)?" | Y, N | - | `ending_knight_caleb`, `ending_make_knight`, `ending_castle_knights`, `ending_final_party` | **Observation:** asked for every roster character, stock ones included, not only the bearer's companions |
| Leave game | screen | Edge L -> DOS | end the session | the loader's "Thanks for playing Wizardry!" in DOS text mode | - | - | `save_leave_game` | - |

## 3. Screen flow
Power-on (DOSBox Pure menu, WIZ2.COM) -> Title -> S -> (loader answers the disk prompt) -> Castle ->
Edge of Town -> Utilities -> Move characters -> moved messages -> Utilities -> Castle -> Tavern (add) ->
Castle -> Boltac's -> Edge of Town -> Maze -> camp (equip) -> maze view <-> battle / chest / message squares /
riddles -> stairs up at floor 1 (0,0) -> Castle; with the staff, alone: Congratulations -> Make ... a knight?
(each character) -> Castle. Leave game -> DOS ("Thanks for playing Wizardry!").

## 4. Elements in detail
Shared with Wizardry I (maze view, party list, battle screen, sheet): see its interface document. New here:
the award marks on the sheet's first line (`RYZ L 11 G-FIG HUMAN ">G"`, `ending_sheet_ryz`) and the "+"
after the hits of a regenerating character with "LO" as the AC of the bearer of the five pieces in the party
list (AC -18 on the sheet: `dialogue_gnilda_test`, `inventory_kod_set`).

## Open questions
- The sage's and the well's prompts after other answers; the floor 2 (16,3) message (not reached).
