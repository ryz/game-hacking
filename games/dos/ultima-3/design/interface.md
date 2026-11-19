# Ultima III: Exodus (DOS) - interface (UI/UX lens)

Every screen, menu, prompt and on-screen element of the game, described as an interface: what it is for, what
it shows, what it accepts, how it answers. Read it to study how the game talks to the player. The same shots
also appear in [systems.md](systems.md), which looks at the rules, and in [content.md](content.md), which shows
the variety of what fills the game; overlap is intended.
Notation: [README.md](README.md). Check: `python3 tools/lenses.py dos/ultima-3`.

Facts carry a confidence tag as everywhere in this folder. A judgement (clear, slow, easy to miss) is written
as **Observation:** with the reason, never as a fact.

## 1. Conventions
- **Input:** keyboard only. On the play screen one letter is one command, arrows move; the command then asks
  for a player number (1-4) and/or a direction (an arrow). In the menus a choice is a letter **and Enter**: the
  letter echoes the whole word ("Option:Organize", `menu_option_echo`) and Enter confirms; shop answers (Y/N,
  Buy/Sell, item letters) work the same; numbers are digits + Enter; words (Other command, Yell) are typed +
  Enter **(verified)**.
- **Refusals:** a command with nothing to act on answers "<command><-What?" (`gameplay_refusals`), "Not
  Here!", "None Left!" (`system_none_left`), "No effect!" (`system_no_effect`), "Not a DNG cmd!" below ground
  (`system_dungeon_not_cmd`), "Not usable cmd!" in combat **(verified)**.
- **Layout:** 320x200 in four CGA colours. Play screen: the map view (11x11 squares) at the left in a magenta
  frame with the two moons "(a)(b)" on top and the wind ("North Wind") below; four status panels at the right;
  the message area below them **(verified, `hud_status`)**. Menus use the same frame with the cyan "Exodus" logo
  on top **(verified, `menu_main`)**.
- **Line of sight:** the map view hides what walls, forests and mountains block (black squares), on Sosaria and
  in townes **(verified: `gameplay_dark_forest`, `dialogue_lcb_9`)**.
- **Text:** grey upper and lower case in a fixed 8x8 font; names keep the case typed ("ryz"); prompts end in
  "?" or "-"; a small triangle is the text cursor **(verified)**.
- **Feedback:** every action prints its name ("North", "Pass", "Enter Castle!") and its result; loading prints
  "Please wait..."; spells and attacks flash the field or mark the struck square (`battle_spell_hit`,
  `battle_bow`); the acting member's panel is shown inverted while a healer or shrine works on it
  (`system_shrine_shazam`) **(verified)**.
- **State visibility:** the panels always show magic points, level, hit points, food and the condition letter
  (G, P, D, A); gold, statistics, equipment, cards and marks only through Ztats, one line per key **(verified)**.
  **Observation:** panel values redraw only when the game touches them, so a change made elsewhere (a status
  set by a trap on someone else) shows late (`system_trap_gas`: four "Poisoned!" lines, one P on the panels).
- **Help:** none in the game; hints come from townspeople, the pub and the oracle **(ROM text, verified)**.

## 2. Screen inventory
| Screen / element | Type | Reached from -> leads to | Purpose | Shows | Accepts | Feedback and errors | Shots | Observation |
|---|---|---|---|---|---|---|---|---|
| Title | screen | power-on -> demo | identity | the Exodus logo drawn line by line, Ultima III, by Lord British, a walking party and a dragon **(verified)** | nothing while drawing | - | `title_drawing`, `title_byline`, `title_screen` | 40 s to draw at the original speed |
| Attract demo | screen | title -> main menu | show play | a strip of Sosaria with castles, frigates and monsters moving, "Press <Space>" **(verified)** | space | - | `title_demo`, `title_demo_moves`, `menu_return_view` | |
| Main menu | menu | demo -> Organize, Journey, demo | start | "From the depths of hell... he comes for VENGEANCE!", three options, the port's credit **(verified)** | R/O/J + Enter | the letter echoes the word | `menu_main`, `menu_option_echo` | |
| Party Organization | menu | main -> seven actions | roster | seven options **(verified)** | letter + Enter | "(Party in Use)", "(No one there)", "(Not Empty!)" | `menu_organize`, `menu_form_inuse`, `menu_terminate`, `menu_create_notempty` | |
| Create | form | Organize -> Organize | new character | Entry#, Points:50, Name, Sex, Race, Type, four statistics, O.K.? **(verified)** | digits, letters + Enter | a value over the points left is not taken | `menu_create_entry`, `menu_create_name`, `menu_create_sex`, `menu_create_race`, `menu_create_type`, `menu_create_str`, `menu_create_ok`, `menu_create_done`, `menu_create_fuzzy`, `menu_create_overspent` | **Observation:** no list of races or classes is shown; the letters must be known from the manual |
| Register | list | Organize | roster | entries 01-20: sex-race-class-status letters, name, * for party members **(verified)** | space | - | `menu_register` | |
| Form the Party | prompt | Organize | party | Player-1..4 = entry numbers, "(Formed)" **(verified)** | digits + Enter | "(Party in Use)" | `menu_form`, `menu_disperse` | |
| Look at a Character | sheet | Organize | one character | name, sex, race, type, status, weapon, armour, statistics, hit points, experience, food, gold **(verified)** | entry number | - | `menu_look` | the only whole character sheet in the game |
| Play screen | screen | Journey -> everything | play | map view, moons, wind, panels, messages **(verified)** | command keys | "Invalid Move!" | `hud_status`, `gameplay_start`, `gameplay_invalid_move` | |
| Status panel | hud element | play screen | party state | per member: number, name, condition, sex-race-class letters, M:, L:, H:, F: **(verified)** | - | updates when touched | `hud_status`, `battle_member_killed` | |
| Moons and wind | hud element | frame of the map | travel state | the two moon phases (0-7), the wind's name **(verified)** | - | - | `system_moongate`, `system_dawn_appears`, `system_wind` | the only clue for moongates and Dawn |
| Message area | hud element | play screen | log and prompts | the last seven lines; each command line led by a small arrow **(verified)** | - | - | all | answers scroll the question away |
| Command prompts | prompt | a command key | choose who/where | "Cast by whom-", "Whose torch:", "Plr to search-", "Direct?", "From Player: To Player:", "Whose gem?" **(verified)** | 1-4, arrows | - | `system_hand_gold`, `system_steal`, `system_spell_sanctu`, `system_look` | |
| Ztats | message | Z -> play | character sheet | one line per key: statistics, H.P., H.M., gold, exp., gems, keys, powders, torches, marks, cards, weapon, armour, owned arms with letters **(verified)** | any key | - | `inventory_ztats_new`, `inventory_ztats_new_arms`, `inventory_ztats_1`, `inventory_ztats_2`, `inventory_ztats_marks`, `inventory_ztats_weapons`, `inventory_ztats_armour` | **Observation:** 22 lines through a seven-line window; never seen whole |
| Map picture | screen | P (gem), Vieda -> play | orientation | the whole land in miniature **(verified)** | any key | - | `system_peer_gem`, `system_spell_vieda` | |
| Talk | message | T with a person | hints | "Who will Transact? 1 Direct? North", the line **(verified)** | player, direction | "Not Here!" if the person moved | `dialogue_moon_1`, `dialogue_fawn_2`, `dialogue_exodus_0` | people wander, so the square must be right |
| Lord British | message | T at the throne | levels | "Welcome my child" and the verdict **(verified)** | player, direction | - | `dialogue_lb_experience`, `dialogue_lb_greater`, `dialogue_lb_mark`, `dialogue_lb_nomore` | |
| Shop dialogue | message | T over a counter | trade | the shop's name, its offer or list, a question **(verified)** | letters/numbers + Enter | "Not enough gold!", "Out you scum!", "You don't own one of those!" | `shop_pub`, `shop_grocer`, `shop_weapons`, `shop_armour`, `shop_healer`, `shop_guild`, `shop_oracle`, `shop_horses`, `shop_weapons_poor`, `shop_armour_sell` | lists are paged: a key shows the rest |
| Combat screen | screen | a fight -> play | battle | the 11x11 field, "---Conflict!!---", "->Orcs", "----Player 1----", the acting member blinking **(verified)** | arrows, A, C, space | "Missed!", "Hit!", "Killed! Exp.+03", "****Victory!****" | `battle_start`, `battle_kill`, `battle_victory`, `battle_orc_hits` | |
| Dungeon view | screen | E on a dungeon -> play | explore | wireframe walls, doors, ladders, chests; "LVL:01", "Head--East" on the frame **(verified)** | arrows, K, D, I | "It's dark!", "Not a DNG cmd!" | `gameplay_dungeon_dark`, `gameplay_dungeon_torch`, `gameplay_dungeon_ladder`, `gameplay_dungeon_chest`, `gameplay_dungeon_l2`, `gameplay_dungeon_l3`, `gameplay_dungeon_l4`, `gameplay_dungeon_l5`, `gameplay_dungeon_l6`, `gameplay_dungeon_l7`, `gameplay_dungeon_l8` | the eight levels look alike but for the number |
| Event pictures | screen | shrine, fountain, rod, Time Lord | moments | a full picture in the map view with its text **(verified)** | player, number | "Shazam!", "How wonderful!", "It left a mark!" | `system_shrine`, `system_fountain`, `system_rod`, `cutscene_timelord` | |
| Quit & Save | message | Q | save | "Quit & Save", the moves, "Please wait..." **(verified)** | - | - | `save_quit` | play goes on |
| Whirlpool texts | message | the whirlpools | transitions | "A huge swirling --WhirlPool-- ...", "You awaken on the shores of a forgotten Land", "All is Dark! You made it!" **(verified)** | - | - | `cutscene_whirlpool`, `cutscene_ambrosia_shore`, `cutscene_ambrosia_return` | |
| All Players Out | message | all dead | game over | the message, D on every panel, a still screen **(verified)** | nothing | - | `gameover_all_out` | no prompt to restart |
| Ending | screen | the fourth card | end | the castle flashing, "Congratulations! ... in 00048393 moves Report thy feat!", the closing text in the map view **(verified)** | nothing | - | `ending_flash`, `ending_congrats`, `ending_text` | |

## 3. Screen flow
- power-on -> title -> attract demo -> (space) main menu
  - Organize a Party -> register / create / form / disperse / terminate / look -> main menu
  - Return to the View -> attract demo
  - Journey Onward -> play screen (Sosaria)
    - E -> towne / castle (walk off the edge back to Sosaria), dungeon (Klimb at level 1's entrance back)
    - a monster -> combat screen -> play screen (a chest left)
    - whirlpool -> Ambrosia (shrine pictures) -> Ambrosia's whirlpool -> Sosaria
    - moongate -> another square of Sosaria
    - fourth card in Castle Exodus -> ending (stays)
    - all dead -> "All Players Out!" (stays)

## 4. Elements in detail
Play screen (verified, `hud_status`): map view 176x176 pixels at the left (11x11 squares of 16x16), the party in
the centre; moons "(0)(1)" centred on the top border; the wind name centred on the bottom border; four panels of
three lines at the right (row 1: number in the border, name, condition letter at the far right; row 2: sex,
race and class letters, M:nn, L:nn; row 3: H:nnnn, F:nnnn); the message area (seven lines) at the bottom right.
In combat the moons and wind stay, the map view becomes the field (`battle_start`); in dungeons the frame reads
"LVL:0n" on top and "Head--East" below (`gameplay_dungeon_torch`).

## Open questions
- None about screens reached; the combat command list (which keys besides A, C, arrows and space) was not read
  from the program.
