# Wolfenstein 3D (DOS) - interface (UI/UX lens)

Every screen, menu, prompt and on-screen element of the game, described as an interface: what it is for, what
it shows, what it accepts, how it answers. Read it to study how the game talks to the player. The same shots
also appear in [systems.md](systems.md), which looks at the rules, and in [content.md](content.md), which shows
the variety of what fills the game; overlap is intended.
Notation: [README.md](README.md). Check: `python3 tools/lenses.py PLATFORM/SLUG`.

Facts carry a confidence tag as everywhere in this folder. A judgement (clear, slow, easy to miss) is written
as **Observation:** with the reason, never as a fact.

## 1. Conventions
- **Input:** keyboard only here (mouse and joystick options exist, `options_control`). Menus: Up/Down move a
  gun-shaped cursor, Enter selects, Esc goes back (verified: `menu_options`). Play: held keys, read 70 times a
  second; this bundle binds W/A/S/D (verified). Text entry for save names and the high-score name (verified:
  `29_save_name`, `highscore_ryz`).
- **Layout:** 320x200. In play the 3D view fills the top, the status bar the bottom 40 lines (verified:
  `hud`). Menus are red screens with a gothic title banner and a footer of key hints (verified: `menu_options`).
- **Text:** gothic logo lettering for titles ("Options", "High Scores", "Get Psyched!"), a bold sans font in
  menus; disabled entries in dark red (verified: `options_control`); in-game messages in a grey box with black
  text (verified: `cheat_mli`).
- **Feedback:** a screen flash for events: gold for treasure (`treasure_pickup`), yellow-green for a key
  (`key_gold_taken`), red for damage (`damage_flash`) (verified). Quitting asks first, with a joke prompt
  (verified: `menu_quit`).
- **State visibility:** floor, score, lives, B.J.'s face, health, ammunition, keys and weapon are always on the
  status bar (verified: `hud`); ratios only at the tally.
- **Help and onboarding:** none in game in this build (no "Read This!", verified); controls are in the manual.

## 2. Screen inventory

| Screen / element | Type | Reached from -> leads to | Purpose | Shows | Accepts | Feedback and errors | Shots | Observation |
|---|---|---|---|---|---|---|---|---|
| Sign-on | screen | power-on -> PC-13 | memory and devices found | id and Activision logos, memory bars, devices | any key | none | `signon` | |
| PC-13 rating | screen | sign-on -> title | rating notice "Profound Carnage" | rating badge | timed | none | `02_pc13` | |
| Title | screen | PC-13 -> attract loop / Options | title picture | logo, B.J. and a guard | any key | none | `title_screen` | |
| Credits | screen | attract loop | id staff | names by job | any key | none | `credits_id` | |
| High Scores | list | attract loop, menu, end of a game | best seven scores | name, episode/floor, score | key | new entry gets a cursor | `high_scores`, `highscore_entry`, `highscore_ryz` | |
| Demo | screen | attract loop | recorded play | the play screen with a "Demo" banner | any key -> Options | none | `demo` | |
| Options menu | menu | any key in the attract loop, Esc in play | main menu | New Game, Sound, Control, Load Game, Save Game and End Game (in play), Change View, View Scores, Back to Demo/Game, Quit | Up/Down, Enter, Esc | in-play entries added | `menu_options`, `24_ingame_menu` | **Observation:** the same menu serves both before and during a game |
| Episode select | menu | New Game -> difficulty | choose one of six episodes | six pictures and titles | Up/Down, Enter | none | `menu_episodes` | |
| Difficulty | menu | episode -> Get Psyched | choose skill | four lines, a face that changes with the cursor (baby B.J., plain, confident, red-eyed) | Up/Down, Enter | none | `menu_difficulty`, `menu_difficulty_daddy`, `menu_difficulty_hurt`, `menu_difficulty_death` | |
| Get Psyched | transition | difficulty -> play | loading | banner and status bar | none | none | `09_get_psyched` | |
| Sound | menu | Options | sound devices | effects, digitized sound, music | Enter toggles | missing devices greyed | `options_sound` | |
| Control | menu | Options | input devices | mouse, joystick, GamePad, sensitivity, customize | Enter | missing devices greyed | `options_control` | |
| Change View | prompt | Options | size the 3D window | black window frame, instructions | arrows, Enter, Esc | | `options_view` | |
| Load Game / Save Game | list | Options | ten slots | slot names or "empty" | Up/Down, Enter, typing | name field with cursor | `menu_load`, `28_save_slots`, `29_save_name`, `30_saved` | |
| Quit prompt | prompt | Quit | confirm | joke text | Y/N | | `menu_quit` | |
| Play view | screen | Get Psyched | the game | 3D view, weapon in hand | play keys | flashes | `e1m1_start`, `env_e2m1` | |
| Status bar | hud element | play | state | floor, score, lives, face, health, ammo, keys, weapon | none | face looks hurt as health falls (7 stages, dead face, grin on a chain gun) | `hud`, `15_guard_dead`, `face_100`, `face_80`, `face_60`, `face_43`, `face_34`, `face_6`, `face_1`, `chaingun_grin` | |
| In-game message box | message | cheats, debug keys | report | grey box, text | key | | `cheat_mli`, `debug_on`, `debug_god`, `debug_warp`, `debug_coords` | |
| Floor tally | screen | elevator switch -> next floor | results | B.J., bonus, time, par, ratios | key | numbers count up | `tally_floor1` | |
| Episode won | screen | boss floor exit -> end text | results | You Win!, total time, averages, code | key | | `victory_run`, `victory_win` | |
| End text | screen | episode won -> High Scores | story | pages with a picture, page number | arrows page, Esc | "pg 1 of 2" | `episode_end_text`, `episode_end_text_2` | |
| Death | transition | health 0 | losing a life | red flash, dead face, red dissolve, floor fades in from red | none | | `damage_flash`, `death_fizzle`, `death_by_hans`, `death_by_hans_red`, `death_restart` | |

## 3. Screen flow
- Power-on -> sign-on -> PC-13 -> title -> credits -> High Scores -> demo -> title ... (any key: Options)
- Options -> New Game -> episode -> difficulty -> Get Psyched -> play
- Play -> Esc -> Options (Save, Load, End Game, Back to Game)
- Play -> elevator switch -> floor tally -> Get Psyched -> next floor
- Boss floor -> exit -> run out -> You Win! -> end text -> High Scores (name entry)
- Play -> death -> same floor again, or (no lives) -> High Scores (name entry) -> title

## 4. Elements in detail
Status bar, left to right (verified: `hud`): FLOOR (number within the episode), SCORE, LIVES, B.J.'s face
(looks around; bloodier as health drops), HEALTH in percent, AMMO, two key slots (gold above silver), the
picture of the weapon in hand.

The face (verified: one real fight against Hans Grosse, `face_100` to `death_by_hans`; faces read at 3x):
| Health | Face | Shot |
|---|---|---|
| 100% | clean, looking around | `face_100` |
| 80% | a cut on the cheek | `face_80` |
| 60% | blood under the nose | `face_60` |
| 43% | blood at the mouth | `face_43` |
| 34% | blood on nose and mouth | `face_34` |
| 6% | swollen, eyes half shut | `face_6` |
| 1% | eyes almost shut, bloodied | `face_1`, `face_1_hans_near` |
| 0% | dead face, mouth open | `death_by_hans` |
| any, chain gun picked up | broad grin, for a moment | `chaingun_grin` |
Stages change every 16 points or so (85-100, 69-84, 53-68, 37-52, 21-36, 5-20, 1-4: source, the released
code; the frames agree). The face also turns left and right at random in every stage (verified).

## Open questions
- ~~The face's damage stages~~ captured 2026-11-25 (table in 4); the god-mode face not captured.
