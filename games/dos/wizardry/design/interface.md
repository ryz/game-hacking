# Wizardry: Proving Grounds of the Mad Overlord (DOS) - interface (UI/UX lens)

Every screen, menu, prompt and on-screen element of the game, described as an interface: what it is for, what
it shows, what it accepts, how it answers. Read it to study how the game talks to the player. The same shots
also appear in [systems.md](systems.md), which looks at the rules, and in [content.md](content.md), which shows
the variety of what fills the game; overlap is intended.
Notation: [README.md](README.md). Check: `python3 tools/lenses.py PLATFORM/SLUG`.

Facts carry a confidence tag as everywhere in this folder. A judgement (clear, slow, easy to miss) is written
as **Observation:** with the reason, never as a fact.

## 1. Conventions
- **Input:** keyboard only. Every menu entry is chosen by the letter before its bracket ("G)ilgamesh's
  Tavern"), characters by their number 1-6, roster entries by letter; Enter (drawn as a bent arrow) leaves a
  menu ("L<Enter>eave") and confirms prompts; Y/N questions take Y or N. The maze uses W (forward), A and D
  (turn), K (kick through a door), C, S, I, O (verified). Spells are typed by name ("Spell name ?"). Bonus points
  use Enter to move the pointer and the cursor keys to change a value, Esc to finish (verified). Wrong keys
  are ignored (verified in battle: a letter that is not an option does nothing). Keys typed while a screen is
  still being drawn can be lost; prompts seem to flush the keyboard (inferred: a name typed into a "name
  already in use" box).
- **Layout:** 320 x 200 in four colours; a framed title tab at the top centre (CASTLE, CAMP, TRAINING
  GROUNDS), a menu box in the middle, and the party window ("# Character name Class AC Hits Status") along
  the bottom on every castle and maze screen (verified). In the maze the top line is the command line and the
  wireframe view fills the middle; in battle the monster groups replace the command line and the monster
  picture sits in the view (verified).
- **Text:** capitals only, one 8 x 8 font; white on black; colour only in pictures (monsters, chest,
  tombstones, title logo) (verified on the EGA palette; a real CGA in this mode shows red and cyan instead,
  see the playbook).
- **Feedback:** messages appear in a framed box over the view and are timed, not confirmed: in battle each
  stays about 2.7 s (verified at the 8088 speed); signs and prompts wait for Enter or Y/N. Irreversible steps
  ask first ("Keep this character (Y/N)?", "Stairs up, take them (Y/N)?") (verified).
- **State visibility:** the party window always shows class, armour class, hit points and status (the status
  column shows the maximum hit points when the character is well; in battle it shows the order given or
  "??????") (verified). Position, floor and facing are never shown, except by DUMAPIC (verified).
- **Help and onboarding:** none beyond the letter menus; the title only warns "You cannot play without
  making a scenario disk!" (verified).

## 2. Screen inventory
One row per screen, menu, prompt, dialog, message type and permanent on-screen element. Type: `screen`, `menu`,
`prompt`, `list`, `message`, `hud element`, `transition`.

| Screen / element | Type | Reached from -> leads to | Purpose | Shows | Accepts | Feedback and errors | Shots | Observation |
|---|---|---|---|---|---|---|---|---|
| Title | screen | power-on -> Castle (S) | start | logo, monster parade, scenario-disk warning | S, M | - | `title_screen` | - |
| Disk prompts | message | S -> Castle | loader | "Place duplicate scenario diskette in drive 1", "Now loading the program into memory" | answered by the loader | - | (planned `boot_*`) | the 1998 loader presses Enter itself |
| Castle | menu | title, every service -> services, Edge of Town | hub | five services, party window | G A T B E | - | `menu_castle` | - |
| Gilgamesh's Tavern | menu | Castle | form the party | add, remove, inspect, divvy gold | A R # D Enter | the add list closes when six are in | `menu_tavern` | - |
| Adventurer's Inn | menu | Castle | rest, level up | "Who will stay?", then five rooms with prices and the gold left | 1-6, A-E, P, Enter | - | `menu_inn` | - |
| Temple of Cant | prompt | Castle | cure | "Who shall we help?" (roster characters in bad shape) | letter, Enter | with nobody to help it closes at once | (planned `menu_temple`) | - |
| Boltac's Trading Post | menu | Castle | shop | buy, sell, uncurse, identify, pool gold; gold of the shopper | B S U I P Enter | - | `shop_boltac` | - |
| Boltac's stock | list | Boltac's -> B | buy | six items per page with prices, gold left | P B F S Enter | - | `shop_boltac_buy` | - |
| Edge of Town | menu | Castle -> Training, Maze, Utilities, leave | gateway | five choices | T M C U L | - | `menu_edge` | - |
| Wizardry Utilities | menu | Edge of Town | roster housekeeping | change name, move characters, restart an "out" party | C M R Enter | - | `menu_utilities` | - |
| Training Grounds | menu | Edge of Town | characters | create, inspect, roster | C I R Enter | - | `menu_training` | - |
| Roster of characters | list | Training -> R | overview | every character: level, alignment-class, race | Enter | - | `inventory_roster` | - |
| Character creation | prompt sequence | Training -> C | new character | name, password, race, alignment, bonus points, class, keep | text, letters, cursor keys, Esc, Y/N | "Name already in use" | (planned `create_*`) | the class list updates as points are spent |
| Character sheet | screen | Tavern #, Camp #, maze I | inspect | name line with level, alignment-class, race, chevron; statistics, gold, E.P., age, HP, AC, status, spell points; commands | R T P S E D I U Enter | - | `inventory_inspect_vet`, `inventory_camp_inspect` | - |
| Maze view | screen | Maze | explore | wireframe corridors, doors as inner frames, command line, party window | W A D K C S I O | "You can't walk through walls!" | `gameplay_maze_f1_start`, `gameplay_full_view` | - |
| Camp | menu | maze C, maze entry | rest stop | inspect, reorder, equip, leave | 1-6 R E Enter | - | `gameplay_camp` | - |
| Square prompts | prompt | stepping on stairs, elevators | move between floors | "Stairs up, take them (Y/N)?" | Y N | - | `gameplay_f2_stairs` | - |
| Signs | message | stepping on a message square | story, hints | framed text, "Press Enter" | Enter | - | `dialogue_sign_f1`, `dialogue_werdna_sign`, `dialogue_f4_desk` | - |
| DUMAPIC report | message | camp spell | position | facing, east, north, down | Enter | - | `system_dumapic` | the only position display |
| Battle | screen | encounter | fight | monster groups with counts, member options, picture, party orders | F P S D U R T, 1-4 | "Press Enter to fight, or T)ake back orders" | `battle_options`, `battle_spell_prompt` | - |
| Chest | menu | after a won fight | loot | chest picture, five choices | O C L I D | - | `battle_chest` | - |
| Cemetery | screen | party killed | game over | tombstones, "Press Enter to leave the cemetery" | Enter | - | `gameover_cemetery` | - |
| Ending | screen | castle with the amulet | win | congratulations, reward, chevron | Enter | - | `ending_congratulations`, `ending_chevron` | - |

## 3. Screen flow
```
title --S--> (loader answers the disk prompts) --> CASTLE
CASTLE: G tavern | A inn | T temple | B Boltac's | E edge of town
EDGE OF TOWN: T training (create / inspect / roster) | M maze | C castle | U utilities | L leave game (to DOS)
M maze --> "Entering Proving Grounds of the Mad Overlord" --> CAMP --Enter--> maze view (floor 1, stairs up)
maze view: W/A/D move | K door | C camp | I inspect | S/O view | square events (stairs, signs, fights)
encounter --> battle rounds --> chest (or cemetery) --> maze view
stairs up on floor 1 --> CASTLE (with the amulet: ENDING --> CASTLE)
```
(verified)

## 4. Elements in detail
- **Party window** (bottom, every castle and maze screen): number, name, alignment-class ("G-FIG"), armour
  class, hit points now, status column (maximum hit points when well, else the condition; in battle the order).
- **Maze view**: white lines only; the walls of up to four squares ahead; doors are drawn as an inner frame on
  a wall; darkness hatches the view (verified `gameplay_dark`).
- **Battle top box**: up to four lines "N) count NAME (alive)"; names are generic until identified (verified).

## Open questions
- What I)nspect does in the maze and whether S and O are toggles in every state (one try each).
- The Leave game screen ("Thanks for playing Wizardry!" is printed by the loader on the DOS screen).
