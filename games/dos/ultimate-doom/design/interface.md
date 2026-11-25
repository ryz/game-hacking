# The Ultimate Doom (DOS) - interface (UI/UX lens)

Every screen, menu, prompt and permanent element, how the player moves between them, and the conventions they
share. Systems behind the screens: [systems.md](systems.md); the variety of what appears on them:
[content.md](content.md). Notation: [README.md](README.md). Check: `python3 tools/lenses.py dos/ultimate-doom`.
Shot ids are from the `main` set unless marked `start`.

## 1. Conventions
- **Input:** keyboard only here (mouse and joystick supported by the game, not used). Arrows move, Ctrl fires,
  Space uses, Tab maps, Esc opens the menu, F1-F11 are shortcuts (help screen `help_keys`) **(verified)**.
- **Layout:** the 3D view fills the top 168 lines; the status bar fills the bottom 32 (ammo, health, weapon
  slots, face, armor, keys, ammo table) **(verified, every in-game shot)**.
- **Text:** red bitmap font for menus and messages; pickup and cheat messages appear on the top line and stay
  about 4 s **(verified, `pickup_armor`)**.
- **Feedback:** the view tints red when hit, gold when an item is picked up, green under the radiation suit,
  red under berserk, inverse grey under invulnerability **(verified, `face_88`, `pickup_megaarmor`,
  `power_radsuit`, `power_berserk`, `power_invuln`)**; the face reacts to damage and direction.
- **State visibility:** everything the player needs is always on the status bar; no inventory screen.
- **Help:** F1 opens a single help screen; Read This! in the menu shows the same kind of pages.
- **Menu cursor:** a blinking skull; Enter chooses, Esc goes back; menus open over the game and pause it.

## 2. Inventory of screens and elements

| Screen / element | Purpose | Shows | Accepts | Answers | Leads to | Shots |
|---|---|---|---|---|---|---|
| Start-up text | DOS start-up of DOOM.EXE | version, registered, memory checks | none | | title | start `01_startup` |
| Title picture | attract loop | the marine, logo, id Software | any key / Esc | menu | main menu, demos | `title_screen` |
| Main menu | top level | New Game, Options, Load Game, Save Game, Read This!, Quit Game | up/down, Enter, Esc | skull cursor | the sub-menus | `menu_main` |
| Episode menu | choose episode | the four episode names | up/down, Enter | | skill menu | `menu_episode` |
| Skill menu | choose difficulty | five skills, Hurt me plenty preselected | up/down, Enter | | first map | `menu_skill` |
| Options | settings | End Game, Messages, Graphic Detail, Screen Size, Mouse Sensitivity, Sound Volume | arrows, Enter | sliders | Sound Volume | start `28_options`, `29_sound` |
| Save Game | save | six slots, name entry | Enter, letters | "game saved." | play | start `31_save_menu`, `32_save_name`, `33_saved` |
| Help screen (F1) | keys | function keys, automap keys, weapons, movement | any key | | play | `help_keys` |
| 3D view | play | the world, the weapon in hand | movement, fire, use | | everything | `env_e1m1`, `env_e2m2` |
| Status bar | state | ammo, health %, weapon slots, face, armor %, keys, ammo table | none | numbers change at once | | `face_55`, `weapon_chaingun` |
| Face | health and damage at a glance | five bands, looks toward the attacker, grin on new weapon, dead face | none | | | `face_88`, `face_28`, `face_4`, `death_floor` |
| Message line | pickups, cheats, saves | one line top left | none | fades after about 4 s | | `pickup_armor`, `pickup_megaarmor` |
| Automap | navigation | lines of the explored map, the map name; computer map shows all; iddt shows things | Tab, F, M, C, +, -, 0 | | play | `automap_full`, `automap_things`, start `13_automap` |
| Screen melt | transition | the old screen melts down into the new one | none | | | start `06_melt` |
| Intermission tally | map result | Kills, Items, Secret percentages counting up, Time, Par | Space skips | count sound (off here) | Entering | `tally_e1m1`, start `24_tally` |
| Entering screen | next map | the episode map with the next base marked | Space | | next map | `entering_e1m2` |
| Episode end text | story | text typed over a flat | Space | | credits / picture | `ending_e1` |
| Credits | after episode 1 text | id Software team | any key | | title | `credits_id` |
| Death | failure | view on the floor, dead face, 0% | Space | | map restart | `death_floor`, `death_barons` |

## 3. Screen flow
Start-up text -> title -> (Esc) main menu -> New Game -> episode -> skill -> melt -> map -> exit -> tally ->
Entering -> next map ... map 8 -> tally -> end text -> credits (E1). Esc at any time opens the main menu over the
game; F1 the help screen; Tab toggles the automap **(verified, start set)**.

## 4. Main screens element by element
- **Status bar** (`weapon_chaingun`): AMMO (current weapon), HEALTH %, ARMS (owned slots 2-7 lit), the face,
  ARMOR %, three key slots, and the ammo table (current / maximum for bullets, shells, rockets, cells).
- **Face** (`face_88` ... `death_floor`): looks ahead at full health, gets bloodier per band, glances toward
  damage, turns to the dead face at 0. **Observation:** the strongest at-a-glance health cue of its time; the
  number lags the face by a frame or two (`face_4` shows 4% while health in memory was already 0).

## Open questions
- Read This! pages, the quit prompt and the Nightmare! confirmation are not shot yet.
