# Wizardry: Proving Grounds of the Mad Overlord - interface (UI/UX lens)

Every screen, menu, prompt and on-screen element of the game, described as an interface: what it is for, what
it shows, what it accepts, how it answers. Read it to study how the game talks to the player. The same shots
also appear in [systems.md](systems.md), which looks at the rules, and in [content.md](content.md), which shows
the variety of what fills the game; overlap is intended.
Notation: [README.md](README.md). Check: `python3 tools/lenses.py apple2/wizardry`.

Facts carry a confidence tag as everywhere in this folder; every row of the inventory is **(verified)** by the
shots it names unless a cell says otherwise. A judgement (clear, slow, easy to miss) is written as
**Observation:** with the reason, never as a fact.

## 1. Conventions
- **Input:** keyboard only. A choice is one letter, printed in the text with a bracket (`A)DD A MEMBER`,
  `[A] THE STABLES`); party members are chosen by number 1-6; names of characters, spells and traps are typed
  and ended with Return; Return alone means leave, none or go on wherever the text says `[RETURN]` / `[RET]`;
  `0` leaves the item prompts **(verified)**. A wrong key is ignored without a message **(verified)**. Keys
  typed while the disk works are lost **(verified)**.
- **Layout:** two kinds of screen. Castle, Training Grounds, camp, sheets and shops are 40-column upper-case
  text: a framed header (`! CASTLE   MARKET !`, the right word names the place: MARKET, TAVERN, INN, TEMPLE,
  SHOP, EXIT), the party table, then the options as a sentence **(verified)**. The maze, fights and chests are
  a hi-res screen in four panes: the view or monster picture top left, commands or the monster groups top
  right with a `SPELLS :` line, a message pane in the middle, the party table at the bottom **(verified)**.
- **Text:** capitals only; white in text mode, green with purple frame lines in the hi-res panes on a colour
  set **(verified)**. Abbreviations in the party table: `G-FIG`, `N-THI` (alignment-class), `AC`, `HITS`,
  `STATUS` (the hit-point maximum when OK, else the condition) **(verified)**.
- **Feedback:** results are timed messages (the T)ime command sets the delay); errors and shop answers are
  short starred lines that vanish by themselves (`** WHO? **`, `** THATS NOT IT **`, `** JUST WHAT YOU NEEDED
  **`); irreversible steps ask (`ARE YOU SURE YOU WANT TO DELETE (Y/N) ?`, `CONFIRM (Y/N) ?`, `KEEP THIS
  CHARACTER (Y/N)? >`) **(verified)**.
- **State visibility:** the party table (class, armour class, hit points, status) is on almost every screen;
  gold, experience, age, spell points and the pack need the character sheet; the position needs the DUMAPIC
  spell; there is no map **(verified)**.
- **Help and onboarding:** every screen lists its own keys; the maze pane lists all commands permanently;
  nothing explains classes, spells or scores (the manual does) **(verified; the manual was not read)**.

## 2. Screen inventory
One row per screen, menu, prompt, dialog, message type and permanent on-screen element. Type: `screen`, `menu`,
`prompt`, `list`, `message`, `hud element`, `transition`.

| Screen / element | Type | Reached from -> leads to | Purpose | Shows | Accepts | Feedback and errors | Shots | Observation |
|---|---|---|---|---|---|---|---|---|
| Opening animation | transition | power-on -> title | sets the tone | "PREPARE YOURSELF FOR THE ULTIMATE IN FANTASY GAMES", the wizard at his cauldron, smoke forming the logo; loops | any key | - | `boot_prepare`, `title_cauldron`, `title_smoke`, `title_logo` | **Observation:** about 30 s before the logo is complete; any key skips it |
| Boot menu | menu | title -> Castle, Utilities, title | start, copyright, version | copyright text, version and serial, `S)TART GAME U)TILITIES T)ITLE PAGE` | `S U T` | - | `menu_copyright` | |
| Disk prompts | prompt | boot menu -> Castle | disk change | `SCENARIO MASTER IN DRV 1, PRESS [RET]`, then `MASTER/DUPLICATE IN DRV 1, PRESS [RET]` | Return | `NOT SCENARIO DISK` (program text) | `boot_disk_master`, `boot_disk_duplicate` | **Observation:** one line on an empty screen; nothing says which side is which |
| Utilities menu | menu | boot menu | disk and roster maintenance | seven entries | letters | - | `menu_utilities` | |
| Utility title cards | prompt | Utilities menu -> the utility's disk prompts | confirm before starting | title, a one-line warning (`NO 10 YEAR PENALTY`, `(INCOMPATIBLE WITH PREVIOUS VERSION)`), `PRESS [RET] TO BEGIN OR [ESC] TO EXIT` | Return, Esc | - | `util_change_names`, `util_transfer`, `util_backup`, `util_recover`, `util_update` | |
| Utility disk steps | prompt | title cards | tell which disk goes where | `PLACE SCENARIO IN DRIVE 1, PRESS RETURN`, `T)O OR F)ROM BACKUP`, the two-drive instructions of update and make scenario disk | Return, letters | - | `util_change_names_disk`, `util_transfer_disk`, `util_backup_dir`, `util_recover_disk`, `util_update_step1`, `util_make_scenario` | **Observation:** update and make-disk spell out source and target drive twice ("BE SURE : NEW=2, OLD=1") |
| Castle | menu | start, every castle place | hub | header, party table, the five places as a sentence | `A G B C E` | - | `menu_castle_empty`, `menu_castle`, `menu_castle_vets`, `ending_castle` | |
| Tavern | menu + prompt | Castle | form the party | party table; the options grow with the party (add only, then remove and see, add vanishes at six) | `A R`, number, typed name, Return | `** WHO? **`, `** THATS NOT IT **`, `** BAD ALIGNMENT **` | `menu_tavern_empty`, `menu_tavern_add`, `tavern_password`, `tavern_who`, `tavern_wrong_password`, `tavern_bad_alignment`, `menu_tavern`, `tavern_remove`, `tavern_removed` | **Observation:** the password is asked even when none was set |
| Inn | menu | Castle | rest and level up | `WHO WILL STAY`, five rooms with prices, then a healing counter (hit points, gold) and the level check | number, `A`-`E`, Return | - | `menu_inn_who`, `menu_inn`, `inn_stables`, `inn_healing`, `inn_royal`, `inn_levelup`, `inn_levelup_mage`, `inn_stables_vet`, `ending_inn` | **Observation:** the party table above keeps the old hit points while the counter runs |
| Temple | prompt | Castle | cure | welcome line, `WHO ARE YOU HELPING ? >`, donation, `WHO WILL TITHE`, the ritual word by word, the result | typed name, number | `** RYZ IS NOT HERE **`, `** CONDI IS OK **`, `** CHEAP APOSTATES! OUT! **` | `menu_temple`, `temple_not_here`, `temple_is_ok`, `temple_donation`, `temple_ritual`, `temple_healed`, `temple_ashes_donation`, `temple_cheap` | **Observation:** nothing lists who needs help; the name must be known |
| Trading post menu | menu | Castle | choose a service | `WHO WILL ENTER`, the member's gold, buy / sell / uncurse / identify / leave | number, `B S U I L` | - | `shop_boltac_who`, `shop_boltac` | |
| Stock list | list | trading post | buy | six numbered items with prices, `UNUSABLE` beside what the class cannot use, gold, purchase / forward / back / start / leave | `P F B S L`, item number | `** JUST WHAT YOU NEEDED **`, `UNUSABLE ITEM - CONFIRM BUY (Y/N) ?`; `YOU CANNOT AFFORD IT` (program text) | `shop_boltac_buy`, `shop_boltac_armor`, `shop_boltac_potions`, `shop_boltac_magic`, `shop_boltac_plus1`, `shop_boltac_rare`, `shop_purchase`, `shop_bought`, `shop_unusable` | **Observation:** a page repeats the last line of the page before (the list moves five places) |
| Sell / identify / uncurse lists | list | trading post | services on the pack | the pack with the offer or fee per item, `WHICH DO YOU WISH TO SELL ? >` (IDENTIFIED, UNCURSED) | item number, Return | `** ANYTHING ELSE, SIRE? **` | `shop_sell`, `shop_sold`, `shop_identify`, `shop_identified`, `shop_uncurse`, `shop_uncursed` | **Observation:** all three use the same list, so uncurse offers items that are not cursed |
| Edge of Town | menu | Castle | leave the castle | maze (only listed with a party), training grounds, castle, leave the game | `M T C L` | - | `menu_edge`, `menu_edge_empty` | |
| Leave game | screen | Edge of Town | end the session | `PRESS [RETURN] FOR MORE WIZARDRY` | Return | - | `save_leave_game` | |
| Training Grounds | prompt | Edge of Town | make and edit characters | instructions and `NAME >` | typed name, `*ROSTER`, Return | `THERE IS NO ROOM LEFT - TRY DELETING`, `PASSWORD >` for a known name | `menu_training`, `training_no_room`, `training_name_password`, `create_new_name` | **Observation:** no menu, the name is the command |
| Roster | list | Training Grounds | names in use | one line per character: name, level, race, class, (status) | `L` | - | `menu_roster_inherited`, `menu_roster`, `gameover_roster_dead` | long lines are cut at column 40 (DIRK THE DARING) |
| Creation form | screen | Training Grounds | build a character | the form fills line by line: name, password, race, points, six scores with an arrow, alignment, class; open classes appear beside the scores | Return, letters, `+ -`, Esc, `Y N` | Esc does nothing while points are left | `create_password`, `create_password_again`, `create_race`, `create_align`, `create_bonus`, `create_bonus_minus`, `create_bonus_spent`, `create_class`, `create_keep` | **Observation:** the class letters keep the gaps of the full list (A, B, D), so a letter always means the same class |
| Character options | menu | Training Grounds | edit | summary line, inspect / delete / reroll / change class / set password | `I D R C S`, Return | Y/N confirmations | `training_char_menu`, `training_delete`, `training_reroll`, `training_change_class`, `training_class_changed`, `training_password` | |
| Character sheet | screen | Tavern, camp, Training | everything about one member | name line (with `">"` after the ending), scores, gold, experience, level, age, hits, AC, status, spell points by level, the mark legend, the pack in two columns, options that fit the place | `E D T R S U I L` | - | `inventory_sheet_l1`, `training_inspect_new`, `training_class_changed_sheet`, `inventory_sheet_vet`, `inventory_sheet_condi`, `inventory_sheet_priest`, `inventory_sheet_thief`, `inventory_sheet_mage`, `inventory_sheet_bishop`, `inventory_sheet_ninja`, `inventory_sheet_samurai`, `inventory_sheet_lord`, `inventory_sheet_jib`, `inventory_cursed`, `inventory_camp_inspect`, `temple_healed_sheet`, `inventory_amulet`, `ending_chevron` | the option list changes with the place: Training offers read and leave, the Tavern adds equip, drop, trade, the camp adds cast, use, identify |
| Sheet prompts | prompt | sheet | trade, drop, use, identify | `TRADE WITH`, `AMT OF GOLD ? >`, `WHAT ITEM`, `DROP ITEM (0=EXIT) ? >`, `USE ITEM (0=EXIT) ? >`, `CAST ON WHO`, `IDENTIFY WHAT ITEM (0=EXIT) ? >`, `SUCCESS!` | numbers, Return | `** SPELL FAILS **` | `inventory_trade`, `inventory_trade_gold`, `inventory_trade_item`, `inventory_drop`, `inventory_dropped`, `camp_use_item`, `camp_use_whom`, `camp_cast_whom`, `inventory_bishop_identify`, `inventory_identified`, `system_fizzle` | **Observation:** drop and trade act at once, without a confirmation |
| Spell books | list | sheet | known spells | spell points left for both lists, then the mage or priest spells grouped by level in two columns | `M P L` | - | `inventory_spellbooks`, `inventory_mage_book`, `inventory_priest_book` | **Observation:** names only; what a spell does is in the manual |
| Equip | prompt | camp, sheet | wear items | `SELECT WEAPON FOR RYZ`, numbered candidates, `WHICH ONE ([RET] FOR NONE) ? >`; then armor and the other slots | number, Return | `** CURSED **` (program text) | `camp_equip`, `camp_equip_armor` | only slots with a candidate are asked |
| Camp | menu | maze `C`, maze entry | manage the party in the maze | party table, reorder / equip / disband / inspect / leave | `R E D`, number, `L` | `CONFIRM (Y/N) ?` | `gameplay_camp`, `camp_reorder`, `camp_disband` | |
| Location and teleport | screen | camp spells | DUMAPIC report; MALOR displacement counters | plain text | `L`; `N S E W U D`, Return, Esc | `YOU BOUNCED BACK TO WHERE YOU WERE!`, `YOU MATERIALIZED IN MID-AIR AND FELL TO A PAINFUL DEATH!` | `system_dumapic`, `system_dumapic_f4`, `camp_malor`, `camp_malor_set`, `camp_malor_home`, `camp_malor_bounce`, `gameover_malor_midair` | **Observation:** west, south and up show as negative east, north and down |
| Maze screen | screen | camp | explore | view (wireframe), command list, `SPELLS :`, message pane, party table | `F L R K C S Q T I` | `OUCH!` in the view | `gameplay_maze_f1_start`, `gameplay_wall`, `gameplay_dark`, `gameplay_door`, `gameplay_f3_crossing`, `gameplay_f6_doors`, `gameplay_f7_hall`, `gameplay_after_werdna` | |
| Maze prompts | prompt | maze squares, maze keys | level changes and tools | `STAIRS GOING UP. TAKE THEM (Y/N) ?`, the elevator buttons, `NEW DELAY (1-5000) >`, `SEARCH (Y/N) ?`, the body search `FOUND: ** NO ONE **` | `Y N`, letters, Return, number | - | `gameplay_stairs`, `gameplay_stairs_down`, `gameplay_stairs_amulet`, `gameplay_elevator`, `gameplay_elevator_f2`, `gameplay_elevator_f4`, `gameplay_time_delay`, `gameplay_inspect_none`, `system_search`, `system_search_found` | |
| Maze messages | message | maze squares | story and traps | one to four lines in the message pane, `[RET] FOR MORE` or `PRESS [RET]` in the right pane when another page follows; `A PIT!`, `A CHUTE!` | Return | - | `gameplay_pit`, `gameplay_chute`, `dialogue_sign_f1`, `dialogue_f1_mapiro`, `dialogue_f1_chicken`, `dialogue_f1_altar`, `dialogue_f2_bronze_smoke`, `dialogue_f2_silver_fog`, `dialogue_f2_silver_fog_flee`, `dialogue_f2_placard`, `dialogue_f2_bear`, `dialogue_f2_frog`, `dialogue_f2_door`, `dialogue_f3_mosaic`, `dialogue_f4_control`, `dialogue_f4_alarm`, `dialogue_f4_alarm_guardians`, `dialogue_f4_treasure`, `dialogue_f4_allocation`, `dialogue_f4_desk`, `dialogue_f4_private`, `dialogue_f4_asleep`, `dialogue_f4_asleep_outside`, `dialogue_f4_bear_wall`, `dialogue_f10_plaque`, `dialogue_f10_plaque_2`, `dialogue_f10_plaque_3`, `dialogue_f10_guardians`, `dialogue_werdna_sign` | **Observation:** the command list is replaced by the paging hint, so it is clear the keys are off |
| Encounter start | transition | maze | announce a fight | `AN ENCOUNTER`, the picture drawn in, the group list, a surprise line | - | - | `battle_encounter`, `battle_surprised`, `battle_f1_skeletons`, `boss_werdna` | |
| Battle orders | screen | encounter | one order per member | monster picture, numbered groups `1) 3 SLIMES (3)`, `RYZ'S OPTIONS` with the letters that member may use, prompts `FIGHT AGAINST GROUP# ?`, `SPELL NAME ? >`, `CAST SPELL ON GROUP #?`, then `PRESS [RETURN] TO FIGHT, OR GO B)ACK TO REDO OPTIONS` | `F S P R U D`, numbers, typed spell, Return, `B` | `YOU DONT KNOW THAT SPELL` (program text) | `battle_slimes`, `battle_spell_prompt`, `battle_group_select`, `battle_spell_group`, `battle_use_item`, `battle_f9_unseen_entity`, `battle_orders`, `boss_werdna_orders`, `battle_three_dead`, `boss_four_dead` | **Observation:** the order screen never shows what was already ordered; B)ack redoes all six |
| Battle messages | message | round | tell the round | attacker, verb, target on three lines, hits and damage, the result line (`KILLS ONE!`, `IS SLAIN!`, `DIES!`, `IS POISONED`, `IS SLEPT`, `IS UNAFFECTED!`, `FLEES!`, `CALLS FOR HELP!`) | - | - | `battle_kill`, `battle_cast`, `battle_mahalito`, `battle_katino`, `battle_breath`, `battle_unaffected`, `battle_multi_hit`, `battle_demon_stab`, `battle_malikto`, `battle_malikto_ninja`, `battle_tiltowait`, `battle_demon_unaffected`, `battle_enemy_spell`, `battle_gas_spell`, `battle_not_slept`, `battle_flees`, `battle_poisoned`, `battle_potion`, `battle_run_failed`, `battle_dispell`, `battle_slain`, `battle_call_for_help`, `battle_help_heard`, `boss_tiltowait`, `boss_werdna_hurt`, `boss_spell_unaffected`, `boss_werdna_killed`, `boss_werdna_spell`, `boss_member_dies`, `boss_vampire_spell`, `boss_werdna_chop`, `boss_mabadi`, `boss_paralyzed`, `boss_level_drain` | **Observation:** a cast is announced without the spell's name; only a few result lines name it ("IS HIT BY MABADI!") |
| Friendly group | prompt | encounter | choose | `A FRIENDLY GROUP OF ... THEY HAIL YOU IN WELCOME! YOU MAY F)IGHT OR L)EAVE IN PEACE.` | `F L` | - | `battle_friendly`, `battle_friendly_thieves`, `battle_f7_friendly_daimyos`, `boss_werdna_friendly`, `boss_friendly_left` | |
| Victory and chest | screen | battle | rewards | the experience line, chest picture, `A CHEST! YOU MAY: O)PEN C)ALFO L)EAVE I)NSPECT D)ISARM`, `WHO (#) WILL ...?`, the trap name, the treasure pile with `FOUND -` and `EACH SHARE IS WORTH n GP!` | `O C L I D`, number, typed trap | `OOPPS! A CROSSBOW BOLT`, `THE CHEST WAS NOT TRAPPED` | `battle_victory`, `battle_dispell_ep`, `boss_werdna_ep`, `battle_chest`, `chest_inspect_who`, `chest_inspected`, `chest_open_who`, `chest_gold`, `chest_disarm_prompt`, `chest_not_trapped`, `chest_calfo_who`, `chest_calfo`, `chest_crossbow_bolt`, `chest_item_found`, `chest_gold_58`, `chest_disarmed`, `boss_amulet_found` | |
| Round 2 and later | screen | round | next orders | the group list with the survivors | as orders | - | `battle_round2`, `battle_demon_alone`, `boss_round2` | |
| Cemetery | screen | a round that kills the last member | game over | six tombstones with RIP, each member's name beside it | Return | - | `gameover_cemetery` | |
| Ending | screen | stairs up with the amulet | reward | the Congratulations text, `PRESS [RETURN], HONORED ONES` | Return | - | `ending_congratulations` | |

## 3. Screen flow
- power-on -> opening animation -> (key) -> boot menu
  - `U` utilities (title card -> disk prompts); `T` title again
  - `S` -> two disk prompts -> **Castle**
    - Tavern (add by name, remove, see -> sheet) ; Inn ; Temple ; Trading post (services -> stock pages)
    - Edge of Town
      - Training Grounds (name -> creation form, or options -> sheet / delete / reroll / class / password; roster)
      - Leave game -> "FOR MORE WIZARDRY" -> disk prompts -> Castle
      - Maze -> Camp -> maze screen
        - `C` camp -> sheet -> spell books, equip, spells (DUMAPIC, MALOR), use, identify
        - squares: stairs (up from floor 1 = Castle), elevator, messages, pits, the chute
        - encounter -> orders -> round messages -> victory -> chest -> maze screen; or the cemetery -> Castle
        - Castle with the amulet -> ending -> Castle

## 4. Elements in detail
- **Party table** (bottom pane in the maze, upper block in the castle): `# CHARACTER NAME  CLASS AC HITS
  STATUS`; STATUS repeats the hit-point maximum while the member is OK and becomes `DEAD`, `POISON` ... when
  not **(verified: `boss_four_dead`, `battle_three_dead`)**.
- **Group lines** in battle: `2) 1 W E R D N A (1)`: group number, how many, the name as far as it is known,
  and in brackets how many of them can act **(verified: counts; the meaning of the bracket is the DOS
  documents')**.
- **Maze view**: about a quarter of the screen width; walls as purple outlines, doors as an inner frame, dark
  squares draw nothing, `OUCH!` is written into the view **(verified: `gameplay_wall`, `gameplay_dark`,
  `gameplay_door`)**.
- **Right pane**: the nine maze commands with the alternative movement keys shown as `A<-W->D CLUSTER`; in
  battle the group list above the member's options; during paged messages only `[RET] FOR MORE`
  **(verified: `gameplay_maze_f1_start`, `battle_slimes`, `dialogue_f2_frog`)**.
- **Sheet legend**: `*=EQUIP, -=CURSED, ?=UNKNOWN, #=UNUSABLE` is printed on every sheet above the pack
  **(verified: `inventory_cursed`, `inventory_sheet_jib`)**.

## Open questions
- What S)tatus and Q)uick plot change on the maze screen.
- The utilities past their first disk prompt (they need second disks).
- After the cemetery Return leads to the Castle with no party (seen; the same picture as `menu_castle_empty`, so not a shot of its own).
