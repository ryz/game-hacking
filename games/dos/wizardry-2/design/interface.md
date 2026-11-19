# Wizardry II: The Knight of Diamonds (DOS) - interface (UI/UX lens)

Every screen, menu, prompt and on-screen element of the game, described as an interface: what it is for, what
it shows, what it accepts, how it answers. Read it to study how the game talks to the player. The same shots
also appear in [systems.md](systems.md), which looks at the rules, and in [content.md](content.md), which shows
the variety of what fills the game; overlap is intended.
Notation: [README.md](README.md). Check: `python3 tools/lenses.py PLATFORM/SLUG`.

Facts carry a confidence tag as everywhere in this folder. A judgement (clear, slow, easy to miss) is written
as **Observation:** with the reason, never as a fact.

## 1. Conventions
The interface is Wizardry I's (verified: identical layouts, fonts and keys; details in
[Wizardry I interface](../../wizardry/design/interface.md)). Short form and what differs:
- **Input:** keyboard only; one letter per menu entry (the letter before ")"), digits for party members,
  letters for roster characters, Enter (a bent arrow on screen) leaves or confirms, typed text for spells and
  riddle answers (verified).
- **Layout:** 320 x 200, four colours (CGA cyan/magenta/white on black): a title box at the top ("LLYLGAMYN",
  "CAMP", "TRAINING GROUNDS", "MOVE CHARACTERS:"), the menu box in the middle, the party list at the bottom
  (# CHARACTER NAME CLASS AC HITS STATUS) (verified).
- **Text:** capitals only; the place name of the Castle is "Llylgamyn" (Wizardry I's Castle had the same title
  box; verified here). Long story texts fill the upper box and wait for Enter page by page (verified: Gnilda,
  sphinx).
- **Feedback:** short messages in the middle box ("RYZ has been moved", "RYZ got an item.", "* Powerless *");
  a wrong riddle answer gives no message, the party is simply back on the square before (verified).
- **State visibility:** the party list (AC, hits, status, or the order in battle) is always on screen; a "+"
  after the hits marks regeneration (verified).
- **Help:** none on screen beyond the menus; the import is explained only by the 2019 `run.bat` text.

## 2. Screen inventory
New or changed screens; the shared ones are listed in Wizardry I's inventory and only named here.

| Screen / element | Type | Reached from -> leads to | Purpose | Shows | Accepts | Feedback and errors | Shots | Observation |
|---|---|---|---|---|---|---|---|---|
| Title | screen | power-on -> scenario disk / Castle | start | logo, "Scenario #2 - The Knight of Diamonds", a picture that changes, S)tart / M)ake scenario disk | S, M | - | `title_screen` | - |
| Make scenario disk | prompt | Title M | prepare a disk | "The disk you inserted has data on it. If you use it, the data will be erased! Use it (Y/N)?" | Y, N | - | planned `menu_make_scenario` | - |
| Castle, Tavern, Inn, Temple, Boltac's, Edge of Town | menu | as Wizardry I | - | as Wizardry I | as Wizardry I | as Wizardry I | `menu_castle`, planned `menu_tavern`... | - |
| Training Grounds | menu | Edge T -> inspect, roster | look at characters | I)nspect a character, R)oster of characters, Leave (no create) | I, R, Enter | - | planned `menu_training` | **Observation:** the menu shrinks to two entries, the only sign that this scenario cannot create characters |
| Wizardry Utilities | menu | Edge U -> change name, move, restart | disk housekeeping | C)hange name, M)ove characters, R)estart an "out" party, Leave | C, M, R, Enter | - | planned `menu_utilities` | - |
| Move characters | list | Utilities M -> moved messages -> Utilities | pick characters from the source disk | "Select chars by (letter), Enter to move them, or (Esc) to exit without moving", the source roster in two columns | letters (toggle "+"), Enter, Esc | a "+" replaces ")" after the letter | planned `system_move_list`, `system_move_marked` | **Observation:** the disk swap prompts of the original are answered by the 1998 loader, so the player sees none |
| Moved message | message | Move -> next character | report | "RYZ has been moved" | - (timed) | - | planned `system_move_moved` | - |
| Camp entry | transition | Edge M -> camp | loading | "Descending into the ruins under the Temple of Gnilda" | - | - | planned `gameplay_camp` | - |
| Maze view, camp, sheets, battle | screen | as Wizardry I | - | as Wizardry I | - | - | `gameplay_maze_f1_start`, `battle_f1_kobold_kings` | - |
| Riddle prompt | prompt | riddle square -> pass or pushed back | test | the story text, then "What is your answer ?" (sphinx) or "Your answer ? >" (Gnilda) with a cursor | text, Enter | none on a wrong answer | `dialogue_sphinx`, `dialogue_gnilda_test` | - |
| Story pages | message | special squares | tell | up to 12 lines per page, Enter for the next | Enter | - | `dialogue_staff_gift` | - |
| Item found | message | battle end, Gnilda | report | "MNZ found : ARMOR", "RYZ got an item." | - | - | planned `boss_found_armor`, `dialogue_got_staff` | - |
| Congratulations | screen | Castle arrival with the staff, alone -> knight prompts | the ending | the text and "Press Enter to select your knights!" | Enter | - | `ending_congratulations` | - |
| Make a knight | prompt | Congratulations -> next character -> Castle | choose companions | "Make CONDI a knight (Y/N)?" one roster character at a time | Y, N | - | planned `ending_make_knight` | **Observation:** asked for every roster character, stock ones included, not only the bearer's party |
| Award marks | hud element | sheet title line | show honours | ">G" / ">K" in quotes after the race | - | - | planned `ending_sheet_ryz` | - |

## 3. Screen flow
Power-on (DOSBox Pure menu, WIZ2.COM) -> Title -> S -> (loader answers the disk prompt) -> Castle ->
Edge of Town -> Utilities -> Move characters -> moved messages -> Utilities -> Castle -> Tavern (add) ->
Castle -> Edge of Town -> Maze -> camp -> maze view <-> battle / special squares -> stairs up at floor 1
(0,0) -> Castle; with the staff, alone: Congratulations -> Make ... a knight? (each character) -> Castle.
Leave game -> DOS ("Thanks for playing Wizardry!").

## 4. Elements in detail
Shared with Wizardry I (maze view, party list, battle screen, sheet): see its interface document. New element:
the award marks on the sheet's first line (`RYZ L 11 G-FIG HUMAN ">G"`).

## Open questions
- Utilities C)hange name and R)estart screens; M)ake scenario disk after Y.
- The floor 2 riddle's prompt text.
