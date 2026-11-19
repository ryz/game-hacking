# Wizardry: Proving Grounds of the Mad Overlord (DOS) - interface (UI/UX lens)

Every screen, menu, prompt and on-screen element of the game, described as an interface: what it is for, what
it shows, what it accepts, how it answers. Read it to study how the game talks to the player. The same shots
also appear in [systems.md](systems.md), which looks at the rules, and in [content.md](content.md), which shows
the variety of what fills the game; overlap is intended.
Notation: [README.md](README.md). Check: `python3 tools/lenses.py dos/wizardry main`.

Facts carry a confidence tag as everywhere in this folder. A judgement (clear, slow, easy to miss) is written
as **Observation:** with the reason, never as a fact.

## 1. Conventions
- **Input:** keyboard only. Every menu entry is chosen by the letter before its bracket ("G)ilgamesh's
  Tavern"), party members by their number 1-6, roster entries by letter; Enter (drawn as a bent arrow) leaves a
  menu ("L<Enter>eave") and confirms prompts; Y/N questions take Y or N. The maze uses W, A, D (move, turn), K
  (kick through a door), C, S, I, O. Spells, trap names and character names are typed (verified:
  `battle_spell_prompt`, `chest_disarm_prompt`, `create_name`). Bonus points use Enter to move the pointer and
  the cursor keys to change a value, Esc to finish (verified: `create_bonus_spent`). Wrong keys are ignored.
  Keys typed while a screen is drawn can be lost (inferred).
- **Layout:** 320 x 200 in four colours; a framed title tab at the top centre (CASTLE, CAMP, TRAINING
  GROUNDS), a menu box in the middle, and the party window ("# Character name Class AC Hits Status") along
  the bottom on every castle and maze screen (verified: `menu_castle`). In the maze the top line is the
  command line and the wireframe view fills the middle; in battle the monster groups replace the command
  line, a message or options box sits under them and the monster picture in the view (verified:
  `battle_f4_fixed`). The character sheet takes the whole middle with its own command box at the bottom
  (`inventory_sheet_vet`).
- **Text:** capitals only, one 8 x 8 font; white on black; colour only in pictures (monsters, chest,
  treasure, tombstones, title logo). Two special glyphs stand for "Potion of" and "Scroll of" in item names
  (verified: `shop_boltac_potions`).
- **Feedback:** messages appear in a framed box and are timed, not confirmed: in battle each stays about
  2.7 s (verified at the 8088 speed); signs and prompts wait for Enter or Y/N ("Press Enter" box). Shops answer
  with a short framed line ("* Just what you needed *", "* Anything else, noble sir? *") (verified:
  `shop_bought`, `shop_sold`). Irreversible steps ask first ("Keep this character (Y/N)?", "Sure you want to
  delete (Y/N)?", "Stairs up, take them (Y/N)?") (verified).
- **State visibility:** the party window always shows class, armour class, hit points and status (the
  status column shows the maximum hit points when the character is well, else DEAD, ASLEEP, PARALY, LOST,
  ASHES; in battle the order given or "??????") (verified: `battle_orders`, `boss_four_dead`,
  `temple_lost_party`). Position, floor and facing are never shown except by DUMAPIC (verified:
  `system_dumapic`). Item marks: "*" equipped, "-" cursed, "?" unknown, "#" unusable (verified, [items](items.md)).
- **Help and onboarding:** none beyond the letter menus; the title warns "You cannot play without making a
  scenario disk!" (verified: `title_screen`).

## 2. Screen inventory
Type: `screen`, `menu`, `prompt`, `list`, `message`, `hud element`, `transition`.

| Screen / element | Type | Reached from -> leads to | Purpose | Shows | Accepts | Feedback and errors | Shots | Observation |
|---|---|---|---|---|---|---|---|---|
| Title | screen | power-on -> loader prompts (S), make disk (M) | start | logo, monster parade, scenario-disk warning | S, M | - | `title_screen`, `title_parade_trio`, `title_parade_pair` | the parade cycles monster pictures from the game |
| Make scenario disk | prompt | title M | prepare a disk | "The disk you inserted has data on it ... Use it (Y/N)?" | Y, N | - | `menu_make_scenario` | the 1998 package ships a ready disk, so it is never needed |
| Disk prompts | transition | S -> Castle | loader | "Place duplicate scenario diskette in drive 1", "Now loading the program into memory" | answered by the loader | - | `boot_disk_prompt`, `boot_loading` | the 1998 loader presses Enter itself |
| Castle | menu | title, every service -> services, Edge of Town | hub | five services, party window | G A T B E | - | `menu_castle_empty`, `menu_castle`, `menu_castle_vets` | - |
| Gilgamesh's Tavern | menu | Castle | form the party | add, remove, inspect (#), divvy gold | A R # D Enter | the add list closes when six are in | `menu_tavern`, `menu_tavern_add`, `tavern_remove`, `tavern_removed` | - |
| Adventurer's Inn | menu | Castle | rest, level up | "Who will stay?", then five rooms with prices and the gold of the guest | 1-6, A-E, P, Enter | the level message or "You need N more E.P." | `menu_inn_who`, `menu_inn`, `inn_stables`, `inn_recuperating`, `inn_levelup` | the recuperating sheet counts up live |
| Temple of Cant | prompt | Castle | cure | "Who shall we help?" (roster characters not OK), donation, payer, ritual | letter, digit, Enter | "* NAME has been healed *" / "will be buried" | `menu_temple_empty`, `temple_dead`, `temple_donation`, `temple_ritual`, `temple_healed`, `temple_ashes_donation`, `temple_buried`, `ending_temple_paralysis`, `ending_temple_healed` | the ritual is typed out word by word |
| Boltac's Trading Post | menu | Castle | shop | who enters, then buy, sell, uncurse, identify, pool gold; the shopper's gold | 1-6, B S U I P Enter | - | `shop_boltac_who`, `shop_boltac` | - |
| Boltac's stock | list | Boltac's -> B | buy | six items per page with prices, gold left, "USELESS" for the shopper's class | P B F S Enter | "Unusable item - buy it (Y/N)?", "* Just what you needed *" | `shop_boltac_buy`, `shop_boltac_armor`, `shop_boltac_potions`, `shop_boltac_magic`, `shop_boltac_rare`, `shop_purchase`, `shop_bought`, `shop_unusable` | F moves one item forward, not one page |
| Boltac's pack lists | list | Boltac's -> S, U, I | sell, uncurse, identify | the shopper's pack with Boltac's prices | digit | "* Anything else, noble sir? *" | `shop_sell`, `shop_sold`, `shop_identify`, `shop_identified`, `shop_uncurse`, `shop_uncursed` | no confirmation before a sale |
| Edge of Town | menu | Castle -> Training, Maze, Utilities, leave | gateway | five choices | T M C U L | L returns to DOS | `menu_edge` | - |
| Wizardry Utilities | menu | Edge of Town | roster housekeeping | change name, move characters, restart an "out" party | C M R Enter | "No characters are in the maze" | `menu_utilities`, `util_change_name`, `util_move`, `util_restart_none` | - |
| Training Grounds | menu | Edge of Town | characters | create, inspect, roster | C I R Enter | - | `menu_training`, `training_pick` | - |
| Training: a character | menu | Training I + letter | manage | inspect, delete, change class, alter password | I D C A Enter | "Sure you want to delete (Y/N)?" | `training_char_menu`, `training_inspect_new`, `training_change_class`, `training_class_changed`, `training_delete`, `training_password` | - |
| Roster of characters | list | Training R | overview | every character: level, alignment-class, race | Enter | - | `inventory_roster` | - |
| Character creation | prompt sequence | Training C | new character | name, password, race, alignment, bonus points with the live class list, class, keep | text, letters, cursor keys, Esc, Y/N | "Name already in use - press Enter" | `create_name`, `create_name_taken`, `create_password`, `create_race`, `create_align`, `create_bonus`, `create_bonus_spent`, `create_class`, `create_keep` | the header line fills in as choices are made ("ZED L 1 N-??? ELF") |
| Character sheet | screen | Tavern #, Camp #, Training I | inspect | name line (level, alignment-class, race, chevron), statistics, gold, E.P., age, HP, AC, status, spell points, pack | R T P S E D I U Enter | - | `inventory_inspect_l1`, `inventory_sheet_vet`, `inventory_camp_inspect`, `ending_chevron`, `ending_chevron_condi` | S)pell and U)se only in camp |
| Sheet sub-prompts | prompt | sheet R, T, P, D, I, S, U | read books, trade, pool, drop, identify, cast, use | a framed question over the sheet | digits, amounts, spell names | "You identified it!" | `inventory_spellbooks`, `inventory_mage_book`, `inventory_priest_book`, `inventory_trade`, `inventory_trade_gold`, `inventory_pool`, `inventory_drop`, `inventory_bishop_identify`, `inventory_identified`, `camp_cast_whom`, `camp_use_item` | - |
| Maze view | screen | Maze | explore | wireframe corridors, doors as inner frames, command line, party window | W A D K C S I O | "You can't walk through walls!" | `gameplay_maze_f1_start`, `gameplay_wall`, `gameplay_door` | - |
| View toggles | hud element | maze S, O | more view | the view full height; the view alone | S, O | - | `gameplay_status_off`, `gameplay_full_view` | - |
| Search for bodies | message | maze I | rescue | "Found:" list | - | "* no one *" | `gameplay_inspect_none` | - |
| Camp | menu | maze C, maze entry | rest stop | inspect, reorder, equip, leave | 1-6 R E Enter | - | `gameplay_camp`, `camp_reorder`, `camp_equip` | - |
| DUMAPIC report | message | camp spell | position | facing, east, north, down | Enter | "* Fizzle! *" on anti-magic squares | `system_dumapic`, `system_fizzle` | the only position display |
| MALOR | prompt | camp spell | teleport | east/north/up offsets and a letter menu | E W N S U D T Q | - | `camp_malor` | - |
| Square prompts | prompt | stairs, elevators, statues | move, search | "Stairs up, take them (Y/N)?", "buttons A through D/F", "Will you search (Y/N)?" | Y N, letters | "RYZ got an item." | `gameplay_stairs`, `gameplay_elevator`, `gameplay_elevator_f4`, `system_search`, `system_search_found` | - |
| Signs and scenes | message | stepping on a message square | story, hints, gates | framed text, "Press Enter" | Enter | - | `dialogue_*` | long texts fill the whole top box |
| Square events | message | pit, chute, rock | hazards | "A pit!", "One moment", "You are in rock!" | - | - | `gameplay_pit`, `gameplay_chute`, `gameover_rock` | - |
| Battle | screen | encounter | fight | monster groups with counts, member options, picture, party orders | F P S D U R T, 1-4 | "Press Enter to fight, or T)ake back orders" | `battle_options`, `battle_orders`, `battle_group_select`, `battle_use_item`, `boss_werdna_orders` | - |
| Battle messages | message | each action | report | one blow or spell per message, its result on the next line | - | - | `battle_kill`, `battle_miss`, `battle_cast`, `battle_enemy_katino`, `boss_werdna_killed` | timed, no key needed |
| Friendly group | prompt | encounter | choose | "A friendly group of ..." | F, L | - | `battle_friendly` | - |
| Rewards | message | end of a fight | report | "Each survivor gets N E.P." / "N G.P.", "NAME found: ITEM" over the treasure picture | - | - | `battle_victory`, `chest_gold`, `boss_amulet_found` | - |
| Chest | menu | after a won fight | loot | chest picture, five choices, "Who (#) will ...?" | O C L I D, digit, trap name | "Oops! Exploding box", "You disarmed the trap!" | `battle_chest`, `chest_*` | - |
| Cemetery | screen | party killed | game over | tombstones, "Press Enter to leave the cemetery" | Enter | - | `gameover_cemetery` | - |
| Ending | screen | castle with the amulet | win | congratulations, reward, chevron | Enter | - | `ending_congratulations`, `ending_castle`, `ending_final_party` | - |

## 3. Screen flow
```
title --S--> (loader answers the disk prompts) --> CASTLE
CASTLE: G tavern | A inn | T temple | B Boltac's | E edge of town
EDGE OF TOWN: T training (create / inspect: delete, change class, password / roster) | M maze | C castle
              | U utilities (change name, move characters, restart) | L leave game (to DOS)
M maze --> CAMP --Enter--> maze view (floor 1, stairs up)
maze view: W/A/D move | K door | C camp (# sheet: read, trade, pool, spell, equip, drop, identify, use) | I search
           | S/O view | square events (stairs, elevators, signs, pits, chute, fixed fights)
encounter --> (friendly? F/L) --> battle rounds --> E.P., gold or chest --> maze view
          \--> all dead --> cemetery --> CASTLE
stairs up on floor 1 (or the floor 10 teleporter) --> CASTLE (with the amulet: ENDING --> CASTLE)
```
(verified)

## 4. Elements in detail
- **Party window** (bottom, every castle and maze screen): number, name, alignment-class ("G-FIG"), armour
  class, hit points now, status column (maximum hit points when well, else the condition; in battle the
  order or "??????"). Sleeping and paralyzed members are moved to the end of the list (verified:
  `battle_party_asleep`, `gameplay_after_werdna`).
- **Maze view**: white lines only; the walls of up to four squares ahead; doors are drawn as an inner frame on
  a wall; darkness fills the view with grey (verified `gameplay_dark`).
- **Battle top box**: up to four lines "N) count NAME (alive)"; names are generic until identified, Werdna's
  is spelled "**W*E*R*D*N*A**" (verified: `boss_werdna`).

## Open questions
- Leave game: the program ends without an in-game screen; the loader prints "Thanks for playing Wizardry!"
  on the DOS screen (verified in a route, not shot: the frame shows the emulator's own menu line).
