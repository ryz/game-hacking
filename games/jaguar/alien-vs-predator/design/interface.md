# Alien vs Predator - interface (UI/UX lens)

Every screen, menu, prompt and on-screen element of the game, described as an interface: what it is for, what
it shows, what it accepts, how it answers. The same shots also appear in [systems.md](systems.md) (rules) and
[content.md](content.md) (variety). Notation: [README.md](README.md).
Check: `python3 tools/lenses.py jaguar/alien-vs-predator`. Shot ids in backticks are in `../shots/main/`
unless marked `start:` (`../shots/start/`).

Facts carry a confidence tag as everywhere in this folder. A judgement is written as **Observation:**.

## 1. Conventions
- **Input:** any fire button confirms in the front-end menus **(verified: A, B and C all pick a character)**;
  inside terminals the buttons split up: B selects, A next page, B previous page, C exits, as the footer of
  each terminal page says **(verified: `terminal_menu`, `log_page1`)**. In play, A is "use", B is "attack"
  **(verified)**. The keypad picks weapons (1-4) and the Predator's vision (6) **(verified)**.
- **Layout:** the 3D view fills the screen; the HUD is drawn as a translucent frame over it in the species'
  colour: green for the Marine, violet for the Alien, gold for the Predator **(verified: `hud_marine`,
  `alien_sublevel1`, `predator_sublevel1`)**. Its brightness is set in the pause menu **(verified:
  `pause_options`)**.
- **Text:** front-end text is green on black in a fixed-width font (briefings, intro); terminals use white
  text on a green Weyland-Yutani screen that types itself out letter by letter **(verified)**.
- **Feedback:** pick-ups and arrivals show large green outlined letters in the middle of the view
  (SHOTGUN COLLECTED, ENTERING SUBLEVEL 5) **(verified: `pickup_shotgun`, `entering_sublevel`)**; damage tints
  the whole screen (red, purple, yellow-green by species) **(verified: `marine_hurt`, `alien_hurt`,
  `predator_hurt`)**.
- **State visibility:** score or honor points at the top, energy bar, weapons with their ammo bars at the
  right, security level at the left (Marine) **(verified: `hud_marine`)**.
- **Help:** prompts sit at the bottom of menus (LEFT and RIGHT to rotate / FIRE to select; UP and DOWN to
  change letter ...) **(verified: `select_alien`, `highscore_entry`)**.
- **Observation:** the menu after a game over drops the first presses for several seconds (the menu redraws
  from the title): routes need long waits there (playbook).

## 2. Inventory
| Screen / element | Purpose | Shows | Accepts | Answers | Leads to | Shots |
|---|---|---|---|---|---|---|
| Boot logo (Jaguar console) | console start | JAGUAR, then ATARI logo | - | - | title | none: needs the `ntsc-bios` model, which a set cannot mix with the game's model (verified in a preview, f400) |
| Title | game start | logo, Alien and Predator art, copyright | fire | menu | main menu | `title_screen`, `start:01_title` |
| Main menu | choose an activity | Select Character, Restore Game, High Scores, Credits | up/down, fire | arrow cursor | carousel, restore list, table, credits | `menu_main`, `start:02_main_menu` |
| Attract intro | idle demo | ship pictures with typed status lines | fire returns | - | menu | `intro_signal`, `intro_docked`, `intro_proximity` |
| Character carousel | pick a species | framed portrait in front, two others at the sides | left/right, fire | rotates | briefing | `select_alien`, `select_predator`, `select_marine`, `start:03_select_alien`, `start:04_select_marine` |
| Briefing | goal of the species | portrait, typed text, LOADING SIMULATION... PRESS FIRE | fire (after loading) | - | first control | `brief_alien`, `brief_predator`, `brief_marine`, `start:05_briefing_marine` |
| HUD (Marine) | state | portrait, score, security, weapons 1-4 with ammo bars | - | updates live | - | `hud_marine`, `marine_brig` |
| HUD (Alien) | state | Alien head top left with the cocoons-in-progress mark under it, score at the top, three attack icons (claw, jaw, tail) with strength bars and the energy bar at the right | - | mark appears after COCOON COMPLETED | - | `alien_start`, `alien_sublevel2`, `alien_cocoon` |
| HUD (Predator) | state | Predator head, honor points, weapon list, energy trace, mask icon | - | - | - | `predator_start`, `predator_sublevel1` |
| Motion tracker | find movement | round radar with blips and a distance in metres bottom left | - | - | - | `marine_tracker`, `marine_tracker_blips` |
| Centre message | pick-up / arrival / cocoon | large outlined text over the view | - | fades after about 3 s | - | `pickup_rounds`, `entering_sublevel`, `predator_attained`, `alien_cocoon_enemy`, `alien_cocoon_complete` |
| Self-destruct timer | time left to escape | TIME m:ss in the centre, red alert tint | - | counts down from 2:00 | ending | `self_destruct` |
| Predator vision filters | see in the dark / through cloak | five colour treatments of the whole view and HUD | keypad 6 | next filter | - | `predator_vision_1`, `predator_vision_2`, `predator_vision_3`, `predator_vision_4`, `predator_vision_5` |
| Facehugger attack | being attacked | the facehugger fills the screen, red tint | rapid left-right **(source)** | - | - | `marine_facehugger_attached` |
| Damage tint | being hit | whole screen tinted | - | - | - | `marine_hurt`, `start:15_second_alien_hit` |
| Pause | stop | PAUSED | Pause resumes, Option opens the menu | - | pause menu | `pause_paused`, `start:24_paused` |
| Pause menu | HUD brightness, save | HUD slider, GAME 1-3, B - SAVE | up/down, left/right, B | slot flashes on save | game | `pause_options`, `start:25_pause_options`, `start:26_save_slot`, `start:27_saved` |
| Restore list | load a save | RESTORE GAME n in the species' font, [ NO GAME ], CANCEL | up/down, fire | - | game | `menu_restore`, `start:28_restore_list` |
| Terminal | information | terminal screen in the wall | A at close range | screen opens | terminal menu | `terminal`, `start:18_terminal` |
| Terminal menu | choose | MAIN MENU: Level Schematic, General Log; B. SELECT C. EXIT | up/down, B, C | text types itself | schematic, log | `terminal_menu`, `start:19_terminal_menu` |
| Level schematic | map | numbered room legend, plan with rooms, E = elevator | C | - | terminal menu | `map_level3`, `start:20_level_schematic` |
| General Log | story and hints | paged text, PAGE n OF m, A. NEXT B. PREVIOUS C. EXIT | A, B, C | - | terminal menu | `log_page1`, `log_page2`, `log_page3`, `start:21_general_log_1`, `start:22_general_log_2`, `start:23_general_log_3` |
| Lift | change level | hatch; inside, big up and down arrows | A, up/down + A | doors close, level changes | next sublevel | `lift_hatch`, `lift_inside`, `lift_arrived` |
| GAME OVER banner | death | GAME OVER in outlined letters over the last view | - | after about 1 s the badge | game over | `alien_gameover`, `predator_gameover` |
| Game over | death | USCM badge, SIMULATION TERMINATED typed out | fire | - | high scores | `gameover` |
| Ending screens | win | Alien: Queen art, THE HIVE IS WHOLE AGAIN / EXPANSION CONTINUES; Predator: trophy art, HONOR IS YOURS!; Marine: capsule launch countdown, explosion, typed USCM report (or the failure report) | fire | - | high scores | `ending_alien`, `ending_predator`, `ending_marine_launch`, `ending_marine_zero`, `ending_marine_report`, `ending_marine_survivor`, `ending_marine_destroyed` |
| High score entry | name a new score | table with the new line, letter cursor, help lines | up/down letter, left/right cursor, fire | - | title | `highscore_entry` |
| High score table | records | five names and scores, Press FIRE | fire | - | menu | `highscores`, `highscore_ryz` |
| Credits | staff | scrolling names over the logo | fire | - | menu | `credits` |

## 3. Screen flow
Title -> (fire) main menu -> Select Character -> carousel -> briefing -> play. Idle on the menu -> attract
intro -> menu. Play -> Pause -> (Option) pause menu -> save -> play. Play -> terminal -> menu -> schematic /
log -> exit. Death -> GAME OVER banner -> game over -> (high score entry) -> title. Win -> ending screen(s) -> high scores. * + # in play -> title. Main menu -> Restore
Game -> slot -> play **(verified for each arrow except restore -> play)**.

## 4. Main screens element by element
- **Marine HUD** (`hud_marine`): top: SCORE and the value; left: the Marine's face above SECURITY and its two
  digits; right: weapons 1-4, each with an ammo bar, the selected one lit; the energy bar is the strip above
  the weapon list **(verified)**. **Observation:** the green frame is drawn over the view and hides much of
  its left and right thirds.
- **Terminal schematic** (`map_level3`): left box: LEVEL THREE and the legend E Elevator, 1 Airlock, 2 Brig,
  3 Barracks, 4 Briefing Room, 5 P O Area, 6 Library, 7 Canteen, 8 Kitchen, 9 Meeting Room; right box: a plan
  of the level with numbered rooms; C. EXIT at the foot **(verified)**. The player's position is not marked
  **(verified)**.

## Open questions
- The Predator's HUD elements were not identified one by one (medkit reserve).
- Screens not reached: First Aid (med-lab), the self-destruct and escape-capsule terminal pages (texts are in
  DRAM: "A. DESTRUCT C. ABORT", "B. LAUNCH ESCAPE CAPSULE"), shown here only through the poked flags.
