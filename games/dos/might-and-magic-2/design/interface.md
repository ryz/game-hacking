# Might and Magic II: Gates to Another World (DOS) - interface (UI/UX lens)

Every screen, menu, prompt and on-screen element of the game, described as an interface: what it is for, what
it shows, what it accepts, how it answers. Read it to study how the game talks to the player. The same shots
also appear in [systems.md](systems.md), which looks at the rules, and in [content.md](content.md), which shows
the variety of what fills the game; overlap is intended.
Notation: [README.md](README.md). Check: `python3 tools/lenses.py PLATFORM/SLUG`.

Facts carry a confidence tag as everywhere in this folder. A judgement (clear, slow, easy to miss) is written
as **Observation:** with the reason, never as a fact.

## 1. Conventions
- **Input:** keyboard only; every screen prints its keys; single keystrokes (letters, digits, arrows), Enter only
  after names and numbers; Esc goes back; Ctrl+letter for destructive or party actions (add/remove a member,
  rename, delete) **(verified)**. Keys typed early stay in the buffer and act on the next screen **(verified)**.
  A key the screen does not use does nothing (no beep seen) **(verified)**.
- **Layout:** 320x200 in 16 colours, red double frames. Play screen: 3-D view top left, command list
  (OPTIONS) or Protection panel top right, a status line (Protect/Options toggle, Day, Year, Face), and the party
  window at the bottom with names and hit points in two columns; the party window doubles as the message area
  **(verified)**. Full-screen text pages (profile, quick ref, view all) keep the frame and end with "('ESC' to go
  back)" **(verified)**.
- **Text:** one bold 8x8 font in mixed case; prompts end with "(y/n)?"; abbreviations on the profile (Lvl, Mgt,
  Int, Per, End, Spd, Acy, Lck, HP, SP, AC, SL, Exp) **(verified)**.
- **Feedback:** results appear as one line in the party window ("Nothing Here!", "Not Locked!"); story messages
  wait for Space ("('Space' to continue)") **(verified)**. Signs appear as a yellow signboard over the view
  **(verified)**.
- **State visibility:** always visible: party names and hit points, day, year, facing; light, magic and element
  resistance on the Protect panel; coordinates and map only on the Location screen **(verified)**.
- **Help and onboarding:** none in the game beyond the key lists; the manual explains rules, spells and skills
  **(verified / source)**.

## 2. Screen inventory
One row per screen, menu, prompt, dialog, message type and permanent on-screen element. Type: `screen`, `menu`,
`prompt`, `list`, `message`, `hud element`, `transition`.

| Screen / element | Type | Reached from -> leads to | Purpose | Shows | Accepts | Feedback and errors | Shots | Observation |
|---|---|---|---|---|---|---|---|---|
| Logo | transition | power-on -> title | publisher logo | "New World Computing Presents..." | - | - | boot_nwc_logo | - |
| Title picture | screen | logo -> opening options | title | animated pegasus scene | any key | - | title_screen | - |
| Opening options | menu | title -> Main Options, About, Copy, drive | start the game | four options | `s` `a` `c` `d` | - | menu_opening, menu_about, menu_copy | - |
| Main Options | menu | -> create, view all, transfer, go to town | roster management | four options | `c` `v` `t` `g` | - | menu_main | - |
| View All | list | Main Options -> profile | the roster A-X | name, class, level, town | letter, Space (hirelings), Esc | - | menu_view_all, menu_hirelings | - |
| Profile | screen | view all, inn, play -> action prompts | one character | statistics, HP, SP, AC, SL, age, experience, gold, gems, food, thievery, condition, 6 equipped, 6 backpack | Ctrl-N, Ctrl-D (menus); Q C D E G R S T U (play) | prompt on the bottom line | inventory_premade, inventory_profile_ryz | - |
| Create | screen | Main Options -> race, alignment, sex, name | roll a character | dice picture, seven statistics, eligible classes | Enter, letters, digits, name | the class list changes with each roll | create_* | **Observation:** the exchange option makes a wanted class reachable without many re-rolls |
| Transfer | prompt | Main Options | import Might and Magic 1 characters | path prompt with examples | text, Enter | - | menu_transfer | - |
| Inn list | list | go to town, sign-in -> play | form the party | characters of this town, ticks, counts C/H | Ctrl-letter, `1`-`5`, Space, `z`, Esc | "'Z' to exit" appears with the first tick | menu_inn_list, save_signed_in | - |
| Play screen | screen | inn exit, every area | exploring | view, OPTIONS, status line, party | arrows, command letters | one-line messages | gameplay_* | - |
| Protection panel | hud element | `p` on the play screen | active effects | Light (n), Magic %, Forces % | `o` back to options | - | system_protect | - |
| Quick Reference | screen | `q` | the party at a glance | HP, SP, level, SL, AC, age, gems, food, condition | Esc | - | inventory_quickref | - |
| Controls | menu | `c` | settings | sounds, walk beep, disposition, delay 0-9 | `1`-`4` | highlighted choice | options_controls | - |
| Location | screen | `m` | where am I | coordinates (map with a Cartographer) | Esc | - | system_location | - |
| Event message | message | stepping or turning onto a square | story, offers | text in the party window, picture in the view | `y`/`n`, Space | - | dialogue_*, system_* | - |
| Sign | message | square before a door | names a place | yellow signboard over the view | - | - | planned | - |
| Encounter | screen | a fight square or chance | choose to fight | monster picture, list of names (+n more), options line | `a` `b` `h` `r` | - | battle_encounter | - |
| Combat | screen | encounter `a` | fight round | picture, monster list with ticks (can melee), "Options for: name" | per-character letters | messages timed by the delay | battle_options_* | - |
| Spell Book | prompt | profile `c` | cast | 9 levels x 7 spells with ticks, "Cast Spell Level", "Number", "'Return' to cast" | digits, Enter | - | system_cast_spellbook | - |
| Innkeeper | prompt | inn square facing the desk | save | innkeeper picture, question | `y`/`n` | inn list after `y` | save_innkeeper | - |

## 3. Screen flow
Power-on -> logo -> title -> opening options -> Main Options -> (create / view all / transfer) -> go to town ->
inn list -> play screen. Play screen -> profile, quick ref, controls, protection, location, event messages,
encounter -> combat -> play screen. Inn square -> innkeeper -> inn list -> play screen or DOS **(verified)**.

## 4. The play screen, element by element
| Element | Where | Shows | Notes |
|---|---|---|---|
| 3-D view | top left, about 200x115 | three squares deep, walls, doors, torches, sky outdoors; monster or person picture during events | "Darkness" text when unlit **(verified)** |
| OPTIONS list | top right | the 13 exploration keys | replaced by the Protection panel with `p` **(verified)** |
| Status line | middle | 'P' Protect / 'O' Options toggle, Day, Year, Face | **(verified)** |
| Party window | bottom | number, name, hit points of up to 8 members in two columns; messages and prompts use the same box | current hit points are printed as "/14", not "14/14" **(verified)** |

## Open questions
- The shop screens (blacksmith lists, guild spell lists, temple menu, tavern menu) and the auto-map: not opened yet.
