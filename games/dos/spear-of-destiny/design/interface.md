# Spear of Destiny (DOS) - interface (UI/UX lens)

Every screen, menu, prompt and permanent element, with what it shows, accepts and leads to. Shots are ids of
the set `main` (`../shots/main/index.md`) unless they start with a number (set `start`). Notation:
[README.md](README.md). Judgements are marked **Observation:**.

## Conventions
- **Input:** keyboard only in this capture (mouse and joystick are offered). Menus: arrows, Enter, Esc. Play:
  W/A/S/D (the bundle's CONFIG.SOD), Ctrl fire, Space use, Shift run, Alt strafe, 1-4 weapons, Esc menu.
- **Layout:** 320x200; the 3D view on top, the blue status bar at the bottom (floor, score, lives, face,
  health, ammo, keys, weapon). Menus are boxes on a blue rippled background with red gothic titles and a
  "Move / Select / Esc back" hint line.
- **Feedback:** red full-screen flash when hit, gold flash on pickups, the face on the status bar, muzzle
  flash, enemies' death falls. **Observation:** the face is the main health signal; the number beside it is
  small.
- **Text:** bitmap fonts; menu entries in grey with the chosen one white and an arrow pointer.
- **State visibility:** everything the player owns is on the status bar; no map, no inventory screen.
- **Help:** none in this build (no Read This!).

## Inventory
| Screen / element | Purpose | Shows | Accepts | Leads to | Shots |
|---|---|---|---|---|---|
| Sign-on | program start | banner, free memory, detected devices | none | rating screen | `signon`, `01_signon` |
| PC-13 rating | attract | "Profound Carnage" rating | none | title | `02_rating` |
| Title picture | attract | the logo over the tower | any key | Options | `title_screen`, `03_picture` |
| Attract credits | attract | id Software staff | any key | Options | `credits_id` |
| High Scores | list | name, level (floor or a Spear icon for a finished game), score | any key | Options | `high_scores`, `highscore_entry` |
| Options menu | main menu | New Game, Sound, Control, Load Game, Change View, View Scores, Back to Demo, Quit; in play also Save Game, End Game, Back to Game | arrows, Enter, Esc | each entry | `menu_options`, `04_options`, `21_ingame_options` |
| Skill menu | choose difficulty | four skills, a face per skill | arrows, Enter | Get Psyched | `menu_difficulty`, `menu_difficulty_daddy`, `menu_difficulty_hurt`, `menu_difficulty_death`, `05_difficulty` |
| Get Psyched! | loading | banner with a progress bar | none | play | `06_get_psyched` |
| Sound | settings | three groups: sound effects, digitized sound, music | arrows, Enter | back | `options_sound` |
| Control | settings | mouse, joystick, GamePad switches, sensitivity, customize | arrows, Enter | back | `options_control` |
| Load / Save Game | slots | ten named slots | arrows, Enter, typing | game | `menu_load`, `22_slots`, `23_slot_name`, `24_saved` |
| Change View | settings | a black box sized with the arrows | arrows, Enter, Esc | back | `options_view` |
| Quit prompt | confirm | a joke line ("waste a few more productive hours?") | Y / N | DOS or back | `menu_quit` |
| 3D view | play | walls, doors, objects, enemies, the weapon | movement keys | | `floor1_start`, `env_f8` |
| Status bar | permanent | floor, score, lives, face, health %, ammo, keys, weapon | none | | `hud` |
| Message box | cheat/debug feedback | white box with black text in the view | key | play | `cheat_mli`, `debug_keys`, `debug_god`, `debug_warp`, `debug_coords` |
| Hit flash | feedback | whole screen tinted red | none | | `12_guard_fires`, `face_9` |
| Death dissolve | feedback | the view fills with red pixels, dead face | none | floor restart | `face_19`, `face_22`, `face_25`, `face_28` |
| Floor tally | end of floor | B.J. portrait, floor completed, bonus, time, par, three ratios counting up | key | next floor | `tally_floor1` |
| Victory animation | ending | B.J. with the Spear on teal, kneeling, collapsing | none | You Win! | `bj_spear`, `bj_kneels`, `bj_collapsed` |
| You Win! | ending | total time, kill/secret/treasure averages | key | end pages | `victory_win` |
| End pages | ending | picture pages with text, credits, Thanks for playing, THE END | key per page | High Scores | `end_text`, `end_debt`, `end_allies`, `end_another_story`, `end_title`, `credits_id_game`, `credits_formgen`, `credits_beta`, `end_thanks`, `end_the_end` |
| Name entry | high score | the new row at the top with a cursor | typing, Enter | Options | `highscore_entry`, `highscore_ryz` |

## Screen flow
Sign-on -> PC-13 -> title -> (attract: credits, high scores, demo) -> any key -> Options -> New Game -> skill ->
Get Psyched -> play <-> Esc Options (Save/Load/End Game) -> elevator -> tally -> next floor ... floor 18 Spear
-> floor 21 -> Angel killed -> victory animation -> You Win! -> 9 end pages -> THE END -> High Scores (name
entry) -> Options. Death -> dissolve -> floor restart, or High Scores when no lives are left.

## Main screens element by element
**Status bar** (`hud`): FLOOR (1-18; floor 21 shows 18), SCORE, LIVES, B.J.'s face (health stage), HEALTH %,
AMMO, two key slots (gold above silver), the weapon picture. **Observation:** floors 19-21 show other numbers
than their index (19 and 20 show their own, 21 shows 18), so the bar does not tell the secret floors apart
from the rest.
