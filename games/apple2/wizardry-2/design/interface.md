# Wizardry II: The Knight of Diamonds - interface (UI/UX lens)

Every screen, menu, prompt and on-screen element of the game, described as an interface: what it is for, what
it shows, what it accepts, how it answers. Read it to study how the game talks to the player. The same shots
also appear in [systems.md](systems.md), which looks at the rules, and in [content.md](content.md), which shows
the variety of what fills the game; overlap is intended.
Notation: [README.md](README.md). Check: `python3 tools/lenses.py apple2/wizardry-2 main`. Shots are ids of
the set `main`; the set `start` shows the first session in play order.

Facts carry a confidence tag as everywhere in this folder. A judgement (clear, slow, easy to miss) is written
as **Observation:** with the reason, never as a fact.

## 1. Conventions
Wizardry I's conventions on this machine apply ([interface](../../wizardry/design/interface.md)) **(verified
by the screens below)**.
- **Input:** keyboard only. Menus show their keys as `X)WORD` and take the letter; lists take a digit (party
  place, item number) or a letter (utility slot); names, spells, riddle answers and trap names are typed in
  capitals and ended with Return; Return alone leaves most screens. One key at a time: a key pressed during a
  disk load is lost **(verified)**. The title takes Return only **(verified)**.
- **Layout:** two families of screens. Town, camp, sheets, shops, utilities and the ending are 40-column text
  screens with a boxed header ("! LLYLGAMN ... MARKET !") and the party table **(verified: `menu_castle`)**.
  The maze and battle are one hi-res screen in four regions: the view (top left), the command list or the
  monster names and options (top right), the "SPELLS :" box / message prompt line, the message box, and the
  party table at the bottom **(verified: `gameplay_maze_f1_start`, `battle_encounter`)**.
- **Text:** capitals only; the hi-res screen uses white lines for the frame, purple for walls and doors, green
  and white text; the place name in the town header changes (MARKET, TAVERN, INN, SHOP, TEMPLE, EXIT)
  **(verified)**.
- **Feedback:** battle and chest messages are timed (about 60-160 frames each) and never wait for a key; maze
  messages wait with "[RET] FOR MORE" or "PRESS [RET]"; irreversible actions ask "(Y/N) ?" (delete, unusable
  buy, disband, fees) **(verified)**. Wrong answers are short ("WRONG!", "CHEAP APOSTATES! OUT!").
- **State visibility:** the party table (name, class with alignment, AC, hits, max hits or status) is on every
  town and maze screen; the floor and position are never shown (DUMAPIC tells them) **(verified)**.
- **Help and onboarding:** none in the game beyond the key lists; the Training Grounds explain why characters
  cannot be created **(verified: `menu_training`)**.

## 2. Screen inventory

| Screen / element | Type | Reached from -> leads to | Purpose | Shows | Accepts | Feedback and errors | Shots | Observation |
|---|---|---|---|---|---|---|---|---|
| Title picture | screen | power-on -> copyright menu | name the game | logo, knight and dragon, "KNIGHT of DIAMONDS" **(verified)** | Return | none | `title_logo` | **Observation:** nothing says which key continues |
| Copyright menu | menu | title -> game, utilities, title | start | copyright, version, `S)TART GAME U)TILITIES T)ITLE PAGE` **(verified)** | `S U T` | - | `menu_copyright` | - |
| Utilities | menu | copyright menu -> each utility | disk housekeeping | seven entries **(verified)** | letters | - | `menu_utilities` | - |
| Utility first screens | prompt | Utilities | announce a utility | its name and "PRESS [RET] TO BEGIN OR [ESC] TO EXIT" **(verified)** | Return, Esc | warnings in the text ("FOLLOW DIRECTIONS CAREFULLY") | `util_recover`, `util_backup`, `util_make_scenario`, `util_update`, `util_change_names`, `system_transfer_begin` | - |
| Transfer | prompts and list | Utilities -> Utilities | move a character between scenario disks | disk prompts, the source's name and characters by letter, password, "CHAR HAS BEEN MOVED" **(verified)** | Return, Esc, letter, password | "CHAR HAS NON-XFERRABLE ITEMS" and others **(program text)** | `system_transfer_source`, `system_transfer_list`, `system_transfer_password`, `system_transfer_target`, `system_transfer_moved`, `system_transfer_second`, `system_transfer_done` | **Observation:** two disk changes per character; six characters take twelve |
| Disk prompts | prompt | start, utilities | ask for a disk | "PLACE BOOT DISK IN DRIVE 1", "SCENARIO MASTER IN DRV 1", "MASTER/DUPLICATE IN DRV 1" **(verified)** | Return | - | `boot_disk_prompt`, `boot_scenario_master`, `boot_scenario_duplicate` | - |
| Castle | menu | start -> the five places | hub | header, party table, the choices **(verified)** | `A G B C E` | - | `menu_castle_empty`, `menu_castle`, `menu_castle_geared`, `menu_castle_solo` | - |
| Tavern | menu and prompts | Castle | form the party | "WHO WILL JOIN ? >", "ENTER PASSWORD >", "WHO WILL LEAVE" **(verified)** | `A R`, digit, Return | the choices shrink as the party fills | `menu_tavern_empty`, `tavern_password`, `tavern_adding`, `menu_tavern`, `tavern_remove` | - |
| Character sheet | screen | Tavern digit, camp digit, Training I)nspect | one character | scores, gold, E.P., level, age, hits, AC, status, spell points, items with `* - ? #` marks, the commands **(verified)** | letters | - | `inventory_sheet_import`, `inventory_sheet_geared`, `inventory_sheet_condi`, `inventory_sheet_ebo`, `inventory_sheet_cubi`, `inventory_sheet_deddo`, `inventory_sheet_mnz`, `inventory_stock_thug`, `inventory_stock_kelrach`, `inventory_stock_fury` | in the Training Grounds only R)ead and L)eave |
| Adventurer's Inn | menus | Castle | rest, level | "WHO WILL STAY", the room list with prices, "YOU NEED n MORE", "YOU MADE A LEVEL!", "IS HEALING UP" with hit points and gold counting **(verified)** | digit, `A-E`, Return | - | `menu_inn_who`, `menu_inn`, `inn_stables`, `inn_healing`, `inn_levelup` | - |
| Boltac's Trading Post | menus and lists | Castle | trade | "WHO WILL ENTER", the member's gold and choices, six items a page with price and "UNUSABLE", prompts per action **(verified)** | digit, `B S U I L`, `P F B S`, item digit, `Y N` | "UNUSABLE ITEM - CONFIRM BUY (Y/N) ?"; a sold or uncursed item leaves the list | `shop_boltac_who`, `shop_boltac`, `shop_buy_weapons`, `shop_buy_armor`, `shop_buy_plate`, `shop_buy_magic`, `shop_buy_plus`, `shop_buy_rare`, `shop_purchase`, `shop_unusable`, `shop_sell`, `shop_sold`, `shop_identify`, `shop_identified`, `shop_uncurse`, `shop_uncursed` | **Observation:** "SCROLL F)ORWARD OR B)ACK" pages overlap by one item |
| Temple of Cant | prompts | Castle | cure | "WHO ARE YOU HELPING ? >", "THE DONATION WILL BE n", "WHO WILL TITHE", "MURMUR - CHANT - PRAY - INVOKE!", "** CONDI IS WELL **" **(verified)** | typed name, digit | "CHEAP APOSTATES! OUT!" | `menu_temple`, `temple_donation`, `temple_ritual`, `temple_healed`, `temple_cheap` | **Observation:** the patient must be outside the party, which the screen does not say |
| Edge of Town | menu | Castle | leave town | `M)AZE T)RAINING GROUNDS C)ASTLE L)EAVE THE GAME` **(verified)** | letters | - | `menu_edge` | - |
| Leave the game | message | Edge of Town | end a session | "PRESS [RETURN] FOR MORE WIZARDRY" **(verified)** | Return | - | `save_leave_game` | - |
| Training Grounds | prompt and menus | Edge of Town | inspect or edit the roster | the "cannot create" text, "NAME >", the character's options, "*ROSTER" list, "(Y/N)", class and password prompts **(verified)** | name, `*ROSTER`, `I D C S`, Return | disbands the party without saying so | `menu_training`, `training_options`, `training_delete`, `training_change_class`, `training_password`, `inventory_roster_original`, `inventory_roster` | **Observation:** the party list is empty afterwards |
| Camp | menu | maze entry, `C` | party care | the party table and `R)EORDER E)QUIP D)ISBAND #) INSPECT L)EAVE` **(verified)** | letters, digits | "CONFIRM (Y/N) ?" for disband | `camp_first`, `camp_menu`, `camp_reorder`, `camp_disband`, `gameplay_party_dead` | - |
| Equip prompts | prompt | camp E)quip | wear items | "SELECT WEAPON FOR RYZ", candidates, "WHICH ONE ([RET] FOR NONE)" per slot kind **(verified)** | digit, Return | - | `camp_equip`, `camp_equip_armor` | **Observation:** every member, every slot kind in a row: 19 prompts for a geared party |
| Sheet prompts | prompt | sheet | act on items and spells | "TRADE WITH", "AMT OF GOLD", "DROP ITEM (0=EXIT)", "USE ITEM", "IDENTIFY WHAT ITEM", "WHAT SPELL", "CAST ON WHO" **(verified)** | digits, text | the item's name changes when identified | `camp_trade`, `camp_trade_gold`, `camp_drop`, `camp_use_item`, `camp_identify`, `camp_identified`, `camp_cast`, `camp_cast_whom` | - |
| Spell books | screen | sheet R)ead | list known spells | spells left per level, then the mage or priest book in two columns **(verified)** | `M P L` | - | `inventory_spellbooks`, `inventory_mage_book`, `inventory_priest_book` | - |
| DUMAPIC, MALOR | screen | camp spell | where am I, teleport | "PARTY LOCATION: ... FACING NORTH ... 0 SQUARES EAST ...", "PARTY TELEPORT: ENTER NSEWU OR D" with three counters **(verified)** | `L`; `N S E W U D`, Return, Esc ("CHICKEN OUT!") | - | `camp_dumapic`, `camp_malor` | - |
| Maze view | screen | camp | play | wireframe view, commands, "SPELLS :" box, message box, party table with AC and hits **(verified)** | `F L R K C Q T S I` | "OUCH!" drawn in the view at a wall | `gameplay_maze_f1_start`, `gameplay_wall`, `env_f1_corridor`, `env_f2_doors`, `env_f3_junction`, `env_f4_hall`, `env_f4_cavern`, `env_f6_spinner`, `gameplay_dark` | **Observation:** the view is small (a quarter of the width); the rest is text |
| Maze prompts | prompt | maze keys | stairs, delay, search | "STAIRS GOING UP/DOWN. TAKE THEM (Y/N) ?", "NEW DELAY (1-9999) >", "LOOKING......." (a text screen) **(verified)** | `Y N`, number | - | `gameplay_stairs_up`, `gameplay_stairs_down`, `gameplay_time`, `gameplay_inspect` | - |
| Maze messages | message | special squares | story, traps | text in the message box; "[RET] FOR MORE" / "PRESS [RET]" in the spell box; one-line trap messages ("A PIT!", "A CHUTE!") disappear by themselves **(verified)** | Return | - | `dialogue_f1_armor_clue`, `dialogue_gnilda`, `gameplay_pit`, `gameplay_chute`, `dialogue_sphinx` | - |
| Maze questions | prompt | special squares | answer, pay, choose | "ANSWER ?" with a block cursor, "FEE IS n / PAY (Y/N) ?", "WHO (#) WILL WADE, [RET] EXITS" **(verified)** | text, `Y N`, digit | "RIGHT!", "WRONG!" | `dialogue_f2_riddle_answer`, `dialogue_sphinx_answer`, `dialogue_sphinx_wrong`, `dialogue_sphinx_right`, `dialogue_f2_sage_fee`, `dialogue_f5_well_fee`, `dialogue_f4_wade`, `dialogue_gnilda_answer` | - |
| Battle | screen | encounter | fight | monster picture, groups "1) 4 MANTICORES (4)", "RYZ'S OPTIONS" and that member's choices, a surprise line, timed round messages **(verified)** | `F S P R U D`, group digit, typed spell, Return, `B` | "PRESS [RET] TO FIGHT, OR GO B)ACK AND RE-ENTER." | `battle_encounter`, `battle_options_condi`, `battle_dispell`, `battle_spell_prompt`, `battle_back_rank`, `battle_group_select`, `battle_orders`, `battle_use_item`, `battle_round2` | **Observation:** the options line shows only what this member may do (no F)ight in the back, no S)PELL in a surprise round) |
| Round messages | message | battle | report the round | one action at a time in the message box, hits and damage, deaths **(verified)** | none (timed) | - | `battle_spell_damage`, `battle_unaffected`, `battle_monster_hit`, `battle_monster_miss`, `battle_fighter_hits`, `battle_condi_hits` | **Observation:** the T)ime delay sets how long each stays |
| Victory and treasure | message | end of a fight | reward | "FOR KILLING THE MONSTERS EACH SURVIVOR GETS n EXPERIENCE POINTS", treasure picture, "X FOUND - item", "EACH SHARE IS WORTH n GP!" **(verified)** | none | - | `battle_victory`, `boss_armor_ep`, `boss_found_armor`, `chest_gold` | - |
| Chest | menu | after a fight | loot | chest picture, `O)PEN C)ALFO L)EAVE I)NSPECT D)ISARM`, "WHO (#) WILL OPEN?", "WHAT TRAP >" **(verified)** | letters, digit, text | "YOU DISARMED IT!", "OOPS! TELEPORTER" | `battle_chest`, `chest_open_who`, `chest_inspected`, `chest_disarm_prompt`, `chest_disarmed`, `chest_trap` | - |
| Cemetery | screen | everyone dead | game over | tombstones with RIP, name and age, "YOUR ENTIRE PARTY HAS BEEN SLAUGHTERED / PRESS RETURN TO LEAVE THE CEMETERY" **(verified)** | Return | - | `gameover_cemetery` | - |
| Ending | screen | stairs with the staff | reward | "*** GAUDEAMOUS ***" text **(verified)** | Return | - | `ending_gaudeamous` | - |
| Awards | prompt | ending -> Castle | knighthoods | "KNIGHTHOODS LEFT : n / AWARD ONE TO NAME (Y/N) ? >" **(verified)** | `Y N` | counter goes down | `ending_award`, `ending_award_ebo` | - |
| Party table | hud element | every screen but sheets | state | number, name, alignment-class, AC, hits, max hits or status (DEAD, STONED); "LO" and "112+" for the regalia **(verified)** | - | updates on a menu change | `ending_castle_knights`, `dialogue_staff_got` | **Observation:** a status word replaces the max hits |

## 3. Screen flow
Power-on -> title -> copyright menu -> (Utilities -> Transfer -> Utilities -> boot disk prompt -> copyright
menu) -> scenario disk prompts -> Castle -> Tavern / Inn / Trading post / Temple / Edge of Town -> Training
Grounds or Camp -> Maze -> Battle -> Chest -> Maze -> stairs -> Castle; all dead -> Cemetery; with the staff:
stairs -> Ending -> Awards -> Castle **(verified)**.

## 4. Elements in detail
- **Maze screen** (`gameplay_maze_f1_start`): view 120 x 70 pixels top left; command list top right
  (`F)ORWARD C)AMP S)TATUS / L)EFT Q)UICK A<-W->D / R)IGHT T)IME CLUSTER / K)ICK I)NSPECT`); below it the
  "SPELLS :" line (also "[RET] FOR MORE" and "PRESS [RET]"); a three-line message box; the party table
  **(verified)**.
- **Battle screen** (`battle_encounter`): the monster picture replaces the view; the command list becomes up to
  four group lines with alive counts in brackets, then "NAME'S OPTIONS" and that member's letters; the message
  box carries surprise and round messages **(verified)**.

## Open questions
- What Q)uick and S)tatus change (no visible change); the effect screens of Dispell and of the staff in use.
