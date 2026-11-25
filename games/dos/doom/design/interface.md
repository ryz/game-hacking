# Doom (DOS, registered 1.1) - interface (UI/UX lens)

Every screen, menu, prompt and element the player meets, the conventions they share and how they connect.
The rules behind them are in [systems.md](systems.md), the variety of content in [content.md](content.md); the
same shots appear there. Notation: [README.md](README.md). Check: `python3 tools/lenses.py dos/doom`.
Shot ids are from the `main` set unless marked `start`. What 1.1 shows differently from The Ultimate Doom 1.9
is marked **1.1**.

## 1. Conventions
- **Input:** keyboard only here. Arrows move, Ctrl fires, Space uses, Tab maps, Esc opens the menu, F1 the
  order page and then the help page, `=`/`-` resize the view (help page `help_keys`) **(verified)**.
- **Layout (1.1):** the game starts with a **reduced 3D window inside a green stone border** above the status
  bar (`view_reduced`, start `07_e1m1_start`); one `=` gives the full-width view over the status bar that 1.9
  uses by default (start `08_view_full`) **(verified)**. All other in-game shots use the full-width view.
- **Text:** red bitmap font for menus and messages; pickup and cheat messages on the top line for about 4 s
  **(verified, `pickup_armor`, `cheat_god`)**.
- **Feedback:** red tint when hit, gold on a pickup, green under the radiation suit, red under berserk,
  inverse grey under invulnerability **(verified, `face_40`, `pickup_megaarmor`, `power_radsuit`,
  `power_berserk`, `power_invuln`)**; the face reacts to damage.
- **Menu cursor:** a skull beside the entry; Enter chooses, Esc goes back; menus open over the game and pause
  it **(verified)**.
- **1.1 menu placement:** the episode and skill menus are drawn over the DOOM logo of the title picture, higher
  than in 1.9 (`menu_episode`, `menu_skill`) **(verified)**.

## 2. Inventory of screens and elements

| Screen / element | Purpose | Shows | Accepts | Answers | Leads to | Shots |
|---|---|---|---|---|---|---|
| Start-up text | DOS start-up of DOOM.EXE | "DOOM Operating System v1.1", commercial version, memory checks, anti-piracy line (**1.1**) | none | | title | start `01_startup` |
| Title picture | attract loop | the marine, logo, id Software 1993 | any key / Esc | menu | main menu, demos | `title_screen`, start `02_title` |
| Main menu | top level | New Game, Options, Load Game, Save Game, Read This!, Quit Game | up/down, Enter, Esc | skull cursor | sub-menus | `menu_main`, start `03_main_menu` |
| Episode menu | choose episode | **1.1:** three episodes (no Thy Flesh Consumed) | up/down, Enter | | skill menu | `menu_episode`, start `04_episode` |
| Skill menu | choose difficulty | **1.1:** four skills, no Nightmare!; Hurt me plenty preselected | up/down, Enter | skull moves | first map | `menu_skill`, `menu_skill_itytd`, `menu_skill_hntr`, `menu_skill_uv`, start `05_skill` |
| Read This! / F1 | order and help | **1.1:** page 1 the order page ("To order DOOM: call 1-800-IDGAMES ... $40.00"), Enter: page 2 the help page | Enter, Esc | | menu / play | `readthis_order`, `readthis_help`, start `26_help_order`, `27_help_keys` |
| Help page in play | keys | function keys, automap keys, weapons, movement | any key | | play | `help_keys` |
| Quit prompt | leave the game | a joke line ("don't leave yet -- there's a demon around that corner!"), press y | Y / other | | DOS or back | `quit_prompt` |
| Load Game | load | six slots | Enter | | play | `load_empty` |
| Save refused | save outside a game | "You can't save if you aren't playing! press a key." | any key | | menu | `save_refused` |
| Save Game | save | six slots, name entry, "game saved." | Enter, letters | message | play | start `28_slots`, `29_typing_name`, `30_saved` |
| Options | settings | End Game, Messages, Graphic Detail, Screen Size, Mouse Sensitivity, Sound Volume | arrows, Enter | sliders | Sound Volume | start `24_options`, `25_sound` |
| 3D view | play | the world, the weapon in hand | movement, fire, use | | everything | `env_e1m1`, `env_e2m1`, `view_reduced` |
| Status bar | state | ammo, health %, arms slots, face, armor %, keys, ammo table | none | numbers change at once | | `weapon_chaingun`, `cheat_idkfa` |
| Face | health at a glance | five bands, god face under iddqd, dead face | none | | | `face_100`, `face_67`, `face_25`, `face_7`, `death_floor`, `cheat_god` |
| Message line | pickups, cheats, saves | one line top left | none | fades | | `pickup_armor`, `pickup_megaarmor`, `cheat_idkfa` |
| Automap | navigation | explored lines and the map name; computer map: all lines; iddt: things | Tab | | play | `automap_full`, `automap_things`, start `13_automap` |
| Screen melt | transition | the old screen melts into the new one | none | | | start `06_melt` |
| Intermission tally | map result | Kills, Items, Secret counting up, Time, Par | Space skips | | Entering | start `20_tally`, `21_tally_done` |
| Entering screen | next map | the episode map with the next base marked | Space | | next map | start `22_entering` |
| Episode end text | story | text typed letter by letter over a flat (E1 grey stone, E2 flesh, E3 grey rock) | Space | | picture | `ending_e1`, `ending_e2`, `ending_e3` |
| End picture | after the end text | **1.1:** after E1 the order page ("Get all three episodes"; 1.9 shows the id credits); E2 Deimos above Hell; E3 Earth's fields with a rabbit, then scrolling to the fallen base | any key | | title | `ending_e1_order`, `ending_e2_deimos`, `ending_e3_bunny`, `ending_e3_scroll` |
| Death | failure | view on the floor, dead face, 0% | Space | | map restart | `death_floor` |

## 3. Screen flow
Start-up text -> title -> (Esc) main menu -> New Game -> episode -> skill -> melt -> map (reduced view) ->
exit -> tally -> Entering -> next map ... map 8 -> end text -> end picture (E1: order page). Esc opens the
menu over the game, F1 the order page then the help page, Tab the automap **(verified, start set)**.

## 4. Main screens element by element
- **Status bar** (`weapon_chaingun`): AMMO, HEALTH %, ARMS (owned slots 2-7 lit), the face, ARMOR %, three
  key slots and the ammo table (current / maximum) **(verified)**.
- **Face** (`face_100` ... `death_floor`): looks ahead at full health, bloodier per band, the dead face at 0
  **(verified)**.

## Open questions
- Whether the reduced view is a saved setting: 1.1 has no DEFAULT.CFG in this install, so the built-in default
  is used every start (inferred).
