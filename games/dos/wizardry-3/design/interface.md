# Wizardry III: Legacy of Llylgamyn (DOS) - interface (UI/UX lens)

Every screen, menu, prompt and on-screen element of the game, described as an interface: what it is for, what
it shows, what it accepts, how it answers. Read it to study how the game talks to the player. The same shots
also appear in [systems.md](systems.md), which looks at the rules, and in [content.md](content.md), which shows
the variety of what fills the game; overlap is intended.
Notation: [README.md](README.md). Check: `python3 tools/lenses.py dos/wizardry-3`.

Facts carry a confidence tag as everywhere in this folder. A judgement (clear, slow, easy to miss) is written
as **Observation:** with the reason, never as a fact. All rows (verified) in set `main`, 2026-11-19.

## 1. Conventions
- **Input:** keyboard only; every menu entry is chosen by its initial letter or a digit, Enter (drawn as a bent
  arrow) leaves or confirms; roster lists by letter, party members by digit; prompts take Y/N; riddles,
  passwords, spells and trap names are typed (`dialogue_f2_answer_air`, `battle_spell_prompt`,
  `chest_disarm_prompt`). Keys pressed during a "One moment" load are lost (`gameplay_one_moment`).
- **Layout:** 320 x 200, white frames on black, pictures in cyan and magenta; a framed title tab ("LLYLGAMYN",
  "CAMP", "TRAINING GROUNDS", "MOVE CHARACTERS:") names the place (`menu_castle_start`, `camp_menu`). The party
  list (# name class AC hits status) fills the bottom of the Castle, camp, maze and combat screens.
- **Text:** capitals only; "OF" drawn as one ligature glyph in item names ("CRYSTAL♡GOOD"); potions start with
  "&", scrolls with a scroll sign; "?" before an unknown item, "*" before an equipped one, "-" before a cursed one,
  "#" before one the character cannot use (`inventory_crystals`, `shop_uncurse`).
- **Feedback:** messages in boxes over the view, long ones with "PRESS ↵"; refusals in boxes ("* Bad
  alignment *", "You can't walk through walls!", "That character is already a legacy!", "You are forbidden to
  enter here! Begone!!", "* You cannot afford our fee *"); shop replies between stars ("* Just what you needed
  *", "* Anything else, noble sir? *").
- **State visibility:** the status column shows the maximum hit points when all is well, the order given during
  a battle round (FIGHT, PARRY, the spell's first six letters, "??????" while not yet given) and conditions
  (DEAD, PARALY, PETRIF, ASHES) (`battle_orders`, `boss_guardian_good_r4`); place and facing are not shown (DUMAPIC
  tells them, `system_dumapic`).
- **Help and onboarding:** none in the game; the 1998 package's run.bat prints the transfer steps.

## 2. Screen inventory
| Screen / element | Type | Reached from -> leads to | Purpose | Shows | Accepts | Feedback and errors | Shots | Observation |
|---|---|---|---|---|---|---|---|---|
| Title | screen | power-on -> Castle | start or make a disk | logo, scenario name, a monster | S, M | - | `title_screen` | |
| Make scenario disk | prompt | title M | copy a scenario disk | "The disk you inserted has data on it ... (Y/N)?" | Y/N | - | `menu_make_scenario` | not followed past the prompt |
| Disk and loading prompts | message | title S | the 1980s disk handling | "Place duplicate scenario diskette in drive 1", "Now loading the program into memory" | none (the loader answers) | - | `boot_disk_prompt`, `boot_loading` | |
| Castle "Llylgamyn" | menu | title, Edge -> Tavern, Inn, Temple, Boltac's, Edge | town hub | five places, party list | G A T B E | - | `menu_castle_empty`, `menu_castle_start`, `menu_castle_geared`, `menu_castle_half2`, `menu_castle_paralyzed`, `menu_castle_after_ending` | |
| Gilgamesh's Tavern | menu | Castle | form the party | A)dd R)emove #)Inspect D)ivvy gold | letters, digits | "* Bad alignment *" in the title frame | `menu_tavern`, `tavern_add`, `tavern_remove`, `menu_tavern_stock`, `menu_tavern_bad_alignment` | **Observation:** the add list shows only characters free to join, letters stay fixed while adding |
| Edge of Town | menu | Castle -> Training, Maze, Utilities, Leave | leave town | five entries | T M C U L | - | `menu_edge_empty` | |
| Wizardry Utilities | menu | Edge -> Move characters | disk work | C)hange name M)ove characters R)estart an "out" party | C M R, Enter (to the Castle) | - | `menu_utilities` | |
| Move characters | list | Utilities | import from Wizardry I/II | the source scenario, then the old roster with "+" marks, then progress boxes per character | 1/2, letters, Enter, Esc | "RYZ has been moved" | `system_move_scenario`, `system_move_list`, `system_move_marked`, `system_move_removing`, `system_move_insert`, `system_move_moving`, `system_move_moved` | **Observation:** the destination-disk prompt is answered by the 1998 loader |
| Training Grounds | menu | Edge | manage characters | I)nspect R)oster Leave (no create) | I R | - | `menu_training`, `training_pick`, `inventory_roster` | |
| Character options | menu | Training inspect | per character | L)egate I)nspect D)elete C)hange class A)lter password | letters | "That character is already a legacy!" | `menu_char_options`, `menu_already_legacy` | |
| Rite of passage | message + prompt | L)egate | the legacy | ceremony text, then "Choose an alignment for descendant" with only the allowed letters | Enter, A/B/C | other letters ignored | `dialogue_rite`, `menu_alignment`, `menu_alignment_thief` | |
| Character sheet | screen | Tavern, Training, camp | statistics and pack | name, level, alignment-class, race, awards in quotes, six statistics, gold, E.P., HP, AC, age, status, spell points, items 1-8 | R T P S E D I U, Enter | - | `inventory_stock_klindt`, `inventory_ancestor_sheet`, `inventory_descendant_sheet`, `inventory_descendant_evil`, `inventory_sheet_geared`, `inventory_sheet_priest`, `inventory_star_sheet`, `inventory_bearer_after` | |
| Boltac's | menu + list | Castle | trade | "Who will enter?", then the menu with gold, pages of six items with prices, the member's pack with sale prices | B S U I P, F/B pages, digits | "Unusable item - buy it (Y/N)?", "* You cannot afford our fee *" | `shop_boltac_who`, `shop_boltac`, `shop_boltac_buy`, `shop_boltac_shields`, `shop_boltac_armor`, `shop_purchase`, `shop_bought`, `shop_boltac_magic`, `shop_unusable`, `shop_sell`, `shop_sold`, `shop_identify_fee`, `shop_pool`, `shop_identified`, `shop_uncurse`, `shop_uncursed` | |
| Adventurer's Inn | menu | Castle | rest | "Who will stay?", five rooms with prices, P)ool gold | digit, A-E | level-up page "You made the next level!" | `menu_inn_who`, `menu_inn`, `inn_recuperating`, `inn_levelup` | |
| Temple of Cant | menu | Castle | cure | the roster in need by letter, the donation, "Murmur - chant - pray - invoke!" and the result | letter, digit | "* CUBI has been cured *", "* CONDI needs KADORTO now *" | `temple_paralyzed`, `temple_petrified`, `temple_donation`, `temple_murmur`, `temple_cured`, `temple_dead`, `temple_resurrect_fee`, `temple_failed` | **Observation:** the chant is spelled out word by word over about half a second each |
| Camp | menu | entering the maze, C | between steps | #)Inspect R)eorder E)quip Leave | digits, letters | - | `camp_menu`, `camp_equipped`, `camp_reorder` | |
| Equip | prompt | camp E, sheet E | wear items | "Select weapon/armor ... Equip which (#)?" one slot after another, then the invoke question for items with powers | digits, Enter, Y/N | - | `camp_equip`, `camp_equip_armor`, `invoke_evil_prompt`, `invoke_good_prompt` | **Observation:** the crystals' power hides behind E)quip, not U)se, so it is easy to miss |
| Sheet commands in camp | prompt | sheet | spells and items | "Cast what spell?", "Cast on whom?", "Use item?", "Drop item?", "Trade with whom?", "Trade item?", identify results | typed names, digits | "You don't have a clue!", "You identified it!" | `camp_cast_what`, `camp_cast_whom`, `camp_use_item`, `camp_drop`, `camp_pool`, `inventory_trade`, `inventory_trade_item`, `inventory_bishop_noclue`, `inventory_bishop_identify`, `inventory_unidentified` | |
| Spell books | list | sheet R | read the spells known | known counts per level, then the mage or priest list | M P, Enter | - | `inventory_read`, `inventory_mage_book`, `inventory_priest_book` | |
| Party position / teleport | message, menu | DUMAPIC, MALOR | where am I / go | "Facing north. 0 east 0 north 1 up."; east/north/up counters with a key menu | E W N S U D T Q | - | `system_dumapic`, `camp_malor` | |
| Maze view | screen | camp -> fights, messages, stairs | explore | command bar, wireframe view (doors as frames, stairs as hatched bars, dark squares hatched grey), party list | W A D K C S I O | "You can't walk through walls!" | `gameplay_maze_f1_start`, `gameplay_wall`, `gameplay_door`, `gameplay_status_off`, `gameplay_full_view`, `gameplay_inspect`, `gameplay_f2`, `gameplay_f3`, `gameplay_f4`, `gameplay_f5`, `gameplay_f5_dark`, `gameplay_f6` | **Observation:** floor views look alike; only messages tell the floors apart |
| Stairs prompt | prompt | stairs squares | change floor | "Stairs up/down, take them (Y/N)?" | Y N | refusal box | `gameplay_stairs_castle`, `gameplay_stairs_up`, `gameplay_stairs_down`, `gameplay_f6_arrival`, `gameplay_teleport_home`, `gameplay_forbidden` | |
| One moment | transition | stairs to floors 5 and 6, chutes | loading | "One moment" box | none (keys lost) | - | `gameplay_one_moment` | **Observation:** up to 30 seconds at 8088 speed |
| Trap squares | message | pit, chute, "Look out!" | danger | "A pit!", "A chute!", "Look out!" | - | hit points lost | `gameplay_pit`, `gameplay_chute`, `dialogue_f4_look_out` | |
| Message box | message | special squares | story, signs, NPCs | text, sometimes a picture, "PRESS ↵" | Enter | - | `dialogue_f1_beach`, `dialogue_f1_water`, `dialogue_f1_fortress`, `dialogue_f1_barracks`, `dialogue_f1_lkbreth`, `dialogue_f2_pole`, `dialogue_f2_dining`, `dialogue_f2_wine_cellar`, `dialogue_f2_desk`, `dialogue_f2_whip`, `dialogue_f3_turn_back`, `dialogue_f3_direction`, `dialogue_f3_monk`, `dialogue_f3_pool`, `dialogue_f3_graveyard`, `dialogue_f3_crock`, `dialogue_f3_further`, `dialogue_f3_taxi`, `dialogue_f4_oily`, `dialogue_f4_abdul`, `dialogue_f5_taxi`, `dialogue_f5_fung`, `dialogue_radiant_statue`, `dialogue_lkbreth_farewell` | |
| Search prompt | prompt | search squares | take or swap items | "You have reached the statue." / the text, then "Will you search (Y/N)?"; "RYZ got an item.", "KLINDT traded an item!" | Y N | - | `dialogue_f2_desk_search`, `dialogue_f2_desk_found`, `dialogue_f3_monk_traded`, `dialogue_f3_pool_traded`, `dialogue_statue_reached`, `dialogue_statue_xeno`, `dialogue_search` | |
| Riddle prompt | prompt | riddle squares | gate | the riddle page, then "What is your answer ?" with a cursor | text, Enter | wrong: pushed back | `dialogue_f2_riddle_air`, `dialogue_f2_answer_air`, `gameplay_riddle_wrong`, `dialogue_f2_password`, `dialogue_f4_riddle_fire`, `dialogue_f4_answer_fire`, `dialogue_f5_riddle_chariot`, `dialogue_f5_answer_chariot`, `dialogue_riddle_death`, `dialogue_answer_death`, `dialogue_riddle_wheel`, `dialogue_answer_wheel` | |
| Fee prompt | prompt | Abdul's squares | pay | "The fee is 2500. Will you pay (Y/N)?" | Y N | - | `dialogue_f3_taxi_fee` | |
| Combat | screen | fights | battle | groups with counts (alive in brackets), a picture per group, member options, messages one per action | F P S D U R T, digits | "Press Enter to fight, or T)ake back orders" | `battle_f1_ambush`, `battle_options_spell`, `battle_spell_prompt`, `battle_use_item`, `battle_orders_spells`, `battle_lahalito`, `battle_katino`, `battle_kill`, `battle_badios_wasted`, `battle_victory`, `battle_dispell_which`, `battle_dispell_fails`, `battle_orders`, `boss_montino` | **Observation:** group names stay generic until identified ("Living Legend" became "Delf" in round 2, `boss_delf_named`) |
| Chest | menu | after fights | loot | "A chest! You may: O)pen C)alfo L)eave alone I)nspect D)isarm", "Who (#) will ...?", "Trap (↵ exits)?" | O C L I D, digits, typed trap name | "You disarmed the trap!", "Oops! Teleporter" | `battle_chest`, `chest_inspect_who`, `chest_inspected`, `chest_calfo`, `chest_disarm_prompt`, `chest_disarmed`, `chest_found_jewelry`, `chest_found_rod`, `chest_trap_oops` | |
| Invoke messages | message | E)quip -> Y | the crystals | three verses (neutral invoker, single crystal, wrong crystal) or the pack changed in silence (right crystal) | Enter | ASHES in the status | `invoke_wrong`, `invoke_ashes`, `invoke_neutral`, `invoke_vanished`, `invoke_one_crystal`, `inventory_neutral_crystal` | **Observation:** success has no message; only the pack shows it |
| Cemetery | screen | a party wiped out | game over | four tombstones "RIP", "Your entire party has been slaughtered" | Enter | - | `gameover_slaughtered`, `gameover_cemetery` | |
| Ending | screens | the orb in the Castle | the end | Congratulations prompt, the Queen's page, one star prompt per roster character | Y N, Enter | - | `ending_congratulations`, `ending_gods_praised`, `ending_award_star` | |

## 3. Screen flow
```
power-on -> DOSBox Pure menu (front end) -> title -S-> disk prompt -> loading -> Castle
Castle -G-> Tavern | -A-> Inn | -T-> Temple | -B-> Boltac's | -E-> Edge of Town
Edge -T-> Training (inspect -> options -> L)egate rite -> alignment) -> Training
Edge -U-> Utilities -M-> Move characters (1/2 -> old roster -> moved) -> Castle
Edge -M-> camp -> maze <-> fights -> chest, messages, stairs, One moment; floor 1 (0,0) stairs down -> Castle
maze, refused floor -> "forbidden" -> Castle;  party wiped out -> cemetery -> Castle (empty)
Edge -L-> "Thanks for playing Wizardry!" (program ends)
Castle with the orb -> Congratulations -> the Queen's page -> star prompts -> Castle
```

## 4. Elements in detail
- **Maze screen:** command bar on top (one line); the wireframe view in the middle (doors as frames inside the
  wall, stairs as hatched bars, dark squares as a hatched grey fill, `gameplay_f5_dark`); the party list below
  with six rows (verified).
- **Character sheet:** first line "NAME L level A-CLA RACE "awards"" - the awards string is where the legacy and
  the star show (">DG" for RYZ after the rite, "*D" for KLINDT after the ending) (verified).
- **Combat screen:** groups at the top with the alive count in brackets, the options or message box in the
  middle, up to four pictures (one per group), the party list with the orders in the status column (verified).

## Open questions
- Utilities C)hange name and R)estart past their first screen, M)ake scenario disk after Y (not tried).
