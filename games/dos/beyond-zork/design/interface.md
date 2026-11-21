# Beyond Zork: The Coconut of Quendor (DOS) - interface (UI/UX lens)

Every screen, menu, prompt and on-screen element of the game, described as an interface: what it is for, what
it shows, what it accepts, how it answers. Read it to study how the game talks to the player. The same shots
also appear in [systems.md](systems.md), which looks at the rules, and in [content.md](content.md), which shows
the variety of what fills the game; overlap is intended.
Notation: [README.md](README.md). Check: `python3 tools/lenses.py PLATFORM/SLUG`.

Facts carry a confidence tag as everywhere in this folder. A judgement (clear, slow, easy to miss) is written
as **Observation:** with the reason, never as a fact.

## 1. Conventions
- **Input:** keyboard only. Typed commands end with Enter; `PERSON, TEXT` talks to someone. F1-F10 type
  whole commands (F4, F5, F6, F10 wait for the object); DEFINE edits them **(verified, `options_define_keys`)**.
  Menus (Character Setup, SETTINGS, DEFINE) use the arrow keys and Enter; attribute editing uses left/right
  **(verified, `menu_create_adjust`)**. Yes/no questions want YES or NO typed. No command history on the up
  arrow; the keypad does nothing on the PC (playbook). Mouse on the map: manual only (not tried).
- **Layout:** 640x200 graphics in 80 columns, 25 rows of 8-pixel text. Enhanced mode: a title bar with the
  room name, a framed room window with the room description, the auto-map at the right, the scrolling
  transcript and prompt below **(verified, `gameplay_hilltop`)**. Standard mode (MODE): one status line with
  every attribute and the exits over a plain scrolling transcript **(verified, `system_mode_standard`)**.
- **Text:** one fixed-width font in light gray on blue (default palette); words that a scroll or a sound
  makes are underlined (Blarn, Macuga, Kerblam, Bang, snap) **(verified, `inventory_scroll_blarn`,
  `system_cellar_locked`)**. Game messages about the interface come in square brackets ("[SAVE
  completed.]", "[Color pallette 4 of 6.]") **(verified)**.
- **Feedback:** every command is answered in the transcript; the room window is redrawn on a move; while a
  monster is present the room window shows an Endurance bar **(verified, `battle_vapor_attack`)**; bracketed
  notices report experience and endurance changes **(verified, `battle_vapor_won`)**.
- **State visibility:** room name always (title bar or status line); attributes only on STATUS (F3) in
  enhanced mode, always in standard mode; money only on `$`/INVENTORY **(verified, `inventory_list`)**.
- **Help and onboarding:** "nymphs" appear on the keyboard to explain the interface (the financial nymph
  explains CASH, the technical nymph explains that eyes are not needed) **(verified, `inventory_list`,
  `extra_technical_nymph`)**. VERSION prints the release **(verified, `extra_version`)**.

## 2. Screen inventory

| Screen / element | Type | Reached from -> leads to | Purpose | Shows | Accepts | Feedback and errors | Shots | Observation |
|---|---|---|---|---|---|---|---|---|
| Colour question | prompt | BZORK.EXE start -> opening prompt | colour or monochrome | "Do you want color?" in 80x25 text | y / n | - | `boot_color_prompt` | - |
| Opening prompt | prompt | colour question -> prologue / restore | new game, restore, quit | copyright, [Type BEGIN, RESTORE or QUIT.] | typed word | - | `menu_begin`, `save_restore` | - |
| Prologue pages | screen | BEGIN -> title card | story set-up | Y'Gael and the council, [MORE] | any key | - | `cutscene_prologue` | - |
| Title card | screen | prologue -> Character Setup | title | BEYOND ZORK, The Coconut of Quendor | any key | - | `title_card` | text only in Bzork.exe; Frotz shows a picture (`extra_frotz_title`) |
| Character Setup | menu | title -> play | choose how to make the character | five entries | arrows, Enter | - | `menu_character_setup` | - |
| Preset list | menu | Setup -> play | pick one of six presets | names and attribute bars | arrows, Enter | - | `menu_select_preset` | - |
| Random roll | screen | Setup -> play | random attributes | bars and percentages | SPACE rolls, Enter accepts | - | `menu_random_character`, `menu_random_reroll` | - |
| Create your own | screen | Setup -> sex -> name -> confirm | spread 60% potential | bars, Potential bar | arrows | "Are you sure these are the attributes you want?" | `menu_create_character`, `menu_create_adjust`, `menu_create_confirm` | - |
| Sex and name prompts | prompt | Create -> save character? | identity | "[The default is MALE.]", "By what Name ...", "Is "Ryz" correct?" | typed | YES/NO confirmations | `menu_create_name`, `menu_create_done` | the name is capitalised by the game (ryz -> Ryz) |
| Save character? / begin | prompt | confirm -> play | keep the character on disk | "Do you want to save this character before you proceed?", "Press any key to begin the story." | YES/NO, any key | - | `menu_create_begin` | - |
| Main play screen | screen | -> everything | play | title bar, room window, map, transcript, prompt | typed commands, F-keys | messages | `gameplay_hilltop`, `env_cove_street`, `env_mizniaport` | - |
| Auto-map | hud element | always in enhanced mode | where am I | rooms as boxes, lines for exits, arrows up/down, `?` unknown | ZOOM | - | `gameplay_hilltop`, `system_zoom_map`, `env_darkness`, `gameplay_lighthouse_1st` | - |
| Status display | screen | F3 / STATUS | attributes | name, level, sex, class, seven bars | - | "[Displaying status.]" | `inventory_status`, `inventory_ryz_status` | in the room window, replaces the description until the next move |
| Inventory | message | F2 / INVENTORY | possessions | items carried and worn, zorkmids | - | - | `inventory_list`, `inventory_cloak_worn` | - |
| Combat monitor | hud element | a monster appears | the fight at a glance | Endurance bar with percent | MONITOR toggles | "[Combat monitor off.]" | `battle_vapor_attack`, `options_monitor` | the bar stays after the fight (`gameplay_eyes`) |
| Standard mode | screen | MODE | plain display | status line EN ST DX IQ CM LK AC, exits | MODE again | "[Normal display mode.]" | `system_mode_standard` | - |
| SETTINGS | menu | `settings` | all display options in one place | Display Mode, Descriptions, Transcripting, Status Notify, Map View, Display Priority, Combat Monitor | arrows, Enter | - | `options_settings` | - |
| DEFINE | menu | `define` | function keys | F1-F10 texts, Restore Defaults, Exit | arrows, typing | - | `options_define_keys` | - |
| COLOR | message | `color` | palette | "[Color pallette N of 6.]" | - | - | `options_color_palette`, `options_color_4`, `options_color_5`, `options_color_6` | the game spells "pallette" |
| NOTIFY, PRIORITY | message | commands | options without the menu | bracketed confirmation | - | - | `options_notify`, `options_priority` | - |
| UNDO | message | F9 | take back a move | "[UNDO completed.]" | - | "[UNDO failed.]" when nothing to undo | `system_undo` | - |
| SAVE / RESTORE | prompt | `save` / `restore` | files | "You mumble the Spell of Saving. Enter save file name. (Default is data\\beyondzo.sav):" | file name | "[SAVE completed.]" | `save_prompt`, `save_done`, `save_restore` | - |
| Death screen | screen | Endurance 0, grue | end of a life | title bar "Death", "You are dead.", choices | RESTORE, RESTART, QUIT (and UNDO when allowed) | - | `gameover_ratant`, `gameover_grue` | UNDO is offered only for a death outside combat |
| Nymph messages | message | first use of some commands | interface hints | a nymph speaks and vanishes | - | - | `inventory_list`, `extra_technical_nymph` | - |
| Frotz 2.32 display | screen | the bundle's .bat | comparison | title picture, proportional font, red frames | - | - | `extra_frotz_title`, `extra_frotz_cove` | not Infocom's interpreter |

## 3. Screen flow
- DOSBox start menu -> BZORK.EXE -> colour question -> opening prompt (BEGIN / RESTORE / QUIT)
  - BEGIN -> prologue (2 pages) -> title card -> Character Setup
    - preset / select preset / random roll -> "Press any key to begin the story" -> Hilltop
    - create your own -> attributes -> YES -> sex -> name -> YES -> YES -> save character? -> any key -> Hilltop
  - RESTORE -> file name -> the saved room
- Play: main screen <-> STATUS / INVENTORY / SETTINGS / DEFINE / COLOR / MODE / ZOOM; SAVE / RESTORE / UNDO
- Death -> RESTORE / RESTART / QUIT (/ UNDO)

## 4. Elements in detail
Main play screen (enhanced mode, `gameplay_hilltop`): row 1 the title bar (room name; on STATUS the character's
name at the left and "Level N Sex Class" at the right, `inventory_status`); rows 2-11 the framed room window
(room description, or the status bars), with the Endurance bar of the combat monitor at its foot in a fight;
right of it the auto-map (about 12 columns); rows 13-25 the transcript, the latest answers and the `>`
prompt with a blinking block cursor. In standard mode (`system_mode_standard`) row 1 is a status line with
the room name, every attribute and the exits.

## Open questions
- Map View "Wide" and Display Priority "Inventory/Status" not looked at.
- Mouse on the map (manual) not tried.
